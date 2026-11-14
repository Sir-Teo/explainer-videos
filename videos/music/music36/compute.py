"""Precompute everything numerical, and every sound, in Part 36 of *Music, Built* ("Bronze and Silk").

    python -m videos.music.music36.compute              # everything missing (under a minute)
    python -m videos.music.music36.compute --force ombak

Numbers are cached in ``.cache/music36/<name>.json``, sounds in ``.cache/music36/audio/``.  The models are Monochord's
(``explainer/music/monochord/bronze.py``): a two-tone bell by modal synthesis with designed mode families, Part 9's
bar, gong and membrane, and a plucked string (Part 35's retuned Karplus–Strong) for the qin.  Every melody is ours, and
the gamelan tunings are illustrative: no two gamelans are tuned alike.

Items:
    hook        two-tone bells: three bells, each struck at the centre and then the side (an ear question: same note?)
    lu          the twelve lü by alternately removing and adding a third; the first five, heard
    jingfang    how close n fifths come to whole octaves; the 53rd, heard against the start
    modes       the five pentatonic modes, heard
    qin         harmonics of one string at the qin's hui, heard
    hetero      the Tune's first phrase in heterophony: plain, ornamented and sustained at once
    spectra     dissonance curves for harmonic and bar spectra; an illustrative slendro on both tones, heard
    scales      illustrative slendro and pelog on a metallophone
    ombak       one note on two metallophones tuned together and tuned to beat (an ear question: which shimmers?)
    cycle       a lancaran cycle: balungan on saron, with ketuk, kenong, kempul and gong
    kotekan     a figuration split between two players: each alone, then together (an ear question: one player or two?)
    thirds      a minor-third bell and a major-third bell, centre then side, heard
    bellsong    a pentatonic melody of ours on a set of two-tone bells, struck centre and side
    twelve      the twelve lü as a chromatic scale
    zhu         a pentatonic phrase in Pythagorean tuning and in Zhu Zaiyu's equal temperament
    melody      a pentatonic melody of ours, then with the two bian tones
    openqin     the qin's seven open strings in a common tuning
    sho         a sustained cluster in the manner of the sho (ours), additive
    patet       two pelog subsets: degrees 1 2 3 5 6 and 2 3 5 6 7
    rates       one pair tuned to beat 3, then 8 times a second
    irama       one balungan line with elaboration at two and at four notes per beat
    two_scales  the Tune's first phrase on a metallophone in an illustrative slendro and pelog
    kebyar      an interlocking burst in the manner of gong kebyar: fast, loud, stopped dead
    stopped     one pitch on the qin as an open string, a stopped note and a harmonic
    tune        Variation 36: the Tune in qin harmonics, then as balungan with interlocking elaboration
    variation   the Variations ledger, row 36
"""

from __future__ import annotations

from fractions import Fraction
from math import log2

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import bronze as B
from explainer.music.monochord import maqam as Q
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.partkit import saver

CACHE = Cache("music36")
CLIPS = ClipStore("music36")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
C4 = 261.6255653005986
_C: dict = {}


def arr(y):
    return Clip(np.asarray(y, float), SR)


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def saron(f, seconds=1.6):
    return cached(("saron", round(f, 3), seconds), lambda: B.metallophone(f, seconds))


def pluck(f, seconds=1.2):
    return cached(("pluck", round(f, 3), seconds), lambda: Q.oud(f, seconds))


def gong(f, seconds=3.0, glide=0.05):
    return cached(("gong", round(f, 3), seconds), lambda: PC.gong(f, seconds=seconds, glide=glide))


def harmonic_tone(f, seconds=1.4, n=6):
    t = np.arange(int(seconds * SR)) / SR
    y = sum((0.75 ** k) * np.sin(2 * np.pi * f * (k + 1) * t) * np.exp(-(1.0 + 0.8 * k) * t) for k in range(n))
    return y * np.clip(t / 0.003, 0, 1)


