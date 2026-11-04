"""statkit.intervals: confidence intervals written out, with their exact coverage (Part 11 of *Statistics, Built*).

    from explainer.stats.kit.intervals import BINOMIAL, binom_coverage, t_interval, fieller, dkw_band

Every binomial interval takes (x, n, alpha) and returns (lo, hi); ``binom_coverage`` computes its exact coverage at
any p by summing over the n + 1 outcomes, so no simulation error enters the sawtooth plots.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy import optimize, stats


def _z(alpha: float) -> float:
    return float(stats.norm.ppf(1 - alpha / 2))


def wald(x, n, alpha=0.05):
    """The textbook interval p-hat +- z sqrt(p-hat (1 - p-hat)/n) (Laplace 1812), clipped to [0, 1]."""
    p = x / n
    h = _z(alpha) * np.sqrt(p * (1 - p) / n)
    return max(0.0, p - h), min(1.0, p + h)


def wilson(x, n, alpha=0.05):
    """Wilson (1927): every p the score test does not reject."""
    z = _z(alpha)
    p = x / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, c - h), min(1.0, c + h)


def agresti_coull(x, n, alpha=0.05):
    """Agresti & Coull (1998): add z^2/2 successes and failures, then Wald."""
    z = _z(alpha)
    nt = n + z * z
    pt = (x + z * z / 2) / nt
    h = z * np.sqrt(pt * (1 - pt) / nt)
    return max(0.0, pt - h), min(1.0, pt + h)


def clopper_pearson(x, n, alpha=0.05):
    """Clopper & Pearson (1934): invert the two one-sided exact binomial tests (beta quantiles)."""
    lo = 0.0 if x == 0 else float(stats.beta.ppf(alpha / 2, x, n - x + 1))
    hi = 1.0 if x == n else float(stats.beta.ppf(1 - alpha / 2, x + 1, n - x))
    return lo, hi


def jeffreys(x, n, alpha=0.05):
    """The equal-tailed Beta(x + 1/2, n - x + 1/2) posterior interval (Jeffreys' prior), as BCD (2001) recommend."""
    lo = 0.0 if x == 0 else float(stats.beta.ppf(alpha / 2, x + 0.5, n - x + 0.5))
    hi = 1.0 if x == n else float(stats.beta.ppf(1 - alpha / 2, x + 0.5, n - x + 0.5))
    return lo, hi


def likelihood_ratio(x, n, alpha=0.05):
    """Every p with 2(l(p-hat) - l(p)) <= chi^2_1 quantile: the inverted likelihood ratio test."""
    c = float(stats.chi2.ppf(1 - alpha, 1))

    def ll(p):
        out = 0.0
        if x > 0:
            out += x * np.log(p)
        if x < n:
            out += (n - x) * np.log(1 - p)
        return out

    ph = x / n
    top = ll(min(max(ph, 1e-12), 1 - 1e-12))
    f = lambda p: 2 * (top - ll(p)) - c  # noqa: E731
    lo = 0.0 if x == 0 else optimize.brentq(f, 1e-12, ph)
    hi = 1.0 if x == n else optimize.brentq(f, ph, 1 - 1e-12)
    return float(lo), float(hi)


BINOMIAL: dict[str, Callable] = {"wald": wald, "wilson": wilson, "agresti_coull": agresti_coull,
                                 "clopper_pearson": clopper_pearson, "jeffreys": jeffreys, "lr": likelihood_ratio}


def binom_coverage(method: Callable, n: int, ps, alpha=0.05) -> np.ndarray:
    """Exact coverage P_p(p in C(X)) for each p, X ~ Binomial(n, p): a sum over the n + 1 outcomes."""
    ps = np.atleast_1d(np.asarray(ps, float))
    ints = np.array([method(x, n, alpha) for x in range(n + 1)])
    pmf = stats.binom.pmf(np.arange(n + 1)[None, :], n, ps[:, None])
    inside = (ints[None, :, 0] <= ps[:, None] + 1e-12) & (ps[:, None] <= ints[None, :, 1] + 1e-12)
    return (pmf * inside).sum(1)


def binom_width(method: Callable, n: int, ps, alpha=0.05) -> np.ndarray:
    """Expected width E_p(hi - lo)."""
    ps = np.atleast_1d(np.asarray(ps, float))
    ints = np.array([method(x, n, alpha) for x in range(n + 1)])
    pmf = stats.binom.pmf(np.arange(n + 1)[None, :], n, ps[:, None])
    return (pmf * (ints[:, 1] - ints[:, 0])[None, :]).sum(1)


def t_interval(x, alpha=0.05):
    x = np.asarray(x, float)
    n = len(x)
    h = stats.t.ppf(1 - alpha / 2, n - 1) * x.std(ddof=1) / np.sqrt(n)
    return float(x.mean() - h), float(x.mean() + h)


def var_interval(x, alpha=0.05):
    """The chi-squared pivot (n - 1)s^2/sigma^2 ~ chi^2_{n-1}: normal data only (Part 8)."""
    x = np.asarray(x, float)
    n = len(x)
    ss = (n - 1) * x.var(ddof=1)
    return float(ss / stats.chi2.ppf(1 - alpha / 2, n - 1)), float(ss / stats.chi2.ppf(alpha / 2, n - 1))


def rate_interval(x, alpha=0.05):
    """Exponential rate: lambda * sum(x) ~ Gamma(n, 1) is a pivot."""
    x = np.asarray(x, float)
    n, s = len(x), x.sum()
    return float(stats.gamma.ppf(alpha / 2, n) / s), float(stats.gamma.ppf(1 - alpha / 2, n) / s)


def fieller(mx, my, vx, vy, cxy=0.0, df=None, alpha=0.05):
    """Fieller (1954): the set of ratios rho = mu_y/mu_x with (my - rho mx)^2 <= q^2 (vy - 2 rho cxy + rho^2 vx).
    Returns ("bounded", lo, hi), ("complement", lo, hi) meaning (-inf, lo] u [hi, inf), or ("all", -inf, inf)."""
    q = float(stats.t.ppf(1 - alpha / 2, df)) if df else _z(alpha)
    a = mx * mx - q * q * vx
    b = -2 * (mx * my - q * q * cxy)
    c = my * my - q * q * vy
    disc = b * b - 4 * a * c
    if a > 0:
        r = np.sqrt(max(disc, 0.0))
        return ("bounded", (-b - r) / (2 * a), (-b + r) / (2 * a))
    if disc < 0:
        return ("all", -np.inf, np.inf)
    r = np.sqrt(disc)
    lo, hi = sorted(((-b - r) / (2 * a), (-b + r) / (2 * a)))
    return ("complement", lo, hi)


def dkw_band(x, alpha=0.05):
    """The Dvoretzky-Kiefer-Wolfowitz band (Massart's constant): F-hat +- sqrt(log(2/alpha)/(2n)) holds for all t at once."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    eps = np.sqrt(np.log(2 / alpha) / (2 * n))
    f = np.arange(1, n + 1) / n
    return x, np.clip(f - eps, 0, 1), np.clip(f + eps, 0, 1), float(eps)


def prediction_interval(x, alpha=0.05):
    """For one new normal observation: x-bar +- t s sqrt(1 + 1/n)."""
    x = np.asarray(x, float)
    n = len(x)
    h = stats.t.ppf(1 - alpha / 2, n - 1) * x.std(ddof=1) * np.sqrt(1 + 1 / n)
    return float(x.mean() - h), float(x.mean() + h)


def order_stat_coverage(n: int, r: int = 1) -> float:
    """Wilks (1941): P(a new draw lands between the r-th smallest and r-th largest of n), any continuous law."""
    return (n + 1 - 2 * r) / (n + 1)
