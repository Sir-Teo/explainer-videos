"""Canon and fugue (Part 20): a melody combined with itself.

A line is a list of ``(midi, onset, duration)`` with times in beats.  The module transforms lines (transposition,
inversion, retrograde, augmentation) and checks the group they form; judges the harmony of lines sounding together
(dissonances on the beat, parallel perfect intervals); counts canons exactly at every interval by dynamic
programming over the leader's last notes, and crab canons by dynamic programming from both ends at once; maps
intervals under invertible counterpoint; answers a fugue subject really or tonally; finds a subject's strettos;
ranks tunes as rounds; and writes a free voice against others by a Viterbi search.  No manim here.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product

import numpy as np

MAJOR = (0, 2, 4, 5, 7, 9, 11)
CONSONANT = {0, 3, 4, 7, 8, 9}               # unisons and octaves, thirds, fifths, sixths (mod 12), as in Part 16
PERFECT = {0, 7}
STEP_NAMES = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh", "octave", "ninth"]


# ---------------------------------------------------------------------------
# Lines and their transformations
# ---------------------------------------------------------------------------
def line(pitches, durations=None, start: float = 0.0) -> list[tuple[int, float, float]]:
    durations = durations or [1.0] * len(pitches)
    out, t = [], start
    for p, d in zip(pitches, durations):
        out.append((int(p), float(t), float(d)))
        t += d
    return out


def end(ln) -> float:
    return max(a + d for _, a, d in ln) if ln else 0.0


def transpose(ln, n: int):
    return [(p + n, a, d) for p, a, d in ln]


def shift(ln, dt: float):
    return [(p, a + dt, d) for p, a, d in ln]


def invert(ln, axis: int | None = None):
    """Mirror every pitch about ``axis`` (default: the first note), so that rising intervals fall."""
    ax = ln[0][0] if axis is None else axis
    return [(2 * ax - p, a, d) for p, a, d in ln]


def retrograde(ln):
    """The line backwards: the last note first, durations kept with their notes."""
    T = end(ln)
    return sorted([(p, T - a - d, d) for p, a, d in ln], key=lambda x: x[1])


def augment(ln, f: float = 2.0, start: float | None = None):
    s = ln[0][1] if start is None else start
    return [(p, s + (a - s) * f, d * f) for p, a, d in ln]


def degree_of(p: int, tonic: int = 0) -> tuple[int, int]:
    """(scale step counted from the tonic, octave) of a diatonic pitch; chromatic pitches take the step below."""
    rel = p - tonic
    octv, pc = divmod(rel, 12)
    step = max(i for i, s in enumerate(MAJOR) if s <= pc)
    return step + 7 * octv, pc - MAJOR[step]


def from_degree(step: int, tonic: int = 0, alter: int = 0) -> int:
    o, s = divmod(step, 7)
    return tonic + 12 * o + MAJOR[s] + alter


def diatonic(p: int, steps: int, tonic: int = 0) -> int:
    """Move a pitch ``steps`` scale steps within the major key on ``tonic`` (a tonal, not a real, transposition)."""
    s, alter = degree_of(p, tonic)
    return from_degree(s + steps, tonic, alter)


def diatonic_invert(ln, axis_step: int, tonic: int = 0):
    """Mirror within the scale about a scale step: the inversion Bach uses in his fugues."""
    out = []
    for p, a, d in ln:
        s, alter = degree_of(p, tonic)
        out.append((from_degree(2 * axis_step - s, tonic, -alter), a, d))
    return out


# the four forms of a row of pitches, as operations on a sequence (transposition aside)
FORMS = ("P", "I", "R", "RI")


def apply_form(seq, form: str):
    s = list(seq)
    if "I" in form:
        s = [2 * s[0] - x for x in s] if form == "I" else s
    if form == "R":
        s = s[::-1]
    if form == "RI":
        s = [2 * seq[0] - x for x in seq][::-1]
    return s


def compose(f: str, g: str) -> str:
    """The form you get by doing g, then f (inversion and retrograde commute, and each undoes itself)."""
    i = ("I" in f) != ("I" in g)
    r = ("R" in f) != ("R" in g)
    return {(False, False): "P", (True, False): "I", (False, True): "R", (True, True): "RI"}[(i, r)]


def group_table() -> dict:
    """The table of the four forms: every one its own inverse, the product of any two the third: Klein's four-group."""
    return {(f, g): compose(f, g) for f in FORMS for g in FORMS}


