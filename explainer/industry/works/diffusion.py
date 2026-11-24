"""Diffusion: how a new product spreads through a market (Part 7).

* :func:`bass` is Frank Bass's 1969 model.  Each year a fraction ``p`` of the people who have not yet adopted do so on
  their own (innovators), and a further fraction ``q`` times the share who already have (imitators, copying
  neighbours).  The cumulative share follows an S-curve that tops out at the market's ceiling ``m``.
* :func:`fit_bass` fits ``p``, ``q``, ``m`` and a start year to a series of shares by least squares.
* :func:`early_forecast` fits only the years before a series first reaches a given share, and forecasts the rest:
  how well could someone have called the S-curve from its start?
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares


def bass(t, p: float, q: float, m: float = 1.0):
    """Cumulative share of the market that has adopted after ``t`` years (``t`` >= 0)."""
    t = np.maximum(np.asarray(t, dtype=float), 0.0)
    e = np.exp(-(p + q) * t)
    return m * (1 - e) / (1 + (q / p) * e)


def peak_year(p: float, q: float) -> float:
    """Years from launch to the year of most new adopters: ln(q/p) / (p + q) (zero if q <= p)."""
    return float(np.log(q / p) / (p + q)) if q > p else 0.0


def fit_bass(years, shares, m_max: float = 100.0) -> dict:
    """Fit p, q, m (a share in the same units as ``shares``, at most ``m_max``) and the launch year t0."""
    years = np.asarray(years, dtype=float)
    shares = np.asarray(shares, dtype=float)
    y0 = years.min()

    def resid(th):
        p, q, m, t0 = th
        return bass(years - t0, p, q, m) - shares
    best = None
    for p0, q0 in ((0.01, 0.3), (0.03, 0.4), (0.005, 0.6), (0.05, 0.2)):
        x0 = (p0, q0, min(max(shares.max() * 1.1, 1.0), m_max), y0 - 1)
        try:
            r = least_squares(resid, x0, bounds=([1e-5, 1e-4, max(shares.max() * 0.5, 0.1), y0 - 60],
                                                 [1.0, 3.0, m_max, y0 + 5]))
        except ValueError:
            continue
        if best is None or r.cost < best.cost:
            best = r
    p, q, m, t0 = best.x
    rmse = float(np.sqrt(np.mean(resid(best.x) ** 2)))
    return dict(p=float(p), q=float(q), m=float(m), t0=float(t0), rmse=rmse)


def predict(fit: dict, years):
    return bass(np.asarray(years, dtype=float) - fit["t0"], fit["p"], fit["q"], fit["m"])


def early_forecast(years, shares, upto: float, m_max: float = 100.0) -> dict | None:
    """Fit only the observations up to (and including) the first year the share reaches ``upto``; forecast the rest.
    Returns the early fit, the full fit and the forecast errors; None if there are too few early points."""
    years = np.asarray(years, dtype=float)
    shares = np.asarray(shares, dtype=float)
    idx = np.where(shares >= upto)[0]
    if len(idx) == 0:
        return None
    k = idx[0] + 1
    if k < 4 or k >= len(years):
        return None
    early = fit_bass(years[:k], shares[:k], m_max)
    full = fit_bass(years, shares, m_max)
    later = years[k:]
    err = predict(early, later) - shares[k:]
    return dict(early=early, full=full, cut=float(years[k - 1]), mae=float(np.mean(np.abs(err))),
                ceiling_error=early["m"] - full["m"])
