"""Durability of object storage (Part 45): a Markov model of failure and repair for an object stored as n fragments
of which any k suffice (replication is k = 1), the mean time to data loss derived by solving the chain exactly, a
Monte Carlo check, and the probability of losing an object in a year."""

from __future__ import annotations

import math
import random

HOURS_PER_YEAR = 24 * 365.25


def mttdl(n: int, k: int, afr: float = 0.02, repair_hours: float = 24.0):
    """States count failed fragments; each live fragment fails at rate lam (from an annual failure rate), and one
    failed fragment is repaired at a time at rate mu; losing more than n - k fragments loses the data.  For this
    birth-death chain the expected time to climb from state i to i + 1 is T_i = (1 + mu T_{i-1}) / lam_i, with
    lam_i = (n - i) lam and T_0 = 1 / (n lam), and the mean time to data loss is the sum of the T_i."""
    lam = -math.log(1 - afr) / HOURS_PER_YEAR
    mu = 1 / repair_hours
    T, total = 0.0, 0.0
    for i in range(n - k + 1):
        li = (n - i) * lam
        T = (1 + (mu * T if i > 0 else 0.0)) / li
        total += T
    years = total / HOURS_PER_YEAR
    p_year = -math.expm1(-1 / years)
    return {"n": n, "k": k, "overhead": n / k, "mttdl_years": years, "p_loss_year": p_year,
            "nines": -math.log10(p_year)}


def schemes(afr=0.02, repair_hours=24.0):
    rows = [mttdl(1, 1, afr, repair_hours), mttdl(2, 1, afr, repair_hours), mttdl(3, 1, afr, repair_hours),
            mttdl(9, 6, afr, repair_hours), mttdl(14, 10, afr, repair_hours), mttdl(16, 10, afr, repair_hours)]
    names = ["one copy", "two copies", "three copies", "RS(6, 3)", "RS(10, 4)", "RS(10, 6)"]
    for r, nm in zip(rows, names):
        r["name"] = nm
    return rows


def simulate(n=3, k=1, afr=0.5, repair_hours=500.0, trials=2000, seed=0):
    """Monte Carlo of the same chain (with exaggerated rates so losses happen in the simulation's lifetime): mean
    time to loss, to compare with the exact solution."""
    rng = random.Random(seed)
    lam = -math.log(1 - afr) / HOURS_PER_YEAR
    mu = 1 / repair_hours
    times = []
    for _ in range(trials):
        t, failed = 0.0, 0
        while failed < n - k + 1:
            rf = (n - failed) * lam
            rr = mu if failed else 0.0
            tot = rf + rr
            t += rng.expovariate(tot)
            failed += 1 if rng.random() < rf / tot else -1
        times.append(t)
    sim = sum(times) / trials / HOURS_PER_YEAR
    return {"simulated_years": sim, "exact_years": mttdl(n, k, afr, repair_hours)["mttdl_years"]}


def correlated(racks=7, per_rack=2, n=14, k=10, rack_afr=0.05, repair_hours=24.0):
    """Whole racks fail together.  With fragments spread per_rack to a rack, the data is lost only if more than
    (n - k) / per_rack racks are down at once; with all fragments on one rack, one rack failure loses it.  Rate of
    loss ~ (rate of a rack failing) x P(enough other racks already down), with each rack down a fraction
    rack_afr x repair_hours of the time."""
    from math import comb
    r = -math.log(1 - rack_afr) / HOURS_PER_YEAR          # per rack per hour
    down = r * repair_hours                                 # chance a given rack is down at a random moment
    need = (n - k) // per_rack + 1                          # racks down at once to lose the data
    rate = racks * r * comb(racks - 1, need - 1) * down ** (need - 1)
    spread = rate * HOURS_PER_YEAR
    one_rack = rack_afr
    return {"racks": racks, "need_down_together": need, "p_loss_year_spread": spread, "p_loss_year_one_rack": one_rack}
