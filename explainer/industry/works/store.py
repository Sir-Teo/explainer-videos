"""The Works' store: a supermarket's year on a two per cent margin, with its price level and its staffing as levers, and
the float a fast-turning retailer earns from its suppliers.  Numpy only.

The store sells ``sales`` dollars a year at price level 1 with gross margin ``gm`` (so goods cost (1 - gm) of base sales
per unit of volume).  Raising its price level to p changes its volume by p ** elasticity (shoppers have rivals nearby);
cutting staff hours to s of normal loses customers to queues, empty shelves and shrink, 1 - 0.6 (1 - s) - 1.5 (1 - s)^2
below normal hours and 1 + 0.3 (s - 1) - (s - 1)^2 above.  Labour is ``labour`` of base sales times s; occupancy is fixed;
other costs are ``other`` of revenue.

The float: inventory sits ``inv_days`` days before it is sold, suppliers are paid after ``pay_days``; the difference times
a day's cost of goods is cash the suppliers lend the retailer.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class Store:
    sales: float = 50e6
    gm: float = 0.233          # Kroger's gross margin, 2025
    labour: float = 0.11
    occupancy: float = 0.03
    other: float = 0.07
    elasticity: float = -5.7

    def volume(self, p: float = 1.0, s: float = 1.0) -> float:
        v = p ** self.elasticity
        if s < 1:
            v *= 1 - 0.6 * (1 - s) - 1.5 * (1 - s) ** 2
        else:
            v *= 1 + 0.3 * (s - 1) - (s - 1) ** 2
        return v

    def year(self, p: float = 1.0, s: float = 1.0) -> dict:
        v = self.volume(p, s)
        revenue = self.sales * p * v
        goods = self.sales * (1 - self.gm) * v
        labour = self.sales * self.labour * s
        occ = self.sales * self.occupancy
        other = revenue * self.other
        profit = revenue - goods - labour - occ - other
        return dict(revenue=revenue, goods=goods, gross=revenue - goods, labour=labour, occupancy=occ, other=other,
                    profit=profit, margin=profit / revenue, volume=v)

    def breakeven_volume(self, cut: float) -> float:
        """The rise in volume that keeps profit unchanged after cutting prices by ``cut`` (labour and rent fixed)."""
        base = self.year()
        unit = (1 - cut) * (1 - self.other) - (1 - self.gm)       # contribution per unit of base sales after the cut
        need = (base["profit"] + base["labour"] + base["occupancy"]) / (self.sales * unit)
        return need - 1

    def best_price(self, grid=None) -> float:
        grid = np.linspace(0.9, 1.1, 201) if grid is None else grid
        return float(grid[int(np.argmax([self.year(p)["profit"] for p in grid]))])

    def but(self, **kw) -> "Store":
        return replace(self, **kw)


def float_days(inventory: float, payables: float, cogs: float) -> dict:
    """Days of inventory and of payables, and the cash suppliers fund (payables less inventory), from annual cost of goods."""
    day = cogs / 365.0
    return dict(inv_days=inventory / day, pay_days=payables / day, funded=payables - inventory)
