"""The House's statistics module (Part 6, *Financial Econometrics*): how not to fool yourself with financial data.

Plain numpy, so every formula is visible and tested:

* :func:`ols` with naive, Newey–West (1987), Hansen–Hodrick (1980) and clustered (one- and two-way, Cameron, Gelbach
  and Miller 2011) standard errors;
* :func:`fama_macbeth`: the time series of cross-sectional slopes (1973);
* :func:`moving_block_bootstrap`, :func:`stationary_bootstrap` (Politis and Romano 1994) for dependent data;
* :func:`sharpe_se` (Lo 2002, Mertens 2002) and :func:`years_to_significance`;
* :func:`bonferroni`, :func:`holm`, :func:`benjamini_hochberg`: family-wise and false-discovery control;
* :func:`stambaugh_bias` and :func:`simulate_predictive`: the bias of predictive regressions (Stambaugh 1999);
* :func:`gmm`: two-step GMM with a HAC weighting matrix and Hansen's J test (1982);
* :func:`dml_plr`: double/debiased machine learning for a partially linear model (Chernozhukov et al. 2018), with
  cross-fitting and a ridge learner on spline features;
* :func:`shrink_means`: empirical-Bayes (James–Stein) shrinkage of many means toward their grand mean.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------------------
def _design(X, const=True):
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    return np.column_stack([np.ones(len(X)), X]) if const else X


def ols(y, X, const=True, se="naive", lags=0, groups=None, groups2=None) -> dict:
    """Least squares of ``y`` on ``X`` (a constant prepended by default).  ``se``: 'naive' (iid), 'white'
    (heteroskedasticity-robust), 'nw' (Newey-West with ``lags`` and Bartlett weights), 'hh' (Hansen-Hodrick: ``lags``
    equal weights, for overlapping horizons; falls back to Newey-West if not positive definite), 'cluster' (by
    ``groups``) or 'cluster2' (two-way, by ``groups`` and ``groups2``).  Returns beta, se, t, resid, r2, n."""
    y = np.asarray(y, float)
    Xd = _design(X, const)
    m = np.isfinite(y) & np.all(np.isfinite(Xd), axis=1)
    y, Xd = y[m], Xd[m]
    n, k = Xd.shape
    XtX_inv = np.linalg.inv(Xd.T @ Xd)
    beta = XtX_inv @ Xd.T @ y
    u = y - Xd @ beta
    if se == "naive":
        V = XtX_inv * (u @ u) / (n - k)
    else:
        if se in ("white", "nw", "hh"):
            S = _hac_meat(Xd, u, lags if se != "white" else 0, kernel="bartlett" if se != "hh" else "uniform")
            if se == "hh" and np.any(np.linalg.eigvalsh(S) <= 0):
                S = _hac_meat(Xd, u, lags, kernel="bartlett")
        elif se == "cluster":
            S = _cluster_meat(Xd, u, np.asarray(groups)[m])
        elif se == "cluster2":
            g1, g2 = np.asarray(groups)[m], np.asarray(groups2)[m]
            inter = np.array([f"{a}|{b}" for a, b in zip(g1, g2)])
            S = _cluster_meat(Xd, u, g1) + _cluster_meat(Xd, u, g2) - _cluster_meat(Xd, u, inter)
        else:
            raise ValueError(se)
        V = XtX_inv @ S @ XtX_inv
    sev = np.sqrt(np.maximum(np.diag(V), 0))
    r2 = 1 - (u @ u) / np.sum((y - y.mean()) ** 2)
    return {"beta": beta, "se": sev, "t": beta / sev, "resid": u, "r2": float(r2), "n": int(n), "V": V}


def _hac_meat(X, u, lags, kernel="bartlett"):
    Xu = X * u[:, None]
    S = Xu.T @ Xu
    for l_ in range(1, lags + 1):
        w = 1 - l_ / (lags + 1) if kernel == "bartlett" else 1.0
        G = Xu[l_:].T @ Xu[:-l_]
        S += w * (G + G.T)
    return S


def _cluster_meat(X, u, g):
    S = np.zeros((X.shape[1], X.shape[1]))
    for c in np.unique(g):
        s = (X[g == c] * u[g == c][:, None]).sum(axis=0)
        S += np.outer(s, s)
    return S


def fama_macbeth(Y, X, nw_lags=0) -> dict:
    """``Y``: periods x assets; ``X``: periods x assets x characteristics (or periods x assets).  Each period, regress
    the cross-section of returns on the characteristics; report the mean slope and its standard error from the time
    series of slopes (with Newey-West ``nw_lags`` if given)."""
    Y = np.asarray(Y, float)
    X = np.asarray(X, float)
    if X.ndim == 2:
        X = X[:, :, None]
    slopes = []
    for t in range(Y.shape[0]):
        m = np.isfinite(Y[t]) & np.all(np.isfinite(X[t]), axis=1)
        if m.sum() <= X.shape[2] + 2:
            continue
        slopes.append(ols(Y[t][m], X[t][m])["beta"])
    G = np.array(slopes)
    T = len(G)
    mean = G.mean(axis=0)
    if nw_lags:
        se = np.array([ols(G[:, j], np.zeros((T, 0)), const=True, se="nw", lags=nw_lags)["se"][0] for j in range(G.shape[1])])
    else:
        se = G.std(axis=0, ddof=1) / np.sqrt(T)
    return {"beta": mean, "se": se, "t": mean / se, "slopes": G, "T": T}


# ---------------------------------------------------------------------------
def moving_block_bootstrap(x, stat, block=12, B=2000, seed=0) -> np.ndarray:
    """``stat`` evaluated on B resamples of ``x`` built from overlapping blocks of length ``block``."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    n = len(x)
    nb = int(np.ceil(n / block))
    out = np.empty(B)
    for b in range(B):
        starts = rng.integers(0, n - block + 1, nb)
        idx = (starts[:, None] + np.arange(block)).ravel()[:n]
        out[b] = stat(x[idx])
    return out


