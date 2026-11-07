"""Precompute every number in Part 16 of *Statistics, Built* ("Without Assumptions: Resampling and Ranks").

    python -m videos.stats.stats16.compute            # everything missing (a few minutes)
    python -m videos.stats.stats16.compute --force board

Results are cached in ``.cache/stats16/<name>.json``.  The law schools, Darwin's maize and the Challenger flights are
the Museum's; incomes, heights and ages are the World's (seed 1662); everything else is a seeded simulation.

Items:
    law         Efron's 15 law schools: r, the bootstrap distribution, jackknife, four intervals
    perm        12 + 12 of the World's incomes: the exact permutation test vs Welch
    signrank    Darwin's 15 pairs: sign test, Wilcoxon's signed rank (exact null), t
    mw          Challenger temperatures, distress vs none: Mann-Whitney U and the AUC
    more        Kruskal-Wallis on incomes by region; Spearman and Kendall on the law schools
    efficiency  power of t vs Wilcoxon-Mann-Whitney at the normal, t_3 and a contaminated normal
    worlds      the bootstrap principle: the median income's real sampling distribution vs one sample's bootstrap
    maxfail     the uniform maximum: the bootstrap's spike at the maximum, P = 1 - (1 - 1/n)^n
    cv          log income on age: training error vs 10-fold cross-validation for polynomial degrees 1-8
    kde         60 of the World's heights: kernel estimates at three bandwidths vs the true density
    board       Coverage Board rows
"""

from __future__ import annotations

import itertools
from dataclasses import asdict
from math import comb

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bootstrap as Bt
from explainer.stats.kit import ranks as R
from explainer.stats.world import World

CACHE = Cache("stats16")
load = CACHE.load
W = World()
R_BOARD = 10_000
L = np.asarray(museum.LAW_LSAT, float)
G = np.asarray(museum.LAW_GPA, float)


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


