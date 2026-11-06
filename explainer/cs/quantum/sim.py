"""A state-vector simulator (Part 53).  n qubits are 2^n complex amplitudes; qubit 0 is the most significant bit
of the basis index (|q0 q1 ... q_{n-1}>).  Gates are unitary matrices applied by reshaping the state into a tensor
of shape (2,)*n; measurement probabilities follow the Born rule.  After Nielsen and Chuang, *Quantum Computation and
Quantum Information*."""

from __future__ import annotations

import math

import numpy as np

S2 = 1 / math.sqrt(2)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = S2 * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * math.pi / 4)]], dtype=complex)


def rx(t):
    return np.array([[math.cos(t / 2), -1j * math.sin(t / 2)], [-1j * math.sin(t / 2), math.cos(t / 2)]])


def ry(t):
    return np.array([[math.cos(t / 2), -math.sin(t / 2)], [math.sin(t / 2), math.cos(t / 2)]], dtype=complex)


def rz(t):
    return np.array([[np.exp(-1j * t / 2), 0], [0, np.exp(1j * t / 2)]])


def phase(t):
    return np.array([[1, 0], [0, np.exp(1j * t)]])


class State:
    def __init__(self, n: int, basis: int = 0):
        self.n = n
        self.v = np.zeros(2 ** n, dtype=complex)
        self.v[basis] = 1.0

    def copy(self):
        s = State(self.n)
        s.v = self.v.copy()
        return s

    def apply(self, U: np.ndarray, *qubits: int) -> "State":
        """Apply a k-qubit unitary to the given qubits (in order)."""
        k = len(qubits)
        t = self.v.reshape((2,) * self.n)
        t = np.moveaxis(t, qubits, range(k))
        sh = t.shape
        t = (U @ t.reshape(2 ** k, -1)).reshape(sh)
        t = np.moveaxis(t, range(k), qubits)
        self.v = t.reshape(-1)
        return self

    def controlled(self, U: np.ndarray, control: int, target: int) -> "State":
        C = np.eye(4, dtype=complex)
        C[2:, 2:] = U
        return self.apply(C, control, target)

    def cnot(self, c, t):
        return self.controlled(X, c, t)

    def probs(self) -> np.ndarray:
        return np.abs(self.v) ** 2

    def marginal(self, qubits) -> np.ndarray:
        p = self.probs().reshape((2,) * self.n)
        other = tuple(q for q in range(self.n) if q not in qubits)
        m = p.sum(axis=other) if other else p
        order = sorted(qubits)
        m = np.moveaxis(m, [order.index(q) for q in qubits], range(len(qubits)))
        return m.reshape(-1)

    def measure(self, rng, qubits=None) -> int:
        qubits = list(range(self.n)) if qubits is None else qubits
        p = self.marginal(qubits)
        return int(rng.choice(len(p), p=p / p.sum()))


def bloch(psi: np.ndarray) -> tuple[float, float, float]:
    """The Bloch vector (x, y, z) of a one-qubit state a|0> + b|1>."""
    a, b = psi
    return (float(2 * (np.conj(a) * b).real), float(2 * (np.conj(a) * b).imag), float(abs(a) ** 2 - abs(b) ** 2))


def bloch_paths(steps: int = 30) -> dict:
    """Trajectories on the Bloch sphere: H taking |0> to |+> (a half turn about the x+z axis), T and S turning
    about z, and an Rx sweep; each as a list of (x, y, z)."""
    out = {}
    def path(start, gen, t1):
        pts = []
        for k in range(steps + 1):
            t = t1 * k / steps
            U = _expm(-1j * t / 2 * gen)
            pts.append(bloch(U @ start))
        return pts
    zero = np.array([1, 0], dtype=complex)
    plus = S2 * np.array([1, 1], dtype=complex)
    nH = (X + Z) / math.sqrt(2)
    out["H on |0>"] = path(zero, nH, math.pi)
    out["T on |+>"] = path(plus, Z, math.pi / 4)
    out["S on |+>"] = path(plus, Z, math.pi / 2)
    out["Rx on |0>"] = path(zero, X, math.pi)
    return out


def _expm(M):
    w, V = np.linalg.eig(M)
    return V @ np.diag(np.exp(w)) @ np.linalg.inv(V)


def is_unitary(U, tol=1e-10) -> bool:
    return bool(np.allclose(U.conj().T @ U, np.eye(U.shape[0]), atol=tol))
