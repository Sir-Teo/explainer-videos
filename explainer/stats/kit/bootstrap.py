"""statkit.bootstrap: the jackknife, the bootstrap and its intervals, cross-validation and kernel density estimates
(Part 16 of *Statistics, Built*).  Checked in ``tests/test_stats_kit_bootstrap.py`` (against SciPy's bootstrap where it
applies).
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy import stats


def resample_indices(n: int, B: int, rng: np.random.Generator) -> np.ndarray:
    return rng.integers(0, n, size=(B, n))


def bootstrap(data, stat: Callable, B: int, rng: np.random.Generator) -> np.ndarray:
    """Replicates stat(data[idx]) for B resamples of the rows of ``data`` (an array, or a tuple of paired arrays)."""
    arrs = data if isinstance(data, tuple) else (data,)
    n = len(arrs[0])
    idx = resample_indices(n, B, rng)
    return np.array([stat(*(np.asarray(a)[i] for a in arrs)) for i in idx])


def jackknife(data, stat: Callable) -> dict:
    """Quenouille (1949) bias and Tukey (1958) standard error from the n leave-one-out estimates."""
    arrs = data if isinstance(data, tuple) else (data,)
    n = len(arrs[0])
    full = stat(*arrs)
    loo = np.array([stat(*(np.delete(np.asarray(a), i) for a in arrs)) for i in range(n)])
    m = loo.mean()
    return {"estimate": float(full), "loo": loo, "bias": float((n - 1) * (m - full)),
            "se": float(np.sqrt((n - 1) / n * np.sum((loo - m) ** 2)))}


def percentile_ci(reps, alpha=0.05):
    return tuple(float(v) for v in np.quantile(reps, [alpha / 2, 1 - alpha / 2]))


def basic_ci(reps, est, alpha=0.05):
    lo, hi = np.quantile(reps, [alpha / 2, 1 - alpha / 2])
    return float(2 * est - hi), float(2 * est - lo)


def normal_ci(reps, est, alpha=0.05):
    z = stats.norm.ppf(1 - alpha / 2)
    s = np.std(reps, ddof=1)
    return float(est - z * s), float(est + z * s)


def bca_ci(reps, est, jack_loo, alpha=0.05):
    """Efron's (1987) bias-corrected and accelerated interval: z0 from the share of replicates below the estimate,
    the acceleration a from the jackknife's skewness."""
    reps = np.asarray(reps)
    z0 = stats.norm.ppf(np.mean(reps < est) + 0.5 * np.mean(reps == est))
    d = np.mean(jack_loo) - np.asarray(jack_loo)
    a = np.sum(d ** 3) / (6 * np.sum(d ** 2) ** 1.5)
    out = []
    for q in (alpha / 2, 1 - alpha / 2):
        z = stats.norm.ppf(q)
        adj = stats.norm.cdf(z0 + (z0 + z) / (1 - a * (z0 + z)))
        out.append(float(np.quantile(reps, adj)))
    return tuple(out), float(z0), float(a)


def bootstrap_t_ci(x, B: int, rng: np.random.Generator, alpha=0.05):
    """The bootstrap-t interval for a mean: resample t* = (mean* - mean)/(s*/sqrt n)."""
    x = np.asarray(x, float)
    n = len(x)
    idx = resample_indices(n, B, rng)
    xb = x[idx]
    t = (xb.mean(1) - x.mean()) / (xb.std(1, ddof=1) / np.sqrt(n))
    lo, hi = np.quantile(t, [alpha / 2, 1 - alpha / 2])
    se = x.std(ddof=1) / np.sqrt(n)
    return float(x.mean() - hi * se), float(x.mean() - lo * se)


def silverman(x) -> float:
    x = np.asarray(x, float)
    s = min(x.std(ddof=1), stats.iqr(x) / 1.349)
    return float(0.9 * s * len(x) ** (-1 / 5))


def kde(x, grid, h: float) -> np.ndarray:
    """Gaussian kernel density estimate: the average of n bumps of width h."""
    x, g = np.asarray(x, float), np.asarray(grid, float)
    return stats.norm.pdf((g[:, None] - x[None, :]) / h).sum(1) / (len(x) * h)


def kfold_poly_cv(x, y, degree: int, k: int, rng: np.random.Generator) -> float:
    """K-fold cross-validated mean squared prediction error of a polynomial fit."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    folds = np.array_split(rng.permutation(len(x)), k)
    err = 0.0
    for f in folds:
        tr = np.setdiff1d(np.arange(len(x)), f)
        c = np.polyfit(x[tr], y[tr], degree)
        err += np.sum((np.polyval(c, x[f]) - y[f]) ** 2)
    return float(err / len(x))
