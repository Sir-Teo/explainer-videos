"""Monochord's composer (Part 42 of *Music, Built*): composing as search under constraints.

A melody is a list of notes ``(key number, onset in beats, length in beats)``, in C major unless said otherwise.

    MOTIVE, OPS                  a motive of ours and Schoenberg's operations on it (transposition, inversion,
                                 retrograde, augmentation, diminution, fragmentation, interval change, new rhythm,
                                 embellishment), all diatonic
    derive(a, b)                 the shortest chain of operations (up to two, transposition free) taking a to b
    develop(motive, plan)        a phrase built by developing variation: each bar the motive under a chain of operations
    count_funnel(n, rules)       how many n-note melodies obey a growing list of rules, counted exactly
    dice_table(seed)             a minuet dice game of ours: 16 bars, 11 options a bar, read by the sum of two dice
    dice_count(table)            distinct minuets, the probability of the likeliest, and the entropy in bits
    illiac(n, rng)               Hiller and Isaacson's method: draw a note, test it against rules, draw again; back up
                                 when stuck; every rejection counted
    markov(corpus, order)        a chain over a corpus of tunes; generate(); longest_copy() measures plagiarism
    critics                      harmony fit, leaps recovered, range, parallels with the bass, the cadence, unity,
                                 variety, and the fit to a tension plan
    tension(mel, chords)         a bar-by-bar tension curve from height, non-chord tones, harmony and density
    compose(motive, chords, ...) generate and test: random developing variations judged by the critics; every rejected
                                 draft is kept with its reason
    evolve(...)                  the same critics as a fitness, by a genetic algorithm

No manim here.  Checked in ``tests/music/test_composer.py``.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from functools import lru_cache

import numpy as np

MAJOR = (0, 2, 4, 5, 7, 9, 11)
MOTIVE = [(64, 0.0, 0.5), (62, 0.5, 0.5), (60, 1.0, 1.0), (67, 2.0, 2.0)]   # E D C, then up a fifth to G: ours
CHORDS = {"I": (0, 4, 7), "ii": (2, 5, 9), "iii": (4, 7, 11), "IV": (5, 9, 0), "V": (7, 11, 2), "vi": (9, 0, 4),
          "V7": (7, 11, 2, 5), "viio": (11, 2, 5)}
ROOT = {"I": 48, "ii": 50, "iii": 52, "IV": 53, "V": 55, "vi": 45, "V7": 55, "viio": 47}
DISTANCE = {"I": 0.0, "vi": 1.0, "iii": 1.0, "IV": 1.0, "ii": 1.5, "V": 1.5, "V7": 2.0, "viio": 2.0}


# --------------------------------------------------------------------------------------------- diatonic helpers
def deg(m: int) -> int:
    """Diatonic index of a white key (C4 = 28); a black key takes the step below."""
    pc = m % 12
    return 7 * (m // 12) + max(i for i, s in enumerate(MAJOR) if s <= pc)


def key_of(d: int) -> int:
    return 12 * (d // 7) + MAJOR[d % 7]


def dstep(m: int, k: int) -> int:
    return key_of(deg(m) + k)


def pitches(mel) -> list[int]:
    return [n[0] for n in mel]


def length(mel) -> float:
    return max(a + d for _, a, d in mel) - min(a for _, a, _ in mel)


def shift_time(mel, t0: float):
    a0 = min(a for _, a, _ in mel)
    return [(m, a - a0 + t0, d) for m, a, d in mel]


# --------------------------------------------------------------------------------------------- operations
def transpose(mel, k: int):
    return [(dstep(m, k), a, d) for m, a, d in mel]


def invert(mel):
    ax = deg(mel[0][0])
    return [(key_of(2 * ax - deg(m)), a, d) for m, a, d in mel]


def retrograde(mel):
    end = max(a + d for _, a, d in mel)
    return sorted([(m, end - a - d, d) for m, a, d in mel], key=lambda n: n[1])


def augment(mel, f: float = 2.0):
    a0 = mel[0][1]
    return [(m, a0 + (a - a0) * f, d * f) for m, a, d in mel]


def diminish(mel):
    return augment(mel, 0.5)


def fragment(mel, k: int = 2):
    return [tuple(n) for n in mel[:k]]


def expand(mel):
    """Widen the largest interval by one step, moving everything after it."""
    p = pitches(mel)
    iv = [deg(b) - deg(a) for a, b in zip(p, p[1:])]
    i = int(np.argmax(np.abs(iv)))
    s = 1 if iv[i] >= 0 else -1
    return [(dstep(m, s) if j > i else m, a, d) for j, (m, a, d) in enumerate(mel)]


def rerhythm(mel):
    """The same pitches in even notes over the same span."""
    a0, span = mel[0][1], length(mel)
    n = len(mel)
    return [(m, a0 + span * j / n, span / n) for j, (m, _, _) in enumerate(mel)]


def embellish(mel):
    """Fill every leap of a third or more with a scale run, in the time of the note before it."""
    out = []
    for j, (m, a, d) in enumerate(mel):
        if j + 1 < len(mel) and abs(deg(mel[j + 1][0]) - deg(m)) >= 2:
            k = deg(mel[j + 1][0]) - deg(m)
            s = 1 if k > 0 else -1
            run = [dstep(m, s * i) for i in range(abs(k))]
            out += [(x, a + d * i / len(run), d / len(run)) for i, x in enumerate(run)]
        else:
            out.append((m, a, d))
    return out


OPS = {"transpose up a step": lambda m: transpose(m, 1), "transpose down a step": lambda m: transpose(m, -1),
       "invert": invert, "retrograde": retrograde, "augment": augment, "diminish": diminish,
       "fragment": lambda m: fragment(m, 2), "expand an interval": expand, "new rhythm": rerhythm, "embellish": embellish}


def _norm(mel):
    """Shape of a melody up to transposition and starting time: (diatonic steps, onsets, lengths)."""
    d0, a0 = deg(mel[0][0]), mel[0][1]
    return tuple((deg(m) - d0, round(a - a0, 4), round(d, 4)) for m, a, d in mel)


def derive(a, b, depth: int = 2):
    """The shortest chain of operations (each one of OPS; transposition is free) that turns ``a`` into ``b``, or None."""
    r = _derive(_norm(a), _norm(b), depth)
    return None if r is None else list(r)


@lru_cache(maxsize=200000)
def _derive(na, goal, depth):
    a = [(key_of(35 + st), on, d) for st, on, d in na]
    if na == goal:
        return ()
    frontier = [((), a)]
    for _ in range(depth):
        nxt = []
        for chain, m in frontier:
            for name, f in OPS.items():
                if name.startswith("transpose"):
                    continue
                y = f(m)
                if _norm(y) == goal:
                    return chain + (name,)
                nxt.append((chain + (name,), y))
        frontier = nxt
    return None


def develop(motive, plan, bar: float = 4.0):
    """plan: one entry a bar, each a list of operation names and a diatonic transposition: ``([ops], k)``.  The result
    sits each bar's figure at the bar's start; a bar is padded by lengthening its last note."""
    out = []
    for b, (ops, k) in enumerate(plan):
        m = [tuple(n) for n in motive]
        for name in ops:
            m = OPS[name](m)
        m = transpose(m, k)
        m = shift_time(m, b * bar)
        end = max(a + d for _, a, d in m)
        if end < (b + 1) * bar - 1e-9:
            last = m[-1]
            m[-1] = (last[0], last[1], (b + 1) * bar - last[1])
        out += [n for n in m if n[1] < (b + 1) * bar - 1e-9]
    return out


# --------------------------------------------------------------------------------------------- the funnel
FUNNEL_RULES = ("start and end on C", "no leap larger than a fifth", "a leap is followed by a step back",
                "no note three times running", "within an octave")


def count_funnel(n: int = 8, lo: int = 0, hi: int = 14, rules=FUNNEL_RULES) -> int:
    """How many n-note melodies on the white keys ``lo..hi`` (diatonic steps above C4) obey ``rules``, counted exactly
    by dynamic programming over (last note, last move, repeats, lowest, highest)."""
    rules = set(rules)
    notes = list(range(lo, hi + 1))
    starts = [x for x in notes if x % 7 == 0] if "start and end on C" in rules else notes

    @lru_cache(maxsize=None)
    def ways(i, last, move, reps, mn, mx):
        if i == n:
            if "start and end on C" in rules and last % 7:
                return 0
            return 1
        tot = 0
        for x in notes:
            s = x - last
            if "no leap larger than a fifth" in rules and abs(s) > 4:
                continue
            if "a leap is followed by a step back" in rules and abs(move) >= 2 and not (abs(s) == 1 and s * move < 0):
                continue
            r = reps + 1 if s == 0 else 1
            if "no note three times running" in rules and r >= 3:
                continue
            a, b = min(mn, x), max(mx, x)
            if "within an octave" in rules and b - a > 7:
                continue
            tot += ways(i + 1, x, s, r, a, b)
        return tot

    return sum(ways(1, x, 0, 1, x, x) for x in starts)


# --------------------------------------------------------------------------------------------- the dice game
MINUET_PLAN = ["I", "V", "I", "IV", "V", "I", "ii", "V", "I", "IV", "I", "V", "vi", "ii", "V", "I"]
DICE_P = {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}


def _figures():
    """Three-beat melodic figures over a chord, as (scale steps from the chord tone it starts on, onsets, lengths):
    each starts on a chord tone, the way the dice games' bars do, so that any can follow any."""
    return [((0, 0, 0), (0, 1, 2), (1, 1, 1)), ((0, 2, 4), (0, 1, 2), (1, 1, 1)), ((0, -1, 0), (0, 1, 2), (1, 1, 1)),
            ((0, 1, 2, 0), (0, 1, 1.5, 2), (1, 0.5, 0.5, 1)), ((0, 2, 1, 0), (0, 1, 1.5, 2), (1, 0.5, 0.5, 1)),
            ((0, -2), (0, 2), (2, 1)), ((0, 1, 0, -1, 0), (0, 0.5, 1, 1.5, 2), (0.5, 0.5, 0.5, 0.5, 1)),
            ((4, 2, 0), (0, 1, 2), (1, 1, 1)), ((0, 1, 2, 3, 4), (0, 0.5, 1, 1.5, 2), (0.5, 0.5, 0.5, 0.5, 1)),
            ((2, 1, 0), (0, 1, 2), (1, 1, 1)), ((0, 4), (0, 1), (1, 2))]


