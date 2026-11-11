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


# ---------------------------------------------------------------------------
# Part 6, expanded: long-run variances, fixed-b, panels, two-pass, MLE, predictive regressions out of sample,
# event studies, Gibbs, causal designs
# ---------------------------------------------------------------------------
def lrv(z, kernel="bartlett", bw=None, nu=None) -> np.ndarray:
    """Long-run variance S = sum_k Gamma_k of a (demeaned) series ``z`` (T, or T x k).  ``kernel``: 'bartlett'
    (Newey-West, bandwidth ``bw`` = lags + 1, default the rule of thumb 0.75 T^(1/3)), 'qs' (quadratic spectral, ``bw``
    a real bandwidth) or 'ewc' (equal-weighted cosine: the average of ``nu`` squared cosine projections, default
    0.4 T^(2/3); Lazarus, Lewis, Stock and Watson 2018)."""
    z = np.asarray(z, float)
    one = z.ndim == 1
    Z = z[:, None] if one else z
    Z = Z - Z.mean(axis=0)
    T = len(Z)
    if kernel == "ewc":
        nu = int(nu or max(1, round(0.4 * T ** (2 / 3))))
        t = np.arange(1, T + 1)
        L = np.array([np.sqrt(2 / T) * (np.cos(np.pi * j * (t - 0.5) / T) @ Z) for j in range(1, nu + 1)])
        S = L.T @ L / nu
    else:
        if bw is None:
            bw = 0.75 * T ** (1 / 3) + 1
        S = Z.T @ Z / T
        for k in range(1, T):
            if kernel == "bartlett":
                w = 1 - k / bw
                if w <= 0:
                    break
            elif kernel == "qs":
                x = 6 * np.pi * (k / bw) / 5
                w = 3 / x ** 2 * (np.sin(x) / x - np.cos(x))
            else:
                raise ValueError(kernel)
            G = Z[k:].T @ Z[:-k] / T
            S = S + w * (G + G.T)
    return float(S[0, 0]) if one else S


def fixed_b_cv(b, kernel="bartlett", alpha=0.05, T=500, reps=20000, seed=0) -> float:
    """Two-sided critical value of the t-statistic of a mean when the long-run variance uses a Bartlett kernel with
    bandwidth ``b T`` (Kiefer and Vogelsang 2005), by simulation of iid normal samples of length ``T``: the fixed-b
    limit W(1) / sqrt(Q_b) is not standard normal, and its critical values grow with ``b``."""
    rng = np.random.default_rng(seed)
    bw = max(b * T, 1.0)
    k = np.arange(1, T)
    w = np.clip(1 - k / bw, 0, None)
    nfft = 1 << int(np.ceil(np.log2(2 * T)))
    out = np.empty(reps)
    for s in range(0, reps, 2000):
        Z = rng.standard_normal((min(2000, reps - s), T))
        m = Z.mean(axis=1)
        D = Z - m[:, None]
        F = np.fft.rfft(D, nfft, axis=1)
        ac = np.fft.irfft(F * np.conj(F), nfft, axis=1)[:, :T] / T
        S = ac[:, 0] + 2 * ac[:, 1:] @ w
        out[s:s + len(m)] = np.sqrt(T) * m / np.sqrt(np.maximum(S, 1e-300))
    return float(np.quantile(np.abs(out), 1 - alpha))


