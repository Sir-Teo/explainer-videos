"""The Works' freight: a truck on an unbalanced lane, a trucking market whose capacity enters fast and leaves slowly, a
railway whose cost per ton-mile falls with traffic density, a delivery route whose cost per package falls with the
density of stops, and the arithmetic of hubs.  Numpy only.

The truck: ``nonfuel`` dollars a mile driven, loaded or empty, plus diesel at ``diesel`` dollars a gallon over ``mpg``
miles a gallon.  A lane runs ``miles`` out, loaded, and the same distance home; the shipper going out pays ``head`` a
loaded mile; going home the truck finds a load paying ``back`` a mile with probability ``p_back`` (else it drives home
empty) and, when it waits for one, loses ``wait_days`` days at ``day_cost`` dollars a day.

The market: monthly; demand for truckload freight follows a path (``demand``); trucks ``K`` earn a spot rate that rises
steeply as demand approaches capacity, ``rate = cost x (D / K) ** elasticity``; carriers add trucks in proportion to the
margin ``entry`` months later and leave only when the margin is negative, more slowly.

The railway: a share ``fixed`` of its operating cost is fixed with the miles of route and the rest varies with ton-miles;
calibrated to Union Pacific's 2025 accounts (operating expenses, route miles, revenue ton-miles), so the average cost of
a ton-mile at density ``d`` (ton-miles a route mile a year) is ``F / d + v``.

The route: a driver and van cost ``hour`` dollars an hour for ``hours`` hours; each stop takes ``dwell`` minutes plus the
drive from the last one at ``speed`` miles an hour; each stop takes ``pps`` packages.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class Truck:
    nonfuel: float = 2.05       # $ a mile before fuel
    mpg: float = 6.5
    diesel: float = 3.65        # $ a gallon

    def per_mile(self) -> float:
        return self.nonfuel + self.diesel / self.mpg

    def but(self, **kw) -> "Truck":
        return replace(self, **kw)


@dataclass(frozen=True)
class Lane:
    miles: float = 720.0          # Chicago to Atlanta
    head: float = 2.84            # $ a loaded mile out (J.B. Hunt's truckload revenue a loaded mile, 2025)
    back: float = 1.60            # $ a loaded mile home, when a load is found
    p_back: float = 0.6           # chance of finding a load home
    wait_days: float = 1.0        # days spent waiting for that load
    day_cost: float = 450.0       # $ a day of a truck and driver standing
    truck: Truck = Truck()

    def trip(self, take_back: bool = True) -> dict:
        """Expected money of one round trip: out loaded, home loaded with probability p_back (if sought) or empty."""
        c = self.truck.per_mile()
        out_rev = self.head * self.miles
        cost = 2 * self.miles * c
        if take_back:
            back_rev = self.p_back * self.back * self.miles
            wait = self.wait_days * self.day_cost
            loaded_share = (1 + self.p_back) / 2
        else:
            back_rev, wait, loaded_share = 0.0, 0.0, 0.5
        profit = out_rev + back_rev - cost - wait
        return dict(out_rev=out_rev, back_rev=back_rev, cost=cost, wait=wait, profit=profit, per_mile=c,
                    empty_share=1 - loaded_share)

    def breakeven_head(self, take_back: bool = True) -> float:
        """The rate a loaded mile out at which the round trip just pays."""
        t = self.trip(take_back)
        return (t["cost"] + t["wait"] - t["back_rev"]) / self.miles

    def needed(self, empty_share: float) -> float:
        """The rate a loaded mile that pays the truck when ``empty_share`` of its miles are driven empty."""
        return self.truck.per_mile() / (1 - empty_share)

    def but(self, **kw) -> "Lane":
        return replace(self, **kw)


@dataclass(frozen=True)
class Market:
    months: int = 96
    elasticity: float = 2.0
    entry: int = 6               # months before new trucks are on the road
    grow: float = 0.05           # share of the margin added as trucks a month when rates pay
    shrink: float = 0.03         # share of the (negative) margin removed as trucks a month when they do not
    boom: float = 0.15           # demand above trend in the boom
    boom_start: int = 12
    boom_len: int = 20
    cost: float = 2.40           # $ a mile, the marginal truck's cost
    seed: int = 29

    def demand(self) -> np.ndarray:
        t = np.arange(self.months)
        d = 1.0 + 0.002 * t
        up = (t >= self.boom_start) & (t < self.boom_start + self.boom_len)
        ramp = np.clip((t - self.boom_start) / 4.0, 0, 1)
        d = d * (1 + self.boom * np.where(up, ramp, 0.0))
        rng = np.random.default_rng(self.seed)
        return d * (1 + 0.01 * rng.standard_normal(self.months))

    def path(self) -> dict:
        D = self.demand()
        K = np.empty(self.months)
        rate = np.empty(self.months)
        K[0] = D[0] / 0.97
        orders = np.zeros(self.months + self.entry + 1)
        for t in range(self.months):
            if t > 0:
                K[t] = K[t - 1] + orders[t]
            rate[t] = self.cost * min(D[t] / K[t], 1.25) ** self.elasticity
            m = rate[t] / self.cost - 1
            if m > 0:
                orders[t + self.entry] += self.grow * m * K[t]
            else:
                K[t] = K[t] * (1 + self.shrink * m)
        return dict(demand=D, capacity=K, rate=rate, util=D / K)

    def but(self, **kw) -> "Market":
        return replace(self, **kw)


@dataclass(frozen=True)
class Railway:
    opex: float = 14.66e9        # $ a year: Union Pacific's 2025 operating expenses (revenue x operating ratio)
    route: float = 32889.0       # route miles
    rtm: float = 426.9e9         # revenue ton-miles a year
    rate: float = 23.2e9 / 426.9e9   # freight revenue a ton-mile
    fixed: float = 0.40

    def F(self) -> float:
        """Fixed cost a route mile a year."""
        return self.fixed * self.opex / self.route

    def v(self) -> float:
        """Variable cost a ton-mile."""
        return (1 - self.fixed) * self.opex / self.rtm

    def density(self) -> float:
        return self.rtm / self.route

    def avg_cost(self, d) -> np.ndarray:
        return self.F() / np.asarray(d, dtype=float) + self.v()

    def breakeven_density(self) -> float:
        return self.F() / (self.rate - self.v())

    def but(self, **kw) -> "Railway":
        return replace(self, **kw)


@dataclass(frozen=True)
class Route:
    hour: float = 65.0
    hours: float = 8.0
    dwell: float = 1.5           # minutes a stop
    speed: float = 20.0          # miles an hour between stops
    pps: float = 1.4             # packages a stop

    def stops(self, spacing) -> np.ndarray:
        """Stops a day when stops are ``spacing`` miles apart."""
        s = np.asarray(spacing, dtype=float)
        return self.hours * 60.0 / (self.dwell + 60.0 * s / self.speed)

    def per_package(self, spacing) -> np.ndarray:
        return self.hour * self.hours / (self.stops(spacing) * self.pps)

    def but(self, **kw) -> "Route":
        return replace(self, **kw)


def lanes(n: int) -> dict:
    """Lanes needed to link n cities: every pair directly (both ways), or through one hub."""
    return dict(direct=n * (n - 1), hub=2 * (n - 1))
