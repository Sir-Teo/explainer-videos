"""Monochord's changes (Part 39 of *Music, Built*): bebop scales, chord scales, third cycles, reharmonisation, and an
improviser judged by the series' own measures.

    RHYTHM_A, GIANT_STEPS, SO_WHAT   chord progressions (not melodies) of well-known tunes, as lead sheets give them
    bebop_scale(symbol)              a dominant (or major) bebop scale: the chord's scale with one chromatic passing tone
    landing(scale, chord, start)     run a scale in eighth notes from a note on the beat: which notes fall on the beats
    bebop_claim()                    the bebop scale lands chord tones on every beat from every chord tone, both ways;
                                     the plain mode does not
    chord_scale(symbol)              a scale for a chord, and its avoid notes (a semitone above a chord tone)
    key_centres(changes)             the tonics a progression arrives at (its major sevenths), and the steps between them
    coltrane(key)                    Coltrane's substitute for ii-V-I: tonics a major third apart, each with its dominant
    reharmonise(melody, scheme)      chords for a melody: diatonic, with secondary dominants, with tritone substitutes
    improvise(changes, seed)         a phrase grammar: runs, arpeggios and enclosures aimed at the next chord's guide tones
    judge(notes, changes)            the measures: chord tones on beats, guide tones at changes, steps, range
"""

from __future__ import annotations

import numpy as np

from . import blues as BL

# Chord progressions only (chord sequences are not protected the way melodies are); as commonly given in lead sheets.
RHYTHM_A = [["Bb", "G7"], ["Cm7", "F7"], ["Bb", "G7"], ["Cm7", "F7"], ["Bb", "Bb7"], ["Eb", "Ebm"], ["Bb", "F7"], ["Bb"]]
GIANT_STEPS = [["B", "D7"], ["G", "Bb7"], ["Eb"], ["Am7", "D7"], ["G", "Bb7"], ["Eb", "F#7"], ["B"], ["Fm7", "Bb7"],
               ["Eb"], ["Am7", "D7"], ["G"], ["C#m7", "F#7"], ["B"], ["Fm7", "Bb7"], ["Eb"], ["C#m7", "F#7"]]
SO_WHAT = [["Dm7"]] * 16 + [["Ebm7"]] * 8 + [["Dm7"]] * 8          # AABA, 32 bars: D dorian, E-flat dorian, D dorian


def symbols(changes) -> list[str]:
    return [s for bar in changes for s in bar]


def _pcs(symbol: str) -> dict:
    c = BL.chord(symbol if any(symbol.endswith(q) for q in ("7", "m", "6", "dim7", "m7b5")) else symbol + "maj7")
    return c


# ------------------------------------------------------------------------------------------------- scales
SCALES = {"7": (0, 2, 4, 5, 7, 9, 10), "maj7": (0, 2, 4, 5, 7, 9, 11), "": (0, 2, 4, 5, 7, 9, 11), "6": (0, 2, 4, 5, 7, 9, 11),
          "m7": (0, 2, 3, 5, 7, 9, 10), "m": (0, 2, 3, 5, 7, 9, 10), "m6": (0, 2, 3, 5, 7, 9, 11), "m7b5": (0, 1, 3, 5, 6, 8, 10),
          "dim7": (0, 2, 3, 5, 6, 8, 9, 11)}


def chord_scale(symbol: str) -> dict:
    """The usual chord-scale choice (mixolydian for a dominant, ionian for a major chord, dorian for a minor seventh,
    locrian for a half-diminished, whole-half for a diminished seventh) and its avoid notes: scale tones a semitone
    above a chord tone."""
    c = _pcs(symbol)
    sc = [(c["root"] + i) % 12 for i in SCALES[c["quality"]]]
    avoid = [p for p in sc if p not in c["pcs"] and (p - 1) % 12 in c["pcs"]]
    return {"symbol": symbol, "scale": sc, "chord": c["pcs"], "avoid": avoid}


def bebop_scale(symbol: str) -> list[int]:
    """The bebop scale (Barry Harris's teaching): a dominant's mixolydian with the major seventh added, or a major
    chord's ionian with the sharp fifth added; eight notes, ascending pitch classes from the root."""
    c = _pcs(symbol)
    base = [(c["root"] + i) % 12 for i in SCALES[c["quality"]]]
    extra = (c["root"] + (11 if c["quality"] == "7" else 8)) % 12
    return sorted(set(base + [extra]), key=lambda p: (p - c["root"]) % 12)


def _scale_line(scale_pcs, start: int, steps: int, direction: int) -> list[int]:
    """Key numbers walking the scale from ``start`` (which must be in it), ``steps`` notes, up (+1) or down (-1)."""
    out = [start]
    m = start
    for _ in range(steps - 1):
        m += direction
        while m % 12 not in scale_pcs:
            m += direction
        out.append(m)
    return out