def clipped_segments(xs, ys, rectangle):
    """Clip line segments to a rectangle without flattening off-scale values."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end - start
        lo, hi = 0.0, 1.0
        for k, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[k] == 0:
                if not lower <= start[k] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower - start[k]) / delta[k], (upper - start[k]) / delta[k]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start + lo * delta, start + hi * delta))
    return result


def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


def compute_law():
    r = corr(L, G)
    g = rng(1979)
    idx = g.integers(0, 15, (2000, 15))
    reps = np.array([corr(L[i], G[i]) for i in idx])
    j = Bt.jackknife((L, G), corr)
    (blo, bhi), z0, a = Bt.bca_ci(reps, r, j["loo"])
    zalpha = stats.norm.ppf([0.025, 0.975])
    adjusted = stats.norm.cdf(z0 + (z0 + zalpha) / (1 - a * (z0 + zalpha)))
    z = np.arctanh(r)
    fz = (np.tanh(z - 1.96 / np.sqrt(12)), np.tanh(z + 1.96 / np.sqrt(12)))
    return nest({"r": r, "reps": reps, "se_boot": reps.std(ddof=1), "se_normal": (1 - r ** 2) / np.sqrt(12), "jack": {k: v for k, v in j.items()},
                 "percentile": Bt.percentile_ci(reps), "basic": Bt.basic_ci(reps, r), "normal": Bt.normal_ci(reps, r), "bca": (blo, bhi),
                 "z0": z0, "a": a, "bca_levels": adjusted, "fisher_z": fz, "first_idx": idx[:6]})


def compute_perm():
    idx_m = W.sample(12, among=W.adult & W.male, seed=161)
    idx_f = W.sample(12, among=W.adult & ~W.male, seed=162)
    x, y = W.income[idx_m] / 1000, W.income[idx_f] / 1000
    obs = x.mean() - y.mean()
    allv = np.r_[x, y]
    tot = allv.sum()
    combos = np.array(list(itertools.combinations(range(24), 12)), dtype=np.int8)
    sa = allv[combos].sum(1)
    null = sa / 12 - (tot - sa) / 12
    p = float(np.mean(np.abs(null) >= abs(obs) - 1e-9))
    w = stats.ttest_ind(x, y, equal_var=False)
    hist, edges = np.histogram(null, bins=60)
    return nest({"x": x, "y": y, "obs": obs, "n_alloc": len(combos), "p": p, "welch_p": w.pvalue, "hist": hist, "edges": edges,
                 "truth": float(W.income[W.adult & W.male].mean() - W.income[W.adult & ~W.male].mean()) / 1000})


def compute_signrank():
    z = np.asarray(museum.DARWIN_ZEA, float)
    w = R.wilcoxon_signed_rank(z)
    npos = int((z > 0).sum())
    sp = stats.binomtest(npos, 15, 0.5).pvalue
    t = stats.ttest_1samp(z, 0)
    ranks = stats.rankdata(np.abs(z))
    return nest({"z": z, "ranks": ranks, "W": w["W"], "p": w["p"], "pmf": w["pmf"], "mean": w["mean"], "npos": npos, "sign_p": sp,
                 "t_p": t.pvalue, "W_max": 120})


def conditional_mann_whitney(x, y):
    """Exact label-randomization law, conditional on the pooled midranks.

    Twice the ranks are integers even with ties. The subset-sum recursion
    counts labelled observations, so repeated values retain their multiplicity.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    m, n = len(x), len(y)
    ranks2 = np.rint(2 * stats.rankdata(np.r_[x, y])).astype(int)
    dp = [dict() for _ in range(n + 1)]
    dp[0][0] = 1
    for j, rank in enumerate(ranks2):
        for k in range(min(n, j + 1), 0, -1):
            for total, count in list(dp[k - 1].items()):
                dp[k][total + rank] = dp[k].get(total + rank, 0) + count
    support = sorted(dp[n])
    us = np.asarray([m * n - (v / 2 - n * (n + 1) / 2) for v in support])
    pmf = np.asarray([dp[n][v] / comb(m + n, n) for v in support])
    order = np.argsort(us)
    us, pmf = us[order], pmf[order]
    u = float(ranks2[:m].sum() / 2 - m * (m + 1) / 2)
    p = float(pmf[np.abs(us - m * n / 2) >= abs(u - m * n / 2) - 1e-12].sum())
    return {"U": u, "auc": u / (m * n), "p": p, "u_grid": us, "pmf": pmf,
            "m": m, "n": n, "allocations": comb(m + n, n)}


def compute_mw():
    t = np.asarray(museum.CHALLENGER_TEMP, float)
    y = np.asarray(museum.CHALLENGER_DISTRESS) > 0
    r = conditional_mann_whitney(t[~y], t[y])
    r["asymptotic_p"] = stats.mannwhitneyu(t[~y], t[y], method="asymptotic").pvalue
    return nest({"warm": t[~y], "cold": t[y], **r})


def monte_carlo_p(null, observed):
    """Two-sided random-permutation p-value including the observed pairing."""
    null = np.asarray(null, float)
    return float((1 + np.count_nonzero(np.abs(null) >= abs(observed))) / (len(null) + 1))


def compute_association():
    g = rng(1)
    r = corr(L, G)
    null = np.asarray([corr(L, g.permutation(G)) for _ in range(20_000)])
    return nest({"r": r, "null": null, "p": monte_carlo_p(null, r)})


def uniform_max_interval(maximum, n, alpha=0.05):
    """Exact one-sided 1-alpha interval from M/theta ~ Beta(n, 1)."""
    return float(maximum), float(maximum / alpha ** (1 / n))


