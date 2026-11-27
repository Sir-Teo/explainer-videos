"""The Works' car business (Part 17): an assembly plant whose shifts are paid whether the line is full or not, a platform
whose engineering is paid once and spread over every car built on it, a battery priced by the kilowatt-hour, a loan
priced by the finance arm, and the Run it choice: launch a model, set the price, then decide shifts and incentives as
the orders come in.

All parameters are this series' illustrations, labelled as models on screen; the films set them beside the measured
figures (the Census Bureau's cost of materials, the carmakers' filings, the Federal Reserve's capacity utilization).
No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plant:
    """An assembly plant building one model, per year.  ``price`` is what the carmaker receives per car (before any
    incentive); ``variable`` is what each car costs to build beyond the people on the line: parts and materials,
    freight, warranty.  Each shift is a crew that is paid for the year whether the line runs full or not (the
    contract's job protections make it a fixed cost until the shift is cut); ``fixed`` is the plant's tooling,
    the model's engineering written off over its life, and overhead."""
    price: float = 45_000.0
    variable: float = 36_000.0
    shift_capacity: float = 125_000.0   # cars a year one shift can build at line rate
    shift_cost: float = 288e6           # $ a year: 2,000 people x 1,800 hours x $80 an hour, wages and benefits
    fixed: float = 900e6                # $ a year

    @property
    def margin(self) -> float:
        """Contribution per car: price less variable cost (before the shift and fixed costs)."""
        return self.price - self.variable

    def capacity(self, shifts: int) -> float:
        return shifts * self.shift_capacity

    def year(self, demand: float, shifts: int = 2, incentive: float = 0.0) -> dict:
        """One year: sales are demand up to the shifts' capacity; profit is contribution less shifts and fixed cost."""
        cars = min(demand, self.capacity(shifts))
        revenue = cars * (self.price - incentive)
        profit = cars * (self.margin - incentive) - shifts * self.shift_cost - self.fixed
        return {"cars": cars, "revenue": revenue, "profit": profit,
                "margin": profit / revenue if revenue else 0.0,
                "utilization": cars / self.capacity(shifts) if shifts else 0.0}

    def break_even(self, shifts: int = 2, incentive: float = 0.0) -> float:
        """Cars a year at which the plant covers its shifts and fixed cost."""
        return (shifts * self.shift_cost + self.fixed) / (self.margin - incentive)

    def hours_per_car(self, shifts: int = 2, people: float = 2000, hours: float = 1800) -> float:
        """Labour hours per car at line rate (the plant's crews over its capacity)."""
        return shifts * people * hours / self.capacity(shifts)


@dataclass(frozen=True)
class Platform:
    """The engineering under a family of models (a body structure, a floor, the electrical architecture), paid once
    and spread over every car built on it for ``years``."""
    engineering: float = 6e9
    years: int = 6

    def per_car(self, cars_a_year: float) -> float:
        return self.engineering / (cars_a_year * self.years)


# --------------------------------------------------------------------------------------------- the launch's three worlds
STATES = (("weak", 0.7, 0.3), ("as planned", 1.0, 0.4), ("strong", 1.3, 0.3))   # demand against plan; probability


def shifts_for(demand: float, plant: Plant | None = None, overtime: float = 1.25) -> dict:
    """The number of shifts (one, two, or a third crew paid an overtime premium) that makes the most of a year's demand,
    with the profit of each."""
    plant = plant or Plant()
    out = {}
    for s in (1, 2, 3):
        p = Plant(plant.price, plant.variable, plant.shift_capacity,
                  plant.shift_cost * (overtime if s == 3 else 1.0), plant.fixed)
        out[s] = p.year(demand, s)
    best = max(out, key=lambda s: out[s]["profit"])
    return {"by_shifts": out, "best": best, "profit": out[best]["profit"]}


def launch(plan: float = 220_000.0, plant: Plant | None = None) -> dict:
    """A model launched for ``plan`` cars a year at the plant's price: profit in each world, locked into the two
    shifts the plan needs or responding with the shifts the orders call for, and the expected values."""
    plant = plant or Plant()
    rows = {}
    for name, s, w in STATES:
        d = plan * s
        r = shifts_for(d, plant)
        rows[name] = {"demand": d, "weight": w, "locked": plant.year(d, 2)["profit"], "respond": r["profit"],
                      "shifts": r["best"]}
    return {"by_state": rows, "locked": sum(v["weight"] * v["locked"] for v in rows.values()),
            "respond": sum(v["weight"] * v["respond"] for v in rows.values())}


# ------------------------------------------------------------------------------------------ Run it: the showroom duel
@dataclass(frozen=True)
class Duel:
    """Run it: orders for your new model come in 30% below plan, and a rival's model, built in a plant just like
    yours, sits in the same showrooms with the same problem.  Each of you either holds the list price or pays a
    discount.  A car's demand is ``base * state * (own price / list) ** -own * (rival's price / list) ** cross``:
    buyers compare the two closely, so a discount mostly takes buyers from the rival (``own`` > ``cross``), and
    when both discount the market grows only a little (elasticity ``own - cross``)."""
    list_price: float = 45_000.0
    base: float = 220_000.0
    state: float = 0.7
    own: float = 7.0
    cross: float = 6.0
    discount: float = 3_000.0

    def demand(self, mine: float, theirs: float) -> float:
        return (self.base * self.state * (mine / self.list_price) ** -self.own
                * (theirs / self.list_price) ** self.cross)

    def payoff(self, me: str, them: str, plant: Plant | None = None, shifts: int = 2) -> dict:
        plant = plant or Plant(price=self.list_price)
        p = {a: self.list_price - (self.discount if a == "discount" else 0.0) for a in (me, them)}
        mine = plant.year(self.demand(p[me], p[them]), shifts, self.list_price - p[me])
        return mine

    def table(self, plant: Plant | None = None) -> dict:
        acts = ("hold", "discount")
        return {(a, b): (self.payoff(a, b, plant)["profit"], self.payoff(b, a, plant)["profit"]) for a in acts
                for b in acts}

    def equilibria(self, plant: Plant | None = None) -> list:
        t, acts = self.table(plant), ("hold", "discount")
        out = []
        for a in acts:
            for b in acts:
                if (all(t[(a, b)][0] >= t[(x, b)][0] for x in acts)
                        and all(t[(a, b)][1] >= t[(a, y)][1] for y in acts)):
                    out.append((a, b))
        return out


def run_it(d: Duel | None = None) -> dict:
    d = d or Duel()
    plant = Plant(price=d.list_price)
    both_cut = plant.year(d.demand(d.list_price, d.list_price), 1)["profit"]
    return {"table": d.table(), "equilibria": d.equilibria(), "both_cut": both_cut}


# ------------------------------------------------------------------------------------------- the battery and the loan
def battery(kwh: float, per_kwh: float) -> float:
    """A battery pack's cost: its usable energy times the cost per kWh."""
    return kwh * per_kwh


def parity_per_kwh(kwh: float, engine_and_gearbox: float) -> float:
    """The pack cost per kWh at which the battery costs what the engine, gearbox and exhaust it replaces do."""
    return engine_and_gearbox / kwh


def payment(principal: float, rate: float, months: int) -> float:
    """The monthly payment on an amortizing loan at annual ``rate``."""
    r = rate / 12
    return principal / months if r == 0 else principal * r / (1 - (1 + r) ** -months)


def lease(price: float, residual: float, rate: float, months: int) -> float:
    """A lease's monthly payment: the car's expected loss of value over the term, plus interest on the money tied up
    (the standard 'money factor' form: rate / 24 on price plus residual)."""
    return (price - residual) / months + (price + residual) * rate / 24
