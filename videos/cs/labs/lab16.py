"""Lab 16: count the comparisons of every sort, against the lg n! lower bound and quicksort's 2(n + 1)H_n - 4n."""

from videos.coursekit import labs
import math
import random

import numpy as np

from explainer.cs.algo import sorts

TITLE = "Counting comparisons: the lower bound, and quicksort's average"
GOAL = ("With the series' instrumented sorts, find the worst case of three algorithms over every permutation of up "
        "to seven keys and compare it with the decision-tree bound; run randomized quicksort 400 times on 1,000 "
        "keys and compare its mean and spread with the formulas; then give two pivot rules a sorted input.")
TASKS = [
    "Add sorts.heapsort to the worst-case table. How far above the bound is it at n = 7, and does sorts.binary_insertion_sort do better than insertion sort?",
    "Call sorts.quicksort(xs, 'first') on 2,000 keys of which only 20 random pairs have been swapped out of sorted order. How close to n(n - 1)/2 does it stay?",
    "Count comparisons of sorts.quickselect for the median of 1,000 keys over 400 runs and compare the mean with (2 + 2 ln 2) n.",
]
RUNS, N = 400, 1000


def run(seed=0):
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)
    lab = labs.Lab()

    # 1. the decision-tree bound against exhaustive worst cases
    for n in range(2, 8):
        bound = sorts.lower_bound(n)
        worst = {name: sorts.worst_case(f, n) for name, f in (("merge insertion", sorts.ford_johnson),
                                                               ("merge sort", sorts.merge_sort),
                                                               ("insertion sort", sorts.insertion_sort))}
        assert all(w >= bound for w in worst.values()), f"a comparison sort beat lg {n}!"
        assert worst["merge insertion"] == bound == sorts.ford_johnson_formula(n), "merge insertion is optimal here"
        assert worst["insertion sort"] == n * (n - 1) // 2
        if n >= 5:
            lab.row(f"worst case over all {math.factorial(n):,} orders of {n} keys",
                    f"bound {bound}   merge insertion {worst['merge insertion']}   merge sort {worst['merge sort']}"
                    f"   insertion sort {worst['insertion sort']}")
    gap = [(n, sorts.ford_johnson_formula(n), sorts.lower_bound(n)) for n in range(2, 13)]
    assert all(f == b for _, f, b in gap[:-1]) and gap[-1][1:] == (30, 29), "the bound is met to n = 11, not at 12"
    lab.row("merge insertion against the bound at n = 12", f"{gap[-1][1]} comparisons, bound {gap[-1][2]}")

    # 2. randomized quicksort on N distinct keys
    keys = rng.permutation(N).tolist()
    counts = np.array([sorts.quicksort(keys, "random", rng=pyrng)[1]["cmp"] for _ in range(RUNS)])
    expect = sorts.quicksort_expected(N)
    sigma = math.sqrt(7 - 2 * math.pi ** 2 / 3) * N  # the large-n standard deviation
    lab.row(f"quicksort, {RUNS} runs on {N:,} keys: mean", f"{counts.mean():,.0f}   (2(n + 1)H_n - 4n = {expect:,.0f})")
    lab.row("its standard deviation", f"{counts.std(ddof=1):,.0f}   (large-n theory 0.648 n = {sigma:,.0f})")
    lab.row("fewest and most comparisons", f"{counts.min():,} and {counts.max():,}   "
                                           f"(lg n! = {sorts.lower_bound(N):,}, n(n - 1)/2 = {N * (N - 1) // 2:,})")
    assert abs(counts.mean() / expect - 1) < 0.015, "the mean should be 2(n + 1)H_n - 4n"
    assert 0.8 < counts.std(ddof=1) / sigma < 1.2, "the spread should be about 0.65 n"
    assert counts.min() >= sorts.lower_bound(N) and counts.max() < 2 * expect

    # 3. a sorted input: the first element as pivot, and the median of three
    n = 2000
    first = sorts.quicksort(list(range(n)), "first")[1]["cmp"]
    med3 = sorts.quicksort(list(range(n)), "median3")[1]["cmp"]
    lab.row(f"sorted input, {n:,} keys", f"first-element pivot {first:,}   median of three {med3:,}   "
                                         f"(n(n - 1)/2 = {n * (n - 1) // 2:,})")
    assert first == n * (n - 1) // 2 and med3 < 2.2 * n * math.log2(n)
    lab.note = ("No comparison sort can beat lg n! in the worst case, and merge insertion meets it for small n; "
                "randomized quicksort averages 2n ln n on every input and rarely strays, while a fixed pivot rule "
                "has inputs that cost n²/2.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ns = np.array([16, 32, 64, 128, 256, 512, 1024])
    series = {"insertion sort": [], "merge sort": [], "quicksort (random pivot)": []}
    for n in ns:
        xs = rng.permutation(int(n)).tolist()
        series["insertion sort"].append(sorts.insertion_sort(xs)[1]["cmp"])
        series["merge sort"].append(sorts.merge_sort(xs)[1]["cmp"])
        series["quicksort (random pivot)"].append(np.mean([sorts.quicksort(xs, "random", rng=pyrng)[1]["cmp"]
                                                           for _ in range(5)]))
    grid = np.geomspace(16, 1024, 60)
    lgfact = np.array([math.lgamma(n + 1) / math.log(2) for n in grid])
    ax[0].fill_between(grid, 1, lgfact, color=labs.RED, alpha=0.12)
    ax[0].plot(grid, lgfact, color=labs.RED, label="lg n!  (nothing sorts below this)")
    ax[0].plot(grid, grid * (grid - 1) / 4, color=labs.GREY, ls="--", label="n(n - 1)/4")
    for (name, ys), color in zip(series.items(), (labs.ORANGE, labs.GREEN, labs.BLUE)):
        ax[0].plot(ns, ys, "o-", color=color, ms=4, lw=1.2, label=name)
    ax[0].set(title="Comparisons to sort n random keys", xlabel="n", ylabel="comparisons", xscale="log", yscale="log",
              ylim=(30, None))
    ax[0].legend()
    ax[1].hist(counts, bins=40, color=labs.BLUE, alpha=0.7, label=f"{RUNS} runs")
    ax[1].axvline(expect, color=labs.GOLD, label="2(n + 1)H_n - 4n")
    ax[1].axvline(sorts.lower_bound(N), color=labs.RED, label="lg n!")
    ax[1].axvspan(expect - sigma, expect + sigma, color=labs.GOLD, alpha=0.12, label="± 0.648 n")
    ax[1].set(title=f"Randomized quicksort on {N:,} keys", xlabel="comparisons", ylabel="runs")
    ax[1].legend()
    lab.fig = fig
    return lab
