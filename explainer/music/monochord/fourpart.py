"""Four-part writing (Part 17): ranges, spacing and doubling; the voice-leading rules between every pair of voices;
chord labels on the beats of a chorale; a chord model learned from Bach; and a harmonizer that chooses chords and
voicings together by dynamic programming, to be judged against Bach on chorales it has not seen.

A chord is a tuple (soprano, alto, tenor, bass) of key numbers.  A label is (root relative to the tonic, kind), with
kinds from :mod:`chords` ("major", "minor", "diminished", "7", ...).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product

import numpy as np

from . import chords as CH

RANGES = ((60, 81), (55, 74), (48, 69), (40, 62))                    # S A T B as textbooks give them: C4–A5, G3–D5, C3–A4, E2–D4
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_NAMES = {(0, 1): "S–A", (0, 2): "S–T", (0, 3): "S–B", (1, 2): "A–T", (1, 3): "A–B", (2, 3): "T–B"}
KINDS = ("major", "minor", "diminished", "7", "m7", "m7b5", "dim7", "maj7", "augmented")
MAJOR = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10, 11)                                    # natural minor and the raised seventh


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------
def in_range(ch) -> bool:
    return all(lo <= p <= hi for p, (lo, hi) in zip(ch, RANGES))


def spacing_ok(ch) -> bool:
    """No crossing; soprano and alto, alto and tenor within an octave; the bass anywhere below (up to two octaves)."""
    s, a, t, b = ch
    return s >= a >= t >= b and s - a <= 12 and a - t <= 12 and t - b <= 24


def parallels(c0, c1, contrary: bool = False) -> list[tuple[tuple[int, int], str]]:
    """Consecutive fifths and octaves (unisons count as octaves) between any pair of voices: both voices move, and
    the interval is a fifth or an octave both times.  With ``contrary``, also the same intervals reached in contrary
    motion ("antiparallels")."""
    out = []
    for i, j in PAIRS:
        a0, a1, b0, b1 = c0[i], c1[i], c0[j], c1[j]
        if a0 == a1 or b0 == b1:
            continue
        v0, v1 = (a0 - b0) % 12, (a1 - b1) % 12
        if v0 != v1 or v0 not in (0, 7):
            continue
        same = (a1 > a0) == (b1 > b0)
        if same or contrary:
            out.append(((i, j), ("fifths" if v0 == 7 else "octaves") + ("" if same else " (contrary)")))
    return out


def hidden(c0, c1) -> bool:
    """Hidden (direct) fifths or octaves in the outer voices: soprano and bass move in the same direction onto a
    fifth or an octave, the soprano by leap."""
    s0, s1, b0, b1 = c0[0], c1[0], c0[3], c1[3]
    if s0 == s1 or b0 == b1 or (s1 > s0) != (b1 > b0):
        return False
    return (s1 - b1) % 12 in (0, 7) and (s0 - b0) % 12 != (s1 - b1) % 12 and abs(s1 - s0) > 2


def overlap(c0, c1) -> bool:
    """A voice moves past where its neighbour just was (above the old note of the voice above, or below the one
    below)."""
    return any(c1[k + 1] > c0[k] or c1[k] < c0[k + 1] for k in range(3))


def leaps(c0, c1) -> list[int]:
    return [abs(int(b) - int(a)) for a, b in zip(c0, c1)]


# ---------------------------------------------------------------------------
# Chord labels
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _templates():
    out = []
    for kind in KINDS:
        offs = tuple(o % 12 for o in CH.offsets(kind))
        out.append((kind, offs))
    return out


@lru_cache(maxsize=None)
def label_pcs(pcs: frozenset, bass_pc: int) -> tuple[int, str, int] | None:
    """The plainest chord containing exactly these pitch classes (a triad may lack its fifth, a seventh chord its
    fifth): (root pc, kind, inversion), or None.  Ties go to the root in the bass, then to the simpler kind."""
    best = None
    for root in range(12):
        for rank, (kind, offs) in enumerate(_templates()):
            members = {(root + o) % 12 for o in offs}
            if not pcs <= members or root not in pcs:
                continue
            third = (root + offs[1]) % 12
            if third not in pcs:
                continue
            if len(offs) == 4 and (root + offs[3]) % 12 not in pcs:
                continue
            missing = len(members - pcs)
            inv = [(root + o) % 12 for o in offs].index(bass_pc) if bass_pc in members else 9
            key = (missing, inv != 0, rank, inv)
            if best is None or key < best[0]:
                best = (key, (root, kind, inv))
    return None if best is None else best[1]


def label(ch, tonic: int) -> tuple[int, str, int] | None:
    """(root relative to the tonic, kind, inversion) of a four-note chord, or None if it is no chord (a passing
    collection)."""
    pcs = frozenset(int(p) % 12 for p in ch)
    lab = label_pcs(pcs, int(ch[3]) % 12)
    if lab is None:
        return None
    root, kind, inv = lab
    return ((root - tonic) % 12, kind, inv)


_DEGREE = {0: (1, ""), 1: (2, "♭"), 2: (2, ""), 3: (3, "♭"), 4: (3, ""), 5: (4, ""), 6: (4, "♯"), 7: (5, ""), 8: (6, "♭"), 9: (6, ""),
           10: (7, "♭"), 11: (7, "")}


def roman(lab, mode: str = "major", figures: bool = True) -> str:
    """A label as a Roman numeral; in minor, the third, sixth and seventh of the natural minor scale need no flat."""
    if lab is None:
        return "–"
    rel, kind, inv = lab
    deg, acc = _DEGREE[rel]
    if mode == "minor" and rel in (3, 8, 10):
        acc = ""
    return acc + CH.roman(deg, kind, inv if figures else 0)


def doubled(ch, lab_abs) -> str | None:
    """Which member of a triad is doubled in a four-note chord: "root", "third", "fifth" (or None for sevenths and
    chords with three different notes doubled ... impossible in four voices)."""
    if lab_abs is None or len(CH.offsets(lab_abs[1])) != 3:
        return None
    root, kind, _ = lab_abs
    offs = CH.offsets(kind)
    counts = Counter((int(p) - root) % 12 for p in ch)
    for name, o in zip(("root", "third", "fifth"), offs):
        if counts.get(o % 12, 0) >= 2:
            return name
    return None


# ---------------------------------------------------------------------------
# Bach, counted
# ---------------------------------------------------------------------------
def verticals(c) -> list[tuple[int, tuple, bool]]:
    """Every change of sounding chord in a chorale: (tick, chord, fermata), all four voices sounding."""
    ticks = sorted({o for v in c.voices for _, o, _, _ in v})
    ferm = {o for v in c.voices for _, o, _, f in v if f}
    out = []
    for t in ticks:
        ch = tuple(c.sounding(j, t) for j in range(4))
        if None in ch:
            continue
        if out and out[-1][1] == ch:
            continue
        out.append((t, ch, t in ferm))
    return out


def rule_census(book) -> dict:
    """How often Bach's chorales do what the rules forbid, counted at every change of chord."""
    moves = 0
    par = Counter()
    contrary = Counter()
    hid = over = cross = out_of_range = spaced = 0
    chords = 0
    examples = []
    for c in book:
        vs = verticals(c)
        for (t0, a, _), (t1, b, _) in zip(vs, vs[1:]):
            moves += 1
            for (i, j), kind in parallels(a, b, contrary=True):
                if "contrary" in kind:
                    contrary[kind.split()[0]] += 1
                else:
                    par[kind] += 1
                    if len(examples) < 40:
                        examples.append({"chorale": c.name, "tick": int(t1), "from": list(a), "to": list(b), "pair": PAIR_NAMES[(i, j)], "kind": kind})
            hid += hidden(a, b)
            over += overlap(a, b)
        for _, ch, _ in vs:
            chords += 1
            cross += not (ch[0] >= ch[1] >= ch[2] >= ch[3])
            out_of_range += not in_range(ch)
            spaced += (ch[0] - ch[1] > 12) or (ch[1] - ch[2] > 12)
    return {"moves": moves, "chords": chords, "parallel": dict(par), "contrary": dict(contrary), "hidden": hid, "overlap": over,
            "crossing": cross, "out_of_range": out_of_range, "spacing": spaced, "examples": examples}


