"""Chromatic harmony (Part 19): applied dominants, mixture, the Neapolitan, augmented sixths, the diminished seventh's
symmetry, enharmonic reinterpretation and the comma it hides, chromatic mediants and Cohn's hexatonic cycles, a
pathfinder for the shortest modulation between two keys, and a tension measure from Lerdahl's tonal pitch space.

Keys are (tonic pitch class, "major" | "minor"); chords are pitch-class tuples, root first, or key numbers.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from itertools import permutations

import numpy as np

from . import chords as CH
from . import tuning as TU

MAJOR = (0, 2, 4, 5, 7, 9, 11)
HARMONIC_MINOR = (0, 2, 3, 5, 7, 8, 11)
NAMES = ("C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B")


def key_name(k) -> str:
    return f"{NAMES[k[0] % 12]} {k[1]}"


def scale(k) -> tuple[int, ...]:
    return tuple((k[0] + s) % 12 for s in (MAJOR if k[1] == "major" else HARMONIC_MINOR))


def triad(root: int, kind: str) -> tuple[int, ...]:
    return tuple((root + o) % 12 for o in CH.offsets(kind))


def diatonic_triads(k) -> list[tuple[int, ...]]:
    """The seven triads of a key (harmonic minor for minor keys, with III as a major triad, not augmented)."""
    sc = scale(k)
    out = []
    for d in range(7):
        t = (sc[d], sc[(d + 2) % 7], sc[(d + 4) % 7])
        if k[1] == "minor" and d == 2:
            t = (sc[d], (sc[d] + 4) % 12, (sc[d] + 7) % 12)
        out.append(t)
    return out


# ---------------------------------------------------------------------------
# Applied dominants, mixture, the Neapolitan, augmented sixths
# ---------------------------------------------------------------------------
def applied_dominant(target_root: int, seventh: bool = True) -> tuple[int, ...]:
    """V7 (or V) of a chord: the major triad a fifth above its root, with a minor seventh."""
    r = (target_root + 7) % 12
    return triad(r, "7" if seventh else "major")


def borrowed(tonic: int = 0) -> dict[str, tuple[int, ...]]:
    """Chords of the parallel minor used in a major key (mixture)."""
    return {"iv": triad(tonic + 5, "minor"), "♭VI": triad(tonic + 8, "major"), "♭III": triad(tonic + 3, "major"),
            "♭VII": triad(tonic + 10, "major"), "ii°": triad(tonic + 2, "diminished"), "i": triad(tonic, "minor")}


def neapolitan(tonic: int = 0) -> tuple[int, ...]:
    """♭II, usually in first inversion (the 'Neapolitan sixth'): the major triad on the lowered second degree."""
    return triad(tonic + 1, "major")


def augmented_sixths(tonic: int = 0) -> dict[str, tuple[int, ...]]:
    """The Italian, French and German sixths of a key, bass first: ♭6 in the bass, ♯4 above, both resolving outward
    by semitone to the dominant's octave."""
    b6, s4, t, two, b3 = (tonic + 8) % 12, (tonic + 6) % 12, tonic % 12, (tonic + 2) % 12, (tonic + 3) % 12
    return {"Italian": (b6, t, s4), "French": (b6, t, two, s4), "German": (b6, t, b3, s4)}


# ---------------------------------------------------------------------------
# The diminished seventh: four leading notes, eight keys
# ---------------------------------------------------------------------------
def dim7(root: int) -> tuple[int, ...]:
    return tuple((root + 3 * i) % 12 for i in range(4))


def dim7_resolutions(chord) -> list[dict]:
    """Every key a diminished seventh chord can lead to: each of its four notes can be the leading note, a semitone
    below a tonic, major or minor."""
    out = []
    for lt in chord:
        tonic = (lt + 1) % 12
        for mode in ("minor", "major"):
            out.append({"leading": lt, "key": (tonic, mode)})
    return out


