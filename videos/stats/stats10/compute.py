"""Precompute every number in Part 10 of *Statistics, Built* ("Significance").

    python -m videos.stats.stats10.compute            # everything missing (a minute or two)
    python -m videos.stats.stats10.compute --force board

Results are cached in ``.cache/stats10/<name>.json``.  Arbuthnot's christenings, Darwin's maize, Mendel's peas and the
tea are the Museum's; heights come from the World (seed 1662); everything else is a seeded simulation or exact.

Items:
    arbuthnot    82 years of London christenings: the male share each year; the sign test
    tea          the hypergeometric null for eight cups; designs with 6, 8, 10 and 12 cups
    darwin       Fisher's 2^15 sign flips of Darwin's maize differences; the t-test beside it
    permute      the World: heights of 7 men from each of two regions, the exact permutation null (3,432 splits)
    pvalues      20,000 one-sample t-tests at d = 0, 0.3, 0.8 (n = 15): the p-value's distribution
    errors       the z-test's size and power picture; power against n
    knapsack     the sum of two dice, fair vs one die loaded: every one of the 2,048 rejection regions, the NP frontier
    wilks        -2 log LR for a Poisson rate (n = 3, 30) against chi-squared(1); sizes
    welch        Student vs Welch sizes over unequal n and variances
    mendel       Mendel's 3:1 and 9:3:3:1 fits; the null distribution of Pearson's statistic by simulation
    clinic       a 2x2 from 200 of the World's patients: chi-squared and Fisher's exact test
    power        power curves, the sample-size formula, and type S / M errors (Gelman & Carlin 2014)
    peeking      a t-test checked after every observation: the false-positive rate against the last n
    dance        25 replications of one experiment: p-values and intervals
    many         20 and 100 null tests: any false positive; Bonferroni
    board        the Coverage Board's Part 10 rows
"""

from __future__ import annotations

from dataclasses import asdict
from itertools import product
from math import comb

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import tests as T
from explainer.stats.world import World

CACHE = Cache("stats10")
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


def histogram_density(values, edges):
    """Density per full sample; observations outside the viewport retain their mass."""
    counts, _ = np.histogram(values, edges)
    return counts / (len(values) * np.diff(edges))


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


def monte_carlo_pvalue(observed, simulated):
    """Two-sided randomization rank including the observed exchangeable assignment."""
    extreme = np.sum(np.abs(simulated) >= abs(observed) - 1e-12)
    return float((extreme + 1) / (len(simulated) + 1))


def compute_arbuthnot():
    m, f = np.asarray(museum.ARB_MALES), np.asarray(museum.ARB_FEMALES)
    share = m / (m + f)
    return nest({"years": museum.ARB_YEARS, "share": share, "males": int(m.sum()), "females": int(f.sum()),
                 "ratio": float(m.sum() / f.sum()), "plus": int((m > f).sum()), "n": len(m),
                 "p": T.sign_test(int((m > f).sum()), len(m))["p"], "min": float(share.min()), "max": float(share.max())})


def compute_tea():
    out = {}
    for cups in (6, 8, 10, 12):
        k = cups // 2
        pmf = [comb(k, j) * comb(k, k - j) / comb(cups, k) for j in range(k + 1)]
        out[str(cups)] = {"pmf": pmf, "all": 1 / comb(cups, k), "splits": comb(cups, k)}
    # a lady who is right about each cup with probability q, choosing the four she believes are milk-first:
    # simulate her chance of a perfect score (power) for q = 0.7, 0.8, 0.9
    g = rng(1935)
    power = {}
    for q in (0.7, 0.8, 0.9):
        hits = 0
        R = 40000
        for _ in range(R):
            truth = np.zeros(8, bool)
            truth[g.choice(8, 4, replace=False)] = True
            score = np.where(truth, g.random(8) < q, g.random(8) > q).astype(float) + g.random(8) * 1e-3
            pick = np.argsort(-score)[:4]
            hits += truth[pick].all()
        power[str(q)] = hits / R
    out["power"] = power
    return nest(out)