def check_table_on(seq) -> bool:
    """Check the table by acting on an actual sequence (up to transposition, since I is taken about the first note)."""
    def norm(s):
        return tuple(x - s[0] for x in s), tuple(s)
    for f, g in product(FORMS, FORMS):
        lhs = apply_form(apply_form(seq, g), f)
        rhs = apply_form(seq, compose(f, g))
        a = [x - lhs[0] for x in lhs]
        b = [x - rhs[0] for x in rhs]
        if a != b:
            return False
    return True


# ---------------------------------------------------------------------------
# Lines sounding together
# ---------------------------------------------------------------------------
def sounding(ln, t: float):
    for p, a, d in ln:
        if a - 1e-9 <= t < a + d - 1e-9:
            return p
    return None


def attacked(ln, t: float) -> bool:
    return any(abs(a - t) < 1e-9 for _, a, _ in ln)


def faults(lines, beat: float = 1.0, start: float | None = None, stop: float | None = None, allow_upper_fourths: bool = True) -> dict:
    """Judge lines sounding together, on every beat: a dissonance is any pair of sounding notes whose interval is not
    a third, fifth, sixth, unison or octave (a fourth is allowed between two voices above the lowest); a parallel is
    the same perfect interval (fifth or octave) on two beats in a row in the same two voices, both moving."""
    lo = min(a for ln in lines for _, a, _ in ln) if start is None else start
    hi = max(end(ln) for ln in lines) if stop is None else stop
    ts = np.arange(lo, hi - 1e-9, beat)
    diss, par, n = 0, 0, 0
    where = []
    prev = None
    for t in ts:
        ps = [sounding(ln, t) for ln in lines]
        live = [(i, p) for i, p in enumerate(ps) if p is not None]
        if len(live) >= 2:
            n += 1
            bass = min(p for _, p in live)
            bad = False
            for (i, p), (j, q) in [(x, y) for k, x in enumerate(live) for y in live[k + 1:]]:
                iv = abs(p - q) % 12
                if iv in CONSONANT:
                    continue
                if iv == 5 and allow_upper_fourths and min(p, q) != bass:
                    continue
                bad = True
            if bad:
                diss += 1
                where.append(float(t))
            if prev is not None:
                for (i, p), (j, q) in [(x, y) for k, x in enumerate(live) for y in live[k + 1:]]:
                    if i in prev and j in prev:
                        p0, q0 = prev[i], prev[j]
                        iv0, iv1 = abs(p0 - q0) % 12, abs(p - q) % 12
                        if iv0 == iv1 and iv1 in PERFECT and p != p0 and q != q0 and (p - p0) * (q - q0) > 0:
                            par += 1
        prev = dict(live) if len(live) >= 2 else None
    return {"dissonant": diss, "parallels": par, "beats": n, "where": where}


def canon_lines(leader, delay: float, interval: int = 0, voices: int = 2):
    return [transpose(shift(leader, k * delay), k * interval) for k in range(voices)]


def round_score(tune, delay: float, voices: int = 3, beat: float = 1.0) -> dict:
    """A tune sung as a round: every voice the same tune, ``delay`` beats apart; judged while at least two sound."""
    lines = canon_lines(tune, delay, 0, voices)
    f = faults(lines, beat=beat, start=delay, stop=end(tune))
    f["rate"] = f["dissonant"] / f["beats"] if f["beats"] else 1.0
    return f


def best_round(tune, delays=None, voices: int = 3, beat: float = 2.0) -> tuple[float, dict]:
    """The delay (a whole number of bars of two beats, at least two) at which a tune sings best as a round, judged on
    the strong beats (every ``beat`` beats)."""
    T = end(tune)
    delays = delays or [float(d) for d in np.arange(4.0, T / 2 + 1e-9, 2.0)]
    scored = [(float(d), round_score(tune, d, voices, beat)) for d in delays]
    scored = [(d, s) for d, s in scored if s["beats"] >= 3]
    return min(scored, key=lambda x: (x[1]["rate"] + 0.05 * x[1]["parallels"], x[0]))


def strettos(subject, delays=None, intervals=(-12, -7, -5, 0, 5, 7, 12), beat: float = 1.0, tolerance: int = 0) -> list[dict]:
    """Every (delay, interval) at which a subject can enter against itself with no dissonant beat (beyond
    ``tolerance``) and no parallels, judged over the overlap."""
    T = end(subject)
    delays = delays if delays is not None else [float(d) for d in np.arange(beat, T - beat + 1e-9, beat)]
    out = []
    for d in delays:
        for iv in intervals:
            lines = canon_lines(subject, d, iv, 2)
            f = faults(lines, beat=beat, start=d, stop=T)
            if f["beats"] >= 2 and f["dissonant"] <= tolerance and f["parallels"] == 0:
                out.append({"delay": float(d), "interval": int(iv), "overlap": f["beats"], "dissonant": f["dissonant"]})
    return out


