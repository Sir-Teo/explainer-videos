"""Precompute everything numerical, and every sound, in Part 28 of *Music, Built* ("New Scales, New Rhythms").

    python -m videos.music.music28.compute              # everything missing (a few minutes)
    python -m videos.music.music28.compute --force census

Numbers are cached in ``.cache/music28/<name>.json``, sounds in ``.cache/music28/audio/``.  The measures are Monochord's
(``explainer/music/monochord/modern.py``).  Every piece of music in this part is ours: the films of this era's
composers are mostly still in copyright, so the part analyses them in words and numbers and plays original pastiches
(SYLLABUS §2.4).  The instruments are Part 7's piano and bowed string and Part 9's bars, gongs and drums.

Items:
    hook        a gamelan texture of our own: a slendro balungan on bars, its elaboration, gongs marking the cycle
    wholetone   the Tune's first phrase in C major, then mapped onto the whole-tone scale
    census      every one of the 4,096 pitch-class sets: 352 shapes up to transposition, 15 with limited transposition,
                Messiaen's seven among them
    planing     the Tune harmonized by function and by planing (an ear question)
    octatonic   the scale; two triads a tritone apart (C and F sharp); an octatonic ostinato; the chance that a random
                k-note collection fits an octatonic, diatonic or whole-tone scale
    accents     an ostinato with regular and with displaced accents (an ear question); additive rhythms
    bartok      additive groupings of 5, 7, 8 and 9 pulses heard; the golden section against its null model
    polychord   the Tune in C over chords in F sharp: one key and two keys fitted
    messiaen    mode 2 chords over a non-retrogradable rhythm; palindromic rhythms counted
    slendro     the same core melody on bars tuned to equal fifths of an octave, then on the piano's black keys
    modes       Messiaen's first three modes, rising, each from C
    triads      the four major triads inside one octatonic scale: C, E flat, F sharp, A
    blocks      three ostinatos of 3, 4 and 5 pulses layered: they realign after 60
    added       a regular rhythm, then with Messiaen's added values
    tune        Variation 28: whole-tone planing, then an octatonic ostinato with moving accents
    variation   the Variations ledger, row 28
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import modern as MD
from explainer.music.monochord import rhythm as RH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music28")
CLIPS = ClipStore("music28")
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


def piano(m: float, seconds: float, velocity: float = 1.1) -> Clip:
    seconds = round(min(max(seconds, 0.12), 3.0), 2)
    key = (round(m, 3), seconds, round(velocity, 2))
    if key not in _P:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4),
                                  velocity=velocity, seconds=seconds + 0.3))
        _P[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _P[key]


def bowed(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(min(seconds, 2.6), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 2.6), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.008, 0.05).at_level(LEVEL)
    return _V[key]


def place(lines, inst, unit: float, gains=None, tail: float = 1.0) -> Clip:
    gains = gains or [0.0] * len(lines)
    placed, end = [], 0.0
    for ln, g in zip(lines, gains):
        for p, a, d in ln:
            placed.append((inst(p, d * unit * 1.02), a * unit, g))
            end = max(end, (a + d) * unit)
    return Clip(mix(placed, duration=end + tail).y, SR)


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


def tune_line(base: int = 72, n: int = 14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


DEG = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}


def to_scale(line, scale, base=72):
    """Map each note's degree in C major onto the same degree of another scale (degree 7 wraps an octave up)."""
    out = []
    for p, a, d in line:
        rel = p - base
        octv, pc = divmod(rel, 12)
        k = DEG[pc]
        o2, j = divmod(k, len(scale))
        out.append((base + 12 * (octv + o2) + scale[j], a, d))
    return out


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    cents = MD.slendro()
    base = 62.0
    def sl(deg):                                   # slendro degree 1..5 (and 6 = 1 an octave up) as a fractional key number
        o, k = divmod(deg - 1, 5)
        return base + 12 * o + cents[k] / 100.0
    balungan = [3, 2, 3, 1, 3, 2, 1, 5, 1, 2, 3, 5, 2, 1, 5, 6]                   # ours, sixteen beats, the gong on the last
    beat = 0.62
    parts = []
    bal = []
    for i, d in enumerate(balungan):
        m = sl(d)
        bal.append((m, i, 1))
        y = PC.marimba(hz(m), seconds=1.4, tuned=False, soft=0.8)
        parts.append((Clip(y, SR).fade(0.0005, 0.2).at_level(LEVEL), i * beat, -2.0))
    elab = []
    for i in range(len(balungan)):                 # the bonang doubles the speed: the beat's note, then the next one's
        a, b = balungan[i], balungan[(i + 1) % len(balungan)]
        for j, d in enumerate((a, b)):
            m = sl(d) + 12
            elab.append((m, i + 0.5 * j, 0.5))
            y = PC.marimba(hz(m), seconds=0.8, tuned=False, soft=1.4)
            parts.append((Clip(y, SR).fade(0.0005, 0.15).at_level(LEVEL), (i + 0.5 * j) * beat, -9.0))
    gongs = []
    for i in range(3, 16, 4):                      # the kenong every fourth beat
        m = sl(balungan[i]) - 12
        gongs.append((m, i, 1))
        y = PC.gong(hz(m), seconds=2.0, glide=0.03, decay=1.6)
        parts.append((Clip(y, SR).fade(0.001, 0.3).at_level(LEVEL), i * beat, -6.0))
    yg = PC.gong(hz(base - 24 + 7.2), seconds=5.0, glide=0.05, decay=0.5)
    parts.append((Clip(yg, SR).fade(0.001, 1.0).at_level(LEVEL), 15 * beat, -1.0))
    c = Clip(mix(parts, duration=16 * beat + 5.0).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["gamelan"])
    return {"balungan": rows(bal), "elab": rows(elab), "gongs": rows(gongs), "gong_beat": 15, "beat": beat, "cents": cents,
            "clips": {"gamelan": save("hook.gamelan", s_, level=None, detail="a gamelan texture of our own in an idealized slendro: a balungan on bars, its elaboration at double speed, the kenong every fourth beat and the great gong at the end; Part 9's bars and gongs")}}