def dice_table(seed: int = 42, plan=MINUET_PLAN) -> list[dict]:
    """16 bars of 3/4, each with eleven options (sums 2 to 12) over the bar's chord in the plan.  Every option starts
    on a chord tone between E5 and C6, so any option can follow any other; the last bar of each half is the same for
    every sum (a cadence), as in the eighteenth-century games."""
    rng = np.random.default_rng(seed)
    figs = _figures()
    table = []
    for b, sym in enumerate(plan):
        tones = [m for m in range(64, 85) if m % 12 in CHORDS[sym]]
        cadence = b in (7, 15)
        opts = {}
        for s in range(2, 13):
            if cadence:
                top = 72 if sym == "I" else 74
                mel = ((top, 0.0, 3.0),) if sym == "I" else ((74, 0.0, 1.0), (71, 1.0, 1.0), (67, 2.0, 1.0))
            else:
                steps, ons, lens = figs[int(rng.integers(len(figs)))]
                start = int(rng.choice([t for t in tones if 72 <= t <= 79]))
                mel = tuple((dstep(start, k), float(o), float(l)) for k, o, l in zip(steps, ons, lens))
            r = ROOT[sym]
            bass = ((r, 0.0, 1.0), (r + 12 if sym != "vi" else r + 12, 1.0, 1.0), (dstep(r + 12, 2), 2.0, 1.0))
            opts[s] = {"melody": mel, "bass": bass, "chord": sym}
        table.append(opts)
    # the games repeat some bars under several sums; ours does too, so counting must look at the music, not the sums
    for b in (3, 11):
        table[b][12] = table[b][2]
    return table


