"""Precompute every number in Part 11 of *Statistics, Built* ("Honest Intervals").

    python -m videos.stats.stats11.compute            # everything missing (about a minute)
    python -m videos.stats.stats11.compute --force board

Results are cached in ``.cache/stats11/<name>.json``.  Binomial coverages are exact (sums over outcomes); heights and
incomes come from the World (seed 1662); everything else is a seeded simulation.

Items:
    sawtooth     the Wald interval's exact coverage at p = 0.2 for n = 10..100, and at n = 50 across p
    rain         100 t-intervals for the World's mean male height from samples of 10
    pivots       coverage of the rate pivot and of the F interval for a variance ratio
    belt         Neyman's belt for Binomial(20, p): the acceptance region of each p; the interval at x = 7
    binom        exact coverage and expected width of six intervals at n = 50 across p
    likelihood   Wald vs likelihood-ratio vs exact for 2 of 30; the rule of three
    midp         Clopper-Pearson vs its mid-p version, coverage at n = 25
    fieller      three samples whose ratio intervals are bounded, a complement, and the whole line
    simultaneous Bonferroni for 5 means; the DKW band vs pointwise intervals for the World's height ECDF
    prediction   CI vs prediction interval vs order statistics for a new observation
    welch        Welch's (1939) two-uniform example: conditional coverage
    credible     the Jeffreys interval's coverage vs its posterior probability; a flat-prior interval at small p
    board        the Coverage Board's Part 11 rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import intervals as I
from explainer.stats.world import World

CACHE = Cache("stats11")
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


def men():
    return W.height[W.adult & W.male]


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



def empirical_cdf_sup(sample, population, *, population_sorted=False):
    """Exact empirical-CDF sup, with ties and both jump limits.

    Between sample jumps the difference is monotone, so its extrema occur at
    their left or right limits. Sorting the finite population once avoids a
    population-sized union for every simulation replicate.
    """
    sample = np.sort(np.asarray(sample, float))
    population = np.asarray(population, float)
    if not population_sorted:
        population = np.sort(population)
    if not len(sample) or not len(population):
        raise ValueError("CDFs require nonempty samples")
    jumps, first, counts = np.unique(sample, return_index=True, return_counts=True)
    left = first / len(sample) - np.searchsorted(population, jumps, side="left") / len(population)
    right = (first + counts) / len(sample) - np.searchsorted(population, jumps, side="right") / len(population)
    return float(max(np.max(np.abs(left)), np.max(np.abs(right))))


def jeffreys_credible(x, n, alpha=0.05):
    """Unmodified equal-tailed posterior interval, including at x=0,n."""
    return tuple(float(v) for v in stats.beta.ppf([alpha / 2, 1 - alpha / 2], x + .5, n - x + .5))

def compute_sawtooth():
    ns = np.arange(10, 101)
    cov_n = [float(I.binom_coverage(I.wald, int(n), [0.2])[0]) for n in ns]
    ps = np.linspace(0.005, 0.995, 397)
    cov_p = I.binom_coverage(I.wald, 50, ps)
    # Brown, Cai & DasGupta's example: p = 0.005, the n needed before Wald's coverage stays above 0.94... report a few
    lucky = {str(n): float(I.binom_coverage(I.wald, n, [0.5])[0]) for n in (17, 40)}
    tiny = {str(n): float(I.binom_coverage(I.wald, n, [0.005])[0]) for n in (100, 591, 592, 1000)}
    return nest({"ns": ns, "cov_n": cov_n, "ps": ps, "cov_p": cov_p, "lucky": lucky, "tiny": tiny,
                 "mean_p": float(cov_p.mean()), "min_n": float(min(cov_n)), "max_n": float(max(cov_n))})


def compute_rain():
    h = men()
    mu = float(h.mean())
    g = rng(1937)
    ints = [I.t_interval(h[g.integers(0, len(h), 10)]) for _ in range(100)]
    ints = np.asarray(ints)
    big = np.asarray([I.t_interval(h[g.integers(0, len(h), 10)]) for _ in range(10000)])
    return nest({"mu": mu, "ints": ints, "hits": int(np.sum((ints[:, 0] <= mu) & (mu <= ints[:, 1]))),
                 "cov10k": float(np.mean((big[:, 0] <= mu) & (mu <= big[:, 1]))), "width": float(np.mean(big[:, 1] - big[:, 0]))})


def compute_pivots():
    g = rng(1925)
    R = 20000
    lam = 0.5
    hits = 0
    for _ in range(R):
        lo, hi = I.rate_interval(g.exponential(1 / lam, 6))
        hits += lo <= lam <= hi
    # F interval for sigma1^2/sigma2^2 from normal samples of 8 and 12
    a, b = g.normal(0, 2, (R, 8)), g.normal(0, 1, (R, 12))
    r = a.var(1, ddof=1) / b.var(1, ddof=1)
    lo = r / stats.f.ppf(0.975, 7, 11)
    hi = r / stats.f.ppf(0.025, 7, 11)
    return nest({"rate": hits / R, "F": float(np.mean((lo <= 4) & (4 <= hi)))})


def compute_belt():
    n, alpha = 20, 0.05
    ps = np.linspace(0.001, 0.999, 300)
    lo, hi = [], []
    for p in ps:
        cdf = stats.binom.cdf(np.arange(n + 1), n, p)
        sf = stats.binom.sf(np.arange(n + 1) - 1, n, p)  # P(X >= x)
        # acceptance: x with P(X <= x) > alpha/2 and P(X >= x) > alpha/2
        acc = np.flatnonzero((cdf > alpha / 2) & (sf > alpha / 2))
        lo.append(int(acc.min()))
        hi.append(int(acc.max()))
    x = 7
    return nest({"n": n, "ps": ps, "lo": lo, "hi": hi, "x": x, "cp": I.clopper_pearson(x, n), "wald": I.wald(x, n)})


def compute_binom():
    n = 50
    ps = np.linspace(0.005, 0.995, 397)
    out = {"n": n, "ps": ps, "cov": {}, "mean": {}, "min": {}, "width05": {}, "width5": {}}
    for k, m in I.BINOMIAL.items():
        c = I.binom_coverage(m, n, ps)
        out["cov"][k] = c
        out["mean"][k] = float(c.mean())
        out["min"][k] = float(c.min())
        out["width05"][k] = float(I.binom_width(m, n, [0.05])[0])
        out["width5"][k] = float(I.binom_width(m, n, [0.5])[0])
    return nest(out)


def compute_likelihood():
    x, n = 2, 30
    ints = {k: m(x, n) for k, m in I.BINOMIAL.items()}
    ps = np.unique(np.r_[np.linspace(0.0005, 0.3, 300), x / n])
    ll = x * np.log(ps) + (n - x) * np.log(1 - ps)
    ll -= x * np.log(x / n) + (n - x) * np.log1p(-x / n)
    three = {str(nn): {"exact": 1 - 0.05 ** (1 / nn), "rule": 3 / nn} for nn in (10, 30, 100, 1000)}
    return nest({"x": x, "n": n, "ints": ints, "ps": ps, "ll": ll, "three": three})


def mid_p(x, n, alpha=0.05):
    from scipy import optimize

    def up(p):  # P(X < x) + P(X = x)/2 = alpha/2 -> upper limit
        return stats.binom.cdf(x - 1, n, p) + 0.5 * stats.binom.pmf(x, n, p) - alpha / 2

    def dn(p):
        return stats.binom.sf(x, n, p) + 0.5 * stats.binom.pmf(x, n, p) - alpha / 2

    lo = 0.0 if x == 0 else optimize.brentq(dn, 1e-12, 1 - 1e-12)
    hi = 1.0 if x == n else optimize.brentq(up, 1e-12, 1 - 1e-12)
    return lo, hi


def compute_midp():
    n = 25
    ps = np.linspace(0.01, 0.99, 197)
    cp = I.binom_coverage(I.clopper_pearson, n, ps)
    mp = I.binom_coverage(mid_p, n, ps)
    return nest({"n": n, "ps": ps, "cp": cp, "mid": mp, "cp_mean": float(cp.mean()), "mid_mean": float(mp.mean()),
                 "mid_min": float(mp.min()), "cp_min": float(cp.min())})


def compute_fieller():
    cases = {}
    for name, (mx, my, sx, sy) in {"clear": (10.0, 5.0, 1.0, 1.0), "weak": (2.2, 5.0, 1.0, 1.0), "rays": (1.7, 5.0, 1.0, 1.0),
                                   "none": (0.8, 0.9, 1.0, 1.0)}.items():
        kind, lo, hi = I.fieller(mx, my, sx ** 2, sy ** 2)
        d = np.sqrt((sy ** 2 + (my / mx) ** 2 * sx ** 2)) / abs(mx)  # delta-method SE of my/mx
        cases[name] = {"mx": mx, "my": my, "kind": kind, "lo": lo if np.isfinite(lo) else None, "hi": hi if np.isfinite(hi) else None,
                       "ratio": my / mx, "delta": [my / mx - 1.96 * d, my / mx + 1.96 * d]}
    return nest(cases)


def compute_simultaneous():
    h = men()
    g = rng(1956)
    n = 100
    x = h[g.integers(0, len(h), n)]
    xs, lo, hi, eps = I.dkw_band(x)
    # coverage of the band (whole curve inside) vs pointwise 95% intervals (all inside at once) over 2,000 samples
    grid = np.linspace(155, 197, 200)
    h_sorted = np.sort(h)
    Ftrue = np.searchsorted(h_sorted, grid, side="right") / len(h)
    band_ok = point_ok = 0
    R = 2000
    for _ in range(R):
        s = np.sort(h[g.integers(0, len(h), n)])
        Fh = np.searchsorted(s, grid, side="right") / n
        band_ok += empirical_cdf_sup(s, h_sorted, population_sorted=True) <= eps
        se = np.sqrt(np.maximum(Fh * (1 - Fh), 1e-12) / n)
        point_ok += np.all(np.abs(Fh - Ftrue) <= 1.96 * se + 1e-12)
    # The DKW check is over the whole line; the Wald check is only over the stated grid.
    return nest({"x": xs, "lo": lo, "hi": hi, "eps": eps, "grid": grid, "Ftrue": Ftrue, "band_cov": band_ok / R,
                 "point_cov": point_ok / R, "point_grid_size": len(grid), "R": R, "n": n})


def compute_prediction():
    h = men()
    g = rng(1941)
    R, n = 20000, 10
    ci = pi = 0
    for _ in range(R):
        s = h[g.integers(0, len(h), n + 1)]
        x, new = s[:n], s[n]
        lo, hi = I.t_interval(x)
        ci += lo <= new <= hi
        lo, hi = I.prediction_interval(x)
        pi += lo <= new <= hi
    inc = W.income[W.adult]
    s = inc[g.integers(0, len(inc), (R, 20))]
    ord_ = np.mean((s[:, -1] > s[:, :-1].min(1)) & (s[:, -1] < s[:, :-1].max(1)))
    # the normal prediction interval on incomes, n = 19
    pin = 0
    for row in s:
        lo, hi = I.prediction_interval(row[:-1])
        pin += lo <= row[-1] <= hi
    return nest({"ci": ci / R, "pi": pi / R, "order_inc": float(ord_), "order_theory": I.order_stat_coverage(19),
                 "pi_inc": pin / R})


def compute_welch():
    g = rng(1939)
    R = 100000
    th = 0.0
    x = g.uniform(th - 0.5, th + 0.5, (R, 2))
    lo, hi = x.min(1), x.max(1)
    cover = (lo <= th) & (th <= hi)
    wide = (hi - lo) >= 0.5
    return nest({"cov": float(cover.mean()), "p_wide": float(wide.mean()), "cov_wide": float(cover[wide].mean()),
                 "cov_narrow": float(cover[~wide].mean())})


def compute_credible():
    n = 50
    ps = np.linspace(0.005, 0.995, 397)
    cov_j = I.binom_coverage(jeffreys_credible, n, ps)

    def flat(x, n, alpha=0.05):
        return float(stats.beta.ppf(alpha / 2, x + 1, n - x + 1)), float(stats.beta.ppf(1 - alpha / 2, x + 1, n - x + 1))

    cov_f = I.binom_coverage(flat, n, ps)
    return nest({"ps": ps, "jeffreys": cov_j, "flat": cov_f, "j_mean": float(cov_j.mean()), "f_mean": float(cov_f.mean()),
                 "f_small": float(I.binom_coverage(flat, n, [0.01])[0]), "j_small": float(I.binom_coverage(jeffreys_credible, n, [0.01])[0])})


R_BOARD = 10000


def compute_board():
    g = rng(11_000)
    rows = []
    n, p = 50, 0.05
    xs = g.binomial(n, p, R_BOARD)
    names = {"wald": r"Wald", "wilson": r"Wilson", "agresti_coull": r"Agresti--Coull", "clopper_pearson": r"Clopper--Pearson",
             "jeffreys": r"Jeffreys"}
    for k, nm in names.items():
        m = I.BINOMIAL[k]
        ints = np.array([m(int(x), n) for x in xs])
        c = float(np.mean((ints[:, 0] <= p) & (p <= ints[:, 1])))
        rows.append(Row(11, nm, r"proportion $0.05$, \ $n = 50$", "coverage", 0.95, c, R_BOARD, float(np.mean(ints[:, 1] - ints[:, 0]))))
    h = men()
    hits = 0
    for _ in range(R_BOARD):
        s = h[g.integers(0, len(h), 11)]
        lo, hi = I.prediction_interval(s[:10])
        hits += lo <= s[10] <= hi
    rows.append(Row(11, r"$t$ prediction interval", r"a new man's height, \ $n = 10$", "coverage", 0.95, hits / R_BOARD, R_BOARD))
    inc = W.income[W.adult]
    hits = 0
    for _ in range(R_BOARD):
        s = inc[g.integers(0, len(inc), 20)]
        lo, hi = I.prediction_interval(s[:19])
        hits += lo <= s[19] <= hi
    rows.append(Row(11, r"$t$ prediction interval", r"a new income, \ $n = 19$", "coverage", 0.95, hits / R_BOARD, R_BOARD))
    save_rows(11, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "sawtooth": compute_sawtooth, "rain": compute_rain, "pivots": compute_pivots, "belt": compute_belt, "binom": compute_binom,
    "likelihood": compute_likelihood, "midp": compute_midp, "fieller": compute_fieller, "simultaneous": compute_simultaneous,
    "prediction": compute_prediction, "welch": compute_welch, "credible": compute_credible, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
