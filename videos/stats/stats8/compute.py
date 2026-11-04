"""Precompute every number in Part 8 of *Statistics, Built* ("From Sample to Population").

    python -m videos.stats.stats8.compute            # everything missing (a couple of minutes)
    python -m videos.stats.stats8.compute --force board

Results are cached in ``.cache/stats8/<name>.json``; the Coverage Board rows go to ``.cache/stats8/board.json``.
Student's criminals, the sleep data and Laplace's census are the Museum's; everything else is the World or a seeded
simulation (statkit's streams), and exact distributions come from SciPy.

Items:
    student      Macdonell's 3,000 heights; Student's 750 samples of 4 (one shuffle of the deck, dealt in fours);
                 t against N(0, 1) and t_3; the naive z-interval's coverage; the same on 3,000 World residents
    machine      sampling distributions of the mean (n = 4, 16, 64) and the median of World men's heights; SE = sigma/sqrt n
    nminus1      E[sum (x - xbar)^2] / n for n = 2..10 with divisors n and n - 1; a sample of 3 for the geometry
    fisher       xbar and s for normal vs exponential samples of 3 (independent vs not); the Helmert rotation
    chisq        (n - 1) s^2 / sigma^2 for n = 4 and 10 against chi^2_{n-1}
    tdist        the t density for 1, 3, 10, 30 df; tail quantiles; Student's sleep data
    fdist        variance ratios of World heights (men vs men) against F; the F density for several df
    mse          bias, variance and MSE of sum (x - xbar)^2 / c for c = n - 1, n, n + 1 (exact, normal); simulation check
    plugin       plug-in estimates (mean, SD, median, IQR, correlation) from World samples of growing size
    laplace      Laplace's 1802 ratio estimate; a World version: towns, births (age 0), the ratio estimator's
                 sampling distribution and its delta-method SE
    fpc          SE of the mean sampling without replacement from a population of 400, n = 1..400
    board        the first Coverage Board rows (R = 10,000 each)
    robust       t-test size and F-test size under non-normal data (Box 1953)
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.world import World

CACHE = Cache("stats8")
load = CACHE.load
W = World()
R_BOARD = 10_000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


def crim_heights() -> np.ndarray:
    T = np.asarray(museum.CRIM_TABLE)
    return np.repeat(np.asarray(museum.CRIM_HEIGHT_CM), T.sum(0))


def adult_heights() -> np.ndarray:
    return W.height[W.adult]


def compute_student():
    h = crim_heights()
    mu, sig = h.mean(), h.std()
    g = rng(1908)
    deck = g.permutation(h)
    samples = deck.reshape(750, 4)
    m, s = samples.mean(1), samples.std(1, ddof=1)
    ties = int(np.sum(s == 0))  # all four heights in the same whole inch: s = 0, t infinite
    with np.errstate(divide="ignore"):
        t = (m - mu) / (s / 2)
    zq = stats.norm.ppf(0.975)
    tq = stats.t.ppf(0.975, 3)
    cover_z = float(np.mean(np.abs(t) <= zq))
    cover_t = float(np.mean(np.abs(t) <= tq))
    ed = np.linspace(-6, 6, 49)
    # the same on 3,000 residents of the World, 10,000 samples of 4 (with replacement from the 3,000)
    a = adult_heights()
    pop = rng(3000).choice(a, 3000, replace=False)
    pm = pop.mean()
    x = pop[rng(4).integers(0, 3000, (10000, 4))]
    tw = (x.mean(1) - pm) / (x.std(1, ddof=1) / 2)
    T = np.asarray(museum.CRIM_TABLE)
    return nest({"heights": np.asarray(museum.CRIM_HEIGHT_CM), "counts": T.sum(0), "mu": mu, "sigma": sig,
                 "first": samples[:6], "t": t, "edges": ed, "hist": np.histogram(t, ed, density=True)[0],
                 "cover_z": cover_z, "cover_t": cover_t, "zq": zq, "tq": tq, "ties": ties,
                 "tail_z": float(np.mean(np.abs(t) > zq)), "world_cover_z": float(np.mean(np.abs(tw) <= zq)),
                 "world_cover_t": float(np.mean(np.abs(tw) <= tq)), "world_hist": np.histogram(tw, ed, density=True)[0]})


def compute_machine():
    a = W.height[W.adult & W.male]
    mu, sig = float(a.mean()), float(a.std())
    g = rng(81)
    out = {"mu": mu, "sigma": sig, "values": rng(82).choice(a, 3000, replace=False)}
    for n in (4, 16, 64):
        x = a[g.integers(0, len(a), (20000, n))]
        m = x.mean(1)
        md = np.median(x, 1)
        out[str(n)] = {"means": m[:2000], "sd_mean": float(m.std()), "sd_median": float(md.std()),
                       "hist": np.histogram(m, np.linspace(150, 190, 81), density=True)[0],
                       "hist_med": np.histogram(md, np.linspace(150, 190, 81), density=True)[0]}
    out["edges"] = np.linspace(150, 190, 81)
    out["eff"] = {str(n): (out[str(n)]["sd_mean"] / out[str(n)]["sd_median"]) ** 2 for n in (4, 16, 64)}
    return nest(out)


def compute_nminus1():
    a = adult_heights()
    sig2 = float(a.var())
    g = rng(83)
    ns = list(range(2, 11))
    by_n, by_n1 = [], []
    for n in ns:
        x = a[g.integers(0, len(a), (40000, n))]
        ss = ((x - x.mean(1, keepdims=True)) ** 2).sum(1)
        by_n.append(float(ss.mean() / n / sig2))
        by_n1.append(float(ss.mean() / (n - 1) / sig2))
    x3 = np.array([168.0, 175.0, 161.0])
    return nest({"ns": ns, "by_n": by_n, "by_n1": by_n1, "sigma2": sig2, "x3": x3, "xbar3": float(x3.mean()),
                 "res3": x3 - x3.mean(), "ss3": float(((x3 - x3.mean()) ** 2).sum())})


def compute_fisher():
    g = rng(84)
    z = g.standard_normal((3000, 3))
    e = g.exponential(size=(3000, 3))
    out = {}
    for name, x in (("normal", z), ("exp", e)):
        m, s = x.mean(1), x.std(1, ddof=1)
        out[name] = {"m": m[:1200], "s": s[:1200], "corr": float(np.corrcoef(m, s)[0, 1])}
    H = np.array([[1 / np.sqrt(3)] * 3, [1 / np.sqrt(2), -1 / np.sqrt(2), 0], [1 / np.sqrt(6), 1 / np.sqrt(6), -2 / np.sqrt(6)]])
    out["helmert"] = H
    out["orth_err"] = float(np.abs(H @ H.T - np.eye(3)).max())
    return nest(out)


def compute_chisq():
    a = adult_heights()
    sig2 = float(a.var())
    g = rng(85)
    out = {"edges": np.linspace(0, 30, 61)}
    for n in (4, 10):
        x = a[g.integers(0, len(a), (20000, n))]
        q = (n - 1) * x.var(1, ddof=1) / sig2
        out[str(n)] = {"hist": np.histogram(q, out["edges"], density=True)[0], "mean": float(q.mean()), "var": float(q.var())}
    xs = np.linspace(0.05, 30, 300)
    out["xs"] = xs
    out["pdf"] = {str(k): stats.chi2.pdf(xs, k) for k in (1, 2, 3, 5, 9, 15)}
    return nest(out)


def compute_tdist():
    xs = np.linspace(-5, 5, 400)
    out = {"xs": xs, "normal": stats.norm.pdf(xs), "pdf": {str(k): stats.t.pdf(xs, k) for k in (1, 3, 10, 30)}}
    out["q975"] = {str(k): float(stats.t.ppf(0.975, k)) for k in (1, 2, 3, 4, 5, 9, 10, 20, 30, 60, 120)}
    out["tail2"] = {str(k): float(2 * stats.t.sf(2, k)) for k in (1, 3, 10, 30)}
    d = np.asarray(museum.SLEEP_DRUG2) - np.asarray(museum.SLEEP_DRUG1)
    n = len(d)
    tt = d.mean() / (d.std(ddof=1) / np.sqrt(n))
    out["sleep"] = {"d": d, "mean": float(d.mean()), "sd": float(d.std(ddof=1)), "t": float(tt),
                    "p_t": float(2 * stats.t.sf(abs(tt), n - 1)), "p_z": float(2 * stats.norm.sf(abs(tt))),
                    "ci": [float(d.mean() - stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n)),
                           float(d.mean() + stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n))]}
    return nest(out)


def compute_fdist():
    a = W.height[W.adult & W.male]
    g = rng(86)
    n1, n2 = 5, 10
    x1 = a[g.integers(0, len(a), (20000, n1))]
    x2 = a[g.integers(0, len(a), (20000, n2))]
    f = x1.var(1, ddof=1) / x2.var(1, ddof=1)
    ed = np.linspace(0, 6, 61)
    xs = np.linspace(0.01, 6, 300)
    return nest({"n1": n1, "n2": n2, "edges": ed, "hist": np.histogram(f, ed, density=True)[0], "xs": xs,
                 "pdf": stats.f.pdf(xs, n1 - 1, n2 - 1), "q": float(stats.f.ppf(0.975, n1 - 1, n2 - 1)),
                 "q_lo": float(stats.f.ppf(0.025, n1 - 1, n2 - 1)),
                 "shapes": {f"{a_},{b_}": stats.f.pdf(xs, a_, b_) for a_, b_ in ((2, 10), (5, 10), (10, 10), (30, 30))}})


def compute_mse():
    n = 5
    cs = np.linspace(2.5, 9, 200)
    k = n - 1  # SS / sigma^2 ~ chi2_k: mean k, variance 2k
    bias = k / cs - 1
    var = 2 * k / cs ** 2
    mse = bias ** 2 + var
    marks = {}
    for c in (n - 1, n, n + 1):
        marks[str(c)] = {"bias": k / c - 1, "var": 2 * k / c ** 2, "mse": (k / c - 1) ** 2 + 2 * k / c ** 2}
    g = rng(87)
    x = g.standard_normal((200000, n))
    ss = ((x - x.mean(1, keepdims=True)) ** 2).sum(1)
    sim = {str(c): float(np.mean((ss / c - 1) ** 2)) for c in (n - 1, n, n + 1)}
    return nest({"n": n, "cs": cs, "bias2": bias ** 2, "var": var, "mse": mse, "marks": marks, "sim": sim})


def compute_plugin():
    a = W.height[W.adult]
    y = W.income[W.adult]
    fam = W.families
    fa, so = fam["father"], fam["child"]
    truth = {"mean": float(a.mean()), "sd": float(a.std()), "median": float(np.median(y)),
             "iqr": float(np.subtract(*np.percentile(y, [75, 25]))), "corr": float(np.corrcoef(fa, so)[0, 1])}
    g = rng(88)
    ns = np.unique(np.round(np.logspace(1, 4, 25)).astype(int))
    paths = {k: [] for k in truth}
    idx = g.integers(0, len(a), 10000)
    jdx = g.integers(0, len(fa), 10000)
    for n in ns:
        s = idx[:n]
        paths["mean"].append(float(a[s].mean()))
        paths["sd"].append(float(a[s].std()))
        paths["median"].append(float(np.median(y[s])))
        paths["iqr"].append(float(np.subtract(*np.percentile(y[s], [75, 25]))))
        paths["corr"].append(float(np.corrcoef(fa[jdx[:n]], so[jdx[:n]])[0, 1]))
    return nest({"ns": ns, "truth": truth, "paths": paths})


def compute_laplace():
    L = museum.LAPLACE
    births = L["sample_births_3yr"] / 3
    ratio = L["sample_pop"] / births
    est = ratio * L["france_births"]
    # the World version: towns as communes, residents aged 0 as the year's births
    town, age = W.town, W.age
    pop = np.bincount(town, minlength=200).astype(float)
    bir = np.bincount(town[age == 0], minlength=200).astype(float)
    N, B = pop.sum(), bir.sum()
    keep = pop >= 200  # communes large enough to have registers
    g = rng(1802)
    k = 30
    ests, ses = [], []
    elig = np.where(keep)[0]
    for _ in range(10000):
        s = g.choice(elig, k, replace=False)
        r = pop[s].sum() / bir[s].sum()
        ests.append(r * B)
        # delta-method (linearization) SE of the ratio, without the finite-population correction
        e = pop[s] - r * bir[s]
        se_r = np.sqrt(np.sum(e ** 2) / (k - 1) / k) / bir[s].mean()
        ses.append(se_r * B)
    ests, ses = np.asarray(ests), np.asarray(ses)
    z = (ests - N) / ses
    return nest({"laplace": {"births": births, "ratio": ratio, "estimate": est},
                 "world": {"N": N, "B": B, "ratio_true": N / B, "n_towns": int(keep.sum()), "k": k,
                           "mean_est": float(ests.mean()), "sd_est": float(ests.std()), "mean_se": float(ses.mean()),
                           "cover": float(np.mean(np.abs(z) <= 1.96)), "ests": ests[:2000],
                           "pop": pop[keep], "bir": bir[keep]}})


def compute_fpc():
    a = adult_heights()
    pop = rng(89).choice(a, 400, replace=False)
    N = len(pop)
    sig = pop.std(ddof=1)
    ns = np.arange(1, N + 1)
    se_wr = sig / np.sqrt(ns)
    se_wor = se_wr * np.sqrt((N - ns) / (N - 1))
    g = rng(90)
    sim_ns = [10, 50, 100, 200, 300, 380]
    sim = []
    for n in sim_ns:
        m = np.array([pop[g.permutation(N)[:n]].mean() for _ in range(4000)])
        sim.append(float(m.std()))
    return nest({"N": N, "ns": ns, "se_wr": se_wr, "se_wor": se_wor, "sim_ns": sim_ns, "sim": sim})


def t_coverage(pop, n, reps, g, known_sigma=False, use_t=True):
    mu, sig = pop.mean(), pop.std()
    x = pop[g.integers(0, len(pop), (reps, n))]
    m = x.mean(1)
    s = sig if known_sigma else x.std(1, ddof=1)
    q = stats.t.ppf(0.975, n - 1) if use_t else stats.norm.ppf(0.975)
    half = q * s / np.sqrt(n)
    cover = np.abs(m - mu) <= half
    return float(cover.mean()), float(np.mean(2 * half))


def compute_board():
    g = rng(8000)
    h = adult_heights()
    y = W.income[W.adult]
    rows = []
    c, w = t_coverage(h, 5, R_BOARD, g, known_sigma=True, use_t=False)
    rows.append(Row(8, r"$z$, known $\sigma$", r"heights, $n = 5$", "coverage", 0.95, c, R_BOARD, w))
    c, w = t_coverage(h, 5, R_BOARD, g, use_t=False)
    rows.append(Row(8, r"$z$ with $s$", r"heights, $n = 5$", "coverage", 0.95, c, R_BOARD, w))
    c, w = t_coverage(h, 5, R_BOARD, g)
    rows.append(Row(8, r"Student's $t$", r"heights, $n = 5$", "coverage", 0.95, c, R_BOARD, w))
    c, w = t_coverage(y, 20, R_BOARD, g)
    rows.append(Row(8, r"Student's $t$", r"incomes, $n = 20$", "coverage", 0.95, c, R_BOARD, w))
    c, w = t_coverage(y, 500, R_BOARD, g)
    rows.append(Row(8, r"Student's $t$", r"incomes, $n = 500$", "coverage", 0.95, c, R_BOARD, w))
    # the F-test for equal variances: two samples of 10 from the same population (size)
    for name, pop in ((r"heights", W.height[W.adult & W.male]), (r"log incomes", np.log(y))):
        a1 = pop[g.integers(0, len(pop), (R_BOARD, 10))]
        a2 = pop[g.integers(0, len(pop), (R_BOARD, 10))]
        f = a1.var(1, ddof=1) / a2.var(1, ddof=1)
        rej = (f > stats.f.ppf(0.975, 9, 9)) | (f < stats.f.ppf(0.025, 9, 9))
        rows.append(Row(8, r"$F$-test for $\sigma_1 = \sigma_2$", rf"{name}, $n = 10, 10$", "size", 0.05, float(rej.mean()), R_BOARD))
    save_rows(8, rows)
    from dataclasses import asdict
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


def compute_robust():
    g = rng(1953)
    out = {"t": {}, "F": {}}
    dists = {"normal": lambda s: g.standard_normal(s), "t5": lambda s: g.standard_t(5, s) / np.sqrt(5 / 3),
             "uniform": lambda s: (g.random(s) - 0.5) * np.sqrt(12), "exponential": lambda s: g.exponential(size=s) - 1}
    kurt = {"normal": 0.0, "t5": 6.0, "uniform": -1.2, "exponential": 6.0}
    for name, f in dists.items():
        x = f((20000, 10))
        t = x.mean(1) / (x.std(1, ddof=1) / np.sqrt(10))
        out["t"][name] = float(np.mean(np.abs(t) > stats.t.ppf(0.975, 9)))
        a, b = f((20000, 10)), f((20000, 10))
        F = a.var(1, ddof=1) / b.var(1, ddof=1)
        out["F"][name] = float(np.mean((F > stats.f.ppf(0.975, 9, 9)) | (F < stats.f.ppf(0.025, 9, 9))))
    out["kurt"] = kurt
    return nest(out)


def compute_extras():
    from math import gamma
    out = {}
    # the SE of the median: 1 / (2 f(m) sqrt n); for N(mu, sigma) f(m) = 1/(sigma sqrt(2 pi))
    m = W.height[W.adult & W.male]
    sig = m.std()
    out["median_se"] = {"64": float(sig * np.sqrt(np.pi / 2) / 8), "sim": load("machine")["64"]["sd_median"]}
    # E s = c4 sigma
    out["c4"] = {str(n): float(np.sqrt(2 / (n - 1)) * gamma(n / 2) / gamma((n - 1) / 2)) for n in (2, 3, 5, 10, 30)}
    # Student's sleep data analysed as two independent groups (wrongly) vs paired
    a, b = np.asarray(museum.SLEEP_DRUG1), np.asarray(museum.SLEEP_DRUG2)
    t2, p2 = stats.ttest_ind(b, a)
    out["unpaired"] = {"t": float(t2), "p": float(p2), "sp": float(np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)),
                       "r": float(np.corrcoef(a, b)[0, 1])}
    # add-two-successes-and-failures shrinkage: MSE of x/n vs (x + 2)/(n + 4), n = 20
    n = 20
    ps = np.linspace(0.005, 0.995, 199)
    k = np.arange(n + 1)
    mse_ml, mse_ac = [], []
    for p_ in ps:
        w = stats.binom.pmf(k, n, p_)
        mse_ml.append(float(np.sum(w * (k / n - p_) ** 2)))
        mse_ac.append(float(np.sum(w * ((k + 2) / (n + 4) - p_) ** 2)))
    out["shrink"] = {"n": n, "ps": ps, "ml": mse_ml, "ac": mse_ac,
                     "cross": [float(ps[i]) for i in range(1, len(ps)) if (mse_ml[i] - mse_ac[i]) * (mse_ml[i - 1] - mse_ac[i - 1]) < 0]}
    # plug-in fails for the maximum: samples of 10 serial numbers from 1..1000
    g = rng(91)
    N, nn = 1000, 10
    mx = np.array([g.choice(N, nn, replace=False).max() + 1 for _ in range(20000)])
    out["maximum"] = {"N": N, "n": nn, "mean_max": float(mx.mean()), "theory": N * nn / (nn + 1) + nn / (nn + 1),
                      "hist": np.histogram(mx, np.linspace(500, 1000, 51), density=True)[0], "edges": np.linspace(500, 1000, 51),
                      "fixed_mean": float((mx * (1 + 1 / nn) - 1).mean())}
    # 40 intervals from samples of 5 heights: z with s vs t
    h = adult_heights()
    mu = h.mean()
    x = h[rng(92).integers(0, len(h), (40, 5))]
    mm, ss = x.mean(1), x.std(1, ddof=1)
    out["stack"] = {"mu": float(mu), "m": mm, "hz": 1.96 * ss / np.sqrt(5), "ht": stats.t.ppf(0.975, 4) * ss / np.sqrt(5)}
    # one-sided misses for skewed data: exponential, n = 10, two-sided t
    gg = rng(93)
    e = gg.exponential(size=(40000, 10))
    tt = (e.mean(1) - 1) / (e.std(1, ddof=1) / np.sqrt(10))
    q = stats.t.ppf(0.975, 9)
    out["tails"] = {"lo": float(np.mean(tt < -q)), "hi": float(np.mean(tt > q))}
    # sample size for a proportion with the FPC
    z, e_, pp = 1.96, 0.03, 0.5
    n0 = z * z * pp * (1 - pp) / e_ ** 2
    out["samplesize"] = {"n0": n0, "N": {str(Nn): float(n0 / (1 + (n0 - 1) / Nn)) for Nn in (2000, 10000, 100000, 10 ** 7)}}
    return nest(out)


def compute_extras2():
    out = {}
    h = adult_heights()
    # SE of a proportion: share of adults taller than 180 cm, samples of 100
    tall = h > 180
    p = float(tall.mean())
    g = rng(94)
    ph = tall[g.integers(0, len(h), (20000, 100))].mean(1)
    out["prop"] = {"p": p, "se": float(np.sqrt(p * (1 - p) / 100)), "sim": float(ph.std()),
                   "hist": np.bincount((ph * 100).astype(int), minlength=101)[:60] / 20000}
    # Fisher's z for the correlation: samples of 10 from a bivariate normal with rho = 0.8
    rho, n = 0.8, 10
    L = np.linalg.cholesky(np.array([[1, rho], [rho, 1]]))
    z = g.standard_normal((20000, n, 2)) @ L.T
    r = np.array([np.corrcoef(a[:, 0], a[:, 1])[0, 1] for a in z])
    zr = np.arctanh(r)
    out["fisherz"] = {"rho": rho, "n": n, "r_hist": np.histogram(r, np.linspace(-0.2, 1, 61), density=True)[0],
                      "z_hist": np.histogram(zr, np.linspace(-0.4, 2.4, 57), density=True)[0], "r_mean": float(r.mean()),
                      "z_sd": float(zr.std()), "z_sd_theory": float(1 / np.sqrt(n - 3)), "z_mean": float(zr.mean()),
                      "atanh_rho": float(np.arctanh(rho)), "r_edges": np.linspace(-0.2, 1, 61), "z_edges": np.linspace(-0.4, 2.4, 57),
                      "r_skew": float(stats.skew(r)), "z_skew": float(stats.skew(zr))}
    # coverage of the chi-square interval for sigma^2 (nominal 95%), n = 10
    cov = {}
    for name, pop in (("normal men", W.height[W.adult & W.male]), ("all adults", h), ("log incomes", np.log(W.income[W.adult]))):
        s2 = pop.var()
        x = pop[g.integers(0, len(pop), (20000, 10))]
        v = x.var(1, ddof=1)
        lo, hi = 9 * v / stats.chi2.ppf(0.975, 9), 9 * v / stats.chi2.ppf(0.025, 9)
        cov[name] = float(np.mean((lo <= s2) & (s2 <= hi)))
    out["varcover"] = cov
    out["kurt"] = {"normal men": float(stats.kurtosis(W.height[W.adult & W.male])), "all adults": float(stats.kurtosis(h)),
                   "log incomes": float(stats.kurtosis(np.log(W.income[W.adult])))}
    # Wilson-Hilferty: (X/k)^(1/3) approx normal
    out["wh"] = {str(k): {"exact": float(stats.chi2.ppf(0.975, k)),
                          "wh": float(k * (1 - 2 / (9 * k) + 1.959964 * np.sqrt(2 / (9 * k))) ** 3),
                          "normal": float(k + 1.959964 * np.sqrt(2 * k))} for k in (3, 9, 30)}
    return nest(out)


ITEMS = {
    "student": compute_student, "machine": compute_machine, "nminus1": compute_nminus1, "fisher": compute_fisher,
    "chisq": compute_chisq, "tdist": compute_tdist, "fdist": compute_fdist, "mse": compute_mse,
    "plugin": compute_plugin, "laplace": compute_laplace, "fpc": compute_fpc, "board": compute_board,
    "robust": compute_robust, "extras": compute_extras, "extras2": compute_extras2,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
