"""Precompute every number in Part 1 of *Statistics, Built* ("The Shape of Data").

    python -m videos.stats.stats1.compute            # everything missing (about a minute)
    python -m videos.stats.stats1.compute --force morph

Results are cached in ``.cache/stats1/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Population values
come from the World (``explainer.stats.world``, seed 1662), historical tables from the Museum
(``explainer.stats.museum``); every random choice here is seeded.

Items:
    populations  one sample of 25 adult heights against the World's mean; twenty samples' 95% intervals
    graunt       London christenings, burials and plague deaths 1629-1710 (the Bills, via Arbuthnot/Creighton);
                 Graunt's 1662 life table; the male surplus year by year
    world        the World's towns (position, region, population), its age pyramid, the truth table of Part 1
    heights      a sample of 200 adult heights: a dot plot's 60, histograms at three bin widths, the Sturges /
                 Scott / Freedman-Diaconis widths, the population's density
    centers      nine incomes for the loss curves; L^p centres of 200 incomes for p in [1, inf]; the mode by
                 a shrinking window; clock times and their circular (Frechet) mean
    spread       three heights for the R^3 picture; SD, MAD and IQR of heights and incomes; Chebyshev's bound
                 against the World's actual fractions
    quantiles    40 incomes for the ECDF and the box plot; box plots of 300 incomes in each of the 10 regions
    shape        skewness and kurtosis of heights, incomes and log incomes; the income tail on log-log axes
                 and its slope (the Pareto exponent), with the Hill estimate
    qq           normal QQ plots: Quetelet's chests (Stigler's corrected table), men's heights, incomes, and a
                 heavy-tailed t(3) sample
    boxcox       the Box-Cox profile log-likelihood of 300 incomes; skewness at lambda = 1, 1/2, 0, -1/2; the
                 square root stabilizing Poisson spreads
    correlation  400 families: mid-parent and child heights, r, the slope, the quadrant counts; r among the
                 tallest quarter of parents (restriction of range); three-point vectors and their cosine
    anscombe     the quartet's summary statistics
    morph        same statistics, different pictures: a World cloud annealed into the word STATS and then into a
                 ring, holding the means, SDs and correlation to two decimals (Matejka & Fitzmaurice 2017)
    simpson      the World's clinic: recovery by treatment, overall and within each severity
    sampling     20 samples of 100 adult heights (their histograms and means) and 2,000 sample means
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.world import World

CACHE = Cache("stats1")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def adult_heights(n, seed):
    return W.height[W.sample(n, among=W.adult, seed=seed)]


def adult_incomes(n, seed):
    return W.income[W.sample(n, among=W.adult, seed=seed)]


# ---------------------------------------------------------------------------
def compute_graunt():
    years = np.array(museum.ARB_YEARS)
    males, females = np.array(museum.ARB_MALES), np.array(museum.ARB_FEMALES)
    chr_ = males + females
    burials = np.array(museum.ARB_BURIALS)
    plague = np.array(museum.ARB_PLAGUE)
    window = years <= 1660  # the years Graunt could read in 1662
    surplus = males > females
    assert surplus.all()  # Arbuthnot's observation: every one of the 82 years
    return {
        "years": years, "christenings": chr_, "burials": burials, "plague": plague, "males": males,
        "females": females, "ratio": males / females,
        "graunt_last": 1660, "n_years": int(len(years)), "all_male_surplus": bool(surplus.all()),
        "ratio_window": float(males[window].sum() / females[window].sum()),
        "burials_1665": int(burials[years == 1665][0]), "plague_1665": int(plague[years == 1665][0]),
        "chr_1665": int(chr_[years == 1665][0]),
        "excess_window": float((burials[window] - chr_[window]).mean()),
        "life_ages": museum.GRAUNT_AGES, "life_alive": museum.GRAUNT_ALIVE,
    }


def compute_world():
    t = W.towns
    pop = np.bincount(W.town, minlength=len(t["xy"]))
    ages = W.age
    edges = np.arange(0, 101, 5)
    men = np.histogram(ages[W.male], edges)[0]
    women = np.histogram(ages[~W.male], edges)[0]
    h = W.height[W.adult]
    y = W.income[W.adult]
    return {
        "xy": t["xy"], "region": t["region"], "pop": pop, "seats": t["seats"],
        "age_edges": edges, "age_men": men, "age_women": women,
        "n": int(W.n), "n_adults": int(W.adult.sum()), "n_towns": int(len(pop)), "n_regions": 10,
        "largest_town": int(pop.max()), "smallest_town": int(pop.min()),
        "mean_height": W.truth("mean_height"), "sd_height": W.truth("sd_height"),
        "mean_height_men": float(W.height[W.adult & W.male].mean()),
        "mean_height_women": float(W.height[W.adult & ~W.male].mean()),
        "mean_income": W.truth("mean_income"), "median_income": W.truth("median_income"),
        "income_q": [float(v) for v in np.quantile(y, [0.1, 0.25, 0.5, 0.75, 0.9, 0.99])],
        "max_income": float(y.max()),
        "share_top1": float(np.sort(y)[-len(y) // 100:].sum() / y.sum()),
        "height_hist_edges": np.arange(130, 211, 1.0),
        "height_hist": np.histogram(h, np.arange(130, 211, 1.0))[0] / len(h),
    }


def compute_heights():
    x = adult_heights(200, seed=1)
    n = len(x)
    iqr = np.subtract(*np.quantile(x, [0.75, 0.25]))
    sturges_k = int(math.ceil(math.log2(n) + 1))
    h_sturges = (x.max() - x.min()) / sturges_k
    h_scott = 3.49 * x.std(ddof=1) * n ** (-1 / 3)
    h_fd = 2 * iqr * n ** (-1 / 3)
    # the population's density (all adults), for the overlay
    pop = W.height[W.adult]
    grid = np.linspace(135, 205, 281)
    kde = stats.gaussian_kde(pop[::50], bw_method=0.08)
    return {"x": x, "n": n, "dots": x[:60], "h_sturges": float(h_sturges), "k_sturges": sturges_k,
            "h_scott": float(h_scott), "h_fd": float(h_fd), "iqr": float(iqr), "sd": float(x.std(ddof=1)),
            "mean": float(x.mean()), "grid": grid, "pop_density": kde(grid),
            "pop_mean": float(pop.mean())}


def lp_center(x, p):
    if np.isinf(p):
        return float((x.min() + x.max()) / 2)
    if p == 1:
        return float(np.median(x))
    f = lambda c: np.sum(np.abs(x - c) ** p)  # noqa: E731
    return float(optimize.minimize_scalar(f, bounds=(x.min(), x.max()), method="bounded",
                                          options={"xatol": 1e-6 * (x.max() - x.min())}).x)


def compute_centers():
    nine = np.sort(adult_incomes(9, seed=2)) / 1000  # thousands
    grid = np.linspace(nine.min() - 5, nine.max() + 5, 400)
    sq = np.array([np.sum((nine - c) ** 2) for c in grid])
    ab = np.array([np.sum(np.abs(nine - c)) for c in grid])
    big = adult_incomes(200, seed=3) / 1000
    ps = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0]
    lp = [lp_center(big, p) for p in ps]
    # the mode: the centre of the window of width w holding the most points, as w shrinks
    hs = adult_heights(400, seed=4)
    modes = []
    for w in (20.0, 10.0, 5.0, 2.5):
        cs = np.linspace(hs.min(), hs.max(), 2000)
        counts = [np.sum(np.abs(hs - c) <= w / 2) for c in cs]
        modes.append([w, float(cs[int(np.argmax(counts))])])
    # clock times (illustrative): 10:40 pm ... 1:30 am, in hours after midnight
    times = np.array([22 + 40 / 60, 23 + 10 / 60, 23 + 35 / 60, 0 + 5 / 60, 0 + 50 / 60, 1 + 30 / 60])
    arith = float(times.mean())
    ang = 2 * np.pi * times / 24
    circ = float((np.arctan2(np.sin(ang).mean(), np.cos(ang).mean()) * 24 / (2 * np.pi)) % 24)
    # Frechet mean on the circle: minimize the sum of squared arc distances
    arc = lambda c: np.sum(np.minimum(np.abs(times - c), 24 - np.abs(times - c)) ** 2)  # noqa: E731
    cgrid = np.linspace(0, 24, 4801)
    frechet = float(cgrid[np.argmin([arc(c) for c in cgrid])])
    return {"nine": nine, "grid": grid, "sq": sq, "ab": ab, "mean9": float(nine.mean()),
            "median9": float(np.median(nine)), "big": big, "ps": ps, "lp": lp,
            "midrange": float((big.min() + big.max()) / 2), "mean200": float(big.mean()),
            "median200": float(np.median(big)), "max200": float(big.max()),
            "modes": modes, "heights400": hs, "times": times, "arith": arith, "circ": circ, "frechet": frechet}


def compute_spread():
    three = np.round(adult_heights(3, seed=5), 1)
    h, y = W.height[W.adult], W.income[W.adult]

    def summary(v):
        q1, q3 = np.quantile(v, [0.25, 0.75])
        return {"sd": float(v.std()), "mad": float(np.median(np.abs(v - np.median(v)))), "iqr": float(q3 - q1),
                "mean": float(v.mean())}

    ks = [1.5, 2.0, 3.0, 4.0]
    frac = lambda v, k: float(np.mean(np.abs(v - v.mean()) < k * v.std()))  # noqa: E731
    return {"three": three, "mean3": float(three.mean()), "height": summary(h), "income": summary(y),
            "ks": ks, "cheb": [1 - 1 / k ** 2 for k in ks], "frac_height": [frac(h, k) for k in ks],
            "frac_income": [frac(y, k) for k in ks]}


def compute_quantiles():
    x = np.sort(adult_incomes(40, seed=6)) / 1000
    q = {k: float(v) for k, v in zip(("q10", "q25", "q50", "q75", "q90"), np.quantile(x, [0.1, 0.25, 0.5, 0.75, 0.9]))}
    from explainer.stats.viz import five_numbers

    regions = []
    for k in range(10):
        idx = W.sample(300, among=W.adult & (W.region == k), seed=100 + k)
        regions.append(five_numbers(W.income[idx] / 1000))
    return {"x": x, **q, "five": five_numbers(x), "regions": regions,
            "region_median_true": [float(np.median(W.income[W.adult & (W.region == k)]) / 1000) for k in range(10)]}


def compute_shape():
    h, y = W.height[W.adult], W.income[W.adult]
    ly = np.log(y)

    def mom(v):
        z = (v - v.mean()) / v.std()
        return {"skew": float(np.mean(z ** 3)), "kurt": float(np.mean(z ** 4) - 3)}

    # the tail: S(x) = P(Y > x) on log-log axes
    xs = np.geomspace(20_000, 5_000_000, 60)
    ys = np.sort(y)
    surv = 1 - np.searchsorted(ys, xs, side="right") / len(ys)
    sel = (xs >= 300_000) & (xs <= 3_000_000) & (surv > 0)
    slope, intercept = np.polyfit(np.log10(xs[sel]), np.log10(surv[sel]), 1)
    k = 2000  # Hill's estimator from the top k incomes
    top = ys[-k - 1:]
    hill = float(1 / np.mean(np.log(top[1:] / top[0])))
    z = (y - y.mean()) / y.std()
    top_share = float(np.max(z) ** 3 / len(y))  # the richest adult's term in the skewness, mean of z^3
    perm = rng(15).permutation(len(y))
    sizes = [1_000, 10_000, 100_000, len(y)]
    skew_n = [mom(y[perm[:k]])["skew"] for k in sizes]
    kurt_n = [mom(y[perm[:k]])["kurt"] for k in sizes]
    return {"height": mom(h), "income": mom(y), "logincome": mom(ly), "tail_x": xs, "tail_s": surv,
            "top_share": top_share, "z_max": float(np.max(z)), "sizes": sizes, "skew_n": skew_n, "kurt_n": kurt_n,
            "slope": float(slope), "intercept": float(intercept), "alpha_true": W.PARETO_ALPHA, "hill": hill,
            "hill_k": k, "mean": float(y.mean()), "median": float(np.median(y)),
            "log_grid": np.linspace(np.log10(3000), np.log10(3e6), 120),
            "log_hist": np.histogram(np.log10(y), np.linspace(np.log10(3000), np.log10(3e6), 61))[0] / len(y),
            "lin_hist": np.histogram(y / 1000, np.linspace(0, 300, 61))[0] / len(y)}


def qq_points(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    p = (np.arange(1, n + 1) - 0.5) / n
    return stats.norm.ppf(p), x


def qq_demo(men):
    """A seeded random subset, paired with quantiles for its own sample size."""
    return qq_points(rng(71).choice(men, 15, replace=False))


def inverse_quantiles(x):
    """Empirical generalized-inverse quantiles, distinct from interpolated quartiles."""
    return dict(zip(("q10", "q25", "q50", "q75", "q90"),
                    np.quantile(x, [0.1, 0.25, 0.5, 0.75, 0.9], method="inverted_cdf")))


def correlation_cloud(r, n, g):
    """Illustrative points with exactly the displayed sample correlation."""
    a = g.standard_normal(n)
    a = (a - a.mean()) / a.std()
    noise = g.standard_normal(n)
    noise -= noise.mean()
    noise -= (noise @ a) / (a @ a) * a
    noise /= noise.std()
    return a, r * a + np.sqrt(max(1 - r * r, 0)) * noise


def compute_qq():
    chest = np.repeat(museum.CHEST_IN, museum.CHEST_COUNT).astype(float)
    # grouped data: one point per class, at the normal quantile of its mid cumulative proportion
    cum = np.cumsum(museum.CHEST_COUNT)
    n = cum[-1]
    mid = (cum - np.array(museum.CHEST_COUNT) / 2) / n
    zc = stats.norm.ppf(mid)
    slope, icept = np.polyfit(zc, museum.CHEST_IN, 1, w=np.sqrt(museum.CHEST_COUNT))
    men = W.height[W.sample(300, among=W.adult & W.male, seed=7)]
    inc = adult_incomes(300, seed=8) / 1000
    t3 = rng(9).standard_t(3, 300)
    out = {"chest_z": zc, "chest_x": np.array(museum.CHEST_IN, float), "chest_n": int(n),
           "chest_mean": float(chest.mean()), "chest_sd": float(chest.std()), "chest_slope": float(slope),
           "chest_icept": float(icept)}
    for name, v in (("men", men), ("income", inc), ("t3", t3)):
        z, s = qq_points(v)
        out[name + "_z"], out[name + "_x"] = z, s
        out[name + "_fit"] = [float(np.median(s)), float(np.subtract(*np.quantile(s, [0.75, 0.25])) / 1.349)]
    return out


def compute_boxcox():
    y = adult_incomes(300, seed=10) / 1000
    lams = np.linspace(-1.0, 1.5, 101)
    ll = [float(stats.boxcox_llf(l, y)) for l in lams]
    lam_hat = float(stats.boxcox_normmax(y, method="mle"))
    top = float(stats.boxcox_llf(lam_hat, y))
    cut = top - stats.chi2.ppf(0.95, 1) / 2  # the likelihood-ratio 95% interval
    f = lambda l: stats.boxcox_llf(l, y) - cut  # noqa: E731
    lam_lo = float(optimize.brentq(f, lam_hat - 2, lam_hat))
    lam_hi = float(optimize.brentq(f, lam_hat, lam_hat + 2))

    def bc(v, l):
        return np.log(v) if abs(l) < 1e-12 else (v ** l - 1) / l

    show = [1.0, 0.5, 0.0, -0.5]
    trans = {str(l): bc(y, l) for l in show}
    sk = {str(l): float(stats.skew(bc(y, l))) for l in show}
    g = rng(11)
    means = [2, 8, 32, 128]
    pois = [g.poisson(m, 400) for m in means]
    return {"y": y, "lams": lams, "ll": np.array(ll), "lam_hat": lam_hat, "show": show, "lam_lo": lam_lo,
            "lam_hi": lam_hi, "ll_top": top, "ll_zero": float(stats.boxcox_llf(0.0, y)),
            **{"t_" + k: v for k, v in trans.items()}, "skew": sk, "pois_means": means,
            "pois_sd": [float(p.std()) for p in pois], "pois_sd_sqrt": [float(np.sqrt(p).std()) for p in pois],
            "pois": np.array(pois)}


def compute_correlation():
    f = W.families
    g = rng(12)
    i = np.sort(g.choice(len(f["child"]), 400, replace=False))
    mid = (f["father"][i] + f["mother"][i] / W.HEIGHT_MEAN[False] * W.HEIGHT_MEAN[True]) / 2  # Galton: women x 1.08
    child = np.where(f["son"][i], f["child"][i], f["child"][i] / W.HEIGHT_MEAN[False] * W.HEIGHT_MEAN[True])
    r = float(np.corrcoef(mid, child)[0, 1])
    slope = float(np.polyfit(mid, child, 1)[0])
    dx, dy = mid - mid.mean(), child - child.mean()
    quad = {"pp": int(np.sum((dx > 0) & (dy > 0))), "mm": int(np.sum((dx < 0) & (dy < 0))),
            "pm": int(np.sum((dx > 0) & (dy < 0))), "mp": int(np.sum((dx < 0) & (dy > 0)))}
    tall = mid > np.quantile(mid, 0.75)
    r_tall = float(np.corrcoef(mid[tall], child[tall])[0, 1])
    # three points: centred vectors and their cosine
    xs = np.array([2.0, 5.0, 8.0])
    ys = np.array([3.0, 3.5, 7.5])
    xc, yc = xs - xs.mean(), ys - ys.mean()
    cos = float(xc @ yc / np.linalg.norm(xc) / np.linalg.norm(yc))
    return {"mid": mid, "child": child, "r": r, "slope": slope, "quad": quad, "tall": tall, "r_tall": r_tall,
            "xs": xs, "ys": ys, "xc": xc, "yc": yc, "cos": cos, "angle": float(np.degrees(np.arccos(cos))),
            "r_check": float(np.corrcoef(xs, ys)[0, 1]),
            "cov": float(np.mean(dx * dy)), "sdx": float(mid.std()), "sdy": float(child.std())}


def compute_anscombe():
    out = {}
    for k, (x, y) in museum.ANSCOMBE.items():
        x, y = np.array(x, float), np.array(y, float)
        b, a = np.polyfit(x, y, 1)
        out[str(k)] = {"x": x.tolist(), "y": y.tolist(), "mx": float(x.mean()), "my": float(y.mean()), "vx": float(x.var(ddof=1)),
                       "vy": float(y.var(ddof=1)), "r": float(np.corrcoef(x, y)[0, 1]), "b": float(b), "a": float(a)}
    return {"sets": out}


# ---------------------------------------------------------------------------
# Same statistics, different graphs (Matejka & Fitzmaurice 2017)
# ---------------------------------------------------------------------------
def letters_segments():
    """The word STATS as stroke segments in a 100 x 100 box."""
    segs = []
    w, hgt, y0 = 14.0, 58.0, 21.0
    for k, ch in enumerate("STATS"):
        x0 = 6 + k * 18.5
        P = lambda a, b: (x0 + a * w, y0 + b * hgt)  # noqa: E731
        if ch == "S":
            pts = [P(1, 1), P(0, 1), P(0, 0.5), P(1, 0.5), P(1, 0), P(0, 0)]
            segs += list(zip(pts[:-1], pts[1:]))
        elif ch == "T":
            segs += [(P(0, 1), P(1, 1)), (P(0.5, 1), P(0.5, 0))]
        elif ch == "A":
            segs += [(P(0, 0), P(0.5, 1)), (P(0.5, 1), P(1, 0)), (P(0.22, 0.42), P(0.78, 0.42))]
    return np.array(segs, float)


def ring_segments(cx, cy, rx, ry, k=72):
    t = np.linspace(0, 2 * np.pi, k + 1)
    pts = np.column_stack([cx + rx * np.cos(t), cy + ry * np.sin(t)])
    return np.stack([pts[:-1], pts[1:]], axis=1)


def seg_dist(p, segs):
    """Distance from points p (m, 2) to the nearest of segments (k, 2, 2)."""
    a, b = segs[:, 0], segs[:, 1]
    ab = b - a
    t = np.clip(((p[:, None, :] - a[None]) * ab[None]).sum(-1) / (ab ** 2).sum(-1)[None], 0, 1)
    proj = a[None] + t[..., None] * ab[None]
    return np.sqrt(((p[:, None, :] - proj) ** 2).sum(-1)).min(1)


def summary2(P):
    return np.round([P[:, 0].mean(), P[:, 1].mean(), P[:, 0].std(ddof=1), P[:, 1].std(ddof=1),
                     np.corrcoef(P[:, 0], P[:, 1])[0, 1]], 2)


def anneal(P, segs, iters, g, snapshots=320, t0=0.4, t1=0.0, step=0.6):
    P = P.copy()
    target = summary2(P)
    frames = [P.copy()]
    every = iters // snapshots
    d = seg_dist(P, segs)
    for it in range(iters):
        temp = t0 + (t1 - t0) * it / iters
        i = g.integers(len(P))
        old = P[i].copy()
        P[i] = old + g.normal(0, step, 2)
        nd = seg_dist(P[i:i + 1], segs)[0]
        if (nd < d[i] or g.random() < temp) and np.array_equal(summary2(P), target):
            d[i] = nd
        else:
            P[i] = old
        if (it + 1) % every == 0:
            frames.append(P.copy())
    return P, np.array(frames)


def compute_morph():
    g = rng(13)
    # the start: 142 World adults, (age, log income), rescaled into the 100 x 100 box
    idx = W.sample(142, among=W.adult & (W.age < 80), seed=14)
    a, li = W.age[idx].astype(float), np.log(W.income[idx])
    P = np.column_stack([(a - a.mean()) / a.std(), (li - li.mean()) / li.std()])
    P = P * np.array([27.0, 21.0]) + np.array([52.0, 50.0])
    start = P.copy()
    s0 = summary2(P)
    P1, f1 = anneal(P, letters_segments(), 320_000, g)
    P2, f2 = anneal(P1, ring_segments(52, 50, 38, 30), 220_000, g)
    assert np.array_equal(summary2(P1), s0) and np.array_equal(summary2(P2), s0)
    # the scene interpolates linearly between snapshots: record the worst drift of the five statistics there
    frames = np.concatenate([f1, f2[1:]])
    drift = 0.0
    for A, B in zip(frames[:-1], frames[1:]):
        for t in (0.25, 0.5, 0.75):
            M = (1 - t) * A + t * B
            raw = np.array([M[:, 0].mean(), M[:, 1].mean(), M[:, 0].std(ddof=1), M[:, 1].std(ddof=1),
                            np.corrcoef(M[:, 0], M[:, 1])[0, 1]])
            drift = max(drift, float(np.max(np.abs(np.round(raw, 2) - s0))))
    return {"start": start, "frames1": f1, "frames2": f2, "stats": s0.tolist(), "letters": letters_segments(),
            "dist1": float(seg_dist(P1, letters_segments()).mean()),
            "dist2": float(seg_dist(P2, ring_segments(52, 50, 38, 30)).mean()),
            "corr_raw": float(np.corrcoef(a, li)[0, 1]), "interp_drift": drift,
            "bounds": [float(frames[..., 0].min()), float(frames[..., 0].max()), float(frames[..., 1].min()),
                       float(frames[..., 1].max())]}


def compute_simpson():
    c = W.clinic
    out = {}
    for name, m in (("all", np.ones_like(c["severe"])), ("mild", ~c["severe"]), ("severe", c["severe"])):
        for tr in (True, False):
            sel = m & (c["treated"] == tr)
            out[f"{name}_{'t' if tr else 'u'}_n"] = int(sel.sum())
            out[f"{name}_{'t' if tr else 'u'}_rate"] = float(c["recovered"][sel].mean())
    out["share_severe_t"] = float(c["severe"][c["treated"]].mean())
    out["share_severe_u"] = float(c["severe"][~c["treated"]].mean())
    out["n"] = int(len(c["severe"]))
    return out


def compute_sampling():
    pop = W.height[W.adult]
    edges = np.arange(140, 206, 3.0)
    samples, means, hists = [], [], []
    for s in range(20):
        x = adult_heights(100, seed=1000 + s)
        samples.append(x)
        means.append(float(x.mean()))
        hists.append(np.histogram(x, edges)[0])
    many = [float(adult_heights(100, seed=5000 + s).mean()) for s in range(2000)]
    return {"edges": edges, "samples": np.array(samples), "means": means, "hists": np.array(hists),
            "many": np.array(many), "mu": float(pop.mean()), "sigma": float(pop.std()),
            "sd_means": float(np.std(many)), "se_formula": float(pop.std() / 10)}



def compute_populations():
    mu = W.truth("mean_height")
    x = adult_heights(25, seed=21)
    xs = [adult_heights(25, seed=300 + k) for k in range(20)]
    means = [float(v.mean()) for v in xs]
    half = [float(1.96 * v.std(ddof=1) / 5) for v in xs]
    cover = [abs(m - mu) <= h for m, h in zip(means, half)]
    return {"mu": mu, "x": x, "xbar": float(x.mean()), "err": float(x.mean() - mu), "means": means,
            "half": half, "cover": cover, "n_cover": int(sum(cover)), "n_adults": int(W.adult.sum())}


ITEMS = {
    "graunt": compute_graunt, "populations": compute_populations, "world": compute_world, "heights": compute_heights, "centers": compute_centers,
    "spread": compute_spread, "quantiles": compute_quantiles, "shape": compute_shape, "qq": compute_qq,
    "boxcox": compute_boxcox, "correlation": compute_correlation, "anscombe": compute_anscombe,
    "morph": compute_morph, "simpson": compute_simpson, "sampling": compute_sampling,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
