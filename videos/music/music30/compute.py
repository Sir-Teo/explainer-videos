"""Precompute everything numerical, and every sound, in Part 30 of *Music, Built* ("Sound Itself").

    python -m videos.music.music30.compute              # everything missing (a few minutes: the brass model)
    python -m videos.music.music30.compute --force phasing

Numbers are cached in ``.cache/music30/<name>.json``, sounds in ``.cache/music30/audio/``.  The measures are Monochord's
(``explainer/music/monochord/soundmass.py``).  The music of this era is in copyright, so every sound here is ours, made
from the series' own instruments: Part 1's string, Part 7's piano and bowed string, Part 8's lips and bore, Part 9's
bells, bars and drums, Part 17's voice.

Items:
    hook        a closed groove of our own: one short fragment of struck and bowed sounds, looped
    tape        a bell, then reversed, then at half speed, then with its attack cut (an ear question)
    chance      the Tune's notes in an order and rhythm chosen by dice
    phasing     a twelve-note figure against itself, one copy slightly faster; its twelve alignments counted
    studie      sine-tone mixtures on the scale of Stockhausen's Studie II (steps of the 25th root of 5)
    clouds      a Poisson cloud of plucks and an evenly spaced one (an ear question); counts per second against Poisson's law
    gliss       a cloud of glissandi, ours
    sieves      the whole-tone, octatonic and diatonic sieves; a sieve that does not repeat at the octave, played
    mass        a cluster of bowed strings a quarter tone apart, growing; its beat rates
    spectral    a brass tone from Part 8's lips on a long bore, then its spectrum orchestrated (an ear question)
    speeds      the Tune's first phrase on tape at normal, double and half speed
    density     a cloud whose Poisson rate rises from 1 to 24 notes a second
    spread      the same eight bowed strings as a cluster, then spread as an open chord
    additive    a five-note figure growing by one note at each repeat, as in Glass
    buildup     the brass tone's harmonics entering one at a time, then the brass tone itself
    unitgen     a unit-generator patch: an oscillator, then with an envelope, then through a filter
    tune        Variation 30: phased against itself; a cloud of glissandi following it; its notes as partials of a string
    variation   the Variations ledger, row 30
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import soundmass as S
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.instruments import winds as W
from explainer.music.monochord.instruments.plucked import plucked as pluck
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music30")
CLIPS = ClipStore("music30")
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
    key = (round(m, 3), round(min(seconds, 4.0), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 4.0), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.02, 0.1).at_level(LEVEL)
    return _V[key]


def plucked(m: float, seconds: float = 1.2) -> Clip:
    return Clip(BOARD.play(pluck(hz(m), seconds=seconds, beta=0.11))).fade(0.001, 0.15).at_level(LEVEL)


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


def tune_line(base: int = 72, n: int = 14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def gliss_tone(p0: float, p1: float, seconds: float, partials: int = 5) -> np.ndarray:
    """A string-like glissando: a few harmonics whose frequency slides from key p0 to p1."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    f = hz(p0) * 2 ** ((p1 - p0) / 12 * t / seconds)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = sum((0.7 ** k) * np.sin((k + 1) * ph) for k in range(partials))
    env = np.minimum(1, t / 0.15) * np.minimum(1, (seconds - t) / 0.3)
    return y * env


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    rng = np.random.default_rng(1948)
    frag = []
    for i, t in enumerate(np.arange(0, 1.6, 0.2)):
        y = DK.woodblock(700.0 + 150 * (i % 3), 0.15) if i % 2 == 0 else PC.drum(hz(40 + 3 * (i % 4)), seconds=0.35, at=0.3)
        frag.append((Clip(np.asarray(y, float), SR).fade(0.0005, 0.05), float(t + rng.uniform(0, 0.03)), -2.0 if i % 2 else 0.0))
    frag.append((bowed(43, 1.6), 0.0, -6.0))
    seg = Clip(mix(frag, duration=1.6).y, SR)
    y = S.loop(seg.y, 8)
    s_ = concat([Clip(y, SR).fade(0.01, 0.3).at_level(LEVEL)], gap=0.0, names=["groove"])
    return {"fragment": 1.6, "loops": 8, "events": [[float(t), float(g)] for _, t, g in frag],
            "clips": {"groove": save("hook.groove", s_, detail="a closed groove of our own: a 1.6-second fragment of Part 9's woodblock and drum over a low bowed note, looped eight times")}}


