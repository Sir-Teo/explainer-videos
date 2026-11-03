"""Deterministic display fit derived from measured warehouse success arrays.

No simulation, cache access or generated results. A free intercept describes an
empirical whole-task decay; its slope is not measured single-step reliability.
"""
from __future__ import annotations

import numpy as np


def agent_decay_fit(ns, success):
    ns, success = np.asarray(ns, dtype=float), np.asarray(success, dtype=float)
    if (ns.ndim != 1 or success.shape != ns.shape or not np.isfinite(ns).all()
            or not np.isfinite(success).all() or np.any(ns <= 0)
            or np.any((success < 0) | (success > 1))):
        raise ValueError('finite positive horizons and success probabilities required')
    mask = success > .02  # same fit selection as the original producer
    if np.unique(ns[mask]).size < 2:
        raise ValueError('at least two distinct retained horizons required')
    slope, intercept = np.polyfit(ns[mask], np.log(success[mask]), 1)
    amplitude, decay = np.exp(intercept), np.exp(slope)
    if not np.isfinite([slope, intercept, amplitude, decay]).all():
        raise ValueError('non-finite empirical decay fit')
    return dict(slope=float(slope), intercept=float(intercept),
                amplitude=float(amplitude), decay=float(decay))


def agent_fit_curve(ns, fit, points=61):
    """Draw only within the observed horizon domain, never extrapolate to zero."""
    ns = np.asarray(ns, dtype=float)
    if ns.ndim != 1 or ns.size < 2 or not np.isfinite(ns).all() or ns.min() <= 0:
        raise ValueError('positive observed horizon domain required')
    xx = np.linspace(ns.min(), ns.max(), points)
    yy = fit['amplitude'] * np.exp(fit['slope'] * xx)
    if not np.isfinite(yy).all():
        raise ValueError('non-finite empirical fit curve')
    return xx, yy
