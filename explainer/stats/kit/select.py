"""statkit.select: choosing models without fooling yourself (Part 28 of *Statistics, Built*).

    from explainer.stats.kit import select as Se
    Se.aic(ll, k), Se.bic(ll, k, n), Se.press(X, y), Se.best_subset(X, y), Se.psis_loo(loglik), Se.stacking_weights(lpd)

Information criteria (AIC, AICc, BIC, Mallows's Cp, TIC); leave-one-out shortcuts for linear smoothers (PRESS, GCV);
degrees of freedom by Monte Carlo covariance (Efron 2004); Freedman's (1983) screening paradox; exhaustive best-subset
and forward stepwise selection; Bayesian leave-one-out by Pareto-smoothed importance sampling and WAIC (Vehtari,
Gelman & Gabry 2017; Watanabe 2010); stacking and BMA weights (Yao, Vehtari, Simpson & Gelman 2018); the normalized
maximum likelihood regret of a Bernoulli sequence (Shtarkov 1987).  Checked in ``tests/test_stats_kit_select.py``.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy import optimize, special, stats

from explainer.stats.kit import ppl as _ppl


# ---------------------------------------------------------------------------------------------------------------
# Criteria
# ---------------------------------------------------------------------------------------------------------------
def gaussian_ll(rss: float, n: int) -> float:
    """The maximized normal log likelihood of a linear model with sigma^2 = rss/n."""
    return float(-0.5 * n * (np.log(2 * np.pi * rss / n) + 1))


def aic(ll: float, k: int) -> float:
    return float(-2 * ll + 2 * k)


def aicc(ll: float, k: int, n: int) -> float:
    return float(aic(ll, k) + 2 * k * (k + 1) / (n - k - 1))


def bic(ll: float, k: int, n: int) -> float:
    return float(-2 * ll + k * np.log(n))


def cp(rss: float, k: int, sigma2: float, n: int) -> float:
    """Mallows's Cp on the mean-squared-error scale: training error plus the optimism 2 k sigma^2 / n."""
    return float(rss / n + 2 * k * sigma2 / n)


def tic_penalty(scores: np.ndarray, hessian: np.ndarray) -> float:
    """Takeuchi's penalty tr(J K^-1): J the mean outer product of per-observation scores, K the mean negative Hessian;
    it equals k when the model is correct."""
    s = np.atleast_2d(np.asarray(scores, float))
    n = s.shape[0]
    J = s.T @ s / n
    K = -np.asarray(hessian, float) / n
    return float(np.trace(J @ np.linalg.inv(K)))


# ---------------------------------------------------------------------------------------------------------------
# Leave-one-out for linear smoothers; degrees of freedom
# ---------------------------------------------------------------------------------------------------------------
def hat_matrix(X) -> np.ndarray:
    X = np.asarray(X, float)
    Q, _ = np.linalg.qr(X)
    return Q @ Q.T


def press(X, y) -> float:
    """Mean squared LOO error of OLS without refitting: residual_i / (1 - h_ii)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    H = hat_matrix(X)
    e = y - H @ y
    return float(np.mean((e / (1 - np.diag(H))) ** 2))


def gcv(rss: float, df: float, n: int) -> float:
    """Generalized cross-validation (Craven & Wahba 1979): (rss/n) / (1 - df/n)^2."""
    return float(rss / n / (1 - df / n) ** 2)


def df_monte_carlo(fit_predict, X, mu, sigma: float, R: int, rng: np.random.Generator) -> float:
    """Efron's (2004) covariance degrees of freedom: sum_i cov(yhat_i, y_i) / sigma^2, estimated by simulating
    y = mu + N(0, sigma^2)."""
    mu = np.asarray(mu, float)
    Y = mu + sigma * rng.standard_normal((R, len(mu)))
    Yh = np.array([fit_predict(X, y) for y in Y])
    cov = np.mean((Yh - Yh.mean(0)) * (Y - Y.mean(0)), axis=0) * R / (R - 1)
    return float(cov.sum() / sigma ** 2)


# ---------------------------------------------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------------------------------------------
def _ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    return b, float(r @ r)


def freedman(n: int, p: int, rng: np.random.Generator, alpha: float = 0.25) -> dict:
    """Freedman's (1983) paradox: regress pure noise y on p pure-noise columns; keep the columns with p-values below
    alpha; refit with only those.  The second regression looks significant."""
    X = rng.standard_normal((n, p))
    y = rng.standard_normal(n)
    out = {}
    for stage, cols in (("first", np.arange(p)), ("second", None)):
        if cols is None:
            cols = np.flatnonzero(out["first"]["p"] < alpha)
        Xd = np.column_stack([np.ones(n), X[:, cols]])
        b, rss = _ols(Xd, y)
        k = Xd.shape[1]
        s2 = rss / (n - k)
        se = np.sqrt(np.diag(np.linalg.inv(Xd.T @ Xd)) * s2)
        t = b / se
        pv = 2 * stats.t.sf(np.abs(t), n - k)
        tss = float(np.sum((y - y.mean()) ** 2))
        r2 = 1 - rss / tss
        F = (r2 / (k - 1)) / ((1 - r2) / (n - k))
        out[stage] = {"cols": cols, "p": pv[1:], "r2": r2, "F": F, "pF": float(stats.f.sf(F, k - 1, n - k)),
                      "n_sig05": int(np.sum(pv[1:] < 0.05)), "n_sig25": int(np.sum(pv[1:] < 0.25))}
    return out


def best_subset(X, y, max_size: int | None = None) -> list[dict]:
    """Exhaustive search (an intercept always included): for each size, the subset with the smallest RSS."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    best = []
    one = np.ones((n, 1))
    for k in range(0, (max_size if max_size is not None else p) + 1):
        bk = None
        for S in combinations(range(p), k):
            Xd = np.column_stack([one, X[:, list(S)]]) if S else one
            _, rss = _ols(Xd, y)
            if bk is None or rss < bk["rss"]:
                bk = {"size": k, "subset": list(S), "rss": rss}
        best.append(bk)
    return best


