"""Precompute everything numerical, and every sound, in Part 33 of *Music, Built* ("The Mathematics of Rhythm and Scale").

    python -m videos.music.music33.compute              # everything missing (a minute or two)
    python -m videos.music.music33.compute --force vuza

Numbers are cached in ``.cache/music33/<name>.json``, sounds in ``.cache/music33/audio/``.  The mathematics is
Monochord's (``explainer/music/monochord/mathmusic.py``).  Rhythms are played on Part 11's clave and hat, notes on Part
7's piano, changes on Part 9's bells; the Bohlen–Pierce tones are synthesized.

Items:
    hook        three Euclidean rhythms: the tresillo E(3,8), the cinquillo E(5,8), the bell pattern E(7,12)
    euclid      Bjorklund's process for E(5,13); Toussaint's catalogue; an ear question (which 5-in-8 rhythm is even?)
    even        the bell pattern E(7,12) and the diatonic scale with the same steps; E(5,12) and the pentatonic, heard
    mos         continued fractions of the fifth; the moment-of-symmetry sizes; stacks of 5, 7 and 12 fifths, heard
    rank        every rhythm of 5 strokes in 8 pulses, ranked by distance from even (the cinquillo first)
    layers      E(3,8), E(5,16) and E(7,16) layered on three instruments, heard
    golden      stacks of the golden-ratio generator: two step sizes at the Fibonacci numbers
    meru        rhythms of n beats with k heavy syllables: Halayudha's triangle
    hunt6       plain hunt on six bells, heard
    oddity      Arom's oddity property counted; a homometric pair of rhythms (an ear question)
    canon       a small rhythmic canon, and a Vuza canon at period 72 found by search and verified, each heard
    prosody     Pingala's counts (Fibonacci); the rhythms of length 5; yamātārājabhānasalagāḥ as a de Bruijn sequence, heard
    ringing     plain hunt and Plain Bob Minimus on four bells: every order once, heard
    temper      equal divisions ranked by their fifths and thirds; vals and commas; a major triad in 19, just, 12 and 31 (an ear question: which is just?)
    bp          the Bohlen–Pierce scale on odd-harmonic and ordinary tones, and its 3:5:7 chord, heard
    tune        Variation 33: the Tune as a tiling canon, rung on bells, and in Bohlen–Pierce
    variation   the Variations ledger, row 33
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import log2

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import mathmusic as MM
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff
from explainer.music.monochord.physics.string import String

CACHE = Cache("music33")
CLIPS = ClipStore("music33")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_P: dict = {}
CLAVE = DK.clave()
HAT = DK.hat()
BLOCK = DK.woodblock()


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


def arr(y):
    return Clip(np.asarray(y, float), SR)


def rhythm_clip(pattern, pulse=0.17, cycles=3, hat=True):
    parts = []
    n = len(pattern)
    for c in range(cycles):
        for i, x in enumerate(pattern):
            t = (c * n + i) * pulse
            if hat:
                parts.append((arr(HAT * 0.25), t, -14.0))
            if x:
                parts.append((arr(CLAVE), t, 0.0))
    return Clip(mix(parts, duration=cycles * n * pulse + 0.6).y, SR)


def notes_clip(notes, unit, vel=0.95):
    parts = [(piano(p, min(d * unit * 1.05, 3.0), vel), a * unit, -2.0) for p, a, d in notes]
    end = max(a + d for _, a, d in notes)
    return Clip(mix(parts, duration=end * unit + 1.2).y, SR)


def tone(f, seconds, odd=False, partials=10):
    t = np.arange(int(seconds * SR)) / SR
    y = np.zeros(len(t))
    for k in range(1, partials + 1):
        if odd and k % 2 == 0:
            continue
        if f * k < 0.45 * SR:
            y += (0.7 ** (k - 1)) * np.sin(2 * np.pi * f * k * t)
    env = np.minimum(1, t / 0.03) * np.exp(-1.2 * t) * np.minimum(1, (seconds - t) / 0.08)
    return y * env


def pat(s):
    return MM.parse(s)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    rs = [("tresillo", "x..x..x."), ("cinquillo", "x.xx.xx."), ("bell", "x.x.xx.x.x.x")]
    clips = [rhythm_clip(pat(s), cycles=3 if len(s) == 8 else 2).at_level(LEVEL) for _, s in rs]
    s_ = concat(clips, gap=0.8, names=[k for k, _ in rs])
    return {"rhythms": [{"name": k, "pattern": s, "k": s.count("x"), "n": len(s)} for k, s in rs], "pulse": 0.17,
            "starts": {k: float(s_.events[k]) for k, _ in rs},
            "clips": {"three": save("hook.three", s_, detail="the tresillo E(3,8), the cinquillo E(5,8) and the West African bell pattern E(7,12), on a clave over a quiet hat; Part 11's kit")}}


def compute_euclid() -> dict:
    stages = MM.euclid_steps(5, 13)
    table = MM.named_euclidean()
    a, b = "xxx.x.x.", "x.xx.xx."
    ca = rhythm_clip(pat(a), cycles=3).at_level(LEVEL)
    cb = rhythm_clip(pat(b), cycles=3).at_level(LEVEL)
    s_ = concat([ca, cb], gap=1.0, names=["A", "B"])
    gaps = {k: MM.steps(pat(s)) for k, s in (("A", a), ("B", b))}
    return {"stages": stages, "result": "".join("x" if x else "." for x in MM.euclid(5, 13)), "table": table,
            "quiz": {"A": a, "B": b}, "answer": "B", "gaps": gaps, "starts": {k: float(s_.events[k]) for k in "AB"}, "pulse": 0.17,
            "clips": {"quiz": save("euclid.quiz", s_, detail="two rhythms of five onsets in eight pulses: A clumped, B the cinquillo; Part 11's kit")}}


def compute_even() -> dict:
    bell = pat("x.x.xx.x.x.x")                                        # E(7,12), rotated to start the major scale
    pent = pat("x.x.x..x.x..")                                        # E(5,12), rotated to start C D E G A
    pulse = 0.2
    out = {}
    clips = []
    for name, p, base in (("bell", bell, 60), ("pentatonic", pent, 60)):
        ons = MM.onsets(p)
        r = rhythm_clip(p, pulse=pulse, cycles=2, hat=True).at_level(LEVEL)
        notes = [(base + o, o, 1.0) for o in ons] + [(base + 12, 12, 1.5)]
        sc = notes_clip(notes, pulse * 1.6).at_level(LEVEL)
        clips += [r, sc]
        out[name] = {"pattern": "".join("x" if x else "." for x in p), "onsets": ons, "steps": MM.steps(p)}
    s_ = concat(clips, gap=0.7, names=["bell", "diatonic", "five", "pentatonic"])
    return {**out, "pulse": pulse, "starts": {k: float(s_.events[k]) for k in ("bell", "diatonic", "five", "pentatonic")},
            "clips": {"two": save("even.two", s_, detail="the bell pattern E(7,12) on a clave, then the same twelve-step positions as notes (the major scale); E(5,12), then the pentatonic scale; Part 11's kit and Part 7's piano")}}


def compute_mos() -> dict:
    conv = MM.convergents(log2(1.5), 8)
    sizes = MM.mos_sizes(log2(1.5), 60)
    clips = []
    for n in (5, 7, 12):
        pcs = sorted({(7 * i) % 12 for i in range(n)}) if n != 5 else sorted({(7 * i) % 12 for i in range(5)})
        notes = [(60 + p, i, 1.0) for i, p in enumerate(pcs)] + [(72, len(pcs), 1.5)]
        clips.append(notes_clip(notes, 0.28).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["5", "7", "12"])
    steps = {}
    for n in (2, 3, 5, 7, 12):
        pts = np.sort((np.arange(n) * log2(1.5)) % 1.0)
        g = np.diff(np.concatenate([pts, [1.0]])) * 1200
        steps[str(n)] = sorted({round(float(x), 1) for x in g})
    return {"convergents": [[f.numerator, f.denominator] for f in conv], "sizes": sizes, "steps": steps,
            "fifth_log": log2(1.5), "starts": {k: float(s_.events[k]) for k in ("5", "7", "12")},
            "clips": {"three": save("mos.three", s_, detail="stacks of 5, 7 and 12 fifths folded into one octave, each played as a scale from C; Part 7's piano")}}


def _even_dist(ons, n):
    from explainer.music.monochord import geometry as G
    return G.evenness([12.0 * o / n for o in ons]) * n / 12.0


def compute_rank() -> dict:
    rows_ = []
    seen = set()
    for c in combinations(range(8), 5):
        key = min(tuple(sorted((x + t) % 8 for x in c)) for t in range(8))
        if key in seen:
            continue
        seen.add(key)
        p = MM.pattern_of(key, 8)
        rows_.append({"pattern": "".join("x" if x else "." for x in p), "dist": _even_dist(key, 8), "euclid": MM.is_rotation(p, MM.euclid(5, 8))})
    rows_.sort(key=lambda r: r["dist"])
    return {"rows": rows_, "count": len(rows_)}


def compute_layers() -> dict:
    pulse = 0.13
    n = 16
    layers = [("low drum", MM.euclid(3, 8) * 2, -3.0), ("woodblock", MM.euclid(5, 16), -1.0), ("clave", MM.euclid(7, 16), 0.0)]
    parts = []
    for cyc in range(4):
        for name, p, g in layers:
            for i, x in enumerate(p):
                if x:
                    snd = {"low drum": arr(PC.drum(hz(45), seconds=0.4, at=0.3)), "woodblock": arr(BLOCK), "clave": arr(CLAVE)}[name]
                    parts.append((snd, (cyc * n + i) * pulse, g))
    c = Clip(mix(parts, duration=4 * n * pulse + 0.8).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["layers"])
    return {"layers": [{"name": k, "pattern": "".join("x" if x else "." for x in p)} for k, p, _ in layers], "pulse": pulse, "n": n,
            "clips": {"layers": save("layers.three", s_, detail="E(3,8) twice on a low drum, E(5,16) on a woodblock and E(7,16) on a clave, together, four times round; Part 9's drum and Part 11's kit")}}


def compute_golden() -> dict:
    phi = (5 ** 0.5 - 1) / 2
    sizes = MM.mos_sizes(phi, 60)
    return {"generator": phi, "sizes": sizes, "fifth_sizes": MM.mos_sizes(log2(1.5), 60)}


def compute_meru() -> dict:
    tri = []
    for n in range(1, 9):
        row = {}
        for r in MM.prosody_rhythms(n):
            k = r.count("L")
            row[k] = row.get(k, 0) + 1
        tri.append([row[k] for k in sorted(row)])
    return {"rows": tri}


def compute_hunt6() -> dict:
    hunt = MM.plain_hunt(6)
    pitches = {1: 79, 2: 77, 3: 76, 4: 74, 5: 72, 6: 67}
    bells = {k: arr(PC.bell(hz(m), seconds=1.2)) for k, m in pitches.items()}
    stroke = 0.17
    parts, t = [], 0.0
    for i, row in enumerate(hunt):
        for b in row:
            parts.append((bells[b], t, -2.0))
            t += stroke
        if i % 2 == 1:
            t += stroke
    c = Clip(mix(parts, duration=t + 1.4).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["hunt"])
    return {"rows": [list(r) for r in hunt], "stroke": stroke,
            "clips": {"hunt": save("hunt6.hunt", s_, detail="plain hunt on six bells tuned G, F, E, D, C and low G, twelve changes and back to rounds; Part 9's bells")}}


def compute_oddity() -> dict:
    counts = {}
    for n in (8, 12, 16):
        row = {}
        for k in range(1, n // 2 + 2):
            classes = set()
            for c in combinations(range(n), k):
                if MM.oddity(c, n):
                    classes.add(min(tuple(sorted((x + t) % n for x in c)) for t in range(n)))
            row[str(k)] = len(classes)
        counts[str(n)] = row
    pairs = MM.homometric_pairs(4, 8)
    a, b = pairs[0]
    pa, pb = MM.pattern_of(a, 8), MM.pattern_of(b, 8)
    s_ = concat([rhythm_clip(pa, cycles=3).at_level(LEVEL), rhythm_clip(pb, cycles=3).at_level(LEVEL)], gap=1.0, names=["A", "B"])
    return {"counts": counts, "pair": [list(a), list(b)], "content": list(MM.interval_content(a, 8)),
            "n_pairs": {"4/8": len(MM.homometric_pairs(4, 8)), "5/12": len(MM.homometric_pairs(5, 12)), "6/12": len(MM.homometric_pairs(6, 12))},
            "bell_odd": MM.oddity(MM.onsets(MM.euclid(7, 12)), 12), "five_odd": MM.oddity(MM.onsets(MM.euclid(5, 12)), 12),
            "answer": "yes", "starts": {k: float(s_.events[k]) for k in "AB"}, "patterns": ["".join("x" if x else "." for x in p) for p in (pa, pb)],
            "clips": {"quiz": save("oddity.quiz", s_, detail="two rhythms of four onsets in eight pulses with the same intervals between their onsets: 0 1 2 5 and 0 1 3 4; Part 11's kit")}}


def compute_canon() -> dict:
    # a small canon: rhythm {0, 1, 4, 5} entering at 0 and 2 fills 8 pulses exactly once
    sA, sB, sn = (0, 1, 4, 5), (0, 2), 8
    small = {"A": list(sA), "B": list(sB), "n": sn, "tiles": MM.is_tiling(sA, sB, sn)}
    pulse = 0.2
    parts = []
    pitches = [72, 64]
    for c in range(2):
        for j, b in enumerate(sB):
            for a in sA:
                parts.append((piano(pitches[j], 0.3, 0.9), (c * sn + a + b) * pulse, -2.0))
    small_clip = Clip(mix(parts, duration=2 * sn * pulse + 1.0).y, SR).at_level(LEVEL)
    chk = MM.vuza_check()
    tB = MM.tilings(MM.VUZA_A, MM.VUZA_N)
    aper = [B for B in tB if not MM.is_periodic(B, MM.VUZA_N)]
    # the Vuza canon heard: twelve voices, each the six-onset rhythm A, entering at B's offsets, each on its own pitch
    voices_p = [48, 52, 55, 59, 62, 64, 67, 69, 71, 72, 74, 76]
    vp = 0.12
    parts, notes = [], []
    for j, b in enumerate(MM.VUZA_B):
        for a in MM.VUZA_A:
            t = (a + b) % MM.VUZA_N
            parts.append((piano(voices_p[j], 0.25, 0.85), t * vp, -2.0))
            notes.append([float(voices_p[j]), float(t), 1.0])
    vz = Clip(mix(parts, duration=MM.VUZA_N * vp + 1.0).y, SR).at_level(LEVEL)
    s1 = concat([small_clip], gap=0.0, names=["small"])
    s2 = concat([vz], gap=0.0, names=["vuza"])
    return {"small": small, "vuza": {"A": list(MM.VUZA_A), "B": list(MM.VUZA_B), "n": MM.VUZA_N, **chk, "n_tilings": len(tB), "n_aperiodic": len(aper)},
            "pulse": pulse, "vpulse": vp, "notes": notes,
            "clips": {"small": save("canon.small", s1, detail="a canon in which the rhythm 0 1 4 5, entering twice, fills eight pulses exactly once, twice round; Part 7's piano"),
                      "vuza": save("canon.vuza", s2, detail="a Vuza canon of period 72: twelve voices on twelve pitches, each the rhythm 0 8 16 18 26 34, entering at 0 1 5 24 25 29 30 36 49 53 60 66, together sounding every pulse exactly once; Part 7's piano")}}


def compute_prosody() -> dict:
    counts = MM.prosody_counts(12)
    r5 = MM.prosody_rhythms(5)
    bits = MM.YAMATA_BITS
    pulse = 0.2
    parts, t = [], 0.0
    times = []
    for rep in range(2):
        for b in bits:
            parts.append((arr(BLOCK), t, 0.0 if b else -4.0))
            times.append(t)
            t += pulse * (2 if b else 1)
        t += pulse * 2
    c1 = Clip(mix(parts, duration=t + 0.6).y, SR).at_level(LEVEL)
    parts2, t2, times2 = [], 0.0, []
    for r in r5:
        start = t2
        for s in r:
            parts2.append((arr(BLOCK), t2, 0.0 if s == "L" else -4.0))
            t2 += pulse * (2 if s == "L" else 1)
        times2.append(start)
        t2 += pulse * 2
    c2 = Clip(mix(parts2, duration=t2 + 0.6).y, SR).at_level(LEVEL)
    s1 = concat([c2], gap=0.0, names=["five"])
    s2 = concat([c1], gap=0.0, names=["yamata"])
    wins = MM.windows(bits, 3)
    return {"counts": counts, "rhythms5": r5, "bits": bits, "syllables": MM.YAMATA, "windows": ["".join("H" if x else "L" for x in w) for w in wins],
            "distinct": len(set(wins)), "times": times, "times5": times2, "pulse": pulse,
            "clips": {"five": save("prosody.five", s1, detail="the eight rhythms of short (one pulse) and long (two pulses) syllables lasting five pulses, the long ones louder; Part 11's woodblock"),
                      "yamata": save("prosody.yamata", s2, detail="the ten syllables ya mā tā rā ja bhā na sa la gā as short and long strokes, twice; Part 11's woodblock")}}


def compute_ringing() -> dict:
    hunt = MM.plain_hunt(4)
    bob = MM.plain_bob_minimus()
    bell_hz = {1: hz(76), 2: hz(74), 3: hz(72), 4: hz(67)}            # treble to tenor: E, D, C, G
    bells = {k: arr(PC.bell(f, seconds=1.4)) for k, f in bell_hz.items()}
    stroke = 0.2
    parts, t = [], 0.0
    for i, row in enumerate(bob):
        for b in row:
            parts.append((bells[b], t, -2.0))
            t += stroke
        if i % 2 == 1:
            t += stroke                                                 # the handstroke gap
    c = Clip(mix(parts, duration=t + 1.6).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["bob"])
    return {"hunt": [list(r) for r in hunt], "bob": [list(r) for r in bob], "distinct": len(set(bob[:-1])), "back": bob[-1] == bob[0],
            "stroke": stroke, "pitches": {str(k): v for k, v in {1: "E", 2: "D", 3: "C", 4: "G"}.items()},
            "clips": {"bob": save("ringing.bob", s_, detail="Plain Bob Minimus on four bells tuned E, D, C, G: 24 changes, every order once, back to rounds, with a gap after each pair of rows; Part 9's bells")}}


def compute_temper() -> dict:
    best = MM.best_edos(60)
    commas = {"81/80": Fraction(81, 80), "Pythagorean": Fraction(531441, 524288), "128/125": Fraction(128, 125), "schisma": Fraction(32805, 32768)}
    vals = {}
    for n in (12, 19, 31, 53):
        v = MM.patent_val(n)
        vals[str(n)] = {"val": list(v), "tempers": {k: MM.tempers_out(v, r) for k, r in commas.items()}, **MM.edo_error(n)}
    clips, chords = [], {}
    tunings = {"12": (400.0, 700.0), "19": (1200 * 6 / 19, 1200 * 11 / 19), "31": (1200 * 10 / 31, 1200 * 18 / 31),
               "just": (1200 * log2(1.25), 1200 * log2(1.5))}
    order = ["19", "just", "12", "31"]                                  # played as A, B, C, D
    for name in order:
        third, fifth = tunings[name]
        ch = [60, 60 + third / 100, 60 + fifth / 100]
        parts = [(piano(m, 2.2, 0.9), 0.0, -2.0) for m in ch]
        clips.append(Clip(mix(parts, duration=2.8).y, SR).at_level(LEVEL))
        chords[name] = {"third": third, "fifth": fifth}
    s_ = concat(clips, gap=0.8, names=list("ABCD"))
    return {"best": best, "vals": vals, "chords": chords, "order": order, "answer": "ABCD"[order.index("just")],
            "starts": {k: float(s_.events[k]) for k in "ABCD"},
            "commas": {k: list(MM.monzo(r)) for k, r in commas.items()},
            "clips": {"four": save("temper.quiz", s_, detail="a C major triad four times: with the third and fifth of 19 equal steps, just (5:4 and 3:2), 12 and 31 equal steps; Part 7's piano, retuned")}}


def compute_bp() -> dict:
    b = MM.bohlen_pierce()
    step = b["step_cents"]
    f0 = hz(55)
    seq = [f0 * 2 ** (k * step / 1200) for k in range(14)]
    parts_odd, parts_all = [], []
    for i, f in enumerate(seq):
        parts_odd.append((Clip(tone(f, 0.5, odd=True), SR), i * 0.3, -2.0))
        parts_all.append((Clip(tone(f, 0.5, odd=False), SR), i * 0.3, -2.0))
    c1 = Clip(mix(parts_odd, duration=14 * 0.3 + 0.8).y, SR).at_level(LEVEL)
    chord = [f0, f0 * 2 ** (6 * step / 1200), f0 * 2 ** (10 * step / 1200)]
    c2 = Clip(mix([(Clip(tone(f, 2.4, odd=True), SR), 0.0, -2.0) for f in chord], duration=3.0).y, SR).at_level(LEVEL)
    c3 = Clip(mix([(Clip(tone(f, 2.4, odd=False), SR), 0.0, -2.0) for f in chord], duration=3.0).y, SR).at_level(LEVEL)
    s_ = concat([c1, c2, c3], gap=0.7, names=["scale", "odd", "all"])
    return {**b, "chord_ratios": [1, 5 / 3, 7 / 3], "starts": {k: float(s_.events[k]) for k in ("scale", "odd", "all")},
            "clips": {"three": save_synth("bp.three", s_, detail="the Bohlen–Pierce scale, 13 equal steps from G2 to the tritave above, on a tone of odd harmonics; then its 3:5:7 chord on odd harmonics, and on all harmonics; additive synthesis")}}


def tune_notes(n=14, base=72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


LAMBDA = [0, 2, 3, 4, 6, 7, 9, 10, 12, 13]                          # the Bohlen–Pierce Lambda mode's degrees (of 13)


def compute_tune() -> dict:
    mel = tune_notes(14)
    # 1. a tiling canon: twelve voices, each the Vuza rhythm, each on one of the Tune's notes in order
    pitches = [p for p, _, _ in mel][:12]
    vp = 0.11
    parts, order = [], [None] * MM.VUZA_N
    for j, b in enumerate(MM.VUZA_B):
        for a in MM.VUZA_A:
            t = (a + b) % MM.VUZA_N
            order[t] = j
            parts.append((piano(pitches[j] - 12, 0.22, 0.85), t * vp, -2.0))
    c1 = Clip(mix(parts, duration=MM.VUZA_N * vp + 0.8).y, SR).at_level(LEVEL)
    # 2. rung on bells tuned to the Tune's first four different pitches: plain hunt
    four = []
    for p, _, _ in mel:
        if p not in four:
            four.append(p)
        if len(four) == 4:
            break
    four_sorted = sorted(four, reverse=True)
    bells = {i + 1: arr(PC.bell(hz(p), seconds=1.2)) for i, p in enumerate(four_sorted)}
    hunt = MM.plain_hunt(4)
    parts2, t = [], 0.0
    for i, row in enumerate(hunt + [hunt[0]]):
        for b in row:
            parts2.append((bells[b], t, -2.0))
            t += 0.18
        if i % 2 == 1:
            t += 0.18
    c2 = Clip(mix(parts2, duration=t + 1.2).y, SR).at_level(LEVEL)
    # 3. in Bohlen–Pierce: the Tune's scale degrees mapped to the Lambda mode
    deg = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
    step = MM.bohlen_pierce()["step_cents"]
    f0 = hz(60)
    parts3 = []
    bp_notes = []
    for p, a, d in mel:
        k = LAMBDA[deg[(p - 72) % 12]]
        f = f0 * 2 ** (k * step / 1200)
        parts3.append((Clip(tone(f, d * 0.42 + 0.1, odd=True), SR), a * 0.42, -2.0))
        bp_notes.append([float(k), float(a), float(d)])
    c3 = Clip(mix(parts3, duration=sum(d for _, _, d in mel) * 0.42 + 0.8).y, SR).at_level(LEVEL)
    s_ = concat([c1, c2, c3], gap=1.0, names=["canon", "bells", "bp"])
    return {"pitches": pitches, "order": order, "vpulse": vp, "four": four_sorted, "hunt": [list(r) for r in hunt], "bp_notes": bp_notes,
            "starts": {k: float(s_.events[k]) for k in ("canon", "bells", "bp")}, "seconds": s_.duration,
            "clips": {"variation": save("tune.variation33", s_, kind="synthesized",
                                        detail="the Tune's first twelve notes as the twelve voices of the Vuza canon; plain hunt on bells tuned to its first four pitches; its first phrases in the Bohlen–Pierce Lambda mode on odd harmonics; Part 7's piano, Part 9's bells, additive synthesis")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 33, "title": "as a Vuza canon, rung in plain hunt, and in Bohlen–Pierce", "seconds": round(t["seconds"], 1),
            "measure": "72 pulses, 12 voices, each pulse struck once; 8 changes on 4 bells; 14 notes in 13 steps to the tritave",
            "clip": "tune.variation33"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation33", 33)


ITEMS = {"hook": compute_hook, "euclid": compute_euclid, "even": compute_even, "mos": compute_mos, "rank": compute_rank, "layers": compute_layers, "golden": compute_golden, "meru": compute_meru, "hunt6": compute_hunt6, "oddity": compute_oddity,
         "canon": compute_canon, "prosody": compute_prosody, "ringing": compute_ringing, "temper": compute_temper, "bp": compute_bp,
         "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
