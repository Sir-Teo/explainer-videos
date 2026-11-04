"""Every number in Part 19 (Term-Structure Models), computed and cached in .cache/quant19/.

    python -m videos.quant.quant19.compute [items] [--force]

* ``shortrate``  Vasicek and CIR fitted by maximum likelihood to the 3-month bill (monthly, 1990-2025); simulated
                 fans; the curves each model can draw from different short rates;
* ``hw``         Hull-White fitted exactly to the Treasury curve of 31 December 2025, its volatility term structure
                 calibrated to the daily moves of the Fed's curve in 2023-2025; caplets, caps and swaptions, quoted in
                 normal and lognormal volatility; a fan of short rates;
* ``hjm``        Gaussian HJM with Part 18's three factors as volatilities: five years of forward curves from today's,
                 and the drift condition checked by the martingale test;
* ``lmm``        a forward-rate market model: caplets by simulation against Black and Bachelier;
* ``bermudan``   a 10-non-call-1 Bermudan receiver swaption under Hull-White by Longstaff-Schwartz: its price, its
                 Europeans and its exercise boundary;
* ``negative``   negative rates: the ECB's deposit rate 1999-2025, and what Black and Bachelier do near zero;
* ``sabr``       normal SABR smiles: what each parameter does (illustrative parameters);
* ``multicurve`` the LIBOR-bill (TED) spread 1986-2022, and a swap valued on one curve and on two;
* ``premia``     Cochrane and Piazzesi's tent on the Fed's curve, fitted to 1964-2003 and tested afterwards, against a
                 small network on the same inputs (both registered before the hold-out);
* ``mbs``        the 30-year mortgage rate since 1971; a stylized prepayment curve and a pass-through's negative
                 convexity against a Treasury;
* ``y1994``      1994: the Fed's hikes, the curve's rise, and a leveraged pool like Orange County's;
* ``envelope``   the trial counter after this part's registrations.
"""

from __future__ import annotations

import inspect
import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, rates as R, sim, termstructure as TS

CACHE = Cache("quant19")
load = pit.counted(CACHE.load, 19, items=("premia",))


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fy(d):
    d = np.asarray(d)
    return d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365


def _curve_2025():
    """The Fed's fitted (Svensson) curve of 31 December 2025, on a fine grid: smooth forwards, as Hull-White's drift
    and every forward-rate model need (Part 18's bootstrap has step forwards)."""
    g = data.gsw("2025-12-01", "2025-12-31")
    i = int(np.searchsorted(g["date"], 20251231, side="right") - 1)
    b, t = g["beta"][i].copy(), g["tau"][i].copy()
    if np.isnan(t[1]) or np.isnan(b[3]):
        b[3], t[1] = 0.0, 1.0
    s = np.arange(0.05, 40.001, 0.05)
    return R.Curve(s, R.nss(s, b, t) / 100)


# ---------------------------------------------------------------------------
def compute_shortrate() -> dict:
    f = data.fred("DTB3", "1990-01-01", "2025-12-31")
    d, v = f["date"], f["value"] / 100
    m = d // 100
    last = np.r_[m[1:] != m[:-1], True]
    dm, x = d[last], np.clip(v[last], 1e-4, None)
    dt = 1 / 12
    cir = sim.cir_mle(x, dt, (0.3, 0.03, 0.08), maxiter=900)
    # Vasicek by exact AR(1): x_{t+1} = b + (x_t - b) e^{-a dt} + eps
    X = np.c_[np.ones(len(x) - 1), x[:-1]]
    c, *_ = np.linalg.lstsq(X, x[1:], rcond=None)
    phi = c[1]
    a = -np.log(phi) / dt
    b = c[0] / (1 - phi)
    res = x[1:] - X @ c
    s = np.sqrt(res.var() * 2 * a / (1 - phi ** 2))
    vas = {"a": float(a), "b": float(b), "sigma": float(s)}
    # fans from today's bill rate, 10 years monthly
    r0 = float(x[-1])
    n, paths = 120, 300
    rng = np.random.default_rng(0)
    vp = np.zeros((paths, n + 1))
    vp[:, 0] = r0
    for k in range(n):
        vp[:, k + 1] = b + (vp[:, k] - b) * phi + np.sqrt(res.var()) * rng.standard_normal(paths)
    cp = sim.cir_exact(r0, cir["kappa"], cir["theta"], cir["sigma"], 10.0, n, paths, seed=0)
    T = np.linspace(0.25, 30, 120)
    shapes = {}
    for r_ in (0.005, 0.03, 0.08):
        shapes[f"{r_:.3f}"] = {"vas": -np.log(TS.vasicek_zcb(r_, a, b, s, T)) / T,
                               "cir": -np.log(TS.cir_zcb(r_, cir["kappa"], cir["theta"], cir["sigma"], T)) / T}
    neg_share = float(np.mean(vp[:, -1] < 0))
    return _json({"t": _fy(dm), "x": x, "cir": {k: cir[k] for k in ("kappa", "theta", "sigma", "loglik", "feller")},
                  "vas": vas, "r0": r0, "vas_paths": vp[:60], "cir_paths": cp[:60], "vas_neg_share": neg_share,
                  "vas_neg_ever": float(np.mean((vp < 0).any(1))), "T": T, "shapes": shapes,
                  "half_life_vas": float(np.log(2) / a), "half_life_cir": float(np.log(2) / cir["kappa"])})


