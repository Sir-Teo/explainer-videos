"""statkit.thesis (Part 65): the dissertation's code.

The question: weighted conformal prediction (Tibshirani, Barber, Candes & Ramdas 2019) keeps its coverage under
covariate shift when the likelihood ratio w = dQ/dP is known. In practice w is estimated. How much coverage is lost?

The theorem proved in the part: if the weights w_hat are fixed (estimated on data independent of the calibration
set), the weighted split-conformal interval covers a test point from the target Q with probability at least
1 - alpha - TV(P_w_hat, Q), where P_w_hat is the source P reweighted by w_hat.  For a Gaussian mean shift
P = N(0, 1), Q = N(mu, 1) and tempered weights w^lam (the estimate of an over-regularized classifier), P_w_hat is
N(lam mu, 1) and the bound is 1 - alpha - (2 Phi(|1 - lam| |mu| / 2) - 1).

This module holds the simulation study's data-generating mechanism and methods, the bound, the weight estimators,
and the NHANES application with a known, designed selection."""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.stats.kit.conformal import weighted_quantile_conformal


def tv_gauss_shift(a: float, b: float) -> float:
    """TV(N(a, 1), N(b, 1)) = 2 Phi(|a - b| / 2) - 1."""
    return float(2 * stats.norm.cdf(abs(a - b) / 2) - 1)


def coverage_bound(alpha: float, mu: float, lam: float) -> float:
    """The theorem's lower bound for tempered Gaussian-tilt weights w^lam: 1 - alpha - TV(N(lam mu, 1), N(mu, 1))."""
    return 1 - alpha - tv_gauss_shift(lam * mu, mu)


def tv_reweighted(w_fn, mu: float, grid=None) -> float:
    """TV(P_w, Q) on a fine grid, where P_w has density w(x) phi(x) / int w phi (the source N(0, 1) reweighted by w)
    and Q = N(mu, 1): the theorem's penalty for any fixed weight function in one dimension."""
    x = np.linspace(-10, 10 + abs(mu), 20001) if grid is None else np.asarray(grid, float)
    dx = x[1] - x[0]
    pw = np.asarray(w_fn(x), float) * stats.norm.pdf(x)
    pw /= pw.sum() * dx
    q = stats.norm.pdf(x, mu)
    return float(0.5 * np.sum(np.abs(pw - q)) * dx)


def mean_fn(x):
    return np.sin(np.asarray(x, float)) + 0.5 * np.asarray(x, float)


def sd_fn(x, gamma: float):
    return np.exp(gamma * np.asarray(x, float))


def draw(n: int, mu: float, gamma: float, rng: np.random.Generator) -> tuple:
    """n pairs with X ~ N(mu, 1) and Y = sin X + X/2 + exp(gamma X) eps: the noise grows with x, so the scores
    |Y - m(X)| depend on where X falls, and a shift in X moves the score distribution."""
    x = mu + rng.standard_normal(n)
    y = mean_fn(x) + sd_fn(x, gamma) * rng.standard_normal(n)
    return x, y


def logistic_weights(x_src, x_tgt, ridge: float = 0.0, degree: int = 1):
    """Estimate dQ/dP by a probabilistic classifier (Part 60): logistic regression of 'target' on polynomial features
    of x, fitted by Newton with an optional ridge penalty (a large ridge shrinks the log ratio towards zero, which
    tempers the weights).  Returns a function x -> w_hat(x), the odds times n_src / n_tgt."""
    xs, xt = np.asarray(x_src, float), np.asarray(x_tgt, float)
    X = np.concatenate([xs, xt])
    F = np.column_stack([X ** k for k in range(degree + 1)])
    y = np.concatenate([np.zeros(len(xs)), np.ones(len(xt))])
    b = np.zeros(F.shape[1])
    pen = ridge * np.eye(F.shape[1])
    pen[0, 0] = 0.0
    for _ in range(50):
        p = 1 / (1 + np.exp(-F @ b))
        H = (F * (p * (1 - p))[:, None]).T @ F + pen
        g = F.T @ (y - p) - pen @ b
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    ratio = len(xs) / len(xt)

    def w(x):
        Fx = np.column_stack([np.asarray(x, float) ** k for k in range(degree + 1)])
        return np.exp(Fx @ b) * ratio
    w.coef = b
    return w


