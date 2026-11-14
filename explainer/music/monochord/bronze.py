"""Monochord's bronze and silk (Part 36 of *Music, Built*): Chinese bells and pitch theory, the guqin, and gamelan.

    two_tone_bell(f, at)          a bell with two families of modes a third apart; striking the centre (``at='a'``)
                                  or the side (``'b'``) brings out one family or the other (a designed model)
    sanfen_lu(n)                  pitches by the 'add or subtract a third' rule: alternate 2/3 and 4/3 of a pipe
    fifths_closeness(n_max)       how near n pure fifths come to a whole number of octaves (Jing Fang's 53)
    PENTATONIC, modes             gong shang jue zhi yu and the five rotations
    HUI                           the guqin's thirteen studs as fractions of the string; harmonic pitches at each
    qin_harmonic(f, hui)          a harmonic touched at a hui (partial number and pitch)
    bar_partials                  a free bar's partial ratios (Part 9)
    dissonance_curve(partials)    Part 5's sensory dissonance for a given spectrum, over an octave
    slendro_like, pelog_like      illustrative tunings: near-equal five, unequal seven (no standard exists)
    paired(f, beat)               the 'shimmer' tuning: a partner instrument tuned to beat at a fixed rate
    colotomic(form, n)            which gong-family instruments strike on each beat of a cycle
    interlock(line)               split a fast figuration into two parts that each leave gaps and together fill every pulse
"""

from __future__ import annotations

from fractions import Fraction
from math import log2

import numpy as np

from .audio import SR
from .instruments import percussion as PC


# ------------------------------------------------------------------------------------------------- the two-tone bell
BELL_A = [1.0, 2.05, 2.92, 4.10, 5.30]                             # one mode family, roughly; ratios to its lowest
THIRD = 2 ** (300 / 1200)                                          # the second family a minor third higher


def two_tone_bell(f: float, at: str = "a", seconds: float = 2.5, third: float = THIRD, sr: int = SR) -> np.ndarray:
    """A bell with an almond-shaped section has two families of modes whose nodes and antinodes are swapped: a blow on
    the centre (the *sui*) excites family A and hardly B; a blow on the side (the *gu*) excites B.  Here the families
    are given designed ratios, B a minor third above A; a model of the principle, not of a measured bell."""
    fa = [f * r for r in BELL_A]
    fb = [f * third * r for r in BELL_A]
    wa, wb = (1.0, 0.08) if at == "a" else (0.08, 1.0)
    amps = [wa * 0.8 ** k for k in range(len(fa))] + [wb * 0.8 ** k for k in range(len(fb))]
    decays = [1.2 + 0.9 * k for k in range(len(fa))] * 2
    return PC.modal(fa + fb, amps, decays, seconds, sr)


# ------------------------------------------------------------------------------------------------- pitch theory
def cents(r) -> float:
    return 1200 * log2(float(r))


def sanfen_lu(n: int = 12) -> list[dict]:
    """The 'three-part loss and gain' rule (sanfen sunyi): from a pipe of length 81, take away a third (x 2/3, up a
    fifth) and add a third (x 4/3, down a fourth) alternately.  Each new length gives a pitch; folded into one octave
    the first five are the pentatonic, the first twelve the twelve lü."""
    L = Fraction(81)
    out = [{"k": 0, "length": L, "cents": 0.0}]
    for k in range(1, n):
        L = L * (Fraction(2, 3) if k % 2 == 1 else Fraction(4, 3))
        out.append({"k": k, "length": L, "cents": (cents(Fraction(81) / L)) % 1200})
    return out


def fifths_closeness(n_max: int = 60) -> list[dict]:
    """For each number n of pure fifths, the distance in cents from the nearest whole number of octaves."""
    out = []
    for n in range(1, n_max + 1):
        c = n * cents(Fraction(3, 2))
        k = round(c / 1200)
        out.append({"n": n, "octaves": k, "gap": c - 1200 * k})
    return out


PENTATONIC = {"gong": 0, "shang": 200, "jue": 400, "zhi": 700, "yu": 900}


def modes() -> dict:
    """The five modes: the pentatonic collection started on each of its notes."""
    notes = sorted(PENTATONIC.values())
    names = {v: k for k, v in PENTATONIC.items()}
    out = {}
    for i, root in enumerate(notes):
        out[names[root]] = [(n - root) % 1200 for n in notes[i:] + notes[:i]]
    return out