def hodrick_se(r1, x, h) -> dict:
    """Long-horizon regression of the ``h``-period sum of one-period returns ``r1[t+1..t+h]`` on ``x[t]`` with Hodrick's
    (1992) 1B standard error: under the null of no predictability the covariance is built from one-period residuals
    times the predictor summed backward over ``h`` periods, so no overlapping residuals enter.  ``r1[t]`` is the
    return over period t+1 (aligned with ``x[t]``)."""
    r1, x = np.asarray(r1, float), np.asarray(x, float)
    T = len(r1)
    X = _design(x)
    R = np.array([r1[t:t + h].sum() for t in range(T - h + 1)])
    Xh = X[:T - h + 1]
    beta = np.linalg.lstsq(Xh, R, rcond=None)[0]
    u = r1 - r1.mean()
    W = np.array([u[t] * X[max(0, t - h + 1):t + 1].sum(axis=0) for t in range(h - 1, T)])
    Sx = W.T @ W / len(W)
    Z = Xh.T @ Xh / len(Xh)
    V = np.linalg.inv(Z) @ Sx @ np.linalg.inv(Z) / len(W)
    se = np.sqrt(np.diag(V))
    return {"beta": beta, "se": se, "t": beta / se}


def within_between(y, x, groups) -> dict:
    """Split a pooled slope into its within-group (group-demeaned) and between-group (group means) slopes.  With
    groups = months, the within slope is pooled OLS with month fixed effects, which equals the Fama-MacBeth average
    weighted by each month's cross-sectional variance of ``x``; the pooled slope is the SS-weighted average of the
    two."""
    y, x, g = np.asarray(y, float), np.asarray(x, float), np.asarray(groups)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x, g = y[ok], x[ok], g[ok]
    _, gi = np.unique(g, return_inverse=True)
    cnt = np.bincount(gi)
    mx, my = np.bincount(gi, x) / cnt, np.bincount(gi, y) / cnt
    xw, yw = x - mx[gi], y - my[gi]
    xb, yb = mx[gi] - x.mean(), my[gi] - y.mean()
    ssw, ssb = float(xw @ xw), float(xb @ xb)
    bw, bb = float(xw @ yw / ssw), float(xb @ yb / ssb)
    xp = x - x.mean()
    return {"within": bw, "between": bb, "pooled": float(xp @ (y - y.mean()) / (xp @ xp)), "ss_within": ssw,
            "ss_between": ssb, "w_within": ssw / (ssw + ssb)}


def two_pass(R, F, shanken=True) -> dict:
    """Two-pass test of a linear factor model.  ``R``: T x N excess returns, ``F``: T x K factors.  First pass:
    time-series betas.  Second pass: each period, regress the cross-section of returns on the betas (Fama-MacBeth);
    the premia lambda are the averages.  Shanken's (1992) correction multiplies the FM variance by 1 + l' Sigma_f^-1 l
    and adds Sigma_f / T, because the betas are estimated."""
    R, F = np.asarray(R, float), np.asarray(F, float)
    if F.ndim == 1:
        F = F[:, None]
    T, N = R.shape
    K = F.shape[1]
    X = _design(F)
    B = np.linalg.lstsq(X, R, rcond=None)[0][1:].T  # N x K
    Bd = _design(B)
    G = np.array([np.linalg.lstsq(Bd, R[t], rcond=None)[0] for t in range(T)])  # T x (K+1)
    lam = G.mean(axis=0)
    Vfm = np.cov(G.T, ddof=1) / T
    Sf = np.atleast_2d(np.cov(F.T, ddof=1))
    c = float(lam[1:] @ np.linalg.solve(Sf, lam[1:]))
    Vsh = Vfm * (1 + c)
    Vsh[1:, 1:] += Sf / T
    out = {"lambda": lam, "se_fm": np.sqrt(np.diag(Vfm)), "se_shanken": np.sqrt(np.diag(Vsh)), "betas": B,
           "slopes": G, "shanken_c": c, "mean_returns": R.mean(axis=0)}
    out["t_fm"] = lam / out["se_fm"]
    out["t_shanken"] = lam / out["se_shanken"]
    return out