def compute_darwin():
    d = np.asarray(museum.DARWIN_ZEA, float)
    r = T.sign_flip_test(d, alternative="greater")
    null = r["null"]
    ed = np.arange(-560, 561, 20) - 10
    t = T.t_test(d)
    return nest({"d": d, "sum": r["stat"], "count": r["count"], "total": r["total"], "p_one": r["p"],
                 "p_two": T.sign_flip_test(d)["p"], "edges": ed, "hist": np.histogram(null, ed)[0], "t": t["t"],
                 "t_p": t["p"], "max": float(np.abs(d).sum())})


def compute_permute():
    men = W.adult & W.male
    a = W.height[np.sort(np.flatnonzero(men & (W.region == 0)))[:2000]]
    b = W.height[np.sort(np.flatnonzero(men & (W.region == 3)))[:2000]]
    g = rng(1010)
    xa, xb = np.round(g.choice(a, 7, replace=False), 0), np.round(g.choice(b, 7, replace=False), 0)
    r = T.permutation_test(xa, xb, reps=None)
    null = r["null"]
    ed = np.arange(-12.5, 13, 1.0)
    # a few illustrative shuffles for the machine, with their statistics
    shuffles = []
    for _ in range(6):
        perm = g.permutation(14)
        shuffles.append(perm)
    t = T.t_test(xa, xb)
    truth = {"a": float(a.mean()), "b": float(b.mean())}
    return nest({"a": xa, "b": xb, "obs": r["stat"], "p": r["p"], "n_splits": len(null), "edges": ed,
                 "hist": np.histogram(null, ed)[0], "shuffles": shuffles, "t_p": t["p"], "truth": truth,
                 "extreme": int(np.sum(np.abs(null) >= abs(r["stat"]) - 1e-9))})


def compute_pvalues():
    g = rng(1925)
    n, R = 15, 20000
    ed = np.linspace(0, 1, 21)
    out = {"edges": ed}
    for dlt in (0.0, 0.3, 0.8):
        x = g.normal(dlt, 1, (R, n))
        t = x.mean(1) / (x.std(1, ddof=1) / np.sqrt(n))
        p = 2 * stats.t.sf(np.abs(t), n - 1)
        out[str(dlt)] = {"hist": np.histogram(p, ed, density=True)[0], "below05": float(np.mean(p < 0.05)),
                         "median": float(np.median(p))}
    return nest(out)


def compute_errors():
    ns = np.arange(2, 61)
    pw = [T.power_z(0.5, 1.0, int(n)) for n in ns]
    return nest({"ns": ns, "power": pw, "n80": T.n_for_power(0.5, 1.0), "n90": T.n_for_power(0.5, 1.0, 0.9)})


def two_dice():
    fair = np.full(6, 1 / 6)
    loaded = np.array([2, 2, 2, 2, 2, 5]) / 15  # one die: a six with probability 1/3
    p0, p1 = np.zeros(13), np.zeros(13)
    for a, b in product(range(6), range(6)):
        p0[a + b + 2] += fair[a] * fair[b]
        p1[a + b + 2] += fair[a] * loaded[b]
    return p0[2:], p1[2:]


def compute_knapsack():
    p0, p1 = two_dice()
    sums = np.arange(2, 13)
    k = len(sums)
    masks = np.array(list(product((0, 1), repeat=k)), bool)
    size = masks @ p0
    power = masks @ p1
    lr = p1 / p0
    order = np.argsort(-lr)
    front = [(0.0, 0.0)]
    s_, w_ = 0.0, 0.0
    for i in order:
        s_ += p0[i]
        w_ += p1[i]
        front.append((s_, w_))
    # the best region of size at most 1/6 by brute force, and the greedy one
    ok = size <= 1 / 6 + 1e-12
    best = int(np.argmax(np.where(ok, power, -1)))
    return nest({"sums": sums, "p0": p0, "p1": p1, "lr": lr, "order": order, "size": size, "power": power,
                 "front": front, "best_mask": masks[best], "best_size": float(size[best]), "best_power": float(power[best])})