def dice_piece(table, sums) -> tuple[list, list]:
    mel, bass = [], []
    for b, s in enumerate(sums):
        o = table[b][s]
        mel += [(m, 3 * b + a, d) for m, a, d in o["melody"]]
        bass += [(m, 3 * b + a, d) for m, a, d in o["bass"]]
    return mel, bass


def dice_count(table) -> dict:
    """Distinct minuets (bars told apart by their notes), the probability of the likeliest one, and the entropy of
    the game in bits; a bar's distinct options carry the summed probabilities of the sums that choose them."""
    distinct, pmax, H = 1, 1.0, 0.0
    per_bar = []
    for opts in table:
        mass = defaultdict(float)
        for s, o in opts.items():
            mass[(o["melody"], o["bass"])] += DICE_P[s]
        distinct *= len(mass)
        pmax *= max(mass.values())
        H += -sum(p * math.log2(p) for p in mass.values())
        per_bar.append(len(mass))
    return {"distinct": distinct, "naive": 11 ** len(table), "p_likeliest": pmax, "entropy_bits": H, "per_bar": per_bar,
            "uniform_bits": math.log2(distinct)}


def dice_joins(table) -> int:
    """The widest melodic leap (semitones) over every pair of consecutive options: small means any can follow any."""
    worst = 0
    for b in range(len(table) - 1):
        for o1 in table[b].values():
            for o2 in table[b + 1].values():
                worst = max(worst, abs(o2["melody"][0][0] - o1["melody"][-1][0]))
    return worst


