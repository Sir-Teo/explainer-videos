"""Every number in Part 21 (Counterparty Risk, XVA and Clearing), computed and cached in .cache/quant21/.

    python -m videos.quant.quant21.compute [items] [--force]

* ``exposure``  exposure fans and profiles (EE, ENE, PFE) of a 10-year swap and of a netting set, under the Hull-White
                model fitted in Part 19 to the Fed's curve of 31 December 2025;
* ``collateral`` the same netting set with variation margin: thresholds and the margin period of risk;
* ``cva``       CVA and DVA of the netting set against a counterparty's CDS-implied hazard curve; first-to-default;
                how DVA grows as the bank's own credit worsens;
* ``wwr``       wrong-way risk: CVA against the correlation between default and the rate factor;
* ``fva``       FVA, KVA and MVA: funding, capital and initial-margin costs over the trades' lives;
* ``aad``       CVA sensitivities to every curve node and hazard by one backward pass in torch, against bumping, and
                the time each takes;
* ``deepxva``   a network trained on simulated cash flows learns the portfolio's future value; EE from the network
                against the exact Hull-White values (in the spirit of Gnoatto, Picarelli and Reisinger);
* ``im``        a SIMM-style initial margin from key-rate DV01s, and an initial-margin profile;
* ``procyc``    margin procyclicality: a 10-day 99% VaR margin on the 10-year Treasury yield, with a 1-year window
                and with EWMA, 2018-2025;
* ``saccr``     SA-CCR exposure at default for netting sets of swaps, with and without collateral;
* ``ccp``       a CCP's default waterfall under simulated member defaults (Cover 2);
* ``nickel``    the IMF's monthly nickel price, 2015-2025 (LME, March 2022).
"""

from __future__ import annotations

import json
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import credit as CR, termstructure as TS, xva as XV
from videos.quant.quant19.compute import _curve_2025, _hw_params

CACHE = Cache("quant21")
load = CACHE.load


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fy(d):
    d = np.asarray(d)
    return d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365


def _setup():
    c = _curve_2025()
    a, s, *_ = _hw_params()
    return c, TS.HullWhite(c, a, s), a, s


TIMES = np.round(np.linspace(1 / 12, 10, 120), 6)
CPTY_CDS = {"tenors": [1, 3, 5, 7, 10], "spreads_bp": [80, 110, 140, 160, 170]}  # an illustrative BBB counterparty
OWN_CDS = {"tenors": [1, 3, 5, 7, 10], "spreads_bp": [40, 55, 70, 80, 85]}      # an illustrative A-rated bank


def _par(c, T):
    pay = np.arange(1, int(T) + 1)
    return float((1 - c.df(float(T))) / c.df(pay).sum())


def _book(c):
    """A netting set: pay fixed on 10 years (100m), receive fixed on 5 years (60m), pay fixed on 3 years (40m), at
    par on 31 December 2025."""
    return [(_par(c, 10), 10.0, 100.0, True), (_par(c, 5), 5.0, 60.0, False), (_par(c, 3), 3.0, 40.0, True)]


def _values(hw, x, book, times=TIMES):
    V = np.zeros((x.shape[0], len(times)))
    per = []
    for K, T, N, payer in book:
        v = np.stack([XV.swap_values_hw(hw, x[:, j], t, K, T, notional=N, payer=payer) for j, t in enumerate(times)], 1)
        per.append(v)
        V += v
    return V, per


def compute_exposure() -> dict:
    c, hw, a, s = _setup()
    x, _ = hw.simulate_x(TIMES, 20000, seed=0)
    book = _book(c)
    V, per = _values(hw, x, book)
    single = XV.exposure_profile(per[0])
    net = XV.exposure_profile(V)
    gross = sum(XV.exposure_profile(p)["EE"] for p in per)
    fan = per[0][:60]
    q = np.quantile(per[0], [0.05, 0.5, 0.95], axis=0)
    return _json({"times": TIMES, "fan": fan, "q": q, "single": single, "net": net, "gross_EE": gross,
                  "book": [{"K": K, "T": T, "N": N, "payer": p} for K, T, N, p in book], "a": a, "sigma": s,
                  "netting_benefit": float(1 - net["EPE"] / np.mean(gross))})


