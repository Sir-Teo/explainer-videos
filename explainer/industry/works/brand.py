"""The Works' brand (Part 22): a branded product against a store label on the same shelf.  Shoppers choose between them by
price and by how well they know the brand, which advertising builds up as a stock that wears off; the brand manager sets
the price and the advertising.  Cutting the advertising makes this year's profit look better and every later year's
worse; cutting the price wins share but gives away margin on every unit.

Shares follow a logit: the brand's utility is k * sqrt(stock) - beta * price + c, the store label's -beta * its price.  The
stock of advertising decays by ``decay`` a year and is topped up by the year's spending.  All numbers are this series'
illustrations; P&G's gross margin (50.2%) and advertising (11.7% of sales) in fiscal 2026 are the anchors.  No manim here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Brand:
    units: float = 500e6       # units a year bought in the category, brand and store label together
    price: float = 10.0        # the brand's shelf price, $
    store_price: float = 5.0   # the store label's price, $
    unit_cost: float = 4.0     # the brand's cost to make and ship a unit, $
    beta: float = 0.45         # how much a dollar of price difference matters
    k: float = 0.05            # how much the stock of advertising matters
    decay: float = 0.2         # share of the advertising stock that wears off each year
    ads: float = 100.0         # advertising a year, $m (the steady budget)
    target: float = 0.45       # the brand's share at the steady budget and price
    rate: float = 0.08

    def steady_stock(self) -> float:
        return self.ads / self.decay

    def constant(self) -> float:
        """The brand's intercept c, set so its share is ``target`` at the steady stock and its own price."""
        odds = math.log(self.target / (1 - self.target))
        return odds - (self.k * math.sqrt(self.steady_stock()) - self.beta * (self.price - self.store_price))

    def share(self, stock: float, price: float | None = None, store_price: float | None = None) -> float:
        """The brand's share at an advertising ``stock``; ``price`` and ``store_price`` default to the calibrated ones (the
        brand's constant stays as calibrated, so a different store price moves the share)."""
        p = self.price if price is None else price
        sp = self.store_price if store_price is None else store_price
        ub = self.k * math.sqrt(max(stock, 0.0)) - self.beta * p + self.constant()
        us = -self.beta * sp
        return 1 / (1 + math.exp(us - ub))

    def run(self, ads, price: float | None = None, store_price: float | None = None) -> dict:
        """Years of advertising budgets ``ads`` ($m) at ``price`` (and the store label at ``store_price``), starting from
        the steady stock: each year's stock, share, profit ($m, after advertising) and the discounted total."""
        p = self.price if price is None else price
        stock, rows, npv = self.steady_stock(), [], 0.0
        for t, a in enumerate(ads):
            stock = (1 - self.decay) * stock + a
            s = self.share(stock, p, store_price)
            profit = s * self.units * (p - self.unit_cost) / 1e6 - a
            rows.append({"year": t + 1, "stock": stock, "share": s, "profit": profit})
            npv += profit / (1 + self.rate) ** (t + 1)
        return {"rows": rows, "npv": npv}

    def choices(self, years: int = 8, promo_price: float = 8.0) -> dict:
        """Run it: hold (the steady budget and price), cut the advertising to nothing, or cut the price."""
        return {"hold": self.run([self.ads] * years), "cut": self.run([0.0] * years),
                "promote": self.run([self.ads] * years, price=promo_price)}


def premium(price: float, cost: float) -> float:
    """How many times its cost a product sells for."""
    return price / cost
