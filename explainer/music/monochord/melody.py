"""Monochord's melodies (Part 14, *Melody*).

A melody here is a list of notes, each ``(semitones above the tonic, beats)``, with the places where its phrases
end.  The module reads the corpus in ``tunes.py``, counts what melodies do, asks which of those things chance
would do anyway, and learns a model of what comes next.

    parse(text, mode) / corpus()             read tunes written in scale degrees
    intervals, interval_histogram            the steps and leaps of a melody
    span, tessitura, median_pitch            how much room it uses, and where it sits
    contour_shape, arch                      the shape of a phrase; the average shape of many
    post_skip / shuffled / random_walk       what follows a leap, in real tunes and in tunes made by chance
    gap_fill                                 is a leap followed by steps back into the gap?
    degree_transitions                       where each degree of the scale tends to go
    NGram                                    a variable-order model of the next note, with its surprise in bits
    zipf                                     rank and frequency of a melody's small patterns
    sequences                                a pattern repeated on another step of the scale
    invert, retrograde, ornament             things to do to a tune

No manim.  Checked in ``tests/music/test_melody.py``.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field

import numpy as np

from .tunes import TUNES

MAJOR = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10)


@dataclass
class Melody:
    name: str
    pitches: list[int]                 # semitones above the tonic (the tonic of the middle octave is 0)
    beats: list[float]
    phrase_ends: list[int] = field(default_factory=list)    # indices one past the last note of each phrase
    mode: str = "major"
    origin: str = ""

    def __len__(self) -> int:
        return len(self.pitches)

    @property
    def onsets(self) -> list[float]:
        return list(np.concatenate([[0.0], np.cumsum(self.beats)[:-1]]))

    @property
    def phrases(self) -> list[list[int]]:
        out, a = [], 0
        for b in self.phrase_ends:
            out.append(self.pitches[a:b])
            a = b
        if a < len(self.pitches):
            out.append(self.pitches[a:])
        return [p for p in out if p]

    def degrees(self) -> list[int]:
        """Each note's place in its scale, 1 to 7 (a chromatic note takes the degree below it), octaves ignored."""
        scale = MINOR if self.mode == "minor" else MAJOR
        out = []
        for p in self.pitches:
            pc = p % 12
            out.append(max(i for i, s in enumerate(scale) if s <= pc) + 1)
        return out


def parse(text: str, mode: str = "major", name: str = "", origin: str = "") -> Melody:
    """Read a tune written in scale degrees (see ``tunes.py`` for the notation)."""
    scale = MINOR if mode == "minor" else MAJOR
    pitches, beats, ends = [], [], []
    for tok in text.split():
        if tok == "/":
            ends.append(len(pitches))
            continue
        body, _, dur = tok.partition("*")
        alter = 0
        while body[0] in "#b":
            alter += 1 if body[0] == "#" else -1
            body = body[1:]
        deg = int(body[0])
        if not 1 <= deg <= 7:
            raise ValueError(f"no degree {deg} in {tok!r}")
        octave = body[1:].count("'") - body[1:].count(",")
        if set(body[1:]) - {"'", ","}:
            raise ValueError(f"cannot read {tok!r}")
        pitches.append(scale[deg - 1] + alter + 12 * octave)
        beats.append(float(dur) if dur else 1.0)
    return Melody(name, pitches, beats, ends, mode, origin)


def corpus(names=None) -> list[Melody]:
    """The tunes of ``tunes.py``, parsed."""
    return [parse(t["notes"], t.get("mode", "major"), name, t.get("origin", "")) for name, t in TUNES.items() if names is None or name in names]


THE_TUNE = "Ah! vous dirai-je, maman (the Tune)"


# ---------------------------------------------------------------------------
# What melodies do
# ---------------------------------------------------------------------------
def intervals(m) -> list[int]:
    p = m.pitches if isinstance(m, Melody) else list(m)
    return [b - a for a, b in zip(p, p[1:])]


def interval_histogram(tunes, lo: int = -12, hi: int = 12) -> dict[int, int]:
    c = Counter(i for m in tunes for i in intervals(m))
    return {k: c.get(k, 0) for k in range(lo, hi + 1)}


def shares(tunes) -> dict:
    """Of all the moves from one note to the next: how many repeat, step (one or two semitones) or leap, and of the
    steps and leaps how many go up."""
    iv = [i for m in tunes for i in intervals(m)]
    n = len(iv)
    rep = sum(i == 0 for i in iv)
    step = [i for i in iv if 1 <= abs(i) <= 2]
    leap = [i for i in iv if abs(i) >= 3]
    return {"moves": n, "repeat": rep / n, "step": len(step) / n, "leap": len(leap) / n, "mean_size": float(np.mean(np.abs(iv))),
            "steps_up": sum(i > 0 for i in step) / max(len(step), 1), "leaps_up": sum(i > 0 for i in leap) / max(len(leap), 1),
            "within_fifth": sum(abs(i) <= 7 for i in iv) / n}