def landing(scale_pcs, chord_pcs, start: int, direction: int = -1, steps: int = 17) -> dict:
    """Run the scale in eighth notes from ``start`` (on a beat): which notes fall on the beats (every other note), and
    how many of those are chord tones."""
    line = _scale_line(scale_pcs, start, steps, direction)
    beats = line[0::2]
    hits = [m % 12 in chord_pcs for m in beats]
    return {"line": line, "beats": beats, "hits": hits, "share": sum(hits) / len(hits)}


def bebop_claim(symbol: str = "C7") -> dict:
    """For every chord tone as a starting point and both directions, over two octaves: the share of beats that land
    on chord tones, for the plain chord scale and for the bebop scale."""
    c = _pcs(symbol)
    plain = chord_scale(symbol)["scale"]
    bebop = bebop_scale(symbol)
    rows = []
    for pc in c["pcs"]:
        start = 60 + (pc - 60) % 12
        for d in (-1, 1):
            a = landing(plain, c["pcs"], start, d)
            b = landing(bebop, c["pcs"], start, d)
            rows.append({"start": start, "direction": d, "plain": a["share"], "bebop": b["share"]})
    return {"symbol": symbol, "plain_scale": plain, "bebop_scale": bebop, "rows": rows,
            "bebop_all": all(r["bebop"] == 1.0 for r in rows), "plain_mean": float(np.mean([r["plain"] for r in rows]))}


# ------------------------------------------------------------------------------------------------- key centres
def key_centres(changes) -> dict:
    syms = symbols(changes)
    tonics = []
    for s in syms:
        c = _pcs(s)
        if c["quality"] in ("maj7", "", "6") and (not tonics or tonics[-1] != c["root"]):
            tonics.append(c["root"])
    distinct = sorted(set(tonics))
    steps = sorted({(b - a) % 12 for a in distinct for b in distinct if a != b})
    return {"tonics": tonics, "distinct": distinct, "steps": steps}


def coltrane(key: str = "C") -> list[str]:
    """Coltrane's substitute for ii-V-I in a key (as in Countdown): ii, then three tonics a major third apart, each
    preceded by its dominant: Dm7 Eb7 Abmaj7 B7 Emaj7 G7 Cmaj7 in C."""
    k = BL.NAMES[key]
    seq = [(2, "m7"), (3, "7"), (8, "maj7"), (11, "7"), (4, "maj7"), (7, "7"), (0, "maj7")]
    return [BL.PCN[(k + r) % 12] + q for r, q in seq]


# ------------------------------------------------------------------------------------------------- reharmonisation
DIATONIC = {0: "Cmaj7", 2: "Dm7", 4: "Em7", 5: "Fmaj7", 7: "G7", 9: "Am7", 11: "Bm7b5"}


def reharmonise(melody, scheme: str = "diatonic") -> list[str]:
    """One chord per melody note (key numbers in C major): ``diatonic`` picks the diatonic seventh chord containing the
    note with the strongest function (I, IV, V first); ``secondary`` makes each chord's predecessor its dominant
    where the root falls by a fifth; ``tritone`` replaces those secondary dominants by their tritone substitutes."""
    pref = ["Cmaj7", "Fmaj7", "G7", "Am7", "Dm7", "Em7", "Bm7b5"]
    out = []
    for m in melody:
        pc = m % 12
        out.append(next(s for s in pref if pc in BL.chord(s)["pcs"]))
    if scheme == "diatonic":
        return out
    res = list(out)
    for i in range(len(out) - 1):
        nxt = BL.chord(out[i + 1])
        dom = BL.PCN[(nxt["root"] + 7) % 12] + "7"
        if out[i] != out[i + 1] and melody[i] % 12 in BL.chord(dom)["pcs"] + [(nxt["root"] + 9) % 12, (nxt["root"] + 2) % 12]:
            res[i] = dom if scheme == "secondary" else BL.tritone_sub(dom)
    return res


# ------------------------------------------------------------------------------------------------- the improviser
def _nearest(pcs, m: int, lo: int = 58, hi: int = 84) -> int:
    cands = [x for x in range(lo, hi + 1) if x % 12 in pcs]
    return min(cands, key=lambda x: (abs(x - m), x))


