"""Precompute every number in Part 12 of *Statistics, Built* ("Least Squares").

    python -m videos.stats.stats12.compute            # everything missing (about a minute)
    python -m videos.stats.stats12.compute --force board

Results are cached in ``.cache/stats12/<name>.json``.  The families, heights and incomes are the World's (seed 1662);
Anscombe's quartet is the Museum's; everything else is a seeded simulation.

Items:
    line         30 of the World's families: child (z) on mid-parent (z), the fit and its squares
    lad          Anscombe's third data set: least squares vs least absolute deviations
    gm           Gauss-Markov by simulation: OLS vs another linear unbiased estimator of the slope
    normal       the slope's sampling distribution over 10,000 samples; t-tests; the nested F-test
    fwl          child on father and mother: the full coefficient = the residual-on-residual slope
    ovb          a simulated wage, schooling and ability: omitted-variable bias, formula vs simulation
    dummies      child's height in cm on mid-parent with a son dummy and an interaction
    poly         log income on age: linear, quadratic, a spline; extrapolation
    bands        confidence, Working-Hotelling and prediction bands for the families fit
    collin       two nearly collinear predictors: VIFs and the confidence ellipse
    anscombe     the quartet's identical fits and very different diagnostics
    hetero       log income vs raw income on age: residual spread; classical vs HC3 SEs
    fallacy      fathers and sons both ways; a simulated "treatment" that only regresses
    board        Coverage Board rows: classical vs HC3 slope intervals with and without heteroskedasticity
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import ols
from explainer.stats.world import World

CACHE = Cache("stats12")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def fam():
    f = W.families
    mid = (f["z_father"] + f["z_mother"]) / 2
    return f, mid


def compute_line():
    f, mid = fam()
    g = rng(1806)
    idx = g.choice(len(mid), 30, replace=False)
    x, y = mid[idx], f["z_child"][idx]
    r = ols.fit(ols.design(x), y)
    big = ols.fit(ols.design(mid), f["z_child"])
    return nest({"x": x, "y": y, "coef": r.coef, "rss": r.rss, "r2": r.r2, "truth": big.coef, "se": r.se()})


def compute_lad():
    x, y = museum.ANSCOMBE[3]
    x, y = np.asarray(x, float), np.asarray(y, float)
    ls = ols.fit(ols.design(x), y).coef
    la = ols.lad(x, y)
    return nest({"x": x, "y": y, "ls": ls, "lad": la})


def compute_gm():
    g = rng(1821)
    n, R = 20, 20000
    x = np.sort(g.uniform(0, 10, n))
    b_ols, b_end = [], []
    for _ in range(R):
        y = 1 + 0.5 * x + g.normal(0, 2, n)
        b_ols.append(ols.fit(ols.design(x), y).coef[1])
        b_end.append((y[-1] - y[0]) / (x[-1] - x[0]))  # the slope through the two end points: linear and unbiased
    b_ols, b_end = np.asarray(b_ols), np.asarray(b_end)
    ed = np.linspace(-0.5, 1.5, 81)
    return nest({"x": x, "sd_ols": b_ols.std(), "sd_end": b_end.std(), "mean_ols": b_ols.mean(), "mean_end": b_end.mean(),
                 "edges": ed, "h_ols": np.histogram(b_ols, ed, density=True)[0], "h_end": np.histogram(b_end, ed, density=True)[0],
                 "theory_ols": 2 / np.sqrt(((x - x.mean()) ** 2).sum()), "theory_end": 2 * np.sqrt(2) / (x[-1] - x[0])})


def compute_normal():
    f, mid = fam()
    g = rng(1900)
    n, R = 30, 10000
    true = ols.fit(ols.design(mid), f["z_child"]).coef[1]
    slopes, ts, cover = [], [], 0
    for _ in range(R):
        idx = g.integers(0, len(mid), n)
        r = ols.fit(ols.design(mid[idx]), f["z_child"][idx])
        slopes.append(r.coef[1])
        ts.append((r.coef[1] - true) / r.se()[1])
        lo, hi = r.ci()[1]
        cover += lo <= true <= hi
    slopes, ts = np.asarray(slopes), np.asarray(ts)
    ed = np.linspace(-4, 4, 41)
    # nested F: child (cm) on father; then add mother
    idx = g.choice(len(mid), 100, replace=False)
    yc = f["child"][idx]
    small = ols.fit(ols.design(f["father"][idx]), yc)
    full = ols.fit(ols.design(f["father"][idx], f["mother"][idx]), yc)
    ft = full.f_test(small)
    tss = float(((yc - yc.mean()) ** 2).sum())
    return nest({"true": true, "sd": slopes.std(), "cover": cover / R, "t_edges": ed, "t_hist": np.histogram(ts, ed, density=True)[0],
                 "F": ft, "rss_small": small.rss, "rss_full": full.rss, "tss": tss, "r2_small": small.r2, "r2_full": full.r2,
                 "t_mother": full.t()[2]})


def compute_fwl():
    f, _ = fam()
    g = rng(1933)
    idx = g.choice(len(f["father"]), 200, replace=False)
    y, a, b = f["z_child"][idx], f["z_father"][idx], f["z_mother"][idx]
    full = ols.fit(ols.design(a, b), y)
    ra = ols.fit(ols.design(b), a).resid
    ry = ols.fit(ols.design(b), y).resid
    fw = ols.fit(np.column_stack([ra]), ry)
    simple = ols.fit(ols.design(a), y)
    return nest({"full": full.coef, "fwl": fw.coef, "simple": simple.coef, "ra": ra, "ry": ry, "corr_ab": np.corrcoef(a, b)[0, 1]})


def compute_ovb():
    g = rng(1957)
    n, R = 500, 4000
    b_short, b_long = [], []
    for _ in range(R):
        ability = g.normal(size=n)
        school = 12 + 2 * (0.6 * ability + 0.8 * g.normal(size=n))
        wage = 1.0 + 0.08 * school + 0.10 * ability + 0.3 * g.normal(size=n)
        b_short.append(ols.fit(ols.design(school), wage).coef[1])
        b_long.append(ols.fit(ols.design(school, ability), wage).coef[1])
    # formula: bias = gamma * delta, delta = cov(school, ability)/var(school) = 2*0.6/4 = 0.3
    delta = 2 * 0.6 / 4.0
    return nest({"short": float(np.mean(b_short)), "long": float(np.mean(b_long)), "true": 0.08, "gamma": 0.10, "delta": delta,
                 "formula": 0.08 + 0.10 * delta})


def compute_dummies():
    f, mid_z = fam()
    g = rng(1960)
    idx = g.choice(len(mid_z), 400, replace=False)
    mid = (f["father"][idx] + f["mother"][idx]) / 2
    son = f["son"][idx].astype(float)
    y = f["child"][idx]
    m1 = ols.fit(ols.design(mid), y)
    m2 = ols.fit(ols.design(mid, son), y)
    m3 = ols.fit(ols.design(mid, son, mid * son), y)
    return nest({"mid": mid, "son": son, "y": y, "m1": m1.coef, "m2": m2.coef, "m3": m3.coef, "r2": [m1.r2, m2.r2, m3.r2],
                 "se3": m3.se(), "p_int": m3.pvalue()[3]})


def compute_poly():
    g = rng(1977)
    adult = np.flatnonzero(W.adult)
    idx = g.choice(adult, 600, replace=False)
    age, y = W.age[idx].astype(float), np.log(W.income[idx])
    lin = ols.fit(ols.design(age), y)
    quad = ols.fit(ols.design(age, age ** 2), y)
    knots = [30, 45, 60, 67]
    basis = [age] + [np.maximum(age - k, 0) for k in knots]
    spl = ols.fit(ols.design(*basis), y)
    grid = np.linspace(18, 99, 200)
    gb = [grid] + [np.maximum(grid - k, 0) for k in knots]
    out = {"age": age, "y": y, "grid": grid, "lin": lin.predict(ols.design(grid)), "quad": quad.predict(ols.design(grid, grid ** 2)),
           "spline": spl.predict(ols.design(*gb)), "r2": [lin.r2, quad.r2, spl.r2], "quad_coef": quad.coef}
    # extrapolation: the quadratic at age 120 and 150
    out["extrap"] = {str(a): float(quad.predict(ols.design(np.array([a]), np.array([a * a])))[0]) for a in (120, 150)}
    # the World's true median log income by age (the career curve)
    a = W.age[W.adult].astype(float)
    li = np.log(W.income[W.adult])
    out["true_mean"] = [float(li[(a >= lo) & (a < lo + 3)].mean()) for lo in range(18, 99, 3)]
    out["true_age"] = list(range(19, 100, 3))
    return nest(out)


def compute_bands():
    d = load("line")
    x, y = np.asarray(d["x"]), np.asarray(d["y"])
    r = ols.fit(ols.design(x), y)
    grid = np.linspace(-2.2, 2.2, 100)
    X0 = ols.design(grid)
    lo, hi = r.band(X0)
    wlo, whi = r.band(X0, simultaneous=True)
    plo, phi = r.band(X0, prediction=True)
    return nest({"grid": grid, "fit": r.predict(X0), "lo": lo, "hi": hi, "wlo": wlo, "whi": whi, "plo": plo, "phi": phi,
                 "t": stats.t.ppf(0.975, r.df), "wh": np.sqrt(2 * stats.f.ppf(0.95, 2, r.df))})


def compute_collin():
    g = rng(1970)
    n = 50
    out = {}
    for name, rho in (("low", 0.0), ("high", 0.95)):
        a = g.normal(size=n)
        b = rho * a + np.sqrt(1 - rho ** 2) * g.normal(size=n)
        y = 1 + a + b + g.normal(size=n)
        X = ols.design(a, b)
        r = ols.fit(X, y)
        C = r.cov()[1:, 1:]
        out[name] = {"coef": r.coef[1:], "cov": C, "vif": ols.vif(X), "se": r.se()[1:], "sum_se": float(np.sqrt(C.sum())), "rho": rho}
    return nest(out)


def compute_anscombe():
    out = {}
    for k, (x, y) in museum.ANSCOMBE.items():
        x, y = np.asarray(x, float), np.asarray(y, float)
        r = ols.fit(ols.design(x), y)
        out[str(k)] = {"x": x, "y": y, "coef": r.coef, "r2": r.r2, "lev": r.leverage, "cooks": r.cooks, "student": r.student,
                       "se": r.se()}
    return nest(out)


def compute_hetero():
    g = rng(1980)
    adult = np.flatnonzero(W.adult & (W.age < 67))
    idx = g.choice(adult, 400, replace=False)
    age, inc = W.age[idx].astype(float), W.income[idx] / 1000
    r = ols.fit(ols.design(age), inc)
    rl = ols.fit(ols.design(age), np.log(inc))
    return nest({"age": age, "inc": inc, "coef": r.coef, "se": r.se(), "hc3": r.se("HC3"), "resid": r.resid,
                 "log_se": rl.se(), "log_hc3": rl.se("HC3")})


def compute_fallacy():
    f, _ = fam()
    zf, zc, son = f["z_father"], f["z_child"], f["son"]
    tall = zf > 1.5
    short = zf < -1.5
    tall_c = zc > 1.5
    out = {"tall_fathers": float(zf[tall].mean()), "their_children": float(zc[tall].mean()),
           "short_fathers": float(zf[short].mean()), "their_children_s": float(zc[short].mean()),
           "tall_children": float(zc[tall_c].mean()), "their_fathers": float(zf[tall_c].mean()),
           "sd_f": float(zf.std()), "sd_c": float(zc.std())}
    # a "treatment" given to the worst scorers on a noisy test, which does nothing
    g = rng(1886)
    n = 10000
    ability = g.normal(size=n)
    t1, t2 = ability + g.normal(size=n), ability + g.normal(size=n)
    worst = t1 < np.quantile(t1, 0.1)
    out["worst_t1"] = float(t1[worst].mean())
    out["worst_t2"] = float(t2[worst].mean())
    out["gain"] = float(t2[worst].mean() - t1[worst].mean())
    return nest(out)


R_BOARD = 10000


def hetero_sample(g, n):
    """A skewed predictor and noise whose SD grows with it: the textbook case where classical SEs fail."""
    x = g.exponential(size=n)
    return x, 1 + x + x * g.normal(size=n)


def compute_board():
    g = rng(12_000)
    f, mid = fam()
    ht = ols.fit(ols.design(mid), f["z_child"]).coef[1]
    res = {k: 0 for k in ("h_c", "h_h", "s50_c", "s50_h", "s500_c", "s500_h")}
    for _ in range(R_BOARD):
        j = g.integers(0, len(mid), 30)
        r = ols.fit(ols.design(mid[j]), f["z_child"][j])
        res["h_c"] += r.ci()[1][0] <= ht <= r.ci()[1][1]
        res["h_h"] += r.ci(kind="HC3")[1][0] <= ht <= r.ci(kind="HC3")[1][1]
        for n in (50, 500):
            x, y = hetero_sample(g, n)
            r = ols.fit(ols.design(x), y)
            lo, hi = r.ci()[1]
            res[f"s{n}_c"] += lo <= 1.0 <= hi
            lo, hi = r.ci(kind="HC3")[1]
            res[f"s{n}_h"] += lo <= 1.0 <= hi
    het = r"$x \sim$ Exp, \ SD $\propto x$"
    rows = [
        Row(12, r"OLS slope, \ classical SE", r"child on mid-parent, \ $n = 30$", "coverage", 0.95, res["h_c"] / R_BOARD, R_BOARD),
        Row(12, r"OLS slope, \ HC3 SE", r"child on mid-parent, \ $n = 30$", "coverage", 0.95, res["h_h"] / R_BOARD, R_BOARD),
        Row(12, r"OLS slope, \ classical SE", het + r", \ $n = 50$", "coverage", 0.95, res["s50_c"] / R_BOARD, R_BOARD),
        Row(12, r"OLS slope, \ HC3 SE", het + r", \ $n = 50$", "coverage", 0.95, res["s50_h"] / R_BOARD, R_BOARD),
        Row(12, r"OLS slope, \ classical SE", het + r", \ $n = 500$", "coverage", 0.95, res["s500_c"] / R_BOARD, R_BOARD),
        Row(12, r"OLS slope, \ HC3 SE", het + r", \ $n = 500$", "coverage", 0.95, res["s500_h"] / R_BOARD, R_BOARD),
    ]
    save_rows(12, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


def compute_hetsim():
    g = rng(1985)
    x, y = hetero_sample(g, 200)
    r = ols.fit(ols.design(x), y)
    return nest({"x": x, "y": y, "coef": r.coef, "se": r.se(), "hc0": r.se("HC0"), "hc3": r.se("HC3"), "resid": r.resid})


ITEMS = {
    "line": compute_line, "lad": compute_lad, "gm": compute_gm, "normal": compute_normal, "fwl": compute_fwl, "ovb": compute_ovb,
    "dummies": compute_dummies, "poly": compute_poly, "bands": compute_bands, "collin": compute_collin, "anscombe": compute_anscombe,
    "hetero": compute_hetero, "fallacy": compute_fallacy, "board": compute_board, "hetsim": compute_hetsim,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
