"""Demand and supply as smooth curves (Agora, Part 2): what many traders' cards add up to, and what the curves say
about shifts, elasticity, taxes and price controls.

Part 1's :class:`~explainer.economics.agora.market.Market` holds a handful of cards, one unit each, and its curves
are staircases.  With many traders the steps shrink until the staircase is a curve; :func:`crowd` draws such a crowd
of cards, and :class:`Linear` is the curve it tends to (values spread evenly between a choke price and zero give a
straight demand line).  On a pair of straight lines everything in the textbook can be computed exactly:

* :meth:`Linear.equilibrium`: where demand meets supply;
* :meth:`Linear.elasticity`: the point elasticities of demand and supply at a price, and :func:`arc_elasticity`,
  the midpoint formula for two observed points;
* :meth:`Linear.shift`: a new market with one curve moved (a frost moves supply to the left);
* :meth:`Linear.tax`: a tax per unit, remitted by either side.  The price buyers pay and the price sellers keep do not
  depend on who remits it; the share each side bears is the other side's elasticity over the sum of the two
  (:func:`buyers_share`); the deadweight loss is the triangle between the curves over the trades the tax prevents;
* :meth:`Linear.cap` and :meth:`Linear.floor`: a legal maximum or minimum price.  The quantity traded is the short
  side's; the triangle is lost; and if the scarce units go by lottery rather than to the traders who value them most,
  the misallocation loses more (Glaeser and Luttmer 2003 measured it for New York's rent control).

Everything is in plain numbers so that the labs can use it without manim.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


def arc_elasticity(q0: float, q1: float, p0: float, p1: float) -> float:
    """The midpoint (arc) elasticity: the change in quantity over its mean, divided by the change in price over its
    mean.  Unlike the plain percentage change, it is the same whichever point you start from."""
    return float(((q1 - q0) / ((q0 + q1) / 2)) / ((p1 - p0) / ((p0 + p1) / 2)))


def buyers_share(eps_d: float, eps_s: float) -> float:
    """The share of a small tax borne by buyers: ``eps_s / (eps_s - eps_d)`` (``eps_d`` negative).  The side that
    can move less pays more; a perfectly inelastic demand (``eps_d = 0``) pays it all."""
    return float(eps_s / (eps_s - eps_d))


def crowd(n: int, choke: float, lowest_cost: float, highest_cost: float, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """``n`` buyers' values spread at random between 0 and ``choke``, and ``n`` sellers' costs between the two cost
    bounds: a crowd whose staircases approach the straight lines of :meth:`Linear.from_crowd`."""
    rng = np.random.default_rng(seed)
    return np.sort(rng.uniform(0, choke, n))[::-1], np.sort(rng.uniform(lowest_cost, highest_cost, n))


@dataclass(frozen=True)
class Linear:
    """Demand ``Q = a - b p`` and supply ``Q = c + d p`` (``b, d > 0``; ``c`` may be negative, so that supply starts
    at a positive price ``-c/d``)."""

    a: float
    b: float
    c: float
    d: float

    @classmethod
    def from_crowd(cls, n: int, choke: float, lowest_cost: float, highest_cost: float) -> "Linear":
        """The lines a :func:`crowd` tends to: ``n`` values uniform on [0, choke] give ``Q = n (1 - p/choke)``;
        costs uniform on [lo, hi] give ``Q = n (p - lo)/(hi - lo)``."""
        return cls(a=float(n), b=n / choke, c=-n * lowest_cost / (highest_cost - lowest_cost),
                   d=n / (highest_cost - lowest_cost))

    # -- the curves ----------------------------------------------------------
    def qd(self, p) -> np.ndarray | float:
        return np.maximum(self.a - self.b * np.asarray(p, float), 0.0)

    def qs(self, p) -> np.ndarray | float:
        return np.maximum(self.c + self.d * np.asarray(p, float), 0.0)

    def pd(self, q) -> np.ndarray | float:
        """Inverse demand: the value of the q-th unit to the buyer who values it least among the first q."""
        return (self.a - np.asarray(q, float)) / self.b

    def ps(self, q) -> np.ndarray | float:
        """Inverse supply: the cost of the q-th unit."""
        return (np.asarray(q, float) - self.c) / self.d

    @property
    def choke(self) -> float:
        """The price at which nobody buys."""
        return self.a / self.b

    @property
    def reservation(self) -> float:
        """The price below which nobody sells."""
        return max(-self.c / self.d, 0.0)

    # -- the equilibrium -----------------------------------------------------
    def equilibrium(self) -> dict:
        p = (self.a - self.c) / (self.b + self.d)
        q = self.a - self.b * p
        cs = 0.5 * q * (self.choke - p)
        # supply starting at a positive price (c <= 0), or with c units offered at no cost (c > 0)
        ps = 0.5 * q * (p - self.reservation) if self.c <= 0 else p * q - (q - self.c) ** 2 / (2 * self.d)
        return {"p": float(p), "q": float(q), "cs": float(cs), "ps": float(ps), "surplus": float(cs + ps)}

    def elasticity(self, p: float | None = None) -> dict:
        """Point elasticities at ``p`` (default: the equilibrium price): demand ``-b p / Q_d``, supply ``d p / Q_s``."""
        if p is None:
            p = self.equilibrium()["p"]
        return {"demand": float(-self.b * p / self.qd(p)), "supply": float(self.d * p / self.qs(p))}

    def revenue(self, p) -> np.ndarray | float:
        """What buyers spend at ``p``: largest where the demand elasticity is minus one (at half the choke price)."""
        return np.asarray(p, float) * self.qd(p)

    # -- comparative statics -------------------------------------------------
    def shift(self, demand: float = 0.0, supply: float = 0.0) -> "Linear":
        """Move the curves sideways: ``demand`` units more wanted at every price, ``supply`` units more offered."""
        return replace(self, a=self.a + demand, c=self.c + supply)

    # -- wedges and controls -------------------------------------------------
    def tax(self, t: float, on: str = "sell") -> dict:
        """A tax of ``t`` per unit.  ``on``: who remits it, which changes nothing that follows (it is in the
        output only to show that).  Returns the price buyers pay, the price sellers keep, the quantity, the revenue,
        the deadweight loss and the shares of the tax each side bears (measured from the untaxed price);
        ``price_called``: the price that changes hands in the market (what buyers pay when sellers remit the tax,
        what sellers keep when buyers do)."""
        if on not in ("sell", "buy"):
            raise ValueError("on is 'sell' or 'buy'")
        e = self.equilibrium()
        # buyers pay pb, sellers keep pb - t, and the two quantities agree: a - b pb = c + d (pb - t)
        pb = (self.a - self.c + self.d * t) / (self.b + self.d)
        pr = pb - t
        q = self.qd(pb)
        dwl = 0.5 * t * (e["q"] - q)
        return {"on": on, "paid": float(pb), "received": float(pr), "q": float(q), "revenue": float(t * q),
                "dwl": float(dwl), "buyers_share": float((pb - e["p"]) / t) if t else float("nan"),
                "sellers_share": float((e["p"] - pr) / t) if t else float("nan"),
                "price_called": float(pb if on == "sell" else pr)}

    def cap(self, p_max: float) -> dict:
        """A legal maximum price.  If it binds, sellers supply ``Q_s(p_max)``, buyers want ``Q_d(p_max)``, and the
        shortage is the difference.  ``triangle``: the surplus lost because fewer units trade, if the units go to the
        buyers who value them most; ``lottery``: the extra loss if they go to buyers drawn at random from all who want
        one at the capped price (each wanting buyer's value then averages the midpoint of ``p_max`` and the choke
        price)."""
        e = self.equilibrium()
        if p_max >= e["p"]:
            return {"binds": False, "q": e["q"], "shortage": 0.0, "triangle": 0.0, "lottery": 0.0}
        qs, qd = float(self.qs(p_max)), float(self.qd(p_max))
        triangle = 0.5 * (e["q"] - qs) * (self.pd(qs) - self.ps(qs))
        best = qs * (self.choke + self.pd(qs)) / 2  # the qs highest values, on a straight demand line
        random_ = qs * (self.choke + p_max) / 2     # qs values drawn from everyone with a value above p_max
        return {"binds": True, "q": qs, "wanted": qd, "shortage": qd - qs, "triangle": float(triangle),
                "lottery": float(best - random_), "surplus_best": float(e["surplus"] - triangle),
                "surplus_lottery": float(e["surplus"] - triangle - (best - random_))}

    def floor(self, p_min: float) -> dict:
        """A legal minimum price: the mirror image of :meth:`cap`, with sellers rationed (``lottery``: if the sales go
        to sellers drawn at random from all who would sell at ``p_min``, not to the cheapest)."""
        e = self.equilibrium()
        if p_min <= e["p"]:
            return {"binds": False, "q": e["q"], "surplus_unsold": 0.0, "triangle": 0.0, "lottery": 0.0}
        qd, qs = float(self.qd(p_min)), float(self.qs(p_min))
        triangle = 0.5 * (e["q"] - qd) * (self.pd(qd) - self.ps(qd))
        best = qd * (self.reservation + self.ps(qd)) / 2
        random_ = qd * (self.reservation + p_min) / 2
        return {"binds": True, "q": qd, "offered": qs, "unsold": qs - qd, "triangle": float(triangle),
                "lottery": float(random_ - best), "surplus_best": float(e["surplus"] - triangle),
                "surplus_lottery": float(e["surplus"] - triangle - (random_ - best))}
