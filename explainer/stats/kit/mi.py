"""statkit.mi -- what you didn't see: missing data and measurement error (Part 41 of *Statistics, Built*).

* **Masks:** MCAR, MAR and MNAR missingness with a known mechanism, for grading methods against the truth.
* **Likelihood:** EM for a multivariate normal with arbitrary holes (Dempster, Laird & Rubin 1977), with the
  observed-data log-likelihood (FIML) at every step.
* **Multiple imputation:** proper Bayesian normal-regression draws, predictive mean matching, logistic draws;
  chained equations (van Buuren & Groothuis-Oudshoorn); Rubin's (1987) rules with Barnard & Rubin's (1999) degrees of
  freedom and the fraction of missing information.
* **Weighting:** IPW and AIPW (doubly robust) means for missing outcomes, with influence-function SEs.
* **MNAR:** Heckman's (1979) selection model by two steps (with the corrected covariance) and by maximum likelihood;
  delta-adjusted (pattern-mixture) imputation for tipping-point analysis.
* **MRP:** multilevel logistic regression with normal random effects for several factors (penalized IRLS with
  variances by approximate marginal likelihood), then poststratification (Gelman & Little 1997).
* **Measurement error:** Spearman's (1904) correction for attenuation; SIMEX (Cook & Stefanski 1994); the matrix
  correction of misclassified 2 x 2 tables.

Tested in ``tests/test_stats_kit_mi.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------------------------------------------------------
# Masks
# ---------------------------------------------------------------------------------------------------------------
def _logit_rate(z, rate: float) -> np.ndarray:
    """Probabilities sigmoid(a + z) with the intercept a chosen so that their mean is ``rate``."""
    z = np.asarray(z, float)
    f = lambda a: float(np.mean(1 / (1 + np.exp(-(a + z)))) - rate)  # noqa: E731
    a = optimize.brentq(f, -30, 30)
    return 1 / (1 + np.exp(-(a + z)))


def mask(kind: str, n: int, rate: float, rng: np.random.Generator, driver=None, strength: float = 1.5) -> dict:
    """A missingness mask (True = missing) with mean ``rate``.  ``kind``: "mcar" (a coin), "mar" (logistic in an
    observed ``driver``), "mnar" (logistic in the value itself, passed as ``driver``).  Returns the mask and the
    true probabilities, so weights can be graded."""
    if kind == "mcar":
        p = np.full(n, rate)
    else:
        z = np.asarray(driver, float)
        z = (z - np.nanmean(z)) / np.nanstd(z)
        p = _logit_rate(strength * z, rate)
    return {"miss": rng.random(n) < p, "p": p}


# ---------------------------------------------------------------------------------------------------------------
# EM for a multivariate normal
# ---------------------------------------------------------------------------------------------------------------
def mvn_obs_loglik(X, mu, S) -> float:
    """The observed-data log-likelihood of a normal with holes (NaN): each row contributes its observed margin."""
    X = np.asarray(X, float)
    ll = 0.0
    for row in X:
        o = ~np.isnan(row)
        if not o.any():
            continue
        d = row[o] - mu[o]
        So = S[np.ix_(o, o)]
        sign, logdet = np.linalg.slogdet(So)
        ll += -0.5 * (o.sum() * math.log(2 * math.pi) + logdet + d @ np.linalg.solve(So, d))
    return float(ll)


def em_mvn(X, iters: int = 200, tol: float = 1e-10) -> dict:
    """EM for (mu, Sigma) of a multivariate normal from rows with NaN holes.  E-step: each missing block's
    conditional mean and covariance given the observed part; M-step: the complete-data MLE from the expected
    sufficient statistics.  ``ll`` records the observed log-likelihood, which never decreases."""
    X = np.asarray(X, float)
    n, p = X.shape
    mu = np.nanmean(X, 0)
    S = np.diag(np.nanvar(X, 0))
    hist = [mvn_obs_loglik(X, mu, S)]
    path = [(mu.copy(), S.copy())]
    for _ in range(iters):
        T1, T2 = np.zeros(p), np.zeros((p, p))
        for row in X:
            m = np.isnan(row)
            x = row.copy()
            C = np.zeros((p, p))
            if m.any():
                o = ~m
                if o.any():
                    B = S[np.ix_(m, o)] @ np.linalg.inv(S[np.ix_(o, o)])
                    x[m] = mu[m] + B @ (row[o] - mu[o])
                    C[np.ix_(m, m)] = S[np.ix_(m, m)] - B @ S[np.ix_(o, m)]
                else:
                    x[m] = mu[m]
                    C[np.ix_(m, m)] = S[np.ix_(m, m)]
            T1 += x
            T2 += np.outer(x, x) + C
        mu = T1 / n
        S = T2 / n - np.outer(mu, mu)
        hist.append(mvn_obs_loglik(X, mu, S))
        path.append((mu.copy(), S.copy()))
        if abs(hist[-1] - hist[-2]) < tol:
            break
    return {"mu": mu, "S": S, "ll": np.array(hist), "path": path, "iters": len(hist) - 1}


# ---------------------------------------------------------------------------------------------------------------
# Imputation and Rubin's rules
# ---------------------------------------------------------------------------------------------------------------
def _design(X):
    X = np.asarray(X, float)
    X = X[:, None] if X.ndim == 1 else X
    return np.column_stack([np.ones(len(X)), X])


def impute_norm(y, X, rng: np.random.Generator, kind: str = "proper") -> np.ndarray:
    """Fill the NaNs of ``y`` from a linear regression on ``X`` (fully observed).  "proper": draw sigma^2 and beta from
    their posterior under a flat prior, then add noise (Rubin's Bayesian imputation); "stochastic": the fitted beta and
    sigma, plus noise; "mean": the fitted value only (deterministic regression imputation); "pmm": predictive mean
    matching, a donor's observed value among the 5 closest predicted values."""
    y = np.asarray(y, float).copy()
    D = _design(X)
    m = np.isnan(y)
    if not m.any():
        return y
    Do, yo = D[~m], y[~m]
    XtX = Do.T @ Do
    b = np.linalg.solve(XtX, Do.T @ yo)
    res = yo - Do @ b
    dfree = len(yo) - D.shape[1]
    s2 = res @ res / dfree
    if kind == "mean":
        y[m] = D[m] @ b
        return y
    if kind == "stochastic":
        y[m] = D[m] @ b + math.sqrt(s2) * rng.standard_normal(m.sum())
        return y
    sig2 = res @ res / rng.chisquare(dfree)
    bstar = b + np.linalg.cholesky(sig2 * np.linalg.inv(XtX)) @ rng.standard_normal(D.shape[1])
    if kind == "proper":
        y[m] = D[m] @ bstar + math.sqrt(sig2) * rng.standard_normal(m.sum())
        return y
    if kind == "pmm":
        pred_o, pred_m = Do @ b, D[m] @ bstar
        out = []
        for v in pred_m:
            near = np.argsort(np.abs(pred_o - v))[:5]
            out.append(yo[rng.choice(near)])
        y[m] = out
        return y
    raise ValueError(kind)


def _logistic_irls(D, y, ridge: float = 1e-6, iters: int = 50):
    b = np.zeros(D.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(D @ b)))
        W = p * (1 - p)
        H = (D * W[:, None]).T @ D + ridge * np.eye(D.shape[1])
        step = np.linalg.solve(H, D.T @ (y - p) - ridge * b)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = 1 / (1 + np.exp(-(D @ b)))
    H = (D * (p * (1 - p))[:, None]).T @ D + ridge * np.eye(D.shape[1])
    return b, np.linalg.inv(H)


