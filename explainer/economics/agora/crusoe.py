"""One person, then two: production possibilities, the margin, and comparative advantage (Agora, Part 1).

Crusoe has ``T`` hours a day.  Hours spent fishing give ``F = a h^alpha`` fish, hours spent gathering give
``C = b (T - h)^beta`` coconuts; with exponents below one each extra hour yields less than the one before
(diminishing returns), so the frontier of what he can have bows outward and the opportunity cost of a fish rises as
he fishes more.  His tastes are Cobb-Douglas, ``U = theta ln F + (1 - theta) ln C``.

Then Friday arrives.  For the trade between them the series uses Ricardo's straight lines (a fixed number of hours
per fish and per coconut), so that the arithmetic of comparative advantage is exact: :func:`ricardo` gives each
person's opportunity costs, their choices alone, the competitive equilibrium when they can trade (who specializes,
the price, what each consumes), and the gain.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq, minimize_scalar


# ---------------------------------------------------------------------------
# One person
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Crusoe:
    hours: float = 10.0
    a: float = 3.0  # fish from the first hour, roughly
    alpha: float = 0.5
    b: float = 4.0  # coconuts
    beta: float = 0.5
    theta: float = 0.6  # the weight on fish in his tastes

    def fish(self, h):
        return self.a * np.asarray(h, float) ** self.alpha

    def coconuts(self, h):
        """Coconuts when ``h`` hours go to fishing (the rest to gathering)."""
        return self.b * (self.hours - np.asarray(h, float)) ** self.beta

    def frontier(self, n: int = 201) -> dict:
        """The production possibilities frontier, traced by the split of the day."""
        h = np.linspace(0, self.hours, n)
        return {"h": h, "fish": self.fish(h), "coconuts": self.coconuts(h)}

    def marginal(self, h: float) -> dict:
        """At a split of ``h`` hours fishing: the marginal products of an hour in each use and the opportunity cost
        of one more fish in coconuts, ``-dC/dF = MP_C / MP_F`` (the slope of the frontier)."""
        mpf = self.a * self.alpha * h ** (self.alpha - 1)
        mpc = self.b * self.beta * (self.hours - h) ** (self.beta - 1)
        return {"mp_fish": float(mpf), "mp_coconuts": float(mpc), "opportunity_cost": float(mpc / mpf)}

    def utility(self, f, c):
        f, c = np.asarray(f, float), np.asarray(c, float)
        return self.theta * np.log(f) + (1 - self.theta) * np.log(c)

    def best(self) -> dict:
        """His best split of the day, where the slope of the frontier equals the slope of his indifference curve
        (marginal rate of transformation = marginal rate of substitution)."""
        r = minimize_scalar(lambda h: -self.utility(self.fish(h), self.coconuts(h)), bounds=(1e-6, self.hours - 1e-6),
                            method="bounded", options={"xatol": 1e-10})
        h = float(r.x)
        f, c = float(self.fish(h)), float(self.coconuts(h))
        mrs = (self.theta / f) / ((1 - self.theta) / c)  # coconuts he would give for one more fish
        return {"h": h, "fish": f, "coconuts": c, "u": float(self.utility(f, c)), "mrs": float(mrs),
                "mrt": self.marginal(h)["opportunity_cost"]}

    def hour_by_hour(self) -> list[dict]:
        """What each successive hour of fishing adds in fish and costs in coconuts (starting from no fishing)."""
        out = []
        for k in range(int(self.hours)):
            df = float(self.fish(k + 1) - self.fish(k))
            dc = float(self.coconuts(k) - self.coconuts(k + 1))
            out.append({"hour": k + 1, "fish": df, "coconuts": dc, "cost_per_fish": dc / df})
        return out


# ---------------------------------------------------------------------------
# Two people
# ---------------------------------------------------------------------------
def ricardo(hours_per_fish=(1.0, 2.0), hours_per_coconut=(2.0, 2.5), hours=(12.0, 12.0), theta: float = 0.6,
            names=("Crusoe", "Friday")) -> dict:
    """Two people with straight-line frontiers and the same Cobb-Douglas tastes (weight ``theta`` on fish).

    Alone, each spends the share ``theta`` of the day fishing.  With trade at a price ``p`` (coconuts per fish), a
    person whose opportunity cost of a fish is below ``p`` makes only fish, above ``p`` only coconuts, and at ``p`` is
    indifferent.  The competitive price clears the market for fish; it is found here by checking the specialized
    case first and the two corner cases (one person makes both goods) after."""
    hf, hc, T = (np.asarray(x, float) for x in (hours_per_fish, hours_per_coconut, hours))
    oc_fish = hf / hc  # coconuts given up per fish: (hours per fish) / (hours per coconut)
    alone = []
    for i in range(2):
        f = theta * T[i] / hf[i]
        c = (1 - theta) * T[i] / hc[i]
        alone.append({"fish": float(f), "coconuts": float(c)})
    lo, hi = sorted(oc_fish)
    fish_maker = int(np.argmin(oc_fish))  # comparative advantage in fish
    coco_maker = 1 - fish_maker

    def demand_fish(p, prod):
        """Fish demanded by both at price p when person i produces prod[i] = (fish, coconuts)."""
        tot = 0.0
        for f, c in prod:
            income = f + c / p  # in fish
            tot += theta * income
        return tot

    # case 1: full specialization, price strictly between the opportunity costs
    full = [(0.0, 0.0), (0.0, 0.0)]
    full[fish_maker] = (T[fish_maker] / hf[fish_maker], 0.0)
    full[coco_maker] = (0.0, T[coco_maker] / hc[coco_maker])
    supply_f = full[fish_maker][0]
    p = brentq(lambda q: demand_fish(q, full) - supply_f, 1e-6, 1e6)
    if lo <= p <= hi:
        prod = full
        regime = "both specialize"
    elif p < lo:
        # the fish maker is too large: he also makes coconuts, the price sits at his opportunity cost
        p = lo
        prod = None
        regime = f"{names[fish_maker]} makes both"
    else:
        p = hi
        prod = None
        regime = f"{names[coco_maker]} makes both"
    if prod is None:
        # at a corner price, solve for the hours the indifferent person spends fishing so that the fish market clears
        ind = fish_maker if regime.startswith(names[fish_maker]) else coco_maker

        def excess(h):
            pr = [(0.0, 0.0), (0.0, 0.0)]
            other = 1 - ind
            pr[ind] = (h / hf[ind], (T[ind] - h) / hc[ind])
            if other == fish_maker:
                pr[other] = (T[other] / hf[other], 0.0)
            else:
                pr[other] = (0.0, T[other] / hc[other])
            return demand_fish(p, pr) - sum(x[0] for x in pr), pr

        h = brentq(lambda x: excess(x)[0], 0.0, float(T[ind]))
        prod = excess(h)[1]
    cons = []
    for (f, c) in prod:
        income = f + c / p
        cons.append({"fish": float(theta * income), "coconuts": float((1 - theta) * income * p)})
    u = lambda d: theta * np.log(d["fish"]) + (1 - theta) * np.log(d["coconuts"])  # noqa: E731
    people = []
    for i in range(2):
        people.append({"name": names[i], "hours_per_fish": float(hf[i]), "hours_per_coconut": float(hc[i]),
                       "hours": float(T[i]), "oc_fish": float(oc_fish[i]), "oc_coconut": float(1 / oc_fish[i]),
                       "max_fish": float(T[i] / hf[i]), "max_coconuts": float(T[i] / hc[i]),
                       "alone": alone[i], "makes": {"fish": float(prod[i][0]), "coconuts": float(prod[i][1])},
                       "trade": cons[i], "gain_u": float(u(cons[i]) - u(alone[i]))})
    absolute = [bool(hf[i] < hf[1 - i] and hc[i] < hc[1 - i]) for i in range(2)]
    return {"people": people, "price": float(p), "band": [float(lo), float(hi)], "regime": regime,
            "fish_maker": fish_maker, "absolute_advantage_in_both": absolute,
            "total_alone": {"fish": sum(a["fish"] for a in alone), "coconuts": sum(a["coconuts"] for a in alone)},
            "total_trade": {"fish": sum(c["fish"] for c in cons), "coconuts": sum(c["coconuts"] for c in cons)},
            "theta": theta}


def joint_frontier(r: dict) -> list[tuple]:
    """The two together: the kinked frontier of total fish and coconuts, from all coconuts to all fish, the person
    with the lower opportunity cost of fish switching to fish first.  Returns its three corners."""
    ps = r["people"]
    i = r["fish_maker"]
    a, b = ps[i], ps[1 - i]
    all_coco = (0.0, a["max_coconuts"] + b["max_coconuts"])
    kink = (a["max_fish"], b["max_coconuts"])
    all_fish = (a["max_fish"] + b["max_fish"], 0.0)
    return [all_coco, kink, all_fish]
