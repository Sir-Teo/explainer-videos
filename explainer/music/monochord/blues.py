"""Monochord's blues and swing (Part 38 of *Music, Built*).

    chord(symbol)                 a chord symbol (C7, Dm7, Cmaj7, F#dim7, Db7 ...) as root and pitch classes
    twelve_bar(key, variant)      the twelve-bar blues: basic, quick-change, and a jazz blues with ii-V's
    swing_ratio(bpm)              a simple model of the long-short ratio against tempo: 3:1 at 120 beats a minute,
                                  falling in a straight line to 1:1 at 300 (the trend Friberg and Sundstrom measured)
    swing_times(onsets, bpm)      eighth-note positions to seconds, swung by the model, with an optional downbeat delay
    walking_bass(changes)         a walking bass: the root on beat one, an approach a semitone from the next root on beat
                                  four, chord and scale tones between, as smooth as possible (dynamic programming)
    guide_tones(changes)          the thirds and sevenths of a progression as two lines with the least total motion
    tritone_sub(symbol)           a dominant seventh's substitute a tritone away, which shares its tritone
    syncopation(notes, beat)      onsets between the beats that are held across the next stronger position
    rag_hands(notes)              a piano part split into hands at a key number
"""

from __future__ import annotations

from itertools import product

import numpy as np

NAMES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
         "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11}
QUALITIES = {"7": (0, 4, 7, 10), "maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10), "m7b5": (0, 3, 6, 10), "dim7": (0, 3, 6, 9),
             "6": (0, 4, 7, 9), "m6": (0, 3, 7, 9), "": (0, 4, 7), "m": (0, 3, 7)}
PCN = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def chord(symbol: str) -> dict:
    root = symbol[:2] if len(symbol) > 1 and symbol[1] in "#b" else symbol[:1]
    q = symbol[len(root):]
    r = NAMES[root]
    iv = QUALITIES[q]
    pcs = [(r + i) % 12 for i in iv]
    third = (r + iv[1]) % 12
    seventh = (r + iv[3]) % 12 if len(iv) > 3 else None
    return {"symbol": symbol, "root": r, "quality": q, "pcs": pcs, "third": third, "seventh": seventh}


def transpose(symbol: str, k: int) -> str:
    c = chord(symbol)
    return PCN[(c["root"] + k) % 12] + c["quality"]


def twelve_bar(key: str = "C", variant: str = "basic") -> list[list[str]]:
    """Twelve bars, each a list of chord symbols (one or two a bar)."""
    if variant == "basic":
        bars = [["C7"], ["C7"], ["C7"], ["C7"], ["F7"], ["F7"], ["C7"], ["C7"], ["G7"], ["F7"], ["C7"], ["G7"]]
    elif variant == "quick":
        bars = [["C7"], ["F7"], ["C7"], ["C7"], ["F7"], ["F7"], ["C7"], ["C7"], ["G7"], ["F7"], ["C7"], ["G7"]]
    elif variant == "jazz":
        bars = [["C7"], ["F7"], ["C7"], ["Gm7", "C7"], ["F7"], ["F#dim7"], ["C7"], ["A7"], ["Dm7"], ["G7"], ["C7", "A7"], ["Dm7", "G7"]]
    else:
        raise ValueError(variant)
    k = NAMES[key]
    return [[transpose(s, k) if k else s for s in b] for b in bars]


# ------------------------------------------------------------------------------------------------- swing
SWING_POINTS = ((120.0, 3.0), (300.0, 1.0))


def swing_ratio(bpm: float) -> float:
    """The long-short ratio of swung eighths: 3:1 at 120 beats a minute falling linearly to 1:1 at 300, held at 3.5
    below and 1 above.  A schematic line through the trend measured on jazz drummers' ride cymbals (Friberg and
    Sundstrom, 2002), not a fit to their data points."""
    (b0, r0), (b1, r1) = SWING_POINTS
    r = r0 + (r1 - r0) * (bpm - b0) / (b1 - b0)
    return float(min(max(r, 1.0), 3.5))


def short_note_ms(bpm: float, ratio: float | None = None) -> float:
    r = swing_ratio(bpm) if ratio is None else ratio
    beat = 60.0 / bpm
    return 1000.0 * beat / (1.0 + r)


