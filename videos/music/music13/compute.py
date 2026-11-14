"""Precompute everything numerical, and every sound, in Part 13 of *Music, Built* ("Intervals and Chords").

    python -m videos.music.music13.compute              # everything missing (about two minutes)
    python -m videos.music.music13.compute --force roots

Numbers are cached in ``.cache/music13/<name>.json`` (+ ``.npz``), sounds in ``.cache/music13/audio/``.  The chord
module is Monochord's (``explainer/music/monochord/chords.py``); published findings are cited in the README.

Items:
    hook        one chord in three positions; the same chord close together in the bass, and spread
    intervals   the thirteen intervals within an octave: numbers, qualities, the line of fifths, inversions, classes
    triads      the four triads; the nineteen shapes of three notes, by their intervals and by Part 5's roughness
    scale       the triads on the seven degrees of a major scale; the three that hold every note
    inversion   a triad over each of its notes; figures; Rameau's reduction; the six-four that wants to move
    roots       Parncutt's root for common chords; the pitch Part 4's ear model hears in each triad
    sevenths    five seventh chords; the tritone and its resolution; the seventh harmonic; thirds stacked to a thirteenth
    voicing     an interval's roughness by register; low limits; every four-voice spacing of one chord, ranked
    doubling    what doubling and leaving out do to the root; shells; two strings through a distortion
    symbols     lead-sheet symbols read; one progression in four notations and two keys; one chord with two names
    tonnetz     Euler's lattice; the moves P, L and R; the cycles of six, eight and twenty-four triads
    tune        Variation 13: the Tune over block triads, re-voiced, spread, with sevenths
    frontier    the four triads by two models and by listeners; a listener that names chords from sound
    variation   the Variations ledger, row 13
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chords as CH
from explainer.music.monochord import consonance as CONS
from explainer.music.monochord import scales as S
from explainer.music.monochord import tune as TUNE
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.instruments.plucked import plucked
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.score import Pitch

CACHE = Cache("music13")
CLIPS = ClipStore("music13")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
P = Pitch.parse
_NOTES: dict = {}


def clip(y, fade=(0.001, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def piano(hz: float, seconds: float) -> Clip:
    key = (round(hz, 3), round(seconds, 3))
    if key not in _NOTES:
        y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.25))
        _NOTES[key] = clip(y, (0.001, 0.18)).at_level(LEVEL)
    return _NOTES[key]


def note(m: float, seconds: float) -> Clip:
    return piano(CH.hz(m), seconds)


def chord(midis, seconds: float, roll: float = 0.012, db=None) -> Clip:
    """Piano notes struck (almost) together: each ``roll`` seconds after the one below it."""
    placed = [(note(m, seconds), k * roll, 0.0 if db is None else db[k]) for k, m in enumerate(midis)]
    return mix(placed, duration=seconds + 0.3 + roll * len(midis))


def seq(chords, dur: float = 1.2, last: float = 1.6, roll: float = 0.012, arp: float = 0.0, gap: float = 0.0) -> Clip:
    """Chords one after another.  With ``arp`` each is first played a note at a time, ``arp`` seconds apart.
    Events ``c0, c1, ...`` (and ``c0.k`` for the k-th note of an arpeggio, ``c0.all`` for the chord after it)."""
    placed, events, t = [], {}, 0.0
    for k, ch in enumerate(chords):
        d = last if k == len(chords) - 1 else dur
        events[f"c{k}"] = t
        if arp:
            for j, m in enumerate(ch):
                placed.append((note(m, arp), t, 0.0))
                events[f"c{k}.{j}"] = t
                t += arp
            events[f"c{k}.all"] = t
        placed.append((chord(ch, d, roll), t, 0.0))
        t += d + gap
    events["end"] = t
    c = mix(placed, duration=t + 0.5)
    return Clip(c.y, SR, events, [])


def organ(freqs, seconds: float, partials: int = 6, rolloff: float = 0.7) -> Clip:
    return clip(sum(organ_tone(f, seconds, partials=partials, rolloff=rolloff) for f in freqs), (0.04, 0.15))


def sines(freqs, seconds: float) -> Clip:
    t = np.arange(int(seconds * SR)) / SR
    return clip(sum(np.sin(2 * np.pi * f * t) for f in freqs), (0.04, 0.15))


def times(c: Clip, prefix: str, count: int, stem: str = "c") -> list[float]:
    return [float(c.events[f"{prefix}{stem}{k}"]) for k in range(count)]


def names(midis, flats: bool = True) -> list[str]:
    return [CH.pitch_label(Pitch.from_midi(int(m), flats=flats)) for m in midis]


def midis_of(pitches) -> list[int]:
    return [p.midi for p in pitches]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    three = [[60, 64, 67], [64, 67, 72], [67, 72, 76]]
    a = seq(three, dur=1.3, last=1.7)
    low, spread = [36, 40, 43], [36, 43, 52]
    b = seq([low, spread], dur=1.9, last=2.2)
    return {"three": three, "three_names": [["C4", "E4", "G4"], ["E4", "G4", "C5"], ["G4", "C5", "E5"]], "three_times": times(a, "", 3),
            "low": low, "spread": spread, "low_names": [["C2", "E2", "G2"], ["C2", "G2", "E3"]], "mud_times": times(b, "", 2),
            "roughness": {"low": CH.spacing_roughness(low), "spread": CH.spacing_roughness(spread), "middle": CH.spacing_roughness(three[0])},
            "clips": {"three": save("hook.three", a, detail="C, E and G in three orders: Part 7's piano"),
                      "mud": save("hook.mud", b, detail="C, E and G close together in the bass; then the same three notes spread out")}}


SPELLED = ["C4", "Db4", "D4", "Eb4", "E4", "F4", "F#4", "G4", "Ab4", "A4", "Bb4", "B4", "C5"]


def compute_intervals() -> dict:
    base = P("C4")
    rows = []
    for nm in SPELLED:
        iv = CH.interval(base, P(nm))
        inv = iv.invert()
        rows.append({"note": nm, "label": CH.pitch_label(P(nm)), "semitones": iv.semitones, "number": iv.number, "quality": iv.quality, "name": iv.name, "short": iv.short,
                     "line": iv.line, "inverse": inv.short, "inverse_name": inv.name, "ic": iv.interval_class})
    line = []
    for d in range(-6, 7):
        p = Pitch("FCGDAEB"[(d + 1) % 7], (d + 1) // 7, 4)
        up = p if p.diatonic >= base.diatonic and p.midi >= base.midi else Pitch(p.step, p.alter, 5)
        iv = CH.interval(base, up).simple()
        line.append({"line": d, "label": CH.pitch_label(p), "short": iv.short, "name": iv.name, "quality": iv.quality})
    # the thirteen intervals, each as two notes in turn and then together
    placed, ev, t = [], {}, 0.0
    for k in range(13):
        ev[f"i{k}"] = t
        placed += [(note(60, 0.32), t, 0.0), (note(60 + k, 0.32), t + 0.32, 0.0), (chord([60, 60 + k] if k else [60], 0.95), t + 0.64, 0.0)]
        ev[f"i{k}.both"] = t + 0.64
        t += 1.75
    ev["end"] = t
    m = mix(placed, duration=t + 0.4)
    allc = Clip(m.y, SR, ev, [])
    # one key of the piano, two names: in quarter-comma meantone (Part 6) they are two sounds
    fifth = 1200 * np.log2(5) / 4
    aug4, dim5 = 6 * fifth - 3600, 4800 - 6 * fifth
    tri = concat([organ([C4, C4 * 2 ** (c / 1200)], 1.7).at_level(LEVEL) for c in (aug4, dim5, 600.0)], gap=0.45, names=["aug4", "dim5", "equal"])
    quiz = concat([chord([60, 60 + k], 1.3).at_level(LEVEL) for k in (5, 6, 7)], gap=0.55, names=["A", "B", "C"])
    classes = [{"ic": k, "name": CH.IC_NAMES[k], "pairs": [[a, 12 - a] for a in ([k] if k in (0, 6) else [k])]} for k in range(7)]
    return {"rows": rows, "line": line, "classes": classes, "times": [float(ev[f"i{k}"]) for k in range(13)], "both": [float(ev[f"i{k}.both"]) for k in range(13)],
            "aug4": float(aug4), "dim5": float(dim5), "septimal": [float(1200 * np.log2(7 / 5)), float(1200 * np.log2(10 / 7))],
            "clips": {"all": save("intervals.all", allc, detail="every interval from C up to the octave: one note, the other, then both"),
                      "tritones": save("intervals.tritones", tri, level=None, kind="synthesized", detail="C with F sharp, then C with G flat, in quarter-comma meantone; then the piano's one key"),
                      "quiz": save("intervals.quiz", quiz, level=None, detail="three intervals above middle C")}}


TRIAD_OFFS = {"major": (0, 4, 7), "minor": (0, 3, 7), "diminished": (0, 3, 6), "augmented": (0, 4, 8)}
JUST = {"major": ((1, 1), (5, 4), (3, 2)), "minor": ((1, 1), (6, 5), (3, 2)), "diminished": ((1, 1), (6, 5), (7, 5)), "augmented": ((1, 1), (5, 4), (25, 16))}
SHAPE_NAMES = {(4, 3, 5): "major triad", (3, 4, 5): "minor triad", (3, 3, 6): "diminished triad", (4, 4, 4): "augmented triad", (5, 2, 5): "suspended (fourths)",
               (1, 1, 10): "three neighbours", (2, 2, 8): "three whole tones"}


def et(semis) -> list[float]:
    return [2.0 ** (s / 12.0) for s in semis]


def compute_triads() -> dict:
    four = [[60 + o for o in TRIAD_OFFS[k]] for k in ("major", "minor", "diminished", "augmented")]
    c = seq(four, dur=1.25, last=1.6, arp=0.26, gap=0.25)
    kinds = []
    for k in ("major", "minor", "diminished", "augmented"):
        th = [b - a for a, b in zip(TRIAD_OFFS[k], TRIAD_OFFS[k][1:])]
        fb = CONS.fundamental_bass(JUST[k])
        kinds.append({"kind": k, "offsets": list(TRIAD_OFFS[k]), "thirds": th, "names": [p.name for p in CH.spell("C4", k)], "labels": [CH.pitch_label(p) for p in CH.spell("C4", k)],
                      "just": [list(r) for r in JUST[k]], "fundamental": [fb.numerator, fb.denominator], "roughness": float(CONS.chord_roughness(et(TRIAD_OFFS[k])))})
    # every shape of three notes (Part 12 counted nineteen)
    shapes = []
    for steps in S.necklaces(12):
        if len(steps) != 3:
            continue
        rots = [tuple(steps[i:] + steps[:i]) for i in range(3)]
        rough = []
        for r in rots:                                       # each of its notes in the bass, within an octave above middle C
            pcs = [0, r[0], r[0] + r[1]]
            rough.append(float(CONS.chord_roughness(et(pcs))))
        pcs0 = S.pcs(steps)[:3] if len(S.pcs(steps)) >= 3 else (0, steps[0], steps[0] + steps[1])
        vec = S.interval_vector((0, steps[0], steps[0] + steps[1]))
        name = next((SHAPE_NAMES[r] for r in rots if r in SHAPE_NAMES), "")
        shapes.append({"steps": list(steps), "pcs": [0, steps[0], steps[0] + steps[1]], "vector": list(vec), "step": bool(vec[0] or vec[1]), "tritone": bool(vec[5]),
                       "roughness": float(np.mean(rough)), "name": name})
    shapes.sort(key=lambda s: s["roughness"])
    clean = [s for s in shapes if not s["step"] and not s["tritone"]]
    quiz = concat([chord([62, 65, 69], 1.5).at_level(LEVEL), chord([62, 66, 69], 1.5).at_level(LEVEL)], gap=0.6, names=["A", "B"])
    return {"four": four, "kinds": kinds, "times": times(c, "", 4), "all_times": [float(c.events[f"c{k}.all"]) for k in range(4)],
            "shapes": shapes, "count": len(shapes), "clean": clean, "no_step": sum(1 for s in shapes if not s["step"]),
            "clips": {"four": save("triads.four", c, detail="major, minor, diminished, augmented: each a note at a time, then together"),
                      "quiz": save("triads.quiz", quiz, level=None, detail="two triads on D")}}


def compute_scale() -> dict:
    tri = CH.scale_chords("C4", 3)
    rows = [{"degree": c["degree"], "kind": c["kind"], "roman": c["roman"], "names": c["names"], "labels": [CH.pitch_label(p) for p in c["pitches"]],
             "midis": midis_of(c["pitches"]), "symbol": CH.symbol(c["pitches"][0], c["kind"])} for c in tri]
    up = [r["midis"] for r in rows] + [[72, 76, 79]]
    a = seq(up, dur=0.72, last=1.5)
    primary = [[60, 64, 67], [60, 65, 69], [59, 62, 67], [60, 64, 67]]
    bass = [48, 41, 43, 48]
    b = seq([[bb] + ch for bb, ch in zip(bass, primary)], dur=1.05, last=1.8)
    counts = {k: sum(1 for r in rows if r["kind"] == k) for k in ("major", "minor", "diminished")}
    covered = sorted({n[:-1] for d in (0, 3, 4) for n in rows[d]["names"]})
    return {"rows": rows, "counts": counts, "covered": covered, "times": times(a, "", 8), "primary": primary, "bass": bass, "primary_roman": ["I", "IV", "V", "I"],
            "primary_times": times(b, "", 4),
            "clips": {"triads": save("scale.triads", a, detail="a triad on each note of the C major scale"),
                      "primary": save("scale.primary", b, detail="the triads on the first, fourth and fifth notes, and home again")}}


def compute_inversion() -> dict:
    c = CH.spell("C4", "major")
    pos = []
    for k in range(3):
        v = CH.invert(c, k)
        ids = CH.identify(v)[0]
        pos.append({"names": [p.name for p in v], "labels": [CH.pitch_label(p) for p in v], "midis": midis_of(v), "figures": list(CH.figures(v)), "figure": CH.figure_name(v),
                    "inversion": ids["inversion"], "bass": CH.pitch_label(v[0]), "intervals": [CH.interval(v[0], p).short for p in v[1:]]})
    upper = [60, 64, 67]
    three = seq([[48] + upper, [52] + upper, [55] + upper], dur=1.5, last=1.8)
    cadence = seq([[55, 60, 64, 67], [55, 59, 62, 67], [48, 60, 64, 67]], dur=1.3, last=2.0)
    quiz = concat([chord([52, 60, 67, 72], 1.7).at_level(LEVEL), chord([48, 60, 67, 76], 1.7).at_level(LEVEL)], gap=0.6, names=["A", "B"])
    g7 = [P(n) for n in ("F4", "G4", "B4", "D5")]
    red = CH.stack_of_thirds(g7)
    ids7 = CH.identify(g7)[0]
    return {"positions": pos, "upper": upper, "basses": [48, 52, 55], "three_times": times(three, "", 3), "cadence_times": times(cadence, "", 3),
            "cadence": [[55, 60, 64, 67], [55, 59, 62, 67], [48, 60, 64, 67]], "cadence_fig": ["6/4", "5/3", ""],
            "puzzle": {"names": [p.name for p in g7], "labels": [CH.pitch_label(p) for p in g7], "stack": [CH.pitch_label(p) for p in red], "figure": CH.figure_name(g7),
                       "root": CH.pitch_label(ids7["root"]), "kind": ids7["kind"], "inversion": ids7["inversion"]},
            "clips": {"three": save("inversion.three", three, detail="C, E and G above; under them C, then E, then G"),
                      "cadence": save("inversion.cadence", cadence, detail="the six-four chord on G, the triad on G, and home"),
                      "quiz": save("inversion.quiz", quiz, level=None, detail="one chord, with two different notes in the bass")}}


def compute_roots() -> dict:
    table = []
    for label, pcs, nm in (("C major", [0, 4, 7], "C E G"), ("C minor", [0, 3, 7], "C E♭ G"), ("B diminished", [11, 2, 5], "B D F"), ("C augmented", [0, 4, 8], "C E G♯"),
                           ("G seventh", [7, 11, 2, 5], "G B D F"), ("A minor seventh", [9, 0, 4, 7], "A C E G"), ("C suspended", [0, 5, 7], "C F G"),
                           ("diminished seventh", [11, 2, 5, 8], "B D F A♭")):
        r = CH.root(pcs)
        table.append({"label": label, "notes": nm, "pcs": pcs, "saliences": r["saliences"], "root": r["root"], "root_name": CH.pitch_label(r["root"]),
                      "second": CH.pitch_label(r["second"]), "ambiguity": r["ambiguity"], "tied": [CH.pitch_label(t) for t in r["tied"]]})
    ear = []
    for k in ("major", "minor", "diminished", "augmented"):
        hz, strength = CONS.harmonicity(et(TRIAD_OFFS[k]))
        m = 69 + 12 * np.log2(hz / 440.0)
        ear.append({"kind": k, "hz": float(hz), "strength": float(strength), "midi": float(m), "name": Pitch.from_midi(int(round(m)), flats=True).name,
                    "label": CH.pitch_label(Pitch.from_midi(int(round(m)), flats=True)), "octaves_below": float((60 - m) / 12)})
    f0 = C4 / 2                                              # 4:5:6 over the C below middle C: the notes are C5, E5, G5
    major = sines([4 * f0, 5 * f0, 6 * f0], 2.2).at_level(LEVEL)
    low = clip(organ_tone(f0, 1.8, partials=5, rolloff=0.6), (0.04, 0.2)).at_level(LEVEL)
    both = mix([(major, 0.0, -2.0), (low, 0.0, -2.0)], duration=2.4)
    miss = concat([major, low, Clip(both.y).at_level(LEVEL)], gap=0.5, names=["chord", "low", "both"])
    dim = seq([[59, 62, 65], [43, 59, 62, 65], [48, 60, 64]], dur=1.6, last=2.0)
    return {"table": table, "ear": ear, "weights": {str(k): v for k, v in CH.ROOT_SUPPORT.items()}, "f0": f0, "dim_times": times(dim, "", 3),
            "clips": {"missing": save("roots.missing", miss, level=None, kind="synthesized", detail="three pure tones at 4, 5 and 6 times 131 hertz; a tone at 131 hertz; both"),
                      "dim": save("roots.dim", dim, detail="B, D and F; then with a G under them; then where that chord goes")}}


def compute_sevenths() -> dict:
    kinds = []
    for k in ("maj7", "7", "m7", "m7b5", "dim7"):
        ps = CH.spell("C4", k)
        kinds.append({"kind": k, "name": CH.KIND_NAMES[k], "symbol": CH.symbol("C", k), "names": [p.name for p in ps], "labels": [CH.pitch_label(p) for p in ps],
                      "midis": midis_of(ps), "offsets": list(CH.offsets(k)), "tritones": int(S.interval_vector(CH.offsets(k))[5])})
    a = seq([k["midis"] for k in kinds], dur=1.3, last=1.7, gap=0.2)
    scale7 = [{"degree": c["degree"], "kind": c["kind"], "roman": c["roman"], "labels": [CH.pitch_label(p) for p in c["pitches"]], "midis": midis_of(c["pitches"]),
               "symbol": CH.symbol(c["pitches"][0], c["kind"])} for c in CH.scale_chords("C4", 4)]
    res = seq([[59, 65], [60, 64], [43, 59, 62, 65], [48, 60, 64]], dur=1.4, last=2.0, gap=0.15)
    ratios_et, ratios_just = et((0, 4, 7, 10)), [1.0, 5 / 4, 3 / 2, 7 / 4]
    just = concat([organ([C4 * r for r in ratios_et], 2.4).at_level(LEVEL), organ([C4 * r for r in ratios_just], 2.4).at_level(LEVEL)], gap=0.6, names=["A", "B"])
    figs = []
    g7 = CH.spell("G3", "7")
    for k in range(4):
        v = CH.invert(g7, k)
        figs.append({"names": [p.name for p in v], "figure": CH.figure_name(v), "bass": CH.pitch_label(v[0])})
    tall = CH.spell("C4", "maj13")
    placed, ev, t = [], {}, 0.0
    for j, p in enumerate(tall):
        placed.append((note(p.midi, 0.42 * (7 - j) + 2.0), t, 0.0))
        ev[f"n{j}"] = t
        t += 0.42
    ev["end"] = t + 2.0
    stack = Clip(mix(placed, duration=t + 2.4).y, SR, ev, [])
    return {"kinds": kinds, "times": times(a, "", 5), "scale": scale7, "resolve_times": times(res, "", 4), "inversions": figs,
            "cents": {"equal": 1000.0, "harmonic": float(1200 * np.log2(7 / 4))},
            "roughness": {"equal": float(CONS.chord_roughness(ratios_et)), "just": float(CONS.chord_roughness(ratios_just))},
            "tall": {"names": [p.name for p in tall], "labels": [CH.pitch_label(p) for p in tall], "members": [1, 3, 5, 7, 9, 11, 13], "times": [float(ev[f"n{j}"]) for j in range(7)],
                     "letters": sorted({p.step for p in tall})},
            "clips": {"kinds": save("sevenths.kinds", a, detail="five seventh chords on C"),
                      "resolve": save("sevenths.resolve", res, detail="B and F, moving to C and E; then the whole chord on G, moving to C"),
                      "just": save("sevenths.just", just, level=None, kind="synthesized", detail="a seventh chord on C: the piano's tuning, then the harmonics 4, 5, 6 and 7"),
                      "stack": save("sevenths.stack", stack, detail="thirds stacked on C, up to the thirteenth")}}


def compute_voicing() -> dict:
    basses = list(range(24, 85))
    curves = {str(s): CH.dyad_by_register(s, basses).tolist() for s in (3, 4, 7, 12)}
    ref = CH.spacing_roughness([48, 52])                      # a major third on the C below middle C
    limits = {str(s): CH.low_limit(s, reference=ref) for s in (3, 4, 7, 12)}
    regs = [72, 60, 48, 36, 24]
    thirds = seq([[b, b + 4] for b in regs], dur=1.35, last=1.9, gap=0.15)
    third_rough = [CH.spacing_roughness([b, b + 4]) for b in regs]
    # how wide a major third is, in critical bands (Part 4's ERB), at each register
    from explainer.music.monochord import ear
    in_bands = [float((CH.hz(b + 4) - CH.hz(b)) / ear.erb(CH.hz(b + 2))) for b in regs]
    vs = CH.voicings([0, 4, 7], 36, 76, voices=4, bass=0, max_gap=19)
    vs = [v for v in vs if v[0] == 36]
    ranked = sorted(vs, key=CH.spacing_roughness)
    best, worst = ranked[0], ranked[-1]
    series = [36, 48, 55, 60, 64, 67]                          # harmonics 1 to 6 of the low C
    bw = seq([list(worst), list(best), series], dur=2.0, last=2.4, gap=0.2)
    return {"basses": basses, "curves": curves, "reference": ref, "limits": limits, "limit_names": {k: Pitch.from_midi(v).name for k, v in limits.items()},
            "registers": regs, "register_names": [Pitch.from_midi(b).name for b in regs], "third_roughness": third_rough, "third_bands": in_bands, "third_times": times(thirds, "", 5),
            "count": len(vs), "best": list(best), "worst": list(worst), "best_names": names(best), "worst_names": names(worst),
            "best_roughness": CH.spacing_roughness(best), "worst_roughness": CH.spacing_roughness(worst), "series": series, "series_roughness": CH.spacing_roughness(series),
            "ranked": [CH.spacing_roughness(v) for v in ranked], "bw_times": times(bw, "", 3),
            "clips": {"thirds": save("voicing.thirds", thirds, detail="one major third, on five different Cs, from high to low"),
                      "spread": save("voicing.spread", bw, detail="one chord, four voices over a low C: the roughest spacing, the smoothest, and the first six harmonics")}}


def spectrum_roughness(y, sr: int = SR, peaks: int = 50) -> float:
    """Part 5's roughness of a recorded sound: its strongest spectral peaks, as partials."""
    n = min(len(y), sr)
    seg = np.asarray(y[int(0.15 * sr): int(0.15 * sr) + n], dtype=np.float64)
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1.0 / sr)
    idx = [i for i in range(2, len(sp) - 2) if sp[i] > sp[i - 1] and sp[i] >= sp[i + 1] and 40.0 < f[i] < 5000.0]
    idx = sorted(idx, key=lambda i: -sp[i])[:peaks]
    a = sp[idx] / sp[idx].max()
    keep = a > 0.01
    return float(CONS.roughness(f[idx][keep], a[keep]))


