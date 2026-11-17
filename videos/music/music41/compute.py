"""Precompute everything numerical, and every sound, in Part 41 of *Music, Built* ("Orchestration").

    python -m videos.music.music41.compute              # everything missing (under a minute)
    python -m videos.music.music41.compute --force match

Numbers are cached in ``.cache/music41/<name>.json``, sounds in ``.cache/music41/audio/``.  The tools are Monochord's
(``explainer/music/monochord/orchestra.py``).  The orchestra is additive: each instrument's harmonic strengths were
measured on the series' physical models (Parts 7 and 8) and resynthesised, so any instrument can play any note quickly
(labelled synthesized); the trumpet's soft and loud notes are also heard straight from Part 8's lip-reed model.  Every
phrase is ours or the Tune; Ravel's Boléro is described and its instrumental idea reproduced, not quoted.

Items:
    hook        a phrase on a horn, then with a celesta and two piccolos on its 4th, 3rd and 5th harmonics (an ear
                question: how many instruments?)
    tour        the phrase on eight instruments, each in a comfortable register
    same        one note, C4, on eight instruments
    which       an ear question: which of three C4s is the clarinet?
    solo        a solo violin answered by the section
    build       Ravel's combination assembled one instrument at a time
    texture     the phrase in four textures
    cresc       a crescendo by orchestration: one, two, four, six instruments
    bright      the trumpet model blown softly and hard: the same note, darker and brighter
    section     a phrase on one violin, then on eight independent violins at the same level
    blend       flute, clarinet, both in unison; flute with a loud trumpet in unison
    spacing     a C major chord on strings: close and low, open, close and high
    klang       the Tune's first phrase with each note on a different instrument
    match       a sung `ah' on C3, then matched by one, two and four instruments (the solver)
    bell        a church bell as the target: what harmonic instruments cannot match
    registers   the clarinet model with the register hole closed and open
    swell       the trumpet model swelling from soft to hard breath
    sizes       a held note on 1, 2, 4, 8 and 16 violins at the same level
    octave      a phrase on violin, then with a flute an octave above
    space       a small timbre space: attack time and brightness
    tune        Variation 41: the Tune in eight orchestrations, the last matched to the vowel
    variation   the Variations ledger, row 41
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import orchestra as O
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import winds as W
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music41")
CLIPS = ClipStore("music41")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
_C: dict = {}


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def arr(y):
    return Clip(np.asarray(y, float), SR)


def inst(name, m, seconds, **kw):
    seconds = round(seconds, 2)
    return cached(("n", name, round(m, 2), seconds, tuple(sorted(kw.items()))), lambda: O.note(name, m, seconds, **kw))


def bounce(parts, end):
    return Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)


def tune_line(n=7, base=60):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def play_line(parts, mel, name, beat, start=0.0, shift=0, gain=0.0, **kw):
    for m, a, d in mel:
        parts.append((arr(inst(name, m + shift, d * beat * 0.97, **kw)), start + a * beat, gain))


# ---------------------------------------------------------------------------------------------------------- items
BOLERO = [("horn", 0, 0.0), ("celesta", 24, -8.0), ("piccolo", 19, -11.0), ("piccolo", 28, -13.0)]


def compute_hook() -> dict:
    mel = tune_line(7, 60)
    beat = 0.5
    parts, starts = [], {}
    starts["horn"] = 0.0
    play_line(parts, mel, "horn", beat, 0.0)
    t1 = 8 * beat + 1.0
    starts["four"] = t1
    for name, shift, g in BOLERO:
        play_line(parts, mel, name, beat, t1, shift, g)
    c = bounce(parts, t1 + 8 * beat + 1.2)
    f0 = O.hz(60)
    cents = {s: float(1200 * np.log2(O.hz(60 + s) / (k * f0))) for s, k in ((24, 4), (19, 3), (28, 5))}
    fus = O.fusion([(n, 60 + s, 10 ** (g / 20)) for n, s, g in BOLERO], f0, cents=20)
    return {"melody": [list(x) for x in mel], "beat": beat, "starts": starts, "parts": BOLERO, "cents_off": cents, "fusion": fus,
            "answer": 4, "clips": {"two": save_synth("hook.two", c, detail="a phrase on a horn, then with a celesta two octaves up and two piccolos a twelfth and two octaves and a third up, in the manner of Ravel's Boléro; additive instruments from the series' measured spectra")}}


def compute_bright() -> dict:
    out = []
    lv = {}
    for name, p in (("soft", 1.0), ("loud", 1.6)):
        y = W.lip_tone(W.trumpet(), 233.0, seconds=1.4, pressure=p)["sound"]
        y = np.asarray(y)
        n = len(y)
        t = np.arange(n) / SR
        y = y * np.clip(t / 0.03, 0, 1) * np.clip((1.4 - t) / 0.1, 0, 1)
        out.append(Clip(y, SR).at_level(LEVEL))
    c = concat(out, gap=0.6, names=["soft", "loud"])
    cents = {k: O.centroid(O.levels(n), 352.0) for k, n in (("soft", "trumpet p"), ("loud", "trumpet f"))}
    return {"centroid": cents, "profiles": {"soft": O.PROFILES["trumpet p"].tolist(), "loud": O.PROFILES["trumpet f"].tolist()},
            "starts": {k: float(c.events[k]) for k in ("soft", "loud")},
            "clips": {"two": save("bright.two", c, detail="Part 8's lip-reed trumpet model on one note, blown softly and then hard: louder and brighter")}}


def compute_same() -> dict:
    """One note, C4, on eight instruments in turn: timbre at a fixed pitch and loudness."""
    names = ["flute", "clarinet", "saxophone", "trumpet p", "horn", "violin", "cello", "celesta"]
    parts, starts, t = [], [], 0.0
    for n in names:
        starts.append(t)
        parts.append((arr(inst(n, 60, 1.1)), t, 0.0))
        t += 1.4
    c = bounce(parts, t + 0.4)
    return {"names": names, "starts": starts, "centroids": {n: (O.centroid(O.levels(n), O.hz(60)) if n != "celesta" else None) for n in names},
            "clips": {"eight": save_synth("same.eight", c, detail="C4 on flute, clarinet, saxophone, trumpet, horn, violin, cello and celesta in turn; additive from the measured spectra")}}


def compute_which() -> dict:
    """An ear question: three C4s at one level, violin, clarinet and flute; which is the clarinet?"""
    names = ["violin", "clarinet", "flute"]
    out = [Clip(np.asarray(inst(n, 60, 1.3), float), SR).at_level(LEVEL) for n in names]
    c = concat(out, gap=0.6, names=names)
    lv = {n: [round(float(20 * np.log10(max(x, 1e-4))), 1) for x in O.levels(n)[:6]] for n in names}
    return {"names": names, "answer": 2, "levels": lv, "starts": {n: float(c.events[n]) for n in names},
            "clips": {"three": save_synth("which.three", c, detail="C4 on a violin, a clarinet and a flute at the same level; additive from the measured spectra")}}


def compute_solo() -> dict:
    """A solo violin phrase answered by the section: the concerto's one against many."""
    mel = tune_line(7, 67)
    beat = 0.45
    parts = []
    play_line(parts, mel, "violin", beat, 0.0)
    t1 = 8 * beat + 0.3
    for m, a, d in mel:
        parts.append((arr(O.section("violin", m - 12, d * beat * 0.97, players=12, seed=int(m * 7 + a))), t1 + a * beat, 0.0))
        parts.append((arr(O.section("cello", m - 24, d * beat * 0.97, players=6, seed=int(m * 3 + a))), t1 + a * beat, -3.0))
    c = bounce(parts, t1 + 8 * beat + 0.8)
    return {"starts": {"solo": 0.0, "tutti": t1}, "beat": beat,
            "clips": {"two": save_synth("solo.two", c, detail="a phrase on one violin, answered an octave lower by twelve violins and six cellos; additive from the bowed-string spectrum")}}


