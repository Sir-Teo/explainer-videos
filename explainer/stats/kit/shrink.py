"""statkit.shrink: borrowing strength (Part 25 of *Statistics, Built*).

    from explainer.stats.kit.shrink import james_stein, sure_js, eb_normal, tweedie, npmle, fay_herriot, meta

James-Stein and its positive part, Stein's unbiased risk estimate, normal-normal empirical Bayes (method of moments
and ML), Tweedie's formula with a log-spline or NPMLE prior, the Kiefer-Wolfowitz NPMLE on a grid by EM, the
Fay-Herriot small-area model, and random-effects meta-analysis (DerSimonian-Laird with Hartung-Knapp).  Checked in
``tests/test_stats_kit_shrink.py``.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats


def james_stein(x, sigma2: float = 1.0, target=None, positive: bool = True) -> dict:
    """James & Stein (1961) shrinkage of x ~ N_p(theta, sigma2 I) towards ``target`` (default: the grand mean, which
    costs one degree of freedom).  Returns the estimates and the shrinkage factor B."""
    x = np.asarray(x, float)
    p = len(x)
    if target is None:
        t, df = x.mean(), p - 3
    else:
        t, df = float(target), p - 2
    S = float(np.sum((x - t) ** 2))
    B = df * sigma2 / S
    if positive:
        B = min(B, 1.0)
    return {"theta": t + (1 - B) * (x - t), "B": B, "target": t, "S": S}


def sure_js(x, sigma2: float = 1.0) -> float:
    """Stein's unbiased risk estimate of James-Stein towards zero: p sigma2 - (p - 2)^2 sigma2^2 / |x|^2."""
    x = np.asarray(x, float)
    p = len(x)
    return float(p * sigma2 - (p - 2) ** 2 * sigma2 ** 2 / np.sum(x ** 2))


def js_risk_exact(theta, sigma2: float = 1.0, R: int = 20000, rng=None) -> dict:
    """Monte Carlo risk of the MLE, James-Stein to zero and its positive part at a given theta."""
    g = np.random.default_rng(0) if rng is None else rng
    theta = np.asarray(theta, float)
    p = len(theta)
    X = theta + np.sqrt(sigma2) * g.standard_normal((R, p))
    S = np.sum(X ** 2, 1)
    B = (p - 2) * sigma2 / S
    js = (1 - B)[:, None] * X
    jsp = np.clip(1 - B, 0, None)[:, None] * X
    return {"mle": float(np.mean(np.sum((X - theta) ** 2, 1))), "js": float(np.mean(np.sum((js - theta) ** 2, 1))),
            "js_plus": float(np.mean(np.sum((jsp - theta) ** 2, 1)))}


def eb_normal(x, s2, method: str = "reml") -> dict:
    """Normal-normal empirical Bayes with unequal known variances: x_i ~ N(theta_i, s2_i), theta_i ~ N(mu, tau2).
    tau2 by ML, REML or moments; the posterior means mu + (1 - B_i)(x_i - mu), B_i = s2_i/(s2_i + tau2)."""
    x, s2 = np.asarray(x, float), np.broadcast_to(np.asarray(s2, float), np.shape(x)).astype(float)

    def mu_of(t2):
        w = 1 / (s2 + t2)
        return float(np.sum(w * x) / np.sum(w))

    def nll(t2):
        v = s2 + t2
        m = mu_of(t2)
        out = 0.5 * np.sum(np.log(v) + (x - m) ** 2 / v)
        if method == "reml":
            out += 0.5 * np.log(np.sum(1 / v))
        return out

    if method == "mom":
        m0 = x.mean()
        t2 = max(float(np.var(x, ddof=1) - np.mean(s2)), 0.0)
    else:
        hi = max(10 * np.var(x), 1e-6)
        r = optimize.minimize_scalar(nll, bounds=(0.0, hi), method="bounded", options={"xatol": 1e-12})
        t2 = float(r.x) if nll(r.x) < nll(0.0) else 0.0
    m = mu_of(t2)
    B = s2 / (s2 + t2)
    return {"tau2": t2, "mu": m, "B": B, "theta": m + (1 - B) * (x - m), "post_sd": np.sqrt(s2 * (1 - B))}