def beat_labels(c) -> list[dict]:
    """The chord on every beat of a chorale, labelled relative to its tonic."""
    out = []
    for t, ch, ferm in c.beats():
        lab = label(ch, c.tonic)
        out.append({"tick": t, "chord": ch, "fermata": ferm, "label": lab})
    return out


class ChordModel:
    """Bigram probabilities of chords on the beat (root relative to the tonic, kind; inversions ignored), counted
    from chorales in one mode, with add-``alpha`` smoothing; and how often each chord carries each soprano degree."""

    def __init__(self, book, mode: str = "major", alpha: float = 0.1, min_count: int = 20):
        uni, bi, emit = Counter(), Counter(), Counter()
        starts, ends = Counter(), Counter()
        for c in book:
            if c.mode != mode:
                continue
            labs = beat_labels(c)
            prev = None
            for k, x in enumerate(labs):
                if x["label"] is None:
                    prev = None
                    continue
                s = x["label"][:2]
                uni[s] += 1
                emit[(s, (x["chord"][0] - c.tonic) % 12)] += 1
                if prev is not None:
                    bi[(prev, s)] += 1
                else:
                    starts[s] += 1
                if x["fermata"]:
                    ends[s] += 1
                prev = s
        self.mode, self.alpha = mode, alpha
        self.states = [s for s, n in uni.most_common() if n >= min_count]
        self.index = {s: k for k, s in enumerate(self.states)}
        n = len(self.states)
        T = np.full((n, n), alpha)
        for (a, b), m in bi.items():
            if a in self.index and b in self.index:
                T[self.index[a], self.index[b]] += m
        self.T = np.log(T / T.sum(1, keepdims=True))
        E = np.full((n, 12), alpha)
        for (s, deg), m in emit.items():
            if s in self.index:
                E[self.index[s], deg] += m
        self.E = np.log(E / E.sum(1, keepdims=True))
        F = np.full(n, alpha)
        for s, m in ends.items():
            if s in self.index:
                F[self.index[s]] += m
        self.F = np.log(F / F.sum())
        S = np.full(n, alpha)
        for st, m in starts.items():
            if st in self.index:
                S[self.index[st]] += m
        self.S = np.log(S / S.sum())
        self.unigram = uni

    def members(self, s) -> tuple[int, ...]:
        rel, kind = s
        return tuple((rel + o) % 12 for o in CH.offsets(kind))

    def name(self, s, inv: int = 0) -> str:
        return roman((s[0], s[1], inv), self.mode)


