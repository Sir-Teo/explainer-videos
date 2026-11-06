"""Tests for Part 52's instruments (explainer/cs/numeric)."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.numeric import analysis, eigen, iterative, linalg, speed


class Dense(unittest.TestCase):
    def test_lu_reconstructs(self):
        rng = np.random.default_rng(1)
        A = rng.standard_normal((6, 6))
        perm, L, U, g = linalg.lu(A)
        self.assertTrue(np.allclose(A[perm], L @ U))
        self.assertTrue(np.allclose(np.tril(U, -1), 0))
        self.assertGreaterEqual(g, 1.0)

    def test_wilkinson_growth(self):
        for n in (4, 8, 16):
            self.assertAlmostEqual(linalg.lu(linalg.wilkinson_matrix(n))[3], 2.0 ** (n - 1))

    def test_pivoting(self):
        r = linalg.pivot_failure((1e-20,))[0]
        self.assertGreater(r["err_no_pivot"], 0.5)
        self.assertLess(r["err_pivot"], 1e-12)

    def test_cholesky(self):
        rng = np.random.default_rng(2)
        X = rng.standard_normal((5, 5))
        A = X @ X.T + 5 * np.eye(5)
        L = linalg.cholesky(A)
        self.assertTrue(np.allclose(L @ L.T, A))

    def test_qr(self):
        rng = np.random.default_rng(3)
        A = rng.standard_normal((7, 4))
        Q, R = linalg.householder(A)
        self.assertTrue(np.allclose(Q @ R, A))
        self.assertTrue(np.allclose(Q.T @ Q, np.eye(7)))
        Qg, Rg, _ = linalg.givens(A)
        self.assertTrue(np.allclose(Qg @ Rg, A))

    def test_orthogonality_order(self):
        r = linalg.orthogonality((10,))[0]
        self.assertGreater(r["cgs"], r["mgs"])
        self.assertGreater(r["mgs"], r["householder"])
        self.assertLess(r["householder"], 1e-13)

    def test_backward_bound(self):
        for r in linalg.forward_vs_backward():
            self.assertLessEqual(r["forward"], 1.01 * r["bound"] + 1e-15)
            self.assertLess(r["backward"], 1e-15)


class Eigen(unittest.TestCase):
    def test_qr_algorithm(self):
        q = eigen.qr_experiment(n=6)
        self.assertLess(q["shifted"]["error"], 1e-12)
        self.assertLess(q["shifted"]["iterations"], q["unshifted"]["iterations"])

    def test_hessenberg_similar(self):
        rng = np.random.default_rng(4)
        A = rng.standard_normal((6, 6))
        H = eigen.hessenberg(A)
        self.assertTrue(np.allclose(np.tril(H, -2), 0))
        self.assertTrue(np.allclose(np.sort_complex(np.linalg.eigvals(H)), np.sort_complex(np.linalg.eigvals(A))))


class Iterative(unittest.TestCase):
    def test_cg_solves(self):
        A = iterative.poisson2d(10)
        b = np.ones(100)
        x, h = iterative.cg(A, b)
        self.assertLess(np.linalg.norm(A @ x - b) / np.linalg.norm(b), 1e-7)
        self.assertLessEqual(len(h) - 1, 100)          # at most n steps in exact arithmetic

    def test_multigrid_rate(self):
        rows = iterative.multigrid_experiment(ms=(15, 31), cycles=6)
        for r in rows:
            self.assertLess(r["factor"], 0.35)

    def test_nested_dissection_is_permutation(self):
        p = iterative.nested_dissection(9)
        self.assertEqual(sorted(p.tolist()), list(range(81)))


class Analysis(unittest.TestCase):
    def test_newton_quadratic(self):
        r = analysis.root_race()
        self.assertGreaterEqual(r["newton"][3], 11)

    def test_bary_exact_on_polynomial(self):
        xs = np.linspace(-1, 1, 6)
        f = lambda x: 3 * x ** 5 - x ** 2 + 1  # noqa: E731
        xx = np.linspace(-1, 1, 50)
        self.assertTrue(np.allclose(analysis.bary(xs, f(xs), xx), f(xx)))

    def test_runge(self):
        rows = {r["n"]: r for r in analysis.runge(ns=(10, 40))["rows"]}
        self.assertGreater(rows[40]["equispaced"], rows[10]["equispaced"])
        self.assertLess(rows[40]["chebyshev"], rows[10]["chebyshev"])

    def test_gauss_exact_degree(self):
        g, w = np.polynomial.legendre.leggauss(4)
        self.assertAlmostEqual(w @ g ** 6, 2 / 7)

    def test_rk45(self):
        ts, ys, _ = analysis.rk45(lambda t, y: -y, 0.0, [1.0], 2.0, tol=1e-9)
        self.assertAlmostEqual(ys[-1][0], np.exp(-2.0), places=7)

    def test_leapfrog_bounded(self):
        k = analysis.kepler(orbits=100)
        self.assertLess(max(abs(x) for x in k["leapfrog"]["energy_drift"]), 0.02)
        self.assertGreater(abs(k["rk4"]["energy_drift"][-1]), abs(k["rk4"]["energy_drift"][0]))


class Speed(unittest.TestCase):
    def test_refinement_converges(self):
        r = speed.refinement(n=100, kappas=(1e3,), iters=4)[0]
        self.assertLess(r["errors"][-1], 1e-12)


if __name__ == "__main__":
    unittest.main()