def forward_stepwise(X, y) -> list[dict]:
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    active, path = [], []
    one = np.ones((n, 1))
    _, rss = _ols(one, y)
    path.append({"size": 0, "subset": [], "rss": rss})
    while len(active) < p:
        cand = [(j, _ols(np.column_stack([one, X[:, active + [j]]]), y)[1]) for j in range(p) if j not in active]
        j, rss = min(cand, key=lambda t: t[1])
        active = active + [j]
        path.append({"size": len(active), "subset": list(active), "rss": rss})
    return path


# ---------------------------------------------------------------------------------------------------------------
# Bayesian LOO and WAIC
# ---------------------------------------------------------------------------------------------------------------
def psis_loo(loglik) -> dict:
    """``loglik``: S draws x n observations of log p(y_i | theta_s).  Pareto-smoothed importance-sampling LOO:
    elpd_loo, its SE, p_loo, and each observation's k-hat."""
    L = np.asarray(loglik, float)
    S, n = L.shape
    lpd = special.logsumexp(L, axis=0) - np.log(S)
    elpd_i, khat = np.empty(n), np.empty(n)
    for i in range(n):
        w, k = _ppl.psis(-L[:, i])
        elpd_i[i] = np.log(np.sum(w * np.exp(L[:, i] - L[:, i].max()))) + L[:, i].max()
        khat[i] = k
    return {"elpd": float(elpd_i.sum()), "se": float(np.sqrt(n * elpd_i.var())), "p_loo": float(lpd.sum() - elpd_i.sum()),
            "elpd_i": elpd_i, "khat": khat, "lpd": float(lpd.sum())}


def waic(loglik) -> dict:
    """Watanabe's widely applicable information criterion on the elpd scale: lpd - sum_i Var_s log p(y_i | theta_s)."""
    L = np.asarray(loglik, float)
    S = L.shape[0]
    lpd_i = special.logsumexp(L, axis=0) - np.log(S)
    p_i = L.var(axis=0, ddof=1)
    return {"elpd": float((lpd_i - p_i).sum()), "p_waic": float(p_i.sum()), "elpd_i": lpd_i - p_i}


def stacking_weights(lpd) -> np.ndarray:
    """Yao et al. (2018): weights on the simplex maximizing sum_i log sum_k w_k exp(lpd[i, k]), where lpd[i, k] is the
    LOO log predictive density of observation i under model k."""
    lpd = np.asarray(lpd, float)
    n, K = lpd.shape
    m = lpd.max(axis=1, keepdims=True)
    P_ = np.exp(lpd - m)

    def neg(z):
        w = special.softmax(np.r_[0.0, z])
        return -np.sum(np.log(P_ @ w + 1e-300))

    r = optimize.minimize(neg, np.zeros(K - 1), method="BFGS")
    return special.softmax(np.r_[0.0, r.x])


def bma_weights(log_evidence, prior=None) -> np.ndarray:
    le = np.asarray(log_evidence, float)
    lp = le + (0.0 if prior is None else np.log(np.asarray(prior, float)))
    return special.softmax(lp)


def nml_bernoulli_regret(n: int) -> float:
    """Shtarkov's complexity log sum_k C(n, k) (k/n)^k (1 - k/n)^(n-k), about (1/2) log(n pi / 2)."""
    k = np.arange(n + 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        lt = (special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)
              + np.where(k > 0, k * np.log(np.maximum(k, 1) / n), 0.0)
              + np.where(k < n, (n - k) * np.log(np.maximum(n - k, 1) / n), 0.0))
    return float(special.logsumexp(lt))
