"""statkit.empirical: empirical processes (Part 48 of *Statistics, Built*).

Everything here is small, exact where it can be, and checked in ``tests/test_stats_kit_empirical.py``:

* the Kolmogorov distribution and KS statistics; Brownian bridges; the empirical process of a sample;
* Rademacher averages, including the exact expected maximum of a simple random walk (the half-line class);
* growth functions: brute-force dichotomy counts for intervals and half-planes, the Sauer--Shelah bound;
* covering and bracketing numbers: greedy nets, the half-line brackets, entropy formulas;
* chaining for Brownian motion on dyadic nets (Dudley); the one-step union bound it beats;
* Bousquet's form of Talagrand's inequality; the DKW bound with Massart's constant;
* Durbin's covariance for the estimated-parameter empirical process (normal location--scale);
* the effect of an estimated nuisance parameter on a Z-estimator (mean absolute deviation, exponential data);
* Chernoff's distribution (argmax of two-sided Brownian motion minus t^2) by simulation; the Grenander constant;
* KS bands for F: the Kolmogorov quantile, the exact finite-n quantile, the bootstrap and the multiplier bootstrap.
"""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np
from scipy import integrate, stats

# ----------------------------------------------------------------------------------------------------------- KS


def kolmogorov_cdf(t, terms: int = 200) -> np.ndarray:
    """P(sup |B| <= t) for a Brownian bridge B: 1 - 2 sum (-1)^(k-1) exp(-2 k^2 t^2) for t >= 0.6, and the Jacobi
    theta form sqrt(2 pi)/t sum exp(-(2k-1)^2 pi^2 / (8 t^2)) below, where the alternating series is unstable."""
    t = np.atleast_1d(np.asarray(t, float))
    k = np.arange(1, terms + 1)[:, None]
    tt = np.maximum(t, 1e-3)[None, :]
    big = 1 - 2 * np.sum((-1.0) ** (k - 1) * np.exp(-2 * k ** 2 * tt ** 2), axis=0)
    small = math.sqrt(2 * math.pi) / tt[0] * np.sum(np.exp(-((2 * k - 1) ** 2) * math.pi ** 2 / (8 * tt ** 2)), axis=0)
    s = np.where(t >= 0.6, big, small)
    return np.where(t <= 0, 0.0, np.clip(s, 0.0, 1.0))


def kolmogorov_quantile(p: float) -> float:
    lo, hi = 0.2, 4.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if kolmogorov_cdf(mid)[0] < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kolmogorov_density(t) -> np.ndarray:
    """The derivative of ``kolmogorov_cdf``, by a central difference of the stable forms."""
    t = np.atleast_1d(np.asarray(t, float))
    h = 1e-5
    d = (kolmogorov_cdf(t + h) - kolmogorov_cdf(np.maximum(t - h, 0))) / (t + h - np.maximum(t - h, 0))
    return np.where(t <= 0, 0.0, np.maximum(d, 0.0))


def ks_stat(x, cdf) -> float:
    """sup_x |F_n(x) - F(x)| for a continuous F, computed at the order statistics."""
    u = np.sort(cdf(np.asarray(x, float)))
    n = len(u)
    i = np.arange(1, n + 1)
    return float(max(np.max(i / n - u), np.max(u - (i - 1) / n)))


def ks_stats_uniform(u: np.ndarray) -> np.ndarray:
    """Row-wise KS statistics of uniform samples (an m x n array)."""
    u = np.sort(u, axis=1)
    n = u.shape[1]
    i = np.arange(1, n + 1)
    return np.maximum(np.max(i / n - u, axis=1), np.max(u - (i - 1) / n, axis=1))


