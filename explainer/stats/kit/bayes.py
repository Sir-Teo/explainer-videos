"""statkit.bayes (I): conjugate updating, credible intervals, prediction, grids and a Metropolis walk (Part 15 of
*Statistics, Built*).

    from explainer.stats.kit.bayes import beta_update, credible, hpd, beta_binomial_pmf, grid_posterior, metropolis

Everything here is exact or checked against SciPy in ``tests/test_stats_kit_bayes.py``; Part 26 builds the full
Bayesian workflow and Part 27 its computation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import optimize, special, stats


# ---------------------------------------------------------------------------------------------------------------
# Conjugate families
# ---------------------------------------------------------------------------------------------------------------
def beta_update(a: float, b: float, successes: int, failures: int) -> tuple[float, float]:
    """Beta(a, b) prior, binomial data: the Beta(a + s, b + f) posterior."""
    return a + successes, b + failures


def gamma_update(shape: float, rate: float, total: float, exposure: float) -> tuple[float, float]:
    """Gamma(shape, rate) prior on a Poisson rate, ``total`` events in ``exposure``: Gamma(shape + total, rate + exposure)."""
    return shape + total, rate + exposure


def normal_update(m0: float, s0: float, xbar: float, sigma: float, n: int) -> tuple[float, float]:
    """N(m0, s0^2) prior on a mean, n observations with known SD sigma: precisions add, means average by precision."""
    p0, pd = 1 / s0 ** 2, n / sigma ** 2
    return (p0 * m0 + pd * xbar) / (p0 + pd), float(np.sqrt(1 / (p0 + pd)))


def normal_unknown_var(x) -> dict:
    """The reference posterior for (mu, sigma^2) under p(mu, sigma^2) propto 1/sigma^2: mu | data is
    xbar + s/sqrt(n) t_{n-1}, the same as Part 8's t-interval."""
    x = np.asarray(x, float)
    n = len(x)
    return {"loc": float(x.mean()), "scale": float(x.std(ddof=1) / np.sqrt(n)), "df": n - 1}


# ---------------------------------------------------------------------------------------------------------------
# Summaries
# ---------------------------------------------------------------------------------------------------------------
def credible(dist, level: float = 0.95) -> tuple[float, float]:
    """Equal-tailed credible interval of a frozen SciPy distribution."""
    a = (1 - level) / 2
    return float(dist.ppf(a)), float(dist.ppf(1 - a))


def hpd(dist, level: float = 0.95) -> tuple[float, float]:
    """Highest-posterior-density interval of a unimodal frozen distribution: the shortest interval with the given
    probability (found by minimizing the width over the lower tail probability)."""
    def width(lo_p):
        return dist.ppf(lo_p + level) - dist.ppf(lo_p)
    r = optimize.minimize_scalar(width, bounds=(1e-12, 1 - level - 1e-12), method="bounded", options={"xatol": 1e-12})
    return float(dist.ppf(r.x)), float(dist.ppf(r.x + level))


def beta_binomial_pmf(k, m: int, a: float, b: float) -> np.ndarray:
    """Posterior predictive for k successes in m new trials under a Beta(a, b) posterior."""
    k = np.asarray(k)
    return np.exp(special.gammaln(m + 1) - special.gammaln(k + 1) - special.gammaln(m - k + 1)
                  + special.betaln(k + a, m - k + b) - special.betaln(a, b))


def rule_of_succession(s: int, n: int) -> float:
    """Laplace: after s successes in n trials, under a uniform prior, P(next is a success) = (s + 1)/(n + 2)."""
    return (s + 1) / (n + 2)


# ---------------------------------------------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------------------------------------------
def grid_posterior(grid, log_prior, log_lik):
    """Normalized posterior on a 1-D grid (trapezoid rule); ``log_prior`` and ``log_lik`` are functions of the grid."""
    g = np.asarray(grid, float)
    lp = log_prior(g) + log_lik(g)
    w = np.exp(lp - lp.max())
    return w / np.trapezoid(w, g)


def grid_posterior_2d(gx, gy, log_post):
    """Normalized posterior on a 2-D grid: returns the density array [len(gy), len(gx)] and both marginals."""
    X, Y = np.meshgrid(gx, gy)
    lp = log_post(X, Y)
    w = np.exp(lp - lp.max())
    w /= np.trapezoid(np.trapezoid(w, gx, axis=1), gy)
    return w, np.trapezoid(w, gy, axis=0), np.trapezoid(w, gx, axis=1)


@dataclass
class Chain:
    draws: np.ndarray
    accepted: np.ndarray

    @property
    def acceptance(self) -> float:
        return float(self.accepted.mean())


def metropolis(log_post, start, step, n: int, rng: np.random.Generator) -> Chain:
    """Random-walk Metropolis (Metropolis et al. 1953): propose x + step * N(0, I); accept with min(1, ratio)."""
    x = np.atleast_1d(np.asarray(start, float)).copy()
    step = np.broadcast_to(np.asarray(step, float), x.shape)
    lp = log_post(x)
    out = np.empty((n, len(x)))
    acc = np.zeros(n, bool)
    for i in range(n):
        y = x + step * rng.standard_normal(len(x))
        ly = log_post(y)
        if np.log(rng.random()) < ly - lp:
            x, lp = y, ly
            acc[i] = True
        out[i] = x
    return Chain(out, acc)


def ess(x) -> float:
    """Effective sample size of a 1-D chain from its autocorrelations (Geyer's initial positive sequence)."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n] / (x.var() * n)
    s = 0.0
    for k in range(1, n - 1, 2):
        pair = ac[k] + ac[k + 1]
        if pair < 0:
            break
        s += pair
    return float(n / (1 + 2 * s))


# ---------------------------------------------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------------------------------------------
def bayes_factor_binomial(s: int, n: int, p0: float = 0.5, a: float = 1.0, b: float = 1.0) -> float:
    """BF_10 for H1: p ~ Beta(a, b) against H0: p = p0, from s successes in n trials (the binomial coefficient
    cancels)."""
    log_m1 = special.betaln(s + a, n - s + b) - special.betaln(a, b)
    log_m0 = s * np.log(p0) + (n - s) * np.log1p(-p0)
    return float(np.exp(log_m1 - log_m0))
