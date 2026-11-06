"""Tests for Part 56's instrument (explainer/cs/spectral)."""

from __future__ import annotations

import math
import unittest

import numpy as np

from explainer.cs.spectral import spectra as S


class Spectral(unittest.TestCase):
    def test_laplacian_psd_and_ones(self):
        A = S.random_regular(30, 4, seed=1)
        L = S.laplacian(A)
        self.assertTrue(np.allclose(L @ np.ones(30), 0))
        self.assertGreaterEqual(np.linalg.eigvalsh(L)[0], -1e-9)

    def test_cycle_spectrum(self):
        n = 12
        w = np.sort(np.linalg.eigvalsh(S.laplacian(S.cycle(n))))
        exact = np.sort([2 - 2 * math.cos(2 * math.pi * k / n) for k in range(n)])
        self.assertTrue(np.allclose(w, exact))

    def test_cheeger(self):
        for r in S.cheeger_check(trials=8):
            self.assertLessEqual(r["lower"], r["phi"] + 1e-9)
            self.assertLessEqual(r["phi"], r["sweep"] + 1e-9)
            self.assertLessEqual(r["sweep"], r["upper"] + 1e-9)

    def test_regular(self):
        A = S.random_regular(50, 3, seed=2)
        self.assertTrue(np.all(A.sum(axis=1) == 3))
        self.assertTrue(np.all(np.diag(A) == 0))

    def test_zigzag_regular(self):
        G = S.random_regular(20, 4, seed=3)
        H = S.random_regular(4, 3, seed=4) if False else S.cycle(4)
        Z = S.zigzag(G, H)
        self.assertTrue(np.allclose(Z.sum(axis=1), 4))
        self.assertTrue(np.allclose(Z, Z.T))

    def test_effective_resistance_path(self):
        A = np.zeros((4, 4))
        for i in range(3):
            A[i, i + 1] = A[i + 1, i] = 1
        self.assertAlmostEqual(S.effective_resistance(A)[0, 3], 3.0)

    def test_mixing_decreases(self):
        r = S.mixing(S.random_regular(40, 4, seed=5), steps=50)
        self.assertLess(r["tv"][-1], r["tv"][0])
        self.assertTrue(all(t <= b + 1e-9 for t, b in zip(r["tv"], r["bound"])))


if __name__ == "__main__":
    unittest.main()
