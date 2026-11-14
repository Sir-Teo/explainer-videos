"""Monochord's geometry of chords (Part 32 of *Music, Built*).

Chords as points in a quotient space (Tymoczko 2006; Callender, Quinn and Tymoczko 2008): an ordered chord of n notes
is a point of R^n; octave equivalence (O) folds it into a torus, permutation (P) into an orbifold; the two-note space is a
Möbius strip, the three-note space a twisted triangular prism whose cross-section is a triangle with the augmented triad
at its centre.  A voice leading is a path; its size is a norm of the voices' displacements.  Everything here works on
pitch classes as real numbers modulo 12 (so microtonal chords are allowed) unless it says otherwise.

    vl(a, b)                       the smallest voice leading between two chords of the same size: (size, moves)
    dyad_strip(a, b)               a two-note chord's place on the Möbius strip: (centre, interval)
    shape(chord)                   a three-note chord's step intervals, a point of the triangle
    evenness(chord)                Euclidean distance to the nearest perfectly even chord
    transposition_vl(chord)        the smallest voice leading to each of the chord's own transpositions
    optic_counts(n)                chord types of n notes under each combination of O, P, T, I, C (12-ET)
    dft(pcs)                       magnitudes of the discrete Fourier transform of a pitch-class set
    bach_voice_leading(book)       Bach's voice leadings against the minimal ones between the same chords
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, permutations

import numpy as np

N = 12


def pc_dist(a: float, b: float, n: float = N) -> float:
    """The shortest distance between two pitch classes on the circle."""
    d = (b - a) % n
    return min(d, n - d)


def signed(a: float, b: float, n: float = N) -> float:
    """The shortest signed move from a to b (ties go up)."""
    d = (b - a) % n
    return d if d <= n / 2 else d - n


def vl(a, b, norm: str = "taxicab") -> tuple:
    """The smallest voice leading from chord a to chord b (pitch classes, equal sizes): every assignment of a's voices to
    b's notes is tried, each voice moving the short way round.  Returns (size, moves) with moves[i] the signed move of
    a's i-th note (a in the order given).  Norms: 'taxicab' (sum of moves), 'euclid', 'max'."""
    a, b = list(a), list(b)
    if len(a) != len(b):
        raise ValueError("chords must have the same number of notes")
    best = None
    for p in set(permutations(range(len(b)))):
        mv = [signed(a[i], b[p[i]]) for i in range(len(a))]
        s = _norm(mv, norm)
        if best is None or s < best[0] - 1e-12:
            best = (s, mv)
    return best


def _norm(mv, norm: str) -> float:
    m = np.abs(np.asarray(mv, float))
    if norm == "taxicab":
        return float(m.sum())
    if norm == "euclid":
        return float(np.sqrt((m ** 2).sum()))
    if norm == "max":
        return float(m.max())
    raise ValueError(norm)


# ---------------------------------------------------------------------------------------------------- two notes
def dyad_strip(a: float, b: float) -> tuple:
    """A two-note chord's point on the Möbius strip: (centre, interval) with interval in [0, 12] and centre in [0, 6).
    The strip's ends are glued with a twist: (c, d) is the same chord as (c + 6, 12 - d).  Unisons lie on the edge
    (d = 0 or 12), tritones on the centre line (d = 6)."""
    x1, x2 = sorted((a % N, b % N))
    d = x2 - x1
    c = (x1 + x2) / 2.0
    while c >= 6:
        c -= 6
        d = 12 - d
    return c, d


def dyads() -> list:
    """The 78 two-note chords of 12-ET (unordered, octave-free, unisons included)."""
    return [(i, j) for i, j in combinations_with_replacement(range(N), 2)]


# -------------------------------------------------------------------------------------------------- three notes
def shape(chord) -> tuple:
    """A three-note chord's step intervals (a, b, c), summing to 12, starting from the note that gives the smallest
    rotation: the chord's place in the triangle of shapes (transposition forgotten)."""
    x = sorted(v % N for v in chord)
    steps = [x[1] - x[0], x[2] - x[1], 12 - (x[2] - x[0])]
    rots = [tuple(steps[i:] + steps[:i]) for i in range(3)]
    return min(rots)


def triangle_xy(steps) -> tuple:
    """Plot a triple of steps (summing to 12) in an equilateral triangle: vertex k is the chord with all 12 in step k."""
    V = np.array([[0.0, 1.0], [-np.sqrt(3) / 2, -0.5], [np.sqrt(3) / 2, -0.5]])
    w = np.asarray(steps, float) / 12.0
    return tuple((w[:, None] * V).sum(axis=0))


# --------------------------------------------------------------------------------------------------- evenness
def evenness(chord) -> float:
    """Euclidean distance from a chord to the nearest perfectly even chord of the same size (pitch classes, any
    transposition of the even chord, voices matched in circular order)."""
    x = np.sort(np.asarray(chord, float) % N)
    n = len(x)
    best = np.inf
    for r in range(n):                                          # which note plays the even chord's first voice
        y = np.concatenate([x[r:], x[:r] + N])
        e = y - N * np.arange(n) / n
        c = e.mean()
        best = min(best, float(np.sqrt(((e - c) ** 2).sum())))
    return best


def transposition_vl(chord, norm: str = "taxicab") -> dict:
    """The smallest voice leading from a chord to each of its transpositions T1 ... T11 (integer pitch classes)."""
    return {k: vl(chord, [(p + k) % N for p in chord], norm)[0] for k in range(1, N)}