def compute_registers() -> dict:
    """Part 8's clarinet model: the same bore blown with the register hole closed (the low register, on the bore's
    lowest mode) and open (the next mode up: a twelfth higher)."""
    out = []
    for hole in (False, True):
        d = W.reed_tone(W.clarinet(register_hole=hole), gamma=0.5, seconds=1.6)
        y = np.asarray(d["sound"])
        t = np.arange(len(y)) / SR
        y = y * np.clip((1.6 - t) / 0.1, 0, 1)
        out.append(Clip(y, SR).at_level(LEVEL))
    c = concat(out, gap=0.6, names=["low", "high"])
    f = {}
    for k, cl in zip(("low", "high"), out):
        y = cl.y[int(0.5 * SR): int(1.4 * SR)]
        S = np.abs(np.fft.rfft(y * np.hanning(len(y))))
        fr = np.fft.rfftfreq(len(y), 1 / SR)
        lo = fr > 60
        f[k] = float(fr[lo][np.argmax(S[lo])])
    return {"peak_hz": f, "starts": {k: float(c.events[k]) for k in ("low", "high")},
            "clips": {"two": save("registers.two", c, detail="Part 8's clarinet model with its register hole closed, then open: the same bore jumps a twelfth")}}


def compute_swell() -> dict:
    """Part 8's trumpet model with the breath rising steadily: one note growing louder and brighter."""
    n = int(3.2 * SR)
    d = W.lip_tone(W.trumpet(), 233.0, seconds=3.2, pressure=1.8)
    # a steady ramp of mouth pressure (the model takes a scalar pressure, so the ramp is made by crossfading three
    # breaths: soft, middle and hard), each its own physical simulation
    soft = np.asarray(W.lip_tone(W.trumpet(), 233.0, seconds=3.2, pressure=1.0)["sound"])
    mid = np.asarray(W.lip_tone(W.trumpet(), 233.0, seconds=3.2, pressure=1.35)["sound"])
    hard = np.asarray(d["sound"])
    t = np.linspace(0, 1, n)
    w1 = np.clip(1 - 2 * t, 0, 1)
    w3 = np.clip(2 * t - 1, 0, 1)
    w2 = 1 - w1 - w3
    yy = (w1 * soft[:n] * 0.4 + w2 * mid[:n] * 0.7 + w3 * hard[:n] * 1.0)
    tt = np.arange(n) / SR
    yy = yy * np.clip(tt / 0.04, 0, 1) * np.clip((3.2 - tt) / 0.1, 0, 1)
    c = Clip(yy / np.abs(yy).max(), SR)
    cen = []
    for k in range(8):
        seg = yy[int(k * n / 8): int((k + 1) * n / 8)]
        S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / SR)
        cen.append(float((fr * S).sum() / S.sum()))
    return {"centroids": cen, "clips": {"one": save("swell.one", c, detail="Part 8's trumpet model swelling from soft to hard breath on one note (three simulations crossfaded): louder and brighter together")}}