def at_cents(base, c):
    return base * 2 ** (c / 1200)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    bells = [C4 * 0.75, C4, C4 * 1.25]
    parts, t, times = [], 0.0, []
    for f in bells:
        for at in ("a", "b"):
            parts.append((arr(cached(("bell", round(f, 2), at), lambda f=f, at=at: B.two_tone_bell(f, at))), t, 0.0))
            times.append(t)
            t += 1.6
        t += 0.6
    s_ = concat([Clip(mix(parts, duration=t + 2.0).y, SR).at_level(LEVEL)], gap=0.0, names=["bells"])
    return {"bells": bells, "times": times, "third_cents": 300.0, "answer": "different",
            "clips": {"bells": save("hook.bells", s_, detail="three two-tone bells, each struck at the centre and then at the side, a minor third higher; modal synthesis with two designed mode families")}}


def compute_lu() -> dict:
    lu = B.sanfen_lu(12)
    first5 = sorted(x["cents"] for x in lu[:5])
    parts, t = [], 0.0
    for c in first5 + [1200.0]:
        parts.append((arr(pluck(at_cents(C4, c), 1.0)), t, 0.0))
        t += 0.45
    s_ = concat([Clip(mix(parts, duration=t + 1.2).y, SR).at_level(LEVEL)], gap=0.0, names=["five"])
    twelve = sorted(x["cents"] for x in lu)
    return {"lu": [{"k": x["k"], "length": str(x["length"]), "cents": x["cents"]} for x in lu], "first5": first5, "twelve": twelve,
            "comma": 12 * 1200 * log2(1.5) - 7 * 1200, "unit": 0.45,
            "clips": {"five": save("lu.five", s_, detail="the first five pitches of the three-part loss and gain rule, folded into one octave and played in order: the pentatonic C D E G A and C; a plucked-string model")}}


def compute_jingfang() -> dict:
    fc = B.fifths_closeness(60)
    best = sorted(fc, key=lambda r: abs(r["gap"]))[:5]
    f = C4
    parts = [(arr(harmonic_tone(f, 4.0)), 0.0, 0.0), (arr(harmonic_tone(at_cents(f, fc[52]["gap"]), 4.0)), 0.0, 0.0)]
    c1 = Clip(mix(parts, duration=4.5).y, SR).at_level(LEVEL)
    parts2 = [(arr(harmonic_tone(f, 4.0)), 0.0, 0.0), (arr(harmonic_tone(at_cents(f, fc[11]["gap"]), 4.0)), 0.0, 0.0)]
    c2 = Clip(mix(parts2, duration=4.5).y, SR).at_level(LEVEL)
    s_ = concat([c2, c1], gap=0.8, names=["12", "53"])
    return {"gaps": [r["gap"] for r in fc], "best": best, "beat12": float(C4 * (2 ** (fc[11]["gap"] / 1200) - 1)), "beat53": float(C4 * (2 ** (fc[52]["gap"] / 1200) - 1)),
            "starts": {k: float(s_.events[k]) for k in ("12", "53")},
            "clips": {"two": save_synth("jingfang.two", s_, detail="C4 sounded with the note reached by 12 pure fifths (23.5 cents sharp), then with the note reached by 53 (3.6 cents sharp): fast and slow beating; additive tones")}}


def compute_modes() -> dict:
    md = B.modes()
    clips = []
    order = ["gong", "shang", "jue", "zhi", "yu"]
    for k in order:
        parts, t = [], 0.0
        for c in md[k] + [1200]:
            parts.append((arr(pluck(at_cents(C4, c), 0.9)), t, 0.0))
            t += 0.32
        clips.append(Clip(mix(parts, duration=t + 0.8).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.5, names=order)
    return {"modes": md, "order": order, "starts": {k: float(s_.events[k]) for k in order}, "unit": 0.32,
            "clips": {"five": save("modes.five", s_, detail="the five pentatonic modes, gong, shang, jue, zhi and yu, each from C; a plucked-string model")}}


def compute_qin() -> dict:
    f = C4 / 2
    seq = [Fraction(1)] + [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(1, 6), Fraction(1, 8)]
    parts, t, rows_ = [], 0.0, []
    for h in seq:
        n = h.denominator if h != 1 else 1
        y = pluck(f * n, 1.4) * (1.0 if n == 1 else 0.8)
        parts.append((arr(y), t, 0.0))
        rows_.append({"hui": str(h), "partial": n, "cents": 1200 * log2(n)})
        t += 1.1
    s_ = concat([Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL)], gap=0.0, names=["harmonics"])
    return {"rows": rows_, "f": f, "step": 1.1, "hui": [str(h) for h in B.HUI], "hui_partials": [h.denominator for h in B.HUI],
            "clips": {"harmonics": save("qin.harmonics", s_, detail="a string at C3, open, then its harmonics touched at a half, a third, a quarter, a fifth, a sixth and an eighth of its length; a plucked-string model at each harmonic's pitch")}}


