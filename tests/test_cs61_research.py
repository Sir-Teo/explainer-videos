"""Tests for Part 61's instrument (explainer/cs/research/method.py)."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.research import method as M


class Research(unittest.TestCase):
    def test_goldbach_small(self):
        r = M.goldbach(10_000)
        self.assertTrue(r["all_hold"])

    def test_collatz_records(self):
        r = M.collatz(1000)
        self.assertEqual(r["records"][-1]["n"], 871)
        self.assertEqual(r["records"][-1]["steps"], 178)

    def test_geometric_mean_symmetric(self):
        m = M.speedup_means()
        self.assertAlmostEqual(m["geo_b_over_a"], 1 / m["geo_a_over_b"])
        self.assertGreater(m["arith_b_over_a"], 1)
        self.assertGreater(m["arith_a_over_b"], 1)

    def test_bootstrap_covers(self):
        rng = np.random.default_rng(0)
        xs = rng.normal(10, 1, 50)
        lo, hi = M.bootstrap(xs, np.mean, B=2000)
        self.assertLess(lo, 10.3)
        self.assertGreater(hi, 9.7)


if __name__ == "__main__":
    unittest.main()