def compute_wholetone() -> dict:
    mel = tune_line(n=7)
    wt = to_scale(mel, (0, 2, 4, 6, 8, 10))
    unit = 0.42
    a = place([mel], lambda m, s: piano(m, s), unit)
    b = place([wt], lambda m, s: piano(m, s), unit)
    s_ = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["major", "whole"])
    return {"major": rows(mel), "whole": rows(wt), "unit": unit, "starts": {k: float(s_.events[k]) for k in ("major", "whole")},
            "periods": {"major": MD.period(MD.DIATONIC), "whole": MD.period(MD.WHOLE_TONE)},
            "clips": {"two": save("wholetone.two", s_, detail="the Tune's first phrase in C major, then on the whole-tone scale, degree for degree, Part 7's piano")}}


def compute_census() -> dict:
    c = MD.census()
    sym = []
    for size, items in sorted(c["symmetric"].items()):
        for it in items:
            sym.append({"size": size, "pcs": list(it["pcs"]), "period": it["period"], "mode": MD.messiaen_mode(it["pcs"])})
    return {"classes": c["classes"], "by_size": {str(k): v for k, v in c["by_size"].items()}, "symmetric": sym, "n_symmetric": c["n_symmetric"],
            "messiaen": {str(k): {"pcs": list(v), "transpositions": MD.transpositions(v)} for k, v in MD.MESSIAEN.items()},
            "all_union": all(MD.is_union_of_cosets(s["pcs"]) for s in sym)}


HARM = [(48, 52, 55), (48, 52, 55), (53, 57, 60), (48, 52, 55), (53, 57, 60), (48, 52, 55), (43, 50, 53), (48, 52, 55)]


