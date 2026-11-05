"""Precompute everything numerical in Part 19 of *Computer Science, Built* ("The Great Paradigms").

    python -m videos.cs.cs19.compute              # everything missing
    python -m videos.cs.cs19.compute --force fft

Results are cached in ``.cache/cs19/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/paradigms.py`` (greedy and matroids, Karatsuba, Strassen, the FFT and NTT, closest pair,
dynamic programmes, backtracking and Dancing Links, each counting its work), tested in
tests/test_cs19_paradigms.py.  Items that time code run on this machine, best of three where it is cheap.

Items:
    pi         a million digits of π by Chudnovsky's series; two million-digit numbers multiplied four ways
    greedy     interval scheduling by four rules; Huffman on the corpus letters; coins
    matroid    greedy on forests (always optimal) against greedy on matchings (not)
    karatsuba  digit products and timings: grade school against Karatsuba, and the crossover
    strassen   scalar operations, and Strassen against numpy's product, timed, with its rounding error
    fft        DFT against FFT, butterflies counted and timed; numpy's FFT
    closest    divide-and-conquer closest pair: distance computations and the strip bound
    fib        naive recursion against memoization
    edit       an edit-distance table with its traceback; quadratic time measured; LCS
    knapsack   the table, greedy's failure, and pseudo-polynomial time
    chain      matrix chains; optimal search trees with and without Knuth's speedup
    tree       independent sets on a tree by DP
    search     n-queens by backtracking; sudoku by plain backtracking and by Dancing Links
    maxsub     maximum subarray four ways, timed
    fftcore    the FFT convolution alone, on digit arrays up to ten million digits
"""

from __future__ import annotations

import decimal
import math
import random
import sys
import time
from collections import Counter

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs19")
load = CACHE.load
sys.set_int_max_str_digits(0)


def _best(f, reps=3):
    best = math.inf
    out = None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = f()
        best = min(best, time.perf_counter() - t0)
    return best, out


def compute_pi() -> dict:
    from explainer.cs.algo import paradigms as P
    t0 = time.perf_counter()
    pi = P.chudnovsky(1_000_000)
    t_pi = time.perf_counter() - t0
    s = str(pi)
    rng = random.Random(19)
    rows = []
    for N in (1_000, 10_000, 100_000, 1_000_000):
        x, y = rng.randrange(10 ** (N - 1), 10 ** N), rng.randrange(10 ** (N - 1), 10 ** N)
        t_int, prod = _best(lambda: x * y, 3 if N < 10 ** 6 else 1)
        t_fft, pf = _best(lambda: P.fft_bigmul(x, y), 3 if N < 10 ** 6 else 1)
        assert pf == prod
        ctx = decimal.Context(prec=2 * N + 10, Emax=decimal.MAX_EMAX)
        dx, dy = decimal.Decimal(x), decimal.Decimal(y)
        t_dec, pd = _best(lambda: ctx.multiply(dx, dy), 3 if N < 10 ** 6 else 1)
        assert int(pd) == prod
        rows.append({"digits": N, "python_int_s": t_int, "fft_s": t_fft, "decimal_s": t_dec})
        print(rows[-1])
    # grade school, measured where it finishes, then extrapolated as n^2
    school = []
    for N in (100, 200, 400, 800):
        a = P.to_digits(rng.randrange(10 ** N))
        b = P.to_digits(rng.randrange(10 ** N))
        t, _ = _best(lambda: P.school_mul(a, b))
        school.append({"digits": N, "s": t})
    rate = school[-1]["s"] / school[-1]["digits"] ** 2
    return {"digits": 1_000_000, "seconds": t_pi, "head": s[:52], "tail": s[-10:], "rows": rows,
            "school": school, "school_rate": rate, "school_1m_s": rate * 1e12}


