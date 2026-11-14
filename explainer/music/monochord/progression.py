"""Progressions (Part 18): the syntax of harmony, measured.  Root motion and harmonic function; how predictable the
next chord is (cross-entropy in bits, on chorales held out by tune); sequences; the rule of the octave and how
closely Bach's basses follow it; Gjerdingen's galant schemata and a detector for them; the old ground basses.

Chords are (root relative to the tonic, kind) as in :mod:`fourpart`; scale degrees are 1-7 (with an accidental
where needed) or semitones above the tonic.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

import numpy as np

from . import chords as CH
from . import fourpart as F

MAJOR = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10)
MOTION_NAMES = {0: "same", 1: "step up", 2: "step up", 3: "third up", 4: "third up", 5: "fifth down", 6: "tritone",
                7: "fifth up", 8: "third down", 9: "third down", 10: "step down", 11: "step down"}
# root motion as the music theorists group it (Meeùs 2000): falling fifths, falling thirds and rising steps carry
# harmony forward ("dominant" progressions); their inverses are "subdominant" progressions or retrogressions
MOTION_KIND = {"fifth down": "forward", "third down": "forward", "step up": "forward", "fifth up": "backward",
               "third up": "backward", "step down": "backward", "same": "none", "tritone": "other"}


# ---------------------------------------------------------------------------
# Chords in a row
# ---------------------------------------------------------------------------
def sequence(c, merge: bool = True) -> list:
    """The chords on a chorale's beats as (root, kind) (None for an unlabelled beat), repeats merged."""
    out = []
    for x in F.beat_labels(c):
        s = x["label"][:2] if x["label"] else None
        if merge and out and out[-1] == s:
            continue
        out.append(s)
    return out


def function(state, mode: str = "major") -> str | None:
    """Riemann's three functions, read off the root: tonic (T), subdominant or predominant (S), dominant (D)."""
    if state is None:
        return None
    rel = state[0]
    if mode == "major":
        return {0: "T", 9: "T", 4: "T", 5: "S", 2: "S", 7: "D", 11: "D"}.get(rel)
    return {0: "T", 3: "T", 8: "S", 5: "S", 2: "S", 7: "D", 11: "D", 10: "D"}.get(rel)


def root_motions(book, mode: str = "major") -> Counter:
    """How the root moves from one chord to the next (repeats merged), by interval class."""
    out = Counter()
    for c in book:
        if c.mode != mode:
            continue
        seq = sequence(c)
        for a, b in zip(seq, seq[1:]):
            if a is None or b is None:
                continue
            out[MOTION_NAMES[(b[0] - a[0]) % 12]] += 1
    return out


def function_transitions(book, mode: str = "major") -> dict:
    """Counts of T, S and D followed by T, S and D (repeated functions merged)."""
    out = Counter()
    for c in book:
        if c.mode != mode:
            continue
        fs = [function(s, mode) for s in sequence(c)]
        fs = [f for f in fs if f is not None]
        fs = [f for k, f in enumerate(fs) if k == 0 or f != fs[k - 1]]
        for a, b in zip(fs, fs[1:]):
            out[(a, b)] += 1
    return {f"{a}{b}": out[(a, b)] for a, b in product("TSD", repeat=2) if a != b}


# ---------------------------------------------------------------------------
# How predictable is the next chord?
# ---------------------------------------------------------------------------
class NGram:
    """An n-gram model of chord symbols with add-``alpha`` smoothing over a fixed vocabulary."""

    def __init__(self, seqs, n: int, vocab, alpha: float = 0.5):
        self.n, self.alpha, self.vocab = n, alpha, list(vocab)
        self.counts = defaultdict(Counter)
        for s in seqs:
            s = ["<s>"] * (n - 1) + list(s)
            for k in range(n - 1, len(s)):
                self.counts[tuple(s[k - n + 1:k])][s[k]] += 1

    def prob(self, ctx, x) -> float:
        c = self.counts.get(tuple(ctx[len(ctx) - self.n + 1:]) if self.n > 1 else (), Counter())
        return (c[x] + self.alpha) / (sum(c.values()) + self.alpha * len(self.vocab))

    def bits(self, seqs) -> float:
        """Cross-entropy, bits per chord, on other sequences."""
        tot, n = 0.0, 0
        for s in seqs:
            s2 = ["<s>"] * (self.n - 1) + list(s)
            for k in range(self.n - 1, len(s2)):
                tot -= np.log2(self.prob(s2[:k], s2[k]))
                n += 1
        return tot / max(n, 1)


