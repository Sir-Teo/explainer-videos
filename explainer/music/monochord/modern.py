"""New scales and new rhythms (Part 28): symmetry, planing, the octatonic, additive and palindromic rhythm, and the
golden section on a null model.

The scales are subsets of the twelve pitch classes.  A scale has *limited transposition* when some transposition other
than by an octave maps it onto itself; Messiaen called the ones he used his modes of limited transposition.  Here every
one of the 4,096 subsets is examined, the symmetric ones are counted, and the claim that a passage "is octatonic" is
set against the chance that a random collection of its size fits an octatonic scale anyway.  No manim.
"""

from __future__ import annotations

import math
from itertools import combinations
from math import comb

import numpy as np

from . import key as K

N = 12
WHOLE_TONE = (0, 2, 4, 6, 8, 10)
OCTATONIC = (0, 1, 3, 4, 6, 7, 9, 10)                                  # half step, whole step, alternating
PENTATONIC = (0, 2, 4, 7, 9)
DIATONIC = (0, 2, 4, 5, 7, 9, 11)
MESSIAEN = {1: (0, 2, 4, 6, 8, 10), 2: (0, 1, 3, 4, 6, 7, 9, 10), 3: (0, 2, 3, 4, 6, 7, 8, 10, 11), 4: (0, 1, 2, 5, 6, 7, 8, 11),
            5: (0, 1, 5, 6, 7, 11), 6: (0, 2, 4, 5, 6, 8, 10, 11), 7: (0, 1, 2, 3, 5, 6, 7, 8, 9, 11)}


# ------------------------------------------------------------------------------------------------------ symmetry
def mask_of(pcs) -> int:
    m = 0
    for p in pcs:
        m |= 1 << (int(p) % N)
    return m


def pcs_of(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(N) if mask >> i & 1)


def rot(mask: int, k: int) -> int:
    k %= N
    return ((mask << k) | (mask >> (N - k))) & ((1 << N) - 1)


def period(pcs) -> int:
    """The smallest transposition (in semitones, 1 to 12) that maps the set onto itself; 12 means only the octave."""
    m = mask_of(pcs)
    return next(k for k in range(1, N + 1) if rot(m, k) == m)


def transpositions(pcs) -> int:
    """How many different sets the twelve transpositions make: 12 for most, fewer for symmetric ones."""
    return period(pcs)


def t_class(pcs) -> int:
    """A name for the set up to transposition: the smallest of its rotations, as a bit mask."""
    m = mask_of(pcs)
    return min(rot(m, k) for k in range(N))


def census() -> dict:
    """Every subset of the twelve pitch classes, up to transposition: how many classes there are of each size, and how
    many of those are symmetric (limited transposition), with their periods."""
    classes = {}
    for m in range(1 << N):
        c = t_class(pcs_of(m))
        classes.setdefault(c, pcs_of(c))
    by_size: dict = {}
    sym: dict = {}
    for c, p in classes.items():
        by_size[len(p)] = by_size.get(len(p), 0) + 1
        if 0 < len(p) < N and period(p) < N:
            sym.setdefault(len(p), []).append({"pcs": p, "period": period(p)})
    return {"classes": len(classes), "by_size": by_size, "symmetric": sym,
            "n_symmetric": sum(len(v) for v in sym.values())}


def is_union_of_cosets(pcs) -> bool:
    """A set has limited transposition exactly when it is a union of cosets of a subgroup of Z12 other than {0}: it
    repeats every d semitones for some proper divisor d of 12."""
    p = set(int(x) % N for x in pcs)
    return any(all((x + d) % N in p for x in p) for d in (1, 2, 3, 4, 6))


def messiaen_mode(pcs) -> int | None:
    """Which of Messiaen's seven modes the set is a transposition of, if any."""
    c = t_class(pcs)
    for k, m in MESSIAEN.items():
        if t_class(m) == c:
            return k
    return None


# ------------------------------------------------------------------------------------------------------ fitting
def collections(scale) -> list[frozenset]:
    """The distinct transpositions of a scale."""
    return sorted({frozenset((p + t) % N for p in scale) for t in range(N)}, key=sorted)


def fits(pcs, scale) -> bool:
    s = set(int(x) % N for x in pcs)
    return any(s <= c for c in collections(scale))


def chance_fits(k: int, scale) -> float:
    """The share of all k-note sets of pitch classes that lie inside some transposition of ``scale``: how often a
    passage using k pitch classes would 'be' in that scale by chance."""
    total = comb(N, k)
    cols = collections(scale)
    hits = sum(1 for s in combinations(range(N), k) if any(set(s) <= c for c in cols))
    return hits / total


def best_fit(pcs_weights: dict, scales: dict) -> dict:
    """For a passage's duration-weighted pitch classes, the share of time inside the best transposition of each scale."""
    total = sum(pcs_weights.values())
    out = {}
    for name, sc in scales.items():
        out[name] = max(sum(w for p, w in pcs_weights.items() if p % N in c) for c in collections(sc)) / total
    return out


