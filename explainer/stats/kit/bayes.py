"""statkit.bayes: conjugate updating, credible intervals, prediction, grids and a Metropolis walk (I, Part 15 of
*Statistics, Built*); the hierarchical normal model on a grid with exact draws, normal Bayes factors and Lindley's
paradox, the Sellke-Bayarri-Berger bound, Bayesian linear regression's evidence, simulation-based calibration, and
the Chinese restaurant process and stick-breaking (II, Part 26).

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


# ---------------------------------------------------------------------------------------------------------------
# II (Part 26): the hierarchical normal model
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Hier:
    """y_j ~ N(theta_j, sigma_j^2), theta_j ~ N(mu, tau^2), p(mu | tau) flat, p(tau) given on a grid (BDA section 5.4)."""
    y: np.ndarray
    sigma: np.ndarray
    tau: np.ndarray
    post_tau: np.ndarray  # density on the grid, integrating to 1
    mu_hat: np.ndarray  # E(mu | tau, y)
    v_mu: np.ndarray  # Var(mu | tau, y)

    def cond_theta(self):
        """E(theta_j | tau, y) and Var(theta_j | tau, y) for every grid tau: arrays (len(tau), J)."""
        t2 = self.tau[:, None] ** 2
        s2 = self.sigma[None, :] ** 2
        w = t2 / (s2 + t2)  # the weight on the school's own estimate: 0 at tau = 0
        mean = w * self.y[None, :] + (1 - w) * self.mu_hat[:, None]
        v_cond = s2 * t2 / (s2 + t2)
        var = v_cond + (1 - w) ** 2 * self.v_mu[:, None]
        return mean, var

    def draws(self, n: int, rng: np.random.Generator) -> dict:
        """Exact posterior draws: tau from the grid (with jitter inside its cell), mu | tau, then theta | mu, tau."""
        p = self.post_tau * np.gradient(self.tau)
        p = p / p.sum()
        k = rng.choice(len(self.tau), size=n, p=p)
        h = np.gradient(self.tau)[k]
        tau = np.clip(self.tau[k] + h * (rng.random(n) - 0.5), 0, None)
        s2 = self.sigma[None, :] ** 2
        t2 = tau[:, None] ** 2
        wj = 1 / (s2 + t2)
        mp = getattr(self, "mu_prior", None)
        m0, p0 = (0.0, 0.0) if mp is None else (float(mp[0]), 1 / float(mp[1]) ** 2)
        v_mu = 1 / (wj.sum(1) + p0)
        mu_hat = v_mu * ((wj * self.y[None, :]).sum(1) + p0 * m0)
        mu = mu_hat + np.sqrt(v_mu) * rng.standard_normal(n)
        prec = 1 / s2 + 1 / np.maximum(t2, 1e-300)
        mean = (self.y[None, :] / s2 + mu[:, None] / np.maximum(t2, 1e-300)) / prec
        theta = np.where(t2 > 1e-12, mean + rng.standard_normal((n, len(self.y))) / np.sqrt(prec), mu[:, None])
        return {"tau": tau, "mu": mu, "theta": theta}


def hier_normal(y, sigma, tau_grid, log_prior_tau=None, mu_prior=None) -> Hier:
    """The marginal posterior of tau: p(tau | y) ∝ p(tau) V_mu^{1/2} prod_j N(y_j | mu_hat, sigma_j^2 + tau^2) with a
    flat prior on mu, or, with ``mu_prior = (m0, s0)``, mu ~ N(m0, s0^2) (integrated out the same way)."""
    y, sigma, tau = np.asarray(y, float), np.asarray(sigma, float), np.asarray(tau_grid, float)
    lp = np.zeros_like(tau) if log_prior_tau is None else np.asarray(log_prior_tau(tau), float)
    V = sigma[None, :] ** 2 + tau[:, None] ** 2
    w = 1 / V
    m0, p0 = (0.0, 0.0) if mu_prior is None else (float(mu_prior[0]), 1 / float(mu_prior[1]) ** 2)
    v_mu = 1 / (w.sum(1) + p0)
    mu_hat = v_mu * ((w * y[None, :]).sum(1) + p0 * m0)
    quad = (w * y[None, :] ** 2).sum(1) + p0 * m0 ** 2 - mu_hat ** 2 / v_mu
    ll = 0.5 * np.log(v_mu) - 0.5 * np.log(V).sum(1) - 0.5 * quad
    lpost = lp + ll
    d = np.exp(lpost - lpost.max())
    d = d / np.trapezoid(d, tau)
    h = Hier(y, sigma, tau, d, mu_hat, v_mu)
    h.mu_prior = mu_prior
    return h


# ---------------------------------------------------------------------------------------------------------------
# II (Part 26): Bayes factors, Lindley, evidence
# ---------------------------------------------------------------------------------------------------------------
def bf01_normal(xbar: float, n: int, sigma: float, tau: float) -> float:
    """BF_01 for H0: mu = 0 against H1: mu ~ N(0, tau^2), from xbar ~ N(mu, sigma^2 / n)."""
    v0 = sigma ** 2 / n
    return float(stats.norm.pdf(xbar, 0, np.sqrt(v0)) / stats.norm.pdf(xbar, 0, np.sqrt(v0 + tau ** 2)))


def sbb_bound(p):
    """Sellke, Bayarri & Berger (2001): BF_01 >= -e p log p for p < 1/e (and 1 beyond)."""
    p = np.asarray(p, float)
    return np.where(p < 1 / np.e, -np.e * p * np.log(np.maximum(p, 1e-300)), 1.0)


def blr_log_evidence(X, y, alpha: float, sigma: float) -> float:
    """log p(y) for y = X w + e, w ~ N(0, I/alpha), e ~ N(0, sigma^2 I): y ~ N(0, sigma^2 I + X X'/alpha)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    C = sigma ** 2 * np.eye(len(y)) + X @ X.T / alpha
    return float(stats.multivariate_normal(np.zeros(len(y)), C, allow_singular=False).logpdf(y))


def blr_posterior(X, y, alpha: float, sigma: float):
    """Posterior mean and covariance of w in Bayesian linear regression."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    A = alpha * np.eye(X.shape[1]) + X.T @ X / sigma ** 2
    S = np.linalg.inv(A)
    return S @ X.T @ y / sigma ** 2, S


# ---------------------------------------------------------------------------------------------------------------
# II (Part 26): checking and nonparametrics
# ---------------------------------------------------------------------------------------------------------------
def sbc_ranks(draw_prior, draw_data, draw_posterior, n_sims: int, L: int, rng: np.random.Generator) -> np.ndarray:
    """Simulation-based calibration (Talts et al. 2018): for each simulation draw theta ~ prior, y ~ p(y | theta) and
    L posterior draws; the rank of theta among them is uniform on 0..L if the posterior is computed correctly."""
    ranks = np.empty(n_sims, int)
    for i in range(n_sims):
        th = draw_prior(rng)
        yv = draw_data(th, rng)
        post = draw_posterior(yv, L, rng)
        ranks[i] = int(np.sum(post < th))
    return ranks


def crp(n: int, alpha: float, rng: np.random.Generator) -> np.ndarray:
    """The Chinese restaurant process: table labels for n customers; customer i+1 joins table k with probability
    n_k / (i + alpha) and a new table with probability alpha / (i + alpha)."""
    z = np.zeros(n, int)
    counts = [1]
    for i in range(1, n):
        p = np.array(counts + [alpha], float) / (i + alpha)
        k = rng.choice(len(p), p=p)
        if k == len(counts):
            counts.append(1)
        else:
            counts[k] += 1
        z[i] = k
    return z


def crp_expected_tables(n: int, alpha: float) -> float:
    """E(number of tables) = sum_{i=0}^{n-1} alpha / (alpha + i), about alpha log(1 + n / alpha)."""
    return float(np.sum(alpha / (alpha + np.arange(n))))


def stick_breaking(alpha: float, K: int, rng: np.random.Generator) -> np.ndarray:
    """The first K weights of a Dirichlet process (Sethuraman 1994): w_k = V_k prod_{j<k} (1 - V_j), V ~ Beta(1, alpha)."""
    v = rng.beta(1, alpha, K)
    return v * np.concatenate([[1.0], np.cumprod(1 - v)[:-1]])
