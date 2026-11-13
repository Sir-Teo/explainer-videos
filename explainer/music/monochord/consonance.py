"""Consonance, six ways (Part 5, *Consonance*).  Each theory of why some notes belong together is a function here, so
that the film can run them all on the same intervals and show where each one fails.

    number        Pythagoras, Galileo, Euler: properties of the ratio p:q itself
    roughness     Helmholtz, Plomp and Levelt, Sethares: beating between partials inside one band of the ear
    harmonicity   Stumpf, Terhardt: how well the partials fit one harmonic series (and so fuse into one pitch)

No manim.  The roughness model is the Plomp-Levelt curve as parameterised by Sethares (1993); it is checked against
his published minima for a harmonic tone.  The harmonicity measure uses Part 4's pitch model (``ear.py``).
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

# ---------------------------------------------------------------------------
# Number
# ---------------------------------------------------------------------------
JUST = {  # the just intervals within an octave, by name
    "unison": (1, 1), "minor second": (16, 15), "major second": (9, 8), "minor third": (6, 5), "major third": (5, 4),
    "fourth": (4, 3), "tritone": (45, 32), "fifth": (3, 2), "minor sixth": (8, 5), "major sixth": (5, 3),
    "minor seventh": (16, 9), "major seventh": (15, 8), "octave": (2, 1),
}


def factorize(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def euler_gradus(p: int, q: int) -> int:
    """Euler's *gradus suavitatis* (1739) of the interval p:q: 1 + the sum of (prime - 1) over the prime factors, with
    multiplicity, of the least common multiple of p and q.  Smaller is sweeter."""
    f = Fraction(p, q)
    n = math.lcm(f.numerator, f.denominator)
    return 1 + sum((prime - 1) * k for prime, k in factorize(n).items())


def coincidence(p: int, q: int) -> Fraction:
    """Galileo's measure (1638): of the pulses of the two notes of p:q, the fraction that arrive together.  In one
    repeat of the pattern the notes give p and q pulses, and one pair coincides."""
    f = Fraction(p, q)
    return Fraction(2, f.numerator + f.denominator)


def tenney(p: int, q: int) -> float:
    """The harmonic distance of Tenney: log2(p q) for p:q in lowest terms."""
    f = Fraction(p, q)
    return math.log2(f.numerator * f.denominator)


def nearest_ratio(x: float, limit: int = 16) -> tuple[int, int]:
    """The simplest ratio near x (denominator up to ``limit``)."""
    f = Fraction(x).limit_denominator(limit)
    return f.numerator, f.denominator


# ---------------------------------------------------------------------------
# Beats
# ---------------------------------------------------------------------------
def beat_rate(f1: float, f2: float) -> float:
    """Two pure tones together swell and fade ``|f1 - f2|`` times a second."""
    return abs(f1 - f2)


def beating(f1: float, f2: float, seconds: float, sr: int = 48_000) -> tuple[np.ndarray, np.ndarray]:
    """The sum of two equal pure tones, and its envelope ``2 |cos(pi (f1 - f2) t)|``."""
    t = np.arange(int(seconds * sr)) / sr
    return np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t), 2 * np.abs(np.cos(np.pi * (f1 - f2) * t))


# ---------------------------------------------------------------------------
# Roughness: Plomp and Levelt's curve, as fitted by Sethares
# ---------------------------------------------------------------------------
B1, B2, XSTAR, S1, S2 = 3.5, 5.75, 0.24, 0.0207, 18.96
PEAK = math.log(B2 / B1) / (B2 - B1)        # where exp(-B1 x) - exp(-B2 x) is greatest: 0.2206


def pl_curve(x):
    """Plomp and Levelt's curve in its own units: x is the separation of two pure tones divided by the separation of
    greatest roughness (about a quarter of a critical band); the curve is scaled to peak at 1."""
    x = np.asarray(x, dtype=float) * PEAK
    peak = math.exp(-B1 * PEAK) - math.exp(-B2 * PEAK)
    return (np.exp(-B1 * x) - np.exp(-B2 * x)) / peak


def worst_separation(f: float) -> float:
    """The separation (Hz) at which two pure tones near frequency f are roughest."""
    return PEAK / XSTAR * (S1 * f + S2)


def pair_roughness(f1, f2, a1=1.0, a2=1.0):
    """The roughness of two pure tones (Sethares 1993): zero in unison, greatest about a quarter of a critical band
    apart, gone by about one band.  Amplitudes enter through the weaker of the two."""
    f1, f2 = np.asarray(f1, dtype=float), np.asarray(f2, dtype=float)
    lo = np.minimum(f1, f2)
    s = XSTAR / (S1 * lo + S2)
    d = np.abs(f2 - f1)
    return np.minimum(a1, a2) * (np.exp(-B1 * s * d) - np.exp(-B2 * s * d))


def roughness(freqs, amps=None) -> float:
    """The total roughness of a set of partials: every pair, added up."""
    f = np.asarray(freqs, dtype=float)
    a = np.ones(len(f)) if amps is None else np.asarray(amps, dtype=float)
    i, j = np.triu_indices(len(f), 1)
    return float(np.sum(pair_roughness(f[i], f[j], a[i], a[j])))


def harmonic_partials(f0: float, n: int = 7, rolloff: float = 0.88, stretch: float = 2.0) -> tuple[np.ndarray, np.ndarray]:
    """The partials of a tone: frequencies ``f0 * k^(log2 stretch)`` (``stretch=2`` is harmonic; 2.1 stretches every
    octave of the series to a ratio of 2.1) and amplitudes ``rolloff^(k-1)``."""
    k = np.arange(1, n + 1)
    return f0 * k ** math.log2(stretch), rolloff ** (k - 1.0)


def dyad_roughness(ratio: float, f0: float = 261.63, n: int = 7, rolloff: float = 0.88, stretch: float = 2.0) -> float:
    """The roughness of two tones of the same timbre a ratio apart."""
    f, a = harmonic_partials(f0, n, rolloff, stretch)
    return roughness(np.concatenate([f, ratio * f]), np.concatenate([a, a]))


def dissonance_curve(ratios, f0: float = 261.63, n: int = 7, rolloff: float = 0.88, stretch: float = 2.0) -> np.ndarray:
    """Roughness against interval, for a timbre: Sethares's dissonance curve."""
    return np.array([dyad_roughness(float(r), f0, n, rolloff, stretch) for r in np.asarray(ratios)])