def impute_logreg(y, X, rng: np.random.Generator) -> np.ndarray:
    """Fill NaNs of a 0/1 ``y`` by a proper logistic draw: beta from its approximate posterior, then Bernoulli."""
    y = np.asarray(y, float).copy()
    D = _design(X)
    m = np.isnan(y)
    if not m.any():
        return y
    b, V = _logistic_irls(D[~m], y[~m])
    bstar = b + np.linalg.cholesky(V + 1e-12 * np.eye(len(b))) @ rng.standard_normal(len(b))
    p = 1 / (1 + np.exp(-(D[m] @ bstar)))
    y[m] = (rng.random(m.sum()) < p).astype(float)
    return y


def mice(data, m: int = 20, iters: int = 10, rng: np.random.Generator | None = None, methods: dict | None = None) -> list:
    """Multiple imputation by chained equations.  ``data``: an (n, p) array with NaNs.  Each column with holes is
    imputed in turn from all the others (currently filled), by ``methods[j]`` ("norm", "pmm" or "logreg"; default
    "norm"), for ``iters`` sweeps, starting from random draws of observed values; repeated ``m`` times."""
    rng = rng or np.random.default_rng(0)
    data = np.asarray(data, float)
    n, p = data.shape
    miss = np.isnan(data)
    methods = methods or {}
    out = []
    for _ in range(m):
        Y = data.copy()
        for j in range(p):
            if miss[:, j].any():
                Y[miss[:, j], j] = rng.choice(data[~miss[:, j], j], miss[:, j].sum())
        for _ in range(iters):
            for j in range(p):
                if not miss[:, j].any():
                    continue
                others = np.delete(Y, j, axis=1)
                yj = data[:, j].copy()
                meth = methods.get(j, "norm")
                if meth == "logreg":
                    Y[:, j] = impute_logreg(yj, others, rng)
                else:
                    Y[:, j] = impute_norm(yj, others, rng, "pmm" if meth == "pmm" else "proper")
        out.append(Y)
    return out


