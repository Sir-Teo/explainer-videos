"""The Works' power system (Part 13): load and load factor, the screening curve, dispatch with a price cap, a
regulated utility's revenue requirement, a gas plant bid into a week with a cold snap, a battery that buys cheap and
sells dear, and a retailer that sells at a fixed price and buys at a floating one.

Costs of technologies come from the Register (EIA's AEO2026 Electricity Market Module assumptions, Part 4); everything
else here is arithmetic, and the parameters of the games are this series' illustrations, labelled as models on screen.
No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

HOURS = 8760


# ----------------------------------------------------------------------------------------------- load
def load_factor(load: list[float] | np.ndarray) -> float:
    """Average load over peak load: how much of the capacity needed for the peak is used on average."""
    a = np.asarray(load, dtype=float)
    return float(a.mean() / a.max())


def diversity(peaks: list[float], combined_peak: float) -> float:
    """Insull's diversity factor: the sum of customers' own peaks over the peak of their combined load."""
    return float(sum(peaks) / combined_peak)


# ----------------------------------------------------------------------------------------------- screening curve
def annuity(rate: float, years: int) -> float:
    """Capital recovery factor: the share of an investment repaid each year to earn ``rate`` over ``years``."""
    return rate / (1 - (1 + rate) ** -years)


@dataclass(frozen=True)
class Tech:
    name: str
    overnight: float      # $ per kW
    fom: float            # $ per kW-year
    vom: float            # $ per MWh
    heat: float           # Btu per kWh (0 or 3,412 for no fuel)
    fuel: float = 0.0     # $ per million Btu
    life: int = 30

    def fixed(self, rate: float = 0.07) -> float:
        """$ per kW-year of capacity, whether it runs or not."""
        return self.overnight * annuity(rate, self.life) + self.fom

    def running(self) -> float:
        """$ per MWh of output: fuel plus variable O&M."""
        burns = self.fuel > 0 and self.heat > 0
        return (self.heat / 1000.0) * self.fuel * burns + self.vom

    def per_kw_year(self, cf: float, rate: float = 0.07) -> float:
        """Total $ per kW-year at capacity factor ``cf`` (share of the year's hours it runs)."""
        return self.fixed(rate) + self.running() * cf * HOURS / 1000.0

    def per_mwh(self, cf: float, rate: float = 0.07) -> float:
        return self.per_kw_year(cf, rate) * 1000.0 / (cf * HOURS) if cf > 0 else float("inf")


def crossover(a: Tech, b: Tech, rate: float = 0.07) -> float | None:
    """Capacity factor above which ``b`` (higher fixed, lower running cost) is cheaper than ``a``."""
    dv = (a.running() - b.running()) * HOURS / 1000.0
    if dv <= 0:
        return None
    return (b.fixed(rate) - a.fixed(rate)) / dv


# ----------------------------------------------------------------------------------------------- dispatch
@dataclass(frozen=True)
class Unit:
    name: str
    mw: float
    cost: float           # $ per MWh offered (marginal cost)


def dispatch(units: list[Unit], demand: float, cap: float = 9000.0, available: dict | None = None) -> dict:
    """Run units cheapest first until demand is met.  The price is the offer of the last unit needed, or ``cap`` (the
    value of lost load) when there is not enough; ``shed`` is the demand that cannot be served.  ``available`` maps a
    unit's name to the share of it that can run."""
    available = available or {}
    left = demand
    out, price = {}, 0.0
    for u in sorted(units, key=lambda u: u.cost):
        mw = u.mw * available.get(u.name, 1.0)
        take = min(mw, max(left, 0.0))
        out[u.name] = take
        if take > 0:
            price = u.cost
        left -= take
    shed = max(left, 0.0)
    return {"price": cap if shed > 1e-9 else price, "run": out, "shed": shed}


# ----------------------------------------------------------------------------------------------- the regulated utility
@dataclass(frozen=True)
class Utility:
    rate_base: float          # $ million of plant and wires, net of depreciation
    roe: float = 0.10         # allowed return on equity
    equity: float = 0.52      # share of the rate base financed with equity
    debt_cost: float = 0.05
    om: float = 900.0         # $ million a year of operations and maintenance
    depreciation: float = 0.035   # share of the rate base a year
    tax: float = 0.21         # on the equity return
    sales: float = 40.0       # TWh a year

    def wacc(self) -> float:
        return self.equity * self.roe + (1 - self.equity) * self.debt_cost

    def requirement(self) -> dict:
        """The revenue requirement, $ million a year, line by line, and the price it implies in cents per kWh."""
        ret = self.rate_base * self.wacc()
        tax = self.rate_base * self.equity * self.roe * self.tax / (1 - self.tax)
        dep = self.rate_base * self.depreciation
        total = self.om + dep + tax + ret
        return {"om": self.om, "depreciation": dep, "tax": tax, "return": ret, "total": total,
                "cents": total / (self.sales * 1e3) * 100}


# ----------------------------------------------------------------------------------------------- Run it: a week with a cold snap
# A week of hourly prices for an energy-only market, the series' illustration of a cold snap: normal days around the
# cost of a gas plant, then two days at the cap.  The plant's own fuel can fail in the cold.
WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def week_prices(normal: float = 35.0, cap: float = 9000.0, snap_days: tuple = (3, 4), seed: int = 13) -> np.ndarray:
    """168 hourly prices: a daily shape around ``normal`` and the cap through the cold snap's days."""
    rng = np.random.default_rng(seed)
    h = np.arange(168)
    shape = 1 + 0.35 * np.sin((h % 24 - 9) / 24 * 2 * np.pi) + 0.05 * rng.standard_normal(168)
    p = normal * shape
    for d in snap_days:
        p[d * 24:(d + 1) * 24] = cap
    p[(snap_days[0] * 24) - 6:snap_days[0] * 24] = np.linspace(normal * 2, cap / 4, 6)
    return np.round(p, 1)


@dataclass
class GasPlantWeek:
    mw: float = 500.0
    cost: float = 30.0          # $ per MWh at normal gas prices
    snap_cost: float = 300.0    # $ per MWh when gas itself is scarce
    hedge: float = 0.0          # share of output sold forward at ``forward``
    forward: float = 40.0
    fails: bool = False         # does it freeze during the snap?
    snap_days: tuple = (3, 4)
    log: list = field(default_factory=list)

    def play(self, prices: np.ndarray) -> dict:
        """Cash, hour by hour: the plant runs when the price covers its cost (if it can), sells its hedge at the
        forward price, and settles any shortfall against the hedge at the spot price."""
        cash = np.zeros(len(prices))
        for t, p in enumerate(prices):
            snap = (t // 24) in self.snap_days
            c = self.snap_cost if snap else self.cost
            can = not (snap and self.fails)
            run = self.mw if (can and p >= c) else 0.0
            sold = self.hedge * self.mw
            cash[t] = sold * self.forward + (run - sold) * p - run * c
        return {"hourly": cash, "total": float(cash.sum()) / 1e6, "cum": np.cumsum(cash) / 1e6}


def run_it(prices: np.ndarray | None = None) -> dict:
    """The four outcomes of chapter 1, $ million for the week."""
    p = week_prices() if prices is None else prices
    out = {}
    for name, hedge, fails in (("spot, runs", 0.0, False), ("hedged, runs", 1.0, False), ("spot, freezes", 0.0, True),
                               ("hedged, freezes", 1.0, True)):
        out[name] = GasPlantWeek(hedge=hedge, fails=fails).play(p)
    return out


# ----------------------------------------------------------------------------------------------- storage
def battery(prices: list[float] | np.ndarray, mw: float = 100.0, hours: float = 4.0, efficiency: float = 0.85) -> dict:
    """A battery that each day charges in the cheapest hours and discharges in the dearest, as many hours as its
    energy allows.  Returns the profit and the hours it charged and discharged."""
    p = np.asarray(prices, dtype=float)
    days = len(p) // 24
    n = int(round(hours))
    charge, discharge, profit = [], [], 0.0
    for d in range(days):
        day = p[d * 24:(d + 1) * 24]
        order = np.argsort(day)
        lo, hi = sorted(order[:n]), sorted(order[-n:])
        gain = day[hi].sum() * mw * efficiency - day[lo].sum() * mw
        if gain > 0:
            profit += gain
            charge += [d * 24 + int(i) for i in lo]
            discharge += [d * 24 + int(i) for i in hi]
    return {"profit": profit, "charge": charge, "discharge": discharge}


# ----------------------------------------------------------------------------------------------- the retailer
def retailer(wholesale: list[float], fixed_price: float, hedge: float, hedge_price: float, other: float = 0.0) -> dict:
    """A supplier that sells at ``fixed_price`` (per unit) and buys ``hedge`` of its needs at ``hedge_price`` and the
    rest at the wholesale price each period.  Returns the margin per unit each period and in total."""
    m = [fixed_price - other - (hedge * hedge_price + (1 - hedge) * w) for w in wholesale]
    return {"margin": m, "total": float(sum(m))}
