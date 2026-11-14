"""Precompute everything numerical, and every sound, in Part 12 of *Music, Built* ("Scales and Modes").

    python -m videos.music.music12.compute              # everything missing (about a minute)
    python -m videos.music.music12.compute --force modes

Numbers are cached in ``.cache/music12/<name>.json`` (+ ``.npz``), sounds in ``.cache/music12/audio/``.  The scale
module is Monochord's (``explainer/music/monochord/scales.py``); published findings are cited in the README.

Items:
    hook        the white keys from C, and the black keys
    stack       one to twelve pure fifths, folded into an octave: the steps they leave; the stacks of 5, 7 and 12
    gaps        the number of sizes of step for stacks of up to sixty notes; where there are two
    modes       the seven modes on one note, brightest to darkest; two to compare; what each does to the Tune
    why         the diatonic scale's evenness, its two sizes of every interval, its interval vector; a scale moved
    minor       the three forms of the minor scale; two endings, without and with a leading note
    fewer       pentatonic, whole-tone, octatonic and blues scales, and how many transpositions each has
    halves      the six ways to fill a fourth; scales as two halves; the seventy-two melakartas
    maps        a major scale, Rast in quarter tones, five equal steps, and the first raga taught in the south
    every       all 352 shapes of scale on twelve notes, by Burnside's lemma and by listing; the three plain sevens
    frontier    every seven-note shape by evenness, fifths and smoothness; a scale of seven equal steps
    tune        Variation 12: the Tune in the seven modes, then pentatonic, whole-tone and octatonic
    variation   the Variations ledger, row 12
"""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import consonance as CONS
from explainer.music.monochord import scales as S
from explainer.music.monochord import tune as TUNE
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.tuning import continued_fraction, convergents

CACHE = Cache("music12")
CLIPS = ClipStore("music12")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
LETTERS = "CDEFGAB"
STEP = 0.3


def clip(y, fade=(0.001, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def piano(hz: float, seconds: float) -> Clip:
    y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.25))
    return clip(y, (0.001, 0.18)).at_level(LEVEL)


def hz_of(semitones: float, base: float = C4) -> float:
    return base * 2.0 ** (semitones / 12.0)


def drone(seconds: float, hz: float = C4 / 2, db: float = -13.0) -> Clip:
    return clip(organ_tone(hz, seconds, partials=4, rolloff=0.6), (0.3, 0.5)).at_level(LEVEL).gain(db)


def run(notes, step: float = STEP, last: float = 2.0, base: float = C4, with_drone: bool = False, t0: float = 0.0) -> Clip:
    """Notes (semitones above ``base``, or cents if a note is a tuple ("c", cents)) one after another on the piano.
    Events ``n0, n1, ...``."""
    placed, events, t = [], {}, t0
    for k, n in enumerate(notes):
        semis = n[1] / 100.0 if isinstance(n, tuple) else float(n)
        d = step * (last if k == len(notes) - 1 else 1.0)
        placed.append((piano(hz_of(semis, base), d), t, 0.0))
        events[f"n{k}"] = t
        t += d
    if with_drone:
        placed.append((drone(t - t0 + 0.4), max(t0 - 0.1, 0.0)))
    c = mix(placed, duration=t + 0.5)
    events["end"] = t
    return Clip(c.y, SR, events, [])


def up(steps, octave: bool = True) -> list[int]:
    p = list(S.pcs(steps))
    return p + [sum(steps)] if octave else p


def spelled(notes) -> list[str]:
    """Seven notes above C (semitones), named with the seven letters in order: the third of C Phrygian is E flat."""
    major = S.pcs(S.MAJOR)
    out = []
    for k, n in enumerate(notes[:7]):
        alter = n - major[k]
        out.append(LETTERS[k] + {0: "", -1: "♭", 1: "♯", -2: "♭♭"}[alter])
    return out


