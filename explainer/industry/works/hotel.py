"""The Works' hotel (Part 35): an owner's hotel for a year, sold month by month through the brand's channels and the
online agents, and a night at the roulette table.

A hotel has a fixed number of rooms and a night that cannot be stored: a room unsold tonight is gone.  Demand each month
follows a seasonal index and falls with the rate (a constant elasticity); nights within a month scatter around that
level (a lognormal spread), so on busy nights the hotel sells out and turns guests away.  Each room sold costs
housekeeping, laundry and supplies; each room available costs a minimum staff, utilities, property tax, insurance and
upkeep.  A branded hotel pays the brand a royalty and programme fees on room revenue and sells more of its rooms
directly; an independent pays no fees but has less demand and sells more through online agents, who charge a
commission.  The owner pays a reserve for refurbishment and interest on the debt that bought the building.  No manim.

    >>> h = Hotel()
    >>> y = h.year(180.0)
    >>> round(100 * y["occupancy"]), round(y["adr"]), round(y["revpar"])
    (70, 180, 126)
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from statistics import NormalDist

import numpy as np

SEASON = (0.70, 0.76, 0.90, 0.96, 1.04, 1.14, 1.24, 1.22, 1.04, 0.96, 0.76, 0.66)
DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

_Q = np.linspace(0.5 / 41, 1 - 0.5 / 41, 41)


_ZQ = np.array([NormalDist().inv_cdf(q) for q in _Q])


@dataclass(frozen=True)
class Hotel:
    """An owner's hotel.  Shares are of room revenue unless stated."""

    rooms: int = 200
    ref_rate: float = 180.0         # the rate at which an average month's demand is `base` of the rooms
    base: float = 0.75              # demand at the reference rate in an average month, share of rooms
    elasticity: float = 1.5         # per cent fall in rooms wanted for each per cent on the rate
    spread: float = 0.22            # night-to-night scatter of demand within a month (log standard deviation)
    season: tuple = SEASON
    branded: bool = True
    lift: float = 0.15              # how much less demand an independent hotel has at the same rate
    ota: float = 0.25               # share of rooms sold through online agents, branded
    ota_indep: float = 0.50         # the same, independent
    commission: float = 0.17        # the online agents' commission
    direct: float = 0.03            # the cost of a direct booking: cards, booking engine
    royalty: float = 0.055          # the brand's royalty
    programme: float = 0.045        # the brand's loyalty, reservation and marketing fees
    discount: float = 0.0           # members' discount on direct bookings
    shift: float = 4.0              # share of agent bookings moved to direct per unit of members' discount
    members: float = 0.6            # share of direct bookings made by loyalty members
    var_cost: float = 35.0          # cost of each room sold: housekeeping, laundry, supplies
    fixed_cost: float = 45.0        # cost of each room available each night: minimum staff, utilities, tax, insurance
    other: float = 0.08             # breakfast, parking and the rest, share of room revenue
    other_margin: float = 0.3
    invest: float = 180e3           # the owner's cost of the hotel per room
    debt: float = 0.6               # share of it borrowed
    interest: float = 0.065
    reserve: float = 0.04           # refurbishment reserve, share of total revenue

    def with_(self, **kw) -> "Hotel":
        return replace(self, **kw)

    def ota_share(self) -> float:
        o = self.ota if self.branded else self.ota_indep
        return max(0.0, o * (1 - self.shift * self.discount))

    def month(self, m: int, rate: float) -> dict:
        """Month ``m`` (0-11) at a posted ``rate``."""
        lift = 1.0 if self.branded else 1.0 - self.lift
        want = self.rooms * self.base * self.season[m] * lift * (rate / self.ref_rate) ** (-self.elasticity)
        nights = want * np.exp(self.spread * _ZQ - 0.5 * self.spread ** 2)
        sold_night = float(np.minimum(nights, self.rooms).mean())
        turned = float(np.maximum(nights - self.rooms, 0).mean())
        d = DAYS[m]
        sold = sold_night * d
        ota = self.ota_share()
        realized = rate * (1 - (1 - ota) * self.members * self.discount)
        room_rev = sold * realized
        dist = room_rev * (ota * self.commission + (1 - ota) * self.direct)
        fees = room_rev * (self.royalty + self.programme) if self.branded else 0.0
        other_rev = self.other * room_rev
        var = self.var_cost * sold
        fixed = self.fixed_cost * self.rooms * d
        ebitda = room_rev + other_rev * self.other_margin - dist - fees - var - fixed
        return dict(month=MONTHS[m], rate=rate, realized=realized, sold=sold, available=self.rooms * d,
                    occupancy=sold / (self.rooms * d), turned=turned * d, room_rev=room_rev, other_rev=other_rev,
                    dist=dist, fees=fees, var=var, fixed=fixed, ebitda=ebitda)

    def year(self, rates) -> dict:
        """The year at one rate for every month, or twelve monthly rates."""
        rs = [float(rates)] * 12 if np.isscalar(rates) else [float(r) for r in rates]
        ms = [self.month(m, r) for m, r in enumerate(rs)]
        tot = {k: sum(x[k] for x in ms) for k in ("sold", "available", "turned", "room_rev", "other_rev", "dist", "fees",
                                                  "var", "fixed", "ebitda")}
        revenue = tot["room_rev"] + tot["other_rev"]
        reserve = self.reserve * revenue
        cost = self.invest * self.rooms
        interest = self.debt * cost * self.interest
        cash = tot["ebitda"] - reserve - interest
        equity = (1 - self.debt) * cost
        return dict(months=ms, rates=rs, **tot, revenue=revenue, occupancy=tot["sold"] / tot["available"],
                    adr=tot["room_rev"] / tot["sold"], revpar=tot["room_rev"] / tot["available"],
                    margin=tot["ebitda"] / revenue, reserve=reserve, interest=interest, cash=cash, equity=equity,
                    yield_=cash / equity, cost=cost)

    def best_flat(self, grid=None) -> dict:
        grid = np.arange(80, 401, 2.0) if grid is None else grid
        return max((self.year(float(r)) for r in grid), key=lambda y: y["ebitda"])

    def best_monthly(self, grid=None) -> dict:
        """Revenue management: the best rate month by month (months are independent here)."""
        grid = np.arange(80, 401, 2.0) if grid is None else grid
        rates = [max(grid, key=lambda r: self.month(m, float(r))["ebitda"]) for m in range(12)]
        return self.year(rates)


