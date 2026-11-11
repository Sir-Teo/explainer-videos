"""Chosen mathematical inputs for Part 32; no market data, historical strategy, cache or registration.

Return increments in the trend examples are dimensionless units. The associated
linear-rule PnL is in squared increment units, with no wealth or risk normalisation.
Portfolio covariance, rates and calendar numbers below are stipulated, not estimates.
"""
from __future__ import annotations

import math

import numpy as np


def trend_paths():
    chosen = {
        "persistent rise": (1.0, 1.0, 1.0, 1.0),
        "alternating": (1.0, -1.0, 1.0, -1.0),
        "rise then reversal": (1.0, 1.0, -1.0, -1.0),
        "one final jump": (0.0, 0.0, 0.0, 4.0),
    }
    out = {}
    for name, values in chosen.items():
        r = np.array(values)
        position = np.r_[0.0, np.cumsum(r)[:-1]]
        out[name] = {"increments": r, "position": position, "path": np.r_[0.0, np.cumsum(r)],
                     "S": float(r.sum()), "Q": float(r @ r), "P": float(position @ r)}
    return out


def volatility_cases():
    target, cap = 0.10, 3.0
    cases = []
    for forecast, realised in [(0.20, 0.20), (0.10, 0.10), (0.02, 0.02), (0.10, 0.20)]:
        exposure = min(target / forecast, cap)
        cases.append({"forecast": forecast, "realised": realised, "exposure": exposure,
                      "conditional_risk": exposure * realised})
    return {"target": target, "cap": cap, "cases": cases}


def covariance_case(rho=-0.2):
    """Two stipulated assets: annual SDs20%/10%, equal standalone risk, target10%."""
    sigma = np.array([0.20, 0.10])
    covariance = np.outer(sigma, sigma) * np.array([[1.0, rho], [rho, 1.0]])
    balanced = np.array([0.60, 0.40])
    inverse = 1.0 / sigma
    inverse /= inverse.sum()
    risk = lambda w: float(np.sqrt(w @ covariance @ w))
    base_risk = risk(inverse)
    leverage = min(0.10 / base_risk, 4.0)
    return {"rho": rho, "sigma": sigma, "covariance": covariance, "sixty_forty": balanced,
            "balanced_risk": risk(balanced), "inverse_weights": inverse, "base_risk": base_risk,
            "leverage": leverage, "target_weights": leverage * inverse,
            "Euler_fraction": inverse * (covariance @ inverse) / base_risk ** 2}


def group_euler_case():
    """Three equal-volatility groups with chosen feasible correlations; no historical fit."""
    correlation = np.array([[1.0, 0.8, 0.0], [0.8, 1.0, 0.1], [0.0, 0.1, 1.0]])
    covariance = 0.10 ** 2 * correlation
    weight = np.ones(3) / 3
    variance = float(weight @ covariance @ weight)
    return {"correlation": correlation, "covariance": covariance, "weight": weight,
            "risk": math.sqrt(variance), "Euler_fraction": weight * (covariance @ weight) / variance}


def currency_case():
    spot, foreign_rate, domestic_rate = 1.10, 0.06, 0.02
    forward = spot * (1 + domestic_rate) / (1 + foreign_rate)
    cases = []
    for spot_change in [-0.05, 0.0, 0.05]:
        terminal = spot * (1 + spot_change)
        total = (1 + foreign_rate) * terminal / spot - 1
        cases.append({"spot_change": spot_change, "terminal_spot": terminal,
                      "foreign_deposit_total": total, "excess_over_domestic": total - domestic_rate,
                      "one_foreign_unit_forward_PnL": terminal - forward})
    return {"spot": spot, "foreign_rate": foreign_rate, "domestic_rate": domestic_rate,
            "forward": forward, "cases": cases}


def calendar_case():
    previous_close, next_open, next_close = 100.0, 102.0, 101.0
    night = next_open / previous_close - 1
    day = next_close / next_open - 1
    return {"previous_close": previous_close, "next_open": next_open, "next_close": next_close,
            "overnight": night, "intraday": day, "whole_day": next_close / previous_close - 1,
            "independent_tests": 100, "test_size": 0.05,
            "one_or_more_false_rejections": 1 - 0.95 ** 100,
            "expected_false_rejections": 100 * 0.05,
            "chosen_gross_edge_bp": 4.0, "chosen_roundtrip_cost_bp": 5.0}


def gaussian_trend_theory():
    """Closed-form independent zero-mean Gaussian reference; no simulation or empirical fit."""
    from scipy.stats import f, norm

    rows = []
    for n in [2, 3, 5, 10, 21, 63, 126, 252]:
        rows.append({"n": n, "mean": 0.0, "variance": n * (n - 1) / 2,
                     "skew": 2 ** 1.5 * (n - 2) / math.sqrt(n * (n - 1)),
                     "win_probability": float(f.sf(1.0, 1, n - 1))})
    mean_cases = []
    for mu, rho in [(0.0, 0.0), (0.0, 0.2), (0.0, -0.2), (0.1, 0.2)]:
        n = 4
        mean_cases.append({"n": n, "mu": mu, "rho": rho,
                           "expected_P": n * (n - 1) * mu ** 2 / 2
                           + sum((n - k) * rho ** k for k in range(1, n))})
    return {"rows": rows, "mean_cases": mean_cases, "limit_skew": 2 * math.sqrt(2),
            "limit_win_probability": float(2 * norm.sf(1.0)), "scope": "Analytic Gaussian reference only"}