# ---------------------------------------------------------------------------
# The harmonizer
# ---------------------------------------------------------------------------
def voicings_under(soprano: int, members, tonic: int, leading: int | None = None) -> list[tuple]:
    """Every (S, A, T, B) with this soprano, the chord's root and third present (and its seventh, for a seventh
    chord), in range and spaced, the leading note not doubled."""
    pcs = [(tonic + m) % 12 for m in members]
    need = {pcs[0], pcs[1]} | ({pcs[3]} if len(pcs) == 4 else set())
    if soprano % 12 not in pcs:
        return []
    out = []
    for a in range(RANGES[1][0], RANGES[1][1] + 1):
        if a % 12 not in pcs or a > soprano or soprano - a > 12:
            continue
        for t in range(RANGES[2][0], RANGES[2][1] + 1):
            if t % 12 not in pcs or t > a or a - t > 12:
                continue
            for b in range(RANGES[3][0], RANGES[3][1] + 1):
                if b % 12 not in pcs or b > t or t - b > 24:
                    continue
                ch = (soprano, a, t, b)
                have = {p % 12 for p in ch}
                if not need <= have:
                    continue
                if leading is not None and sum(p % 12 == leading for p in ch) > 1:
                    continue
                out.append(ch)
    return out


DEFAULT_WEIGHTS = {"chord": 1.0, "melody": 1.0, "motion": 0.25, "bass": 0.08, "parallel": 6.0, "hidden": 1.5, "overlap": 1.0, "leap": 0.6,
                   "inversion": 0.4, "leading": 3.0, "seventh": 3.0, "end": 2.0, "doubling": 0.6, "repeat": 1.0, "start": 1.0}
