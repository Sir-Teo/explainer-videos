"""Lab 32: replay reference strings through FIFO, LRU and OPT, and find Belady's anomaly."""

from videos.coursekit import labs  # noqa: I001  (first, so the library imports without manim)

import random

import numpy as np

from explainer.cs.os import paging as P

TITLE = "Which page to evict: Belady's anomaly and the stack property"
GOAL = ("Count page faults on Belady's reference string with 1 to 5 frames under FIFO, LRU and OPT; search random "
        "strings for the anomaly; then check on a trace with locality that LRU never gets worse with more "
        "frames, that one pass of stack distances gives its whole miss curve, and that OPT is never beaten.")
TASKS = [
    "Add 'clock' and 'arc' to the right panel. Which one tracks LRU, and where does either beat it?",
    "Search strings of length 12 over 5 pages going from 3 to 4 frames (P.anomalies(12, 5, 3, rng)). Do you find any?",
    "Set the hot-set probability to 0.5 and to 0.99. How does the knee of the miss curve move, and why?",
]
BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
POLICIES = (("fifo", labs.RED), ("lru", labs.BLUE), ("opt", labs.GREEN))


def locality_trace(rng, n=4000, pages=40, hot=6, p_hot=0.9, phase=400):
    """A hot set of `hot` pages that moves every `phase` references; the other references go anywhere."""
    out, base = [], 0
    for i in range(n):
        if i % phase == 0:
            base = int(rng.integers(0, pages))
        out.append((base + int(rng.integers(0, hot))) % pages if rng.random() < p_hot else int(rng.integers(0, pages)))
    return out


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Belady's string (Chapter 7)
    sizes = [1, 2, 3, 4, 5]
    table = {p: P.curve(BELADY, sizes, p) for p, _ in POLICIES}
    for p, _ in POLICIES:
        lab.row(f"Belady's string, {p.upper()} faults at 1..5 frames", "  ".join(str(f) for f in table[p]))
    assert (table["fifo"][2], table["fifo"][3]) == (9, 10), "FIFO: 9 faults with 3 frames, 10 with 4"
    assert all(a >= b for a, b in zip(table["lru"], table["lru"][1:])), "LRU has no anomaly"

    # 2. how rare the anomaly is, and that LRU and OPT never show it
    found = P.anomalies(20, 6, 4, random.Random(seed + 6), trials=20000)   # length 20, 6 pages, 4 against 5 frames
    lab.row("random strings where FIFO(5) > FIFO(4)", f"{len(found)} of 20,000   (the film, seed 0: 2)")
    assert all(P.faults(s, 5, "lru") <= P.faults(s, 4, "lru") for s, _, _ in found)
    worse = 0
    for _ in range(1500):
        s = [int(x) for x in rng.integers(0, 6, 20)]
        fifo, lru, opt = (P.curve(s, range(1, 7), p) for p in ("fifo", "lru", "opt"))
        worse += any(b > a for a, b in zip(lru, lru[1:])) or any(b > a for a, b in zip(opt, opt[1:]))
        assert all(o <= min(f, r) for o, f, r in zip(opt, fifo, lru)), "OPT is never beaten"
    lab.row("of 1,500 random strings, LRU or OPT worse with more frames", f"{worse}   (the stack property: 0)")
    assert worse == 0

    # 3. Mattson's one pass against a simulation at every size, on a trace with locality
    trace = locality_trace(rng)
    ks = list(range(1, 25))
    one_pass = P.lru_curve(trace, ks)
    direct = P.curve(trace, ks, "lru")
    lab.row("LRU miss curve, 24 sizes", f"one pass of stack distances = 24 simulations: {one_pass == direct}")
    assert one_pass == direct
    curves = {"fifo": P.curve(trace, ks, "fifo"), "lru": direct, "opt": P.curve(trace, ks, "opt")}
    lab.row("locality trace, faults with 8 frames", "   ".join(f"{p.upper()} {curves[p][7]:,}" for p, _ in POLICIES))
    assert all(o <= min(f, r) for o, f, r in zip(curves["opt"], curves["fifo"], curves["lru"]))

    # 4. Sleator and Tarjan: LRU with k frames against OPT with h, and the cyclic worst case
    cyc = [i % 4 for i in range(120)]
    lab.row("4 pages in a cycle, 3 frames, 120 references", f"LRU {P.faults(cyc, 3, 'lru')}   OPT {P.faults(cyc, 3, 'opt')}"
                                                           "   (the film: 120 and 42)")
    assert P.faults(cyc, 3, "lru") == 120 and P.faults(cyc, 3, "opt") == 42
    for h in (2, 4, 8):
        k = 2 * h
        assert curves["lru"][k - 1] <= k / (k - h + 1) * curves["opt"][h - 1] + h, "the competitive bound"
    lab.note = ("FIFO can fault more with more memory; LRU and OPT cannot, because the pages held with k frames "
                "are always a subset of those held with k + 1, and that same fact gives every LRU size in one pass.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for p, c in POLICIES:
        ax[0].plot(sizes, table[p], "o-", color=c, label=p.upper())
    ax[0].annotate("more memory,\nmore faults", (4, 10), (4.15, 11.2), color=labs.RED, fontsize=9,
                   arrowprops=dict(arrowstyle="->", color=labs.RED))
    ax[0].set(title="Belady's string 1 2 3 4 1 2 5 1 2 3 4 5", xlabel="frames", ylabel="page faults", xticks=sizes,
              ylim=(4, 12.6))
    ax[0].legend()
    for p, c in POLICIES:
        ax[1].plot(ks, curves[p], color=c, label=p.upper())
    ax[1].plot(ks[::2], one_pass[::2], "o", color=labs.GOLD, ms=4, label="LRU from stack distances")
    ax[1].set(title="4,000 references with a moving hot set of 6 pages", xlabel="frames", ylabel="page faults",
              yscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