def improvise(changes, seed: int = 0, lo: int = 58, hi: int = 84, rest_prob: float = 0.18, start: int = 70) -> list[tuple]:
    """Eighth notes over ``changes`` (bars of 4 beats; a chord per bar or two): returns [(key, eighth index)].
    For each half-bar (two beats, four eighths) the improviser aims at a target on the next half-bar's first beat: a
    guide tone (third or seventh) of the chord there, nearest the current note.  It reaches it by one of four figures
    chosen at random: a bebop-scale run (from a chord tone, so chord tones land on beats), an arpeggio, an enclosure
    (a scale tone above, a semitone below, then the target), or a rest.  Phrases are breathed: after a rest the line
    restarts near the middle of the range."""
    rng = np.random.default_rng(seed)
    beats = BL.beats_of(changes)
    nb = len(beats)
    notes = []
    m = start
    for h in range(0, nb, 2):                                        # half-bars
        sym = beats[h]
        c = _pcs(sym)
        nxt = _pcs(beats[(h + 2) % nb])
        target_pcs = [nxt["third"], nxt["seventh"] if nxt["seventh"] is not None else nxt["root"]]
        kind = rng.choice(["run", "arp", "enclose", "rest"], p=[0.42, 0.25, 0.2, 0.13 if h else 0.0] / np.sum([0.42, 0.25, 0.2, 0.13 if h else 0.0]))
        e0 = 2 * h
        if kind == "rest" or (h and rng.random() < rest_prob * 0.5):
            m = _nearest(c["pcs"], 70 + int(rng.integers(-4, 5)), lo, hi)
            continue
        if kind == "run":
            first = _nearest(c["pcs"], m, lo, hi)
            sc = bebop_scale(sym) if c["quality"] in ("7", "maj7", "", "6") else chord_scale(sym)["scale"]
            d = -1 if first > 72 else (1 if first < 64 else int(rng.choice([-1, 1])))
            line = _scale_line(sc, first, 4, d)
            if line[-1] < lo or line[-1] > hi:
                line = _scale_line(sc, first, 4, -d)
        elif kind == "arp":
            first = _nearest(c["pcs"], m, lo, hi)
            chord_notes = sorted(x for x in range(first, first + 13) if x % 12 in c["pcs"])[:4]
            line = chord_notes if first < 76 else sorted((x for x in range(first - 12, first + 1) if x % 12 in c["pcs"]), reverse=True)[:4]
        else:
            tgt = _nearest(target_pcs, m, lo + 2, hi - 2)
            sc = chord_scale(sym)["scale"]
            above = tgt + 1
            while above % 12 not in sc:
                above += 1
            first = _nearest(c["pcs"], m, lo, hi)
            line = [first, above, tgt - 1, tgt]
            notes += [(x, e0 + k) for k, x in enumerate(line)]
            m = tgt
            continue
        notes += [(x, e0 + k) for k, x in enumerate(line)]
        m = _nearest(target_pcs, line[-1], lo, hi)
    return notes


def random_line(changes, seed: int = 0, lo: int = 58, hi: int = 84, scale: bool = True) -> list[tuple]:
    """A baseline: eighth notes chosen at random (from each chord's scale, or from all twelve pitch classes), moving
    by steps and small leaps."""
    rng = np.random.default_rng(seed)
    beats = BL.beats_of(changes)
    out = []
    m = 70
    for e in range(2 * len(beats)):
        sym = beats[e // 2]
        pcs = chord_scale(sym)["scale"] if scale else list(range(12))
        cands = [x for x in range(max(lo, m - 4), min(hi, m + 4) + 1) if x % 12 in pcs and x != m]
        m = int(rng.choice(cands))
        out.append((m, e))
    return out


def judge(notes, changes) -> dict:
    """The series' measures for a line over changes: the share of on-beat notes that are chord tones; the share of
    chord changes whose first beat brings a guide tone of the new chord; the share of notes in the chord's scale; the
    share of moves that are steps (Part 14's measure); the range."""
    beats = BL.beats_of(changes)
    syms = beats
    on = [(m, e) for m, e in notes if e % 2 == 0]
    ct = [m % 12 in _pcs(syms[e // 2])["pcs"] for m, e in on]
    changes_at = [i for i in range(len(beats)) if i == 0 or beats[i] != beats[i - 1]]
    at = {e // 2: m for m, e in notes if e % 2 == 0}
    guide_hits = []
    for i in changes_at:
        if i in at:
            c = _pcs(beats[i])
            guide_hits.append(at[i] % 12 in (c["third"], c["seventh"]))
    insc = [m % 12 in chord_scale(syms[e // 2])["scale"] for m, e in notes]
    ms = [m for m, _ in notes]
    moves = [abs(ms[i + 1] - ms[i]) for i in range(len(ms) - 1)]
    return {"notes": len(notes), "on_beat_chord_tones": float(np.mean(ct)) if ct else 0.0,
            "guide_at_changes": float(np.mean(guide_hits)) if guide_hits else 0.0, "changes_hit": len(guide_hits),
            "in_scale": float(np.mean(insc)) if insc else 0.0, "steps": float(np.mean([0 < x <= 2 for x in moves])) if moves else 0.0,
            "range": (min(ms), max(ms)) if ms else (0, 0)}