def flow_through(h: Hotel, rate: float, step: float = 0.05) -> dict:
    """How much of an extra 5% of room revenue reaches the hotel's profit when it comes from a higher rate (the same
    rooms sold, demand assumed unchanged) and when it comes from more rooms sold at the same rate."""
    y = h.year(rate)
    extra = step * y["room_rev"]
    ota = h.ota_share()
    pct = ota * h.commission + (1 - ota) * h.direct + ((h.royalty + h.programme) if h.branded else 0.0)
    keep_rate = extra * (1 - pct)
    rooms_more = extra / y["adr"]
    keep_occ = extra * (1 - pct) + extra * h.other * h.other_margin - rooms_more * h.var_cost
    return dict(extra=extra, from_rate=keep_rate / extra, from_rooms=keep_occ / extra, pct=pct)


def roulette(players: int = 2000, buy_in: float = 500.0, bet: float = 25.0, spins: int = 100, seed: int = 0) -> dict:
    """Players each buy ``buy_in`` of chips and bet ``bet`` on red at single-zero roulette (18 of 37 pockets win, paying
    even money) for up to ``spins`` spins or until their chips run out.  Returns each player's result, the casino's win
    and its win as a share of the chips bought (the 'hold' on the drop)."""
    rng = np.random.default_rng(seed)
    p = 18 / 37
    chips = np.full(players, buy_in)
    wagered = np.zeros(players)
    for _ in range(spins):
        live = chips >= bet
        if not live.any():
            break
        win = rng.random(players) < p
        chips = np.where(live, chips + np.where(win, bet, -bet), chips)
        wagered += np.where(live, bet, 0.0)
    result = chips - buy_in
    house = -result.sum()
    return dict(result=result, house=house, drop=buy_in * players, hold=house / (buy_in * players),
                wagered=wagered.sum(), edge=1 / 37, win_share=float((result > 0).mean()),
                expected=wagered.sum() / 37)
