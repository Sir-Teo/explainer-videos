"""Availability arithmetic (Part 50): nines as downtime budgets, series and parallel composition, the renewal
formula A = MTBF / (MTBF + MTTR), common-mode failures, k-of-n groups (a Raft majority) and N + k capacity."""

from __future__ import annotations

import math
import random

YEAR_MIN = 365.25 * 24 * 60


def nines(a: float) -> float:
    return -math.log10(1 - a) if a < 1 else float("inf")


def downtime(a: float) -> dict:
    """Allowed downtime at availability ``a``, in minutes per year, per 30-day month and per week."""
    q = 1 - a
    return {"availability": a, "nines": nines(a), "per_year_min": q * YEAR_MIN, "per_month_min": q * 30 * 24 * 60,
            "per_week_min": q * 7 * 24 * 60}


def nines_table(levels=(0.99, 0.995, 0.999, 0.9999, 0.99999)) -> list[dict]:
    return [downtime(a) for a in levels]


# ---------------------------------------------------------------- composition

def evaluate(node) -> float:
    """``node`` is a component's availability (a float), or ("series", [...]), ("parallel", [...]) or
    ("kofn", k, [...]) of independent parts."""
    if isinstance(node, (int, float)):
        return float(node)
    kind = node[0]
    if kind == "series":
        return math.prod(evaluate(c) for c in node[1])
    if kind == "parallel":
        return 1 - math.prod(1 - evaluate(c) for c in node[1])
    if kind == "kofn":
        k, parts = node[1], [evaluate(c) for c in node[2]]
        # exact probability that at least k of the (possibly different) parts are up, by dynamic programming
        dist = [1.0]
        for p in parts:
            new = [0.0] * (len(dist) + 1)
            for i, v in enumerate(dist):
                new[i] += v * (1 - p)
                new[i + 1] += v * p
            dist = new
        return sum(dist[k:])
    raise ValueError(kind)


def series_parallel(a: float = 0.99, ns=(1, 2, 3, 5, 10, 20, 50)) -> dict:
    """The two laws on one component of availability ``a``: n in series, and n in parallel."""
    return {"a": a, "series": [{"n": n, "up": a ** n, "nines": nines(a ** n)} for n in ns],
            "parallel": [{"n": n, "up": 1 - (1 - a) ** n, "nines": nines(1 - (1 - a) ** n)} for n in ns[:4]]}


def request_path() -> dict:
    """A request's path as a circuit: DNS, then a pair of load balancers, three app servers (any one), and a
    database primary with a standby; illustrative availabilities.  Compared with the same path built from single
    components."""
    stages = [("DNS", ("parallel", [0.999, 0.999, 0.999, 0.999])),          # four authoritative servers
              ("load balancers", ("parallel", [0.999, 0.999])),
              ("app servers", ("parallel", [0.99, 0.99, 0.99])),
              ("database", ("parallel", [0.999, 0.999]))]
    single = [("DNS", 0.999), ("load balancer", 0.999), ("app server", 0.99), ("database", 0.999)]
    rows = [{"stage": s, "up": evaluate(n)} for s, n in stages]
    total = evaluate(("series", [n for _, n in stages]))
    s_total = evaluate(("series", [n for _, n in single]))
    return {"rows": rows, "total": total, "nines": nines(total), "single": [{"stage": s, "up": u} for s, u in single],
            "single_total": s_total, "single_nines": nines(s_total), "downtime": downtime(total),
            "single_downtime": downtime(s_total)}


# ---------------------------------------------------------------- MTBF and MTTR