def compute_doubling() -> dict:
    base = CH.root([0, 4, 7])
    rows = [{"label": "one of each", "weights": [1, 1, 1], **{k: base[k] for k in ("salience", "ambiguity")}}]
    for label, w in (("root doubled", [2, 1, 1]), ("third doubled", [1, 2, 1]), ("fifth doubled", [1, 1, 2])):
        r = CH.root([0, 4, 7], w)
        rows.append({"label": label, "weights": w, "salience": r["salience"], "ambiguity": r["ambiguity"], "second": CH.pitch_label(r["second"])})
    no_fifth, no_third = CH.root([0, 4]), CH.root([0, 7])
    # how loud the fifth already is inside one piano note: its third partial against its first
    y = note(48, 1.5).mono
    sp = np.abs(np.fft.rfft(y[: SR] * np.hanning(SR)))
    f = np.fft.rfftfreq(SR, 1.0 / SR)
    f0 = CH.hz(48)
    lev = [float(20 * np.log10(sp[(f > k * f0 * 0.97) & (f < k * f0 * 1.03)].max() / sp[(f > f0 * 0.97) & (f < f0 * 1.03)].max())) for k in (1, 2, 3, 4, 5)]
    shells = [[48, 52, 55, 58], [48, 64, 70], [48, 64, 71], [48, 63, 70]]
    shell = seq(shells, dur=1.5, last=1.9, gap=0.15)
    # two guitar strings through a distortion: a fifth, a major third, a whole triad
    def strings(ms, seconds=2.2):
        return sum(plucked(CH.hz(m), seconds=seconds, beta=0.14) for m in ms)

    def drive(x, gain=18.0):
        x = x / np.max(np.abs(x))
        return np.tanh(gain * x)

    power = {}
    parts = []
    for label, ms in (("fifth", [40, 47]), ("third", [40, 44]), ("triad", [40, 44, 47])):
        clean, dirty = strings(ms), drive(strings(ms))
        power[label] = {"midis": ms, "clean": spectrum_roughness(clean), "driven": spectrum_roughness(dirty)}
        parts.append(clip(dirty, (0.002, 0.25)).at_level(LEVEL - 2.0))
    pw = concat(parts, gap=0.45, names=["fifth", "third", "triad"])
    return {"rows": rows, "no_fifth": {"root": CH.pitch_label(no_fifth["root"]), "ambiguity": no_fifth["ambiguity"], "salience": no_fifth["salience"]},
            "no_third": {"root": CH.pitch_label(no_third["root"]), "ambiguity": no_third["ambiguity"], "salience": no_third["salience"]},
            "partials_db": lev, "shells": shells, "shell_names": ["C7, every note", "C7: root, third, seventh", "Cmaj7: root, third, seventh", "Cm7: root, third, seventh"],
            "shell_times": times(shell, "", 4), "power": power,
            "clips": {"shell": save("doubling.shell", shell, detail="a seventh chord whole; then three seventh chords with only root, third and seventh"),
                      "power": save("doubling.power", pw, level=None, kind="physical model", detail="Part 1's plucked strings through a hard clipper: a fifth, a major third, a triad")}}