def compute_planing() -> dict:
    mel = tune_line(n=7)
    unit = 0.45
    func = [(p, 2 * i, 2) for i, ch in enumerate([(48, 52, 55), (53, 57, 60), (53, 57, 60), (48, 52, 55)]) for p in ch]
    func = [(p, a, d) for p, a, d in func if a < 8]
    planed = MD.planed(mel, shape=(-3, -7, -12))                      # a major triad, its fifth on top, under every note
    a = place([mel, func], lambda m, s: piano(m, s), unit, gains=[0.0, -4.0])
    b = place([mel] + planed, lambda m, s: piano(m, s), unit, gains=[0.0, -4.0, -4.0, -5.0])
    s_ = concat([b.at_level(LEVEL), a.at_level(LEVEL)], gap=1.2, names=["A", "B"])                # A: planed; B: functional
    return {"melody": rows(mel), "functional": rows(func), "planed": [rows(v) for v in planed], "unit": unit, "answer": "A",
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("planing.quiz", s_, detail="the Tune's first phrase twice: over major triads moving in parallel under every note (planing), then over tonic and subdominant chords; Part 7's piano")}}


def compute_octatonic() -> dict:
    scale = [60 + p for p in MD.OCTATONIC] + [72]
    unit = 0.3
    sc = place([[(p, i, 1) for i, p in enumerate(scale)]], lambda m, s: piano(m, s), unit)
    chord = [(48, 0, 4), (55, 0, 4), (64, 0, 4), (54, 0, 4), (61, 0, 4), (70, 0, 4)]                   # C major and F sharp major
    arp = [(p, 4 + 0.5 * i, 0.5) for i, p in enumerate([60, 64, 67, 72, 66, 70, 73, 78, 72, 67, 64, 60, 78, 73, 70, 66])]
    ch = place([chord + arp], lambda m, s: piano(m, s), 0.45)
    ost = []
    pat = [0, 1, 3, 4, 6, 4, 3, 1]
    for r in range(4):
        for i, k in enumerate(pat):
            ost.append((48 + MD.OCTATONIC[k] + (0 if r < 2 else 3), 8 * r + i, 1))
    os_ = place([ost], bowed, 0.2)
    s_ = concat([sc.at_level(LEVEL), ch.at_level(LEVEL), os_.at_level(LEVEL)], gap=1.0, names=["scale", "chord", "ostinato"])
    chance = {name: [MD.chance_fits(k, sc_) for k in range(3, 9)] for name, sc_ in
              (("octatonic", MD.OCTATONIC), ("diatonic", MD.DIATONIC), ("whole-tone", MD.WHOLE_TONE))}
    return {"scale": rows([(p, i, 1) for i, p in enumerate(scale)]), "chord": rows(chord), "arp": rows(arp), "ostinato": rows(ost),
            "units": {"scale": unit, "chord": 0.45, "ostinato": 0.2}, "starts": {k: float(s_.events[k]) for k in ("scale", "chord", "ostinato")},
            "petrushka_fits": MD.fits([0, 4, 7, 6, 10, 1], MD.OCTATONIC), "chance": chance, "ks": list(range(3, 9)),
            "clips": {"three": save("octatonic.three", s_, detail="the octatonic scale on C; C major and F sharp major together, then arpeggiated; an octatonic ostinato, ours; Part 7's piano and bowed string")}}


def drum_hit(acc: bool) -> Clip:
    y = PC.drum(hz(43), seconds=0.5, at=0.4, damping=6.0) if acc else DK.woodblock(800.0, 0.15)
    return Clip(np.asarray(y, float), SR).fade(0.0005, 0.05)


def chord_hit(acc: bool, notes=(52, 56, 59, 62, 63, 67)) -> Clip:
    parts = [(bowed(m, 0.16), 0.0, 0.0) for m in notes]
    c = Clip(mix(parts, duration=0.3).y, SR)
    return c.gain(0.0 if acc else -12.0)


def compute_accents() -> dict:
    rng = np.random.default_rng(1913)
    pulses = 32
    unit = 0.18
    regular = list(range(0, pulses, 4))
    displaced = MD.accents(pulses, 8, rng)
    clips = []
    for accs in (regular, displaced):
        parts = []
        for i in range(pulses):
            parts.append((chord_hit(i in accs), i * unit, 0.0))
        clips.append(Clip(mix(parts, duration=pulses * unit + 0.8).y, SR).at_level(LEVEL))
    s_ = concat([clips[1], clips[0]], gap=1.2, names=["A", "B"])                 # A: displaced; B: regular
    return {"pulses": pulses, "regular": regular, "displaced": displaced, "unit": unit, "answer": "A",
            "off": {"regular": MD.off_share(regular), "displaced": MD.off_share(displaced)},
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("accents.quiz", s_, detail="one chord, repeated in even pulses (ours, on Part 7's bowed string): accents placed at random, then on every fourth pulse")}}


