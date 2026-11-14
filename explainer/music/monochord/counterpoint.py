"""Monochord's counterpoint (Part 16, *Two Voices*).

Two voices, each a good line, and both heard as two.  This module states Fux's rules for writing a line against a
cantus firmus, checks a line against them, counts every line that obeys them (exactly, by dynamic programming),
samples among those lines at random, writes lines in all five of Fux's species, and measures how independent two
voices are.

    FUX_DORIAN                         the cantus firmus of Fux's first exercise (1725)
    RULES                              the rules of first species, by name, each with the perceptual principle behind it
    check(cf, cp, rules)               the rules a first-species line breaks, and where
    count(cf, rules)                   how many first-species lines obey ``rules`` (dynamic programming over states)
    sample(cf, rules, rng)             one of those lines, every one equally likely
    best(cf, rules)                    the line a simple scoring of Fux's preferences likes best
    species(cf, n, rng)                a line in species 2, 3, 4 or 5, as (pitch, start, beats) events
    motions(a, b)                      parallel, similar, contrary and oblique motion between two voices
    independence(upper, lower)         how much the two voices fuse: perfect intervals reached in the same direction,
                                       motion types, onsets that coincide
    organum(cf, interval)              a voice moving in parallel with the cantus, as in the ninth century

Pitches are MIDI numbers; a cantus firmus is a list of them, one per bar.  Counterpoint is written above the cantus
unless ``below=True``.  No manim.  Checked in ``tests/music/test_counterpoint.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np

FUX_DORIAN = [62, 65, 64, 62, 67, 65, 69, 67, 65, 64, 62]       # D F E D G F A G F E D: Fux's first cantus firmus
WHITE = (0, 2, 4, 5, 7, 9, 11)
CONSONANT = {0, 3, 4, 7, 8, 9}                                  # unison/octave, thirds, fifth, sixths (mod 12)
PERFECT = {0, 7}
IMPERFECT = {3, 4, 8, 9}
MELODIC = {0, 1, 2, 3, 4, 5, 7, 12}                             # moves a line may make (semitones), plus the ascending minor sixth
NAMES = {"consonance": "only consonances against the cantus",
         "start": "begin on a perfect consonance",
         "cadence": "end on the octave or unison, by step, through the sixth or third",
         "unison": "no unison except at the ends",
         "parallel": "no parallel fifths or octaves",
         "direct": "no perfect consonance reached by similar motion",
         "melodic": "no tritones, sevenths or leaps larger than an octave",
         "repeat": "no repeated notes",
         "recovery": "after a leap larger than a third, a step back",
         "run": "no more than three parallel thirds or sixths in a row",
         "spacing": "no crossing, and no more than a tenth apart",
         "climax": "a single highest note"}
PRINCIPLE = {"consonance": "consonant intervals do not mask or roughen each other (Parts 4 and 5)",
             "start": "a perfect consonance establishes the mode",
             "cadence": "the leading note and the closing perfect consonance mark the end (Part 15)",
             "unison": "a unison is one note: the two voices disappear into each other",
             "parallel": "tonal fusion plus co-modulation: two voices that fuse and move together become one",
             "direct": "co-modulation into a fused interval",
             "melodic": "pitch proximity: a line that leaps far or awkwardly breaks into pieces (Part 14)",
             "repeat": "a line that stands still stops being a line",
             "recovery": "regression to the middle of the range (Part 14)",
             "run": "parallel imperfect intervals also co-modulate, if they go on long enough",
             "spacing": "crossed voices swap identities; far-apart voices stop interacting",
             "climax": "an arch with one peak (Part 14)"}
RULES = tuple(NAMES)


def vertical(cf: int, cp: int, below: bool = False) -> int:
    """The interval between the voices in semitones, measured upward from the lower voice."""
    return cf - cp if below else cp - cf


def motion(a0: int, a1: int, b0: int, b1: int) -> str:
    """How two voices move from one moment to the next: parallel (same direction, same interval class), similar,
    contrary or oblique (one voice stays)."""
    da, db = a1 - a0, b1 - b0
    if da == 0 and db == 0:
        return "static"
    if da == 0 or db == 0:
        return "oblique"
    if (da > 0) != (db > 0):
        return "contrary"
    return "parallel" if (a1 - b1) % 12 == (a0 - b0) % 12 else "similar"


def candidates(cf, below: bool = False, compass: tuple[int, int] | None = None) -> list[list[int]]:
    """The notes the counterpoint may use against each note of the cantus: the white keys in its compass (a twelfth
    above the cantus's lowest note to a tenth above its highest, or the mirror below), and at the penultimate note the
    leading note a semitone below the final (musica ficta) where the mode lacks it."""
    lo_cf, hi_cf = min(cf), max(cf)
    lo, hi = compass if compass is not None else ((lo_cf, hi_cf + 16) if not below else (lo_cf - 16, hi_cf))
    white = [m for m in range(lo, hi + 1) if m % 12 in WHITE]
    out = [list(white) for _ in cf]
    final = cf[-1]
    lead = [m for m in range(lo, hi + 1) if (m - final) % 12 == 11]          # a semitone below the final, in every octave
    out[-2] = sorted(set(out[-2]) | set(lead))
    return out


def _ok_melodic(prev: int, cur: int) -> bool:
    d = cur - prev
    return abs(d) in MELODIC or d == 8


@dataclass(frozen=True)
class _Ctx:
    cf: tuple
    rules: frozenset
    below: bool
    cands: tuple


def _allowed(ctx: _Ctx, i: int, prev: int | None, prev_move: int, run: int, cp: int) -> tuple[bool, int]:
    """Whether ``cp`` may follow ``prev`` against cantus note ``i``, and the new run of parallel imperfect intervals."""
    cf, R, below = ctx.cf, ctx.rules, ctx.below
    n = len(cf)
    v = vertical(cf[i], cp, below)
    if "spacing" in R and not (0 <= v <= 16):
        return False, 0
    vc = v % 12
    if "consonance" in R and vc not in CONSONANT:
        return False, 0
    if "unison" in R and v == 0 and 0 < i < n - 1:
        return False, 0
    if i == 0:
        if "start" in R and not (vc in PERFECT and (not below or vc == 0)):
            return False, 0
        return True, 0
    if "repeat" in R and cp == prev:
        return False, 0
    if "melodic" in R and not _ok_melodic(prev, cp):
        return False, 0
    move = cp - prev
    if "recovery" in R and abs(prev_move) > 4 and not (0 < abs(move) <= 2 and (move > 0) != (prev_move > 0)):
        return False, 0
    pv = vertical(cf[i - 1], prev, below)
    m = motion(prev, cp, cf[i - 1], cf[i])
    if "parallel" in R and vc in PERFECT and pv % 12 == vc and m == "parallel":
        return False, 0
    if "direct" in R and vc in PERFECT and m in ("similar", "parallel"):
        return False, 0
    new_run = run + 1 if (m == "parallel" and vc in IMPERFECT and pv % 12 in IMPERFECT and (vc in (3, 4)) == (pv % 12 in (3, 4))) else 0
    if "run" in R and new_run >= 3:
        return False, 0
    if i == n - 1 and "cadence" in R:
        if vc != 0 or abs(move) > 2:
            return False, 0
        if (pv in (9, 3) if not below else pv in (3, 15)) is False:
            return False, 0
    if i == n - 2 and "cadence" in R:
        final = cf[-1]
        # the counterpoint is a step from its final note: above, the leading note under the octave; below, the step above
        if not below and (cp - final) % 12 != 11:
            return False, 0
        if below and (cp - final) % 12 != 2:
            return False, 0
    return True, new_run


def _key(rules) -> frozenset:
    return frozenset(RULES if rules is None else rules)


def count(cf, rules=None, below: bool = False, compass=None) -> int:
    """The number of first-species lines against ``cf`` that obey every rule in ``rules`` (all of them by default)."""
    ctx = _Ctx(tuple(cf), _key(rules), below, tuple(tuple(c) for c in candidates(cf, below, compass)))
    return _counter(ctx)(0, None, 0, 0, 999, -999, 0)


def _counter(ctx: _Ctx):
    n = len(ctx.cf)
    climax = "climax" in ctx.rules

    @lru_cache(maxsize=None)
    def go(i, prev, prev_move, run, hi, hicount, _unused=0):
        if i == n:
            return 1 if (not climax or hicount == 1) else 0
        total = 0
        for cp in ctx.cands[i]:
            ok, nr = _allowed(ctx, i, prev, prev_move, run, cp)
            if not ok:
                continue
            nh, nc = (cp, 1) if cp > hi else ((hi, hicount + 1) if cp == hi else (hi, hicount))
            if climax and nc > 1 and nh == hi and cp == hi:
                pass                                                    # a repeated peak can still be overtaken later
            total += go(i + 1, cp, 0 if prev is None else cp - prev, nr, nh, nc)
        return total

    def start(i, prev, prev_move, run, lo, hi, hicount):
        return go(i, prev, prev_move, run, hi, hicount)

    start.go = go
    return start


def sample(cf, rules=None, rng=None, below: bool = False, compass=None) -> list[int] | None:
    """One line chosen uniformly at random from all those that obey ``rules``."""
    rng = np.random.default_rng() if rng is None else rng
    ctx = _Ctx(tuple(cf), _key(rules), below, tuple(tuple(c) for c in candidates(cf, below, compass)))
    go = _counter(ctx).go
    n = len(cf)
    state = (0, None, 0, 0, -999, 0)
    if go(*state) == 0:
        return None
    out = []
    i, prev, pm, run, hi, hc = state
    while i < n:
        options, weights = [], []
        for cp in ctx.cands[i]:
            ok, nr = _allowed(ctx, i, prev, pm, run, cp)
            if not ok:
                continue
            nh, nc = (cp, 1) if cp > hi else ((hi, hc + 1) if cp == hi else (hi, hc))
            w = go(i + 1, cp, 0 if prev is None else cp - prev, nr, nh, nc)
            if w:
                options.append((cp, nr, nh, nc))
                weights.append(w)
        p = np.array(weights, dtype=float)
        cp, nr, nh, nc = options[int(rng.choice(len(options), p=p / p.sum()))]
        pm = 0 if prev is None else cp - prev
        out.append(cp)
        i, prev, run, hi, hc = i + 1, cp, nr, nh, nc
    return out


def check(cf, cp, rules=None, below: bool = False) -> list[tuple[int, str]]:
    """Every (bar, rule) that a first-species line breaks.  The state the rules depend on (the last move, the run of
    parallel imperfect intervals) is carried along exactly as in ``count``."""
    R = _key(rules)
    out = []
    run, prev_move = 0, 0
    free = _Ctx(tuple(cf), frozenset(), below, ())
    for i in range(len(cf)):
        prev = cp[i - 1] if i else None
        for rule in R:
            if rule == "climax":
                continue
            ok, _ = _allowed(_Ctx(tuple(cf), frozenset({rule}), below, ()), i, prev, prev_move, run, cp[i])
            if not ok:
                out.append((i, rule))
        _, run = _allowed(free, i, prev, prev_move, run, cp[i])
        prev_move = 0 if i == 0 else cp[i] - cp[i - 1]
    if "climax" in R and sum(1 for x in cp if x == max(cp)) > 1:
        out.append((int(np.argmax(cp)), "climax"))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# Preferences: what Fux recommends but does not forbid
# ---------------------------------------------------------------------------
def score(cf, cp, below: bool = False) -> float:
    """Higher is better: contrary motion, imperfect consonances, steps, a climax away from the ends, variety."""
    s = 0.0
    n = len(cf)
    for i in range(1, n):
        m = motion(cp[i - 1], cp[i], cf[i - 1], cf[i])
        s += {"contrary": 2.0, "oblique": 0.5, "similar": 0.0, "parallel": -0.5, "static": -2.0}[m]
        v = vertical(cf[i], cp[i], below) % 12
        s += 0.8 if v in IMPERFECT else 0.0
        d = abs(cp[i] - cp[i - 1])
        s += 0.6 if d <= 2 else (0.0 if d <= 5 else -0.8)
    k = int(np.argmax(cp))
    s += 1.5 if 0.3 * n <= k <= 0.8 * n else 0.0
    s += 0.3 * len(set(cp))
    return s


def best(cf, rules=None, below: bool = False, tries: int = 3000, seed: int = 0) -> list[int]:
    """The best-scoring of many lines sampled uniformly from those that obey the rules."""
    rng = np.random.default_rng(seed)
    pool = [sample(cf, rules, rng, below) for _ in range(tries)]
    pool = [p for p in pool if p is not None]
    return max(pool, key=lambda p: (score(cf, p, below), tuple(p)))


# ---------------------------------------------------------------------------
# Species 2 to 5: lines as events (pitch, start, beats), a bar of the cantus being four beats
# ---------------------------------------------------------------------------
def _is_cons(cf_note: int, p: int) -> bool:
    return (p - cf_note) % 12 in CONSONANT and 0 <= p - cf_note <= 16


def _step(p: int, d: int) -> int:
    """The white key ``d`` scale steps above (``d`` > 0) or below ``p``."""
    q = p
    for _ in range(abs(d)):
        q += 1 if d > 0 else -1
        while q % 12 not in WHITE:
            q += 1 if d > 0 else -1
    return q


def _patterns(n: int, c: int, prev: int | None, first: bool, pen: bool, lead: int, rng) -> list[tuple]:
    """Candidate bars for species ``n`` over cantus note ``c``: tuples of (pitch, beats, tied).  Dissonances are
    allowed only where the species allows them, and are checked against the next note later."""
    near = [p for p in range(c, c + 17) if p % 12 in WHITE and _is_cons(c, p) and (prev is None or (p != prev and _ok_melodic(prev, p)))]
    if first:
        near = [p for p in near if (p - c) % 12 in PERFECT and p > c]
    rng.shuffle(near)
    near.sort(key=lambda p: 0 if prev is None else abs(p - prev) + rng.random() * 3)
    near = near[:5]
    out = []
    if n == 2:
        for x in near:
            if pen:
                if abs(x - lead) <= 4 and x != lead:
                    out.append(((x, 2.0, False), (lead, 2.0, False)))
                continue
            for d in (-2, -1, 1, 2):
                y = _step(x, d)
                if y != x and c <= y <= c + 16:
                    out.append(((x, 2.0, False), (y, 2.0, False)))
    elif n == 3:
        for x in near:
            shapes = []
            for d in (-1, 1):
                shapes += [(x, _step(x, d), _step(x, 2 * d), _step(x, 3 * d)), (x, _step(x, d), x, _step(x, -d)), (x, _step(x, 2 * d), _step(x, d), _step(x, 2 * d)),
                           (x, _step(x, d), _step(x, 2 * d), _step(x, d))]
            letter = lead if lead is not None and lead % 12 in WHITE else (None if lead is None else lead - 1)
            for sh in shapes:
                if pen:
                    if sh[-1] != letter:
                        continue
                    sh = sh[:-1] + (lead,)                               # the leading note, raised where the mode needs it
                if all(c <= q <= c + 16 for q in sh):
                    out.append(tuple((q, 1.0, False) for q in sh))
    elif n == 4:
        held = [prev] if prev is not None else []
        for h in held:
            if pen:
                if not _is_cons(c, h) and _step(h, -1) == lead:
                    out.append(((h, 2.0, True), (lead, 2.0, False)))
                elif _is_cons(c, h) and h != lead and abs(h - lead) <= 4:
                    out.append(((h, 2.0, True), (lead, 2.0, False)))
                continue
            if not _is_cons(c, h):
                r = _step(h, -1)
                if _is_cons(c, r) and (r - c) % 12 in IMPERFECT:
                    out.append(((h, 2.0, True), (r, 2.0, False)))
                continue
            for y in near:
                if y != h:
                    out.append(((h, 2.0, True), (y, 2.0, False)))
        if first:
            out = [((None, 2.0, False), (x, 2.0, False)) for x in near]
    rng.shuffle(out)
    return out


def _bar_ok(c: int, nxt_c: int | None, bar: tuple, nxt_first: int | None, prev: int | None, prev_down: tuple | None, n: int) -> bool:
    """Local checks on a bar: the downbeat is consonant unless it is a prepared suspension; a weak-beat dissonance
    is approached and left by step in one direction (passing) or returns (neighbour); no perfect interval reached by
    similar motion on a downbeat; no fifths or octaves on successive downbeats."""
    ps = [q for q, _, _ in bar if q is not None]
    if any(q == c for q in ps):
        return False                                                 # no unison with the cantus except at the end
    seq = ([prev] if prev is not None else []) + ps + ([nxt_first] if nxt_first is not None else [])
    for a, b in zip(seq, seq[1:]):
        if a == b and not (n == 4):
            return False
        if not _ok_melodic(a, b) and a != b:
            return False
    for k, (q, beats, tied) in enumerate(bar):
        if q is None:
            continue
        if _is_cons(c, q):
            continue
        if k == 0 and n == 4 and tied:
            continue                                                 # a suspension: checked when the patterns are made
        if k == 0:
            return False
        before = bar[k - 1][0] if bar[k - 1][0] is not None else prev
        after = bar[k + 1][0] if k + 1 < len(bar) else nxt_first
        if before is None or after is None or abs(q - before) > 2 or abs(after - q) > 2 or after == q:
            return False
    down = bar[0][0] if bar[0][0] is not None else bar[1][0]
    if prev_down is not None and down is not None:
        pc, pq = prev_down
        v, pv = (down - c) % 12, (pq - pc) % 12
        if v in PERFECT and v == pv and down != pq:
            return False
        if v in PERFECT and prev is not None and motion(prev, down, pc, c) in ("parallel", "similar") and not bar[0][2]:
            return False
    return True


def species(cf, n: int, rng=None, tries: int = 400) -> list[tuple[int, float, float]] | None:
    """A line above ``cf`` in species ``n``: 1, one note to a bar; 2, two, with passing dissonances on the weak
    beat; 3, four, with passing and neighbouring dissonances; 4, syncopated, with suspensions that resolve down by
    step; 5, the four mixed.  Randomized depth-first search, bar by bar; the best-scoring of ``tries`` attempts.
    Returns (pitch, start beat, beats) events, a bar being four beats; tied notes are merged."""
    rng = np.random.default_rng(0) if rng is None else rng
    if n == 1:
        cp = best(cf, tries=max(tries, 500), seed=int(rng.integers(0, 10_000)))
        return [(p, 4.0 * k, 4.0) for k, p in enumerate(cp)]
    best_line, best_s = None, -1e9
    final = cf[-1]
    for _ in range(tries):
        kinds = [n if n != 5 else int(rng.choice([2, 3, 4, 3, 2])) for _ in cf]
        if n == 5:
            kinds[0], kinds[-2] = 2, 4
        line = _search(cf, kinds, final, rng)
        if line is None:
            continue
        s = _species_score(cf, line)
        if s > best_s:
            best_line, best_s = line, s
    return best_line


def _search(cf, kinds, final, rng, budget: int = 3000):
    bars = len(cf)
    lead_all = [p for p in range(min(cf), max(cf) + 17) if (p - final) % 12 == 11]
    calls = [0]

    def go(b, prev, prev_down, acc):
        calls[0] += 1
        if calls[0] > budget:
            return None
        c = cf[b]
        if b == bars - 1:
            ends = [p for p in range(c, c + 17) if (p - final) % 12 == 0 and prev is not None and 0 < abs(p - prev) <= 2]
            if not ends:
                return None
            return acc + [((ends[0], 4.0, False),)]
        pen = b == bars - 2
        lead = min(lead_all, key=lambda p: abs(p - (prev if prev is not None else p))) if lead_all else None
        if pen and lead is not None and lead <= c:
            return None
        for bar in _patterns(kinds[b], c, prev, b == 0, pen, lead, rng):
            nxt_first = None
            if not _bar_ok(c, cf[b + 1], bar, None, prev, prev_down, kinds[b]):
                continue
            last = bar[-1][0]
            down = bar[0][0] if bar[0][0] is not None else bar[1][0]
            res = go(b + 1, last, (c, down), acc + [bar])
            if res is not None:
                # a weak-beat dissonance at the end of this bar must step to the next downbeat
                nb = res[b + 1]
                nd = nb[0][0]
                q = bar[-1][0]
                if not _is_cons(c, q) and (nd is None or abs(nd - q) > 2 or nd == q):
                    continue
                return res
        return None

    bars_out = go(0, None, None, [])
    if bars_out is None:
        return None
    events, t = [], 0.0
    for b, bar in enumerate(bars_out):
        for q, beats, tied in bar:
            if q is not None:
                if tied and events and events[-1][0] == q:
                    p0, a0, d0 = events[-1]
                    events[-1] = (p0, a0, d0 + beats)
                else:
                    events.append((q, t, beats))
            t += beats
    return events


def _species_score(cf, line) -> float:
    s = 0.0
    ps = [p for p, _, _ in line]
    for a, b in zip(ps, ps[1:]):
        d = abs(b - a)
        s += 0.4 if 1 <= d <= 2 else (-0.8 if d > 5 else 0.0)
    s -= 1.0 * sum(1 for a, b, c_, d in zip(ps, ps[1:], ps[2:], ps[3:]) if a == c_ and b == d)      # a two-note cell said over and over
    s += 0.15 * len(set(ps))
    top = max(ps)
    s += 1.5 if ps.count(top) == 1 else -1.0
    ind = independence(line, [(c, 4.0 * k, 4.0) for k, c in enumerate(cf)])
    s += 4.0 * ind["contrary"] - 8.0 * ind["fused"]
    return s


# ---------------------------------------------------------------------------
# Independence
# ---------------------------------------------------------------------------
def _sounding(events, t: float):
    for p, a, d in events:
        if a <= t + 1e-9 < a + d:
            return p
    return None


FUSING = {0, 5, 7}                                              # unison/octave, fourth, fifth: the intervals that fuse most (Part 4)


def independence(upper, lower) -> dict:
    """How independent two voices are, from (pitch, start, beats) events.  At every moment when either voice
    begins a note: the motion since the last such moment, and whether the two notes there form a fusing interval
    (octave, fifth or fourth) reached with both voices moving in the same direction (a "fused" moment, by Huron's
    principles of tonal fusion and co-modulation); and whether the two voices began together.  Shares of motion
    and of fused moments are over the moments where at least one voice moved."""
    times = sorted({a for _, a, _ in upper} | {a for _, a, _ in lower})
    pairs = [(t, _sounding(upper, t), _sounding(lower, t)) for t in times]
    pairs = [x for x in pairs if x[1] is not None and x[2] is not None]
    starts_u, starts_l = {a for _, a, _ in upper}, {a for _, a, _ in lower}
    kinds = {"parallel": 0, "similar": 0, "contrary": 0, "oblique": 0}
    fused = fusing = 0
    for (t0, u0, l0), (t1, u1, l1) in zip(pairs, pairs[1:]):
        m = motion(u0, u1, l0, l1)
        if m == "static":
            continue
        kinds[m] += 1
        v = abs(u1 - l1) % 12
        if v in FUSING:
            fusing += 1
            if m in ("parallel", "similar"):
                fused += 1
    together = sum(1 for t, _, _ in pairs if t in starts_u and t in starts_l)
    moves = max(sum(kinds.values()), 1)
    return {**{k: v / moves for k, v in kinds.items()}, "fused": fused / moves, "fusing": fusing / moves, "together": together / max(len(pairs), 1),
            "moments": len(pairs), "moves": sum(kinds.values())}


def organum(cf, interval: int = -7) -> list[int]:
    """A second voice in strict parallel with the cantus, ``interval`` semitones away (a fifth below by default):
    the parallel organum described in the *Musica enchiriadis* (about 900)."""
    return [c + interval for c in cf]


def first_species_events(cf, cp) -> tuple[list, list]:
    return [(p, 4.0 * k, 4.0) for k, p in enumerate(cp)], [(c, 4.0 * k, 4.0) for k, c in enumerate(cf)]


def funnel(cf, order=None) -> list[tuple[str, int]]:
    """How many lines remain as the rules are added one at a time, starting from any notes at all."""
    order = list(RULES) if order is None else order
    out = [("no rules", count(cf, rules=()))]
    have = []
    for r in order:
        have.append(r)
        out.append((r, count(cf, rules=tuple(have))))
    return out
