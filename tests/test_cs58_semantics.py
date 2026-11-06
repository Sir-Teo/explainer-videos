"""Tests for Part 58's instrument (explainer/cs/semantics/meaning.py)."""

from __future__ import annotations

import random
import unittest

from explainer.cs.semantics import meaning as M


class Semantics(unittest.TestCase):
    def test_three_semantics_agree(self):
        rng = random.Random(7)
        for _ in range(60):
            p = M.random_program(rng)
            v1 = M.small(p)[0]
            self.assertEqual(M._val(v1), M._val(M.big(p)))
            self.assertEqual(M._val(v1), M._val(M.cek(p)[0]))

    def test_factorial(self):
        self.assertEqual(M.fact_trace(5)["value"], 120)

    def test_kleene(self):
        rows = M.kleene()
        for a, b in zip(rows, rows[1:]):
            for n, v in a["defined"].items():
                self.assertEqual(b["defined"][n], v)

    def test_nbe(self):
        for r in M.nbe_experiment():
            self.assertEqual(r["nbe"], r["expected"])
            self.assertTrue(r["same_normal_form"])

    def test_bisim(self):
        b = M.bisim_examples()
        self.assertTrue(b["choice"]["same_traces"])
        self.assertFalse(b["choice"]["bisimilar"])
        self.assertTrue(b["vending"]["bisimilar"])


if __name__ == "__main__":
    unittest.main()