def compute_collateral() -> dict:
    c, hw, a, s = _setup()
    x, _ = hw.simulate_x(TIMES, 20000, seed=0)
    V, _ = _values(hw, x, _book(c))
    out = {"none": XV.exposure_profile(V)}
    # monthly grid: a margin period of one step (about a month) is the coarsest the grid allows; also on a weekly
    # grid for the first year, to show the 10-day MPOR
    for name, th in (("threshold 2m", 2.0), ("threshold 0", 0.0)):
        out[name] = XV.exposure_profile(XV.collateralised(V, TIMES, threshold=th, mpor=1 / 12))
    tw = np.round(np.arange(1, 253) / 252 * 1.0, 6)
    xw, _ = hw.simulate_x(tw, 8000, seed=1)
    Vw, _ = _values(hw, xw, _book(c), tw)
    w0 = XV.exposure_profile(Vw)
    w10 = XV.exposure_profile(XV.collateralised(Vw, tw, threshold=0.0, mpor=10 / 252))
    return _json({"times": TIMES, "profiles": out, "weekly": {"t": tw, "none": w0["EE"], "mpor10": w10["EE"],
                                                              "ratio": float(w10["EPE"] / w0["EPE"])}})


def _hazards(q):
    def df(t):
        return np.exp(-0.04 * np.asarray(t, float))
    return CR.bootstrap_hazard(q["tenors"], np.array(q["spreads_bp"]) / 1e4, df, 0.4)


def compute_cva() -> dict:
    c, hw, a, s = _setup()
    e = load("exposure")
    EE, ENE = np.asarray(e["net"]["EE"]), np.asarray(e["net"]["ENE"])
    kc, hc = _hazards(CPTY_CDS)
    ko, ho = _hazards(OWN_CDS)
    df = c.df
    uni = XV.cva(EE, TIMES, df, kc, hc)
    bil = XV.cva(EE, TIMES, df, kc, hc, own=(ko, ho))
    d_ = XV.dva(ENE, TIMES, df, ko, ho, cpty=(kc, hc))
    # DVA as the bank's own spread widens: a parallel multiple of its CDS curve
    mult = [1, 2, 3, 4, 6]
    dvas = []
    for m_ in mult:
        k2, h2 = _hazards({"tenors": OWN_CDS["tenors"], "spreads_bp": list(np.array(OWN_CDS["spreads_bp"]) * m_)})
        dvas.append(XV.dva(ENE, TIMES, df, k2, h2, cpty=(kc, hc)))
    dQ = XV.default_density(TIMES, kc, hc)
    contrib = 0.6 * EE * df(TIMES) * dQ
    return _json({"cva": uni, "cva_bilateral": bil, "dva": d_, "bcva": bil - d_, "mult": mult, "dva_by_spread": dvas,
                  "contrib": contrib, "knots": kc, "hazards": hc, "own_hazards": ho, "times": TIMES,
                  "cva_bp_running": float(uni / sum(0.25 * c.df(np.arange(0.25, 10.01, 0.25))) / 100 * 1e4)})


def compute_wwr() -> dict:
    c, hw, a, s = _setup()
    x, _ = hw.simulate_x(TIMES, 20000, seed=0)
    V, _ = _values(hw, x, _book(c))
    kc, hc = _hazards(CPTY_CDS)
    lam = float(np.mean(hc))
    rhos = [-0.6, -0.3, 0.0, 0.3, 0.6, 0.9]
    out = [XV.wrong_way_cva(V, x, TIMES, c.df, lam, rho=r_, seed=5) for r_ in rhos]
    return _json({"rhos": rhos, "cva": out, "lam": lam})


