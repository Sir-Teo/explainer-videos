"""Lab 2: search every position of the 3 x 3 sliding puzzle and check the invariant; then count hats that come home."""

from collections import deque
from math import factorial

import numpy as np

from videos.coursekit import labs

TITLE = "An invariant against a search, and one fixed point on average"
GOAL = ("Breadth-first search from the solved 2 x 3 and 3 x 3 sliding puzzles, and compare the positions reached "
        "with the positions the parity invariant allows. Then shuffle n hats many times and compare the number "
        "that return to their owners with the derangement count and with linearity of expectation.")
TASKS = [
    "Start the search from the solved board with tiles 7 and 8 swapped. Which positions does it reach, and what is their invariant?",
    "Drop the blank's distance from the invariant and use the permutation's parity alone. Find a single move that changes it.",
    "Change hats to n = 3 and then n = 50. Which of the two results (mean 1, P(none) near 1/e) depends on n?",
]


def moves(rows, cols):
    """For each square the blank can be on, the squares it can swap with."""
    out = []
    for z in range(rows * cols):
        r, c = divmod(z, cols)
        out.append([rr * cols + cc for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                    if 0 <= rr < rows and 0 <= cc < cols])
    return out


def invariant(board, rows, cols):
    """The parity of the permutation of all squares (the blank counts as the last tile) plus the blank's taxicab
    distance from its home corner: every slide is one swap and moves the blank one square, so it never changes."""
    n = rows * cols
    perm = [(v - 1) % n for v in board]
    seen, cycles = [False] * n, 0
    for i in range(n):
        if not seen[i]:
            cycles += 1
            while not seen[i]:
                seen[i] = True
                i = perm[i]
    r, c = divmod(board.index(0), cols)
    return (n - cycles + (rows - 1 - r) + (cols - 1 - c)) % 2


def bfs(rows, cols):
    """Distances from the solved board to every position that slides can reach.  A board is a bytes object."""
    start = bytes(list(range(1, rows * cols)) + [0])
    table = moves(rows, cols)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        b = queue.popleft()
        z = b.index(0)
        d = dist[b] + 1
        for t in table[z]:
            nb = bytearray(b)
            nb[z], nb[t] = nb[t], 0
            nb = bytes(nb)
            if nb not in dist:
                dist[nb] = d
                queue.append(nb)
    return dist


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the search against the invariant
    for rows, cols in ((2, 3), (3, 3)):
        dist = bfs(rows, cols)
        total = factorial(rows * cols)
        lab.row(f"{rows} x {cols} puzzle: positions reached", f"{len(dist):,} of {total:,}   (half: {total // 2:,})")
        assert len(dist) == total // 2
        boards = list(dist)
        sample = boards if total < 1000 else [boards[i] for i in rng.choice(len(boards), 20_000, replace=False)]
        assert all(invariant(b, rows, cols) == 0 for b in sample), "every reached position keeps the invariant"
    depth = np.bincount(list(dist.values()))
    lab.row("3 x 3: hardest positions", f"{len(depth) - 1} moves, {depth[-1]} of them   (the film: 31 moves)")
    assert len(depth) - 1 == 31
    swapped = bytes((1, 2, 3, 4, 5, 6, 8, 7, 0))
    lab.row("3 x 3 with 7 and 8 swapped", f"invariant {invariant(swapped, 3, 3)}, reached: {swapped in dist}")
    assert invariant(swapped, 3, 3) == 1 and swapped not in dist
    # (the 2 x 3 boards are all checked; of the 3 x 3 boards, a random 20,000)

    # 2. the hat check: n hats handed back at random
    n, trials = 10, 40_000
    perms = np.argsort(rng.random((trials, n)), axis=1)
    fixed = (perms == np.arange(n)).sum(axis=1)
    d = [1, 0]
    for k in range(2, n + 1):
        d.append((k - 1) * (d[-1] + d[-2]))  # derangements: D(k) = (k - 1)(D(k-1) + D(k-2))
    p0 = d[n] / factorial(n)
    lab.row(f"{n} hats: mean number returned", f"{fixed.mean():.3f}   (linearity of expectation: 1)")
    lab.row(f"{n} hats: P(nobody gets their own)", f"{(fixed == 0).mean():.4f}   (D({n})/{n}! = {p0:.4f}, 1/e = {np.exp(-1):.4f})")
    assert abs(fixed.mean() - 1) < 0.03 and abs((fixed == 0).mean() - p0) < 0.012
    assert abs(p0 - np.exp(-1)) < 1e-6
    lab.note = ("The search reaches exactly the half of the positions that the invariant allows, so the invariant "
                "is the whole story; and a random hand-back returns one hat on average whatever n is.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].bar(np.arange(len(depth)), depth, color=labs.BLUE, width=0.85)
    ax[0].set(title="3 x 3 puzzle: positions at each distance from solved", xlabel="moves", ylabel="positions")
    ks = np.arange(0, 7)
    ax[1].bar(ks - 0.2, [(fixed == k).mean() for k in ks], width=0.4, color=labs.BLUE, label=f"{trials:,} shuffles of {n} hats")
    ax[1].bar(ks + 0.2, [np.exp(-1) / factorial(int(k)) for k in ks], width=0.4, color=labs.GOLD, label="Poisson(1)")
    ax[1].set(title="Hats returned to their owners", xlabel="number of fixed points", ylabel="probability")
    ax[1].legend()
    ax[0].set_axisbelow(True)
    ax[1].set_axisbelow(True)
    lab.fig = fig
    return lab