def _hw_params():
    """Hull-White's a and sigma from the term structure of the daily volatility of zero yields, 2023-2025: in the
    model the n-year zero yield moves by sigma B(n) / n per unit of the short rate's shock."""
    from scipy.optimize import least_squares
    g = data.gsw("2023-01-01", "2025-12-31")
    mats = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30])
    Y = g["y"][:, mats - 1] / 100
    ok = ~np.isnan(Y).any(1)
    vol = np.diff(Y[ok], axis=0).std(0) * np.sqrt(252)

    def res(p):
        a, s = np.exp(p)
        return s * (1 - np.exp(-a * mats)) / (a * mats) - vol
    sol = least_squares(res, np.log([0.05, 0.01]))
    a, s = np.exp(sol.x)
    return float(a), float(s), mats, vol, s * (1 - np.exp(-a * mats)) / (a * mats)


def compute_hw() -> dict:
    c = _curve_2025()
    a, s, mats, vol, fitv = _hw_params()
    hw = TS.HullWhite(c, a, s)
    t = np.linspace(0.05, 30, 200)
    phi = hw.phi(t)
    times = np.linspace(0, 10, 121)[1:]
    x, D = hw.simulate_x(times, 20000, seed=0)
    r = x + hw.phi(times)[None, :]
    reprice = np.abs(D.mean(0) / c.df(times) - 1).max()
    # caplets on 3-month SOFR-style rates, 2 years out, across strikes; quoted in normal and Black vol
    T, dlt = 2.0, 0.25
    P1, P2 = c.df(T), c.df(T + dlt)
    F = (P1 / P2 - 1) / dlt
    Ks = F + np.linspace(-0.02, 0.02, 21)
    Ks = Ks[Ks > 0.002]
    prices = np.array([hw.caplet(k, T, dlt) for k in Ks])
    ann = dlt * P2
    nv = np.array([TS.normal_iv(p / ann, F, k, T) for p, k in zip(prices, Ks)])
    from explainer.quant.house import bs
    lv = []
    for p, k in zip(prices, Ks):
        from scipy.optimize import brentq
        lv.append(brentq(lambda sg: TS.black_swaption(F, k, T, sg, ann) - p, 1e-4, 5.0))
    del bs
    # swaption grid (ATM payer, normal vol)
    grid = {}
    for Tx in (1, 2, 5, 10):
        for ten in (2, 5, 10):
            times_ = Tx + np.arange(1, ten + 1)
            A = c.df(times_).sum()
            Fsw = (c.df(Tx) - c.df(times_[-1])) / A
            pr = hw.swaption(Fsw, Tx, ten, payer=True)
            grid[f"{Tx}x{ten}"] = {"F": float(Fsw), "price": float(pr), "nvol": TS.normal_iv(pr / A, Fsw, Fsw, Tx)}
    cap5 = hw.cap(F, 5.0, 0.25)
    return _json({"a": a, "sigma": s, "mats": mats, "vol": vol, "fitvol": fitv, "t": t, "phi": phi, "f0": c.inst_fwd(t),
                  "times": times, "r_paths": r[:80], "r_q": np.percentile(r, [5, 25, 50, 75, 95], axis=0),
                  "reprice_max_rel": float(reprice), "caplet": {"T": T, "F": F, "K": Ks, "price": prices, "nvol": nv,
                                                                  "lvol": np.array(lv)},
                  "swaptions": grid, "cap5": cap5, "neg_share_10y": float(np.mean(r[:, -1] < 0))})