def swing_times(eighths, bpm: float, ratio: float | None = None, delay_ms: float = 0.0) -> np.ndarray:
    """Positions in eighth notes (0, 1, 2 ...: even numbers are on the beat) to seconds.  An off-beat eighth falls
    ``r/(1+r)`` of the way through its beat; ``delay_ms`` delays the on-beat eighths only (a soloist's late downbeats)."""
    r = swing_ratio(bpm) if ratio is None else ratio
    beat = 60.0 / bpm
    e = np.asarray(eighths, float)
    b = np.floor(e / 2.0)
    frac = e / 2.0 - b                                            # 0 on the beat, 0.5 for the off-beat, others between
    on = frac < 1e-9
    pos = np.where(on, 0.0, np.where(np.abs(frac - 0.5) < 1e-9, r / (1 + r), frac))
    t = (b + pos) * beat
    return t + np.where(on, delay_ms / 1000.0, 0.0)


# ------------------------------------------------------------------------------------------------- walking bass
def _scale_for(c: dict) -> list[int]:
    """A scale for a chord: mixolydian for a dominant, dorian for a minor seventh, major for maj7/6, locrian for m7b5,
    the diminished scale for dim7."""
    q, r = c["quality"], c["root"]
    steps = {"7": (0, 2, 4, 5, 7, 9, 10), "m7": (0, 2, 3, 5, 7, 9, 10), "maj7": (0, 2, 4, 5, 7, 9, 11), "6": (0, 2, 4, 5, 7, 9, 11),
             "m7b5": (0, 1, 3, 5, 6, 8, 10), "dim7": (0, 2, 3, 5, 6, 8, 9, 11), "": (0, 2, 4, 5, 7, 9, 11), "m": (0, 2, 3, 5, 7, 8, 10),
             "m6": (0, 2, 3, 5, 7, 9, 10)}[q]
    return [(r + s) % 12 for s in steps]


def beats_of(changes: list[list[str]], beats_per_bar: int = 4) -> list[str]:
    out = []
    for bar in changes:
        per = beats_per_bar // len(bar)
        for s in bar:
            out += [s] * per
    return out


def walking_bass(changes: list[list[str]], lo: int = 36, hi: int = 55, start: int | None = None) -> list[int]:
    """One note a beat.  Rules: the first beat of each chord is its root; the beat before a chord change is a
    semitone above or below the next root (a chromatic approach); other beats are chord tones, or scale tones of the
    chord; consecutive notes differ by at most a fifth.  Among all bass lines obeying the rules, the program chooses
    the one with the least total motion (Viterbi over the candidates on each beat), preferring chord tones."""
    seq = beats_of(changes)
    n = len(seq)
    cands, cost_here = [], []
    for i, s in enumerate(seq):
        c = chord(s)
        first = i == 0 or seq[i - 1] != s
        nxt = chord(seq[(i + 1) % n])
        last = seq[(i + 1) % n] != s
        if first:
            pcs, pen = {c["root"]: 0.0}, None
        elif last:
            pcs = {(nxt["root"] + 1) % 12: 0.0, (nxt["root"] - 1) % 12: 0.0}
        else:
            pcs = {p: 0.0 for p in c["pcs"]}
            for p in _scale_for(c):
                pcs.setdefault(p, 1.5)
        cs, cc = [], []
        for m in range(lo, hi + 1):
            if m % 12 in pcs:
                cs.append(m)
                cc.append(pcs[m % 12])
        cands.append(cs)
        cost_here.append(cc)
    INF = 1e18
    best_line, best_cost = None, INF
    for j0, m0 in enumerate(cands[0]):                              # the cycle closes: the last note approaches the first
        D = [[INF] * len(c) for c in cands]
        back = [[-1] * len(c) for c in cands]
        D[0][j0] = cost_here[0][j0] + (abs(m0 - start) if start is not None else abs(m0 - 43) * 0.2)
        for i in range(1, n):
            for j, m in enumerate(cands[i]):
                best, arg = INF, -1
                for k, q in enumerate(cands[i - 1]):
                    if D[i - 1][k] >= INF:
                        continue
                    leap = abs(m - q)
                    if leap == 0 or leap > 7:
                        continue
                    v = D[i - 1][k] + leap + (2.0 if leap > 4 else 0.0)
                    if v < best:
                        best, arg = v, k
                D[i][j], back[i][j] = best + cost_here[i][j], arg
        for j, m in enumerate(cands[-1]):
            if abs(m - m0) == 1 and D[-1][j] < best_cost:
                out = [m]
                jj = j
                for i in range(n - 1, 0, -1):
                    jj = back[i][jj]
                    out.append(cands[i - 1][jj])
                best_line, best_cost = out[::-1], D[-1][j]
    if best_line is None:
        raise ValueError("no walking line obeys the rules in this range")
    return best_line


