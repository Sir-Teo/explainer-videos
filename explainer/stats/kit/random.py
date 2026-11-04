"""Randomness on demand (Part 7): generators, samplers and the simulation-study harness.

Generators (chapter 1): ``randu`` (IBM, 1960s: bad on purpose), ``lcg`` (Lehmer 1949), ``PCG32`` (O'Neill 2014).
Samplers: ``inverse_cdf`` (chapter 2), ``rejection`` (chapter 3, von Neumann 1951), ``box_muller`` (1958),
``marsaglia_tsang`` gamma (2000), ``AliasTable`` (Walker 1974; Vose 1991) (chapter 4).
Simulation studies (chapter 6, after Morris, White & Crowther 2019): ``streams`` gives independent, reproducible
generators; ``mc_se`` the Monte Carlo standard error of a mean or a proportion; ``simulate`` runs an estimator over
replicate data sets and reports bias, empirical SE, coverage and their Monte Carlo errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

M31, M32, M64 = 2 ** 31, 2 ** 32, 2 ** 64


def randu(seed: int, n: int) -> np.ndarray:
    """IBM's RANDU: x <- 65539 x mod 2^31 (integers).  Consecutive triples lie on 15 planes, since
    x_{k+2} = 6 x_{k+1} - 9 x_k (mod 2^31) (Marsaglia 1968)."""
    out = np.empty(n, dtype=np.int64)
    x = seed
    for i in range(n):
        x = (65539 * x) % M31
        out[i] = x
    return out


def lcg(a: int, c: int, m: int, seed: int, n: int) -> list[int]:
    """The linear congruential generator x <- (a x + c) mod m.  Full period m iff (Hull & Dobell 1962): c and m
    coprime; a - 1 divisible by every prime factor of m; and by 4 if 4 divides m."""
    out, x = [], seed
    for _ in range(n):
        x = (a * x + c) % m
        out.append(x)
    return out


class PCG32:
    """PCG32 (XSH RR): a 64-bit LCG state, output through a xorshift and a rotation chosen by the top bits
    (M. E. O'Neill, 2014).  ``stream`` selects one of 2^63 independent sequences."""

    MULT = 6364136223846793005

    def __init__(self, seed: int = 42, stream: int = 54):
        self.inc = ((stream << 1) | 1) % M64
        self.state = 0
        self.next32()
        self.state = (self.state + seed) % M64
        self.next32()

    def next32(self) -> int:
        old = self.state
        self.state = (old * self.MULT + self.inc) % M64
        xorshifted = (((old >> 18) ^ old) >> 27) & 0xFFFFFFFF
        rot = old >> 59
        return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF

    def random(self, n: int) -> np.ndarray:
        """n uniforms on [0, 1), with 32 bits each."""
        return np.array([self.next32() for _ in range(n)], dtype=np.float64) / M32


def inverse_cdf(quantile: Callable, u) -> np.ndarray:
    """X = F^{-1}(U) has CDF F when U is uniform (the probability integral transform run backwards)."""
    return quantile(np.asarray(u, float))


def discrete_inverse(pmf, u) -> np.ndarray:
    """Inversion for a law on 0, 1, ..., k - 1: the first k with F(k) > u."""
    return np.searchsorted(np.cumsum(pmf), np.asarray(u, float), side="right")


def rejection(target_pdf: Callable, M: float, n: int, rng: np.random.Generator, lo=0.0, hi=1.0):
    """Rejection from a uniform box on [lo, hi] x [0, M] (M >= max of the target density times (hi - lo)):
    accepted x's follow the target; the acceptance rate is 1 / (M (hi - lo))."""
    out, tries = [], 0
    while len(out) < n:
        x = rng.uniform(lo, hi, n)
        y = rng.uniform(0, M, n)
        tries += n
        out.extend(x[y <= target_pdf(x)].tolist())
    return np.asarray(out[:n]), len(out) / tries


def box_muller(u1, u2):
    """Two independent standard normals from two uniforms (Box & Muller 1958): R = sqrt(-2 log U1), angle 2 pi U2."""
    r = np.sqrt(-2 * np.log(u1))
    return r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)


