"""Tests for explainer/cs/algo/optim.py (Part 23 of Computer Science, Built)."""

import math
import random
import unittest

import numpy as np

from explainer.cs.algo import optim as O


class Simplex(unittest.TestCase):
    def test_against_highs_and_duality(self):
        from scipy.optimize import linprog
        rng = random.Random(0)
        for _ in range(30):
            c, A, b = O.random_lp(rng.randint(2, 6), rng.randint(2, 8), rng)
            for rule in ("dantzig", "bland", "steepest"):
                r = O.simplex(c, A, b, rule=rule)
                s = linprog([-v for v in c], A_ub=A, b_ub=b, method="highs")
                self.assertAlmostEqual(r["value"], -s.fun, places=7)
                self.assertAlmostEqual(sum(y * v for y, v in zip(r["duals"], b)), r["value"], places=7)
                self.assertTrue(all(y >= -1e-12 for y in r["duals"]))

    def test_klee_minty(self):
        for n in range(2, 8):
            c, A, b = O.klee_minty(n)
            r = O.simplex(c, A, b, exact=True)
            self.assertEqual(r["pivots"], 2 ** n - 1)
            self.assertEqual(r["value_exact"], 5 ** n)

    def test_vertices(self):
        V = O.vertices_3d([[1, 1, 1]], [1])
        self.assertEqual(len(V), 4)


class PolyTime(unittest.TestCase):
    def test_ellipsoid(self):
        A = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        b = np.array([3.1, -2.9, 1.1, -0.9])
        x, steps, _ = O.ellipsoid_feasible(A, b, R=10)
        self.assertIsNotNone(x)
        self.assertTrue(np.all(A @ x <= b + 1e-12))

    def test_barrier(self):
        path, _ = O.barrier_path([1, 1], [[1, 2], [3, 1], [-1, 0], [0, -1]], [4, 6, 0, 0], x0=[0.5, 0.5])
        self.assertTrue(np.allclose(path[-1][1], [1.6, 1.2], atol=1e-3))


class Combinatorial(unittest.TestCase):
    def test_tu(self):
        M = O.bipartite_incidence([(0, 0), (0, 1), (1, 1), (1, 2), (2, 0)], 3, 3)
        self.assertTrue(O.is_totally_unimodular(M)[0])
        self.assertFalse(O.is_totally_unimodular(np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]]))[0])

    def test_knapsack(self):
        rng = random.Random(1)
        for _ in range(10):
            vals = [rng.randint(1, 50) for _ in range(15)]
            wts = [rng.randint(1, 30) for _ in range(15)]
            cap = 100
            best = O.knapsack_dp(vals, wts, cap)
            self.assertEqual(O.branch_and_bound_knapsack(vals, wts, cap)[0], best)
            v, _ = O.knapsack_fptas(vals, wts, cap, 0.2)
            self.assertGreaterEqual(v, 0.8 * best)
            self.assertLessEqual(v, best)

    def test_vertex_and_set_cover(self):
        rng = random.Random(2)
        n = 10
        E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
        opt, _ = O.vertex_cover_exact(n, E)
        self.assertLessEqual(len(O.vertex_cover_matching(n, E)), 2 * opt)
        lp, x, cov = O.vertex_cover_lp(n, E)
        self.assertLessEqual(lp, opt + 1e-9)
        self.assertLessEqual(len(cov), 2 * opt)
        self.assertTrue(all(u in cov or v in cov for u, v in E))
        U, S, o = O.harmonic_bad_set_cover(4)
        self.assertEqual(len(O.set_cover_exact(U, S)), o)
        self.assertGreater(len(O.set_cover_greedy(U, S)), o)

    def test_tsp(self):
        rng = random.Random(3)
        P = [(rng.random(), rng.random()) for _ in range(10)]
        opt, tour = O.held_karp(P)
        self.assertAlmostEqual(O.tour_length(P, tour), opt)
        dt, _ = O.double_tree(P)
        self.assertLessEqual(O.tour_length(P, dt), 2 * opt + 1e-9)
        ch, *_ = O.christofides(P)
        self.assertEqual(sorted(ch), list(range(10)))
        self.assertLessEqual(O.tour_length(P, ch), 1.5 * opt + 1e-9)

    def test_gw(self):
        rng = random.Random(4)
        n = 10
        E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.5]
        ex, _ = O.maxcut_exact(n, E)
        V, sdp = O.gw_vectors(n, E)
        self.assertGreaterEqual(sdp, ex - 1e-6)
        self.assertGreaterEqual(np.mean(O.gw_round(V, E)), 0.878 * ex - 1e-9)
        a, _ = O.gw_alpha()
        self.assertAlmostEqual(a, 0.87856, places=4)


class Online(unittest.TestCase):
    def test_paging(self):
        k = 4
        trace = list(range(k + 1)) * 50
        self.assertEqual(O.paging(trace, k, "lru"), len(trace))
        self.assertLessEqual(O.paging(trace, k, "opt"), len(trace) // k + k + 1)
        rng = random.Random(5)
        t = [rng.randint(0, 12) for _ in range(500)]
        self.assertLessEqual(O.paging(t, 5, "opt"), O.paging(t, 5, "lru"))

    def test_ski(self):
        B = 10
        for d in range(1, 40):
            self.assertLessEqual(O.ski_rental(B, d), 2 * min(d, B))

    def test_hedge(self):
        L = np.random.default_rng(0).random((1000, 8))
        a, best, _ = O.hedge(L, math.sqrt(8 * math.log(8) / 1000))
        self.assertLessEqual(a - best, math.sqrt(1000 * math.log(8) / 2) + 1e-9)
        lo, hi, _ = O.mw_zero_sum(np.array([[0.5, 1, 0], [0, 0.5, 1], [1, 0, 0.5]]), 3000)
        self.assertLessEqual(lo, 0.5 + 1e-9)
        self.assertGreaterEqual(hi, 0.5 - 1e-9)
        self.assertLess(hi - lo, 0.05)


if __name__ == "__main__":
    unittest.main()