def compute_greedy() -> dict:
    from explainer.cs.algo import paradigms as P
    from videos.cs.cs16.compute import _full_text
    rng = random.Random(3)
    # one instance to draw
    ivs = []
    while len(ivs) < 11:
        s = rng.randrange(0, 22)
        iv = (s, s + rng.randrange(2, 7))
        if iv not in ivs:
            ivs.append(iv)
    pick = P.activity_selection(ivs, "finish")
    # each rule against the optimum on random instances
    stats = {r: 0 for r in ("finish", "start", "shortest", "fewest")}
    trials = 2000
    for _ in range(trials):
        inst = []
        for _ in range(rng.randrange(4, 12)):
            s = rng.randrange(0, 30)
            inst.append((s, s + rng.randrange(1, 10)))
        opt = P.max_compatible(inst)
        for r in stats:
            stats[r] += len(P.activity_selection(inst, r)) == opt
    # small counterexamples for the wrong rules
    bad = {"start": [(0, 10), (1, 3), (4, 6), (7, 9)], "shortest": [(0, 5), (4, 7), (6, 11)],
           "fewest": [(0, 2), (3, 5), (6, 8), (9, 11), (1, 4), (1, 4), (1, 4), (2, 3), (4, 7), (5, 6), (5, 6), (5, 6),
                      (7, 10), (7, 10), (7, 10)]}
    bad_res = {r: {"chosen": len(P.activity_selection(v, r)), "best": P.max_compatible(v), "ivs": v}
               for r, v in bad.items()}
    # Huffman on the letters of the thirty novels
    import re
    words = re.findall(r"[a-z]+", _full_text().decode("utf-8", "ignore").lower())
    freq = Counter(ch for w in words for ch in w)
    freq[" "] = len(words) - 1                       # one space between words
    total = sum(freq.values())
    L = P.huffman(dict(freq))
    avg = sum(freq[s] * L[s] for s in freq) / total
    H = -sum(c / total * math.log2(c / total) for c in freq.values())
    top = sorted(freq, key=lambda s: -freq[s])
    coins_us = all(len(P.coin_greedy(a, [1, 5, 10, 25])) == len(P.coin_dp(a, [1, 5, 10, 25])) for a in range(1, 100))
    fails = [a for a in range(1, 100) if len(P.coin_greedy(a, [1, 3, 4])) != len(P.coin_dp(a, [1, 3, 4]))]
    return {"ivs": ivs, "pick": pick, "stats": stats, "trials": trials, "bad": bad_res, "symbols": len(freq),
            "letters": total, "avg_bits": avg, "entropy": H, "fixed_bits": math.ceil(math.log2(len(freq))),
            "codes": [[s, L[s], freq[s] / total] for s in top], "us_coins_optimal": coins_us,
            "coins134_fail": fails[:12], "coins134_fail_n": len(fails)}


def compute_matroid() -> dict:
    from explainer.cs.algo import paradigms as P
    from itertools import combinations
    rng = random.Random(5)
    trials, forest_ok, match_ok, worst = 400, 0, 0, 1.0
    for _ in range(trials):
        n = 6
        edges = [(u, v, round(rng.random(), 3)) for u, v in combinations(range(n), 2) if rng.random() < 0.6]
        if not edges:
            continue
        g = P.greedy_max_weight(edges, lambda e: e[2], P.forest_independent(n))
        best = 0
        for k in range(1, n):
            for sub in combinations(edges, k):
                if P.forest_independent(n)(list(sub)):
                    best = max(best, sum(e[2] for e in sub))
        forest_ok += abs(sum(e[2] for e in g) - best) < 1e-9
        gm = P.greedy_max_weight(edges, lambda e: e[2], P.matching_independent)
        bm = P.max_weight_matching_brute(edges)
        ratio = sum(e[2] for e in gm) / bm
        match_ok += ratio > 1 - 1e-9
        worst = min(worst, ratio)
    # the smallest failure: a path a-b-c-d with weights 2, 3, 2
    path = [(0, 1, 2.0), (1, 2, 3.0), (2, 3, 2.0)]
    gp = P.greedy_max_weight(path, lambda e: e[2], P.matching_independent)
    return {"trials": trials, "forest_ok": forest_ok, "match_ok": match_ok, "match_worst": worst,
            "path_greedy": sum(e[2] for e in gp), "path_best": P.max_weight_matching_brute(path)}


