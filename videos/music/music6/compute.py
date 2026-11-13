"""Precompute everything numerical, and every sound, in Part 6 of *Music, Built* ("Tuning").

    python -m videos.music.music6.compute              # everything missing (a few seconds)
    python -m videos.music.music6.compute --force pump

Numbers are cached in ``.cache/music6/<name>.json`` (+ ``.npz``), sounds in ``.cache/music6/audio/``.  The tuning
systems are Monochord's (``explainer/music/monochord/tuning.py``), exact where they can be; published tables and
dates are cited in the README.

Items:
    pump        four times round one progression in pure chords, and how far the tonic has sunk
    circle      twelve pure fifths against seven octaves: the Pythagorean comma; Pythagorean tuning and its wolf
    syntonic    four fifths against a pure third: the syntonic comma; the lattice of just intonation and its wolf
    meantone    quarter-comma meantone: pure thirds, narrow fifths, one wolf; a good key and a bad one
    well        Werckmeister III against the others, key by key
    equal       the twelfth root of two; what equal temperament costs; the beats a tuner counts
    why12       continued fractions of log2(3/2); the errors of every equal division up to 60; triads in 12, 19, 31, 53
    piano       stretched octaves on stiff strings; a model of Railsback's curve
    tune        Variation 6: the Tune, harmonised, in eight tunings
    variation   the Variations ledger, row 6
    nextpart    one plucked note, for Part 7
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import consonance as K
from explainer.music.monochord import tune as TUNE
from explainer.music.monochord import tuning as T
from explainer.music.monochord.partkit import organ_chord, organ_tone, saver, string_note

CACHE = Cache("music6")
CLIPS = ClipStore("music6")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
C4 = 261.6255653005986


def frac(x: Fraction) -> list[int]:
    return [x.numerator, x.denominator]


def spread(notes: dict, names) -> list[float]:
    """A chord's notes as frequencies, in close position upwards from the first name, near middle C."""
    out, last = [], None
    for n in names:
        f = C4 * float(notes[n])
        while last is not None and f < last:
            f *= 2
        out.append(f)
        last = f
    return out


# ---------------------------------------------------------------------------
def compute_pump() -> dict:
    rounds = 4
    chords = T.comma_pump(rounds)
    beat = 0.95
    clips, rows = [], []
    order = {"C": ("C", "E", "G"), "A": ("A", "C", "E"), "D": ("D", "F", "A"), "G": ("G", "B", "D")}
    for k, ch in enumerate(chords):
        names = order[ch["root"]]
        done = 0 if k == 0 else (k - 1) // 4                # rounds completed before this chord
        lo = 0.84 * float(Fraction(80, 81) ** done)        # the octave this round's notes are placed in sinks with the tonic
        freqs = []
        for n in names:
            r = float(ch["notes"][n])
            while r >= 2 * lo:
                r /= 2
            while r < lo:
                r *= 2
            freqs.append(C4 * r)
        freqs.sort()
        last = k == len(chords) - 1
        clips.append(organ_chord(freqs, beat * (2.4 if last else 1.0), fade=(0.02, 0.08), decay=0.6))
        tonic = min(freqs, key=lambda f: abs(1200 * math.log2(f / C4) - T.pump_drift(done + (1 if (k and k % 4 == 0) else 0)))) if ch["root"] == "C" else None
        rows.append({"root": ch["root"], "quality": ch["quality"], "notes": {n: frac(ch["notes"][n]) for n in names}, "freqs": freqs,
                     "tonic_cents": 1200 * math.log2(tonic / C4) if tonic else None})
    seq = concat([c.at_level(LEVEL) for c in clips], gap=0.0, names=[f"c{k}" for k in range(len(clips))])
    first, last = clips[0], clips[-1]
    compare = concat([organ_chord(rows[0]["freqs"], 2.0).at_level(LEVEL), organ_chord(rows[-1]["freqs"], 2.0).at_level(LEVEL)], gap=0.4, names=["first", "last"])
    drift = [T.pump_drift(r) for r in range(rounds + 1)]
    one = T.comma_pump(1)
    return {"rounds": rounds, "rows": rows, "beat": beat, "drift": drift, "per_round": drift[1], "total": drift[-1],
            "chain": [{"root": c["root"], "quality": c["quality"], "notes": {n: frac(v) for n, v in c["notes"].items()}} for c in one],
            "comma": frac(T.SYNTONIC_COMMA), "comma_cents": T.cents(T.SYNTONIC_COMMA), "semitone_fraction": abs(drift[1]) / 100.0,
            "clips": {"rounds": save("pump.rounds", seq, level=None, detail="one progression, four times, in pure chords"),
                      "compare": save("pump.compare", compare, level=None, detail="the first chord and the last")}}


