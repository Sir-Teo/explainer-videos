"""The Works' mine (Part 9): grade and the rock it costs, a copper mine's cash flows, its break-even price and the
option to wait, a cost curve, and Simon and Ehrlich's basket of five metals.

Units: tonnes, percent grades, US dollars; copper prices in dollars a pound (2,204.62 pounds a tonne).  The films
label the mines here as models and set them beside real ones (BHP's Escondida, Freeport's operations).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

LB_PER_T = 2204.62


def rock_per_tonne(grade_pct: float, recovery: float = 0.85, strip: float = 0.0) -> float:
    """Tonnes of rock that must be moved for one tonne of metal: ore at ``grade_pct`` percent, a share ``recovery``
    of the metal in it recovered, and ``strip`` tonnes of waste removed for every tonne of ore."""
    return (1.0 + strip) / (grade_pct / 100.0 * recovery)


@dataclass
class Mine:
    """An open-pit copper mine.  It mills ``mill_mtpa`` million tonnes of ore a year from a reserve of ``ore_mt``
    million tonnes at ``grade`` percent copper, falling by ``grade_fall`` (a share) each year, recovering
    ``recovery``; it moves ``strip`` tonnes of waste per tonne of ore.  Costs: ``mine_cost`` a tonne moved, ``mill_cost``
    a tonne milled, ``other`` a pound (smelting, freight, overheads), less ``credit`` a pound from by-products.  It takes
    ``capex`` million dollars over ``build`` years, and ``closure`` million at the end; the state takes ``royalty`` of
    revenue and ``tax`` of profit."""
    name: str
    ore_mt: float
    grade: float
    mill_mtpa: float
    recovery: float = 0.87
    strip: float = 2.0
    grade_fall: float = 0.02
    mine_cost: float = 2.2
    mill_cost: float = 7.0
    other: float = 0.55
    credit: float = 0.0
    capex: float = 3000.0
    build: int = 3
    closure: float = 300.0
    royalty: float = 0.04
    tax: float = 0.27

    @property
    def life(self) -> int:
        return int(round(self.ore_mt / self.mill_mtpa))

    def grades(self) -> np.ndarray:
        return self.grade * (1 - self.grade_fall) ** np.arange(self.life)

    def copper_kt(self) -> np.ndarray:
        """Copper produced each year of operation, thousand tonnes."""
        return self.mill_mtpa * 1e6 * self.grades() / 100 * self.recovery / 1e3

    def unit_cost(self) -> np.ndarray:
        """Cash cost a pound of copper, each year of operation."""
        ore = self.mill_mtpa * 1e6
        site = ore * (1 + self.strip) * self.mine_cost + ore * self.mill_cost
        lbs = self.copper_kt() * 1e3 * LB_PER_T
        return site / lbs + self.other - self.credit

    def cashflows(self, price) -> np.ndarray:
        """Cash each year from the decision ($m): building, then operating, then closing; ``price`` in dollars a pound,
        a number or a path covering every year."""
        n = self.build + self.life + 1
        p = np.full(n, float(price)) if np.isscalar(price) else np.asarray(price, float)[:n]
        cf = np.zeros(n)
        cf[:self.build] -= self.capex / self.build
        lbs = self.copper_kt() * 1e3 * LB_PER_T / 1e6  # million pounds
        for k in range(self.life):
            y = self.build + k
            rev = p[y] * lbs[k]
            cost = self.unit_cost()[k] * lbs[k]
            dep = self.capex / self.life
            royalty = self.royalty * rev
            tax = self.tax * max(rev - cost - royalty - dep, 0.0)
            cf[y] += rev - cost - royalty - tax
        cf[-1] -= self.closure
        return cf

    def npv(self, price, rate: float = 0.08) -> float:
        cf = self.cashflows(price)
        return float(np.sum(cf / (1 + rate) ** np.arange(len(cf))))

    def breakeven(self, rate: float = 0.08) -> float:
        return float(brentq(lambda p: self.npv(p, rate), 0.05, 20.0))


def wait_value(mine: Mine, p0: float, vol: float = 0.25, rate: float = 0.08, n: int = 4000, seed: int = 0) -> dict:
    """Build now, or wait a year and build only if the price then makes the mine worth building?  The price a year on
    is lognormal around ``p0`` with volatility ``vol``; the decision next year is taken at that price, held flat."""
    rng = np.random.default_rng(seed)
    p1 = p0 * np.exp(vol * rng.standard_normal(n) - vol ** 2 / 2)
    later = np.array([max(mine.npv(p, rate), 0.0) for p in p1]) / (1 + rate)
    now = mine.npv(p0, rate)
    return dict(now=now, wait=float(later.mean()), build_share=float((later > 0).mean()))


def cost_curve(points) -> list[tuple]:
    """``points`` = [(name, cost a pound, output)]; returns them sorted by cost with each one's left and right edge."""
    out, x = [], 0.0
    for name, c, q in sorted(points, key=lambda t: t[1]):
        out.append((name, c, x, x + q))
        x += q
    return out


def basket(start: dict, end: dict, stake: float = 200.0) -> float:
    """What a basket worth ``stake`` in each metal at ``start`` prices is worth at ``end`` prices."""
    return float(sum(stake * end[m] / start[m] for m in start))


def bet_windows(prices: dict, length: int = 10) -> list[tuple]:
    """Every ``length``-year window in which all metals have a price: (first year, the basket's end value relative to
    its start).  Ehrlich, who bet on scarcity, wins a window when the ratio is above 1."""
    years = sorted(set.intersection(*[set(v) for v in prices.values()]))
    out = []
    for y in years:
        if y + length in years:
            start = {m: prices[m][y] for m in prices}
            end = {m: prices[m][y + length] for m in prices}
            out.append((y, basket(start, end, 1.0) / len(prices)))
    return out