# ------------------------------------------------------------------------------------------------- harmony
def planed(melody, shape=(0, -3, -7)) -> list:
    """Planing: the same chord shape under every melody note, moving in parallel (shape in semitones below the top)."""
    return [[(p + s, a, d) for p, a, d in melody] for s in shape]


def two_key_fit(pitches, weights=None) -> dict:
    """How well one key, and how well the best pair of keys mixed half and half, fits a set of notes."""
    dist = K.distribution(list(pitches), weights)
    one = K.correlations(dist)
    best1 = max(one, key=one.get)
    profiles = {k: K.profile_for(k) for k in K.KEYS}
    best2, r2 = None, -2.0
    for a, b in combinations(K.KEYS, 2):
        pr = profiles[a] + profiles[b]
        r = float(np.corrcoef(dist, pr)[0, 1])
        if r > r2:
            best2, r2 = (a, b), r
    return {"one": best1, "r_one": float(one[best1]), "two": best2, "r_two": r2}


# --------------------------------------------------------------------------------------------------- rhythm
def additive(n: int, parts=(2, 3)) -> list[tuple[int, ...]]:
    """Every way to fill n quick pulses with groups of 2 and 3 (Bartók's 'Bulgarian' rhythms), in order."""
    if n == 0:
        return [()]
    out = []
    for p in parts:
        if p <= n:
            out += [(p, *rest) for rest in additive(n - p, parts)]
    return out


def palindromes(n: int, values=(1, 2, 3, 4)) -> list[tuple[int, ...]]:
    """Every rhythm of total length n, made of the given durations, that reads the same backwards: Messiaen's
    non-retrogradable rhythms."""
    return [r for r in compositions(n, values) if r == r[::-1]]


def compositions(n: int, values) -> list[tuple[int, ...]]:
    if n == 0:
        return [()]
    out = []
    for v in values:
        if v <= n:
            out += [(v, *rest) for rest in compositions(n - v, values)]
    return out


def count_palindromes(n: int, values=(1, 2, 3, 4)) -> int:
    """Counted without listing: a palindrome is a half, an optional middle value, and the half reversed."""
    def c(m):
        f = [1] + [0] * m
        for i in range(1, m + 1):
            f[i] = sum(f[i - v] for v in values if v <= i)
        return f
    f = c(n)
    total = f[n // 2] if n % 2 == 0 else 0
    for v in values:
        if v <= n and (n - v) % 2 == 0:
            total += f[(n - v) // 2]
    return total


def accents(pulses: int, k: int, rng) -> list[int]:
    """k accents placed at random among ``pulses`` even pulses: a stand-in for a displaced-accent ostinato."""
    return sorted(int(x) for x in rng.choice(pulses, size=k, replace=False))


def metric_weight(i: int, groups=(4, 4)) -> int:
    """How strong pulse i is in a bar of the given beat groups (sixteenths): 3 on the downbeat, 2 on a beat, 1 on an
    eighth, 0 otherwise; for a 4/4 bar of sixteenths."""
    if i % 16 == 0:
        return 3
    if i % 4 == 0:
        return 2
    if i % 2 == 0:
        return 1
    return 0


def off_share(onsets, bar: int = 16) -> float:
    """The share of accents that fall off the beat."""
    return float(np.mean([metric_weight(i % bar) < 2 for i in onsets])) if onsets else 0.0


# ------------------------------------------------------------------------------------------------- the golden section
PHI = (math.sqrt(5) - 1) / 2


def golden_window(bars: int, tol: float) -> int:
    """How many of a piece's ``bars`` bar positions lie within ``tol`` bars of either golden point (0.382 or 0.618)."""
    pts = (PHI * bars, (1 - PHI) * bars)
    return sum(1 for b in range(1, bars + 1) if any(abs(b - g) <= tol for g in pts))


def golden_chance(bars: int, tol: float, landmarks: int) -> float:
    """The chance that at least one of ``landmarks`` events, each at a bar chosen at random, falls within ``tol`` bars of
    a golden point: the null model a golden-section claim must beat."""
    p = golden_window(bars, tol) / bars
    return 1.0 - (1.0 - p) ** landmarks


def fibonacci(n: int) -> list[int]:
    f = [1, 2]
    while len(f) < n:
        f.append(f[-1] + f[-2])
    return f[:n]


# ------------------------------------------------------------------------------------------------- tunings
def slendro(cents=(0, 240, 480, 720, 960)) -> list[float]:
    """An idealized slendro: five near-equal steps (measured Javanese sets vary, and are not equal)."""
    return list(cents)


def equal_cents(k: int) -> list[float]:
    return [1200.0 * i / k for i in range(k)]
