"""Lab 9: replay three loop orders of a matrix multiply through Pebble's cache model, LRU against the optimal policy."""

from videos.coursekit import labs

import math

import numpy as np

from explainer.cs.pebble.cache import SetAssoc, belady, miss_curve, stack_distances

TITLE = "Loop order, stack distance and the scan that defeats LRU"
GOAL = ("Write down the address trace of an n x n matrix multiply in three loop orders, and check Mattson's rule on "
        "each: a fully associative LRU cache of C lines hits exactly the references whose stack distance is below C. "
        "Then run a cyclic scan of C + 1 lines, where LRU misses every reference and Belady's MIN misses one in C.")
TASKS = [
    "Make the cache 2-way (SetAssoc(cap * 64, ways=2)) and count the misses of each order again. Which order suffers from conflicts?",
    "Change the tile from 8 to 4 and to 16. At which cache capacity does each tile size stop missing?",
    "Scan C + 2 and 2C lines cyclically instead of C + 1. How do the LRU and MIN miss fractions change?",
]


def matmul_lines(n, order, tile=8):
    """Line numbers (64-byte lines, 8-byte doubles, row-major) touched by C[i][j] += A[i][k] * B[k][j]."""
    if order == "tiled":
        idx = [(i, j, k) for i0 in range(0, n, tile) for k0 in range(0, n, tile) for j0 in range(0, n, tile)
               for i in range(i0, min(i0 + tile, n)) for k in range(k0, min(k0 + tile, n))
               for j in range(j0, min(j0 + tile, n))]
        i, j, k = np.array(idx).T
    else:
        a, b, c = (g.ravel() for g in np.meshgrid(*[np.arange(n)] * 3, indexing="ij"))
        i, j, k = (a, b, c) if order == "ijk" else (a, c, b)  # ikj: the innermost loop walks a row of B and of C
    base = n * n * 8
    addr = np.stack([(i * n + k) * 8, base + (k * n + j) * 8, 2 * base + (i * n + j) * 8], axis=1).ravel()
    return addr // 64


def lru_misses(lines, capacity):
    cache = SetAssoc(capacity * 64, line=64, ways=capacity)  # one set: fully associative, LRU
    for ln in lines:
        cache.access(int(ln) * 64)
    return cache.misses


def run(seed=0):
    rng = np.random.default_rng(seed)
    n = int(rng.choice([16, 18, 20]))
    lab = labs.Lab()
    dist, miss = {}, {}
    for order in ("ijk", "ikj", "tiled"):
        lines = matmul_lines(n, order)
        d = dist[order] = stack_distances(lines)
        for cap in (8, 32):
            miss[order, cap] = lru_misses(lines, cap)
            assert miss[order, cap] == int(((d < 0) | (d >= cap)).sum()), "LRU hits exactly the stack distances below C"
        opt, first = belady(lines, 32), int((d < 0).sum())
        lab.row(f"n = {n}, {order}: LRU misses of {len(lines):,} references",
                f"{miss[order, 8]:,} in 8 lines   {miss[order, 32]:,} in 32 lines   (MIN in 32: {opt:,}; first touches {first})")
        assert first <= opt <= miss[order, 32], "no policy beats MIN, and nothing avoids the first touches"
    assert miss["ikj", 8] < 0.5 * miss["ijk", 8], "in a small cache, walking B by columns misses far more than by rows"
    assert miss["tiled", 32] < min(miss["ijk", 32], miss["ikj", 32]), "three 8 x 8 tiles fit in 32 lines"

    C = int(rng.choice([8, 12, 16]))
    R = 12 * (C + 1)
    scan = np.arange(R) % (C + 1)
    lru, opt = lru_misses(scan, C), belady(scan, C)
    formula = C + math.ceil((R - C) / C)
    lab.row(f"cyclic scan of {C + 1} lines, cache of {C}: LRU", f"{lru} misses of {R} references")
    lab.row(f"cyclic scan of {C + 1} lines, cache of {C}: MIN", f"{opt} misses   (C + ceil((R - C)/C) = {formula})")
    assert lru == R and opt == formula
    lab.note = ("The same multiplications in a different order touch the same lines at different stack distances, so "
                "each order has its own miss curve and none wins at every capacity; a scan one line longer than the "
                "cache is LRU's worst case and nearly free for MIN.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    fine = [2 ** e for e in range(1, 11)]
    for order, color in (("ijk", labs.RED), ("ikj", labs.BLUE), ("tiled", labs.GREEN)):
        ax[0].plot(fine, miss_curve(dist[order], fine), "o-", color=color, ms=4, label=order)
    ax[0].set(xscale="log", title=f"{n} x {n} multiply: LRU miss ratio by loop order", xlabel="cache capacity (lines of 64 bytes)",
              ylabel="misses per reference")
    ax[0].legend()
    for policy, color, name in ((None, labs.RED, "LRU"), ("min", labs.GREEN, "MIN")):
        cum = [lru_misses(scan[:t], C) if policy is None else belady(scan[:t], C) for t in range(0, R + 1, C + 1)]
        ax[1].plot(range(0, R + 1, C + 1), cum, "o-", color=color, ms=4, label=name)
    ax[1].plot([0, R], [0, R], ls=":", color=labs.MUTED, label="every reference misses")
    ax[1].set(title=f"Cyclic scan of {C + 1} lines in a cache of {C}", xlabel="references", ylabel="misses so far")
    ax[1].legend()
    lab.fig = fig
    return lab