# ---------------------------------------------------------------------------
# Counting canons exactly: one note a beat, in C major
# ---------------------------------------------------------------------------
def scale_notes(lo: int = 60, hi: int = 79, tonic: int = 0) -> list[int]:
    return [p for p in range(lo, hi + 1) if (p - tonic) % 12 in MAJOR]


def _ok_move(a: int, b: int) -> bool:
    m = abs(b - a)
    return m in (1, 2, 3, 4, 5, 7, 12)                 # a step, a third, a fourth, a fifth or an octave; no repeats


def _vert_ok(x: int, y: int) -> bool:
    return abs(x - y) % 12 in CONSONANT


def _parallel(x0, y0, x1, y1) -> bool:
    i0, i1 = abs(x0 - y0) % 12, abs(x1 - y1) % 12
    return i0 == i1 and i1 in PERFECT and (x1 - x0) * (y1 - y0) > 0


def count_canons(n: int, delay: int, steps: int, notes=None, tonic: int = 0, cadence: bool = True) -> int:
    """The number of melodies of ``n`` notes, one a beat, in the major scale, that make a two-voice canon with
    themselves: the follower enters ``delay`` beats later, ``steps`` scale steps away (positive above), and from its
    entry every beat is consonant, no two beats in a row make parallel perfect intervals, and the leader moves only
    by allowed leaps.  The leader starts on the tonic; with ``cadence`` it also ends on the tonic.  Exact, by
    dynamic programming over the leader's last ``delay`` notes."""
    notes = notes or scale_notes(60, 79, tonic)
    idx = {p: i for i, p in enumerate(notes)}
    follow = {p: diatonic(p, steps, tonic) for p in notes}

    @lru_cache(maxsize=None)
    def go(k: int, last: tuple) -> int:
        if k == n:
            return 1 if (not cadence or (last[-1] - tonic) % 12 == 0) else 0
        tot = 0
        for x in notes:
            if not _ok_move(last[-1], x):
                continue
            if k >= delay:
                y = follow[last[-delay]]
                if not _vert_ok(x, y):
                    continue
                if k > delay:
                    x0, y0 = last[-1], follow[last[-delay - 1]] if len(last) > delay else None
                    if y0 is not None and _parallel(x0, y0, x, y):
                        continue
            tot += go(k + 1, (last + (x,))[-(delay + 1):])
        return tot

    starts = [p for p in notes if (p - tonic) % 12 == 0]
    return sum(go(1, (s,)) for s in starts)


def sample_canon(n: int, delay: int, steps: int, rng=None, notes=None, tonic: int = 0, tries: int = 20000) -> list[int] | None:
    """One canon melody of the kind ``count_canons`` counts, by randomized depth-first search with a preference for
    steps over leaps."""
    rng = rng or np.random.default_rng(0)
    notes = notes or scale_notes(60, 79, tonic)
    follow = {p: diatonic(p, steps, tonic) for p in notes}
    budget = [tries]

    def ok(seq, x):
        k = len(seq)
        if not _ok_move(seq[-1], x):
            return False
        if k >= delay:
            y = follow[seq[k - delay]]
            if not _vert_ok(x, y):
                return False
            if k > delay and _parallel(seq[-1], follow[seq[k - delay - 1]], x, y):
                return False
        return True

    def dfs(seq):
        budget[0] -= 1
        if budget[0] < 0:
            return None
        if len(seq) == n:
            return seq if (seq[-1] - tonic) % 12 == 0 else None
        cands = [x for x in notes if ok(seq, x)]
        w = np.array([1.0 / (1 + abs(x - seq[-1])) ** 1.5 for x in cands]) if cands else np.array([])
        order = list(rng.choice(len(cands), size=len(cands), replace=False, p=w / w.sum())) if cands else []
        for i in order:
            r = dfs(seq + [cands[i]])
            if r:
                return r
        return None

    start = [p for p in notes if (p - tonic) % 12 == 0]
    return dfs([start[0] if len(start) == 1 else start[int(rng.integers(0, len(start)))]])