def minima(ratios, curve, depth: float = 0.0) -> list[float]:
    """The interior local minima of a curve (those at least ``depth`` below both neighbouring maxima)."""
    r, c = np.asarray(ratios), np.asarray(curve)
    out = []
    for i in range(1, len(c) - 1):
        if c[i] < c[i - 1] and c[i] <= c[i + 1]:
            left = c[:i][::-1]
            right = c[i + 1:]
            lmax = left[0]
            for v in left:
                if v < lmax:
                    break
                lmax = v
            rmax = right[0]
            for v in right:
                if v < rmax:
                    break
                rmax = v
            if min(lmax, rmax) - c[i] >= depth:
                out.append(float(r[i]))
    return out


def chord_roughness(ratios, f0: float = 261.63, n: int = 7, rolloff: float = 0.88, stretch: float = 2.0) -> float:
    """The roughness of a chord whose notes stand at ``ratios`` above ``f0`` (1 for the lowest)."""
    f, a = harmonic_partials(f0, n, rolloff, stretch)
    return roughness(np.concatenate([r * f for r in ratios]), np.concatenate([a for _ in ratios]))


# ---------------------------------------------------------------------------
# Harmonicity
# ---------------------------------------------------------------------------
def chord_wave(ratios, f0: float = 261.63, seconds: float = 0.4, sr: int = 48_000, n: int = 7, rolloff: float = 0.88,
               stretch: float = 2.0) -> np.ndarray:
    """A chord as sound: sines, one per partial of each note."""
    t = np.arange(int(seconds * sr)) / sr
    f, a = harmonic_partials(f0, n, rolloff, stretch)
    y = np.zeros(len(t))
    for r in ratios:
        for fk, ak in zip(r * f, a):
            if fk < 0.45 * sr:
                y += ak * np.sin(2 * np.pi * fk * t)
    return y


LOWEST_PITCH = 30.0      # hertz: below about this, a repetition is heard as a rhythm, not as a pitch


def periodicity(ratios, f0: float = 261.63, **kw) -> tuple[np.ndarray, np.ndarray]:
    """Part 4's summary autocorrelation of a chord, weighted by how well the ear can use each delay: fully at short
    delays, not at all beyond the period of the lowest pitch (a linear taper).  Returns ``(delays in s, strength)``."""
    from . import ear

    y = chord_wave(ratios, f0, **kw)
    lags, s = ear.summary_acf(y, 48_000, max_lag=1.0 / LOWEST_PITCH)
    floor = float(np.min(s[int(48_000 / (2 * f0)):]))
    return lags, np.maximum(1.0 - lags * LOWEST_PITCH, 0.0) * (s - floor) / (1.0 - floor)


def harmonicity(ratios, f0: float = 261.63, **kw) -> tuple[float, float]:
    """How well a chord fuses into one pitch: the pitch (Hz) and the strength (0 to 1) of the strongest repetition
    the ear can use, at a period no shorter than the lowest note's.  A chord whose partials all belong to one
    harmonic series repeats at that series's period; the lower that series's fundamental, the weaker the fusion."""
    lags, w = periodicity(ratios, f0, **kw)
    a = int(48_000 / (f0 * 1.03))
    k = a + int(np.argmax(w[a:]))
    return 48_000 / k, float(w[k])


def fundamental_bass(ratios_pq) -> Fraction:
    """The fundamental of the harmonic series that a chord of exact ratios belongs to, as a fraction of its lowest
    note: for 4:5:6 it is 1/4 (two octaves below), for 10:12:15 it is 1/10."""
    fr = [Fraction(p, q) for p, q in ratios_pq]
    den = math.lcm(*[f.denominator for f in fr])
    nums = [int(f * den) for f in fr]
    g = math.gcd(*nums)
    return Fraction(g, den)
