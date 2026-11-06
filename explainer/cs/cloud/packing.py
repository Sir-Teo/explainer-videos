"""Scheduling as bin packing (Part 45): next fit, first fit, first fit decreasing and best fit against an exact
branch-and-bound optimum on small instances; the adversarial family on which next fit uses nearly twice the optimum;
vector packing over CPU and memory; and the reduction from partition that makes packing NP-hard."""

from __future__ import annotations

import random


def next_fit(items, cap=1.0):
    bins, cur = [], []
    load = 0.0
    for x in items:
        if load + x > cap + 1e-12:
            bins.append(cur)
            cur, load = [], 0.0
        cur.append(x)
        load += x
    if cur:
        bins.append(cur)
    return bins


def first_fit(items, cap=1.0):
    bins, loads = [], []
    for x in items:
        for i, l in enumerate(loads):
            if l + x <= cap + 1e-12:
                bins[i].append(x)
                loads[i] += x
                break
        else:
            bins.append([x])
            loads.append(x)
    return bins


def best_fit(items, cap=1.0):
    bins, loads = [], []
    for x in items:
        best, room = None, None
        for i, l in enumerate(loads):
            r = cap - l - x
            if r >= -1e-12 and (room is None or r < room):
                best, room = i, r
        if best is None:
            bins.append([x])
            loads.append(x)
        else:
            bins[best].append(x)
            loads[best] += x
    return bins


def ffd(items, cap=1.0):
    return first_fit(sorted(items, reverse=True), cap)


def optimum(items, cap=1.0, limit=None):
    """Exact minimum number of bins by branch and bound (items sorted decreasing; each item tried in every open bin
    with room, and in one new bin; bins with equal loads are not tried twice)."""
    xs = sorted(items, reverse=True)
    best = [len(ffd(xs, cap))]
    lower = int(-(-sum(xs) // cap)) if cap == 1.0 else None
    loads = []

    def go(k):
        if len(loads) >= best[0]:
            return
        if k == len(xs):
            best[0] = len(loads)
            return
        if lower is not None and best[0] == lower:
            return
        seen = set()
        for i in range(len(loads)):
            if loads[i] + xs[k] <= cap + 1e-12 and round(loads[i], 9) not in seen:
                seen.add(round(loads[i], 9))
                loads[i] += xs[k]
                go(k + 1)
                loads[i] -= xs[k]
        loads.append(xs[k])
        go(k + 1)
        loads.pop()
    go(0)
    return best[0]


def compare(n=24, trials=200, seed=0, dist="uniform"):
    rng = random.Random(seed)
    tot = {"next fit": 0.0, "first fit": 0.0, "best fit": 0.0, "first fit decreasing": 0.0}
    worst = dict.fromkeys(tot, 1.0)
    for _ in range(trials):
        if dist == "uniform":
            items = [round(rng.uniform(0.05, 0.7), 3) for _ in range(n)]
        else:
            items = [round(rng.choice([0.26, 0.24, 0.51, 0.49, 0.3, 0.2]) + rng.uniform(-0.01, 0.01), 3)
                     for _ in range(n)]
        opt = optimum(items)
        for name, f in (("next fit", next_fit), ("first fit", first_fit), ("best fit", best_fit),
                        ("first fit decreasing", ffd)):
            r = len(f(items)) / opt
            tot[name] += r
            worst[name] = max(worst[name], r)
    return {"n": n, "trials": trials, "dist": dist, "mean_ratio": {k: v / trials for k, v in tot.items()},
            "worst_ratio": worst}


def next_fit_bad(k=20, eps=0.01):
    """k halves alternating with k tiny items eps: next fit closes a bin at every half, using k bins; the optimum
    pairs the halves and puts all the small items together, about k/2 + 1, so the ratio tends to 2."""
    items = []
    for _ in range(k):
        items += [0.5, eps]
    nf = len(next_fit(items))
    import math
    opt = optimum(items) if k <= 12 else math.ceil(k / 2) + math.ceil(k * eps - 1e-9)   # halves paired; smalls together
    return {"items": len(items), "next_fit": nf, "optimum": opt, "ratio": nf / opt}


def vector_pack(machines=40, jobs=200, seed=1):
    """Containers with (CPU, memory) demands on machines with capacity (1, 1): first fit decreasing by the larger
    dimension, against packing by CPU alone (which overloads memory and must spill)."""
    rng = random.Random(seed)
    js = []
    for _ in range(jobs):
        kind = rng.random()
        if kind < 0.4:
            js.append((rng.uniform(0.2, 0.5), rng.uniform(0.02, 0.1)))      # compute-heavy
        elif kind < 0.8:
            js.append((rng.uniform(0.02, 0.1), rng.uniform(0.2, 0.5)))      # memory-heavy
        else:
            js.append((rng.uniform(0.05, 0.2), rng.uniform(0.05, 0.2)))

    def pack(order):
        loads = []
        for c, m in order:
            for L in loads:
                if L[0] + c <= 1 and L[1] + m <= 1:
                    L[0] += c
                    L[1] += m
                    break
            else:
                loads.append([c, m])
        return loads
    two = pack(sorted(js, key=lambda j: -max(j)))
    one = pack(sorted(js, key=lambda j: -j[0]))
    lb = max(sum(c for c, _ in js), sum(m for _, m in js))
    util = lambda L: (sum(x[0] for x in L) / len(L), sum(x[1] for x in L) / len(L))  # noqa: E731
    return {"jobs": jobs, "lower_bound": lb, "ffd_max_dim": len(two), "ffd_cpu_only": len(one),
            "util_max_dim": util(two), "util_cpu_only": util(one)}


def partition_reduction(nums=(3, 1, 1, 2, 2, 1)):
    """Partition reduces to bin packing: the numbers split into two equal halves iff items nums/(sum/2) fit in two
    bins of size 1."""
    half = sum(nums) / 2
    items = [x / half for x in nums]
    return {"numbers": list(nums), "half": half, "items": items, "bins_needed": optimum(items),
            "partition_exists": optimum(items) == 2}