def compute_fva() -> dict:
    c, hw, a, s = _setup()
    e = load("exposure")
    EE, ENE = np.asarray(e["net"]["EE"]), np.asarray(e["net"]["ENE"])
    kc, hc = _hazards(CPTY_CDS)
    surv = CR.survival(TIMES, kc, hc)
    f = XV.fva(EE, ENE, TIMES, c.df, 0.008, 0.008, survival=surv)
    # capital: SA-CCR-like EAD profile from the EE (alpha 1.4 x EEPE-style), 8% capital at 10% cost of capital
    cap = 1.4 * np.asarray(e["net"]["PFE"]) * 0.08 * 0.5
    kva = XV.capital_cost(cap, TIMES, c.df, 0.10)
    im = load("im")
    mva = XV.capital_cost(np.interp(TIMES, im["times"], im["profile"]), TIMES, c.df, 0.008)
    return _json({**f, "KVA": kva, "MVA": mva, "spread": 0.008, "capital_profile": cap})


def compute_aad() -> dict:
    c, hw, a, s = _setup()
    zt = np.array([0.5, 1, 2, 3, 5, 7, 10, 20, 30.0])
    zz = -np.log(c.df(zt)) / zt
    kc, hc = _hazards(CPTY_CDS)
    book = _book(c)
    tm = TIMES[::3]
    t0 = time.time()
    v, gz, gh = XV.cva_torch(zt, zz, kc, hc, a, s, book, tm, n_paths=8000, seed=1)
    t_aad = time.time() - t0
    bz, bh = [], []
    t0 = time.time()
    for i in range(len(zz)):
        up = zz.copy()
        up[i] += 1e-4
        bz.append((XV.cva_torch(zt, up, kc, hc, a, s, book, tm, n_paths=8000, seed=1)[0] - v) / 1e-4)
    for i in range(len(hc)):
        up = np.array(hc, float).copy()
        up[i] += 1e-4
        bh.append((XV.cva_torch(zt, zz, kc, up, a, s, book, tm, n_paths=8000, seed=1)[0] - v) / 1e-4)
    t_bump = time.time() - t0
    return _json({"cva": v, "zt": zt, "grad_zero": gz, "grad_hazard": gh, "bump_zero": bz, "bump_hazard": bh,
                  "hazard_t": kc, "t_aad": t_aad, "t_bump": t_bump, "n_inputs": len(zz) + len(hc)})


def compute_deepxva() -> dict:
    """Learn V(t_j, x) for the netting set from simulated cash flows alone (no pricing formula), one small network
    over (t, x), by regressing discounted future cash flows on the state; then EE from the network's values against
    EE from the exact Hull-White values on fresh paths."""
    import torch
    c, hw, a, s = _setup()
    book = _book(c)
    tm = TIMES[::4]
    x, D = hw.simulate_x(np.r_[tm, np.arange(tm[-1] + 1 / 12, 10.0001, 1 / 12)], 6000, seed=2)
    # cash flows of the book on annual fixed dates and annual floating resets (simplified: floating = realised simple
    # rate over each year, from the path's discount factors)
    grid = np.r_[tm, np.arange(tm[-1] + 1 / 12, 10.0001, 1 / 12)]
    Dt = D  # exp(-int_0^t r) at grid dates

    def disc_at(T):
        j = int(np.argmin(np.abs(grid - T)))
        return Dt[:, j]
    feats, targ = [], []
    for j, t in enumerate(tm):
        pv = np.zeros(x.shape[0])
        for K, T, N, payer in book:
            for k in range(1, int(T) + 1):
                if k <= t + 1e-12:
                    continue
                d1, d0 = disc_at(float(k)), disc_at(float(k - 1)) if k - 1 > 0 else np.ones(x.shape[0])
                L = (d0 / d1 - 1)  # realised annual simple rate, paid at k
                cf = N * (L - K) * (1 if payer else -1)
                pv += cf * d1
        tgt = pv / Dt[:, j]
        feats.append(np.c_[np.full(x.shape[0], t), x[:, j]])
        targ.append(tgt)
    Xf = torch.tensor(np.vstack(feats), dtype=torch.float32)
    yf = torch.tensor(np.concatenate(targ), dtype=torch.float32)[:, None]
    mu, sd = Xf.mean(0), Xf.std(0)
    ys = yf.std()
    torch.manual_seed(0)
    net = torch.nn.Sequential(torch.nn.Linear(2, 64), torch.nn.SiLU(), torch.nn.Linear(64, 64), torch.nn.SiLU(),
                              torch.nn.Linear(64, 1))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    losses = []
    for ep in range(1500):
        idx = torch.randint(0, len(Xf), (4096,))
        opt.zero_grad()
        loss = ((net((Xf[idx] - mu) / sd) - yf[idx] / ys) ** 2).mean()
        loss.backward()
        opt.step()
        if ep % 50 == 0:
            losses.append(float(loss))
    # fresh paths: exact values against the network's
    xe, _ = hw.simulate_x(tm, 20000, seed=9)
    Ve, _ = _values(hw, xe, book, tm)
    with torch.no_grad():
        Vn = np.stack([(net((torch.tensor(np.c_[np.full(len(xe), t), xe[:, j]], dtype=torch.float32) - mu) / sd)
                        * ys).numpy()[:, 0] for j, t in enumerate(tm)], 1)
    ee_e, ee_n = XV.exposure_profile(Ve)["EE"], XV.exposure_profile(Vn)["EE"]
    kc, hc = _hazards(CPTY_CDS)
    return _json({"times": tm, "EE_exact": ee_e, "EE_net": ee_n, "losses": losses,
                  "cva_exact": XV.cva(ee_e, tm, c.df, kc, hc), "cva_net": XV.cva(ee_n, tm, c.df, kc, hc),
                  "rmse": float(np.sqrt(np.mean((Ve - Vn) ** 2))), "scale": float(np.std(Ve))})