def npmle(x, sigma: float = 1.0, grid=None, iters: int = 3000, tol: float = 1e-10) -> dict:
    """The Kiefer-Wolfowitz (1956) nonparametric MLE of the prior g in x_i ~ N(theta_i, sigma^2), theta_i ~ g, on a
    fixed grid, by EM (the mixing weights' fixed-point update).  The fitted g is discrete, usually with few atoms."""
    x = np.asarray(x, float)
    grid = np.linspace(x.min(), x.max(), 300) if grid is None else np.asarray(grid, float)
    L = stats.norm.pdf(x[:, None], grid[None, :], sigma)
    w = np.full(len(grid), 1 / len(grid))
    ll_old = -np.inf
    for _ in range(iters):
        f = L @ w
        w = w * (L / f[:, None]).mean(0)
        ll = float(np.sum(np.log(L @ w)))
        if ll - ll_old < tol:
            break
        ll_old = ll
    f = L @ w
    post_mean = (L * w[None, :]) @ grid / f
    return {"grid": grid, "w": w, "loglik": ll, "post_mean": post_mean, "marginal": f}


def tweedie(x, sigma: float, marginal_logdens_grad) -> np.ndarray:
    """Tweedie's formula (Robbins 1956; Efron 2011): E(theta | x) = x + sigma^2 d/dx log f(x), f the marginal."""
    return np.asarray(x, float) + sigma ** 2 * marginal_logdens_grad(np.asarray(x, float))


def fay_herriot(y, D, X) -> dict:
    """Fay & Herriot (1979): direct estimates y_i ~ N(theta_i, D_i), theta_i = x_i'beta + v_i, v_i ~ N(0, A).  A by
    REML; EBLUP theta_i = gamma_i y_i + (1 - gamma_i) x_i'beta, gamma_i = A/(A + D_i)."""
    y, D, X = np.asarray(y, float), np.asarray(D, float), np.asarray(X, float)

    def beta_of(A):
        w = 1 / (A + D)
        Xw = X * w[:, None]
        return np.linalg.solve(X.T @ Xw, Xw.T @ y)

    def nll(A):
        v = A + D
        b = beta_of(A)
        r = y - X @ b
        Xw = X / v[:, None]
        return 0.5 * (np.sum(np.log(v)) + np.sum(r ** 2 / v) + np.linalg.slogdet(X.T @ Xw)[1])

    r = optimize.minimize_scalar(nll, bounds=(0.0, 10 * np.var(y)), method="bounded", options={"xatol": 1e-12})
    A = float(r.x) if nll(r.x) < nll(0.0) else 0.0
    b = beta_of(A)
    g = A / (A + D)
    return {"A": A, "beta": b, "gamma": g, "eblup": g * y + (1 - g) * (X @ b), "synthetic": X @ b}


def meta(y, v, alpha: float = 0.05) -> dict:
    """Random-effects meta-analysis: DerSimonian & Laird (1986) tau^2 by moments, the inverse-variance pooled
    estimate with its usual z interval, and the Hartung & Knapp (2001) t interval; I^2 (Higgins & Thompson 2002)."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    w = 1 / v
    mu_fe = float(np.sum(w * y) / np.sum(w))
    Q = float(np.sum(w * (y - mu_fe) ** 2))
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (k - 1)) / c)
    ws = 1 / (v + tau2)
    mu = float(np.sum(ws * y) / np.sum(ws))
    se = float(np.sqrt(1 / np.sum(ws)))
    z = stats.norm.ppf(1 - alpha / 2)
    q_hk = float(np.sum(ws * (y - mu) ** 2) / (k - 1))
    se_hk = float(np.sqrt(q_hk / np.sum(ws)))
    t = stats.t.ppf(1 - alpha / 2, k - 1)
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    return {"mu": mu, "se": se, "tau2": tau2, "Q": Q, "I2": I2, "ci_dl": (mu - z * se, mu + z * se),
            "se_hk": se_hk, "ci_hk": (mu - t * se_hk, mu + t * se_hk), "mu_fe": mu_fe, "se_fe": float(np.sqrt(1 / np.sum(w)))}