def nearest_transposition(chord) -> tuple:
    """The smallest voice leading to a transposition that is a different chord: (size, k)."""
    s = sorted(p % N for p in chord)
    out = []
    for k, v in transposition_vl(chord).items():
        if sorted((p + k) % N for p in chord) != s:
            out.append((v, k))
    return min(out)


# ------------------------------------------------------------------------------------------------- OPTIC counts
def _canon(ch, T: bool, I: bool, C: bool):
    ch = tuple(sorted(p % N for p in ch))
    if C:
        ch = tuple(sorted(set(ch)))
    forms = [ch]
    if T:
        forms = [tuple(sorted((p + k) % N for p in f)) for f in forms for k in range(N)]
    if I:
        forms = forms + [tuple(sorted((-p) % N for p in f)) for f in forms]
        if T:
            forms = [tuple(sorted((p + k) % N for p in f)) for f in forms for k in range(N)]
    return min(forms)


def optic_counts(n: int = 3) -> dict:
    """The number of n-note chords of 12-ET (octave and permutation equivalence always on, OP) when transposition (T),
    inversion (I) and cardinality (C: doublings ignored) are added, by brute force."""
    chords = list(combinations_with_replacement(range(N), n))
    out = {"OP": len(chords)}
    for T, I, C, name in ((True, False, False, "OPT"), (True, True, False, "OPTI"), (False, False, True, "OPC"),
                          (True, False, True, "OPTC"), (True, True, True, "OPTIC")):
        out[name] = len({_canon(c, T, I, C) for c in chords})
    return out


# ------------------------------------------------------------------------------------------------------ Fourier
def dft(pcs, n: int = N) -> np.ndarray:
    """|F_k| for k = 0 ... 6 of a pitch-class set's indicator (Lewin 1959; Quinn; Amiot)."""
    k = np.arange(n // 2 + 1)
    x = np.asarray(sorted(set(int(p) % n for p in pcs)))
    z = np.exp(-2j * np.pi * np.outer(k, x) / n).sum(axis=1)
    return np.abs(z)


def dft_champions(size: int) -> dict:
    """For each coefficient k = 1 ... 6, the prime forms of the given size with the largest |F_k|."""
    from explainer.music.monochord import atonal as A
    classes = sorted({A.prime_form(c) for c in combinations(range(N), size)})
    out = {}
    for k in range(1, 7):
        vals = {c: float(dft(c)[k]) for c in classes}
        top = max(vals.values())
        out[k] = {"value": top, "sets": [c for c, v in vals.items() if abs(v - top) < 1e-9]}
    return out


# -------------------------------------------------------------------------------------------------------- Bach
def bach_voice_leading(book, upper_only: bool = False) -> dict:
    """For every change between consecutive beat chords of the chorales: Bach's voice leading (the semitones each voice
    really moves, summed) against the smallest voice leading between the same two multisets of pitch classes.  With
    ``upper_only`` the bass is left out (soprano, alto, tenor)."""
    actual, minimal, n_eq = [], [], 0
    rng = np.random.default_rng(0)
    shuffled = []
    for c in book:
        beats = c.beats()
        for (_, a, _), (_, b, _) in zip(beats, beats[1:]):
            if a == b:
                continue
            va = a[:3] if upper_only else a
            vb = b[:3] if upper_only else b
            act = sum(abs(q - p) for p, q in zip(va, vb))
            m = vl([p % N for p in va], [q % N for q in vb])[0]
            actual.append(act)
            minimal.append(m)
            if abs(act - m) < 1e-9:
                n_eq += 1
            # a control: the same two chords with the second chord's notes given to the voices at random
            perm = rng.permutation(len(vb))
            shuffled.append(sum(pc_dist(va[i] % N, vb[perm[i]] % N) for i in range(len(va))))
    actual, minimal, shuffled = np.array(actual, float), np.array(minimal, float), np.array(shuffled, float)
    return {"n": int(len(actual)), "minimal_share": n_eq / len(actual), "mean_actual": float(actual.mean()),
            "mean_minimal": float(minimal.mean()), "mean_shuffled": float(shuffled.mean()),
            "excess_hist": np.bincount((actual - minimal).astype(int), minlength=8)[:8].tolist()}


# ------------------------------------------------------------------------------------------------ chord graphs
def semitone_neighbours(chord) -> list:
    """Chords (as sorted pitch-class tuples, no doublings) one semitone away: one voice moves up or down a semitone."""
    s = sorted(chord)
    out = set()
    for i in range(len(s)):
        for d in (-1, 1):
            t = list(s)
            t[i] = (t[i] + d) % N
            if len(set(t)) == len(t):
                out.add(tuple(sorted(t)))
    return sorted(out)


def semitone_path(a, b) -> list:
    """The shortest chain of one-semitone moves from chord a to chord b (breadth-first)."""
    from collections import deque
    a, b = tuple(sorted(x % N for x in a)), tuple(sorted(x % N for x in b))
    prev = {a: None}
    q = deque([a])
    while q:
        t = q.popleft()
        if t == b:
            break
        for u in semitone_neighbours(t):
            if u not in prev:
                prev[u] = t
                q.append(u)
    path, t = [], b
    while t is not None:
        path.append(t)
        t = prev[t]
    return path[::-1]