def symbols(book, mode: str, merge: bool = True) -> list:
    """Each chorale as a list of Roman numerals (no inversions), unlabelled beats dropped."""
    out = []
    for c in book:
        if c.mode != mode:
            continue
        out.append([F.roman((s[0], s[1], 0), mode) for s in sequence(c, merge) if s is not None])
    return out


def predictability(train, test, mode: str = "major", merge: bool = True, alpha: float = 0.1) -> dict:
    """Bits per chord on held-out chorales: every chord equally likely, the chords' frequencies alone (n = 1), and
    the chord after one (n = 2) and two (n = 3) chords; and the same for the held-out chorales shuffled, which keeps
    their chords and destroys their order."""
    tr, te = symbols(train, mode, merge), symbols(test, mode, merge)
    vocab = sorted({x for s in tr + te for x in s})
    out = {"vocab": len(vocab), "uniform": float(np.log2(len(vocab)))}
    rng = np.random.default_rng(0)
    shuffled = [list(rng.permutation(s)) for s in te]
    for n in (1, 2, 3):
        m = NGram(tr, n, vocab, alpha)
        out[f"n{n}"] = m.bits(te)
        out[f"n{n}_shuffled"] = m.bits(shuffled)
    return out


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------
def fifth_chains(book, mode: str = "major", min_len: int = 3) -> Counter:
    """Runs of roots falling by fifth (or rising by fourth), by number of chords in the run."""
    out = Counter()
    for c in book:
        if c.mode != mode:
            continue
        seq = [s for s in sequence(c)]
        run = 1
        for a, b in zip(seq, seq[1:]):
            if a is not None and b is not None and (b[0] - a[0]) % 12 == 5:
                run += 1
            else:
                if run >= min_len:
                    out[run] += 1
                run = 1
        if run >= min_len:
            out[run] += 1
    return out


# ---------------------------------------------------------------------------
# The rule of the octave (Campion 1716): a chord for every degree of a scale in the bass
# ---------------------------------------------------------------------------
# figures above each bass degree, ascending and descending, in major; ``#6`` is a raised sixth
RULE_OF_OCTAVE = {
    "up": {1: "5/3", 2: "6/4/3", 3: "6", 4: "6/5", 5: "5/3", 6: "6", 7: "6/5", 8: "5/3"},
    "down": {8: "5/3", 7: "6", 6: "#6/4/3", 5: "5/3", 4: "4/2", 3: "6", 2: "6/4/3", 1: "5/3"},
}


def rule_chord(degree: int, direction: str, tonic: int = 0) -> tuple[int, ...]:
    """The pitch classes of the rule of the octave's chord over a degree of the major scale (bass first)."""
    fig = RULE_OF_OCTAVE[direction][degree]
    fig = {"4/2": "6/4/2"}.get(fig, fig)                               # a 4/2 is short for 6/4/2
    bass = (tonic + MAJOR[(degree - 1) % 7]) % 12
    k = (degree - 1) % 7
    out = [bass]
    for part in fig.split("/"):
        raised = part.startswith("#")
        n = int(part.lstrip("#"))
        pc = (tonic + MAJOR[(k + n - 1) % 7]) % 12
        out.append((pc + 1) % 12 if raised else pc)
    if fig in ("6", "5/3", "6/5"):                                    # a 6 is 6/3 and a 6/5 is 6/5/3, a 5/3 is 5/3
        third = (tonic + MAJOR[(k + 2) % 7]) % 12
        if third not in out:
            out.append(third)
    return tuple(dict.fromkeys(out))


def upper_voices(pcs, bass: int, lo: int = 55, hi: int = 81) -> list[tuple]:
    """Every (soprano, alto, tenor) above ``bass`` from the chord's notes, neighbours within an octave, so that with
    the bass every note of the chord sounds."""
    keys = [m for m in range(max(lo, bass + 1), hi + 1) if m % 12 in pcs]
    need = set(pcs)
    out = []
    for t in keys:
        for a in keys:
            if a <= t or a - t > 12:
                continue
            for s_ in keys:
                if s_ <= a or s_ - a > 12:
                    continue
                if {s_ % 12, a % 12, t % 12, bass % 12} >= need:
                    out.append((s_, a, t))
    return out