def compute_bartok() -> dict:
    groupings = [(2, 3), (2, 2, 3), (3, 3, 2), (2, 2, 2, 3)]
    unit = 0.13
    clips = []
    for g in groupings:
        parts = []
        t = 0
        for rep in range(4):
            for k, n in enumerate(g):
                parts.append((Clip(np.asarray(PC.drum(hz(45 if k == 0 else 52), seconds=0.4, at=0.4), float), SR).fade(0.0005, 0.05), t * unit, 0.0 if k == 0 else -5.0))
                for j in range(1, n):
                    parts.append((Clip(np.asarray(DK.woodblock(900.0, 0.1), float), SR), (t + j) * unit, -10.0))
                t += n
        clips.append(Clip(mix(parts, duration=t * unit + 0.6).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.9, names=["g5", "g7", "g8", "g9"])
    counts = {n: len(MD.additive(n)) for n in range(2, 17)}
    gold = {"window_88_1": MD.golden_window(88, 1), "p1": MD.golden_chance(88, 1, 1), "p5": MD.golden_chance(88, 1, 5),
            "p10_2": MD.golden_chance(88, 2, 10), "curve": [[m, MD.golden_chance(88, 1, m)] for m in range(1, 21)],
            "curve2": [[m, MD.golden_chance(88, 2, m)] for m in range(1, 21)], "fib": MD.fibonacci(12)}
    return {"groupings": [list(g) for g in groupings], "unit": unit, "starts": {k: float(s_.events[k]) for k in ("g5", "g7", "g8", "g9")},
            "counts": {str(k): v for k, v in counts.items()}, "golden": gold,
            "clips": {"four": save("bartok.four", s_, detail="additive rhythms, ours: 2+3, 2+2+3, 3+3+2 and 2+2+2+3 pulses, each four times, a low drum on each group's first pulse; Part 9's drums")}}


def compute_polychord() -> dict:
    mel = tune_line(n=14)
    unit = 0.42
    fs = [(54, 2 * i, 2) for i in range(8)] + [(58, 2 * i, 2) for i in range(8)] + [(61, 2 * i, 2) for i in range(8)]
    c = place([mel, fs], lambda m, s: piano(m, s), unit, gains=[0.0, -5.0])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["bi"])
    from explainer.music.monochord import key as K

    def best(notes):
        cor = K.correlations(K.distribution([p for p, _, _ in notes], [d for _, _, d in notes]))
        k = max(cor, key=cor.get)
        return {"key": list(k), "r": float(cor[k])}
    fit = {"melody": best(mel), "chords": best(fs), "both": best(mel + fs)}
    return {"melody": rows(mel), "chords": rows(fs), "unit": unit, "fit": fit,
            "clips": {"bi": save("polychord.bi", s_, detail="the Tune's first two phrases in C major over F sharp major chords, ours, Part 7's piano")}}


