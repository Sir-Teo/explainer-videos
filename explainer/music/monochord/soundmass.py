"""Sound itself (Part 30): tape operations, phasing, stochastic clouds, sieves, sound masses and spectra orchestrated.

After 1945 composers worked with recorded sound, chance and process instead of notes alone.  These are the
calculations behind the film's sketches: what a tape machine does to a sound (speed, reversal, a loop, a cut attack),
the patterns two loops of one figure pass through as they drift apart, a cloud of events whose onsets form a Poisson
process (Xenakis), Xenakis's sieves (scales and rhythms as unions of residue classes), the beating inside a cluster of
close pitches, and a recorded spectrum turned into a chord for an ensemble (spectral music).  No manim.
"""

from __future__ import annotations

import math
from itertools import product

import numpy as np

from . import SR


# ------------------------------------------------------------------------------------------------------------ tape
def speed(y: np.ndarray, factor: float) -> np.ndarray:
    """Play a tape ``factor`` times faster: everything up by log2(factor) octaves and shorter by the same factor."""
    n = int(len(y) / factor)
    x = np.arange(n) * factor
    return np.interp(x, np.arange(len(y)), y)


def reverse(y: np.ndarray) -> np.ndarray:
    return np.asarray(y)[::-1].copy()


def cut_attack(y: np.ndarray, seconds: float, sr: int = SR, fade: float = 0.03) -> np.ndarray:
    """Remove the first ``seconds`` of a sound and fade in what is left: Schaeffer's experiment with a bell."""
    k = int(seconds * sr)
    out = np.asarray(y, float)[k:].copy()
    f = int(fade * sr)
    out[:f] *= np.linspace(0, 1, f)
    return out


def loop(y: np.ndarray, times: int, crossfade: float = 0.01, sr: int = SR) -> np.ndarray:
    """A closed groove: the same fragment over and over."""
    y = np.asarray(y, float)
    c = int(crossfade * sr)
    seg = y.copy()
    seg[:c] *= np.linspace(0, 1, c)
    seg[-c:] *= np.linspace(1, 0, c)
    return np.tile(seg, times)


def attack_time(y: np.ndarray, sr: int = SR, frac: float = 0.9) -> float:
    """Seconds from the start until the envelope first reaches ``frac`` of its maximum."""
    env = np.abs(np.asarray(y, float))
    w = max(int(0.002 * sr), 1)
    env = np.convolve(env, np.ones(w) / w, mode="same")
    return float(np.argmax(env >= frac * env.max()) / sr)


# --------------------------------------------------------------------------------------------------------- phasing
def phase_patterns(pattern, shifts=None) -> list[dict]:
    """Two copies of a looped figure, the second ahead by k steps: for each k, the pairs that sound together, how many
    of them are unisons, and how many distinct pitch pairs (a measure of how rich the composite is)."""
    p = list(pattern)
    n = len(p)
    shifts = range(n) if shifts is None else shifts
    out = []
    for k in shifts:
        pairs = [(p[i], p[(i + k) % n]) for i in range(n)]
        out.append({"shift": int(k), "pairs": pairs, "unisons": sum(a == b for a, b in pairs),
                    "distinct": len({tuple(sorted(x)) for x in pairs}),
                    "intervals": sorted({abs(a - b) % 12 for a, b in pairs})})
    return out


def drift_times(n_notes: int, unit: float, faster: float, loops: int) -> tuple[np.ndarray, np.ndarray]:
    """Onset times of a figure looped ``loops`` times at ``unit`` seconds a note, and of a copy played ``faster`` times
    as fast: the second gains one note on the first every 1/(faster - 1) notes."""
    k = np.arange(n_notes * loops)
    return k * unit, k * unit / faster


# ---------------------------------------------------------------------------------------------------- stochastics
def poisson_onsets(rate: float, seconds: float, rng) -> np.ndarray:
    """Onsets of a Poisson process: exponential gaps of mean 1/rate."""
    t, out = 0.0, []
    while True:
        t += rng.exponential(1.0 / rate)
        if t >= seconds:
            return np.array(out)
        out.append(t)


def counts_per_cell(onsets, seconds: float, cell: float) -> np.ndarray:
    edges = np.arange(0.0, seconds + 1e-9, cell)
    return np.histogram(onsets, edges)[0]