def compute_wilks():
    g = rng(1938)
    lam0 = 2.0
    out = {}
    ed = np.linspace(0, 8, 33)
    for n in (3, 30):
        S = g.poisson(lam0 * n, 100000).astype(float)
        with np.errstate(divide="ignore", invalid="ignore"):
            w = 2 * (np.where(S > 0, S * np.log(S / (n * lam0)), 0.0) - (S - n * lam0))
        out[str(n)] = {"hist": histogram_density(w, ed), "size": float(np.mean(w > stats.chi2.ppf(0.95, 1))),
                       "mean": float(w.mean())}
    out["edges"] = ed
    xs = np.linspace(0.05, 8, 200)
    out["xs"] = xs
    out["chi2"] = stats.chi2.pdf(xs, 1)
    return nest(out)


def size_two_sample(g, n1, n2, s1, s2, R=20000):
    x = g.normal(0, s1, (R, n1))
    y = g.normal(0, s2, (R, n2))
    m1, m2 = x.mean(1), y.mean(1)
    v1, v2 = x.var(1, ddof=1), y.var(1, ddof=1)
    sp = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2) * (1 / n1 + 1 / n2))
    ts = (m1 - m2) / sp
    a, b = v1 / n1, v2 / n2
    tw = (m1 - m2) / np.sqrt(a + b)
    df = (a + b) ** 2 / (a * a / (n1 - 1) + b * b / (n2 - 1))
    return float(np.mean(np.abs(ts) > stats.t.ppf(0.975, n1 + n2 - 2))), float(np.mean(np.abs(tw) > stats.t.ppf(0.975, df)))


def compute_welch():
    g = rng(1947)
    rows = []
    for n1, n2 in ((10, 10), (10, 40), (40, 10)):
        for ratio in (1.0, 2.0, 4.0):
            st, we = size_two_sample(g, n1, n2, ratio, 1.0)
            rows.append({"n1": n1, "n2": n2, "ratio": ratio, "student": st, "welch": we})
    return nest({"rows": rows})


def compute_mendel():
    shape = T.chisq_test(museum.MENDEL_SHAPE, [0.75, 0.25])
    colour = T.chisq_test(museum.MENDEL_COLOUR, [0.75, 0.25])
    di = T.chisq_test(museum.MENDEL_DIHYBRID, [9 / 16, 3 / 16, 3 / 16, 1 / 16])
    g = rng(1866)
    n = sum(museum.MENDEL_DIHYBRID)
    p = np.array([9, 3, 3, 1]) / 16
    sim = g.multinomial(n, p, 100000)
    e = n * p
    x2 = ((sim - e) ** 2 / e).sum(1)
    ed = np.linspace(0, 14, 57)
    xs = np.linspace(0.05, 14, 200)
    return nest({"shape": shape, "colour": colour, "di": di, "n": n, "edges": ed, "hist": histogram_density(x2, ed),
                 "xs": xs, "chi2_3": stats.chi2.pdf(xs, 3), "sim_size": float(np.mean(x2 > stats.chi2.ppf(0.95, 3))),
                 "sim_below": float(np.mean(x2 <= di["chi2"]))})


def compute_clinic():
    c = W.clinic
    g = rng(2020)
    idx = g.choice(len(c["treated"]), 200, replace=False)
    tr, rec = c["treated"][idx], c["recovered"][idx]
    tab = [[int(np.sum(tr & rec)), int(np.sum(tr & ~rec))], [int(np.sum(~tr & rec)), int(np.sum(~tr & ~rec))]]
    ch = T.chisq_test(tab)
    fe = T.fisher_exact(tab, "two-sided")
    full = [[int(np.sum(c["treated"] & c["recovered"])), int(np.sum(c["treated"] & ~c["recovered"]))],
            [int(np.sum(~c["treated"] & c["recovered"])), int(np.sum(~c["treated"] & ~c["recovered"]))]]
    return nest({"table": tab, "chi2": ch["chi2"], "p": ch["p"], "expected": ch["expected"], "fisher_p": fe["p"],
                 "full": full, "full_rates": [full[0][0] / sum(full[0]), full[1][0] / sum(full[1])]})


