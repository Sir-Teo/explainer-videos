"""The Works' aerospace business (Part 18): an airliner programme that spends billions before its first delivery and
earns them back over hundreds of aircraft as its learning curve brings the cost of each one down; an engine sold
below its cost and paid for over twenty-five years of service; and the Run it choice, a new airliner or a re-engined
old one, with a rival making the same choice.

All parameters are this series' illustrations, labelled as models on screen; the films set them beside the filings
(Boeing's program accounting quantities and losses, Airbus's deliveries and margins, GE Aerospace's service revenue).
No manim here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Programme:
    """An airliner programme, in dollars: development spent evenly over ``dev_years``, then deliveries ramping to
    ``rate`` a year, each sold at ``price``; the n-th aircraft costs ``first_cost * n ** log2(learning)`` (Wright's
    curve: each doubling of the count built cuts the cost of the next one to ``learning`` of what it was)."""
    dev: float = 20e9
    dev_years: int = 6
    price: float = 110e6
    first_cost: float = 450e6
    learning: float = 0.82
    rate: float = 120.0
    ramp: tuple = (0.15, 0.4, 0.7, 1.0)
    years: int = 25
    discount: float = 0.08

    def unit_cost(self, n: float) -> float:
        return self.first_cost * n ** math.log2(self.learning)

    def deliveries(self) -> list[float]:
        return [self.rate * (self.ramp[t] if t < len(self.ramp) else 1.0) for t in range(self.years)]

    def flows(self) -> list[dict]:
        """Year by year: deliveries, revenue, cost of the aircraft built, cash, cumulative cash."""
        out, built, cum = [], 0.0, 0.0
        for t in range(self.dev_years):
            cum -= self.dev / self.dev_years
            out.append({"year": t, "units": 0.0, "revenue": 0.0, "cost": self.dev / self.dev_years,
                        "cash": -self.dev / self.dev_years, "cum": cum, "built": 0.0})
        for k, d in enumerate(self.deliveries()):
            n = int(round(d))
            cost = sum(self.unit_cost(built + i + 1) for i in range(n))
            built += n
            cash = n * self.price - cost
            cum += cash
            out.append({"year": self.dev_years + k, "units": n, "revenue": n * self.price, "cost": cost, "cash": cash,
                        "cum": cum, "built": built})
        return out

    def npv(self) -> float:
        return sum(f["cash"] / (1 + self.discount) ** f["year"] for f in self.flows())

    def break_even(self) -> dict:
        """The aircraft delivered, and the years, before cumulative cash turns positive (undiscounted); None if never."""
        for f in self.flows():
            if f["built"] and f["cum"] >= 0:
                return {"units": f["built"], "year": f["year"]}
        return {"units": None, "year": None}

    def trough(self) -> float:
        return min(f["cum"] for f in self.flows())

    def unit_crosses_price(self) -> float:
        """The aircraft number after which each one costs less to build than it sells for."""
        return (self.first_cost / self.price) ** (1 / -math.log2(self.learning))


@dataclass(frozen=True)
class Engine:
    """A jet engine sold to the airframer or airline below its cost, then serviced for ``life`` years: spare parts and
    shop visits billed per flight hour, at a margin."""
    price: float = 12e6
    cost: float = 15e6
    hours: float = 3000.0          # flight hours a year
    per_hour: float = 350.0        # service revenue per flight hour, $
    service_margin: float = 0.35
    life: int = 25
    discount: float = 0.08

    def lifetime(self) -> dict:
        sale = self.price - self.cost
        yearly = self.hours * self.per_hour * self.service_margin
        pv = sum(yearly / (1 + self.discount) ** t for t in range(1, self.life + 1))
        revenue = self.price + self.hours * self.per_hour * self.life
        return {"sale": sale, "service_yearly": yearly, "service_pv": pv, "value": sale + pv,
                "service_share": self.hours * self.per_hour * self.life / revenue,
                "payback_years": next((t for t in range(1, self.life + 1)
                                       if sale + sum(yearly / (1 + self.discount) ** s for s in range(1, t + 1)) >= 0), None)}


def launch_aid(p: Programme, share: float = 1 / 3, levy: float = 8e6) -> dict:
    """Launch aid: governments lend ``share`` of the development cost, interest free, repaid by a ``levy`` on each
    aircraft delivered until the loan is paid off; if too few are sold, the rest is never repaid.  Returns the maker's
    cumulative cash by year, its trough and value today, and how much of the loan was repaid within the programme."""
    loan = share * p.dev
    owed, cum, out, npv = loan, 0.0, {}, 0.0
    for f in p.flows():
        cash = f["cash"]
        if f["units"] == 0:
            cash += loan / p.dev_years
        else:
            pay = min(owed, levy * f["units"])
            owed -= pay
            cash -= pay
        cum += cash
        npv += cash / (1 + p.discount) ** f["year"]
        out[f["year"]] = cum
    return {"cum": out, "trough": min(out.values()), "npv": npv, "repaid": loan - owed, "loan": loan}


# --------------------------------------------------------------------------------------------- Run it: new or re-engine
OPTIONS = {"new": {"dev": 20e9, "years": 7, "gain": 0.20, "label": "a new airliner"},
           "reengine": {"dev": 3e9, "years": 4, "gain": 0.14, "label": "the old airliner with new engines"}}


@dataclass(frozen=True)
class Duel:
    """Run it: two airframers share a segment of ``market`` aircraft a year for ``horizon`` years, each earning
    ``margin`` a plane.  Each chooses a new airliner or a re-engined one (``OPTIONS``: development cost, years to
    first delivery, fuel saving).  Until a product arrives a maker sells its old one; buyers split each year's market by
    fuel burn, share_i = (1 / burn_i) ** k / sum over makers, so a few per cent of fuel moves a lot of orders."""
    market: float = 1000.0
    margin: float = 12e6
    horizon: int = 25
    k: float = 12.0
    discount: float = 0.08
    options: dict = None

    @property
    def opts(self) -> dict:
        return self.options or OPTIONS

    def _burn(self, choice: str, t: int) -> float:
        o = self.opts[choice]
        return 1.0 - o["gain"] if t >= o["years"] else 1.0

    def payoff(self, me: str, them: str) -> float:
        """My programme's value today, $: margins on my share each year less my development, spent before entry."""
        o = self.opts[me]
        v = -sum(o["dev"] / o["years"] / (1 + self.discount) ** t for t in range(o["years"]))
        for t in range(self.horizon):
            a, b = (1 / self._burn(me, t)) ** self.k, (1 / self._burn(them, t)) ** self.k
            v += self.market * a / (a + b) * self.margin / (1 + self.discount) ** t
        return v

    def table(self) -> dict:
        acts = tuple(self.opts)
        return {(a, b): (self.payoff(a, b), self.payoff(b, a)) for a in acts for b in acts}

    def equilibria(self) -> list:
        t, acts = self.table(), tuple(self.opts)
        return [(a, b) for a in acts for b in acts
                if all(t[(a, b)][0] >= t[(x, b)][0] for x in acts) and all(t[(a, b)][1] >= t[(a, y)][1] for y in acts)]


def variant(new_gain: float = 0.23, re_gain: float = 0.13) -> dict:
    """The options with different fuel savings: a bigger leap for the new airliner, a smaller one for the re-engine."""
    return {"new": {**OPTIONS["new"], "gain": new_gain}, "reengine": {**OPTIONS["reengine"], "gain": re_gain}}


def run_it(d: Duel | None = None) -> dict:
    d = d or Duel()
    alt = Duel(options=variant())
    return {"table": d.table(), "equilibria": d.equilibria(), "alt_table": alt.table(), "alt_equilibria": alt.equilibria()}