# --------------------------------------------------------------------------------------------- generate and test
ILLIAC_RULES = {
    "range": "within an octave of C",
    "tritone": "no melodic tritone",
    "seventh": "no melodic seventh or larger leap",
    "repeat": "no note three times running",
    "recover": "after a leap of more than a fourth, a step back",
    "end": "end on C, approached by step",
}


def _illiac_ok(line, x, n):
    """Which rule a candidate next note x breaks (or None), given the line so far and its planned length n."""
    if not 60 <= x <= 72:
        return "range"
    if line:
        s = x - line[-1]
        if abs(s) == 6:
            return "tritone"
        if abs(s) >= 10:
            return "seventh"
        if len(line) >= 2 and line[-1] == line[-2] == x:
            return "repeat"
        if len(line) >= 2:
            prev = line[-1] - line[-2]
            if abs(prev) > 5 and not (1 <= abs(s) <= 2 and s * prev < 0):
                return "recover"
    if len(line) == n - 1 and (x != 60 and x != 72 or (line and abs(x - line[-1]) > 2)):
        return "end"
    return None


def illiac(n: int = 12, rng=None, tries: int = 50) -> dict:
    """A cantus firmus of n white notes, as Hiller and Isaacson's programs made one: the first note C; each next note
    drawn at random from the white keys C4 to C5 and tested; a failed note is drawn again; after ``tries`` failures
    the line backs up a note.  Returns the line, every rejection by rule, and the number of draws."""
    rng = rng or np.random.default_rng(0)
    white = [m for m in range(60, 73) if m % 12 in MAJOR]
    line = [60]
    rejected = Counter()
    draws, backs = 0, 0
    fails = [0]
    while len(line) < n:
        x = int(rng.choice(white))
        draws += 1
        why = _illiac_ok(line, x, n)
        if why is None:
            line.append(x)
            fails.append(0)
            continue
        rejected[why] += 1
        fails[-1] += 1
        if fails[-1] >= tries and len(line) > 1:
            line.pop()
            fails.pop()
            fails[-1] += 1
            backs += 1
    return {"line": line, "rejected": dict(rejected), "draws": draws, "backtracks": backs}