def compute_hjm() -> dict:
    from videos.quant.quant18.compute import load as load18
    p = load18("pca")
    c = _curve_2025()
    tau = np.linspace(0, 30, 121)
    f0 = c.inst_fwd(np.maximum(tau, 0.02))
    mats = np.asarray(p["mats"], float)
    L = np.asarray(p["loadings"])
    sd = np.asarray(p["sd_bp"]) * 1e-4 * np.sqrt(252)  # annual
    # factor vols for yields at mats -> forward-rate vols: interpolate yield loadings, then f = d(y tau)/dtau
    vols = []
    for k in range(3):
        yv = np.interp(tau, mats, L[k] * sd[k], left=L[k][0] * sd[k])
        fv = np.gradient(yv * tau, tau)
        vols.append(fv)
    vols = np.array(vols)
    out = TS.hjm_gaussian(f0, tau, vols, T=5.0, n_steps=500, n_paths=4000, seed=0)
    curves = out["curves"]
    snaps = [0, 100, 200, 300, 400, 500]
    sample = curves[::25, :6]  # time x paths x tau
    # martingale check: P(5, 5 + m) / bank against P(0, 5 + m)
    chk = []
    for m in (1, 5, 10, 20):
        k = int(np.searchsorted(tau, m))
        PT = np.exp(-np.trapezoid(curves[-1][:, :k + 1], tau[:k + 1], axis=1))
        k0 = int(np.searchsorted(tau, 5 + m))
        P0 = np.exp(-np.trapezoid(f0[:k0 + 1], tau[:k0 + 1]))
        chk.append({"m": m, "ratio": float(np.mean(PT / out["bank"]) / P0)})
    drift = (vols * np.cumsum(vols * np.diff(tau, prepend=0)[None, :], axis=1)).sum(0)
    return _json({"tau": tau, "f0": f0, "vols": vols, "drift": drift, "paths": sample, "snaps": snaps,
                  "mean_T": curves[-1].mean(0), "q_T": np.percentile(curves[-1], [5, 50, 95], axis=0),
                  "check": chk, "share": p["share"][:3]})


def compute_lmm() -> dict:
    c = _curve_2025()
    dlt = 0.5
    T = np.arange(1, 11) * dlt
    L0 = (c.df(T - dlt) / c.df(T) - 1) / dlt
    lo = TS.lmm_caplets(L0, dlt, 0.25, n_paths=40000, seed=0)
    no = TS.lmm_caplets(L0, dlt, 0.009, n_paths=40000, seed=0, normal=True)
    return _json({"T": T, "L0": L0, "black": lo, "normal": no})


def compute_bermudan() -> dict:
    c = _curve_2025()
    a, s, *_ = _hw_params()
    hw = TS.HullWhite(c, a, s)
    T0, Tend = 1.0, 10.0
    times = T0 + np.arange(1, 10)
    K = float((c.df(T0) - c.df(Tend)) / c.df(times).sum())
    out = TS.bermudan_swaption_lsm(hw, K, T0, Tend, freq=1, payer=False, n_paths=60000, seed=0)
    out2 = TS.bermudan_swaption_lsm(hw, K, T0, Tend, freq=1, payer=False, n_paths=60000, seed=1)
    return _json({"K": K, "a": a, "sigma": s, **out, "seed1": out2["price"], "se1": out2["se"]})


def compute_negative() -> dict:
    d, v = (lambda f: (f["date"], f["value"]))(data.fred("ECBDFR", "1999-01-01", "2025-12-31"))
    neg = v < 0
    first_neg = int(d[np.argmax(neg)])
    last_neg = int(d[np.where(neg)[0][-1]])
    T, K = 1.0, 0.0
    Fs = np.linspace(-0.01, 0.02, 61)
    bach = TS.bachelier(Fs, K, T, 0.006)
    black = np.array([TS.black_swaption(F, max(K, 1e-6), T, 0.6) if F > 0 else np.nan for F in Fs])
    return _json({"t": _fy(d), "dfr": v, "first_neg": first_neg, "last_neg": last_neg, "min": float(v.min()),
                  "F": Fs, "bach": bach, "black": black})


def compute_sabr() -> dict:
    F, T = 0.035, 2.0
    K = np.linspace(0.005, 0.065, 61)
    base = {"alpha": 0.009, "beta": 0.0, "rho": -0.2, "nu": 0.35}
    out = {"K": K, "base": TS.sabr_normal_iv(F, K, T, **base)}
    for name, vals in (("alpha", (0.006, 0.012)), ("rho", (-0.6, 0.3)), ("nu", (0.1, 0.7))):
        out[name] = [TS.sabr_normal_iv(F, K, T, **{**base, name: v_}) for v_ in vals]
        out[name + "_vals"] = vals
    return _json({**out, "F": F, "T": T, "params": base})