def compute_im() -> dict:
    c, hw, a, s = _setup()
    from explainer.quant.house import rates as R
    keys = XV.SIMM_TENORS
    book = _book(c)
    # key-rate DV01 of each swap today (per 1 bp, in millions on the book's notionals)
    out = np.zeros(len(keys))
    for K, T, N, payer in book:
        t = np.arange(1, int(T) + 1).astype(float)
        cf = np.full(len(t), -K * N if payer else K * N)
        cf[-1] += -N if payer else N
        kr = R.key_rate_dv01(t, cf, c, keys)
        # the floating leg's value is par: its rate risk sits at the first reset, ignored here
        out += kr
    im0 = XV.simm_like_ir_delta(out)
    # an IM profile: the book's DV01s shrink as the swaps run off; IM scales with the remaining DV01
    prof = []
    tt = np.arange(0, 10.01, 0.5)
    for t0 in tt:
        o = np.zeros(len(keys))
        for K, T, N, payer in book:
            if T - t0 <= 0:
                continue
            t = np.arange(np.ceil(t0 + 1e-9), int(T) + 1).astype(float) - t0
            if len(t) == 0:
                continue
            cf = np.full(len(t), -K * N if payer else K * N)
            cf[-1] += -N if payer else N
            o += R.key_rate_dv01(t, cf, c, keys)
        prof.append(XV.simm_like_ir_delta(o))
    return _json({"keys": keys, "dv01": out, "im": im0, "times": tt, "profile": prof})


def compute_procyc() -> dict:
    f = data.fred("DGS10", "2016-01-01", "2025-12-31")
    d, y = f["date"], f["value"]
    dy = np.diff(y) * 100  # bp
    dd = d[1:]
    win = 250
    dv01 = 0.085  # $ per bp per $100 of a 10-year note: about 8.5 bp of price per bp
    var_hist, var_ewma = [], []
    lam = 0.97
    v = np.var(dy[:win])
    for i in range(win, len(dy)):
        s10 = np.sqrt(10) * np.quantile(np.abs(dy[i - win:i]), 0.99)
        var_hist.append(s10 * dv01)
        v = lam * v + (1 - lam) * dy[i - 1] ** 2
        var_ewma.append(2.33 * np.sqrt(10 * v) * dv01)
    t = _fy(dd[win:])
    vh, ve = np.array(var_hist), np.array(var_ewma)
    k20 = (t > 2020.1) & (t < 2020.4)
    pre = (t > 2019.9) & (t < 2020.15)
    return _json({"t": t, "hist": vh, "ewma": ve, "pre": {"hist": float(vh[pre].mean()), "ewma": float(ve[pre].mean())},
                  "peak2020": {"hist": float(vh[k20].max()), "ewma": float(ve[k20].max())},
                  "max": {"t": float(t[np.argmax(ve)]), "ewma": float(ve.max())}})


