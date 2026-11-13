"""Lab 35: count the page I/Os of four join algorithms, then test schedules for serializability."""

from videos.coursekit import labs  # noqa: I001  (first, so the library imports without manim)

import itertools

import numpy as np

from explainer.cs.db import joins
from explainer.cs.db import txn

TITLE = "Joins by the page, and which interleavings are safe"
GOAL = ("Join a 400-page table with a 200-page table by block nested loops, sort-merge and Grace hash with 5 to 80 "
        "pages of memory, and compare every measured page count with its formula. Then test interleaved "
        "transactions with the precedence graph, against a brute-force search over serial orders, with and "
        "without two-phase locking.")
TASKS = [
    "Make the outer table 10 times larger (n_r=200_000) at B = 80. Which join wins now, and what does the formula say?",
    "Run txn.run_2pl with policy='wait-die' and 'wound-wait' and count r['aborted']. Which aborts more, and why?",
    "Count how many of the 90 interleavings are view-serializable (txn.view_serializable). Which ones are new?",
]
BUFFERS = (5, 10, 20, 40, 80)
THREE = {1: [("r", "x"), ("w", "y")], 2: [("r", "y"), ("w", "x")], 3: [("w", "x"), ("w", "y")]}   # Chapter 9's three


def schedule(programs, order):
    """Interleave the programs in this order of turns, with no locks, and commit them all."""
    at = dict.fromkeys(programs, 0)
    s = []
    for t in order:
        if at[t] < len(programs[t]):
            s.append((t, *programs[t][at[t]]))
            at[t] += 1
    return s + [(t, "c", None) for t in programs]


def serial_order_exists(s):
    """Brute force: is there an order of the transactions that every conflicting pair of steps respects?"""
    ops = [st for st in s if st[1] in "rw"]
    pairs = {(a[0], b[0]) for i, a in enumerate(ops) for b in ops[i + 1:]
             if a[0] != b[0] and a[2] == b[2] and "w" in (a[1], b[1])}
    names = sorted({st[0] for st in s})
    return any(all(p.index(a) < p.index(b) for a, b in pairs) for p in itertools.permutations(names))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. joins, page by page (Chapter 5): M = 400 and N = 200 pages of 50 rows
    rows = {B: joins.compare(B=B, seed=seed) for B in BUFFERS}
    for B in (5, 80):
        m, f = rows[B]["measured"], rows[B]["formula"]
        lab.row(f"B = {B}: block nested loops", f"measured {m['block nested loops']:,}   formula {f['block nested loops']:,}")
        lab.row(f"B = {B}: sort-merge", f"measured {m['sort-merge']:,}   formula {f['sort-merge']:,}")
    for B in BUFFERS:
        m, f = rows[B]["measured"], rows[B]["formula"]
        assert m["block nested loops"] == f["block nested loops"] and m["sort-merge"] == f["sort-merge"], B
        assert abs(m["grace hash"] / f["grace hash"] - 1) < 0.12, "partial pages cost Grace hash a few percent"
        assert m["index nested loops"] <= f["index nested loops"], "keys without a match read no data page"
    small, large = rows[5]["measured"], rows[80]["measured"]
    lab.row("Grace hash, formula 3(M + N)", f"{rows[5]['formula']['grace hash']:,}   (measured within 12% at every B;"
                                            f" buckets fit in memory from B = {min(B for B in BUFFERS if rows[B]['buckets_fit'])})")
    assert min(large, key=large.get) == "block nested loops", "with 80 pages of memory the simplest join wins"
    assert min(small, key=small.get) == "grace hash" and small["block nested loops"] > 10 * small["grace hash"]

    # 2. conflict serializability (Chapter 9): the 90 interleavings of three two-step transactions
    orders = sorted(set(itertools.permutations([1, 1, 2, 2, 3, 3])))
    good = sum(txn.conflict_serializable(schedule(THREE, o))[0] for o in orders)
    lab.row("interleavings of three transactions", f"{len(orders)}, conflict-serializable: {good}   (the film: 90 and 10)")
    assert (len(orders), good) == (90, 10)

    # 3. the precedence graph against brute force, and what two-phase locking guarantees (Chapter 10)
    free, locked = {}, {}
    for n in (2, 3, 4):
        ok_free = ok_2pl = 0
        for _ in range(300):
            progs = {t: [(str(rng.choice(["r", "w"])), str(rng.choice(list("ABC")))) for _ in range(3)]
                     for t in range(1, n + 1)}
            order = [int(t) for t in rng.integers(1, n + 1, 12 * n)]
            s = schedule(progs, order + list(progs) * 3)
            verdict = txn.conflict_serializable(s)[0]
            assert verdict == serial_order_exists(s), "no cycle exactly when a serial order exists"
            assert not verdict or txn.view_serializable(s)[0], "conflict-serializable implies view-serializable"
            ok_free += verdict
            ok_2pl += txn.conflict_serializable(txn.run_2pl(progs, order)["schedule"])[0]
        free[n], locked[n] = ok_free / 300, ok_2pl / 300
    lab.row("random interleavings serializable, 2 / 3 / 4 transactions",
            "   ".join(f"{free[n]:.0%}" for n in (2, 3, 4)) + "   with strict 2PL: "
            + "   ".join(f"{locked[n]:.0%}" for n in (2, 3, 4)))
    assert all(v == 1.0 for v in locked.values()), "every 2PL schedule is conflict-serializable"
    assert free[4] < free[2] < 0.9
    lab.note = ("The cheapest join depends on the memory: block nested loops with 80 buffer pages, hashing with 5. "
                "Most interleavings are not serializable, and the precedence graph finds exactly the ones that "
                "are; two-phase locking admits only those.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for name, c in (("block nested loops", labs.RED), ("sort-merge", labs.BLUE), ("grace hash", labs.GREEN)):
        ax[0].plot(BUFFERS, [rows[B]["formula"][name] for B in BUFFERS], color=c, label=f"{name}, formula")
        ax[0].plot(BUFFERS, [rows[B]["measured"][name] for B in BUFFERS], "o", color=c)
    ax[0].plot([], [], "o", color=labs.GREY, label="measured page I/Os")
    ax[0].set(title="Joining 400 pages with 200", xlabel="buffer pages B", ylabel="page I/Os", xscale="log",
              yscale="log", xticks=BUFFERS, xticklabels=[str(b) for b in BUFFERS])
    ax[0].minorticks_off()
    ax[0].set_yticks([2000, 5000, 10000, 20000], ["2,000", "5,000", "10,000", "20,000"])
    ax[0].legend()
    x = np.arange(3)
    ax[1].bar(x - 0.2, [free[n] for n in (2, 3, 4)], width=0.4, color=labs.RED, label="no locks")
    ax[1].bar(x + 0.2, [locked[n] for n in (2, 3, 4)], width=0.4, color=labs.GREEN, label="strict two-phase locking")
    ax[1].set_xticks(x, ["2 transactions", "3", "4"])
    ax[1].set(title="Random interleavings that are conflict-serializable", ylabel="fraction of 300", ylim=(0, 1.3))
    ax[1].legend(loc="upper right", ncols=2)
    lab.fig = fig
    return lab