# --------------------------------------------------------------------------------------------- chains
def markov(seqs, order: int = 1) -> dict:
    """Transition counts from each run of ``order`` notes (as intervals from the tonic, octave kept) to the next."""
    T = defaultdict(Counter)
    for s in seqs:
        s = list(s)
        for i in range(order, len(s)):
            T[tuple(s[i - order:i])][s[i]] += 1
    return {"order": order, "T": T, "starts": [tuple(s[:order]) for s in seqs if len(s) > order]}


def generate(model, n: int, rng=None, end_on=0) -> list[int]:
    """Walk the chain for n notes; when a context was never seen, back off to a random start.  The walk prefers to end
    on ``end_on`` when the last step allows it."""
    rng = rng or np.random.default_rng(0)
    k = model["order"]
    st = model["starts"][int(rng.integers(len(model["starts"])))]
    out = list(st)
    while len(out) < n:
        ctx = tuple(out[-k:])
        nxt = model["T"].get(ctx)
        if not nxt:
            st = model["starts"][int(rng.integers(len(model["starts"])))]
            out += list(st)[: n - len(out)]
            continue
        keys = list(nxt)
        p = np.array([nxt[x] for x in keys], float)
        if len(out) == n - 1 and end_on in nxt:
            out.append(end_on)
            break
        out.append(int(keys[int(rng.choice(len(keys), p=p / p.sum()))]))
    return out[:n]


def longest_copy(seq, seqs) -> dict:
    """The longest run of consecutive notes of ``seq`` found verbatim in one tune of ``seqs``, and which."""
    best, who = 0, None
    seq = list(seq)
    for name, s in seqs.items():
        s = list(s)
        # longest common substring by dynamic programming
        prev = [0] * (len(s) + 1)
        for i in range(1, len(seq) + 1):
            cur = [0] * (len(s) + 1)
            for j in range(1, len(s) + 1):
                if seq[i - 1] == s[j - 1]:
                    cur[j] = prev[j - 1] + 1
                    if cur[j] > best:
                        best, who = cur[j], name
            prev = cur
    return {"run": best, "tune": who}


