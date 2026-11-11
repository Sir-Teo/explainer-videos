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
        self.assertTrue(np.allclose(np.linalg.norm(V, axis=1), 1))
        cuts = O.gw_round(V, E)
        self.assertTrue(all(0 <= cut <= ex for cut in cuts))
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



class BoundaryContracts(unittest.TestCase):
    def test_simplex_budget_is_not_optimality(self):
        self.assertEqual(O.simplex([1], [[1]], [1], max_pivots=0)["status"], "iteration_limit")
        self.assertEqual(O.simplex([1], [[1]], [1], max_pivots=1)["status"], "optimal")
        self.assertEqual(O.simplex([1], [], [])["status"], "unbounded")
        for kwargs in ({"rule": "unknown"}, {"max_pivots": -1}):
            with self.assertRaises(ValueError):
                O.simplex([1], [[1]], [1], **kwargs)
        with self.assertRaises(ValueError):
            O.simplex([1], [[-1]], [-1])

    def test_partial_minor_search_is_inconclusive(self):
        triangle = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        self.assertIsNone(O.is_totally_unimodular(triangle, max_k=2)[0])
        passed, witness = O.is_totally_unimodular(triangle)
        self.assertFalse(passed)
        self.assertEqual(abs(witness[2]), 2)
        with self.assertRaises(ValueError):
            O.is_totally_unimodular([[0.5]])

    def test_integer_knapsack_avoids_float_ratio_ties(self):
        for values in ([2**53, 2**53 + 1], [2**100 + 1, 2**100]):
            best, choice, _, _ = O.branch_and_bound_knapsack(values, [1, 1], 1)
            self.assertEqual(best, max(values))
            self.assertEqual(sum(choice.values()), 1)

    def test_nearly_integral_bound_is_not_an_integral_solution(self):
        values, weights, capacity = [100, 100], [10**12, 1], 10**12 - 1
        best, choice, _, _ = O.branch_and_bound_knapsack(values, weights, capacity)
        self.assertEqual(best, 100)
        self.assertLessEqual(sum(weights[i] * v for i, v in choice.items()), capacity)
        self.assertEqual(O.branch_and_bound_knapsack([], [], 0)[:2], (0, {}))

    def test_fptas_discards_ineligible_items_before_scaling(self):
        self.assertEqual(O.knapsack_fptas([2**100, 10, 9], [100, 1, 1], 2, 0.5)[0], 19)
        for values, weights in (([], []), ([0], [1]), ([4], [5])):
            self.assertEqual(O.knapsack_fptas(values, weights, 1, 0.5), (0, 0))
        for epsilon in (0, -1, 1.1, math.nan):
            with self.assertRaises(ValueError):
                O.knapsack_fptas([1], [1], 1, epsilon)

    def test_graph_iterators_are_materialized(self):
        edges = [(0, 1), (1, 2), (0, 2)]
        optimum, cover = O.vertex_cover_exact(3, iter(edges))
        self.assertEqual(optimum, 2)
        self.assertTrue(all(u in cover or v in cover for u, v in edges))
        self.assertEqual(O.vertex_cover_lp(0, [])[0], 0)
        self.assertEqual(O.vertex_cover_matching(0, []), set())

    def test_uncoverable_set_family_does_not_loop(self):
        for solver in (O.set_cover_exact, O.set_cover_greedy):
            self.assertEqual(solver([], []), [])
            with self.assertRaises(ValueError):
                solver({1, 2}, [{1}])

    def test_empty_and_singleton_tours(self):
        self.assertEqual(O.held_karp([]), (0, []))
        self.assertEqual(O.held_karp([(0, 0)]), (0, [0]))
        self.assertEqual(O.mst_prim([]), [])
        self.assertEqual(O.double_tree([])[0], [])
        self.assertEqual(O.christofides([])[0], [])
        self.assertEqual(O.nearest_neighbour_tour([]), [])
        with self.assertRaises(ValueError):
            O.min_weight_perfect_matching([(0, 0)] * 3, [0, 1, 2])

    def test_local_sdp_value_is_not_an_upper_bound(self):
        vectors, local = O.gw_vectors(2, [(0, 1)], iters=0)
        self.assertLess(local, O.maxcut_exact(2, [(0, 1)])[0])
        self.assertTrue(np.allclose(np.linalg.norm(vectors, axis=1), 1))
        self.assertEqual(O.gw_vectors(2, [])[1], 0)
        self.assertEqual(O.maxcut_exact(0, []), (0, 0))
        self.assertEqual(O.gw_round(vectors, []), [0] * 200)

    def test_stable_weights_at_large_learning_rate(self):
        algorithm, best, history = O.hedge(np.ones((10, 2)), 1000)
        self.assertEqual((algorithm, best), (10, 10))
        self.assertTrue(np.isfinite(history).all())
        self.assertTrue(np.allclose(history, 0.5))
        lower, upper, average = O.mw_zero_sum(np.ones((2, 2)), 10, eta=1000)
        self.assertEqual((lower, upper), (1, 1))
        self.assertTrue(np.isfinite(average).all())
        with self.assertRaises(ValueError):
            O.hedge([[2, 0]], 0.1)
        with self.assertRaises(ValueError):
            O.mw_zero_sum([[0]], 0)

    def test_ellipsoid_checks_the_last_permitted_centre(self):
        self.assertIsNone(O.ellipsoid_feasible([[-1, 0]], [-1], max_steps=0)[0])
        point, steps, _ = O.ellipsoid_feasible([[-1, 0]], [-1], max_steps=1)
        self.assertIsNotNone(point)
        self.assertGreaterEqual(point[0], 1)
        self.assertEqual(steps, 1)
        with self.assertRaises(ValueError):
            O.ellipsoid_feasible([[1]], [1])

    def test_barrier_requires_a_strict_interior(self):
        with self.assertRaises(ValueError):
            O.barrier_path([1], [[1], [-1]], [1, 0], x0=[0])
        with self.assertRaises(ValueError):
            O.barrier_path([1], [[1], [-1]], [1, 1], ts=[0])

    def test_zero_capacity_cache_and_domains(self):
        for policy in ("lru", "fifo", "random", "marking", "opt"):
            self.assertEqual(O.paging([1, 1, 2], 0, policy), 3)
        with self.assertRaises(ValueError):
            O.paging([], -1, "lru")
        with self.assertRaises(ValueError):
            O.paging([], 1, "unknown")
        with self.assertRaises(ValueError):
            O.ski_rental(0, 10)
        self.assertEqual(O.ski_rental(1, 0), 0)

    def test_bipartite_endpoint_sides(self):
        with self.assertRaises(ValueError):
            O.bipartite_incidence([(0, 0)], 0, 1)
        with self.assertRaises(ValueError):
            O.bipartite_incidence([(1, 0)], 1, 1)


if __name__ == "__main__":
    unittest.main()