def span(m) -> int:
    """From the lowest note to the highest, in semitones."""
    return max(m.pitches) - min(m.pitches)


def median_pitch(m) -> float:
    return float(np.median(m.pitches))


def tessitura(m) -> tuple[float, float]:
    """Where a melody spends its time: the pitches a quarter and three quarters of the way up its notes, weighted
    by how long each lasts."""
    order = np.argsort(m.pitches)
    p, w = np.asarray(m.pitches, dtype=float)[order], np.asarray(m.beats)[order]
    c = np.cumsum(w) / w.sum()
    return float(p[np.searchsorted(c, 0.25)]), float(p[np.searchsorted(c, 0.75)])


def contour_shape(phrase) -> str:
    """Huron's nine shapes: compare a phrase's first note, the average of the notes between, and its last."""
    if len(phrase) < 3:
        return "level"
    a, mid, b = phrase[0], float(np.mean(phrase[1:-1])), phrase[-1]
    up1, up2 = np.sign(round(mid - a, 6)), np.sign(round(b - mid, 6))
    return {(1, -1): "arch", (-1, 1): "valley", (1, 1): "rising", (-1, -1): "falling", (0, 0): "level", (1, 0): "rising then level",
            (0, -1): "level then falling", (-1, 0): "falling then level", (0, 1): "level then rising"}[(int(up1), int(up2))]


def arch(tunes, bins: int = 9, min_notes: int = 5) -> np.ndarray:
    """The average shape of a phrase: each phrase's notes, measured from its own mean pitch and stretched to the
    same length, averaged over every phrase of every tune."""
    rows = []
    for m in tunes:
        for ph in m.phrases:
            if len(ph) >= min_notes:
                x = np.linspace(0, 1, len(ph))
                rows.append(np.interp(np.linspace(0, 1, bins), x, np.asarray(ph, dtype=float) - np.mean(ph)))
    return np.mean(rows, axis=0)


# ---------------------------------------------------------------------------
# Leaps, and what follows them (von Hippel and Huron 2000)
# ---------------------------------------------------------------------------
def post_skip(tunes, skip: int = 3) -> dict:
    """After every leap of ``skip`` semitones or more: does the next move go back (a reversal) or on (a
    continuation)?  Counted for all leaps, and separately by where the leap lands: further from the tune's median
    pitch than it began (departing), nearer to it on the same side (approaching), or across it (crossing)."""
    out = {k: {"reversal": 0, "continuation": 0, "repeat": 0} for k in ("all", "departing", "approaching", "crossing", "landing")}
    for m in tunes:
        p = m.pitches if isinstance(m, Melody) else list(m)
        med = float(np.median(p))
        for a, b, c in zip(p, p[1:], p[2:]):
            if abs(b - a) < skip:
                continue
            what = "repeat" if c == b else ("reversal" if (c - b) * (b - a) < 0 else "continuation")
            if b == med:
                kind = "landing"
            elif (a - med) * (b - med) < 0:
                kind = "crossing"
            elif abs(b - med) > abs(a - med):
                kind = "departing"
            else:
                kind = "approaching"
            out["all"][what] += 1
            out[kind][what] += 1
    for k, v in out.items():
        moved = v["reversal"] + v["continuation"]
        v["share"] = v["reversal"] / moved if moved else float("nan")
        v["n"] = moved + v["repeat"]
    return out


def shuffled(tunes, seed: int = 0) -> list[Melody]:
    """The same tunes with each one's notes in a random order: every note it had, none of its design."""
    rng = np.random.default_rng(seed)
    out = []
    for m in tunes:
        idx = rng.permutation(len(m))
        out.append(Melody(m.name, [m.pitches[i] for i in idx], [m.beats[i] for i in idx], list(m.phrase_ends), m.mode, m.origin))
    return out


def urn_melody(n: int, low: int = 0, high: int = 12, seed: int = 0) -> list[int]:
    """Notes drawn at random, each independently, from a bell-shaped spread over a range: a melody with no memory."""
    rng = np.random.default_rng(seed)
    mid, sd = (low + high) / 2, (high - low) / 4
    return [int(np.clip(round(x), low, high)) for x in rng.normal(mid, sd, n)]