def compute_messiaen() -> dict:
    mode = MD.MESSIAEN[2]
    rhythm = (1, 2, 3, 2, 1)                                     # a palindrome, in sixteenths
    chords = [[60 + mode[(i + j) % 8] + 12 * ((i + j) // 8) for j in (0, 2, 4, 6)] for i in range(len(rhythm))]
    unit = 0.22
    lines, t = [], 0
    for r, ch in zip(rhythm, chords):
        for p in ch:
            lines.append((p, t, r))
        t += r
    seq = lines + [(p, a + t, d) for p, a, d in lines]
    c = place([seq], lambda m, s: piano(m, s, 0.9), unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["mode2"])
    counts = {n: MD.count_palindromes(n) for n in range(1, 17)}
    allc = {n: len(MD.compositions(n, (1, 2, 3, 4))) for n in range(1, 17)}
    return {"chords": chords, "rhythm": list(rhythm), "notes": rows(seq), "unit": unit, "palindromes": {str(k): v for k, v in counts.items()},
            "all": {str(k): v for k, v in allc.items()},
            "clips": {"mode2": save("messiaen.mode2", s_, detail="chords from Messiaen's second mode over a non-retrogradable rhythm (1-2-3-2-1 sixteenths), twice, ours; Part 7's piano")}}


def compute_tune() -> dict:
    mel = tune_line(n=14)
    wt = to_scale(mel, (0, 2, 4, 6, 8, 10))
    planed = MD.planed(wt, shape=(-4, -8))                       # augmented triads, planed: whole-tone through and through
    unit = 0.4
    c1 = place([wt] + planed, lambda m, s: piano(m, s, 1.0), unit, gains=[0.0, -5.0, -5.0])
    octm = to_scale(mel, (0, 2, 3, 5, 6, 8, 9, 11))                # the Tune on the octatonic, whole step first
    rng = np.random.default_rng(28)
    ost = []
    pat = [0, 3, 6, 9]
    for i in range(32):
        ost.append((36 + pat[i % 4] + (12 if i % 8 >= 4 else 0), 0.5 * i, 0.5))
    acc = sorted(set(int(x) for x in rng.choice(32, 9, replace=False)) | {0})
    c2m = place([[(p, a, d) for p, a, d in octm]], bowed, unit)
    parts = [(c2m, 0.0, 0.0)]
    for i, (p, a, d) in enumerate(ost):
        parts.append((piano(p, 0.5 * unit, 1.4 if i in acc else 0.6), a * unit, 0.0 if i in acc else -6.0))
    c2 = Clip(mix(parts, duration=16 * unit + 1.2).y, SR)
    s_ = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.2, names=["whole", "octa"])
    return {"whole": rows(wt), "planed": [rows(v) for v in planed], "octa": rows(octm), "ostinato": rows(ost), "accents": acc, "unit": unit,
            "starts": {k: float(s_.events[k]) for k in ("whole", "octa")}, "seconds": s_.duration,
            "notes": {"planed_chords": len(wt), "accents": len(acc), "ostinato": len(ost)},
            "clips": {"variation": save("tune.variation28", s_, detail="the Tune in whole-tone planing (augmented triads under every note), then on the octatonic scale (bowed) over an ostinato with accents placed at random (piano); ours")}}


def compute_variation() -> dict:
    t = load("tune")
    n = t["notes"]
    return {"part": 28, "title": r"in whole-tone planing, then over an octatonic ostinato with moving accents", "seconds": round(t["seconds"], 2),
            "measure": rf"{n['planed_chords']} augmented triads planed; {n['accents']} accents placed at random on {n['ostinato']} ostinato notes",
            "clip": "tune.variation28"}


def compute_slendro() -> dict:
    h = load("hook")
    bal = [(m, a, d) for m, a, d in h["balungan"]]
    sl_cents = MD.slendro()
    pent = [0, 200, 400, 700, 900]                                 # black keys from C sharp, as cents above it
    beat = 0.5
    def degree(m):
        c = round(((m - 62.0) * 100) % 1200, 3)
        k = min(range(5), key=lambda i: abs(sl_cents[i] - c))
        return k, int((m - 62.0) // 12)
    a_parts, b_parts, mapped = [], [], []
    for m, t, d in bal:
        k, o = degree(m)
        a_parts.append((Clip(PC.marimba(hz(m), seconds=1.2, tuned=False, soft=0.8), SR).fade(0.0005, 0.2).at_level(LEVEL), t * beat, 0.0))
        pm = 61 + 12 * o + pent[k] / 100.0
        mapped.append((pm, t, d))
        b_parts.append((piano(pm, beat * 1.2, 1.0), t * beat, 0.0))
    ca = Clip(mix(a_parts, duration=len(bal) * beat + 1.2).y, SR)
    cb = Clip(mix(b_parts, duration=len(bal) * beat + 1.2).y, SR)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.0, names=["slendro", "piano"])
    return {"slendro": rows(bal), "piano": rows(mapped), "beat": beat, "cents": {"slendro": sl_cents, "pentatonic": pent},
            "diff": [round(a - b, 1) for a, b in zip(sl_cents, pent)], "starts": {k: float(s_.events[k]) for k in ("slendro", "piano")},
            "clips": {"two": save("slendro.two", s_, detail="the hook's core melody on bars tuned to five equal steps, then on the piano's black keys; Part 9's bars and Part 7's piano")}}


def compute_modes() -> dict:
    unit = 0.22
    clips, lines = [], {}
    for k in (1, 2, 3):
        sc = [60 + p for p in MD.MESSIAEN[k]] + [72]
        ln = [(p, i, 1) for i, p in enumerate(sc)]
        lines[str(k)] = rows(ln)
        clips.append(place([ln], lambda m, s: piano(m, s), unit).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=["m1", "m2", "m3"])
    return {"lines": lines, "unit": unit, "starts": {k: float(s_.events[k]) for k in ("m1", "m2", "m3")},
            "clips": {"three": save("modes.three", s_, detail="Messiaen's first three modes of limited transposition, rising from C: whole-tone, octatonic, the nine-note third mode; Part 7's piano")}}


def compute_triads() -> dict:
    roots = [0, 3, 6, 9]
    unit = 0.5
    chords = []
    for i, r in enumerate(roots):
        for x in (0, 4, 7):
            chords.append((48 + r + x, 2 * i, 2))
    c = place([chords], lambda m, s: piano(m, s, 1.0), unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["four"])
    inside = all(MD.fits([r, r + 4, r + 7], MD.OCTATONIC) for r in roots)
    return {"chords": rows(chords), "unit": unit, "roots": roots, "inside": inside,
            "clips": {"four": save("triads.four", s_, detail="the four major triads of one octatonic scale, C, E flat, F sharp and A, in turn; Part 7's piano")}}


def compute_blocks() -> dict:
    unit = 0.16
    pats = {3: [60, 63, 67], 4: [72, 70, 67, 70], 5: [48, 48, 55, 53, 51]}
    total = 60
    lines = []
    for n, pat in pats.items():
        lines.append([(pat[i % n], i, 1) for i in range(total)])
    c = place(lines, lambda m, s: piano(m, s, 0.9), unit, gains=[-2.0, -1.0, 0.0])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["blocks"])
    return {"lines": [rows(v) for v in lines], "unit": unit, "periods": list(pats), "lcm": int(np.lcm.reduce(list(pats))),
            "clips": {"blocks": save("blocks.layers", s_, detail="three ostinatos of 3, 4 and 5 pulses layered, ours, until they realign after 60 pulses; Part 7's piano")}}


def compute_added() -> dict:
    unit = 0.18
    regular = [2, 2, 2, 2, 2, 2, 2, 2]
    added = [2, 2, 3, 2, 2, 2, 3, 2]                              # a sixteenth added in two places
    def drum_line(durs):
        parts, t = [], 0
        for d in durs:
            parts.append((Clip(np.asarray(DK.woodblock(900.0, 0.12), float), SR), t * unit, 0.0))
            t += d
        return Clip(mix(parts, duration=t * unit + 0.6).y, SR)
    s_ = concat([drum_line(regular).at_level(LEVEL), drum_line(added).at_level(LEVEL)], gap=1.0, names=["regular", "added"])
    return {"regular": regular, "added": added, "unit": unit, "starts": {k: float(s_.events[k]) for k in ("regular", "added")},
            "clips": {"two": save("added.two", s_, detail="eight even notes on a woodblock, then the same with a sixteenth added in two places (Messiaen's added value); Part 9's bars")}}


ITEMS = {"hook": compute_hook, "wholetone": compute_wholetone, "census": compute_census, "planing": compute_planing, "octatonic": compute_octatonic,
         "accents": compute_accents, "bartok": compute_bartok, "polychord": compute_polychord, "messiaen": compute_messiaen, "slendro": compute_slendro, "modes": compute_modes,
         "triads": compute_triads, "blocks": compute_blocks, "added": compute_added, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
