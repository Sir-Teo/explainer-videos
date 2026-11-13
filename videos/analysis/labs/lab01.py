"""Lab 1: play the open-cover game on [0, 1], where it is won, and on (0, 1], where it is lost."""

from fractions import Fraction
from math import floor, log

import numpy as np

from videos.coursekit import labs

TITLE = "Heine-Borel as a game: finite subcovers, and the cover that has none"
GOAL = ("Draw a random open cover of [0, 1] and extract a finite subcover by a greedy walk; then cover (0, 1] by the "
        "intervals (x/3, 3x) and count how many are needed for [a, 1] as a shrinks to 0.")
TASKS = [
    "Change the family (x/3, 3x) to (x/k, kx) for k = 1.1 and k = 10. How does the count for a = 1e-6 change, and why is it never bounded?",
    "Add the single interval (-0.01, 0.01) to the family covering (0, 1]. Show that the count for [0, 1] is now finite, and find it.",
    "Replace Rudin's hop by Newton's step p -> p/2 + 1/p and compare how fast the two close in on the hole at the square root of 2.",
]


def greedy(intervals, lo, hi):
    """The fewest open intervals of the list whose union contains [lo, hi], by the walk from the left: among the
    intervals containing the first uncovered point, take the one reaching furthest right.  None if a point is missed."""
    chosen, t = [], lo
    while True:
        reach = [(b, a) for a, b in intervals if a < t < b]
        if not reach:
            return None
        b, a = max(reach)
        chosen.append((a, b))
        if b > hi:
            return chosen
        t = b  # b itself is not covered by (a, b): the next interval must contain it


def brute_minimum(intervals, lo, hi, grid, limit=4):
    """The smallest subcover of [lo, hi] with at most ``limit`` intervals, by trying every subset (or None)."""
    from itertools import combinations

    inside = [(grid > a) & (grid < b) for a, b in intervals]
    for k in range(1, limit + 1):
        for combo in combinations(range(len(intervals)), k):
            if np.all(np.any([inside[i] for i in combo], axis=0)):
                return k
    return None


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Rudin's hop: the set {p in Q : p^2 < 2} has no largest element (exact fractions).
    p, ups = Fraction(1), [Fraction(1)]
    for _ in range(8):
        q = (2 * p + 2) / (p + 2)
        assert p < q and q * q < 2 and q * q - 2 == 2 * (p * p - 2) / (p + 2) ** 2, "the hop stays below and climbs"
        p = q
        ups.append(q)
    lab.row("Rudin's hop from 1, eight steps", f"{ups[4]} -> ... -> {ups[-1]}   (2 - p^2 = {float(2 - p * p):.2e})")

    # 2. A random open cover of [0, 1]: a finite subcover exists and the greedy walk finds a smallest one.
    n_cover = 70
    centers = np.concatenate([np.linspace(0, 1, 12), rng.uniform(0, 1, n_cover - 12)])
    radii = np.concatenate([np.full(12, 0.05), rng.uniform(0.01, 0.09, n_cover - 12)])
    cover = [(c - r, c + r) for c, r in zip(centers, radii)]
    sub = greedy(cover, 0.0, 1.0)
    grid = np.linspace(0, 1, 100_001)
    covered = np.zeros(grid.size, bool)
    for a, b in sub or []:
        covered |= (grid > a) & (grid < b)
    assert sub is not None and covered.all(), "the finite subcover covers a 100,001-point grid of [0, 1]"
    small = [(c - r, c + r) for c, r in zip(np.concatenate([[0.0, 1.0], rng.uniform(0, 1, 16)]),
                                            rng.uniform(0.12, 0.3, 18))]
    walk = greedy(small, 0.0, 1.0)
    best = brute_minimum(small, 0.0, 1.0, np.linspace(0, 1, 2001), limit=len(walk) if walk else 0)
    assert walk is not None and best == len(walk), "the greedy walk is a smallest subcover (checked by brute force)"
    lab.row("random cover of [0, 1]", f"{n_cover} open intervals; greedy finite subcover uses {len(sub)}")
    lab.row("greedy against every subset (18 wide intervals)", f"greedy {len(walk)}, smallest possible {best}")

    # 3. The cover {(x/3, 3x) : 0 < x <= 1} of (0, 1]: [a, 1] needs more and more intervals as a -> 0.
    k = 3.0
    family = [(x / k, k * x) for x in np.geomspace(1e-8, 1, 3201)]  # a fine sample of the family
    lefts = [10.0 ** -e for e in range(1, 7)]
    counts, theory = [], []
    for a in lefts:
        counts.append(len(greedy(family, a, 1.0)))
        # each interval spans a factor k^2 and open intervals must overlap, so N intervals reach down only to left
        # ends above k^(-2N): N is the least integer greater than ln(1/a) / ln(k^2)
        theory.append(floor(log(1 / a) / log(k * k)) + 1)
    for a, c, t in zip(lefts, counts, theory):
        lab.row(f"(0, 1] cover: intervals needed for [{a:g}, 1]", f"{c}   (theory {t})")
    assert all(t <= c <= t + 1 for c, t in zip(counts, theory)), "the count matches the logarithmic law"
    assert all(c2 > c1 for c1, c2 in zip(counts, counts[1:])), "the count grows without bound as a -> 0"
    assert greedy(family, 0.0, 1.0) is None, "no interval of the family contains 0: [0, 1] is not even covered"
    fine = np.geomspace(1e-7, 1e-1, 25)
    slope = np.polyfit(np.log(1 / fine), [len(greedy(family, a, 1.0)) for a in fine], 1)[0]
    lab.row("growth per factor e in 1/a", f"{slope:.3f}   (theory 1/ln 9 = {1 / log(9):.3f})")
    assert abs(slope - 1 / log(9)) < 0.05
    lab.note = ("On the closed interval a finite subcover always exists; on (0, 1] the same game needs about "
                "ln(1/a)/ln 9 intervals to reach a, so no finite number reaches 0: closedness is what is used.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for i, (a, b) in enumerate(cover):
        ax[0].plot([a, b], [i % 14 + 2, i % 14 + 2], color=labs.BLUE, lw=1.2, alpha=0.55)
    for i, (a, b) in enumerate(sub):
        ax[0].plot([a, b], [-1 - i % 2, -1 - i % 2], color=labs.GOLD, lw=3)
    ax[0].plot([0, 1], [0.5, 0.5], color=labs.INK, lw=2.5)
    ax[0].plot([], [], color=labs.BLUE, label=f"the cover: {n_cover} open intervals")
    ax[0].plot([], [], color=labs.GOLD, lw=3, label=f"a finite subcover: {len(sub)}")
    ax[0].plot([], [], color=labs.INK, lw=2.5, label="[0, 1]")
    ax[0].set(title="[0, 1]: the game is won", xlabel="x", yticks=[], ylim=(-3, 21))
    ax[0].legend(loc="upper right", ncols=1)
    aa = np.geomspace(1e-6, 0.5, 200)
    ax[1].step(aa, [floor(log(1 / a) / log(k * k)) + 1 for a in aa], color=labs.MUTED, where="mid",
               label="theory: least N > ln(1/a) / ln 9")
    ax[1].scatter(lefts, counts, color=labs.GOLD, zorder=3, label="greedy count for [a, 1]")
    ax[1].set(xscale="log", title="(0, 1] covered by (x/3, 3x): the count has no bound", xlabel="left end a",
              ylabel="intervals needed")
    ax[1].legend()
    lab.fig = fig
    return lab
