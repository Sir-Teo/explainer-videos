"""The Classical style as programs: what Part 26 computes, on the string quartets of Haydn, Mozart and Beethoven.

    Harmony      how often the harmony changes from beat to beat.
    Cadences     authentic cadences (the bass falling a fifth to a downbeat, the top on the tonic or third), the bars
                 between them, and how many of those gaps are 4 or 8 bars: periodic phrasing.
    Texture      which voice leads (has the most notes) in each bar, how often the lead changes hands, how many bars
                 have an accompaniment figure (a voice repeating or breaking one chord).
    Keys         a key tracker over a movement (Part 15's), its tonal plan.
    Style        eight features per movement and Part 24's nearest-centroid test with leave-one-out.

    from explainer.music.monochord import baroque, classical as CL
    m = CL.Movement(baroque.load_quartets()[0])
    CL.features(m)
"""

from __future__ import annotations

import bisect
from collections import Counter

import numpy as np

from . import key as K

FEATURES = ("harmonic rhythm", "periodic phrases", "cadences per bar", "first violin leads", "lead changes", "notes per bar",
            "register span", "accompaniment figures")


class Movement:
    """A quartet movement: four voices top to bottom, its bar and beat in ticks (24 to a quarter)."""

    def __init__(self, row: dict):
        self.composer = row["composer"]
        self.name = row["name"]
        self.time = tuple(row["time"])
        self.voices = row["voices"]
        num, den = self.time
        self.bar = int(24 * 4 * num / den)
        if den == 8 and num % 3 == 0:
            self.beat = 3 * 12
        else:
            self.beat = 24 * 4 // den
        self.length = max(o + d for v in self.voices for _, o, d in v)
        self.bars = self.length // self.bar
        self._on = [[o for _, o, _ in v] for v in self.voices]

    def at(self, j: int, t: int):
        i = bisect.bisect_right(self._on[j], t) - 1
        if i < 0:
            return None
        p, o, d = self.voices[j][i]
        return p if o <= t < o + d else None

    def sonority(self, t: int) -> frozenset:
        return frozenset(p % 12 for p in (self.at(j, t) for j in range(len(self.voices))) if p is not None)


def harmonic_rhythm(m: Movement) -> float:
    """The share of beats on which the set of sounding pitch classes changes."""
    sets = [m.sonority(t) for t in range(0, m.length, m.beat)]
    return float(np.mean([a != b for a, b in zip(sets, sets[1:])])) if len(sets) > 1 else 0.0


def cadences(m: Movement) -> list[int]:
    """Bars that begin with an authentic cadence: the lowest voice falls a fifth (or rises a fourth) onto the downbeat
    and holds at least a beat, and the top voice there is the bass's note or its third."""
    bass, top = m.voices[-1], m.voices[0]
    out = []
    for i in range(1, len(bass)):
        p0, o0, d0 = bass[i - 1]
        p, o, d = bass[i]
        if (p0 - p) % 12 == 7 and o % m.bar == 0 and d >= m.beat and o0 + d0 == o:
            tp = m.at(0, o)
            if tp is not None and (tp - p) % 12 in (0, 3, 4):
                out.append(o // m.bar)
    return out


def phrase_gaps(m: Movement) -> list[int]:
    c = cadences(m)
    return [b - a for a, b in zip(c, c[1:]) if b - a >= 2]


def lead_voices(m: Movement) -> list[int]:
    """For every bar, the voice with the most note onsets (ties to the higher voice)."""
    counts = np.zeros((m.bars + 1, len(m.voices)), dtype=int)
    for j, v in enumerate(m.voices):
        for _, o, _ in v:
            counts[o // m.bar, j] += 1
    return [int(np.argmax(row)) for row in counts[: m.bars]]


def accompaniment_bars(m: Movement) -> float:
    """The share of bars in which some lower voice (2nd violin, viola, cello) has at least four notes all drawn from
    one or two pitch classes or from one triad: repeated notes, a broken chord, an Alberti-like figure."""
    hits = 0
    for b in range(m.bars):
        lo, hi = b * m.bar, (b + 1) * m.bar
        found = False
        for v in m.voices[1:]:
            ps = [p for p, o, _ in v if lo <= o < hi]
            if len(ps) >= 4:
                pcs = {p % 12 for p in ps}
                if len(pcs) <= 2 or (len(pcs) == 3 and _is_triad(pcs)):
                    found = True
                    break
        hits += int(found)
    return hits / max(m.bars, 1)


def _is_triad(pcs) -> bool:
    for r in pcs:
        rel = {(p - r) % 12 for p in pcs}
        if rel in ({0, 4, 7}, {0, 3, 7}, {0, 3, 6}):
            return True
    return False


def features(m: Movement) -> np.ndarray:
    gaps = phrase_gaps(m)
    lead = lead_voices(m)
    notes = sum(len(v) for v in m.voices)
    span = np.mean([max(p for p, _, _ in v) - min(p for p, _, _ in v) for v in m.voices if v])
    return np.array([harmonic_rhythm(m), float(np.mean([g in (4, 8) for g in gaps])) if gaps else 0.0, len(cadences(m)) / max(m.bars, 1),
                     float(np.mean([x == 0 for x in lead])), float(np.mean([a != b for a, b in zip(lead, lead[1:])])) if len(lead) > 1 else 0.0,
                     float(np.log(notes / max(m.bars, 1))), float(span), accompaniment_bars(m)])


def tonal_plan(m: Movement, window_bars: int = 8, hop_bars: int = 2) -> list[dict]:
    """Part 15's key tracker over the whole texture: the key of each window of ``window_bars`` bars."""
    ps, bs = [], []
    for v in m.voices:
        for p, o, d in v:
            ps.append((o, p, d))
    ps.sort()
    pitches = [p for _, p, _ in ps]
    onsets = [o / m.bar for o, _, _ in ps]
    durs = [d / m.bar for _, _, d in ps]
    out = []
    for start in np.arange(0, max(m.bars - window_bars, 0) + 1, hop_bars):
        sel = [(p, d) for p, o, d in zip(pitches, onsets, durs) if start <= o < start + window_bars]
        if not sel:
            continue
        dist = K.distribution([p for p, _ in sel], [d for _, d in sel])
        out.append({"bar": float(start), "key": K.find_key(dist)})
    return out