def times(c: Clip, prefix: str, count: int) -> list[float]:
    return [float(c.events[f"{prefix}n{k}"]) for k in range(count)]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    white = run(up(S.MAJOR), step=0.32)
    black = run([6, 8, 10, 13, 15, 18], step=0.32)
    seq = concat([white.at_level(LEVEL), black.at_level(LEVEL)], gap=0.6, names=["white", "black"])
    return {"white": up(S.MAJOR), "black": [6, 8, 10, 13, 15, 18], "white_times": times(seq, "white.", 8), "black_times": times(seq, "black.", 6),
            "clips": {"keys": save("hook.keys", seq, level=None, detail="the white keys from C, then the black keys: Part 7's piano")}}


CHAIN = ["F", "C", "G", "D", "A", "E", "B", "F♯", "C♯", "G♯", "D♯", "A♯"]


def compute_stack() -> dict:
    rows = []
    for n in range(1, 13):
        pts = S.stack(n)                                    # the chain begins on F: position 0 is F
        rows.append({"n": n, "points": pts.tolist(), "gaps": S.gaps(pts).tolist() if n > 1 else [1200.0], "sizes": S.gap_sizes(pts) if n > 1 else [1200.0]})
    order = [float((k * S.FIFTH) % 1.0) for k in range(12)]  # in the order the notes are added
    parts, names = [], []
    for n in (5, 7, 12):
        pts = S.stack(n)
        c_at = (S.FIFTH) % 1.0                               # C is one fifth above F
        rot = np.sort((pts - c_at) % 1.0) if n >= 7 else pts  # seven and twelve are heard from C, five from F
        base = C4 if n >= 7 else C4 * 2 ** (1 - S.FIFTH)          # the F above middle C
        hzs = [base * 2 ** p for p in rot] + [base * 2]
        placed, ev, t = [], {}, 0.0
        for k, h in enumerate(hzs):
            d = 0.3 * (2.0 if k == len(hzs) - 1 else 1.0)
            placed.append((piano(h, d), t, 0.0))
            ev[f"n{k}"] = t
            t += d
        m = mix(placed, duration=t + 0.5)
        parts.append(Clip(m.y, SR, ev, []).at_level(LEVEL))
        names.append(f"s{n}")
    seq = concat(parts, gap=0.7, names=names)
    return {"rows": rows, "order": order, "chain": CHAIN, "fifth_cents": 1200 * S.FIFTH, "comma": 1200 * (12 * S.FIFTH - 7),
            "starts": {str(n): float(seq.events[f"s{n}"]) for n in (5, 7, 12)}, "counts": {"5": 6, "7": 8, "12": 13},
            "note_times": {str(n): times(seq, f"s{n}.", c) for n, c in ((5, 6), (7, 8), (12, 13))},
            "clips": {"three": save("stack.three", seq, level=None, detail="stacks of five, seven and twelve pure fifths, played as scales")}}


def compute_gaps() -> dict:
    ns = list(range(2, 61))
    sizes = [len(S.gap_sizes(S.stack(n))) for n in ns]
    moments = S.moments(60)
    pairs = {str(n): S.gap_sizes(S.stack(n)) for n in moments}
    cf = continued_fraction(S.FIFTH, 8)
    conv = [int(c.denominator) for c in convergents(cf)]
    return {"n": ns, "sizes": sizes, "moments": moments, "pairs": pairs, "ratios": {k: v[0] / v[1] for k, v in pairs.items()},
            "continued_fraction": cf, "convergent_denominators": conv, "all_at_most_three": max(sizes) <= 3}


def chord(semis, seconds: float) -> Clip:
    return mix([(piano(hz_of(s), seconds), 0.012 * k, 0.0) for k, s in enumerate(semis)]).at_level(LEVEL)


