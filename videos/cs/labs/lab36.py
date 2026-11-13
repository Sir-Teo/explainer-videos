"""Lab 36: measure ALOHA against G e^(-2G) and G e^(-G), and watch distance vector count to infinity."""

from videos.coursekit import labs

import math
import random

import numpy as np

from explainer.cs.net import mac
from explainer.cs.net import routing

TITLE = "ALOHA's 1/2e and the count to infinity"
GOAL = ("Simulate pure and slotted ALOHA as Poisson processes and compare the throughput with G e^(-2G) and G e^(-G). "
        "Then cut a link under distance-vector routing and count the rounds until the dead route reaches 16, with and "
        "without split horizon, on a line and on a triangle.")
TASKS = [
    "Raise the offered load to G = 3 in both protocols. How many attempts does one delivered frame cost in each?",
    "Run the line with mode='poison' and infinity=64. Which of the two changes the number of rounds, and why?",
    "Make the triangle a square (A-B-C-E-A, with D on C) and cut C-D under split horizon. How long does it count now?",
]

LINE = {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}
TRIANGLE = {"A": {"B": 1, "C": 1}, "B": {"A": 1, "C": 1}, "C": {"A": 1, "B": 1, "D": 1}, "D": {"C": 1}}


def run(seed=0):
    rng = random.Random(seed)
    lab = labs.Lab()
    Gs = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    pure = [mac.aloha(G, 40_000, rng)["S"] for G in Gs]
    slotted = [mac.slotted_aloha(G, 40_000, rng)["S"] for G in Gs]
    for G, s, f in ((0.5, pure[2], 0.5 * math.exp(-1)), (1.0, slotted[4], math.exp(-1))):
        name = "pure ALOHA at G = 0.5" if G == 0.5 else "slotted ALOHA at G = 1"
        lab.row(name, f"measured S = {s:.3f}   formula {f:.3f}")
    for G, p, s in zip(Gs, pure, slotted):
        assert abs(p - G * math.exp(-2 * G)) < 0.012, f"pure ALOHA is on G e^(-2G) at G = {G}"
        assert abs(s - G * math.exp(-G)) < 0.012, f"slotted ALOHA is on G e^(-G) at G = {G}"
    assert max(pure) < 0.2 and max(slotted) < 0.385, "no load beats 1/2e or 1/e"
    assert pure[-1] < 0.02, "at G = 3 the pure channel carries almost nothing: more load, less throughput"

    # distance vector: converge, cut a link, run again, and follow the dead destination's distance
    runs = {}
    for name, net, cut, dest in (("line A-B-C, cut B-C", LINE, ("B", "C"), "C"),
                                      ("triangle with D on C, cut C-D", TRIANGLE, ("C", "D"), "D")):
        for mode in ("plain", "split"):
            after = routing.dv_fail(net, *cut, mode=mode)["after"]
            dist = [min(t[x][dest][0] for x in t if x != dest) for t in after["history"]]  # the best rumour left
            runs[name, mode] = (after["converged"], dist)
            lab.row(f"{name}, {mode}", f"{after['converged']} rounds; shortest believed distance: {' '.join(map(str, dist[:7]))} ...")
            assert dist[-1] == 16, "the dead destination ends at infinity (16)"
    line, tri = "line A-B-C, cut B-C", "triangle with D on C, cut C-D"
    assert runs[line, "plain"][0] == 15, "the film: 15 rounds to count to 16 on the line"
    assert runs[line, "split"][0] <= 2, "split horizon ends a two-node loop at once"
    assert runs[tri, "split"][0] == 15, "but the triangle still counts for 15 rounds"
    steps = np.diff([d for d in runs[tri, "split"][1] if d < 16])
    assert set(steps[1:]) == {1}, "around the triangle the rumour grows by one hop per round"
    lab.note = ("Throughput follows G e^(-2G) and G e^(-G), so offering more than G = 1/2 (or 1) delivers less; and a "
                "distance vector forgets a dead route only by counting up to 16, which split horizon cures for two "
                "routers but not for three.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    g = np.linspace(0.01, 3.2, 200)
    ax[0].plot(g, g * np.exp(-2 * g), color=labs.RED, label="G e^(-2G): pure")
    ax[0].plot(g, g * np.exp(-g), color=labs.BLUE, label="G e^(-G): slotted")
    ax[0].scatter(Gs, pure, color=labs.RED, s=28, zorder=3, label="pure, simulated")
    ax[0].scatter(Gs, slotted, color=labs.BLUE, s=28, zorder=3, label="slotted, simulated")
    ax[0].axhline(1 / (2 * math.e), color=labs.MUTED, ls="--", lw=1)
    ax[0].text(3.2, 1 / (2 * math.e) + 0.008, "1/2e", color=labs.MUTED, ha="right")
    ax[0].set(title="ALOHA: throughput against offered load", xlabel="offered load G (attempts per frame time)",
              ylabel="throughput S (frames per frame time)", ylim=(0, 0.45))
    ax[0].legend(loc="upper right")
    styles = {(line, "plain"): (labs.RED, "-", 3.2, "line, plain"),
              (tri, "split"): (labs.GOLD, "--", 1.6, "triangle, split horizon (the same climb)"),
              (line, "split"): (labs.GREEN, "-", 1.8, "line, split horizon")}
    for key, (color, ls, lw, name) in styles.items():
        d = runs[key][1]
        ax[1].step(range(len(d)), d, where="post", color=color, ls=ls, lw=lw, label=name)
    ax[1].axhline(16, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(0.2, 16.4, "infinity = 16", color=labs.MUTED)
    ax[1].set(title="After the cut: the best distance still believed", xlabel="round", ylabel="distance to the dead destination",
              ylim=(0, 18.5))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