def compute_sizes() -> dict:
    mel_note = 67
    parts, starts, t = [], [], 0.0
    lv = []
    for n in (1, 2, 4, 8, 16):
        starts.append(t)
        y = O.section("violin", mel_note, 2.0, players=n, seed=n)
        lv.append(O.rms_db(y))
        parts.append((Clip(y / np.abs(y).max(), SR), t, 0.0))
        t += 2.5
    c = bounce(parts, t)
    return {"players": [1, 2, 4, 8, 16], "level_db": [x - lv[0] for x in lv], "starts": starts,
            "clips": {"five": save_synth("sizes.five", c, detail="one held G4 on 1, 2, 4, 8 and 16 violins, each version at the same level: the chorus grows; additive from the bowed-string spectrum")}}


def compute_octave() -> dict:
    mel = tune_line(7, 67)
    beat = 0.45
    parts, starts = [], {}
    starts["violin"] = 0.0
    play_line(parts, mel, "violin", beat, 0.0)
    t1 = 8 * beat + 0.8
    starts["octave"] = t1
    play_line(parts, mel, "violin", beat, t1)
    play_line(parts, mel, "flute", beat, t1, 12, -4.0)
    c = bounce(parts, t1 + 8 * beat + 0.8)
    return {"starts": starts, "beat": beat,
            "clips": {"two": save_synth("octave.two", c, detail="a phrase on violin, then with a flute an octave above; additive from the measured spectra")}}


