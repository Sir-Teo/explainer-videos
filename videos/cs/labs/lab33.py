"""Lab 33: enumerate every interleaving of two racing increments, then break and repair Peterson's lock."""

from videos.coursekit import labs  # noqa: I001  (first, so the library imports without manim)

import itertools
from collections import Counter
from math import comb

import numpy as np

from explainer.cs.conc import mc

TITLE = "Every schedule of a race, and a lock that the store buffer breaks"
GOAL = ("Run the part's model checker on two threads that each add one to a counter k times: count the schedules "
        "and the final values, and check them against a brute-force enumeration and a random scheduler. Then ask "
        "the checker whether Peterson's lock keeps mutual exclusion under SC, TSO and PSO, with and without fences.")
TASKS = [
    "Use mc.counter(3, 1): three threads, one increment each. How many schedules are there, and which finals occur?",
    "Explore mc.naive_flags(1) with the mutex invariant and print r.trace(r.violation). Which eight steps break it?",
    "Check mc.bakery(2, 1) under 'tso' with and without fence=True. Does Lamport's bakery need the fence too?",
]
STEPS = ("ld", "add", "st")


def final_count(order):
    """Run one interleaving by hand: `order` lists which thread takes each step; every increment is ld, add, st."""
    c, reg, pc = 0, [0, 0], [0, 0]
    for t in order:
        step = STEPS[pc[t] % 3]
        if step == "ld":
            reg[t] = c
        elif step == "add":
            reg[t] += 1
        else:
            c = reg[t]
        pc[t] += 1
    return c


def brute_force(k):
    """Every way to interleave two threads of 3k steps each, by choosing which positions thread 0 takes."""
    n = 6 * k
    out = Counter()
    for where in itertools.combinations(range(n), 3 * k):
        order = [1] * n
        for i in where:
            order[i] = 0
        out[final_count(order)] += 1
    return dict(out)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    def count(s, prog):
        return dict(zip(prog.vars, s[2]))["c"]

    # 1. counter++ twice (Chapter 2): schedules, states and outcomes
    table = {}
    for k in (1, 2, 3, 4):
        prog = mc.counter(2, k)
        table[k] = (mc.schedules(prog, project=count), mc.explore(prog, project=count).states)
        assert sum(table[k][0].values()) == comb(6 * k, 3 * k), "C(6k, 3k) schedules"
        assert min(table[k][0]) == (1 if k == 1 else 2), "for k >= 2 the count can end as low as 2"
    one, two = table[1][0], table[2][0]
    lab.row("k = 1: 20 schedules", f"{one[2]} end at 2, {one[1]} at 1   (the film: 2 and 18)")
    assert one == {2: 2, 1: 18} and one == brute_force(1)
    lab.row("k = 2: 924 schedules, by final count", "   ".join(f"{c}: {n}" for c, n in sorted(two.items())))
    assert two == brute_force(2), "the checker agrees with the brute-force enumeration"
    lab.row("schedules against states, k = 1..4",
            "   ".join(f"{sum(table[k][0].values()):,} / {table[k][1]:,}" for k in (1, 2, 3, 4)))
    assert [table[k][1] for k in (1, 2, 3, 4)] == [22, 138, 585, 1846]
    for how in ("fai", "lock"):
        assert set(mc.explore(mc.counter(2, 3, how), project=count).finals) == {6}, how

    # 2. a random scheduler sees only part of what the checker proves possible
    seen = Counter()
    for _ in range(20000):
        order = rng.permutation([0] * 9 + [1] * 9)
        seen[final_count(order)] += 1
    possible = table[3][0]
    lab.row("k = 3, 20,000 random schedules: finals seen", "   ".join(f"{c}: {n}" for c, n in sorted(seen.items()))
            + f"   (possible: {min(possible)}..{max(possible)})")
    assert set(seen) <= set(possible) and seen[6] / 20000 < 0.01, "almost every schedule loses an update"

    # 3. Peterson under three memory models (Chapters 3 and 4)
    verdict = {}
    for model in ("sc", "tso", "pso"):
        for fence in (False, True, "both"):
            r = mc.explore(mc.peterson(fence, 1), model, mc.mutex)
            verdict[model, fence] = (r.violation is not None, len(r.trace(r.violation)) if r.violation else 0, r.states)
    names = {False: "no fence", True: "one fence", "both": "two fences"}
    for model in ("sc", "tso", "pso"):
        lab.row(f"Peterson under {model.upper()}", "   ".join(
            f"{names[f]}: " + (f"broken in {verdict[model, f][1]} steps" if verdict[model, f][0] else "safe")
            for f in (False, True, "both")))
    assert not verdict["sc", False][0] and verdict["sc", False][2] == 258
    assert verdict["tso", False][:2] == (True, 10) and not verdict["tso", True][0]
    assert verdict["pso", True][0] and not verdict["pso", "both"][0]

    # 4. the dining philosophers (Chapter 8)
    dead, fixed = mc.explore(mc.philosophers(5, False)), mc.explore(mc.philosophers(5, True))
    lab.row("five philosophers", f"deadlock after {len(dead.trace(dead.deadlocks[0]))} steps;"
                                 f" one reversed: none in {fixed.states:,} states")
    assert dead.deadlocks and not fixed.deadlocks
    lab.note = ("Testing samples schedules; the checker visits every state. Two plain increments are almost never "
                "safe, and Peterson's proof holds only while stores reach memory in program order.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for k, c in ((1, labs.GREY), (2, labs.BLUE), (3, labs.GOLD), (4, labs.RED)):
        sch = table[k][0]
        total = sum(sch.values())
        lost = sorted(2 * k - f for f in sch)
        ax[0].plot(lost, [sch[2 * k - m] / total for m in lost], "o-", color=c, label=f"k = {k}: {total:,} schedules")
    ax[0].set(title="Two threads, k increments each: updates lost", xlabel="updates lost (2k − final count)",
              ylabel="fraction of schedules")
    ax[0].legend()
    ks = [1, 2, 3, 4]
    ax[1].plot(ks, [comb(6 * k, 3 * k) for k in ks], "o-", color=labs.RED, label="schedules: C(6k, 3k)")
    ax[1].plot(ks, [table[k][1] for k in ks], "o-", color=labs.GREEN, label="states the checker visits")
    ax[1].set(title="Why the checker searches states, not schedules", xlabel="increments per thread k", yscale="log",
              xticks=ks)
    ax[1].legend()
    lab.fig = fig
    return lab