def count_crabs(n: int, notes=None, tonic: int = 0) -> int:
    """The number of melodies of ``n`` notes (one a beat, major scale, allowed moves) that sound well against their own
    retrograde: note k against note n-1-k is consonant on every beat, with no parallel perfect intervals; the melody
    starts and ends on notes of the tonic triad.  Exact, by dynamic programming over pairs from both ends inwards."""
    notes = notes or scale_notes(60, 79, tonic)
    triad = {(tonic + i) % 12 for i in (0, 4, 7)}
    half = n // 2

    @lru_cache(maxsize=None)
    def go(i: int, a: int, b: int) -> int:
        # pair i is (x[i], x[n-1-i]) = (a, b); fill pair i+1
        if n % 2 == 0 and i == half - 1:
            # the middle: pair half is (b, a); voice A moves a -> b, voice B moves b -> a
            return 1 if _ok_move(a, b) else 0
        if n % 2 == 1 and i == half - 1:
            tot = 0
            for m in notes:                                # the middle note sounds against itself
                if _ok_move(a, m) and _ok_move(m, b) and not _parallel(a, b, m, m):
                    tot += 1
            return tot
        tot = 0
        for c in notes:
            if not _ok_move(a, c):
                continue
            for d in notes:
                if not _ok_move(d, b) or not _vert_ok(c, d) or _parallel(a, b, c, d):
                    continue
                tot += go(i + 1, c, d)
        return tot

    tot = 0
    for a in notes:
        for b in notes:
            if a % 12 in triad and b % 12 in triad and _vert_ok(a, b):
                tot += go(0, a, b)
    return tot


def sample_crab(n: int, rng=None, notes=None, tonic: int = 0, tries: int = 50000, head=None) -> list[int] | None:
    """A crab-canon melody by randomized search over pairs, optionally beginning with ``head``."""
    rng = rng or np.random.default_rng(0)
    notes = notes or scale_notes(60, 79, tonic)
    triad = {(tonic + i) % 12 for i in (0, 4, 7)}
    half = n // 2
    budget = [tries]

    def dfs(pairs):
        budget[0] -= 1
        if budget[0] < 0:
            return None
        i = len(pairs) - 1
        a, b = pairs[-1]
        if i == half - 1:
            if n % 2 == 0:
                if _ok_move(a, b):
                    return [p for p, _ in pairs] + [q for _, q in pairs][::-1]
                return None
            mids = [m for m in notes if _ok_move(a, m) and _ok_move(m, b) and not _parallel(a, b, m, m)]
            if not mids:
                return None
            m = mids[int(rng.integers(0, len(mids)))]
            return [p for p, _ in pairs] + [m] + [q for _, q in pairs][::-1]
        cs = []
        for c in notes:
            if head is not None and i + 1 < len(head) and c != head[i + 1]:
                continue
            if not _ok_move(a, c):
                continue
            for d in notes:
                if _ok_move(d, b) and _vert_ok(c, d) and not _parallel(a, b, c, d):
                    cs.append((c, d))
        if not cs:
            return None
        w = np.array([1.0 / (1 + abs(c - a) + abs(d - b)) ** 1.5 for c, d in cs])
        for j in rng.choice(len(cs), size=len(cs), replace=False, p=w / w.sum()):
            r = dfs(pairs + [cs[j]])
            if r:
                return r
        return None

    starts = [(a, b) for a in notes for b in notes if a % 12 in triad and b % 12 in triad and _vert_ok(a, b)
              and (head is None or a == head[0])]
    for j in rng.permutation(len(starts)):
        r = dfs([starts[j]])
        if r:
            return r
    return None


def crab_ok(mel) -> dict:
    """Judge a melody against its retrograde, beat by beat."""
    ln = line(mel)
    return faults([ln, retrograde(ln)], allow_upper_fourths=False)


# ---------------------------------------------------------------------------
# Invertible counterpoint
# ---------------------------------------------------------------------------
def invertible(at: int) -> dict:
    """What each consonance becomes when the upper voice is moved below the lower, at the octave (``at`` = 7 scale
    steps), the tenth (9) or the twelfth (11): an interval of s steps becomes at - s.  Steps 0..7: unison..octave."""
    cons = {0, 2, 4, 5, 7}                              # unison, third, fifth, sixth, octave, in scale steps
    out = {}
    for s in range(0, 8):
        t = at - s
        tc = t % 7 in {0, 2, 4, 5}
        out[s] = {"becomes": t, "consonant_before": s % 7 in {0, 2, 4, 5}, "consonant_after": tc,
                  "perfect_after": t % 7 in {0, 4}}
    return out


# ---------------------------------------------------------------------------
# Fugue: answers, a free voice, an exposition
# ---------------------------------------------------------------------------
def real_answer(subject, tonic: int = 0):
    return transpose(subject, 7)


