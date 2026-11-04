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


def _hw_params(start="2023-01-01", end="2025-12-31"):
    """Hull-White's a and sigma from the term structure of the daily volatility of zero yields, 2023-2025: in the
    model the n-year zero yield moves by sigma B(n) / n per unit of the short rate's shock."""
    from scipy.optimize import least_squares
    g = data.gsw(start, end)
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
    sweep = []
    for aa in (0.005, 0.02, 0.05, 0.1, 0.2):  # the switch option against mean reversion, sigma held
        h2 = TS.HullWhite(c, aa, s)
        o = TS.bermudan_swaption_lsm(h2, K, T0, Tend, freq=1, payer=False, n_paths=30000, seed=2)
        sweep.append({"a": aa, "bermudan": o["price"], "best_european": max(o["europeans"])})
    return _json({"K": K, "a": a, "sigma": s, **out, "seed1": out2["price"], "se1": out2["se"], "sweep": sweep})


def compute_negative() -> dict:
    d, v = (lambda f: (f["date"], f["value"]))(data.fred("ECBDFR", "1999-01-01", "2025-12-31"))
    neg = v < 0
    first_neg = int(d[np.argmax(neg)])
    last_neg = int(d[np.where(neg)[0][-1]])
    T, K = 1.0, 0.0
    Fs = np.linspace(-0.01, 0.02, 61)
    bach = TS.bachelier(Fs, K, T, 0.006)
    black = np.array([TS.black_swaption(F, max(K, 1e-6), T, 0.6) if F > 0 else np.nan for F in Fs])
    g = data.fred("IRLTLT01DEM156N", "1999-01-01", "2025-12-31")  # German 10-year government yield, monthly
    gn = g["value"] < 0
    bund = {"t": _fy(g["date"]), "v": g["value"], "first": int(g["date"][np.argmax(gn)]),
            "last": int(g["date"][np.where(gn)[0][-1]]), "min": float(g["value"].min()),
            "min_date": int(g["date"][np.argmin(g["value"])]), "months": int(gn.sum())}
    return _json({"t": _fy(d), "dfr": v, "first_neg": first_neg, "last_neg": last_neg, "min": float(v.min()),
                  "F": Fs, "bach": bach, "black": black, "bund": bund})


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
    # an off-market swap: receive 1.5% fixed (struck when rates were low) against 3-month LIBOR, per 100 notional
    K = 0.015
    fwd_one = (np.r_[1.0, o1[:-1]] / o1 - 1) / 0.25
    off_two = float(100 * np.sum(0.25 * ois * (K - fwd_lib)))
    off_one = float(100 * np.sum(0.25 * o1 * (K - fwd_one)))
    return _json({"t": _fy(d), "ted": v, "peak": {"date": int(d[k]), "pct": float(v[k])}, "pre2007": float(pre),
                  "fixed_two": fixed_two, "fixed_one": fixed_one, "basis": basis, "K_off": K, "off_two": off_two,
                  "off_one": off_one, "annuity_two": float(np.sum(0.25 * ois)), "annuity_one": float(np.sum(0.25 * o1))})


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
    # option-adjusted spread: the spread over the model's rates that matches an (illustrative) market price, against
    # the same spread with the option switched off (zero volatility); the gap is the option's cost
    from scipy.optimize import brentq
    mkt = 101.0
    oas = brentq(lambda z: TS.mbs_price(0.065, 0.0, n_paths=300, seed=0, oas=z) - mkt, -0.02, 0.05, xtol=1e-6)
    zvs = brentq(lambda z: TS.mbs_price(0.065, 0.0, n_paths=2, seed=0, sigma=1e-9, oas=z) - mkt, -0.02, 0.05,
                 xtol=1e-6)
    # the summer 2003 sell-off, often attributed in part to convexity hedging; and the Fed's MBS holdings
    t10 = data.fred("DGS10", "2003-05-01", "2003-09-30")
    i0 = int(np.argmin(t10["value"]))
    i1 = i0 + int(np.argmax(t10["value"][i0:]))
    fed = data.fred("WSHOMCB", "2009-01-01", "2025-12-31")
    j = int(np.argmax(fed["value"]))
    y2003 = {"low": {"date": int(t10["date"][i0]), "v": float(t10["value"][i0])},
             "high": {"date": int(t10["date"][i1]), "v": float(t10["value"][i1])}}
    fedmbs = {"t": _fy(fed["date"]), "v": fed["value"] / 1e6, "peak": {"date": int(fed["date"][j]),
                                                                        "v": float(fed["value"][j] / 1e6)},
              "end": float(fed["value"][-1] / 1e6)}
    return _json({"y2003": y2003, "fed": fedmbs, "oas": {"mkt": mkt, "oas": float(oas), "zvs": float(zvs)}, "t": _fy(d), "rate": v, "low": {"t": float(_fy(d)[int(np.argmin(v))]), "v": float(v.min())},
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


# ---------------------------------------------------------------------------
# Additions: estimation bias, the rate-level elasticity of vol, SABR's density, LMM correlation, cap stripping
# ---------------------------------------------------------------------------
def compute_meanrev() -> dict:
    s = load("shortrate")
    x = np.asarray(s["x"])
    v = s["vas"]
    dt, n = 1 / 12, len(x)
    phi = np.exp(-v["a"] * dt)
    sd = v["sigma"] * np.sqrt((1 - phi ** 2) / (2 * v["a"]))
    # the AR(1) estimate's own standard error on the real data
    X = np.c_[np.ones(n - 1), x[:-1]]
    c, *_ = np.linalg.lstsq(X, x[1:], rcond=None)
    res = x[1:] - X @ c
    se_phi = float(np.sqrt(res.var() / np.sum((x[:-1] - x[:-1].mean()) ** 2)))
    # re-estimate on 2000 Vasicek histories of the same length, started at the same point, with the fitted truth
    rng = np.random.default_rng(0)
    m = 2000
    sims = np.zeros((m, n))
    sims[:, 0] = x[0]
    for k in range(n - 1):
        sims[:, k + 1] = v["b"] + (sims[:, k] - v["b"]) * phi + sd * rng.standard_normal(m)
    a_hat = np.empty(m)
    for i in range(m):
        y = sims[i]
        Xi = np.c_[np.ones(n - 1), y[:-1]]
        ci, *_ = np.linalg.lstsq(Xi, y[1:], rcond=None)
        a_hat[i] = -np.log(min(max(ci[1], 1e-6), 0.999999)) / dt
    return _json({"a": v["a"], "phi": float(c[1]), "se_phi": se_phi, "a_hat": a_hat, "years": n / 12,
                  "median": float(np.median(a_hat)), "mean": float(a_hat.mean()),
                  "q": np.quantile(a_hat, [0.05, 0.5, 0.95]),
                  "share_double": float(np.mean(a_hat > 2 * v["a"])),
                  "a_ci": [float(-np.log(min(c[1] + 1.96 * se_phi, 0.999999)) / dt),
                           float(-np.log(c[1] - 1.96 * se_phi) / dt)]})


def compute_ratevol() -> dict:
    f = data.fred("DGS10", "1962-01-01", "2025-12-31")
    d, v = f["date"], f["value"]
    yr = d // 10000
    rows = []
    for y in range(1962, 2026):
        s_ = yr == y
        if s_.sum() < 150:
            continue
        lv = v[s_]
        dv = np.diff(lv)
        rows.append((y, lv.mean(), np.std(dv) * np.sqrt(252) * 100, np.std(np.diff(np.log(lv))) * np.sqrt(252) * 100))
    a = np.array(rows)
    X = np.c_[np.ones(len(a)), np.log(a[:, 1])]
    cn, *_ = np.linalg.lstsq(X, np.log(a[:, 2]), rcond=None)
    return _json({"year": a[:, 0], "level": a[:, 1], "nvol_bp": a[:, 2], "lvol_pct": a[:, 3], "beta": float(cn[1]),
                  "c": float(cn[0]), "cv_n": float(np.std(a[:, 2]) / np.mean(a[:, 2])),
                  "cv_l": float(np.std(a[:, 3]) / np.mean(a[:, 3]))})


def compute_sabrpdf() -> dict:
    F = 0.035
    K = np.linspace(0.0005, 0.09, 1791)
    dK = K[1] - K[0]
    out = {}
    for T in (2.0, 10.0):
        p = {"alpha": 0.048, "beta": 0.5, "rho": -0.2, "nu": 0.35}
        iv = TS.sabr_normal_iv(F, K, T, **p)
        C = TS.bachelier(F, K, T, iv)
        pdf = np.diff(C, 2) / dK ** 2
        neg = pdf < 0
        out[f"{T:g}"] = {"K": K[1:-1:5], "pdf": pdf[::5], "neg_upto": float(K[1:-1][neg].max()) if neg.any() else 0.0,
                         "neg_mass": float(-pdf[neg].sum() * dK), "atm_nvol": float(iv[np.argmin(np.abs(K - F))])}
    return _json({"F": F, "params": {"alpha": 0.048, "beta": 0.5, "rho": -0.2, "nu": 0.35}, **out})


def compute_lmmcorr() -> dict:
    c = _curve_2025()
    dlt = 0.5
    Ti = 5.0 + dlt * np.arange(10)  # the forwards of a 5y x 5y swaption
    P = c.df(Ti + dlt)
    L = (c.df(Ti) / P - 1) / dlt
    w = dlt * P / np.sum(dlt * P)
    S = float(np.sum(w * L))
    sig = 0.009
    betas = [0.0, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    vols = []
    for b_ in betas:
        rho = np.exp(-b_ * np.abs(Ti[:, None] - Ti[None, :]))
        vols.append(float(np.sqrt(w @ (rho * sig * sig) @ w)))
    # a check of the frozen-weight formula by simulation: correlated normal forwards to expiry, the swap rate exact
    rng = np.random.default_rng(0)
    b_chk = 0.2
    rho = np.exp(-b_chk * np.abs(Ti[:, None] - Ti[None, :]))
    Lc = np.linalg.cholesky(rho)
    Z = rng.standard_normal((50000, len(Ti))) @ Lc.T
    LT = L + sig * np.sqrt(5.0) * Z
    PT = np.cumprod(1 / (1 + dlt * LT), axis=1)
    ST = (1 - PT[:, -1]) / (dlt * PT.sum(1))
    mc = float(np.std(ST) / np.sqrt(5.0))
    return _json({"T": Ti, "S": S, "beta": betas, "nvol": vols, "caplet": sig, "check_beta": b_chk, "check_mc": mc,
                  "check_formula": vols[betas.index(b_chk)]})


def compute_capstrip() -> dict:
    c = _curve_2025()
    dlt = 0.25
    t = dlt * np.arange(1, 40)  # caplet resets, 3 months to 9.75 years
    P = c.df(t + dlt)
    F = (c.df(t) / P - 1) / dlt

    def abcd(T, a=0.004, b=0.006, c_=0.45, d=0.0075):  # Rebonato's hump, normal vol
        return (a + b * T) * np.exp(-c_ * T) + d
    sv = abcd(t)
    mats = np.arange(1, 11)
    flat, K = [], []
    for M in mats:
        sel = t + dlt <= M + 1e-9
        k = float(np.sum(dlt * P[sel] * F[sel]) / np.sum(dlt * P[sel]))
        price = float(np.sum(TS.bachelier(F[sel], k, t[sel], sv[sel], dlt * P[sel])))
        from scipy.optimize import brentq
        fv = brentq(lambda s_: float(np.sum(TS.bachelier(F[sel], k, t[sel], s_, dlt * P[sel]))) - price, 1e-5, 0.1)
        flat.append(fv)
        K.append(k)
    # strip: from the flat vols back to piecewise-constant caplet vols between cap maturities
    strip = []
    from scipy.optimize import brentq
    for i, M in enumerate(mats):
        sel = t + dlt <= M + 1e-9
        k = K[i]
        target = float(np.sum(TS.bachelier(F[sel], k, t[sel], flat[i], dlt * P[sel])))
        prev = t + dlt <= (mats[i - 1] if i else 0) + 1e-9
        known = np.zeros(len(t))
        for j, Mj in enumerate(mats[:i]):
            known[(t + dlt <= Mj + 1e-9) & (t + dlt > (mats[j - 1] if j else 0) + 1e-9)] = strip[j]
        new = sel & ~prev

        def f(s_):
            v_ = known.copy()
            v_[new] = s_
            return float(np.sum(TS.bachelier(F[sel], k, t[sel], v_[sel], dlt * P[sel]))) - target
        strip.append(brentq(f, 1e-5, 0.1))
    return _json({"t": t, "spot": sv, "mats": mats, "flat": flat, "strip": strip, "K": K})



def compute_lattice() -> dict:
    """The Bermudan again, by backward induction on the state with no simulation; and the callable bond it hedges."""
    b = load("bermudan")
    c = _curve_2025()
    hw = TS.HullWhite(c, b["a"], b["sigma"])
    K = b["K"]
    lat = TS.bermudan_swaption_lattice(hw, K, 1.0, 10.0)
    euro = [TS.bermudan_swaption_lattice(hw, K, 1.0, 10.0, dates=[t]) for t in b["dates"]]
    sweep = [{"a": x["a"], "lattice": TS.bermudan_swaption_lattice(TS.HullWhite(c, x["a"], b["sigma"]), K, 1.0, 10.0),
              "lsm": x["bermudan"]} for x in b["sweep"]]
    # a 10-year bond paying K annually, callable at par each year from year 1: the investor is short the Bermudan
    t = np.arange(1, 11)
    bullet = float(100 * (K * c.df(t).sum() + c.df(10.0)))
    callable_ = bullet - 100 * lat

    def ytm(price):
        from scipy.optimize import brentq
        return brentq(lambda y: float(np.sum(100 * K / (1 + y) ** t) + 100 / (1 + y) ** 10) - price, -0.05, 0.3)
    return _json({"lattice": lat, "lsm": b["price"], "se": b["se"], "europeans_lattice": euro,
                  "europeans_closed": b["europeans"], "sweep": sweep, "bullet": bullet, "callable": callable_,
                  "y_bullet": ytm(bullet), "y_callable": ytm(callable_), "K": K})


def _month_end_curves(start="1990-01-01"):
    g = data.gsw(start, "2025-12-31")
    m = g["date"] // 100
    idx = np.where(np.r_[m[1:] != m[:-1], True])[0]
    r0 = []
    for i in idx:
        b_, t_ = g["beta"][i].copy(), g["tau"][i].copy()
        if np.isnan(t_[1]) or np.isnan(b_[3]):
            b_[3], t_[1] = 0.0, 1.0
        r0.append(R.nss(np.array([0.25]), b_, t_)[0] / 100)
    return g, idx, np.array(r0)


def compute_pq() -> dict:
    """Vasicek twice: fitted to the short rate's history (P) and to the cross-section of yields (Q), same sigma."""
    from scipy.optimize import least_squares
    s = load("shortrate")
    v = s["vas"]
    g, idx, r0 = _month_end_curves()
    mats = np.array([1, 2, 3, 5, 7, 10.0])
    Y = g["y"][idx][:, (mats - 1).astype(int)] / 100
    ok = np.isfinite(Y).all(1)
    sg = v["sigma"]

    def res(p):
        a, bq = p
        return np.concatenate([-np.log(TS.vasicek_zcb(r0[ok], a, bq, sg, T)) / T - Y[ok][:, k]
                               for k, T in enumerate(mats)])
    f = least_squares(res, [0.1, 0.05], bounds=([1e-3, -0.1], [2.0, 0.3]))
    aq, bq = f.x
    T = np.linspace(0.25, 10, 40)
    avg_r0 = float(r0[ok].mean())
    return _json({"aP": v["a"], "bP": v["b"], "aQ": float(aq), "bQ": float(bq), "sigma": sg,
                  "rmse_bp": float(np.sqrt(np.mean(f.fun ** 2)) * 1e4), "mats": mats, "avg_curve": Y[ok].mean(0),
                  "avg_r0": avg_r0, "T": T,
                  "curve_P": -np.log(TS.vasicek_zcb(avg_r0, v["a"], v["b"], sg, T)) / T,
                  "curve_Q": -np.log(TS.vasicek_zcb(avg_r0, aq, bq, sg, T)) / T, "n": int(ok.sum()),
                  "lam": float(aq * (bq - v["b"]) / sg)})


def compute_twofactor() -> dict:
    """Correlations of daily yield changes against the 2-year, in the data and in a two-factor Gaussian model."""
    from scipy.optimize import least_squares
    g = data.gsw("1990-01-01", "2025-12-31")
    n = np.arange(1, 31)
    dy = np.diff(g["y"], axis=0)
    ok = np.isfinite(dy).all(1)
    C = np.corrcoef(dy[ok].T)
    a1, a2 = 0.02, 0.9

    def model(p):
        r_, rho = p
        l1, l2 = (1 - np.exp(-a1 * n)) / (a1 * n), r_ * (1 - np.exp(-a2 * n)) / (a2 * n)
        cov = np.outer(l1, l1) + np.outer(l2, l2) + rho * (np.outer(l1, l2) + np.outer(l2, l1))
        sd = np.sqrt(np.diag(cov))
        return cov / np.outer(sd, sd)
    sel = [0, 1, 4, 9, 19, 29]
    f = least_squares(lambda p: (model(p) - C)[np.ix_(sel, sel)].ravel(), [1.0, -0.5], bounds=([0.01, -0.99], [10, 0.99]))
    M = model(f.x)
    return _json({"n": n, "data": C[1], "model": M[1], "data_1_30": float(C[0, 29]), "model_1_30": float(M[0, 29]),
                  "data_2_10": float(C[1, 9]), "model_2_10": float(M[1, 9]), "a1": a1, "a2": a2,
                  "ratio": float(f.x[0]), "rho": float(f.x[1])})


def compute_premia_acm() -> dict:
    """The Cochrane-Piazzesi forecast against the NY Fed's ACM term premium (Part 18), month by month."""
    p = load("premia")
    a = data.acm()
    t = np.asarray(p["t"])
    pm = (np.floor(t) * 100 + np.floor((t - np.floor(t)) * 12 + 1e-6) + 1).astype(int)
    am = a["date"] // 100
    pos = {m: i for i, m in enumerate(am)}
    pairs = [(i, pos[m]) for i, m in enumerate(pm) if m in pos]
    i1, i2 = map(np.array, zip(*pairs))
    cp = np.asarray(p["pred_cp"])[i1] * 100
    tp5 = a["tp"][i2][:, 4]
    return _json({"t": t[i1], "cp": cp, "tp5": tp5, "corr": float(np.corrcoef(cp, tp5)[0, 1]),
                  "corr10": float(np.corrcoef(cp, a["tp"][i2][:, 9])[0, 1])})


def compute_greeks() -> dict:
    """The Bermudan's risks by the lattice: a 1 bp parallel move of the curve, 1 bp of normal volatility; and the
    same for its most valuable European, the natural first hedge."""
    b = load("bermudan")
    c = _curve_2025()
    K, a, sg = b["K"], b["a"], b["sigma"]
    up = R.Curve(c.t, c.z + 1e-4)
    dn = R.Curve(c.t, c.z - 1e-4)
    k = int(np.argmax(b["europeans"]))
    T = float(b["dates"][k])

    def berm(cv, s_):
        return TS.bermudan_swaption_lattice(TS.HullWhite(cv, a, s_), K, 1.0, 10.0)

    def euro(cv, s_):
        return TS.HullWhite(cv, a, s_).swaption(K, T, 10.0 - T, 1, payer=False)
    out = {}
    for name, f in (("bermudan", berm), ("european", euro)):
        v0 = f(c, sg)
        out[name] = {"price": v0, "delta": (f(up, sg) - f(dn, sg)) / 2, "vega": (f(c, sg + 1e-4) - f(c, sg - 1e-4)) / 2,
                     "gamma": f(up, sg) + f(dn, sg) - 2 * v0}
    n_eu = out["bermudan"]["vega"] / out["european"]["vega"]
    # the swap that clears the remaining delta: a 10-year receiver swap's DV01 per unit notional
    t = np.arange(1, 11)
    swap_dv01 = float(np.sum(K * (R.Curve(c.t, c.z + 1e-4).df(t) - R.Curve(c.t, c.z - 1e-4).df(t))) / 2 +
                      (R.Curve(c.t, c.z + 1e-4).df(10.0) - R.Curve(c.t, c.z - 1e-4).df(10.0)) / 2)
    resid = out["bermudan"]["delta"] - n_eu * out["european"]["delta"]
    return _json({**out, "T_eu": T, "n_eu": n_eu, "resid_delta": resid, "swap_dv01": swap_dv01,
                  "n_swap": -resid / swap_dv01})


def compute_famabliss() -> dict:
    """Fama and Bliss (1987): each bond's excess return on its own forward spread, 1964-2025; the expectations
    hypothesis says every slope is zero."""
    d, lp = _premia_data()
    cp = TS.cochrane_piazzesi(lp)
    fwd, rx = cp["fwd"][:-12], cp["rx"]
    dd = d[:-12]
    sel = dd >= 19640101
    out = []
    for k, n in enumerate(range(2, 6)):
        x = (fwd[:, k + 1] - fwd[:, 0])[sel]
        y = rx[sel, k]
        X = np.c_[np.ones(len(x)), x]
        b_, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b_
        # Newey-West standard error with 12 lags for the overlapping annual returns
        u = X * e[:, None]
        S = u.T @ u
        for L in range(1, 13):
            w = 1 - L / 13
            G = u[L:].T @ u[:-L]
            S += w * (G + G.T)
        Q = np.linalg.inv(X.T @ X)
        se = float(np.sqrt((Q @ S @ Q)[1, 1]))
        out.append({"n": n, "slope": float(b_[1]), "se": se, "r2": float(1 - e.var() / y.var())})
    return _json({"rows": out, "start": 1964, "end": int(dd[sel][-1] // 10000)})


def compute_hwwin() -> dict:
    """Hull-White's two parameters fitted to the same kind of data in four different three-year windows."""
    out = []
    for a_, b_ in (("2004-01-01", "2006-12-31"), ("2010-01-01", "2012-12-31"), ("2019-01-01", "2021-12-31"),
                   ("2023-01-01", "2025-12-31")):
        a, s_, mats, vol, fit = _hw_params(a_, b_)
        out.append({"window": f"{a_[:4]}--{b_[:4]}", "a": a, "sigma": s_, "mats": mats, "vol": vol, "fit": fit})
    return _json({"windows": out})

ITEMS = {"shortrate": compute_shortrate, "hw": compute_hw, "hjm": compute_hjm, "lmm": compute_lmm,
         "bermudan": compute_bermudan, "negative": compute_negative, "sabr": compute_sabr,
         "multicurve": compute_multicurve, "premia": compute_premia, "mbs": compute_mbs, "y1994": compute_y1994,
         "meanrev": compute_meanrev, "ratevol": compute_ratevol, "sabrpdf": compute_sabrpdf, "lmmcorr": compute_lmmcorr,
         "capstrip": compute_capstrip, "lattice": compute_lattice, "pq": compute_pq, "twofactor": compute_twofactor,
         "premia_acm": compute_premia_acm, "greeks": compute_greeks,
         "famabliss": compute_famabliss, "hwwin": compute_hwwin, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
