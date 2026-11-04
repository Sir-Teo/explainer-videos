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
    # simulate on the exposure dates and on every payment date, so cash flows are discounted exactly on each path
    grid = np.unique(np.round(np.r_[tm, np.arange(1, 11)], 9))
    x_all, D = hw.simulate_x(grid, 8000, seed=2)
    pos = {round(float(g_), 9): i for i, g_ in enumerate(grid)}
    x = x_all[:, [pos[round(float(t), 9)] for t in tm]]
    Dt = D[:, [pos[round(float(t), 9)] for t in tm]]

    def disc_at(T):
        return D[:, pos[round(float(T), 9)]]
    feats, targ = [], []
    for j, t in enumerate(tm):
        pv = np.zeros(x.shape[0])
        for K, T, N, payer in book:
            for k in range(1, int(T) + 1):
                if k <= t + 1e-12:
                    continue
                d1 = disc_at(float(k))
                # the floating leg as the exact valuation treats it: the period under way resets today, so it accrues
                # from t; later periods accrue from their own start
                d0 = Dt[:, j] if k - 1 < t - 1e-12 else (disc_at(float(k - 1)) if k - 1 > 0 else np.ones(x.shape[0]))
                L = (d0 / d1 - 1)  # realised simple rate over the period, paid at k
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
    for ep in range(2500):
        idx = torch.randint(0, len(Xf), (4096,))
        opt.zero_grad()
        loss = ((net((Xf[idx] - mu) / sd) - yf[idx] / ys) ** 2).mean()
        loss.backward()
        opt.step()
        if ep % 50 == 0:
            losses.append(float(loss.detach()))
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



def compute_products() -> dict:
    """Expected exposure profiles of four product shapes on $100 million, from the same rate model where one is
    needed: an interest-rate swap (diffusion against run-off), an FX forward (diffusion only), a cross-currency swap
    (a final exchange of notionals: diffusion and an FX leg that keeps growing), and a bought option (exposure is its
    whole value, never negative)."""
    from scipy.stats import norm
    e = load("exposure")
    t = np.asarray(TIMES)
    s_fx = 0.10
    fx_fwd = 100 * s_fx * np.sqrt(t) * norm.pdf(0)  # EE of N(0, s sqrt t) x 100: s sqrt(t / 2 pi)
    xccy = np.asarray(e["single"]["EE"]) * 0.6 + 100 * s_fx * np.sqrt(t) * norm.pdf(0) * 0.8
    T = 10.0
    opt = np.array([100 * 0.2 * np.sqrt(T) * norm.pdf(0)] * len(t))  # ATM option value, flat in expectation
    eff = np.maximum.accumulate(np.asarray(e["net"]["EE"]))
    one = t <= 1.0 + 1e-9
    return _json({"times": t, "swap": e["single"]["EE"], "fx_forward": fx_fwd, "xccy": xccy, "option": opt,
                  "eff_EE": eff, "EEPE": float(np.mean(eff[one])), "EPE_1y": float(np.mean(np.asarray(e["net"]["EE"])[one]))})


def compute_calls() -> dict:
    """How the minimum transfer amount trades exposure against operational load: margin calls a year and EPE, on a
    daily grid over one year of the netting set."""
    c, hw, a, s = _setup()
    tw = np.round(np.arange(1, 253) / 252, 6)
    xw, _ = hw.simulate_x(tw, 4000, seed=3)
    Vw, _ = _values(hw, xw, _book(c), tw)
    out = []
    for mta in (0.0, 0.25, 0.5, 1.0, 2.0):
        C = np.zeros_like(Vw)
        held = np.zeros(Vw.shape[0])
        calls = np.zeros(Vw.shape[0])
        for j in range(Vw.shape[1]):
            need = Vw[:, j - 10] if j >= 10 else np.zeros(Vw.shape[0])  # what the 10-day-stale value calls for
            move = need - held
            do = np.abs(move) >= max(mta, 1e-12)
            held = np.where(do, need, held)
            calls += do
            C[:, j] = held
        out.append({"mta": mta, "calls": float(calls.mean()), "EPE": float(np.maximum(Vw - C, 0).mean())})
    return _json({"rows": out})


