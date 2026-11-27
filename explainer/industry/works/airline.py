"""The Works' airline (Part 28): one flight, its seats sold over sixty days to two kinds of traveller, and what it costs to
fly whether the seats are full or not.

The flight.  ``seats`` seats on a route of ``miles`` miles, costing ``casm`` dollars per available seat-mile to fly: the
cost is fixed once the flight is scheduled, so an empty seat earns nothing and saves almost nothing.

The travellers.  Leisure travellers book early and only at the ``low`` fare; their number is Poisson with mean
``leisure``.  Business travellers book late and pay the ``high`` fare; their number is Poisson with mean ``business``.
Because the leisure travellers come first, a seat sold cheaply in week one may be a seat a business traveller would have
paid for in the last week.

The airline's choices.  ``protect``: how many seats to hold back for the late, high fare (the booking limit for the low
fare is the capacity less the protected seats).  ``oversell``: how many seats beyond the cabin to sell, because a
share ``noshow`` of booked travellers do not turn up; each traveller who turns up to a full aircraft is paid ``bump``
to take a later flight.

Littlewood's rule (1972) gives the best protection level: protect the y-th seat while the chance that more than y
business travellers want it is above the ratio of the low fare to the high one.

Expected revenue is computed by simulation with a fixed seed, so every run gives the same numbers.  Every number is this
series' illustration, anchored on Delta's 2025 cost per available seat-mile (19.31 cents; 13.86 excluding fuel and some
items) and load factor (84%), and Southwest's average fare ($190) and stage length (780 miles).  After Littlewood (1972);
see *Economics, Built* Part 60 for EMSR-b and dynamic pricing.  No manim.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class Flight:
    seats: int = 180
    low: float = 129.0
    high: float = 429.0
    leisure: float = 190.0     # mean leisure demand
    business: float = 40.0     # mean business demand
    noshow: float = 0.08
    bump: float = 900.0
    miles: float = 1000.0
    casm: float = 0.16         # dollars per available seat-mile
    draws: int = 40_000
    seed: int = 28

    def cost(self) -> float:
        """The flight's cost, $: seats x miles x cost per seat-mile."""
        return self.seats * self.miles * self.casm

    def _demand(self):
        rng = np.random.default_rng(self.seed)
        return rng.poisson(self.leisure, self.draws), rng.poisson(self.business, self.draws), rng.random((self.draws,))

    def sell(self, protect: int = 0, oversell: int = 0, fixed: float | None = None) -> dict:
        """Expected results of one flight: seats sold, revenue, bumped travellers and their cost, load factor, profit.

        ``fixed``: sell every seat at one fare to whoever comes, leisure travellers buying only if it is at most the low
        fare and business travellers if it is at most the high fare."""
        dl, db, u = self._demand()
        cap = self.seats + oversell
        if fixed is not None:
            want_l = dl if fixed <= self.low else np.zeros_like(dl)
            want_b = db if fixed <= self.high else np.zeros_like(db)
            sold_l = np.minimum(want_l, cap)
            sold_b = np.minimum(want_b, cap - sold_l)
            rev = (sold_l + sold_b) * fixed
        else:
            limit = max(0, cap - protect)
            sold_l = np.minimum(dl, limit)
            sold_b = np.minimum(db, cap - sold_l)
            rev = sold_l * self.low + sold_b * self.high
        sold = sold_l + sold_b
        # show-ups: binomial, drawn with a fixed generator per call so results are reproducible
        rng = np.random.default_rng(self.seed + 1)
        show = rng.binomial(sold, 1 - self.noshow)
        bumped = np.maximum(0, show - self.seats)
        flown = np.minimum(show, self.seats)
        out = dict(sold=float(sold.mean()), sold_low=float(sold_l.mean()), sold_high=float(sold_b.mean()),
                   turned_away=float((db - sold_b).mean()), revenue=float(rev.mean()), bumped=float(bumped.mean()),
                   bump_cost=float(bumped.mean() * self.bump), load=float(flown.mean() / self.seats))
        out["net"] = out["revenue"] - out["bump_cost"]
        out["profit"] = out["net"] - self.cost()
        out["fare"] = out["revenue"] / out["sold"] if out["sold"] else 0.0
        return out

    def littlewood(self) -> int:
        """The protection level from Littlewood's rule: the largest y with P(business demand >= y) > low/high."""
        from math import exp, factorial

        ratio = self.low / self.high
        cdf, y = 0.0, 0
        lam = self.business
        while True:
            # P(D >= y+1) = 1 - P(D <= y)
            cdf += exp(-lam) * lam ** y / factorial(y)
            if 1 - cdf <= ratio:
                return y + 1 if y + 1 <= self.seats else self.seats
            y += 1

    def sweep_protect(self, step: int = 2, top: int = 80) -> dict:
        return {y: self.sell(protect=y)["net"] for y in range(0, top + 1, step)}

    def sweep_oversell(self, protect: int | None = None, top: int = 24) -> dict:
        p = self.littlewood() if protect is None else protect
        return {k: self.sell(protect=p, oversell=k)["net"] for k in range(0, top + 1)}

    def but(self, **kw) -> "Flight":
        return replace(self, **kw)


def breakeven_load(fare: float, casm: float, miles: float) -> float:
    """The share of seats that must be sold at ``fare`` to cover the flight's cost: casm x miles / fare."""
    return casm * miles / fare