def empirical_process(x, cdf, grid) -> np.ndarray:
    """sqrt(n)(F_n - F) on a grid."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    fn = np.searchsorted(x, grid, side="right") / n
    return math.sqrt(n) * (fn - cdf(np.asarray(grid, float)))


def brownian_bridge(m: int, rng: np.random.Generator, reps: int = 1) -> np.ndarray:
    """reps Brownian bridges on the grid j/m, j = 0..m."""
    w = np.concatenate([np.zeros((reps, 1)), np.cumsum(rng.standard_normal((reps, m)) / math.sqrt(m), axis=1)], axis=1)
    t = np.linspace(0, 1, m + 1)
    return w - t[None, :] * w[:, -1:]


# --------------------------------------------------------------------------------------------- Rademacher


def walk_max_abs_expectation(n: int) -> float:
    """E max_{0<=k<=n} |S_k| for a simple symmetric random walk, exactly, by absorption at +-a."""
    total = 0.0
    for a in range(1, n + 1):
        # P(max |S_k| < a): walk on -(a-1)..(a-1), killed on leaving
        size = 2 * a - 1
        p = np.zeros(size)
        p[a - 1] = 1.0
        for _ in range(n):
            q = np.zeros(size)
            q[1:] += 0.5 * p[:-1]
            q[:-1] += 0.5 * p[1:]
            p = q
        total += 1.0 - p.sum()
    return total


def rademacher_halflines(n: int) -> float:
    """The empirical Rademacher average E sup_t |(1/n) sum eps_i 1{X_i <= t}| for n distinct points: the expected
    maximum absolute partial sum of n signs, over n.  Exact."""
    return walk_max_abs_expectation(n) / n


def rademacher_finite(values: np.ndarray, rng: np.random.Generator, reps: int = 2000) -> float:
    """Monte Carlo E sup_f |(1/n) sum eps_i f(x_i)| for a finite class given as a (k x n) matrix of values."""
    v = np.asarray(values, float)
    n = v.shape[1]
    eps = rng.choice([-1.0, 1.0], size=(reps, n))
    return float(np.mean(np.max(np.abs(eps @ v.T), axis=1)) / n)


def massart_finite(values: np.ndarray) -> float:
    """Massart's finite-class lemma: E sup |(1/n) sum eps f| <= max_f ||f||_n sqrt(2 log(2k)) / sqrt(n)."""
    v = np.asarray(values, float)
    k, n = v.shape
    r = float(np.max(np.sqrt(np.mean(v ** 2, axis=1))))
    return r * math.sqrt(2 * math.log(2 * k)) / math.sqrt(n)


# ---------------------------------------------------------------------------------------------------- VC


def sauer_shelah(n: int, d: int) -> int:
    return int(sum(math.comb(n, i) for i in range(0, min(d, n) + 1)))


def dichotomies_halflines(x) -> int:
    x = np.sort(np.asarray(x, float))
    return len(x) + 1


def dichotomies_intervals(x) -> int:
    """Distinct subsets {x_i in [a, b]} for distinct reals: contiguous runs plus the empty set."""
    n = len(np.unique(x))
    return n * (n + 1) // 2 + 1


def dichotomies_halfplanes(pts) -> int:
    """Distinct subsets {p : <w, p> <= b} cut out by closed half-planes, by brute force over critical directions."""
    p = np.asarray(pts, float)
    n = len(p)
    if n <= 1:
        return n + 1
    angles = []
    for i, j in combinations(range(n), 2):
        d = p[j] - p[i]
        a = math.atan2(d[1], d[0]) + math.pi / 2
        angles += [a % (2 * math.pi), (a + math.pi) % (2 * math.pi)]
    angles = np.sort(np.array(angles))
    mids = (angles + np.roll(angles, -1)) / 2
    mids[-1] = (angles[-1] + angles[0] + 2 * math.pi) / 2
    seen = set()
    for th in mids:
        w = np.array([math.cos(th), math.sin(th)])
        order = np.argsort(p @ w)
        mask = 0
        seen.add(0)
        for k in order:
            mask |= 1 << int(k)
            seen.add(mask)
    return len(seen)


