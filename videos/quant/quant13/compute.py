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
load = CACHE.load

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


ITEMS = {"facts": compute_facts, "calibrate": compute_calibrate, "qe": compute_qe, "skew": compute_skew,
         "sabr": compute_sabr, "landscape": compute_landscape, "history": compute_history, "slv": compute_slv,
         "exotics": compute_exotics, "bergomi": compute_bergomi, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