def rubin(estimates, variances, df_complete: float | None = None, level: float = 0.95) -> dict:
    """Rubin's rules: Qbar = mean of the estimates, W = mean within-imputation variance, B = between variance,
    T = W + (1 + 1/m) B.  Degrees of freedom: Rubin's (m - 1)(1 + 1/r)^2 with r = (1 + 1/m) B / W, or Barnard & Rubin's
    small-sample version when ``df_complete`` is given.  Also the fraction of missing information."""
    q = np.asarray(estimates, float)
    u = np.asarray(variances, float)
    m = len(q)
    Q, W = float(q.mean()), float(u.mean())
    B = float(q.var(ddof=1)) if m > 1 else 0.0
    T = W + (1 + 1 / m) * B
    r = (1 + 1 / m) * B / W if W > 0 else np.inf
    df_old = (m - 1) * (1 + 1 / r) ** 2 if r > 0 else np.inf
    if df_complete is not None:
        lam = (1 + 1 / m) * B / T
        dobs = (df_complete + 1) / (df_complete + 3) * df_complete * (1 - lam)
        df = 1 / (1 / df_old + 1 / dobs)
    else:
        df = df_old
    lam = (1 + 1 / m) * B / T if T > 0 else 0.0
    fmi = (r + 2 / (df + 3)) / (r + 1) if np.isfinite(df) else lam
    tq = stats.t.ppf(0.5 + level / 2, df) if np.isfinite(df) else stats.norm.ppf(0.5 + level / 2)
    se = math.sqrt(T)
    return {"est": Q, "W": W, "B": B, "T": T, "se": se, "df": float(df), "lambda": float(lam), "fmi": float(fmi),
            "ci": (Q - tq * se, Q + tq * se), "m": m}


# ---------------------------------------------------------------------------------------------------------------
# Weighting
# ---------------------------------------------------------------------------------------------------------------
def response_model(r, X) -> dict:
    """A logistic model for responding (r = 1) given fully observed ``X``: the fitted propensities and coefficients."""
    D = _design(X)
    b, V = _logistic_irls(D, np.asarray(r, float))
    return {"p": 1 / (1 + np.exp(-(D @ b))), "coef": b, "cov": V}


