"""statkit.hdp: high-dimensional probability (Part 51 of *Statistics, Built*).

Checked in ``tests/test_stats_kit_hdp.py``:

* the sphere: the exact law of one coordinate of a uniform point on S^{n-1}, the mass of an equatorial band, the
  distribution of the angle between random directions; uniform sampling;
* thin shells: ||g|| for g ~ N(0, I_n); Johnson-Lindenstrauss distortions of random projections;
* sub-Gaussian and sub-exponential norms; Hoeffding, Bernstein and Chernoff bounds against exact binomial tails;
* Gaussian concentration of Lipschitz functions (the maximum, the norm) against simulation;
* random matrices: extreme singular values of Gaussian matrices against sqrt(n) +- sqrt(p); covariance estimation error
  in operator norm; the Marchenko-Pastur law;
* matrix Bernstein for a sum of random rank-one matrices;
* Gaussian comparison: Slepian's lemma for exchangeable Gaussians; Sudakov's minoration;
* statistical dimension of the l1 descent cone (Amelunxen, Lotz, McCoy & Tropp 2014), and basis-pursuit recovery;
* Gaussian widths of simple sets;
* chaining: Brownian motion's grid maximum, Dudley's entropy integral and the single-scale union bound.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize, special, stats

# ------------------------------------------------------------------------------------------------- the sphere


def sphere_coordinate_pdf(x, n: int) -> np.ndarray:
    """The density of x_1 for x uniform on S^{n-1} in R^n: c_n (1 - x^2)^((n-3)/2) on [-1, 1]."""
    x = np.asarray(x, float)
    c = math.exp(special.gammaln(n / 2) - special.gammaln((n - 1) / 2) - 0.5 * math.log(math.pi))
    return np.where(np.abs(x) < 1, c * np.maximum(1 - x ** 2, 0) ** ((n - 3) / 2), 0.0)


def sphere_band_mass(t: float, n: int) -> float:
    """P(|x_1| <= t) for x uniform on S^{n-1}: x_1^2 ~ Beta(1/2, (n-1)/2)."""
    return float(stats.beta.cdf(t ** 2, 0.5, (n - 1) / 2))


def sphere_band_for(mass: float, n: int) -> float:
    """The half-width t of the equatorial band holding ``mass`` of the sphere."""
    return float(math.sqrt(stats.beta.ppf(mass, 0.5, (n - 1) / 2)))


def sample_sphere(n: int, m: int, rng: np.random.Generator) -> np.ndarray:
    g = rng.standard_normal((m, n))
    return g / np.linalg.norm(g, axis=1, keepdims=True)


def angle_pdf(theta, n: int) -> np.ndarray:
    """Density of the angle between two independent uniform directions in R^n: proportional to sin^(n-2)."""
    theta = np.asarray(theta, float)
    logc = special.gammaln(n / 2) - special.gammaln((n - 1) / 2) - 0.5 * math.log(math.pi)
    with np.errstate(divide="ignore"):
        return np.exp(logc + (n - 2) * np.log(np.sin(theta)))


# ------------------------------------------------------------------------------------------------ thin shells


def norm_chi_moments(n: int) -> dict:
    """||g||, g ~ N(0, I_n): a chi with n degrees of freedom.  Mean sqrt(2) G((n+1)/2)/G(n/2), variance n - mean^2."""
    m = math.sqrt(2) * math.exp(special.gammaln((n + 1) / 2) - special.gammaln(n / 2))
    return {"mean": m, "var": n - m ** 2, "sd": math.sqrt(max(n - m ** 2, 0.0))}


def jl_distortion(X: np.ndarray, k: int, rng: np.random.Generator) -> dict:
    """Project the rows of X by a k x d Gaussian matrix / sqrt(k); return the ratios of squared pairwise distances."""
    d = X.shape[1]
    G = rng.standard_normal((d, k)) / math.sqrt(k)
    Y = X @ G
    i, j = np.triu_indices(len(X), 1)
    a = np.sum((X[i] - X[j]) ** 2, axis=1)
    b = np.sum((Y[i] - Y[j]) ** 2, axis=1)
    r = b / a
    return {"ratios": r, "max_dev": float(np.max(np.abs(r - 1)))}


def jl_dimension(N: int, eps: float) -> int:
    """A standard JL dimension: k >= 4 log N / (eps^2/2 - eps^3/3) (Dasgupta & Gupta 2003)."""
    return int(math.ceil(4 * math.log(N) / (eps ** 2 / 2 - eps ** 3 / 3)))


# ------------------------------------------------------------------------------- tails: Hoeffding, Bernstein


def hoeffding_tail(t, n: int, a: float = 0.0, b: float = 1.0) -> np.ndarray:
    """P(mean - E >= t) <= exp(-2 n t^2 / (b - a)^2)."""
    t = np.atleast_1d(np.asarray(t, float))
    return np.minimum(np.exp(-2 * n * t ** 2 / (b - a) ** 2), 1.0)


def bernstein_tail(t, n: int, var: float, b: float = 1.0) -> np.ndarray:
    """P(mean - E >= t) <= exp(-n t^2 / (2 (var + b t / 3))), |X - EX| <= b."""
    t = np.atleast_1d(np.asarray(t, float))
    return np.minimum(np.exp(-n * t ** 2 / (2 * (var + b * t / 3))), 1.0)


def chernoff_binomial(t, n: int, p: float) -> np.ndarray:
    """The Chernoff bound exp(-n KL(p + t || p)) for a Binomial mean."""
    t = np.atleast_1d(np.asarray(t, float))
    q = np.clip(p + t, 1e-12, 1 - 1e-12)
    kl = q * np.log(q / p) + (1 - q) * np.log((1 - q) / (1 - p))
    return np.where(p + t >= 1, 0.0, np.exp(-n * kl))


def binomial_mean_tail(t, n: int, p: float) -> np.ndarray:
    t = np.atleast_1d(np.asarray(t, float))
    k = np.ceil(n * (p + t) - 1e-9)
    return stats.binom.sf(k - 1, n, p)


def psi2_norm_bounded(c: float) -> float:
    """||X||_psi2 for |X| <= c, mean zero, at the worst case (a symmetric +-c sign): c / sqrt(log 2)."""
    return c / math.sqrt(math.log(2))


def psi2_norm_normal(sigma: float = 1.0) -> float:
    """||N(0, s^2)||_psi2 = s sqrt(8/3): the t with E exp(X^2/t^2) = 2."""
    return sigma * math.sqrt(8 / 3)


def psi_norm_empirical(x, which: int = 2) -> float:
    """The empirical Orlicz norm inf{t : mean exp(|x|^which / t^which) <= 2}."""
    x = np.abs(np.asarray(x, float))

    def f(t):
        return float(np.mean(np.exp(np.minimum((x / t) ** which, 700)))) - 2

    lo, hi = 1e-3, 10 * float(np.max(x)) + 1
    return float(optimize.brentq(f, lo, hi))


# ------------------------------------------------------------------------------- Lipschitz concentration


def gaussian_concentration(t) -> np.ndarray:
    """P(f(g) - E f(g) >= t) <= exp(-t^2/2) for 1-Lipschitz f (Tsirelson-Ibragimov-Sudakov)."""
    t = np.atleast_1d(np.asarray(t, float))
    return np.exp(-t ** 2 / 2)


def expected_max_gaussians(n: int) -> float:
    """E max of n iid N(0,1), by quadrature."""
    f = lambda x: x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1)  # noqa: E731
    return float(integrate.quad(f, -10, 12, limit=200)[0])


# ---------------------------------------------------------------------------------------- random matrices


def singular_extremes(n: int, p: int, rng: np.random.Generator, reps: int = 50) -> dict:
    """Largest and smallest singular values of n x p Gaussian matrices."""
    hi, lo = [], []
    for _ in range(reps):
        s = np.linalg.svd(rng.standard_normal((n, p)), compute_uv=False)
        hi.append(s[0])
        lo.append(s[-1])
    return {"max": float(np.mean(hi)), "min": float(np.mean(lo)), "max_sd": float(np.std(hi)), "min_sd": float(np.std(lo)),
            "gordon_max": math.sqrt(n) + math.sqrt(p), "gordon_min": math.sqrt(n) - math.sqrt(p)}


def covariance_error(n: int, p: int, rng: np.random.Generator, reps: int = 50) -> float:
    """E ||S - I||_op for S the sample covariance of n N(0, I_p) vectors (mean known)."""
    out = []
    for _ in range(reps):
        X = rng.standard_normal((n, p))
        S = X.T @ X / n
        out.append(np.max(np.abs(np.linalg.eigvalsh(S - np.eye(p)))))
    return float(np.mean(out))


def covariance_error_limit(n: int, p: int) -> float:
    """The edge of Marchenko-Pastur: ||S - I|| -> max((1 + sqrt(g))^2 - 1, 1 - (1 - sqrt(g))^2), g = p/n."""
    g = p / n
    return max((1 + math.sqrt(g)) ** 2 - 1, 1 - (1 - math.sqrt(min(g, 1))) ** 2)


def marchenko_pastur_pdf(x, gamma: float) -> np.ndarray:
    """The Marchenko-Pastur density for the eigenvalues of S, aspect ratio gamma = p/n <= 1."""
    x = np.asarray(x, float)
    a, b = (1 - math.sqrt(gamma)) ** 2, (1 + math.sqrt(gamma)) ** 2
    inside = (x > a) & (x < b)
    out = np.zeros_like(x)
    out[inside] = np.sqrt((b - x[inside]) * (x[inside] - a)) / (2 * math.pi * gamma * x[inside])
    return out


# -------------------------------------------------------------------------------------- matrix Bernstein


def matrix_bernstein_rank_one(n: int, p: int, rng: np.random.Generator, reps: int = 200) -> dict:
    """S = (1/n) sum (x_i x_i^T - I) with x_i uniform on sqrt(p) S^{p-1} (bounded: ||x x^T - I|| <= p).  Matrix
    Bernstein: E||S|| <= sqrt(2 v log(2p)) + L log(2p)/3 with v = ||sum E X_i^2|| / n^2 = (p - 1)/n, L = p/n."""
    vals = []
    for _ in range(reps):
        X = sample_sphere(p, n, rng) * math.sqrt(p)
        S = X.T @ X / n - np.eye(p)
        vals.append(np.max(np.abs(np.linalg.eigvalsh(S))))
    v = (p - 1) / n
    L = p / n
    bound = math.sqrt(2 * v * math.log(2 * p)) + L * math.log(2 * p) / 3
    return {"mean": float(np.mean(vals)), "bound": bound, "scalar_union": math.sqrt(2 * v * math.log(2 * p * p))}


# --------------------------------------------------------------------------------------------- comparison


def exchangeable_max(n: int, rho: float, rng: np.random.Generator, reps: int = 4000) -> float:
    """E max of n N(0,1) with pairwise correlation rho: sqrt(1 - rho) Z_i + sqrt(rho) W."""
    Z = rng.standard_normal((reps, n))
    W = rng.standard_normal((reps, 1))
    return float(np.mean(np.max(math.sqrt(1 - rho) * Z + math.sqrt(rho) * W, axis=1)))


def sudakov_lower(eps: float, N: int) -> float:
    """Sudakov's minoration: E sup >= (eps/2) sqrt(log N) / sqrt(2)... in the form E max over an eps-separated set of N
    points >= c eps sqrt(log N); we return the explicit constant from E max of N iid N(0, eps^2/2) (Slepian):
    (eps/sqrt 2) E max_N Z."""
    return eps / math.sqrt(2) * expected_max_gaussians(N)


# ---------------------------------------------------------------------------------- statistical dimension


def stat_dim_l1(s: int, p: int) -> float:
    """The statistical dimension of the l1 descent cone at an s-sparse vector in R^p (Amelunxen et al. 2014):
    inf_{tau >= 0} { s (1 + tau^2) + (p - s) E[(|g| - tau)_+^2] }, E[(|g| - tau)_+^2] = 2[(1 + tau^2) Phi(-tau) - tau phi(tau)]."""
    def J(tau):
        tail = 2 * ((1 + tau ** 2) * stats.norm.sf(tau) - tau * stats.norm.pdf(tau))
        return s * (1 + tau ** 2) + (p - s) * tail

    r = optimize.minimize_scalar(J, bounds=(0, 10), method="bounded")
    return float(r.fun)


def donoho_tanner_curve(rho_grid, p: int = 2000) -> np.ndarray:
    """Phase transition in (s/p, m/p): m/p = delta(s)/p, by the statistical dimension."""
    return np.array([stat_dim_l1(max(1, int(round(r * p))), p) / p for r in rho_grid])


def gaussian_width_l1_ball(p: int) -> float:
    """w(B_1^p) = E max_i |g_i| ~ sqrt(2 log 2p)."""
    f = lambda x: x * 2 * p * stats.norm.pdf(x) * (2 * stats.norm.cdf(x) - 1) ** (p - 1)  # noqa: E731
    return float(integrate.quad(f, 0, 12, limit=200)[0])


def gaussian_width_l2_ball(p: int) -> float:
    return norm_chi_moments(p)["mean"]


# ------------------------------------------------------------------------------------------------- chaining


def walk_max(N: int, rng: np.random.Generator, reps: int = 2000) -> float:
    """E max_{0 <= j <= N} B(j/N) for Brownian motion on a grid of N steps; tends to sqrt(2/pi) as N grows."""
    out = []
    for _ in range(max(1, reps // 200)):
        S = np.cumsum(rng.standard_normal((200, N)), axis=1) / math.sqrt(N)
        out.append(np.maximum(S.max(axis=1), 0.0))
    return float(np.mean(np.concatenate(out)))


def dudley_brownian(delta: float = 0.0) -> float:
    """Dudley's entropy integral for Brownian motion on [0, 1] in its canonical metric d(s, t) = sqrt|s - t|:
    N(eps) = 1/eps^2 intervals, so int_delta^1 sqrt(log N(eps)) d eps = int_delta^1 sqrt(2 log(1/eps)) d eps,
    which is sqrt(pi/2) at delta = 0 (constants of the theorem aside)."""
    f = lambda e: math.sqrt(2 * math.log(1 / e))  # noqa: E731
    return float(integrate.quad(f, max(delta, 0.0), 1, limit=200)[0])


def union_bound_max(N: int, sigma: float = 1.0) -> float:
    """The single-scale bound E max of N centred Gaussians with SD <= sigma: sigma sqrt(2 log N)."""
    return sigma * math.sqrt(2 * math.log(N))
