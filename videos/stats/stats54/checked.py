"""Part-local numerical repairs; shared historical kit stays reproducible."""
from __future__ import annotations

import math
import numpy as np
from scipy.optimize import linprog
from scipy.special import expit, xlogy
from explainer.stats.kit import slt as SL


def separator(pts, labels):
    pts, lab = np.asarray(pts, float), np.asarray(labels, bool)
    if lab.all() or not lab.any():
        w = np.array([1., 0.])
        return w, float((pts @ w).min() - 1 if lab.all() else (pts @ w).max() + 1)
    signs = 2 * lab.astype(float) - 1
    A = signs[:, None] * np.column_stack([pts, -np.ones(len(pts))])
    fit = linprog(np.zeros(3), A_ub=-A, b_ub=-np.ones(len(pts)), bounds=[(None, None)] * 3, method="highs")
    if not fit.success:
        if fit.status != 2:
            raise RuntimeError(fit.message)
        return None, 0.
    w, b = fit.x[:2], fit.x[2]
    norm = np.linalg.norm(w)
    if not np.all(signs * (pts @ w - b) >= 1 - 1e-7):
        raise ArithmeticError("separator failed margin check")
    return w / norm, float(b / norm)


def threshold_values(x, y, ts, side="right"):
    order = np.argsort(x)
    xs, ys = np.asarray(x)[order], np.asarray(y)[order]
    prefix = np.r_[0, np.cumsum(2 * ys - 1)]
    return (np.sum(ys == 0) + prefix[np.searchsorted(xs, ts, side=side)]) / len(xs)


def erm_threshold(x, y):
    ts = np.unique(np.r_[0., x, 1.])
    return float(ts[np.argmin(threshold_values(x, y, ts))])


def uniform_deviation_threshold(x, y, t0=.5, eta=.1):
    """Exact supremum, including both limits at every grouped sample jump."""
    ts = np.unique(np.r_[0., x, t0, 1.])
    right = np.abs(threshold_values(x, y, ts) - SL.threshold_risk(ts, t0, eta))
    left_ts = ts[ts > 0]
    left = np.abs(threshold_values(x, y, left_ts, "left") - SL.threshold_risk(left_ts, t0, eta))
    return float(max(right.max(), left.max(initial=0)))


def best_stump(X, y, weights):
    best = (np.inf, 0, 0., 1)
    total = float(np.sum(weights))
    for j in range(X.shape[1]):
        order = np.argsort(X[:, j], kind="stable")
        xs, ys, ws = X[order, j], y[order], weights[order]
        cuts = np.r_[0, np.flatnonzero(np.diff(xs) > 0) + 1, len(xs)]
        err = np.sum(ws[ys < 0]) + np.r_[0., np.cumsum(ws * np.where(ys > 0, 1., -1.))]
        for sign, errors in ((1, err), (-1, total - err)):
            i = int(cuts[np.argmin(errors[cuts])])
            if errors[i] < best[0]:
                threshold = -np.inf if i == 0 else float(xs[i - 1])
                best = (float(errors[i]), j, threshold, sign)
    actual = float(weights @ (SL.stump_predict(X, *best[1:]) != y))
    if not math.isclose(actual, best[0], abs_tol=1e-12):
        raise ArithmeticError("stump error disagrees with prediction")
    return (actual, *best[1:])


def adaboost(X, y, T, Xte, yte):
    weights = np.full(len(y), 1 / len(y))
    F, Ft = np.zeros(len(y)), np.zeros(len(yte))
    tr, te, margins, errors, alphas = [], [], {}, [], []
    for t in range(1, T + 1):
        error, j, threshold, sign = best_stump(X, y, weights)
        # A perfect stump gives a finite display score; this only matters at machine endpoints.
        e = np.clip(error, 1e-15, 1 - 1e-15)
        alpha = .5 * np.log((1 - e) / e)
        h = SL.stump_predict(X, j, threshold, sign)
        F += alpha * h
        Ft += alpha * SL.stump_predict(Xte, j, threshold, sign)
        weights *= np.exp(-alpha * y * h)
        weights /= weights.sum()
        alphas.append(float(alpha)); errors.append(error)
        tr.append(float(np.mean(np.where(F >= 0, 1., -1.) != y)))
        te.append(float(np.mean(np.where(Ft >= 0, 1., -1.) != yte)))
        if t in (5, 50, 500, T):
            margins[t] = y * F / max(np.sum(np.abs(alphas)), np.finfo(float).tiny)
    return dict(train=tr, test=te, margins=margins, weighted_errors=errors, alphas=alphas)