def ipw_mean(y, r, p) -> dict:
    """The Hajek IPW mean sum(r y / p) / sum(r / p) for an outcome seen when r = 1, with an influence-function SE
    (treating p as known; estimating p usually shrinks the SE a little)."""
    y, r, p = np.asarray(y, float), np.asarray(r, float), np.asarray(p, float)
    w = r / p
    yy = np.where(r == 1, y, 0.0)
    mu = float((w * yy).sum() / w.sum())
    phi = w * (yy - mu)
    return {"est": mu, "se": float(np.sqrt(np.sum(phi ** 2)) / w.sum())}


def aipw_mean(y, r, p, mhat) -> dict:
    """The augmented IPW (doubly robust) mean: mean(mhat + r (y - mhat) / p); consistent if either the response model
    p or the outcome model mhat is right (Robins, Rotnitzky & Zhao 1994).  SE from its influence function."""
    y, r, p, mhat = (np.asarray(a, float) for a in (y, r, p, mhat))
    yy = np.where(r == 1, y, 0.0)
    psi = mhat + r * (yy - mhat) / p
    mu = float(psi.mean())
    return {"est": mu, "se": float(psi.std(ddof=1) / math.sqrt(len(psi)))}


# ---------------------------------------------------------------------------------------------------------------
# MNAR: Heckman and tipping points
# ---------------------------------------------------------------------------------------------------------------
def _probit(Z, s, iters: int = 100):
    Z = np.asarray(Z, float)
    g = np.zeros(Z.shape[1])
    for _ in range(iters):
        eta = Z @ g
        Phi = np.clip(stats.norm.cdf(eta), 1e-12, 1 - 1e-12)
        phi = stats.norm.pdf(eta)
        lam1, lam0 = phi / Phi, -phi / (1 - Phi)
        score = Z.T @ np.where(s == 1, lam1, lam0)
        w = np.where(s == 1, lam1 * (lam1 + eta), lam0 * (lam0 + eta))
        H = (Z * w[:, None]).T @ Z
        step = np.linalg.solve(H, score)
        g += step
        if np.max(np.abs(step)) < 1e-10:
            break
    eta = Z @ g
    Phi = np.clip(stats.norm.cdf(eta), 1e-12, 1 - 1e-12)
    phi = stats.norm.pdf(eta)
    lam1, lam0 = phi / Phi, -phi / (1 - Phi)
    w = np.where(s == 1, lam1 * (lam1 + eta), lam0 * (lam0 + eta))
    V = np.linalg.inv((Z * w[:, None]).T @ Z)
    return g, V


def heckman_twostep(y, X, s, Z) -> dict:
    """Heckman (1979): a probit of selection s on Z; then OLS of y on [X, lambda] among the selected, with
    lambda = phi(Z'g) / Phi(Z'g) the inverse Mills ratio.  rho sigma is lambda's coefficient; the covariance is
    Heckman's correction for the heteroscedasticity and for the estimated g (Greene's formula)."""
    s = np.asarray(s, int)
    Zd, Xd = _design(Z), _design(X)
    g, Vg = _probit(Zd, s)
    eta = Zd @ g
    lam = stats.norm.pdf(eta) / np.clip(stats.norm.cdf(eta), 1e-12, None)
    k = s == 1
    Xs = np.column_stack([Xd[k], lam[k]])
    ys = np.asarray(y, float)[k]
    b = np.linalg.lstsq(Xs, ys, rcond=None)[0]
    e = ys - Xs @ b
    blam = b[-1]
    delta = lam[k] * (lam[k] + eta[k])
    s2 = e @ e / k.sum() + blam ** 2 * delta.mean()
    rho2 = min(blam ** 2 / s2, 1.0)
    XtXi = np.linalg.inv(Xs.T @ Xs)
    D = 1 - rho2 * delta
    Q = rho2 * (Xs * delta[:, None]).T @ Zd[k] @ Vg @ Zd[k].T @ (Xs * delta[:, None])
    V = s2 * XtXi @ ((Xs * D[:, None]).T @ Xs + Q) @ XtXi
    return {"beta": b[:-1], "beta_lambda": blam, "cov": V[:-1, :-1], "se": np.sqrt(np.diag(V))[:-1], "sigma": math.sqrt(s2),
            "rho": math.copysign(math.sqrt(rho2), blam), "gamma": g, "mills": lam}


