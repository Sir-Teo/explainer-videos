"""Precompute every number in Part 38 of *Statistics, Built* ("Time Series in Depth").

    OMP_NUM_THREADS=1 python -m videos.stats.stats38.compute            # everything missing (a few minutes)
    python -m videos.stats.stats38.compute --force board

Results are cached in ``.cache/stats38/<name>.json``.  The Nile's minima and flow, the sunspots, the DAX and the US
macro series are the Museum's; the rest are seeded simulations.

Items:
    hurst       Toussoun's Nile minima: R/S, Hurst's H, against white noise and a fitted AR(1)
    spectra     the periodogram's inconsistency; Welch and multitaper; the sunspot cycle
    unitroot    the Dickey-Fuller distribution against the normal; ADF and KPSS on US macro series
    coint       spurious regression; Engle-Granger and Johansen on US consumption and income
    garch       DAX returns: heavy tails, ARCH effects, GARCH(1,1), value-at-risk exceedances
    longmem     ARFIMA autocorrelations, GPH on the minima, the variance of a long-memory mean
    kalman      the Nile's flow as a local level: MLE, filter, smoother, missing years, the 1899 drop; ellipses
    em          EM for the local level's variances
    nonlinear   EKF, UKF and a particle filter on Kitagawa's benchmark; Hamilton's regimes in US GDP growth
    var         a VAR of inflation, unemployment and the T-bill rate: Granger tests and impulse responses
    bootstrap   block and stationary bootstraps for an autocorrelated mean; the Nile minima's mean
    forecast    rolling-origin evaluation on Mauna Loa CO2
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import ts as T

CACHE = Cache("stats38")
load = CACHE.load

NBER = [(1960.25, 1961.0), (1969.75, 1970.75), (1973.75, 1975.0), (1980.0, 1980.5), (1981.5, 1982.75),
        (1990.5, 1991.0), (2001.0, 2001.75), (2007.75, 2009.25)]


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def ar1(n, phi, g, burn=200, sigma=1.0):
    e = sigma * g.standard_normal(n + burn)
    x = np.zeros(n + burn)
    for t in range(1, n + burn):
        x[t] = phi * x[t - 1] + e[t]
    return x[burn:]


def compute_hurst():
    yrs, m = museum.nile_minima()
    h = T.hurst_rs(m)
    g = rng(3801)
    h_iid = [T.hurst_rs(g.standard_normal(len(m)))["H"] for _ in range(200)]
    phi = float(T.acf(m, 1)[1])
    h_ar = [T.hurst_rs(ar1(len(m), phi, g))["H"] for _ in range(200)]
    z = np.cumsum(m - m.mean())
    return nest({"years": yrs, "minima": m, "rs": h, "H": h["H"], "H_iid_mean": float(np.mean(h_iid)),
                 "H_iid_q": [float(np.percentile(h_iid, 2.5)), float(np.percentile(h_iid, 97.5))],
                 "H_ar_mean": float(np.mean(h_ar)), "H_ar_q": [float(np.percentile(h_ar, 2.5)), float(np.percentile(h_ar, 97.5))],
                 "phi": phi, "cumdev": z, "range": float(z.max() - z.min()), "n": len(m), "acf": T.acf(m, 60),
                 "mean": float(m.mean()), "sd": float(m.std())})


def compute_spectra():
    g = rng(3802)
    small, big = g.standard_normal(128), g.standard_normal(2048)
    ps, pb = T.periodogram(small), T.periodogram(big)
    wb = T.welch(big, 128)
    yrs, s = museum.sunspots()
    k = (yrs >= 1700)
    x = s[k]
    pr = T.periodogram(x)
    wl = T.welch(x, 64)
    mt = T.multitaper(x, 4.0)
    peak = lambda f, S: float(1 / f[int(np.argmax(S))])
    ar = T.ar_ols(x, 2)
    return nest({"wn": {"f_small": ps["f"], "I_small": ps["I"], "f_big": pb["f"], "I_big": pb["I"], "f_w": wb["f"],
                        "S_w": wb["S"], "sd_small": float(np.std(ps["I"])), "sd_big": float(np.std(pb["I"])),
                        "sd_w": float(np.std(wb["S"])), "k": wb["k"]},
                 "sun": {"years": yrs[k], "x": x, "f": pr["f"], "I": pr["I"], "f_w": wl["f"], "S_w": wl["S"],
                         "f_mt": mt["f"], "S_mt": mt["S"], "peak_I": peak(pr["f"], pr["I"]), "peak_w": peak(wl["f"], wl["S"]),
                         "peak_mt": peak(mt["f"], mt["S"]), "ar2": ar["phi"], "ar2_sigma2": ar["sigma2"],
                         "ar2_period": T.ar2_period(*ar["phi"]),
                         "ar2_spec": T.arma_spectrum(pr["f"], ar["phi"], (), ar["sigma2"])}})


def df_sim(T_, reps, g, trend="c"):
    e = g.standard_normal((reps, T_ + 1))
    X = np.cumsum(e, 1)
    out = np.empty(reps)
    for i in range(reps):
        out[i] = T.adf(X[i], 0, trend)["t"]
    return out


def paired_persistence(n, phi, g):
    """Random-walk and stationary AR paths driven by the same future innovations."""
    innovations = g.standard_normal(n)
    last = g.normal(scale=1 / math.sqrt(1 - phi ** 2))
    stationary = np.empty(n)
    for t, shock in enumerate(innovations):
        last = phi * last + shock
        stationary[t] = last
    return np.cumsum(innovations), stationary, innovations


def compute_unitroot():
    g = rng(3803)
    n = 200
    rw, st, innovations = paired_persistence(n, 0.9, g)
    taus = df_sim(100, 20000, g)
    edges = np.linspace(-5, 3, 81)
    tn = df_sim(100, 20000, g, "n")
    u = museum.us_macro()
    series = {"log real GDP": (np.log(u["realgdp"]), "ct"), "unemployment": (u["unemp"], "c"),
              "T-bill rate": (u["tbilrate"], "c"), "inflation": (u["infl"], "c"), "GDP growth": (100 * np.diff(np.log(u["realgdp"])), "c")}
    tests = {}
    for name, (x, tr) in series.items():
        a = T.adf(x, 4, tr)
        k = T.kpss(x, tr)
        tests[name] = {"adf": a["t"], "crit": df_critical_safe(a["T"], tr), "kpss": k["eta"], "kcrit": k["crit"][0.05]}
    return nest({"rw": rw, "st": st, "hist": np.histogram(taus, edges)[0], "edges": edges, "hist_n": len(taus), "hist_outside": int(np.sum((taus < edges[0]) | (taus > edges[-1]))), "innovations": innovations,
                 "q05": float(np.percentile(taus, 5)), "crit": T.df_critical(100, 0.05, "c"),
                 "size_normal": float(np.mean(taus < -1.645)), "size_normal2": float(np.mean(np.abs(taus) > 1.96)),
                 "mean_tau": float(taus.mean()), "q05_n": float(np.percentile(tn, 5)), "tests": tests})


def df_critical_safe(Tn, tr):
    return T.df_critical(Tn, 0.05, tr)


def compute_coint():
    g = rng(3804)
    reps, n = 5000, 100
    tstat, r2 = np.empty(reps), np.empty(reps)
    for i in range(reps):
        x, y = np.cumsum(g.standard_normal(n)), np.cumsum(g.standard_normal(n))
        X = np.column_stack([np.ones(n), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        s2 = e @ e / (n - 2)
        tstat[i] = b[1] / math.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
        r2[i] = 1 - e @ e / np.sum((y - y.mean()) ** 2)
    ex = (np.cumsum(g.standard_normal(n)), np.cumsum(g.standard_normal(n)))
    u = museum.us_macro()
    lc, ly, li = np.log(u["realcons"]), np.log(u["realdpi"]), np.log(u["realinv"])
    eg = T.engle_granger(lc, ly, lags=2)
    eg_rev = T.engle_granger(ly, lc, lags=2)
    jo = T.johansen_trace(np.column_stack([lc, ly, li]), k=2)
    jo_crit = [29.80, 15.49, 3.84]  # 5% trace critical values (Osterwald-Lenum), constant in the ECM, p = 3
    return nest({"t_hist": np.histogram(tstat, np.linspace(-20, 20, 41))[0],
                 "hist_n": reps, "hist_outside": int(np.sum(np.abs(tstat) > 20)), "reject": float(np.mean(np.abs(tstat) > 1.96)), "median_r2": float(np.median(r2)),
                 "share_r2_05": float(np.mean(r2 > 0.5)), "example": ex,
                 "t": u["t"], "lc": lc, "ly": ly, "eg": {k: eg[k] for k in ("beta", "t", "crit5")}, "eg_resid": eg["resid"],
                 "adf_lc": T.adf(lc, 2, "ct")["t"], "adf_ly": T.adf(ly, 2, "ct")["t"],
                 "eg_rev_t": eg_rev["t"], "johansen": jo["trace"], "jo_crit": jo_crit, "jo_eig": jo["eig"]})


def compute_garch():
    d = museum.eustock()["DAX"]
    r = 100 * np.diff(np.log(d))
    f = T.garch11_fit(r)
    s = np.sqrt(f["s2"])
    lm = T.arch_lm(r - r.mean(), 5)
    kurt = float(stats.kurtosis(r, fisher=False))
    z = (r - f["mu"]) / s
    q = stats.norm.ppf(0.01)
    exc_const = (r - r.mean()) < q * r.std()
    exc_garch = z < q
    # by halves of the sample: exceedances cluster in turbulence for the constant-variance rule
    vol = s > np.median(s)
    return nest({"r": r, "s": s, "price": d, "mu": f["mu"], "omega": f["omega"], "alpha": f["alpha"], "beta": f["beta"],
                 "persistence": f["persistence"], "half_life": f["half_life"], "loglik": f["loglik"], "lm": lm,
                 "kurt": kurt, "kurt_z": float(stats.kurtosis(z, fisher=False)), "acf_r": T.acf(r, 30),
                 "acf_r2": T.acf(r ** 2, 30), "acf_abs": T.acf(np.abs(r), 30), "n": len(r),
                 "exc_const": float(exc_const.mean()), "exc_garch": float(exc_garch.mean()),
                 "exc_const_hi": float(exc_const[vol].mean()), "exc_const_lo": float(exc_const[~vol].mean()),
                 "exc_garch_hi": float(exc_garch[vol].mean()), "exc_garch_lo": float(exc_garch[~vol].mean()),
                 "sd": float(r.std()), "uncond_sd": float(math.sqrt(f["omega"] / (1 - f["persistence"])))})


def compute_longmem():
    yrs, m = museum.nile_minima()
    gp = T.gph(m)
    lw = T.local_whittle(m, 0.65)
    d = lw["d"]
    gph_range = {str(pw): T.gph(m, pw)["d"] for pw in (0.5, 0.55, 0.6, 0.65, 0.7)}
    lags = np.arange(0, 61)
    acf_f = T.arfima_acf(0.4, 60)
    phi1 = T.arfima_acf(0.4, 1)[1]
    acf_ar = phi1 ** lags
    g = rng(3805)
    sim = T.simulate_arfima(0.4, 663, g, 1.0)
    n = len(m)
    rho = T.arfima_acf(d, n)
    var_ratio = float(1 + 2 * np.sum((1 - np.arange(1, n) / n) * rho[1:n]))  # Var(mean) relative to iid
    se_naive = float(m.std() / math.sqrt(n))
    return nest({"d": d, "se": lw["se"], "m": lw["m"], "H": d + 0.5, "gph": gp, "gph_range": gph_range, "lags": lags, "acf_frac": acf_f, "acf_ar": acf_ar,
                 "acf_sample": T.acf(m, 60), "sim": sim, "var_ratio": var_ratio, "se_naive": se_naive,
                 "se_lm": float(se_naive * math.sqrt(var_ratio)), "neff": float(n / var_ratio), "n": n,
                 "weights": T.frac_diff_weights(0.4, 30), "rate": 2 * d - 1})


def compute_kalman():
    yrs, y = museum.nile()
    f = T.local_level_mle(y)
    kf, sm = f["kf"], f["sm"]
    ym = y.copy()
    ym[20:40] = np.nan
    ym[60:80] = np.nan
    kfm = T.kalman(ym, [[1.0]], [[1.0]], [[f["q"]]], [[f["r"]]], [y[0]], [[1e7]])
    smm = T.rts(kfm)
    lvl = sm["ms"][:, 0]
    jumps = np.diff(lvl)
    j = int(np.argmin(jumps))
    # a level shift at 1899 as a regression effect: compare the likelihood with and without it
    step = (yrs >= 1899).astype(float)

    def ll_shift(delta):
        return T.kalman(y - delta * step, [[1.0]], [[1.0]], [[f["q"]]], [[f["r"]]], [y[0]], [[1e7]])["loglik"]

    grid = np.linspace(-400, 100, 251)
    lls = np.array([ll_shift(dd) for dd in grid])
    dhat = float(grid[np.argmax(lls)])
    # the ellipses: a constant-velocity target tracked from noisy positions
    g = rng(3806)
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = np.diag([0.02, 0.05])
    R = np.array([[1.0]])
    x = np.array([0.0, 1.0])
    xs, ys = [], []
    for t in range(8):
        x = F @ x + g.multivariate_normal([0, 0], Q)
        xs.append(x.copy()), ys.append(x[0] + g.standard_normal())
    track = T.kalman(np.array(ys), F, [[1.0, 0.0]], Q, R, [0.0, 0.5], np.diag([1.0, 1.0]))
    return nest({"years": yrs, "y": y, "q": f["q"], "r": f["r"], "loglik": f["loglik"], "signal_noise": f["q"] / f["r"],
                 "filt": kf["mf"][:, 0], "filt_sd": np.sqrt(kf["Pf"][:, 0, 0]), "pred": kf["mp"][:, 0],
                 "pred_sd": np.sqrt(kf["Pp"][:, 0, 0] + f["r"]), "smooth": lvl, "smooth_sd": np.sqrt(sm["Ps"][:, 0, 0]),
                 "miss_y": ym, "miss_smooth": smm["ms"][:, 0], "miss_sd": np.sqrt(smm["Ps"][:, 0, 0]),
                 "biggest_drop_year": int(yrs[j + 1]), "biggest_drop": float(jumps[j]), "shift": dhat,
                 "lr_shift": float(2 * (lls.max() - ll_shift(0.0))), "shift_variances_fixed": True, "shift_date_selected_from_same_record": True,
                 "track": {"x": np.array(xs), "y": np.array(ys), "mp": track["mp"], "Pp": track["Pp"], "mf": track["mf"],
                           "Pf": track["Pf"]}})


def compute_em():
    yrs, y = museum.nile()
    e = T.local_level_em(y, 1000.0, 10000.0, iters=300)
    f = T.local_level_mle(y)
    p = e["path"]
    return nest({"q_path": p[:, 0], "r_path": p[:, 1], "ll_path": p[:, 2], "q": e["q"], "r": e["r"], "q_mle": f["q"],
                 "r_mle": f["r"], "ll_mle": f["loglik"], "monotone": bool(np.all(np.diff(p[:, 2]) > -1e-6))})


def kitagawa(T_, g, Q=10.0, R=1.0):
    f = lambda x, t: x / 2 + 25 * x / (1 + x * x) + 8 * np.cos(1.2 * (t + 1))
    h = lambda x: x * x / 20
    x, xs, ys = 0.1, [], []
    for t in range(T_):
        x = f(x, t) + math.sqrt(Q) * g.standard_normal()
        xs.append(x), ys.append(h(x) + math.sqrt(R) * g.standard_normal())
    return np.array(xs), np.array(ys), f, h


def compute_nonlinear():
    g = rng(3807)
    xs, ys, f, h = kitagawa(100, g)
    fj = lambda x, t: 0.5 + 25 * (1 - x * x) / (1 + x * x) ** 2
    hj = lambda x: x / 10
    e = T.ekf(ys, f, fj, h, hj, 10.0, 1.0, 0.1, 5.0)
    u = T.ukf(ys, f, h, 10.0, 1.0, 0.1, 5.0)
    p = T.bootstrap_pf(ys, f, h, 10.0, 1.0, 0.1, 5.0, 3000, g)
    rmse = lambda m: float(np.sqrt(np.mean((m - xs) ** 2)))
    # averaged over 30 seeds
    rm = {"ekf": [], "ukf": [], "pf": []}
    for s in range(30):
        gg = rng(3900 + s)
        xx, yy, _, _ = kitagawa(100, gg)
        rm["ekf"].append(np.sqrt(np.mean((T.ekf(yy, f, fj, h, hj, 10.0, 1.0, 0.1, 5.0)["m"] - xx) ** 2)))
        rm["ukf"].append(np.sqrt(np.mean((T.ukf(yy, f, h, 10.0, 1.0, 0.1, 5.0)["m"] - xx) ** 2)))
        rm["pf"].append(np.sqrt(np.mean((T.bootstrap_pf(yy, f, h, 10.0, 1.0, 0.1, 5.0, 2000, gg)["m"] - xx) ** 2)))
    u_ = museum.us_macro()
    gr = 400 * np.diff(np.log(u_["realgdp"]))
    tt = u_["t"][1:]
    hm = T.hamilton_fit(gr)
    inrec = np.array([any(a <= t <= b for a, b in NBER) for t in tt])
    return nest({"x": xs, "y": ys, "ekf": e["m"], "ukf": u["m"], "pf": p["m"], "pf_lo": p["lo"], "pf_hi": p["hi"],
                 "rmse": {"ekf": rmse(e["m"]), "ukf": rmse(u["m"]), "pf": rmse(p["m"])},
                 "rmse30": {k: float(np.mean(v)) for k, v in rm.items()},
                 "gdp": {"t": tt, "growth": gr, "p_low": hm["p_low"], "mu": hm["mu"], "sigma": hm["sigma"], "P": hm["P"],
                         "dur_low": hm["duration_low"], "dur_high": hm["duration_high"], "nber": NBER,
                         "p_in": float(hm["p_low"][inrec].mean()), "p_out": float(hm["p_low"][~inrec].mean())}})


def compute_var():
    u = museum.us_macro()
    Y = np.column_stack([u["infl"], u["unemp"], u["tbilrate"]])
    names = ["inflation", "unemployment", "T-bill rate"]
    p = 4
    fit = T.var_fit(Y, p)
    G = {f"{names[c]} -> {names[e]}": T.granger_test(Y, p, c, e) for c in range(3) for e in range(3) if c != e}
    H = 20
    Psi = T.irf(fit, H)
    g = rng(3808)
    U, X, B = fit["U"], fit["X"], fit["B"]
    boots = []
    for _ in range(300):
        idx = g.integers(0, len(U), len(U))
        Yb = np.zeros_like(Y)
        Yb[:p] = Y[:p]
        Ub = U[idx]
        for t in range(p, len(Y)):
            xt = np.concatenate([[1.0]] + [Yb[t - j] for j in range(1, p + 1)])
            Yb[t] = xt @ B + Ub[t - p]
        boots.append(T.irf(T.var_fit(Yb, p), H))
    boots = np.array(boots)
    lo, hi = np.percentile(boots, 5, 0), np.percentile(boots, 95, 0)
    return nest({"names": names, "t": u["t"], "Y": Y, "p": p, "granger": G, "irf": Psi, "lo": lo, "hi": hi, "H": H})


def compute_bootstrap():
    g = rng(3809)
    x = ar1(500, 0.5, g)
    bi = x[g.integers(0, len(x), (2000, len(x)))].mean(1)
    bb = T.block_bootstrap_means(x, 30, 2000, g)
    bs = T.stationary_bootstrap_means(x, 30, 2000, g)
    true_sd = float(math.sqrt((1 / 500) * (1 / (1 - 0.25)) * (1 + 0.5) / (1 - 0.5)))
    yrs, m = museum.nile_minima()
    mi = m[g.integers(0, len(m), (2000, len(m)))].mean(1)
    mb = {b: float(T.block_bootstrap_means(m, b, 2000, g).std()) for b in (5, 20, 50, 100)}
    lm = load("longmem")
    return nest({"x": x, "sd_iid": float(bi.std()), "sd_block": float(bb.std()), "sd_stat": float(bs.std()), "true_sd": true_sd,
                 "nw": T.newey_west_se(x), "hist_iid": np.histogram(bi - x.mean(), np.linspace(-0.4, 0.4, 41))[0],
                 "hist_block": np.histogram(bb - x.mean(), np.linspace(-0.4, 0.4, 41))[0],
                 "nile_iid": float(mi.std()), "nile_block": mb, "nile_lm": lm["se_lm"], "nile_naive": lm["se_naive"]})


def compute_forecast():
    t, y = museum.co2_monthly()
    n = len(y)
    origins = list(range(n - 24 - 10 * 12, n - 24 + 1, 12))
    H = 24
    err = {"naive": [], "snaive": [], "hw": [], "drift": []}
    for o in origins:
        train, test = y[:o], y[o:o + H]
        f_naive = np.full(H, train[-1])
        f_snaive = np.array([train[o - 12 + (h % 12)] for h in range(H)])
        slope = (train[-1] - train[-13]) / 12
        f_drift = np.array([train[o - 12 + (h % 12)] + 12 * slope * (1 + h // 12) for h in range(H)])
        hw = T.fit_holt_winters(train, 12, h=H)
        f_hw = np.asarray(hw["forecast"])[:H]
        for k, fc in (("naive", f_naive), ("snaive", f_snaive), ("hw", f_hw), ("drift", f_drift)):
            err[k].append(T.mase(test, fc, train, 12))
    # leakage: choosing the "best" of 50 random tweaks on the test period itself
    gq = rng(3810)
    o = origins[-1]
    train, test = y[:o], y[o:o + H]
    hw = np.asarray(T.fit_holt_winters(train, 12, h=H)["forecast"])[:H]
    tweaks = [hw + gq.normal(0, 0.3) + gq.normal(0, 0.02) * np.arange(H) for _ in range(50)]
    best = min(tweaks, key=lambda f_: T.mase(test, f_, train, 12))
    nxt = y[o + H:o + 2 * H] if o + 2 * H <= n else None
    return nest({"origins": [float(t[o]) for o in origins], "mase": {k: float(np.mean(v)) for k, v in err.items()},
                 "mase_by_origin": err, "t": t, "y": y, "leak_best": float(T.mase(test, best, train, 12)),
                 "leak_honest": float(T.mase(test, hw, train, 12))})


def compute_gallery():
    """Four seeded series, each breaking one of Part 17's assumptions."""
    g = rng(3812)
    n = 300
    ar = ar1(n, 0.6, g)
    rw = np.cumsum(g.standard_normal(n))
    e, s2 = np.zeros(n), np.full(n, 1.0)
    for t in range(1, n):
        s2[t] = 0.05 + 0.12 * e[t - 1] ** 2 + 0.85 * s2[t - 1]
        e[t] = math.sqrt(s2[t]) * g.standard_normal()
    lm = T.simulate_arfima(0.45, n, g)
    lvl = np.cumsum(0.3 * g.standard_normal(n))
    obs = lvl + g.standard_normal(n)
    return nest({"ar": ar, "rw": rw, "garch": e, "lm": lm, "level": lvl, "obs": obs,
                 "acf_ar": T.acf(ar, 40), "acf_lm": T.acf(lm, 40)})