def grs(R, F) -> dict:
    """Gibbons, Ross and Shanken (1989): are all N time-series alphas zero?  F-distributed with (N, T - N - K) df."""
    R, F = np.asarray(R, float), np.asarray(F, float)
    if F.ndim == 1:
        F = F[:, None]
    T, N = R.shape
    K = F.shape[1]
    X = _design(F)
    coef = np.linalg.lstsq(X, R, rcond=None)[0]
    a = coef[0]
    E = R - X @ coef
    Sig = E.T @ E / (T - K - 1)
    mu = F.mean(axis=0)
    Om = np.atleast_2d(np.cov(F.T, ddof=1))
    stat = (T - N - K) / N * float(a @ np.linalg.solve(Sig, a)) / (1 + float(mu @ np.linalg.solve(Om, mu)))
    return {"F": stat, "p": float(stats.f.sf(stat, N, T - N - K)), "alpha": a, "df": (N, T - N - K)}


def _num_grad(f, th, h=1e-5):
    th = np.asarray(th, float)
    g = []
    for j in range(len(th)):
        e = np.zeros_like(th)
        e[j] = h * max(1.0, abs(th[j]))
        g.append((f(th + e) - f(th - e)) / (2 * e[j]))
    return np.array(g)


def mle(nll_obs, theta0, steps=40, record=True, tol=1e-9) -> dict:
    """Maximum likelihood by damped Newton steps on the summed negative log-likelihood ``nll_obs(theta)`` (one value
    per observation), with numerical derivatives.  Returns the estimate, the iterates (for a replay), the naive
    standard errors (inverse Hessian, which trusts the model) and the sandwich H^-1 J H^-1 (quasi-ML: valid when the
    model is wrong), J being the outer product of the per-observation scores."""
    f = lambda t: float(np.sum(nll_obs(t)))  # noqa: E731
    th = np.asarray(theta0, float)
    path, vals = [th.copy()], [f(th)]
    for _ in range(steps):
        g = _num_grad(f, th)
        H = np.array([_num_grad(lambda t, j=j: _num_grad(f, t)[j], th) for j in range(len(th))])
        H = (H + H.T) / 2
        w, U = np.linalg.eigh(H)
        step = -U @ ((U.T @ g) / np.maximum(np.abs(w), 1e-8))
        lam, cur = 1.0, f(th)
        while f(th + lam * step) > cur and lam > 1e-6:
            lam /= 2
        th = th + lam * step
        path.append(th.copy())
        vals.append(f(th))
        if abs(vals[-2] - vals[-1]) < tol * max(1.0, abs(vals[-1])):
            break
    H = np.array([_num_grad(lambda t, j=j: _num_grad(f, t)[j], th) for j in range(len(th))])
    H = (H + H.T) / 2
    scores = np.column_stack([(nll_obs(th + e) - nll_obs(th - e)) / (2 * e.max())
                              for e in np.eye(len(th)) * 1e-5 * np.maximum(1.0, np.abs(th))])
    J = scores.T @ scores
    Hi = np.linalg.inv(H)
    return {"theta": th, "path": np.array(path) if record else None, "nll": np.array(vals),
            "se_naive": np.sqrt(np.diag(Hi)), "se_sandwich": np.sqrt(np.diag(Hi @ J @ Hi)), "H": H, "J": J}


def oos_r2(r, x, start, ct=False, min_obs=24) -> dict:
    """Out-of-sample R^2 of a predictive regression (Goyal and Welch 2008; Campbell and Thompson 2008).  ``r[t]`` is the
    return over period t+1 and ``x[t]`` the predictor known at t.  For each t >= ``start``, fit on observations
    before t, forecast r[t], and compare with the running historical mean.  ``ct``: Campbell-Thompson restrictions
    (a wrong-signed slope, against the full-sample sign, falls back to the mean; negative forecasts are set to
    zero).  Returns R2_OS, the cumulative SSE difference (positive = predictor ahead) and the forecasts."""
    r, x = np.asarray(r, float), np.asarray(x, float)
    sign = np.sign(ols(r, x)["beta"][1])
    fc, mean_fc, slopes = [], [], []
    for t in range(start, len(r)):
        rr, xx = r[:t], x[:t]
        m = np.isfinite(rr) & np.isfinite(xx)
        if m.sum() < min_obs:
            fc.append(np.nan); mean_fc.append(np.nan); slopes.append(np.nan)  # noqa: E702
            continue
        b = ols(rr[m], xx[m])["beta"]
        f_ = b[0] + b[1] * x[t]
        mu = rr[m].mean()
        if ct:
            if np.sign(b[1]) != sign:
                f_ = mu
            f_ = max(f_, 0.0)
        fc.append(f_); mean_fc.append(mu); slopes.append(b[1])  # noqa: E702
    fc, mean_fc = np.array(fc), np.array(mean_fc)
    y = r[start:]
    ok = np.isfinite(fc) & np.isfinite(y)
    e1, e0 = (y - fc) ** 2, (y - mean_fc) ** 2
    dsse = np.cumsum(np.where(ok, e0 - e1, 0.0))
    return {"r2_os": float(1 - e1[ok].sum() / e0[ok].sum()), "dsse": dsse, "forecast": fc, "mean_forecast": mean_fc,
            "slopes": np.array(slopes)}