def gap_fill(tunes, leap: int = 5, within: int = 4) -> dict:
    """Meyer's gap-fill: after a leap of ``leap`` semitones or more, do the next ``within`` notes move back into
    the gap by step?  Returns the share of leaps that are filled (at least two of the following moves are steps in
    the opposite direction, landing inside the gap)."""
    filled = total = 0
    for m in tunes:
        p = m.pitches
        for k in range(len(p) - 1):
            d = p[k + 1] - p[k]
            if abs(d) < leap or k + 1 + within >= len(p):
                continue
            total += 1
            lo, hi = min(p[k], p[k + 1]), max(p[k], p[k + 1])
            back = 0
            for j in range(k + 1, k + 1 + within):
                s = p[j + 1] - p[j]
                if 1 <= abs(s) <= 2 and s * d < 0 and lo <= p[j + 1] <= hi:
                    back += 1
            filled += back >= 2
    return {"leaps": total, "filled": filled, "share": filled / total if total else float("nan")}


def degree_transitions(tunes, mode: str = "major") -> np.ndarray:
    """``T[i, j]``: of the times degree i + 1 is followed by another note, how often that note is degree j + 1."""
    c = np.zeros((7, 7))
    for m in tunes:
        if m.mode != mode:
            continue
        d = m.degrees()
        for a, b in zip(d, d[1:]):
            c[a - 1, b - 1] += 1
    return c / np.maximum(c.sum(axis=1, keepdims=True), 1)


def degree_counts(tunes, mode: str = "major", weighted: bool = True) -> np.ndarray:
    """How much of the time each degree sounds (by duration, or by count)."""
    c = np.zeros(7)
    for m in tunes:
        if m.mode != mode:
            continue
        for d, b in zip(m.degrees(), m.beats):
            c[d - 1] += b if weighted else 1.0
    return c / c.sum()


# ---------------------------------------------------------------------------
# A model of what comes next
# ---------------------------------------------------------------------------
class NGram:
    """A variable-order Markov model of a melody's notes (as semitones above the tonic, octaves kept).  It keeps
    counts for every context of up to ``order`` notes and blends them, long contexts first, falling back to
    shorter ones in proportion to how often the long context has been seen to do something new (the escape of
    PPM method C, as in Pearce's IDyOM).  ``surprise`` is the information content of each note in bits."""

    def __init__(self, order: int = 2, alphabet=None):
        self.order = order
        self.counts = [defaultdict(Counter) for _ in range(order + 1)]
        self.alphabet = sorted(alphabet) if alphabet is not None else None

    def fit(self, tunes) -> "NGram":
        seqs = [list(m.pitches) if isinstance(m, Melody) else list(m) for m in tunes]
        if self.alphabet is None:
            self.alphabet = sorted({p for s in seqs for p in s})
        for s in seqs:
            for k, x in enumerate(s):
                for n in range(self.order + 1):
                    if k - n >= 0:
                        self.counts[n][tuple(s[k - n:k])][x] += 1
        return self

    def distribution(self, context) -> dict:
        """The probability of every note of the alphabet after a context."""
        context = tuple(context)[-self.order:] if self.order else ()
        probs = {a: 1.0 / len(self.alphabet) for a in self.alphabet}          # order -1: nothing known
        for n in range(0, min(self.order, len(context)) + 1):
            c = self.counts[n].get(context[len(context) - n:], None)
            if not c:
                continue
            total, kinds = sum(c.values()), len(c)
            lam = total / (total + kinds)                                    # trust in this context
            probs = {a: lam * c.get(a, 0) / total + (1 - lam) * probs[a] for a in self.alphabet}
        return probs

    def surprise(self, seq) -> np.ndarray:
        seq = list(seq.pitches) if isinstance(seq, Melody) else list(seq)
        out = []
        for k, x in enumerate(seq):
            p = self.distribution(seq[:k]).get(x, 0.0)
            out.append(-math.log2(max(p, 1e-12)))
        return np.array(out)

    def continuations(self, context, top: int = 5) -> list[tuple[int, float]]:
        d = self.distribution(context)
        return sorted(d.items(), key=lambda kv: -kv[1])[:top]

    def generate(self, n: int, start=(0,), seed: int = 0) -> list[int]:
        rng = np.random.default_rng(seed)
        out = list(start)
        while len(out) < n:
            d = self.distribution(out)
            keys = list(d)
            out.append(int(rng.choice(keys, p=np.array([d[k] for k in keys]) / sum(d.values()))))
        return out


def cross_entropy(tunes, order: int) -> float:
    """Bits per note when each tune is predicted by a model that has learnt from all the others."""
    tunes = list(tunes)
    alphabet = sorted({p for m in tunes for p in m.pitches})
    bits = notes = 0.0
    for k, m in enumerate(tunes):
        model = NGram(order, alphabet).fit(tunes[:k] + tunes[k + 1:])
        s = model.surprise(m)
        bits += float(s.sum())
        notes += len(s)
    return bits / notes


