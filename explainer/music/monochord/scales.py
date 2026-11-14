"""Monochord's scales (Part 12, *Scales and Modes*): which notes, out of all there could be.

    stack, gaps, gap_sizes, moments        fifths piled up and folded into an octave; how many sizes of step they leave
    Scale, MODES, modes, brightness        a scale as steps in semitones; its rotations; how bright each is
    maximally_even, evenness               the most even way to put k notes among n
    interval_vector, is_deep, myhill       how often each interval occurs; scales in which every count is different
    transpositions, common_tones           how many versions a scale has; what a transposition keeps
    necklaces, burnside, classify          every scale shape there is on twelve notes
    tetrachords, melakartas                fourths filled in three steps; the seventy-two parent scales of Carnatic music
    NAMED                                  the scales the part plays, as steps

A scale here is a tuple of steps that add up to the octave (in semitones for scales of the twelve notes, in cents
for others).  No manim.  Checked in ``tests/music/test_scales.py``.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations

import numpy as np

FIFTH = math.log2(1.5)            # a pure fifth, in octaves
NOTE_NAMES = ("C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B")


# ---------------------------------------------------------------------------
# Stacking a generator
# ---------------------------------------------------------------------------
def stack(n: int, generator: float = FIFTH, start: int = 0) -> np.ndarray:
    """``n`` notes a generator apart (a pure fifth by default), folded into one octave and sorted: positions in
    octaves, from 0 to 1.  ``start`` is how many fifths below the first note the stack begins."""
    return np.sort(((np.arange(n) - start) * generator) % 1.0)


def gaps(points) -> np.ndarray:
    """The steps between neighbouring notes round the octave, in cents."""
    p = np.sort(np.asarray(points, dtype=float))
    return 1200.0 * np.diff(np.concatenate([p, [p[0] + 1.0]]))


def gap_sizes(points, tol: float = 0.01) -> list[float]:
    """The different sizes of step, in cents, largest first."""
    out = []
    for g in sorted(gaps(points), reverse=True):
        if not out or abs(out[-1] - g) > tol:
            out.append(float(g))
    return out


def moments(limit: int = 60, generator: float = FIFTH) -> list[int]:
    """The numbers of notes at which a stack has steps of exactly two sizes (below ``limit``)."""
    return [n for n in range(2, limit + 1) if len(gap_sizes(stack(n, generator))) == 2]


# ---------------------------------------------------------------------------
# Scales of the twelve notes
# ---------------------------------------------------------------------------
def pcs(steps) -> tuple[int, ...]:
    """The notes of a scale as semitones above its first note."""
    out, t = [], 0
    for s in steps:
        out.append(t)
        t += s
    return tuple(out)


def steps_of(notes, n: int = 12) -> tuple[int, ...]:
    """The steps of a set of notes (numbers mod ``n``), starting from its lowest."""
    p = sorted(set(int(x) % n for x in notes))
    return tuple((b - a) % n or n for a, b in zip(p, p[1:] + p[:1]))


MAJOR = (2, 2, 1, 2, 2, 2, 1)
MODE_NAMES = ("Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian")     # the modes of the white keys from C, D, E ...
NAMED = {
    "major": MAJOR, "natural minor": (2, 1, 2, 2, 1, 2, 2), "harmonic minor": (2, 1, 2, 2, 1, 3, 1), "melodic minor": (2, 1, 2, 2, 2, 2, 1),
    "pentatonic": (2, 2, 3, 2, 3), "minor pentatonic": (3, 2, 2, 3, 2), "blues": (3, 2, 1, 1, 3, 2), "whole-tone": (2, 2, 2, 2, 2, 2),
    "octatonic": (2, 1, 2, 1, 2, 1, 2, 1), "chromatic": (1,) * 12, "double harmonic": (1, 3, 1, 2, 1, 3, 1),
}


def rotate(steps, k: int) -> tuple[int, ...]:
    return tuple(steps[k % len(steps):]) + tuple(steps[: k % len(steps)])


def modes(steps=MAJOR) -> list[tuple[int, ...]]:
    """Every rotation of a scale: the same notes, each taken as the first."""
    return [rotate(steps, k) for k in range(len(steps))]


MODES = dict(zip(MODE_NAMES, modes(MAJOR)))


def brightness(steps) -> int:
    """The sum of a scale's notes in semitones above its first: raising any note makes a scale brighter."""
    return sum(pcs(steps))


def by_brightness() -> list[tuple[str, tuple[int, ...]]]:
    """The seven modes from brightest to darkest: Lydian first, Locrian last.  Each differs from the next by one
    note lowered a semitone."""
    return sorted(MODES.items(), key=lambda kv: -brightness(kv[1]))


def fifths_position(name: str) -> int:
    """Where a mode's first note stands in the chain of fifths F C G D A E B that makes the white keys (F is 0)."""
    white = {"Lydian": 0, "Ionian": 1, "Mixolydian": 2, "Dorian": 3, "Aeolian": 4, "Phrygian": 5, "Locrian": 6}
    return white[name]