def compute_cvarisk() -> dict:
    """CVA as a position: its sensitivity to the counterparty's spread (CS01), the CDS notional that hedges it, and
    the incremental CVA of adding a new 5-year trade to the netting set, against its stand-alone CVA."""
    c, hw, a, s = _setup()
    x, _ = hw.simulate_x(TIMES, 20000, seed=0)
    book = _book(c)
    V, _ = _values(hw, x, book)
    EE = XV.exposure_profile(V)["EE"]

    def cva_at(mult, ee=EE):
        k, h = _hazards({"tenors": CPTY_CDS["tenors"], "spreads_bp": list(np.array(CPTY_CDS["spreads_bp"]) * mult)})
        return XV.cva(ee, TIMES, c.df, k, h)
    base = cva_at(1.0)
    mults = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    path = [cva_at(m_) for m_ in mults]
    # CS01: a parallel 1 bp in the counterparty's curve
    k1, h1 = _hazards({"tenors": CPTY_CDS["tenors"], "spreads_bp": list(np.array(CPTY_CDS["spreads_bp"]) + 1.0)})
    cs01 = XV.cva(EE, TIMES, c.df, k1, h1) - base
    k0, h0 = _hazards(CPTY_CDS)
    a5, _ = CR.cds_legs(5.0, k0, h0, lambda t: np.exp(-0.04 * np.asarray(t, float)))
    cds_cs01 = a5 * 1e-4  # per unit notional, per bp
    hedge = cs01 / cds_cs01
    # incremental CVA: a new 5-year receiver (offsets the 10-year payer) and a new 5-year payer (adds to it)
    out = {}
    for name, payer in (("receiver", False), ("payer", True)):
        K = _par(c, 5)
        vn = np.stack([XV.swap_values_hw(hw, x[:, j], t, K, 5.0, notional=50.0, payer=payer)
                       for j, t in enumerate(TIMES)], 1)
        alone = XV.cva(XV.exposure_profile(vn)["EE"], TIMES, c.df, k0, h0)
        withb = XV.cva(XV.exposure_profile(V + vn)["EE"], TIMES, c.df, k0, h0)
        out[name] = {"alone": alone, "incremental": withb - base}
    return _json({"base": base, "mults": mults, "path": path, "cs01": cs01, "cds_hedge_notional": hedge,
                  "incremental": out})


def compute_fvaasym() -> dict:
    """FVA with a funding spread to borrow above the spread earned when lending: the cost no longer cancels."""
    c, hw, a, s = _setup()
    e = load("exposure")
    EE, ENE = np.asarray(e["net"]["EE"]), np.asarray(e["net"]["ENE"])
    kc, hc = _hazards(CPTY_CDS)
    surv = CR.survival(TIMES, kc, hc)
    rows = []
    for b_, l_ in ((0.008, 0.008), (0.008, 0.002), (0.015, 0.002), (0.003, 0.003)):
        f = XV.fva(EE, ENE, TIMES, c.df, b_, l_, survival=surv)
        rows.append({"borrow": b_, "lend": l_, **f})
    return _json({"rows": rows})


def compute_imcva() -> dict:
    """Initial margin against CVA: two-way IM sized at the q-quantile of the 10-day move removes most of the
    exposure, and costs its funding instead. CVA and MVA as the IM quantile rises."""
    c, hw, a, s = _setup()
    tw = np.round(np.arange(1, 253 * 3) / 252, 6)
    tw = tw[tw <= 3.0]
    xw, _ = hw.simulate_x(tw, 3000, seed=4)
    Vw, _ = _values(hw, xw, _book(c), tw)
    kc, hc = _hazards(CPTY_CDS)
    d10 = Vw[:, 10:] - Vw[:, :-10]
    out = []
    for q in (0.0, 0.9, 0.95, 0.99, 0.999):
        im = np.quantile(np.abs(d10), q) if q > 0 else 0.0
        E = np.maximum(XV.collateralised(Vw, tw, threshold=0.0, mpor=10 / 252) - im, 0.0)
        ee = E.mean(0)
        cv = XV.cva(ee, tw, c.df, kc, hc)
        mva = XV.capital_cost(np.full(len(tw), im), tw, c.df, 0.008)
        out.append({"q": q, "im": float(im), "cva": cv, "mva": mva})
    return _json({"rows": out, "horizon": 3.0})


