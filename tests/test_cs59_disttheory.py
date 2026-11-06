"""Tests for Part 59's instrument (explainer/cs/disttheory/theory.py)."""

from __future__ import annotations

import unittest

from explainer.cs.disttheory import theory as T


class Theory(unittest.TestCase):
    def test_cole_vishkin(self):
        r = T.cole_vishkin(n=5000)
        self.assertTrue(r["proper"])
        self.assertLessEqual(r["rounds"], T.log_star(5000) + 5)

    def test_log_star(self):
        self.assertEqual(T.log_star(65536), 4)
        self.assertEqual(T.log_star(16), 3)

    def test_hexagon_violates(self):
        self.assertTrue(T.hexagon()["violations"])

    def test_sperner_odd(self):
        for s in range(20):
            self.assertTrue(T.sperner(k=6, seed=s)["odd"])

    def test_majority(self):
        r = T.majority(n=60, margin=4, trials=5)
        self.assertEqual(r["correct"], 1.0)


if __name__ == "__main__":
    unittest.main()
