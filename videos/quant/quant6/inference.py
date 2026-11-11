"""Corrected fixed-beta inference, preserving Part 6's legacy computations.

Shanken (1992), theorem 2, separates factor variation from errors in estimated
betas. GRS uses consistent covariance divisors (Kamstra and Shi 2021).
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def shanken_covariance(fm_cov, factor_cov, premium, periods):
    """Correctly specified, iid-factor approximation; fm_cov already divides by T.

    The first coefficient is the cross-sectional intercept. This does not correct
    for serial dependence or model misspecification. Use consistent divisors.
    """
    fm_cov = np.asarray(fm_cov, float)
    factor_cov = np.atleast_2d(np.asarray(factor_cov, float))
    premium = np.atleast_1d(np.asarray(premium, float))
    c = float(premium @ np.linalg.solve(factor_cov, premium))
    factor_component = np.zeros_like(fm_cov)
    factor_component[1:, 1:] = factor_cov / periods
    return (1 + c) * (fm_cov - factor_component) + factor_component


def grs_test(returns, factors):
    """Normal-error GRS alpha test, with divisor T for both covariances.

    Exact F inference needs iid homoskedastic normal errors independent of the
    factor design, full rank, and T > N + K. These are model assumptions, not
    established properties of the financial data.
    """
    R, F = np.asarray(returns, float), np.asarray(factors, float)
    if F.ndim == 1:
        F = F[:, None]
    T, N = R.shape
    K = F.shape[1]
    if T <= N + K:
        raise ValueError("GRS needs more dates than assets plus factors")
    X = np.column_stack([np.ones(T), F])
    coef = np.linalg.lstsq(X, R, rcond=None)[0]
    residuals = R - X @ coef
    residual_cov = residuals.T @ residuals / T
    centered_factors = F - F.mean(axis=0)
    factor_cov = centered_factors.T @ centered_factors / T
    factor_mean, alpha = F.mean(axis=0), coef[0]
    statistic = ((T - N - K) / N * float(alpha @ np.linalg.solve(residual_cov, alpha))
                 / (1 + float(factor_mean @ np.linalg.solve(factor_cov, factor_mean))))
    return {"F": statistic, "p": float(stats.f.sf(statistic, N, T - N - K)),
            "alpha": alpha, "df": (N, T - N - K)}
