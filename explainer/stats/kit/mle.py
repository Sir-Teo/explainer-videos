"""statkit.mle: the theory of maximum likelihood, made computable, for Part 22 of *Statistics, Built* ("Likelihood in
Depth").

Two-component normal mixtures fitted by EM (Dempster, Laird & Rubin 1977), with the log likelihood recorded at every
step and the rate of convergence (the fraction of missing information); Pearson's (1894) method of moments for the same
mixture, solved numerically; the Wald, score and likelihood-ratio statistics for a binomial and for a logistic slope;
profile likelihoods; the Neyman-Scott problem; the sandwich variance for a misspecified Poisson regression and the
quasi-Poisson dispersion; Besag's (1975) pseudo-likelihood for an Ising lattice, with a Gibbs sampler to make one; the
Cauchy location MLE; and a numerical Hessian.  Checked in ``tests/test_stats_kit_mle.py``.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------------------------------------------------------------
# Numerical derivatives
# ---------------------------------------------------------------------------------------------------------------------
def numerical_hessian(f, theta, h: float = 1e-4) -> np.ndarray:
    """Central-difference Hessian of a scalar function (step h scaled to each coordinate's size)."""
    theta = np.asarray(theta, float)
    p = len(theta)
    H = np.empty((p, p))
    hs = h * np.maximum(1.0, np.abs(theta))
    for i in range(p):
        for j in range(i, p):
            e_i, e_j = np.zeros(p), np.zeros(p)
            e_i[i], e_j[j] = hs[i], hs[j]
            v = (f(theta + e_i + e_j) - f(theta + e_i - e_j) - f(theta - e_i + e_j) + f(theta - e_i - e_j)) / (4 * hs[i] * hs[j])
            H[i, j] = H[j, i] = v
    return H


# ---------------------------------------------------------------------------------------------------------------------
# Two-component normal mixtures: EM and Pearson's moments
# ---------------------------------------------------------------------------------------------------------------------
def mix_loglik(x, theta, w=None) -> float:
    """Log likelihood of p N(mu1, s1^2) + (1 - p) N(mu2, s2^2); theta = (p, mu1, s1, mu2, s2); w = counts."""
    x = np.asarray(x, float)
    w = np.ones(len(x)) if w is None else np.asarray(w, float)
    p, m1, s1, m2, s2 = theta
    if not (0 < p < 1 and s1 > 0 and s2 > 0):
        return -np.inf
    d = p * stats.norm.pdf(x, m1, s1) + (1 - p) * stats.norm.pdf(x, m2, s2)
    return float(np.sum(w * np.log(np.maximum(d, 1e-300))))


def em_mixture(x, theta0, w=None, iters: int = 500, tol: float = 1e-12) -> dict:
    """EM for a two-component normal mixture (counts ``w`` allowed).  E-step: each point's posterior probability of
    component 1; M-step: weighted proportion, means and SDs.  Returns the parameter path and log likelihoods, which
    never decrease."""
    x = np.asarray(x, float)
    w = np.ones(len(x)) if w is None else np.asarray(w, float)
    th = np.asarray(theta0, float).copy()
    path, ll = [th.copy()], [mix_loglik(x, th, w)]
    for _ in range(iters):
        p, m1, s1, m2, s2 = th
        a = p * stats.norm.pdf(x, m1, s1)
        b = (1 - p) * stats.norm.pdf(x, m2, s2)
        r = a / (a + b)
        w1, w2 = w * r, w * (1 - r)
        n1, n2 = w1.sum(), w2.sum()
        m1, m2 = (w1 @ x) / n1, (w2 @ x) / n2
        s1, s2 = np.sqrt((w1 @ (x - m1) ** 2) / n1), np.sqrt((w2 @ (x - m2) ** 2) / n2)
        th = np.array([n1 / (n1 + n2), m1, s1, m2, s2])
        path.append(th.copy())
        ll.append(mix_loglik(x, th, w))
        if abs(ll[-1] - ll[-2]) < tol:
            break
    P = np.array(path)
    # the EM rate: successive step lengths shrink by the largest fraction of missing information
    steps = np.linalg.norm(np.diff(P, axis=0), axis=1)
    k = max(2, len(steps) // 3)
    rate = float(np.median(steps[k:-1] / steps[k - 1:-2])) if len(steps) > 6 else np.nan
    return {"theta": th, "path": P, "loglik": np.array(ll), "resp": r, "rate": rate}


def mix_moments(theta, k_max: int = 6) -> np.ndarray:
    """The mean and the central moments 2..k_max of a two-component normal mixture."""
    p, m1, s1, m2, s2 = theta
    mean = p * m1 + (1 - p) * m2
    out = [mean]
    for k in range(2, k_max + 1):
        tot = 0.0
        for q, m, s in ((p, m1, s1), (1 - p, m2, s2)):
            d = m - mean
            # E[(Y - mean)^k] for Y ~ N(m, s^2): sum_j C(k, j) d^(k-j) E[Z^j] s^j, E[Z^j] = (j-1)!! for even j
            e = sum(_comb(k, j) * d ** (k - j) * (s ** j) * _dfact(j - 1) for j in range(0, k + 1, 2))
            tot += q * e
        out.append(tot)
    return np.array(out)


def _comb(n, k):
    from math import comb
    return comb(n, k)


def _dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def pearson_moments(x, w=None, starts: int = 400, seed: int = 1894) -> dict:
    """Pearson's (1894) method: match the mean and central moments 2-5 of a two-component normal mixture.  Pearson
    reduced this to a ninth-degree polynomial; here the five equations are solved numerically from many starts and the
    distinct solutions kept.  Each solution's sixth moment is compared with the data's, Pearson's tie-breaker."""
    x = np.asarray(x, float)
    w = np.ones(len(x)) if w is None else np.asarray(w, float)
    mean = (w @ x) / w.sum()
    target = np.array([mean] + [(w @ (x - mean) ** k) / w.sum() for k in range(2, 7)])
    sd = np.sqrt(target[1])
    scale = np.array([sd] + [sd ** k for k in range(2, 7)])
    g = np.random.default_rng(seed)
    sols = []
    for _ in range(starts):
        th0 = [g.uniform(0.05, 0.95), mean + sd * g.normal(), sd * g.uniform(0.2, 1.2), mean + sd * g.normal(), sd * g.uniform(0.2, 1.2)]
        fun = lambda th: (mix_moments(th)[:5] - target[:5]) / scale[:5]  # noqa: E731
        try:
            r = optimize.least_squares(fun, th0, bounds=([1e-3, -np.inf, 1e-6, -np.inf, 1e-6], [1 - 1e-3, np.inf, np.inf, np.inf, np.inf]))
        except Exception:
            continue
        if r.cost < 1e-16:
            th = r.x
            if th[1] > th[3]:  # label the components so that component 1 has the smaller mean
                th = np.array([1 - th[0], th[3], th[4], th[1], th[2]])
            if not any(np.allclose(th, s_, rtol=1e-4, atol=1e-7) for s_ in sols):
                sols.append(th)
    six = [float(mix_moments(s_)[5]) for s_ in sols]
    return {"solutions": sols, "sixth": six, "sixth_data": float(target[5]), "target": target}


# ---------------------------------------------------------------------------------------------------------------------
# The trinity
# ---------------------------------------------------------------------------------------------------------------------
def binomial_trinity(x: int, n: int, p0: float) -> dict:
    """Wald, score and likelihood-ratio statistics for H0: p = p0 with x successes in n trials (each ~ chi^2_1)."""
    ph = x / n
    ll = lambda p: x * np.log(p) + (n - x) * np.log(1 - p)  # noqa: E731
    wald = (ph - p0) ** 2 / (ph * (1 - ph) / n)
    score = (ph - p0) ** 2 / (p0 * (1 - p0) / n)
    lr = 2 * (ll(ph) - ll(p0))
    return {"wald": float(wald), "score": float(score), "lr": float(lr), "phat": ph,
            "p": {k: float(stats.chi2.sf(v, 1)) for k, v in (("wald", wald), ("score", score), ("lr", lr))}}


def logistic_slope_tests(x, y) -> dict:
    """For logistic regression of y on x (with intercept): the MLE, its Wald z for slope = 0, and the LR statistic."""
    X = np.column_stack([np.ones(len(x)), x])
    b = np.zeros(2)
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        Wd = p * (1 - p)
        step = np.linalg.solve(X.T @ (Wd[:, None] * X) + 1e-12 * np.eye(2), X.T @ (y - p))
        b = b + step
        if np.linalg.norm(step) < 1e-10:
            break
    p = 1 / (1 + np.exp(-X @ b))
    info = X.T @ ((p * (1 - p))[:, None] * X)
    se = float(np.sqrt(np.linalg.inv(info)[1, 1]))
    ll1 = float(np.sum(y * (X @ b) - np.logaddexp(0, X @ b)))
    p0 = y.mean()
    ll0 = float(np.sum(y * np.log(p0) + (1 - y) * np.log(1 - p0)))
    return {"b": b, "se": se, "z": float(b[1] / se), "lr": 2 * (ll1 - ll0), "ll": ll1}


def logistic_profile_ci(x, y, level: float = 0.95, grid=None) -> tuple:
    """The likelihood-ratio (profile) interval for a logistic slope: slopes whose profile log likelihood is within
    chi^2_1(level)/2 of the maximum."""
    X1 = np.ones((len(x), 1))
    fit = logistic_slope_tests(x, y)
    cut = fit["ll"] - stats.chi2.ppf(level, 1) / 2

    def prof(b1):
        a = fit["b"][0]
        for _ in range(60):
            eta = a + b1 * x
            p = 1 / (1 + np.exp(-eta))
            g = np.sum(y - p)
            h = np.sum(p * (1 - p))
            a += g / max(h, 1e-12)
            if abs(g) < 1e-10:
                break
        eta = a + b1 * x
        return float(np.sum(y * eta - np.logaddexp(0, eta)))

    b1 = fit["b"][1]
    s = fit["se"]
    lo = optimize.brentq(lambda t: prof(t) - cut, b1 - 50 * s, b1) if prof(b1 - 50 * s) < cut else -np.inf
    hi = optimize.brentq(lambda t: prof(t) - cut, b1, b1 + 50 * s) if prof(b1 + 50 * s) < cut else np.inf
    return lo, hi


# ---------------------------------------------------------------------------------------------------------------------
# Profiles, Neyman-Scott, sandwiches
# ---------------------------------------------------------------------------------------------------------------------
def gamma_loglik(x, a, b) -> float:
    """Gamma log likelihood, shape a and rate b."""
    x = np.asarray(x, float)
    n = len(x)
    from scipy.special import gammaln
    return float(n * a * np.log(b) - n * gammaln(a) + (a - 1) * np.sum(np.log(x)) - b * np.sum(x))


def gamma_profile(x, shapes) -> dict:
    """The profile log likelihood of a gamma shape: for each shape a the best rate is a / mean(x)."""
    x = np.asarray(x, float)
    m = x.mean()
    prof = np.array([gamma_loglik(x, a, a / m) for a in shapes])
    i = int(np.argmax(prof))
    return {"shapes": np.asarray(shapes), "profile": prof, "a_hat": float(shapes[i]), "rate_hat": float(shapes[i] / m)}


def neyman_scott(n_pairs: int, sigma: float, rng: np.random.Generator) -> dict:
    """Pairs x_i1, x_i2 ~ N(mu_i, sigma^2) with a new mu_i for every pair: the MLE of sigma^2 is
    sum (x_i1 - x_i2)^2 / (4n), which tends to sigma^2 / 2; the unbiased fix divides by 2n."""
    mu = rng.normal(0, 5, n_pairs)
    x1 = mu + sigma * rng.normal(size=n_pairs)
    x2 = mu + sigma * rng.normal(size=n_pairs)
    d2 = (x1 - x2) ** 2
    return {"mle": float(d2.sum() / (4 * n_pairs)), "fixed": float(d2.sum() / (2 * n_pairs))}


def poisson_regression(X, y, iters: int = 50) -> dict:
    """Poisson regression by IRLS, with the model-based and the sandwich (robust) variances and the Pearson dispersion
    estimate used by quasi-Poisson."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1])
    b[0] = np.log(max(y.mean(), 1e-8))
    for _ in range(iters):
        mu = np.exp(X @ b)
        step = np.linalg.solve(X.T @ (mu[:, None] * X), X.T @ (y - mu))
        b = b + step
        if np.linalg.norm(step) < 1e-12:
            break
    mu = np.exp(X @ b)
    A = X.T @ (mu[:, None] * X)
    Ai = np.linalg.inv(A)
    U = X * (y - mu)[:, None]
    sand = Ai @ (U.T @ U) @ Ai
    phi = float(np.sum((y - mu) ** 2 / mu) / (len(y) - X.shape[1]))
    return {"b": b, "se_model": np.sqrt(np.diag(Ai)), "se_sandwich": np.sqrt(np.diag(sand)), "phi": phi,
            "se_quasi": np.sqrt(np.diag(Ai) * phi)}


def cauchy_mle(x) -> float:
    """The Cauchy location MLE: Newton from the median, with a safeguarded line search."""
    x = np.asarray(x, float)
    t = float(np.median(x))
    f = lambda t: -np.sum(np.log1p((x - t) ** 2))  # noqa: E731
    for _ in range(100):
        u = x - t
        g = np.sum(2 * u / (1 + u ** 2))
        h = np.sum(2 * (u ** 2 - 1) / (1 + u ** 2) ** 2)
        step = -g / h if h < 0 else g
        s = 1.0
        while f(t + s * step) < f(t) - 1e-12 and s > 1e-8:
            s /= 2
        t += s * step
        if abs(s * step) < 1e-12:
            break
    return t


def cauchy_observed_info(x, t) -> float:
    u = np.asarray(x, float) - t
    return float(np.sum(2 * (1 - u ** 2) / (1 + u ** 2) ** 2))


# ---------------------------------------------------------------------------------------------------------------------
# Pseudo-likelihood for an Ising lattice (Besag 1975)
# ---------------------------------------------------------------------------------------------------------------------
def ising_gibbs(L: int, beta: float, sweeps: int, rng: np.random.Generator) -> np.ndarray:
    """A sample of +-1 spins on an L x L torus with P(x) proportional to exp(beta sum_<ij> x_i x_j), by Gibbs
    sweeps in a checkerboard order."""
    x = rng.choice([-1, 1], size=(L, L))
    ii, jj = np.indices((L, L))
    for _ in range(sweeps):
        for parity in (0, 1):
            m = (ii + jj) % 2 == parity
            s = np.roll(x, 1, 0) + np.roll(x, -1, 0) + np.roll(x, 1, 1) + np.roll(x, -1, 1)
            p = 1 / (1 + np.exp(-2 * beta * s))
            new = np.where(rng.random((L, L)) < p, 1, -1)
            x = np.where(m, new, x)
    return x


def ising_pseudo_mle(x) -> dict:
    """Besag's pseudo-likelihood: maximize prod_i P(x_i | neighbours) = prod_i 1 / (1 + exp(-2 beta x_i s_i)), a
    logistic regression of each spin on its neighbour sum without intercept.  Newton in one dimension."""
    s = np.roll(x, 1, 0) + np.roll(x, -1, 0) + np.roll(x, 1, 1) + np.roll(x, -1, 1)
    z = (2 * x * s).ravel().astype(float)
    b = 0.0
    for _ in range(100):
        p = 1 / (1 + np.exp(-b * z))  # P(observed spin | neighbours)
        g = np.sum(z * (1 - p))
        h = -np.sum(z * z * p * (1 - p))
        step = -g / h
        b += step
        if abs(step) < 1e-12:
            break
    pl = float(np.sum(-np.logaddexp(0, -b * z)))
    return {"beta": float(b), "logpl": pl}
