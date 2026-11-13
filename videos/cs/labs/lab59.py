"""Lab 59: 3-colour rings of up to a million nodes, run the hexagon against a protocol, and count Sperner's triangles."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.disttheory import theory

TITLE = "Locality, a liar and a lemma"
GOAL = ("Run Cole and Vishkin's colouring on oriented rings of ten to a million nodes and compare the rounds with "
        "log* n and the colours with the bound the bit trick allows; run the hexagon argument against a three-process "
        "majority protocol; and check Sperner's lemma on 200 random colourings.")
TASKS = [
    "Give every node the same identifier before the first round (c[:] = 7 in cole_vishkin). Which line fails, and "
    "what does that say about anonymous rings?",
    "Change _protocol to decide the minimum of what a process heard instead of the majority, and rerun hexagon(). "
    "Which pairs break now, and why must some pair always break?",
    "In sperner(), let the vertices on the side between corners 0 and 1 take colour 2 as well. Find a colouring with "
    "an even number of rainbow triangles.",
]


def run(seed=0):
    lab = labs.Lab()

    # 1. Cole-Vishkin: proper, about log* n rounds, colours within the bound b bits -> 2 b colours
    ns = (10, 100, 1000, 10_000, 100_000, 1_000_000)
    runs = [theory.cole_vishkin(n, seed=seed) for n in ns]
    for r in runs:
        assert r["proper"], "three colours, different on every edge"
        assert r["rounds"] <= r["log_star"] + 3, "log* n plus two or three rounds"
        assert r["rounds"] >= 0.5 * r["log_star"] - 1, "Linial: no algorithm does better"
    lab.row("ring size n", "  ".join(f"{n:,}" for n in ns))
    lab.row("rounds used", "  ".join(str(r["rounds"]) for r in runs))
    lab.row("log* n", "  ".join(str(r["log_star"]) for r in runs))
    big = runs[-1]
    bits = math.ceil(math.log2(ns[-1] + 2 ** 20))  # identifiers lie below n + 2^20
    bound, colours = [], big["colours"]
    for used in colours[1:-3]:  # the bit-position rounds: b-bit colours become colours below 2 b
        bound.append(2 * bits)
        assert used <= bound[-1], "a b-bit colour becomes a pair (bit position, bit): at most 2 b of them"
        bits = math.ceil(math.log2(2 * bits))
    assert colours[-3:] == [5, 4, 3], "the clean-up removes colours 5, 4 and 3"
    lab.row("colours after each round, n = 1,000,000", "  ".join(f"{c:,}" for c in colours[1:]))
    lab.row("the bound 2b for those rounds", "  ".join(str(b) for b in bound) + "  5  4  3")

    # 2. the hexagon: a three-process protocol cannot survive one liar
    hx = theory.hexagon()
    broken = sorted(tuple(p["pair"]) for p in hx["violations"])
    lab.row("hexagon: decisions of A0 B0 C0 A1 B1 C1", " ".join(str(hx["decisions"][k]) for k in hx["names"]))
    lab.row("pairs that break agreement or validity", ", ".join(f"{a}-{b}" for a, b in broken) + "   (theory: at least one)")
    assert len(broken) >= 1, "n = 3, f = 1: some adjacent pair must fail"
    assert all(p["byzantine"] == "B" for p in hx["violations"]) and broken == [("C0", "A1"), ("C1", "A0")]

    # 3. Sperner's lemma: the number of rainbow triangles is odd
    counts = np.array([theory.sperner(k=10, seed=1000 * seed + s)["count"] for s in range(200)])
    lab.row("rainbow triangles in 200 random colourings", f"{counts.min()} to {counts.max()}, odd in "
                                                           f"{int((counts % 2 == 1).sum())} of 200   (theory: all)")
    assert np.all(counts % 2 == 1), "Sperner: an odd number, so at least one"

    # 4. exact majority by four states: #A - #B never changes, so the majority wins
    maj = theory.majority(n=100, margin=4, trials=10, seed=seed)
    strong = [h["A"] - h["B"] for h in maj["trace"]]
    lab.row("exact majority, 52 against 48", f"correct in {maj['correct']:.0%} of 10 runs, mean parallel time "
                                              f"{maj['parallel_time_mean']:.0f}")
    assert maj["correct"] == 1.0 and set(strong) == {4}, "the strong margin is invariant"
    lab.note = ("A ring of a million nodes is 3-coloured in 7 rounds because each round replaces a colour by the "
                "position of one bit; the hexagon and Sperner's lemma are the counting arguments behind two "
                "impossibility theorems, and here they are run.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    rounds = np.arange(len(colours))
    ax[0].plot(rounds, colours, "o-", color=labs.BLUE, label="colours in use, n = 1,000,000")
    ax[0].plot(rounds[1:], bound + [5, 4, 3], "--", color=labs.MUTED, label="allowed: 2b, then 5, 4, 3")
    ax[0].axhline(3, color=labs.GREEN, lw=1, label="three colours")
    ax[0].set(yscale="log", xlabel="round", ylabel="colours", title="Cole-Vishkin: a million colours to three")
    ax[0].legend()
    values = np.arange(counts.min() - 1, counts.max() + 2)
    ax[1].bar(values, [(counts == v).sum() for v in values],
              color=[labs.GOLD if v % 2 else labs.RED for v in values], width=0.8)
    ax[1].set(xlabel="rainbow triangles among the 100 small ones", ylabel="colourings of 200",
              title="Sperner's lemma: the count is always odd")
    ax[1].set_axisbelow(True)
    ax[1].text(0.98, 0.94, "even counts: none", transform=ax[1].transAxes, ha="right", va="top", color=labs.MUTED)
    lab.fig = fig
    return lab