def entropy(values) -> float:
    c = np.array(list(Counter(values).values()), dtype=float)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def zipf(tunes, n: int = 2) -> dict:
    """Rank and frequency of the patterns of ``n`` successive intervals in a corpus, and the slope of the best
    line through them on logarithmic axes (Zipf's law is a slope near -1)."""
    c = Counter()
    for m in tunes:
        iv = intervals(m)
        for k in range(len(iv) - n + 1):
            c[tuple(iv[k:k + n])] += 1
    freq = np.array(sorted(c.values(), reverse=True), dtype=float)
    rank = np.arange(1, len(freq) + 1)
    slope, intercept = np.polyfit(np.log(rank), np.log(freq), 1)
    return {"rank": rank.tolist(), "frequency": freq.tolist(), "slope": float(slope), "kinds": len(freq), "total": int(freq.sum()),
            "top": [(list(k), v) for k, v in c.most_common(5)]}


# ---------------------------------------------------------------------------
# Motive, sequence, and things to do to a tune
# ---------------------------------------------------------------------------
def scale_steps(m: Melody) -> list[int]:
    """Each note as a number of scale steps above the tonic (chromatic notes take the step below)."""
    scale = MINOR if m.mode == "minor" else MAJOR
    out = []
    for p in m.pitches:
        o, pc = divmod(p, 12)
        out.append(7 * o + max(i for i, s in enumerate(scale) if s <= pc))
    return out


def sequences(m: Melody, length: int = 4) -> list[dict]:
    """Places where ``length`` notes are followed at once by the same shape (in scale steps, with the same rhythm)
    on another step of the scale: a sequence.  An exact repeat (shift 0) is listed too."""
    s, b = scale_steps(m), m.beats
    out = []
    for k in range(len(s) - 2 * length + 1):
        first, second = s[k:k + length], s[k + length:k + 2 * length]
        shift = second[0] - first[0]
        if [x - first[0] for x in first] == [x - second[0] for x in second] and b[k:k + length] == b[k + length:k + 2 * length] and len(set(first)) > 1:
            out.append({"at": k, "length": length, "shift": shift})
    return out


def invert(m: Melody, axis: int | None = None, diatonic: bool = True) -> Melody:
    """Upside down: every move up becomes the same move down.  ``diatonic`` keeps the notes in the scale (steps
    are mirrored as scale steps); otherwise semitones are mirrored exactly.  The axis is the first note."""
    if not diatonic:
        ax = m.pitches[0] if axis is None else axis
        return Melody(m.name + ", inverted", [2 * ax - p for p in m.pitches], list(m.beats), list(m.phrase_ends), m.mode, m.origin)
    scale = MINOR if m.mode == "minor" else MAJOR
    s = scale_steps(m)
    ax = s[0] if axis is None else axis
    mirrored = [2 * ax - x for x in s]
    return Melody(m.name + ", inverted", [12 * (x // 7) + scale[x % 7] for x in mirrored], list(m.beats), list(m.phrase_ends), m.mode, m.origin)


def retrograde(m: Melody) -> Melody:
    return Melody(m.name + ", backwards", m.pitches[::-1], m.beats[::-1], [len(m) - e for e in m.phrase_ends[::-1] if e < len(m)] + [len(m)], m.mode, m.origin)


def ornament(m: Melody, kind: str = "passing") -> Melody:
    """Decorate a tune without changing where it goes.  ``passing``: fill each leap of up to a fifth with the
    scale notes on the way.
    ``neighbour``: turn a repeated note into note, upper neighbour, note.  ``turn``: begin each long note with
    the notes above and below it."""
    scale = MINOR if m.mode == "minor" else MAJOR
    s = scale_steps(m)

    def pitch(step):
        return 12 * (step // 7) + scale[step % 7]

    p, b, ends = [], [], []
    for k in range(len(s)):
        nxt = s[k + 1] if k + 1 < len(s) else None
        at_end = (k + 1) in m.phrase_ends
        if kind == "passing" and nxt is not None and 2 <= abs(nxt - s[k]) <= 4 and not at_end and m.beats[k] >= 1:
            way = 1 if nxt > s[k] else -1
            run = [s[k] + way * j for j in range(abs(nxt - s[k]))]            # this note, and every scale step on the way to the next
            p += [m.pitches[k]] + [pitch(x) for x in run[1:]]
            b += [m.beats[k] / len(run)] * len(run)
        elif kind == "neighbour" and nxt is not None and nxt == s[k] and not at_end and m.beats[k] >= 1:
            p += [m.pitches[k], pitch(s[k] + 1)]
            b += [m.beats[k] / 2, m.beats[k] / 2]
        elif kind == "turn" and m.beats[k] >= 2:
            p += [pitch(s[k] + 1), m.pitches[k], pitch(s[k] - 1), m.pitches[k]]
            b += [0.25, 0.25, 0.25, m.beats[k] - 0.75]
        else:
            p.append(m.pitches[k])
            b.append(m.beats[k])
        if at_end:
            ends.append(len(p))
    return Melody(f"{m.name}, with {kind} notes", p, b, ends, m.mode, m.origin)