def poisson_pmf(k: int, lam: float) -> float:
    return math.exp(-lam) * lam ** k / math.factorial(k)


def glissandi(n: int, seconds: float, lo: float, hi: float, rng, max_len: float = 2.5, target=None) -> list[dict]:
    """n straight glissandi in (time, key number): random starts and slopes, or drawn towards a ``target(t)`` curve."""
    out = []
    for _ in range(n):
        t0 = rng.uniform(0, seconds - 0.5)
        d = rng.uniform(0.5, max_len)
        p0 = rng.uniform(lo, hi) if target is None else target(t0) + rng.normal(0, 3)
        p1 = rng.uniform(lo, hi) if target is None else target(min(t0 + d, seconds)) + rng.normal(0, 3)
        out.append({"t0": float(t0), "t1": float(min(t0 + d, seconds)), "p0": float(p0), "p1": float(p1)})
    return out


# ------------------------------------------------------------------------------------------------------------ sieves
def sieve(terms, n: int = 12) -> list[int]:
    """A Xenakis sieve: a union of intersections of residue classes.  ``terms`` is a list of intersections, each a
    list of (modulus, residue) pairs: [[(3, 2), (4, 0)], [(3, 1), (4, 1)]] means (3n+2 and 4n) or (3n+1 and 4n+1)."""
    return [x for x in range(n) if any(all(x % m == r for m, r in term) for term in terms)]


WHOLE_TONE_SIEVE = [[(2, 0)]]
OCTATONIC_SIEVE = [[(3, 0)], [(3, 1)]]
# C major from moduli 3 and 4: by the Chinese remainder theorem each pitch class is one pair of residues
DIATONIC_SIEVE = [[(3, 0), (4, 0)], [(3, 2), (4, 2)], [(3, 1), (4, 0)], [(3, 2), (4, 1)], [(3, 1), (4, 3)], [(3, 0), (4, 1)], [(3, 2), (4, 3)]]


# ---------------------------------------------------------------------------------------------------------- masses
def cluster(center: float, width: float, voices: int) -> list[float]:
    """Key numbers of a cluster: ``voices`` pitches spread evenly over ``width`` semitones around ``center``."""
    if voices == 1:
        return [center]
    return list(np.linspace(center - width / 2, center + width / 2, voices))


def beat_rates(pitches) -> list[float]:
    """The beat frequencies between neighbouring pitches of a cluster, in Hz."""
    f = sorted(440.0 * 2 ** ((p - 69) / 12) for p in pitches)
    return [b - a for a, b in zip(f, f[1:])]


# --------------------------------------------------------------------------------------------------------- spectra
def harmonic_levels(y: np.ndarray, f0: float, count: int = 16, sr: int = SR) -> list[float]:
    """The level (dB relative to the strongest) of each of the first ``count`` harmonics of f0 in a sound."""
    x = np.asarray(y, float)
    x = x[len(x) // 4: 3 * len(x) // 4]
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)), 4 * len(x)))
    df = sr / (4 * len(x))
    lv = []
    for h in range(1, count + 1):
        i = int(round(h * f0 / df))
        w = max(int(0.03 * f0 / df), 2)
        lv.append(float(spec[max(i - w, 0): i + w + 1].max()) if i + w < len(spec) else 0.0)
    ref = max(lv)
    return [float(20 * np.log10(max(v, 1e-12) / ref)) for v in lv]


def orchestrate(f0: float, levels, floor_db: float = -40.0) -> list[dict]:
    """A spectrum as a chord: each harmonic above ``floor_db`` becomes a note at its exact frequency (as a fractional
    key number) with its own loudness, assigned to an instrument by register."""
    out = []
    for h, db in enumerate(levels, start=1):
        if db < floor_db:
            continue
        f = h * f0
        key = 69 + 12 * math.log2(f / 440.0)
        inst = "piano" if key < 52 else ("bowed" if key < 84 else "voice")
        out.append({"harmonic": h, "hz": f, "key": key, "db": db, "inst": inst, "cents_from_et": 100 * (key - round(key))})
    return out


def harmonic_key(h: int, f0: float) -> float:
    return 69 + 12 * math.log2(h * f0 / 440.0)