def compute_section() -> dict:
    mel = tune_line(7, 67)
    beat = 0.5
    one, sec = [], []
    for m, a, d in mel:
        one.append((arr(inst("violin", m, d * beat * 0.97)), a * beat, 0.0))
        sec.append((arr(O.section("violin", m, d * beat * 0.97, players=8, seed=int(m + 10 * a))), a * beat, 0.0))
    y1 = Clip(mix(one, duration=8 * beat + 0.6).y, SR)
    y8 = Clip(mix(sec, duration=8 * beat + 0.6).y, SR)
    lvl1 = O.rms_db(y1.y)
    lvl8 = O.rms_db(y8.y)
    coherent = lvl1 + 20 * np.log10(8)
    c = concat([y1.at_level(LEVEL), y8.at_level(LEVEL)], gap=0.8, names=["one", "eight"])
    return {"players": 8, "one_db": lvl1, "eight_db": lvl8, "gain_db": lvl8 - lvl1, "coherent_gain_db": float(20 * np.log10(8)),
            "incoherent_gain_db": float(10 * np.log10(8)), "starts": {k: float(c.events[k]) for k in ("one", "eight")},
            "clips": {"two": save_synth("section.two", c, detail="a phrase on one violin, then on eight, each with its own small detuning, vibrato and timing, played at the same level; additive from the bowed-string model's spectrum")}}


def compute_blend() -> dict:
    """A held C5: flute, clarinet, both in unison at equal level; then flute with a trumpet 6 dB louder (as a trumpet
    playing forte is).  For each, the mix's brightness (spectral centroid) and the flute's share of the power."""
    m = 72
    pairs = [("flute", [("flute", 0.0)]), ("clarinet", [("clarinet", 0.0)]), ("flute+clarinet", [("flute", 0.0), ("clarinet", 0.0)]),
             ("flute+trumpet", [("flute", 0.0), ("trumpet f", 6.0)])]
    parts, starts, t = [], {}, 0.0
    stats = {}
    for name, members in pairs:
        starts[name] = t
        for inst_name, g in members:
            parts.append((arr(inst(inst_name, m, 1.6)), t, g))
        powers = {n: float((O.levels(n) ** 2).sum() / (O.levels(n) ** 2).sum() * 10 ** (g / 10)) for n, g in members}
        comp = sum((O.levels(n) * 10 ** (g / 20)) ** 2 for n, g in members)
        cen = float((O.hz(m) * np.arange(1, O.H + 1) * comp).sum() / comp.sum())
        tot = sum(powers.values())
        stats[name] = {"centroid": cen, "flute_share": powers.get("flute", 0.0) / tot,
                       "members": {n: O.centroid(O.levels(n), O.hz(m)) for n, _ in members}}
        t += 2.2
    c = bounce(parts, t + 0.4)
    return {"key": m, "starts": starts, "stats": stats,
            "clips": {"four": save_synth("blend.four", c, detail="a held C5 on flute, on clarinet, on both in unison, then on flute with a trumpet 6 dB louder; additive from the measured spectra")}}


TOUR = [("piccolo", 24), ("flute", 12), ("clarinet", 0), ("saxophone", -12), ("trumpet p", 0), ("horn", -12), ("violin", 12), ("cello", -12)]


def compute_tour() -> dict:
    """The Tune's first phrase on each instrument, placed in a comfortable part of its range."""
    mel = tune_line(7, 60)
    beat = 0.36
    parts, starts, t = [], [], 0.0
    for name, shift in TOUR:
        starts.append(t)
        play_line(parts, mel, name, beat, t, shift)
        t += 8 * beat + 0.5
    c = bounce(parts, t + 0.3)
    base = {n: n.split()[0] for n, _ in TOUR}
    return {"tour": TOUR, "starts": starts, "beat": beat, "ranges": {n: O.RANGES[base[n]] for n, _ in TOUR if base[n] in O.RANGES},
            "clips": {"tour": save_synth("tour.eight", c, detail="the Tune's first phrase on piccolo, flute, clarinet, saxophone, trumpet, horn, violin and cello in turn; additive from the measured spectra")}}


def compute_build() -> dict:
    """Ravel's combination assembled one instrument at a time: horn; + celesta (4th harmonic); + piccolo (3rd);
    + piccolo (5th)."""
    mel = tune_line(7, 60)
    beat = 0.45
    parts, starts, t = [], [], 0.0
    for k in range(1, 5):
        starts.append(t)
        for name, shift, g in BOLERO[:k]:
            play_line(parts, mel, name, beat, t, shift, g)
        t += 8 * beat + 0.8
    c = bounce(parts, t + 0.4)
    return {"starts": starts, "beat": beat, "steps": [b[0] for b in BOLERO],
            "clips": {"four": save_synth("build.four", c, detail="a phrase on a horn, then with a celesta, then a piccolo on the third harmonic, then another on the fifth, added one at a time")}}


