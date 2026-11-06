"""statkit.ppi: prediction-powered inference (Part 34 of *Statistics, Built*).

Given n labelled pairs (X_i, Y_i) and N unlabelled X_j with a machine-learning prediction f(X) for both, estimate a
population mean or a regression coefficient.  Three ways: the classical estimate from the n labels alone; the naive
'predictions as data' estimate from the N predictions (biased unless f is perfect); and Angelopoulos, Bates, Fannjiang,
Jordan & Zrnic's (2023) prediction-powered estimate, the prediction mean corrected by the 'rectifier' (the mean
prediction error on the labelled data), with PPI++'s power-tuned weight lambda (Angelopoulos, Duchi & Zrnic 2023).
Checked in ``tests/test_stats_kit_conformal.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def classical_mean(y, alpha: float = 0.1) -> dict:
    y = np.asarray(y, float)
    se = y.std(ddof=1) / math.sqrt(len(y))
    z = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(y.mean()), "se": float(se), "lo": float(y.mean() - z * se), "hi": float(y.mean() + z * se)}


def naive_mean(f_unlab, alpha: float = 0.1) -> dict:
    """Treat the predictions as if they were data: a tight interval around the wrong target."""
    return classical_mean(f_unlab, alpha)


def ppi_mean(y_lab, f_lab, f_unlab, alpha: float = 0.1, lam: float | None = 1.0) -> dict:
    """theta_PP = lam * mean(f_unlab) - mean(lam f_lab - y_lab), with variance lam^2 var(f)/N + var(y - lam f)/n.
    ``lam=None`` uses PPI++'s variance-minimizing lam = cov(y, f) / ((1 + n/N) var(f)), clipped to [0, 1]."""
    y, fl, fu = np.asarray(y_lab, float), np.asarray(f_lab, float), np.asarray(f_unlab, float)
    n, N = len(y), len(fu)
    if lam is None:
        vf = np.var(np.r_[fl, fu], ddof=1)
        lam = float(np.clip(np.cov(y, fl)[0, 1] / ((1 + n / N) * vf), 0.0, 1.0))
    est = lam * fu.mean() - (lam * fl - y).mean()
    var = lam ** 2 * fu.var(ddof=1) / N + (y - lam * fl).var(ddof=1) / n
    se = math.sqrt(var)
    z = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(est), "se": float(se), "lo": float(est - z * se), "hi": float(est + z * se), "lam": lam,
            "rectifier": float((fl - y).mean())}


def ppi_ols(X_lab, y_lab, f_lab, X_unlab, f_unlab, alpha: float = 0.1) -> dict:
    """Prediction-powered least squares: beta = (X_u'X_u/N)^{-1} [X_u'f_u/N - X_l'(f_l - y)/n], with the sandwich
    variance of Angelopoulos et al. (2023), Thm. 3 (lam = 1).  Intercept included."""
    Xl = np.column_stack([np.ones(len(X_lab)), np.asarray(X_lab, float)])
    Xu = np.column_stack([np.ones(len(X_unlab)), np.asarray(X_unlab, float)])
    y, fl, fu = np.asarray(y_lab, float), np.asarray(f_lab, float), np.asarray(f_unlab, float)
    n, N = len(y), len(fu)
    Su = Xu.T @ Xu / N
    beta = np.linalg.solve(Su, Xu.T @ fu / N - Xl.T @ (fl - y) / n)
    Si = np.linalg.inv(Su)
    eu = fu - Xu @ beta
    el = (fl - y)
    Vu = (Xu * eu[:, None]).T @ (Xu * eu[:, None]) / N
    rl = Xl * el[:, None]
    Vl = np.cov(rl.T, ddof=1)
    V = Si @ (Vu / N + Vl / n) @ Si
    se = np.sqrt(np.diag(V))
    z = stats.norm.ppf(1 - alpha / 2)
    return {"beta": beta, "se": se, "lo": beta - z * se, "hi": beta + z * se}


def classical_ols(X, y, alpha: float = 0.1) -> dict:
    Z = np.column_stack([np.ones(len(X)), np.asarray(X, float)])
    y = np.asarray(y, float)
    b = np.linalg.lstsq(Z, y, rcond=None)[0]
    e = y - Z @ b
    Si = np.linalg.inv(Z.T @ Z)
    V = Si @ (Z * (e ** 2)[:, None]).T @ Z @ Si  # HC0 sandwich
    se = np.sqrt(np.diag(V))
    z = stats.norm.ppf(1 - alpha / 2)
    return {"beta": b, "se": se, "lo": b - z * se, "hi": b + z * se}
