"""statkit.asymptotics -- the risk-bump explorer (Part 47 of *Statistics, Built*, "Asymptotic Statistics").

* **Hodges's estimator:** the exact scaled risk n E(T - theta)^2 of "xbar, or 0 if |xbar| < n^{-1/4}" for normal data,
  over theta and over local parameters theta = h / sqrt n.
* **Quantiles:** the Bahadur remainder sqrt(n)(xi_hat - xi) - sqrt(n)(p - F_n(xi)) / f(xi).
* **U-statistics:** the Hoeffding decomposition of a kernel's variance; a degenerate kernel's chi-square limit.
* **LAN:** the local log-likelihood ratio for a Cauchy location family against its Gaussian-shift limit.
* **Efficiency:** Pitman efficiencies of the sign and Wilcoxon tests against the t test.
* **Saddlepoints:** Daniels's density and Lugannani-Rice's tail for a mean of exponentials, against the exact gamma,
  the normal and the one-term Edgeworth approximations.
* **Non-regular models:** the uniform maximum; the bootstrap's failure for it and the m-out-of-n repair.

Tested in ``tests/test_stats_kit_asymptotics.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------------------------------------------
# Hodges's superefficient estimator
# ---------------------------------------------------------------------------------------------------------------
def _z2_mass(lo, hi):
    """int_lo^hi z^2 phi(z) dz and int_lo^hi phi(z) dz, elementwise."""
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    P = stats.norm.cdf(hi) - stats.norm.cdf(lo)
    t = np.where(np.isfinite(hi), hi * stats.norm.pdf(hi), 0.0) - np.where(np.isfinite(lo), lo * stats.norm.pdf(lo), 0.0)
    return P - t, P


def hodges_risk(theta, n: int, power: float = 0.25) -> np.ndarray:
    """n E(T - theta)^2 for T = xbar 1(|xbar| >= n^{-power}), xbar ~ N(theta, 1/n), exactly.  With Z = sqrt n (xbar -
    theta), T = 0 when Z lies in (lo, hi) = sqrt n(-a - theta, a - theta), a = n^{-power}; there the loss is n theta^2,
    elsewhere Z^2."""
    theta = np.asarray(theta, float)
    a = n ** (-power)
    lo, hi = math.sqrt(n) * (-a - theta), math.sqrt(n) * (a - theta)
    z2_in, p_in = _z2_mass(lo, hi)
    return (1 - z2_in) + n * theta ** 2 * p_in


def hodges_local(h, n: int, power: float = 0.25) -> np.ndarray:
    """The scaled risk at the local parameter theta = h / sqrt n."""
    return hodges_risk(np.asarray(h, float) / math.sqrt(n), n, power)


# ---------------------------------------------------------------------------------------------------------------
# Quantiles
# ---------------------------------------------------------------------------------------------------------------
def bahadur_remainder(n: int, reps: int, rng, p: float = 0.5) -> dict:
    """For standard normal samples: sqrt n (xi_hat - xi) and its Bahadur linearization sqrt n (p - F_n(xi)) / f(xi);
    the remainder's RMS shrinks like n^{-1/4}."""
    xi = stats.norm.ppf(p)
    f = stats.norm.pdf(xi)
    x = rng.normal(0, 1, (reps, n))
    q = np.quantile(x, p, axis=1, method="inverted_cdf")
    Fn = np.mean(x <= xi, axis=1)
    lead = math.sqrt(n) * (p - Fn) / f
    full = math.sqrt(n) * (q - xi)
    return {"full": full, "lead": lead, "rms_rem": float(np.sqrt(np.mean((full - lead) ** 2))),
            "sd_full": float(full.std()), "theory_sd": math.sqrt(p * (1 - p)) / f}


# ---------------------------------------------------------------------------------------------------------------
# U-statistics
# ---------------------------------------------------------------------------------------------------------------
def u_statistic(x, kernel) -> float:
    """sum_{i<j} h(x_i, x_j) / C(n, 2), for a symmetric kernel of order 2 vectorized over pairs."""
    x = np.asarray(x, float)
    i, j = np.triu_indices(len(x), 1)
    return float(np.mean(kernel(x[i], x[j])))


def gini_variance(n: int) -> dict:
    """Gini's mean difference |x - y| for N(0, 1) data: theta = 2/sqrt(pi); the Hoeffding projection h1(x) = E|x - Y|
    has variance zeta1, the kernel zeta2; Var U = [4(n - 2) zeta1 + 2 zeta2] / (n(n - 1)), by quadrature."""
    from scipy import integrate

    theta = 2 / math.sqrt(math.pi)
    h1 = lambda x: 2 * stats.norm.pdf(x) + x * (2 * stats.norm.cdf(x) - 1)  # noqa: E731  E|x - Y|, Y ~ N(0,1)
    zeta1 = integrate.quad(lambda x: (h1(x) - theta) ** 2 * stats.norm.pdf(x), -12, 12)[0]
    zeta2 = 2.0 - theta ** 2  # E|X - Y|^2 = Var(X - Y) = 2
    var = (4 * (n - 2) * zeta1 + 2 * zeta2) / (n * (n - 1))
    return {"theta": theta, "zeta1": zeta1, "zeta2": zeta2, "var": var, "first_order": 4 * zeta1 / n}


