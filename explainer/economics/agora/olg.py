"""Agora's overlapping generations (Part 22 of *Economics, Built*): Samuelson's (1958) and Diamond's (1965) economies.

Each generation lives two periods (a period is about thirty years): it works when young, saves, and lives on its
savings (and any pension) when old.  Log utility ``ln c1 + beta ln c2``; Cobb-Douglas production ``A k^alpha`` per
young worker with full depreciation over a period; the population grows by the factor ``1 + n`` a period.

* :func:`diamond_path`, :func:`diamond_steady`: ``k' = s(w, R') / (1 + n)`` with saving
  ``beta/(1+beta) (w - d) - d (1+n) / ((1+beta) R')`` when a pay-as-you-go pension takes d from each young worker and
  pays ``(1+n) d`` to each old one.  With ``d = 0``: ``k' = (1-alpha) beta A k^alpha / ((1+beta)(1+n))``.
* :func:`pension_welfare`: steady-state lifetime utility as the pension grows; it rises (a free lunch) when the economy
  is dynamically inefficient, ``R < 1 + n``, and falls when it is efficient.
* :func:`samuelson_money`: Samuelson's consumption-loan economy without capital: money (or a pension) lets each
  generation trade with the next, and its return is the growth rate.

numpy only.
"""

from __future__ import annotations

import numpy as np


def _saving(w, R_next, beta, d, n):
    return beta / (1 + beta) * (w - d) - d * (1 + n) / ((1 + beta) * R_next)


def diamond_step(k: float, alpha: float, beta: float, n: float, A: float = 1.0, d: float = 0.0) -> float:
    """Next period's capital per young worker, solving ``(1+n) k' = s(w, R(k'))`` by bisection."""
    w = (1 - alpha) * A * k ** alpha

    def gap(k1):
        R1 = alpha * A * k1 ** (alpha - 1)
        return (1 + n) * k1 - _saving(w, R1, beta, d, n)
    lo, hi = 1e-12, max(w, 1e-9)
    if gap(hi) < 0:
        return hi
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def diamond_path(k0: float, periods: int, alpha: float = 0.3, beta: float = 0.5, n: float = 0.4, A: float = 10.0,
                 d: float = 0.0) -> dict:
    ks = [k0]
    for _ in range(periods):
        ks.append(diamond_step(ks[-1], alpha, beta, n, A, d))
    k = np.array(ks)
    return {"k": k.tolist(), "R": (alpha * A * k ** (alpha - 1)).tolist(), "y": (A * k ** alpha).tolist()}


def diamond_steady(alpha: float = 0.3, beta: float = 0.5, n: float = 0.4, A: float = 10.0, d: float = 0.0) -> dict:
    p = diamond_path(1.0, 400, alpha, beta, n, A, d)
    k = p["k"][-1]
    R = alpha * A * k ** (alpha - 1)
    w = (1 - alpha) * A * k ** alpha
    s = _saving(w, R, beta, d, n)
    c1 = w - d - s
    c2 = R * s + (1 + n) * d
    k_gold = (alpha * A / (1 + n)) ** (1 / (1 - alpha))
    return {"k": k, "R": R, "w": w, "c1": c1, "c2": c2, "utility": float(np.log(c1) + beta * np.log(c2)),
            "k_gold": k_gold, "efficient": bool(R >= 1 + n), "d": d}


def pension_welfare(ds, **kw) -> dict:
    rows = [diamond_steady(d=float(d), **kw) for d in ds]
    return {"d": list(map(float, ds)), "utility": [r["utility"] for r in rows], "R": [r["R"] for r in rows],
            "k": [r["k"] for r in rows]}


def samuelson_money(n: float = 0.4, endowment=(1.0, 0.0), beta: float = 0.9) -> dict:
    """Two-period lives, endowment (e1, e2) and no storage: without trade the old starve; with money (or a
    pay-as-you-go pension) each young generation buys the old's money, and the return on money is 1 + n.  With log
    utility the young save ``beta/(1+beta) e1`` in money."""
    e1, e2 = endowment
    s = beta / (1 + beta) * e1
    c1 = e1 - s
    c2 = e2 + (1 + n) * s
    return {"autarky": (e1, e2), "money": (c1, c2), "return": 1 + n,
            "utility_autarky": float(np.log(e1) + beta * np.log(max(e2, 1e-12))),
            "utility_money": float(np.log(c1) + beta * np.log(c2))}