def german_as_dominant(tonic: int = 0) -> dict:
    """The German sixth of a key respelled: the same four keys are the dominant seventh of the key a semitone above
    the dominant's root... that is, of ♭II's key."""
    ger = augmented_sixths(tonic)["German"]
    v7 = triad((tonic + 8) % 12, "7")
    return {"german": ger, "dominant_of": ((tonic + 1) % 12, "major"), "same": set(ger) == set(v7)}


# ---------------------------------------------------------------------------
# The comma it hides: enharmonic cycles in pure intervals
# ---------------------------------------------------------------------------
def pure_cycle(step: Fraction, n: int) -> float:
    """How far n pure intervals of ``step`` miss the octave(s) they stand for, in cents (positive: too wide)."""
    total = TU.cents(step ** n)
    octaves = round(total / 1200)
    return total - 1200 * octaves


def enharmonic_drift() -> dict:
    """Three pure major thirds (5:4) fall short of an octave by the diesis; four pure minor thirds (6:5) overshoot it;
    in equal temperament both close exactly."""
    return {"three major thirds": pure_cycle(Fraction(5, 4), 3), "four minor thirds": pure_cycle(Fraction(6, 5), 4),
            "diesis": TU.cents(TU.DIESIS), "equal": 0.0}


# ---------------------------------------------------------------------------
# Chromatic mediants and the hexatonic cycle (Cohn 1996)
# ---------------------------------------------------------------------------
def plr(t, move: str):
    return {"P": CH.P, "L": CH.L, "R": CH.R}[move](t)


def hexatonic(start=(0, "major")) -> list:
    """Alternate P and L from a triad: six triads, each a single semitone from the last, and back to the start."""
    out, t = [start], start
    for k in range(6):
        t = plr(t, "P" if k % 2 == 0 else "L")
        out.append(t)
    return out


def chromatic_mediants(root: int = 0) -> list[tuple[int, str]]:
    """The major triads a major or minor third away from a major triad: they share one note and move the others by
    semitone or tone."""
    return [((root + d) % 12, "major") for d in (4, 8, 3, 9)]


def voice_leading(a, b) -> dict:
    """The least total motion (semitones) carrying chord a's notes onto chord b's (same size), and how each moves."""
    a, b = list(a), list(b)
    if len(a) != len(b):
        raise ValueError("chords of one size")
    best = None
    for perm in permutations(b):
        moves = [((y - x + 6) % 12) - 6 for x, y in zip(a, perm)]
        c = sum(abs(m) for m in moves)
        if best is None or c < best[0]:
            best = (c, moves, perm)
    return {"cost": int(best[0]), "moves": [int(m) for m in best[1]], "to": [int(x) for x in best[2]]}


# ---------------------------------------------------------------------------
# The shortest modulation: a graph of keys
# ---------------------------------------------------------------------------
KEYS = [(t, m) for m in ("major", "minor") for t in range(12)]


def pivots(a, b) -> list[tuple[int, ...]]:
    """Triads two keys share (a pivot chord can be heard in the first key and continue in the second)."""
    ta = {tuple(sorted(t)) for t in diatonic_triads(a)}
    return [t for t in diatonic_triads(b) if tuple(sorted(t)) in ta]


def edges(k, chromatic: bool = True) -> dict:
    """The keys reachable from k in one step, and how: a shared triad; and, with ``chromatic``, a diminished seventh
    respelled (to keys whose tonics are a minor third apart), a German sixth heard as a dominant seventh (to the key
    a semitone above), the Neapolitan heard as a tonic, subdominant or dominant elsewhere."""
    out = {}
    for j in KEYS:
        if j != k and pivots(k, j):
            out.setdefault(j, "a shared triad")
    if chromatic:
        lt = (k[0] + 11) % 12
        for c in dim7(lt):
            for m in ("major", "minor"):
                j = ((c + 1) % 12, m)
                if j != k:
                    out.setdefault(j, "a diminished seventh, respelled")
        out.setdefault(((k[0] + 1) % 12, "major"), "a German sixth heard as a dominant seventh")
        out.setdefault(((k[0] + 1) % 12, "minor"), "a German sixth heard as a dominant seventh")
        n = (k[0] + 1) % 12
        for j in (((n + 7) % 12, "major"), ((n + 5) % 12, "major"), (n, "major")):           # ♭II as IV, as V, as I
            if j != k:
                out.setdefault(j, "the Neapolitan heard as a chord of the new key")
    return out


