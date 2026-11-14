"""Music before tonality, as programs: what Part 23 computes.

    Chant       the eight modes (final, reciting tone, range); a classifier by final and range; psalm tones.
    Guido       the gamut, the three hexachords, and solmization by the fewest mutations (a shortest path).
    Organum     parallel organum and the tritone it makes; the *Musica enchiriadis* boundary rule; florid organum.
    Rhythm      the six rhythmic modes, read from patterns of ligatures; Notre Dame organum on a held tenor.
    Mensuration tempus and prolation; reading perfect time (imperfection and alteration) from note shapes.
    Isorhythm   talea against color, their periods and realignment; finding a talea in a real tenor.
    Census      intervals on the beat, parallels, cadences and final sonorities in fourteenth-century polyphony.

    m = classify([62, 65, 64, 62, 67, 69, 67, 65, 64, 62])       # -> 1 (Dorian)
    syl, mut = solmize(UT_QUEANT)                                 # ut re fa re mi re ...
    notes = isorhythm(color, talea)                               # (pitch, onset, duration)
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np

LETTERS = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 10: "B♭", 11: "B"}

# ---------------------------------------------------------------------------
# Chant: the eight modes
# ---------------------------------------------------------------------------
# (number, Greek name, final, reciting tone (tenor) as key numbers in the chant register, the range's low and high)
MODES = {
    1: ("Dorian", 62, 69), 2: ("Hypodorian", 62, 65),
    3: ("Phrygian", 64, 72), 4: ("Hypophrygian", 64, 69),
    5: ("Lydian", 65, 72), 6: ("Hypolydian", 65, 69),
    7: ("Mixolydian", 67, 74), 8: ("Hypomixolydian", 67, 72),
}
MANERIA = {2: "protus", 4: "deuterus", 5: "tritus", 7: "tetrardus"}       # pitch class of the final -> maneria
FINAL_PC = {"protus": 2, "deuterus": 4, "tritus": 5, "tetrardus": 7}


def mode_range(m: int) -> tuple[int, int]:
    """The ideal range: authentic, the final to the octave above; plagal, a fourth below the final to a fifth above."""
    f = MODES[m][1]
    return (f, f + 12) if m % 2 else (f - 5, f + 7)


def classify(pitches) -> int:
    """The mode of a chant by the theorists' rules: the last note gives the maneria (D, E, F or G); the range decides
    authentic or plagal (plagal if the melody goes a third or more below its final, authentic if it climbs a sixth or
    more above it); where the range does not decide, the more used of the two reciting tones does."""
    final = pitches[-1]
    man = MANERIA.get(final % 12)
    if man is None:
        raise ValueError("final not on D, E, F or G")
    base = {"protus": 1, "deuterus": 3, "tritus": 5, "tetrardus": 7}[man]
    lo, hi = min(pitches) - final, max(pitches) - final
    if lo <= -3 and hi < 9:
        return base + 1
    if hi >= 9 and lo > -3:
        return base
    ta = sum(p % 12 == MODES[base][2] % 12 for p in pitches)
    tp = sum(p % 12 == MODES[base + 1][2] % 12 for p in pitches)
    return base if ta >= tp else base + 1


def tenor_share(pitches, m: int) -> float:
    """How much of a chant sits on its mode's reciting tone (in the octave of the mode's range)."""
    t = MODES[m][2] % 12
    return float(np.mean([p % 12 == t for p in pitches]))


def profile(pitches) -> np.ndarray:
    """Pitch-class distribution relative to the final (12 bins)."""
    f = pitches[-1]
    h = np.zeros(12)
    for p in pitches:
        h[(p - f) % 12] += 1
    return h / h.sum()


# Ut queant laxis, the hymn for St John the Baptist whose lines begin on C D E F G A (after the Liber Usualis; pitches
# only), with its syllables
UT_QUEANT = [(60, "Ut"), (62, "que"), (65, "ant"), (62, "la"), (64, ""), (62, "xis"),
             (62, "re"), (62, "so"), (60, "na"), (62, "re"), (64, "fi"), (64, "bris"),
             (64, "Mi"), (65, "ra"), (67, "ge"), (64, ""), (62, "sto"), (64, ""), (60, "rum"), (62, ""),
             (65, "fa"), (67, "mu"), (69, "li"), (67, "tu"), (65, ""), (64, "o"), (62, "rum"), (62, ""),
             (67, "Sol"), (69, "ve"), (67, "pol"), (65, ""), (64, "lu"), (65, ""), (67, "ti"), (62, ""),
             (69, "La"), (67, "bi"), (69, "i"), (65, "re"), (67, ""), (69, "a"), (69, "tum"),
             (67, "Sanc"), (65, "te"), (62, "Io"), (60, "an"), (64, "ne"), (62, "s")]
UT_LINES = [0, 6, 12, 20, 28, 36, 43]                             # where each line starts (a note index)
DIES_IRAE = [65, 64, 65, 62, 64, 60, 62, 62]                     # Di-es i-rae, di-es il-la: its first line


def psalm_tone(m: int, syllables: int = 14, accent_mediant: int = 7) -> list[int]:
    """A psalm verse, simplified: an intonation rising to the reciting tone, recitation, a mediant cadence that dips
    and returns, recitation, and a termination falling to the final."""
    name, final, tenor = MODES[m]
    up = [final, final + (2 if (tenor - final) > 4 else 0), tenor]
    med = [tenor, tenor - 2 if (tenor - 2) % 12 in (0, 2, 4, 5, 7, 9, 11) else tenor - 1, tenor]
    term = []
    p = tenor
    while p > final:
        q = p - 1
        while q % 12 not in (0, 2, 4, 5, 7, 9, 11):
            q -= 1
        q = p - 2 if (p - 2) % 12 in (0, 2, 4, 5, 7, 9, 11) and (p - 1) % 12 not in (4, 11) else q
        term.append(q)
        p = q
    rec = max(syllables - len(up) - len(med) - len(term), 2)
    first = up + [tenor] * (rec // 2) + med
    return first + [tenor] * (rec - rec // 2) + term


# ---------------------------------------------------------------------------
# Guido: the gamut and the hexachords
# ---------------------------------------------------------------------------
SYLLABLES = ("ut", "re", "mi", "fa", "sol", "la")
STEPS6 = (0, 2, 4, 5, 7, 9)                                       # tone tone semitone tone tone
GAMUT_LOW, GAMUT_HIGH = 43, 76                                    # Gamma-ut (G2) to e-la (E5)


def hexachords() -> list[tuple[str, int]]:
    """The seven hexachords of the gamut: (kind, starting key number); hard on G, natural on C, soft on F."""
    out = []
    for start in (43, 48, 53, 55, 60, 65, 67):
        kind = {7: "hard", 0: "natural", 5: "soft"}[start % 12]
        out.append((kind, start))
    return out


def gamut() -> list[int]:
    """Every note of Guido's gamut: the white notes from G2 to E5 plus the two b-flats (B-flat 3 and 4)."""
    notes = sorted({start + s for _, start in hexachords() for s in STEPS6})
    return [n for n in notes if GAMUT_LOW <= n <= GAMUT_HIGH]