TEXTURES = ["unison", "melody and accompaniment", "chorale", "counterpoint"]


def compute_texture() -> dict:
    mel = tune_line(7, 72)
    beat = 0.45
    parts, starts, t = [], {}, 0.0
    chords = {0: [48, 55, 64], 2: [48, 55, 64], 4: [53, 57, 65], 6: [48, 55, 64]}
    for kind in TEXTURES:
        starts[kind] = t
        if kind == "unison":
            play_line(parts, mel, "violin", beat, t, -12)
            play_line(parts, mel, "clarinet", beat, t, -12, -3.0)
            play_line(parts, mel, "cello", beat, t, -24, -2.0)
        elif kind == "melody and accompaniment":
            play_line(parts, mel, "flute", beat, t)
            for a, ch in chords.items():
                for k in range(2):
                    for m in ch[1:]:
                        parts.append((arr(inst("violin", m, beat * 0.8)), t + (a + k) * beat, -10.0))
                parts.append((arr(inst("cello", ch[0] - 12, 2 * beat * 0.95)), t + a * beat, -5.0))
        elif kind == "chorale":
            for a, ch in chords.items():
                top = [m for m, aa, d in mel if aa == a]
                for m, name in zip(ch + top, ("cello", "horn", "horn", "trumpet p")):
                    parts.append((arr(inst(name, m, 2 * beat * 0.97)), t + a * beat, -3.0))
        else:
            play_line(parts, mel, "clarinet", beat, t)
            play_line(parts, mel, "cello", beat, t + 2 * beat, -24, -1.0)
            play_line(parts, mel, "flute", beat, t + 4 * beat, 12, -3.0)
        t += (12 if kind == "counterpoint" else 8) * beat + 0.8
    c = bounce(parts, t + 0.4)
    return {"textures": TEXTURES, "starts": starts, "beat": beat,
            "clips": {"four": save_synth("texture.four", c, detail="the Tune's first phrase in four textures: three instruments in octaves, flute over string accompaniment, a brass chorale, and a three-part canon; additive instruments")}}


CRESC = [[("clarinet", 0, 0.0)], [("clarinet", 0, 0.0), ("violin", 12, -3.0)],
         [("clarinet", 0, -2.0), ("violin", 12, -3.0), ("horn", -12, -3.0), ("cello", -12, -4.0)],
         [("piccolo", 24, -8.0), ("flute", 12, -4.0), ("violin", 12, -2.0), ("trumpet f", 0, -3.0), ("horn", -12, -3.0), ("cello", -24, -2.0)]]


def compute_cresc() -> dict:
    """Boléro's plan in miniature: one phrase four times, with more instruments each time (the clip is not
    levelled per pass, so the growth is heard)."""
    mel = tune_line(7, 60)
    beat = 0.42
    parts, starts, t = [], [], 0.0
    for k, recipe in enumerate(CRESC):
        starts.append(t)
        for name, shift, g in recipe:
            play_line(parts, mel, name, beat, t, shift, g - 9.0 + 3.0 * k)
        t += 8 * beat + 0.3
    c = bounce(parts, t + 0.8)
    return {"starts": starts, "beat": beat, "sizes": [len(r) for r in CRESC],
            "clips": {"four": save_synth("cresc.four", c, detail="a phrase four times, with one, two, four and six instruments, growing louder: a crescendo by orchestration")}}


SPACINGS = {"close, low": [36, 40, 43], "open": [36, 43, 52], "close, high": [72, 76, 79]}


def compute_spacing() -> dict:
    parts, starts, t = [], {}, 0.0
    rough = {}
    for name, notes in SPACINGS.items():
        starts[name] = t
        for m in notes:
            parts.append((arr(O.section("cello" if m < 55 else "violin", m, 2.2, players=4, seed=m)), t, 0.0))
        rough[name] = O.voicing_roughness(notes, "violin")
        t += 2.8
    c = bounce(parts, t + 0.3)
    return {"voicings": SPACINGS, "roughness": rough, "starts": starts,
            "clips": {"three": save_synth("spacing.three", c, detail="a C major chord on string sections: close and low, open, close and high; additive from the bowed-string model's spectrum")}}


