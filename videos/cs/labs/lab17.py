"""Lab 17: fill hash tables to nine loads and count probes against Knuth's formulas; grow random search trees."""

from videos.coursekit import labs
import math
import random

import numpy as np

from explainer.cs.algo import ds, sorts

TITLE = "Probes against load, and the depth of a random search tree"
GOAL = ("With the series' instrumented tables, fill linear-probing and double-hashing tables step by step and "
        "count the probes of hits and misses at each load against Knuth's formulas; then build random binary "
        "search trees and compare their mean depth with 2(1 + 1/n)H_n - 4, their comparisons with quicksort's, "
        "and their height on sorted input with an AVL tree's.")
TASKS = [
    "Replace ds.LinearProbing by ds.RobinHood and compare the mean and the largest probe count of a hit at load 0.9. Which one changes?",
    "Hash with k % 1024 instead of k % M into the same table (all homes in the first quarter). What happens to misses at load 0.2?",
    "Insert the sorted keys into ds.Treap and ds.LLRB as well. How do their heights compare with the AVL bound 1.4405 lg(n + 2)?",
]
M, TABLES, PROBES = 4096, 6, 1500
LOADS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


def harmonic(n):
    return sum(1 / k for k in range(1, n + 1))


def run(seed=0):
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)
    lab = labs.Lab()

    # 1. open addressing: the same keys into a linear-probing and a double-hashing table
    miss = {"linear": np.zeros(len(LOADS)), "double": np.zeros(len(LOADS))}
    hit = np.zeros(len(LOADS))
    longest = 0
    for _ in range(TABLES):
        keys = [int(k) for k in rng.integers(0, 1 << 40, int(LOADS[-1] * M))]
        lin = ds.LinearProbing(M, lambda k: k % M)
        dbl = ds.DoubleHashing(M, lambda k: k % M, lambda k: k // M)
        done = 0
        for j, load in enumerate(LOADS):
            while done < int(load * M):
                lin.insert(keys[done])
                dbl.insert(keys[done])
                done += 1
            fresh = [int(k) for k in rng.integers(0, 1 << 40, PROBES)]
            miss["linear"][j] += np.mean([lin.find(k) for k in fresh]) / TABLES
            miss["double"][j] += np.mean([dbl.find(k) for k in fresh]) / TABLES
            hit[j] += np.mean([lin.find(k) for k in keys[:done]]) / TABLES
        longest = max(longest, max(lin.clusters()))
    a = np.array(LOADS)
    knuth_miss, knuth_hit, uniform = 0.5 * (1 + 1 / (1 - a) ** 2), 0.5 * (1 + 1 / (1 - a)), 1 / (1 - a)
    for j in (4, 6, 8):
        lab.row(f"load {LOADS[j]}: probes for a miss, linear probing", f"{miss['linear'][j]:.2f}   (Knuth {knuth_miss[j]:.2f})")
        lab.row(f"load {LOADS[j]}: probes for a miss, double hashing", f"{miss['double'][j]:.2f}   (1/(1 - a) = {uniform[j]:.2f})")
        lab.row(f"load {LOADS[j]}: probes for a hit, linear probing", f"{hit[j]:.2f}   (Knuth {knuth_hit[j]:.2f})")
    lab.row("longest cluster at load 0.9", f"{longest} of {M} slots")
    assert np.all(np.abs(miss["linear"][:7] / knuth_miss[:7] - 1) < 0.12), "misses should follow (1 + 1/(1 - a)^2)/2"
    assert np.all(np.abs(hit[:7] / knuth_hit[:7] - 1) < 0.08), "hits should follow (1 + 1/(1 - a))/2"
    assert np.all(np.abs(miss["double"][:8] / uniform[:8] - 1) < 0.08), "double hashing should behave like uniform probing"
    assert np.all(miss["linear"][5:] > 1.2 * miss["double"][5:]), "clustering should cost linear probing extra"

    # 2. binary search trees
    n, trees = 2000, 20
    depth = []
    for _ in range(trees):
        xs = [pyrng.random() for _ in range(n)]
        t = ds.BST()
        for x in xs:
            t.insert(x)
        depth.append(np.mean(t.depths()))
        assert t.cmp == sorts.quicksort(xs, "first")[1]["cmp"], "a BST's insertions are quicksort's comparisons"
    theory = 2 * (1 + 1 / n) * harmonic(n) - 4
    chain, avl = ds.BST(), ds.AVL()
    for x in range(500):
        chain.insert(x)
    for x in range(n):
        avl.insert(x)
    lab.row(f"random BST, {n:,} keys: mean depth", f"{np.mean(depth):.2f}   (2(1 + 1/n)H_n - 4 = {theory:.2f})")
    lab.row("comparisons to build it", f"{t.cmp:,}, the same as quicksort with the first key as pivot")
    lab.row("height on sorted input", f"plain BST {chain.height()} levels for 500 keys; AVL {avl.height()} levels for "
                                      f"{n:,}   (bound {1.4405 * math.log2(n + 2):.1f})")
    assert abs(np.mean(depth) / theory - 1) < 0.06, "random BST depth should be about 2 ln n"
    assert chain.height() == 500 and avl.height() < 1.4405 * math.log2(n + 2)
    lab.note = ("Open addressing is constant-time only while the table has room: at load a a miss costs about "
                "(1 + 1/(1 - a)^2)/2 probes under linear probing and 1/(1 - a) without clustering; a search tree's "
                "depth is logarithmic on random input, and balancing makes it so on every input.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    grid = np.linspace(0.05, 0.92, 100)
    ax[0].plot(grid, 0.5 * (1 + 1 / (1 - grid) ** 2), color=labs.GOLD, label="Knuth: (1 + 1/(1 - a)²)/2")
    ax[0].plot(grid, 1 / (1 - grid), color=labs.GREY, ls="--", label="uniform probing: 1/(1 - a)")
    ax[0].plot(a, miss["linear"], "o", color=labs.BLUE, label="linear probing, measured")
    ax[0].plot(a, miss["double"], "s", color=labs.GREEN, ms=5, label="double hashing, measured")
    ax[0].set(title=f"Probes for an unsuccessful search ({M:,} slots)", xlabel="load a = keys / slots",
              ylabel="probes (log scale)", yscale="log")
    ax[0].legend()
    sizes = np.array([50, 100, 200, 400, 800, 1600, 3200])
    means = []
    for size in sizes:
        d = []
        for _ in range(4):
            t = ds.BST()
            for x in rng.random(int(size)).tolist():
                t.insert(x)
            d.append(np.mean(t.depths()))
        means.append(np.mean(d))
    ax[1].plot(sizes, [2 * (1 + 1 / s) * harmonic(int(s)) - 4 for s in sizes], color=labs.GOLD, label="2(1 + 1/n)H_n - 4")
    ax[1].plot(sizes, np.log2(sizes + 1) - 2, color=labs.GREY, ls="--", label="a perfectly balanced tree: about lg n - 2")
    ax[1].plot(sizes, means, "o", color=labs.BLUE, label="random BSTs, mean depth")
    ax[1].set(title="Mean depth of a node, in edges", xlabel="keys n (log scale)", ylabel="depth", xscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