def stationary_bootstrap(x, stat, mean_block=12, B=2000, seed=0) -> np.ndarray:
    """Politis and Romano (1994): blocks of geometric length (mean ``mean_block``) wrapping around the sample, so the
    resampled series is stationary."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    n = len(x)
    p = 1 / mean_block
    out = np.empty(B)
    for b in range(B):
        idx = np.empty(n, int)
        i = rng.integers(n)
        for k in range(n):
            idx[k] = i
            i = rng.integers(n) if rng.random() < p else (i + 1) % n
        out[b] = stat(x[idx])
    return out


# ---------------------------------------------------------------------------
def sharpe_se(sr: float, n: int, skew: float = 0.0, kurt: float = 3.0) -> float:
    """Standard error of an estimated Sharpe ratio (per period) from ``n`` iid returns: sqrt((1 + sr^2/2) / n) for
    Gaussian returns (Lo 2002); with skewness and kurtosis, sqrt((1 - skew sr + (kurt - 1)/4 sr^2) / n) (Mertens 2002)."""
    return float(np.sqrt((1 - skew * sr + (kurt - 1) / 4 * sr ** 2) / n))


def years_to_significance(sr_annual: float, t: float = 2.0) -> float:
    """Years of data before a true annual Sharpe ratio ``sr_annual`` has an expected t-statistic of ``t`` (t = SR sqrt(T))."""
    return float((t / sr_annual) ** 2)


# ---------------------------------------------------------------------------
def bonferroni(p, alpha=0.05) -> np.ndarray:
    p = np.asarray(p, float)
    return p <= alpha / len(p)


def holm(p, alpha=0.05) -> np.ndarray:
    p = np.asarray(p, float)
    order = np.argsort(p)
    m = len(p)
    rej = np.zeros(m, bool)
    for i, j in enumerate(order):
        if p[j] <= alpha / (m - i):
            rej[j] = True
        else:
            break
    return rej


def benjamini_hochberg(p, q=0.05) -> np.ndarray:
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    thresh = q * np.arange(1, m + 1) / m
    below = p[order] <= thresh
    k = np.max(np.flatnonzero(below)) + 1 if below.any() else 0
    rej = np.zeros(m, bool)
    rej[order[:k]] = True
    return rej


# ---------------------------------------------------------------------------
def stambaugh_bias(rho: float, cov_uv: float, var_v: float, T: int) -> float:
    """E[beta_hat - beta] ~ (cov(u, v) / var(v)) * E[rho_hat - rho], with E[rho_hat - rho] ~ -(1 + 3 rho) / T
    (Kendall 1954; Stambaugh 1999), for r_{t+1} = a + beta x_t + u, x_{t+1} = c + rho x_t + v."""
    return float(cov_uv / var_v * (-(1 + 3 * rho) / T))


def simulate_predictive(T: int, rho: float, corr_uv: float, beta: float = 0.0, n: int = 5000, sd_u=1.0, sd_v=1.0,
                        seed=0) -> np.ndarray:
    """OLS slopes of r_{t+1} on x_t across ``n`` simulated samples of length ``T`` with a persistent predictor."""
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    burn = 200
    L = np.linalg.cholesky(np.array([[sd_u ** 2, corr_uv * sd_u * sd_v], [corr_uv * sd_u * sd_v, sd_v ** 2]]))
    for i in range(n):
        e = rng.standard_normal((T + burn + 1, 2)) @ L.T
        x = np.empty(T + burn + 1)
        x[0] = 0.0
        for t in range(1, T + burn + 1):
            x[t] = rho * x[t - 1] + e[t, 1]
        x = x[burn:]
        r = beta * x[:-1] + e[burn + 1:, 0]
        xx = x[:-1] - x[:-1].mean()
        out[i] = xx @ (r - r.mean()) / (xx @ xx)
    return out


# ---------------------------------------------------------------------------
def gmm(moments, theta0, lags=0, bounds=None) -> dict:
    """Two-step GMM.  ``moments(theta)`` returns an n x q matrix of moment conditions (mean zero at the truth).  Step 1
    uses the identity weight, step 2 the inverse of the (Newey-West, ``lags``) long-run covariance at the step-1
    estimate.  Returns theta, standard errors, Hansen's J statistic and its p-value (q - p degrees of freedom)."""
    theta0 = np.asarray(theta0, float)

    def obj(th, W):
        g = moments(th).mean(axis=0)
        return float(g @ W @ g)

    q = moments(theta0).shape[1]
    r1 = optimize.minimize(obj, theta0, args=(np.eye(q),), method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14,
                                                                                         "maxiter": 20000})
    G1 = moments(r1.x)
    n = len(G1)
    Gc = G1 - G1.mean(axis=0)
    S = Gc.T @ Gc / n
    for l_ in range(1, lags + 1):
        w = 1 - l_ / (lags + 1)
        C = Gc[l_:].T @ Gc[:-l_] / n
        S += w * (C + C.T)
    W = np.linalg.inv(S)
    r2 = optimize.minimize(obj, r1.x, args=(W,), method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14,
                                                                               "maxiter": 20000})
    th = r2.x
    # Jacobian of the mean moments by central differences
    p = len(th)
    D = np.zeros((q, p))
    for j in range(p):
        h = 1e-5 * max(1.0, abs(th[j]))
        e = np.zeros(p)
        e[j] = h
        D[:, j] = (moments(th + e).mean(axis=0) - moments(th - e).mean(axis=0)) / (2 * h)
    V = np.linalg.inv(D.T @ W @ D) / n
    J = n * obj(th, W)
    df = q - p
    return {"theta": th, "se": np.sqrt(np.maximum(np.diag(V), 0)), "J": float(J), "df": int(df),
            "p_J": float(stats.chi2.sf(J, df)) if df > 0 else float("nan"), "n": int(n)}