KLANG = ["flute", "clarinet", "horn", "violin", "saxophone", "cello", "trumpet p"]


def compute_klang() -> dict:
    mel = tune_line(7, 60)
    beat = 0.55
    parts = []
    for (m, a, d), name in zip(mel, KLANG):
        parts.append((arr(inst(name, m + (12 if name in ("flute",) else 0) - (12 if name == "cello" else 0), d * beat * 1.05)), a * beat, 0.0))
    t1 = 8 * beat + 0.8
    play_line(parts, mel, "clarinet", beat, t1)
    c = bounce(parts, t1 + 8 * beat + 0.8)
    c.events = {"klang": 0.0, "one": t1}
    return {"melody": [list(x) for x in mel], "beat": beat, "instruments": KLANG, "starts": {"klang": 0.0, "one": t1},
            "clips": {"two": save_synth("klang.two", c, detail="the Tune's first phrase with each note on a different instrument, then all on the clarinet; additive from the measured spectra")}}


BELL = [(0.5, -6.0), (1.0, 0.0), (1.2, -3.0), (1.5, -6.0), (2.0, -4.0), (2.5, -10.0), (2.61, -12.0), (3.0, -14.0), (4.0, -16.0)]   # a church bell's partials (Part 9)


def compute_bell() -> dict:
    """A bell as a target: Part 9's church-bell partials (hum, prime, minor-third tierce, quint, nominal ...).  The
    solver can only offer harmonic spectra, and the bell's minor third is not a harmonic."""
    f0 = O.hz(60)
    target = [(f0 * r, 10 ** (db / 20)) for r, db in BELL]
    res = {b: O.match(target, f0 / 2, budget=b) for b in (1, 4)}
    from explainer.music.monochord.instruments import percussion as PC
    bell = PC.bell(f0, seconds=2.5)
    parts = [(arr(bell / np.abs(bell).max()), 0.0, 0.0)]
    t = 3.0
    for ch in res[4]["chosen"]:
        parts.append((arr(inst(ch["instrument"], ch["key"], 2.2)), t, 20 * np.log10(max(ch["gain"], 1e-3)) / 2))
    c = bounce(parts, t + 2.6)
    return {"errors": {str(b): r["error_db"] for b, r in res.items()}, "chosen": res[4]["chosen"], "starts": {"bell": 0.0, "match": t},
            "vowel_error": load("match")["results"]["4"]["error_db"],
            "clips": {"two": save_synth("bell.two", c, detail="Part 9's church bell on C4, then the solver's best four instruments: the bell's minor-third partial cannot be matched by harmonic instruments")}}


def compute_space() -> dict:
    """A small timbre space of our orchestra: attack time and brightness (centroid at C4) for each instrument."""
    att = {"flute": 0.06, "clarinet": 0.06, "saxophone": 0.06, "trumpet p": 0.03, "trumpet f": 0.02, "horn": 0.05, "violin": 0.06,
           "cello": 0.06, "piccolo": 0.06, "celesta": 0.001, "harp": 0.003}
    pts = {}
    for name, a in att.items():
        if name == "celesta":
            cen = float(sum(O.hz(60) * r * 10 ** (db / 10) for r, db in O.CELESTA) / sum(10 ** (db / 10) for r, db in O.CELESTA))
        elif name == "harp":
            cen = O.centroid(O.levels("violin") * 10 ** (-np.arange(O.H) / 20), O.hz(60))
        else:
            cen = O.centroid(O.levels(name), O.hz(60))
        pts[name] = {"attack_ms": a * 1000, "centroid": cen}
    return {"points": pts}


