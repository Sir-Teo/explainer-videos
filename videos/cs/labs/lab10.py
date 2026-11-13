"""Lab 10: schedule a random computation greedily on 1 to 64 processors and hold it against Brent's bound."""

from videos.coursekit import labs

import math

import numpy as np

from explainer.cs.pebble import parallel as par

TITLE = "Brent's theorem, two scans and a sorting network"
GOAL = ("Build a computation of 2,000 unit nodes, schedule it greedily on p processors, and check "
        "max(T1/p, Tinf) <= Tp <= T1/p + Tinf for every p. Then count the additions of the Hillis-Steele and "
        "Blelloch scans, and test Batcher's 8-wire bitonic network with the 0-1 principle, whole and with one "
        "comparator removed.")
TASKS = [
    "Schedule with priority=lambda v: -v (newest ready node first). Does the makespan stay inside the two bounds? Must it?",
    "Replace the random computation by par.fork_join_tree(10) and compare par.steal(d, p)['makespan'] with greedy's.",
    "Find the 0-1 input that each single removed comparator of par.bitonic(8) fails on. Is any comparator redundant?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    d = par.Dag.random(2000, width=int(rng.integers(24, 48)), fan=3, seed=seed + 1)
    t1, tinf = d.work(), d.span()
    ps = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
    spans = []
    lab = labs.Lab()
    lab.row("work T1, span Tinf, parallelism", f"{t1}, {tinf}, {t1 / tinf:.1f}")
    for p in ps:
        g = par.greedy(d, p)
        spans.append(g["makespan"])
        lower, upper = max(math.ceil(t1 / p), tinf), t1 / p + tinf
        assert lower <= g["makespan"] <= upper, "Brent: a greedy schedule lies between the bounds"
        assert g["complete"] <= t1 / p and g["incomplete"] <= tinf, "the proof's two kinds of step"
        if p in (2, 8, 64):
            lab.row(f"p = {p}: greedy steps", f"{g['makespan']}   (at least {lower}, at most {upper:.0f}; "
                                               f"{g['complete']} complete + {g['incomplete']} incomplete)")
    assert spans[0] == t1 and spans[-1] < 1.2 * tinf, "one processor does the work; many approach the span"

    ns = [2 ** k for k in range(1, 11)]
    hs, bl = [], []
    for n in ns:
        xs = [int(v) for v in rng.integers(0, 100, n)]
        h, b = par.hillis_steele(xs), par.blelloch(xs)
        prefix = np.cumsum(xs)
        assert h["result"] == list(prefix) and b["result"] == [0] + list(prefix[:-1]), "both compute the running totals"
        assert h["ops"] == n * int(math.log2(n)) - n + 1 and b["ops"] == 2 * (n - 1)
        hs.append(h["ops"])
        bl.append(b["ops"])
    lab.row("scan of 1,024 numbers: additions", f"Hillis-Steele {hs[-1]:,} = n log2 n - n + 1   Blelloch {bl[-1]:,} = 2(n - 1)")

    net = par.bitonic(8)
    ok, _ = par.sorts_all_01(net, 8)
    k = int(rng.integers(len(net)))
    broken, witness = par.sorts_all_01(net[:k] + net[k + 1:], 8)
    lab.row("bitonic network on 8 wires", f"{len(net)} comparators in {len(par.layers(net))} layers; sorts all 256 0-1 inputs: {ok}")
    lab.row(f"the same without comparator {k}", f"fails on {''.join(map(str, witness))}" if not broken else "still sorts")
    assert ok and par.sorts_all_perms(net, 8) and (len(net), len(par.layers(net))) == (24, 6)
    assert not broken and par.apply(net[:k] + net[k + 1:], witness) != sorted(witness), "every comparator is needed"
    lab.note = ("A greedy schedule is never more than T1/p + Tinf, so it is within a factor of two of the best; "
                "Blelloch's scan does linear work where Hillis-Steele does n log n; 256 inputs of zeros and ones "
                "certify a network that 40,320 orderings would.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.arange(1, 65)
    ax[0].plot(grid, t1 / grid + tinf, color=labs.ORANGE, label="Brent: T1/p + Tinf")
    ax[0].plot(grid, np.maximum(t1 / grid, tinf), color=labs.GREY, label="lower bound max(T1/p, Tinf)")
    ax[0].plot(ps, spans, "o", color=labs.GREEN, label="greedy schedule")
    ax[0].set(xscale="log", yscale="log", title=f"{t1} nodes, span {tinf}: steps on p processors", xlabel="processors p",
              ylabel="steps")
    ax[0].legend()
    ax[1].plot(ns, hs, "o-", color=labs.RED, label="Hillis-Steele: n log2 n - n + 1")
    ax[1].plot(ns, bl, "o-", color=labs.BLUE, label="Blelloch: 2(n - 1)")
    ax[1].plot(ns, [n - 1 for n in ns], ls=":", color=labs.MUTED, label="serial: n - 1")
    ax[1].set(xscale="log", yscale="log", title="Additions to scan n numbers", xlabel="n", ylabel="additions")
    ax[1].legend()
    lab.fig = fig
    return lab
