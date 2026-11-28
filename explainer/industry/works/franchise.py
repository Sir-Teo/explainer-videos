"""The Works' restaurant and franchise (Part 34): a franchisee's store for a year, and a franchisor setting its fees.

The franchisee pays for the kitchen, the seats and the sign, runs the store, and pays the franchisor rent and royalties
as a share of sales, plus a share into the advertising fund.  The franchisor collects those fees from every store it
can persuade someone to open; set them too high and fewer franchisees can earn their money back in time, so the system
grows more slowly.  No manim.

    >>> s = Store()
    >>> round(s.year()["profit"] / 1e3)
    368
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass(frozen=True)
class Store:
    """A franchised quick-service restaurant for a year.  Shares are of sales."""

    sales: float = 4.0e6            # a year's sales
    food: float = 0.31              # food and paper
    labour: float = 0.30            # crew and managers at normal sales
    labour_fixed: float = 0.6       # the part of labour that does not move with sales (minimum crews, managers)
    fees: float = 0.128             # rent and royalties to the franchisor
    ad: float = 0.04                # the advertising fund
    other: float = 0.10             # utilities, repairs, insurance, card fees and the rest
    delivery: float = 0.15          # the share of sales that comes through delivery apps
    commission: float = 0.20        # the apps' commission on those sales
    invest: float = 1.5e6           # the franchisee's own investment: equipment, seating, signs, decor
    wage: float = 1.0               # wages against today's

    def with_(self, **kw) -> "Store":
        return replace(self, **kw)

    def year(self, sales: float | None = None) -> dict:
        """The store's year at ``sales`` (default its normal sales); labour partly fixed, partly moving with sales."""
        s = self.sales if sales is None else sales
        base = self.sales
        food = self.food * s
        lab = self.wage * self.labour * (self.labour_fixed * base + (1 - self.labour_fixed) * s)
        fees = self.fees * s
        ad = self.ad * s
        other = self.other * s
        apps = self.delivery * self.commission * s
        profit = s - food - lab - fees - ad - other - apps
        return dict(sales=s, food=food, labour=lab, fees=fees, ad=ad, other=other, apps=apps, profit=profit,
                    margin=profit / s if s else float("nan"),
                    payback=self.invest / profit if profit > 0 else float("inf"))


@dataclass(frozen=True)
class Franchisor:
    """A franchisor choosing its take (rent and royalties as a share of each store's sales).  Each year a pool of would-be
    franchisees considers opening a store; each opens if the store would pay back their investment within their own
    patience, which differs from person to person (lognormal around a median).  Fees are charged on every open store;
    the franchisor's own costs are a share of its fees plus a fixed overhead."""

    store: Store = Store()
    pool: float = 400.0             # would-be franchisees considering a store each year
    patience: float = 5.0           # the median franchisee's longest acceptable payback, years
    spread: float = 0.35            # the spread (log standard deviation) of patience
    start: int = 1000               # stores open at the start
    years: int = 10
    cost_share: float = 0.16        # the franchisor's costs on its fees (the property it leases to franchisees, mostly)
    overhead: float = 60e6          # its offices, menu, training and inspectors a year

    def with_(self, **kw) -> "Franchisor":
        return replace(self, **kw)

    def opening_rate(self, take: float) -> float:
        """The share of the pool that opens a store at this take."""
        pb = self.store.with_(fees=take).year()["payback"]
        if not math.isfinite(pb):
            return 0.0
        return 1.0 - _phi((math.log(pb) - math.log(self.patience)) / self.spread)

    def run(self, take: float) -> dict:
        st = self.store.with_(fees=take)
        rate = self.opening_rate(take)
        n = float(self.start)
        stores, profit = [], []
        for _ in range(self.years):
            n += self.pool * rate
            fees = n * st.sales * take
            stores.append(n)
            profit.append(fees * (1 - self.cost_share) - self.overhead)
        return dict(take=take, rate=rate, opened=self.pool * rate * self.years, stores=stores, profit=profit,
                    total=sum(profit), last=profit[-1], franchisee=st.year())

    def sweep(self, takes) -> dict:
        return {t: self.run(t) for t in takes}