# ------------------------------------------------------------------------------------------------- the guqin
HUI = [Fraction(1, 8), Fraction(1, 6), Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2),
       Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(5, 6), Fraction(7, 8)]


def qin_harmonic(f: float, hui: Fraction) -> dict:
    """Touching the string lightly at fraction ``hui`` of its length leaves only the partials with a node there: the
    lowest is partial ``den`` (the fraction's denominator in lowest terms)."""
    n = hui.denominator
    return {"partial": n, "hz": f * n, "cents_above_open": cents(n)}


# ------------------------------------------------------------------------------------------------- gamelan
def bar_partials(n: int = 4) -> list[float]:
    """A free-free uniform bar's partial ratios (Part 9): 1, 2.756, 5.404, 8.933 ..."""
    beta = [4.7300, 7.8532, 10.9956, 14.1372, 17.2788]
    return [(b / beta[0]) ** 2 for b in beta[:n]]


def metallophone(f: float, seconds: float = 2.0, partials=None, sr: int = SR) -> np.ndarray:
    ratios = partials or bar_partials(4)
    amps = [1.0, 0.45, 0.25, 0.12][: len(ratios)]
    decays = [1.0, 2.5, 5.0, 8.0][: len(ratios)]
    return PC.modal([f * r for r in ratios], amps, decays, seconds, sr)


def _pair_roughness(f1, f2, a1, a2):
    """Plomp-Levelt roughness of two sine partials (Sethares's parametrization)."""
    s = 0.24 / (0.0207 * min(f1, f2) + 18.96)
    d = abs(f2 - f1)
    return a1 * a2 * (np.exp(-3.5 * s * d) - np.exp(-5.75 * s * d))


def dissonance_curve(ratios, amps=None, f0: float = 250.0, cents_range=(0, 1250), step: float = 2.0) -> tuple[np.ndarray, np.ndarray]:
    """Sensory dissonance of two tones with the given partial ratios, as the interval between them grows."""
    amps = amps or [0.88 ** k for k in range(len(ratios))]
    cs = np.arange(cents_range[0], cents_range[1] + step, step)
    out = []
    for c in cs:
        g = 2 ** (c / 1200)
        fa = [f0 * r for r in ratios]
        fb = [f0 * g * r for r in ratios]
        F = fa + fb
        A = list(amps) + list(amps)
        tot = 0.0
        for i in range(len(F)):
            for j in range(i + 1, len(F)):
                tot += _pair_roughness(F[i], F[j], A[i], A[j])
        out.append(tot)
    return cs, np.array(out)


def minima(cs, d, depth: float = 0.02) -> list[float]:
    """Local minima of a dissonance curve that are at least ``depth`` (relative) below their neighbourhood."""
    out = []
    for i in range(2, len(d) - 2):
        if d[i] < d[i - 1] and d[i] <= d[i + 1]:
            lo, hi = max(0, i - 25), min(len(d), i + 25)
            if d[lo:hi].max() - d[i] > depth * d.max():
                out.append(float(cs[i]))
    return out


# illustrative tunings, not measurements of any one gamelan (each gamelan has its own)
SLENDRO_LIKE = [0, 231, 474, 717, 955, 1200]
PELOG_LIKE = [0, 120, 270, 540, 670, 785, 950, 1200]


def paired(f: float, beat: float = 6.0) -> float:
    """The partner of a note at ``f`` tuned to beat ``beat`` times a second (the higher instrument of the pair)."""
    return f + beat


COLOTOMIC = {
    "lancaran": {"beats": 16, "gong": [16], "kenong": [4, 8, 12, 16], "kempul": [6, 10, 14], "ketuk": [1, 3, 5, 7, 9, 11, 13, 15]},
}


def colotomic(form: str = "lancaran") -> list[list[str]]:
    """For each beat of the cycle, the gong-family instruments that strike on it."""
    f = COLOTOMIC[form]
    out = []
    for b in range(1, f["beats"] + 1):
        out.append([k for k in ("gong", "kenong", "kempul", "ketuk") if b in f[k]])
    return out


def interlock(line: list) -> tuple[list, list]:
    """Split a figuration (one note per pulse) between two players, polos and sangsih, alternately: each has a gap
    on every other pulse; together they play every pulse exactly once."""
    a = [x if i % 2 == 0 else None for i, x in enumerate(line)]
    b = [x if i % 2 == 1 else None for i, x in enumerate(line)]
    return a, b