def compute_more():
    groups = [W.income[W.sample(10, among=W.adult & (W.region == k), seed=170 + k)] / 1000 for k in (0, 3, 7)]
    kw = stats.kruskal(*groups)
    f = stats.f_oneway(*groups)
    return nest({"groups": groups, "H": kw.statistic, "kw_p": kw.pvalue, "F": f.statistic, "f_p": f.pvalue,
                 "pearson": corr(L, G), "spearman": R.spearman(L, G), "kendall": R.kendall(L, G)})


def compute_efficiency():
    g = rng(1948)
    n, shift, reps = 20, 0.8, 4000
    out = {}
    for name in ("normal", "t3", "contaminated"):
        rej_t = rej_w = 0
        for _ in range(reps):
            if name == "normal":
                a, b = g.normal(size=n), g.normal(size=n)
            elif name == "t3":
                a, b = g.standard_t(3, n) / np.sqrt(3), g.standard_t(3, n) / np.sqrt(3)
            else:
                a = np.where(g.random(n) < 0.1, g.normal(0, 5, n), g.normal(size=n))
                b = np.where(g.random(n) < 0.1, g.normal(0, 5, n), g.normal(size=n))
            b = b + shift
            rej_t += stats.ttest_ind(a, b).pvalue < 0.05
            rej_w += stats.mannwhitneyu(a, b, method="asymptotic").pvalue < 0.05
        out[name] = {"t": rej_t / reps, "w": rej_w / reps}
    return nest({"power": out, "are_normal": 3 / np.pi, "n": n, "shift": shift})


def compute_worlds():
    pop = W.income[W.adult] / 1000
    truth = float(np.median(pop))
    g = rng(1979)
    real = np.array([np.median(g.choice(pop, 25)) for _ in range(2000)])
    sample = W.income[W.sample(25, among=W.adult, seed=163)] / 1000
    boot = np.array([np.median(sample[g.integers(0, 25, 25)]) for _ in range(2000)])
    return nest({"truth": truth, "real": real, "sample": sample, "est": float(np.median(sample)), "boot": boot,
                 "sd_real": real.std(ddof=1), "sd_boot": boot.std(ddof=1)})


def compute_maxfail():
    g = rng(1943)
    n = 50
    x = g.uniform(0, 1, n)
    m = x.max()
    boot = np.array([x[g.integers(0, n, n)].max() for _ in range(4000)])
    real = np.array([g.uniform(0, 1, n).max() for _ in range(4000)])
    return nest({"n": n, "max": m, "boot": boot, "real": real, "p_spike": float(np.mean(boot == m)), "theory": 1 - (1 - 1 / n) ** n,
                 "limit": 1 - np.exp(-1), "exact_ci": uniform_max_interval(m, n)})


def compute_cv():
    idx = W.sample(200, among=W.adult & (W.age < 70), seed=164)
    age = W.age[idx].astype(float)
    y = np.log(W.income[idx])
    x = (age - 45) / 15
    g = rng(10)
    train, cv = [], []
    for d in range(1, 9):
        c = np.polyfit(x, y, d)
        train.append(float(np.mean((np.polyval(c, x) - y) ** 2)))
        cv.append(float(np.mean([Bt.kfold_poly_cv(x, y, d, 10, rng(100 + r)) for r in range(5)])))
    return nest({"train": train, "cv": cv, "best": int(np.argmin(cv)) + 1, "age": age, "y": y, "n": 200})


def compute_kde():
    idx = W.sample(60, among=W.adult, seed=165)
    h = W.height[idx]
    grid = np.linspace(140, 205, 400)
    pop = W.height[W.adult]
    counts, edges = np.histogram(pop, bins=130, range=(140, 205))
    dens = counts / (len(pop) * np.diff(edges))
    mids = (edges[:-1] + edges[1:]) / 2
    s = Bt.silverman(h)
    return nest({"x": h, "grid": grid, "silverman": s, "small": Bt.kde(h, grid, 1.0), "mid": Bt.kde(h, grid, s), "big": Bt.kde(h, grid, 10.0),
                 "true_x": mids, "true_y": dens, "visible_mass": float(counts.sum() / len(pop))})


