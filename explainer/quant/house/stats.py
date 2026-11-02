"""The House's returns statistics (Part 1, *The Fair Game*): what a price series looks like, measured.

Every function takes plain arrays of returns (decimal, one per period) and is used again by later parts: the
variance ratio by Part 6's tests, the tail estimators by Part 40's risk models, the autocorrelations by Part 7.

* :func:`log_returns`, :func:`simple_to_log`, :func:`aggregate`: returns and their horizons;
* :func:`autocorr`: sample autocorrelations at several lags;
* :func:`variance_ratio`: Lo and MacKinlay's (1988) test that a series is a random walk, with the
  heteroskedasticity-robust statistic z* that keeps its size when volatility clusters;
* :func:`hill`, :func:`survival`: the tail exponent and the empirical tail;
* :func:`excess_kurtosis`, :func:`gaussian_tail_years`, :func:`powerlaw_tail_years`: how heavy the tails are, and how
  often a move of a given size comes under a Gaussian and under a fitted power law.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def log_returns(prices) -> np.ndarray:
    p = np.asarray(prices, float)
    return np.diff(np.log(p))


def simple_to_log(r) -> np.ndarray:
    return np.log1p(np.asarray(r, float))


def aggregate(r, h: int, overlapping: bool = False) -> np.ndarray:
    """Sums of ``h`` consecutive (log) returns: non-overlapping blocks by default, or every rolling window."""
    r = np.asarray(r, float)
    if overlapping:
        c = np.concatenate([[0.0], np.cumsum(r)])
        return c[h:] - c[:-h]
    n = len(r) // h
    return r[: n * h].reshape(n, h).sum(axis=1)


def autocorr(x, lags) -> np.ndarray:
    """Sample autocorrelations of ``x`` at each lag (the usual biased estimator: one mean, one variance)."""
    x = np.asarray(x, float) - np.mean(x)
    v = np.dot(x, x)
    return np.array([np.dot(x[: len(x) - k], x[k:]) / v if k > 0 else 1.0 for k in np.atleast_1d(lags)])


def variance_ratio(r, q: int) -> dict:
    """Lo and MacKinlay's variance ratio VR(q) = Var(q-period return) / (q Var(one-period return)) from overlapping
    q-period sums, with their small-sample bias corrections, and two test statistics: ``z`` (iid increments) and
    ``z_star`` (robust to heteroskedasticity: only uncorrelated increments are assumed).  Under a random walk
    VR(q) = 1; VR(q) - 1 is approximately 2 sum_k (1 - k/q) rho_k, so positive autocorrelation pushes it above one."""
    x = np.asarray(r, float)
    nq = len(x)
    mu = x.mean()
    d = x - mu
    var1 = np.dot(d, d) / (nq - 1)
    sums = aggregate(x, q, overlapping=True)
    m = q * (nq - q + 1) * (1 - q / nq)
    varq = np.sum((sums - q * mu) ** 2) / m
    vr = varq / var1
    # iid: asymptotic variance 2(2q-1)(q-1) / (3q nq)
    z = (vr - 1) / np.sqrt(2 * (2 * q - 1) * (q - 1) / (3 * q * nq))
    # heteroskedasticity-consistent: theta = sum_j (2(q-j)/q)^2 delta_j
    d2 = d ** 2
    denom = np.sum(d2) ** 2
    theta = 0.0
    for j in range(1, q):
        delta = nq * np.sum(d2[j:] * d2[:-j]) / denom
        theta += (2 * (q - j) / q) ** 2 * delta
    z_star = (vr - 1) / np.sqrt(theta / nq)  # delta_j ~ 1 for iid data, so theta / nq -> the iid variance
    return {"q": q, "vr": float(vr), "z": float(z), "z_star": float(z_star),
            "p_star": float(2 * stats.norm.sf(abs(z_star)))}


def hill(x, k: int | None = None, frac: float = 0.02) -> float:
    """Hill's (1975) estimate of the tail exponent alpha of |x| (P(|X| > u) ~ u^-alpha) from the ``k`` largest
    values (default: the top ``frac`` of the sample)."""
    a = np.sort(np.abs(np.asarray(x, float)))[::-1]
    k = k or max(int(frac * len(a)), 10)
    top = a[: k + 1]
    return float(1.0 / np.mean(np.log(top[:k] / top[k])))


def hill_curve(x, ks) -> np.ndarray:
    """The Hill estimate for each number of order statistics in ``ks`` (the "Hill plot")."""
    a = np.sort(np.abs(np.asarray(x, float)))[::-1]
    la = np.log(a)
    out = []
    for k in ks:
        out.append(1.0 / (np.mean(la[:k]) - la[k]))
    return np.array(out)


def survival(x, n_points: int = 200) -> tuple[np.ndarray, np.ndarray]:
    """The empirical tail P(|X| > u) of |x| on a log grid of thresholds u (from the median to the maximum)."""
    a = np.sort(np.abs(np.asarray(x, float)))
    u = np.geomspace(np.median(a), a[-1], n_points)
    p = 1.0 - np.searchsorted(a, u, side="right") / len(a)
    return u, p


def excess_kurtosis(x) -> float:
    return float(stats.kurtosis(np.asarray(x, float), fisher=True, bias=False))


def gaussian_tail_years(z: float, per_year: float = 252.0, two_sided: bool = False) -> float:
    """Years between moves at least ``z`` standard deviations (down, or either way) if returns were Gaussian."""
    p = stats.norm.sf(abs(z)) * (2 if two_sided else 1)
    return float(1.0 / (p * per_year))


def powerlaw_tail_years(x, threshold: float, frac: float = 0.02, per_year: float = 252.0, side: str = "down") -> float:
    """Years between moves beyond ``threshold`` (a return, e.g. -0.17) under a power-law tail fitted by Hill to the
    worst ``frac`` of ``x`` on that side: P(X < -u) = frac (u / u_frac)^-alpha beyond the fit's threshold."""
    x = np.asarray(x, float)
    tail = -x if side == "down" else x
    a = np.sort(tail)[::-1]
    k = max(int(frac * len(a)), 10)
    alpha = 1.0 / np.mean(np.log(a[:k] / a[k]))
    p = (k / len(a)) * (abs(threshold) / a[k]) ** (-alpha)
    return float(1.0 / (p * per_year))
