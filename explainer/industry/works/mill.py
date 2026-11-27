"""The Works' mills (Part 11): an integrated steel mill and a minimill, the glut game, cement kilns with their delivery
areas, a quarry's reach, and the chemistry of the carbon chapter.

Units: million tonnes a year of capacity, dollars a tonne, dollars million a year of fixed cost.  The mills' costs are
this series' assumptions, set near what the companies disclose (Nucor's scrap cost and price, Cleveland-Cliffs' recipe
of ore, coke and scrap per ton); the films label them as models.  No manim here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# molar masses, g/mol
FE, H2, H2O, CACO3, CAO, CO2 = 55.845, 2.016, 18.015, 100.087, 56.077, 44.009


@dataclass
class Mill:
    """A steel mill: ``capacity`` million tonnes a year; ``fixed`` $ million a year whatever it makes (labour,
    maintenance, depreciation, pensions); ``variable`` $ a tonne (metal, coke or power, alloys, consumables), or a
    function of the steel price when its main input moves with it (scrap).  ``min_rate`` is the lowest stable operating
    rate (a blast furnace cannot simply run at a fifth of its capacity); ``idle`` the share of fixed costs still paid
    while banked; ``restart`` $ million to bring it back."""
    name: str
    capacity: float
    fixed: float
    variable: float
    min_rate: float = 0.0
    idle: float = 0.5
    restart: float = 0.0
    scrap_share: float = 0.0   # if > 0, the metal part of variable cost moves with the steel price (minimill)

    def var_cost(self, price: float, base_price: float = 1000.0) -> float:
        """Variable cost a tonne; for a scrap-fed mill, the metal part scales with the steel price (scrap follows
        steel)."""
        if self.scrap_share <= 0:
            return self.variable
        metal = self.variable * self.scrap_share
        return self.variable - metal + metal * price / base_price

    def unit_cost(self, rate: float, price: float = 1000.0) -> float:
        return self.var_cost(price) + self.fixed / (self.capacity * rate)

    def profit(self, price: float, rate: float) -> float:
        """$ million a year at ``price`` and operating ``rate`` (share of capacity)."""
        return (price - self.var_cost(price)) * self.capacity * rate - self.fixed

    def breakeven_rate(self, price: float) -> float:
        m = price - self.var_cost(price)
        return float("inf") if m <= 0 else self.fixed / (m * self.capacity)

    def breakeven_price(self, rate: float = 1.0) -> float:
        lo, hi = 0.0, 5000.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if self.profit(mid, rate) < 0 else (lo, mid)
        return (lo + hi) / 2


INTEGRATED = Mill("integrated mill (blast furnace)", capacity=3.0, fixed=750.0, variable=520.0, min_rate=0.75,
                  idle=0.5, restart=60.0)
MINIMILL = Mill("minimill (electric arc furnace)", capacity=3.0, fixed=300.0, variable=560.0, min_rate=0.3, idle=0.3,
                restart=5.0, scrap_share=0.75)

# the glut: eight quarters of the market price ($ a tonne) and of orders (share of the mill's capacity its customers take)
GLUT_PRICE = [880, 800, 700, 640, 620, 660, 740, 860]
GLUT_ORDERS = [1.0, 0.9, 0.8, 0.65, 0.6, 0.7, 0.85, 1.0]
SPOT_DISCOUNT = 0.15   # tonnes beyond the order book sell this far below the market price


def glut(mill: Mill = INTEGRATED, strategy: str = "price", prices=GLUT_PRICE, orders=GLUT_ORDERS,
         discount: float = SPOT_DISCOUNT) -> dict:
    """Play a glut quarter by quarter.  Strategies:

    ``price``   run full: sell the order book at the market price and push the rest out at ``discount`` below it;
    ``output``  make only what is ordered, but never below the furnace's ``min_rate`` (the excess goes at a discount);
    ``bank``    as ``output``, but bank the furnace in any quarter when orders fall below ``min_rate`` (pay the idle
                share of fixed costs, make nothing, lose those orders) and pay ``restart`` when it comes back.

    Returns per-quarter profit ($ million), rate, extra tonnes pushed onto the market (million t) and the total."""
    q_fixed = mill.fixed / 4
    cap_q = mill.capacity / 4
    out = {"profit": [], "rate": [], "extra": [], "banked": []}
    banked = False
    for p, o in zip(prices, orders):
        vc = mill.var_cost(p)
        if strategy == "price":
            rate = 1.0
        elif strategy in ("output", "bank"):
            rate = max(o, mill.min_rate)
        else:
            raise ValueError(strategy)
        if strategy == "bank" and o < mill.min_rate:
            out["profit"].append(-q_fixed * mill.idle)
            out["rate"].append(0.0)
            out["extra"].append(0.0)
            out["banked"].append(True)
            banked = True
            continue
        restart = mill.restart if banked else 0.0
        banked = False
        sold_full = min(o, rate) * cap_q
        sold_spot = max(rate - o, 0.0) * cap_q
        rev = sold_full * p + sold_spot * p * (1 - discount)
        out["profit"].append(rev - rate * cap_q * vc - q_fixed - restart)
        out["rate"].append(rate)
        out["extra"].append(sold_spot)
        out["banked"].append(False)
    out["total"] = float(sum(out["profit"]))
    return out


def industry_glut(n_mills: int = 10, share_pushing: float = 1.0, elasticity: float = -3.0, prices=GLUT_PRICE,
                  orders=GLUT_ORDERS) -> list[float]:
    """What the market price becomes if ``share_pushing`` of ``n`` identical mills run full instead of matching orders:
    the extra tonnes (relative to the order book) depress the price by 1/|elasticity| per cent for each per cent of
    extra supply.  Returns the new price path."""
    out = []
    for p, o in zip(prices, orders):
        extra = share_pushing * (1.0 - o) / o      # extra supply as a share of what is demanded
        out.append(p * max(0.3, 1 + extra / elasticity))
    return out


# --------------------------------------------------------------------------------------------------- cement kilns
@dataclass
class Kiln:
    """A cement plant at ``x`` (km along a line, or (x, y)) with a cash cost ``cost`` $ a tonne at its gate."""
    name: str
    x: float | tuple
    cost: float


def delivered(kiln: Kiln, at, haul: float) -> float:
    """The cheapest price at which ``kiln`` can deliver a tonne at ``at`` (km), with trucking at ``haul`` $ a
    tonne-km."""
    d = np.linalg.norm(np.atleast_1d(np.asarray(at, float)) - np.atleast_1d(np.asarray(kiln.x, float)))
    return kiln.cost + haul * d


def market(kilns: list[Kiln], points, haul: float) -> list[dict]:
    """For each point: who serves it (cheapest delivered cost) and the price competition allows there (the
    second-cheapest delivered cost, as when rivals bid; Bertrand with transport costs)."""
    res = []
    for pt in points:
        c = sorted((delivered(k, pt, haul), k.name) for k in kilns)
        res.append({"at": pt, "winner": c[0][1], "cost": c[0][0], "price": c[1][0] if len(c) > 1 else np.inf,
                    "margin": (c[1][0] - c[0][0]) if len(c) > 1 else np.inf})
    return res


def radius(price: float, cost: float, haul: float) -> float:
    """How far a plant can ship before its delivered cost reaches ``price`` (km, or miles if ``haul`` is per
    ton-mile)."""
    return max(price - cost, 0.0) / haul


def doubling_distance(price: float, haul: float) -> float:
    """Distance at which trucking has doubled the price of a load (aggregates: price at the quarry ``price``)."""
    return price / haul


# --------------------------------------------------------------------------------------------------- chemistry
def calcination_co2(cao_in_clinker: float = 0.65) -> float:
    """Tonnes of CO2 released from limestone per tonne of clinker (CaCO3 -> CaO + CO2), before any fuel is burned."""
    return cao_in_clinker * CO2 / CAO


def hydrogen_per_tonne_iron() -> float:
    """Tonnes of hydrogen to reduce haematite to a tonne of iron: Fe2O3 + 3 H2 -> 2 Fe + 3 H2O."""
    return 1.5 * H2 / FE


def carbon_per_tonne_iron() -> float:
    """Tonnes of CO2 if the oxygen is taken by carbon instead: Fe2O3 + 3 CO -> 2 Fe + 3 CO2 (the chemistry alone)."""
    return 1.5 * CO2 / FE


def hydrogen_cost(price_per_kg: float, kwh_per_kg: float = 52.0, power_price: float | None = None) -> dict:
    """Hydrogen for one tonne of iron: kilograms, electricity (MWh, if made by electrolysis at ``kwh_per_kg``) and
    its cost at ``price_per_kg``."""
    kg = hydrogen_per_tonne_iron() * 1000
    out = {"kg": kg, "mwh": kg * kwh_per_kg / 1000, "cost": kg * price_per_kg}
    if power_price is not None:
        out["power_cost"] = out["mwh"] * power_price
    return out


def smelter_power(tonnes_per_year: float, kwh_per_tonne: float) -> dict:
    """A smelter's electricity: TWh a year and the continuous load in MW."""
    twh = tonnes_per_year * kwh_per_tonne / 1e9
    return {"twh": twh, "mw": twh * 1e6 / 8760}
