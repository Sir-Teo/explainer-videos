"""statkit.capstone: the tools of a complete analysis, for Part 20 of *Statistics, Built* ("The Analysis").

A decision log that records each cleaning step and how many rows it removed; restricted cubic splines (Harrell's
parametrization) for checking nonlinearity; the reliability of a single noisy measurement from two replicates; and
regression calibration (Carroll, Ruppert, Stefanski & Crainiceanu), which replaces an error-prone exposure by its
best linear prediction from a replicate before fitting the outcome model.  The design-based regression itself is in
``statkit.survey`` (``svy_ols``, ``psu_bootstrap_weights``).  Checked in ``tests/test_stats_kit_capstone.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class DecisionLog:
    """Each step of a cleaning funnel: its name, why, the rows it removed and the rows left."""

    n0: int
    steps: list = field(default_factory=list)

    def apply(self, keep: np.ndarray, mask: np.ndarray, step: str, why: str = "") -> np.ndarray:
        new = keep & np.asarray(mask, bool)
        self.steps.append({"step": step, "why": why, "removed": int(keep.sum() - new.sum()), "left": int(new.sum())})
        return new

    def table(self) -> list:
        return [{"step": "start", "why": "", "removed": 0, "left": self.n0}] + self.steps


def rcs_basis(x, knots) -> np.ndarray:
    """Restricted (natural) cubic spline basis with the given knots: x, then k - 2 nonlinear terms, each cubic between
    the knots and linear beyond the outer two (Harrell 2015, eq. 2.25, scaled by (t_k - t_1)^2)."""
    x = np.asarray(x, float)
    t = np.sort(np.asarray(knots, float))
    k = len(t)
    pos = lambda u: np.clip(u, 0, None) ** 3  # noqa: E731
    cols = [x]
    s = (t[-1] - t[0]) ** 2
    for j in range(k - 2):
        c = (pos(x - t[j]) - pos(x - t[-2]) * (t[-1] - t[j]) / (t[-1] - t[-2])
             + pos(x - t[-1]) * (t[-2] - t[j]) / (t[-1] - t[-2]))
        cols.append(c / s)
    return np.column_stack(cols)


def reliability(w1, w2) -> float:
    """The share of the variance of one measurement that is between-person: Cov(W1, W2) / Var(W1), estimated from
    two replicates with independent errors (the correlation if the two have equal variance)."""
    w1, w2 = np.asarray(w1, float), np.asarray(w2, float)
    c = np.cov(w1, w2)
    return float(c[0, 1] / np.sqrt(c[0, 0] * c[1, 1]))


def regression_calibration(w1, w2, Z=None, weights=None) -> dict:
    """Regress the second replicate on the first and the covariates ``Z``: since W2 = X + U2 with U2 independent of
    (W1, Z), E[W2 | W1, Z] = E[X | W1, Z].  Returns the calibrated exposure ``xhat`` (for every row, from W1 and Z),
    the coefficients, and ``lam``, the coefficient on W1 (the attenuation factor given Z)."""
    w1, w2 = np.asarray(w1, float), np.asarray(w2, float)
    n = len(w1)
    Zm = np.ones((n, 1)) if Z is None else np.column_stack([np.ones(n), np.asarray(Z, float)])
    D = np.column_stack([w1, Zm])
    wt = np.ones(n) if weights is None else np.asarray(weights, float)
    ok = np.isfinite(w2)
    Dw = D[ok] * np.sqrt(wt[ok])[:, None]
    g = np.linalg.lstsq(Dw, w2[ok] * np.sqrt(wt[ok]), rcond=None)[0]
    return {"xhat": D @ g, "coef": g, "lam": float(g[0])}
