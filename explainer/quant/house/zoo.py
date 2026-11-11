"""The House's tools for the factor zoo (Part 25): hundreds of candidate factors, and how to keep the true ones.

* Hurdles: the expected best t-statistic among pure noise (:func:`noise_max_t`), Bonferroni's hurdle as the number of
  tests grows (:func:`bonferroni_t`); the step-down and false-discovery procedures live in ``econ``.
* Publication bias: empirical-Bayes shrinkage of a cross-section of t-statistics (:func:`eb_shrink`).
* The shrinkage SDF of Kozak, Nagel and Santosh (2020): ridge on the factors' means and covariance
  (:func:`kns_b`), its cross-validated R^2 (:func:`kns_cv`), and its portfolio (``F @ b``).
* Latent factors: PCA and risk-premium PCA (Lettau and Pelger 2020) (:func:`pca`, :func:`rp_pca`).
* Selection: a coordinate-descent lasso (:func:`lasso`) and Feng, Giglio and Xiu's (2020) double-selection test of a
  new factor against the zoo (:func:`double_selection`).
* Model comparison: the maximum squared Sharpe ratio of a set of factors (:func:`max_sh2`), the quantity Barillas and
  Shanken (2018) rank models by.

Returns are monthly; ``F`` is T x K (factors or long-short portfolios, excess returns).
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def tstat(x) -> float:
    """The t-statistic of a mean, sqrt(T) mean / sd."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x)))


def noise_max_t(n: int, T: int = 240, sims: int = 4000, seed: int = 0, absolute: bool = False) -> dict:
    """The best t-statistic among ``n`` independent strategies with no true premium, each with ``T`` months:
    simulated mean and 5th/95th percentiles. With independent strategies it is the maximum of n draws from (nearly)
    a standard normal: about sqrt(2 ln n)."""
    rng = np.random.default_rng(seed)
    m = np.empty(sims)
    for s in range(sims):
        z = rng.standard_t(T - 1, n)
        m[s] = np.max(np.abs(z)) if absolute else np.max(z)
    return {"mean": float(m.mean()), "p5": float(np.percentile(m, 5)), "p95": float(np.percentile(m, 95)),
            "approx": float(np.sqrt(2 * np.log(n)))}


def bonferroni_t(M, alpha: float = 0.05) -> np.ndarray:
    """The two-sided t hurdle that keeps the chance of any false discovery among ``M`` tests below ``alpha``."""
    M = np.asarray(M, float)
    return stats.norm.ppf(1 - alpha / (2 * M))


def eb_shrink(t) -> dict:
    """Empirical Bayes for a cross-section of t-statistics: t_i = theta_i + e_i, e_i ~ N(0, 1), theta_i ~ N(m, v).
    The method of moments gives v = var(t) - 1; each posterior mean is m + v/(v + 1) (t_i - m). Returns the shrink
    factor v/(v + 1), the prior mean and variance, and the shrunk t's. (Ignores the selection at t = 2 that
    publication adds; Chen and Zimmermann (2020) model it and find it small.)"""
    t = np.asarray(t, float)
    m, v = float(t.mean()), float(max(t.var(ddof=1) - 1, 1e-9))
    k = v / (v + 1)
    return {"shrink": k, "m": m, "v": v, "post": m + k * (t - m)}


def kns_b(mu, S, gamma: float) -> np.ndarray:
    """Kozak, Nagel and Santosh's L2 shrinkage SDF: b = (S + gamma I)^-1 mu. gamma = 0 is the unpenalised tangency
    (Part 23's Hansen-Jagannathan weights); larger gamma shrinks the loadings of low-variance directions most, which
    is where estimated means are least reliable relative to their risk."""
    S = np.asarray(S, float)
    return np.linalg.solve(S + gamma * np.eye(len(S)), np.asarray(mu, float))


def kns_kappa_gamma(S, T: int, kappa: float) -> float:
    """KNS's parameterisation: a prior root-expected squared Sharpe ratio ``kappa`` (annualised in their paper; here
    per period, as the data) maps to gamma = tr(S) / (T kappa^2)."""
    return float(np.trace(np.asarray(S, float)) / (T * kappa ** 2))


def _r2(mu_te, S_te, b) -> float:
    e = mu_te - S_te @ b
    return float(1 - (e @ e) / (mu_te @ mu_te))


