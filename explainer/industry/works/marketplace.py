"""The Works' marketplace (Part 32): a platform that brings buyers and sellers together, takes a share of every sale,
sells advertising to its sellers and delivers the orders; and a direct brand that buys its customers.

Both sides choose whether to join.  A buyer comes for selection (more sellers), low prices, fast delivery and results that
are not crowded with ads; a seller comes if what it keeps from its sales, after the platform's fees and its advertising,
covers its own fixed costs, which differ from seller to seller.  Each side's size depends on the other's, so the
platform's choices (its take rate, its ad load, its delivery promise) are solved for the point where both sides settle.
No manim.

    >>> m = Marketplace()
    >>> s = m.solve()
    >>> round(s["gmv"] / 1e9), round(s["profit"] / 1e9, 1)
    (37, 3.9)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace


def _logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass(frozen=True)
class Marketplace:
    """A marketplace for a year.  Money in dollars; buyers and sellers in people and firms."""

    buyers_max: float = 100e6       # people who might shop here
    sellers_max: float = 1.0e6      # firms that might sell here
    basket: float = 40.0            # dollars an order
    orders: float = 15.0            # orders a buyer places a year with the reference selection and a two-day promise
    margin: float = 0.55            # a seller's price less what the goods cost it, a share of the price
    take: float = 0.30              # commission and fulfilment fees, a share of what buyers pay
    ad: float = 0.06                # what sellers spend on ads on the platform, a share of what buyers pay
    days: float = 2.0               # the delivery promise
    pass_through: float = 0.5       # the share of fees above the reference that sellers put into their prices
    fixed_median: float = 60e3      # the median seller's own fixed costs a year
    fixed_spread: float = 1.2       # the spread (log standard deviation) of sellers' fixed costs
    # buyers' tastes: a constant, the pull of selection, the push of price, of slow delivery and of ad clutter
    b0: float = 0.2
    b_sel: float = 0.8
    b_price: float = 0.12           # per percent of price above the reference
    b_days: float = 0.6             # per day beyond two
    b_ads: float = 8.0              # per unit of ad load beyond the reference
    sel_ref: float = 200e3          # the reference number of sellers
    take_ref: float = 0.30
    ad_ref: float = 0.06
    # the platform's costs
    ship_var: float = 5.0           # dollars an order to pick, pack and carry, before speed
    ship_speed: float = 2.0         # dollars an order divided by the promise in days
    network: float = 4.0e9          # fixed cost of the network a year, divided by the promise in days
    payments: float = 0.025         # card and payment costs, a share of what buyers pay
    overhead: float = 1.0e9         # technology and staff a year

    def with_(self, **kw) -> "Marketplace":
        return replace(self, **kw)

    def price_index(self) -> float:
        """Buyers' prices against the reference, from the fees sellers pass on."""
        return 1.0 + self.pass_through * ((self.take + self.ad) - (self.take_ref + self.ad_ref))

    def buyer_share(self, sellers: float) -> float:
        x = (self.b0 + self.b_sel * math.log(max(sellers, 1.0) / self.sel_ref)
             - self.b_price * 100 * (self.price_index() - 1) - self.b_days * (self.days - 2.0)
             - self.b_ads * (self.ad - self.ad_ref))
        return _logistic(x)

    def orders_per_buyer(self, sellers: float) -> float:
        sel = 1.0 + 0.15 * math.log(max(sellers, 1.0) / self.sel_ref)
        speed = 1.0 + 0.12 * (2.0 - self.days)
        return max(self.orders * sel * speed, 0.0)

    def seller_share(self, gmv_per_seller: float) -> float:
        keep = gmv_per_seller * (self.margin - self.take - self.ad)
        if keep <= 0:
            return 0.0
        return _norm_cdf((math.log(keep) - math.log(self.fixed_median)) / self.fixed_spread)

    def solve(self, iters: int = 4000) -> dict:
        """Settle both sides: buyers depend on sellers and sellers on buyers' spending; damped fixed-point iteration."""
        S = 0.2 * self.sellers_max
        for _ in range(iters):
            B = self.buyers_max * self.buyer_share(S)
            n = B * self.orders_per_buyer(S)
            gmv = n * self.basket                                               # dollars buyers pay
            S_new = self.sellers_max * self.seller_share(gmv / max(S, 1.0))
            if abs(S_new - S) < 1.0:
                S = S_new
                break
            S = 0.7 * S + 0.3 * max(S_new, 1.0)
        B = self.buyers_max * self.buyer_share(S)
        n = B * self.orders_per_buyer(S)
        gmv = n * self.basket
        fees, ads = self.take * gmv, self.ad * gmv
        ship = n * (self.ship_var + self.ship_speed / self.days)
        network = self.network / self.days
        pay = self.payments * gmv
        profit = fees + ads - ship - network - pay - self.overhead
        return dict(buyers=B, sellers=S, orders=n, gmv=gmv, fees=fees, ads=ads, revenue=fees + ads, ship=ship,
                    network=network, payments=pay, overhead=self.overhead, profit=profit,
                    cost_per_order=(ship + network) / n if n else float("nan"),
                    seller_keep=self.margin - self.take - self.ad, price=self.price_index())

    def sweep(self, name: str, values) -> dict:
        return {v: self.with_(**{name: v}).solve() for v in values}


def cost_per_order(orders: float, days: float = 2.0, ship_var: float = 5.0, ship_speed: float = 2.0,
                   network: float = 4.0e9) -> float:
    """The cost of delivering an order when a network whose fixed cost grows with speed is spread over ``orders``."""
    return ship_var + ship_speed / days + network / days / orders


@dataclass(frozen=True)
class Brand:
    """A direct-to-consumer brand that buys its customers with ads.  A customer costs ``cac`` to acquire, places a first
    order of ``first`` dollars, and each later year is still buying with probability ``retention``, spending ``repeat``."""

    cac: float = 60.0
    first: float = 80.0
    repeat: float = 120.0
    margin: float = 0.45            # contribution after goods, shipping and returns, a share of sales
    retention: float = 0.40

    def with_(self, **kw) -> "Brand":
        return replace(self, **kw)

    def cumulative(self, years: int = 5) -> list[float]:
        """A customer's cumulative contribution less the cost of acquiring them, at the end of each year (year 0 is the
        first order)."""
        out, total, alive = [], self.first * self.margin - self.cac, 1.0
        out.append(total)
        for _ in range(years):
            alive *= self.retention
            total += alive * self.repeat * self.margin
            out.append(total)
        return out

    def lifetime(self) -> float:
        r = self.retention
        return self.first * self.margin + self.repeat * self.margin * r / (1 - r) - self.cac

    def payback_year(self, years: int = 10):
        for y, v in enumerate(self.cumulative(years)):
            if v >= 0:
                return y
        return None