def compute_modes() -> dict:
    order = S.by_brightness()
    rows = []
    for name, steps in order:
        notes = list(S.pcs(steps))
        rows.append({"name": name, "steps": list(steps), "notes": notes, "names": spelled(notes), "brightness": S.brightness(steps), "chain": S.fifths_position(name)})
    parts = [run(up(st), with_drone=True).at_level(LEVEL) for _, st in order]
    names = [r["name"] for r in rows]
    seq = concat(parts, gap=0.45, names=names)
    quiz = concat([run(up(S.MODES["Dorian"]), step=0.34, with_drone=True).at_level(LEVEL), run(up(S.MODES["Mixolydian"]), step=0.34, with_drone=True).at_level(LEVEL)], gap=0.9, names=["A", "B"])
    rel = concat([run(up(S.MAJOR)).at_level(LEVEL), run([n - 3 for n in up(S.NAMED["natural minor"])]).at_level(LEVEL),
                  concat([chord([-12, 0, 4, 7], 1.2), chord([-15, -3, 0, 4], 1.6)], gap=0.0).at_level(LEVEL)], gap=0.6, names=["major", "minor", "chords"])
    ionian = S.pcs(S.MODES["Ionian"])
    used = sorted({d for d, _ in TUNE.TUNE})
    changed = {r["name"]: [d for d in used if r["notes"][d - 1] != ionian[d - 1]] for r in rows}
    return {"rows": rows, "starts": [float(seq.events[n]) for n in names], "note_times": [times(seq, f"{n}.", 8) for n in names],
            "quiz": {"A": "Dorian", "B": "Mixolydian"}, "quiz_answer": "B", "tune_degrees": used, "tune_changed": changed,
            "same_tune": [n for n, ch in changed.items() if not ch], "relative_starts": [float(rel.events[k]) for k in ("major", "minor", "chords")],
            "degree_names": ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading note"],
            "formulas": {r["name"]: [("♭" if r["notes"][k] < ionian[k] else "♯" if r["notes"][k] > ionian[k] else "") + str(k + 1) for k in range(7)] for r in rows},
            "clips": {"seven": save("modes.seven", seq, level=None, detail="the seven modes on C over a held C, brightest first"),
                      "quiz": save("modes.quiz", quiz, level=None, detail="two modes on C over a held C"),
                      "relative": save("modes.relative", rel, level=None, detail="C major, A minor, and their home chords: the same seven notes")}}


