"""Precompute every number in Part 17 of *Statistics, Built* ("Time Series").

    python -m videos.stats.stats17.compute            # everything missing (a few minutes)
    python -m videos.stats.stats17.compute --force board

Results are cached in ``.cache/stats17/<name>.json``.  Yule's marriages and mortality, the sunspots and Mauna Loa's
CO2 are the Museum's; everything else is a seeded simulation.

Items:
    yule        Church of England marriages vs mortality, 1866-1911: r in levels and in differences; random walks
    trio        white noise, an AR(1) and a random walk: series and sample ACFs
    meanci      the mean of an AR(1): variance inflation, effective n, the iid, Newey-West and block intervals
    arma        theoretical ACF/PACF and roots for a gallery of AR, MA and ARMA models
    slutsky     moving sums of white noise make cycles (Slutsky 1927); an AR(2) with complex roots
    sunspot     Yule's AR(2) for the sunspots of 1749-1924: Yule-Walker, least squares, roots, period
    identify    simulated AR(2) and MA(2): sample ACF and PACF
    order       sunspots: AIC over AR orders, Ljung-Box for AR(2) and AR(9)
    forecast    sunspots 1925-1955 forecast from 1749-1924: AR(2) and AR(9), intervals, MASE
    co2         Mauna Loa: classical decomposition, the seasonal figure, the trend's growth
    hw          Holt-Winters on CO2 1959-1997, forecasts for 1998-2001, MASE vs the seasonal naive
    spurious    two independent random walks: r, R^2 and the slope t-test; differenced
    mcomp       a small forecasting competition: naive, drift, SES, Holt, AR(AIC), and their combination
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import ts as T

CACHE = Cache("stats17")
load = CACHE.load
R_BOARD = 10_000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def sunspot_window(y0=1749, y1=1924):
    yrs, s = museum.sunspots()
    k = (yrs >= y0) & (yrs <= y1)
    return yrs[k], s[k]


def compute_yule():
    m, c = np.asarray(museum.YULE_MORTALITY), np.asarray(museum.YULE_CE_MARRIAGES)
    years = np.arange(1866, 1912)
    g = rng(1926)
    rw = np.array([np.corrcoef(T.random_walk(46, g), T.random_walk(46, g))[0, 1] for _ in range(20_000)])
    wn = np.array([np.corrcoef(g.normal(size=46), g.normal(size=46))[0, 1] for _ in range(20_000)])
    pair = (T.random_walk(46, rng(7)), T.random_walk(46, rng(8)))
    return nest({"years": years, "mortality": m, "marriages": c, "r": np.corrcoef(m, c)[0, 1],
                 "r_diff": np.corrcoef(np.diff(m), np.diff(c))[0, 1], "rw_r": rw, "wn_r": wn,
                 "rw_big": np.mean(np.abs(rw) > 0.5), "wn_big": np.mean(np.abs(wn) > 0.5),
                 "pair": pair, "pair_r": np.corrcoef(*pair)[0, 1]})


def compute_trio():
    g = rng(17)
    n = 200
    wn = g.normal(size=n)
    ar = T.simulate_arma([0.8], [], n, g)
    rw = T.random_walk(n, g)
    return nest({"wn": wn, "ar": ar, "rw": rw, "acf_wn": T.acf(wn, 20), "acf_ar": T.acf(ar, 20), "acf_rw": T.acf(rw, 20),
                 "theory_ar": 0.8 ** np.arange(21), "band": 2 / np.sqrt(n)})


def compute_meanci():
    g = rng(1987)
    n, rho = 100, 0.7
    x = T.simulate_arma([rho], [], n, g)
    s = x.std(ddof=1)
    iid = (x.mean() - 1.984 * s / np.sqrt(n), x.mean() + 1.984 * s / np.sqrt(n))
    nw = T.newey_west_se(x)
    bm = T.block_bootstrap_means(x, 10, 2000, g)
    # the real SD of the mean, by simulation, and the exact formula
    means = np.array([T.simulate_arma([rho], [], n, g).mean() for _ in range(4000)])
    k = np.arange(1, n)
    exact_var = (1 + 2 * np.sum((1 - k / n) * rho ** k)) / (1 - rho ** 2) / n
    return nest({"x": x, "n": n, "rho": rho, "mean": x.mean(), "s": s, "iid": iid, "iid_se": s / np.sqrt(n), "nw_se": nw,
                 "nw": (x.mean() - 1.96 * nw, x.mean() + 1.96 * nw), "block_se": bm.std(ddof=1),
                 "block": np.quantile(bm, [0.025, 0.975]), "real_sd": means.std(ddof=1), "exact_sd": np.sqrt(exact_var),
                 "inflation": (1 + rho) / (1 - rho), "neff": T.ar1_neff(n, rho), "acf": T.acf(x, 12),
                 "nw_lags": int(np.floor(4 * (n / 100) ** (2 / 9)))})


def compute_arma():
    models = {"ar_pos": ([0.9], []), "ar_neg": ([-0.9], []), "ma": ([], [0.8]), "arma": ([0.7], [0.5]),
              "ar2": ([1.3, -0.6], []), "ma2": ([], [0.6, 0.4])}
    out = {}
    g = rng(170)
    for k, (phi, th) in models.items():
        a = T.arma_acf(phi, th, 20)
        pc = T.durbin_levinson(a)[0]
        out[k] = {"phi": phi, "theta": th, "acf": a, "pacf": pc, "ar_roots": T.ar_roots(phi) if phi else [],
                  "ma_roots": T.ma_roots(th) if th else [], "x": T.simulate_arma(phi, th, 150, g)}
    out["ar_explode"] = {"x": np.cumprod(np.r_[1.0, np.full(30, 1.1)]) + 0.0}
    return nest(out)


def compute_slutsky():
    g = rng(1927)
    e = g.normal(size=310)
    ms = np.convolve(e, np.ones(10), mode="valid")[:300]
    ar2 = T.simulate_arma([1.3, -0.6], [], 300, g)
    return nest({"e": e[:300], "msum": ms, "ar2": ar2, "period_ar2": T.ar2_period(1.3, -0.6),
                 "acf_msum": T.acf(ms, 30), "acf_ar2": T.acf(ar2, 30)})


def compute_sunspot():
    yrs, s = sunspot_window()
    yw = T.yule_walker(s, 2)
    ols = T.ar_ols(s, 2)
    roots = T.ar_roots(ols["phi"])
    allyrs, alls = museum.sunspots()
    return nest({"years": yrs, "s": s, "yw": yw["phi"], "yw_sigma2": yw["sigma2"], "ols": ols["phi"], "ols_se": ols["se"],
                 "mu": ols["mu"], "sigma2": ols["sigma2"], "roots": roots, "modulus": np.abs(roots[0]),
                 "period": T.ar2_period(*ols["phi"]), "acf": T.acf(s, 30), "pacf": T.pacf(s, 15),
                 "all_years": allyrs, "all": alls, "band": 2 / np.sqrt(len(s))})


def compute_identify():
    g = rng(1970)
    a = T.simulate_arma([1.3, -0.6], [], 300, g)
    m = T.simulate_arma([], [0.6, 0.4], 300, g)
    return nest({"ar": a, "ma": m, "acf_ar": T.acf(a, 20), "pacf_ar": T.pacf(a, 20), "acf_ma": T.acf(m, 20),
                 "pacf_ma": T.pacf(m, 20), "band": 2 / np.sqrt(300)})


def compute_order():
    yrs, s = sunspot_window()
    aic = T.aic_ar(s, 12)
    p_best = int(np.argmin(aic))
    out = {"aic": aic, "best": p_best}
    for p in (2, p_best):
        f = T.ar_ols(s, p)
        Q, pv = T.ljung_box(f["resid"], 20, fitdf=p)
        out[f"p{p}"] = {"phi": f["phi"], "Q": Q, "p": pv, "resid_acf": T.acf(f["resid"], 20), "sigma2": f["sigma2"]}
    out["band"] = 2 / np.sqrt(len(s))
    return nest(out)


def compute_forecast():
    yrs, s = sunspot_window()
    allyrs, alls = museum.sunspots()
    h = 31
    actual = alls[(allyrs >= 1925) & (allyrs < 1925 + h)]
    order = load("order")
    out = {"years": np.arange(1925, 1925 + h), "actual": actual, "train_years": yrs[-60:], "train": s[-60:]}
    for p in (2, order["best"]):
        f = T.ar_ols(s, p)
        fc = T.ar_forecast(s, f["phi"], f["mu"], f["sigma2"], h)
        out[f"p{p}"] = {"mean": fc["mean"], "lo": fc["lo"], "hi": fc["hi"], "se": fc["se"],
                        "mase": T.mase(actual[:11], fc["mean"][:11], s, 1), "mase_all": T.mase(actual, fc["mean"], s, 1)}
    out["naive_mase"] = T.mase(actual[:11], np.full(11, s[-1]), s, 1)
    out["mean_mase"] = T.mase(actual[:11], np.full(11, s.mean()), s, 1)
    out["sd"] = float(s.std())
    out["best"] = order["best"]
    return nest(out)


def compute_co2():
    t, y = museum.co2_monthly()
    d = T.decompose(y, 12)
    tr = d["trend"]
    k = ~np.isnan(tr)
    tt, trr = t[k], tr[k]
    early = np.polyfit(tt[tt < 1969], trr[tt < 1969], 1)[0]
    late = np.polyfit(tt[tt > 1991], trr[tt > 1991], 1)[0]
    return nest({"t": t, "y": y, "trend": tr, "seasonal": d["seasonal"], "remainder": d["remainder"], "figure": d["figure"],
                 "early": early, "late": late, "rem_sd": np.nanstd(d["remainder"]), "amp": d["figure"].max() - d["figure"].min(),
                 "first": y[:12].mean(), "last": y[-12:].mean()})


def compute_hw():
    t, y = museum.co2_monthly()
    cut = np.searchsorted(t, 1998.0)
    train, test = y[:cut], y[cut:]
    h = len(test)
    hw = T.fit_holt_winters(train, 12, h)
    snaive = np.resize(train[-12:], h)
    # drift + seasonal naive: last year's value plus the average annual rise
    drift = (train[-12:].mean() - train[:12].mean()) / (len(train) / 12 - 1)
    sdrift = snaive + drift * (np.arange(h) // 12 + 1)
    s = T.ses(train, 0.5)
    return nest({"t": t, "y": y, "cut": int(cut), "fitted": hw["fitted"], "forecast": hw["forecast"], "alpha": hw["alpha"],
                 "beta": hw["beta"], "gamma": hw["gamma"], "snaive": snaive, "sdrift": sdrift,
                 "mase_hw": T.mase(test, hw["forecast"], train, 12), "mase_snaive": T.mase(test, snaive, train, 12),
                 "mase_sdrift": T.mase(test, sdrift, train, 12), "ses_flat": float(s[-1]),
                 "mase_ses": T.mase(test, np.full(h, s[-1]), train, 12)})


def spurious_stats(x, y):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    s2 = r @ r / (n - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    r2 = 1 - r @ r / np.sum((y - y.mean()) ** 2)
    dw = np.sum(np.diff(r) ** 2) / (r @ r)
    return b[1] / se, r2, dw


def compute_spurious():
    g = rng(1974)
    n = 100
    ts_, r2s, dws, td = [], [], [], []
    for _ in range(5000):
        x, y = T.random_walk(n, g), T.random_walk(n, g)
        t, r2, dw = spurious_stats(x, y)
        ts_.append(t), r2s.append(r2), dws.append(dw)
        td.append(spurious_stats(np.diff(x), np.diff(y))[0])
    ts_, r2s, dws, td = map(np.asarray, (ts_, r2s, dws, td))
    crit = stats.t.ppf(0.975, n - 2)
    ex = (T.random_walk(n, rng(3)), T.random_walk(n, rng(4)))
    t, r2, dw = spurious_stats(*ex)
    return nest({"t": ts_, "r2": r2s, "dw": dws, "t_diff": td, "reject": np.mean(np.abs(ts_) > crit),
                 "reject_diff": np.mean(np.abs(td) > crit), "median_r2": np.median(r2s), "median_dw": np.median(dws),
                 "ex": ex, "ex_t": t, "ex_r2": r2, "ex_dw": dw, "n": n})


def _fc_methods(train, h):
    n = len(train)
    out = {"naive": np.full(h, train[-1]), "drift": train[-1] + (train[-1] - train[0]) / (n - 1) * np.arange(1, h + 1)}
    # SES with alpha by one-step SSE on a grid
    al = np.linspace(0.05, 1, 20)
    sse = [np.sum((train[1:] - T.ses(train, a)[1:n]) ** 2) for a in al]
    out["ses"] = np.full(h, T.ses(train, al[int(np.argmin(sse))])[-1])
    pmax = min(6, n // 5)
    p = int(np.argmin(T.aic_ar(train, pmax)))
    if p == 0:
        out["ar"] = np.full(h, train.mean())
    else:
        f = T.ar_ols(train, p)
        out["ar"] = T.ar_forecast(train, f["phi"], f["mu"], f["sigma2"], h)["mean"] if T.is_stationary(f["phi"]) else out["naive"]
    out["combo"] = (out["drift"] + out["ses"] + out["ar"]) / 3
    return out


def compute_mcomp():
    g = rng(1982)
    series = []
    for k in range(60):
        kind = k % 4
        n = int(g.integers(40, 120))
        if kind == 0:
            x = 50 + T.simulate_arma([0.6], [], n, g, sigma=3)
        elif kind == 1:
            x = 50 + T.random_walk(n, g, 2)
        elif kind == 2:
            x = 50 + 0.4 * np.arange(n) + T.simulate_arma([0.5], [], n, g, sigma=3)
        else:
            x = 50 + np.cumsum(0.3 + T.simulate_arma([0.4], [], n, g, sigma=1.5))
        series.append(x)
    series.append(np.asarray(museum.YULE_MORTALITY))
    series.append(np.asarray(museum.YULE_CE_MARRIAGES))
    yrs, s = museum.sunspots()
    series.append(s[(yrs >= 1900) & (yrs <= 2008)])
    h = 6
    methods = ["naive", "drift", "ses", "ar", "combo"]
    scores = {m: [] for m in methods}
    for x in series:
        train, test = x[:-h], x[-h:]
        fc = _fc_methods(train, h)
        for m in methods:
            scores[m].append(T.mase(test, fc[m], train, 1))
    sc = {m: np.asarray(v) for m, v in scores.items()}
    ranks = stats.rankdata(np.column_stack([sc[m] for m in methods]), axis=1)
    return nest({"methods": methods, "mean_mase": {m: float(np.mean(sc[m])) for m in methods},
                 "median_mase": {m: float(np.median(sc[m])) for m in methods},
                 "mean_rank": {m: float(ranks[:, i].mean()) for i, m in enumerate(methods)}, "n_series": len(series), "h": h})


def compute_board():
    g = rng(17_000)
    n, rho = 100, 0.7
    hits = {"iid": 0, "nw": 0, "block": 0}
    for _ in range(R_BOARD):
        x = T.simulate_arma([rho], [], n, g, burn=100)
        m = x.mean()
        se = x.std(ddof=1) / np.sqrt(n)
        hits["iid"] += abs(m) <= stats.t.ppf(0.975, n - 1) * se
        hits["nw"] += abs(m) <= 1.96 * T.newey_west_se(x)
        bm = T.block_bootstrap_means(x, 10, 499, g)
        lo, hi = np.quantile(bm, [0.025, 0.975])
        hits["block"] += 2 * m - hi <= 0 <= 2 * m - lo
    rt = rd = 0
    crit = stats.t.ppf(0.975, n - 2)
    for _ in range(R_BOARD):
        x, y = T.random_walk(n, g), T.random_walk(n, g)
        rt += abs(spurious_stats(x, y)[0]) > crit
        rd += abs(spurious_stats(np.diff(x), np.diff(y))[0]) > stats.t.ppf(0.975, n - 3)
    ar = r"AR(1), \ $\rho = 0.7$, \ $n = 100$"
    rw = r"two independent random walks, \ $n = 100$"
    rows = [
        Row(17, r"iid $t$-interval, \ the mean", ar, "coverage", 0.95, hits["iid"] / R_BOARD, R_BOARD),
        Row(17, r"Newey--West (HAC), \ the mean", ar, "coverage", 0.95, hits["nw"] / R_BOARD, R_BOARD),
        Row(17, r"moving-block bootstrap, \ the mean", ar, "coverage", 0.95, hits["block"] / R_BOARD, R_BOARD),
        Row(17, r"slope $t$-test, \ levels", rw, "size", 0.05, rt / R_BOARD, R_BOARD),
        Row(17, r"slope $t$-test, \ differences", rw, "size", 0.05, rd / R_BOARD, R_BOARD),
    ]
    save_rows(17, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "yule": compute_yule, "trio": compute_trio, "meanci": compute_meanci, "arma": compute_arma, "slutsky": compute_slutsky,
    "sunspot": compute_sunspot, "identify": compute_identify, "order": compute_order, "forecast": compute_forecast,
    "co2": compute_co2, "hw": compute_hw, "spurious": compute_spurious, "mcomp": compute_mcomp, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