def augmented_predictive(r, x) -> dict:
    """Amihud and Hurvich (2004): add the predictor's bias-corrected innovation to the predictive regression, which
    removes Stambaugh's bias.  ``r[t]`` is the return over t+1, ``x`` the predictor (same length).  Returns the
    corrected slope and its standard error (augmented OLS variance plus phi^2 Var(rho_c))."""
    r, x = np.asarray(r, float), np.asarray(x, float)
    T = len(x) - 1
    ar = ols(x[1:], x[:-1])
    rho = float(ar["beta"][1])
    rho_c = min(rho + (1 + 3 * rho) / T + 3 * (1 + 3 * rho) / T ** 2, 0.9999)
    th_c = float(np.mean(x[1:] - rho_c * x[:-1]))
    v_c = x[1:] - th_c - rho_c * x[:-1]
    aug = ols(r[:-1], np.column_stack([x[:-1], v_c]))
    phi = float(aug["beta"][2])
    var_rho = (1 + 3 / T + 9 / T ** 2) ** 2 * float(ar["se"][1]) ** 2
    se = float(np.sqrt(aug["se"][1] ** 2 + phi ** 2 * var_rho))
    return {"beta": float(aug["beta"][1]), "se": se, "t": float(aug["beta"][1] / se), "rho": rho, "rho_c": rho_c,
            "phi": phi}


def ivx(r, x, cz=1.0, delta=0.95) -> dict:
    """A univariate IVX test (Kostakis, Magdalinos and Stamatogiannis 2015): instrument the predictor with a
    filtered version of its own changes, z_t = sum_j rho_z^(t-j) dx_j, rho_z = 1 - cz / T^delta, which is less
    persistent than x whatever x's persistence, so the Wald statistic is chi^2(1) without knowing rho.  ``r[t]`` is the
    return over t+1.  (Simplified: no finite-sample mean correction.)"""
    r, x = np.asarray(r, float), np.asarray(x, float)
    y, xl = r[:-1], x[:-1]
    T = len(y)
    rz = 1 - cz / T ** delta
    dx = np.diff(x, prepend=x[0])[:-1]
    z = np.zeros(T)
    for t in range(1, T):
        z[t] = rz * z[t - 1] + dx[t]
    yd, xd = y - y.mean(), xl - xl.mean()
    beta = float(z @ yd / (z @ xd))
    u = yd - beta * xd
    zd = z - z.mean()
    var = float((u @ u / T) * (zd @ zd) / (z @ xd) ** 2)
    W = beta ** 2 / var
    return {"beta": beta, "se": float(np.sqrt(var)), "wald": float(W), "p": float(stats.chi2.sf(W, 1)), "rho_z": rz}