def compute_symbols() -> dict:
    read = []
    for text in ("C", "Am7", "G7/B", "Bbmaj7", "F#m7b5", "Dsus4", "E5", "Bdim7"):
        d = CH.parse_symbol(text)
        read.append({"text": d["symbol"], "kind": CH.KIND_NAMES[d["kind"]], "labels": [CH.pitch_label(p) for p in d["pitches"]], "bass": None if d["bass"] is None else CH.pitch_label(d["bass"])})
    prog = [(1, "major", 0), (1, "major", 1), (4, "major", 0), (5, "7", 0), (1, "major", 0)]          # degree, kind, inversion
    keys, voiced, clips_ = {}, {}, []
    for tonic in ("C4", "Eb4"):
        t = P(tonic)
        sc = [t.up(k, CH.MAJOR_STEPS[k]) for k in range(7)]
        syms, basses, chords_, cur = [], [], [], None
        for d, k, inv in prog:
            root = sc[d - 1]
            notes = CH.spell(root, k)
            bass = notes[inv]
            syms.append(CH.symbol(root, k, bass if inv else None))
            basses.append(CH.pitch_label(bass))
            pcs = CH.pcs_of(root.midi, k)
            start = tuple(sorted(n.midi for n in notes))
            cur = start if cur is None else CH.nearest_voicing(cur if len(cur) == len(pcs) else (cur + (cur[-1] + 3,) if len(cur) < len(pcs) else cur[:len(pcs)]), pcs, low=57, high=72)
            b = 36 + bass.midi % 12
            chords_.append([b if b >= 40 else b + 12] + list(cur))
        keys[tonic[:-1]] = {"symbols": syms, "bass": basses}
        voiced[tonic[:-1]] = chords_
        clips_.append(seq(chords_, dur=1.0, last=1.7).at_level(LEVEL))
    roman = [CH.roman(d, k, inv) for d, k, inv in prog]
    nashville = ["1", "1/3", "4", "5⁷", "1"]
    figured = ["", "6", "", "7", ""]
    c = concat(clips_, gap=0.7, names=["C", "Eb"])
    two = CH.identify([P("C4"), P("E4"), P("G4"), P("A4")])
    return {"read": read, "keys": keys, "roman": roman, "nashville": nashville, "figured": figured, "voiced": voiced,
            "times": {"C": times(c, "C.", 5), "Eb": times(c, "Eb.", 5)}, "start": {"C": float(c.events["C"]), "Eb": float(c.events["Eb"])},
            "two": [{"symbol": CH.symbol(CH.pitch_label(x["root"]).replace("♭", "b").replace("♯", "#"), x["kind"], "C" if x["root"] != 0 else None), "root": CH.pitch_label(x["root"]),
                     "kind": CH.KIND_NAMES[x["kind"]]} for x in two],
            "clips": {"prog": save("symbols.prog", c, level=None, detail="one progression in C, then in E flat")}}