def compute_power():
    deltas = np.linspace(-1.2, 1.2, 121)
    curves = {str(n): [T.power_z(float(d), 1.0, n) for d in deltas] for n in (10, 30, 100)}
    g = rng(2014)
    # type S and M: a true effect of 0.1 SD measured with n = 50 per group (two-sample z with known sigma)
    out = {"deltas": deltas, "curves": curves, "n80": {str(d): T.n_for_power(d, 1.0) for d in (0.2, 0.5, 0.8)}}
    sm = {}
    for d, n in ((0.1, 50), (0.3, 50), (0.5, 64)):
        se = np.sqrt(2 / n)
        est = g.normal(d, se, 200000)
        sig = np.abs(est / se) > 1.96
        sm[f"{d}_{n}"] = {"power": float(sig.mean()), "type_s": float(np.mean(est[sig] < 0)),
                          "exaggeration": float(np.mean(np.abs(est[sig])) / d), "se": float(se)}
    out["sm"] = sm
    est = g.normal(0.1, np.sqrt(2 / 50), 400)
    out["sm_draws"] = est
    return nest(out)


def compute_peeking():
    g = rng(1969)
    R, N = 10000, 500
    x = g.standard_normal((R, N))
    cs = np.cumsum(x, 1)
    cs2 = np.cumsum(x * x, 1)
    n = np.arange(1, N + 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        var = (cs2 - cs ** 2 / n) / (n - 1)
        t = (cs / n) / np.sqrt(var / n)
    crit = stats.t.ppf(0.975, np.maximum(n - 1, 1))
    hit = np.abs(t) > crit
    start = 10
    hit[:, :start - 1] = False
    first = np.where(hit.any(1), hit.argmax(1) + 1, 0)
    ends = [10, 20, 50, 100, 200, 500]
    ever = {str(e): float(np.mean((first > 0) & (first <= e))) for e in ends}
    curve = [float(np.mean((first > 0) & (first <= e))) for e in range(start, N + 1)]
    # looks every 10 observations instead, up to 100
    looks = list(range(10, 101, 10))
    any10 = np.zeros(R, bool)
    for e in looks:
        any10 |= hit[:, e - 1]
    paths = t[:6, :200]
    return nest({"ever": ever, "curve": curve, "start": start, "N": N, "every10_to100": float(any10.mean()),
                 "paths": np.nan_to_num(paths), "crit": crit[:200]})


def compute_dance():
    g = rng(2012)
    n, d = 32, 0.5
    reps = []
    for _ in range(25):
        x, y = g.normal(d, 1, n), g.normal(0, 1, n)
        r = T.t_test(x, y)
        diff = x.mean() - y.mean()
        h = stats.t.ppf(0.975, 2 * n - 2) * r["se"]
        reps.append({"p": r["p"], "diff": diff, "lo": diff - h, "hi": diff + h})
    pw = T.power_z(d, np.sqrt(2), n)
    big = g.normal(d, 1, (20000, n)), g.normal(0, 1, (20000, n))
    xs, ys = big
    sp = np.sqrt((xs.var(1, ddof=1) + ys.var(1, ddof=1)) / 2 * 2 / n)
    pp = 2 * stats.t.sf(np.abs((xs.mean(1) - ys.mean(1)) / sp), 2 * n - 2)
    qs = np.quantile(pp, [0.1, 0.25, 0.5, 0.75, 0.9])
    return nest({"reps": reps, "power_approx": pw, "power_sim": float(np.mean(pp < 0.05)), "p_quantiles": qs, "n": n, "d": d})


def compute_many():
    g = rng(2009)
    out = {"any": {str(m): 1 - 0.95 ** m for m in (1, 5, 20, 100)}}
    p = g.random(100)
    out["p100"] = np.sort(p)
    out["n_sig"] = int(np.sum(p < 0.05))
    out["n_bonf"] = int(np.sum(p < 0.05 / 100))
    sims = g.random((20000, 20))
    out["sim20_any"] = float(np.mean((sims < 0.05).any(1)))
    out["sim20_bonf"] = float(np.mean((sims < 0.05 / 20).any(1)))
    return nest(out)


R_BOARD = 10000


def compute_board():
    g = rng(10_000)
    rows = []
    men = W.height[W.adult & W.male]
    women = W.height[W.adult & ~W.male]
    # two samples of 10 from the same population (men's heights): Student's pooled t
    x, y = men[g.integers(0, len(men), (R_BOARD, 10))], men[g.integers(0, len(men), (R_BOARD, 10))]
    p = np.array([T.t_test(a, b)["p"] for a, b in zip(x, y)])
    rows.append(Row(10, r"Student's two-sample $t$", r"men's heights, $n = 10, 10$", "size", 0.05, float(np.mean(p < 0.05)), R_BOARD))
    # unequal spreads, the small group the more variable: women's heights recentred, stretched 3x, n = 10; men's n = 40
    shift = men.mean() - women.mean()
    wide = (women - women.mean()) * 3 + women.mean() + shift
    x, y = wide[g.integers(0, len(wide), (R_BOARD, 10))], men[g.integers(0, len(men), (R_BOARD, 40))]
    ps = np.array([T.t_test(a, b)["p"] for a, b in zip(x, y)])
    pw = np.array([T.welch_test(a, b)["p"] for a, b in zip(x, y)])
    rows.append(Row(10, r"Student's two-sample $t$", r"$\sigma_1 \approx 2.7\sigma_2$, \ $n = 10, 40$", "size", 0.05,
                    float(np.mean(ps < 0.05)), R_BOARD))
    rows.append(Row(10, r"Welch's $t$", r"$\sigma_1 \approx 2.7\sigma_2$, \ $n = 10, 40$", "size", 0.05, float(np.mean(pw < 0.05)),
                    R_BOARD))
    # a t-test peeked at after every observation from 10 to 100 (men's heights, H0 the true mean)
    mu = float(men.mean())
    hits = 0
    for _ in range(R_BOARD):
        z = men[g.integers(0, len(men), 100)] - mu
        cs, cs2 = np.cumsum(z), np.cumsum(z * z)
        n = np.arange(1, 101)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (cs / n) / np.sqrt((cs2 - cs ** 2 / n) / (n - 1) / n)
        crit = stats.t.ppf(0.975, np.maximum(n - 1, 1))
        hits += bool(np.any(np.abs(t[9:]) > crit[9:]))
    rows.append(Row(10, r"$t$-test, \ peeking after every observation", r"men's heights, $n = 10 \dots 100$", "size", 0.05,
                    hits / R_BOARD, R_BOARD))
    # the permutation test on skewed incomes, n = 8, 8 (size)
    inc = W.income[W.adult]
    hits = 0
    for _ in range(2000):
        a, b = inc[g.integers(0, len(inc), 8)], inc[g.integers(0, len(inc), 8)]
        result = T.permutation_test(a, b, reps=999, seed=int(g.integers(1 << 30)))
        hits += monte_carlo_pvalue(result["stat"], result["null"]) <= 0.05
    rows.append(Row(10, r"permutation test", r"incomes, $n = 8, 8$", "size", 0.05, hits / 2000, 2000))
    save_rows(10, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "arbuthnot": compute_arbuthnot, "tea": compute_tea, "darwin": compute_darwin, "permute": compute_permute,
    "pvalues": compute_pvalues, "errors": compute_errors, "knapsack": compute_knapsack, "wilks": compute_wilks,
    "welch": compute_welch, "mendel": compute_mendel, "clinic": compute_clinic, "power": compute_power,
    "peeking": compute_peeking, "dance": compute_dance, "many": compute_many, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