def event_mean_test(r, is_event) -> dict:
    """Event days against all other days for a market-wide event (every 'firm' shares the date): the abnormal return
    is the event-day mean minus the non-event mean, and its standard error comes from the time series of non-event
    days (the crude dependence adjustment: no diversification across events that share a date)."""
    r = np.asarray(r, float)
    ev = np.asarray(is_event, bool)
    a, b = r[ev], r[~ev]
    ar = float(a.mean() - b.mean())
    se = float(b.std(ddof=1) * np.sqrt(1 / len(a) + 1 / len(b)))
    return {"ar": ar, "se": se, "t": ar / se, "n_events": int(ev.sum()), "mean_event": float(a.mean()),
            "mean_other": float(b.mean())}


def placebo_means(r, n_events, reps=10000, exclude=None, seed=0) -> np.ndarray:
    """Means of ``reps`` random sets of ``n_events`` days (drawn from the days not in ``exclude``): the null
    distribution of an event-day mean."""
    r = np.asarray(r, float)
    pool = r if exclude is None else r[~np.asarray(exclude, bool)]
    rng = np.random.default_rng(seed)
    return np.array([pool[rng.choice(len(pool), n_events, replace=False)].mean() for _ in range(reps)])


def stationary_indices(n, mean_block=12, B=1, seed=0) -> np.ndarray:
    """B x n index arrays of the stationary bootstrap (Politis and Romano 1994), vectorised: blocks start uniformly,
    have geometric lengths with mean ``mean_block`` and wrap around the end of the sample."""
    rng = np.random.default_rng(seed)
    out = np.empty((B, n), int)
    for b in range(B):
        k = int(2 * n / mean_block) + 10
        L = rng.geometric(1 / mean_block, k)
        while L.sum() < n:
            L = np.concatenate([L, rng.geometric(1 / mean_block, k)])
        nb = int(np.searchsorted(np.cumsum(L), n)) + 1
        L = L[:nb]
        s = rng.integers(0, n, nb)
        pos = np.arange(L.sum()) - np.repeat(np.cumsum(L) - L, L)
        out[b] = ((np.repeat(s, L) + pos) % n)[:n]
    return out


def gibbs_hierarchical(est, se, draws=5000, chains=4, seed=0, burn=500) -> dict:
    """Gibbs sampler for alpha_i ~ N(mu, tau^2), est_i ~ N(alpha_i, se_i^2), flat priors on mu and tau.  Each
    conditional is conjugate: alpha | mu, tau is normal (a precision-weighted average); mu | alpha, tau is normal;
    tau^2 | alpha, mu is scaled inverse chi-square.  Returns the traces (chains x draws) of mu and tau, and the
    posterior means of the alphas."""
    y, s2 = np.asarray(est, float), np.asarray(se, float) ** 2
    k = len(y)
    mu_tr, tau_tr = np.empty((chains, draws)), np.empty((chains, draws))
    a_sum = np.zeros(k)
    cnt = 0
    for c in range(chains):
        rng = np.random.default_rng(seed + c)
        mu, tau2 = rng.normal(y.mean(), y.std()), y.var() * rng.uniform(0.2, 3)
        for it in range(draws + burn):
            prec = 1 / s2 + 1 / tau2
            a = rng.normal((y / s2 + mu / tau2) / prec, np.sqrt(1 / prec))
            mu = rng.normal(a.mean(), np.sqrt(tau2 / k))
            tau2 = float(np.sum((a - mu) ** 2) / rng.chisquare(k - 2))
            tau2 = max(tau2, 1e-12)
            if it >= burn:
                mu_tr[c, it - burn], tau_tr[c, it - burn] = mu, np.sqrt(tau2)
                a_sum += a
                cnt += 1
    return {"mu": mu_tr, "tau": tau_tr, "alpha_post": a_sum / cnt}