RULE_WEIGHTS = ("parallel", "hidden", "overlap", "leap", "leading", "seventh", "inversion", "doubling")


def pair_costs(P, C, sp, sc, model, w, tonic) -> np.ndarray:
    """The cost of every move from the chords ``P`` (m x 4, states ``sp``) to the chords ``C`` (n x 4, states
    ``sc``), as an m x n array."""
    P, C = np.asarray(P)[:, None, :], np.asarray(C)[None, :, :]
    d = C - P
    cost = -w["chord"] * model.T[np.ix_(sp, sc)]
    cost = cost + w["motion"] * (np.abs(d[..., 1]) + np.abs(d[..., 2])) + w["bass"] * np.abs(d[..., 3])
    par = np.zeros(cost.shape)
    for i, j in PAIRS:
        a0, a1, b0, b1 = P[..., i], C[..., i], P[..., j], C[..., j]
        v0, v1 = (a0 - b0) % 12, (a1 - b1) % 12
        par += (a0 != a1) & (b0 != b1) & (v0 == v1) & ((v0 == 0) | (v0 == 7)) & (np.sign(a1 - a0) == np.sign(b1 - b0))
    cost = cost + w["parallel"] * par
    s0, s1, b0, b1 = P[..., 0], C[..., 0], P[..., 3], C[..., 3]
    hid = (s0 != s1) & (b0 != b1) & (np.sign(s1 - s0) == np.sign(b1 - b0)) & np.isin((s1 - b1) % 12, (0, 7)) & ((s0 - b0) % 12 != (s1 - b1) % 12) & (np.abs(s1 - s0) > 2)
    cost = cost + w["hidden"] * hid
    ov = np.zeros(cost.shape, dtype=bool)
    for k in range(3):
        ov |= (C[..., k + 1] > P[..., k]) | (C[..., k] < P[..., k + 1])
    cost = cost + w["overlap"] * ov
    cost = cost + w["leap"] * ((np.abs(d[..., 1]) > 4).astype(float) + (np.abs(d[..., 2]) > 4))
    lead = (tonic + 11) % 12
    for k in (0, 3):
        cost = cost + w["leading"] * ((P[..., k] % 12 == lead) & (C[..., k] % 12 == tonic % 12) & (d[..., k] != 1))
    sev = np.array([_seventh(model.states[i], tonic) if _seventh(model.states[i], tonic) is not None else -1 for i in sp])[:, None]
    for k in range(4):
        bad = (P[..., k] % 12 == sev) & ~((d[..., k] >= -2) & (d[..., k] < 0)) & (d[..., k] != 0)
        cost = cost + w["seventh"] * bad
    same = (np.asarray(sp)[:, None] == np.asarray(sc)[None, :]) & (P[..., 3] == C[..., 3])
    cost = cost + w["repeat"] * same
    return cost