def kl_bernoulli(q, p):
    if not 0 <= q <= 1 or not 0 <= p <= 1:
        raise ValueError("Bernoulli probabilities must be in [0,1]")
    if p == 0: return 0. if q == 0 else np.inf
    if p == 1: return 0. if q == 1 else np.inf
    return float(xlogy(q, q / p) + xlogy(1 - q, (1 - q) / (1 - p)))


def kl_inverse(q, c):
    if not 0 <= q <= 1 or c < 0: raise ValueError("invalid KL inversion")
    if q == 0: return float(-np.expm1(-c))
    if q == 1: return 1.
    lo, hi = q, 1.
    for _ in range(80):
        mid = (lo + hi) / 2
        if kl_bernoulli(q, mid) > c: hi = mid
        else: lo = mid
    return lo


def mcse(values):
    return float(np.std(values, ddof=1) / np.sqrt(len(values)))


def sgd_divergence(X, y, steps, lr, rng, reps=40):
    if lr > 8 or np.max(np.linalg.norm(X, axis=1)) > 1 + 1e-12:
        raise ValueError("nonexpansive logistic update assumptions failed")
    n, p = X.shape
    paths, visits = [], []
    for _ in range(reps):
        i0 = int(rng.integers(n))
        X2, y2 = X.copy(), y.copy()
        z = rng.standard_normal(p)
        X2[i0], y2[i0] = z / max(1., np.linalg.norm(z)), -y[i0]
        w, w2 = np.zeros(p), np.zeros(p)
        indices = rng.integers(n, size=steps)
        path = []
        for i in indices:
            w += lr * y[i] * X[i] * expit(-y[i] * (X[i] @ w))
            w2 += lr * y2[i] * X2[i] * expit(-y2[i] * (X2[i] @ w2))
            path.append(np.linalg.norm(w - w2))
        paths.append(path); visits.append(np.cumsum(indices == i0))
    paths, visits = np.asarray(paths), np.asarray(visits)
    if np.any(paths > 2 * lr * visits + 1e-10):
        raise ArithmeticError("pathwise changed-index bound failed")
    return dict(divergence=paths.mean(0), mcse=paths.std(0, ddof=1) / np.sqrt(reps),
                paths=paths, changed_visits=visits, bound=2 * lr * np.arange(1, steps + 1) / n)


def expected_min_norm_risk(n, p, p_total=1000, sigma=.5):
    """Unconditional excess latent prediction risk, isotropic Gaussian design."""
    omitted, included = 1 - p / p_total, p / p_total
    if abs(p - n) <= 1: return np.inf
    if p < n: return omitted + (sigma**2 + omitted) * p / (n - p - 1)
    return omitted + (1 - n / p) * included + (sigma**2 + omitted) * n / (p - n - 1)


def benign_risk(n, rng, k=5, p_tail=20000, tail_var=.0005, sigma=.5, reps=4):
    risks, train = [], []
    for _ in range(reps):
        X = np.column_stack([rng.standard_normal((n, k)), np.sqrt(tail_var) * rng.standard_normal((n, p_tail))])
        beta = np.r_[np.ones(k), np.zeros(p_tail)]
        y = X @ beta + sigma * rng.standard_normal(n)
        # Full-row-rank Gaussian design: the dual solve is the minimum-norm solution.
        fit = X.T @ np.linalg.solve(X @ X.T, y)
        error = beta - fit
        risks.append(float(error[:k] @ error[:k] + tail_var * (error[k:] @ error[k:])))
        train.append(float(np.mean((X @ fit - y)**2)))
    if max(train) > 1e-18:
        raise ArithmeticError("claimed interpolator has nonzero residual")
    return dict(excess=float(np.mean(risks)), noise=sigma**2, samples=risks, mcse=mcse(risks),
                train_mse=train, tail_effective_rank=p_tail, tail_total_variance=p_tail * tail_var)
