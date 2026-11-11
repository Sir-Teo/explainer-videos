"""Tests for Part 61's instrument (explainer/cs/research/method.py)."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.research import method as M


class Research(unittest.TestCase):
    def test_bootstrap_contracts_and_constant_data(self):
        self.assertEqual(M.bootstrap([3, 3, 3], B=20), (3, 3))
        for xs, kwargs in (([], {}), ([float("nan")], {}), ([[1, 2]], {}),
                           ([1, 2], {"B": 0}), ([1, 2], {"alpha": 1})):
            with self.assertRaises(ValueError):
                M.bootstrap(xs, **kwargs)

    def test_goldbach_small(self):
        r = M.goldbach(10_000)
        self.assertTrue(r["all_hold"])
        self.assertEqual(M.goldbach(4)["worst_p"], 2)
        with self.assertRaises(ValueError):
            M.goldbach(3)

    def test_collatz_records(self):
        r = M.collatz(1000)
        self.assertEqual(r["records"][-1]["n"], 871)
        self.assertEqual(r["records"][-1]["steps"], 178)
        self.assertEqual(M.collatz(2)["max_steps"], 0)
        with self.assertRaises(ValueError):
            M.collatz(1)

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