def syllable_options(p: int) -> list[tuple[int, str]]:
    """Every (hexachord index, syllable) that names key number p."""
    out = []
    for i, (_, start) in enumerate(hexachords()):
        d = p - start
        if d in STEPS6:
            out.append((i, SYLLABLES[STEPS6.index(d)]))
    return out


def solmize(pitches) -> tuple[list[str], list[int]]:
    """Name every note by a syllable with the fewest changes of hexachord (mutations), a shortest path through the
    hexachords; ties prefer staying in the hexachord you began in.  Returns the syllables and the indices of the
    notes where a mutation happens."""
    opts = [syllable_options(p) for p in pitches]
    if any(not o for o in opts):
        raise ValueError("a note outside the gamut")
    INF = 10 ** 9
    cost = [{h: (0, None) for h, _ in opts[0]}]
    for k in range(1, len(pitches)):
        cur = {}
        for h, _ in opts[k]:
            best = (INF, None)
            for g, (c, _) in cost[-1].items():
                c2 = c + (0 if g == h else 1)
                if c2 < best[0] or (c2 == best[0] and g == h):
                    best = (c2, g)
            cur[h] = best
        cost.append(cur)
    h = min(cost[-1], key=lambda x: cost[-1][x][0])
    path = [h]
    for k in range(len(pitches) - 1, 0, -1):
        h = cost[k][h][1]
        path.append(h)
    path.reverse()
    syl = [dict(opts[k])[path[k]] for k in range(len(pitches))]
    mut = [k for k in range(1, len(path)) if path[k] != path[k - 1]]
    return syl, mut