def marsaglia_tsang(alpha: float, n: int, rng: np.random.Generator):
    """Gamma(alpha, 1) for alpha >= 1 (Marsaglia & Tsang 2000): d = alpha - 1/3, c = 1/sqrt(9d); propose
    v = (1 + c Z)^3 and accept with a squeeze-free log test.  Returns draws and the acceptance rate."""
    d = alpha - 1 / 3
    c = 1 / np.sqrt(9 * d)
    out, tries = [], 0
    while len(out) < n:
        z = rng.standard_normal(n)
        u = rng.random(n)
        tries += n
        v = (1 + c * z) ** 3
        ok = v > 0
        acc = ok & (np.log(u, where=ok, out=np.full(n, np.inf)) < 0.5 * z * z + d - d * np.where(ok, v, 1) +
                    d * np.log(np.where(ok, v, 1)))
        out.extend((d * v[acc]).tolist())
    return np.asarray(out[:n]), len(out) / tries


@dataclass
class AliasTable:
    """Walker's alias method (1974), in Vose's form (1991): O(1) draws from a finite law.  Pick a column uniformly;
    keep it with probability ``prob[col]``, else take ``alias[col]``."""

    prob: np.ndarray
    alias: np.ndarray

    @classmethod
    def build(cls, p) -> "AliasTable":
        n = len(p)
        q = np.asarray(p, float) * n / np.sum(p)
        prob, alias = np.ones(n), np.arange(n)
        small = [i for i in range(n) if q[i] < 1]
        large = [i for i in range(n) if q[i] >= 1]
        while small and large:
            s, big = small.pop(), large.pop()
            prob[s], alias[s] = q[s], big
            q[big] -= 1 - q[s]
            (small if q[big] < 1 else large).append(big)
        return cls(prob, alias)

    def draw(self, n: int, rng: np.random.Generator) -> np.ndarray:
        col = rng.integers(0, len(self.prob), n)
        return np.where(rng.random(n) < self.prob[col], col, self.alias[col])


def streams(seed: int, k: int) -> list[np.random.Generator]:
    """k independent, reproducible generators from one seed (numpy's SeedSequence spawning)."""
    return [np.random.Generator(np.random.PCG64(s)) for s in np.random.SeedSequence(seed).spawn(k)]


def mc_se(values) -> float:
    """Monte Carlo standard error of the mean of replicate values: sd / sqrt(R).  For a coverage proportion c,
    this is sqrt(c (1 - c) / R)."""
    v = np.asarray(values, float)
    return float(v.std(ddof=1) / np.sqrt(len(v)))


def simulate(dgp: Callable, method: Callable, truth: float, reps: int, seed: int) -> dict:
    """A simulation study in miniature (ADEMP: Morris, White & Crowther 2019).  ``dgp(rng)`` makes a data set;
    ``method(data)`` returns (estimate, lower, upper).  Reports bias, empirical SE and coverage, each with its
    Monte Carlo standard error, from ``reps`` replicates on one reproducible stream."""
    rng = np.random.Generator(np.random.PCG64(seed))
    est, cov = np.empty(reps), np.empty(reps)
    for r in range(reps):
        e, lo, hi = method(dgp(rng))
        est[r], cov[r] = e, lo <= truth <= hi
    bias = est.mean() - truth
    emp_se = est.std(ddof=1)
    c = cov.mean()
    return {"bias": float(bias), "bias_mcse": float(emp_se / np.sqrt(reps)), "emp_se": float(emp_se),
            "emp_se_mcse": float(emp_se / np.sqrt(2 * (reps - 1))), "coverage": float(c),
            "coverage_mcse": float(np.sqrt(c * (1 - c) / reps)), "reps": reps}