def compute_saccr() -> dict:
    c, hw, a, s = _setup()
    book = _book(c)
    trades = [{"notional": N, "S": 0.0, "E": T, "delta": 1 if p else -1, "mtm": 0.0} for K, T, N, p in book]
    alone = [XV.sa_ccr_ir_ead([tr])["EAD"] for tr in trades]
    net = XV.sa_ccr_ir_ead(trades)
    # after rates fall 100 bp the payers are out of the money: MTM from the curve shift
    e = load("exposure")
    marg = XV.sa_ccr_ir_ead(trades, margined=True)
    return _json({"alone": alone, "sum_alone": float(sum(alone)), "net": net, "margined": marg,
                  "capital_8pct_rw100": float(net["EAD"] * 0.08)})


def compute_ccp() -> dict:
    """A CCP with 20 clearing members of unequal size. A defaulting member's portfolio loses IM x S in the close-out,
    S lognormal (usually below its margin, sometimes far above); defaults are correlated through one stress factor.
    The default fund is sized to Cover 2: the two largest members' losses beyond margin in an extreme but plausible
    close-out (S = 3). Each scenario's loss beyond the defaulters' margin runs down the waterfall."""
    from scipy.stats import norm
    rng = np.random.default_rng(0)
    n_m, n = 20, 400000
    im = np.sort(rng.lognormal(0.0, 0.9, n_m))[::-1]
    im = im / im.sum() * 100  # initial margin, total 100
    df_total = float(np.sum(im[:2] * (3.0 - 1.0)))
    contrib = df_total * im / im.sum()
    M = rng.standard_normal(n)
    dflt = (np.sqrt(0.5) * M[:, None] + np.sqrt(0.5) * rng.standard_normal((n, n_m))) < norm.ppf(0.005)
    S = np.exp(-0.2 + 0.5 * rng.standard_normal((n, n_m)) - 0.25 * np.minimum(M, 0)[:, None])  # worse in stress
    beyond = (dflt * np.maximum(im[None, :] * (S - 1), 0)).sum(1)
    own_df = (dflt * contrib[None, :]).sum(1)
    skin = 0.1 * df_total
    layers = XV.ccp_waterfall(beyond, 0.0, own_df, skin, df_total - own_df, df_total)
    any_d = dflt.any(1)
    hit = {k: float(np.mean(v[any_d] > 1e-9)) for k, v in layers.items() if k != "defaulter IM"}
    return _json({"im": im, "df_total": df_total, "skin": skin, "hit_given_default": hit,
                  "p_any_default": float(any_d.mean()), "p_two": float(np.mean(dflt.sum(1) >= 2)),
                  "q_beyond": np.quantile(beyond[any_d], [0.5, 0.99, 0.999]),
                  "worst": {k: float(v.max()) for k, v in layers.items()}})

def compute_nickel() -> dict:
    f = data.fred("PNICKUSDM", "2015-01-01", "2025-12-31")
    k = int(np.argmax(f["value"]))
    return _json({"t": _fy(f["date"]), "v": f["value"], "max": {"date": int(f["date"][k]), "v": float(f["value"][k])}})


ITEMS = {"exposure": compute_exposure, "collateral": compute_collateral, "cva": compute_cva, "wwr": compute_wwr,
         "im": compute_im, "fva": compute_fva, "aad": compute_aad, "deepxva": compute_deepxva,
         "procyc": compute_procyc, "saccr": compute_saccr, "ccp": compute_ccp, "nickel": compute_nickel}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
