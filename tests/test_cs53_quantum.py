"""Tests for Part 53's instruments (explainer/cs/quantum)."""

from __future__ import annotations

import math
import unittest

import numpy as np

from explainer.cs.quantum import algorithms as A
from explainer.cs.quantum import qec, sim


class Sim(unittest.TestCase):
    def test_qubit_selection_and_gate_shape(self):
        s = sim.State(2, basis=1)
        np.testing.assert_allclose(s.marginal([1, 0]), [0, 0, 1, 0])
        for qubits in ((0, 0), (-1,), (2,)):
            with self.assertRaises(ValueError):
                s.marginal(qubits)
        with self.assertRaises(ValueError):
            s.apply(sim.H, 0, 1)
        with self.assertRaises(ValueError):
            sim.State(2, -1)
        with self.assertRaises(ValueError):
            qec.repetition(ds=(2,), ps=[.1], trials=10)

    def test_gates_unitary(self):
        for U in (sim.H, sim.X, sim.Y, sim.Z, sim.S, sim.T, sim.rx(0.3), sim.ry(1.1), sim.rz(2.0)):
            self.assertTrue(sim.is_unitary(U))

    def test_apply_matches_kron(self):
        rng = np.random.default_rng(0)
        v = rng.standard_normal(8) + 1j * rng.standard_normal(8)
        s = sim.State(3)
        s.v = v.copy()
        s.apply(sim.H, 1)
        self.assertTrue(np.allclose(s.v, np.kron(np.kron(np.eye(2), sim.H), np.eye(2)) @ v))

    def test_bloch_poles(self):
        self.assertEqual(sim.bloch(np.array([1, 0])), (0.0, 0.0, 1.0))
        x, y, z = sim.bloch(np.array([1, 1]) / math.sqrt(2))
        self.assertAlmostEqual(x, 1.0)


class Algorithms(unittest.TestCase):
    def test_chsh(self):
        r = A.chsh(trials=2000)
        self.assertAlmostEqual(r["quantum"], math.cos(math.pi / 8) ** 2)
        self.assertEqual(r["classical"], 0.75)

    def test_dj(self):
        c = A.deutsch_jozsa()["cases"]
        self.assertAlmostEqual(c["constant 0"]["p_zero"], 1.0)
        self.assertLess(c["balanced (parity)"]["p_zero"], 1e-12)

    def test_bv_simon(self):
        self.assertEqual(A.bernstein_vazirani(0b1101)["measured"], 0b1101)
        self.assertEqual(A.simon(0b101)["found"], 0b101)

    def test_qft(self):
        r = A.qft_check(5)
        self.assertLess(r["max_diff_fft"], 1e-12)

    def test_shor(self):
        self.assertEqual(A.shor(15, 7)["factors"], [3, 5])
        self.assertEqual(A.shor(21, 2)["factors"], [3, 7])

    def test_grover(self):
        g = A.grover(n=6)
        self.assertEqual(g["best_iters"], 6)
        self.assertTrue(np.allclose(g["probs"], g["formula"]))

    def test_bb84(self):
        self.assertEqual(A.bb84()["error_rate"], 0.0)
        self.assertAlmostEqual(A.bb84(n=20000, eve=True)["error_rate"], 0.25, delta=0.02)


class Qec(unittest.TestCase):
    def test_three_qubit(self):
        for f in (None, 0, 1, 2):
            self.assertTrue(qec.three_qubit(flip=f)["restored"])

    def test_repetition_exact(self):
        r = qec.repetition(ds=(3,), ps=[0.1], trials=100_000)["rows"][0]
        self.assertAlmostEqual(r["exact"], 3 * 0.01 * 0.9 + 0.001)
        self.assertAlmostEqual(r["simulated"], r["exact"], delta=0.003)


if __name__ == "__main__":
    unittest.main()
