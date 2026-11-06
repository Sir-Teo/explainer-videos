"""Tests for Part 57's instrument (explainer/cs/learn/theory.py)."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.learn import theory as T


class Learning(unittest.TestCase):
    def test_shattering(self):
        s = T.shattering()
        self.assertTrue(s["three"]["shattered"])
        self.assertFalse(s["square"]["shattered"])
        self.assertEqual(s["square"]["separable_count"], 14)

    def test_growth_formula(self):
        for r in T.growth(ms=range(1, 7), trials=1):
            self.assertEqual(r["realized"], r["exact_general"])
            self.assertLessEqual(r["realized"], r["sauer"])

    def test_rectangles_within_bound(self):
        for r in T.rectangle_curves(ms=(50, 200), trials=100)["rows"]:
            self.assertLessEqual(r["p95"], r["rect_bound"])

    def test_perceptron_bound(self):
        for r in T.perceptron_margin(dims=(5, 50), n=500):
            self.assertLessEqual(r["mistakes"], r["bound"] + 1e-9)

    def test_halving(self):
        h = T.halving(N=256, T=100)
        self.assertLessEqual(h["mistakes"], 8)

    def test_gf2(self):
        rng = np.random.default_rng(1)
        X = rng.integers(0, 2, (40, 12))
        s = np.zeros(12, int)
        s[[1, 5, 9]] = 1
        y = (X @ s) % 2
        x = T._gf2_solve(X, y)
        self.assertTrue(np.all((X @ x) % 2 == y))

    def test_compression(self):
        self.assertTrue(T.rectangle_compression()["consistent"])


if __name__ == "__main__":
    unittest.main()