def heckman_mle(y, X, s, Z) -> dict:
    """The selection model by maximum likelihood: y* = X b + e, s* = Z g + u, (e, u) bivariate normal with
    correlation rho and Var u = 1; y seen when s* > 0."""
    s = np.asarray(s, int)
    Zd, Xd = _design(Z), _design(X)
    y = np.asarray(y, float)
    kx, kz = Xd.shape[1], Zd.shape[1]
    two = heckman_twostep(y, X, s, Z)
    x0 = np.concatenate([two["beta"], two["gamma"], [math.log(two["sigma"]), math.atanh(np.clip(two["rho"], -0.95, 0.95))]])
    k = s == 1

    def nll(par):
        b, g = par[:kx], par[kx:kx + kz]
        sig, rho = math.exp(par[-2]), math.tanh(par[-1])
        zg = Zd @ g
        ll0 = stats.norm.logcdf(-zg[~k]).sum()
        e = (y[k] - Xd[k] @ b) / sig
        a = (zg[k] + rho * e) / math.sqrt(1 - rho ** 2)
        ll1 = (stats.norm.logcdf(a) + stats.norm.logpdf(e) - math.log(sig)).sum()
        return -(ll0 + ll1)

    res = optimize.minimize(nll, x0, method="BFGS", options={"gtol": 1e-7, "maxiter": 5000})
    return {"beta": res.x[:kx], "gamma": res.x[kx:kx + kz], "sigma": math.exp(res.x[-2]), "rho": math.tanh(res.x[-1]),
            "loglik": -res.fun, "se": np.sqrt(np.diag(res.hess_inv))[:kx]}


# ---------------------------------------------------------------------------------------------------------------
# MRP
# ---------------------------------------------------------------------------------------------------------------
def mrp_fit(y, factors: list, X=None, iters: int = 60, grid=(0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0)) -> dict:
    """A multilevel logistic regression y ~ fixed X + a random intercept per level of each factor (normal, SD tau_f),
    fitted as penalized IRLS; each tau_f chosen from ``grid`` by a Laplace approximation to the marginal likelihood
    (coordinate-wise).  Returns a predictor for new rows."""
    y = np.asarray(y, float)
    n = len(y)
    Fx = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), np.asarray(X, float)])
    levels = [np.unique(f) for f in factors]
    blocks = [(np.asarray(f)[:, None] == lv[None, :]).astype(float) for f, lv in zip(factors, levels)]
    D = np.column_stack([Fx] + blocks)
    sizes = [b.shape[1] for b in blocks]

    def fit(taus):
        prec = np.concatenate([np.full(Fx.shape[1], 1e-6)] + [np.full(s_, 1 / t ** 2) for s_, t in zip(sizes, taus)])
        b = np.zeros(D.shape[1])
        for _ in range(iters):
            p = 1 / (1 + np.exp(-(D @ b)))
            H = (D * (p * (1 - p))[:, None]).T @ D + np.diag(prec)
            step = np.linalg.solve(H, D.T @ (y - p) - prec * b)
            b += step
            if np.max(np.abs(step)) < 1e-9:
                break
        p = 1 / (1 + np.exp(-(D @ b)))
        H = (D * (p * (1 - p))[:, None]).T @ D + np.diag(prec)
        ll = float(np.sum(y * np.log(p + 1e-15) + (1 - y) * np.log(1 - p + 1e-15)))
        rnd = prec[Fx.shape[1]:]
        lap = ll - 0.5 * float(np.sum(rnd * b[Fx.shape[1]:] ** 2)) + 0.5 * float(np.sum(np.log(rnd))) - 0.5 * np.linalg.slogdet(H)[1]
        return b, H, lap

    taus = [0.5] * len(factors)
    for _ in range(2):
        for j in range(len(factors)):
            best = None
            for t in grid:
                tt = list(taus)
                tt[j] = t
                lap = fit(tt)[2]
                if best is None or lap > best[0]:
                    best = (lap, t)
            taus[j] = best[1]
    b, H, lap = fit(taus)
    return {"coef": b, "cov": np.linalg.inv(H), "taus": taus, "levels": levels, "kx": Fx.shape[1], "sizes": sizes}


