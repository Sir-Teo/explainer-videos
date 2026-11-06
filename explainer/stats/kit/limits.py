"""statkit.limits -- the weak-convergence lab (Part 43 of *Statistics, Built*, "Measure-Theoretic Probability").

* **Distances between laws on the line:** Kolmogorov (exact for a lattice law against a continuous one), Lévy, the
  Wasserstein-1 distance (the area between the CDFs), and the Lévy-Prokhorov distance bracketed from both sides:
  below by Lévy's (L <= pi on R) and above by the Ky Fan distance of the quantile coupling (Strassen: pi is the
  smallest Ky Fan distance over all couplings).
* **Exact laws of standardized sums:** Bernoulli (binomial), exponential (gamma) and Poisson sums, so convergence
  rates can be measured without simulation error; and the binary-digit and quantile constructions that build every
  random variable on ([0, 1], Lebesgue).
* **Bounds:** Berry-Esseen with Shevtsova's (2011) constant 0.4748; the Wasserstein bound E|X|^3 / sqrt(n) that Stein's
  method gives by the zero-bias coupling (Goldstein 2010; Chen, Goldstein & Shao 2011, Thm 4.1).
* **Characteristic functions:** empirical, numerical inversion, and Lévy's tail bound used in the continuity
  theorem's proof.
* **Stable laws:** Chambers, Mallows & Stuck's (1976) sampler; **large deviations:** Cramér's rate as a Legendre
  transform, with the Bernoulli rate (a Kullback-Leibler divergence) in closed form; **extremes:** GEV laws, the
  classical norming constants, and the exact distance of a normalized maximum from its limit.
* **Series and the strong law:** the random harmonic series, Kolmogorov's three series, the Cantor function.

Tested in ``tests/test_stats_kit_limits.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special, stats

SHEVTSOVA = 0.4748  # the best known Berry-Esseen constant for i.i.d. sums (Shevtsova 2011)


# ---------------------------------------------------------------------------------------------------------------
# Distances between laws on the line
# ---------------------------------------------------------------------------------------------------------------
def kolmogorov(F, G, x) -> float:
    """sup_x |F(x) - G(x)| over a grid (F, G callables or arrays on ``x``)."""
    x = np.asarray(x, float)
    a = F(x) if callable(F) else np.asarray(F, float)
    b = G(x) if callable(G) else np.asarray(G, float)
    return float(np.max(np.abs(a - b)))


def kolmogorov_lattice(atoms, probs, G) -> dict:
    """The exact Kolmogorov distance between a discrete law (``atoms`` sorted, ``probs``) and a continuous CDF G: the
    supremum is attained at an atom, from one side or the other.  Returns the distance and where it is attained."""
    a = np.asarray(atoms, float)
    p = np.asarray(probs, float)
    right = np.cumsum(p)
    left = right - p
    g = G(a)
    d1, d2 = np.abs(right - g), np.abs(left - g)
    i1, i2 = int(np.argmax(d1)), int(np.argmax(d2))
    if d1[i1] >= d2[i2]:
        return {"d": float(d1[i1]), "x": float(a[i1]), "side": "right", "F": float(right[i1]), "G": float(g[i1])}
    return {"d": float(d2[i2]), "x": float(a[i2]), "side": "left", "F": float(left[i2]), "G": float(g[i2])}


def levy(F, G, x, tol: float = 1e-7) -> float:
    """Lévy's metric: inf{eps > 0 : F(x - eps) - eps <= G(x) <= F(x + eps) + eps for all x}, by bisection on a grid.
    It metrizes weak convergence on R and is the side of the largest square that fits between the two graphs."""
    x = np.asarray(x, float)
    g = G(x)

    def ok(e):
        return bool(np.all(F(x - e) - e <= g + 1e-12) and np.all(g <= F(x + e) + e + 1e-12))

    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return float(hi)


def wasserstein1(F, G, x) -> float:
    """The Wasserstein-1 (Kantorovich) distance on R: the area between the CDFs."""
    x = np.asarray(x, float)
    a = F(x) if callable(F) else np.asarray(F, float)
    b = G(x) if callable(G) else np.asarray(G, float)
    return float(np.trapezoid(np.abs(a - b), x))


def ky_fan(d) -> float:
    """The Ky Fan distance inf{eps : P(|X - Y| > eps) <= eps} of a coupling, from equally weighted samples (or
    quantile-grid values) of |X - Y|."""
    d = np.sort(np.abs(np.asarray(d, float)))[::-1]
    m = len(d)
    # with eps = d_(k+1) (the (k+1)-th largest), P(|X - Y| > eps) <= k/m; the answer is min_k max(d_(k+1), k/m)
    cand = [max(d[0], 0.0)] if m else [0.0]
    for k in range(1, m + 1):
        nxt = d[k] if k < m else 0.0
        cand.append(max(nxt, k / m))
    return float(min(cand))


def prokhorov_bracket(F, G, Finv, Ginv, x, m: int = 20_000) -> dict:
    """Lower and upper bounds on the Lévy-Prokhorov distance pi(F, G) on R: Lévy's metric <= pi <= the Ky Fan distance
    of the quantile coupling (F^-1(U), G^-1(U)) (Strassen's theorem)."""
    u = (np.arange(m) + 0.5) / m
    return {"levy": levy(F, G, x), "ky_fan": ky_fan(Finv(u) - Ginv(u))}


# ---------------------------------------------------------------------------------------------------------------
# Exact laws of standardized sums
# ---------------------------------------------------------------------------------------------------------------
def bernoulli_sum_atoms(n: int, p: float = 0.5) -> dict:
    """The standardized binomial: atoms (k - np)/sqrt(np(1 - p)), k = 0..n, with their probabilities."""
    k = np.arange(n + 1)
    s = math.sqrt(n * p * (1 - p))
    return {"atoms": (k - n * p) / s, "probs": stats.binom.pmf(k, n, p)}


def poisson_sum_atoms(n: int, lam: float = 1.0, kmax: int | None = None) -> dict:
    """A sum of n Poisson(lam) is Poisson(n lam): its standardized atoms and probabilities."""
    mu = n * lam
    kmax = kmax or int(mu + 12 * math.sqrt(mu) + 20)
    k = np.arange(kmax + 1)
    return {"atoms": (k - mu) / math.sqrt(mu), "probs": stats.poisson.pmf(k, mu)}


def exponential_sum_cdf(n: int):
    """The CDF of (S_n - n)/sqrt(n) for a sum of n standard exponentials (a gamma(n) law)."""
    return lambda z: stats.gamma.cdf(n + np.sqrt(n) * np.asarray(z, float), n)


def exponential_sum_ppf(n: int):
    return lambda u: (stats.gamma.ppf(np.asarray(u, float), n) - n) / math.sqrt(n)


def lattice_cdf(atoms, probs):
    """A right-continuous step CDF from atoms and probabilities, as a callable."""
    a = np.asarray(atoms, float)
    c = np.cumsum(np.asarray(probs, float))

    def F(x):
        i = np.searchsorted(a, np.asarray(x, float), side="right")
        return np.where(i > 0, c[np.maximum(i - 1, 0)], 0.0)

    return F


def lattice_ppf(atoms, probs):
    a = np.asarray(atoms, float)
    c = np.cumsum(np.asarray(probs, float))

    def Q(u):
        i = np.searchsorted(c, np.asarray(u, float), side="left")
        return a[np.minimum(i, len(a) - 1)]

    return Q


def binary_digits(u, k: int) -> np.ndarray:
    """The first k binary digits of u in [0, 1): Borel's (1909) observation that they are independent fair coins
    under Lebesgue measure."""
    u = np.atleast_1d(np.asarray(u, float))
    out = np.zeros((len(u), k), int)
    v = u.copy()
    for j in range(k):
        v = 2 * v
        out[:, j] = (v >= 1).astype(int)
        v = v - out[:, j]
    return out


def cantor_function(x, depth: int = 40) -> np.ndarray:
    """The Cantor (devil's staircase) function: continuous, constant off the Cantor set, rising from 0 to 1 while its
    derivative is zero almost everywhere -- the CDF of a singular law."""
    x = np.clip(np.asarray(x, float), 0.0, 1.0)
    out = np.zeros_like(x)
    v = x.copy()
    done = np.zeros(x.shape, bool)
    for j in range(1, depth + 1):
        v = 3 * v
        d = np.floor(v)
        d = np.minimum(d, 2)
        hit = (d == 1) & ~done
        out = np.where(hit, out + 0.5 ** j, out)
        done |= hit
        out = np.where(~done & (d == 2), out + 0.5 ** j, out)
        v = v - d
    out = np.where(x >= 1.0, 1.0, out)
    return out


# ---------------------------------------------------------------------------------------------------------------
# Bounds
# ---------------------------------------------------------------------------------------------------------------
def third_abs_moment(kind: str, p: float = 0.5) -> float:
    """E|X - mu|^3 / sigma^3 for the summands used in the lab."""
    if kind == "bernoulli":
        q = 1 - p
        return float((p * q ** 3 + q * p ** 3) / (p * q) ** 1.5)
    if kind == "exponential":
        # E|X - 1|^3 for X ~ Exp(1): 12/e - 2
        return float(12 / math.e - 2)
    if kind == "uniform":
        # (X - 1/2) on [-1/2, 1/2]: E|.|^3 = 1/32, sigma^3 = (1/12)^1.5
        return float((1 / 32) / (1 / 12) ** 1.5)
    if kind == "poisson":
        x = np.arange(0, 60)
        return float(np.sum(stats.poisson.pmf(x, 1.0) * np.abs(x - 1.0) ** 3))
    raise ValueError(kind)


def berry_esseen(rho: float, n: int, C: float = SHEVTSOVA) -> float:
    """sup_z |P(S_n* <= z) - Phi(z)| <= C rho / sqrt(n), rho = E|X - mu|^3 / sigma^3."""
    return float(C * rho / math.sqrt(n))


def stein_wasserstein(rho: float, n: int) -> float:
    """d_W(S_n*, Z) <= rho / sqrt(n): Stein's method with the zero-bias coupling."""
    return float(rho / math.sqrt(n))


def stein_residual(f, fprime, x) -> float:
    """E[f'(X) - X f(X)] estimated from a sample: zero for every smooth bounded f exactly when X ~ N(0, 1)."""
    x = np.asarray(x, float)
    return float(np.mean(fprime(x) - x * f(x)))


def stein_solution(h, z, grid=None) -> np.ndarray:
    """The bounded solution of Stein's equation f'(w) - w f(w) = h(w) - E h(Z):
    f(w) = e^{w^2/2} int_{-inf}^w (h(x) - E h(Z)) e^{-x^2/2} dx, evaluated by quadrature on ``grid``."""
    grid = np.linspace(-8, 8, 16001) if grid is None else np.asarray(grid, float)
    phi = stats.norm.pdf(grid)
    Eh = float(np.trapezoid(h(grid) * phi, grid))
    integrand = (h(grid) - Eh) * phi
    cum = np.concatenate([[0.0], np.cumsum((integrand[1:] + integrand[:-1]) / 2 * np.diff(grid))])
    f = cum / np.maximum(phi, 1e-300)
    return np.interp(np.asarray(z, float), grid, f)


# ---------------------------------------------------------------------------------------------------------------
# Characteristic functions
# ---------------------------------------------------------------------------------------------------------------
def cf_empirical(x, t) -> np.ndarray:
    x, t = np.asarray(x, float), np.asarray(t, float)
    return np.mean(np.exp(1j * t[:, None] * x[None, :]), axis=1)


def cf_invert_density(phi, x, T: float = 40.0, m: int = 8001) -> np.ndarray:
    """f(x) = (1/2 pi) int e^{-itx} phi(t) dt, truncated to |t| <= T (for integrable phi)."""
    t = np.linspace(-T, T, m)
    ph = phi(t)
    x = np.asarray(x, float)
    return np.real(np.trapezoid(np.exp(-1j * t[None, :] * x[:, None]) * ph[None, :], t, axis=1)) / (2 * math.pi)


def levy_tail_bound(phi, u: float, m: int = 4001) -> float:
    """(1/u) int_{-u}^{u} (1 - Re phi(t)) dt, which bounds P(|X| > 2/u) from above: the step in Lévy's continuity
    theorem that turns phi_n -> phi (continuous at 0) into tightness."""
    t = np.linspace(-u, u, m)
    return float(np.trapezoid(1 - np.real(phi(t)), t) / u)


# ---------------------------------------------------------------------------------------------------------------
# Stable laws
# ---------------------------------------------------------------------------------------------------------------
def stable_sample(alpha: float, beta: float, size, rng: np.random.Generator) -> np.ndarray:
    """Chambers, Mallows & Stuck (1976): a standard alpha-stable draw with characteristic function
    exp(-|t|^alpha (1 - i beta sign(t) tan(pi alpha / 2))) for alpha != 1 (and the Cauchy-type formula for alpha = 1)."""
    V = rng.uniform(-math.pi / 2, math.pi / 2, size)
    W = rng.exponential(1.0, size)
    if abs(alpha - 1) < 1e-12:
        return (2 / math.pi) * ((math.pi / 2 + beta * V) * np.tan(V)
                                - beta * np.log((math.pi / 2) * W * np.cos(V) / (math.pi / 2 + beta * V)))
    B = math.atan(beta * math.tan(math.pi * alpha / 2)) / alpha
    S = (1 + beta ** 2 * math.tan(math.pi * alpha / 2) ** 2) ** (1 / (2 * alpha))
    return S * np.sin(alpha * (V + B)) / np.cos(V) ** (1 / alpha) * (np.cos(V - alpha * (V + B)) / W) ** ((1 - alpha) / alpha)


def stable_cf(t, alpha: float) -> np.ndarray:
    """The symmetric alpha-stable characteristic function exp(-|t|^alpha)."""
    return np.exp(-np.abs(np.asarray(t, float)) ** alpha)


# ---------------------------------------------------------------------------------------------------------------
# Large deviations
# ---------------------------------------------------------------------------------------------------------------
def cramer_rate(logmgf, a: float, t_max: float = 50.0) -> float:
    """Cramér's rate I(a) = sup_t (t a - Lambda(t)), the Legendre transform of the log-MGF, by bounded maximization."""
    res = optimize.minimize_scalar(lambda t: -(t * a - logmgf(t)), bounds=(-t_max, t_max), method="bounded",
                                   options={"xatol": 1e-12})
    return float(-res.fun)


def bernoulli_rate(a: float, p: float) -> float:
    """I(a) = a log(a/p) + (1 - a) log((1 - a)/(1 - p)): the Kullback-Leibler divergence KL(a || p)."""
    if a <= 0:
        return -math.log(1 - p)
    if a >= 1:
        return -math.log(p)
    return float(a * math.log(a / p) + (1 - a) * math.log((1 - a) / (1 - p)))


def binomial_upper_tail(n: int, p: float, a: float) -> float:
    """P(S_n / n >= a), exactly."""
    return float(stats.binom.sf(math.ceil(n * a - 1e-9) - 1, n, p))


# ---------------------------------------------------------------------------------------------------------------
# Extremes
# ---------------------------------------------------------------------------------------------------------------
def gev_cdf(x, xi: float) -> np.ndarray:
    """G_xi(x) = exp(-(1 + xi x)^(-1/xi)) on 1 + xi x > 0 (Gumbel exp(-e^{-x}) at xi = 0)."""
    x = np.asarray(x, float)
    if abs(xi) < 1e-12:
        return np.exp(-np.exp(-x))
    z = 1 + xi * x
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.exp(-np.power(np.maximum(z, 1e-300), -1 / xi))
    return np.where(z > 0, out, 0.0 if xi > 0 else 1.0)


def max_norming(kind: str, n: int, alpha: float = 2.0) -> tuple:
    """(a_n, b_n) with (M_n - b_n)/a_n converging: exponential -> Gumbel (1, log n); Pareto(alpha) -> Fréchet
    (n^{1/alpha}, 0); uniform -> reversed Weibull (1/n, 1); normal -> Gumbel with the classical constants."""
    if kind == "exponential":
        return 1.0, math.log(n)
    if kind == "pareto":
        return n ** (1 / alpha), 0.0
    if kind == "uniform":
        return 1.0 / n, 1.0
    if kind == "normal":
        r = math.sqrt(2 * math.log(n))
        return 1 / r, r - (math.log(math.log(n)) + math.log(4 * math.pi)) / (2 * r)
    raise ValueError(kind)


def max_cdf(kind: str, n: int, x, alpha: float = 2.0) -> np.ndarray:
    """P((M_n - b_n)/a_n <= x) = F(a_n x + b_n)^n, exactly."""
    a, b = max_norming(kind, n, alpha)
    y = a * np.asarray(x, float) + b
    if kind == "exponential":
        F = np.where(y > 0, -np.expm1(-np.maximum(y, 0)), 0.0)
    elif kind == "pareto":
        F = np.where(y >= 1, 1 - np.maximum(y, 1) ** -alpha, 0.0)
    elif kind == "uniform":
        F = np.clip(y, 0, 1)
    else:
        F = stats.norm.cdf(y)
    with np.errstate(divide="ignore"):
        return np.exp(n * np.log(np.maximum(F, 1e-300))) * (F > 0)


def max_limit(kind: str, x, alpha: float = 2.0) -> np.ndarray:
    x = np.asarray(x, float)
    if kind in ("exponential", "normal"):
        return gev_cdf(x, 0.0)
    if kind == "pareto":
        return np.where(x > 0, np.exp(-np.maximum(x, 1e-300) ** -alpha), 0.0)
    if kind == "uniform":
        return np.where(x < 0, np.exp(-np.abs(x)), 1.0)
    raise ValueError(kind)


# ---------------------------------------------------------------------------------------------------------------
# Series and the strong law
# ---------------------------------------------------------------------------------------------------------------
def random_series(p: float, n: int, reps: int, rng: np.random.Generator) -> np.ndarray:
    """Partial sums of sum_k eps_k / k^p with independent random signs: by Kolmogorov's three-series (here two-series)
    theorem the series converges almost surely iff sum 1/k^{2p} < infinity, i.e. p > 1/2."""
    k = np.arange(1, n + 1)
    signs = rng.choice([-1.0, 1.0], size=(reps, n))
    return np.cumsum(signs / k ** p, axis=1)


def three_series_terms(p: float, n: int, c: float = 1.0) -> dict:
    """The three series for X_k = eps_k / k^p truncated at c: sum P(|X_k| > c), sum E[X_k 1(|X_k| <= c)],
    sum Var(X_k 1(|X_k| <= c)), each up to n."""
    k = np.arange(1, n + 1).astype(float)
    size = 1 / k ** p
    inside = size <= c
    return {"tail": float(np.sum(~inside)), "mean": 0.0, "var": float(np.sum(np.where(inside, size ** 2, 0.0)))}


def zeta_partial(s: float, n: int) -> float:
    return float(special.zeta(s) - special.zeta(s, n + 1)) if s > 1 else float(np.sum(1 / np.arange(1, n + 1) ** s))


# ---------------------------------------------------------------------------------------------------------------
# The Poisson limit and heavy tails
# ---------------------------------------------------------------------------------------------------------------
def tv_binomial_poisson(n: int, p: float) -> float:
    """The total variation distance between Binomial(n, p) and Poisson(np), exactly."""
    kmax = max(n, int(n * p + 20 * math.sqrt(n * p + 1) + 20))
    k = np.arange(kmax + 1)
    b = np.where(k <= n, stats.binom.pmf(np.minimum(k, n), n, p), 0.0)
    q = stats.poisson.pmf(k, n * p)
    return float(0.5 * (np.sum(np.abs(b - q)) + stats.poisson.sf(kmax, n * p)))


def le_cam_bound(ps) -> float:
    """Le Cam (1960): the total variation distance between a sum of independent Bernoulli(p_i) and Poisson(sum p_i)
    is at most sum p_i^2."""
    ps = np.asarray(ps, float)
    return float(np.sum(ps ** 2))


def hill(x, k: int) -> float:
    """Hill's (1975) estimator of the tail index alpha from the k largest |x|: 1 / mean(log(X_(i) / X_(k+1)))."""
    a = np.sort(np.abs(np.asarray(x, float)))[::-1]
    return float(1.0 / np.mean(np.log(a[:k] / a[k])))
