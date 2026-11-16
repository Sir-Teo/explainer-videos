"""Sixteenth-century style as programs: what Part 24 computes.

    Dissonance   every dissonance against the lowest voice classified as Jeppesen would: passing, neighbour,
                 suspension (prepared, resolved down by step), cambiata, or free.
    Melody       leaps and how they are recovered; intervals the style forbids.
    Sonority     how many sonorities hold a third; full triads; final chords.
    Imitation    points of imitation: the same opening intervals entering in other voices.
    Stylometry   a feature vector per piece and a nearest-centroid classifier with leave-one-out.
    Tuning       Zarlino's just triad and Vicentino's thirty-one tones, in cents.

    from explainer.music.monochord import renaissance, palestrina as PS
    book = renaissance.load()
    PS.dissonances(book[0])          # Counter of treatments
"""

from __future__ import annotations

import bisect
import math
from collections import Counter

import numpy as np

CONSONANT = {0, 3, 4, 7, 8, 9}
KINDS = ("passing", "neighbour", "suspension", "cambiata", "anticipation", "free")


class Voices:
    """Fast lookups into a piece's voices: what sounds at a time, and a note's neighbours."""

    def __init__(self, piece):
        self.piece = piece
        self.v = piece.voices
        self.on = [[o for _, o, _ in v] for v in self.v]

    def at(self, j: int, t: int):
        """(index, note) sounding in voice j at time t, or None."""
        i = bisect.bisect_right(self.on[j], t) - 1
        if i < 0:
            return None
        p, o, d = self.v[j][i]
        return (i, self.v[j][i]) if o <= t < o + d else None

    def prev(self, j: int, i: int):
        if i <= 0:
            return None
        a, b = self.v[j][i - 1], self.v[j][i]
        return a if a[1] + a[2] == b[1] else None

    def next(self, j: int, i: int):
        if i + 1 >= len(self.v[j]):
            return None
        a, b = self.v[j][i], self.v[j][i + 1]
        return b if a[1] + a[2] == b[1] else None


def _step(a: int, b: int) -> bool:
    return 1 <= abs(a - b) <= 2


def classify(V: Voices, j: int, i: int, low: int, li: int, t: int) -> str | None:
    """The treatment of one dissonance at time t between voice j's note i and the lowest voice's note li, or None if
    neither note begins at t (the dissonance was already counted when it began).

    If the upper note was held while the bass moved under it, it is a suspension when it was consonant when struck
    and falls by step next; otherwise it is free.  If the upper note arrives (alone or with the bass), it is judged by
    how it is approached and left."""
    a = V.v[j][i]
    b = V.v[low][li]
    if a[1] != t and b[1] != t:
        return None
    p, o, d = a
    if o < t:                                                      # held over a moving bass
        nx = V.next(j, i)
        struck = V.at(low, o)
        prepared = struck is not None and (p - V.v[low][struck[0]][0]) % 12 in CONSONANT
        if nx is not None and 1 <= p - nx[0] <= 2 and prepared:
            return "suspension"
        return _motion(V, low, li)                                  # else the bass made it: judge the bass's note
    k = _motion(V, j, i)
    if k == "free" and b[1] == t:
        k = _motion(V, low, li)                                     # the bass may be the passing note
    return k


def _motion(V: Voices, j: int, i: int) -> str:
    p = V.v[j][i][0]
    pr, nx = V.prev(j, i), V.next(j, i)
    if pr is not None and nx is not None and _step(p, pr[0]) and _step(nx[0], p):
        return "passing" if np.sign(p - pr[0]) == np.sign(nx[0] - p) else "neighbour"
    if pr is not None and nx is not None and 1 <= pr[0] - p <= 2 and 3 <= p - nx[0] <= 4:
        return "cambiata"                                          # down a step to the dissonance, then down a third
    if nx is not None and nx[0] == p and pr is not None and _step(p, pr[0]):
        return "anticipation"
    return "free"


def dissonances(piece) -> Counter:
    """Every dissonance against the lowest sounding voice (seconds, fourths, tritones, sevenths above it), counted once,
    where it begins, and classified."""
    V = Voices(piece)
    res = Counter()
    ons = sorted({o for v in piece.voices for _, o, _ in v})
    for t in ons:
        live = []
        for j in range(len(V.v)):
            s_ = V.at(j, t)
            if s_ is not None:
                live.append((j, s_[0], s_[1][0]))
        if len(live) < 2:
            continue
        low = min(live, key=lambda x: x[2])
        for j, i, p in live:
            if j == low[0] or (p - low[2]) % 12 in CONSONANT:
                continue
            k = classify(V, j, i, low[0], low[1], t)
            if k is not None:
                res[k] += 1
    return res


def shares(c: Counter) -> dict:
    tot = sum(c.values())
    return {k: c.get(k, 0) / tot if tot else 0.0 for k in KINDS}


# ---------------------------------------------------------------------------
# Melody
# ---------------------------------------------------------------------------
def melodic(piece) -> dict:
    """Leaps (a fourth or more) and whether the next move turns back by step; intervals the style avoids (sevenths,
    augmented and diminished intervals, leaps over an octave, the descending sixth), per thousand moves."""
    moves = leaps = recovered = forbidden = 0
    for v in piece.voices:
        ps = [p for p, _, _ in v]
        for k in range(len(ps) - 1):
            iv = ps[k + 1] - ps[k]
            if iv == 0:
                continue
            moves += 1
            a = abs(iv)
            if a in (10, 11) or a > 12 or a == 6 or iv in (-8, -9):
                forbidden += 1
            if a >= 5:
                leaps += 1
                if k + 2 < len(ps):
                    nx = ps[k + 2] - ps[k + 1]
                    if 1 <= abs(nx) <= 2 and np.sign(nx) == -np.sign(iv):
                        recovered += 1
    return {"moves": moves, "leaps": leaps, "recovered": recovered, "forbidden": forbidden}


