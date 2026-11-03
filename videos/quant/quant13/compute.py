"""Every number in Part 13 (Stochastic Volatility and Jumps), computed and cached in .cache/quant13/.

    python -m videos.quant.quant13.compute [items] [--force]

Items (seconds to a few minutes each on a CPU):

* ``facts``      bitcoin's volatility moves: 30-day realized vol, DVOL, the vol of vol, and the leverage correlation
                 between returns and changes in implied vol (Binance daily, Deribit DVOL), 2021-2025;
* ``calibrate``  Black-Scholes, Heston, Bates, variance gamma and NIG fitted to the Surface (10 December 2025) by
                 the House's calibrator (COS pricing); errors by expiry; SABR fitted slice by slice;
* ``qe``         Monte Carlo bias of full-truncation Euler against Andersen's QE scheme, under the calibrated Heston;
* ``skew``       the at-the-money skew by maturity: the market against every model;
* ``sabr``       the SABR backbone, and the negative density of Hagan's formula at low strikes;
* ``landscape``  Heston's loss over (kappa, xi), the others re-optimized at each point; a multi-start;
* ``history``    Heston calibrated to 100 weekly surfaces (2024-2025): parameter instability;
* ``slv``        stochastic local volatility by the particle method (Guyon and Henry-Labordere): the leverage
                 function, and its vanilla repricing error;
* ``exotics``    forward smiles and a cliquet under local vol, Heston, Bates, VG and SLV, all fitted to the same
                 vanillas;
* ``bergomi``    the forward variance curve read from the Surface, against Heston's;
* ``envelope``   registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import numpy as np
from scipy.optimize import least_squares

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, pit, smile, stochvol as sv, surface, volsurface as V

CACHE = Cache("quant13")
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 13)  # the series' trial counter as of this part

DAY = surface.DAYS[0]
MODELS = ("Heston", "Bates", "VG", "NIG")


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _quotes(day=DAY, min_T=2 / 365, max_k=0.6):
    q = surface.build(day)
    ok = (np.abs(q["k"]) < max_k) & (q["T"] > min_T)
    return {k: (np.asarray(v)[ok] if isinstance(v, np.ndarray) and len(v) == len(ok) else v) for k, v in q.items()}


def _sub(Q, m):
    return {k: (v[m] if isinstance(v, np.ndarray) and len(v) == len(m) else v) for k, v in Q.items()}


def _rmse(iv, Q, m=None):
    m = np.ones(len(Q["K"]), bool) if m is None else m
    return float(np.sqrt(np.average((iv[m] - Q["iv"][m]) ** 2 * 1e4, weights=Q["vega"][m])))


def _model_iv_all(name, x, Q):
    out = np.empty(len(Q["K"]))
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        out[m] = sv.surface_iv(name, x, float(Q["F"][m][0]), Q["K"][m], T)
    return out


def _ssvi():
    s = CACHE.__class__("quant12").load("surface")
    fit = s["ssvi"]
    return fit, s


def _ssvi_w(fit, k, T):
    return V.ssvi_surface_w(fit, k, T)


# ---------------------------------------------------------------------------
def compute_facts() -> dict:
    kl = data.binance_klines("BTCUSDT", "1d", "2021-04", "2025-11")
    t = np.asarray(kl["time"], float)
    c = np.asarray(kl["close"], float)
    r = np.diff(np.log(c))
    rv30 = np.sqrt(np.convolve(r ** 2, np.ones(30), "valid") / 30 * 365)
    dv = data.deribit_dvol("2021-04", "2025-11", resolution=86400)
    td = np.asarray(dv["time"], float)
    vd = np.asarray(dv["close"], float) / 100
    lv = np.log(vd)
    # daily changes of log DVOL matched to the same day's return
    days_r = (t[1:] // 86400).astype(int)
    days_v = (td // 86400).astype(int)
    pos = {d: i for i, d in enumerate(days_v)}
    pairs = []
    for i, d in enumerate(days_r):
        j, j0 = pos.get(d), pos.get(d - 1)  # DVOL's close on day d against day d - 1, with day d's return
        if j is not None and j0 is not None:
            pairs.append((r[i], lv[j] - lv[j0], t[i + 1]))
    pr = np.array(pairs)
    corr = float(np.corrcoef(pr[:, 0], pr[:, 1])[0, 1])
    years = {}
    for y in range(2021, 2026):
        a = datetime(y, 1, 1, tzinfo=timezone.utc).timestamp()
        b = datetime(y + 1, 1, 1, tzinfo=timezone.utc).timestamp()
        m = (pr[:, 2] >= a) & (pr[:, 2] < b)
        if m.sum() > 60:
            years[y] = float(np.corrcoef(pr[m, 0], pr[m, 1])[0, 1])
    volvol = float(np.std(pr[:, 1]) * np.sqrt(365))
    # down days against up days: the average change in DVOL
    dn = float(np.mean(pr[pr[:, 0] < -0.05, 1]) * 100)
    up = float(np.mean(pr[pr[:, 0] > 0.05, 1]) * 100)
    return _json({"t": t[30:], "rv30": rv30, "dvol_t": td, "dvol": vd, "leverage_corr": corr, "by_year": years,
                  "volvol": volvol, "n": len(pr), "dvol_change_down5": dn, "dvol_change_up5": up,
                  "rv_min": float(rv30.min()), "rv_max": float(rv30.max())})


def compute_calibrate() -> dict:
    Q = _quotes()
    out = {"n": len(Q["K"]), "S": Q["S"], "expiries_days": sorted(set(np.round(Q["T"] * 365).astype(int).tolist()))}
    # Black-Scholes: one volatility for everything
    p = float(np.average(Q["iv"], weights=Q["vega"]))  # the least-squares single vol, vega-weighted
    fits = {"BS": {"params": {"sigma": float(p)}, "x": [float(p)], "iv": np.full(len(Q["K"]), p)}}
    for name in MODELS:
        starts = [None]
        if name == "Heston":
            starts += [(0.2, 1.0, 0.3, 0.8, -0.3), (0.3, 5.0, 0.2, 3.0, 0.0)]
        if name == "Bates":
            starts += [(0.15, 3, 0.25, 1.5, -0.3, 0.5, -0.1, 0.2), (0.15, 3, 0.25, 1.5, -0.3, 3, 0.0, 0.15)]
        best = min((sv.calibrate(name, Q, x0=s0) for s0 in starts), key=lambda r: r["cost"])
        best["iv"] = _model_iv_all(name, best["x"], Q)
        fits[name] = best
    for name, f in fits.items():
        f["rmse"] = _rmse(f["iv"], Q)
        f["by_expiry"] = {int(round(T * 365)): _rmse(f["iv"], Q, Q["T"] == T) for T in np.unique(Q["T"])}
    h = fits["Heston"]["params"]
    out["feller"] = 2 * h["kappa"] * h["theta"] / h["xi"] ** 2
    # SABR, beta = 1, fitted slice by slice (alpha, rho, nu)
    sabr = {}
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        if m.sum() < 6:
            continue
        F = float(Q["F"][m][0])
        K, iv, w = Q["K"][m], Q["iv"][m], np.sqrt(Q["vega"][m] / Q["vega"][m].mean())
        r = least_squares(lambda p: (sv.sabr_iv(F, K, T, p[0], 1.0, p[1], p[2]) - iv) * w * 100,
                          [float(np.median(iv)), -0.1, 1.5], bounds=([0.01, -0.999, 0.01], [5, 0.999, 20]))
        sabr[int(round(T * 365))] = {"alpha": r.x[0], "rho": r.x[1], "nu": r.x[2],
                                     "rmse": float(np.sqrt(np.average((sv.sabr_iv(F, K, T, *[r.x[0], 1.0, r.x[1], r.x[2]])
                                                                       - iv) ** 2 * 1e4, weights=Q["vega"][m])))}
    allm = np.concatenate([np.full((Q["T"] == T).sum(), int(round(T * 365))) for T in np.unique(Q["T"])])
    sab_iv = np.empty(len(Q["K"]))
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        d = sabr.get(int(round(T * 365)))
        sab_iv[m] = sv.sabr_iv(float(Q["F"][m][0]), Q["K"][m], T, d["alpha"], 1.0, d["rho"], d["nu"]) if d else np.nan
    okm = np.isfinite(sab_iv)
    out["sabr"] = sabr
    tt = np.array([int(d) for d in sabr]) / 365
    nu = np.array([v["nu"] for v in sabr.values()])
    out["sabr_nu_power"] = float(np.polyfit(np.log(tt), np.log(nu), 1)[0])  # vol of vol ~ T^a: Part 14's clue
    out["sabr_rmse"] = _rmse(np.where(okm, sab_iv, 0), Q, okm)
    # three slices to draw
    shown = []
    for d_ in (9, 51, 198):
        T = Q["T"][np.argmin(np.abs(Q["T"] * 365 - d_))]
        m = Q["T"] == T
        F = float(Q["F"][m][0])
        kk = np.linspace(Q["k"][m].min() - 0.03, Q["k"][m].max() + 0.03, 61)
        curves = {name: sv.surface_iv(name, fits[name]["x"], F, F * np.exp(kk), T).tolist() for name in MODELS}
        shown.append({"days": int(round(T * 365)), "k": Q["k"][m], "iv": Q["iv"][m], "kk": kk, "curves": curves})
    out["shown"] = shown
    out["fits"] = {n: {k: v for k, v in f.items() if k != "iv"} for n, f in fits.items()}
    out["quotes"] = {"k": Q["k"], "T": Q["T"], "iv": Q["iv"], "days": allm}
    return _json(out)


def _heston_x():
    return load("calibrate")["fits"]["Heston"]["x"]


def compute_qe() -> dict:
    v0, kappa, theta, xi, rho = _heston_x()
    S0, T = 1.0, 0.25
    Ks = (0.8, 1.0)
    cf = lambda u, TT: sv.heston_cf(u, TT, v0, kappa, theta, xi, rho)  # noqa: E731
    exact = {K: float(sv.cos_price(cf, S0, K, T, -1 if K < 1 else 1)[0]) for K in Ks}
    ns = [2, 4, 8, 16, 32, 64, 128]
    n_paths = 200_000
    rows = []
    for n in ns:
        S = sv.heston_qe(S0, v0, kappa, theta, xi, rho, T, n, n_paths, seed=n)
        g = np.random.default_rng(1000 + n)
        dt = T / n
        x = np.zeros(n_paths)
        v = np.full(n_paths, v0)
        for _ in range(n):  # full-truncation Euler (Lord, Koekkoek and van Dijk 2010)
            z1 = g.standard_normal(n_paths)
            z2 = rho * z1 + np.sqrt(1 - rho ** 2) * g.standard_normal(n_paths)
            vp = np.maximum(v, 0)
            x += -0.5 * vp * dt + np.sqrt(vp * dt) * z1
            v = v + kappa * (theta - vp) * dt + xi * np.sqrt(vp * dt) * z2
        SE = np.exp(x)
        for K in Ks:
            cp = -1 if K < 1 else 1
            for scheme, ST in (("QE", S[-1]), ("Euler", SE)):
                pay = np.maximum(cp * (ST - K), 0)
                rows.append({"n": n, "K": K, "scheme": scheme, "bias": float(pay.mean() - exact[K]),
                             "se": float(pay.std() / np.sqrt(n_paths)), "rel": float((pay.mean() - exact[K]) / exact[K])})
    return _json({"rows": rows, "exact": {str(k): v for k, v in exact.items()}, "T": T, "n_paths": n_paths,
                  "params": [v0, kappa, theta, xi, rho], "feller": 2 * kappa * theta / xi ** 2})


def compute_skew() -> dict:
    c = load("calibrate")
    Q = _quotes()
    mkt = []
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        if m.sum() < 6:
            continue
        p = smile.fit_svi(Q["k"][m], Q["iv"][m] ** 2 * T, weights=Q["vega"][m])
        h = 0.01
        sig = lambda k: np.sqrt(smile.svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"]) / T)  # noqa: E731
        mkt.append({"T": float(T), "skew": float((sig(h) - sig(-h)) / (2 * h)), "atm": float(sig(0.0))})
    Ts = np.exp(np.linspace(np.log(2 / 365), np.log(1.0), 30))
    models = {}
    for name in MODELS:
        x = c["fits"][name]["x"]
        sk = []
        for T in Ts:
            iv = sv.surface_iv(name, x, 1.0, np.exp(np.array([-0.01, 0.01])), T)
            sk.append(float((iv[1] - iv[0]) / 0.02))
        models[name] = sk
    # a power law for the market's |skew| ~ c T^a (Part 14 asks why a is near -1/2)
    tt = np.array([r["T"] for r in mkt])
    ss = np.abs(np.array([r["skew"] for r in mkt]))
    ok = ss > 1e-4
    a, lc = np.polyfit(np.log(tt[ok]), np.log(ss[ok]), 1)
    return _json({"market": mkt, "T": Ts, "models": models, "power": float(a), "power_c": float(np.exp(lc))})


def compute_sabr() -> dict:
    c = load("calibrate")
    d = c["sabr"]["51"] if "51" in c["sabr"] else list(c["sabr"].values())[len(c["sabr"]) // 2]
    T = 51 / 365
    F0 = 1.0
    atm0 = float(sv.sabr_iv(F0, F0, T, d["alpha"], 1.0, d["rho"], d["nu"])[0])
    Fs = np.linspace(0.7, 1.3, 25)
    backbone = {}
    for beta in (0.0, 0.5, 1.0):
        # choose alpha so that today's at-the-money vol matches
        al = least_squares(lambda a: sv.sabr_iv(F0, F0, T, a[0], beta, d["rho"], d["nu"]) - atm0, [atm0]).x[0]
        backbone[str(beta)] = [float(sv.sabr_iv(F, F, T, al, beta, d["rho"], d["nu"])[0]) for F in Fs]
    # Hagan's density where it famously fails: a rates-like smile (3% forward, beta 1/2) at ten years
    out = {"Fs": Fs, "backbone": backbone, "atm0": atm0, "params": d}
    dens = {}
    Fr, al, be, rh, nu = 0.03, 0.035, 0.5, -0.3, 0.4
    K = np.linspace(0.0005, 0.09, 180)
    for TT in (1.0, 10.0):
        with np.errstate(all="ignore"):
            pdf = sv.sabr_density(Fr, K, TT, al, be, rh, nu, h=1e-5)
        dens[f"{TT:.0f}"] = {"K": K, "pdf": pdf, "min": float(np.nanmin(pdf)),
                             "mass": float(np.nansum(pdf) * (K[1] - K[0])),
                             "neg_below": float(K[pdf < 0].max()) if (pdf < 0).any() else 0.0}
    out["density_params"] = {"F": Fr, "alpha": al, "beta": be, "rho": rh, "nu": nu,
                             "atm": float(sv.sabr_iv(Fr, Fr, 10.0, al, be, rh, nu)[0])}
    out["density"] = dens
    return _json(out)


def compute_landscape() -> dict:
    Q = _quotes()
    F, K, T, iv, cp = Q["F"], Q["K"], Q["T"], Q["iv"], Q["cp"]
    pre = {"price": np.array([float(bs.black(f, k, t, s, cp=int(c))) for f, k, t, s, c in zip(F, K, T, iv, cp)])}
    d1 = np.log(F / K) / (iv * np.sqrt(T)) + 0.5 * iv * np.sqrt(T)
    pre["vega"] = F * np.sqrt(T) * bs.npdf(d1)
    kappas = np.exp(np.linspace(np.log(0.5), np.log(30), 15))
    xis = np.exp(np.linspace(np.log(0.3), np.log(8), 15))
    best = load("calibrate")["fits"]["Heston"]["x"]
    L = np.zeros((len(kappas), len(xis)))
    inner = np.zeros((len(kappas), len(xis), 3))
    for i, ka in enumerate(kappas):
        x0 = [best[0], best[2], best[4]]
        for j, xi in enumerate(xis):
            f = lambda p: sv.residuals("Heston", [p[0], ka, p[1], xi, p[2]], Q, pre)  # noqa: E731
            r = least_squares(f, x0, bounds=([1e-3, 1e-3, -0.99], [4, 4, 0.99]), max_nfev=60)
            L[i, j] = float(np.sqrt(np.mean(r.fun ** 2)))
            inner[i, j] = r.x
            x0 = r.x
    g = np.random.default_rng(13)
    starts = []
    for _ in range(12):
        x0 = [g.uniform(0.05, 0.6), np.exp(g.uniform(np.log(0.5), np.log(20))), g.uniform(0.05, 0.6),
              np.exp(g.uniform(np.log(0.3), np.log(6))), g.uniform(-0.8, 0.5)]
        r = sv.calibrate("Heston", Q, x0=x0, max_nfev=300)
        starts.append({"x0": x0, "x": r["x"], "rmse": r["rmse"]})
    return _json({"kappa": kappas, "xi": xis, "loss": L, "inner": inner, "starts": starts, "best": best})


def compute_history() -> dict:
    d = date(2024, 1, 3)
    rows = []
    x0 = None
    while d <= date(2025, 11, 26):
        try:
            Q = _quotes(d.isoformat(), min_T=6 / 365)
            r = sv.calibrate("Heston", Q, x0=x0, max_nfev=200)
            r0 = sv.calibrate("Heston", Q, max_nfev=200) if x0 is not None else r
            r = min((r, r0), key=lambda z: z["cost"])
            rows.append({"day": d.isoformat(), "x": r["x"], "rmse": r["rmse"], "n": len(Q["K"])})
            x0 = r["x"]
        except Exception as e:
            rows.append({"day": d.isoformat(), "error": str(e)[:200]})
        d += timedelta(days=7)
    good = [r for r in rows if "x" in r]
    X = np.array([r["x"] for r in good])
    chg = np.abs(np.diff(np.log(np.maximum(X[:, :4], 1e-6)), axis=0))
    return _json({"rows": good, "skipped": [r["day"] for r in rows if "error" in r],
                  "median_weekly_change": {n: float(np.median(chg[:, i])) for i, n in enumerate(("v0", "kappa", "theta", "xi"))},
                  "rmse_median": float(np.median([r["rmse"] for r in good])),
                  "range": {n: [float(X[:, i].min()), float(X[:, i].max())] for i, n in
                            enumerate(("v0", "kappa", "theta", "xi", "rho"))}})


def _lv_fn(fit):
    return V.local_vol_fn(fit)


def _simulate(model, n_paths=40000, days=120, seed=7, slv_out=None, mix=0.5):
    """Daily paths of log(S/S0), zero rates, for every model in the comparison."""
    dt = 1 / 365
    c = load("calibrate")["fits"]
    if model in ("Heston", "Bates"):
        x = c[model]["x"]
        if model == "Heston":
            S = sv.heston_qe(1.0, *x, days * dt, days, n_paths, seed=seed)
        else:
            S = sv.bates_paths(1.0, *x, days * dt, days, n_paths, seed=seed)
        return np.log(S)
    if model == "VG":
        return np.log(sv.vg_paths(1.0, *c["VG"]["x"], days * dt, days, n_paths, seed=seed))
    fit, _ = _ssvi()
    if model == "LV":
        m = 4  # sub-steps per day: short-dated local vol is steep, and a daily Euler step underprices by a vol point
        return V.local_vol_paths(fit, days, n_paths, seed=seed, substeps=m)
    # SLV: Heston variance times a leverage function, calibrated on the fly by the particle method; the mixing
    # fraction keeps half of Heston's vol of vol, the leverage function does the rest (the House's slv_paths)
    return sv.slv_paths(_lv_fn(fit), c["Heston"]["x"], days, n_paths, mix=mix, substeps=4, n_sub=8000, seed=seed,
                        info=slv_out)


def _iv_from_paths(xT, k, T):
    out = []
    for kk in k:
        cp = 1 if kk >= 0 else -1
        p = float(np.mean(np.maximum(cp * (np.exp(xT) - np.exp(kk)), 0)))
        out.append(float(bs.implied_vol(p, 1.0, np.exp(kk), T, 0.0, 0.0, cp)))
    return np.array(out)


def compute_slv() -> dict:
    meta = {}
    X = _simulate("SLV", slv_out=meta)
    fit, _ = _ssvi()
    k = np.linspace(-0.3, 0.3, 13)
    rep = []
    for days in (30, 60, 90, 120):
        T = days / 365
        mc = _iv_from_paths(X[days], k, T)
        tgt = np.sqrt(_ssvi_w(fit, k, T) / T)
        rep.append({"days": days, "mc": mc, "target": tgt, "err": float(np.sqrt(np.mean((mc - tgt) ** 2)) * 100)})
    return _json({"L": meta["L"], "grid": meta["grid"], "reprice": rep, "k": k})


def compute_exotics() -> dict:
    k = np.linspace(-0.25, 0.25, 11)
    fit, _ = _ssvi()
    out = {"k": k, "models": {}}
    T2 = 30 / 365
    out["today"] = np.sqrt(_ssvi_w(fit, k, T2) / T2)
    for m in ("LV", "Heston", "Bates", "VG", "SLV"):
        X = _simulate(m)
        fwd = _iv_from_paths(X[90] - X[60], k, T2)
        vanilla90 = _iv_from_paths(X[90], np.array([-0.1, 0.0, 0.1]), 90 / 365)
        S = np.exp(X)
        cl = sv.cliquet(S, [0, 30, 60, 90, 120], cap=0.10, floor=0.0, gfloor=0.0)
        fs = sv.forward_start(S, 60, 90)
        out["models"][m] = {"fwd_iv": fwd, "fwd_atm": float(fwd[5]), "fwd_skew": float(fwd[3] - fwd[7]),
                            "cliquet": cl, "forward_start": fs, "vanilla90": vanilla90}
    cls = np.array([v["cliquet"] for v in out["models"].values()])
    out["cliquet_spread"] = float((cls.max() - cls.min()) / cls.mean())
    out["today_skew"] = float(out["today"][3] - out["today"][7])
    out["today_vanilla90"] = np.sqrt(_ssvi_w(fit, np.array([-0.1, 0.0, 0.1]), 90 / 365) / (90 / 365))
    return _json(out)


def compute_bergomi() -> dict:
    """Bergomi's state variable: the forward variance curve xi_0(T) = d/dT [T * K_var(T)], read from variance-swap
    strikes (Part 12's 1/K^2 strip) on the SSVI fit to the Surface, against the calibrated Heston's."""
    fit, s = _ssvi()
    F = 1.0
    K = np.exp(np.linspace(-2.5, 2.0, 3001))
    Tg = np.asarray(fit["T"], float)  # the quoted expiries: forward variance is constant between them
    tv = []
    for T in Tg:
        iv = np.sqrt(_ssvi_w(fit, np.log(K / F), T) / T)
        otm = np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))
        tv.append(V.var_swap_strike(K, otm, F, T) * T)
    tv = np.array(tv)
    edges = np.concatenate([[0.0], Tg])
    fwd = np.diff(np.concatenate([[0.0], tv])) / np.diff(edges)  # between consecutive expiries
    v0, kappa, theta, xi, rho = _heston_x()
    Th = np.linspace(0, Tg[-1], 200)
    hes = theta + (v0 - theta) * np.exp(-kappa * Th)
    # realized volatility by day of the week (UTC), Binance hourly, 2024-2025: does the market's weekend dip match?
    kl = data.binance_klines("BTCUSDT", "1h", "2024-01", "2025-11")
    t = np.asarray(kl["time"])
    r = np.diff(np.log(np.asarray(kl["close"], float)))
    dow = ((t[1:] // 86400) + 3) % 7  # 0 = Monday
    by_dow = [float(np.sqrt(np.mean(r[dow == d] ** 2) * 24 * 365)) for d in range(7)]
    return _json({"by_dow": by_dow, "edges": edges, "market_fwd_var": fwd, "kvar": np.sqrt(tv / Tg), "T": Tg, "heston_T": Th,
                  "heston_fwd_var": hes})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


# ---------------------------------------------------------------------------
# The expansion (November 2026): every item below is new; the items above keep their names and outputs.

def _ts_year(ts):
    return 1970 + np.asarray(ts, float) / (365.2425 * 86400)


def compute_vol_facts() -> dict:
    """Clustering (the autocorrelation of |r| against r), DVOL's mean reversion (AR(1) on log DVOL), the daily pairs
    of (return, change in log DVOL) for the scatter, and the S&P 500 on 19 October 1987 (Yahoo, 1986-1987)."""
    from scipy.stats import norm

    kl = data.binance_klines("BTCUSDT", "1d", "2021-04", "2025-11")
    t = np.asarray(kl["time"], float)
    c = np.asarray(kl["close"], float)
    r = np.diff(np.log(c))

    def acf(x, L):
        x = x - x.mean()
        return [float(np.dot(x[:-k], x[k:]) / np.dot(x, x)) for k in range(1, L + 1)]

    dv = data.deribit_dvol("2021-04", "2025-11", resolution=86400)
    td = np.asarray(dv["time"], float)
    lv = np.log(np.asarray(dv["close"], float) / 100)
    phi, a = np.polyfit(lv[:-1], lv[1:], 1)
    kap = -np.log(phi) * 365
    days_r = (t[1:] // 86400).astype(int)
    pos = {d: i for i, d in enumerate((td // 86400).astype(int))}
    pairs = [(r[i], lv[pos[d]] - lv[pos[d - 1]], _ts_year(t[i + 1])) for i, d in enumerate(days_r)
             if d in pos and d - 1 in pos]
    pr = np.array(pairs)
    sp = data.yahoo_daily("^GSPC", start="1986-01-01", through="1987-12-31")
    ymd, cl = np.asarray(sp["date"]), np.asarray(sp["close"], float)
    i = int(np.flatnonzero(ymd == 19871019)[0])
    rs = np.diff(np.log(cl))
    r87 = float(rs[i - 1])
    sd = float(np.std(rs[i - 1 - 250:i - 1]))
    z = r87 / sd
    log10p = float(norm.logcdf(z) / np.log(10))
    return _json({"acf_abs": acf(np.abs(r), 60), "acf_ret": acf(r, 60), "ar1_phi": float(phi), "ar1_a": float(a),
                  "dvol_kappa": float(kap), "dvol_halflife_days": float(np.log(2) / -np.log(phi)),
                  "dvol_mean": float(np.exp(a / (1 - phi))),
                  "pairs": pr, "price_t": _ts_year(t), "price": c,
                  "crash1987": {"ret": r87, "sd": sd, "z": float(z), "log10p": log10p, "close_before": float(cl[i - 1]),
                                "close": float(cl[i]), "sd_annual": sd * np.sqrt(252),
                                "years_between": float(10 ** (-log10p) / 252)}})


def compute_mixing() -> dict:
    """Hull-White and Romano-Touzi on the fitted Heston: the conditional Black-Scholes estimator (average Black's
    price over simulated variance paths, with the spot shifted by xi_T) against COS, and plain Monte Carlo from the
    same paths; and the crowd of conditional Gaussians behind the smile, with rho = 0 and with rho fitted."""
    v0, kappa, theta, xi, rho = _heston_x()
    T, n, N = 0.25, 91, 20_000
    k = np.linspace(-0.4, 0.4, 13)
    K = np.exp(k)
    cp = np.where(k >= 0, 1, -1)

    def paths(xi_, rho_, N_, seed):
        S, v = sv.heston_qe(1.0, v0, kappa, theta, xi_, rho_, T, n, N_, seed=seed, return_v=True)
        dt = T / n
        iv = (0.5 * (v[:-1] + v[1:])).sum(0) * dt  # integral of v (trapezoid)
        isw = (v[-1] - v0 - kappa * theta * T + kappa * iv) / xi_  # integral of sqrt(v) dW2, from the v equation
        return S[-1], iv, isw

    ST, iv, isw = paths(xi, rho, N, 131)
    lnxi = rho * isw - 0.5 * rho ** 2 * iv
    sig = np.sqrt((1 - rho ** 2) * iv / T)
    cond = np.array([bs.black(np.exp(lnxi), Kk, T, sig, cp=int(c_)) for Kk, c_ in zip(K, cp)])  # (13, N)
    plain = np.maximum(cp[:, None] * (ST[None, :] - K[:, None]), 0)
    cos = sv.cos_price(lambda u, TT: sv.heston_cf(u, TT, v0, kappa, theta, xi, rho), 1.0, K, T, cp)
    to_iv = lambda p: sv.implied_vols(p, 1.0, K, T, cp)  # noqa: E731
    rows = {"k": k, "cos_iv": to_iv(cos), "cond_iv": to_iv(cond.mean(1)), "plain_iv": to_iv(plain.mean(1)),
            "cond_se": cond.std(1) / np.sqrt(N), "plain_se": plain.std(1) / np.sqrt(N), "cos": cos,
            "cond": cond.mean(1), "plain": plain.mean(1)}
    rows["se_ratio"] = rows["plain_se"] / rows["cond_se"]
    rows["z"] = (rows["cond"] - cos) / rows["cond_se"]
    # the crowd: 40 paths' conditional Gaussians for ln S_T, for vol of vol scaled by s, rho = 0 and rho fitted
    kk = np.linspace(-0.6, 0.6, 49)
    crowd = {}
    for s in (0.0, 0.25, 0.5, 1.0, 2.0):
        for rr, tag in ((0.0, "0"), (rho, "fit")):
            if s == 0 and tag == "fit":
                continue
            if s == 0:
                ivs = np.full(40, v0 * 0 + (theta + (v0 - theta) * (1 - np.exp(-kappa * T)) / (kappa * T)) * T)
                lx = np.zeros(40)
                smile_ = np.sqrt(ivs[0] / T) * np.ones_like(kk)
            else:
                _, ivs, isw_ = paths(xi * s, rr, 40, 7)
                lx = rr * isw_ - 0.5 * rr ** 2 * ivs
                smile_ = sv.model_iv(lambda u, TT: sv.heston_cf(u, TT, v0, kappa, theta, xi * s, rr), 1.0, np.exp(kk), T)
            crowd[f"{s:g}_{tag}"] = {"mean": lx - 0.5 * (1 - rr ** 2) * ivs, "var": (1 - rr ** 2) * ivs, "iv": smile_}
    atm = {f"{s:g}": float(crowd[f"{s:g}_0"]["iv"][24]) for s in (0.0, 0.25, 0.5, 1.0, 2.0)}
    wing = {f"{s:g}": float(0.5 * (crowd[f"{s:g}_0"]["iv"][0] + crowd[f"{s:g}_0"]["iv"][-1])) for s in
            (0.0, 0.25, 0.5, 1.0, 2.0)}
    return _json({"T": T, "N": N, "rows": rows, "kk": kk, "crowd": crowd, "atm": atm, "wing": wing,
                  "params": [v0, kappa, theta, xi, rho]})


def _heston_cf_original(u, T, v0, kappa, theta, xi, rho):
    """Heston's (1993) original form, with g = (b + d) / (b - d) and e^{+dT}: correct, but its complex logarithm
    crosses the branch cut for long maturities."""
    u = np.asarray(u, complex)
    iu = 1j * u
    b = kappa - rho * xi * iu
    d = np.sqrt(b * b + xi * xi * (iu + u * u))
    g = (b + d) / (b - d)
    e = np.exp(d * T)
    C = kappa * theta / xi ** 2 * ((b + d) * T - 2 * np.log((1 - g * e) / (1 - g)))
    D = (b + d) / xi ** 2 * (1 - e) / (1 - g * e)
    return np.exp(C + D * v0)


def compute_trap() -> dict:
    """The 'little trap' (Albrecher, Mayer, Schoutens and Tistaert 2007): where Heston's original form of the
    characteristic function goes wrong on our fitted model and on textbook parameters; the path of its log's
    argument around the origin; the price error it causes; the CF itself as a helix; the Fang-Oosterlee benchmark."""
    x = _heston_x()
    u = np.linspace(1e-6, 60, 6001)
    sets = {"fit": list(x), "textbook": [0.04, 1.5, 0.04, 1.0, -0.7]}
    out = {"sets": sets, "first_wrong": {}, "prices": {}}
    for name, p in sets.items():
        for T in (0.25, 1.0, 3.0):
            with np.errstate(all="ignore"):
                a = sv.heston_cf(u, T, *p)
                b = _heston_cf_original(u, T, *p)
            ok = np.isfinite(b)
            bad = ~ok | (np.abs(a - b) > 1e-6 * np.maximum(1, np.abs(a)))
            bad &= np.abs(a) > 1e-12
            j = int(np.flatnonzero(bad)[0]) if bad.any() else -1
            out["first_wrong"][f"{name}_{T:g}"] = {"u": float(u[j]) if j >= 0 else None,
                                                   "abs_phi": float(np.abs(a[j])) if j >= 0 else 0.0,
                                                   "n_wrong": int(bad.sum())}
            Ks = np.array([0.7, 1.0, 1.3])

            def naive(uu, TT, p=p):
                uu = np.asarray(uu, complex)
                if np.any(uu.imag != 0):  # the cumulants that set COS's range: taken from the correct form
                    return sv.heston_cf(uu, TT, *p)
                with np.errstate(all="ignore"):
                    z = _heston_cf_original(uu, TT, *p)
                z = np.where(uu == 0, 1.0, z)  # 0/0 at u = 0, where phi = 1
                return np.where(np.isfinite(z), z, 0)

            pa = sv.cos_price(lambda uu, TT: sv.heston_cf(uu, TT, *p), 1.0, Ks, T, 1)
            pb = sv.cos_price(naive, 1.0, Ks, T, 1)
            out["prices"][f"{name}_{T:g}"] = {"K": Ks, "little": pa, "original": pb,
                                              "iv_little": sv.implied_vols(pa, 1.0, Ks, T, 1),
                                              "iv_original": [float(bs.implied_vol(float(q), 1.0, float(k_), T, 0, 0, 1))
                                                              if 0 < q < 1 else float("nan") for q, k_ in zip(pb, Ks)]}
    # the argument of the logarithm, z(u), for u in [0, 20], T = 1, on our fit
    v0, kappa, theta, xi, rho = x
    uu = np.linspace(1e-6, 20, 801)
    iu = 1j * uu
    bb = kappa - rho * xi * iu
    d = np.sqrt(bb * bb + xi * xi * (iu + uu * uu))
    T = 1.0
    g1 = (bb + d) / (bb - d)
    z_orig = (1 - g1 * np.exp(d * T)) / (1 - g1)
    g2 = (bb - d) / (bb + d)
    z_lt = (1 - g2 * np.exp(-d * T)) / (1 - g2)
    cross = np.flatnonzero((np.imag(z_orig[:-1]) * np.imag(z_orig[1:]) < 0) & (np.real(z_orig[:-1]) < 0))
    out["winding"] = {"u": uu, "orig_re": z_orig.real, "orig_im": z_orig.imag, "lt_re": z_lt.real, "lt_im": z_lt.imag,
                      "cross_u": uu[cross]}
    # the CF as a helix, 30 days and one year
    uh = np.linspace(0, 16, 321)
    out["helix"] = {}
    for T in (30 / 365, 0.25):
        ph = sv.heston_cf(uh, T, *x)
        out["helix"][f"{round(T * 365)}"] = {"u": uh, "re": ph.real, "im": ph.imag}
    cf = lambda uu_, TT: sv.heston_cf(uu_, TT, 0.0175, 1.5768, 0.0398, 0.5751, -0.5711)  # noqa: E731
    out["benchmark"] = {"cos": float(sv.cos_price(cf, 100.0, 100.0, 1.0, 1)[0]), "ref": 5.785155435}
    out["benchmark"]["err"] = abs(out["benchmark"]["cos"] - 5.785155435)
    return _json(out)


def _thin_trace(tr, keep=400):
    """A calibration trace as (evaluation, rmse, best-so-far rmse, x), thinned to at most ``keep`` rows; the
    best-so-far x is carried with it."""
    ev = np.array([e[0] for e in tr], float)
    rm = np.array([e[1] for e in tr], float)
    rm = np.where(np.isfinite(rm), rm, np.nan)
    best = np.fmin.accumulate(np.where(np.isfinite(rm), rm, np.inf))
    bi, xs = 0, []
    for i in range(len(tr)):
        if rm[i] <= best[i] + 1e-15:
            bi = i
        xs.append(tr[bi][2])
    idx = np.unique(np.linspace(0, len(tr) - 1, min(keep, len(tr))).astype(int))
    return {"eval": ev[idx], "rmse": np.minimum(rm[idx], 60), "best": best[idx], "x": np.array(xs)[idx]}


def _checkpoints(best, n=8):
    """Indices into a thinned trace where the best-so-far loss reaches successive levels between start and end."""
    b = np.asarray(best)
    lv = np.exp(np.linspace(np.log(b[0]), np.log(b[-1]), n))
    out = sorted({int(np.argmax(b <= v + 1e-12)) for v in lv} | {0, len(b) - 1})
    return out


SURF_K = np.linspace(-0.4, 0.4, 17)


def _surface_grid(name, x, Ts):
    return np.array([sv.surface_iv(name, x, 1.0, np.exp(SURF_K), T) for T in Ts])


def compute_heston_replay() -> dict:
    """The Heston calibration of the Surface, replayed: every residual evaluation from the default start and two
    random starts, the model surface rebuilt at checkpoints of the default run, and the vega-weighted implied-vol
    error at those checkpoints (the calibrator's own loss is a price-over-vega approximation of it)."""
    Q = _quotes()
    g = np.random.default_rng(13)
    starts = [None]
    for _ in range(2):
        starts.append([g.uniform(0.05, 0.6), np.exp(g.uniform(np.log(0.5), np.log(20))), g.uniform(0.05, 0.6),
                       np.exp(g.uniform(np.log(0.3), np.log(6))), g.uniform(-0.8, 0.5)])
    runs = []
    for s0 in starts:
        r = sv.calibrate("Heston", Q, x0=s0, trace=True)
        runs.append({"x0": s0 if s0 is not None else list(sv.MODELS["Heston"]["x0"]), "x": r["x"], "rmse": r["rmse"],
                     "nfev": r["nfev"], "n_eval": len(r["trace"]), "trace": _thin_trace(r["trace"])})
    Ts = np.unique(Q["T"])
    tr = runs[0]["trace"]
    ck = _checkpoints(tr["best"])
    frames = []
    for i in ck:
        x = tr["x"][i]
        iv = _model_iv_all("Heston", x, Q)
        frames.append({"i": i, "x": x, "grid": _surface_grid("Heston", x, Ts), "iv_rmse": _rmse(iv, Q)})
    return _json({"runs": runs, "frames": frames, "T": Ts, "k": SURF_K, "quotes": {"k": Q["k"], "T": Q["T"], "iv": Q["iv"]},
                  "bs_rmse": load("calibrate")["fits"]["BS"]["rmse"]})


def compute_heston_sliders() -> dict:
    """What each Heston parameter does: the fitted model's surface with one parameter moved at a time (five values
    each), and the short-maturity skew against rho xi / (4 sqrt v0)."""
    x = np.array(_heston_x())
    Ts = np.array([3, 9, 30, 90, 289]) / 365
    vals = {"v0": [0.08, 0.15, x[0], 0.35, 0.5], "kappa": [1.0, 4.0, x[1], 30.0, 60.0],
            "theta": [0.1, 0.18, x[2], 0.4, 0.6], "xi": [0.5, 2.0, x[3], 6.0, 8.0], "rho": [-0.8, -0.5, x[4], 0.0, 0.4]}
    names = ("v0", "kappa", "theta", "xi", "rho")
    out = {"T": Ts, "k": SURF_K, "base": x, "vals": vals, "grids": {}}
    for j, n in enumerate(names):
        out["grids"][n] = []
        for v in vals[n]:
            y = x.copy()
            y[j] = v
            out["grids"][n].append(_surface_grid("Heston", y, Ts))
    v0, kappa, theta, xi, rho = x
    sk = sv.surface_iv("Heston", x, 1.0, np.exp(np.array([-0.005, 0.005])), 2 / 365)
    out["skew_2d"] = float((sk[1] - sk[0]) / 0.01)
    out["skew_formula"] = float(rho * xi / (4 * np.sqrt(v0)))
    return _json(out)


def compute_qe_density() -> dict:
    """One step of the fitted Heston variance: full-truncation Euler (and its negative mass) and Andersen's QE
    against the exact scaled non-central chi-squared law: the first two moments, the Kolmogorov-Smirnov distance and
    the transport (Wasserstein-1) distance; histograms for the picture."""
    from scipy.stats import ncx2

    v0f, kappa, theta, xi, rho = _heston_x()
    N = 100_000

    def exact_cdf(v, dt, x):
        E = np.exp(-kappa * dt)
        c = xi * xi * (1 - E) / (4 * kappa)
        return ncx2.cdf(np.asarray(x) / c, 4 * kappa * theta / (xi * xi), 4 * kappa * E * v / (xi * xi * (1 - E)))

    def ks(sample, v, dt):
        s = np.sort(sample)
        F = exact_cdf(v, dt, s)
        i = np.arange(1, len(s) + 1)
        return float(max(np.max(i / len(s) - F), np.max(F - (i - 1) / len(s))))

    def w1(sample, v, dt):  # the transport distance: how far probability must move, int |F_n - F| dv
        s = np.sort(sample)
        x = np.linspace(0, max(s[-1], 1e-9) * 1.05, 4000)
        Fn = np.searchsorted(s, x, side="right") / len(s)
        return float(np.trapezoid(np.abs(Fn - exact_cdf(v, dt, x)), x))

    rows, hist = [], {}
    g = np.random.default_rng(5)
    for v in (0.05, theta, 0.5):
        for dt, tag in ((1 / 365, "day"), (1 / 52, "week"), (1 / 12, "month")):
            raw = v + kappa * (theta - v) * dt + xi * np.sqrt(v * dt) * g.standard_normal(N)
            eu = np.maximum(raw, 0)
            _, vs = sv.heston_qe(1.0, v, kappa, theta, xi, rho, dt, 1, N, seed=17, return_v=True)
            qe = vs[1]
            E = np.exp(-kappa * dt)
            m = theta + (v - theta) * E
            s2 = v * xi ** 2 * E / kappa * (1 - E) + theta * xi ** 2 / (2 * kappa) * (1 - E) ** 2
            rows.append({"v": float(v), "dt": tag, "psi": float(s2 / m ** 2), "neg": float((raw < 0).mean()),
                         "ks_euler": ks(eu, v, dt), "ks_qe": ks(qe, v, dt), "zero_euler": float((eu == 0).mean()),
                         "zero_qe": float((qe == 0).mean()), "exact_zero": 0.0,
                         "mean_exact": float(m), "mean_euler": float(eu.mean()), "mean_qe": float(qe.mean()),
                         "var_exact": float(s2), "var_euler": float(eu.var()), "var_qe": float(qe.var()),
                         "w1_euler": w1(eu, v, dt), "w1_qe": w1(qe, v, dt),
                         "exact_below": float(exact_cdf(v, dt, 0.01 * m))})
            if tag == "week" and v in (0.05, 0.5):
                hi = 0.4 if v == 0.05 else 1.4
                lo = -0.3 if v == 0.05 else -0.2
                edges = np.linspace(lo, hi, 71)
                xs = 0.5 * (edges[1:] + edges[:-1])
                cdf = exact_cdf(v, dt, np.maximum(edges, 0))
                hist[f"{v:g}"] = {"edges": edges, "euler_raw": np.histogram(raw, edges)[0] / N,
                                  "euler": np.histogram(eu, edges)[0] / N, "qe": np.histogram(qe, edges)[0] / N,
                                  "exact": np.diff(cdf), "x": xs, "qe_zero": float((qe == 0).mean()),
                                  "euler_zero": float((eu == 0).mean())}
    return _json({"rows": rows, "hist": hist, "params": [v0f, kappa, theta, xi, rho], "N": N})


def compute_sabr_replay() -> dict:
    """SABR (beta = 1) fitted slice by slice, every least-squares evaluation recorded: the curve at checkpoints, and
    the expansion's skew rho nu / 2 and curvature against the formula's own finite differences."""
    Q = _quotes()
    out = []
    for T in np.unique(Q["T"]):
        m = Q["T"] == T
        if m.sum() < 6:
            continue
        F = float(Q["F"][m][0])
        K, iv, w = Q["K"][m], Q["iv"][m], np.sqrt(Q["vega"][m] / Q["vega"][m].mean())
        log = []

        def f(p):
            e = (sv.sabr_iv(F, K, T, p[0], 1.0, p[1], p[2]) - iv) * w * 100
            log.append((len(log), float(np.sqrt(np.mean(e ** 2))), [float(z) for z in p]))
            return e

        r = least_squares(f, [float(np.median(iv)), -0.1, 1.5], bounds=([0.01, -0.999, 0.01], [5, 0.999, 20]))
        tr = _thin_trace(log, keep=200)
        ck = _checkpoints(tr["best"], n=6)
        kq = np.log(K / F)
        kk = np.linspace(kq.min() - 0.02, kq.max() + 0.02, 41)
        curves = [sv.sabr_iv(1.0, np.exp(kk), T, tr["x"][i][0], 1.0, tr["x"][i][1], tr["x"][i][2]) for i in ck]
        a, rh, nu = r.x
        h = 1e-3
        s_ = lambda kv: sv.sabr_iv(1.0, np.exp(np.atleast_1d(kv)), T, a, 1.0, rh, nu)[0]  # noqa: E731
        fac = 1 + (rh * nu * a / 4 + (2 - 3 * rh ** 2) / 24 * nu ** 2) * T
        out.append({"days": int(round(T * 365)), "T": float(T), "k": kq, "iv": iv, "kk": kk, "curves": curves,
                    "ck": ck, "trace": tr, "x": r.x, "skew_num": float((s_(h) - s_(-h)) / (2 * h)),
                    "skew_formula": float(rh * nu / 2 * fac),
                    "curv_num": float((s_(h) - 2 * s_(0.0) + s_(-h)) / h ** 2),
                    "curv_formula": float((2 - 3 * rh ** 2) * nu ** 2 / (6 * a) * fac)})
    return _json({"slices": out})


def compute_sabr_pde() -> dict:
    """Arbitrage-free SABR (Hagan et al. 2014) on the rates-like example of the sabr item: the density solved
    forward to 10 years, its mass and the masses absorbed at zero, the implied vols it prices against Hagan's
    formula, and Hagan's own density at the same dates (negative at long maturities)."""
    Fr, al, be, rh, nu = 0.03, 0.035, 0.5, -0.3, 0.4
    snaps = (0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0)
    K = np.linspace(0.005, 0.09, 35)
    r = sv.sabr_pde_density(Fr, al, be, rh, nu, 10.0, n=480, f_max=0.24, n_t=4000, snaps=snaps, K=K)
    Fc = r["F"]
    keep = Fc <= 0.12
    sheet = []
    for s in r["snaps"]:
        T = s["T"]
        with np.errstate(all="ignore"):
            hd = sv.sabr_density(Fr, Fc[keep][::2], T, al, be, rh, nu, h=1e-5)
        sheet.append({"T": T, "Q": s["Q"][keep][::2], "QL": s["QL"], "QR": s["QR"], "hagan": hd})
    pde_iv = np.array([bs.implied_vol(float(c_), Fr, float(k), 10.0, 0, 0, 1) if c_ > max(Fr - k, 0) + 1e-14 else np.nan
                       for c_, k in zip(r["call"], K)])
    hag_iv = sv.sabr_iv(Fr, K, 10.0, al, be, rh, nu)
    atm = sv.sabr_pde_density(Fr, al, be, rh, nu, 10.0, n=480, f_max=0.24, n_t=4000, K=[Fr])
    atm_iv = float(bs.implied_vol(float(atm["call"][0]), Fr, Fr, 10.0, 0, 0, 1))
    return _json({"F": Fc[keep][::2], "sheet": sheet, "mass": r["mass"], "mean": r["mean"], "QL": r["QL"], "QR": r["QR"],
                  "min_Q": float(r["Q"].min()), "K": K, "pde_iv": pde_iv, "hagan_iv": hag_iv, "atm_pde": atm_iv,
                  "atm_hagan": float(sv.sabr_iv(Fr, Fr, 10.0, al, be, rh, nu)[0]),
                  "params": {"F": Fr, "alpha": al, "beta": be, "rho": rh, "nu": nu}, "n": 480, "n_t": 4000})


CGMY_INF = dict(lo=(1e-4, 0.5, 1.5, 1.05), hi=(50.0, 60.0, 60.0, 1.95), x0=(0.05, 5.0, 8.0, 1.5))


def compute_levy_fits() -> dict:
    """Merton, Kou and CGMY (on both sides of Y = 1) fitted to the Surface by the House's calibrator, with VG and NIG
    refitted with their traces for the race; vega-weighted implied-vol errors overall and by expiry; the three
    slices' smiles."""
    Q = _quotes()
    c = load("calibrate")
    out = {"fits": {}}
    specs = {"Merton": {}, "Kou": {}, "CGMY": {}, "CGMY_inf": CGMY_INF, "VG": {}, "NIG": {}}
    for tag, kw in specs.items():
        name = "CGMY" if tag.startswith("CGMY") else tag
        r = sv.calibrate(name, Q, x0=kw.get("x0"), lo=kw.get("lo"), hi=kw.get("hi"), max_nfev=300, trace=True)
        iv = _model_iv_all(name, r["x"], Q)
        ok = np.isfinite(iv)
        by = {int(round(T * 365)): _rmse(np.where(ok, iv, 0), Q, (Q["T"] == T) & ok) for T in np.unique(Q["T"])}
        out["fits"][tag] = {"model": name, "params": r["params"], "x": r["x"], "rmse": r["rmse"],
                            "rmse_iv": _rmse(np.where(ok, iv, 0), Q, ok), "by_expiry": by, "nfev": r["nfev"],
                            "trace": _thin_trace(r["trace"], keep=250)}
        print(f"   {tag}: {out['fits'][tag]['rmse_iv']:.2f} vol points, {r['params']}", flush=True)
    shown = []
    for sl in c["shown"]:
        T = Q["T"][np.argmin(np.abs(Q["T"] * 365 - sl["days"]))]
        F = float(Q["F"][Q["T"] == T][0])
        kk = np.asarray(sl["kk"])
        shown.append({"days": sl["days"], "curves": {t: sv.surface_iv(f["model"], f["x"], F, F * np.exp(kk), T)
                                                     for t, f in out["fits"].items() if t in ("Merton", "Kou", "CGMY_inf")}})
    out["shown"] = shown
    return _json(out)


def compute_bates_replay() -> dict:
    """Bates fitted to the Surface from the three starts of the calibrate item, every evaluation recorded: watch the
    jump intensity run to its bound while the jump size shrinks to its floor."""
    Q = _quotes()
    starts = [None, (0.15, 3, 0.25, 1.5, -0.3, 0.5, -0.1, 0.2), (0.15, 3, 0.25, 1.5, -0.3, 3, 0.0, 0.15)]
    runs = []
    for s0 in starts:
        r = sv.calibrate("Bates", Q, x0=s0, trace=True)
        runs.append({"x0": s0 if s0 is not None else list(sv.MODELS["Bates"]["x0"]), "x": r["x"], "rmse": r["rmse"],
                     "trace": _thin_trace(r["trace"], keep=300)})
    return _json({"runs": runs, "hi": sv.MODELS["Bates"]["hi"], "lo": sv.MODELS["Bates"]["lo"]})


def _cgmy_path(C, G, M, Y, T, n, seed, eps=1e-3):
    """An illustrative CGMY path: jumps larger than eps as a compound Poisson process (sizes by inverse transform on
    a grid), the small jumps as a Brownian motion of the same variance (Asmussen and Rosinski 2001)."""
    g = np.random.default_rng(seed)
    x = np.exp(np.linspace(np.log(eps), np.log(3.0), 4000))
    dens_p = C * np.exp(-M * x) / x ** (1 + Y)
    dens_n = C * np.exp(-G * x) / x ** (1 + Y)
    dx = np.diff(x)
    mp = np.concatenate([[0], np.cumsum(0.5 * (dens_p[1:] + dens_p[:-1]) * dx)])
    mn = np.concatenate([[0], np.cumsum(0.5 * (dens_n[1:] + dens_n[:-1]) * dx)])
    lam_p, lam_n = mp[-1], mn[-1]
    s2 = 2 * C * eps ** (2 - Y) / (2 - Y)  # small jumps' variance per unit time (untempered, eps small)
    dt = T / n
    X = np.zeros(n + 1)
    for i in range(n):
        npj, nnj = g.poisson(lam_p * dt), g.poisson(lam_n * dt)
        up = np.interp(g.random(npj) * lam_p, mp, x).sum() if npj else 0.0
        dn = np.interp(g.random(nnj) * lam_n, mn, x).sum() if nnj else 0.0
        X[i + 1] = X[i] + up - dn + np.sqrt(s2 * dt) * g.standard_normal()
    return X, float(lam_p + lam_n)


def compute_lab_vg() -> dict:
    """Variance gamma, priced two ways: COS against 200,000 simulated paths for a 30-day at-the-money call under the
    fitted VG; the gamma clock (illustrative nu = 0.25) turning one Brownian path into a VG path; CGMY paths for three
    values of Y."""
    s, nu, th = load("calibrate")["fits"]["VG"]["x"]
    T = 30 / 365
    cos = float(sv.cos_price(lambda u, TT: sv.vg_cf(u, TT, s, nu, th), 1.0, 1.0, T, 1)[0])
    S = sv.vg_paths(1.0, s, nu, th, T, 30, 200_000, seed=11)
    pay = np.maximum(S[-1] - 1.0, 0)
    g = np.random.default_rng(21)
    n, Tc, nu_c = 240, 0.25, 0.25
    G = g.gamma(Tc / n / nu_c, nu_c, n)  # gamma clock increments: mean dt, variance nu dt
    Z = g.standard_normal(n)
    W_bus = np.concatenate([[0], np.cumsum(np.sqrt(Tc / n) * Z)])  # the same normals in business time
    X_vg = np.concatenate([[0], np.cumsum(0.6 * np.sqrt(G) * Z)])
    clock = np.concatenate([[0], np.cumsum(G)])
    paths = {}
    for Y in (-0.5, 0.5, 1.5):
        from scipy.special import gamma as Gf
        C = 0.25 / (Gf(2 - Y) * 2 * 5.0 ** (Y - 2))  # annual variance 0.25 with G = M = 5
        X, lam = _cgmy_path(C, 5.0, 5.0, Y, 1.0, 1000, seed=31)
        paths[f"{Y:g}"] = {"X": X, "C": C, "lam_eps": lam}
    return _json({"cos": cos, "mc": float(pay.mean()), "se": float(pay.std() / np.sqrt(len(pay))), "n": len(pay),
                  "params": [s, nu, th], "clock": {"t": np.linspace(0, Tc, n + 1), "G": clock, "W": W_bus * 0.6,
                                                   "X": X_vg, "nu": nu_c, "sigma": 0.6},
                  "cgmy": paths})


def _local_slope(T, sk, lo, hi):
    T, sk = np.asarray(T), np.abs(np.asarray(sk))
    m = (T >= lo) & (T <= hi) & (sk > 1e-6)
    return float(np.polyfit(np.log(T[m]), np.log(sk[m]), 1)[0]) if m.sum() >= 2 else float("nan")


def compute_skew_more() -> dict:
    """The term structure of the ATM skew for every model (the skew item's four plus Merton, Kou, CGMY and the SABR
    slices), local power-law slopes on 2-14 and 60-365 days, and smiles at twelve maturities for the small
    multiples."""
    s = load("skew")
    lf = load("levy_fits")["fits"]
    c = load("calibrate")
    Ts = np.asarray(s["T"])
    models = {k: list(v) for k, v in s["models"].items()}
    xs = {n: c["fits"][n]["x"] for n in ("Heston", "Bates", "VG", "NIG")}
    for tag in ("Merton", "Kou", "CGMY_inf"):
        f = lf[tag]
        xs[tag] = f["x"]
        sk = []
        for T in Ts:
            iv = sv.surface_iv(f["model"], f["x"], 1.0, np.exp(np.array([-0.01, 0.01])), T)
            sk.append(float((iv[1] - iv[0]) / 0.02))
        models[tag] = sk
    sabr = []
    for d, p in c["sabr"].items():
        T = int(d) / 365
        iv = sv.sabr_iv(1.0, np.exp(np.array([-0.01, 0.01])), T, p["alpha"], 1.0, p["rho"], p["nu"])
        sabr.append({"T": T, "skew": float((iv[1] - iv[0]) / 0.02)})
    slopes = {n: {"short": _local_slope(Ts, v, 2 / 365, 14 / 365), "long": _local_slope(Ts, v, 60 / 365, 1.0)}
              for n, v in models.items()}
    mk = s["market"]
    slopes["market"] = {"all": s["power"],
                        "short": _local_slope([r["T"] for r in mk], [r["skew"] for r in mk], 2 / 365, 17 / 365),
                        "long": _local_slope([r["T"] for r in mk], [r["skew"] for r in mk], 50 / 365, 1.0)}
    slopes["SABR"] = {"all": _local_slope([r["T"] for r in sabr], [r["skew"] for r in sabr], 0, 2)}
    Tm = np.exp(np.linspace(np.log(1.0), np.log(2 / 365), 12))
    z = np.linspace(-2.5, 2.5, 21)
    small = {}
    for n in ("Heston", "Bates", "Merton", "VG", "NIG", "CGMY_inf"):
        name = {"CGMY_inf": "CGMY"}.get(n, n)
        small[n] = [sv.surface_iv(name, xs[n], 1.0, np.exp(z * 0.5 * np.sqrt(T)), T) for T in Tm]
    return _json({"T": Ts, "models": models, "sabr": sabr, "slopes": slopes, "market": mk, "Tm": Tm, "z": z,
                  "small": small})


def _reprice(X, fit, k=np.linspace(-0.3, 0.3, 13), days=(30, 60, 90, 120)):
    out = []
    for d in days:
        T = d / 365
        mc = _iv_from_paths(X[d], k, T)
        tgt = np.sqrt(_ssvi_w(fit, k, T) / T)
        out.append(float(np.sqrt(np.nanmean((mc - tgt) ** 2)) * 100))
    return out


def compute_slv_particles() -> dict:
    """The particle method's convergence: repricing error against the number of particles (2,000, 8,000, 40,000),
    three seeds each, and against the kernel bandwidth at 8,000; and a small live run whose particle cloud, E[v | x]
    and leverage are kept at a few dates for the picture."""
    fit, _ = _ssvi()
    lv = _lv_fn(fit)
    x = _heston_x()
    Ns, seeds, bws = (2000, 8000, 40000), (1, 2, 3), (0.5, 2.0)
    part = CACHE.partial("slv_particles", {"Ns": Ns, "seeds": seeds, "bws": bws, "v": 1})
    for N in Ns:
        for s in seeds:
            key = f"{N}_{s}"
            if key not in part:
                X = sv.slv_paths(lv, x, 120, N, mix=0.5, n_sub=min(8000, N), seed=s)
                part[key] = _reprice(X, fit)
                print(f"   slv N={N} seed={s}: {part[key]}", flush=True)
    for b in bws:
        for s in seeds:
            key = f"bw{b:g}_{s}"
            if key not in part:
                X = sv.slv_paths(lv, x, 120, 8000, mix=0.5, n_sub=8000, seed=s, bw_mult=b)
                part[key] = _reprice(X, fit)
                print(f"   slv bw={b} seed={s}: {part[key]}", flush=True)
    info = {}
    snap_days = (1, 2, 3, 4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 50, 60)
    sv.slv_paths(lv, x, 60, 8000, mix=0.5, n_sub=8000, seed=4, info=info, snap_days=snap_days, n_snap=900,
                 grid=np.linspace(-0.6, 0.6, 61))
    grid = info["grid"]
    lv_grid = [lv(grid, s_["day"] / 365) for s_ in info["snaps"]]
    res = {"days": [30, 60, 90, 120], "Ns": Ns, "seeds": seeds, "bws": bws,
           "err": {k: part[k] for k in part.done}, "grid": grid, "snaps": info["snaps"], "lv": lv_grid}
    part.finish()
    return _json(res)


def compute_mixing_sweep() -> dict:
    """The mixing fraction eta swept from 0 (local vol driven by particles) to 1 (Heston's full vol of vol), 40,000
    particles each: the repricing error, the leverage at 60 days, the 30-day forward smile in 60 days, the cliquet and
    the forward-start price. Three seeds at eta = 1/2 (seed 7 is the exotics item's SLV)."""
    fit, _ = _ssvi()
    lv = _lv_fn(fit)
    x = _heston_x()
    k = np.linspace(-0.25, 0.25, 11)
    runs = [(e, 7) for e in (0.0, 0.25, 0.5, 0.75, 1.0)] + [(0.5, 8), (0.5, 9)]
    part = CACHE.partial("mixing_sweep", {"runs": runs, "v": 1})
    for e, s in runs:
        key = f"{e:g}_{s}"
        if key in part:
            continue
        info = {}
        X = sv.slv_paths(lv, x, 120, 40_000, mix=e, n_sub=8000, seed=s, info=info)
        S = np.exp(X)
        fwd = _iv_from_paths(X[90] - X[60], k, 30 / 365)
        L60 = next(z["L"] for z in info["L"] if round(z["t"] * 365) == 60)
        part[key] = _json({"eta": e, "seed": s, "reprice": _reprice(X, fit), "fwd_iv": fwd, "fwd_atm": float(fwd[5]),
                     "fwd_skew": float(fwd[3] - fwd[7]), "cliquet": sv.cliquet(S, [0, 30, 60, 90, 120], cap=0.10,
                                                                                  floor=0.0, gfloor=0.0),
                     "forward_start": sv.forward_start(S, 60, 90), "L60": L60})
        print(f"   eta={e} seed={s}: cliquet {part[key]['cliquet']:.4f}, fwd skew {part[key]['fwd_skew']:.4f}, "
              f"err {part[key]['reprice']}", flush=True)
    res = {"k": k, "grid": np.linspace(-1.0, 1.0, 81), "runs": [part[f"{e:g}_{s}"] for e, s in runs]}
    part.finish()
    return _json(res)


BERGOMI = {"k1": 8.0, "k2": 0.35, "theta": 0.25, "rho12": 0.0}


def _bergomi_vol(tau, omega, p=BERGOMI):
    k1, k2, th, r12 = p["k1"], p["k2"], p["theta"], p["rho12"]
    a = 1 / np.sqrt((1 - th) ** 2 + th ** 2 + 2 * r12 * th * (1 - th))
    return omega * a * np.sqrt((1 - th) ** 2 * np.exp(-2 * k1 * tau) + th ** 2 * np.exp(-2 * k2 * tau)
                               + 2 * r12 * th * (1 - th) * np.exp(-(k1 + k2) * tau))


def compute_bergomi_sim() -> dict:
    """Bergomi's two-factor model of the forward variance curve, started from the Surface's curve (the bergomi
    item): illustrative factor speeds (k1 = 8, k2 = 0.35, theta = 0.25, uncorrelated), with omega set so the model's
    30-day vol index has DVOL's measured vol of vol. 2,000 curves for 120 days; one ribbon to draw; the martingale
    check; Heston's curve, which moves as one exponential, for contrast."""
    b = load("bergomi")
    f = load("facts")
    edges, fv = np.asarray(b["edges"]), np.asarray(b["market_fwd_var"])
    Tg = np.linspace(0, 300, 61) / 365

    def xi0(T):
        j = np.clip(np.searchsorted(edges, T, side="right") - 1, 0, len(fv) - 1)
        return fv[j]

    # omega: the vol of the 30-day variance-swap rate's log is (1/30d) int vol(tau) dtau times xi share; for a vol
    # index (sqrt) halve it; match DVOL's vol of vol
    taus = np.linspace(0, 30 / 365, 301)
    unit = float(np.trapezoid(_bergomi_vol(taus, 1.0), taus) / (30 / 365))
    omega = 2 * f["volvol"] / unit
    p = BERGOMI
    a = 1 / np.sqrt((1 - p["theta"]) ** 2 + p["theta"] ** 2)
    g = np.random.default_rng(23)
    n_days, N = 120, 2000
    dt = 1 / 365
    X1 = np.zeros(N)
    X2 = np.zeros(N)
    ribbon, mean_at = [], {}
    var1 = var2 = 0.0
    for d in range(n_days + 1):
        t = d * dt
        T = t + Tg  # the curve's dates, from t forward
        tau = T - t
        xT = a * ((1 - p["theta"]) * np.exp(-p["k1"] * tau)[None, :] * X1[:, None]
                  + p["theta"] * np.exp(-p["k2"] * tau)[None, :] * X2[:, None])
        varx = a ** 2 * ((1 - p["theta"]) ** 2 * np.exp(-2 * p["k1"] * tau) * var1
                         + p["theta"] ** 2 * np.exp(-2 * p["k2"] * tau) * var2)
        curve_ = xi0(T)[None, :] * np.exp(omega * xT - 0.5 * omega ** 2 * varx[None, :])
        if d % 2 == 0:
            ribbon.append(curve_[0])
        if d in (30, 60, 120):
            mean_at[str(d)] = {"mean": curve_.mean(0), "xi0": xi0(T), "T": T}
        z1, z2 = g.standard_normal(N), g.standard_normal(N)
        X1 = X1 * np.exp(-p["k1"] * dt) + np.sqrt((1 - np.exp(-2 * p["k1"] * dt)) / (2 * p["k1"])) * z1
        X2 = X2 * np.exp(-p["k2"] * dt) + np.sqrt((1 - np.exp(-2 * p["k2"] * dt)) / (2 * p["k2"])) * z2
        var1 = var1 * np.exp(-2 * p["k1"] * dt) + (1 - np.exp(-2 * p["k1"] * dt)) / (2 * p["k1"])
        var2 = var2 * np.exp(-2 * p["k2"] * dt) + (1 - np.exp(-2 * p["k2"] * dt)) / (2 * p["k2"])
    v0, kappa, theta, xi, rho = _heston_x()
    _, v = sv.heston_qe(1.0, v0, kappa, theta, xi, rho, n_days / 365, n_days * 4, 1, seed=23, return_v=True)
    hes = [theta + (v[4 * d, 0] - theta) * np.exp(-kappa * Tg) for d in range(0, n_days + 1, 2)]
    tau_v = np.linspace(0, 1, 101)
    return _json({"Tg": Tg, "ribbon": np.array(ribbon), "heston_ribbon": np.array(hes), "t": np.arange(0, n_days + 1, 2) / 365,
                  "mean_at": mean_at, "omega": omega, "params": p, "tau": tau_v,
                  "volvol_bergomi": _bergomi_vol(tau_v, omega),
                  "volvol_heston": xi * np.sqrt(v0) * np.exp(-kappa * tau_v) / (theta + (v0 - theta) * np.exp(-kappa * tau_v)),
                  "dvol_volvol": f["volvol"]})


def compute_ssr() -> dict:
    """The skew-stickiness ratio of the fitted Heston by maturity: R = (d sigma_ATM / d ln S) / skew, with the
    regression E[dv | d ln S] = rho xi d ln S, by COS finite differences in v0. Local vol's short-maturity value is 2."""
    v0, ka, th, xi, rho = _heston_x()

    def atm_skew(v, T):
        iv = sv.surface_iv("Heston", [v, ka, th, xi, rho], 1.0, np.exp(np.array([-0.01, 0.0, 0.01])), T)
        return iv[1], (iv[2] - iv[0]) / 0.02

    rows = []
    for d in (2, 7, 14, 30, 60, 90, 180, 365):
        T = d / 365
        a0, sk = atm_skew(v0, T)
        h = 1e-3
        da = (atm_skew(v0 + h, T)[0] - atm_skew(v0 - h, T)[0]) / (2 * h)
        rows.append({"days": d, "atm": float(a0), "skew": float(sk), "R": float(da * rho * xi / sk)})
    return _json({"rows": rows})


def compute_fwd_semi() -> dict:
    """Heston's forward smile two ways: the one-dimensional integral over the law of v at 60 days (COS inside),
    against Monte Carlo from three seeds (40,000 paths each) and the estimate as paths accumulate; and three paths'
    monthly returns for the cliquet picture."""
    x = _heston_x()
    k = np.asarray(load("exotics")["k"])
    T1, tau = 60 / 365, 30 / 365
    p = sv.heston_forward_start(x, T1, tau, k, n=400)
    semi = sv.implied_vols(p, 1.0, np.exp(k), tau, 1)
    seeds = {}
    acc = {}
    for s in (7, 8, 9):
        X = _simulate("Heston", seed=s)
        r = X[90] - X[60]
        seeds[str(s)] = _iv_from_paths(r, k, tau)
        if s == 7:
            for n in (500, 1000, 2000, 5000, 10000, 20000, 40000):
                acc[str(n)] = _iv_from_paths(r[:n], k, tau)
            Sm = np.exp(X[[0, 30, 60, 90, 120]][:, :3])
            mret = Sm[1:] / Sm[:-1] - 1
            pay = np.maximum(np.exp(r) - np.exp(k[:, None]), 0)
            se = pay.std(1) / np.sqrt(len(r))
    return _json({"k": k, "semi_iv": semi, "semi": p, "mc": seeds, "acc": acc, "mc_se_price": se, "monthly": mret,
                  "T1": T1, "tau": tau})


def compute_vol_puzzle() -> dict:
    """The SPX/VIX puzzle in bitcoin's form: the fitted Heston's (and Bates's) own 30-day vol index, simulated over
    four years (xi is the same under P and Q), against DVOL; its realized vol of vol and its correlation with returns;
    the implied vols of options on that index (30 and 90 days) with the hard floor; Jensen's gap."""
    f = load("facts")
    c = load("calibrate")["fits"]
    out = {"dvol_volvol": f["volvol"], "dvol_corr": f["leverage_corr"], "models": {}}
    tau = 30 / 365
    for name in ("Heston", "Bates"):
        x = c[name]["x"]
        v0, ka, th, xi, rho = x[:5]
        jv = 0.0
        if name == "Bates":
            lam, mj, sj = x[5:]
            kbar = np.exp(mj + 0.5 * sj * sj) - 1
            jv = 2 * lam * (kbar - mj)  # the jumps' constant contribution to the variance-swap rate
        n_days = 4 * 365
        S, v = sv.heston_qe(1.0, v0, ka, th, xi, rho, n_days / 365, n_days * 4, 200, seed=5, return_v=True)
        vd = v[::4]
        VIX = np.sqrt(sv.heston_vix2(vd, ka, th, tau) + jv)
        dl = np.diff(np.log(VIX), axis=0)
        r = np.diff(np.log(S[::4]), axis=0)
        vv = np.std(dl, axis=0) * np.sqrt(365)
        cor = np.array([np.corrcoef(r[:, i], dl[:, i])[0, 1] for i in range(dl.shape[1])])
        smiles = {}
        for Td in (30, 90):
            T = Td / 365
            ms = np.array([0.8, 0.9, 1.0, 1.1, 1.25, 1.5])
            q = sv.heston_vix_options(v0, ka, th, xi, T, [1.0], tau)
            Fv = q["future"]
            if jv:  # shift by the constant jump variance: recompute on the shifted index
                vT = sv._cir_quantiles(v0, ka, th, xi, T, 4000)
                vix = np.sqrt(sv.heston_vix2(vT, ka, th, tau) + jv)
                Fv = float(vix.mean())
                calls = np.array([np.maximum(vix - m * Fv, 0).mean() for m in ms])
                puts = np.array([np.maximum(m * Fv - vix, 0).mean() for m in ms])
                vsv = float(np.sqrt(np.mean(vix ** 2)))
            else:
                q = sv.heston_vix_options(v0, ka, th, xi, T, ms * Fv, tau)
                calls, puts, vsv = q["call"], q["put"], q["var_swap_vol"]
            ivs = [float(bs.implied_vol(float(cl if m >= 1 else pt), Fv, float(m * Fv), T, 0, 0, 1 if m >= 1 else -1))
                   for m, cl, pt in zip(ms, calls, puts)]
            smiles[str(Td)] = {"m": ms, "iv": ivs, "future": Fv, "var_swap_vol": vsv}
        vT = sv._cir_quantiles(v0, ka, th, xi, 30 / 365, 400)
        out["models"][name] = {"volvol_median": float(np.median(vv)), "volvol_q": np.percentile(vv, [10, 90]),
                               "corr_median": float(np.median(cor)), "path": VIX[:, 0], "smiles": smiles,
                               "floor": float(np.sqrt(th * (1 - (1 - np.exp(-ka * tau)) / (ka * tau)) + jv)),
                               "hist": np.histogram(dl.ravel(), np.linspace(-0.4, 0.4, 41))[0] / dl.size,
                               "vix2_q": sv.heston_vix2(vT, ka, th, tau) + jv}
    dv = np.log(np.asarray(f["dvol"]))
    out["dvol_hist"] = np.histogram(np.diff(dv), np.linspace(-0.4, 0.4, 41))[0] / (len(dv) - 1)
    out["edges"] = np.linspace(-0.4, 0.4, 41)
    out["ratio"] = out["models"]["Heston"]["volvol_median"] / f["volvol"]
    return _json(out)


def compute_hessian() -> dict:
    """Identifiability at the Heston optimum: the Gauss-Newton Hessian J'J in log coordinates (rho raw), its
    eigenvalues and condition number, the standard errors sigma^2 H^-1, and the profile Hessian over (log kappa,
    log xi) with the other three re-optimized (the Schur complement), whose eigenvectors are drawn on the landscape."""
    Q = _quotes()
    pre = sv._pre(Q)
    x = np.array(_heston_x())
    to = lambda x_: np.concatenate([np.log(x_[:4]), x_[4:]])  # noqa: E731
    back = lambda y: np.concatenate([np.exp(y[:4]), y[4:]])  # noqa: E731
    y0 = to(x)
    r0 = sv.residuals("Heston", x, Q, pre)
    J = np.empty((len(r0), 5))
    for j in range(5):
        h = 1e-4
        yp, ym = y0.copy(), y0.copy()
        yp[j] += h
        ym[j] -= h
        J[:, j] = (sv.residuals("Heston", back(yp), Q, pre) - sv.residuals("Heston", back(ym), Q, pre)) / (2 * h)
    H = J.T @ J
    ev, V_ = np.linalg.eigh(H)
    s2 = float(r0 @ r0 / (len(r0) - 5))
    cov = s2 * np.linalg.inv(H)
    a, bb = [1, 3], [0, 2, 4]
    Hp = H[np.ix_(a, a)] - H[np.ix_(a, bb)] @ np.linalg.solve(H[np.ix_(bb, bb)], H[np.ix_(bb, a)])
    evp, Vp = np.linalg.eigh(Hp)
    return _json({"names": ["log v0", "log kappa", "log theta", "log xi", "rho"], "H": H, "eig": ev, "vecs": V_,
                  "cond": float(ev[-1] / ev[0]), "se": np.sqrt(np.diag(cov)), "s2": s2, "profile_H": Hp,
                  "profile_eig": evp, "profile_vecs": Vp, "profile_cond": float(evp[-1] / evp[0]), "x": x})


REG_LAMS = (0.03, 0.3)


def compute_history_reg() -> dict:
    """The 100 weekly Heston fits again, each pulled toward last week's parameters (calibrate_reg, relative
    changes, lam in REG_LAMS): the median weekly parameter change against the median fit error, for the frontier."""
    h = load("history")
    days = [r["day"] for r in h["rows"]]
    part = CACHE.partial("history_reg", {"lams": REG_LAMS, "days": days, "v": 1})
    for lam in REG_LAMS:
        prev = h["rows"][0]["x"]
        for d in days:
            key = f"{lam:g}_{d}"
            if key in part:
                prev = part[key]["x"]
                continue
            Q = _quotes(d, min_T=6 / 365)
            r = sv.calibrate_reg("Heston", Q, prev, lam, max_nfev=200)
            part[key] = {"x": r["x"], "rmse": r["rmse"]}
            prev = r["x"]
            print(f"   reg lam={lam} {d}: rmse {r['rmse']:.2f} x {np.round(r['x'], 3).tolist()}", flush=True)
    out = {"lams": [0.0] + list(REG_LAMS), "days": days, "series": {}, "frontier": []}
    raw = np.array([r["x"] for r in h["rows"]])
    for lam in out["lams"]:
        if lam == 0:
            X = raw
            rm = np.array([r["rmse"] for r in h["rows"]])
        else:
            X = np.array([part[f"{lam:g}_{d}"]["x"] for d in days])
            rm = np.array([part[f"{lam:g}_{d}"]["rmse"] for d in days])
        chg = np.abs(np.diff(np.log(np.maximum(X[:, :4], 1e-6)), axis=0))
        out["series"][f"{lam:g}"] = {"x": X, "rmse": rm}
        out["frontier"].append({"lam": lam, "median_change": {n: float(np.median(chg[:, i])) for i, n in
                                                             enumerate(("v0", "kappa", "theta", "xi"))},
                                "median_change_all": float(np.median(chg)), "rmse_median": float(np.median(rm)),
                                "kappa_at_bound": float((X[:, 1] > 19.9).mean())})
    part.finish()
    return _json(out)


def compute_mv_delta() -> dict:
    """Bitcoin's minimum-variance delta (Hull and White 2017) on real data: a 30-day at-the-money call marked at
    DVOL every day from 2021 to 2025, hedged for one day with Black-Scholes's delta and with delta + vega beta / S, beta
    the regression slope of the change in DVOL on the day's return: fixed from 2021-22 (in and out of sample), and
    rolling over the past 60 to 365 days. Descriptive hedging, not a trading strategy: the counter does not move."""
    from scipy.stats import norm

    kl = data.binance_klines("BTCUSDT", "1d", "2021-04", "2025-11")
    t = np.asarray(kl["time"], float)
    c = np.asarray(kl["close"], float)
    dv = data.deribit_dvol("2021-04", "2025-11", resolution=86400)
    td = (np.asarray(dv["time"], float) // 86400).astype(int)
    vd = np.asarray(dv["close"], float) / 100
    pos = {d: i for i, d in enumerate(td)}
    days = (t // 86400).astype(int)
    rows = [(t[i], c[i], c[i + 1], vd[pos[days[i]]], vd[pos[days[i + 1]]]) for i in range(len(days) - 1)
            if days[i] in pos and days[i + 1] in pos]
    R = np.array(rows)
    T, h = 30 / 365, 1 / 365
    S0, S1, s0, s1 = R[:, 1], R[:, 2], R[:, 3], R[:, 4]
    K = S0
    C0 = bs.price(S0, K, T, s0, cp=1)
    C1 = bs.price(S1, K, T - h, s1, cp=1)
    d1 = 0.5 * s0 * np.sqrt(T)
    delta = norm.cdf(d1)
    vega = S0 * np.sqrt(T) * bs.npdf(d1)
    ret = S1 / S0 - 1
    dsig = s1 - s0
    yr = _ts_year(R[:, 0])
    tr = yr < 2023
    beta = float(np.polyfit(ret[tr], dsig[tr], 1)[0])
    e_bs = (C1 - C0 - delta * (S1 - S0)) / S0
    mv = sv.mv_delta(delta, vega, beta, S0)
    e_fix = (C1 - C0 - mv * (S1 - S0)) / S0
    out = {"beta_fixed": beta, "n": len(R), "mean_delta": float(delta.mean()), "mean_mv": float(mv.mean()),
           "fixed": {"in": float(1 - e_fix[tr].var() / e_bs[tr].var()), "out": float(1 - e_fix[~tr].var() / e_bs[~tr].var())},
           "rolling": {}}
    for W in (60, 90, 180, 365):
        b = np.full(len(ret), np.nan)
        for i in range(W, len(ret)):
            b[i] = np.polyfit(ret[i - W:i], dsig[i - W:i], 1)[0]
        ok = np.isfinite(b)
        e = (C1 - C0 - sv.mv_delta(delta, vega, np.where(ok, b, 0), S0) * (S1 - S0)) / S0
        by = {}
        for y in range(2021, 2026):
            m = ok & (yr >= y) & (yr < y + 1)
            if m.sum() > 30:
                by[str(y)] = float(1 - e[m].var() / e_bs[m].var())
        out["rolling"][str(W)] = {"all": float(1 - e[ok].var() / e_bs[ok].var()), "by_year": by}
        if W == 60:
            out["race"] = {"t": yr[ok], "cum_bs": np.cumsum(e_bs[ok] ** 2), "cum_mv": np.cumsum(e[ok] ** 2),
                           "beta": b[ok], "mean_mv": float(sv.mv_delta(delta, vega, b, S0)[ok].mean()),
                           "mean_bs": float(delta[ok].mean())}
    by = {}
    for y in range(2021, 2026):
        m = (yr >= y) & (yr < y + 1)
        by[str(y)] = float(1 - e_fix[m].var() / e_bs[m].var())
    out["fixed"]["by_year"] = by
    return _json(out)


def compute_heston_hedge() -> dict:
    """In the fitted Heston world (simulated, its truth known): a 30-day at-the-money call hedged daily with the
    Black-Scholes delta at the option's own implied vol, Heston's delta, and the minimum-variance delta
    C_S + C_v rho xi / S; 2,000 paths, prices from a COS grid in (ln S, v)."""
    from scipy.interpolate import RegularGridInterpolator
    from scipy.stats import norm

    v0, ka, th, xi, rho = _heston_x()
    days, N = 30, 2000
    xs = np.linspace(-0.6, 0.6, 61)
    vs = np.concatenate([[1e-4], np.exp(np.linspace(np.log(0.005), np.log(3.0), 47))])
    grids = []
    for d in range(days):
        tau = (days - d) / 365
        G = np.empty((len(xs), len(vs)))
        for j, v in enumerate(vs):
            G[:, j] = np.exp(xs) * sv.cos_price(lambda u, TT: sv.heston_cf(u, TT, v, ka, th, xi, rho), 1.0,
                                                np.exp(-xs), tau, 1)  # C(S, K = 1) = S C(1, 1 / S)
        grids.append(RegularGridInterpolator((xs, vs), G, bounds_error=False, fill_value=None))
    S, v = sv.heston_qe(1.0, v0, ka, th, xi, rho, days / 365, days * 8, N, seed=41, return_v=True)
    S, v = S[::8], v[::8]
    out = {}
    pnl = {m: np.zeros(N) for m in ("BS", "Heston", "MV")}
    C0 = float(grids[0]((0.0, v0)))
    deltas = {m: [] for m in pnl}
    for d in range(days):
        x = np.log(S[d])
        vv = np.clip(v[d], vs[0], vs[-1])
        g = grids[d]
        hS = 1e-3
        C = g(np.column_stack([x, vv]))
        CS = (g(np.column_stack([x + hS, vv])) - g(np.column_stack([x - hS, vv]))) / (2 * hS * S[d])
        hv = np.maximum(1e-3, 0.05 * vv)
        Cv = (g(np.column_stack([x, vv + hv])) - g(np.column_stack([x, np.maximum(vv - hv, vs[0])]))) / (
            vv + hv - np.maximum(vv - hv, vs[0]))
        tau = (days - d) / 365
        ivs = np.array([bs.implied_vol(float(cc), float(s_), 1.0, tau, 0, 0, 1) for cc, s_ in zip(C, S[d])])
        dbs = norm.cdf((np.log(S[d]) + 0.5 * ivs ** 2 * tau) / (ivs * np.sqrt(tau)))
        dmv = CS + Cv * rho * xi / S[d]
        for m, D in (("BS", dbs), ("Heston", CS), ("MV", dmv)):
            pnl[m] += D * (S[d + 1] - S[d])
            deltas[m].append(float(np.nanmean(D)))
    pay = np.maximum(S[-1] - 1.0, 0)
    for m in pnl:
        e = C0 + pnl[m] - pay
        out[m] = {"sd": float(np.nanstd(e)), "mean": float(np.nanmean(e)), "mean_delta": float(np.mean(deltas[m]))}
    out["unhedged_sd"] = float(np.std(C0 - pay))
    out["price"] = C0
    return _json(out)


REV_KAPPAS = (15.0, 30.0, 60.0, 120.0)


def compute_reversionary() -> dict:
    """Heston refitted with kappa held at 15, 30, 60 and 120 (the other four free): the reversionary regime of Abi
    Jaber and De Carvalho (2023). The vol of vol it needs, the fit error, the 3- and 9-day smiles."""
    Q = _quotes()
    x = np.array(_heston_x())
    spec = sv.MODELS["Heston"]
    out = {"runs": []}
    for ka in REV_KAPPAS:
        lo, hi = list(spec["lo"]), list(spec["hi"])
        lo[1] = hi[1] = ka
        hi[3] = 40.0  # room for the vol of vol
        x0 = x.copy()
        x0[1] = ka
        x0[3] = min(x[3] * np.sqrt(ka / x[1]), 39.0)
        r = sv.calibrate("Heston", Q, x0=x0, lo=lo, hi=hi, max_nfev=300, trace=True)
        iv = _model_iv_all("Heston", r["x"], Q)
        sm = {}
        for d_ in (3, 9, 51):
            T = Q["T"][np.argmin(np.abs(Q["T"] * 365 - d_))]
            m = Q["T"] == T
            kk = np.linspace(Q["k"][m].min() - 0.02, Q["k"][m].max() + 0.02, 41)
            sm[str(d_)] = {"kk": kk, "iv": sv.surface_iv("Heston", r["x"], 1.0, np.exp(kk), T), "k": Q["k"][m],
                           "q": Q["iv"][m]}
        out["runs"].append({"kappa": ka, "x": r["x"], "rmse": r["rmse"], "rmse_iv": _rmse(iv, Q),
                            "by_expiry": {int(round(T * 365)): _rmse(iv, Q, Q["T"] == T) for T in np.unique(Q["T"])},
                            "xi_over_sqrt_kappa": float(r["x"][3] / np.sqrt(ka)), "smiles": sm,
                            "trace": _thin_trace(r["trace"], keep=150)})
        print(f"   kappa={ka}: xi {r['x'][3]:.2f}, iv rmse {out['runs'][-1]['rmse_iv']:.2f}", flush=True)
    return _json(out)


ITEMS = {"facts": compute_facts, "calibrate": compute_calibrate, "qe": compute_qe, "skew": compute_skew,
         "sabr": compute_sabr, "landscape": compute_landscape, "history": compute_history, "slv": compute_slv,
         "exotics": compute_exotics, "bergomi": compute_bergomi, "envelope": compute_envelope,
         # the expansion
         "vol_facts": compute_vol_facts, "mixing": compute_mixing, "trap": compute_trap,
         "heston_replay": compute_heston_replay, "heston_sliders": compute_heston_sliders,
         "qe_density": compute_qe_density, "sabr_replay": compute_sabr_replay, "sabr_pde": compute_sabr_pde,
         "levy_fits": compute_levy_fits, "bates_replay": compute_bates_replay, "lab_vg": compute_lab_vg,
         "skew_more": compute_skew_more, "ssr": compute_ssr, "fwd_semi": compute_fwd_semi,
         "vol_puzzle": compute_vol_puzzle, "hessian": compute_hessian, "mv_delta": compute_mv_delta,
         "bergomi_sim": compute_bergomi_sim, "reversionary": compute_reversionary,
         "heston_hedge": compute_heston_hedge, "slv_particles": compute_slv_particles,
         "mixing_sweep": compute_mixing_sweep, "history_reg": compute_history_reg}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
