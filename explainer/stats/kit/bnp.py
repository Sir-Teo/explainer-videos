"""statkit.bnp: Bayesian asymptotics and nonparametric Bayes (Part 53 of *Statistics, Built*).

Checked in ``tests/test_stats_kit_bnp.py``:

* the Gaussian sequence model with Gaussian priors theta_k ~ N(0, tau^2 k^(-1-2 alpha)): the exact posterior, its exact
  frequentist risk and spread, credible balls and their coverage, credible intervals for linear functionals and their
  exact coverage (Knapik, van der Vaart & van Zanten 2011); empirical Bayes choice of alpha by marginal likelihood;
* Bernstein-von Mises: the total variation between a Beta posterior and its normal approximation, by quadrature;
* misspecification: a Poisson model for overdispersed counts, its credible interval and a calibrated generalized
  (tempered) posterior;
* the Dirichlet process: its posterior mean CDF, pointwise Beta credible bands, Polya-urn draws; a collapsed Gibbs
  sampler for a Dirichlet-process mixture of normals (Neal 2000, Algorithm 3);
* sparse normal means: the spike-and-slab posterior with a Beta-binomial prior on the inclusion weight, integrated on a
  grid; marginal inclusion probabilities and credible intervals; the horseshoe's posterior by quadrature.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, special, stats

# ---------------------------------------------------------------------------------------- the sequence model


def prior_var(K: int, alpha: float, tau2: float = 1.0) -> np.ndarray:
    k = np.arange(1, K + 1)
    return tau2 * k ** (-1.0 - 2.0 * alpha)


def sobolev_truth(K: int, beta: float, scale: float = 1.0) -> np.ndarray:
    """theta_k = scale * k^(-1/2 - beta) * sin(k): a beta-regular truth (just inside the Sobolev ball of order beta)."""
    k = np.arange(1, K + 1)
    return scale * k ** (-0.5 - beta) * np.sin(k)


def posterior(Y, n: int, lam) -> dict:
    """Y_k = theta_k + Z_k / sqrt(n), theta_k ~ N(0, lam_k): posterior N(w Y, lam / (1 + n lam)), w = n lam / (1 + n lam)."""
    lam = np.asarray(lam, float)
    w = n * lam / (1 + n * lam)
    return {"mean": w * np.asarray(Y, float), "var": lam / (1 + n * lam), "w": w}


def risk(theta0, n: int, lam) -> dict:
    """Exact frequentist risk of the posterior mean, split into bias^2 and variance, and the posterior spread."""
    lam = np.asarray(lam, float)
    w = n * lam / (1 + n * lam)
    th = np.asarray(theta0, float)
    b2 = float(np.sum((1 - w) ** 2 * th ** 2))
    v = float(np.sum(w ** 2) / n)
    spread = float(np.sum(lam / (1 + n * lam)))
    return {"bias2": b2, "var": v, "risk": b2 + v, "spread": spread}


def credible_ball_coverage(theta0, n: int, lam, level: float = 0.95, reps: int = 4000, rng=None) -> dict:
    """Frequentist coverage of the posterior credible ball {theta: ||theta - mean|| <= r}, r the posterior quantile of
    ||theta - mean|| (a weighted chi-square), both by simulation."""
    rng = rng or np.random.default_rng(0)
    lam = np.asarray(lam, float)
    th = np.asarray(theta0, float)
    K = len(lam)
    w = n * lam / (1 + n * lam)
    pv = lam / (1 + n * lam)
    draws = np.sum(pv * rng.standard_normal((reps, K)) ** 2, axis=1)
    r2 = float(np.quantile(draws, level))
    err = -(1 - w) * th + w * rng.standard_normal((reps, K)) / math.sqrt(n)
    d2 = np.sum(err ** 2, axis=1)
    return {"coverage": float(np.mean(d2 <= r2)), "radius": math.sqrt(r2), "dist": float(np.mean(np.sqrt(d2)))}


def functional_coverage(theta0, n: int, lam, a, level: float = 0.95) -> dict:
    """Exact frequentist coverage of the credible interval for L(theta) = sum a_k theta_k: the posterior is
    N(sum a w Y, sum a^2 v); under theta0 its centre is N(sum a w theta0, sum a^2 w^2 / n)."""
    lam = np.asarray(lam, float)
    a = np.asarray(a, float)
    th = np.asarray(theta0, float)
    w = n * lam / (1 + n * lam)
    s_post = math.sqrt(float(np.sum(a ** 2 * lam / (1 + n * lam))))
    bias = float(np.sum(a * (w - 1) * th))
    s_freq = math.sqrt(float(np.sum(a ** 2 * w ** 2)) / n)
    z = stats.norm.ppf(0.5 + level / 2)
    cov = stats.norm.cdf((z * s_post - bias) / s_freq) - stats.norm.cdf((-z * s_post - bias) / s_freq)
    return {"coverage": float(cov), "s_post": s_post, "s_freq": s_freq, "bias": bias}


def log_marginal(Y, n: int, alpha: float, tau2: float = 1.0) -> float:
    """log p(Y | alpha): Y_k ~ N(0, lam_k + 1/n) independently."""
    Y = np.asarray(Y, float)
    s2 = prior_var(len(Y), alpha, tau2) + 1.0 / n
    return float(-0.5 * np.sum(np.log(2 * math.pi * s2) + Y ** 2 / s2))


def eb_alpha(Y, n: int, grid=None, tau2: float = 1.0) -> float:
    grid = np.linspace(0.1, 4.0, 79) if grid is None else np.asarray(grid)
    ll = [log_marginal(Y, n, a, tau2) for a in grid]
    return float(grid[int(np.argmax(ll))])


def contraction_rate(n: int, alpha: float, beta: float) -> float:
    """The posterior's contraction rate in the sequence model: n^(-min(alpha, beta)/(1 + 2 alpha)) (van der Vaart & van
    Zanten 2008; Knapik et al. 2011); the minimax rate n^(-beta/(1 + 2 beta)) when alpha = beta."""
    return n ** (-min(alpha, beta) / (1 + 2 * alpha))


# --------------------------------------------------------------------------------------- Bernstein-von Mises


def bvm_tv_beta(k: int, n: int, a: float = 1.0, b: float = 1.0) -> float:
    """TV between the Beta(a + k, b + n - k) posterior and N(p_hat, p_hat(1 - p_hat)/n), by quadrature."""
    ph = min(max(k / n, 1e-9), 1 - 1e-9)
    sd = math.sqrt(ph * (1 - ph) / n)
    post = stats.beta(a + k, b + n - k)
    f = lambda x: abs(post.pdf(x) - stats.norm.pdf(x, ph, sd))  # noqa: E731
    lo, hi = max(0.0, ph - 12 * sd - 0.05), min(1.0, ph + 12 * sd + 0.05)
    inside = integrate.quad(f, lo, hi, limit=400, points=[ph])[0]
    outside = stats.norm.cdf(lo, ph, sd) + stats.norm.sf(hi, ph, sd) + post.cdf(lo) + post.sf(hi)
    return 0.5 * (inside + outside)


# ----------------------------------------------------------------------------------------- misspecification


def poisson_gamma_ci(y, a: float = 0.01, b: float = 0.01, level: float = 0.95, eta: float = 1.0) -> tuple:
    """Credible interval for a Poisson mean under a Gamma(a, b) prior; eta < 1 tempers the likelihood (a generalized
    posterior Gamma(a + eta sum y, b + eta n))."""
    y = np.asarray(y, float)
    g = stats.gamma(a + eta * y.sum(), scale=1 / (b + eta * len(y)))
    return float(g.ppf(0.5 - level / 2)), float(g.ppf(0.5 + level / 2))


def calibrated_eta(y) -> float:
    """eta = mean / variance: the tempering that matches the posterior spread to the sandwich variance (for a Poisson
    working model, the inverse of the dispersion)."""
    y = np.asarray(y, float)
    v = y.var(ddof=1)
    return float(min(1.0, y.mean() / v)) if v > 0 else 1.0


# -------------------------------------------------------------------------------------- the Dirichlet process


def dp_posterior_cdf(x, data, alpha: float, base_cdf) -> np.ndarray:
    """E[F(x) | data] = (alpha G(x) + n F_n(x)) / (alpha + n)."""
    data = np.sort(np.asarray(data, float))
    n = len(data)
    Fn = np.searchsorted(data, np.asarray(x, float), side="right") / n
    return (alpha * base_cdf(np.asarray(x, float)) + n * Fn) / (alpha + n)


def dp_band(x, data, alpha: float, base_cdf, level: float = 0.95) -> tuple:
    """Pointwise credible band: F(x) | data ~ Beta(A H(x), A (1 - H(x))), A = alpha + n, H the posterior mean."""
    H = dp_posterior_cdf(x, data, alpha, base_cdf)
    A = alpha + len(data)
    lo = stats.beta.ppf(0.5 - level / 2, np.maximum(A * H, 1e-9), np.maximum(A * (1 - H), 1e-9))
    hi = stats.beta.ppf(0.5 + level / 2, np.maximum(A * H, 1e-9), np.maximum(A * (1 - H), 1e-9))
    return np.where(H <= 0, 0.0, lo), np.where(H >= 1, 1.0, hi)


def polya_urn(m: int, alpha: float, base_sampler, rng) -> np.ndarray:
    """m draws from a random G ~ DP(alpha, G0) by the Blackwell-MacQueen urn."""
    out = []
    for i in range(m):
        if rng.random() < alpha / (alpha + i):
            out.append(base_sampler(rng))
        else:
            out.append(out[rng.integers(i)])
    return np.asarray(out)


def stick_weights(alpha: float, K: int, rng) -> np.ndarray:
    v = rng.beta(1, alpha, K)
    return v * np.concatenate([[1.0], np.cumprod(1 - v)[:-1]])


def _nig_logpred(x, n, s, ss, mu0, k0, a0, b0):
    """log posterior predictive of x under a normal-inverse-gamma model given n points with sum s and sum of squares ss."""
    kn = k0 + n
    mn = (k0 * mu0 + s) / kn
    an = a0 + n / 2
    xbar = s / n if n > 0 else 0.0
    bn = b0 + 0.5 * (ss - n * xbar ** 2) + k0 * n * (xbar - mu0) ** 2 / (2 * kn) if n > 0 else b0
    scale = math.sqrt(bn * (kn + 1) / (an * kn))
    return stats.t.logpdf(x, 2 * an, loc=mn, scale=scale)


def dp_mixture_gibbs(x, alpha: float, iters: int, rng, mu0=None, k0: float = 0.1, a0: float = 2.0, b0=None, burn: int = 200,
                     grid=None) -> dict:
    """Collapsed Gibbs sampling for a DP mixture of normals with a normal-inverse-gamma base (Neal 2000, Alg. 3).
    Returns the posterior mean density on ``grid`` and the trace of the number of clusters."""
    x = np.asarray(x, float)
    n = len(x)
    mu0 = float(np.mean(x)) if mu0 is None else mu0
    b0 = float(np.var(x)) / 4 if b0 is None else b0
    z = np.zeros(n, int)
    stats_ = {0: [n, float(x.sum()), float((x ** 2).sum())]}
    grid = np.linspace(x.min() - 1, x.max() + 1, 200) if grid is None else np.asarray(grid)
    dens = np.zeros_like(grid)
    ks = []
    kept = 0
    for it in range(iters):
        for i in range(n):
            c = z[i]
            st = stats_[c]
            st[0] -= 1
            st[1] -= x[i]
            st[2] -= x[i] ** 2
            if st[0] == 0:
                del stats_[c]
            labels = list(stats_.keys())
            logp = [math.log(stats_[c2][0]) + _nig_logpred(x[i], *stats_[c2], mu0, k0, a0, b0) for c2 in labels]
            logp.append(math.log(alpha) + _nig_logpred(x[i], 0, 0.0, 0.0, mu0, k0, a0, b0))
            logp = np.asarray(logp)
            pr = np.exp(logp - logp.max())
            pr /= pr.sum()
            j = rng.choice(len(pr), p=pr)
            if j == len(labels):
                new = max(stats_.keys(), default=-1) + 1
                stats_[new] = [0, 0.0, 0.0]
                c2 = new
            else:
                c2 = labels[j]
            z[i] = c2
            stats_[c2][0] += 1
            stats_[c2][1] += x[i]
            stats_[c2][2] += x[i] ** 2
        ks.append(len(stats_))
        if it >= burn:
            f = alpha / (alpha + n) * np.exp(_nig_logpred(grid, 0, 0.0, 0.0, mu0, k0, a0, b0))
            for st in stats_.values():
                f = f + st[0] / (alpha + n) * np.exp(_nig_logpred(grid, *st, mu0, k0, a0, b0))
            dens += f
            kept += 1
    return {"grid": grid, "density": dens / max(kept, 1), "k_trace": np.asarray(ks)}


# --------------------------------------------------------------------------------------- sparse normal means


def spike_slab_posterior(y, tau: float = 2.0, a: float = 1.0, b=None, sigma: float = 1.0, ngrid: int = 400) -> dict:
    """y_i ~ N(theta_i, sigma^2), theta_i ~ w N(0, tau^2) + (1 - w) delta_0, w ~ Beta(a, b) (b = n by default:
    Castillo & van der Vaart's complexity prior). The posterior of w is integrated on a grid; returns the marginal
    inclusion probabilities, the posterior mean, and the posterior of w."""
    y = np.asarray(y, float)
    n = len(y)
    b = float(n) if b is None else b
    wg = (np.arange(ngrid) + 0.5) / ngrid
    l1 = stats.norm.logpdf(y, 0, math.sqrt(sigma ** 2 + tau ** 2))
    l0 = stats.norm.logpdf(y, 0, sigma)
    # log p(y | w) = sum log(w e^{l1} + (1 - w) e^{l0})
    L = np.array([np.sum(np.logaddexp(math.log(w) + l1, math.log(1 - w) + l0)) for w in wg])
    lp = L + stats.beta.logpdf(wg, a, b)
    pw = np.exp(lp - lp.max())
    pw /= pw.sum()
    incl = np.zeros(n)
    for w, q in zip(wg, pw):
        r1 = math.log(w) + l1
        r0 = math.log(1 - w) + l0
        incl += q * np.exp(r1 - np.logaddexp(r1, r0))
    shrink = tau ** 2 / (tau ** 2 + sigma ** 2)
    return {"incl": incl, "mean": incl * shrink * y, "w_grid": wg, "w_post": pw, "slab_var": shrink * sigma ** 2,
            "slab_mean": shrink * y}


def spike_slab_interval(incl: float, slab_mean: float, slab_var: float, level: float = 0.95) -> tuple:
    """The equal-tailed credible interval of the mixture (1 - incl) delta_0 + incl N(m, v)."""
    sd = math.sqrt(slab_var)

    def cdf(t):
        return (1 - incl) * (t >= 0) + incl * stats.norm.cdf(t, slab_mean, sd)

    def q(p):
        lo, hi = slab_mean - 12 * sd - 1, slab_mean + 12 * sd + 1
        for _ in range(80):
            mid = (lo + hi) / 2
            if cdf(mid) < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    return q(0.5 - level / 2), q(0.5 + level / 2)


def horseshoe_posterior(y: float, tau: float, sigma: float = 1.0, level: float = 0.95, nk: int = 400) -> dict:
    """theta | lambda ~ N(0, lambda^2 tau^2), lambda ~ C+(0, 1): the posterior of theta given y, a scale mixture of
    normals over lambda; returns its mean and an equal-tailed credible interval, by quadrature on log lambda."""
    u = np.linspace(-9, 9, nk)
    lam = np.exp(u)
    prior = 2 / (math.pi * (1 + lam ** 2)) * lam  # density of log lambda
    v = lam ** 2 * tau ** 2
    like = stats.norm.pdf(y, 0, np.sqrt(sigma ** 2 + v))
    wts = prior * like
    wts /= wts.sum()
    m = v / (v + sigma ** 2) * y
    s = np.sqrt(v * sigma ** 2 / (v + sigma ** 2))
    mean = float(np.sum(wts * m))

    def cdf(t):
        return float(np.sum(wts * stats.norm.cdf(t, m, s)))

    def q(p):
        lo, hi = -abs(y) - 20, abs(y) + 20
        for _ in range(70):
            mid = (lo + hi) / 2
            if cdf(mid) < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    return {"mean": mean, "lo": q(0.5 - level / 2), "hi": q(0.5 + level / 2)}


def special_beta_log(a, b):
    return special.betaln(a, b)