# ---------------------------------------------------------------------------
# Organum
# ---------------------------------------------------------------------------
WHITE = (0, 2, 4, 5, 7, 9, 11)


def diatonic_shift(p: int, steps: int) -> int:
    """Move a white note by ``steps`` scale steps (negative: down)."""
    q, k = p, 0
    d = 1 if steps > 0 else -1
    while k < abs(steps):
        q += d
        if q % 12 in WHITE:
            k += 1
    return q


def parallel(chant, steps: int = -3) -> list[int]:
    """Strict parallel organum: the organal voice a diatonic fourth (``steps=-3``) or fifth (-4) below each note."""
    return [diatonic_shift(p, steps) for p in chant]


def tritones(upper, lower) -> int:
    return sum(1 for a, b in zip(upper, lower) if (a - b) % 12 == 6)


def enchiriadis(chant, floor: int = 60, steps: int = -3) -> list[int]:
    """Organum at the fourth by the rule of the *Musica enchiriadis* (about 900), simplified: the organal voice may not
    go below a boundary note (``floor``), so it holds there while the chant moves above, and it meets the chant in a
    unison at the end of the phrase (the *occursus*); a fourth that would be a tritone is avoided by holding."""
    out = []
    for p in chant:
        q = diatonic_shift(p, steps)
        if q < floor:
            q = min(p, floor)
        if (p - q) % 12 == 6:                                     # a tritone: keep the previous note instead
            q = out[-1] if out else floor
        out.append(q)
    out[-1] = chant[-1]
    return out


def florid(tenor, rng, notes_per=(4, 8), consonant=(7, 12, 19)) -> list[list[int]]:
    """Florid (melismatic) organum, as at St Martial and Santiago: over each held tenor note a melisma that starts and
    ends on a perfect consonance and moves mostly by step in between."""
    out = []
    prev = None
    for t in tenor:
        n = int(rng.integers(notes_per[0], notes_per[1] + 1))
        starts = [t + c for c in consonant if t + c <= 81]
        s = min(starts, key=lambda x: abs(x - prev)) if prev is not None else starts[0]
        end = starts[int(rng.integers(len(starts)))]
        line = [s]
        p = s
        for k in range(1, n - 1):
            left = n - 1 - k
            want = np.sign(end - p) if abs(end - p) >= 2 * left else rng.choice([-1, 1])
            step = int(want) * (1 if rng.random() < 0.8 else 2)
            p = diatonic_shift(p, step) if p % 12 in WHITE else p + step
            line.append(p)
        line.append(end)
        out.append(line)
        prev = end
    return out


# ---------------------------------------------------------------------------
# The rhythmic modes and Notre Dame organum
# ---------------------------------------------------------------------------
# one ordo of each mode in breves (a perfect long is 3 breves): L B | B L | L. B B | B B L. | L. L. | B B B
RHYTHMIC_MODES = {1: (2, 1), 2: (1, 2), 3: (3, 1, 2), 4: (1, 2, 3), 5: (3, 3), 6: (1, 1, 1)}
MODE_NAMES = {1: "trochaic", 2: "iambic", 3: "dactylic", 4: "anapaestic", 5: "spondaic", 6: "tribrachic"}
# the pattern of ligatures (notes bound in one sign) that signals each mode: the first group, then the rest
LIGATURES = {1: (3, 2), 2: (2, 3), 3: (1, 3), 4: (3, 1), 5: (3, 3), 6: (4, 3)}


def mode_of(groups) -> int | None:
    """The rhythmic mode signalled by a sequence of ligature sizes, by the standard patterns: mode 1 is a three-note
    ligature then two-note ones (3 2 2 2), mode 2 two-note ones ending in a three (2 2 2 3), mode 3 a single note then
    threes (1 3 3 3), mode 5 threes throughout, mode 6 a four then threes.  None if no pattern fits."""
    g = list(groups)
    if not g:
        return None
    if g[0] == 3 and all(x == 2 for x in g[1:]) and len(g) > 1:
        return 1
    if g[-1] == 3 and all(x == 2 for x in g[:-1]) and len(g) > 1:
        return 2
    if g[0] == 1 and all(x == 3 for x in g[1:]) and len(g) > 1:
        return 3
    if g[-1] == 1 and all(x == 3 for x in g[:-1]) and len(g) > 1:
        return 4
    if g[0] == 4 and all(x == 3 for x in g[1:]):
        return 6
    if all(x == 3 for x in g):
        return 5
    return None


