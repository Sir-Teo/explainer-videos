"""statkit.testing -- the Neyman-structure lab (Part 46 of *Statistics, Built*, "The Theory of Testing and
Confidence").

* **Behrens-Fisher:** Welch-Satterthwaite degrees of freedom; Behrens and Fisher's fiducial critical values by
  quadrature; sizes of the pooled t, Welch and Behrens-Fisher tests by simulation.
* **Neyman-Pearson:** randomized UMP one-sided binomial tests; the UMPU two-sided binomial test (two side conditions,
  solved exactly); the equal-tailed test's bias; the generalized Neyman-Pearson lemma as a linear programme.
* **Neyman structure:** the conditional (Fisher) test for two binomials given the total, randomized to be similar, and
  its unconditional size at every value of the nuisance parameter.
* **Likelihood ratios on a boundary:** Chernoff's chi-bar-squared mixture.
* **Confidence sets:** Clopper-Pearson by inverting tests, with exact coverage functions; Fieller's sets for a ratio
  (bounded, the complement of an interval, or the whole line); Feldman & Cousins's unified intervals for a Poisson
  mean with known background, against flip-flopping.
* **Simultaneous inference:** closed testing with Bonferroni (Holm) or Simes local tests; Scheffe's constant.
* **Conditional inference:** Buehler-style recognizable subsets for the n = 2 t interval.
* **Evidence:** Berger & Sellke's bounds on P(H0 | x) over classes of priors; the -e p log p calibration.
* **Goodness of fit:** Kolmogorov-Smirnov with estimated parameters (Lilliefors).

Tested in ``tests/test_stats_kit_testing.py``.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import integrate, optimize, special, stats


# ---------------------------------------------------------------------------------------------------------------
# Behrens-Fisher
# ---------------------------------------------------------------------------------------------------------------
def welch_df(v1, v2, n1, n2):
    """Welch-Satterthwaite degrees of freedom from the two variances of the means v_i = s_i^2 / n_i."""
    v1, v2 = np.asarray(v1, float), np.asarray(v2, float)
    return (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))


def bf_critical(phi, n1: int, n2: int, alpha: float = 0.05) -> float:
    """The Behrens-Fisher fiducial critical value: c with P(|T1 sin(phi) - T2 cos(phi)| > c) = alpha, T_i ~ t_{n_i - 1}
    independent, tan(phi) = (s1/sqrt n1) / (s2/sqrt n2)."""
    sp, cp = math.sin(phi), math.cos(phi)
    t1, t2 = stats.t(n1 - 1), stats.t(n2 - 1)

    def tail(c):
        f = lambda u: t2.pdf(u) * (t1.sf((c + u * cp) / sp) + t1.cdf((-c + u * cp) / sp)) if sp > 1e-12 else 0.0  # noqa: E731
        if sp <= 1e-12:
            return 2 * t2.sf(c)
        if cp <= 1e-12:
            return 2 * t1.sf(c)
        return integrate.quad(f, -np.inf, np.inf, limit=200)[0]

    return optimize.brentq(lambda c: tail(c) - alpha, 0.5, 60)


def two_sample_sizes(n1: int, s1: float, n2: int, s2: float, reps: int, rng, alpha: float = 0.05, grid: int = 41) -> dict:
    """Rejection rates under H0 (equal means) of the pooled t test, Welch's test and the Behrens-Fisher test, with
    unequal variances.  The Behrens-Fisher critical values are interpolated over a grid of phi."""
    x = rng.normal(0, s1, (reps, n1))
    y = rng.normal(0, s2, (reps, n2))
    m1, m2 = x.mean(1), y.mean(1)
    v1, v2 = x.var(1, ddof=1), y.var(1, ddof=1)
    sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)
    t_pool = (m1 - m2) / np.sqrt(sp2 * (1 / n1 + 1 / n2))
    se = np.sqrt(v1 / n1 + v2 / n2)
    d = (m1 - m2) / se
    df = welch_df(v1 / n1, v2 / n2, n1, n2)
    rej_pool = np.abs(t_pool) > stats.t.ppf(1 - alpha / 2, n1 + n2 - 2)
    rej_welch = np.abs(d) > stats.t.ppf(1 - alpha / 2, df)
    phis = np.linspace(0, math.pi / 2, grid)
    cs = np.array([bf_critical(p, n1, n2, alpha) for p in phis])
    phi = np.arctan2(np.sqrt(v1 / n1), np.sqrt(v2 / n2))
    rej_bf = np.abs(d) > np.interp(phi, phis, cs)
    return {"pooled": rej_pool, "welch": rej_welch, "bf": rej_bf, "df": df, "phis": phis, "cs": cs}


# ---------------------------------------------------------------------------------------------------------------
# Neyman-Pearson for the binomial
# ---------------------------------------------------------------------------------------------------------------
def ump_binomial(n: int, p0: float, alpha: float = 0.05) -> dict:
    """The randomized UMP test of p <= p0 against p > p0: reject when X > c, with probability gamma when X = c."""
    x = np.arange(n + 1)
    pmf = stats.binom.pmf(x, n, p0)
    sf = np.cumsum(pmf[::-1])[::-1]  # P(X >= x)
    # the smallest c with P(X > c) <= alpha, so that P(X > c) <= alpha < P(X >= c)
    c = int(np.min(x[(sf - pmf) <= alpha + 1e-15]))
    gamma = (alpha - (sf[c] - pmf[c])) / pmf[c]
    phi = np.where(x > c, 1.0, 0.0)
    phi[c] = gamma
    return {"c": c, "gamma": float(gamma), "phi": phi}


def power(phi, n: int, p) -> np.ndarray:
    """E_p phi(X) for X ~ Bin(n, p), for a vector of p."""
    p = np.atleast_1d(np.asarray(p, float))
    x = np.arange(n + 1)
    return stats.binom.pmf(x[None, :], n, p[:, None]) @ np.asarray(phi, float)


def umpu_binomial(n: int, p0: float, alpha: float = 0.05) -> dict:
    """The UMPU test of p = p0 against p != p0: phi = 1 outside [c1, c2], gamma_i at c_i, with
    E phi = alpha and E[X phi] = alpha n p0 (the derivative of the power vanishes at p0)."""
    x = np.arange(n + 1)
    f = stats.binom.pmf(x, n, p0)
    best = None
    for c1 in range(0, n + 1):
        for c2 in range(c1, n + 1):
            out = (x < c1) | (x > c2)
            a0, a1 = f[out].sum(), (x * f)[out].sum()
            if c1 == c2:
                # one randomized point: need g with a0 + g f = alpha and a1 + g c f = alpha n p0
                g = (alpha - a0) / f[c1]
                if 0 <= g <= 1 and abs(a1 + g * c1 * f[c1] - alpha * n * p0) < 1e-10:
                    best = (c1, c2, g, g)
                continue
            A = np.array([[f[c1], f[c2]], [c1 * f[c1], c2 * f[c2]]])
            b = np.array([alpha - a0, alpha * n * p0 - a1])
            g = np.linalg.solve(A, b)
            if np.all(g >= -1e-12) and np.all(g <= 1 + 1e-12):
                best = (c1, c2, float(np.clip(g[0], 0, 1)), float(np.clip(g[1], 0, 1)))
                break
        if best is not None:
            break
    c1, c2, g1, g2 = best
    phi = np.where((x < c1) | (x > c2), 1.0, 0.0)
    phi[c1], phi[c2] = g1, g2
    return {"c1": c1, "c2": c2, "g1": g1, "g2": g2, "phi": phi}


def equal_tailed_binomial(n: int, p0: float, alpha: float = 0.05) -> np.ndarray:
    """The randomized test with alpha/2 in each tail (each side a UMP one-sided test at level alpha/2)."""
    up = ump_binomial(n, p0, alpha / 2)["phi"]
    lo = ump_binomial(n, 1 - p0, alpha / 2)["phi"][::-1]
    return np.minimum(1.0, up + lo)


def generalized_np(f0, f1, constraints, alpha_vec) -> np.ndarray:
    """The generalized Neyman-Pearson lemma as a linear programme: maximize sum phi f1 subject to
    sum phi g_k = a_k for each constraint row g_k, 0 <= phi <= 1 (Dantzig & Wald 1951)."""
    f1 = np.asarray(f1, float)
    A = np.asarray(constraints, float)
    r = optimize.linprog(-f1, A_eq=A, b_eq=np.asarray(alpha_vec, float), bounds=[(0, 1)] * len(f1), method="highs")
    return r.x


# ---------------------------------------------------------------------------------------------------------------
# Neyman structure: two binomials
# ---------------------------------------------------------------------------------------------------------------
def conditional_test(m: int, n: int, alpha: float = 0.05, randomized: bool = True) -> dict:
    """X ~ Bin(m, p1), Y ~ Bin(n, p2); test p1 <= p2 against p1 > p2.  Given T = X + Y = t, X is hypergeometric under
    H0 whatever the common p, so a level-alpha test of each slice is similar: Neyman structure.  Returns phi[x, t]."""
    phi = np.zeros((m + 1, m + n + 1))
    for t in range(m + n + 1):
        lo, hi = max(0, t - n), min(m, t)
        xs = np.arange(lo, hi + 1)
        pmf = stats.hypergeom.pmf(xs, m + n, m, t)
        tail = 0.0
        for xv, pv in zip(xs[::-1], pmf[::-1]):
            if tail + pv <= alpha + 1e-12:
                phi[xv, t] = 1.0
                tail += pv
            else:
                if randomized:
                    phi[xv, t] = (alpha - tail) / pv
                break
    return {"phi": phi}


def unconditional_size(phi, m: int, n: int, p) -> np.ndarray:
    """P(reject) when p1 = p2 = p, for each p: the size as a function of the nuisance parameter."""
    p = np.atleast_1d(np.asarray(p, float))
    out = []
    for q in p:
        px = stats.binom.pmf(np.arange(m + 1), m, q)
        py = stats.binom.pmf(np.arange(n + 1), n, q)
        tot = 0.0
        for xv in range(m + 1):
            tot += px[xv] * np.sum(py * phi[xv, xv + np.arange(n + 1)])
        out.append(tot)
    return np.array(out)


# ---------------------------------------------------------------------------------------------------------------
# Likelihood ratios on a boundary
# ---------------------------------------------------------------------------------------------------------------
def chibar_critical(alpha: float = 0.05) -> float:
    """Chernoff (1954): testing mu = 0 against mu >= 0 from Z ~ N(mu, 1), the LRT max(0, Z)^2 is
    0.5 chi^2_0 + 0.5 chi^2_1 under H0; its critical value is the chi^2_1 quantile at 1 - 2 alpha."""
    return float(stats.chi2.ppf(1 - 2 * alpha, 1))


# ---------------------------------------------------------------------------------------------------------------
# Confidence sets
# ---------------------------------------------------------------------------------------------------------------
def clopper_pearson(x: int, n: int, level: float = 0.95) -> tuple:
    a = 1 - level
    lo = 0.0 if x == 0 else stats.beta.ppf(a / 2, x, n - x + 1)
    hi = 1.0 if x == n else stats.beta.ppf(1 - a / 2, x + 1, n - x)
    return float(lo), float(hi)


def coverage_binomial(intervals, n: int, p) -> np.ndarray:
    """Exact coverage at each p of intervals[x] = (lo, hi), x = 0..n."""
    p = np.atleast_1d(np.asarray(p, float))
    lo = np.array([iv[0] for iv in intervals])
    hi = np.array([iv[1] for iv in intervals])
    pmf = stats.binom.pmf(np.arange(n + 1)[None, :], n, p[:, None])
    cov = (lo[None, :] <= p[:, None]) & (p[:, None] <= hi[None, :])
    return np.sum(pmf * cov, axis=1)


def wald_binomial(x: int, n: int, level: float = 0.95) -> tuple:
    z = stats.norm.ppf(0.5 + level / 2)
    ph = x / n
    h = z * math.sqrt(ph * (1 - ph) / n)
    return ph - h, ph + h


def fieller(a: float, b: float, va: float, vb: float, cab: float = 0.0, level: float = 0.95) -> dict:
    """Fieller's set for rho = alpha / beta from estimates a ~ N(alpha, va), b ~ N(beta, vb): {rho : (a - rho b)^2 <=
    z^2 (va - 2 rho cab + rho^2 vb)}, a quadratic inequality.  Kind 'bounded', 'exclusive' (two rays) or 'all'."""
    z2 = stats.norm.ppf(0.5 + level / 2) ** 2
    A = b ** 2 - z2 * vb
    B = -2 * (a * b - z2 * cab)
    C = a ** 2 - z2 * va
    disc = B * B - 4 * A * C
    if A > 0:
        r = math.sqrt(disc)
        return {"kind": "bounded", "lo": (-B - r) / (2 * A), "hi": (-B + r) / (2 * A)}
    if disc < 0:
        return {"kind": "all"}
    r = math.sqrt(disc)
    lo, hi = sorted(((-B - r) / (2 * A), (-B + r) / (2 * A)))
    return {"kind": "exclusive", "lo": lo, "hi": hi}


def fc_intervals(b: float, level: float = 0.9, mu_grid=None, nmax: int = 60) -> dict:
    """Feldman & Cousins (1998): n ~ Poisson(mu + b), b known, mu >= 0.  For each mu, accept the n with the largest
    ratio R = P(n | mu) / P(n | mu_best), mu_best = max(0, n - b), until the acceptance probability reaches `level`;
    the interval for an observed n is the set of mu whose acceptance region contains it."""
    mu_grid = np.linspace(0, 20, 2001) if mu_grid is None else np.asarray(mu_grid, float)
    n = np.arange(nmax + 1)
    best = np.maximum(0, n - b)
    acc = np.zeros((len(mu_grid), nmax + 1), bool)
    for i, mu in enumerate(mu_grid):
        p = stats.poisson.pmf(n, mu + b)
        R = p / stats.poisson.pmf(n, best + b)
        order = np.argsort(-R, kind="stable")
        tot = 0.0
        for k in order:
            acc[i, k] = True
            tot += p[k]
            if tot >= level:
                break
    lo = np.array([mu_grid[acc[:, k]].min() if acc[:, k].any() else np.nan for k in n])
    hi = np.array([mu_grid[acc[:, k]].max() if acc[:, k].any() else np.nan for k in n])
    return {"n": n, "lo": lo, "hi": hi, "mu": mu_grid, "acc": acc}


def poisson_coverage(lo, hi, b: float, mu) -> np.ndarray:
    """Exact coverage at each mu of intervals [lo[n], hi[n]] for n ~ Poisson(mu + b)."""
    mu = np.atleast_1d(np.asarray(mu, float))
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    n = np.arange(len(lo))
    pmf = stats.poisson.pmf(n[None, :], mu[:, None] + b)
    cov = (lo[None, :] <= mu[:, None] + 1e-12) & (mu[:, None] <= hi[None, :] + 1e-12)
    return np.sum(pmf * cov, axis=1)


def flipflop_intervals(b: float, level: float = 0.9, nmax: int = 60, z_switch: float = 3.0) -> dict:
    """Flip-flopping (Feldman & Cousins's section II): quote a one-sided upper limit if n is below b + z_switch sqrt(b),
    a central interval otherwise, each from the classical Neyman construction, and clip mu at 0."""
    n = np.arange(nmax + 1)
    lo, hi = np.zeros(len(n)), np.zeros(len(n))
    a = 1 - level
    for k in n:
        upper = lambda m, q: stats.poisson.cdf(k, m + b) - q  # noqa: E731
        if k < b + z_switch * math.sqrt(b):
            # one-sided upper limit: P(N <= k | mu + b) = a
            f = lambda m: upper(m, a)  # noqa: E731
            hi[k] = optimize.brentq(f, 0, 200) if f(0) > 0 else 0.0
            lo[k] = 0.0
        else:
            f = lambda m: upper(m, a / 2)  # noqa: E731
            hi[k] = optimize.brentq(f, 0, 200) if f(0) > 0 else 0.0
            g = lambda m: stats.poisson.sf(k - 1, m + b) - a / 2  # noqa: E731  P(N >= k) = a/2
            lo[k] = optimize.brentq(g, 0, 200) if g(0) < 0 else 0.0
    return {"n": n, "lo": lo, "hi": hi}


# ---------------------------------------------------------------------------------------------------------------
# Simultaneous inference
# ---------------------------------------------------------------------------------------------------------------
def closed_test(pvals, alpha: float = 0.05, local: str = "bonferroni") -> np.ndarray:
    """Marcus, Peritz & Gabriel (1976): reject H_i when every intersection hypothesis containing i is rejected by a
    level-alpha local test (Bonferroni gives Holm's procedure; Simes gives Hommel's)."""
    p = np.asarray(pvals, float)
    m = len(p)
    rejected_sets = {}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            ps = np.sort(p[list(S)])
            if local == "bonferroni":
                rej = ps[0] <= alpha / len(S)
            elif local == "simes":
                rej = np.any(ps <= alpha * np.arange(1, len(S) + 1) / len(S))
            else:
                raise ValueError(local)
            rejected_sets[S] = rej
    return np.array([all(rejected_sets[S] for S in rejected_sets if i in S) for i in range(m)])


def holm(pvals, alpha: float = 0.05) -> np.ndarray:
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    rej = np.zeros(m, bool)
    for k, i in enumerate(order):
        if p[i] <= alpha / (m - k):
            rej[i] = True
        else:
            break
    return rej


def scheffe_constant(k: int, df: float = np.inf, level: float = 0.95) -> float:
    """Scheffe's multiplier sqrt(k F_{k, df}(level)) (sqrt(chi^2_k) when df is infinite): simultaneous for every
    linear combination in a k-dimensional space."""
    if np.isinf(df):
        return float(math.sqrt(stats.chi2.ppf(level, k)))
    return float(math.sqrt(k * stats.f.ppf(level, k, df)))


# ---------------------------------------------------------------------------------------------------------------
# Conditional inference
# ---------------------------------------------------------------------------------------------------------------
def t2_conditional(mu_over_sigma, k: float, reps: int, rng, level: float = 0.5) -> dict:
    """n = 2 normal observations, the t interval xbar +- t_{1, (1+level)/2} s / sqrt 2.  Its coverage overall and on the
    recognizable set {|xbar| / s <= k} (Buehler 1959; Brown 1967)."""
    x = rng.normal(mu_over_sigma, 1.0, (reps, 2))
    xb = x.mean(1)
    s = np.abs(x[:, 0] - x[:, 1]) / math.sqrt(2)
    h = stats.t.ppf(0.5 + level / 2, 1) * s / math.sqrt(2)
    cov = np.abs(xb - mu_over_sigma) <= h
    sel = np.abs(xb) / s <= k
    return {"overall": float(cov.mean()), "conditional": float(cov[sel].mean()), "share": float(sel.mean())}


# ---------------------------------------------------------------------------------------------------------------
# p-values and evidence
# ---------------------------------------------------------------------------------------------------------------
def berger_sellke(p: float, prior_h0: float = 0.5) -> dict:
    """Lower bounds on P(H0 | x) for the two-sided normal test of theta = 0 with p-value p: over all priors g on
    theta != 0 (B = exp(-z^2/2)), over symmetric unimodal g (uniform priors), and over N(0, tau^2) priors; and the
    Sellke-Bayarri-Berger calibration B >= -e p log p."""
    z = stats.norm.isf(p / 2)

    def post(B):
        return 1 / (1 + (1 - prior_h0) / prior_h0 / B)

    B_all = math.exp(-z * z / 2)

    def B_unif(K):
        m = (stats.norm.cdf(z + K) - stats.norm.cdf(z - K)) / (2 * K)
        return stats.norm.pdf(z) / m

    B_su = optimize.minimize_scalar(B_unif, bounds=(1e-6, 50), method="bounded").fun

    def B_norm(t2):
        return math.sqrt(1 + t2) * math.exp(-z * z / 2 * t2 / (1 + t2))

    B_n = optimize.minimize_scalar(B_norm, bounds=(1e-9, 1e4), method="bounded").fun
    calib = -math.e * p * math.log(p) if p < 1 / math.e else 1.0
    return {"z": z, "all": post(B_all), "symmetric": post(B_su), "normal": post(B_n), "calibration": post(calib),
            "B_all": B_all, "B_sym": B_su, "B_norm": B_n, "B_calib": calib}


# ---------------------------------------------------------------------------------------------------------------
# Goodness of fit
# ---------------------------------------------------------------------------------------------------------------
def ks_estimated(n: int, reps: int, rng, alpha: float = 0.05) -> dict:
    """KS statistics for normality with the mean and SD estimated from the data, against the KS critical value for a
    fully specified null: the size (Lilliefors 1967), and the simulated correct critical value."""
    x = rng.normal(0, 1, (reps, n))
    z = (x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True)
    z.sort(axis=1)
    F = stats.norm.cdf(z)
    i = np.arange(1, n + 1)
    D = np.maximum(np.max(i / n - F, axis=1), np.max(F - (i - 1) / n, axis=1))
    crit = stats.kstwo.ppf(1 - alpha, n)
    return {"D": D, "crit_naive": float(crit), "size": float(np.mean(D > crit)), "crit_lilliefors": float(np.quantile(D, 1 - alpha))}