def harmonize(soprano, tonic: int, model: ChordModel, fermatas=(), weights=None, top: int = 14, plain: bool = False) -> dict:
    """Chords and voicings under a soprano (one key number per beat), chosen together by the Viterbi algorithm.
    The cost of a path adds, beat by beat: minus the log-probability of the chord after the last one and of the
    soprano's degree in it; the motion of the inner voices and of the bass; the rule penalties (parallel and
    hidden fifths and octaves, overlaps, inner-voice leaps, an unresolved leading note or seventh, a chord in
    inversion, a doubled major third); a chord repeated with the same bass; at a fermata, how often Bach ends a
    phrase on that chord.  ``plain`` keeps only the chord model and the motion of the voices (no rules), for
    comparison."""
    w = dict(DEFAULT_WEIGHTS, **(weights or {}))
    if plain:
        w.update({k: 0.0 for k in RULE_WEIGHTS})
    lead = (tonic + 11) % 12
    n = len(soprano)
    fer = set(fermatas)
    layers = []
    for k, s in enumerate(soprano):
        deg = (s - tonic) % 12
        opts = []
        for si in np.argsort(-model.E[:, deg])[:top]:
            mem = model.members(model.states[si])
            if deg in mem:
                opts += [(int(si), ch) for ch in voicings_under(s, mem, tonic, lead)]
        if not opts:
            raise ValueError(f"no chord fits beat {k}")
        layers.append(opts)

    def unary(k, opts):
        out = np.zeros(len(opts))
        for j, (si, ch) in enumerate(opts):
            st = model.states[si]
            u = -w["melody"] * model.E[si, (ch[0] - tonic) % 12]
            root = (tonic + st[0]) % 12
            u += w["inversion"] * (ch[3] % 12 != root)
            if st[1] == "major" and doubled(ch, ((tonic + st[0]) % 12, "major", 0)) == "third":
                u += w["doubling"]
            if k in fer or k == n - 1:
                u -= w["end"] * model.F[si]
            if k == 0:
                u -= w["start"] * model.S[si]
            if k == n - 1:
                u += 4.0 * (st[0] != 0) + 2.0 * (ch[3] % 12 != tonic % 12)
            out[j] = u
        return out

    cost = unary(0, layers[0])
    back = []
    for k in range(1, n):
        prev, cur = layers[k - 1], layers[k]
        trans = pair_costs([c for _, c in prev], [c for _, c in cur], [s for s, _ in prev], [s for s, _ in cur], model, w, tonic)
        tot = cost[:, None] + trans
        bk = np.argmin(tot, axis=0)
        cost = tot[bk, np.arange(len(cur))] + unary(k, cur)
        back.append(bk)
    j = int(np.argmin(cost))
    path = [j]
    for bk in reversed(back):
        j = int(bk[j])
        path.append(j)
    path.reverse()
    chosen = [layers[k][j] for k, j in enumerate(path)]
    return {"chords": [tuple(int(x) for x in c) for _, c in chosen], "states": [model.states[s] for s, _ in chosen], "cost": float(np.min(cost))}


def _seventh(state, tonic):
    mem = CH.offsets(state[1])
    return (tonic + state[0] + mem[3]) % 12 if len(mem) == 4 else None


def evaluate(ours, bach) -> dict:
    """Ours against Bach's on the same soprano, beat by beat: the same chord (root and kind), the same bass note,
    the same inner voices; and the rule counts and inner-voice motion of each."""
    n = min(len(ours["chords"]), len(bach["chords"]))
    same_chord = np.mean([a == b for a, b in zip(ours["states"][:n], bach["states"][:n])])
    same_bass = np.mean([a[3] % 12 == b[3] % 12 for a, b in zip(ours["chords"][:n], bach["chords"][:n])])

    def stats(chs):
        par = sum(len(parallels(a, b)) for a, b in zip(chs, chs[1:]))
        mot = np.mean([abs(b[1] - a[1]) + abs(b[2] - a[2]) for a, b in zip(chs, chs[1:])])
        return {"parallels": int(par), "inner_motion": float(mot), "hidden": int(sum(hidden(a, b) for a, b in zip(chs, chs[1:])))}

    return {"same_chord": float(same_chord), "same_bass": float(same_bass), "ours": stats(ours["chords"][:n]), "bach": stats(bach["chords"][:n])}


def bach_on_beats(c) -> dict:
    """Bach's chords on the beats of a chorale, in the same form as :func:`harmonize`'s answer."""
    labs = beat_labels(c)
    return {"chords": [x["chord"] for x in labs], "states": [x["label"][:2] if x["label"] else None for x in labs],
            "fermatas": [k for k, x in enumerate(labs) if x["fermata"]], "soprano": [x["chord"][0] for x in labs]}