def dichotomies_rectangles(pts) -> int:
    """Distinct subsets cut out by closed axis-aligned rectangles (brute force over boundary points)."""
    p = np.asarray(pts, float)
    xs, ys = np.unique(p[:, 0]), np.unique(p[:, 1])
    seen = {0}
    for a in range(len(xs)):
        for b in range(a, len(xs)):
            for c in range(len(ys)):
                for d in range(c, len(ys)):
                    m = (p[:, 0] >= xs[a]) & (p[:, 0] <= xs[b]) & (p[:, 1] >= ys[c]) & (p[:, 1] <= ys[d])
                    seen.add(sum(1 << int(i) for i in np.nonzero(m)[0]))
    return len(seen)


def growth_halfplanes(n: int) -> int:
    """Points in general position: n(n - 1) + 2 half-plane dichotomies (Cover 1965)."""
    return n * (n - 1) + 2 if n >= 1 else 1


# ------------------------------------------------------------------------------------- covering, bracketing


def greedy_cover(vectors: np.ndarray, eps: float, metric: str = "l2") -> int:
    """Size of a greedy eps-net (centres taken from the set) under the empirical L2 or sup metric."""
    v = np.asarray(vectors, float)
    alive = np.ones(len(v), bool)
    count = 0
    while alive.any():
        i = int(np.nonzero(alive)[0][0])
        d = np.sqrt(np.mean((v - v[i]) ** 2, axis=1)) if metric == "l2" else np.max(np.abs(v - v[i]), axis=1)
        alive &= d > eps
        count += 1
    return count


def bracketing_halflines(eps: float) -> int:
    """L2(P) bracketing number of {1{x <= t}} for continuous P: brackets of P-mass eps^2, so ceil(1/eps^2)."""
    return int(math.ceil(1 / eps ** 2))


def lipschitz_paths(m: int, k: int, rng: np.random.Generator) -> np.ndarray:
    """k random 1-Lipschitz functions on m grid points of [0, 1], with f(0) uniform on [0, 1], clipped to [0, 1]."""
    steps = rng.uniform(-1, 1, size=(k, m - 1)) / (m - 1)
    f = np.concatenate([rng.uniform(0, 1, (k, 1)), steps], axis=1).cumsum(axis=1)
    return np.clip(f, 0, 1)


# ------------------------------------------------------------------------------------------------- chaining


def chaining_bound_bm(levels: int = 40) -> dict:
    """Dudley-style chaining bound for E sup_{t in [0,1]} B_t on dyadic nets.  Level-k links B(t) - B(parent) have
    sd 2^{-k/2}; there are 2^{k-1} new points, so E max of the links <= 2^{-k/2} sqrt(2 log 2^{k-1}).  Returns the per-level
    terms and their sum; also the one-step union bound over 2^K points, which grows like sqrt(2 K log 2)."""
    terms = [1 / math.sqrt(2 * math.pi)]  # level 0: E max(B_0, B_1) = E max(0, B_1)
    for k in range(1, levels + 1):
        sd = 2 ** (-k / 2)  # each new point j/2^k is 2^-k from its parent, so the link has sd 2^{-k/2}
        terms.append(sd * math.sqrt(2 * math.log(2 ** (k - 1))))  # the max of 2^{k-1} such links (0 for one)
    union = [math.sqrt(2 * math.log(2 ** k)) for k in range(1, levels + 1)]
    return {"terms": terms, "bound": float(sum(terms)), "union": union, "exact": math.sqrt(2 / math.pi)}


def dudley_integral(log_n, delta: float, m: int = 4000) -> float:
    """int_0^delta sqrt(log N(eps)) d eps for a callable log N."""
    e = np.linspace(delta / m, delta, m)
    return float(np.trapezoid(np.sqrt(np.maximum(log_n(e), 0)), e))


