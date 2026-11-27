"""The Works' machinery business (Part 19): a maker whose new-machine sales follow the capital-goods cycle while its
installed base throws off steady parts and service revenue; and the Run it tender, in which two makers bid for a fleet
whose servicing is worth more than the machines.

All parameters are this series' illustrations, labelled as models on screen; the films set them beside the filings
(Otis's New Equipment and Service segments, Caterpillar's backlog and dealers, the Census Bureau's machinery orders).
No manim here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# --------------------------------------------------------------------------------------------- Run it: the tender
@dataclass(frozen=True)
class Tender:
    """Two makers bid for a customer's fleet of ``fleet`` machines that cost ``cost`` each ($m) to build.  Each bids
    ``hold`` or ``cut``; the lower bid wins the whole fleet and a tie splits it.  The winner then services the machines
    it sold: ``service`` ($m, value today) per machine, earned on the share ``attach`` of machines whose owners keep
    buying parts and service from the maker rather than from an independent shop."""
    fleet: int = 100
    cost: float = 1.0
    hold: float = 1.3
    cut: float = 0.9
    service: float = 0.6
    attach: float = 1.0

    def margin(self, price: float) -> float:
        return price - self.cost + self.service * self.attach

    def payoff(self, me: str, them: str) -> float:
        p = {"hold": self.hold, "cut": self.cut}
        if p[me] < p[them]:
            share = 1.0
        elif p[me] > p[them]:
            share = 0.0
        else:
            share = 0.5
        return share * self.fleet * self.margin(p[me])

    def table(self) -> dict:
        return {(a, b): (self.payoff(a, b), self.payoff(b, a)) for a in ("hold", "cut") for b in ("hold", "cut")}

    def equilibria(self) -> list:
        t, acts = self.table(), ("hold", "cut")
        return [(a, b) for a in acts for b in acts
                if all(t[(a, b)][0] >= t[(x, b)][0] for x in acts) and all(t[(a, b)][1] >= t[(a, y)][1] for y in acts)]

    def floor_price(self) -> float:
        """The price at which a machine plus its expected servicing just breaks even: where undercutting stops."""
        return self.cost - self.service * self.attach


def attach_threshold(t: Tender | None = None) -> float:
    """The attach rate above which cutting the price is the better reply to a rival who holds (both makers cut)."""
    t = t or Tender()
    # cut/hold beats hold/hold when fleet*(cut - cost + s*a) > fleet/2*(hold - cost + s*a)
    return max(0.0, ((t.hold - t.cost) / 2 - (t.cut - t.cost)) / (t.service / 2))


# --------------------------------------------------------------------------------------------- the installed base
@dataclass(frozen=True)
class Maker:
    """A machinery maker: new machines sold each year follow ``demand`` (a list of units); each machine sells for
    ``price`` at a ``new_margin`` and works for ``life`` years, earning ``service_rate`` of its price a year in parts and
    service at a ``service_margin``."""
    price: float = 1.0
    new_margin: float = 0.05
    life: int = 15
    service_rate: float = 0.12
    service_margin: float = 0.25

    def run(self, demand: list) -> list[dict]:
        out = []
        for t, units in enumerate(demand):
            base = sum(demand[max(0, t - self.life + 1): t + 1])
            new_rev = units * self.price
            svc_rev = base * self.price * self.service_rate
            out.append({"year": t, "units": units, "base": base, "new_rev": new_rev, "svc_rev": svc_rev,
                        "new_profit": new_rev * self.new_margin, "svc_profit": svc_rev * self.service_margin})
        return out


def cycle_demand(years: int = 40, mean: float = 100.0, swing: float = 0.45, period: float = 8.0, growth: float = 0.02,
                 crash: tuple = (18, 0.5)) -> list[float]:
    """New-machine demand on a capital-goods cycle: a trend, a sine wave of ``period`` years and ``swing`` amplitude, and a
    crash year in which orders halve (``crash`` = (year, factor))."""
    out = []
    for t in range(years):
        d = mean * (1 + growth) ** t * (1 + swing * math.sin(2 * math.pi * t / period))
        if t == crash[0]:
            d *= crash[1]
        out.append(max(d, 0.0))
    return out


def swings(rows: list[dict], key: str, start: int = 15) -> dict:
    """Peak-to-trough fall and coefficient of variation of a series after the base has filled (``start``)."""
    xs = [r[key] for r in rows[start:]]
    mean = sum(xs) / len(xs)
    sd = (sum((x - mean) ** 2 for x in xs) / len(xs)) ** 0.5
    worst = min((b - a) / a for a, b in zip(xs, xs[1:]) if a > 0)
    return {"cv": sd / mean, "worst_fall": worst}