def compute_circle() -> dict:
    steps = []
    r = Fraction(1)
    for k in range(13):
        steps.append({"k": k, "exact": frac(Fraction(3, 2) ** k), "folded": frac(T.fold(r)), "cents": T.cents(T.fold(r)) if k < 12 else 1200 + T.cents(T.PYTHAGOREAN_COMMA),
                      "name": ("C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "E#", "B#")[k]})
        r *= Fraction(3, 2)
    comma = T.PYTHAGOREAN_COMMA
    walk = concat([Clip(organ_tone(C4 * float(Fraction(*s["folded"])), 0.5, decay=1.5)).fade(0.01, 0.06).at_level(LEVEL - 1) for s in steps[:12]]
                  + [Clip(organ_tone(C4 * float(comma), 0.9, decay=1.0)).fade(0.01, 0.1).at_level(LEVEL - 1)], gap=0.03, names=[f"s{k}" for k in range(13)])
    both = Clip(organ_tone(C4, 3.0) + organ_tone(C4 * float(comma), 3.0)).fade(0.03, 0.15)
    p = T.pythagorean()
    pure, wolf = dict(p.fifths())["C"], dict(p.fifths())["G#"]
    gs, eb = C4 * 2 ** ((p.pc("G#") - 1200) / 1200), C4 * 2 ** (p.pc("Eb") / 1200)
    fifths = concat([organ_chord([C4, C4 * 1.5], 2.2).at_level(LEVEL), organ_chord([gs, eb], 2.2).at_level(LEVEL)], gap=0.4, names=["pure", "wolf"])
    return {"steps": steps, "comma": frac(comma), "comma_cents": T.cents(comma), "beat": C4 * (float(comma) - 1), "power3": 3 ** 12, "power2": 2 ** 19,
            "fifths": [[n, s] for n, s in p.fifths()], "thirds": [[n, s] for n, s in p.thirds()], "wolf_cents": wolf, "pure_cents": pure,
            "wolf_beat": abs(3 * gs - 2 * eb), "wolf_hz": [gs, eb],
            "clips": {"walk": save("circle.walk", walk, level=None, detail="twelve pure fifths from C, folded into one octave, and the note they reach"),
                      "both": save("circle.both", both, detail="C, and the C twelve pure fifths away, together"),
                      "wolf": save("circle.wolf", fifths, level=None, detail="a pure fifth, then the one left over")}}


def compute_syntonic() -> dict:
    pyth, pure = Fraction(81, 64), Fraction(5, 4)
    seq = concat([organ_chord([C4, C4 * float(pyth)], 2.4).at_level(LEVEL), organ_chord([C4, C4 * float(pure)], 2.4).at_level(LEVEL)], gap=0.4, names=["fifths", "pure"])
    # the lattice of just intonation: each note as 3^a 5^b (octaves ignored)
    lattice = []
    for name, r in T.JUST.items():
        a, b = None, None
        for bb in (-1, 0, 1):
            for aa in range(-3, 4):
                if T.fold(Fraction(3) ** aa * Fraction(5) ** bb) == r:
                    a, b = aa, bb
        lattice.append({"name": name, "ratio": frac(r), "fifths": a, "thirds": b, "cents": T.cents(r)})
    j = T.just()
    d_a = j.interval("D", "A")
    da = organ_chord([C4 * float(T.JUST["D"]), C4 * float(T.JUST["A"])], 2.2).at_level(LEVEL)
    cg = organ_chord([C4, C4 * 1.5], 2.2).at_level(LEVEL)
    top = float(Fraction(5, 4) ** 3)                        # three pure thirds: 125/64, short of the octave
    diesis = concat([organ_chord([C4, 2 * C4], 2.2).at_level(LEVEL), organ_chord([C4, top * C4], 2.2).at_level(LEVEL)], gap=0.4, names=["octave", "thirds"])
    return {"three_thirds": frac(Fraction(5, 4) ** 3), "diesis": frac(T.DIESIS), "diesis_cents": T.cents(T.DIESIS), "diesis_beat": abs(2 * C4 - top * C4),
            "from_fifths": frac(pyth), "pure": frac(pure), "comma": frac(T.SYNTONIC_COMMA), "comma_cents": T.cents(T.SYNTONIC_COMMA),
            "beat": abs(5 * C4 - 4 * C4 * float(pyth)), "lattice": lattice, "d_a_cents": d_a, "d_a_ratio": frac(T.JUST["A"] / T.JUST["D"]),
            "fifths": [[n, s] for n, s in j.fifths()], "schisma_cents": T.cents(T.SCHISMA),
            "clips": {"thirds": save("syntonic.thirds", seq, level=None, detail="a third made of four fifths, then a pure third"),
                      "diesis": save("syntonic.diesis", diesis, level=None, detail="an octave, then the note three pure thirds up against the same C"),
                      "wolf": save("syntonic.wolf", concat([cg, da], gap=0.4, names=["cg", "da"]), level=None, detail="the fifth C to G, then the fifth D to A, in just intonation")}}


def triad(t: T.Tuning, root: str, seconds: float, octave: int = 4, a4: float | None = None) -> Clip:
    i = T.NAMES.index(root)
    names = [root, T.NAMES[(i + 4) % 12], T.NAMES[(i + 7) % 12]]
    c = C4
    f = [c * 2 ** (t.pc(n) / 1200.0) for n in names]
    for k in (1, 2):                                        # close position, upwards
        while f[k] < f[k - 1]:
            f[k] *= 2
    if f[0] > C4 * 1.6:                                     # keep every chord near middle C
        f = [x / 2 for x in f]
    return organ_chord(f, seconds)


def compute_meantone() -> dict:
    m = T.meantone()
    size = dict(m.fifths())["C"]
    wolf = dict(m.fifths())["G#"]
    thirds = dict(m.thirds())
    good, bad = triad(m, "C", 2.4).at_level(LEVEL), triad(m, "G#", 2.4).at_level(LEVEL)
    seq = concat([good, bad], gap=0.5, names=["A", "B"])
    three = concat([triad(t, "C", 2.4).at_level(LEVEL) for t in (T.pythagorean(), T.equal(12), m)], gap=0.4, names=["pythagorean", "equal", "meantone"])
    third_err = {"pythagorean": dict(T.pythagorean().thirds())["C"] - T.cents(T.PURE_THIRD), "equal": 400.0 - T.cents(T.PURE_THIRD), "meantone": 0.0}
    return {"three_errors": third_err, "fifth_cents": size, "fifth_ratio": 5 ** 0.25, "narrow_by": T.cents(T.PURE_FIFTH) - size, "third_cents": thirds["C"],
            "wolf_cents": wolf, "wolf_wide_by": wolf - T.cents(T.PURE_FIFTH), "bad_third": thirds["B"], "bad_third_wide_by": thirds["B"] - T.cents(T.PURE_THIRD),
            "good_keys": [n for n, s in m.thirds() if abs(s - T.cents(T.PURE_THIRD)) < 1], "bad_keys": [n for n, s in m.thirds() if s > 420],
            "fifth_beat": abs(3 * C4 - 2 * C4 * 2 ** (size / 1200)), "errors": {"C": m.triad_error("C"), "G#": m.triad_error("G#")},
            "cents": list(m.cents), "diesis_cents": T.cents(T.DIESIS),
            "clips": {"keys": save("meantone.keys", seq, level=None, detail="one chord shape in two keys of a meantone keyboard"),
                      "three": save("meantone.three", three, level=None, detail="the chord of C major in Pythagorean tuning, equal temperament and meantone")}}


def compute_well() -> dict:
    systems = {"Pythagorean": T.pythagorean(), "meantone": T.meantone(), "Werckmeister III": T.werckmeister3(), "equal": T.equal(12)}
    table = {name: {"thirds": [[n, s - T.cents(T.PURE_THIRD)] for n, s in t.thirds()], "fifths": [[n, s - T.cents(T.PURE_FIFTH)] for n, s in t.fifths()]}
             for name, t in systems.items()}
    w = T.werckmeister3()
    keys = ["C", "E", "F#"]
    seq = concat([triad(w, k, 2.2).at_level(LEVEL) for k in keys], gap=0.4, names=keys)
    thirds = dict(w.thirds())
    return {"table": table, "keys": keys, "thirds": {k: thirds[k] for k in keys}, "wide": {k: thirds[k] - T.cents(T.PURE_THIRD) for k in keys},
            "narrow_fifths": [n for n, s in w.fifths() if s < 700], "order": [n for n, _ in w.thirds()],
            "clips": {"keys": save("well.keys", seq, level=None, detail="the major chords on C, E and F sharp in Werckmeister's temperament")}}


def compute_equal() -> dict:
    e = T.equal(12)
    root = T.root12_of_2(24)
    table = T.tuner_table(e)
    pure, tempered = organ_chord([C4, C4 * 1.25], 2.6).at_level(LEVEL), organ_chord([C4, C4 * 2 ** (4 / 12)], 2.6).at_level(LEVEL)
    order = ["pure", "equal"]
    seq = concat([pure, tempered], gap=0.5, names=["A", "B"])
    err = T.edo_errors(12)
    worked = next(r for r in table if r["low"] == "A3" and r["high"] == "E4")
    scale_mm = 650.0
    frets = [{"fret": k, "from_nut_mm": scale_mm * (1 - 2 ** (-k / 12))} for k in range(0, 13)]
    return {"roots": {"sqrt2": 2 ** 0.5, "sqrt_sqrt2": 2 ** 0.25, "cbrt": 2 ** (1 / 12)}, "scale_mm": scale_mm, "frets": frets,
            "first_fret_mm": frets[1]["from_nut_mm"], "rule": 1 / (1 - 2 ** (-1 / 12)),
            "root": root, "decimals": 24, "semitone": 2 ** (1 / 12), "fifth_error": err["fifth_error"], "third_error": err["third_error"],
            "third_beat": 5 * C4 - 4 * C4 * 2 ** (4 / 12), "table": table, "worked": worked, "quiz_answer": "A is pure",
            "steps": [{"k": k, "ratio": 2 ** (k / 12), "hz": 440.0 * 2 ** ((k - 9) / 12)} for k in range(13)],
            "clips": {"third": save("equal.third", seq, level=None, detail="a major third, pure and then equal-tempered")}}


def compute_why12() -> dict:
    x = math.log2(1.5)
    cf = T.continued_fraction(x, 8)
    conv = T.convergents(cf)
    ns = np.arange(2, 61)
    fifth = np.array([abs(T.edo_errors(int(n))["fifth_error"]) for n in ns])
    third = np.array([abs(T.edo_errors(int(n))["third_error"]) for n in ns])
    picks = [5, 7, 12, 19, 31, 41, 53]
    rows = [T.edo_errors(n) for n in picks]
    best = [int(n) for k, n in enumerate(ns) if all(fifth[k] < fifth[j] for j in range(k))]       # each better than every smaller division
    chords = []
    for n in (12, 19, 31, 53):
        step = 1200.0 / n
        f = [C4, C4 * 2 ** (T.step_of(n, 1.25) * step / 1200), C4 * 2 ** (T.step_of(n, 1.5) * step / 1200)]
        chords.append(organ_chord(f, 2.0).at_level(LEVEL))
    chords.append(organ_chord([C4, C4 * 1.25, C4 * 1.5], 2.0).at_level(LEVEL))
    seq = concat(chords, gap=0.35, names=["n12", "n19", "n31", "n53", "pure"])
    return {"log": x, "cf": cf, "convergents": [frac(c) for c in conv], "n": ns, "fifth": fifth, "third": third, "rows": rows, "record_fifths": best,
            "clips": {"triads": save("why12.triads", seq, level=None, detail="the major chord in 12, 19, 31 and 53 equal steps, then pure")}}


def compute_piano() -> dict:
    keys = np.arange(1, 89)
    curve = np.array(T.railsback())
    b = np.array([T.piano_b(int(k)) for k in keys])
    # an octave on a very stiff string: exact, and stretched until its partials line up
    stiff = 0.006
    lo = 880.0
    wide = 2 ** ((1200 + T.stretched_octave(stiff)) / 1200)
    exact = Clip(organ_tone(lo, 2.4, b=stiff) + organ_tone(2 * lo, 2.4, b=stiff)).fade(0.03, 0.12).at_level(LEVEL - 1)
    stretched = Clip(organ_tone(lo, 2.4, b=stiff) + organ_tone(wide * lo, 2.4, b=stiff)).fade(0.03, 0.12).at_level(LEVEL - 1)
    f_lo = [T.stiff_partial(lo, n, stiff) for n in range(1, 5)]
    return {"keys": keys, "curve": curve, "b": b, "top": float(curve[-1]), "bottom": float(curve[0]), "stiff": stiff, "lo": lo,
            "stretch_cents": T.stretched_octave(stiff), "partials": f_lo, "beat_exact": abs(f_lo[1] - 2 * lo), "b_a4": T.piano_b(49), "b_c8": T.piano_b(88),
            "clips": {"octave": save("piano.octave", concat([exact, stretched], gap=0.5, names=["exact", "stretched"]), level=None,
                                     detail="an octave on stiff strings: exactly 2 to 1, then stretched")}}


# the Tune's harmony: one chord to each note, by degree
HARMONY = {1: "C", 5: "C", 6: "F", 4: "F", 3: "C", 2: "G"}
DEGREE_NOTE = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "A"}


def compute_tune() -> dict:
    versions = [("Pythagorean", T.pythagorean(), 0), ("meantone, in C", T.meantone(), 0), ("meantone, in A flat: the wolf", T.meantone(), 8),
                ("Werckmeister III", T.werckmeister3(), 0), ("12 equal", T.equal(12), 0), ("19 equal", T.equal_just(19), 0), ("31 equal", T.equal_just(31), 0),
                ("53 equal", T.equal_just(53), 0)]
    phrases = [0, 1, 2, 3, 4, 5, 4, 5]                      # A A' B B A A', and A A' once more
    beat = 0.55
    placed, notes, events, rows = [], [], {}, []
    t0 = 0.0
    for v, ((name, tun, shift), ph) in enumerate(zip(versions, phrases)):
        events[f"v{v}"] = t0
        ev = TUNE.events(beat, [ph])

        def hz(note: str, octave_up: int = 0) -> float:
            i = (T.NAMES.index(note) + shift) % 12
            base = C4 * 2 ** (tun.cents[shift] / 1200.0) if shift else C4
            rel = (tun.cents[i] - tun.cents[shift]) % 1200.0
            return base * 2 ** (rel / 1200.0) * 2 ** octave_up

        errs, rough = [], []
        for e in ev:
            mel = hz(DEGREE_NOTE[e["degree"]], 1)          # the melody an octave above the chords
            root = HARMONY[e["degree"]]
            i = T.NAMES.index(root)
            ch = [hz(root), hz(T.NAMES[(i + 4) % 12]), hz(T.NAMES[(i + 7) % 12])]
            for k in (1, 2):
                while ch[k] < ch[k - 1]:
                    ch[k] *= 2
            if ch[0] > hz("C") * 1.45:
                ch = [x / 2 for x in ch]
            dur = e["dur"]
            y = organ_tone(mel, dur + 0.12, decay=1.2) * 1.0 + sum(organ_tone(f, dur + 0.12, decay=0.5) for f in ch) * 0.55
            placed.append((Clip(y).fade(0.006, 0.1), t0 + e["t"]))
            k = len(notes)
            events[f"n{k}"] = t0 + e["t"]
            notes.append({"t": t0 + e["t"], "dur": dur, "hz": mel, "name": e["name"], "degree": e["degree"], "version": v, "chord": root})
            third = 1200 * math.log2(ch[1] / ch[0]) % 1200
            fifth = 1200 * math.log2(ch[2] / ch[0]) % 1200
            errs.append(math.sqrt(((third - T.cents(T.PURE_THIRD)) ** 2 + (fifth - T.cents(T.PURE_FIFTH)) ** 2) / 2))
            rough.append(K.chord_roughness([1.0, ch[1] / ch[0], ch[2] / ch[0]], ch[0]))
        rows.append({"name": name, "phrase": ph, "error": float(np.mean(errs)), "worst": float(np.max(errs)), "rough": float(np.mean(rough))})
        t0 += sum(e["dur"] for e in ev) + 0.35
    events["end"] = t0 - 0.35
    c = mix(placed, duration=max(t0 - 0.35 + 0.4, max(start + cl.duration for cl, start in placed)))
    c = Clip(c.y, SR, events, notes)
    return {"clip": save("tune.variation6", c, detail="the Tune with chords, in eight tunings"), "notes": notes, "rows": rows, "seconds": c.duration,
            "best": min(rows, key=lambda r: r["error"])["name"], "worst": max(rows, key=lambda r: r["error"])["name"],
            "range": [min(r["error"] for r in rows), max(r["error"] for r in rows)]}


def compute_variation() -> dict:
    t = load("tune")
    lo, hi = t["range"]
    return {"part": 6, "title": r"with chords, in eight tunings: Pythagorean, meantone and its wolf, Werckmeister, 12, 19, 31 and 53", "seconds": t["seconds"],
            "measure": rf"its chords are from {lo:.0f} to {hi:.0f} cents out of tune", "clip": "tune.variation6"}


def compute_nextpart() -> dict:
    c = string_note(0.5, 2.6)
    return {"clips": {"pluck": save("next.pluck", c, kind="physical model", detail="Part 1's string, plucked")}}


ITEMS = {"pump": compute_pump, "circle": compute_circle, "syntonic": compute_syntonic, "meantone": compute_meantone, "well": compute_well,
         "equal": compute_equal, "why12": compute_why12, "piano": compute_piano, "tune": compute_tune, "variation": compute_variation,
         "nextpart": compute_nextpart}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