def weighted_interval(x_cal, y_cal, w_fn, x_test, alpha: float) -> np.ndarray:
    """Weighted split-conformal half-widths for absolute-residual scores around the known mean m(x): for each test
    point, the weighted (1 - alpha) quantile of the calibration scores with the test point's weight at +inf.
    ``w_fn = None`` gives ordinary split conformal."""
    s = np.abs(np.asarray(y_cal) - mean_fn(x_cal))
    if w_fn is None:
        n = len(s)
        k = math.ceil((n + 1) * (1 - alpha))
        q = np.inf if k > n else np.sort(s)[k - 1]
        return np.full(len(x_test), q)
    wc = w_fn(x_cal)
    wt = w_fn(x_test)
    return np.array([weighted_quantile_conformal(s, wc, float(v), alpha) for v in wt])


def one_run(n_cal: int, n_tgt: int, mu: float, gamma: float, alpha: float, method: str, rng: np.random.Generator,
            n_test: int = 200, lam: float = 0.5) -> dict:
    """One replicate of the study: a calibration set from the source, a test set from the target, and an unlabelled
    target sample of size n_tgt for estimating weights (independent of the calibration set).  Returns the coverage
    over the test set and the mean half-width."""
    xc, yc = draw(n_cal, 0.0, gamma, rng)
    xt, yt = draw(n_test, mu, gamma, rng)
    if method == "none":
        w = None
    elif method == "oracle":
        w = lambda x: np.exp(mu * np.asarray(x) - mu * mu / 2)  # noqa: E731
    elif method == "tempered":
        w = lambda x: np.exp(lam * (mu * np.asarray(x) - mu * mu / 2))  # noqa: E731
    elif method == "estimated":
        xs_u = rng.standard_normal(n_tgt)
        xt_u = mu + rng.standard_normal(n_tgt)
        w = logistic_weights(xs_u, xt_u)
    elif method == "misspecified":
        # a classifier that sees only |x|: it cannot represent a shift in the mean
        xs_u = rng.standard_normal(n_tgt)
        xt_u = mu + rng.standard_normal(n_tgt)
        w0 = logistic_weights(np.abs(xs_u), np.abs(xt_u))
        w = lambda x: w0(np.abs(np.asarray(x)))  # noqa: E731
    else:
        raise ValueError(method)
    h = weighted_interval(xc, yc, w, xt, alpha)
    cov = np.abs(yt - mean_fn(xt)) <= h
    bound = 1 - alpha - tv_reweighted(w if w is not None else (lambda x: np.ones_like(np.asarray(x, float))), mu)
    fin = np.isfinite(h)
    return {"coverage": float(cov.mean()), "width": float(np.median(2 * h[fin])) if fin.any() else float("inf"),
            "inf": float(np.mean(~fin)), "bound": bound}


def study(mus, gammas, methods, reps: int, n_cal: int, n_tgt: int, alpha: float, rng: np.random.Generator) -> list:
    """The preregistered simulation: every (mu, gamma, method) cell, ``reps`` replicates; coverage with its Monte Carlo
    SE, the median finite width, the fraction of infinite intervals, and the theorem's bound (averaged over runs)."""
    out = []
    for mu in mus:
        for g in gammas:
            for m in methods:
                r = [one_run(n_cal, n_tgt, mu, g, alpha, m, rng) for _ in range(reps)]
                c = np.array([x["coverage"] for x in r])
                w = np.array([x["width"] for x in r])
                out.append({"mu": mu, "gamma": g, "method": m, "coverage": float(c.mean()),
                            "mcse": float(c.std(ddof=1) / math.sqrt(reps)), "width": float(np.median(w[np.isfinite(w)])) if np.isfinite(w).any() else None,
                            "inf": float(np.mean([x["inf"] for x in r])), "bound": float(np.mean([x["bound"] for x in r]))})
    return out


def selection_probs(age, center: float = 45.0, scale: float = 8.0) -> np.ndarray:
    """The application's designed selection: a person enters the (source) study with probability
    expit(-(age - center) / scale), so the old are under-represented, as in many volunteer samples."""
    return 1 / (1 + np.exp((np.asarray(age, float) - center) / scale))