def lattice_name(a: int, b: int) -> str:
    line = a + 4 * b                                         # a major third is four fifths (less a comma)
    return CH.pitch_label(Pitch("FCGDAEB"[(line + 1) % 7], (line + 1) // 7, 4))


def voice_led(triads, start=(60, 64, 67)) -> list[list[int]]:
    out, cur = [list(start)], tuple(start)
    for t in triads[1:]:
        cur = CH.nearest_voicing(cur, CH.triad_pcs(t), low=min(cur) - 4, high=max(cur) + 4)
        out.append(list(cur))
    return out


def compute_tonnetz() -> dict:
    pts = [{"a": a, "b": b, "pc": CH.at(a, b), "name": lattice_name(a, b)} for b in range(-1, 3) for a in range(-3, 5)]
    c = (0, "major")
    moves = {}
    for nm, f in CH.MOVES.items():
        u = f(c)
        vl = CH.voice_leading(CH.triad_pcs(c), CH.triad_pcs(u))
        moves[nm] = {"to": CH.triad_name(u), "pcs": list(CH.triad_pcs(u)), "kept": sorted(set(CH.triad_pcs(c)) & set(CH.triad_pcs(u))), "cost": vl["cost"]}
    usual = {(1, "minor"): "C♯m", (6, "minor"): "F♯m", (8, "minor"): "G♯m", (6, "major"): "F♯"}          # the names a musician would write
    cycles = {w: [[t[0], t[1], CH.triad_name(t) if w == "PL" else usual.get(t, CH.triad_name(t))] for t in CH.cycle(c, w)] for w in ("PL", "PR", "LR")}
    plr = concat([seq([[60, 64, 67], v], dur=0.95, last=1.4).at_level(LEVEL) for v in ([60, 63, 67], [59, 64, 67], [60, 64, 69])], gap=0.5, names=["P", "L", "R"])
    hexa = [tuple(t[:2]) for t in cycles["PL"]] + [c]
    hv = voice_led(hexa)
    hx = seq(hv, dur=1.15, last=2.0)
    lr = [tuple(t[:2]) for t in cycles["LR"]] + [c]
    lv = voice_led(lr)
    lrc = seq(lv, dur=0.52, last=1.8)
    total = sum(CH.motion(a, b) for a, b in zip(lv, lv[1:]))
    dist = {CH.triad_name((r, k)): CH.tonnetz_distance(c, (r, k)) for r in range(12) for k in ("major", "minor")}
    return {"points": pts, "moves": moves, "cycles": cycles, "hexa_voicings": hv, "hexa_times": times(hx, "", len(hv)), "lr_voicings": lv, "lr_times": times(lrc, "", len(lv)),
            "lr_motion": int(total), "plr_times": {k: [float(plr.events[k]), float(plr.events[f"{k}.c1"])] for k in "PLR"}, "distances": dist, "farthest": max(dist.values()),
            "commas": {"syntonic": float(1200 * np.log2(81 / 80)), "diesis": float(1200 * np.log2(128 / 125))},
            "clips": {"plr": save("tonnetz.plr", plr, level=None, detail="C major to C minor, to E minor, to A minor: one note moves each time"),
                      "hexa": save("tonnetz.hexa", hx, detail="six triads, each a semitone's motion from the last, and home"),
                      "lr": save("tonnetz.lr", lrc, detail="all twenty-four major and minor triads, each keeping two notes of the one before")}}


def compute_frontier() -> dict:
    # the four triads: two models from Part 5, and the order listeners give (Roberts 1986; Johnson-Laird et al. 2012)
    four = []
    for k in ("major", "minor", "diminished", "augmented"):
        hz, strength = CONS.harmonicity(et(TRIAD_OFFS[k]))
        four.append({"kind": k, "roughness": float(CONS.chord_roughness(et(TRIAD_OFFS[k]))), "fusion": float(strength)})
    by_rough = [f["kind"] for f in sorted(four, key=lambda f: f["roughness"])]
    by_fusion = [f["kind"] for f in sorted(four, key=lambda f: -f["fusion"])]
    listeners = ["major", "minor", "diminished", "augmented"]
    # a listener: chroma of a piano chord against templates
    def heard(midis, harmonics):
        y = chord(midis, 0.9).mono
        return CH.recognise(CH.chroma(y, SR), harmonics=harmonics)

    tests = {"root position, middle": lambda r, k: [60 + r + o for o in TRIAD_OFFS[k]],
             "first inversion": lambda r, k: [60 + r + TRIAD_OFFS[k][1], 60 + r + 7, 72 + r],
             "second inversion": lambda r, k: [55 + r, 60 + r, 60 + r + TRIAD_OFFS[k][1]],
             "close, two octaves down": lambda r, k: [36 + r + o for o in TRIAD_OFFS[k]]}
    acc = {}
    for label, make in tests.items():
        row = {}
        for h in (1, 4):
            right = sum(1 for r in range(12) for k in ("major", "minor") if (lambda g: (g["root"], g["kind"]) == (r, k))(heard(make(r, k), h)))
            row[str(h)] = right
        acc[label] = row
    sevens = {}
    for k, lab in (("7", "dominant seventh"), ("m7", "minor seventh"), ("maj7", "major seventh")):
        outs = {}
        for r in range(12):
            g = heard([48 + r + o for o in CH.offsets(k)], 4)
            rel = ((g["root"] - r) % 12, g["kind"])
            outs[str(rel)] = outs.get(str(rel), 0) + 1
        sevens[lab] = outs
    y = chord([60, 64, 67], 0.9).mono
    ch = CH.chroma(y, SR)
    # and on the Variation: every half bar of it, melody and all
    tune = load("tune")
    audio = CLIPS.load("tune.variation13").mono
    var = []
    for k, ph in enumerate(tune["phrases"]):
        right, rows = 0, []
        for c_ in ph["chords"]:
            a, b = int(c_["t"] * SR), int((c_["t"] + 2 * tune["beat"]) * SR)
            g = CH.recognise(CH.chroma(audio[a:b], SR), harmonics=4)
            want = (ROOT[c_["degree"]] % 12, "major")
            ok = (g["root"], g["kind"]) == want
            right += ok
            rows.append({"want": CH.triad_name(want), "heard": CH.triad_name((g["root"], g["kind"])), "ok": bool(ok)})
        var.append({"name": ph["name"], "right": int(right), "of": len(ph["chords"]), "rows": rows})
    return {"four": four, "variation": var, "variation_right": sum(v["right"] for v in var), "variation_of": sum(v["of"] for v in var), "by_roughness": by_rough, "by_fusion": by_fusion, "listeners": listeners, "accuracy": acc, "sevenths": sevens, "chroma": ch.tolist(),
            "chroma_names": ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"], "trials": 24}


# ---------------------------------------------------------------------------
# Variation 13
# ---------------------------------------------------------------------------
HARMONY = {0: [1, 1, 4, 1], 1: [4, 1, 5, 1], 2: [1, 4, 1, 5], 3: [1, 4, 1, 5], 4: [1, 1, 4, 1], 5: [4, 1, 5, 1]}     # one chord to every two beats
TREATMENTS = ["block triads, root position", "the same kind of chords, re-voiced", "spread: bass, fifth, tenth", "sevenths, as shells", "re-voiced, over a bass", "and to a close"]
ROOT = {1: 60, 4: 53, 5: 55}                                 # C4, F3, G3
SEVENTH = {1: "maj7", 4: "maj7", 5: "7"}


def shell(r: int, kind: str, prev=None) -> list[int]:
    """The third and seventh of a seventh chord, in the octaves nearest the last pair."""
    off = CH.offsets(kind)
    cands = [(a, b) for a in (r + off[1] - 12, r + off[1], r + off[1] + 12) for b in (r + off[3] - 12, r + off[3], r + off[3] + 12) if 55 <= a < b <= 72]
    cands += [(b, a) for a in (r + off[1] - 12, r + off[1], r + off[1] + 12) for b in (r + off[3] - 12, r + off[3], r + off[3] + 12) if 55 <= b < a <= 72]
    if prev is None:
        return list(min(cands, key=lambda c: abs(c[0] - 64)))
    return list(min(cands, key=lambda c: CH.motion(prev, c)))


def compute_tune() -> dict:
    beat = 0.6
    placed, events, phrases = [], {}, []
    t0, i = 0.0, 0
    for k in range(6):
        degs = TUNE.PHRASES[k]
        events[f"phrase{k}"] = t0
        t = t0
        mel = []
        for d, b in degs:
            m = 72 + CH.MAJOR_STEPS[d - 1]
            placed.append((note(m, b * beat), t, 0.0))
            events[f"n{i}"] = t
            mel.append({"midi": m, "t": t, "beats": b, "name": Pitch.from_midi(m).name})
            t += b * beat
            i += 1
        chords_, prev = [], (60, 64, 67)
        for j, deg in enumerate(HARMONY[k]):
            r = ROOT[deg]
            pcs = CH.pcs_of(r, "major")
            bass = r - 12
            if k == 0:
                v = [r, r + 4, r + 7]
            elif k == 1:
                prev = CH.nearest_voicing(prev, pcs, low=57, high=70)
                v = list(prev)
            elif k == 2:
                v = [bass, bass + 7, bass + 16]               # root, fifth, tenth: wide at the bottom
            elif k == 3:
                prev = tuple(shell(r, SEVENTH[deg], None if j == 0 else prev))
                v = [bass] + list(prev)
            elif k == 4:
                prev = CH.nearest_voicing(prev, pcs, low=57, high=70)
                v = [bass] + list(prev)
            else:
                prev = CH.nearest_voicing(prev, pcs, low=57, high=70)
                v = [bass] + list(prev) + ([65] if deg == 5 else [])       # the dominant takes its seventh
                if j == 3:
                    v = [36, 48, 55, 60, 64]
            tc = t0 + j * 2 * beat
            placed.append((chord(sorted(v), 2 * beat, roll=0.01), tc, -5.0))
            events[f"h{k}.{j}"] = tc
            chords_.append({"midis": [int(x) for x in sorted(v)], "t": tc, "degree": deg, "names": [Pitch.from_midi(int(x), flats=True).name for x in sorted(v)]})
        phrases.append({"name": TREATMENTS[k], "melody": mel, "chords": chords_, "t0": t0, "seconds": t - t0})
        t0 = t
    events["end"] = t0
    c = mix(placed, duration=t0 + 1.6)
    out = Clip(c.y, SR, events, []).at_level(LEVEL)
    # the whole Tune's chords, in root position and re-voiced: how far the three voices travel
    degrees = [d for k in range(6) for d in HARMONY[k]]
    block = [[ROOT[d], ROOT[d] + 4, ROOT[d] + 7] for d in degrees]
    smooth, cur = [], (60, 64, 67)
    for d in degrees:
        cur = CH.nearest_voicing(cur, CH.pcs_of(ROOT[d], "major"), low=57, high=70)
        smooth.append(list(cur))
    return {"clip": save("tune.variation13", out, level=None, detail="the Tune over chords, six ways: Part 7's piano"), "seconds": out.duration, "phrases": phrases,
            "block_motion": int(sum(CH.motion(a, b) for a, b in zip(block, block[1:]))), "voiced_motion": int(sum(CH.motion(a, b) for a, b in zip(smooth, smooth[1:]))),
            "chords": len(degrees), "names": TREATMENTS, "beat": beat}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 13, "title": r"over block triads, then re-voiced, spread, and with sevenths", "seconds": t["seconds"],
            "measure": rf"re-voiced, the chords' three voices travel {t['voiced_motion']} semitones over the Tune instead of {t['block_motion']}", "clip": "tune.variation13"}


ITEMS = {"hook": compute_hook, "intervals": compute_intervals, "triads": compute_triads, "scale": compute_scale, "inversion": compute_inversion, "roots": compute_roots,
         "sevenths": compute_sevenths, "voicing": compute_voicing, "doubling": compute_doubling, "symbols": compute_symbols, "tonnetz": compute_tonnetz,
         "tune": compute_tune, "frontier": compute_frontier, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