def compute_board():
    g = rng(16_000)
    res = {}
    pop = W.income[W.adult] / 1000
    mu = float(pop.mean())
    n, B = 15, 999
    hits = {"pct": 0, "bca": 0, "bt": 0, "t": 0}
    for _ in range(R_BOARD):
        x = g.choice(pop, n)
        idx = g.integers(0, n, (B, n))
        xb = x[idx]
        means = xb.mean(1)
        est = x.mean()
        lo, hi = np.quantile(means, [0.025, 0.975])
        hits["pct"] += lo <= mu <= hi
        loo = (x.sum() - x) / (n - 1)
        (blo, bhi), _, _ = Bt.bca_ci(means, est, loo)
        hits["bca"] += blo <= mu <= bhi
        tb = (means - est) / (xb.std(1, ddof=1) / np.sqrt(n))
        tlo, thi = np.quantile(tb, [0.025, 0.975])
        se = x.std(ddof=1) / np.sqrt(n)
        hits["bt"] += est - thi * se <= mu <= est - tlo * se
        tc = stats.t.ppf(0.975, n - 1)
        hits["t"] += abs(est - mu) <= tc * se
    for k in hits:
        res[k] = hits[k] / R_BOARD
    # the uniform maximum, n = 50, theta = 1
    pm = bm = 0
    for _ in range(R_BOARD):
        x = g.uniform(0, 1, 50)
        mb = x[g.integers(0, 50, (B, 50))].max(1)
        lo, hi = np.quantile(mb, [0.025, 0.975])
        pm += lo <= 1.0 <= hi
        m = x.max()
        bm += 2 * m - hi <= 1.0 <= 2 * m - lo
    res["max_pct"], res["max_basic"] = pm / R_BOARD, bm / R_BOARD
    # sizes under contamination, 20 + 20, no shift
    rt = rw = 0
    for _ in range(R_BOARD):
        a = np.where(g.random(20) < 0.1, g.normal(0, 5, 20), g.normal(size=20))
        b = np.where(g.random(20) < 0.1, g.normal(0, 5, 20), g.normal(size=20))
        rt += stats.ttest_ind(a, b).pvalue < 0.05
        rw += stats.mannwhitneyu(a, b, method="asymptotic").pvalue < 0.05
    res["size_t"], res["size_w"] = rt / R_BOARD, rw / R_BOARD
    inc = r"the World's incomes, \ $n = 15$"
    rows = [
        Row(16, r"bootstrap percentile", inc, "coverage", 0.95, res["pct"], R_BOARD),
        Row(16, r"bootstrap BCa", inc, "coverage", 0.95, res["bca"], R_BOARD),
        Row(16, r"bootstrap-$t$", inc, "coverage", 0.95, res["bt"], R_BOARD),
        Row(16, r"Student's $t$", inc, "coverage", 0.95, res["t"], R_BOARD),
        Row(16, r"percentile, \ the maximum", r"Uniform$(0, \theta)$, \ $n = 50$", "coverage", 0.95, res["max_pct"], R_BOARD),
        Row(16, r"basic, \ the maximum", r"Uniform$(0, \theta)$, \ $n = 50$", "coverage", 0.95, res["max_basic"], R_BOARD),
        Row(16, r"$t$-test", r"contaminated normal, \ 20 + 20", "size", 0.05, res["size_t"], R_BOARD),
        Row(16, r"Wilcoxon--Mann--Whitney", r"contaminated normal, \ 20 + 20", "size", 0.05, res["size_w"], R_BOARD),
    ]
    save_rows(16, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "law": compute_law, "association": compute_association, "perm": compute_perm, "signrank": compute_signrank, "mw": compute_mw, "more": compute_more,
    "efficiency": compute_efficiency, "worlds": compute_worlds, "maxfail": compute_maxfail, "cv": compute_cv,
    "kde": compute_kde, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