def compute_apc() -> dict:
    """Anti-procyclicality tools (as in EMIR): a 25% buffer released in stress, and a floor from a 10-year look-back,
    applied to the EWMA margin of chapter 9; how far each one cuts the jump of March 2020."""
    f = data.fred("DGS10", "2006-01-01", "2025-12-31")
    d, y = f["date"], f["value"]
    dy = np.diff(y) * 100
    dd = d[1:]
    dv01 = 0.085
    lam, v = 0.97, np.var(dy[:250])
    ew, fl = [], []
    for i in range(250, len(dy)):
        v = lam * v + (1 - lam) * dy[i - 1] ** 2
        ew.append(2.33 * np.sqrt(10 * v) * dv01)
        lo = max(0, i - 2520)
        fl.append(np.sqrt(10) * np.quantile(np.abs(dy[lo:i]), 0.99) * dv01)
    t = _fy(dd[250:])
    ew, fl = np.array(ew), np.array(fl)
    buffered = np.maximum(ew * 1.25, 0)
    # the buffer is released in stress: margin = max(ewma, 1.25 x ewma of calm times) -> use a 1.25 x one-year median
    calm = np.array([np.median(ew[max(0, i - 250):i + 1]) for i in range(len(ew))]) * 1.25
    buf = np.maximum(ew, calm)
    floor = np.maximum(ew, fl)
    sel = t >= 2017
    k = (t > 2020.1) & (t < 2020.4)
    pre = (t > 2019.9) & (t < 2020.15)

    def jump(z):
        return float(z[k].max() / z[pre].mean())
    return _json({"t": t[sel], "ewma": ew[sel], "buffer": buf[sel], "floor": floor[sel],
                  "jump": {"ewma": jump(ew), "buffer": jump(buf), "floor": jump(floor)},
                  "calm_level": {"ewma": float(ew[pre].mean()), "buffer": float(buf[pre].mean()),
                                 "floor": float(floor[pre].mean())}})


def compute_modelrisk() -> dict:
    """The same netting set's EE and CVA under Hull-White with other mean reversions, each re-fitted to the same
    10-year yield volatility (sigma scaled so the 10-year zero's volatility matches): exposure is a model output."""
    c = _curve_2025()
    a0, s0, *_ = _hw_params()
    kc, hc = _hazards(CPTY_CDS)

    def vol10(a, s):
        return s * (1 - np.exp(-a * 10)) / (a * 10)
    out = []
    for a in (0.0087, 0.03, 0.06, 0.1, 0.2):
        s = s0 * vol10(a0, s0) / vol10(a, s0) if a != a0 else s0
        hw = TS.HullWhite(c, a, s)
        x, _ = hw.simulate_x(TIMES, 10000, seed=0)
        V, _ = _values(hw, x, _book(c))
        ee = XV.exposure_profile(V)["EE"]
        out.append({"a": a, "sigma": float(s), "EE": ee, "cva": XV.cva(ee, TIMES, c.df, kc, hc)})
    return _json({"rows": out, "times": TIMES})


def compute_convergence() -> dict:
    """CVA's Monte Carlo error: twenty independent runs at each path count."""
    c, hw, a, s = _setup()
    kc, hc = _hazards(CPTY_CDS)
    book = _book(c)
    tm = TIMES[::2]
    out = []
    for n in (250, 1000, 4000, 16000):
        vals = []
        for r_ in range(20):
            x, _ = hw.simulate_x(tm, n, seed=100 + r_)
            V, _ = _values(hw, x, book, tm)
            vals.append(XV.cva(XV.exposure_profile(V)["EE"], tm, c.df, kc, hc))
        out.append({"n": n, "mean": float(np.mean(vals)), "sd": float(np.std(vals))})
    return _json({"rows": out})