def compute_board():
    rows = []
    g = rng(3811)
    reps = 4000
    taus = df_sim(100, reps, g)
    rows.append(Row(38, r"Dickey--Fuller $t$, \ normal critical value", r"random walks, \ $T = 100$", "size", 0.05,
                    float(np.mean(taus < -1.645)), reps))
    rows.append(Row(38, r"Dickey--Fuller $t$, \ MacKinnon's value", r"random walks, \ $T = 100$", "size", 0.05,
                    float(np.mean(taus < T.df_critical(100, 0.05, "c"))), reps))
    kp = []
    for _ in range(2000):
        kp.append(T.kpss(ar1(200, 0.5, g))["eta"] > 0.463)
    rows.append(Row(38, r"KPSS, \ Bartlett long-run variance", r"stationary AR(1), \ $\phi = 0.5$, \ $T = 200$", "size", 0.05,
                    float(np.mean(kp)), 2000))
    sp, eg = [], []
    for _ in range(2000):
        x, y = np.cumsum(g.standard_normal(100)), np.cumsum(g.standard_normal(100))
        X = np.column_stack([np.ones(100), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        se = math.sqrt(e @ e / 98 * np.linalg.inv(X.T @ X)[1, 1])
        sp.append(abs(b[1] / se) > 1.96)
        r = T.engle_granger(y, x)
        eg.append(r["t"] < r["crit5"])
    rows.append(Row(38, r"regression $t$-test, \ two random walks", r"independent random walks, \ $T = 100$", "size", 0.05,
                    float(np.mean(sp)), 2000))
    rows.append(Row(38, r"Engle--Granger, \ MacKinnon's values", r"independent random walks, \ $T = 100$", "size", 0.05,
                    float(np.mean(eg)), 2000))
    ci, cb = [], []
    for _ in range(500):
        x = ar1(500, 0.5, g)
        m = x.mean()
        si = x[g.integers(0, 500, (800, 500))].mean(1).std()
        sb = T.block_bootstrap_means(x, 30, 800, g).std()
        ci.append(abs(m) <= 1.645 * si)
        cb.append(abs(m) <= 1.645 * sb)
    rows.append(Row(38, r"i.i.d.\ bootstrap CI for the mean", r"AR(1), \ $\phi = 0.5$, \ $n = 500$", "coverage", 0.9,
                    float(np.mean(ci)), 500))
    rows.append(Row(38, r"moving-block bootstrap CI \ (blocks of 30)", r"AR(1), \ $\phi = 0.5$, \ $n = 500$", "coverage", 0.9,
                    float(np.mean(cb)), 500))
    save_rows(38, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "hurst": compute_hurst, "spectra": compute_spectra, "unitroot": compute_unitroot, "coint": compute_coint,
    "garch": compute_garch, "longmem": compute_longmem, "kalman": compute_kalman, "em": compute_em,
    "nonlinear": compute_nonlinear, "var": compute_var, "bootstrap": compute_bootstrap, "forecast": compute_forecast, "gallery": compute_gallery,
    "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
