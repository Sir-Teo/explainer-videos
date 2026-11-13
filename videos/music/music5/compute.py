"""Precompute everything numerical, and every sound, in Part 5 of *Music, Built* ("Consonance").

    python -m videos.music.music5.compute              # everything missing (under a minute)
    python -m videos.music.music5.compute --force curve

Numbers are cached in ``.cache/music5/<name>.json`` (+ ``.npz``), sounds in ``.cache/music5/audio/``.  The theories
of consonance are Monochord's (``explainer/music/monochord/consonance.py``); published results are cited in the
README.

Items:
    bent        the cold open: a timbre for which a true octave is rough and a wide one smooth
    number      Pythagoras and Euler: thirteen just intervals ranked by their ratios; a fifth mistuned by five cents
    pulses      Galileo: two trains of pulses, three against two, speeding up until they are a fifth
    beats       two pure tones 1, 4 and 12 Hz apart; a string being tuned to another
    plomp       two pure tones gliding apart; Plomp and Levelt's curve; a pure fifth and a pure tritone
    curve       the roughness of two harmonic tones against their interval; its minima; a glide through an octave
    worked      which partials of a fifth and of a tritone meet, and which nearly meet
    stretched   the same curve for a tone with stretched partials; four sounds
    fusion      the pitch a chord fuses into: Part 4's model on fifths, fourths, thirds and a major triad
    triads      major, minor, diminished and augmented: roughness and fundamental bass; a map of all triads
    culture     the major third of the Middle Ages (81:64) against the pure one (5:4)
    tune        Variation 5: the Tune in a bent timbre, in parallel intervals that only that timbre makes smooth
    variation   the Variations ledger, row 5
    nextpart    twelve pure fifths against seven octaves
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import consonance as K
from explainer.music.monochord import ear
from explainer.music.monochord.partkit import play_tune, saver, string_note
from explainer.music.monochord.pitch import cents

CACHE = Cache("music5")
CLIPS = ClipStore("music5")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
C4 = 261.6255653005986
N, ROLL = 7, 0.88            # the tone of this part: seven partials, each 0.88 of the one below


def sines(freqs, amps, seconds: float, decay: float = 0.0) -> np.ndarray:
    """Partials added up; ``decay`` makes each die away (faster the higher it is), as on a struck or plucked thing."""
    t = np.arange(int(seconds * SR)) / SR
    y = np.zeros(len(t))
    for k, (f, a) in enumerate(zip(freqs, amps)):
        if f < 0.45 * SR:
            y += a * np.sin(2 * np.pi * f * t) * (np.exp(-decay * (1 + 0.35 * k) * t) if decay else 1.0)
    return y


def tone(f0: float, seconds: float, stretch: float = 2.0, decay: float = 0.0) -> np.ndarray:
    f, a = K.harmonic_partials(f0, N, ROLL, stretch)
    return sines(f, a, seconds, decay)


def chord(ratios, seconds: float, f0: float = C4, stretch: float = 2.0, decay: float = 0.0) -> Clip:
    return Clip(sum(tone(f0 * r, seconds, stretch, decay) for r in ratios)).fade(0.03, 0.12)


def pure(freqs, seconds: float) -> Clip:
    return Clip(sines(freqs, [1.0] * len(freqs), seconds)).fade(0.03, 0.1)


def glide(lo: float, r0: float, r1: float, seconds: float, partials: int = N, stretch: float = 2.0):
    """A fixed tone and one that slides from ratio r0 to r1 above it (evenly in pitch); ``(samples, ratio at each sample)``."""
    t = np.arange(int(seconds * SR)) / SR
    ratio = r0 * (r1 / r0) ** (t / seconds)
    k = np.arange(1, partials + 1)
    mult, amp = k ** math.log2(stretch), ROLL ** (k - 1.0)
    y = np.zeros(len(t))
    phase = 2 * np.pi * np.cumsum(lo * ratio) / SR
    for m, a in zip(mult, amp):
        y += a * np.sin(2 * np.pi * lo * m * t) + a * np.sin(m * phase)
    return y, ratio


# ---------------------------------------------------------------------------
def compute_bent() -> dict:
    wide = 2.1
    a, b = chord((1, 2.0), 2.2, stretch=wide), chord((1, wide), 2.2, stretch=wide)
    seq = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=0.5, names=["A", "B"])
    return {"wide": wide, "cents_wide": cents(wide / 2.0), "rough_true": K.dyad_roughness(2.0, stretch=wide),
            "rough_wide": K.dyad_roughness(wide, stretch=wide),
            "clips": {"pair": save("bent.pair", seq, level=None, detail="two notes together, twice: an exact octave, then one 84 cents wide")}}


def compute_number() -> dict:
    rows = []
    for name, (p, q) in K.JUST.items():
        rows.append({"name": name, "p": p, "q": q, "cents": cents(p / q), "gradus": K.euler_gradus(p, q),
                     "together": [K.coincidence(p, q).numerator, K.coincidence(p, q).denominator],
                     "repeat": q, "tenney": K.tenney(p, q)})
    # a fifth five cents wide: to the ear a fifth; to arithmetic, a monster
    wide = 1.5 * 2 ** (5 / 1200)
    fr = Fraction(wide).limit_denominator(400)
    lo = C4
    beat = abs(3 * lo - 2 * lo * wide)
    seq = concat([chord((1, 1.5), 2.6).at_level(LEVEL), chord((1, wide), 2.6).at_level(LEVEL)], gap=0.5, names=["pure", "wide"])
    return {"rows": rows, "wide_ratio": [fr.numerator, fr.denominator], "wide_gradus": K.euler_gradus(fr.numerator, fr.denominator),
            "wide_cents": 5.0, "wide_beat": beat, "pure_gradus": K.euler_gradus(3, 2),
            "tradition": {"perfect": ["unison", "octave", "fifth", "fourth"], "imperfect": ["major third", "minor third", "major sixth", "minor sixth"],
                          "dissonant": ["major second", "minor second", "minor seventh", "major seventh", "tritone"]},
            "clips": {"fifths": save("number.fifths", seq, level=None, detail="a fifth of exactly 3 to 2, then one five cents wide")}}


def compute_pulses() -> dict:
    secs, hold = 9.0, 2.0
    t = np.arange(int((secs + hold) * SR)) / SR
    grow = np.minimum(t / secs, 1.0)
    y = np.zeros(len(t))
    marks = {}
    for name, rate0 in (("three", 3.0), ("two", 2.0)):
        rate = rate0 * 100.0 ** grow                       # from 3 and 2 a second to 300 and 200
        phase = np.cumsum(rate) / SR
        ticks = np.flatnonzero(np.diff(np.floor(phase)) > 0)
        marks[name] = ticks / SR
        pulse = np.hanning(int(0.0006 * SR))
        for i in ticks:
            y[i:i + len(pulse)] += pulse[: len(y) - i]
    c = Clip(y).fade(0.001, 0.1)
    c.events.update({"slow": 0.0, "fast": secs})
    pattern = {f"{p}:{q}": {"a": [k / p for k in range(p + 1)], "b": [k / q for k in range(q + 1)]} for p, q in ((2, 1), (3, 2), (45, 32))}
    return {"seconds": secs, "hold": hold, "three_t": marks["three"][marks["three"] < 6.5], "two_t": marks["two"][marks["two"] < 6.5],
            "pattern_3_2": pattern["3:2"], "end_hz": [300.0, 200.0],
            "clips": {"speedup": save("pulses.speedup", c, level=LEVEL - 2, detail="clicks: three against two, a hundred times faster by the end")}}


def compute_beats() -> dict:
    f = 440.0
    gaps = [1.0, 4.0, 12.0]
    parts = [pure([f, f + g], 3.0) for g in gaps]
    seq = concat([p.at_level(LEVEL) for p in parts], gap=0.4, names=[f"b{int(g)}" for g in gaps])
    # a second tone brought into tune with the first: 226 Hz sliding to 220 in six seconds, then two seconds in tune
    secs, hold = 6.0, 2.0
    t = np.arange(int((secs + hold) * SR)) / SR
    f2 = np.where(t < secs, 226.0 - 6.0 * t / secs, 220.0)
    y = tone(220.0, secs + hold) + sum(ROLL ** (k - 1.0) * np.sin(2 * np.pi * k * np.cumsum(f2) / SR) for k in range(1, N + 1))
    tune_clip = Clip(y).fade(0.03, 0.2)
    tune_clip.events.update({"start": 0.0, "in_tune": secs})
    return {"f": f, "gaps": gaps, "worked": {"a": 220.0, "b": 222.0, "beats": 2.0}, "tune_from": 226.0, "tune_to": 220.0, "tune_seconds": secs,
            "clips": {"three": save("beats.three", seq, level=None, detail="pairs of pure tones 1, 4 and 12 Hz apart"),
                      "tuning": save("beats.tuning", tune_clip, detail="one tone slid down until it matches another")}}


def compute_plomp() -> dict:
    lo = 500.0
    x = np.linspace(0, 6, 601)
    secs = 12.0
    y, ratio = glide(lo, 1.0, 2.0, secs, partials=1)
    rough = K.pair_roughness(lo, lo * ratio)
    c = Clip(y).fade(0.03, 0.15)
    worst = K.worst_separation(lo)
    semis = 12 * np.log2(ratio)
    fifth, tritone = (lo, 1.5 * lo), (lo, lo * 45 / 32)
    seq = concat([pure(fifth, 2.2).at_level(LEVEL - 1), pure(tritone, 2.2).at_level(LEVEL - 1)], gap=0.5, names=["A", "B"])
    return {"lo": lo, "x": x, "curve": K.pl_curve(x), "seconds": secs, "semis": semis[::480], "rough": (rough / rough.max())[::480],
            "worst_hz": worst, "worst_semitones": 12 * math.log2((lo + worst) / lo), "worst_time": float(secs * math.log2((lo + worst) / lo)),
            "band_hz": float(ear.erb(lo)), "worst_over_band": worst / float(ear.erb(lo)),
            "pure_fifth": float(K.pair_roughness(*fifth)), "pure_tritone": float(K.pair_roughness(*tritone)),
            "peak": float(rough.max()), "quiz_answer": "A",
            "clips": {"glide": save("plomp.glide", c, level=LEVEL - 1, detail="two pure tones: one stays at 500 Hz, the other climbs an octave"),
                      "pure": save("plomp.pure", seq, level=None, detail="two pairs of pure tones: a fifth and a tritone")}}


def compute_curve() -> dict:
    r = np.linspace(1.0, 2.3, 2601)
    c = K.dissonance_curve(r, C4, N, ROLL)
    found = K.minima(r, c, depth=0.01)
    names = {v: k for k, v in K.JUST.items()}
    rows = []
    for m in found:
        p, q = K.nearest_ratio(m, 9)
        rows.append({"ratio": m, "p": p, "q": q, "off_cents": cents(m / (p / q)), "name": names.get((p, q), ""),
                     "rough": float(np.interp(m, r, c))})
    secs = 18.0
    y, ratio = glide(C4, 1.0, 2.06, secs)
    rough_t = np.interp(ratio[::480], r, c)
    clip = Clip(y).fade(0.03, 0.2)
    return {"r": r[::4], "curve": c[::4], "max": float(c.max()), "minima": rows, "seconds": secs, "ratio_t": ratio[::480], "rough_t": rough_t,
            "partials": N, "rolloff": ROLL,
            "clips": {"glide": save("curve.glide", clip, detail="two tones of seven partials: one stays on C, the other climbs an octave")}}


def compute_worked() -> dict:
    out = {}
    for name, ratio in (("fifth", 1.5), ("tritone", 45 / 32)):
        lo = [C4 * k for k in range(1, N + 1)]
        up = [C4 * ratio * k for k in range(1, N + 1)]
        pairs = []
        for i, a in enumerate(lo, 1):
            for j, b in enumerate(up, 1):
                d = abs(a - b)
                band = float(ear.erb(min(a, b)))
                if d < band:
                    pairs.append({"lower": i, "upper": j, "hz": [a, b], "apart": d, "band": band,
                                  "rough": float(K.pair_roughness(a, b, ROLL ** (i - 1), ROLL ** (j - 1)))})
        out[name] = {"ratio": ratio, "pairs": sorted(pairs, key=lambda p: -p["rough"]), "meet": [p for p in pairs if p["apart"] < 0.01],
                     "total": K.dyad_roughness(ratio, C4, N, ROLL)}
    return out


def compute_stretched() -> dict:
    wide = load("bent")["wide"]
    r = np.linspace(1.0, 2.3, 2601)
    c = K.dissonance_curve(r, C4, N, ROLL, stretch=wide)
    found = K.minima(r, c, depth=0.01)
    plain = K.minima(r, K.dissonance_curve(r, C4, N, ROLL), depth=0.01)
    table = [{"plain": a, "bent": b, "predicted": a ** math.log2(wide)} for a, b in zip(plain, found)]
    f, _ = K.harmonic_partials(100.0, N, ROLL, wide)
    four = [chord((1, 2.0), 2.0), chord((1, wide), 2.0), chord((1, 2.0), 2.0, stretch=wide), chord((1, wide), 2.0, stretch=wide)]
    seq = concat([x.at_level(LEVEL) for x in four], gap=0.45, names=["plain_true", "plain_wide", "bent_true", "bent_wide"])
    grid = {"plain_true": K.dyad_roughness(2.0), "plain_wide": K.dyad_roughness(wide), "bent_true": K.dyad_roughness(2.0, stretch=wide),
            "bent_wide": K.dyad_roughness(wide, stretch=wide)}
    return {"wide": wide, "r": r[::4], "curve": c[::4], "minima": found, "table": table, "partials_of_100": f, "grid": grid,
            "worst_gap": max(abs(row["bent"] - row["predicted"]) for row in table),
            "clips": {"four": save("stretched.four", seq, level=None, detail="an octave and a wide octave, in an ordinary tone and in a bent one")}}


def compute_fusion() -> dict:
    rows = []
    for name, ratios, pq in (("octave", (1, 2.0), [(1, 1), (2, 1)]), ("fifth", (1, 1.5), [(1, 1), (3, 2)]), ("fourth", (1, 4 / 3), [(1, 1), (4, 3)]),
                             ("major third", (1, 5 / 4), [(1, 1), (5, 4)]), ("major triad", (1, 5 / 4, 3 / 2), [(1, 1), (5, 4), (3, 2)])):
        hz, strength = K.harmonicity(ratios, C4)
        bass = K.fundamental_bass(pq)
        rows.append({"name": name, "model_hz": hz, "strength": strength, "bass": [bass.numerator, bass.denominator], "bass_hz": C4 * float(bass),
                     "off_cents": cents(hz / (C4 * float(bass)))})
    # three pure tones, 4 : 5 : 6 of middle C, and the note they imply
    high = [4 * C4, 5 * C4, 6 * C4]
    t = np.arange(int(0.4 * SR)) / SR
    implied, sal = ear.pitch(sum(np.sin(2 * np.pi * f * t) for f in high), SR, lo=100, hi=700)
    seq = concat([pure(high, 2.4).at_level(LEVEL - 1), pure([C4], 1.6).at_level(LEVEL - 4), pure(high, 2.4).at_level(LEVEL - 1)],
                 gap=0.4, names=["chord", "bass", "again"])
    # a minor second in both ears together, then one tone in each ear
    a, b = 440.0, 440.0 * 16 / 15
    both = pure([a, b], 2.4).at_level(LEVEL - 1)
    g = float(np.abs(both.mono).max()) / 2.0
    split = mix([(Clip(sines([a], [g], 2.4)).fade(0.03, 0.1), 0.0, 0.0, -1.0), (Clip(sines([b], [g], 2.4)).fade(0.03, 0.1), 0.0, 0.0, 1.0)])
    ears = concat([Clip(both.stereo), split], gap=0.5, names=["together", "apart"])
    return {"rows": rows, "high": high, "implied_hz": implied, "implied_cents": cents(implied / C4), "implied_salience": sal,
            "second": [a, b], "second_beat": b - a,
            "clips": {"bass": save("fusion.bass", seq, level=None, detail="three high pure tones; a low one; the three again"),
                      "ears": save("fusion.ears", ears, level=None, needs="headphones: the second sound puts one tone in each ear",
                                   detail="a minor second in both ears, then one tone in each ear")}}


def compute_triads() -> dict:
    kinds = [("major", [(1, 1), (5, 4), (3, 2)]), ("minor", [(1, 1), (6, 5), (3, 2)]), ("diminished", [(1, 1), (6, 5), (36, 25)]),
             ("augmented", [(1, 1), (5, 4), (25, 16)])]
    rows = []
    for name, pq in kinds:
        ratios = [p / q for p, q in pq]
        bass = K.fundamental_bass(pq)
        den = math.lcm(*[q for _, q in pq])
        whole = [int(Fraction(p, q) * den) for p, q in pq]
        g = math.gcd(*whole)
        rows.append({"name": name, "pq": pq, "as_integers": [w // g for w in whole], "rough": K.chord_roughness(ratios, C4, N, ROLL),
                     "bass": [bass.numerator, bass.denominator], "repeat": bass.denominator // bass.numerator if bass.numerator == 1 else float(1 / bass),
                     "octaves_below": -math.log2(float(bass))})
    # every chord of three notes within a fifth and a bit: the lower interval and the upper one, in semitones
    steps = np.arange(0.5, 6.01, 0.1)
    grid = np.array([[K.chord_roughness((1, 2 ** (a / 12), 2 ** ((a + b) / 12)), C4, N, ROLL) for a in steps] for b in steps])
    # the valleys of that map, and the chords that sit in them
    known = {(4, 3): "major", (3, 4): "minor", (5, 4): "major, on its fifth", (3, 5): "major, on its third", (4, 5): "minor, on its third",
             (5, 3): "minor, on its fifth"}
    valleys = []
    for i in range(1, len(steps) - 1):
        for j in range(1, len(steps) - 1):
            v = grid[i, j]
            if v == grid[i - 1:i + 2, j - 1:j + 2].min():
                a, b = float(steps[j]), float(steps[i])
                valleys.append({"lower": a, "upper": b, "rough": float(v), "name": known.get((round(a), round(b)), "")})
    valleys.sort(key=lambda r: r["rough"])
    seen, unique = set(), []
    for v in valleys:                                       # one valley for each pair of whole semitones
        key = (round(v["lower"]), round(v["upper"]))
        if key not in seen:
            seen.add(key)
            unique.append(v)
    valleys = unique
    seq = concat([chord([p / q for p, q in pq], 1.8).at_level(LEVEL) for _, pq in kinds], gap=0.4, names=[k for k, _ in kinds])
    pair = concat([chord([p / q for p, q in pq], 2.2).at_level(LEVEL) for _, pq in kinds[:2]], gap=0.5, names=["A", "B"])
    return {"rows": rows, "steps": steps, "grid": grid, "valleys": valleys, "same_roughness": abs(rows[0]["rough"] / rows[1]["rough"] - 1),
            "clips": {"four": save("triads.four", seq, level=None, detail="four chords of three notes: major, minor, diminished, augmented"),
                      "pair": save("triads.pair", pair, level=None, detail="two chords built from the same three intervals")}}


def compute_culture() -> dict:
    thirds = {"pythagorean": Fraction(81, 64), "just": Fraction(5, 4)}
    rows = {k: {"p": v.numerator, "q": v.denominator, "cents": cents(float(v)), "rough": K.dyad_roughness(float(v), C4, N, ROLL),
                "beat": abs(5 * C4 - 4 * C4 * float(v))} for k, v in thirds.items()}
    seq = concat([chord((1, float(thirds["pythagorean"])), 2.4).at_level(LEVEL), chord((1, float(thirds["just"])), 2.4).at_level(LEVEL)],
                 gap=0.5, names=["pythagorean", "just"])
    return {"rows": rows, "times": rows["pythagorean"]["rough"] / rows["just"]["rough"],
            "clips": {"thirds": save("culture.thirds", seq, level=None, detail="a major third of 81 to 64, then one of 5 to 4")}}


def compute_tune() -> dict:
    wide = load("bent")["wide"]
    bend = math.log2(wide)
    fifth = 1.5 ** bend                                    # the bent timbre's own 'fifth'

    def voice(hz, dur, e):
        hz = C4 * (hz / C4) ** bend                        # the scale is stretched with the timbre
        stretch = 2.0 if e["phrase"] == 4 else wide       # phrase 5: the same notes, with ordinary partials
        notes = [hz] if e["phrase"] < 2 else [hz, hz * fifth]
        y = sum(tone(f, dur + 0.25, stretch, decay=1.6) for f in notes)
        return Clip(y).fade(0.004, 0.08).at_level(LEVEL - (0.0 if len(notes) == 1 else 1.0))

    c = play_tune(voice, tonic=C4, tail=0.9)
    rough = {"bent": [], "plain": []}
    notes = []
    for n in c.notes:
        hz = C4 * (n["hz"] / C4) ** bend
        kind = "alone" if n["phrase"] < 2 else ("plain" if n["phrase"] == 4 else "bent")
        notes.append({**n, "hz": hz, "kind": kind})
        if n["phrase"] >= 2:
            rough["bent"].append(K.dyad_roughness(fifth, hz, N, ROLL, stretch=wide))
            rough["plain"].append(K.dyad_roughness(fifth, hz, N, ROLL, stretch=2.0))
    c = Clip(c.y, SR, c.events, notes)
    return {"clip": save("tune.variation5", c, detail="a tone with stretched partials; phrase 5 has ordinary ones"), "notes": notes, "seconds": c.duration,
            "fifth": fifth, "fifth_cents": cents(fifth), "rough_bent": float(np.mean(rough["bent"])), "rough_plain": float(np.mean(rough["plain"])),
            "times": float(np.mean(rough["plain"]) / np.mean(rough["bent"]))}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 5, "title": r"in a bent timbre, in parallel `fifths' that only that timbre makes smooth", "seconds": t["seconds"],
            "measure": rf"the same intervals are {t['times']:.0f} times rougher with ordinary partials", "clip": "tune.variation5"}


def compute_nextpart() -> dict:
    comma = Fraction(3 ** 12, 2 ** 19)
    a, b = C4, C4 * float(comma)
    one, two = chord((1,), 1.6, f0=a), chord((1,), 1.6, f0=b)
    both = Clip(tone(a, 3.2) + tone(b, 3.2)).fade(0.03, 0.15)
    seq = concat([one.at_level(LEVEL - 1), two.at_level(LEVEL - 1), both.at_level(LEVEL)], gap=0.35, names=["c", "c_again", "both"])
    return {"comma": [comma.numerator, comma.denominator], "cents": cents(float(comma)), "beat": b - a,
            "clips": {"comma": save("next.comma", seq, level=None, detail="C; the C reached by twelve pure fifths; both together")}}


ITEMS = {"bent": compute_bent, "number": compute_number, "pulses": compute_pulses, "beats": compute_beats, "plomp": compute_plomp,
         "curve": compute_curve, "worked": compute_worked, "stretched": compute_stretched, "fusion": compute_fusion, "triads": compute_triads,
         "culture": compute_culture, "tune": compute_tune, "variation": compute_variation, "nextpart": compute_nextpart}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