def kns_cv(F, gammas, folds: int = 3) -> dict:
    """Cross-validate the shrinkage: contiguous blocks, fit b on the other blocks, score the held block by the
    cross-sectional R^2 of its mean returns explained by its covariance with the SDF: 1 - |mu - S b|^2 / |mu|^2.
    Returns the mean out-of-block R^2 for each gamma, and the best gamma."""
    F = np.asarray(F, float)
    T = len(F)
    edges = np.linspace(0, T, folds + 1).astype(int)
    out = np.zeros((folds, len(gammas)))
    for k in range(folds):
        te = np.zeros(T, bool)
        te[edges[k]:edges[k + 1]] = True
        mu_tr, S_tr = F[~te].mean(0), np.cov(F[~te].T)
        mu_te, S_te = F[te].mean(0), np.cov(F[te].T)
        for j, g in enumerate(gammas):
            out[k, j] = _r2(mu_te, S_te, kns_b(mu_tr, S_tr, g))
    r2 = out.mean(0)
    return {"r2": r2, "best": float(np.asarray(gammas)[int(np.argmax(r2))]), "folds": out}


def pca(F) -> dict:
    """Principal components of the covariance: eigenvalues (descending), their shares, and eigenvectors (columns)."""
    S = np.cov(np.asarray(F, float).T)
    w, V = np.linalg.eigh(S)
    i = np.argsort(w)[::-1]
    return {"eig": w[i], "share": w[i] / w[i].sum(), "V": V[:, i]}


def rp_pca(F, gamma: float = 10.0) -> dict:
    """Lettau and Pelger (2020): risk-premium PCA. Eigenvectors of the second moment plus gamma times the outer
    product of the means, (1/T) F'F + gamma mu mu', so the components explain both co-movement (as PCA does) and
    average returns. gamma = -1 is ordinary PCA of the covariance."""
    F = np.asarray(F, float)
    mu = F.mean(0)
    M = F.T @ F / len(F) + gamma * np.outer(mu, mu)
    w, V = np.linalg.eigh(M)
    i = np.argsort(w)[::-1]
    return {"eig": w[i], "V": V[:, i]}


def max_sh2(F) -> float:
    """The largest squared Sharpe ratio (per period) attainable from the factors F: mu' S^-1 mu."""
    F = np.asarray(F, float)
    if F.ndim == 1:
        F = F[:, None]
    mu = F.mean(0)
    return float(mu @ np.linalg.solve(np.atleast_2d(np.cov(F.T)), mu))


def lasso(X, y, lam: float, iters: int = 500, tol: float = 1e-8) -> np.ndarray:
    """Coordinate-descent lasso without intercept on standardised columns: minimise (1/2n)|y - Xb|^2 + lam |b|_1.
    Returns coefficients on the original scale of X."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, p = X.shape
    sd = X.std(0)
    sd[sd == 0] = 1
    Z = X / sd
    b = np.zeros(p)
    r = y.copy()
    zz = (Z ** 2).sum(0) / n
    for _ in range(iters):
        bmax = 0.0
        for j in range(p):
            old = b[j]
            rho = Z[:, j] @ r / n + zz[j] * old
            new = np.sign(rho) * max(abs(rho) - lam, 0) / zz[j]
            if new != old:
                r -= Z[:, j] * (new - old)
                b[j] = new
                bmax = max(bmax, abs(new - old))
        if bmax < tol:
            break
    return b / sd


def double_selection(R, g, H, lam1: float, lam2: float) -> dict:
    """Feng, Giglio and Xiu (2020): does factor ``g`` add to an SDF that may load on any of the zoo ``H``? Across test
    assets R (T x N): stage 1, lasso the assets' mean returns on their covariances with H; stage 2, lasso their
    covariances with g on those with H; stage 3, regress mean returns on cov(R, g) and the union of selected
    cov(R, h). The coefficient on cov(R, g) is g's SDF loading lambda_g, with a heteroskedasticity-robust t across
    assets (a simplification of their standard error)."""
    R, g, H = np.asarray(R, float), np.asarray(g, float), np.asarray(H, float)
    T, N = R.shape
    Rc = R - R.mean(0)
    Cg = Rc.T @ (g - g.mean()) / (T - 1)
    CH = Rc.T @ (H - H.mean(0)) / (T - 1)
    mu = R.mean(0)
    s1 = np.flatnonzero(lasso(CH, mu, lam1))
    s2 = np.flatnonzero(lasso(CH, Cg, lam2))
    sel = sorted(set(s1) | set(s2))
    X = np.c_[np.ones(N), Cg, CH[:, sel]] if sel else np.c_[np.ones(N), Cg]
    coef, *_ = np.linalg.lstsq(X, mu, rcond=None)
    e = mu - X @ coef
    XtX = np.linalg.inv(X.T @ X)
    V = XtX @ (X.T * e ** 2) @ X @ XtX
    return {"lambda_g": float(coef[1]), "t": float(coef[1] / np.sqrt(V[1, 1])), "selected": sel,
            "n1": int(len(s1)), "n2": int(len(s2))}