def realize(mode: int, pitches, unit: float = 1.0) -> list[tuple]:
    """Notes (pitch, onset, duration) in a rhythmic mode, durations in breves times ``unit``."""
    pat = RHYTHMIC_MODES[mode]
    out, t = [], 0.0
    for k, p in enumerate(pitches):
        d = pat[k % len(pat)] * unit
        out.append((p, t, d))
        t += d
    return out


def ligatures_for(mode: int, n: int) -> list[int]:
    """How a scribe would bind ``n`` notes in a mode (the standard pattern, cut to length)."""
    a, b = LIGATURES[mode]
    if mode in (2, 4):
        body = [a] * max((n - b) // a, 0)
        return body + [n - sum(body)]
    out = [a]
    while sum(out) < n:
        out.append(min(b, n - sum(out)))
    return out


CONSONANT_ND = (0, 7, 12, 19, 24)                                 # unison, fifth, octave, twelfth, double octave


def notre_dame(tenor: int, perfections: int, rng, voices: int = 3, exchange: int = 4) -> list[list[tuple]]:
    """An organum on one held tenor note in the manner of the Notre Dame quadrupla (ours, not Pérotin's): upper voices
    in the first rhythmic mode (long, short), each perfection beginning on a perfect consonance with the tenor and
    with every other voice an octave, fifth or unison apart, the short note a step away; in every block of
    ``exchange`` perfections the two upper voices swap their lines (*Stimmtausch*).  Durations in breves; returns
    voices top to bottom, tenor last."""
    homes = [tenor + c for c in (12, 19, 24) if tenor + c <= 82]
    lines = [[] for _ in range(voices)]
    prev = [homes[min(k, len(homes) - 1)] for k in range(voices)][::-1]
    prev = sorted(prev, reverse=True)
    block = []
    for k in range(perfections):
        if exchange and voices >= 2 and k % (2 * exchange) >= exchange and block:
            src = block[k % exchange]
            chord = [src[1], src[0]] + src[2:]
        else:
            cand = []
            for _ in range(60):
                ch = [prev[j] + int(rng.choice([-5, -3, 0, 0, 2, 4, 5])) for j in range(voices)]
                ch = [min(max(x, tenor + 7), 82) for x in ch]
                ch = [x if (x - tenor) % 12 in (0, 7) else min((y for y in range(x - 5, x + 6) if (y - tenor) % 12 in (0, 7) and y > tenor), key=lambda y: abs(y - x))
                      for x in ch]
                spread = sum(abs(a - b) for a, b in zip(ch, prev)) + 6 * (len(set(ch)) < voices)
                cand.append((spread + rng.random(), ch))
            chord = min(cand)[1]
            if k % (2 * exchange) < exchange:
                block = block[: k % (2 * exchange)] + [chord]
        for j in range(voices):
            p = chord[j]
            nb = diatonic_shift(p, int(rng.choice([-1, 1]))) if p % 12 in WHITE else p + 1
            lines[j].append((p, 3.0 * k, 2.0))
            lines[j].append((nb, 3.0 * k + 2.0, 1.0))
        prev = chord
    lines.append([(tenor, 0.0, 3.0 * perfections)])
    return lines


# ---------------------------------------------------------------------------
# Mensuration
# ---------------------------------------------------------------------------
# (tempus perfect?, prolation major?) -> (sign, minims in a breve, a modern equivalent)
MENSURATIONS = {(True, True): ("O with a dot", 9, "9/8"), (True, False): ("O", 6, "3/4"),
                (False, True): ("C with a dot", 6, "6/8"), (False, False): ("C", 4, "2/4")}


def breve(tempus_perfect: bool, prolation_major: bool) -> tuple[int, int]:
    """(semibreves in a breve, minims in a semibreve)."""
    return (3 if tempus_perfect else 2), (3 if prolation_major else 2)


def read_perfect(shapes: str) -> list[int]:
    """Read a string of breves and semibreves ('B', 'S') in perfect time, in semibreves, by the rules of Franco of
    Cologne and the Ars nova: a breve is perfect (3) unless a single semibreve stands next to it, which takes a third
    away (imperfection, *a parte post*: the breve before it); of two semibreves between perfections the second is
    doubled (alteration); in a group of more, they fill perfections of three, and any one or two left over are read
    as above."""
    out = []
    i = 0
    tokens = list(shapes)
    vals = [3 if c == "B" else 1 for c in tokens]
    k = 0
    while k < len(tokens):
        if tokens[k] == "S":
            j = k
            while j < len(tokens) and tokens[j] == "S":
                j += 1
            n = j - k
            rem = n % 3
            if rem == 1:
                # a single semibreve imperfects the breve before it (or, at the start, the one after it)
                if k > 0 and tokens[k - 1] == "B":
                    vals[k - 1] = 2
                elif j < len(tokens) and tokens[j] == "B":
                    vals[j] = 2
            elif rem == 2:
                vals[j - 1] = 2                                    # alteration: the second of the last two is doubled
            k = j
        else:
            k += 1
    out = vals
    del i
    return out


# ---------------------------------------------------------------------------
# Isorhythm
# ---------------------------------------------------------------------------
def isorhythm(color, talea, diminution: float = 1.0, repeats: int | None = None) -> list[tuple]:
    """Lay a color (pitches) through a talea (durations; a negative duration is a rest) until both run out together,
    or for ``repeats`` statements of the color.  Returns notes (pitch, onset, duration) and keeps rests as gaps."""
    n_col = len(color)
    n_tal = sum(1 for d in talea if d > 0)
    total = repeats * n_col if repeats else n_col * n_tal // math.gcd(n_col, n_tal)
    out, t, k, i = [], 0.0, 0, 0
    while k < total:
        d = talea[i % len(talea)] * diminution
        if d > 0:
            out.append((color[k % n_col], t, d))
            k += 1
        t += abs(d)
        i += 1
    return out


def periods(n_color: int, n_talea: int) -> dict:
    """How talea and color line up: they begin together again after lcm notes."""
    L = n_color * n_talea // math.gcd(n_color, n_talea)
    return {"lcm": L, "colors": L // n_color, "taleae": L // n_talea}


def bar_prints(voice, bar: int) -> list[tuple]:
    """A voice as a list of bars, each the tuple of (offset in the bar, duration) of the notes that start in it: its
    rhythm with the pitches left out."""
    if not voice:
        return []
    nb = max(o for _, o, _ in voice) // bar + 1
    f = [[] for _ in range(nb)]
    for _, o, d in voice:
        f[o // bar].append((o % bar, d))
    return [tuple(x) for x in f]


def talea_scan(voice, bar: int, lo: int = 6) -> dict:
    """Find a talea: for every lag of at least ``lo`` bars, the share of bars whose rhythm is repeated exactly that
    many bars later.  Returns the best lag, its share, and the scan."""
    f = bar_prints(voice, bar)
    n = len(f)
    scan = {}
    for P in range(lo, n // 2 + 1):
        scan[P] = float(np.mean([f[i] == f[i + P] for i in range(n - P)]))
    if not scan:
        return {"lag": None, "share": 0.0, "scan": {}}
    P = max(scan, key=lambda x: (scan[x], -x))
    return {"lag": P, "share": scan[P], "scan": scan}


def shuffled_share(voice, bar: int, rng, trials: int = 20, lo: int = 6) -> float:
    """The best share a voice's bars reach at any lag when their order is shuffled: the chance level."""
    f = bar_prints(voice, bar)
    best = 0.0
    for _ in range(trials):
        g = [f[i] for i in rng.permutation(len(f))]
        n = len(g)
        for P in range(lo, n // 2 + 1):
            best = max(best, float(np.mean([g[i] == g[i + P] for i in range(n - P)])))
    return best


def color_scan(voice, lo: int = 6) -> dict:
    """Find a color: the lag (in notes) at which the voice's pitch sequence best repeats itself."""
    q = [p for p, _, _ in voice]
    n = len(q)
    scan = {P: float(np.mean([q[i] == q[i + P] for i in range(n - P)])) for P in range(lo, n // 2 + 1)}
    if not scan:
        return {"lag": None, "share": 0.0}
    P = max(scan, key=lambda x: (scan[x], -x))
    return {"lag": P, "share": scan[P]}


# ---------------------------------------------------------------------------
# Census of fourteenth-century polyphony (pieces from ``trecento``)
# ---------------------------------------------------------------------------
def interval_class(a: int, b: int) -> int:
    return abs(a - b) % 12


PERFECT = {0, 7}
IMPERFECT = {3, 4, 8, 9}


def on_off_beat(piece, per_bar: int | None = None) -> dict:
    """Intervals between the lowest sounding voice and each other voice: at the start of every bar, and at every other
    onset.  Shares of perfect consonances (unison, fifth, octave), imperfect ones (thirds, sixths) and dissonances."""
    on, off = Counter(), Counter()
    grid = piece.grid(4)                                            # sixteenth notes of the edition
    step = 6
    bar = piece.bar // step
    starts = {o // step for v in piece.voices for _, o, _ in v}
    for t in sorted(starts):
        if t >= len(grid):
            continue
        row = [x for x in grid[t] if x >= 0]
        if len(row) < 2:
            continue
        low = min(row)
        for x in row:
            if x == low:
                continue
            ic = interval_class(x, low)
            kind = "perfect" if ic in PERFECT else ("imperfect" if ic in IMPERFECT else "dissonant")
            (on if bar and t % bar == 0 else off)[kind] += 1
    norm = lambda c: {k: c[k] / max(sum(c.values()), 1) for k in ("perfect", "imperfect", "dissonant")}  # noqa: E731
    return {"on": norm(on), "off": norm(off), "n_on": sum(on.values()), "n_off": sum(off.values())}


def parallels(voices_grid) -> dict:
    """Parallel fifths and octaves between every pair of voices, at each change of either voice, per 100 moves where
    both voices move in the same direction."""
    g = voices_grid
    par, similar, moves = 0, 0, 0
    for i in range(g.shape[1]):
        for j in range(i + 1, g.shape[1]):
            a, b = g[:, i], g[:, j]
            prev = None
            for t in range(len(a)):
                if a[t] < 0 or b[t] < 0:
                    prev = None
                    continue
                cur = (a[t], b[t])
                if prev is not None and cur != prev:
                    moves += 1
                    da, db = cur[0] - prev[0], cur[1] - prev[1]
                    if da * db > 0:
                        similar += 1
                        ic0, ic1 = interval_class(*prev), interval_class(*cur)
                        if ic0 == ic1 and ic0 in PERFECT and abs(cur[0] - cur[1]) == abs(prev[0] - prev[1]):
                            par += 1
                prev = cur
    return {"parallels": par, "moves": moves, "per_100": 100.0 * par / max(moves, 1)}


def cadences(piece) -> dict:
    """Sixth-to-octave cadences between any two voices (a major sixth expanding to an octave by contrary steps); how
    many have the upper voice rising by a semitone (a leading tone), and how many add a third voice rising by a
    semitone to the fifth (the double leading-tone cadence)."""
    grid = piece.grid(4)
    n, V = grid.shape
    found, lead, double = 0, 0, 0
    # the sonority at each change
    rows = [tuple(grid[t]) for t in range(n)]
    ch = [t for t in range(1, n) if rows[t] != rows[t - 1]]
    for t in ch:
        a, b = rows[t - 1], rows[t]
        for i in range(V):
            for j in range(V):
                if i == j or min(a[i], a[j], b[i], b[j]) < 0:
                    continue
                if a[i] - a[j] == 9 and b[i] - b[j] == 12 and b[i] - a[i] in (1, 2) and a[j] - b[j] in (1, 2):
                    found += 1
                    up = b[i] - a[i] == 1
                    lead += up
                    if up and any(k not in (i, j) and min(a[k], b[k]) >= 0 and b[k] - a[k] == 1 and (b[k] - b[j]) % 12 == 7 for k in range(V)):
                        double += 1
    return {"sixth_octave": found, "leading_tone": lead, "double": double}


def final_sonority(piece) -> str:
    """The last chord: 'open' (only unisons, fifths and octaves above the bass), 'third' (a third or sixth in it)."""
    f = piece.final()
    low = min(f)
    ics = {interval_class(x, low) for x in f if x != low}
    return "third" if ics & IMPERFECT else "open"