def renewal(mtbf_h: float = 720.0, mttr_h: float = 2.0, years: float = 200.0, seed: int = 0) -> dict:
    """Alternate exponential up times (mean ``mtbf_h``) and exponential repairs (mean ``mttr_h``); the measured
    fraction of time up against MTBF / (MTBF + MTTR).  The first year's timeline is kept for drawing."""
    rng = random.Random(seed)
    t, up_time, horizon = 0.0, 0.0, years * 365.25 * 24
    first_year = []
    while t < horizon:
        u = rng.expovariate(1 / mtbf_h)
        d = rng.expovariate(1 / mttr_h)
        if t < 365.25 * 24:
            first_year.append((t, t + u, t + u + d))
        up_time += min(u, max(0.0, horizon - t))
        t += u + d
    measured = up_time / max(t, horizon)
    return {"mtbf_h": mtbf_h, "mttr_h": mttr_h, "formula": mtbf_h / (mtbf_h + mttr_h), "measured": measured,
            "first_year": first_year[:40], "failures_first_year": len(first_year)}


def mttr_lever(mtbf_h: float = 720.0, mttr_h: float = 2.0) -> list[dict]:
    """Doubling the time between failures and halving the time to repair give exactly the same availability:
    2M / (2M + R) = M / (M + R/2).  Repair is usually the cheaper lever."""
    rows = []
    for name, m, r in (("today", mtbf_h, mttr_h), ("fail half as often", 2 * mtbf_h, mttr_h),
                       ("repair twice as fast", mtbf_h, mttr_h / 2), ("repair in 10 minutes", mtbf_h, 1 / 6)):
        a = m / (m + r)
        rows.append({"case": name, "mtbf_h": m, "mttr_h": r, "up": a, "nines": nines(a),
                     "down_min_per_year": (1 - a) * YEAR_MIN})
    return rows


# ---------------------------------------------------------------- correlation

def common_mode(a: float = 0.999, replicas: int = 3, shares=(0.0, 0.01, 0.05, 0.1, 0.3), trials: int = 2_000_000,
                seed: int = 0) -> list[dict]:
    """Each replica is down a fraction 1 - a of the time; a share ``c`` of that downtime is a common-mode event
    (a bad deploy, a shared power feed, one configuration) that takes all replicas down together.  Parallel
    availability by Monte Carlo against the independence formula 1 - (1 - a)^k."""
    import numpy as np
    rng = np.random.default_rng(seed)
    q = 1 - a
    out = []
    for c in shares:
        shared = rng.random(trials) < c * q
        own_q = (1 - c) * q / (1 - c * q) if c < 1 else 0.0        # keeps each replica's own downtime at q
        own = rng.random((trials, replicas)) < own_q
        down = shared | own.all(axis=1)
        up = 1 - float(down.mean())
        exact = 1 - (c * q + (1 - c * q) * own_q ** replicas)
        out.append({"share": c, "up": up, "exact": exact, "nines": nines(exact),
                    "independent": 1 - q ** replicas, "independent_nines": nines(1 - q ** replicas)})
    return out


# ---------------------------------------------------------------- groups

def majority(n: int, a: float) -> float:
    return evaluate(("kofn", n // 2 + 1, [a] * n))


def raft_table(avails=(0.99, 0.999), sizes=(1, 3, 5, 7)) -> list[dict]:
    """A Raft group (Part 38) serves while a majority is up."""
    return [{"a": a, "n": n, "up": majority(n, a), "nines": nines(majority(n, a))} for a in avails for n in sizes]


def n_plus_k(need: int = 10, a: float = 0.99, spares=(0, 1, 2, 3)) -> list[dict]:
    """A service needs ``need`` machines' capacity; with k spares it survives while at least ``need`` are up."""
    return [{"spares": k, "up": evaluate(("kofn", need, [a] * (need + k))),
             "nines": nines(evaluate(("kofn", need, [a] * (need + k))))} for k in spares]


def swiss_cheese(layers=(0.1, 0.05, 0.2, 0.1), rho: float = 0.0) -> dict:
    """Reason's Swiss-cheese model: an accident needs a hole in every layer of defence.  Independent layers
    multiply; when one latent condition (fatigue, a missing alert) opens holes together, they do not."""
    indep = math.prod(layers)
    return {"layers": list(layers), "independent": indep}
