"""Prices as messages: Hayek's tin (Agora, Part 1).

``n`` users of tin each see only the price.  User ``i`` would buy ``q_i(p) = a_i p^(-e_i)``: a user with a good
substitute (copper, aluminium, glass) has a large elasticity ``e_i`` and cuts back sharply when tin dears; a user with
none barely moves.  At the old price ``p = 1`` the market clears with supply ``S``.  Then a mine closes and supply
falls by a share ``cut``.

* :func:`clear` finds the price at which the users together want exactly the tin there is (they never learn why it
  rose: Hayek's point is that "it does not matter which of these two causes has made tin more scarce").
* :func:`tatonnement` reaches the same price by raising it while demand exceeds supply, as a market's traders feel
  their way there.
* :func:`welfare_loss` is the value of the tin that is given up, for any allocation of the cut: through the price
  (each user cuts to where tin is worth the new price to them) or by a planner who rations everyone equally.  The
  price-driven cut loses less, because the tin is taken from the uses where it was worth least; the planner could
  match it only by knowing every user's demand curve, ``2n`` numbers that change whenever anything does, where the
  price is one number.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def users(n: int = 60, seed: int = 1945) -> dict:
    """A population of tin users: sizes ``a`` (lognormal) and elasticities ``e`` from 0.1 (no substitute) to 2.5
    (a good one)."""
    rng = np.random.default_rng(seed)
    a = rng.lognormal(0.0, 0.6, n)
    a = a / a.sum() * 100.0  # 100 units of tin are used at the old price
    e = np.sort(rng.uniform(0.1, 2.5, n))
    rng.shuffle(e)
    return {"a": a, "e": e, "n": n, "supply": float(a.sum())}


def demand(u: dict, p: float) -> np.ndarray:
    return u["a"] * p ** (-u["e"])


def clear(u: dict, cut: float) -> dict:
    """The new price after supply falls by ``cut`` (a share), and each user's new quantity and cut."""
    s1 = u["supply"] * (1 - cut)
    p = brentq(lambda x: demand(u, x).sum() - s1, 1.0, 1e3)
    q1 = demand(u, p)
    return {"price": float(p), "supply": s1, "q0": u["a"], "q1": q1, "cut_share": 1 - q1 / u["a"]}


def tatonnement(u: dict, cut: float, speed: float = 0.6, steps: int = 40) -> dict:
    """Walras's groping: start at the old price, raise it in proportion to excess demand (relative to supply)."""
    s1 = u["supply"] * (1 - cut)
    p, path = 1.0, [1.0]
    for _ in range(steps):
        z = (demand(u, p).sum() - s1) / s1
        p *= 1 + speed * z
        path.append(p)
    return {"path": np.array(path), "excess": np.array([(demand(u, x).sum() - s1) / s1 for x in path])}


def _value(a: float, e: float, q0: float, q1: float) -> float:
    """The value to a user of the tin between q1 and q0: the area under the inverse demand p(q) = (q / a)^(-1/e)."""
    if q1 >= q0:
        return 0.0
    return float(quad(lambda q: (q / a) ** (-1.0 / e), q1, q0, limit=200)[0])


def welfare_loss(u: dict, q1: np.ndarray) -> float:
    """Total value given up when each user goes from the old quantity to ``q1``."""
    return float(sum(_value(a, e, a, q) for a, e, q in zip(u["a"], u["e"], q1)))


def compare(u: dict, cut: float) -> dict:
    """The same shortfall allocated by the price and by equal rationing: the value each loses."""
    c = clear(u, cut)
    rationed = u["a"] * (1 - cut)
    by_price = welfare_loss(u, c["q1"])
    by_rule = welfare_loss(u, rationed)
    return {**c, "loss_price": by_price, "loss_rationing": by_rule, "ratio": by_rule / by_price,
            "numbers_planner": 2 * u["n"], "numbers_market": 1}
