"""Delivery instruments (Part 41): a merge queue that tests batches and bisects failures, and a canary analysis that
must tell a bad release from noise."""

from __future__ import annotations

import math
import random


def merge_queue(batch: int, p_bad: float = 0.03, changes: int = 20000, test_hours: float = 0.5, seed: int = 0):
    """Changes arrive in a queue; the queue takes ``batch`` at a time, merges them on top of main and runs the
    tests (``test_hours``).  If green, all land.  If red, bisect: split the batch in halves and test each, down to
    the guilty changes, which are rejected; the rest land.  Returns test runs per change, hours of testing per
    landed change, and how many bad changes landed (none: every landed batch was tested)."""
    rng = random.Random(seed)
    runs = landed = rejected = 0
    i = 0

    def test(group):
        nonlocal runs
        runs += 1
        return not any(group)

    def resolve(group):
        nonlocal landed, rejected
        if test(group):
            landed += len(group)
            return
        if len(group) == 1:
            rejected += 1
            return
        h = len(group) // 2
        resolve(group[:h])
        resolve(group[h:])
    while i < changes:
        group = [rng.random() < p_bad for _ in range(min(batch, changes - i))]
        i += len(group)
        resolve(group)
    green = (1 - p_bad) ** batch
    return {"batch": batch, "p_bad": p_bad, "runs_per_change": runs / changes, "landed": landed,
            "rejected": rejected, "p_green": green, "hours_per_change": runs * test_hours / changes}


def merge_queue_table(batches=(1, 2, 4, 8, 16, 32, 64), ps=(0.01, 0.03, 0.1)):
    return [merge_queue(b, p) for p in ps for b in batches]


def canary(base_rate: float = 0.001, bad_rate: float = 0.002, requests=(1000, 3000, 10000, 30000, 100000),
           alpha: float = 0.01, trials: int = 4000, seed: int = 0):
    """A canary receives n requests of a new release, the baseline n of the old.  Declare it bad when a one-sided
    two-proportion z-test rejects at level ``alpha``.  Returns, for each n, the power (bad releases caught) and the
    false-alarm rate (good releases blocked), by simulation."""
    import numpy as np
    rng = np.random.default_rng(seed)
    z = _zcrit(alpha)
    rows = []
    for n in requests:
        def flags(rate_canary):
            a = rng.binomial(n, base_rate, size=trials)
            b = rng.binomial(n, rate_canary, size=trials)
            p = (a + b) / (2 * n)
            se = np.sqrt(np.maximum(p * (1 - p) * 2 / n, 1e-12))
            return ((b - a) / n / se) > z
        rows.append({"requests": n, "power": float(flags(bad_rate).mean()),
                     "false_alarm": float(flags(base_rate).mean()),
                     "expected_errors": n * base_rate})
    return {"rows": rows, "base_rate": base_rate, "bad_rate": bad_rate, "alpha": alpha}


def _zcrit(alpha):
    lo, hi = 0.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if 0.5 * math.erfc(mid / math.sqrt(2)) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