def distances(start=(0, "major"), chromatic: bool = True) -> dict:
    """Breadth-first search: the fewest modulation steps from ``start`` to every key, and one shortest route."""
    dist, prev = {start: 0}, {start: None}
    q = deque([start])
    while q:
        k = q.popleft()
        for j, how in edges(k, chromatic).items():
            if j not in dist:
                dist[j] = dist[k] + 1
                prev[j] = (k, how)
                q.append(j)
    routes = {}
    for k in dist:
        path, cur = [], k
        while prev[cur] is not None:
            p, how = prev[cur]
            path.append((p, cur, how))
            cur = p
        routes[k] = list(reversed(path))
    return {"dist": dist, "routes": routes}


# ---------------------------------------------------------------------------
# Tension: Lerdahl's chord distance in tonal pitch space (2001)
# ---------------------------------------------------------------------------
def _fifths(a: int, b: int) -> int:
    d = (7 * (b - a)) % 12
    return min(d, 12 - d)


def basic_space(root: int, kind: str, k) -> list[set]:
    """Lerdahl's basic space: the root; root and fifth; the triad; the key's scale; all twelve notes."""
    t = triad(root, kind)
    fifth = (root + 7) % 12 if kind in ("major", "minor", "7") else t[2]
    return [{root}, {root, fifth}, set(t[:3]), set(scale(k)), set(range(12))]


def chord_distance(x, y) -> int:
    """δ(x → y) = i + j + k, for chords x, y given as (root, kind, key): i, the steps between their keys on the
    circle of fifths; j, the steps between their roots on the circle of fifths within the key; k, the notes in
    y's basic space that are not in x's, counted level by level."""
    (rx, kx, keyx), (ry, ky, keyy) = x, y
    i = _fifths(keyx[0] + (3 if keyx[1] == "minor" else 0), keyy[0] + (3 if keyy[1] == "minor" else 0))
    j = _fifths(rx, ry)
    bx, by = basic_space(rx, kx, keyx), basic_space(ry, ky, keyy)
    k = sum(len(by[l] - bx[l]) for l in range(4))
    return i + j + k


def tension_curve(progression) -> list[int]:
    """Sequential tension: the distance of each chord from the one before (the first is 0)."""
    return [0] + [chord_distance(a, b) for a, b in zip(progression, progression[1:])]


# ---------------------------------------------------------------------------
# The Tristan chord
# ---------------------------------------------------------------------------
TRISTAN = {"chord": (53, 59, 63, 68), "resolution": (52, 56, 62, 71)}      # F B D♯ G♯ (bar 2) to E G♯ D B (bar 3)
TRISTAN_READINGS = [
    {"name": "a French sixth in A minor", "notes": "F B D♯ A", "how": "G♯ is an appoggiatura to A; the chord resolves to V, E"},
    {"name": "a half-diminished seventh", "notes": "F G♯ B D♯ = F A♭ C♭ E♭", "how": "the 'Tristan chord' as a sonority: iiø7 of E♭ minor, or viiø7, heard for itself"},
    {"name": "an altered dominant of E", "notes": "B D♯ F A", "how": "V7 of V with a lowered fifth (F), G♯ an appoggiatura"},
    {"name": "no function at all", "notes": "F B D♯ G♯", "how": "Kurth (1920): a chord of pure tension, defined by its voice leading"},
]


def tristan_voice_leading() -> dict:
    a = [p % 12 for p in TRISTAN["chord"]]
    b = [p % 12 for p in TRISTAN["resolution"]]
    return voice_leading(a, b)