def compute_karatsuba() -> dict:
    from explainer.cs.algo import paradigms as P
    rng = random.Random(7)
    rows = []
    for k in range(4, 13):
        n = 2 ** k
        a = P.to_digits(rng.randrange(10 ** (n - 1), 10 ** n))
        b = P.to_digits(rng.randrange(10 ** (n - 1), 10 ** n))
        reps = 3 if n <= 1024 else 1
        t_s, _ = _best(lambda: P.school_mul(a, b), reps)
        c = [0]
        P.karatsuba(a, b, c)
        t_k1, _ = _best(lambda: P.karatsuba(a, b), reps)
        t_k32, _ = _best(lambda: P.karatsuba(a, b, cutoff=32), reps)
        rows.append({"n": n, "school_products": n * n, "kara_products": c[0], "school_s": t_s, "kara1_s": t_k1,
                     "kara32_s": t_k32})
        print(rows[-1])
    cross = next((r["n"] for r in rows if r["kara32_s"] < r["school_s"]), None)
    return {"rows": rows, "crossover": cross, "exponent": math.log2(3)}


def compute_strassen() -> dict:
    from explainer.cs.algo import paradigms as P
    counts = []
    for k in range(1, 11):
        n = 2 ** k
        m, a = P.strassen_counts(n)
        counts.append({"n": n, "naive_mults": n ** 3, "strassen_mults": m, "naive_adds": n * n * (n - 1),
                       "strassen_adds": a})
    rng = np.random.default_rng(0)
    timed = []
    for n in (512, 1024, 2048, 4096):
        A, B = rng.standard_normal((n, n)), rng.standard_normal((n, n))
        reps = 3 if n <= 2048 else 1
        t_np, C = _best(lambda: A @ B, reps)
        t_st, S = _best(lambda: P.strassen(A, B, cutoff=256), reps)
        err_np = float(np.max(np.abs(C - S)) / np.max(np.abs(C)))
        timed.append({"n": n, "numpy_s": t_np, "strassen_s": t_st, "rel_diff": err_np})
        print(timed[-1])
    # rounding: Strassen against the exact product of small integers stored as floats
    A = rng.integers(-1000, 1000, (256, 256)).astype(np.float64) / 7
    B = rng.integers(-1000, 1000, (256, 256)).astype(np.float64) / 3
    exact = (A.astype(np.longdouble) @ B.astype(np.longdouble))
    e_np = float(np.max(np.abs(A @ B - exact)))
    e_st = float(np.max(np.abs(P.strassen(A, B, cutoff=8) - exact)))
    return {"counts": counts, "timed": timed, "err_numpy": e_np, "err_strassen": e_st}


def compute_fft() -> dict:
    from explainer.cs.algo import paradigms as P
    rng = random.Random(11)
    rows = []
    for k in range(5, 12):
        n = 2 ** k
        a = [complex(rng.random(), 0) for _ in range(n)]
        c = [0]
        P.fft(a, c)
        t_fft, F = _best(lambda: P.fft(a), 3)
        if n <= 2048:
            t_dft, D = _best(lambda: P.dft(a), 1)
            err = max(abs(x - y) for x, y in zip(F, D))
        else:
            t_dft, err = None, None
        arr = np.array(a)
        t_np, _ = _best(lambda: np.fft.fft(arr), 5)
        rows.append({"n": n, "butterflies": c[0], "dft_products": n * n, "dft_s": t_dft, "fft_s": t_fft,
                     "numpy_s": t_np, "max_diff": err})
        print(rows[-1])
    big = []
    for n in (2 ** 16, 2 ** 20, 2 ** 22):
        arr = np.random.default_rng(1).standard_normal(n)
        t, _ = _best(lambda: np.fft.fft(arr), 3)
        big.append({"n": n, "numpy_s": t})
    # polynomial product example for the screen
    p, q = [1, 2, 3], [4, 5]
    return {"rows": rows, "big": big, "poly": [p, q, P.poly_mul_fft(p, q)],
            "ntt_check": P.ntt(P.ntt([3, 1, 4, 1, 5, 9, 2, 6]), invert=True)}