def compute_match() -> dict:
    f0 = O.hz(48)
    target = O.vowel_target(f0=f0)
    results = {b: O.match(target, f0, budget=b) for b in (1, 2, 4)}
    voice = CH.sing([(48, 0.0, 2.2)], "bass", "a", seed=1)
    parts = [(arr(voice / np.abs(voice).max()), 0.0, 0.0)]
    starts = {"voice": 0.0}
    t = 3.0
    for b in (1, 2, 4):
        starts[str(b)] = t
        for ch in results[b]["chosen"]:
            parts.append((arr(inst(ch["instrument"], ch["key"], 2.2)), t, 20 * np.log10(max(ch["gain"], 1e-3)) / 2))
        t += 3.0
    c = bounce(parts, t + 0.2)
    return {"f0": f0, "target_bands": results[4]["target_bands"], "results": {str(b): r for b, r in results.items()},
            "edges": O.ERB_EDGES.tolist(), "starts": starts,
            "clips": {"four": save_synth("match.four", c, detail="a sung `ah' on C3 by Part 17's model voice, then the solver's matches with one, two and four instruments from our orchestra")}}


ORCH = [   # eight orchestrations of the Tune's first phrase: (title, [(instrument, transposition, gain dB)])
    ("strings", [("violin", 12, 0.0), ("violin", 7, -6.0), ("cello", -12, -4.0)]),
    ("woodwinds", [("flute", 12, 0.0), ("clarinet", 0, -3.0)]),
    ("brass", [("trumpet p", 0, 0.0), ("horn", -12, -2.0)]),
    ("flute and clarinet in unison", [("flute", 12, 0.0), ("clarinet", 12, -2.0)]),
    ("horn, celesta and piccolos (Ravel's idea)", [(n, s, g) for n, s, g in BOLERO]),
    ("a melody of timbres", "klang"),
    ("tutti in octaves", [("piccolo", 24, -6.0), ("flute", 12, -3.0), ("violin", 12, 0.0), ("trumpet f", 0, -4.0), ("cello", -12, -3.0), ("horn", 0, -6.0)]),
    ("matched to the vowel `ah'", "match"),
]


def compute_tune() -> dict:
    mel = tune_line(7, 60)
    beat = 0.45
    parts, starts, t = [], [], 0.0
    m4 = load("match")["results"]["4"]["chosen"]
    for title, recipe in ORCH:
        starts.append(t)
        if recipe == "klang":
            for (m, a, d), name in zip(mel, KLANG):
                parts.append((arr(inst(name, m + (12 if name == "flute" else 0) - (12 if name == "cello" else 0), d * beat * 1.05)), t + a * beat, 0.0))
        elif recipe == "match":
            # each Tune note voiced like the vowel: the matched instruments on the same harmonics of each note
            for m, a, d in mel:
                for ch in m4:
                    k = ch["harmonic"]
                    mm = int(round(m - 12 + 12 * np.log2(k)))
                    parts.append((arr(inst(ch["instrument"], mm, d * beat * 0.97)), t + a * beat, 20 * np.log10(max(ch["gain"], 1e-3)) / 2))
        else:
            for name, shift, g in recipe:
                play_line(parts, mel, name, beat, t, shift, g)
        t += 8 * beat + 0.7
    c = bounce(parts, t + 0.4)
    return {"titles": [x for x, _ in ORCH], "starts": starts, "beat": beat, "melody": [list(x) for x in mel], "seconds": c.duration,
            "match": m4, "clips": {"variation": save_synth("tune.variation41", c, detail="the Tune's first phrase in eight orchestrations, the last matched by the solver to a sung `ah'; additive instruments from the series' measured spectra")}}


def compute_variation() -> dict:
    t = load("tune")
    m = load("match")["results"]
    return {"part": 41, "title": "in eight orchestrations, the last matched to a vowel", "seconds": round(t["seconds"], 1),
            "measure": f"the vowel matched within {m['4']['error_db']:.1f} dB a band by four instruments, {m['1']['error_db']:.1f} dB by one",
            "clip": "tune.variation41"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation41", 41)


ITEMS = {"hook": compute_hook, "same": compute_same, "which": compute_which, "solo": compute_solo, "registers": compute_registers, "swell": compute_swell, "sizes": compute_sizes, "octave": compute_octave,
         "space": compute_space, "tour": compute_tour, "build": compute_build, "texture": compute_texture, "cresc": compute_cresc, "bright": compute_bright, "section": compute_section, "blend": compute_blend, "spacing": compute_spacing,
         "klang": compute_klang, "match": compute_match, "tune": compute_tune, "bell": compute_bell, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
