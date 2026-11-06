"""The theory of congestion control (Part 37): Chiu and Jain's phase plot, and network utility maximization.

    chiu_jain(rule, x0, capacity, steps)   two users sharing a link of the given capacity, each told "overloaded" when
        x1 + x2 > capacity; rule in {"AIMD", "AIAD", "MIAD", "MIMD"} with increase a (or factor) and decrease b.
        Returns the trajectory and the final fairness (Jain's index) and efficiency
    num_dual(routes, capacities, step, iters)   Kelly's network utility maximization with log utilities (proportional
        fairness), solved by dual (sub)gradient ascent: each link sets a price from its excess demand, each flow
        sends x_r = 1 / (sum of prices on its route).  Returns rates, prices and the convex-solver optimum to compare
"""
from __future__ import annotations

import math


def jain(xs) -> float:
    xs = list(xs)
    return sum(xs) ** 2 / (len(xs) * sum(x * x for x in xs))


def chiu_jain(rule: str, x0=(0.1, 0.6), capacity: float = 1.0, steps: int = 60, a: float = 0.02,
              b: float = 0.5, m: float = 1.1) -> dict:
    x1, x2 = x0
    traj = [(x1, x2)]
    for _ in range(steps):
        over = x1 + x2 > capacity
        if rule == "AIMD":
            x1, x2 = (x1 * b, x2 * b) if over else (x1 + a, x2 + a)
        elif rule == "AIAD":
            x1, x2 = (max(0, x1 - a), max(0, x2 - a)) if over else (x1 + a, x2 + a)
        elif rule == "MIMD":
            x1, x2 = (x1 * b, x2 * b) if over else (x1 * m, x2 * m)
        elif rule == "MIAD":
            x1, x2 = (max(0, x1 - a), max(0, x2 - a)) if over else (x1 * m, x2 * m)
        traj.append((x1, x2))
    tail = traj[-20:]
    fair = sum(jain(p) if sum(p) > 0 else 1 for p in tail) / len(tail)
    eff = sum(sum(p) for p in tail) / len(tail) / capacity
    return {"rule": rule, "trajectory": traj, "fairness": fair, "efficiency": eff,
            "final_ratio": (tail[-1][0] / tail[-1][1]) if tail[-1][1] else None}


def num_dual(routes: dict, capacities: dict, step: float = 0.02, iters: int = 4000) -> dict:
    """routes: flow -> list of links; capacities: link -> capacity.  Maximize sum log x_r s.t. link loads <= c."""
    p = {l: 1.0 for l in capacities}
    hist = []
    for k in range(iters):
        x = {r: 1.0 / max(1e-9, sum(p[l] for l in ls)) for r, ls in routes.items()}
        for l, c in capacities.items():
            load = sum(x[r] for r, ls in routes.items() if l in ls)
            p[l] = max(1e-6, p[l] + step * (load - c))
        if k % 50 == 0:
            hist.append({"iter": k, "x": dict(x), "p": dict(p)})
    x = {r: 1.0 / sum(p[l] for l in ls) for r, ls in routes.items()}
    util = sum(math.log(v) for v in x.values())
    loads = {l: sum(x[r] for r, ls in routes.items() if l in ls) for l in capacities}
    return {"x": x, "p": p, "utility": util, "loads": loads, "history": hist}


def max_min(routes: dict, capacities: dict) -> dict:
    """Max-min fair rates by progressive filling, to set beside proportional fairness."""
    x = {r: 0.0 for r in routes}
    frozen = set()
    cap = dict(capacities)
    while len(frozen) < len(routes):
        active = [r for r in routes if r not in frozen]
        # the smallest equal increment that saturates some link
        best = None
        for l, c in cap.items():
            users = [r for r in active if l in routes[r]]
            if users:
                inc = (c - sum(x[r] for r in routes if l in routes[r])) / len(users)
                if best is None or inc < best[0]:
                    best = (inc, l)
        if best is None:
            break
        inc, l = best
        for r in active:
            x[r] += inc
        for r in active:
            if l in routes[r]:
                frozen.add(r)
    return x