def mrp_predict(fit: dict, factors: list, X=None, draws: int = 0, rng: np.random.Generator | None = None):
    """Predicted probabilities for new rows (cells); with ``draws``, also a matrix of draws from the approximate
    posterior (normal at the mode), for intervals of poststratified totals."""
    n = len(factors[0])
    Fx = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), np.asarray(X, float)])
    blocks = [(np.asarray(f)[:, None] == lv[None, :]).astype(float) for f, lv in zip(factors, fit["levels"])]
    D = np.column_stack([Fx] + blocks)
    p = 1 / (1 + np.exp(-(D @ fit["coef"])))
    if not draws:
        return p
    rng = rng or np.random.default_rng(0)
    L = np.linalg.cholesky(fit["cov"] + 1e-10 * np.eye(len(fit["coef"])))
    B = fit["coef"][:, None] + L @ rng.standard_normal((len(fit["coef"]), draws))
    return p, 1 / (1 + np.exp(-(D @ B)))


# ---------------------------------------------------------------------------------------------------------------
# Measurement error and misclassification
# ---------------------------------------------------------------------------------------------------------------
def disattenuate(r_xy: float, rel_x: float, rel_y: float = 1.0) -> float:
    """Spearman (1904): the correlation between true scores is r_xy / sqrt(rel_x rel_y)."""
    return r_xy / math.sqrt(rel_x * rel_y)


def simex(w, y, sigma_u2: float, Z=None, lambdas=(0.5, 1.0, 1.5, 2.0), B: int = 200, rng: np.random.Generator | None = None) -> dict:
    """SIMEX (Cook & Stefanski 1994) for the slope of y on an error-prone w (error variance ``sigma_u2``): add extra
    noise of variance lambda sigma_u2, refit, average over B draws, and extrapolate the slope as a quadratic in lambda
    back to lambda = -1, where the measurement error would vanish."""
    rng = rng or np.random.default_rng(0)
    w, y = np.asarray(w, float), np.asarray(y, float)
    n = len(w)
    Zm = np.zeros((n, 0)) if Z is None else np.asarray(Z, float).reshape(n, -1)

    def slope(x):
        D = np.column_stack([np.ones(n), x, Zm])
        return float(np.linalg.lstsq(D, y, rcond=None)[0][1])

    lam = [0.0] + list(lambdas)
    est = [slope(w)]
    for l_ in lambdas:
        est.append(float(np.mean([slope(w + math.sqrt(l_ * sigma_u2) * rng.standard_normal(n)) for _ in range(B)])))
    c = np.polyfit(lam, est, 2)
    return {"lambda": np.array(lam), "slope": np.array(est), "coef": c, "simex": float(np.polyval(c, -1.0)), "naive": est[0]}


def misclass_correct(a: float, b: float, c: float, d: float, se: float, sp: float) -> dict:
    """Correct a 2 x 2 table of exposure (rows: cases a, b = exposed, unexposed; controls c, d) for nondifferential
    exposure misclassification with sensitivity ``se`` and specificity ``sp``: the true exposed count among n is
    (observed exposed - (1 - sp) n) / (se + sp - 1).  Returns the corrected counts and odds ratios."""
    def fix(e, u):
        n = e + u
        te = (e - (1 - sp) * n) / (se + sp - 1)
        return te, n - te

    A, Bc = fix(a, b)
    C, Dd = fix(c, d)
    return {"table": (A, Bc, C, Dd), "or_observed": a * d / (b * c), "or_corrected": A * Dd / (Bc * C)}