def compute_multicurve() -> dict:
    d, v = (lambda f: (f["date"], f["value"]))(data.fred("TEDRATE", "1986-01-01", "2022-01-21"))
    k = int(np.argmax(v))
    pre = v[(d >= 20000101) & (d < 20070801)].mean()
    # a 5-year swap paying 3-month LIBOR = OIS + basis, valued on one curve and on two
    c = _curve_2025()
    basis = 0.0025
    t = np.arange(0.25, 5.0001, 0.25)
    ois = c.df(t)
    fwd_ois = (np.r_[1.0, ois[:-1]] / ois - 1) / 0.25
    fwd_lib = fwd_ois + basis
    fixed_two = float(np.sum(fwd_lib * 0.25 * ois) / np.sum(0.25 * ois))
    one = R.Curve(c.t, c.z + basis)  # discount on the LIBOR curve too
    o1 = one.df(t)
    fixed_one = float((1 - o1[-1]) / np.sum(0.25 * o1))
    return _json({"t": _fy(d), "ted": v, "peak": {"date": int(d[k]), "pct": float(v[k])}, "pre2007": float(pre),
                  "fixed_two": fixed_two, "fixed_one": fixed_one, "basis": basis})


# ---------------------------------------------------------------------------
# Bond risk premia: Cochrane-Piazzesi and a small network, registered before the hold-out
# ---------------------------------------------------------------------------
PREMIA_RULE = {"target": "average 1-year excess log return of 2-5 year zeros (GSW)", "fit": "1964-2003 monthly",
               "validation": "2004-2020", "holdout": "2021-2025 (sealed)", "models": ["CP tent: OLS on y1 and four "
               "forwards", "MLP 5-16-1 on the same five inputs, 3 seeds averaged, early stopping on 1994-2003"]}


def _premia_data():
    g = data.gsw("1963-01-01", "2025-12-31")
    m = g["date"] // 100
    idx = np.where(np.r_[m[1:] != m[:-1], True])[0]
    n = np.arange(1, 6)
    lp = []
    for i in idx:
        b, t = g["beta"][i].copy(), g["tau"][i].copy()
        if np.isnan(t[1]) or np.isnan(b[3]):
            b[3], t[1] = 0.0, 1.0
        lp.append(-R.nss(n.astype(float), b, t) / 100 * n)
    return g["date"][idx], np.array(lp)


def _premia_models(d, lp):
    cp = TS.cochrane_piazzesi(lp)
    X, rx = cp["fwd"][:-12], cp["rx"].mean(1)
    dd = d[:-12]
    tr = (dd >= 19640101) & (dd < 20040101)
    Xt = np.c_[np.ones(tr.sum()), X[tr]]
    gam = np.linalg.lstsq(Xt, rx[tr], rcond=None)[0]
    pred_cp = np.c_[np.ones(len(X)), X] @ gam
    import torch
    preds = []
    mu, sdv = X[tr].mean(0), X[tr].std(0)
    Z = (X - mu) / sdv
    es = (dd >= 19940101) & (dd < 20040101)
    fit = tr & ~es
    for seed in range(3):
        torch.manual_seed(seed)
        net = torch.nn.Sequential(torch.nn.Linear(5, 16), torch.nn.Tanh(), torch.nn.Linear(16, 1))
        opt = torch.optim.Adam(net.parameters(), lr=1e-2, weight_decay=1e-4)
        xt = torch.tensor(Z[fit], dtype=torch.float32)
        yt = torch.tensor(rx[fit], dtype=torch.float32)[:, None]
        xv = torch.tensor(Z[es], dtype=torch.float32)
        yv = torch.tensor(rx[es], dtype=torch.float32)[:, None]
        best, state = 1e9, None
        for ep in range(1500):
            opt.zero_grad()
            loss = ((net(xt) - yt) ** 2).mean()
            loss.backward()
            opt.step()
            with torch.no_grad():
                vl = float(((net(xv) - yv) ** 2).mean())
            if vl < best:
                best, state = vl, {k: v.clone() for k, v in net.state_dict().items()}
        net.load_state_dict(state)
        with torch.no_grad():
            preds.append(net(torch.tensor(Z, dtype=torch.float32)).numpy()[:, 0])
    return gam, pred_cp, np.mean(preds, 0), rx, dd