def realize_rule(direction: str = "up", tonic: int = 0, start=(67, 64, 60)) -> list[tuple]:
    """The rule of the octave over a bass climbing (or falling) an octave, the upper three voices taking the
    shortest way from chord to chord: a partimento player's first exercise."""
    degrees = list(range(1, 9)) if direction == "up" else list(range(8, 0, -1))
    bass0 = 48 + tonic
    out = []
    prev = tuple(start)
    for d in degrees:
        b = bass0 + MAJOR[(d - 1) % 7] + (12 if d == 8 else 0)
        pcs = rule_chord(d, direction, tonic)
        cands = upper_voices(pcs, b)
        last = out[-1] if out else None
        up = min(cands, key=lambda v: (len(F.parallels(last, v + (b,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev)), abs(v[0] - prev[0])))
        out.append(up + (b,))
        prev = up
    return out


def realize_bass(bass, tonic: int = 0, start=(72, 67, 64)) -> list[dict]:
    """A partimento player in a few lines: an unfigured bass in a major key, realized by the rule of the octave.
    Where the bass moves by step, the chord is the rule's for that degree and direction; where it leaps, or ends,
    a root-position triad (a first-inversion chord on the leading note); the upper voices take the shortest way and
    avoid parallels."""
    out, prev = [], tuple(start)
    for k, b in enumerate(bass):
        pc = (b - tonic) % 12
        deg = MAJOR.index(pc) + 1 if pc in MAJOR else None
        nxt = bass[k + 1] if k + 1 < len(bass) else None
        step = nxt is not None and 1 <= abs(nxt - b) <= 2
        if deg is not None and step:
            direction = "up" if nxt > b else "down"
            pcs = rule_chord(deg, direction, tonic)
            how = f"rule, {direction}"
        else:
            root = b if deg != 7 else b - 4
            third = (root + (4 if (root - tonic) % 12 in (0, 5, 7) else 3)) % 12
            fifth = (root + (6 if (root - tonic) % 12 == 11 else 7)) % 12
            pcs = (b % 12, root % 12, third, fifth)
            pcs = tuple(dict.fromkeys(pcs))
            how = "leap: a triad"
        cands = upper_voices(pcs, b)
        last = out[-1]["chord"] if out else None
        up = min(cands, key=lambda v: (len(F.parallels(last, v + (b,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        out.append({"chord": up + (b,), "how": how, "figure": figure_of(up + (b,))})
        prev = up
    return out


def figure_of(ch) -> str:
    from .score import Pitch
    return CH.figure_name([Pitch.from_midi(int(p)) for p in ch])


def bach_vs_rule(book) -> dict:
    """Where Bach's bass moves by step through a degree in major, the share of beats whose figure is the rule of
    the octave's for that degree and direction (6/4/3 and 4/3, 6/5 and 6/5/3 counted alike), and the share whose notes
    all belong to the rule's chord (a chord with a note left out, such as vii\u00b06 for V4/3, counts)."""
    norm = {"6/4/3": "4/3", "#6/4/3": "4/3", "6/5": "6/5", "5/3": "5/3", "6": "6", "4/2": "4/2"}
    hits = defaultdict(lambda: [0, 0, 0])
    for c in book:
        if c.mode != "major":
            continue
        beats = [(t, ch) for t, ch, _ in c.beats()]
        for (t0, a), (t1, b), (t2, z) in zip(beats, beats[1:], beats[2:]):
            d1, d2 = b[3] - a[3], z[3] - b[3]
            if not (1 <= abs(d1) <= 2 and 1 <= abs(d2) <= 2 and (d1 > 0) == (d2 > 0)):
                continue
            deg_pc = (b[3] - c.tonic) % 12
            if deg_pc not in MAJOR:
                continue
            deg = MAJOR.index(deg_pc) + 1
            direction = "up" if d1 > 0 else "down"
            want = RULE_OF_OCTAVE[direction][deg]
            got = figure_of(b)
            key = (direction, deg)
            hits[key][1] += 1
            hits[key][0] += norm.get(want, want) == norm.get(got, got)
            rule_pcs = {(c.tonic + x) % 12 for x in rule_chord(deg, direction)}
            hits[key][2] += len({p % 12 for p in b}) >= 3 and {p % 12 for p in b} <= rule_pcs
    return {f"{d}{g}": {"agree": a, "n": n, "within": w, "rule": RULE_OF_OCTAVE[d][g]} for (d, g), (a, n, w) in sorted(hits.items())}


# ---------------------------------------------------------------------------
# Galant schemata (Gjerdingen 2007), as bass and melody degrees, and a detector
# ---------------------------------------------------------------------------
# each event: (bass degree, melody degree); degrees in semitones above the tonic (major)
SCHEMATA = {
    "Romanesca": [(0, 0), (11, 7), (9, 0), (4, 0)],          # bass 1-7-6-3 under melody 1-5-1-1
    "Prinner": [(5, 9), (4, 7), (2, 5), (0, 4)],             # melody 6-5-4-3 over bass 4-3-2-1
    "Do-Re-Mi": [(0, 0), (11, 2), (0, 4)],                   # melody 1-2-3 over bass 1-7-1
    "Meyer": [(0, 0), (2, 11), (11, 5), (0, 4)],             # melody 1-7 ... 4-3 over bass 1-2 ... 7-1
    "Fonte": [(1, 7), (2, 5), (11, 5), (0, 4)],              # bass #1-2, 7-1 under melody 5-4, 4-3 (minor, then major)
    "Monte": [(4, 10), (5, 9), (6, 0), (7, 11)],             # bass 3-4, #4-5 under melody b7-6, 1-7
    "Ponte": [(7, 7), (7, 11), (7, 2), (7, 5)],              # a dominant pedal under a rising melody
    "Quiescenza": [(0, 10), (0, 9), (0, 11), (0, 0)],        # a tonic pedal under b7-6-7-1
}


def degree_events(c) -> list[tuple[int, int]]:
    """A chorale as (bass, soprano) degrees on its beats, in semitones above the tonic, repeats merged."""
    out = []
    for _, ch, _ in c.beats():
        e = ((ch[3] - c.tonic) % 12, (ch[0] - c.tonic) % 12)
        if not out or out[-1] != e:
            out.append(e)
    return out


def find_schemata(events, schemata=SCHEMATA) -> list[tuple[str, int]]:
    """Every place where a schema's events occur in order, consecutively (after merging repeats)."""
    hits = []
    for name, pat in schemata.items():
        L = len(pat)
        for k in range(len(events) - L + 1):
            if all(events[k + j] == pat[j] for j in range(L)):
                hits.append((name, k))
    return hits


def schema_census(book) -> dict:
    """How often each schema occurs in the major chorales, and in the same chorales with their beats shuffled."""
    real, shuf = Counter(), Counter()
    rng = np.random.default_rng(0)
    where = defaultdict(list)
    for c in book:
        if c.mode != "major":
            continue
        ev = degree_events(c)
        for name, k in find_schemata(ev):
            real[name] += 1
            where[name].append((c.name, k))
        for name, _ in find_schemata([ev[i] for i in rng.permutation(len(ev))]):
            shuf[name] += 1
    return {"real": dict(real), "shuffled": dict(shuf), "where": {k: v[:5] for k, v in where.items()}}


# ---------------------------------------------------------------------------
# Ground basses: progressions repeated under variations
# ---------------------------------------------------------------------------
# chords as (root relative to the tonic, kind) and the bass note's degree in semitones; one chord to a half bar
GROUNDS = {
    "lament": {"mode": "minor", "bass": [0, 10, 8, 7], "chords": [(0, "minor"), (7, "minor"), (5, "minor"), (7, "major")],
               "text": "the descending minor tetrachord: 1-b7-b6-5"},
    "folia": {"mode": "minor", "bass": [0, 7, 0, 10, 3, 10, 0, 7],
              "chords": [(0, "minor"), (7, "major"), (0, "minor"), (10, "major"), (3, "major"), (10, "major"), (0, "minor"), (7, "major")],
              "text": "i-V-i-VII-III-VII-i-V"},
    "romanesca": {"mode": "major", "bass": [0, 11, 9, 4, 5, 0, 5, 7],
                  "chords": [(0, "major"), (7, "major"), (9, "minor"), (4, "minor"), (5, "major"), (0, "major"), (5, "major"), (7, "major")],
                  "text": "I-V6-vi-iii-IV-I-IV-V: Pachelbel's bass is one"},
    "passamezzo": {"mode": "minor", "bass": [0, 10, 0, 7, 3, 10, 0, 7],
                   "chords": [(0, "minor"), (10, "major"), (0, "minor"), (7, "major"), (3, "major"), (10, "major"), (0, "minor"), (7, "major")],
                   "text": "passamezzo antico: i-VII-i-V-III-VII-i-V"},
}


def ground_voicings(name: str, tonic: int = 0, top: tuple = (72, 67, 64)) -> list[tuple]:
    """A ground bass realized in four voices, the upper three by the shortest way."""
    g = GROUNDS[name]
    out = []
    prev = tuple(top)
    for (rel, kind), b in zip(g["chords"], g["bass"]):
        pcs = [(tonic + rel + o) % 12 for o in CH.offsets(kind)]
        bass = 43 + ((tonic + b - 7) % 12)
        cands = upper_voices(pcs, bass, 55, 79)
        last = out[-1] if out else None
        best = min(cands, key=lambda v: (len(F.parallels(last, v + (bass,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        out.append(best + (bass,))
        prev = best
    return out
