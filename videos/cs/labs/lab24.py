"""Lab 24: count the cells that prefix sums, Fenwick trees, segment trees and square-root blocks touch."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.algo import practice as pr

TITLE = "What a range structure touches"
GOAL = ("Drive a Fenwick tree, a segment tree and square-root blocks with the same random updates and range sums, "
        "check every answer against a plain array, and count the cells each one touches against popcount, 2 lg n and "
        "3 sqrt(n); then check three linear-time or counting claims of the part by brute force.")
TASKS = [
    "Replace the segment tree's sum by min (op=min, ident=float('inf')) and check range minima against numpy. Why can the Fenwick tree not do the same?",
    "Time the Fenwick loop against the plain array's a[l:r + 1].sum() at n = 2**16 with time.perf_counter. At which n does the count of cells stop predicting the time?",
    "Change sliding_max's window from 50 to 5,000 and print the pops per element. Why does the amortized count not grow with the window?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the same trace of updates and range sums on three structures, checked against a plain array
    sizes = [2 ** k for k in range(4, 15, 2)]
    per_op = {"plain array": [], "Fenwick tree": [], "segment tree": [], "sqrt blocks": []}
    for n in sizes:
        a = rng.integers(-50, 51, n).astype(np.int64)
        fen, seg, blocks = pr.Fenwick(n), pr.SegTree(a.tolist()), pr.SqrtDecomp(a.tolist())
        for i, v in enumerate(a.tolist()):
            fen.add(i + 1, v)
        fen.touched, ops, scanned = 0, 300, 0
        for _ in range(ops):
            i, v = int(rng.integers(n)), int(rng.integers(-50, 51))
            a[i] += v
            path = fen.add(i + 1, v)
            seg.update(i, int(a[i]))
            blocks.update(i, int(a[i]))
            assert len(path) <= n.bit_length(), "an update climbs at most floor(lg n) + 1 cells"
            lo, hi = sorted(int(x) for x in rng.integers(0, n, 2))
            truth = int(a[lo:hi + 1].sum())
            scanned += hi - lo + 1
            cover = []
            assert fen.range(lo + 1, hi + 1) == truth and seg.query(lo, hi, cover) == truth and blocks.query(lo, hi) == truth
            assert len(cover) <= 2 * n.bit_length(), "at most two covering nodes per level"
            fen.prefix(hi + 1)
            assert len(fen.last_path) == pr.popcount(hi + 1), "a prefix query reads popcount(i) cells"
        per_op["plain array"].append((scanned + ops) / (2 * ops))
        per_op["Fenwick tree"].append(fen.touched / (4 * ops))  # one add and three prefix calls per round
        per_op["segment tree"].append(seg.visits / (2 * ops))
        per_op["sqrt blocks"].append((blocks.touched + ops) / (2 * ops))
        assert blocks.touched / ops <= 3 * np.sqrt(n), "a block query touches at most about 3 sqrt(n) cells"
    n = sizes[-1]
    lab.row(f"n = {n:,}: cells per operation", "   ".join(f"{k} {v[-1]:,.1f}" for k, v in per_op.items()))
    lab.row("bounds at that n", f"lg n + 1 = {n.bit_length()}   sqrt(n) = {int(np.sqrt(n))}   mean range length about n / 3 = {n // 3:,}")
    assert per_op["Fenwick tree"][-1] < per_op["segment tree"][-1] < per_op["sqrt blocks"][-1] < per_op["plain array"][-1] / 10

    # 2. the sliding-window maximum: right, and linear
    x = rng.integers(0, 1000, 20_000).tolist()
    out, _, pops = pr.sliding_max(x, 50, trace=True)
    assert out == np.lib.stride_tricks.sliding_window_view(np.array(x), 50).max(axis=1).tolist()
    assert pops <= len(x), "each index leaves the deque at most once"
    lab.row("sliding maximum, 20,000 values, window 50", f"{pops:,} deque removals   (at most n; checking every window: {50 * (len(x) - 49):,})")

    # 3. submasks: exactly 3^n loop iterations over all masks of n elements
    total = sum(sum(1 for _ in pr.submasks(m)) for m in range(1 << 9))
    assert total == 3 ** 9
    lab.row("submasks of all 9-bit masks", f"{total:,} = 3^9   (not 4^9 = {4 ** 9:,})")

    # 4. meet in the middle against brute force
    items = [int(v) for v in rng.integers(1, 10 ** 6, 18)]
    hit = sum(v for v, keep in zip(items, rng.random(18) < 0.5) if keep)
    for target in (hit, hit + 1, sum(items) + 1):
        (f1, w1), (f2, w2) = pr.subset_sum_mitm(items, target), pr.subset_sum_brute(items, target)
        assert f1 == f2, "the same answer as trying every subset"
    assert f1 is False and w1 <= 3 * 2 ** 9 and w2 == 2 ** 18
    lab.row("subset sum, 18 items", f"meet in the middle {w1:,} sums and searches, brute force {w2:,} subsets")
    lab.note = ("The counts follow the structure: a Fenwick query reads one cell per set bit of its index, a segment "
                "tree visits a few nodes per level, blocks cost a square root. They are counts of cells, not nanoseconds; the "
                "film's second half measures what the machine adds.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for (name, v), color in zip(per_op.items(), (labs.RED, labs.GREEN, labs.BLUE, labs.GOLD)):
        ax[0].loglog(sizes, v, "o-", color=color, label=name)
    ax[0].set(title="Cells touched per operation (updates and range sums)", xlabel="array length n", ylabel="cells")
    ax[0].legend()
    idx = np.arange(1, 65)
    ax[1].bar(idx, [pr.popcount(int(i)) for i in idx], color=labs.GREEN, width=0.8, label="prefix query: popcount(i)")
    ax[1].step(idx, [len(pr.Fenwick(64).add(int(i), 1)) for i in idx], where="mid", color=labs.GOLD, label="update: cells above i")
    ax[1].axhline(7, color=labs.MUTED, ls="--", label="lg n + 1 = 7")
    ax[1].set(title="A Fenwick tree on 64 cells: work at each index", xlabel="index i", ylabel="cells touched", ylim=(0, 9.5))
    ax[1].legend(ncols=3, loc="upper center", fontsize=8)
    lab.fig = fig
    return lab
