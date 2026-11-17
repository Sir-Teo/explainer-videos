"""Precompute everything numerical, and every sound, in Part 50 of *Music, Built* ("Dynamics, Distortion and Pitch").

    python -m videos.music.music50.compute              # everything missing (about two minutes)
    python -m videos.music.music50.compute --force hook

Numbers are cached in ``.cache/music50/<name>.json``, sounds in ``.cache/music50/audio/``.  The tools are Monochord's
(``explainer/music/monochord/dynamics.py``).  The voice is Part 8's source-filter voice; the guitar Part 40's; the drums
Part 40's; the piano Part 7's.  Every shaper, compressor, stretcher and pitch corrector is computed here.

Items:
    hook        an ear question: the Tune sung a little out of tune, then hard-tuned; which was corrected?
    shapers     harmonics of a sine through a hard clip, tanh and a cubic; a Chebyshev shaper's exact harmonics
    fuzz        a riff on Part 40's guitar, clean then through a hard-driven shaper
    imd         a fifth and a major third through the same shaper: the difference tones
    alias       an ear question: a sweep through a hard clip at 48 kHz, plainly and 8 times oversampled; aliasing measured,
                with antiderivative antialiasing too
    curves      a compressor's static curves and its response to a step
    comp        an ear question: a drum groove plain and compressed, matched in loudness
    pump        the groove compressed hard with a fast release (pumping) and a slow one
    duck        a bass ducked by the kick through a sidechain
    stretch     the Tune twice as long, by overlap-add and by the phase vocoder
    pitch       Part 8's voice shifted up a fifth by resampling and by PSOLA
    correct     the out-of-tune voice's pitch track, and the corrector's targets at three speeds
    vocoder     a sung line as modulator, a chord as carrier, and the vocoded result; ring modulation
    shapers3    one guitar note through the hard clip, tanh and the cubic shaper
    cheblevels  a Chebyshev shaper fed a tone at three levels: quiet is purer, loud is brighter
    gate        a snare track with hiss between the hits, plain and gated
    speeds      the out-of-tune voice corrected slowly, faster and instantly
    tune50      Variation 50: the Tune sung, hard-tuned, vocoded and stretched eightfold
    variation   the Variations ledger, row 50
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import resample_poly

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import dynamics as D
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music50")
CLIPS = ClipStore("music50")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BEAT = 0.5


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def tune_notes(phrases=(0,), base=60, detune=0.0, seed=50, beat=BEAT):
    """The Tune as sung notes (key, start, seconds); with ``detune``, each note off by up to that many semitones."""
    rng = np.random.default_rng(seed)
    out = []
    for e in T.events(beat, list(phrases)):
        off = rng.uniform(-detune, detune) if detune else 0.0
        out.append((base + MAJOR[e["degree"]] + off, e["t"], e["dur"]))
    return out


def sung(notes, vowel="a", part="soprano"):
    y = CH.sing(notes, part, vowel)
    return 0.5 * y / np.max(np.abs(y))


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


# ---------------------------------------------------------------------------------------------------------- items
def correct_voice(y, speed_ms=0.0):
    tt, f0, conf = D.yin(y, SR)
    tg = D.correct(f0, tt, speed_ms=speed_ms)
    ratio = np.where((f0 > 0) & (tg > 0), tg / np.maximum(f0, 1.0), 1.0)
    return D.psola(y, SR, tt, f0, ratio), tt, f0, tg


def compute_hook() -> dict:
    y = sung(tune_notes(detune=0.45))
    z, tt, f0, tg = correct_voice(y, 0.0)
    t2, f2, _ = D.yin(z, SR)
    c = concat([C(y), C(z)], gap=1.0, names=["first", "second"])
    v = (f0 > 0) & (tg > 0)
    before = float(np.median(np.abs(1200 * np.log2(f0[v] / tg[v]))))
    tg2 = np.interp(t2, tt, tg)
    v2 = (f2 > 0) & (tg2 > 0)
    after = float(np.median(np.abs(1200 * np.log2(f2[v2] / tg2[v2]))))
    return {"answer": "second", "before_cents": before, "after_cents": after,
            "t": tt[::2].tolist(), "f0": f0[::2].tolist(), "target": tg[::2].tolist(), "t2": t2[::2].tolist(), "f2": f2[::2].tolist(),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("hook.two", c, detail="the Tune's first phrase sung by Part 8's voice with every note up to 45 cents off, then corrected instantly to the C major scale by PSOLA")}}


def compute_shapers() -> dict:
    t = np.arange(SR) / SR
    x = np.cos(2 * np.pi * 1000 * t)
    out = {k: D.harmonics(D.shape(x, k, 3.0), 1000, SR, 9) for k in ("hard", "tanh", "cubic")}
    amps = [1.0, 0.0, 0.5, 0.0, 0.25]
    out["cheb_amps"] = amps
    out["cheb"] = D.harmonics(D.cheb_shaper(amps, x), 1000, SR, 6)
    xs = np.linspace(-1.5, 1.5, 200)
    out["curves"] = {"x": xs.tolist(), "hard": np.clip(xs * 1.0, -1, 1).tolist(), "tanh": np.tanh(1.5 * xs).tolist(),
                     "cubic": (lambda y: 1.5 * y - 0.5 * y ** 3)(np.clip(xs, -1, 1)).tolist()}
    return out


RIFF = [(40, 0.0, 0.3), (40, 0.3, 0.3), (43, 0.6, 0.3), (45, 0.9, 0.6), (40, 1.5, 0.3), (40, 1.8, 0.3), (47, 2.1, 0.3), (45, 2.4, 0.6)]


def compute_fuzz() -> dict:
    p = [(arr(P40.guitar(m, d * 0.95)), a, 0.0) for m, a, d in RIFF]
    clean = mix(p, duration=3.4).y
    clean = 0.5 * clean / np.max(np.abs(clean))
    fz = P40.drive(clean, 10.0)
    fz = 0.5 * fz / np.max(np.abs(fz))
    c = concat([C(clean), C(fz)], gap=0.8, names=["clean", "fuzz"])
    return {"starts": {"clean": float(c.events["clean"]), "fuzz": float(c.events["fuzz"])}, "riff": [list(r) for r in RIFF],
            "clips": {"two": save("fuzz.two", c, detail="a riff on Part 40's electric guitar, clean, then through a hard-driven tanh shaper and a speaker's band limit")}}


def compute_imd() -> dict:
    t = np.arange(SR) / SR
    out = {}
    for name, (f1, f2) in {"fifth": (220.0, 330.0), "third": (220.0, 275.0)}.items():
        x = 0.5 * np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)
        y = np.tanh(4 * x)
        w = np.hanning(len(y))
        Y = 20 * np.log10(np.abs(np.fft.rfft(y * w)) + 1e-9)
        f = np.fft.rfftfreq(len(y), 1 / SR)
        keep = f <= 1400
        Y = Y - Y.max()
        peaks = []
        for k in range(1, len(f) - 1):
            if keep[k] and Y[k] > -45 and Y[k] >= Y[k - 1] and Y[k] >= Y[k + 1]:
                peaks.append([float(f[k]), float(Y[k])])
        out[name] = {"f1": f1, "f2": f2, "peaks": peaks, "gcd": float(math.gcd(int(f1), int(f2)))}
    chords = []
    for keys in ([40, 47, 52], [40, 44, 47, 52]):
        g = sum(arr(P40.guitar(m, 1.6)).y[: int(1.6 * SR)] for m in keys)
        chords.append(C(P40.drive(g, 10.0)))
    c = concat(chords, gap=0.8, names=["power", "major"])
    out["starts"] = {"power": float(c.events["power"]), "major": float(c.events["major"])}
    out["clips"] = {"two": save("imd.two", c, detail="Part 40's guitar, distorted: a power chord (E, B, E) then an E major chord (E, G sharp, B, E)")}
    return out


def compute_alias() -> dict:
    secs = 5.0
    t = np.arange(int(secs * SR)) / SR
    f0, f1 = 500.0, 6000.0
    ph = 2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * secs))
    x = 0.9 * np.sin(ph) * np.clip(t / 0.05, 0, 1) * np.clip((secs - t) / 0.1, 0, 1)
    naive = np.clip(3 * x, -1, 1)
    os_ = resample_poly(np.clip(3 * resample_poly(x, 8, 1), -1, 1), 1, 8)[: len(x)]
    c = concat([C(0.4 * naive), C(0.4 * os_)], gap=1.0, names=["first", "second"])
    tt = np.arange(SR) / SR
    tone = 0.9 * np.sin(2 * np.pi * 3733 * tt)
    meas = {"plain": D.alias_energy(np.tanh(4 * tone), 3733, SR), "adaa": D.alias_energy(D.adaa_tanh(tone, 4), 3733, SR),
            "x8": D.alias_energy(resample_poly(np.tanh(4 * resample_poly(tone, 8, 1)), 1, 8), 3733, SR)}
    return {"answer": "first", "f0": f0, "f1": f1, "seconds": secs, "measure": meas,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("alias.two", c, detail="a sine sweeping from 500 Hz to 6 kHz through a hard clip, computed at 48 kHz, then computed 8 times oversampled")}}


def compute_curves() -> dict:
    lv = np.linspace(-60, 0, 121)
    curves = {str(r): D.static_curve(lv, -20, r, 6).tolist() for r in (2, 4, 10)}
    t = np.arange(int(1.2 * SR)) / SR
    x = np.where(t < 0.4, 0.05, 0.8) * np.sin(2 * np.pi * 220 * t)
    x = np.where(t > 0.8, 0.05 * np.sin(2 * np.pi * 220 * t), x)
    r = D.compressor(x, SR, -20, 4, 6, 5, 120)
    gr = r["gr_db"]
    i0, i1 = int(0.4 * SR), int(0.8 * SR)
    att = float(np.argmax(gr[i0:] > 0.9 * gr[i1 - 10]) / SR * 1000)
    rel = float(np.argmax(gr[i1:] < 0.1 * gr[i1 - 10]) / SR * 1000)
    return {"levels": lv.tolist(), "curves": curves, "gr": gr[::120].tolist(), "env": np.abs(x)[::120].tolist(), "attack_ms": att,
            "release_ms": rel, "steady_gr": float(gr[i1 - 10]), "threshold": -20, "knee": 6}


def groove(bars=4, bpm=96):
    parts = []
    P40.drums(parts, "funk", bpm, bars, gain=0.0)
    beat = 60 / bpm
    for b in range(bars):
        for i, m in enumerate([36, 36, 39, 41]):
            parts.append((arr(P38.bass(m, beat * 0.85)), (4 * b + i) * beat, -3.0))
    y = mix(parts, duration=bars * 4 * beat + 0.5).y
    return 0.5 * y / np.max(np.abs(y))


def spread(y, win_ms=20.0):
    """How much the short-term level wanders: the 95th minus the 10th percentile of 20 ms levels, silence left out."""
    L = D.short_term_levels(y, SR, win_ms)
    L = L[L > -60]
    return float(np.percentile(L, 95) - np.percentile(L, 10))


def compute_comp() -> dict:
    g = groove()
    r = D.compressor(g, SR, threshold=-24, ratio=6, knee=6, attack_ms=3, release_ms=80)
    y = norm_rms(r["y"])
    gg = norm_rms(g)
    m = max(np.max(np.abs(y)), np.max(np.abs(gg)))
    y, gg = 0.9 * y / m, 0.9 * gg / m
    c = concat([C(gg), C(y)], gap=1.0, names=["first", "second"])
    return {"answer": "second", "crest": {"plain": D.crest_db(gg), "compressed": D.crest_db(y)},
            "levels": {"plain": D.short_term_levels(gg, SR).tolist(), "compressed": D.short_term_levels(y, SR).tolist()},
            "spread": {"plain": spread(gg), "compressed": spread(y)},
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("comp.two", c, detail="a funk groove on Part 40's drums with a plucked bass, plain, then compressed (6:1 above -24 dB, 3 ms attack, 80 ms release), both at the same average loudness")}}


def compute_pump() -> dict:
    g = groove()
    out = []
    for rel in (25.0, 400.0):
        r = D.compressor(g, SR, threshold=-30, ratio=10, knee=3, attack_ms=2, release_ms=rel)
        out.append(C(0.9 * norm_rms(r["y"]) / max(np.max(np.abs(norm_rms(r["y"]))), 1e-9)))
    c = concat(out, gap=1.0, names=["fast", "slow"])
    return {"starts": {"fast": float(c.events["fast"]), "slow": float(c.events["slow"])},
            "clips": {"two": save("pump.two", c, detail="the groove compressed hard (10:1 above -30 dB, 2 ms attack) with a 25 ms release, then a 400 ms release")}}


def compute_duck() -> dict:
    bpm = 120
    beat = 60 / bpm
    kick = np.zeros(int(4 * 4 * beat * SR) + SR // 2)
    parts = []
    for b in range(16):
        k = arr(P40.kick()).y
        i = int(b * beat * SR)
        kick[i:i + len(k)] += k[: len(kick) - i]
    pad = arr(P40.pad([0, 4, 7], 4 * 4 * beat + 0.4, base=48, bright=3000)).y
    pad = np.r_[pad, np.zeros(len(kick) - len(pad))][: len(kick)]
    r = D.compressor(pad, SR, threshold=-30, ratio=20, knee=3, attack_ms=2, release_ms=150, sidechain=kick)
    a = 0.5 * kick / np.max(np.abs(kick)) + 0.4 * pad / np.max(np.abs(pad))
    b = 0.5 * kick / np.max(np.abs(kick)) + 0.4 * r["y"] / np.max(np.abs(pad))
    c = concat([C(a), C(b)], gap=1.0, names=["plain", "ducked"])
    return {"gr": r["gr_db"][: int(4 * beat * SR):240].tolist(), "beat": beat,
            "starts": {"plain": float(c.events["plain"]), "ducked": float(c.events["ducked"])},
            "clips": {"two": save_synth("duck.two", c, detail="a kick on every beat with a sustained pad, then with the pad's compressor keyed by the kick (a sidechain): the pad ducks and swells")}}


def piano_tune(phrases=(0,), beat=0.42):
    p = []
    for e in T.events(beat, list(phrases)):
        p.append((arr(P38.piano(60 + MAJOR[e["degree"]], e["dur"] * 0.95, 0.75)), e["t"], 0.0))
    y = mix(p, duration=T.events(beat, list(phrases))[-1]["t"] + 1.0).y
    return 0.5 * y / np.max(np.abs(y))


def compute_stretch() -> dict:
    x = sung(tune_notes())[: int(3.8 * SR)]
    a = D.ola_stretch(x, 2.0)
    b = D.pv_stretch(x, 2.0)
    c = concat([C(x), C(0.5 * a / np.max(np.abs(a))), C(0.5 * b / np.max(np.abs(b)))], gap=0.8, names=["original", "ola", "pv"])
    return {"starts": {k: float(c.events[k]) for k in ("original", "ola", "pv")},
            "clips": {"three": save_synth("stretch.three", c, detail="the Tune's first phrase sung by Part 8's voice; then twice as long by overlap-add; then twice as long by the phase vocoder with phase locking")}}


def compute_pitch() -> dict:
    x = sung(tune_notes(phrases=(0,)))[: int(3.8 * SR)]
    up = 2 ** (7 / 12)
    rs = resample_poly(x, 2, 3)
    tt, f0, _ = D.yin(x, SR)
    ps = D.psola(x, SR, tt, f0, np.full(len(tt), up))
    c = concat([C(x), C(rs), C(ps)], gap=0.8, names=["original", "resampled", "psola"])
    return {"ratio": up, "durations": {"original": len(x) / SR, "resampled": len(rs) / SR, "psola": len(ps) / SR},
            "starts": {k: float(c.events[k]) for k in ("original", "resampled", "psola")},
            "clips": {"three": save_synth("pitch.three", c, detail="Part 8's voice singing the Tune's first phrase; raised a fifth by playing it faster (resampling); raised a fifth by PSOLA, keeping its length and its vowel")}}


def compute_correct() -> dict:
    y = sung(tune_notes(detune=0.45))
    tt, f0, _ = D.yin(y, SR)
    out = {"t": tt.tolist(), "f0": f0.tolist()}
    for sp in (0.0, 60.0, 250.0):
        out[str(int(sp))] = D.correct(f0, tt, speed_ms=sp).tolist()
    return out


def vowel_line(notes, vowels):
    parts = []
    for (m, a, d), v in zip(notes, vowels):
        parts.append((Clip(CH.sing([(m, 0.0, d)], "tenor", v), SR), a, 0.0))
    y = mix(parts, duration=max(a + d for _, a, d in notes) + 0.4).y
    return 0.6 * y / np.max(np.abs(y))


def saw_chord(keys, seconds):
    t = np.arange(int(seconds * SR)) / SR
    y = np.zeros(len(t))
    for m in keys:
        f = 440 * 2 ** ((m - 69) / 12)
        for k in range(1, int(8000 / f)):
            y += np.sin(2 * np.pi * k * f * t) / k
    return 0.5 * y / np.max(np.abs(y))


def compute_vocoder() -> dict:
    notes = tune_notes(base=48)
    vowels = ["a", "i", "u", "E", "O", "a", "i"]
    mod = vowel_line(notes, vowels)
    car = saw_chord([48, 52, 55, 60], len(mod) / SR)
    v = D.vocoder(mod, car, SR, bands=16)
    rm = D.ring(mod, SR, 300.0)
    c = concat([C(mod), C(car[: int(2.0 * SR)]), C(v["y"] * 0.5), C(0.5 * rm / np.max(np.abs(rm)))], gap=0.8, names=["voice", "carrier", "vocoded", "ring"])
    return {"edges": v["edges"], "envs": v["envs"], "vowels": vowels, "starts": {k: float(c.events[k]) for k in ("voice", "carrier", "vocoded", "ring")},
            "clips": {"four": save_synth("vocoder.four", c, detail="Part 8's voice singing the Tune's first phrase on changing vowels; a sawtooth chord; the chord vocoded by the voice in 16 bands; the voice ring-modulated by 300 Hz")}}


def compute_shapers3() -> dict:
    g = arr(P40.guitar(45, 1.8)).y
    g = g / np.max(np.abs(g))
    clips = []
    for k in ("hard", "tanh", "cubic"):
        y = D.shape(g, k, 5.0)
        clips.append(C(0.5 * y / np.max(np.abs(y))))
    c = concat(clips, gap=0.6, names=["hard", "tanh", "cubic"])
    return {"starts": {k: float(c.events[k]) for k in ("hard", "tanh", "cubic")},
            "clips": {"three": save("shapers3.three", c, detail="one note on Part 40's guitar driven five times into a hard clip, a tanh and a cubic soft clip, with no speaker filter")}}


def compute_cheblevels() -> dict:
    amps = [1.0, 0.0, 0.5, 0.0, 0.25, 0.0, 0.15]
    t = np.arange(int(1.5 * SR)) / SR
    env = np.clip(t / 0.02, 0, 1) * np.clip((1.5 - t) / 0.1, 0, 1)
    clips, spec = [], {}
    for lv in (0.25, 0.6, 1.0):
        x = lv * np.cos(2 * np.pi * 220 * t)
        y = D.cheb_shaper(amps, x)
        spec[str(lv)] = D.harmonics(y[: SR], 220, SR, 7)
        clips.append(C(0.5 * y / np.max(np.abs(y)) * env))
    c = concat(clips, gap=0.6, names=["quiet", "middle", "full"])
    return {"amps": amps, "spec": spec, "starts": {k: float(c.events[k]) for k in ("quiet", "middle", "full")},
            "clips": {"three": save_synth("cheblevels.three", c, detail="a 220 Hz cosine at a quarter, 0.6 and full amplitude through a Chebyshev shaper designed for harmonics 1, 3, 5, 7 at full amplitude; each played at the same peak level")}}


def compute_gate() -> dict:
    rng = np.random.default_rng(5)
    x = np.zeros(int(4.0 * SR))
    for k in range(6):
        sn = arr(P40.snare(k % 3)).y
        i = int(k * 0.6 * SR)
        x[i:i + len(sn)] += 0.6 * sn[: len(x) - i] / np.max(np.abs(sn))
    x += 0.006 * rng.standard_normal(len(x))
    y = D.gate(x, SR, threshold=-36, ratio=10, attack_ms=0.5, release_ms=60)
    c = concat([C(x), C(y)], gap=0.8, names=["plain", "gated"])
    return {"floor_db": float(20 * np.log10(0.006)), "starts": {"plain": float(c.events["plain"]), "gated": float(c.events["gated"])},
            "levels": {"plain": D.short_term_levels(x, SR, 20).tolist(), "gated": D.short_term_levels(y, SR, 20).tolist()},
            "clips": {"two": save("gate.two", c, detail="six snare hits from Part 40 over a steady hiss, plain, then through a gate (threshold -36 dB, ratio 10, 60 ms release)")}}


def compute_speeds() -> dict:
    y = sung(tune_notes(detune=0.45))
    clips = []
    for sp in (250.0, 60.0, 0.0):
        z, *_ = correct_voice(y, sp)
        clips.append(C(z))
    c = concat(clips, gap=0.8, names=["slow", "fast", "instant"])
    return {"starts": {k: float(c.events[k]) for k in ("slow", "fast", "instant")},
            "clips": {"three": save_synth("speeds.three", c, detail="Part 8's voice singing the Tune's first phrase a little out of tune, corrected with a 250 ms glide, a 60 ms glide, and instantly")}}


def compute_tune50() -> dict:
    y = sung(tune_notes(detune=0.45))
    z, *_ = correct_voice(y, 0.0)
    notes = tune_notes(base=48)
    mod = vowel_line(notes, ["a", "i", "u", "E", "O", "a", "i"])
    car = saw_chord([48, 52, 55, 60], len(mod) / SR)
    vc = D.vocoder(mod, car, SR, bands=16)["y"] * 0.5
    head = sung(tune_notes())[: int(1.0 * SR)]
    st = D.pv_stretch(head, 8.0)
    st = 0.5 * st / np.max(np.abs(st))
    names = ["sung", "tuned", "vocoded", "stretched"]
    c = concat([C(y), C(z), C(vc), C(st)], gap=0.7, names=names)
    tt, f0, _ = D.yin(y, SR)
    tg = D.correct(f0, tt)
    t2, f2, _ = D.yin(z, SR)
    tg2 = np.interp(t2, tt, tg)
    v1 = (f0 > 0) & (tg > 0)
    v2 = (f2 > 0) & (tg2 > 0)
    return {"names": names, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in names},
            "before": float(np.median(np.abs(1200 * np.log2(f0[v1] / tg[v1])))), "after": float(np.median(np.abs(1200 * np.log2(f2[v2] / tg2[v2])))),
            "stretched_s": len(st) / SR,
            "clips": {"variation50": save_synth("tune.variation50", c, detail="the Tune's first phrase sung by Part 8's voice a little out of tune; hard-tuned by PSOLA; vocoded onto a sawtooth chord; and its first second stretched eightfold by the phase vocoder")}}


def compute_variation() -> dict:
    t = load("tune50")
    return {"part": 50, "title": "sung, hard-tuned, vocoded and stretched eightfold", "seconds": round(t["seconds"], 1),
            "measure": f"median pitch error {t['before']:.0f} cents sung, {t['after']:.1f} after correction; one second stretched to {t['stretched_s']:.1f}",
            "clip": "tune.variation50"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation50", 50)


ITEMS = {"hook": compute_hook, "shapers": compute_shapers, "fuzz": compute_fuzz, "imd": compute_imd, "alias": compute_alias,
         "curves": compute_curves, "comp": compute_comp, "pump": compute_pump, "duck": compute_duck, "stretch": compute_stretch, "pitch": compute_pitch,
         "correct": compute_correct, "vocoder": compute_vocoder, "shapers3": compute_shapers3, "cheblevels": compute_cheblevels, "gate": compute_gate,
         "speeds": compute_speeds, "tune50": compute_tune50, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