def tune_line(n=14, base=0):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def compute_hetero() -> dict:
    mel = tune_line(7)
    unit = 0.5
    parts = []
    plain = [(p, a, d) for p, a, d in mel]
    orn = []
    for p, a, d in mel:
        orn += [(p, a, d * 0.5), (p + 2 if p < 9 else p - 2, a + d * 0.5, d * 0.25), (p, a + d * 0.75, d * 0.25)]
    sus = [(mel[0][0], 0.0, 4.0), (mel[4][0], 4.0, mel[-1][1] + mel[-1][2] - 4.0)]
    for p, a, d in plain:
        parts.append((arr(pluck(C4 * 2 ** (p / 12), d * unit + 0.3)), a * unit, 0.0))
    for p, a, d in orn:
        parts.append((arr(saron(C4 * 2 * 2 ** (p / 12), d * unit + 0.6)), a * unit, -4.0))
    for p, a, d in sus:
        parts.append((arr(harmonic_tone(C4 / 2 * 2 ** (p / 12), d * unit + 0.4)), a * unit, -6.0))
    total = (mel[-1][1] + mel[-1][2]) * unit + 1.2
    s_ = concat([Clip(mix(parts, duration=total).y, SR).at_level(LEVEL)], gap=0.0, names=["hetero"])
    return {"plain": [list(x) for x in plain], "ornamented": [list(x) for x in orn], "sustained": [list(x) for x in sus], "unit": unit,
            "clips": {"three": save("hetero.three", s_, detail="the Tune's first phrase in heterophony: plain on a plucked string, ornamented on a metallophone an octave up, and in long notes below; physical models")}}


def compute_spectra() -> dict:
    cs, dh = B.dissonance_curve([1, 2, 3, 4, 5, 6])
    _, db = B.dissonance_curve(B.bar_partials(4))
    sc = B.SLENDRO_LIKE
    clips = []
    for kind in ("harmonic", "bar"):
        parts, t = [], 0.0
        for c in sc + list(reversed(sc[:-1])):
            f = at_cents(C4, c)
            y = harmonic_tone(f, 1.0) if kind == "harmonic" else saron(f, 1.0)
            parts.append((arr(y), t, 0.0))
            t += 0.34
        for c1, c2 in ((0, sc[2]), (0, sc[3])):
            pass
        clips.append(Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["harmonic", "bar"])
    return {"cents": cs[::2].tolist(), "harmonic": dh[::2].tolist(), "bar": db[::2].tolist(),
            "min_harmonic": B.minima(cs, dh), "min_bar": B.minima(cs, db), "bar_partials": B.bar_partials(4), "slendro": sc,
            "starts": {k: float(s_.events[k]) for k in ("harmonic", "bar")},
            "clips": {"two": save("spectra.two", s_, kind="physical model", detail="an illustrative slendro-like scale up and down on a tone of harmonic partials (additive) and on a free bar (Part 9's partials 1, 2.76, 5.40, 8.93)")}}


def compute_scales() -> dict:
    clips = []
    for sc in (B.SLENDRO_LIKE, B.PELOG_LIKE):
        parts, t = [], 0.0
        for c in sc + list(reversed(sc[:-1])):
            parts.append((arr(saron(at_cents(C4, c), 1.1)), t, 0.0))
            t += 0.3
        clips.append(Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["slendro", "pelog"])
    return {"slendro": B.SLENDRO_LIKE, "pelog": B.PELOG_LIKE, "starts": {k: float(s_.events[k]) for k in ("slendro", "pelog")},
            "slendro_steps": np.diff(B.SLENDRO_LIKE).tolist(), "pelog_steps": np.diff(B.PELOG_LIKE).tolist(),
            "clips": {"two": save("scales.two", s_, detail="illustrative slendro (five near-equal steps) and pelog (seven unequal steps) up and down on a metallophone; Part 9's bar")}}