def bm_sup_on_grid(k: int, rng: np.random.Generator, reps: int = 4000, fine: int = 12) -> float:
    """E max_{j <= 2^k} B(j / 2^k), simulated on a fine dyadic path (2^fine steps)."""
    m = 2 ** fine
    w = np.concatenate([np.zeros((reps, 1)), np.cumsum(rng.standard_normal((reps, m)) / math.sqrt(m), axis=1)], axis=1)
    idx = np.arange(0, m + 1, m // (2 ** k))
    return float(np.mean(np.max(w[:, idx], axis=1)))


# ------------------------------------------------------------------------------------------- concentration


def bousquet_tail(t, n: int, sigma2: float, ez: float, b: float = 1.0) -> np.ndarray:
    """Bousquet (2002): for Z = sup_f sum (f(X_i) - Pf), |f - Pf| <= b, sigma^2 >= sup Var f,
    P(Z >= EZ + sqrt(2 x v) + b x / 3) <= exp(-x), v = n sigma^2 + 2 b EZ.  Returns the bound on P(Z >= EZ + t)."""
    t = np.atleast_1d(np.asarray(t, float))
    v = n * sigma2 + 2 * b * ez
    out = np.empty_like(t)
    for i, s in enumerate(t):
        lo, hi = 0.0, 1e4
        for _ in range(200):
            x = 0.5 * (lo + hi)
            if math.sqrt(2 * x * v) + b * x / 3 < s:
                lo = x
            else:
                hi = x
        out[i] = math.exp(-lo)
    return np.minimum(out, 1.0)


def dkw_tail(t, n: int) -> np.ndarray:
    """DKW with Massart's constant: P(sqrt(n) D_n > t) <= 2 exp(-2 t^2)."""
    t = np.atleast_1d(np.asarray(t, float))
    return np.minimum(2 * np.exp(-2 * t ** 2), 1.0)


# --------------------------------------------------------------------------------- estimated parameters


def durbin_variance_normal(z) -> np.ndarray:
    """Pointwise variance of the limit of sqrt(n)(F_n(x) - Phi((x - xbar)/s)) at z = (x - mu)/sigma (Durbin 1973):
    Phi(1 - Phi) - phi^2 - (z phi)^2 / 2."""
    z = np.asarray(z, float)
    P, p = stats.norm.cdf(z), stats.norm.pdf(z)
    return P * (1 - P) - p ** 2 - (z * p) ** 2 / 2


def durbin_variance_exponential(x) -> np.ndarray:
    """The same for the exponential with estimated rate (scale family): F(1-F) - (x f(x))^2 at rate 1."""
    x = np.asarray(x, float)
    F, f = 1 - np.exp(-x), np.exp(-x)
    return F * (1 - F) - (x * f) ** 2


def ks_estimated_normal(x) -> float:
    x = np.asarray(x, float)
    m, s = x.mean(), x.std(ddof=1)
    return ks_stat(x, lambda v: stats.norm.cdf((v - m) / s))


def ks_estimated_normal_rows(z: np.ndarray) -> np.ndarray:
    m = z.mean(axis=1, keepdims=True)
    s = z.std(axis=1, ddof=1, keepdims=True)
    return ks_stats_uniform(stats.norm.cdf((z - m) / s))


def parametric_bootstrap_ks(x, rng: np.random.Generator, B: int = 999) -> dict:
    """The KS test of normality with estimated parameters, calibrated by a parametric bootstrap."""
    x = np.asarray(x, float)
    n = len(x)
    d = ks_estimated_normal(x)
    db = ks_estimated_normal_rows(rng.standard_normal((B, n)))
    return {"D": d, "p": float((1 + np.sum(db >= d)) / (B + 1)), "crit95": float(np.quantile(db, 0.95))}


# ------------------------------------------------------------------------------------------------ nuisance


def mad_exponential() -> dict:
    """Mean absolute deviation of Exp(1) data, theta = E|X - c|, about the median (c = log 2) and about the mean
    (c = 1).  With c estimated, the influence function gains (2F(c) - 1)(...) times the nuisance's influence:
    zero at the median, not zero at the mean.  Returns theta, the naive variance (c known) and the correct one."""
    out = {}
    # about the median: IF of c-hat is (1/2 - 1{x <= m}) / f(m); the derivative 2F(m) - 1 = 0 kills it
    m = math.log(2)
    th_m = m  # E|X - log 2| = log 2 for Exp(1)
    def q(g, c):
        return integrate.quad(g, 0, c)[0] + integrate.quad(g, c, np.inf)[0]

    def ex2(c):
        return q(lambda x: (x - c) ** 2 * math.exp(-x), c)
    naive_m = ex2(m) - th_m ** 2
    out["median"] = {"c": m, "theta": th_m, "slope": 0.0, "naive": naive_m, "correct": naive_m}
    # about the mean: theta = 2/e; slope dtheta/dc = 2F(1) - 1 = 1 - 2/e; IF of xbar is x - 1
    c = 1.0
    th = 2 / math.e
    slope = 2 * (1 - math.exp(-c)) - 1
    naive = ex2(c) - th ** 2
    cov = q(lambda x: (abs(x - c) - th) * (x - c) * math.exp(-x), c)
    correct = naive + 2 * slope * cov + slope ** 2 * 1.0
    out["mean"] = {"c": c, "theta": th, "slope": slope, "naive": naive, "correct": correct, "cov": cov}
    return out


# -------------------------------------------------------------------------------------------- cube-root


def chernoff_draws(rng: np.random.Generator, reps: int = 4000, half: float = 2.5, m: int = 4000) -> np.ndarray:
    """argmax_t (W(t) - t^2) for two-sided Brownian motion W on [-half, half], m steps per side."""
    dt = half / m
    t = np.arange(1, m + 1) * dt
    out = np.empty(reps)
    for r in range(reps):
        right = np.cumsum(rng.standard_normal(m)) * math.sqrt(dt) - t ** 2
        left = np.cumsum(rng.standard_normal(m)) * math.sqrt(dt) - t ** 2
        ir, il = int(np.argmax(right)), int(np.argmax(left))
        best = max(0.0, right[ir], left[il])
        out[r] = 0.0 if best == 0.0 else (t[ir] if right[ir] >= left[il] else -t[il])
    return out


CHERNOFF_SD = 0.5133  # sqrt(0.26355) (Groeneboom & Wellner 2001)


def grenander_constant(f0: float, fprime: float) -> float:
    """Prakasa Rao (1969): n^{1/3}(f_hat(x0) - f(x0)) => |f(x0) f'(x0) / 2|^{1/3} 2 Z, Z Chernoff's distribution.
    Returns the multiplier of Z."""
    return 2 * abs(f0 * fprime / 2) ** (1 / 3)


# ----------------------------------------------------------------------------------------------- KS bands


def ks_band_quantiles(n: int, level: float = 0.95) -> dict:
    """Half-widths (on the D_n scale) of KS confidence bands: Kolmogorov's asymptotic, the exact finite-n, and DKW."""
    return {
        "kolmogorov": kolmogorov_quantile(level) / math.sqrt(n),
        "exact": float(stats.kstwo.ppf(level, n)),
        "dkw": math.sqrt(math.log(2 / (1 - level)) / (2 * n)),
    }


def bootstrap_ks_quantile(x, rng: np.random.Generator, B: int = 999, level: float = 0.95) -> float:
    """The level quantile of sup |F*_n - F_n| over nonparametric resamples."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    idx = np.sort(rng.integers(0, n, size=(B, n)), axis=1)
    # F*_n and F_n are step functions on the data; compare them at the data points (right limits and left limits)
    fn = np.arange(1, n + 1) / n
    cnt = np.zeros((B, n))
    for b in range(B):
        cnt[b] = np.searchsorted(idx[b], np.arange(n), side="right") / n
    d = np.max(np.abs(cnt - fn[None, :]), axis=1)
    return float(np.quantile(d, level))


def multiplier_ks_quantile(x, rng: np.random.Generator, B: int = 999, level: float = 0.95) -> float:
    """The multiplier bootstrap: sup_t |(1/n) sum xi_i (1{X_i <= t} - F_n(t))| with xi_i ~ N(0, 1)."""
    n = len(x)
    xi = rng.standard_normal((B, n))
    # with sorted data, the process at the k-th order statistic is (1/n)(sum_{i<=k} xi_i - (k/n) sum xi)
    s = np.cumsum(xi, axis=1)
    k = np.arange(1, n + 1) / n
    proc = (s - k[None, :] * s[:, -1:]) / n
    return float(np.quantile(np.max(np.abs(proc), axis=1), level))
