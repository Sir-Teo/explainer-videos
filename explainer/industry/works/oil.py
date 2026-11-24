"""The Works' oil industry (Part 8): a well that declines, a field's cash flows and break-even price, a shale treadmill,
a refinery's crack spread, the price that clears a supply loss, and a price that wanders.

Numbers here are models.  The films label them as such and set them beside the real ones (EIA's production and
prices, the Dallas Fed's break-evens, Saudi Aramco's lifting cost).  Units: barrels a day (b/d), dollars a barrel,
years, millions of dollars.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq

DAYS = 365.0


# --- a well ------------------------------------------------------------------------------------------------------
def arps(t, qi: float, di: float, b: float):
    """Arps's decline: the rate (b/d) after ``t`` years, from an initial rate ``qi`` and an initial decline ``di`` a
    year.  ``b`` = 0 is exponential, 0 < b < 1 hyperbolic (shale wells fit b near 1), b = 1 harmonic."""
    t = np.asarray(t, dtype=float)
    if b == 0:
        return qi * np.exp(-di * t)
    return qi / (1.0 + b * di * t) ** (1.0 / b)


def arps_cum(t, qi: float, di: float, b: float):
    """Barrels produced by ``t`` years (the integral of ``arps``, in barrels)."""
    t = np.asarray(t, dtype=float)
    if b == 0:
        return qi * DAYS * (1 - np.exp(-di * t)) / di
    if b == 1:
        return qi * DAYS * np.log1p(di * t) / di
    return qi * DAYS / ((1 - b) * di) * (1 - (1 + b * di * t) ** (1 - 1 / b))


def first_year_decline(di: float, b: float) -> float:
    """How far the rate falls over the first year, as a share of the initial rate."""
    return float(1 - arps(1.0, 1.0, di, b))


# --- a field ------------------------------------------------------------------------------------------------------
@dataclass
class Field:
    """A development: spend ``capex`` ($m) over ``build`` years, then produce from ``wells`` wells that each start at
    ``qi`` b/d and decline by Arps (``di``, ``b``), for ``life`` years.  Each barrel costs ``opex`` to lift; the state
    takes a ``royalty`` share of revenue and a ``tax`` share of profit after costs and depreciation."""
    name: str
    capex: float
    build: int
    wells: int
    qi: float
    di: float
    b: float
    life: int
    opex: float
    royalty: float = 0.125
    tax: float = 0.21
    note: str = ""

    def barrels(self) -> np.ndarray:
        """Barrels produced in each year from the decision (year 0), millions."""
        out = np.zeros(self.build + self.life)
        for y in range(self.life):
            out[self.build + y] = self.wells * (arps_cum(y + 1, self.qi, self.di, self.b) -
                                                arps_cum(y, self.qi, self.di, self.b)) / 1e6
        return out

    def cashflows(self, price) -> np.ndarray:
        """Cash after royalty, operating cost, capital and tax in each year ($m), at a price (a number or a path)."""
        q = self.barrels()
        n = len(q)
        p = np.full(n, float(price)) if np.isscalar(price) else np.asarray(price, float)[:n]
        spend = np.zeros(n)
        spend[:max(self.build, 1)] = self.capex / max(self.build, 1)
        rev = p * q
        royalty = self.royalty * rev
        opex = self.opex * q
        dep = np.zeros(n)
        if q.sum() > 0:
            dep = self.capex * q / q.sum()  # unit of production
        taxable = rev - royalty - opex - dep
        tax = self.tax * np.maximum(taxable, 0)
        return rev - royalty - opex - tax - spend

    def npv(self, price, rate: float = 0.10) -> float:
        cf = self.cashflows(price)
        return float(np.sum(cf / (1 + rate) ** np.arange(len(cf))))

    def breakeven(self, rate: float = 0.10) -> float:
        """The flat price at which the development just earns ``rate``."""
        return float(brentq(lambda p: self.npv(p, rate), 0.01, 500.0))

    def state_take(self, price: float) -> float:
        """Royalty and tax as a share of the profit before them (undiscounted, over the field's life)."""
        q = self.barrels()
        rev = price * q.sum()
        pre = rev - self.opex * q.sum() - self.capex
        royalty = self.royalty * rev
        tax = self.tax * max(rev - royalty - self.opex * q.sum() - self.capex, 0)
        return float((royalty + tax) / pre) if pre > 0 else float("nan")


def prospects() -> list[Field]:
    """Three illustrative developments for the film's game: a conventional onshore field, a deepwater platform and
    a pad of shale wells.  Round, plausible numbers for a model, not any company's."""
    return [
        Field("Conventional onshore", capex=700, build=2, wells=40, qi=700, di=0.10, b=0.3, life=25, opex=14,
              note="slow decline, long life"),
        Field("Deepwater platform", capex=6000, build=5, wells=12, qi=15000, di=0.15, b=0.5, life=20, opex=14,
              note="years to build, a very large flow"),
        Field("Shale pad", capex=120, build=1, wells=10, qi=650, di=1.5, b=1.0, life=15, opex=15,
              note="cheap, fast, and steep"),
    ]


# --- shale: a treadmill -----------------------------------------------------------------------------------------
def treadmill(new_wells_per_month, qi: float = 1000, di: float = 1.2, b: float = 1.0) -> np.ndarray:
    """Total output (b/d) of a basin that brings on ``new_wells_per_month[k]`` wells in month k, each declining by
    Arps from ``qi``."""
    n = np.asarray(new_wells_per_month, float)
    months = len(n)
    out = np.zeros(months)
    rates = arps(np.arange(months) / 12.0, qi, di, b)
    for k in range(months):
        out[k:] += n[k] * rates[:months - k]
    return out


def wells_to_hold(level: float, qi: float = 1000, di: float = 1.2, b: float = 1.0, months: int = 600) -> float:
    """New wells a month needed to hold a basin's output steady at ``level`` b/d, once old wells have settled."""
    per_well = arps(np.arange(months) / 12.0, qi, di, b).sum()
    return float(level / per_well)


# --- the market: inelastic both ways ------------------------------------------------------------------------------
def clearing_multiple(loss: float, eps_d: float = -0.05, eps_s: float = 0.05) -> float:
    """By how much the price must multiply to clear a market that loses a share ``loss`` of its supply, with
    constant elasticities of demand (negative) and supply: m = (1 - loss) ** (1 / (eps_d - eps_s))."""
    return float((1.0 - loss) ** (1.0 / (eps_d - eps_s)))


def price_paths(n: int, years: int, p0: float = 70.0, vol: float = 0.30, revert: float = 0.25, mean: float = 70.0,
                seed: int = 0) -> np.ndarray:
    """``n`` annual price paths that wander: log price reverts towards ``mean`` at ``revert`` a year, with yearly
    shocks of ``vol``."""
    rng = np.random.default_rng(seed)
    out = np.zeros((n, years))
    lp = np.full(n, np.log(p0))
    for y in range(years):
        out[:, y] = np.exp(lp)
        lp = lp + revert * (np.log(mean) - lp) + vol * rng.standard_normal(n)
    return out


# --- refining ------------------------------------------------------------------------------------------------------
def crack_321(crude: float, gasoline_gal: float, distillate_gal: float) -> float:
    """The 3-2-1 crack spread, dollars a barrel of crude: two barrels of gasoline and one of distillate, less three of
    crude, per barrel of crude (product prices in dollars a gallon; 42 gallons a barrel)."""
    return (2 * gasoline_gal * 42 + distillate_gal * 42 - 3 * crude) / 3


@dataclass
class Refinery:
    """A refinery as a spread business: it buys crude, sells a yield of products, and pays a cash cost a barrel."""
    capacity: float = 300_000          # b/d
    yields: dict = field(default_factory=lambda: {"gasoline": 0.46, "distillate": 0.30, "jet": 0.09, "other": 0.15})
    cash_cost: float = 6.0             # $/bbl

    def margin(self, crude: float, prices: dict) -> float:
        """Gross margin less cash cost, dollars a barrel of crude (product prices in dollars a barrel)."""
        value = sum(self.yields[k] * prices[k] for k in self.yields)
        return value - crude - self.cash_cost

    def profit(self, crude: float, prices: dict, utilisation: float = 0.9) -> float:
        """Cash profit a year, $m."""
        return self.margin(crude, prices) * self.capacity * utilisation * DAYS / 1e6