def compute_why() -> dict:
    white = S.pcs(S.MAJOR)
    even = S.maximally_even(7)
    formula = [(12 * j + 5) // 7 for j in range(7)]             # the offset only chooses the key: with 5 the notes are C D E F G A B
    sevens = list(combinations(range(1, 12), 6))
    ev = sorted({round(S.evenness((0, *c)), 6) for c in sevens}, reverse=True)
    vec = {k: list(S.interval_vector(S.pcs(S.NAMED[k]))) for k in ("major", "melodic minor", "whole-tone", "pentatonic")}
    common = [S.common_tones(white, t) for t in range(1, 12)]
    c_major, g_major, db_major = up(S.MAJOR), [n + 7 for n in up(S.MAJOR)], [n + 1 for n in up(S.MAJOR)]
    seq = concat([run(c_major).at_level(LEVEL), run([n - 12 if n > 12 else n for n in g_major]).at_level(LEVEL), run(db_major).at_level(LEVEL)], gap=0.6, names=["C", "G", "Db"])
    return {"formula": formula, "even_steps": list(S.steps_of(even)), "evenness": {k: S.evenness(S.pcs(S.NAMED[k])) for k in ("major", "melodic minor", "harmonic minor")},
            "evenness_best": ev[0], "evenness_second": ev[1], "vectors": vec, "deep": S.is_deep(white), "common": common,
            "myhill": {str(k): v for k, v in S.myhill(S.MAJOR).items()}, "interval_names": {"2": "seconds", "3": "thirds", "4": "fourths", "5": "fifths", "6": "sixths", "7": "sevenths"},
            "starts": [float(seq.events[k]) for k in ("C", "G", "Db")],
            "clips": {"fifth": save("why.fifth", seq, level=None, detail="a major scale on C, on G and on D flat")}}


def compute_minor() -> dict:
    nat, har, mel = up(S.NAMED["natural minor"]), up(S.NAMED["harmonic minor"]), up(S.NAMED["melodic minor"])
    a = -3                                                   # the scales are heard on the A below middle C
    seq = concat([run([n + a for n in nat]).at_level(LEVEL), run([n + a for n in har]).at_level(LEVEL), run([n + a for n in mel] + [n + a for n in nat[::-1][1:]]).at_level(LEVEL)],
                 gap=0.6, names=["natural", "harmonic", "melodic"])
    # two endings in A minor: an E minor chord, then an E major chord, each before A minor
    e_min, e_maj, a_min = [-8, -5, -1, 4], [-8, -4, -1, 4], [-15, -3, 0, 4]
    plain = concat([chord(e_min, 1.1), chord(a_min, 1.8)], gap=0.0)
    lead = concat([chord(e_maj, 1.1), chord(a_min, 1.8)], gap=0.0)
    two = concat([plain.at_level(LEVEL), lead.at_level(LEVEL)], gap=0.9, names=["A", "B"])
    return {"natural": nat, "harmonic": har, "melodic": mel, "names": {"natural": "A B C D E F G A", "harmonic": "A B C D E F G♯ A", "melodic": "A B C D E F♯ G♯ A"},
            "augmented_second": S.NAMED["harmonic minor"][5], "starts": [float(seq.events[k]) for k in ("natural", "harmonic", "melodic")],
            "note_times": {k: times(seq, f"{k}.", 8) for k in ("natural", "harmonic", "melodic")}, "quiz_answer": "B",
            "clips": {"three": save("minor.three", seq, level=None, detail="A minor: natural, harmonic, and melodic up and down"),
                      "leading": save("minor.leading", two, level=None, detail="two endings on A minor")}}


def compute_fewer() -> dict:
    kinds = ["pentatonic", "whole-tone", "octatonic", "blues"]
    parts = [run(up(S.NAMED[k])).at_level(LEVEL) for k in kinds]
    seq = concat(parts, gap=0.6, names=kinds)
    rng = np.random.default_rng(11)
    moves = rng.choice([-2, -1, -1, 1, 1, 2], size=13)                   # one walk, in steps of a scale; it is played on three scales
    walks, wnames, wnotes = [], [], {}
    for nm, steps in (("five", S.NAMED["pentatonic"]), ("seven", S.MAJOR), ("twelve", S.NAMED["chromatic"])):
        k, idx, seqn = len(steps), len(steps), []
        for mv in np.concatenate([[0], moves]):
            idx = int(np.clip(idx + mv, 0, 2 * k))
            octave, j = divmod(idx, k)
            seqn.append(S.pcs(steps)[j] + 12 * (octave - 1))
        wnotes[nm] = seqn
        walks.append(run(seqn, step=0.26).at_level(LEVEL))
        wnames.append(nm)
    wseq = concat(walks, gap=0.7, names=wnames)
    return {"walk_moves": [int(m) for m in moves], "walk_notes": wnotes, "walk_starts": [float(wseq.events[n]) for n in wnames], "kinds": kinds, "steps": {k: list(S.NAMED[k]) for k in kinds}, "notes": {k: up(S.NAMED[k]) for k in kinds},
            "transpositions": {k: S.transpositions(S.pcs(S.NAMED[k])) for k in kinds + ["major", "chromatic"]},
            "vectors": {k: list(S.interval_vector(S.pcs(S.NAMED[k]))) for k in kinds}, "starts": [float(seq.events[k]) for k in kinds],
            "clips": {"four": save("fewer.four", seq, level=None, detail="pentatonic, whole-tone, octatonic and blues scales on C"),
                      "walks": save("fewer.walks", wseq, level=None, detail="one random walk, played on five notes, on seven and on twelve")}}


def compute_halves() -> dict:
    tetra = S.tetrachords()
    mel = S.melakartas()
    lower, upper = [0, 2, 4, 5], [7, 9, 11, 12]
    d_lower, d_upper = [0, 1, 4, 5], [7, 8, 11, 12]
    seq = concat([run(lower, last=1.6).at_level(LEVEL), run(upper, last=1.6).at_level(LEVEL), run(lower + upper).at_level(LEVEL), run(d_lower + d_upper).at_level(LEVEL)],
                 gap=0.5, names=["lower", "upper", "major", "double"])
    names = {"major": [2, 2, 1], "dorian": [2, 1, 2], "phrygian": [1, 2, 2], "hijaz": [1, 3, 1]}
    return {"tetrachords": [list(t) for t in tetra], "named": names, "scales_of_two_halves": len(tetra) ** 2, "melakartas": len(mel), "mela_count": [2, 6, 6],
            "maya": [0, 1, 4, 5, 7, 8, 11], "modes_among": sum(1 for x in mel if S.steps_necklace(S.steps_of(x)) == S.steps_necklace(S.MAJOR)),
            "starts": [float(seq.events[k]) for k in ("lower", "upper", "major", "double")],
            "clips": {"two": save("halves.two", seq, level=None, detail="two halves of a major scale, the whole, and a scale of two other halves")}}


def compute_maps() -> dict:
    rast = [200, 150, 150, 200, 200, 150, 150]               # in cents: steps of four and three quarter-tones
    five = [240] * 5
    cum = lambda st: [("c", float(v)) for v in np.concatenate([[0], np.cumsum(st)])]        # noqa: E731
    maya = [0, 1, 4, 5, 7, 8, 11, 12]
    seq = concat([run(up(S.MAJOR)).at_level(LEVEL), run(cum(rast)).at_level(LEVEL), run(cum(five)).at_level(LEVEL), run(maya).at_level(LEVEL)], gap=0.6,
                 names=["major", "rast", "five", "maya"])
    dyad = lambda cents_: mix([(piano(C4, 1.5), 0.0, 0.0), (piano(C4 * 2 ** (cents_ / 1200.0), 1.5), 0.012, 0.0)]).at_level(LEVEL)        # noqa: E731
    thirds = concat([dyad(400), dyad(350), dyad(300)], gap=0.5, names=["A", "B", "C"])
    return {"thirds": {"A": 400, "B": 350, "C": 300}, "thirds_answer": "B", "thirds_starts": [float(thirds.events[k]) for k in "ABC"], "rast": rast, "rast_quarters": [4, 3, 3, 4, 4, 3, 3], "five": five, "major": [200, 200, 100, 200, 200, 200, 100], "maya": maya,
            "rast_third": 350, "major_third": 400, "minor_third": 300, "starts": [float(seq.events[k]) for k in ("major", "rast", "five", "maya")],
            "clips": {"four": save("maps.four", seq, level=None, detail="a major scale; Rast in quarter tones; five equal steps; Mayamalavagowla"),
                      "thirds": save("maps.thirds", thirds, level=None, detail="three thirds above the same note: 400, 350 and 300 cents")}}


def compute_every() -> dict:
    neck = S.necklaces(12)
    counts = S.classify(12)
    terms = [[d, S.euler_phi(d), 2 ** (12 // d)] for d in (1, 2, 3, 4, 6, 12)]
    sevens = [list(s) for s in neck if len(s) == 7]
    plain = [s for s in sevens if set(s) <= {1, 2}]
    dia = list(S.steps_necklace(S.MAJOR))
    order = [S.NAMED["melodic minor"], S.MAJOR, (2, 2, 2, 2, 2, 1, 1)]
    seq = concat([run(up(st)).at_level(LEVEL) for st in order], gap=0.7, names=["A", "B", "C"])
    four = [list(x) for x in S.necklaces(4)]
    return {"four": four, "four_total": int(S.burnside(4)), "four_terms": [[1, 1, 16], [2, 1, 4], [4, 2, 2]], "total": int(S.burnside(12)), "listed": len(neck), "terms": terms, "sum": sum(p * c for _, p, c in terms), "counts": [counts[k] for k in range(13)],
            "with_tonic": 2 ** 11, "sevens": sevens, "sevens_with_tonic": math.comb(11, 6), "plain": plain, "diatonic": dia, "quiz_answer": "B",
            "quiz_steps": [list(s) for s in order], "starts": [float(seq.events[k]) for k in "ABC"],
            "clips": {"three": save("every.three", seq, level=None, detail="three scales of seven notes, each made only of whole and half steps")}}


def compute_frontier() -> dict:
    neck = [s for s in S.necklaces(12) if len(s) == 7]
    rows = []
    for s in neck:
        notes = S.pcs(s)
        rough = float(np.mean([CONS.dyad_roughness(2 ** ((b - a) / 12.0)) for a, b in combinations(notes, 2)]))
        rows.append({"steps": list(s), "evenness": S.evenness(notes), "fifths": S.interval_vector(notes)[4], "roughness": rough})
    dia = list(S.steps_necklace(S.MAJOR))
    by_rough = sorted(rows, key=lambda r: r["roughness"])
    rank = 1 + [r["steps"] for r in by_rough].index(dia)
    fives = [s for s in S.necklaces(12) if len(s) == 5]
    five_best = max(fives, key=lambda s: S.interval_vector(S.pcs(s))[4])
    # seven equal steps: a scale, and the Tune's first phrase in it
    eq = 1200.0 / 7
    scale = run([("c", k * eq) for k in range(8)])
    phrase = run([("c", (d - 1) * eq) for d, _ in TUNE.PHRASES[0]], step=0.42)
    seq = concat([scale.at_level(LEVEL), phrase.at_level(LEVEL)], gap=0.7, names=["scale", "tune"])
    return {"rows": rows, "diatonic": dia, "roughness_rank": rank, "of": len(rows), "five_best": list(five_best), "pentatonic": list(S.steps_necklace(S.NAMED["pentatonic"])),
            "equal_step": eq, "equal_fifth": 4 * eq, "equal_third": 2 * eq, "starts": [float(seq.events[k]) for k in ("scale", "tune")],
            "clips": {"equal": save("frontier.equal", seq, level=None, detail="seven equal steps to the octave: a scale, and the Tune's first phrase")}}


# the Tune's phrases: six in the modes from brightest to darkest but one, then four more turns of the first phrase
PLAN = [("Lydian", S.MODES["Lydian"]), ("Ionian", S.MODES["Ionian"]), ("Mixolydian", S.MODES["Mixolydian"]), ("Dorian", S.MODES["Dorian"]),
        ("Aeolian", S.MODES["Aeolian"]), ("Phrygian", S.MODES["Phrygian"]), ("Locrian", S.MODES["Locrian"]), ("pentatonic", S.NAMED["pentatonic"]),
        ("whole-tone", S.NAMED["whole-tone"]), ("octatonic", S.NAMED["octatonic"])]


def degree_note(steps, degree: int) -> int:
    """The note of a scale ``degree`` places from its first (1 is the first; 0 and below go under it)."""
    p, k = S.pcs(steps), len(steps)
    octave, idx = divmod(degree - 1, k)
    return p[idx] + 12 * octave


def compute_tune() -> dict:
    beat = 0.5
    placed, events, phrases = [], {}, []
    t0, i = 0.0, 0
    for k, (name, steps) in enumerate(PLAN):
        degs = TUNE.PHRASES[k] if k < 6 else TUNE.PHRASES[0]
        events[f"phrase{k}"] = t0
        t = t0
        mel, low = [], []
        for d, b in degs:
            top, under = degree_note(steps, d), degree_note(steps, d - 2)             # a second voice two places lower in the scale
            placed.append((piano(hz_of(top), b * beat), t, 0.0))
            placed.append((piano(hz_of(under), b * beat), t, -7.0))
            events[f"n{i}"] = t
            mel.append(top)
            low.append(under)
            t += b * beat
            i += 1
        phrases.append({"name": name, "notes": list(S.pcs(steps)), "melody": mel, "under": low, "t0": t0, "seconds": t - t0})
        t0 = t
    events["end"] = t0
    placed.append((drone(t0 + 0.6, db=-15.0), 0.0))
    c = mix(placed, duration=t0 + 1.2)
    out = Clip(c.y, SR, events, []).at_level(LEVEL)
    lowered = sum(a - b for a, b in zip(S.pcs(S.MODES["Lydian"]), S.pcs(S.MODES["Locrian"])))
    return {"clip": save("tune.variation12", out, level=None, detail="the Tune and a second voice two places below it, over a held C"),
            "seconds": out.duration, "phrases": phrases, "lowered": lowered, "names": [p["name"] for p in phrases]}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 12, "title": r"in the seven modes, brightest to darkest, then pentatonic, whole-tone and octatonic", "seconds": t["seconds"],
            "measure": rf"from Lydian to Locrian, {t['lowered']} notes fall a semitone, one at a time", "clip": "tune.variation12"}


ITEMS = {"hook": compute_hook, "stack": compute_stack, "gaps": compute_gaps, "modes": compute_modes, "why": compute_why, "minor": compute_minor, "fewer": compute_fewer,
         "halves": compute_halves, "maps": compute_maps, "every": compute_every, "frontier": compute_frontier, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