def compute_wwrhw() -> dict:
    """Hull and White's (2012) wrong-way model: the counterparty's hazard rate depends on the netting set's value,
    lambda_i(t) = exp(a(t) + b V_i(t)), with a(t) re-fitted at each date so the average survival still matches the
    CDS curve. CVA as b varies (b > 0: default likelier when the bank is owed more)."""
    from scipy.optimize import brentq
    c, hw, a, s = _setup()
    x, _ = hw.simulate_x(TIMES, 20000, seed=0)
    V, _ = _values(hw, x, _book(c))
    kc, hc = _hazards(CPTY_CDS)
    Q = CR.survival(TIMES, kc, hc)
    dt = np.diff(np.r_[0.0, TIMES])
    P = c.df(TIMES)
    out = []
    for b in (-0.1, -0.05, 0.0, 0.05, 0.1, 0.2):
        Sprev = np.ones(V.shape[0])
        cva = 0.0
        for j in range(len(TIMES)):
            def gap(aj):
                return float(np.mean(Sprev * np.exp(-np.exp(aj + b * V[:, j]) * dt[j]))) - Q[j]
            aj = brentq(gap, -30.0, 5.0)
            S = Sprev * np.exp(-np.exp(aj + b * V[:, j]) * dt[j])
            cva += 0.6 * P[j] * float(np.mean(np.maximum(V[:, j], 0.0) * (Sprev - S)))
            Sprev = S
        out.append({"b": b, "cva": cva})
    return _json({"rows": out})

def compute_haircut() -> dict:
    """Non-cash collateral: the counterparty posts 10-year Treasuries instead of cash. Over the margin period the
    bonds lose value exactly when rates rise, which is when this pay-fixed netting set's exposure grows. Exposure
    with cash, with bonds at no haircut, and with Basel's 4% supervisory haircut for long sovereigns. Daily grid,
    first year, zero threshold, 10-day margin period."""
    c, hw, a, s = _setup()
    tw = np.round(np.arange(1, 253) / 252, 6)
    xw, _ = hw.simulate_x(tw, 8000, seed=1)
    Vw, _ = _values(hw, xw, _book(c), tw)
    lag = np.searchsorted(tw, tw - 10 / 252 + 1e-12, side="right") - 1
    ok = lag >= 0
    Vl = np.where(ok[None, :], Vw[:, np.clip(lag, 0, None)], 0.0)
    xl = np.where(ok[None, :], xw[:, np.clip(lag, 0, None)], 0.0)
    C = Vl  # zero threshold, two-way
    B10 = (1 - np.exp(-a * 10)) / a
    dy = B10 / 10 * (xw - xl)          # change in the 10-year zero yield over the margin period
    dur = 8.5
    out = {}
    for name, h_ in (("cash", None), ("bonds, no haircut", 0.0), ("bonds, 4% haircut", 0.04)):
        if h_ is None:
            held = C
        else:
            # the poster delivers C/(1-h) of bonds at the call date; only collateral received is haircut
            # (collateral the bank has posted is left as a cash-like claim: only what it receives is in bonds)
            held = np.where(C > 0, C / (1 - h_) * (1 - dur * dy), C)
        E = np.maximum(Vw - held, 0.0)
        out[name] = {"EE": E.mean(0), "EPE": float(E.mean())}
    corr = float(np.corrcoef((Vw - Vl)[:, 20:].ravel(), -dy[:, 20:].ravel())[0, 1])
    return _json({"t": tw, "profiles": out, "corr": corr, "duration": dur})