def compute_tape() -> dict:
    bell = PC.bell(hz(67), seconds=3.0)
    b = np.asarray(bell, float)
    parts = {"bell": b, "reversed": S.reverse(b), "half": S.speed(b, 0.5)[: int(4.0 * SR)], "cut": S.cut_attack(b, 0.25)}
    order = ["cut", "reversed", "bell", "half"]                    # A, B, C, D: the untouched bell is C
    s_ = concat([Clip(parts[k], SR).fade(0.001, 0.2).at_level(LEVEL) for k in order], gap=0.8, names=order)
    return {"order": order, "starts": {k: float(s_.events[k]) for k in order}, "attack": {k: S.attack_time(parts[k]) for k in order},
            "env": {k: [float(x) for x in np.abs(parts[k])[:: SR // 50][:200]] for k in order}, "answer": "C",
            "clips": {"four": save("tape.four", s_, detail="a bell from Part 9 four ways: with its first quarter-second cut off, reversed, untouched, and at half speed (an octave lower)")}}


def compute_chance() -> dict:
    rng = np.random.default_rng(1951)
    pcs = sorted({p for p, _, _ in tune_line(n=14)})
    notes, t = [], 0.0
    for _ in range(20):
        p = int(rng.choice(pcs)) + 12 * int(rng.integers(-1, 2))
        d = float(rng.choice([0.5, 1, 1.5, 2, 3]))
        rest = float(rng.choice([0, 0, 0.5, 1]))
        notes.append((p, t, d))
        t += d + rest
    unit = 0.35
    c = place([notes], piano, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["dice"])
    return {"notes": rows(notes), "unit": unit, "pitches": pcs,
            "clips": {"dice": save("chance.dice", s_, detail="the Tune's own notes, in an order, register, length and spacing chosen by dice; Part 7's piano")}}


FIG = [72, 74, 76, 72, 74, 76, 79, 76, 74, 72, 74, 76]          # ours, from the Tune's first notes


def compute_phasing() -> dict:
    pats = S.phase_patterns([p % 12 for p in FIG])
    unit = 0.16
    loops = 14
    faster = 1 + 1 / (len(FIG) * 4)                             # gains one note every four loops
    a, b = S.drift_times(len(FIG), unit, faster, loops)
    pa = [(piano(FIG[i % len(FIG)], unit * 1.6, 0.9), t, -1.0) for i, t in enumerate(a)]
    pb = [(piano(FIG[i % len(FIG)] + 0.0, unit * 1.6, 0.9), t, -1.0) for i, t in enumerate(b)]
    c = Clip(mix(pa + pb, duration=a[-1] + 1.5).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["phase"])
    shift = [float((t2 - t1) / unit) for t1, t2 in zip(a[:: len(FIG)], b[:: len(FIG)])]
    return {"figure": FIG, "patterns": [{"shift": p["shift"], "unisons": p["unisons"], "distinct": p["distinct"]} for p in pats],
            "unit": unit, "loops": loops, "faster": faster, "seconds": float(a[-1] + 1.5), "drift": shift,
            "clips": {"phase": save("phasing.phase", s_, detail="a twelve-note figure of our own on Part 7's piano, twice: the second copy a little faster, so that it drifts a note ahead every four loops")}}


def compute_clouds() -> dict:
    rng = np.random.default_rng(1955)
    seconds, rate = 8.0, 5.0
    on = S.poisson_onsets(rate, seconds, rng)
    even = np.linspace(0, seconds, len(on), endpoint=False)
    pitches = rng.uniform(60, 84, len(on))
    def cloud(times):
        parts = [(plucked(float(round(p))), float(t), -3.0) for t, p in zip(times, pitches)]
        return Clip(mix(parts, duration=seconds + 1.2).y, SR).at_level(LEVEL)
    s_ = concat([cloud(on), cloud(even)], gap=1.2, names=["A", "B"])
    long_on = S.poisson_onsets(rate, 600.0, rng)
    counts = S.counts_per_cell(long_on, 600.0, 1.0)
    hist = np.bincount(counts, minlength=14)[:14]
    expect = [600 * S.poisson_pmf(k, rate) for k in range(14)]
    gaps = np.diff(np.concatenate([[0], on]))
    return {"onsets": on.tolist(), "even": even.tolist(), "pitches": pitches.tolist(), "rate": rate, "seconds": seconds,
            "hist": hist.tolist(), "expect": expect, "gap_cv": float(np.std(gaps) / np.mean(gaps)), "answer": "A",
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("clouds.quiz", s_, detail="two clouds of the same plucked notes from Part 1's string: one at Poisson times (gaps exponential), one evenly spaced")}}


def compute_gliss() -> dict:
    rng = np.random.default_rng(1954)
    gl = S.glissandi(40, 12.0, 45, 90, rng)
    y = np.zeros(int(13.5 * SR))
    for g in gl:
        seg = gliss_tone(g["p0"], g["p1"], g["t1"] - g["t0"]) * 0.08
        i = int(g["t0"] * SR)
        y[i:i + len(seg)] += seg[: len(y) - i]
    s_ = concat([Clip(y, SR).fade(0.05, 0.6).at_level(LEVEL)], gap=0.0, names=["cloud"])
    return {"glissandi": gl, "seconds": 12.0,
            "clips": {"cloud": save("gliss.cloud", s_, kind="synthesized", detail="forty glissandi with random starts, lengths and slopes, ours, each a few harmonics sliding together (additive synthesis)")}}


def compute_sieves() -> dict:
    sv = [[(5, 0)], [(7, 2)]]
    keys = S.sieve(sv, 36)
    unit = 0.24
    line = [(48 + k, i, 1) for i, k in enumerate(keys)]
    c = place([line], piano, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["sieve"])
    gaps = [b - a for a, b in zip(keys, keys[1:])]
    return {"whole": S.sieve(S.WHOLE_TONE_SIEVE), "octatonic": S.sieve(S.OCTATONIC_SIEVE), "diatonic": S.sieve(S.DIATONIC_SIEVE),
            "diatonic_terms": S.DIATONIC_SIEVE, "nonoctave": keys, "gaps": gaps, "period": 35, "line": rows(line), "unit": unit,
            "clips": {"sieve": save("sieves.nonoctave", s_, detail="the sieve 5n or 7n+2 over three octaves from C3: a scale that repeats only every 35 semitones; Part 7's piano")}}


def compute_mass() -> dict:
    pitches = S.cluster(62.0, 3.5, 8)
    parts = []
    for i, p in enumerate(pitches):
        parts.append((bowed(p, 6.0 - 0.5 * i), 0.5 * i, -2.0))
    c = Clip(mix(parts, duration=7.5).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["mass"])
    return {"pitches": [float(p) for p in pitches], "beats": S.beat_rates(pitches), "entry": 0.5,
            "clips": {"mass": save("mass.cluster", s_, detail="eight bowed strings half a semitone apart, entering one by one: a cluster that beats; Part 7's bowed string")}}


def compute_spectral() -> dict:
    bore = W.trumpet(tube=2.75, radius=0.0069, bell=0.6, bell_radius=0.1)
    d = W.lip_tone(bore, 100.0, 2.4, attack=0.06)
    tone = np.asarray(d["sound"], float)
    f0 = W.playing(d["p"], tail=0.4)["hz"]
    lv = S.harmonic_levels(tone, f0, 16)
    notes = S.orchestrate(f0, lv, floor_db=-36.0)
    parts = []
    for n in notes:
        g = (n["db"]) * 0.5
        if n["inst"] == "piano":
            c = piano(n["key"], 3.0, 0.8)
        elif n["inst"] == "bowed":
            c = bowed(n["key"], 3.0)
        else:
            y = CH.sing([(n["key"], 0.0, 3.0)], "soprano", "u")
            c = Clip(y / max(np.abs(y).max(), 1e-9) * 0.5, SR).fade(0.05, 0.3).at_level(LEVEL)
        parts.append((c, 0.0, g))
    chord = Clip(mix(parts, duration=3.6).y, SR)
    tclip = Clip(tone, SR).fade(0.01, 0.3)
    s_ = concat([tclip.at_level(LEVEL), chord.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"f0": f0, "levels": lv, "notes": notes, "answer": "B", "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("spectral.quiz", s_, kind="synthesized", detail="a brass tone from Part 8's lips on a long bore, then its harmonics given to an ensemble: piano, bowed strings and a synthetic voice")}}


def compute_tune() -> dict:
    rng = np.random.default_rng(30)
    head = tune_line(n=7)
    unit = 0.2
    loops = 6
    n = len(head)
    beats = [(p, a, d) for p, a, d in head]
    total = 8.0
    faster = 1 + 1 / (8 * 3)
    pa, pb = [], []
    for L in range(loops):
        for p, a, d in beats:
            pa.append((piano(p, d * unit, 0.9), (L * total + a) * unit, -1.0))
            pb.append((piano(p, d * unit, 0.9), (L * total + a) * unit / faster, -1.0))
    c1 = Clip(mix(pa + pb, duration=loops * total * unit + 1.0).y, SR)
    mel = tune_line(n=14)
    seconds = 9.0
    def target(t):
        k = min(int(t / seconds * 16), 15)
        for p, a, d in mel:
            if a <= k < a + d:
                return p
        return mel[-1][0]
    gl = S.glissandi(30, seconds, 55, 90, rng, max_len=1.6, target=target)
    y = np.zeros(int((seconds + 1.5) * SR))
    for g in gl:
        seg = gliss_tone(g["p0"], g["p1"], g["t1"] - g["t0"]) * 0.1
        i = int(g["t0"] * SR)
        y[i:i + len(seg)] += seg[: len(y) - i]
    c2 = Clip(y, SR).fade(0.05, 0.5)
    f0 = hz(36)                                                    # C2: the Tune's notes as its partials 8 to 13.5 ...
    part = {72: 8, 74: 9, 76: 10, 77: 11, 79: 12, 81: 13}
    unit3 = 0.42
    drone = Clip(BOARD.play(pluck(f0, seconds=7.5, beta=0.11))).fade(0.001, 0.4).at_level(LEVEL)
    pp = [(drone, 0.0, -4.0)]
    keys = []
    for p, a, d in mel:
        h = part[p]
        k = S.harmonic_key(h, f0)
        keys.append((k, a, d, h))
        pp.append((plucked(k, d * unit3 + 0.6), a * unit3, 0.0))
    c3 = Clip(mix(pp, duration=16 * unit3 + 2.0).y, SR)
    s_ = concat([c1.at_level(LEVEL), Clip(c2.y, SR).at_level(LEVEL), c3.at_level(LEVEL)], gap=1.2, names=["phase", "cloud", "partials"])
    return {"head": rows(head), "loops": loops, "faster": faster, "unit": unit, "glissandi": gl, "cloud_seconds": seconds,
            "partials": [[float(k), float(a), float(d), int(h)] for k, a, d, h in keys], "unit3": unit3,
            "cents": {str(h): float(100 * (S.harmonic_key(h, f0) - p)) for p, h in part.items()},
            "starts": {k: float(s_.events[k]) for k in ("phase", "cloud", "partials")}, "seconds": s_.duration,
            "notes": {"glissandi": len(gl), "partials": len(keys)},
            "clips": {"variation": save("tune.variation30", s_, kind="synthesized",
                                        detail="the Tune's first phrase phased against itself (Part 7's piano); a cloud of glissandi drawn to its first two phrases (additive synthesis); the phrases played on the harmonics of Part 1's low C string")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 30, "title": r"phased against itself, as a cloud of glissandi, and on the harmonics of a string", "seconds": round(t["seconds"], 2),
            "measure": rf"{t['notes']['glissandi']} glissandi; on C's harmonics the Tune's A is {t['cents']['13']:+.0f} cents and its F {t['cents']['11']:+.0f} cents from the piano's",
            "clip": "tune.variation30"}


def compute_studie() -> dict:
    step = 5 ** (1 / 25)
    base = 100.0
    freqs = [base * step ** k for k in range(81)]
    rng = np.random.default_rng(1954)
    mixtures = []
    y = np.zeros(int(9.0 * SR))
    t = 0.0
    for j in range(5):
        k0 = int(rng.integers(10, 60))
        spread = int(rng.integers(1, 5))
        ks = [k0 + spread * i for i in range(5)]
        dur = float(rng.choice([0.8, 1.2, 1.6]))
        n = int(dur * SR)
        tt = np.arange(n) / SR
        env = np.minimum(1, tt / 0.02) * np.exp(-tt * float(rng.uniform(0.5, 2.5)))
        seg = sum(np.sin(2 * np.pi * freqs[k] * tt) for k in ks) * env / 5
        i = int(t * SR)
        y[i:i + n] += seg[: len(y) - i]
        mixtures.append({"t": t, "ks": ks, "hz": [freqs[k] for k in ks], "dur": dur})
        t += dur + 0.35
    s_ = concat([Clip(y[: int((t + 0.5) * SR)], SR).fade(0.01, 0.3).at_level(LEVEL)], gap=0.0, names=["studie"])
    return {"step_cents": 1200 * np.log2(step), "freqs": freqs[:: 10], "mixtures": mixtures, "n_freqs": 81,
            "clips": {"studie": save("studie.mixtures", s_, kind="synthesized", detail="five mixtures of five sine tones each, ours, on the scale of Stockhausen's Studie II: 81 frequencies from 100 Hz, each the 25th root of 5 above the last")}}


def compute_speeds() -> dict:
    mel = tune_line(n=7)
    base = place([mel], piano, 0.4)
    y = base.y
    parts = {"normal": y, "double": S.speed(y, 2.0), "half": S.speed(y, 0.5)}
    order = ["normal", "double", "half"]
    s_ = concat([Clip(parts[k], SR).fade(0.005, 0.2).at_level(LEVEL) for k in order], gap=0.8, names=order)
    return {"order": order, "starts": {k: float(s_.events[k]) for k in order}, "durations": {k: len(parts[k]) / SR for k in order},
            "melody": rows(mel),
            "clips": {"three": save("speeds.three", s_, detail="the Tune's first phrase on Part 7's piano, then the same recording at double speed and at half speed")}}


def compute_density() -> dict:
    rng = np.random.default_rng(1957)
    seconds = 12.0
    t, on = 0.0, []
    while t < seconds:                                            # a Poisson process whose rate rises linearly
        lam = 1.0 + 23.0 * t / seconds
        t += rng.exponential(1.0 / lam)
        if t < seconds:
            on.append(t)
    pitches = rng.uniform(55, 90, len(on))
    parts = [(plucked(float(round(p)), 0.8), float(x), -6.0) for x, p in zip(on, pitches)]
    c = Clip(mix(parts, duration=seconds + 1.0).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["rise"])
    counts = S.counts_per_cell(np.array(on), seconds, 1.0)
    return {"onsets": on, "pitches": pitches.tolist(), "seconds": seconds, "counts": counts.tolist(),
            "clips": {"rise": save("density.rise", s_, detail="a cloud of plucks from Part 1's string whose Poisson rate rises from 1 to 24 notes a second over twelve seconds")}}


def compute_spread() -> dict:
    cl = S.cluster(62.0, 3.5, 8)
    op = [38, 45, 52, 59, 64, 69, 74, 79]                        # fifths and fourths: an open chord
    a = Clip(mix([(bowed(p, 3.5), 0.0, -2.0) for p in cl], duration=4.0).y, SR)
    b = Clip(mix([(bowed(p, 3.5), 0.0, -2.0) for p in op], duration=4.0).y, SR)
    s_ = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["cluster", "open"])
    return {"cluster": [float(p) for p in cl], "open": op, "starts": {k: float(s_.events[k]) for k in ("cluster", "open")},
            "beats_open": S.beat_rates(op)[:3],
            "clips": {"two": save("spread.two", s_, detail="eight bowed strings as a cluster half a semitone apart, then the same eight spread in fifths and fourths; Part 7's bowed string")}}


def compute_additive() -> dict:
    fig = [72, 76, 79, 76, 74]
    seq, t = [], 0.0
    for k in range(1, len(fig) + 1):
        for rep in range(2):
            for p in fig[:k]:
                seq.append((p, t, 1))
                t += 1
    unit = 0.17
    c = place([seq], lambda m, s: piano(m, s, 0.9), unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["grow"])
    return {"figure": fig, "notes": rows(seq), "unit": unit, "lengths": list(range(1, len(fig) + 1)),
            "clips": {"grow": save("additive.grow", s_, detail="a five-note figure of our own, played twice at each length from one note to five, as in Philip Glass's additive process; Part 7's piano")}}


def compute_buildup() -> dict:
    sp = load("spectral")
    notes = sp["notes"]
    gap = 0.45
    parts = []
    for i, n in enumerate(notes):
        dur = 0.6 + gap * (len(notes) - i)
        if n["inst"] == "piano":
            c = piano(n["key"], dur, 0.8)
        elif n["inst"] == "bowed":
            c = bowed(n["key"], dur)
        else:
            y = CH.sing([(n["key"], 0.0, dur)], "soprano", "u")
            c = Clip(y / max(np.abs(y).max(), 1e-9) * 0.5, SR).fade(0.05, 0.2).at_level(LEVEL)
        parts.append((c, gap * i, n["db"] * 0.5))
    total = gap * len(notes) + 1.0
    ch = Clip(mix(parts, duration=total + 0.5).y, SR)
    s_ = concat([ch.at_level(LEVEL)], gap=0.0, names=["build"])
    return {"notes": [{"harmonic": n["harmonic"], "inst": n["inst"], "key": n["key"]} for n in notes], "gap": gap,
            "clips": {"build": save("buildup.harmonics", s_, kind="synthesized", detail="the brass tone's sixteen harmonics entering one at a time, lowest first, each on the ensemble's instrument for its register")}}


def compute_unitgen() -> dict:
    f = 220.0
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    saw = 2 * ((f * t) % 1.0) - 1                                  # an oscillator: a sawtooth
    env = np.minimum(1, t / 0.01) * np.exp(-2.2 * t)               # an envelope generator
    y1 = saw * 0.5
    y2 = saw * env
    cutoff = 300 + 3000 * np.exp(-3.0 * t)                         # a low-pass filter whose cutoff falls
    y3 = np.zeros(n)
    z = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * cutoff[i] / SR)
        z = (1 - a) * y2[i] + a * z
        y3[i] = z
    s_ = concat([Clip(y, SR).fade(0.005, 0.1).at_level(LEVEL) for y in (y1, y2, y3)], gap=0.7, names=["osc", "env", "filter"])
    return {"f": f, "starts": {k: float(s_.events[k]) for k in ("osc", "env", "filter")},
            "wave": [float(x) for x in saw[: int(SR * 3 / f)]], "env": [float(x) for x in env[:: SR // 50]],
            "clips": {"three": save("unitgen.three", s_, kind="synthesized", detail="a unit-generator patch at 220 Hz: a sawtooth oscillator alone, then shaped by a decaying envelope, then through a low-pass filter whose cutoff falls")}}


ITEMS = {"hook": compute_hook, "tape": compute_tape, "chance": compute_chance, "phasing": compute_phasing, "studie": compute_studie, "clouds": compute_clouds,
         "gliss": compute_gliss, "sieves": compute_sieves, "mass": compute_mass, "spectral": compute_spectral, "speeds": compute_speeds, "density": compute_density,
         "spread": compute_spread, "additive": compute_additive, "buildup": compute_buildup, "unitgen": compute_unitgen, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