def compute_closest() -> dict:
    from explainer.cs.algo import paradigms as P
    rng = random.Random(13)
    rows = []
    for n in (100, 1000, 10_000, 100_000):
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        t, (d, pair, nd, smax) = _best(lambda: P.closest_pair(pts), 3 if n < 10 ** 5 else 1)
        row = {"n": n, "dist_computations": nd, "brute_computations": n * (n - 1) // 2, "strip_max": smax, "s": t}
        if n <= 1000:
            row["brute_s"], (bd, _, _) = _best(lambda: P.closest_brute(pts), 1)
            assert abs(bd - d) < 1e-12
        rows.append(row)
        print(row)
    show = [(round(rng.uniform(-6, 0), 3), round(rng.uniform(-2.8, 2.4), 3)) for _ in range(48)]
    d, pair, _, _ = P.closest_pair(show)
    return {"rows": rows, "show": show, "show_pair": [list(pair[0]), list(pair[1])], "show_d": d}


def compute_fib() -> dict:
    from explainer.cs.algo import paradigms as P
    rows = []
    for n in (10, 15, 20, 25, 30):
        v, calls = P.fib_naive_calls(n)
        t, _ = _best(lambda: P.fib_naive_calls(n), 1)
        _, mc = P.fib_memo_calls(n)
        rows.append({"n": n, "value": v, "naive_calls": calls, "memo_calls": mc, "naive_s": t})
    return {"rows": rows}


def compute_edit() -> dict:
    from explainer.cs.algo import paradigms as P
    a, b = "intention", "execution"
    D, ops, path = P.edit_distance(a, b)
    rng = random.Random(17)
    rows = []
    for n in (250, 500, 1000, 2000):
        x = "".join(rng.choice("acgt") for _ in range(n))
        y = "".join(rng.choice("acgt") for _ in range(n))
        t, (DD, _, _) = _best(lambda: P.edit_distance(x, y), 1)
        rows.append({"n": n, "cells": (n + 1) ** 2, "s": t, "distance": DD[-1][-1]})
        print(rows[-1])
    l, seq = P.lcs("ABCBDAB", "BDCABA")
    return {"a": a, "b": b, "D": D, "ops": ops, "path": path, "rows": rows, "lcs": [l, "".join(seq)]}


def compute_knapsack() -> dict:
    from explainer.cs.algo import paradigms as P
    items = [(5, 10), (4, 40), (6, 30), (3, 50), (2, 15), (7, 45)]
    W = 12
    best, chosen, cells = P.knapsack(items, W)
    greedy = P.knapsack_greedy(items, W)
    rng = random.Random(23)
    worse, trials, worst = 0, 500, 1.0
    for _ in range(trials):
        its = [(rng.randrange(1, 30), rng.randrange(1, 60)) for _ in range(15)]
        Wt = rng.randrange(20, 120)
        b, _, _ = P.knapsack(its, Wt)
        g = P.knapsack_greedy(its, Wt)
        worse += g < b
        worst = min(worst, g / b if b else 1.0)
    # pseudo-polynomial: 20 items; scale the weights (and W) by 10, 100, 1000 …: same problem, more cells
    base = [(rng.randrange(1, 30), rng.randrange(1, 60)) for _ in range(20)]
    scale = []
    for s in (1, 10, 100, 1000, 10_000):
        its = [(w * s, v) for w, v in base]
        Wt = 100 * s
        t, (b, _, c) = _best(lambda: P.knapsack(its, Wt), 1)
        scale.append({"scale": s, "W": Wt, "bits": Wt.bit_length(), "cells": c, "s": t, "best": b})
        print(scale[-1])
    return {"items": items, "W": W, "best": best, "chosen": chosen, "cells": cells, "greedy": greedy,
            "trials": trials, "greedy_worse": worse, "greedy_worst": worst, "scale": scale}


def compute_chain() -> dict:
    from explainer.cs.algo import paradigms as P
    dims = [30, 35, 15, 5, 10, 20, 25]
    cost, br = P.matrix_chain(dims)
    left = P.chain_cost(dims, None)
    # the worst bracketing, by brute force over the Catalan many
    from functools import lru_cache

    @lru_cache(None)
    def worst(i, j):
        if i == j:
            return 0
        return max(worst(i, k) + worst(k + 1, j) + dims[i] * dims[k + 1] * dims[j + 1] for k in range(i, j))
    rng = random.Random(29)
    bst = []
    for n in (25, 50, 100, 200):
        p = [rng.random() for _ in range(n)]
        s = sum(p)
        p = [x / s for x in p]
        t1, (e1, i1) = _best(lambda: P.optimal_bst(p), 1)
        t2, (e2, i2) = _best(lambda: P.optimal_bst(p, knuth=True), 1)
        assert abs(e1 - e2) < 1e-9
        bst.append({"n": n, "plain_iters": i1, "knuth_iters": i2, "plain_s": t1, "knuth_s": t2, "cost": e1})
        print(bst[-1])
    return {"dims": dims, "best": cost, "brackets": br, "left_to_right": left, "worst": worst(0, len(dims) - 2),
            "catalan": math.comb(2 * 5, 5) // 6, "bst": bst}


def compute_tree() -> dict:
    from explainer.cs.algo import paradigms as P
    rng = random.Random(31)
    n = 15
    parent = {v: rng.randrange(max(0, v - 4), v) for v in range(1, n)}
    children = {}
    for v, p in parent.items():
        children.setdefault(p, []).append(v)
    w = [rng.randrange(1, 10) for _ in range(n)]
    best = P.tree_mis(children, 0, w)
    assert best == P.tree_mis_brute(n, list(parent.items()), w)
    # which vertices: recompute with choice tracking
    memo = {}

    def go(v):
        take, skip = w[v], 0
        for c in children.get(v, []):
            t, s = go(c)
            take += s
            skip += max(t, s)
        memo[v] = (take, skip)
        return take, skip
    go(0)
    chosen = []

    def pick(v, can):
        t, s = memo[v]
        if can and t >= s:
            chosen.append(v)
            for c in children.get(v, []):
                pick(c, False)
        else:
            for c in children.get(v, []):
                pick(c, True)
    pick(0, True)
    big_n = 200_000
    par = {v: rng.randrange(v) for v in range(1, big_n)}
    ch = {}
    for v, p in par.items():
        ch.setdefault(p, []).append(v)
    ww = [rng.randrange(1, 10) for _ in range(big_n)]
    # iterative version for the big tree (recursion would be too deep)
    order = [0]
    for v in order:
        order.extend(ch.get(v, []))
    take, skip = list(ww), [0] * big_n
    t0 = time.perf_counter()
    for v in reversed(order):
        for c in ch.get(v, []):
            take[v] += skip[c]
            skip[v] += max(take[c], skip[c])
    t_big = time.perf_counter() - t0
    return {"n": n, "parent": parent, "w": w, "best": best, "chosen": sorted(chosen), "big_n": big_n,
            "big_s": t_big, "big_best": max(take[0], skip[0])}


ESCARGOT = "1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3.."
INKALA12 = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
EASY = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"


def compute_search() -> dict:
    from explainer.cs.algo import paradigms as P
    queens = []
    for n in range(4, 15):
        t, (sols, nodes) = _best(lambda: P.queens(n), 1)
        queens.append({"n": n, "solutions": sols, "nodes": nodes, "placements": n ** n, "s": t})
    q8_plain = P.queens(8, bitmask=False)
    sud = []
    for name, g in (("an easy newspaper puzzle", EASY), ("AI Escargot (Inkala, 2006)", ESCARGOT),
                    ("Inkala's 2012 puzzle", INKALA12)):
        t1, (out, nodes, ups, nsol) = _best(lambda: P.solve_sudoku(g.replace(".", "0")), 1)
        t2, (out2, nodes2) = _best(lambda: P.sudoku_naive(g), 1)
        assert out2 == out and nsol == 1
        sud.append({"name": name, "grid": g, "givens": sum(ch != "." for ch in g), "solution": out,
                    "dlx_nodes": nodes, "dlx_updates": ups, "dlx_s": t1, "naive_nodes": nodes2, "naive_s": t2})
        print(sud[-1]["name"], nodes, nodes2, t1, t2)
    return {"queens": queens, "q8_plain_nodes": q8_plain[1], "sudoku": sud}


def compute_maxsub() -> dict:
    from explainer.cs.algo import paradigms as P
    rng = random.Random(37)
    rows = []
    for n in (100, 200, 400, 1000, 10_000, 100_000, 1_000_000):
        a = [rng.randrange(-100, 101) for _ in range(n)]
        row = {"n": n}
        ans = P.maxsub_kadane(a)
        for name, f, cap in (("cubic", P.maxsub_cubic, 400), ("quadratic", P.maxsub_quadratic, 10_000),
                             ("divide", P.maxsub_divide, 1_000_000), ("kadane", P.maxsub_kadane, 1_000_000)):
            if n <= cap:
                t, v = _best(lambda: f(a), 1 if n > 1000 else 3)
                assert v == ans
                row[name] = t
        rows.append(row)
        print(row)
    show = [rng.randrange(-9, 10) for _ in range(16)]
    best, bi, bj = -math.inf, 0, 0
    for i in range(len(show)):
        for j in range(i, len(show)):
            if sum(show[i:j + 1]) > best:
                best, bi, bj = sum(show[i:j + 1]), i, j
    return {"rows": rows, "show": show, "show_best": best, "show_range": [bi, bj]}


def compute_fftcore() -> dict:
    """The transform alone: convolve two million-digit numbers held as base-10^4 arrays (no conversion)."""
    rng = np.random.default_rng(41)
    rows = []
    for N in (10_000, 100_000, 1_000_000, 10_000_000):
        a = rng.integers(0, 10_000, N // 4).astype(np.float64)
        b = rng.integers(0, 10_000, N // 4).astype(np.float64)
        n = 1
        while n < len(a) + len(b):
            n *= 2

        def conv():
            c = np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)
            return np.rint(c)
        t, c = _best(conv, 3)
        raw = np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)
        resid = float(np.max(np.abs(raw - np.rint(raw))))      # must stay well below 0.5 to round exactly
        # exactness: compare a stretch against exact integer convolution
        k = 64
        exact = np.convolve(a[:k].astype(np.int64), b[:k].astype(np.int64))[:k]
        ok = bool(np.all(c[:k].astype(np.int64) == exact))
        rows.append({"digits": N, "fft_core_s": t, "exact_prefix": ok, "max_term": float(np.max(c)),
                     "max_residual": resid})
        print(rows[-1])
    return {"rows": rows}


ITEMS = {
    "pi": compute_pi, "greedy": compute_greedy, "matroid": compute_matroid, "karatsuba": compute_karatsuba,
    "strassen": compute_strassen, "fft": compute_fft, "closest": compute_closest, "fib": compute_fib,
    "edit": compute_edit, "knapsack": compute_knapsack, "chain": compute_chain, "tree": compute_tree,
    "search": compute_search, "maxsub": compute_maxsub, "fftcore": compute_fftcore,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
