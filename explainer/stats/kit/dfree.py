"""statkit.dfree: distribution-free inference and its limits (Part 57 of *Statistics, Built*).

    the Bahadur-Savage family: the t-interval driven to zero coverage          (Bahadur & Savage 1956)
    the quantile lemma's exact coverage                                         (Vovk et al. 2005)
    full conformal for ridge regression, by a grid of candidate labels          (Vovk et al. 2005)
    jackknife, jackknife+ and their coverage for an unstable fit                (Barber et al. 2021)
    conditional coverage by bins, and group-conditional calibration             (Vovk 2012; Gibbs, Cherian & Candes 2023)
    nonexchangeable conformal with fixed weights                                (Barber, Candes, Ramdas & Tibshirani 2023)
    conformal risk control                                                      (Angelopoulos et al. 2024)
    conformal outlier p-values and BH                                           (Bates et al. 2023)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

# ------------------------------------------------------------------------------------------------ Bahadur-Savage


def bahadur_savage_coverage(n: int, eps: float, shift: float = 3.0, alpha: float = 0.05) -> dict:
    """The mixture (1 - eps) N(0, 1) + eps delta_{shift/eps}: its mean is exactly ``shift``, whatever eps.  The
    t-interval covers the mean only if the sample contains at least one atom (and even then not always); exactly,
    P(no atom) = (1 - eps)^n, so coverage <= 1 - (1 - eps)^n + (1 - eps)^n P(t-interval of N(0,1) data covers shift)."""
    p_none = (1 - eps) ** n
    z = stats.t.ppf(1 - alpha / 2, n - 1)
    # with no atom, the data are N(0,1): the interval covers 'shift' with probability P(|xbar - shift| <= z s / sqrt n),
    # negligible for shift >= 1 and moderate n; bound it by the normal approximation
    cov_none = float(stats.norm.cdf(z - shift * math.sqrt(n)) - stats.norm.cdf(-z - shift * math.sqrt(n)))
    return {"p_none": p_none, "upper": float(1 - p_none + p_none * cov_none), "mean": shift}


def bahadur_savage_sim(n: int, eps: float, rng: np.random.Generator, shift: float = 3.0, reps: int = 4000,
                       alpha: float = 0.05) -> float:
    """Simulated coverage of the t-interval for the mean of the Bahadur-Savage mixture."""
    M = shift / eps
    X = rng.standard_normal((reps, n))
    atom = rng.random((reps, n)) < eps
    X[atom] = M
    m, s = X.mean(1), X.std(1, ddof=1)
    z = stats.t.ppf(1 - alpha / 2, n - 1)
    return float(np.mean(np.abs(m - shift) <= z * s / math.sqrt(n)))


# ---------------------------------------------------------------------------------------- the quantile lemma


def quantile_lemma_coverage(n: int, alpha: float) -> dict:
    """Split conformal with n calibration scores (continuous, exchangeable): coverage is exactly k/(n + 1),
    k = ceil((n + 1)(1 - alpha)), between 1 - alpha and 1 - alpha + 1/(n + 1)."""
    k = math.ceil((n + 1) * (1 - alpha))
    return {"k": k, "exact": min(1.0, k / (n + 1)), "lower": 1 - alpha, "upper": 1 - alpha + 1 / (n + 1)}


def conformal_coverage_law(n: int, alpha: float) -> dict:
    """The conditional coverage given the calibration set, P(Y in C | calibration), is Beta(k, n + 1 - k) distributed
    (Vovk 2012): its mean is the marginal coverage; its spread shows why one calibration set can miss."""
    k = math.ceil((n + 1) * (1 - alpha))
    a, b = k, n + 1 - k
    return {"a": a, "b": b, "mean": a / (a + b), "q05": float(stats.beta.ppf(0.05, a, b)), "q95": float(stats.beta.ppf(0.95, a, b))}


# ----------------------------------------------------------------------------------------------- full conformal


def ridge_fit_predict(X, y, Xnew, lam: float):
    X, y, Xnew = np.asarray(X, float), np.asarray(y, float), np.asarray(Xnew, float)
    p = X.shape[1]
    b = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)
    return Xnew @ b


def full_conformal_ridge(X, y, x_new, lam: float, alpha: float = 0.1, grid=None) -> dict:
    """Full conformal prediction set for ridge regression at x_new: every candidate y' whose absolute residual, after
    refitting on all n + 1 points, is not among the alpha largest.  Computed on a grid of candidates."""
    X, y, x_new = np.asarray(X, float), np.asarray(y, float), np.asarray(x_new, float)
    n = len(y)
    if grid is None:
        sd = np.std(y)
        grid = np.linspace(y.min() - 3 * sd, y.max() + 3 * sd, 801)
    Xa = np.vstack([X, x_new])
    H = Xa @ np.linalg.solve(Xa.T @ Xa + lam * np.eye(X.shape[1]), Xa.T)  # the hat matrix of the augmented fit
    keep = []
    for c in grid:
        ya = np.r_[y, c]
        r = np.abs(ya - H @ ya)
        keep.append(np.sum(r >= r[-1]) / (n + 1) > alpha)
    keep = np.asarray(keep)
    ins = grid[keep]
    return {"grid": grid, "keep": keep, "lo": float(ins.min()) if len(ins) else np.nan, "hi": float(ins.max()) if len(ins) else np.nan}


# ------------------------------------------------------------------------------------------------- jackknife+


def jackknife_intervals(fit_predict, X, y, Xtest, alpha: float = 0.1) -> dict:
    """The naive jackknife (full-fit prediction +- the (1 - alpha) quantile of leave-one-out residuals) and the
    jackknife+ (Barber et al. 2021) for every test point."""
    X, y, Xt = np.asarray(X, float), np.asarray(y, float), np.asarray(Xtest, float)
    n = len(y)
    loo = np.zeros(n)
    mt = np.zeros((n, len(Xt)))
    for i in range(n):
        m = np.ones(n, bool)
        m[i] = False
        both = fit_predict(X[m], y[m], np.vstack([X[i:i + 1], Xt]))
        loo[i] = abs(y[i] - both[0])
        mt[i] = both[1:]
    full = fit_predict(X, y, Xt)
    k = math.ceil((n + 1) * (1 - alpha))
    q = np.sort(loo)[k - 1] if k <= n else np.inf
    lo_p = -np.sort(-(mt - loo[:, None]), axis=0)[k - 1] if k <= n else np.full(len(Xt), -np.inf)
    hi_p = np.sort(mt + loo[:, None], axis=0)[k - 1] if k <= n else np.full(len(Xt), np.inf)
    return {"jack_lo": full - q, "jack_hi": full + q, "plus_lo": lo_p, "plus_hi": hi_p}


def min_norm_fit_predict(X, y, Xnew):
    """Minimum-norm least squares: an interpolating, unstable algorithm when p >= n (Part 54's double descent)."""
    b = np.linalg.pinv(np.asarray(X, float)) @ np.asarray(y, float)
    return np.asarray(Xnew, float) @ b


# ----------------------------------------------------------------------------------------- conditional coverage


def binned_coverage(x, covered, bins) -> dict:
    """Coverage within bins of a covariate: conditional coverage, estimated."""
    x, c = np.asarray(x, float), np.asarray(covered, float)
    idx = np.digitize(x, bins) - 1
    out = []
    for b in range(len(bins) - 1):
        m = idx == b
        out.append(float(c[m].mean()) if m.any() else np.nan)
    return {"mid": (np.asarray(bins[:-1]) + np.asarray(bins[1:])) / 2, "coverage": np.asarray(out)}


def gcc_group_threshold(scores, groups_cal, groups_test_row, alpha: float = 0.1) -> float:
    """Gibbs, Cherian & Candes (2023) for the class of group indicators (overlapping groups allowed): the threshold
    for a test point is the largest S such that S is at most the fitted (1 - alpha) quantile regression of the scores
    on the group indicators, refitted with the test point's (features, S) added.  For finite classes the regression
    is a linear programme; computed here by bisection on S with scipy's LP."""
    s = np.asarray(scores, float)
    G = np.asarray(groups_cal, float)
    g = np.asarray(groups_test_row, float)
    tau = 1 - alpha

    def fitted(S):
        Xa = np.vstack([G, g])
        ya = np.r_[s, S]
        n, d = Xa.shape
        # min sum tau u + (1 - tau) v, Xa b + u - v = ya, u, v >= 0
        c = np.r_[np.zeros(d), tau * np.ones(n), (1 - tau) * np.ones(n)]
        A = np.hstack([Xa, np.eye(n), -np.eye(n)])
        res = optimize.linprog(c, A_eq=A, b_eq=ya, bounds=[(None, None)] * d + [(0, None)] * (2 * n), method="highs")
        return float(g @ res.x[:d])

    lo, hi = float(np.min(s)) - 1.0, float(np.max(s)) + 1.0
    if fitted(hi) >= hi:
        return np.inf
    for _ in range(30):
        mid = (lo + hi) / 2
        if mid <= fitted(mid):
            lo = mid
        else:
            hi = mid
    return lo


# ------------------------------------------------------------------------------------------- nonexchangeable


def nexcp_threshold(scores, weights, alpha: float = 0.1) -> float:
    """Nonexchangeable conformal (Barber, Candes, Ramdas & Tibshirani 2023): the (1 - alpha) quantile of the scores
    weighted by fixed weights w_i (normalized together with a unit weight at +inf for the test point).  Coverage is at
    least 1 - alpha - sum_i w~_i d_TV(Z, Z^i)."""
    s, w = np.asarray(scores, float), np.asarray(weights, float)
    o = np.argsort(s)
    s, w = s[o], w[o]
    tot = w.sum() + 1.0
    cw = np.cumsum(w) / tot
    i = np.searchsorted(cw, 1 - alpha)
    return float(s[i]) if i < len(s) else float("inf")


# ------------------------------------------------------------------------------------------------- risk control


def conformal_risk_control(loss_matrix, lambdas, alpha: float, B: float = 1.0) -> float:
    """Angelopoulos, Bates, Fisch, Lei & Schuster (2024): with losses L_i(lambda) in [0, B], nonincreasing in lambda,
    choose lambda_hat = inf{lambda: (n R_n(lambda) + B)/(n + 1) <= alpha}; then E L_{n+1}(lambda_hat) <= alpha."""
    L = np.asarray(loss_matrix, float)
    n = L.shape[0]
    risk = (L.sum(0) + B) / (n + 1)
    ok = np.flatnonzero(risk <= alpha)
    return float(lambdas[ok[0]]) if len(ok) else float(lambdas[-1])


# ---------------------------------------------------------------------------------------- outlier detection


def outlier_pvalues(cal_scores, test_scores) -> np.ndarray:
    """Conformal p-values for outlier detection (Bates, Candes, Lei, Romano & Sesia 2023): larger scores are more
    outlying; p_j = (1 + #{cal >= s_j}) / (n + 1), marginally super-uniform for inliers and PRDS across test points."""
    c = np.sort(np.asarray(cal_scores, float))
    t = np.asarray(test_scores, float)
    ge = len(c) - np.searchsorted(c, t, side="left")
    return (1 + ge) / (len(c) + 1)
