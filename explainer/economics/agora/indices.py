"""Price and quantity indices (Agora, Part 3): how much did prices rise, when the basket itself changed?

A price index compares the cost of a basket of goods in two periods.  Which basket is the whole question:

* :func:`laspeyres` prices the *first* period's basket at both sets of prices.  When a price rises and people buy less
  of that good, the old basket overweights it, so Laspeyres overstates the rise in the cost of living (substitution
  bias, the first of the Boskin Commission's four);
* :func:`paasche` prices the *second* period's basket, and understates it;
* :func:`fisher`, the geometric mean of the two, and :func:`tornqvist`, a weighted geometric mean of price relatives
  with the two periods' average expenditure shares, are "superlative": exact for flexible forms of preferences, and in
  practice close to the true index;
* :func:`cost_of_living`: for a consumer with Cobb-Douglas tastes the true index is known exactly (the geometric mean
  of price relatives with the fixed spending shares), so the bias of each formula can be measured;
* :func:`chained` links period-to-period indices into a series.  Chaining keeps the weights up to date; with
  Laspeyres or Paasche links it can drift when prices bounce around, and with Fisher links it hardly does
  (:func:`chain_drift`).

Everything is plain numpy, for the labs.
"""

from __future__ import annotations

import numpy as np


def _a(x) -> np.ndarray:
    return np.asarray(x, float)


def laspeyres(p0, p1, q0) -> float:
    """sum p1 q0 / sum p0 q0: the old basket at new prices over the old basket at old prices."""
    p0, p1, q0 = _a(p0), _a(p1), _a(q0)
    return float(p1 @ q0 / (p0 @ q0))


def paasche(p0, p1, q1) -> float:
    """sum p1 q1 / sum p0 q1: the new basket at new prices over the new basket at old prices."""
    p0, p1, q1 = _a(p0), _a(p1), _a(q1)
    return float(p1 @ q1 / (p0 @ q1))


def fisher(p0, p1, q0, q1) -> float:
    """The geometric mean of Laspeyres and Paasche (Fisher's "ideal" index, 1922)."""
    return float(np.sqrt(laspeyres(p0, p1, q0) * paasche(p0, p1, q1)))


def tornqvist(p0, p1, q0, q1) -> float:
    """exp( sum_i  (s_i0 + s_i1)/2  ln(p_i1 / p_i0) ), with s the expenditure shares."""
    p0, p1, q0, q1 = _a(p0), _a(p1), _a(q0), _a(q1)
    s0 = p0 * q0 / (p0 @ q0)
    s1 = p1 * q1 / (p1 @ q1)
    return float(np.exp(((s0 + s1) / 2) @ np.log(p1 / p0)))


def cost_of_living(p0, p1, shares) -> float:
    """The exact cost-of-living index of a Cobb-Douglas consumer who spends the fixed ``shares`` of income on each good:
    prod (p1/p0)^share.  (What it costs at the new prices to be exactly as well off as before.)"""
    p0, p1, s = _a(p0), _a(p1), _a(shares)
    return float(np.exp(s @ np.log(p1 / p0)))


def cobb_douglas_demand(p, income: float, shares) -> np.ndarray:
    """Quantities a Cobb-Douglas consumer buys: share_i * income / p_i."""
    return _a(shares) * income / _a(p)


def chained(prices, quantities, formula: str = "fisher") -> np.ndarray:
    """Link period-to-period indices: I_t = I_{t-1} * index(t-1, t), starting at 1.  ``prices`` and ``quantities``
    are (T, n) arrays; ``formula`` is ``laspeyres``, ``paasche``, ``fisher`` or ``tornqvist``."""
    P, Q = _a(prices), _a(quantities)
    out = [1.0]
    for t in range(1, len(P)):
        if formula == "laspeyres":
            r = laspeyres(P[t - 1], P[t], Q[t - 1])
        elif formula == "paasche":
            r = paasche(P[t - 1], P[t], Q[t])
        elif formula == "tornqvist":
            r = tornqvist(P[t - 1], P[t], Q[t - 1], Q[t])
        elif formula == "fisher":
            r = fisher(P[t - 1], P[t], Q[t - 1], Q[t])
        else:
            raise ValueError(formula)
        out.append(out[-1] * r)
    return np.array(out)


def fixed_base(prices, quantities, formula: str = "laspeyres") -> np.ndarray:
    """Each period compared directly with period 0 (the base basket for Laspeyres, the current one for Paasche)."""
    P, Q = _a(prices), _a(quantities)
    out = []
    for t in range(len(P)):
        if formula == "laspeyres":
            out.append(laspeyres(P[0], P[t], Q[0]))
        elif formula == "paasche":
            out.append(paasche(P[0], P[t], Q[t]))
        elif formula == "fisher":
            out.append(fisher(P[0], P[t], Q[0], Q[t]))
        else:
            raise ValueError(formula)
    return np.array(out)


def chain_drift(prices, quantities) -> dict:
    """Prices that end where they began: the chained index should end at 1.  Returns the final value of each chained
    formula (Laspeyres drifts up, Paasche down, Fisher stays close to 1)."""
    return {f: float(chained(prices, quantities, f)[-1]) for f in ("laspeyres", "paasche", "fisher", "tornqvist")}
