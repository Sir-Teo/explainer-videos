"""Precompute everything numerical, and every sound, in Part 29 of *Music, Built* ("Twelve Tones").

    python -m videos.music.music29.compute              # everything missing (a few minutes)
    python -m videos.music.music29.compute --force sets

Numbers are cached in ``.cache/music29/<name>.json``, sounds in ``.cache/music29/audio/``.  The measures are Monochord's
(``explainer/music/monochord/atonal.py``).  Two pieces are played from the music21 corpus's encodings, both now in the
public domain: Schoenberg's Six Little Piano Pieces, Op. 19, Nos. 2 and 6 (1911), and Webern's canon *Dormi Jesu*,
Op. 16 No. 2 (1924).  Every other example is ours.

Items:
    hook        Schoenberg, Op. 19 No. 6, whole, on Part 7's piano
    op19        Op. 19 No. 2, whole; its pitch-class content and its most frequent set classes
    sets        two chords related by transposition or inversion (an ear question); prime forms and interval vectors
    classes     every set class by brute force and by Burnside's lemma; counts by size
    zhex        the Z-related tetrachords heard; Z-pairs counted; the hexachord theorem checked on all 924 hexachords
    row         a row and its 48 forms; an ear question (which is the inversion?); Webern's canon in inversion, heard
    allint      every all-interval row (3,856); Berg's Lyric Suite row heard
    combin      the six all-combinatorial hexachords; a row and its combinatorial inversion together, heard
    total       a pointillist passage of our own: pitch, duration and loudness each from a series
    hear        an ear question: which of two rows is a form of the first?; the chance that two random rows share a hexachord
    trichords   the twelve trichord classes, each as a close chord on C
    hexpair     a hexachord and its complement, as chords
    op25        the row of Schoenberg's Piano Suite, Op. 25, once up the keyboard
    tune        Variation 29: a row grown from the Tune's intervals, then a pointillist variation on it
    variation   the Variations ledger, row 29
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import atonal as A
from explainer.music.monochord import melody as M
from explainer.music.monochord import romantic as R
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff
from explainer.music.monochord.physics.string import String

CACHE = Cache("music29")
CLIPS = ClipStore("music29")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
VIOLIN = STR.violin_body()
C4 = 261.6255653005986
_P: dict = {}
_V: dict = {}


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float, velocity: float = 1.0) -> Clip:
    seconds = round(min(max(seconds, 0.12), 3.5), 2)
    key = (round(m, 3), seconds, round(velocity, 2))
    if key not in _P:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4),
                                  velocity=velocity, seconds=seconds + 0.3))
        _P[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _P[key]


def bowed(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(min(seconds, 3.0), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 3.0), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.008, 0.05).at_level(LEVEL)
    return _V[key]


def place(lines, inst, unit: float, gains=None, tail: float = 1.2) -> Clip:
    gains = gains or [0.0] * len(lines)
    placed, end = [], 0.0
    for ln, g in zip(lines, gains):
        for p, a, d in ln:
            placed.append((inst(p, d * unit * 1.02), a * unit, g))
            end = max(end, (a + d) * unit)
    return Clip(mix(placed, duration=end + tail).y, SR)


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


def piece(word: str) -> dict:
    return next(r for r in R.load_library() if word in r["path"])


def beats(notes):
    return [(p, o / 24.0, d / 24.0) for p, o, d in notes]


def line_of(row, start=60, unit_beats=1.0, octaves=None):
    octaves = octaves or [0] * len(row)
    return [(start + pc + 12 * o, i * unit_beats, unit_beats) for i, (pc, o) in enumerate(zip(row, octaves))]


def tune_intervals():
    t = M.corpus([M.THE_TUNE])[0]
    ps = list(t.pitches)
    return [b - a for a, b in zip(ps, ps[1:]) if b != a]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    p = piece("opus19/movement6")
    notes = beats(R.all_notes(p["parts"]))
    unit = 1.1
    c = place([notes], lambda m, s: piano(m, s, 0.8), unit, tail=2.5)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["op19"])
    return {"notes": rows(notes), "unit": unit, "bars": 9,
            "clips": {"op19": save("hook.op19no6", s_, detail="Schoenberg, Six Little Piano Pieces, Op. 19 No. 6 (1911), whole, from the encoding, Part 7's piano")}}


def compute_op19() -> dict:
    p = piece("opus19/movement2")
    notes = beats(R.all_notes(p["parts"]))
    unit = 0.75
    c = place([notes], lambda m, s: piano(m, s, 0.9), unit, tail=2.0)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["op19"])
    # simultaneities: the pitch classes sounding at each onset
    onsets = sorted({a for _, a, _ in notes})
    chords = []
    for t in onsets:
        pcs = A.norm([q for q, a, d in notes if a <= t < a + d])
        if len(pcs) >= 3:
            chords.append(pcs)
    classes = Counter(A.prime_form(c_) for c_ in chords)
    pc_time = [0.0] * 12
    for q, a, d in notes:
        pc_time[int(q) % 12] += d
    m = R.measure(R.all_notes(p["parts"]))
    return {"notes": rows(notes), "unit": unit, "pc_time": pc_time, "chords": len(chords),
            "top": [[list(k), v, list(A.interval_vector(k))] for k, v in classes.most_common(6)],
            "chromaticism": m["chromaticism"], "clarity": m["clarity"],
            "clips": {"op19": save("op19.no2", s_, detail="Schoenberg, Op. 19 No. 2 (1911), whole, from the encoding, Part 7's piano")}}


def compute_sets() -> dict:
    a = [60, 61, 64, 66]                              # {0, 1, 4, 6}
    b = [67 - (x - 60) for x in a]                    # its inversion about G: 67, 66, 63, 61
    unit = 0.9
    ca = place([[(p, 0, 2) for p in a] + [(p, 2.5 + 0.5 * i, 0.5) for i, p in enumerate(a)]], piano, unit)
    cb = place([[(p, 0, 2) for p in sorted(b)] + [(p, 2.5 + 0.5 * i, 0.5) for i, p in enumerate(sorted(b))]], piano, unit)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    examples = {}
    for name, s in (("major triad", [0, 4, 7]), ("minor triad", [0, 3, 7]), ("dominant seventh", [0, 4, 7, 10]),
                    ("half-diminished", [0, 3, 6, 10]), ("Tristan chord", [5, 11, 3, 8]), ("all-interval tetrachord", [0, 1, 4, 6])):
        examples[name] = {"set": A.norm(s), "normal": list(A.normal_order(s)), "prime": list(A.prime_form(s)), "iv": list(A.interval_vector(s))}
    return {"A": a, "B": sorted(b), "unit": unit, "answer": "inversion", "starts": {k: float(s_.events[k]) for k in "AB"},
            "prime_A": list(A.prime_form(a)), "prime_B": list(A.prime_form(b)), "examples": examples,
            "clips": {"quiz": save("sets.quiz", s_, detail="two four-note chords, each struck and then broken: {C, C sharp, E, F sharp}, then its inversion; Part 7's piano")}}


def compute_classes() -> dict:
    sc = A.set_classes()
    by = Counter(len(k) for k in sc)
    return {"brute": len(sc), "burnside": A.burnside_ti(), "by_size": {str(k): by[k] for k in range(13)},
            "forte_sizes": {"3": 12, "4": 29, "5": 38, "6": 50, "7": 38, "8": 29, "9": 12}}


def compute_zhex() -> dict:
    z = A.z_pairs()
    zt = [p for p in z if len(p[0]) == 4][0]
    unit = 0.8
    chords = []
    for i, s in enumerate(zt):
        notes = [(60 + x, 3 * i, 2.5) for x in s]
        chords += notes
    c = place([chords], piano, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["z"])
    h = A.hexachord_theorem()
    zs = Counter(len(p[0]) for p in z)
    return {"pairs": [[list(a), list(b)] for a, b in z], "by_size": {str(k): v for k, v in zs.items()}, "z4": [list(x) for x in zt],
            "iv_z4": list(A.interval_vector(zt[0])), "hexachord": h, "chords": rows(chords), "unit": unit,
            "example": {"set": [0, 1, 2, 4, 7, 8], "complement": list(A.complement([0, 1, 2, 4, 7, 8])),
                        "iv": list(A.interval_vector([0, 1, 2, 4, 7, 8])), "iv_c": list(A.interval_vector(A.complement([0, 1, 2, 4, 7, 8])))},
            "diff_triad": A.ic_count_with_complement([0, 4, 7]),
            "clips": {"z": save("zhex.z", s_, detail="the two all-interval tetrachords, {C, C sharp, E, F sharp} and {C, C sharp, E flat, G}: different chords, the same intervals; Part 7's piano")}}


ROW = [0, 11, 7, 8, 3, 1, 2, 10, 6, 5, 4, 9]                  # ours


def compute_row() -> dict:
    f = A.forms(ROW)
    unit = 0.32
    p0 = line_of(f["P0"], start=60)
    i0 = line_of(f["I0"], start=60)
    r0 = line_of(f["R0"], start=60)
    cP = place([p0], piano, unit)
    cA = place([r0], piano, unit)                                 # A: the retrograde
    cB = place([i0], piano, unit)                                 # B: the inversion
    s_ = concat([cP.at_level(LEVEL), cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.0, names=["P", "A", "B"])
    w = piece("webern")
    g, k = beats(w["parts"]["Gesang"]), beats(w["parts"]["Klarinette"])
    gi = [b[0] - a[0] for a, b in zip(g, g[1:])]
    ki = [b[0] - a[0] for a, b in zip(k, k[1:])]
    inverted = sum(1 for x, y in zip(gi, ki) if x == -y)
    lag = g[0][1] - k[0][1]
    wunit = 0.62
    cv = Clip(CH.sing([(p, a * wunit, d * wunit) for p, a, d in g], "soprano", "u"), SR)
    cv = Clip(cv.y / max(np.abs(cv.y).max(), 1e-9) * 0.5, SR).fade(0.02, 0.3)
    ck = place([k], bowed, wunit)
    cw = Clip(mix([(cv.at_level(LEVEL), 0.0, 0.0), (ck, 0.0, -2.0)], duration=max(cv.duration, ck.duration) + 0.5).y, SR)
    s2 = concat([cw.at_level(LEVEL)], gap=0.0, names=["canon"])
    return {"row": ROW, "forms": {k_: v for k_, v in f.items()}, "distinct": A.distinct_forms(ROW), "matrix": A.matrix(ROW),
            "P0": rows(p0), "R0": rows(r0), "I0": rows(i0), "unit": unit, "answer": "B", "starts": {k_: float(s_.events[k_]) for k_ in ("P", "A", "B")},
            "webern": {"voice": rows(g), "clarinet": rows(k), "inverted": inverted, "intervals": len(gi), "lag_beats": lag,
                       "same_durations": sum(1 for a, b in zip(g, k) if a[2] == b[2]), "notes": len(g), "unit": wunit},
            "clips": {"quiz": save("row.quiz", s_, detail="a twelve-tone row of our own (P0), then its retrograde, then its inversion; Part 7's piano"),
                      "canon": save("row.webern", s2, kind="synthesized", level=None,
                                    detail="Webern, Dormi Jesu, Op. 16 No. 2 (1924), whole, from the encoding: a synthetic soprano (on 'oo') and Part 7's bowed string in place of the clarinet")}}


BERG = [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]


def compute_allint() -> dict:
    rows_ = A.all_interval_rows()
    mid = sum(1 for r in rows_ if A.intervals(r)[5] == 6)         # the tritone always falls in the middle
    ends = sum(1 for r in rows_ if (r[-1] - r[0]) % 12 == 6)      # and the first and last notes are a tritone apart
    unit = 0.36
    berg = line_of(BERG, start=60)
    c = place([berg], piano, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["berg"])
    sym = sum(1 for r in rows_ if A.intervals(r) == [(12 - x) % 12 for x in A.intervals(r)][::-1])
    return {"count": len(rows_), "first": list(rows_[0]), "berg": BERG, "berg_ok": A.is_all_interval(BERG), "berg_intervals": A.intervals(BERG),
            "tritone_middle": mid, "tritone_ends": ends, "unit": unit, "line": rows(berg), "symmetric": sym,
            "clips": {"berg": save("allint.berg", s_, detail="the row of Berg's Lyric Suite (1926), an all-interval row, once up the keyboard; Part 7's piano")}}


def compute_combin() -> dict:
    hexes = A.all_combinatorial_hexachords()
    row = [0, 2, 1, 4, 3, 5, 9, 11, 6, 10, 7, 8]
    first = set(row[:6])
    partner = None
    for n in range(12):
        inv = [(n - x) % 12 for x in row]
        if set(inv[:6]) == set(range(12)) - first:
            partner = (n, inv)
            break
    unit = 0.3
    top = line_of(row, start=72)
    bot = line_of(partner[1], start=48)
    c = place([top, bot], piano, unit, gains=[0.0, -2.0])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["two"])
    return {"hexachords": [list(h) for h in hexes], "row": row, "partner": partner[1], "partner_n": partner[0],
            "aggregates": [sorted(set(row[:6]) | set(partner[1][:6])), sorted(set(row[6:]) | set(partner[1][6:]))],
            "top": rows(top), "bot": rows(bot), "unit": unit,
            "clips": {"two": save("combin.two", s_, detail="a row of our own and its combinatorial inversion played together: each half-bar holds all twelve pitch classes; Part 7's piano")}}


def compute_total() -> dict:
    rng = np.random.default_rng(1949)
    row = [0, 11, 7, 8, 3, 1, 2, 10, 6, 5, 4, 9]
    dur_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]                     # in sixteenths
    dyn_series = [0.4, 1.4, 0.7, 1.1, 0.5, 1.3, 0.8, 1.0, 0.6, 1.2, 0.9, 0.45]
    order_d = [row.index(i) for i in range(12)]
    notes, t = [], 0.0
    reg = rng.integers(-2, 3, size=12)
    for i, pc in enumerate(row):
        d = dur_series[(order_d[i]) % 12] / 4.0
        p = 60 + pc + 12 * int(reg[i])
        notes.append((p, t, d, dyn_series[i]))
        t += d
    unit = 0.36
    placed = [(piano(p, d * unit, v), a * unit, 0.0) for p, a, d, v in notes]
    c = Clip(mix(placed, duration=t * unit + 1.5).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["total"])
    return {"notes": [[float(p), float(a), float(d), float(v)] for p, a, d, v in notes], "unit": unit, "row": row,
            "durations": [n[2] * 4 for n in notes], "dynamics": [n[3] for n in notes],
            "clips": {"total": save("total.points", s_, detail="a pointillist passage of our own: pitch classes from a row, durations from 1 to 12 sixteenths and loudness from series, registers scattered; Part 7's piano")}}


def compute_hear() -> dict:
    rng = np.random.default_rng(29)
    f = A.forms(ROW)
    target = f["RI5"]
    scramble = list(ROW[:6][::-1]) + list(ROW[6:])
    unit = 0.3
    cP = place([line_of(ROW)], piano, unit)
    cA = place([line_of(scramble)], piano, unit)
    cB = place([line_of(target)], piano, unit)
    s_ = concat([cP.at_level(LEVEL), cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.0, names=["P", "A", "B"])
    # how often does a random ordering share the first hexachord with P0 (a "related" row by content alone)?
    trials = 20000
    share = sum(1 for _ in range(trials) if set(rng.permutation(12)[:6]) == set(ROW[:6])) / trials
    return {"row": ROW, "A": scramble, "B": target, "B_name": "RI5", "unit": unit, "answer": "B", "starts": {k: float(s_.events[k]) for k in ("P", "A", "B")},
            "share_random": share, "share_exact": 1 / 924,
            "clips": {"quiz": save("hear.quiz", s_, detail="our row, then a reordering of it, then one of its 48 forms (the retrograde inversion on F); Part 7's piano")}}


def compute_tune() -> dict:
    ivs = tune_intervals()
    row = A.tune_row(ivs, start=0)
    f = A.forms(row)
    unit = 0.34
    plain = line_of(row, start=60)
    rng = np.random.default_rng(2029)
    seq = f["P0"] + f["I7"] + f["R0"]
    pts, t = [], 0.0
    for i, pc in enumerate(seq):
        d = [0.5, 1, 1.5, 0.75][i % 4]
        oc = int(rng.integers(-2, 3))
        pts.append((60 + pc + 12 * oc, t, d))
        t += d if i % 3 else d + 0.5
    c1 = place([plain], lambda m, s: piano(m, s), unit)
    c2 = Clip(mix([((bowed if i % 3 == 1 else (lambda m, s: piano(m, s, 0.9)))(p, d * unit), a * unit, 0.0) for i, (p, a, d) in enumerate(pts)],
                  duration=t * unit + 1.5).y, SR)
    s_ = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.2, names=["row", "points"])
    return {"intervals": ivs, "row": row, "plain": rows(plain), "points": rows(pts), "unit": unit,
            "starts": {k: float(s_.events[k]) for k in ("row", "points")}, "seconds": s_.duration,
            "notes": {"from_tune": sum(1 for _ in row[: len(row)]), "points": len(pts), "forms": 3},
            "clips": {"variation": save("tune.variation29", s_, detail="a row grown from the Tune's intervals (Part 7's piano), then a pointillist variation on three of its forms (piano and bowed string); ours")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 29, "title": r"as a twelve-tone row grown from its own intervals, then scattered in points", "seconds": round(t["seconds"], 2),
            "measure": rf"row {' '.join(str(x) for x in t['row'])}; {t['notes']['points']} notes from three of its 48 forms",
            "clip": "tune.variation29"}


def compute_trichords() -> dict:
    tri = sorted([pf for pf in A.set_classes() if len(pf) == 3])
    unit = 0.7
    notes = []
    for i, pf in enumerate(tri):
        notes += [(60 + x, 1.5 * i, 1.2) for x in pf]
    c = place([notes], lambda m, s: piano(m, s, 0.9), unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["twelve"])
    return {"classes": [list(t) for t in tri], "ivs": [list(A.interval_vector(t)) for t in tri], "unit": unit, "step": 1.5,
            "clips": {"twelve": save("trichords.twelve", s_, detail="the twelve trichord classes in prime form, each as a close chord on middle C; Part 7's piano")}}


def compute_hexpair() -> dict:
    h = [0, 1, 2, 4, 7, 8]
    comp = list(A.complement(h))
    unit = 0.8
    notes = [(60 + x, 0, 2.5) for x in h] + [(60 + x, 3.2, 2.5) for x in comp]
    c = place([notes], lambda m, s: piano(m, s, 0.8), unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["pair"])
    return {"hex": h, "comp": comp, "iv": list(A.interval_vector(h)), "iv_c": list(A.interval_vector(comp)), "unit": unit,
            "same_class": A.prime_form(h) == A.prime_form(comp),
            "clips": {"pair": save("hexpair.two", s_, detail="the hexachord {C, C sharp, D, E, G, A flat} and its complement, each as one chord; Part 7's piano")}}


OP25 = [4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10]


def compute_op25() -> dict:
    unit = 0.36
    line = line_of(OP25, start=60)
    c = place([line], piano, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["row"])
    return {"row": OP25, "line": rows(line), "unit": unit, "ends": (OP25[-1] - OP25[0]) % 12, "is_row": A.is_row(OP25),
            "tetrachords": [list(A.prime_form(OP25[i:i + 4])) for i in (0, 4, 8)], "all_interval": A.is_all_interval(OP25),
            "clips": {"row": save("op25.row", s_, detail="the row of Schoenberg's Piano Suite, Op. 25 (1921-23), once up the keyboard; Part 7's piano")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation29", 29)


ITEMS = {"hook": compute_hook, "op19": compute_op19, "sets": compute_sets, "classes": compute_classes, "zhex": compute_zhex, "row": compute_row,
         "allint": compute_allint, "combin": compute_combin, "total": compute_total, "hear": compute_hear, "trichords": compute_trichords, "hexpair": compute_hexpair, "op25": compute_op25, "tune": compute_tune,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