def iv_2sls(y, x, z) -> dict:
    """Two-stage least squares with one endogenous regressor ``x`` and instruments ``z`` (a constant added).  Returns
    the slope, its standard error and the first-stage F statistic."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    Z = _design(z)
    fs = ols(x, np.asarray(z, float))
    q = Z.shape[1] - 1
    F = float(fs["beta"][1:] @ np.linalg.solve(fs["V"][1:, 1:], fs["beta"][1:]) / q)
    xh = Z @ fs["beta"]
    X, Xh = _design(x), _design(xh)
    b = np.linalg.solve(Xh.T @ X, Xh.T @ y)
    u = y - X @ b
    V = np.linalg.inv(Xh.T @ Xh) * (u @ u) / (len(y) - 2)
    return {"beta": float(b[1]), "se": float(np.sqrt(V[1, 1])), "F": F}


def did_2x2(y_t1, y_t0, y_c1, y_c0) -> float:
    """The two-by-two difference in differences: the treated group's change minus the control group's change."""
    return float((np.mean(y_t1) - np.mean(y_t0)) - (np.mean(y_c1) - np.mean(y_c0)))


def twfe(Y, D) -> dict:
    """Two-way fixed effects regression of a balanced panel ``Y`` (units x periods) on a treatment dummy ``D``, and
    the implicit weight it puts on each treated cell's effect (de Chaisemartin and D'Haultfoeuille 2020): the
    residual of D after removing unit and period means.  Under staggered adoption some weights are negative."""
    Y, D = np.asarray(Y, float), np.asarray(D, float)
    dm = lambda A: A - A.mean(1, keepdims=True) - A.mean(0, keepdims=True) + A.mean()  # noqa: E731
    Dt = dm(D)
    beta = float((Dt * dm(Y)).sum() / (Dt * Dt).sum())
    W = np.where(D > 0, Dt, 0.0)
    W = W / W.sum()
    return {"beta": beta, "weights": W}


def did_cs(Y, cohort) -> dict:
    """Callaway and Sant'Anna (2021), simplest form: for each adoption cohort g and period t >= g, the 2x2 DiD of
    cohort g against units not yet treated at t (and never-treated units), from period g - 1; averaged over cells
    with equal weight per treated unit-period.  ``cohort``: first treated period per unit (np.inf if never)."""
    Y = np.asarray(Y, float)
    coh = np.asarray(cohort, float)
    n, T = Y.shape
    cells = []
    for g in np.unique(coh[np.isfinite(coh)]):
        g = int(g)
        if g < 1:
            continue
        tr = coh == g
        for t in range(g, T):
            ctrl = coh > t
            if not ctrl.any():
                continue
            att = (Y[tr, t] - Y[tr, g - 1]).mean() - (Y[ctrl, t] - Y[ctrl, g - 1]).mean()
            cells.append((g, t, float(att), int(tr.sum())))
    w = np.array([c[3] for c in cells], float)
    att = float(np.sum(w * np.array([c[2] for c in cells])) / w.sum()) if cells else float("nan")
    return {"att": att, "cells": cells}


def rd_local_linear(x, y, c=0.0, bw=1.0) -> dict:
    """Sharp regression discontinuity: local linear fits with a triangular kernel within ``bw`` of the cutoff ``c`` on
    each side; the jump is the difference of the two intercepts at ``c`` (with a heteroskedasticity-robust se)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    fits = {}
    for side, m in (("right", (x >= c) & (x < c + bw)), ("left", (x < c) & (x > c - bw))):
        xs, ys = x[m] - c, y[m]
        w = 1 - np.abs(xs) / bw
        X = _design(xs)
        Wx = X * w[:, None]
        A = np.linalg.inv(X.T @ Wx)
        b = A @ Wx.T @ ys
        u = ys - X @ b
        V = A @ ((Wx * u[:, None]).T @ (Wx * u[:, None])) @ A
        fits[side] = (b, V[0, 0], int(m.sum()))
    jump = float(fits["right"][0][0] - fits["left"][0][0])
    se = float(np.sqrt(fits["right"][1] + fits["left"][1]))
    return {"jump": jump, "se": se, "n": fits["right"][2] + fits["left"][2], "left": fits["left"][0].tolist(),
            "right": fits["right"][0].tolist()}