def tonal_answer(subject, tonic: int = 0):
    """The answer in the dominant, with the head's tonic answered by the dominant and its dominant by the tonic (a
    fifth becomes a fourth), so that the answer does not leave the home key at once; after the head (the first note
    that is neither tonic nor dominant), the real answer: up a fifth, in the dominant key."""
    out, head = [], True
    for p, a, d in subject:
        pc = (p - tonic) % 12
        if head and pc in (0, 7):
            q = p + 7 if pc == 0 else p + 5
        else:
            head = False
            q = p + 7
        out.append((q, a, d))
    return out


def free_voice(others, grid, notes, start=None, stop=None, prefer_imperfect: bool = True, below: bool = False,
               ends=None, avoid=()) -> list[int] | None:
    """A Viterbi search for a voice of one note per grid point, consonant with every other voice sounding there (a
    fourth allowed above the lowest), with no parallel perfect intervals against any of them, moving by allowed steps
    and leaps; cost: the size of each move, a small penalty for perfect intervals and for repeated notes.  ``ends``
    fixes the (first, last) pitch classes; ``avoid`` lists intervals (mod 12) not to make against any other voice
    (a counter-line without fifths survives inversion at the octave)."""
    T = len(grid)
    INF = 1e18
    cost = [{p: INF for p in notes} for _ in range(T)]
    back = [{p: None for p in notes} for _ in range(T)]

    def ok_at(k, p):
        live = [s for s in (sounding(o, grid[k]) for o in others) if s is not None]
        bass = min(live + [p])
        for q in live:
            iv = abs(p - q) % 12
            if iv in avoid:
                return False
            if iv in CONSONANT:
                continue
            if iv == 5 and min(p, q) != bass:
                continue
            return False
        if below and live and p > min(live):
            return False
        if not below and live and p < max(live) and len(others) == 1:
            return False
        return True

    def pen(k, p):
        live = [s for s in (sounding(o, grid[k]) for o in others) if s is not None]
        return sum(0.6 for q in live if abs(p - q) % 12 in PERFECT) if prefer_imperfect else 0.0

    for p in notes:
        if ok_at(0, p) and (ends is None or p % 12 == ends[0]):
            cost[0][p] = pen(0, p)
    for k in range(1, T):
        prev_live = [sounding(o, grid[k - 1]) for o in others]
        live = [sounding(o, grid[k]) for o in others]
        for p in notes:
            if not ok_at(k, p):
                continue
            best, arg = INF, None
            for q in notes:
                c0 = cost[k - 1][q]
                if c0 >= INF:
                    continue
                m = abs(p - q)
                if m not in (0, 1, 2, 3, 4, 5, 7, 12):
                    continue
                bad = False
                for a0, a1 in zip(prev_live, live):
                    if a0 is not None and a1 is not None and _parallel(q, a0, p, a1):
                        bad = True
                        break
                if bad:
                    continue
                c = c0 + (0.25 * m if m <= 2 else 0.6 * m) + (2.5 if m == 0 else 0.0) + pen(k, p)
                if c < best:
                    best, arg = c, q
            cost[k][p], back[k][p] = best, arg
    finals = [p for p in notes if cost[-1][p] < INF and (ends is None or p % 12 == ends[1])]
    if not finals:
        return None
    p = min(finals, key=lambda x: cost[-1][x])
    out = [p]
    for k in range(T - 1, 0, -1):
        p = back[k][p]
        out.append(p)
    return out[::-1]


def round_census(tunes, voices: int = 3, beat: float = 2.0) -> list[dict]:
    """Rank tunes by how well they sing as rounds, at their best delay: dissonant strong beats per strong beat, plus a
    twentieth for each pair of parallels."""
    out = []
    for m in tunes:
        ln = line([60 + p for p in m.pitches], list(m.beats))
        if end(ln) < 8:
            continue
        d, s = best_round(ln, voices=voices, beat=beat)
        out.append({"name": m.name, "delay": d, "rate": s["rate"], "dissonant": s["dissonant"], "beats": s["beats"],
                    "parallels": s["parallels"]})
    return sorted(out, key=lambda r: (r["rate"] + 0.05 * r["parallels"], r["name"]))


# ---------------------------------------------------------------------------
# Two famous subjects, for the series (pitches as Bach wrote them; rhythm simplified)
# ---------------------------------------------------------------------------
ROYAL_THEME = [60, 63, 67, 68, 59, 67, 66, 65, 64, 63, 62, 61, 60, 59, 55, 60, 65, 63, 62, 60]
ROYAL_RHYTHM = [2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 2]
ART_OF_FUGUE = [62, 69, 65, 62, 61, 62, 64, 65, 67, 65, 64, 62]
ART_RHYTHM = [2, 2, 2, 2, 2, 1, 1, 1.5, 0.5, 0.5, 0.5, 2]
