"""Part 19's instruments against brute force and known values."""

from __future__ import annotations

import math
import random
import unittest
from itertools import combinations

import numpy as np

from explainer.cs.algo import paradigms as P


class Greedy(unittest.TestCase):
    def test_activity_selection_is_optimal(self):
        rng = random.Random(1)
        for _ in range(200):
            ivs = []
            for _ in range(rng.randrange(1, 14)):
                s = rng.randrange(0, 40)
                ivs.append((s, s + rng.randrange(1, 12)))
            self.assertEqual(len(P.activity_selection(ivs, "finish")), P.max_compatible(ivs))

    def test_huffman_kraft_and_optimality(self):
        freq = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}         # CLRS's example: cost 224
        L = P.huffman(freq)
        self.assertAlmostEqual(sum(2.0 ** -l for l in L.values()), 1.0)
        self.assertEqual(sum(freq[s] * L[s] for s in freq), 224)

    def test_coins(self):
        self.assertEqual(len(P.coin_greedy(6, [1, 3, 4])), 3)
        self.assertEqual(len(P.coin_dp(6, [1, 3, 4])), 2)

    def test_matroid_greedy_on_forests(self):
        rng = random.Random(2)
        n = 6
        edges = [(u, v, rng.random()) for u, v in combinations(range(n), 2)]
        g = P.greedy_max_weight(edges, lambda e: e[2], P.forest_independent(n))
        best = 0
        for k in range(n):
            for sub in combinations(edges, k):
                if P.forest_independent(n)(list(sub)):
                    best = max(best, sum(e[2] for e in sub))
        self.assertAlmostEqual(sum(e[2] for e in g), best)


class Multiply(unittest.TestCase):
    def test_karatsuba(self):
        rng = random.Random(3)
        for _ in range(50):
            x, y = rng.randrange(10 ** 60), rng.randrange(10 ** 45)
            c = [0]
            out = P.karatsuba(P.to_digits(x), P.to_digits(y), c)
            self.assertEqual(P.from_digits(P._carry(out)), x * y)

    def test_karatsuba_count(self):
        for k in range(1, 8):
            n = 2 ** k
            c = [0]
            P.karatsuba([9] * n, [9] * n, c)
            self.assertEqual(c[0], 3 ** k)

    def test_strassen(self):
        rng = np.random.default_rng(4)
        A, B = rng.standard_normal((128, 128)), rng.standard_normal((128, 128))
        self.assertTrue(np.allclose(P.strassen(A, B, cutoff=16), A @ B))
        self.assertEqual(P.strassen_counts(8)[0], 7 ** 3)

    def test_fft(self):
        rng = random.Random(5)
        a = [complex(rng.random(), rng.random()) for _ in range(64)]
        self.assertTrue(np.allclose(P.fft(a), P.dft(a)))
        self.assertTrue(np.allclose(P.ifft(P.fft(a)), a))
        self.assertEqual(P.poly_mul_fft([1, 2, 3], [4, 5]), [4, 13, 22, 15])

    def test_ntt_and_bigmul(self):
        a = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(P.ntt(P.ntt(a), invert=True), a)
        rng = random.Random(6)
        x, y = rng.randrange(10 ** 5000), rng.randrange(10 ** 4000)
        self.assertEqual(P.fft_bigmul(x, y), x * y)

    def test_pi(self):
        self.assertEqual(str(P.chudnovsky(50)), "314159265358979323846264338327950288419716939937510")


class DivideAndDP(unittest.TestCase):
    def test_closest_pair(self):
        rng = random.Random(7)
        pts = [(rng.random(), rng.random()) for _ in range(300)]
        d, _, n, k = P.closest_pair(pts)
        self.assertAlmostEqual(d, P.closest_brute(pts)[0])
        self.assertLess(n, 300 * 299 // 2 // 5)
        self.assertLessEqual(k, 7)

    def test_edit_distance(self):
        D, ops, _ = P.edit_distance("kitten", "sitting")
        self.assertEqual(D[-1][-1], 3)
        self.assertEqual(sum(o != "=" for o in ops), 3)
        self.assertEqual(P.lcs("ABCBDAB", "BDCABA")[0], 4)

    def test_knapsack(self):
        rng = random.Random(8)
        items = [(rng.randrange(1, 20), rng.randrange(1, 30)) for _ in range(12)]
        W = 50
        best = 0
        for mask in range(1 << len(items)):
            w = sum(items[i][0] for i in range(len(items)) if mask >> i & 1)
            if w <= W:
                best = max(best, sum(items[i][1] for i in range(len(items)) if mask >> i & 1))
        self.assertEqual(P.knapsack(items, W)[0], best)

    def test_matrix_chain(self):
        self.assertEqual(P.matrix_chain([30, 35, 15, 5, 10, 20, 25])[0], 15125)          # CLRS 14.2

    def test_optimal_bst(self):
        rng = random.Random(9)
        p = [rng.random() for _ in range(30)]
        a, ia = P.optimal_bst(p)
        b, ib = P.optimal_bst(p, knuth=True)
        self.assertAlmostEqual(a, b)
        self.assertLess(ib, ia)

    def test_tree_mis(self):
        rng = random.Random(10)
        n = 14
        parent = {v: rng.randrange(v) for v in range(1, n)}
        children = {}
        for v, p in parent.items():
            children.setdefault(p, []).append(v)
        w = [rng.randrange(1, 10) for _ in range(n)]
        self.assertEqual(P.tree_mis(children, 0, w), P.tree_mis_brute(n, list(parent.items()), w))

    def test_fib(self):
        self.assertEqual(P.fib_naive_calls(20), (6765, 21891))
        self.assertEqual(P.fib_memo_calls(20)[0], 6765)


class Search(unittest.TestCase):
    def test_queens(self):
        self.assertEqual(P.queens(8)[0], 92)
        self.assertEqual(P.queens(8, bitmask=False)[0], 92)

    def test_sudoku(self):
        g = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        out, nodes, ups, nsol = P.solve_sudoku(g)
        self.assertEqual(nsol, 1)
        for i, ch in enumerate(g):
            if ch != "0":
                self.assertEqual(out[i], ch)
        for r in range(9):
            self.assertEqual(set(out[9 * r:9 * r + 9]), set("123456789"))
        self.assertEqual(P.sudoku_naive(g.replace("0", "."))[0], out)

    def test_max_subarray(self):
        rng = random.Random(11)
        for _ in range(50):
            a = [rng.randrange(-20, 20) for _ in range(rng.randrange(1, 40))]
            r = P.maxsub_cubic(a)
            self.assertEqual(P.maxsub_quadratic(a), r)
            self.assertEqual(P.maxsub_divide(a), r)
            self.assertEqual(P.maxsub_kadane(a), r)


if __name__ == "__main__":
    unittest.main()
