"""The Works' farm (Part 10): an acre's arithmetic, a forward sale and storage, Cochrane's treadmill, and the season
game.

Units: dollars per planted acre, bushels per acre, dollars per bushel; prices per tonne convert with ``BU_PER_T``.  The
films set these models beside USDA's cost-of-production accounts and label them as models.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# bushels in a metric tonne: corn weighs 56 pounds a bushel, soybeans and wheat 60
BU_PER_T = {"corn": 2204.62 / 56, "soybeans": 2204.62 / 60, "wheat": 2204.62 / 60}


def per_bushel(price_per_tonne: float, crop: str = "corn") -> float:
    return price_per_tonne / BU_PER_T[crop]


@dataclass
class Acre:
    """One planted acre: ``yield_bu`` bushels, ``operating`` dollars of seed, fertilizer, chemicals, fuel and repairs,
    and ``overhead`` dollars of machinery, land, unpaid labour and other allocated costs (of which ``land``)."""
    crop: str
    yield_bu: float
    operating: float
    overhead: float
    land: float = 0.0

    @property
    def cost(self) -> float:
        return self.operating + self.overhead

    def revenue(self, price: float) -> float:
        return self.yield_bu * price

    def net(self, price: float) -> float:
        return self.revenue(price) - self.cost

    def breakeven_price(self, operating_only: bool = False) -> float:
        return (self.operating if operating_only else self.cost) / self.yield_bu

    def land_residual(self, price: float) -> float:
        """What is left for the land after every other cost: the most a farmer could pay in rent and break even."""
        return self.revenue(price) - (self.cost - self.land)


def sell(expected_bu: float, actual_bu: float, plant_price: float, harvest_price: float, later_price: float,
         hedge: float = 0.0, store: float = 0.0, months: int = 8, carry: float = 0.04) -> float:
    """Revenue per acre from one season's marketing.  A share ``hedge`` of the expected crop is sold forward at
    planting at ``plant_price``; if the crop falls short, the shortfall is bought back at ``harvest_price``.  Of the
    unhedged grain, a share ``store`` is kept ``months`` months at ``carry`` dollars a bushel a month and sold at
    ``later_price``; the rest is sold at harvest."""
    forward = hedge * expected_bu
    rest = actual_bu - forward
    if rest < 0:
        return forward * plant_price + rest * harvest_price
    kept = store * rest
    return forward * plant_price + (rest - kept) * harvest_price + kept * (later_price - months * carry)


def treadmill(years: int = 30, gain: float = 0.12, elasticity: float = -0.4, speed: float = 0.45, mid: float = 10.0,
              unit_cost: float = 1.0) -> dict:
    """Cochrane's treadmill.  A new method raises output per acre by ``gain`` at the same cost an acre; farmers adopt it
    along a logistic curve.  Demand has constant ``elasticity``, so the price falls as total output rises.  Returns the
    adopted share, the price, and the profit per acre of an adopter and of a farmer who has not adopted."""
    t = np.arange(years)
    share = 1 / (1 + np.exp(-speed * (t - mid)))
    q = 1 + gain * share
    p = q ** (1 / elasticity) * (unit_cost * 1.15)  # starts with a 15% margin over cost
    adopter = p * (1 + gain) - unit_cost
    laggard = p - unit_cost
    return dict(years=t, share=share, output=q, price=p, adopter=adopter, laggard=laggard)


def margin_ladder(companies: dict) -> list[tuple]:
    """``companies`` = {name: (revenue, profit)}; returns (name, revenue, profit, margin) sorted by margin."""
    out = [(k, r, p, p / r) for k, (r, p) in companies.items() if r]
    return sorted(out, key=lambda q: q[3])