# --------------------------------------------------------------------------------------------- critics
def chord_at(chords, t: float, bar: float = 4.0, per_bar: int = 1) -> str:
    i = int(t // (bar / per_bar))
    return chords[min(i, len(chords) - 1)]


def strong(a: float, bar: float = 4.0) -> bool:
    return abs((a % bar) % 2.0) < 1e-9


def harmony_fit(mel, chords, bar: float = 4.0, per_bar: int = 1) -> float:
    """Share of notes on strong beats (1 and 3 of 4/4) that belong to the chord sounding there."""
    hits = [m % 12 in CHORDS[chord_at(chords, a, bar, per_bar)] for m, a, _ in mel if strong(a, bar)]
    return float(np.mean(hits)) if hits else 0.0


def leaps_recovered(mel) -> float:
    """Of the leaps larger than a third, the share followed by a step in the opposite direction (Part 14's gap fill)."""
    p = pitches(mel)
    n, ok = 0, 0
    for i in range(len(p) - 2):
        s = p[i + 1] - p[i]
        if abs(s) > 4:
            n += 1
            t = p[i + 2] - p[i + 1]
            ok += 1 <= abs(t) <= 2 and s * t < 0
    return ok / n if n else 1.0


def span(mel) -> int:
    p = pitches(mel)
    return max(p) - min(p)


def parallels(mel, bass, bar: float = 4.0) -> int:
    """Parallel fifths and octaves between the melody and the bass, from one bar's downbeat to the next."""
    def at(line, t):
        cand = [m for m, a, d in line if a <= t + 1e-9 < a + d]
        return cand[-1] if cand else None
    n = 0
    end = max(a + d for _, a, d in mel)
    ts = np.arange(0.0, end - 1e-9, bar)
    for t0, t1 in zip(ts, ts[1:]):
        a0, a1, b0, b1 = at(mel, t0), at(mel, t1), at(bass, t0), at(bass, t1)
        if None in (a0, a1, b0, b1) or a0 == a1 or b0 == b1:
            continue
        i0, i1 = (a0 - b0) % 12, (a1 - b1) % 12
        if i0 == i1 and i0 in (0, 7) and (a1 - a0) * (b1 - b0) > 0:
            n += 1
    return n


def cadence(mel) -> bool:
    """The last note is C, on a downbeat, reached by step."""
    p = pitches(mel)
    return p[-1] % 12 == 0 and abs(mel[-1][1] % 4.0) < 1e-9 and 1 <= abs(p[-1] - p[-2]) <= 2


def _shape(fig, last_len: bool = True):
    d0, a0 = deg(fig[0][0]), fig[0][1]
    return tuple((deg(m) - d0, round(a - a0, 4)) + ((round(d, 4),) if (last_len or j < len(fig) - 1) else ())
                 for j, (m, a, d) in enumerate(fig))


@lru_cache(maxsize=None)
def _family(motive_norm) -> dict:
    """Every figure reachable from the motive (or its first two or three notes) by up to two operations, by shape
    without the last note's length (a bar may hold its last note longer)."""
    base = [(key_of(35 + st), on, d) for st, on, d in motive_norm]
    out = {}
    starts = [((), base), (("fragment",), fragment(base, 2)), (("first three notes",), fragment(base, 3))]
    frontier = list(starts)
    for chain, m in frontier:
        out.setdefault(_shape(m, False), chain)
    for _ in range(2):
        nxt = []
        for chain, m in frontier:
            for name, f in OPS.items():
                if name.startswith("transpose"):
                    continue
                y = f(m)
                out.setdefault(_shape(y, False), chain + (name,))
                nxt.append((chain + (name,), y))
        frontier = nxt
    return out


def bar_figures(mel, bar: float = 4.0) -> list:
    nb = int(round(length(mel) / bar))
    return [[n for n in mel if b * bar - 1e-9 <= n[1] < (b + 1) * bar - 1e-9] for b in range(nb)]


def derivation(fig, motive):
    """How a bar's figure derives from the motive (a tuple of operation names), or None."""
    return _family(_norm(motive)).get(_shape(fig, False)) if fig else None


def unity(mel, motive, bar: float = 4.0) -> float:
    """Share of bars (the last, the cadence, excepted) whose figure derives from the motive by at most two operations."""
    figs = bar_figures(mel, bar)[:-1]
    return float(np.mean([derivation(f, motive) is not None for f in figs])) if figs else 0.0


def flow(mel, bar: float = 4.0) -> float:
    """Share of bars before the last that keep moving: no note held three beats or more."""
    figs = bar_figures(mel, bar)[:-1]
    return float(np.mean([all(d < 3.0 for _, _, d in f) for f in figs])) if figs else 0.0


def variety(mel, bar: float = 4.0) -> float:
    """Share of bars whose figure (up to transposition) is not repeated elsewhere in the phrase."""
    nb = int(round(length(mel) / bar))
    figs = []
    for b in range(nb):
        fig = [n for n in mel if b * bar - 1e-9 <= n[1] < (b + 1) * bar - 1e-9]
        figs.append(_norm(fig) if fig else ())
    c = Counter(figs)
    return float(np.mean([c[f] == 1 for f in figs]))


def tension(mel, chords, bar: float = 4.0) -> list[float]:
    """Tension in each bar: the mean height above C4 in octaves, plus the share of non-chord tones, plus the chord's
    harmonic distance from the tonic (0 for I, 1 for IV and vi, 1.5 for ii and V, 2 for V7), plus notes a beat over
    two.  A crude model, after the factors Lerdahl and Krumhansl's (2007) tension model weighs."""
    nb = int(round(length(mel) / bar))
    out = []
    for b in range(nb):
        fig = [n for n in mel if b * bar - 1e-9 <= n[1] < (b + 1) * bar - 1e-9]
        sym = chords[min(b, len(chords) - 1)]
        if not fig:
            out.append(DISTANCE[sym])
            continue
        h = np.mean([(m - 60) / 12 for m, _, _ in fig])
        nct = np.mean([m % 12 not in CHORDS[sym] for m, _, _ in fig])
        dens = len(fig) / bar / 2
        out.append(float(h + nct + DISTANCE[sym] + dens))
    return out


def plan_fit(curve, plan) -> float:
    """Correlation between a tension curve and a planned one."""
    a, b = np.asarray(curve, float), np.asarray(plan, float)
    if a.std() < 1e-9 or b.std() < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


HARD = ("leaps", "cadence", "range", "parallels", "harmony")    # leaps: no tritone, seventh or more than an octave;
#                                                                 range: no more than a tenth


def judge(mel, bass, chords, motive, plan=None, tension_weight: float = 1.0) -> dict:
    """Every critic's verdict.  Hard critics reject a draft outright; soft ones score what survives."""
    v = {"harmony": harmony_fit(mel, chords), "recovered": leaps_recovered(mel), "span": span(mel),
         "parallels": parallels(mel, bass), "cadence": cadence(mel), "unity": unity(mel, motive), "variety": variety(mel),
         "flow": flow(mel)}
    v["tension_fit"] = plan_fit(tension(mel, chords), plan) if plan is not None else 0.0
    p = pitches(mel)
    v["bad_leaps"] = sum(abs(b - a) in (6, 10, 11) or abs(b - a) > 12 for a, b in zip(p, p[1:]))
    fails = []
    if v["bad_leaps"]:
        fails.append("leaps")
    if not v["cadence"]:
        fails.append("cadence")
    if v["span"] > 16:
        fails.append("range")
    if v["parallels"] > 0:
        fails.append("parallels")
    if v["harmony"] < 0.75:
        fails.append("harmony")
    v["fails"] = fails
    w = tension_weight
    v["score"] = (v["recovered"] + v["unity"] + 0.5 * v["variety"] + w * (v["tension_fit"] + 1) / 2 + v["harmony"] + v["flow"]) / (4.5 + w)
    return v


# --------------------------------------------------------------------------------------------- the searcher
OP_NAMES = [k for k in OPS if not k.startswith("transpose")]


def random_plan(rng, bars: int, motive, chords):
    """A random developing variation: each bar a chain of 0 to 2 operations, transposed so its first note is a tone of
    the bar's chord near the previous bar's last note; the last bar a cadential figure."""
    plan = []
    prev = motive[0][0]
    for b in range(bars):
        # the basic idea is stated plainly first, as in Schoenberg's sentence; then anything goes
        size = 0 if b == 0 else int(rng.integers(0, 3))
        ops = [OP_NAMES[int(i)] for i in rng.choice(len(OP_NAMES), size=size, replace=False)]
        m = [tuple(n) for n in motive]
        for name in ops:
            m = OPS[name](m)
        sym = chords[min(b, len(chords) - 1)]
        cands = [k for k in range(-7, 8) if dstep(m[0][0], k) % 12 in CHORDS[sym]]
        dist = [abs(dstep(m[0][0], k) - prev) + 1.5 * max(0, max(dstep(x, k) for x, _, _ in m) - 77)
                + 1.5 * max(0, 62 - min(dstep(x, k) for x, _, _ in m)) for k in cands]
        w = np.exp(-np.array(dist, float) / 3.0)
        k = int(cands[int(rng.choice(len(cands), p=w / w.sum()))])
        plan.append((ops, k))
        prev = dstep(m[-1][0], k)
    return plan


def with_cadence(mel, bars: int, bar: float = 4.0):
    """End on C on the last downbeat, held a bar, reached by step: if the last note is not a step from the nearest C,
    its second half becomes the note a step away (D above, or B below)."""
    end = (bars - 1) * bar
    body = [(m, a, min(d, end - a)) for m, a, d in mel if a < end - 1e-9]
    last = body[-1]
    c = min((60, 72), key=lambda x: abs(x - last[0]))
    if not 1 <= abs(last[0] - c) <= 2:
        approach = c + 2 if last[0] > c else c - 1
        half = last[2] / 2 if last[2] < 2 else last[2] - 1.0
        body[-1] = (last[0], last[1], half)
        body.append((approach, last[1] + half, last[2] - half))
    return body + [(c, end, bar)]


def compose(motive, chords, bass, rng=None, drafts: int = 2000, plan=None, keep_rejected: int = 6,
            tension_weight: float = 1.0) -> dict:
    """Generate and test.  Each draft is a random developing variation of the motive with a cadence; the hard critics
    reject it or the soft ones score it; the best is kept.  The rejected drafts are counted by the first critic that
    refused them, and a few are kept to be shown."""
    rng = rng or np.random.default_rng(0)
    bars = len(chords)
    best, rejected, survivors = None, Counter(), 0
    shown = []
    trace = []
    for i in range(drafts):
        p = random_plan(rng, bars - 1, motive, chords)
        mel = develop(motive, p)
        mel = with_cadence(mel, bars)
        v = judge(mel, bass, chords, motive, plan, tension_weight)
        if v["fails"]:
            rejected[v["fails"][0]] += 1
            if len(shown) < keep_rejected and v["fails"][0] not in [s["why"] for s in shown]:
                shown.append({"draft": i, "why": v["fails"][0], "melody": mel, "verdict": {k: v[k] for k in ("harmony", "span", "parallels", "cadence")}})
            trace.append(None)
            continue
        survivors += 1
        if best is None or v["score"] > best["verdict"]["score"]:
            best = {"draft": i, "melody": mel, "plan": p, "verdict": v}
        trace.append(best["verdict"]["score"])
    return {"best": best, "rejected": dict(rejected), "survivors": survivors, "drafts": drafts, "shown": shown, "trace": trace}


def evolve(motive, chords, bass, rng=None, pop: int = 40, gens: int = 40, plan=None) -> dict:
    """A genetic algorithm over developing-variation plans: fitness is the critics' score (zero if a hard critic
    refuses); children take bars from two parents and one bar is re-drawn with a small probability."""
    rng = rng or np.random.default_rng(0)
    bars = len(chords)

    def build(p):
        return with_cadence(develop(motive, p), bars)

    def fit(p):
        v = judge(build(p), bass, chords, motive, plan)
        return 0.0 if v["fails"] else v["score"]

    P = [random_plan(rng, bars - 1, motive, chords) for _ in range(pop)]
    F = [fit(p) for p in P]
    best_curve, mean_curve = [max(F)], [float(np.mean(F))]
    for _ in range(gens):
        new = [P[int(np.argmax(F))]]
        while len(new) < pop:
            i, j = rng.choice(pop, 2, replace=False), rng.choice(pop, 2, replace=False)
            a = P[i[0]] if F[i[0]] >= F[i[1]] else P[i[1]]
            b = P[j[0]] if F[j[0]] >= F[j[1]] else P[j[1]]
            cut = int(rng.integers(1, bars - 1))
            child = list(a[:cut]) + list(b[cut:])
            if rng.random() < 0.5:
                k = int(rng.integers(bars - 1))
                child[k] = random_plan(rng, bars - 1, motive, chords)[k]
            new.append(child)
        P = new
        F = [fit(p) for p in P]
        best_curve.append(max(F))
        mean_curve.append(float(np.mean(F)))
    k = int(np.argmax(F))
    return {"best": build(P[k]), "plan": P[k], "fitness": F[k], "best_curve": best_curve, "mean_curve": mean_curve}


def bass_line(chords, bar: float = 4.0) -> list:
    """A plain bass: the chord's root on beats 1 and 3."""
    out = []
    for b, sym in enumerate(chords):
        r = ROOT[sym]
        out += [(r, b * bar, 2.0), (r, b * bar + 2.0, 2.0)]
    return out
