"""The Works' distributor (Part 33): a wholesaler that buys from makers in bulk, holds the stock, sells on credit and
delivers to many small customers, on a margin of a few cents.

Its choices: how much safety stock to hold (more stock fills more orders, ties up more money, and customers who are let
down take their orders elsewhere); whether to hold stock at all or have the maker ship each order direct (drop-ship);
and how much of a town's customers to serve on one delivery route (density).  No manim.

    >>> d = Distributor()
    >>> round(d.year()["profit"] / 1e6, 1)
    83.3
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass(frozen=True)
class Distributor:
    """A distributor for a year, with a drug wholesaler's margins by default.  Money in dollars, time in days."""

    sales: float = 5.0e9            # sales a year when every order is filled
    gm: float = 0.036               # gross margin: sales less the cost of the goods, a share of sales
    opex: float = 0.021             # warehouses, trucks and people, a share of base sales (they do not shrink with a bad year)
    lead: float = 14.0              # days from ordering to receiving from the maker
    review: float = 14.0            # days between orders to the maker
    cv: float = 1.0                 # variability of a line's daily demand (standard deviation over mean)
    loss: float = 0.02              # share of sales lost for each point of fill rate below 99%
    recv: float = 25.0              # days customers take to pay
    pay: float = 56.0               # days the distributor takes to pay makers
    wacc: float = 0.08              # the cost of capital, charged on money tied up (and earned on money held for others)
    z: float = 2.0                  # safety stock, in standard deviations of demand over the lead time and review period
    # drop-shipping: the maker ships each order direct
    drop_lead: float = 4.0          # days a drop-shipped order takes to arrive
    drop_keep: float = 0.55         # share of sales kept when customers must wait for drop-shipped orders
    drop_gm: float = 0.020          # the margin a distributor earns for passing an order on without holding the stock
    drop_opex: float = 0.008        # its costs, as a share of base sales

    def with_(self, **kw) -> "Distributor":
        return replace(self, **kw)

    def fill(self, z: float | None = None) -> float:
        """The share of order lines filled from stock (the cycle service level)."""
        return _phi(self.z if z is None else z)

    def stock_days(self, z: float | None = None) -> float:
        """Days of stock: half a review period of cycle stock plus safety stock."""
        z = self.z if z is None else z
        return self.review / 2 + max(z, 0.0) * self.cv * math.sqrt(self.lead + self.review)

    def volume(self, z: float | None = None) -> float:
        return max(1.0 - self.loss * max(0.0, 99.0 - 100.0 * self.fill(z)), 0.0)

    def year(self, z: float | None = None) -> dict:
        z = self.z if z is None else z
        v = self.volume(z)
        s = self.sales * v
        cogs = s * (1 - self.gm)
        gp = s - cogs
        opex = self.opex * self.sales
        op = gp - opex
        inv = cogs / 365 * self.stock_days(z)
        rec = s / 365 * self.recv
        ap = cogs / 365 * self.pay
        cap = inv + rec - ap
        charge = self.wacc * cap
        return dict(sales=s, volume=v, fill=self.fill(z), gp=gp, opex=opex, op=op, inventory=inv, receivables=rec,
                    payables=ap, capital=cap, charge=charge, profit=op - charge, margin=op / s if s else float("nan"),
                    stock_days=self.stock_days(z))

    def drop_ship(self) -> dict:
        """The same customers served without holding stock: the maker ships each order direct."""
        s = self.sales * self.drop_keep
        gp = s * self.drop_gm
        opex = self.drop_opex * self.sales
        op = gp - opex
        rec = s / 365 * self.recv
        ap = s * (1 - self.drop_gm) / 365 * self.pay
        cap = rec - ap
        charge = self.wacc * cap
        return dict(sales=s, gp=gp, opex=opex, op=op, inventory=0.0, receivables=rec, payables=ap, capital=cap,
                    charge=charge, profit=op - charge, margin=op / s)

    def best_z(self, lo: float = 0.0, hi: float = 3.5, n: int = 351) -> float:
        zs = [lo + (hi - lo) * k / (n - 1) for k in range(n)]
        return max(zs, key=lambda z: self.year(z)["profit"])


@dataclass(frozen=True)
class Route:
    """A delivery truck's day: it drives out from the depot, stops at customers spread across a town, and drives back.
    The more of the town's customers a distributor serves, the closer together its stops."""

    density: float = 1.0            # customers of this kind per square mile
    shift: float = 10.0             # hours a driver works
    stem: float = 1.0               # hours to and from the delivery area, together
    service: float = 0.25           # hours at each stop
    speed: float = 20.0             # miles an hour between stops
    cost: float = 900.0             # a truck and driver for a day
    drops: float = 5000.0           # dollars of goods delivered at a stop

    def stops(self, share: float) -> float:
        spacing = 1.0 / math.sqrt(max(self.density * share, 1e-9))   # miles between neighbouring customers served
        return (self.shift - self.stem) / (self.service + spacing / self.speed)

    def cost_per_stop(self, share: float) -> float:
        return self.cost / self.stops(share)

    def cost_share(self, share: float) -> float:
        """Delivery cost as a share of the goods delivered."""
        return self.cost_per_stop(share) / self.drops


def margin_turns(margin: float, turns: float) -> float:
    """Return on capital as margin times turns (sales over capital)."""
    return margin * turns