# ---------------------------------------------------------------------------------------------------------------
# LAN and efficiency
# ---------------------------------------------------------------------------------------------------------------
def cauchy_local_llr(n: int, h: float, reps: int, rng) -> dict:
    """log prod f(x_i - h/sqrt n) / f(x_i) under theta = 0 for the Cauchy location family (Fisher information 1/2),
    against LAN's N(-h^2 I/2, h^2 I)."""
    x = rng.standard_cauchy((reps, n))
    t = h / math.sqrt(n)
    llr = np.sum(np.log1p(x ** 2) - np.log1p((x - t) ** 2), axis=1)
    I = 0.5
    return {"llr": llr, "mean": float(llr.mean()), "var": float(llr.var()), "lan_mean": -h * h * I / 2, "lan_var": h * h * I}


def pitman_are(name: str) -> float:
    """Pitman asymptotic relative efficiencies against the t test for normal data, and for the double exponential."""
    return {"sign_normal": 2 / math.pi, "wilcoxon_normal": 3 / math.pi, "sign_laplace": 2.0, "wilcoxon_laplace": 1.5,
            "wilcoxon_min": 108 / 125}[name]


def local_power(h, info: float, alpha: float = 0.05, two_sided: bool = False) -> np.ndarray:
    """Le Cam's third lemma: a test of theta = 0 with statistic asymptotically N(0, 1) under H0 has local power
    1 - Phi(z_alpha - h sqrt(I)) at theta = h / sqrt n (one-sided)."""
    h = np.asarray(h, float)
    if two_sided:
        z = stats.norm.ppf(1 - alpha / 2)
        return stats.norm.sf(z - h * math.sqrt(info)) + stats.norm.cdf(-z - h * math.sqrt(info))
    return stats.norm.sf(stats.norm.ppf(1 - alpha) - h * math.sqrt(info))


# ---------------------------------------------------------------------------------------------------------------
# Saddlepoints for the mean of exponentials
# ---------------------------------------------------------------------------------------------------------------
def mean_exp_density(xbar, n: int) -> dict:
    """The density of the mean of n Exp(1) variables: exact (Gamma(n, 1/n)), normal, one-term Edgeworth and
    Daniels's saddlepoint (exact up to Stirling's constant), with the saddlepoint renormalized."""
    xb = np.asarray(xbar, float)
    exact = stats.gamma.pdf(xb, n, scale=1 / n)
    z = (xb - 1) * math.sqrt(n)
    normal = math.sqrt(n) * stats.norm.pdf(z)
    edge = normal * (1 + (2 / (6 * math.sqrt(n))) * (z ** 3 - 3 * z))  # skewness 2, H3
    # K(t) = -log(1 - t); saddlepoint s solves K'(s) = xbar: s = 1 - 1/xbar; K''(s) = xbar^2
    s = 1 - 1 / xb
    K = -np.log1p(-s)
    sp = np.sqrt(n / (2 * math.pi * xb ** 2)) * np.exp(n * (K - s * xb))
    return {"exact": exact, "normal": normal, "edgeworth": edge, "saddle": sp}


def lugannani_rice(xbar, n: int) -> dict:
    """P(Xbar >= x) for the mean of n Exp(1): exact, normal, and the Lugannani-Rice saddlepoint formula."""
    x = np.asarray(xbar, float)
    exact = stats.gamma.sf(x, n, scale=1 / n)
    normal = stats.norm.sf((x - 1) * math.sqrt(n))
    s = 1 - 1 / x
    K = -np.log1p(-s)
    w = np.sign(s) * np.sqrt(2 * n * (s * x - K))
    u = s * np.sqrt(n * x ** 2)
    lr = stats.norm.sf(w) + stats.norm.pdf(w) * (1 / u - 1 / w)
    return {"exact": exact, "normal": normal, "lr": lr}


# ---------------------------------------------------------------------------------------------------------------
# Non-regular: the uniform maximum and the bootstrap
# ---------------------------------------------------------------------------------------------------------------
def uniform_max_bootstrap(n: int, B: int, rng, m: int | None = None) -> dict:
    """One sample from U(0, 1); the bootstrap law of n (max - max*) (or m (max - max*_m) for m-out-of-n), against the
    true limit Exp(1).  The ordinary bootstrap puts mass about 1 - (1 - 1/n)^n -> 1 - 1/e at 0."""
    x = rng.random(n)
    M = x.max()
    k = n if m is None else m
    idx = rng.integers(0, n, (B, k))
    Mb = x[idx].max(axis=1)
    stat = k * (M - Mb)
    return {"stat": stat, "atom0": float(np.mean(stat == 0)), "theory_atom": 1 - (1 - 1 / n) ** n if m is None else None,
            "ks_exp": float(stats.kstest(stat, "expon").statistic)}