# ---------------------------------------------------------------------------
def _spline_features(X, knots=12, at=None):
    """Linear splines in each column (knots at quantiles of ``at``, the training sample, default ``X``) plus pairwise
    products."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    A = X if at is None else (np.asarray(at, float) if np.asarray(at).ndim > 1 else np.asarray(at, float)[:, None])
    cols = [X]
    for j in range(X.shape[1]):
        qs = np.quantile(A[:, j], np.linspace(0, 1, knots + 2)[1:-1])
        cols += [np.maximum(X[:, [j]] - q, 0) for q in qs]
    if X.shape[1] > 1:
        cols += [(X[:, [a]] * X[:, [b]]) for a in range(X.shape[1]) for b in range(a + 1, X.shape[1])]
    return np.column_stack(cols)


def ridge_fit_predict(Xtr, ytr, Xte, lam=1.0, knots=12):
    F, Ft = _spline_features(Xtr, knots), _spline_features(Xte, knots, at=Xtr)
    mu, sd = F.mean(axis=0), F.std(axis=0) + 1e-12
    F, Ft = (F - mu) / sd, (Ft - mu) / sd
    A = F.T @ F + lam * np.eye(F.shape[1])
    w = np.linalg.solve(A, F.T @ (ytr - ytr.mean()))
    return ytr.mean() + Ft @ w


def dml_plr(y, d, X, folds=5, lam=1.0, seed=0) -> dict:
    """Partially linear model y = theta d + g(X) + e, d = m(X) + v.  Cross-fitted: learn E[y|X] and E[d|X] on the other
    folds, residualise, and regress residual on residual (Chernozhukov et al. 2018).  Also returns the naive OLS of y
    on d and X, which is biased when g is nonlinear and d depends on X."""
    y, d = np.asarray(y, float), np.asarray(d, float)
    X = np.asarray(X, float)
    n = len(y)
    rng = np.random.default_rng(seed)
    fold = rng.permutation(n) % folds
    ry, rd = np.empty(n), np.empty(n)
    for k in range(folds):
        tr, te = fold != k, fold == k
        ry[te] = y[te] - ridge_fit_predict(X[tr], y[tr], X[te], lam)
        rd[te] = d[te] - ridge_fit_predict(X[tr], d[tr], X[te], lam)
    theta = float(rd @ ry / (rd @ rd))
    psi = (ry - theta * rd) * rd
    se = float(np.sqrt(np.mean(psi ** 2) / np.mean(rd ** 2) ** 2 / n))
    naive = ols(y, np.column_stack([d, X]))
    return {"theta": theta, "se": se, "naive": float(naive["beta"][1]), "naive_se": float(naive["se"][1])}


# ---------------------------------------------------------------------------
def shrink_means(means, ses) -> dict:
    """Empirical-Bayes normal-normal shrinkage: each mean is pulled toward the grand mean by B_i = s_i^2 / (s_i^2 + tau^2),
    with the between-asset variance tau^2 estimated by the method of moments (truncated at zero)."""
    m = np.asarray(means, float)
    s2 = np.asarray(ses, float) ** 2
    grand = float(np.average(m, weights=1 / s2))
    tau2 = max(float(np.var(m, ddof=1) - np.mean(s2)), 0.0)
    B = s2 / (s2 + tau2) if tau2 > 0 else np.ones_like(s2)
    return {"shrunk": grand + (1 - B) * (m - grand), "grand": grand, "tau": float(np.sqrt(tau2)), "B": B}