# ---------------------------------------------------------------------------
# Sonority
# ---------------------------------------------------------------------------
def sonorities(piece, step: int = 24) -> dict:
    """At every ``step`` ticks: does the sonority hold a third (or sixth) above its bass?  Is it a full triad (third and
    fifth, or a sixth chord)?  And the last chord."""
    g = piece.grid(24 // step if step <= 24 else 1) if step <= 24 else piece.grid(1)[:: step // 24]
    third = triad = n = 0
    for row in g:
        x = [p for p in row if p >= 0]
        if len(x) < 2:
            continue
        n += 1
        b = min(x)
        ics = {(p - b) % 12 for p in x if p != b}
        if ics & {3, 4, 8, 9}:
            third += 1
        if ({3, 4} & ics and 7 in ics) or ({8, 9} & ics and {3, 4} & ics):
            triad += 1
    f = piece.final()
    b = min(f)
    fin = {(p - b) % 12 for p in f if p != b}
    return {"n": n, "third": third, "triad": triad, "final_third": bool(fin & {3, 4})}


# ---------------------------------------------------------------------------
# Imitation
# ---------------------------------------------------------------------------
def head(voice, k: int = 4):
    """The first k melodic intervals of a voice (repeated notes merged), and when it enters."""
    ps, start = [], None
    for p, o, d in voice:
        if start is None:
            start = o
        if not ps or ps[-1] != p:
            ps.append(p)
        if len(ps) > k:
            break
    return tuple(ps[i + 1] - ps[i] for i in range(min(k, len(ps) - 1))), start


def imitation(piece, k: int = 4, tonal: bool = True) -> dict:
    """Does the piece open with a point of imitation?  Voices whose first k intervals match the first entry's (exactly,
    or with steps of the same direction and size class when ``tonal``), with their delays and transpositions."""
    heads = sorted(((head(v, k), v[0][0]) for v in piece.voices if v), key=lambda x: x[0][1])
    (first, t0), p0 = heads[0]
    out = []
    for (h, t), p in heads[1:]:
        exact = h == first
        sim = len(h) == len(first) and all(np.sign(a) == np.sign(b) and abs(abs(a) - abs(b)) <= 1 for a, b in zip(h, first))
        if exact or (tonal and sim):
            out.append({"delay": t - t0, "interval": (p - p0), "exact": exact})
    return {"entries": len(out) + 1, "voices": len(piece.voices), "followers": out, "imitative": len(out) >= 1}


# ---------------------------------------------------------------------------
# Stylometry
# ---------------------------------------------------------------------------
FEATURES = ("free", "passing", "suspension", "neighbour", "leap_share", "recovered", "forbidden", "third", "triad", "step_share",
            "rest_share", "note_len")


def features(piece) -> np.ndarray:
    dz = shares(dissonances(piece))
    m = melodic(piece)
    s = sonorities(piece)
    steps = sum(1 for v in piece.voices for a, b in zip(v, v[1:]) if 1 <= abs(a[0] - b[0]) <= 2)
    moves = max(m["moves"], 1)
    span = piece.length * len(piece.voices)
    sounding = sum(d for v in piece.voices for _, _, d in v)
    lens = [d for v in piece.voices for _, _, d in v]
    return np.array([dz["free"], dz["passing"], dz["suspension"], dz["neighbour"], m["leaps"] / moves, m["recovered"] / max(m["leaps"], 1),
                     1000 * m["forbidden"] / moves, s["third"] / max(s["n"], 1), s["triad"] / max(s["n"], 1), steps / moves,
                     1 - sounding / max(span, 1), float(np.log(np.median(lens)))])


def loo_centroid(X: np.ndarray, y: list) -> dict:
    """Nearest-centroid classification, leave-one-out, on standardized features: accuracy and the confusion counts."""
    X = np.asarray(X, float)
    labels = sorted(set(y))
    y = np.array(y)
    pred = []
    for i in range(len(X)):
        mask = np.arange(len(X)) != i
        # The held-out piece must not influence feature scaling.
        mu, sd = X[mask].mean(0), X[mask].std(0) + 1e-9
        Z = (X - mu) / sd
        cents = {c: Z[mask & (y == c)].mean(0) for c in labels}
        pred.append(min(labels, key=lambda c: float(np.sum((Z[i] - cents[c]) ** 2))))
    pred = np.array(pred)
    conf = {a: {b: int(np.sum((y == a) & (pred == b))) for b in labels} for a in labels}
    return {"accuracy": float(np.mean(pred == y)), "confusion": conf, "pred": pred.tolist()}


def centroid_weights(X: np.ndarray, y: list, a, b) -> dict:
    """Which features separate class a from class b: the difference of standardized means."""
    X = np.asarray(X, float)
    Z = (X - X.mean(0)) / (X.std(0) + 1e-9)
    y = np.array(y)
    d = Z[y == a].mean(0) - Z[y == b].mean(0)
    return dict(zip(FEATURES, (float(x) for x in d)))


# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------
def cents(r: float) -> float:
    return 1200 * math.log2(r)


def triad_cents() -> dict:
    """The major third and fifth of a triad: Pythagorean, Zarlino's just (4:5:6), equal, and Vicentino's 31 equal."""
    return {"pythagorean": (cents(81 / 64), cents(3 / 2)), "just": (cents(5 / 4), cents(3 / 2)), "equal": (400.0, 700.0),
            "31-tone": (10 * 1200 / 31, 18 * 1200 / 31)}