# ---------------------------------------------------------------------------
# Evenness, and what follows from it
# ---------------------------------------------------------------------------
def maximally_even(k: int, n: int = 12, offset: int = 0) -> tuple[int, ...]:
    """Clough and Douthett's most even ``k`` notes among ``n``: note j is at floor((n j + offset) / k)."""
    return tuple(sorted(((n * j + offset) // k) % n for j in range(k)))


def is_maximally_even(notes, n: int = 12) -> bool:
    k = len(set(notes))
    want = {steps_necklace(steps_of(maximally_even(k, n)))}
    return steps_necklace(steps_of(notes, n)) in want


def evenness(notes, n: int = 12) -> float:
    """How evenly notes are spread round the octave: the size of the k-th Fourier coefficient of the set, divided
    by k (1 for k notes equally spaced, less for any other set)."""
    p = np.array(sorted(set(notes)), dtype=float)
    k = len(p)
    return float(abs(np.exp(-2j * np.pi * k * p / n).sum()) / k)


def interval_vector(notes, n: int = 12) -> tuple[int, ...]:
    """How many pairs of notes are 1, 2, ... n/2 steps apart (the shorter way round)."""
    p = sorted(set(int(x) % n for x in notes))
    v = [0] * (n // 2)
    for a, b in combinations(p, 2):
        d = (b - a) % n
        v[min(d, n - d) - 1] += 1
    return tuple(v)


def is_deep(notes, n: int = 12) -> bool:
    """A deep scale: every interval occurs a different number of times."""
    v = interval_vector(notes, n)
    return len(set(v)) == len(v)


def common_tones(notes, shift: int, n: int = 12) -> int:
    """How many notes a scale keeps when it is moved up by ``shift`` steps."""
    p = set(int(x) % n for x in notes)
    return len(p & {(x + shift) % n for x in p})


def transpositions(notes, n: int = 12) -> int:
    """How many different sets of notes a scale's transpositions make."""
    p = frozenset(int(x) % n for x in notes)
    return len({frozenset((x + t) % n for x in p) for t in range(n)})


def myhill(steps) -> dict:
    """For each generic interval (a second, a third, ...), the sizes it comes in.  Myhill's property: exactly two
    sizes for every one of them."""
    k = len(steps)
    out = {}
    for span in range(1, k):
        sizes = sorted({sum(rotate(steps, i)[:span]) for i in range(k)})
        out[span + 1] = sizes
    return out


def has_myhill(steps) -> bool:
    return all(len(v) == 2 for v in myhill(steps).values())


# ---------------------------------------------------------------------------
# Every scale shape
# ---------------------------------------------------------------------------
def steps_necklace(steps) -> tuple[int, ...]:
    """A scale's steps turned to the rotation that comes first: the name of its shape, whatever note it starts on."""
    return min(rotate(steps, k) for k in range(len(steps)))


def necklaces(n: int = 12) -> list[tuple[int, ...]]:
    """Every shape of scale on ``n`` notes: the sets of notes, with sets that differ only by transposition counted
    once.  Each is given as steps (the empty set as ``()``)."""
    seen = set()
    for mask in range(1 << n):
        notes = [i for i in range(n) if mask >> i & 1]
        seen.add(steps_necklace(steps_of(notes, n)) if notes else ())
    return sorted(seen, key=lambda s: (len(s), s))


def euler_phi(m: int) -> int:
    return sum(1 for k in range(1, m + 1) if math.gcd(k, m) == 1)


def burnside(n: int = 12, colours: int = 2) -> Fraction:
    """The number of necklaces of ``n`` beads in ``colours`` colours, by Burnside's lemma: the average, over the n
    rotations, of the number of colourings each rotation leaves alone.  A rotation by n/d steps (there are phi(d)
    of each kind) leaves alone the colourings that repeat every n/d beads: colours^(n/d) of them."""
    return Fraction(sum(euler_phi(d) * colours ** (n // d) for d in range(1, n + 1) if n % d == 0), n)


def classify(n: int = 12) -> dict:
    """The necklaces of ``n`` notes, counted by how many notes they have."""
    out: dict[int, int] = {}
    for s in necklaces(n):
        out[len(s)] = out.get(len(s), 0) + 1
    return out


# ---------------------------------------------------------------------------
# Tetrachords and the melakartas
# ---------------------------------------------------------------------------
def tetrachords(span: int = 5, parts: int = 3) -> list[tuple[int, ...]]:
    """Every way to fill a fourth (five semitones) with three steps of at least a semitone."""
    out = []
    for a in range(1, span):
        for b in range(1, span - a):
            out.append((a, b, span - a - b))
    return out


def melakartas() -> list[tuple[int, ...]]:
    """The seventy-two parent scales of Carnatic music, by Venkatamakhin's rule: the first and fifth notes are
    fixed; the fourth is perfect or raised; the second and third take any two of the four places between the
    first note and the fourth (six ways), and the sixth and seventh any two of the four places above the fifth
    (six ways).  Each is a tuple of seven notes in semitones above the first."""
    out = []
    for ma in (5, 6):
        for ri, ga in combinations((1, 2, 3, 4), 2):
            for dha, ni in combinations((8, 9, 10, 11), 2):
                out.append((0, ri, ga, ma, 7, dha, ni))
    return out
