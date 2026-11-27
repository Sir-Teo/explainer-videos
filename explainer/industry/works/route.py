"""The Works' waste business (Part 14): a collection route whose cost per stop falls with density, why a second hauler
on the same street loses money, and a landfill whose airspace is an inventory, valued against the years it takes to
permit the next one.

All parameters are this series' illustrations, labelled as models on screen.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Route:
    """A rear-loader's day: fixed truck and crew cost, driving between stops and to the tip, and a few seconds at each
    stop.  Density is the number of customer stops per mile of street driven."""
    truck_day: float = 1100.0      # $ a day: truck, fuel at idle, crew
    seconds_per_stop: float = 25.0
    mph: float = 12.0              # between stops
    tip_hours: float = 2.0         # driving to the tip and back, unloading
    shift_hours: float = 10.0
    homes_per_mile: float = 80.0   # homes on the street
    stops_per_ton: float = 25.0    # a ton of household waste from 25 homes' bins

    def stops_per_day(self, share: float = 1.0) -> float:
        """Stops a truck makes in a shift when it serves ``share`` of the homes on the street."""
        per_mile = self.homes_per_mile * share
        hours_per_stop = self.seconds_per_stop / 3600 + 1 / (per_mile * self.mph)
        return (self.shift_hours - self.tip_hours) / hours_per_stop

    def cost_per_stop(self, share: float = 1.0) -> float:
        return self.truck_day / self.stops_per_day(share)


def split_street(route: Route, price: float, shares=(1.0, 0.5)) -> dict:
    """Profit a day for one hauler with all the street, and for each of two haulers with half."""
    out = {}
    for s in shares:
        n = route.stops_per_day(s)
        out[s] = dict(stops=n, cost=route.cost_per_stop(s), profit=(price - route.cost_per_stop(s)) * n)
    return out


@dataclass(frozen=True)
class Landfill:
    airspace: float = 30.0         # million tons it can still take
    tons_per_year: float = 1.5     # million tons a year
    tip_fee: float = 55.0          # $ a ton
    cost_per_ton: float = 25.0     # $ a ton to operate, cover, monitor
    closure: float = 60.0          # $ million at the end, capping and decades of monitoring (discounted lump)

    def life(self) -> float:
        return self.airspace / self.tons_per_year

    def value(self, rate: float = 0.07, fee_growth: float = 0.02) -> float:
        """$ million: the discounted margin on the remaining airspace, less closure, with the tip fee rising."""
        years = int(np.floor(self.life()))
        v = 0.0
        for t in range(1, years + 1):
            fee = self.tip_fee * (1 + fee_growth) ** t
            v += (fee - self.cost_per_ton) * self.tons_per_year / (1 + rate) ** t
        return v - self.closure / (1 + rate) ** years


def airspace_price(fee_now: float, permit_years: int, scarce_fee: float, rate: float = 0.07, years: int = 30) -> list[float]:
    """Run it: a region with one landfill; a rival needs ``permit_years`` to permit.  Until then the incumbent can charge
    ``scarce_fee``; afterwards competition brings the fee back to ``fee_now``.  Returns the incumbent's fee path."""
    return [scarce_fee if t < permit_years else fee_now for t in range(years)]


@dataclass(frozen=True)
class ValleyLandfill:
    """Run it (Part 14): the only landfill in a valley.  Its own region makes ``region`` million tons a year; a
    neighbouring region sends ``neighbours`` more if the gate fee is no higher than ``rival_fee`` (their own landfill
    plus the haul).  The valley's waste goes elsewhere above ``ceiling`` (the next landfill's fee plus the haul).  A
    rival applies for a permit; once it opens, both charge ``rival_fee`` and split the volume."""
    airspace: float = 30.0         # million tons
    cost: float = 25.0             # $ a ton: operating, cover, leachate, gas, set-aside for closure
    region: float = 1.5
    neighbours: float = 1.0
    rival_fee: float = 45.0
    ceiling: float = 65.0
    rate: float = 0.07
    expansion: float = 15.0        # million tons an expansion permit adds
    expansion_cost: float = 15.0   # $ million spent on the application now
    expansion_year: int = 8        # the year it is granted

    def play(self, plan: str, rival_year: int, years: int = 60) -> dict:
        """``plan`` is "fill" (charge the rivals' fee from the start), "ceiling" (charge what the valley will bear
        until the rival opens) or "expand" (the ceiling, and apply now to expand).  Returns the year-by-year fees,
        tons, cash and what is left, and the present value in $ million."""
        left, pv, rows = self.airspace, 0.0, []
        if plan == "expand":
            pv -= self.expansion_cost
        for t in range(1, years + 1):
            if plan == "expand" and t == self.expansion_year:
                left += self.expansion
            if left <= 1e-9:
                rows.append(dict(year=t, fee=0.0, tons=0.0, cash=0.0, left=0.0))
                continue
            rival = t > rival_year
            if rival:
                fee, tons = self.rival_fee, (self.region + self.neighbours) / 2
            elif plan == "fill":
                fee, tons = self.rival_fee, self.region + self.neighbours
            else:
                fee, tons = self.ceiling, self.region
            tons = min(tons, left)
            left -= tons
            cash = (fee - self.cost) * tons
            pv += cash / (1 + self.rate) ** t
            rows.append(dict(year=t, fee=fee, tons=tons, cash=cash, left=left))
        full = next((r["year"] for r in rows if r["left"] <= 1e-9), None)
        return dict(plan=plan, rival_year=rival_year, pv=pv, rows=rows, full=full,
                    per_ton=pv / (self.airspace + (self.expansion if plan == "expand" else 0)))


def run_it(landfill: ValleyLandfill | None = None, rival_years=(15, 5)) -> dict:
    lf = landfill or ValleyLandfill()
    return {(p, y): lf.play(p, y) for p in ("fill", "ceiling", "expand") for y in rival_years}
