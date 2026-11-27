"""The Works' chip business (Part 15): dies on a wafer, the yield a defect density allows, a fab whose income statement
is its utilization, and the Run it choice between building a fab and booking a foundry.

All parameters are this series' illustrations, labelled as models on screen.  No manim here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def dies_per_wafer(die_mm2: float, wafer_mm: float = 300.0) -> float:
    """Gross dies on a round wafer: the wafer's area over the die's, less the partial dies lost around the edge."""
    r = wafer_mm / 2
    return math.pi * r * r / die_mm2 - math.pi * wafer_mm / math.sqrt(2 * die_mm2)


def yield_poisson(die_mm2: float, defects_cm2: float) -> float:
    """The share of dies with no killer defect, if defects fall at random: exp(-area x density)."""
    return math.exp(-die_mm2 / 100 * defects_cm2)


def good_dies(die_mm2: float, defects_cm2: float, wafer_mm: float = 300.0) -> float:
    return dies_per_wafer(die_mm2, wafer_mm) * yield_poisson(die_mm2, defects_cm2)


def learning(d0: float, d_floor: float, wafers: float, half: float) -> float:
    """Defect density after ``wafers`` have been made on a process: it falls from ``d0`` towards ``d_floor``, halving
    the gap every ``half`` wafers."""
    return d_floor + (d0 - d_floor) * 0.5 ** (wafers / half)


@dataclass(frozen=True)
class Fab:
    """A leading-edge fab: what it costs to build, the tools' life, its fixed running costs, its capacity, and what
    each wafer costs in materials, power and chemicals."""
    capex: float = 20.0            # $ billion
    life: float = 5.0              # years over which the tools are written off
    fixed: float = 1.0             # $ billion a year: people, maintenance, overhead
    capacity: float = 50_000       # wafers a month
    variable: float = 2_500.0      # $ a wafer

    def year_cost(self, wafers_a_month: float) -> float:
        """$ billion a year to own and run the fab at a loading of ``wafers_a_month``."""
        return self.capex / self.life + self.fixed + self.variable * wafers_a_month * 12 / 1e9

    def cost_per_wafer(self, wafers_a_month: float) -> float:
        return self.year_cost(wafers_a_month) * 1e9 / (wafers_a_month * 12)


@dataclass(frozen=True)
class Chip:
    die_mm2: float = 100.0
    price: float = 60.0            # $ a good die sold


def plan(volume: float, own: bool, fab: Fab | None = None, chip: Chip | None = None, foundry_price: float = 17_000.0,
         d_new: float = 0.5, d_mature: float = 0.1, years: int = 5) -> dict:
    """Run it: a designer who needs ``volume`` wafers a month for ``years`` years either builds its own fab (``own``),
    starting on the learning curve at ``d_new`` defects a cm2, or books a foundry at ``foundry_price`` a wafer with the
    foundry's mature ``d_mature``.  Returns the cost per good die, the yearly profit and the fab's utilization."""
    fab = fab or Fab()
    chip = chip or Chip()
    wafers = volume * 12 * years
    if own:
        # the learning curve, averaged over the wafers made
        steps = 60
        ds = [learning(d_new, d_mature, wafers * (k + 0.5) / steps, half=150_000) for k in range(steps)]
        good = sum(good_dies(chip.die_mm2, d) for d in ds) / steps
        cost_wafer = fab.cost_per_wafer(volume) if volume <= fab.capacity else float("nan")
        util = volume / fab.capacity
    else:
        good = good_dies(chip.die_mm2, d_mature)
        cost_wafer = foundry_price
        util = None
    cost_die = cost_wafer / good
    profit = (chip.price - cost_die) * good * volume * 12 / 1e9
    return dict(volume=volume, own=own, good=good, cost_wafer=cost_wafer, cost_die=cost_die, profit=profit, util=util)


def run_it(volumes=(5_000, 20_000, 50_000), **kw) -> dict:
    return {(v, own): plan(v, own, **kw) for v in volumes for own in (False, True)}