def compute_premia() -> dict:
    d, lp = _premia_data()
    code = inspect.getsource(_premia_data) + inspect.getsource(_premia_models)
    reg = {"cp_tent_oos": pit.register("cp_tent_oos", code, PREMIA_RULE, trials=1),
           "mlp_bond_premia_oos": pit.register("mlp_bond_premia_oos", code, PREMIA_RULE, trials=1)}
    gam, p_cp, p_nn, rx, dd = _premia_models(d, lp)
    pit.open_envelope("cp_tent_oos", "gsw_bond_rx", dd, rx)
    pit.open_envelope("mlp_bond_premia_oos", "gsw_bond_rx", dd, rx)
    tr = dd < 20040101

    def r2_oos(pred, sel):
        bench = rx[tr].mean()  # the in-sample mean: the honest naive forecast
        return float(1 - np.sum((rx[sel] - pred[sel]) ** 2) / np.sum((rx[sel] - bench) ** 2))
    val = (dd >= 20040101) & (dd < 20210101)
    hold = dd >= 20210101
    full = TS.cochrane_piazzesi(lp)
    return _json({"gamma": gam, "gamma_full": full["gamma"], "r2_in": float(1 - np.var(rx[tr] - p_cp[tr]) / np.var(rx[tr])),
                  "r2_full": full["r2"], "val": {"cp": r2_oos(p_cp, val), "nn": r2_oos(p_nn, val)},
                  "hold": {"cp": r2_oos(p_cp, hold), "nn": r2_oos(p_nn, hold)}, "t": _fy(dd), "rx": rx,
                  "pred_cp": p_cp, "pred_nn": p_nn, "registered": reg, "trials": pit.trials_so_far(),
                  "rule": PREMIA_RULE})


def compute_mbs() -> dict:
    d, v = (lambda f: (f["date"], f["value"]))(data.fred("MORTGAGE30US", "1971-01-01", "2025-12-31"))
    inc = np.linspace(-0.03, 0.03, 121)
    shifts = np.linspace(-0.03, 0.03, 25)
    mbs = np.array([TS.mbs_price(0.065, s_, n_paths=300, seed=0) for s_ in shifts])
    # a Treasury of the same starting price sensitivity: a bullet with the MBS's duration at par
    tsy = []
    k0 = int(np.argmin(np.abs(shifts)))
    dur = -(mbs[k0 + 1] - mbs[k0 - 1]) / (shifts[k0 + 1] - shifts[k0 - 1]) / mbs[k0]
    for s_ in shifts:
        tsy.append(mbs[k0] * np.exp(-dur * s_))
    conv = (mbs[k0 + 1] - 2 * mbs[k0] + mbs[k0 - 1]) / ((shifts[1] - shifts[0]) ** 2 * mbs[k0])
    return _json({"t": _fy(d), "rate": v, "low": {"t": float(_fy(d)[int(np.argmin(v))]), "v": float(v.min())},
                  "high": {"t": float(_fy(d)[int(np.argmax(v))]), "v": float(v.max())}, "inc": inc,
                  "cpr": TS.cpr_scurve(inc), "shifts": shifts, "mbs": mbs, "tsy": np.array(tsy), "duration": dur,
                  "convexity": conv, "end": float(v[-1])})


def compute_y1994() -> dict:
    f = data.fred("DFEDTAR", "1993-06-01", "1995-12-31")
    g = data.gsw("1993-06-01", "1995-12-31")
    k0 = int(np.searchsorted(g["date"], 19940103))
    k1 = int(np.argmax(g["y"][:, 9]))
    curves = {str(g["date"][k]): g["y"][k] for k in (k0, k1)}
    dy5 = float((g["y"][k1, 4] - g["y"][k0, 4]) / 100)
    # Orange County's pools at the end of June 1994 (SEC): 19.8 bn of securities on 7.2 bn of deposits, 12.6 bn
    # borrowed by reverse repo; the reported losses of 1.5-1.7 bn imply this average duration on the year's move
    eq, assets, repo = 7.2, 19.8, 12.6
    implied = [L / (assets * dy5) for L in (1.5, 1.7)]
    return _json({"ff_t": _fy(f["date"]), "ff": f["value"], "t": _fy(g["date"]), "y2": g["y"][:, 1], "y10": g["y"][:, 9],
                  "curves": curves, "dy5": dy5, "peak": int(g["date"][k1]), "pool": {"equity": eq, "assets": assets,
                                                                                         "repo": repo,
                                                                                         "implied_duration": implied,
                                                                                         "leverage": assets / eq}})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": load("premia")["registered"]}


ITEMS = {"shortrate": compute_shortrate, "hw": compute_hw, "hjm": compute_hjm, "lmm": compute_lmm,
         "bermudan": compute_bermudan, "negative": compute_negative, "sabr": compute_sabr,
         "multicurve": compute_multicurve, "premia": compute_premia, "mbs": compute_mbs, "y1994": compute_y1994,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
