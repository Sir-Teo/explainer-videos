"""The Works' shipping market (Part 27): a fleet on a freight-rate cycle in which ships ordered today arrive years later,
an owner choosing when to order, and a ship's daily cost at different speeds.

The market.  Demand for ships (in ship-equivalents) grows ``growth`` a year with a random shock; the fleet grows by the
ships ordered ``lag`` years before and shrinks by scrapping.  Utilization is demand over fleet, and a ship's daily
earnings rise very steeply as utilization nears one: when every ship is busy, a cargo owner will pay almost anything for
the last one, and when ships are idle, earnings fall to what keeps the engines turning.  The industry orders in
proportion to today's profit (everyone sees the same rates and orders at once), and scraps more when earnings are low.

The owner.  Two rules for when to order a ship, at most one every ``gap`` years: follow the market (order when earnings
are high) or go against it (order when they are low).  A ship costs a newbuilding price that rises with today's
earnings, arrives ``lag`` years later, and earns the market rate less its running cost for the rest of the run; what is
left of its life at the end is valued at that year's price.

The ship's day.  Fuel burned a day rises with the cube of speed, so fuel a mile rises with the square: slowing down
saves fuel but needs more ships to carry the same cargo.

Every number is this series' illustration; the anchors are ZIM's average freight rate per TEU (about $1,000 in 2019,
$3,240 in 2022, $1,203 in 2023), Frontline's VLCC earnings ($148,500 a day in the third quarter of 2026 against a cash
breakeven of about $24,100), and the container orderbook of 11.3m TEU against a fleet of 33.3m (Alphaliner via ZIM).
After Greenwood and Hanson (2015), 'Waves in Ship Prices and Investment'.  No manim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Market:
    years: int = 30
    burn: int = 12              # years simulated before the owner starts, so the fleet is not at its starting point
    growth: float = 0.03
    shock: float = 0.045
    lag: int = 3                # years from order to delivery
    floor: float = 10.0         # $ thousand a day earned by an idle-ish ship
    top: float = 100.0          # $ thousand a day when every ship is busy
    knee: float = 0.80          # utilization below which earnings sit at the floor
    breakeven: float = 25.0     # $ thousand a day: running cost plus the cost of the capital in the ship
    opex: float = 9.0           # $ thousand a day of running cost
    herd: float = 0.22          # industry orders, as a share of the fleet, at the top rate
    seed: int = 1

    def earnings(self, u: float) -> float:
        x = max(0.0, (min(u, 1.0) - self.knee) / (1 - self.knee))
        return self.floor + (self.top - self.floor) * x ** 3

    def price(self, e: float) -> float:
        """A new ship's price, $ million, rising with today's earnings."""
        return 40.0 + 40.0 * np.sqrt(max(e, self.floor) / self.breakeven)

    def path(self) -> dict:
        rng = np.random.default_rng(self.seed)
        T = self.burn + self.years
        demand = np.empty(T)
        fleet = np.empty(T)
        orders = np.zeros(T + self.lag + 1)
        earn = np.empty(T)
        demand[0], fleet[0] = 90.0, 100.0
        for t in range(T):
            if t > 0:
                demand[t] = demand[t - 1] * (1 + self.growth + self.shock * rng.standard_normal())
                e_prev = earn[t - 1]
                scrap = (0.045 if e_prev < 15 else 0.02) * fleet[t - 1]
                fleet[t] = fleet[t - 1] + orders[t - self.lag] - scrap if t >= self.lag else fleet[t - 1] - scrap
            u = demand[t] / fleet[t]
            earn[t] = self.earnings(u)
            orders[t] = fleet[t] * (0.02 + self.herd * max(0.0, (earn[t] - self.breakeven) / (self.top - self.breakeven)))
        s = slice(self.burn, T)
        return dict(demand=demand[s], fleet=fleet[s], util=demand[s] / fleet[s], earn=earn[s], orders=orders[:T][s],
                    price=np.array([self.price(e) for e in earn[s]]))

    def owner(self, rule: str, gap: int = 3, hi: float = 40.0, lo: float = 18.0, life: int = 25) -> dict:
        """The owner's ships under ``rule`` ('follow' or 'against'): when each was ordered, its price, what it earned and
        its profit over the run, valuing what is left of each ship at the end at that year's price."""
        P = self.path()
        e, price = P["earn"], P["price"]
        ships, last = [], -gap
        for t in range(self.years - self.lag):
            go = e[t] > hi if rule == "follow" else e[t] < lo
            if go and t - last >= gap:
                ships.append(t)
                last = t
        out = []
        for t in ships:
            d = t + self.lag
            cash = sum((e[k] - self.opex) * 0.365 for k in range(d, self.years))     # $ million a year: thousand/day x 365
            age = self.years - d
            resid = price[-1] * max(0.0, 1 - age / life)
            out.append(dict(order=t, delivery=d, price=price[t], earned=cash, resid=resid, profit=cash + resid - price[t],
                            ret=(cash + resid) / price[t] - 1))
        tot_cost = sum(s["price"] for s in out)
        tot_back = sum(s["earned"] + s["resid"] for s in out)
        return dict(rule=rule, ships=out, cost=tot_cost, back=tot_back, profit=tot_back - tot_cost,
                    ret=tot_back / tot_cost - 1 if tot_cost else 0.0,
                    avg_price=float(np.mean([s["price"] for s in out])) if out else 0.0,
                    avg_earn_at_delivery=float(np.mean([e[s["delivery"]] for s in out])) if out else 0.0)


def fuel_per_day(speed: float, design: float = 20.0, tonnes_at_design: float = 100.0) -> float:
    """Tonnes of fuel a day at ``speed`` knots: the cube law around a design speed."""
    return tonnes_at_design * (speed / design) ** 3


def voyage(distance: float = 11_000.0, speed: float = 20.0, fuel_price: float = 600.0, ship_day: float = 40_000.0,
           design: float = 20.0, tonnes_at_design: float = 100.0) -> dict:
    """One voyage of ``distance`` nautical miles: days at sea, fuel burned and its cost, the ship's other daily cost."""
    days = distance / (speed * 24)
    fuel = fuel_per_day(speed, design, tonnes_at_design) * days
    return dict(days=days, fuel_t=fuel, fuel_cost=fuel * fuel_price, ship_cost=days * ship_day,
                total=fuel * fuel_price + days * ship_day)


def best_speed(fuel_price: float = 600.0, ship_day: float = 40_000.0, **kw) -> float:
    """The speed, in knots, that makes a voyage cheapest: where the fuel saved by going slower equals the extra days."""
    speeds = np.arange(10.0, 24.01, 0.1)
    costs = [voyage(speed=v, fuel_price=fuel_price, ship_day=ship_day, **kw)["total"] for v in speeds]
    return float(speeds[int(np.argmin(costs))])