def compute_ombak() -> dict:
    notes = [C4 / 2, C4, C4 * 2]
    clips = []
    for beat in (0.0, 6.0):
        parts, t = [], 0.0
        for f in notes:
            parts.append((arr(saron(f, 2.4)), t, -3.0))
            parts.append((arr(saron(B.paired(f, beat), 2.4)), t, -3.0))
            t += 2.0
        clips.append(Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=["A", "B"])
    cents_off = [1200 * log2((f + 6.0) / f) for f in notes]
    return {"notes": notes, "beat": 6.0, "cents_off": cents_off, "answer": "B", "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("ombak.quiz", s_, detail="three notes in three octaves, each on two metallophones: A tuned exactly together, B with the second instrument 6 Hz higher at every pitch; Part 9's bar")}}


def compute_cycle() -> dict:
    beat = 0.42
    bal = [2, 3, 2, 1, 2, 3, 2, 1, 3, 5, 3, 2, 3, 5, 3, 1]          # a balungan of ours in slendro degrees 1..5
    sc = B.SLENDRO_LIKE
    col = B.colotomic("lancaran")
    parts = []
    for cyc in range(2):
        for i in range(16):
            t = (cyc * 16 + i) * beat
            deg = bal[i]
            parts.append((arr(saron(at_cents(C4, sc[deg - 1]), 1.0)), t, 0.0))
            for inst in col[i]:
                if inst == "gong":
                    parts.append((arr(gong(at_cents(C4 / 4, sc[deg - 1]), 3.5)), t, -2.0))
                elif inst == "kenong":
                    parts.append((arr(saron(at_cents(C4 / 2, sc[deg - 1]), 1.8)), t, -6.0))
                elif inst == "kempul":
                    parts.append((arr(gong(at_cents(C4 / 2, sc[deg - 1]), 2.0, 0.02)), t, -7.0))
                elif inst == "ketuk":
                    parts.append((arr(saron(C4 / 2 * 0.9, 0.25)[: int(0.15 * SR)]), t, -14.0))
    s_ = concat([Clip(mix(parts, duration=32 * beat + 3.0).y, SR).at_level(LEVEL)], gap=0.0, names=["cycle"])
    return {"balungan": bal, "colotomic": col, "beat": beat,
            "clips": {"cycle": save("cycle.lancaran", s_, detail="two cycles of a lancaran of ours: a sixteen-beat balungan on a saron, with ketuk, kenong, kempul and gong; Part 9's bars and gongs, in an illustrative slendro")}}


def compute_kotekan() -> dict:
    sc = B.SLENDRO_LIKE
    fig = [1, 2, 3, 2, 3, 5, 3, 2, 1, 2, 3, 5, 6, 5, 3, 2]
    a, b = B.interlock(fig)
    pulse = 0.12
    clips = []
    for part in (a, b, fig):
        parts = []
        for cyc in range(3):
            for i, x in enumerate(part):
                if x is not None:
                    c = sc[(x - 1) % 5] + (1200 if x > 5 else 0)
                    parts.append((arr(saron(at_cents(C4 * 2, c), 0.5)), (cyc * 16 + i) * pulse, 0.0))
        clips.append(Clip(mix(parts, duration=48 * pulse + 0.8).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["polos", "sangsih", "both"])
    return {"figure": fig, "polos": a, "sangsih": b, "pulse": pulse, "answer": "two",
            "starts": {k: float(s_.events[k]) for k in ("polos", "sangsih", "both")},
            "clips": {"three": save("kotekan.three", s_, detail="a figuration of ours split between two players: the first part alone, the second alone, then both, which sound as one fast line; Part 9's bar")}}


def compute_thirds() -> dict:
    parts, t, times = [], 0.0, []
    for third in (2 ** (300 / 1200), 2 ** (400 / 1200)):
        for at in ("a", "b"):
            parts.append((arr(cached(("bell3", round(third, 4), at), lambda third=third, at=at: B.two_tone_bell(C4, at, third=third))), t, 0.0))
            times.append(t)
            t += 1.6
        t += 0.8
    s_ = concat([Clip(mix(parts, duration=t + 2.0).y, SR).at_level(LEVEL)], gap=0.0, names=["thirds"])
    return {"times": times, "thirds": [300, 400],
            "clips": {"two": save("thirds.two", s_, detail="two two-tone bells on C4: one with its side note a minor third up, one a major third up; each centre then side; modal synthesis")}}


def compute_bellsong() -> dict:
    # three bells give six notes: C/E-flat, D/F, G/B-flat... we use centre and side of bells on C, D, G, A (minor and major thirds)
    bells = {"C": (C4, 2 ** (400 / 1200)), "D": (at_cents(C4, 200), 2 ** (300 / 1200)), "G": (at_cents(C4, 700), 2 ** (400 / 1200)),
             "A": (at_cents(C4, 900), 2 ** (300 / 1200))}
    # notes available: C(a) E(b) D(a) F(b) G(a) B(b) A(a) C'(b); a melody on C D E G A
    seq = [("C", "a"), ("D", "a"), ("C", "b"), ("G", "a"), ("A", "a"), ("G", "a"), ("C", "b"), ("D", "a"), ("C", "a")]
    parts, t, times = [], 0.0, []
    for b, at in seq:
        f, third = bells[b]
        parts.append((arr(cached(("bellS", b, at), lambda f=f, third=third, at=at: B.two_tone_bell(f, at, seconds=1.8, third=third))), t, 0.0))
        times.append(t)
        t += 0.55
    s_ = concat([Clip(mix(parts, duration=t + 1.8).y, SR).at_level(LEVEL)], gap=0.0, names=["song"])
    names = {("C", "a"): "C", ("C", "b"): "E", ("D", "a"): "D", ("G", "a"): "G", ("A", "a"): "A"}
    return {"seq": [[b, at, names.get((b, at), "")] for b, at in seq], "times": times,
            "clips": {"song": save("bellsong.song", s_, detail="a pentatonic melody of ours, C D E G A G E D C, on four two-tone bells, E sounded by striking the C bell at its side; modal synthesis")}}


def compute_twelve() -> dict:
    tw = sorted(x["cents"] for x in B.sanfen_lu(12))
    parts, t = [], 0.0
    for c in tw + [1200.0]:
        parts.append((arr(pluck(at_cents(C4, c), 0.8)), t, 0.0))
        t += 0.3
    s_ = concat([Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL)], gap=0.0, names=["twelve"])
    return {"cents": tw, "unit": 0.3, "steps": np.diff(tw + [1200.0]).round(1).tolist(),
            "clips": {"chromatic": save("twelve.chromatic", s_, detail="the twelve lü as a rising chromatic scale (Pythagorean semitones of 90 and 114 cents); a plucked-string model")}}


def compute_zhu() -> dict:
    pyth = [0, 203.91, 407.82, 701.96, 905.87, 1200, 905.87, 701.96, 407.82, 203.91, 0]
    et = [0, 200, 400, 700, 900, 1200, 900, 700, 400, 200, 0]
    clips = []
    for sc in (pyth, et):
        parts, t = [], 0.0
        for c in sc:
            parts.append((arr(pluck(at_cents(C4, c), 0.9)), t, 0.0))
            t += 0.34
        parts += [(arr(harmonic_tone(C4, 2.0)), t, -3.0), (arr(harmonic_tone(at_cents(C4, sc[2]), 2.0)), t, -3.0)]
        clips.append(Clip(mix(parts, duration=t + 2.4).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["pyth", "et"])
    return {"pyth": pyth, "et": et, "starts": {k: float(s_.events[k]) for k in ("pyth", "et")},
            "clips": {"two": save("zhu.two", s_, detail="the pentatonic up and down, then C with its third: in Pythagorean tuning (third 408 cents) and in equal temperament (400); a plucked-string model and additive tones")}}


def compute_melody() -> dict:
    mel5 = [(9, 1), (7, 1), (4, 1), (7, 1), (9, 1), (12, 2), (9, 1), (7, 1), (4, 1), (2, 1), (0, 3)]
    mel7 = [(9, 1), (7, 1), (6, 0.5), (4, 0.5), (7, 1), (9, 1), (11, 0.5), (12, 1.5), (9, 1), (7, 1), (4, 1), (2, 1), (0, 3)]
    clips, out = [], {}
    for name, mel in (("five", mel5), ("seven", mel7)):
        parts, t = [], 0.0
        for p, d in mel:
            parts.append((arr(pluck(at_cents(C4, p * 100), d * 0.36 + 0.4)), t, 0.0))
            t += d * 0.36
        clips.append(Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL))
        out[name] = [[p, d] for p, d in mel]
    s_ = concat(clips, gap=0.8, names=["five", "seven"])
    return {**out, "unit": 0.36, "starts": {k: float(s_.events[k]) for k in ("five", "seven")},
            "clips": {"two": save("melody.two", s_, detail="a pentatonic melody of ours ending on gong (C), then the same with the bian tones F sharp and B as passing notes; a plucked-string model")}}


def compute_openqin() -> dict:
    tuning = [0, 203.91, 498.04, 701.96, 905.87, 1200, 1403.91]
    parts, t = [], 0.0
    for c in tuning:
        parts.append((arr(pluck(at_cents(C4 / 2, c), 1.6)), t, 0.0))
        t += 0.6
    parts.append((arr(pluck(C4 / 2, 2.0)), t + 0.3, -2.0))
    parts.append((arr(pluck(at_cents(C4 / 2, 1200), 2.0)), t + 0.3, -2.0))
    s_ = concat([Clip(mix(parts, duration=t + 2.6).y, SR).at_level(LEVEL)], gap=0.0, names=["open"])
    return {"tuning": tuning, "names": ["C", "D", "F", "G", "A", "c", "d"], "unit": 0.6,
            "clips": {"open": save("openqin.open", s_, detail="the seven open strings of a qin model tuned C D F G A c d by pure fifths and fourths, then the octave C c; a plucked-string model")}}


def compute_sho() -> dict:
    chords = [[69, 71, 76, 78, 81, 83], [71, 76, 78, 81, 83, 85], [69, 74, 76, 79, 81, 83]]
    parts, t = [], 0.0
    for ch in chords:
        for m in ch:
            f = 440 * 2 ** ((m - 69) / 12)
            n = int(3.0 * SR)
            tt = np.arange(n) / SR
            y = sum((0.6 ** k) * np.sin(2 * np.pi * f * (k + 1) * tt) for k in range(5))
            env = np.minimum(1, tt / 0.8) * np.minimum(1, (3.0 - tt) / 0.6)
            parts.append((Clip(y * env, SR), t, -6.0))
        t += 2.6
    s_ = concat([Clip(mix(parts, duration=t + 0.8).y, SR).at_level(LEVEL)], gap=0.0, names=["sho"])
    return {"chords": chords,
            "clips": {"three": save_synth("sho.three", s_, detail="three sustained clusters of six notes in the manner of the sho's aitake (our voicings), each swelling and fading; additive tones")}}


def compute_patet() -> dict:
    pel = B.PELOG_LIKE
    subsets = {"1 2 3 5 6": [1, 2, 3, 5, 6], "2 3 5 6 7": [2, 3, 5, 6, 7]}
    clips = []
    for k, sub in subsets.items():
        parts, t = [], 0.0
        seq = sub + [sub[0] + 7] + list(reversed(sub))
        for deg in seq:
            c = pel[(deg - 1) % 7] + (1200 if deg > 7 else 0)
            parts.append((arr(saron(at_cents(C4, c), 1.0)), t, 0.0))
            t += 0.32
        clips.append(Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["A", "B"])
    return {"subsets": subsets, "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"two": save("patet.two", s_, detail="two five-note subsets of an illustrative pelog, degrees 1 2 3 5 6 and 2 3 5 6 7, each up and down; Part 9's bar")}}


def compute_rates() -> dict:
    clips = []
    for beat in (3.0, 8.0):
        parts = [(arr(saron(C4, 3.0)), 0.0, -3.0), (arr(saron(C4 + beat, 3.0)), 0.0, -3.0), (arr(saron(at_cents(C4, 700), 3.0)), 1.5, -3.0),
                 (arr(saron(at_cents(C4, 700) + beat, 3.0)), 1.5, -3.0)]
        clips.append(Clip(mix(parts, duration=4.8).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["slow", "fast"])
    return {"rates": [3.0, 8.0], "starts": {k: float(s_.events[k]) for k in ("slow", "fast")},
            "clips": {"two": save("rates.two", s_, detail="two notes on paired metallophones, first beating 3 times a second, then 8; Part 9's bar")}}


def compute_irama() -> dict:
    sc = B.SLENDRO_LIKE
    bal = [2, 3, 2, 1, 2, 3, 5, 3]
    beat = 0.6
    clips = []
    for dens in (2, 4):
        parts = []
        for i, deg in enumerate(bal):
            t = i * beat
            parts.append((arr(saron(at_cents(C4, sc[deg - 1]), 1.2)), t, 0.0))
            nxt = bal[(i + 1) % len(bal)]
            for k in range(dens):
                d_ = deg if k % 2 == 0 else nxt
                parts.append((arr(saron(at_cents(C4 * 2, sc[d_ - 1]), 0.5)), t + k * beat / dens, -8.0))
        clips.append(Clip(mix(parts, duration=len(bal) * beat + 1.2).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["two", "four"])
    return {"balungan": bal, "beat": beat, "starts": {k: float(s_.events[k]) for k in ("two", "four")},
            "clips": {"two": save("irama.two", s_, detail="one balungan line of ours with an elaborating part at two notes per beat, then at four; Part 9's bar in an illustrative slendro")}}


def compute_two_scales() -> dict:
    mel = tune_line(7)
    sl = B.SLENDRO_LIKE
    pl = B.PELOG_LIKE
    deg5 = {0: 0, 2: 1, 4: 2, 5: 2, 7: 3, 9: 4, 11: 4}
    deg7 = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
    clips = []
    for sc, deg in ((sl, deg5), (pl, deg7)):
        parts = []
        for p, a, d in mel:
            parts.append((arr(saron(at_cents(C4, sc[deg[p % 12]]), d * 0.42 + 0.6)), a * 0.42, 0.0))
        clips.append(Clip(mix(parts, duration=(mel[-1][1] + mel[-1][2]) * 0.42 + 1.2).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["slendro", "pelog"])
    return {"starts": {k: float(s_.events[k]) for k in ("slendro", "pelog")}, "note": "slendro has five notes, so the Tune's F and E share a key",
            "clips": {"two": save("two_scales.two", s_, detail="the Tune's first phrase on a metallophone in an illustrative slendro (its F and E fall on one key) and pelog; Part 9's bar")}}


def compute_kebyar() -> dict:
    sc = B.SLENDRO_LIKE
    fig = [1, 2, 3, 5, 3, 2, 3, 5, 6, 5, 3, 5, 3, 2, 1, 2] * 2
    pulse = 0.085
    parts = []
    for i, x in enumerate(fig):
        c = sc[(x - 1) % 5] + (1200 if x > 5 else 0)
        parts.append((arr(saron(at_cents(C4 * 2, c), 0.35)), i * pulse, 0.0))
        parts.append((arr(saron(B.paired(at_cents(C4 * 2, c), 7.0), 0.35)), i * pulse, -1.0))
    end = len(fig) * pulse
    parts.append((arr(gong(C4 / 4, 2.5)), end, 2.0))
    s_ = concat([Clip(mix(parts, duration=end + 2.0).y, SR).at_level(LEVEL)], gap=0.0, names=["burst"])
    return {"pulse": pulse, "n": len(fig),
            "clips": {"burst": save("kebyar.burst", s_, detail="a burst of ours in the manner of gong kebyar: a fast interlocking figure on paired metallophones beating 7 Hz, cut off by a gong; Part 9's bars and gong")}}


def compute_stopped() -> dict:
    f = C4 / 2
    target = f * 2
    parts = [(arr(pluck(target, 1.6)), 0.0, 0.0), (arr(pluck(target, 1.6) * 0.9), 1.8, 0.0)]
    t = np.arange(int(1.6 * SR)) / SR
    harm = sum((0.3 ** k) * np.sin(2 * np.pi * target * (k + 1) * t) for k in range(3)) * np.exp(-1.2 * t) * np.clip(t / 0.004, 0, 1)
    parts.append((Clip(harm, SR), 3.6, 0.0))
    s_ = concat([Clip(mix(parts, duration=5.6).y, SR).at_level(LEVEL)], gap=0.0, names=["three"])
    return {"times": [0.0, 1.8, 3.6],
            "clips": {"three": save("stopped.three", s_, kind="physical model", detail="one pitch three ways: an open string, the same pitch as a stopped note (the plucked-string model), and as a pure, bell-like harmonic (a near-sine additive tone standing in)")}}


QIN_TUNING = [0, 203.91, 498.04, 701.96, 905.87, 1200, 1403.91]     # C D F G A c d above C3, tuned by pure fifths and fourths


def qin_note(target_cents):
    """The harmonic on the qin's strings nearest a target (cents above C3): (string, partial, cents, error)."""
    best = None
    for s, sc in enumerate(QIN_TUNING):
        for n in range(2, 9):                                        # touched harmonics only, not open strings
            c = sc + 1200 * log2(n)
            e = c - target_cents
            if best is None or abs(e) < abs(best[3]):
                best = (s, n, c, e)
    return best


def compute_tune() -> dict:
    mel = tune_line(14)
    unit = 0.38
    # 1. qin harmonics: each note of the Tune (an octave above C4) as the nearest natural harmonic on a qin string
    parts, qn = [], []
    for p, a, d in mel:
        target = 2400 + p * 100
        s, n, c, e = qin_note(target)
        parts.append((arr(pluck(C4 / 2 * 2 ** (c / 1200), d * unit + 0.6) * 0.85), a * unit, 0.0))
        qn.append({"string": s + 1, "partial": n, "cents": c, "error": e})
    end1 = (mel[-1][1] + mel[-1][2]) * unit
    c1 = Clip(mix(parts, duration=end1 + 1.0).y, SR).at_level(LEVEL)
    # 2. balungan: the Tune's notes on the beats, mapped to an illustrative pelog, with kotekan doubling at four pulses a beat
    pel = B.PELOG_LIKE
    deg = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
    beat = 0.48
    parts = []
    bal = []
    for p, a, d in mel:
        for k in range(int(d)):
            bal.append(pel[deg[p % 12]])
    for i, c in enumerate(bal):
        parts.append((arr(saron(at_cents(C4, c), 1.2)), i * beat, 0.0))
        nxt = bal[i + 1] if i + 1 < len(bal) else bal[0]
        fig = [c, nxt, c, nxt]
        a_, b_ = B.interlock(fig)
        for k, x in enumerate(fig):
            parts.append((arr(saron(at_cents(C4 * 2, x), 0.45)), i * beat + k * beat / 4, -8.0 if k % 2 == 0 else -9.0))
        if (i + 1) % 4 == 0:
            parts.append((arr(saron(at_cents(C4 / 2, c), 1.8)), i * beat, -8.0))
    parts.append((arr(gong(at_cents(C4 / 4, bal[-1]), 3.5)), (len(bal) - 1) * beat, -4.0))
    c2 = Clip(mix(parts, duration=len(bal) * beat + 3.0).y, SR).at_level(LEVEL)
    s_ = concat([c1, c2], gap=1.0, names=["qin", "gamelan"])
    return {"qin": qn, "unit": unit, "balungan": bal, "beat": beat, "starts": {k: float(s_.events[k]) for k in ("qin", "gamelan")},
            "worst": max(abs(q["error"]) for q in qn), "seconds": s_.duration, "melody": [list(x) for x in mel],
            "clips": {"variation": save("tune.variation36", s_, detail="the Tune's first two phrases as natural harmonics on a qin tuned C D F G A c d, then as a balungan in an illustrative pelog with interlocking elaboration, kenong and gong; plucked-string and bar models")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 36, "title": "in qin harmonics, then as balungan with interlocking parts", "seconds": round(t["seconds"], 1),
            "measure": f"14 notes as harmonics, the worst {t['worst']:.0f} cents from equal temperament; a {len(t['balungan'])}-beat balungan, 4 pulses a beat",
            "clip": "tune.variation36"}


ITEMS = {"hook": compute_hook, "lu": compute_lu, "jingfang": compute_jingfang, "modes": compute_modes, "qin": compute_qin,
         "hetero": compute_hetero, "spectra": compute_spectra, "scales": compute_scales, "ombak": compute_ombak, "cycle": compute_cycle,
         "kotekan": compute_kotekan, "thirds": compute_thirds, "bellsong": compute_bellsong, "twelve": compute_twelve,
         "zhu": compute_zhu, "melody": compute_melody, "openqin": compute_openqin, "sho": compute_sho, "patet": compute_patet,
         "rates": compute_rates, "irama": compute_irama, "two_scales": compute_two_scales, "kebyar": compute_kebyar,
         "stopped": compute_stopped, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