# ------------------------------------------------------------------------------------------------- guide tones
def guide_tones(symbols: list[str], lo: int = 52, hi: int = 72) -> dict:
    """Thirds and sevenths of each chord as two voices, upper and lower: each chord's two guide tones are assigned to
    the voices (either way round) and to registers in [lo, hi] so that the total motion is least (Viterbi).  For a
    triad the root stands in for the missing seventh."""
    states = []
    for s in symbols:
        c = chord(s)
        a, b = c["third"], (c["seventh"] if c["seventh"] is not None else c["root"])
        opts = []
        for x in range(lo, hi + 1):
            for y in range(lo, hi + 1):
                if x > y and x - y <= 11 and {x % 12, y % 12} == {a, b}:
                    opts.append((x, y))
        states.append(opts)
    INF = 1e18
    D = [[0.0] * len(states[0])]
    back = [[-1] * len(states[0])]
    for i in range(1, len(states)):
        row, br = [], []
        for (x, y) in states[i]:
            best, arg = INF, -1
            for k, (p, q) in enumerate(states[i - 1]):
                v = D[-1][k] + abs(x - p) + abs(y - q)
                if v < best:
                    best, arg = v, k
            row.append(best)
            br.append(arg)
        D.append(row)
        back.append(br)
    # prefer a middle register at the end, to break ties
    j = int(np.argmin([D[-1][k] + 0.01 * abs(sum(states[-1][k]) / 2 - 64) for k in range(len(states[-1]))]))
    path = [states[-1][j]]
    for i in range(len(states) - 1, 0, -1):
        j = back[i][j]
        path.append(states[i - 1][j])
    path = path[::-1]
    upper = [p[0] for p in path]
    lower = [p[1] for p in path]
    moves = [abs(upper[i + 1] - upper[i]) + abs(lower[i + 1] - lower[i]) for i in range(len(path) - 1)]
    return {"upper": upper, "lower": lower, "total": int(sum(moves)), "moves": moves,
            "max_step": max([max(abs(upper[i + 1] - upper[i]), abs(lower[i + 1] - lower[i])) for i in range(len(path) - 1)] or [0])}


def tritone_sub(symbol: str) -> str:
    c = chord(symbol)
    if c["quality"] != "7":
        raise ValueError("a tritone substitute replaces a dominant seventh")
    return PCN[(c["root"] + 6) % 12] + "7"


def tritone(symbol: str) -> set:
    c = chord(symbol)
    return {c["third"], c["seventh"]}


# ------------------------------------------------------------------------------------------------- ragtime
def rag_hands(notes, split: int = 61) -> tuple[list, list]:
    """Notes (key, onset, duration) split into right hand (above ``split``) and left hand."""
    right = [n for n in notes if n[0] > split]
    left = [n for n in notes if n[0] <= split]
    return right, left


def syncopation(notes, beat: int = 24) -> dict:
    """For one hand's notes (ticks, ``beat`` per quarter): onsets, distinct onset times, those on the beat, on the
    half-beat, and on the sixteenths between; and *syncopations*: notes starting between the beats (not on a beat)
    that are still sounding at the next stronger position, with no new onset there in that hand."""
    times = sorted({o for _, o, _ in notes})
    starts = set(times)
    ends = {}
    for p, o, d in notes:
        ends[o] = max(ends.get(o, 0), o + d)
    half = beat // 2
    on_beat = [t for t in times if t % beat == 0]
    on_half = [t for t in times if t % beat == half]
    between = [t for t in times if t % half != 0]
    sync = []
    for t in times:
        if t % beat == 0:
            continue
        # the next stronger position: the next beat for a half-beat onset, the next eighth for a sixteenth
        strong = (t // beat + 1) * beat if t % half == 0 else (t // half + 1) * half
        if ends[t] > strong and strong not in starts:
            sync.append(t)
    return {"onsets": len(times), "on_beat": len(on_beat), "on_half": len(on_half), "between": len(between),
            "syncopated": len(sync), "sync_times": sync}