def compute_lsmexpo() -> dict:
    """The industry's standard for the same problem: at each exposure date, regress the realised discounted cash
    flows on polynomials of the state (Part 16's Longstaff-Schwartz regression, used for exposure), on the same
    training paths and targets as chapter 7's network; then EE and CVA on fresh paths. Also the count of basis
    functions a full cubic needs as the number of risk factors grows."""
    c, hw, a, s = _setup()
    book = _book(c)
    tm = TIMES[::4]
    grid = np.unique(np.round(np.r_[tm, np.arange(1, 11)], 9))
    x_all, D = hw.simulate_x(grid, 8000, seed=2)
    pos = {round(float(g_), 9): i for i, g_ in enumerate(grid)}
    x = x_all[:, [pos[round(float(t), 9)] for t in tm]]
    Dt = D[:, [pos[round(float(t), 9)] for t in tm]]

    def disc_at(T):
        return D[:, pos[round(float(T), 9)]]
    xe, _ = hw.simulate_x(tm, 20000, seed=9)
    Ve, _ = _values(hw, xe, book, tm)
    out = {}
    for deg in (1, 3):
        Vr = np.zeros_like(Ve)
        for j, t in enumerate(tm):
            pv = np.zeros(x.shape[0])
            for K, T, N, payer in book:
                for k in range(1, int(T) + 1):
                    if k <= t + 1e-12:
                        continue
                    d1 = disc_at(float(k))
                    d0 = Dt[:, j] if k - 1 < t - 1e-12 else (disc_at(float(k - 1)) if k - 1 > 0 else np.ones(x.shape[0]))
                    pv += N * ((d0 / d1 - 1) - K) * (1 if payer else -1) * d1
            tgt = pv / Dt[:, j]
            sc = x[:, j].std() + 1e-12
            B = np.vander(x[:, j] / sc, deg + 1)
            beta, *_ = np.linalg.lstsq(B, tgt, rcond=None)
            Vr[:, j] = np.vander(xe[:, j] / sc, deg + 1) @ beta
        ee_r = XV.exposure_profile(Vr)["EE"]
        kc, hc = _hazards(CPTY_CDS)
        out[f"deg{deg}"] = {"EE": ee_r, "cva": XV.cva(ee_r, tm, c.df, kc, hc),
                            "rmse": float(np.sqrt(np.mean((Ve - Vr) ** 2)))}
    from math import comb
    nbasis = {d: comb(d + 3, 3) for d in (1, 2, 5, 10, 20, 50)}
    ee_e = XV.exposure_profile(Ve)["EE"]
    kc, hc = _hazards(CPTY_CDS)
    return _json({"times": tm, "EE_exact": ee_e, "cva_exact": XV.cva(ee_e, tm, c.df, kc, hc), **out,
                  "nbasis_cubic": nbasis})

def compute_imbacktest() -> dict:
    """Backtesting a margin model: how often did the 10-day move in the 10-year yield exceed the EWMA margin set ten
    days before, 2017-2025? A 99% model should be exceeded about 1% of the time (Kupiec's likelihood-ratio test)."""
    from scipy.stats import chi2
    f = data.fred("DGS10", "2016-01-01", "2025-12-31")
    y = f["value"]
    dy = np.diff(y) * 100
    lam, v = 0.97, np.var(dy[:250])
    exc, n = 0, 0
    flags = []
    for i in range(250, len(dy) - 10):
        v = lam * v + (1 - lam) * dy[i - 1] ** 2
        lim = 2.576 * np.sqrt(10 * v)  # two-sided 99%: either direction of move is a loss to one side
        move = abs(y[i + 10] - y[i]) * 100
        hit = move > lim
        flags.append(hit)
        exc += hit
        n += 1
    p_hat = exc / n
    p = 0.01
    lr = -2 * (np.log((1 - p) ** (n - exc) * p ** exc) - np.log((1 - p_hat) ** (n - exc) * max(p_hat, 1e-12) ** exc))
    t = _fy(f["date"][1:][250:len(dy) - 10])
    fl = np.array(flags)
    by_year = {int(yr): float(fl[t.astype(int) == yr].mean()) for yr in range(2017, 2026)}
    return _json({"rate": p_hat, "n": n, "exceptions": int(exc), "lr": float(lr), "pval": float(1 - chi2.cdf(lr, 1)),
                  "by_year": by_year})

ITEMS = {"exposure": compute_exposure, "collateral": compute_collateral, "cva": compute_cva, "wwr": compute_wwr,
         "im": compute_im, "fva": compute_fva, "aad": compute_aad, "deepxva": compute_deepxva,
         "procyc": compute_procyc, "saccr": compute_saccr, "ccp": compute_ccp, "nickel": compute_nickel,
         "products": compute_products, "calls": compute_calls, "cvarisk": compute_cvarisk, "fvaasym": compute_fvaasym,
         "imcva": compute_imcva, "apc": compute_apc, "modelrisk": compute_modelrisk, "convergence": compute_convergence,
         "imbacktest": compute_imbacktest, "wwrhw": compute_wwrhw, "haircut": compute_haircut, "lsmexpo": compute_lsmexpo}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
