"""The Works' electronics business (Part 16): a device's dollar split between the component makers, the assembler and the
brand; the assembler's accounts, where buying the parts and reselling them makes revenue large and the margin thin; and
the Run it choice, a brand's order that needs a new plant.

All parameters are this series' illustrations, labelled as models on screen.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Device:
    """One device, per unit, in dollars: what the brand sells it for, what its parts cost, the assembler's fee for
    assembly and test, and the brand's own spending (design, software, marketing, distribution)."""
    price: float = 900.0
    bom: float = 450.0            # the bill of materials
    fee: float = 30.0             # assembly, test and logistics: the assembler's value added
    brand_costs: float = 160.0    # R&D, software, marketing, distribution, warranty
    parts_margin: float = 0.25    # what the component makers keep of the bill of materials, on average

    def split(self) -> dict:
        """Where the price goes: component makers' costs and profit, the assembler's fee, the brand's costs and profit."""
        parts_profit = self.bom * self.parts_margin
        brand_profit = self.price - self.bom - self.fee - self.brand_costs
        return {"parts cost": self.bom - parts_profit, "parts profit": parts_profit, "assembler": self.fee,
                "brand costs": self.brand_costs, "brand profit": brand_profit}


@dataclass(frozen=True)
class Assembler:
    """An assembler's year on one device: it buys the parts and sells the finished device to the brand (turnkey), or
    the brand consigns the parts and pays only the fee."""
    labour: float = 9.0           # $ a unit: people on the line
    other: float = 3.0            # $ a unit: power, logistics, scrap
    fixed: float = 60e6           # $ a year: the plant's overhead
    plant: float = 800e6          # $: the plant and its tools
    turnkey: bool = True

    def year(self, units: float, d: Device | None = None) -> dict:
        d = d or Device()
        revenue = units * (d.fee + (d.bom if self.turnkey else 0.0))
        cost = units * (self.labour + self.other + (d.bom if self.turnkey else 0.0)) + self.fixed
        profit = revenue - cost
        return {"revenue": revenue, "profit": profit, "margin": profit / revenue if revenue else 0.0,
                "on_fee": profit / (units * d.fee) if units else 0.0, "return_on_plant": profit / self.plant}


@dataclass(frozen=True)
class Offer:
    """Run it: a brand offers ``units`` devices a year for ``years`` years at ``fee`` a unit, if a new plant is ready in
    a year.  After the term it renews for ``renewal`` more years with probability ``p`` (or moves the work elsewhere)."""
    units: float = 20e6
    years: int = 3
    renewal: int = 3
    fee: float = 30.0
    rate: float = 0.08
    ramp: tuple = (0.5, 1.0, 1.0)


PLANS = {"decline": "Decline: keep the old lines busy with smaller orders",
         "build": "Build the plant the brand asked for",
         "abroad": "Build in a new country: cheaper labour, a slower ramp"}


def _cash(plan: str, o: Offer, a: Assembler) -> list[float]:
    """Cash flows, year 0 (the build) to the end of the renewal, if the order renews."""
    if plan == "decline":
        return [0.0] * (1 + o.years + o.renewal)
    if plan == "abroad":
        a = Assembler(labour=a.labour * 0.5, other=a.other, fixed=a.fixed, plant=a.plant * 1.1, turnkey=a.turnkey)
        ramp = (0.3, 0.7, 1.0)
    else:
        ramp = o.ramp
    flows = [-a.plant]
    for t in range(o.years + o.renewal):
        load = ramp[t] if t < len(ramp) else 1.0
        flows.append(load * o.units * (o.fee - a.labour - a.other) - a.fixed)
    return flows


def npv(flows: list[float], rate: float) -> float:
    return sum(c / (1 + rate) ** t for t, c in enumerate(flows))


def play(plan: str, p: float, o: Offer | None = None, a: Assembler | None = None) -> dict:
    """The plan's value today at the renewal probability ``p``: with and without renewal, and expected."""
    o, a = o or Offer(), a or Assembler()
    flows = _cash(plan, o, a)
    first = flows[:1 + o.years]
    rest = [0.0] * (1 + o.years) + flows[1 + o.years:]
    v_no, v_rest = npv(first, o.rate), npv(rest, o.rate)
    return {"flows": flows, "no_renewal": v_no, "renewal": v_no + v_rest, "expected": v_no + p * v_rest,
            "break_even_p": (-v_no / v_rest) if v_rest > 0 and v_no < 0 else (0.0 if v_no >= 0 else None)}


def run_it(ps=(0.0, 0.25, 0.5, 0.75, 1.0)) -> dict:
    return {(plan, p): play(plan, p) for plan in PLANS for p in ps}
