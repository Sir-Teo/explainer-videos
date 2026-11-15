"""Precompute everything numerical, and every sound, in Part 52 of *Music, Built* ("Synthesis II: FM, Grains and
Physical Models").

    python -m videos.music.music52.compute              # everything missing (about two minutes)
    python -m videos.music.music52.compute --force hook

Numbers are cached in ``.cache/music52/<name>.json``, sounds in ``.cache/music52/audio/``.  The tools are Monochord's
(``explainer/music/monochord/synth2.py``); the piano is Part 7's, the voice Part 8's, the bell Part 9's and the
finite-difference string Part 1's and Part 7's.

Items:
    hook        an ear question: a bell from two sine oscillators (Chowning's FM) and Part 9's bell from its measured
                partials; which used two oscillators?
    vib2fm      a vibrato whose rate rises from 4 Hz to 220 Hz at a fixed depth, until it is no longer vibrato
    bessel      FM's lines predicted by Bessel functions and measured; an index sweep heard
    ratios      four carrier-to-modulator ratios; their lines; three heard
    chowning    Chowning's brass, bell and drum (1973)
    dx          a DX-style engine: an electric piano, a feedback bass and a bell; feedback's sawtooth measured
    gabor       Gabor's grains: bandwidth against length
    grains      Part 8's voice frozen, stretched, shifted and scattered into a cloud
    spectral    Part 7's piano note as sinusoids and a residual; its inharmonicity; resynthesized harmonic
    sampler     one piano sample stretched over four octaves against the piano computed at each note
    ks          Karplus-Strong untuned and tuned by an all-pass: errors in cents; a high phrase heard both ways
    waveguide   the waveguide against the finite-difference string, sample for sample
    clarinet    a waveguide clarinet: its threshold, its odd harmonics, a crescendo and the Tune
    modal       a stiff, damped string by finite differences and by modes: the scheme's dispersion; an ear question
    costs       each method timed for one second of sound
    tune52      Variation 52: the Tune on FM keys and bells, dissolved into grains and back
    variation   the Variations ledger, row 52
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.signal import resample_poly, stft
from scipy.special import jv

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import dynamics as D
from explainer.music.monochord import synth as S1
from explainer.music.monochord import synth2 as F
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics import string as STR
from videos.music.music38 import compute as P38

CACHE = Cache("music52")
CLIPS = ClipStore("music52")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
save_pm = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BEAT = 0.5
arr = P38.arr


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def tune_notes(phrases=(0,), base=60, beat=BEAT):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def norm(y, peak=0.5):
    y = np.asarray(y, float)
    return peak * y / (np.max(np.abs(y)) + 1e-12)


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def fade(y, a=0.003, r=0.03):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


def spec_rows(y, lo=50.0, hi=8000.0, rows=110, nper=2048, hop=480):
    f, t, Z = stft(y, SR, nperseg=nper, noverlap=nper - hop)
    P = 20 * np.log10(np.abs(Z) + 1e-9)
    r = np.geomspace(lo, hi, rows)
    out = np.array([np.interp(r, f, P[:, j]) for j in range(P.shape[1])]).T
    return (out - out.max()).tolist()


# ---------------------------------------------------------------------------------------------------------- FM
def exp_env(n, tau, sr=SR):
    return np.exp(-np.arange(n) / sr / tau)


def fm_bell(f, seconds=5.0, ratio=1.4, imax=10.0, tau=1.6):
    """Chowning's bell: carrier and modulator in the ratio 1 : 1.4, the index and the amplitude dying together."""
    n = int(seconds * SR)
    e = exp_env(n, tau)
    return fade(F.fm(f, ratio * f, imax * e, n) * e * np.clip(np.arange(n) / (0.002 * SR), 0, 1))


def fm_brass(f, seconds, imax=5.0):
    n = int(seconds * SR)
    e = F.env_adsr(n, SR, 0.06, 0.12, 0.75, 0.1, max(seconds - 0.15, 0.05))
    return fade(F.fm(f, f, imax * e, n) * e)


def fm_drum(f=80.0, seconds=0.6, imax=25.0):
    n = int(seconds * SR)
    e = exp_env(n, 0.05)
    return fade(F.fm(f, f * 55 / 80, imax * exp_env(n, 0.02), n) * e)


def compute_hook() -> dict:
    a = fm_bell(hz(67), 5.0)
    b = PC.bell(hz(67), 5.0)
    c = concat([C(norm_rms(b)), C(norm_rms(a))], gap=1.0, names=["first", "second"])
    f = hz(67)
    pred = [(float(fr), float(abs(am))) for fr, am in F.sidebands(f, 1.4 * f, 10.0 * math.exp(-0.25 / 1.6), 12) if 0 < fr < 6000]
    return {"answer": "second", "f": f, "fm_lines": pred, "bell": PC.bell_partials(f),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="G4 on Part 9's tuned bell (its measured partials), then on two sine oscillators in Chowning's ratio 1 : 1.4, the modulation index dying with the note")}}


def compute_vib2fm() -> dict:
    secs = 9.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    rate = 4.0 * (220.0 / 4.0) ** (t / secs)
    pm = 2 * np.pi * np.cumsum(rate) / SR
    inst = 440.0 + 60.0 * np.cos(pm)
    y = np.sin(2 * np.pi * np.cumsum(inst) / SR) * np.clip(t / 0.05, 0, 1) * np.clip((secs - t) / 0.2, 0, 1)
    c = concat([C(norm_rms(y))], names=["sweep"])
    return {"seconds": secs, "rate": rate[::480].tolist(), "spec": spec_rows(y, 100, 2000, 100), "depth": 60.0, "fc": 440.0,
            "clips": {"one": save("vib2fm.one", c, detail="a 440 Hz sine with a vibrato of 60 Hz each way, its rate rising from 4 to 220 times a second")}}


def compute_bessel() -> dict:
    n = SR
    fc, fmod, I = 1000.0, 250.0, 2.0
    y = F.fm(fc, fmod, I, n)
    pred = [(f, a) for f, a in F.sidebands(fc, fmod, I, 8) if 0 < f < 3200]
    meas = F.line_levels(y, [f for f, _ in pred]).tolist()
    err = float(max(abs(abs(a) - m) for (_, a), m in zip(pred, meas)))
    Is = np.linspace(0, 10, 201)
    curves = {str(k): jv(k, Is).tolist() for k in range(5)}
    secs = 6.0
    m = int(secs * SR)
    tt = np.arange(m) / SR
    idx = 8.0 * tt / secs
    sw = F.fm(220.0, 220.0, idx, m) * np.clip(tt / 0.05, 0, 1) * np.clip((secs - tt) / 0.2, 0, 1)
    c = concat([C(norm_rms(sw))], names=["sweep"])
    levels = {}
    for Iv in (0.0, 1.0, 2.0, 4.0, 8.0):
        lines = [(f, abs(a)) for f, a in F.sidebands(220.0, 220.0, Iv, 14) if 0 < f < 3600]
        levels[str(Iv)] = lines
    bw = {str(Iv): 2 * (Iv + 1) * 220.0 for Iv in (0.0, 1.0, 2.0, 4.0, 8.0)}
    return {"fc": fc, "fm": fmod, "I": I, "pred": [[f, a] for f, a in pred], "meas": meas, "max_err": err, "Is": Is.tolist(), "curves": curves,
            "levels": levels, "carson": bw, "sweep_s": secs,
            "clips": {"one": save("bessel.sweep", c, detail="a 220 Hz carrier modulated at 220 Hz, the index rising from 0 to 8 over six seconds")}}


RATIOS = [("1:1", 1.0), ("1:2", 2.0), ("1:1.4", 1.4), ("1:3.5", 3.5)]


def compute_ratios() -> dict:
    f = 220.0
    lines = {}
    for name, r in RATIOS:
        lines[name] = [(fr, abs(a)) for fr, a in F.sidebands(f, r * f, 3.0, 10) if 0 < fr < 3000]
    clips = []
    n = int(1.6 * SR)
    for name, r in RATIOS[:3]:
        e = F.env_adsr(n, SR, 0.02, 0.4, 0.6, 0.2, 1.3)
        clips.append(C(norm_rms(fade(F.fm(f, r * f, 3.0 * e, n) * e))))
    c = concat(clips, gap=0.6, names=["r11", "r12", "r114"])
    return {"f": f, "lines": lines, "starts": {k: float(c.events[k]) for k in ("r11", "r12", "r114")},
            "clips": {"three": save("ratios.three", c, detail="a 220 Hz carrier modulated at index 3 by 220 Hz (1 : 1), 440 Hz (1 : 2) and 308 Hz (1 : 1.4)")}}


def compute_chowning() -> dict:
    brass = np.concatenate([fm_brass(hz(m), d * 0.95) for m, _, d in tune_notes(beat=0.42)[:4]])
    bell = fm_bell(hz(72), 4.0)
    drum = np.concatenate([fm_drum(80.0, 0.45) for _ in range(4)])
    c = concat([C(norm_rms(brass)), C(norm_rms(bell)), C(norm_rms(drum))], gap=0.7, names=["brass", "bell", "drum"])
    n = int(1.0 * SR)
    e = F.env_adsr(n, SR, 0.06, 0.12, 0.75, 0.1, 0.85)
    return {"env": e[::240].tolist(), "starts": {k: float(c.events[k]) for k in ("brass", "bell", "drum")},
            "clips": {"three": save("chowning.three", c, detail="Chowning's recipes on two oscillators: brass (1 : 1, the index following the envelope), a bell (1 : 1.4, the index dying), a drum (80 : 55 Hz, a fast-dying index of 25)")}}


def epiano(f, seconds):
    n = int((seconds + 0.6) * SR)
    e_body = exp_env(n, 1.2) * np.clip(np.arange(n) / (0.002 * SR), 0, 1)
    e_mod = exp_env(n, 0.5)
    e_tine = exp_env(n, 0.25)
    e_tm = exp_env(n, 0.03)
    gate = np.where(np.arange(n) / SR < seconds, 1.0, np.exp(-(np.arange(n) / SR - seconds) / 0.08))
    y = F.operators("pairs", [1.0, 1.0, 1.0, 14.0], [1.0, 1.6, 0.35, 2.2], f, n, envs=[e_body * gate, e_mod, e_tine * gate, e_tm])
    return fade(y)


def fm_bass(f, seconds):
    n = int((seconds + 0.1) * SR)
    e = exp_env(n, 0.6) * np.clip(np.arange(n) / (0.002 * SR), 0, 1)
    gate = np.where(np.arange(n) / SR < seconds, 1.0, np.exp(-(np.arange(n) / SR - seconds) / 0.03))
    y = F.operators("stack2", [1.0, 1.0], [1.0, 2.5], f, n, envs=[e * gate, exp_env(n, 0.15)], feedback=0.8)
    return fade(y)


def fm_tbell(f, seconds):
    n = int((seconds + 1.5) * SR)
    e = exp_env(n, 1.4) * np.clip(np.arange(n) / (0.001 * SR), 0, 1)
    y = F.operators("stack2", [1.0, 3.5], [1.0, 2.0], f, n, envs=[e, exp_env(n, 0.8)])
    return fade(y)


def phrase(fn, notes, end_pad=1.5):
    parts = [(C(fn(hz(m), d * 0.95)), a, 0.0) for m, a, d in notes]
    return mix(parts, duration=max(a + d for _, a, d in notes) + end_pad).y


def compute_dx() -> dict:
    notes = tune_notes(beat=0.42)
    ep = phrase(epiano, notes)
    bs = phrase(fm_bass, [(m - 24, a, d) for m, a, d in notes], 0.4)
    bl = phrase(fm_tbell, [(m + 12, a, d) for m, a, d in notes], 2.0)
    c = concat([C(norm_rms(ep)), C(norm_rms(bs)), C(norm_rms(bl))], gap=0.7, names=["epiano", "bass", "bell"])
    fb = {}
    for g in (0.0, 0.8, 1.5):
        n = SR
        y = _feedback_osc(220.0, n, g)
        fb[str(g)] = D.harmonics(y, 220.0, SR, 8)
    return {"feedback": fb, "starts": {k: float(c.events[k]) for k in ("epiano", "bass", "bell")},
            "clips": {"three": save("dx.three", c, detail="the Tune's first phrase on a four-operator electric piano (two pairs, one with a 14 : 1 tine), a two-operator bass with feedback two octaves down, and a 1 : 3.5 bell an octave up")}}


def _feedback_osc(f, n, g):
    """One operator modulating itself: as the feedback rises, a sine leans into a sawtooth."""
    out = F._ops_loop(int(n), float(SR), float(f), np.array([1.0]), np.array([1.0]), np.ones((1, n)), -np.ones((1, 3), dtype=np.int64), 0, float(g))
    return out[0]


# ---------------------------------------------------------------------------------------------------------- grains
def compute_gabor() -> dict:
    rows = []
    shapes = {}
    for ms in (5.0, 20.0, 80.0):
        g = F.gabor_grain(1000.0, ms)
        G = np.abs(np.fft.rfft(g, 1 << 16))
        G /= G.max()
        f = np.fft.rfftfreq(1 << 16, 1 / SR)
        above = f[G > 0.5]
        bw = float(above.max() - above.min())
        rows.append({"ms": ms, "bw": bw, "product": bw * ms / 1000})
        k = np.linspace(0, len(g) - 1, 300).astype(int)
        shapes[str(int(ms))] = {"y": g[k].tolist(), "spec_f": f[(f > 0) & (f < 2000)][::20].tolist(), "spec": G[(f > 0) & (f < 2000)][::20].tolist()}
    return {"rows": rows, "shapes": shapes}


def voice_line():
    y = CH.sing(tune_notes(base=60), "soprano", "a")
    return 0.5 * y / np.max(np.abs(y))


def compute_grains() -> dict:
    v = voice_line()
    L = len(v) / SR
    freeze = F.grains(v, 3.0, 1.15, density=60, grain_ms=70, scatter_s=0.02, seed=1)
    stretch = F.grains(v, 4 * 3.5, lambda t: t / 4, density=50, grain_ms=80, seed=2)
    shift = F.grains(v, 3.5, lambda t: t, density=60, grain_ms=50, pitch=2 ** (7 / 12), sync=True, seed=3)
    cloud = F.grains(v, 4.0, lambda t: t * 3.5 / 4, density=120, grain_ms=40, scatter_s=0.6, pitch_jitter=7, seed=4)
    names = ["source", "freeze", "stretch", "shift", "cloud"]
    ys = [v[: int(3.6 * SR)], freeze["y"], stretch["y"][: int(8.0 * SR)], shift["y"], cloud["y"]]
    c = concat([C(norm_rms(fade(y))) for y in ys], gap=0.7, names=names)
    log = cloud["grains"]
    return {"names": names, "counts": {k: len(g["grains"]) for k, g in zip(names[1:], (freeze, stretch, shift, cloud))},
            "cloud": [[float(a), float(b), float(r)] for a, b, r in log[::2]], "source_s": L,
            "starts": {k: float(c.events[k]) for k in names},
            "clips": {"five": save("grains.five", c, detail="Part 8's voice singing the Tune's first phrase; frozen on one vowel by grains read from one place; stretched four times; raised a fifth at the same speed; scattered into a cloud of grains with random positions and pitches")}}


# ---------------------------------------------------------------------------------------------------------- spectral model
def compute_spectral() -> dict:
    y = np.asarray(P38.piano(60, 2.0), float)[: int(2.2 * SR)]
    y = y / np.max(np.abs(y))
    f0 = hz(60)
    tr = F.track_harmonics(y, f0, count=24)
    sines = F.resynth(tr, len(y))
    near, resid = F.split_partials(y, tr["partials"], f0)
    ratio_db = float(10 * np.log10(np.sum(resid ** 2) / np.sum(y ** 2)))
    early = slice(0, int(0.08 * SR))
    late = slice(int(0.3 * SR), int(1.5 * SR))
    r_early = float(10 * np.log10(np.sum(resid[early] ** 2) / np.sum(y[early] ** 2)))
    r_late = float(10 * np.log10(np.sum(resid[late] ** 2) / np.sum(y[late] ** 2)))
    fr = tr["partials"]
    f1 = fr[0]
    cents = (1200 * np.log2(fr / (np.arange(1, len(fr) + 1) * f1))).tolist()
    B = float(np.polyfit(np.arange(1, len(fr) + 1) ** 2, (fr / (np.arange(1, len(fr) + 1) * f1)) ** 2, 1)[0])
    trh = {"t": tr["t"], "amps": tr["amps"], "freqs": np.outer(np.arange(1, tr["amps"].shape[0] + 1) * f1, np.ones(tr["amps"].shape[1]))}
    harm = F.resynth(trh, len(y))
    sine_err = float(10 * np.log10(np.sum((np.abs(np.fft.rfft(sines)) - np.abs(np.fft.rfft(near))) ** 2) / np.sum(np.abs(np.fft.rfft(near)) ** 2)))
    gain = 12.0
    c = concat([C(y), C(sines), C(resid * 10 ** (gain / 20)), C(harm)], gap=0.7, names=["piano", "sines", "residual", "harmonic"])
    amps = tr["amps"][:12, ::4]
    return {"f0": f0, "t": tr["t"][::4].tolist(), "amps": (20 * np.log10(amps / amps.max() + 1e-6)).tolist(), "cents": cents,
            "resid_db": ratio_db, "resid_early": r_early, "resid_late": r_late, "gain": gain, "B": B, "sine_err": sine_err,
            "starts": {k: float(c.events[k]) for k in ("piano", "sines", "residual", "harmonic")},
            "clips": {"four": save_pm("spectral.four", c, detail="middle C on Part 7's computed piano; its 24 tracked harmonics resynthesized as sines; the residual, raised 12 dB; the sines made exactly harmonic")}}


# ---------------------------------------------------------------------------------------------------------- sampler
def compute_sampler() -> dict:
    src = np.asarray(P38.piano(60, 1.5), float)
    clips, names = [], []
    for m in (36, 84):
        r = hz(m) / hz(60)
        k = np.arange(0, len(src) - 1, r)
        i0 = np.floor(k).astype(int)
        fr = k - i0
        samp = src[i0] * (1 - fr) + src[i0 + 1] * fr
        comp = np.asarray(P38.piano(m, 1.5), float)
        clips += [C(norm_rms(fade(samp[: int(2.0 * SR)]))), C(norm_rms(fade(comp[: int(2.0 * SR)])))]
        names += [f"sample{m}", f"real{m}"]
    c = concat(clips, gap=0.6, names=names)
    durs = {"36": len(src) / SR * hz(60) / hz(36), "84": len(src) / SR * hz(60) / hz(84)}
    gb = 88 * 8 * 2 * 20.0 * 48000 * 3 / 1e9
    return {"durations": durs, "src_s": len(src) / SR, "library_gb": gb, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"four": save_pm("sampler.four", c, detail="one recording of middle C on Part 7's piano played back two octaves down, then the piano computed at C2; the same recording two octaves up, then the piano computed at C6")}}


# ---------------------------------------------------------------------------------------------------------- Karplus-Strong
def compute_ks() -> dict:
    notes = list(range(60, 97, 3))
    unt, tun = [], []
    for m in notes:
        f = hz(m)
        unt.append(float(1200 * np.log2(SR / F.ks_loop_delay(f, tuned=False) / f)))
        tun.append(float(1200 * np.log2(F.measured_pitch(F.ks_tuned(f, 0.6), guess=f) / f)))
    ph = tune_notes(base=84, beat=0.36)
    a = phrase(lambda f, d: F.ks_tuned(f, d + 0.4, tuned=False, rho=0.998), ph, 0.6)
    b = phrase(lambda f, d: F.ks_tuned(f, d + 0.4, rho=0.998), ph, 0.6)
    c = concat([C(norm_rms(a)), C(norm_rms(b))], gap=0.8, names=["untuned", "tuned"])
    return {"notes": notes, "untuned": unt, "tuned": tun, "starts": {"untuned": float(c.events["untuned"]), "tuned": float(c.events["tuned"])},
            "clips": {"two": save_pm("ks.two", c, detail="the Tune's first phrase two octaves above middle C on Karplus-Strong strings: the delay rounded to whole samples, then tuned exactly by an all-pass")}}


# ---------------------------------------------------------------------------------------------------------- waveguide
def compute_waveguide() -> dict:
    s = STR.String.tuned(220.0)
    N = 100
    x = np.linspace(0, s.L, N + 1)
    sh = STR.pluck_shape(x, s.L, 0.2)
    run = STR.simulate(s, sh, 0.5, N=N, pickup=0.2371)
    wg = F.waveguide(sh, 0.5, run.sr, pickup=0.2371)
    a = np.asarray(run.pickup)
    err = float(np.max(np.abs(a - wg)))
    return {"sr": run.sr, "N": N, "max_err": err, "out": a[:400].tolist(), "shape": sh.tolist()}


# ---------------------------------------------------------------------------------------------------------- clarinet
def compute_clarinet() -> dict:
    ps = np.round(np.arange(0.1, 1.31, 0.05), 2)
    rms = []
    for p in ps:
        y = F.clarinet(220.0, 0.5, pressure=float(p), breath=0.0, normalize=False)
        rms.append(float(np.sqrt(np.mean(y[int(0.3 * SR):] ** 2))))
    y = F.clarinet(220.0, 1.0)
    h = D.harmonics(y[int(0.3 * SR):], F.measured_pitch(y, guess=220.0), SR, 8)
    secs = 4.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    # a crescendo: mouth pressure rising slowly through the threshold
    from explainer.music.monochord.synth2 import _clarinet_loop
    os = 4
    fs = SR * os
    tt = np.arange(n * os) / fs
    pm = (0.4 + 0.55 * tt / secs) * np.clip(tt / 0.03, 0, 1) * np.clip((secs - tt) / 0.05, 0, 1)
    a = 0.5 ** (1 / os)
    L = int(round(fs / 196.0 / 2 - a / (1 - a)))
    out = np.zeros(len(pm))
    _clarinet_loop(pm, L, a, out)
    cres = resample_poly(out, 1, os)[:n]
    from scipy.signal import butter, sosfilt
    cres = sosfilt(butter(1, 20.0, btype="high", fs=SR, output="sos"), cres)
    onset = float(t[np.argmax(np.abs(cres) > 0.1 * np.max(np.abs(cres)))])
    notes = tune_notes(base=55, beat=0.45)
    tn = phrase(lambda f, d: F.clarinet(f, d + 0.02, release=0.04), notes, 0.3)
    c = concat([C(norm(cres, 0.5)), C(norm_rms(tn))], gap=0.8, names=["crescendo", "tune"])
    return {"pressures": ps.tolist(), "rms": rms, "harmonics": h, "onset_s": onset, "onset_p": float(0.4 + 0.55 * onset / secs),
            "starts": {"crescendo": float(c.events["crescendo"]), "tune": float(c.events["tune"])},
            "clips": {"two": save_pm("clarinet.two", c, detail="a waveguide clarinet on G3, the mouth pressure rising slowly from 0.4 to 0.95 of the reed's closing pressure; then the Tune's first phrase on it")}}


# ---------------------------------------------------------------------------------------------------------- modal
def compute_modal() -> dict:
    s = STR.String.tuned(196.0, kappa=0.6, sigma0=1.2, sigma1=2e-4)
    secs = 2.0
    r = STR.simulate(s, lambda x: STR.pluck_shape(x, s.L, 0.2), secs, sr=SR, pickup=0.2371)
    fd = np.asarray(r.pickup)
    nm = 80
    coef = STR.sine_coefficients(STR.pluck_shape(r.x, s.L, 0.2), nm)
    md = F.modal_string(s.f1, s.B, s.mode_decay(np.arange(1, nm + 1)), coef, secs, SR)
    err = float(10 * np.log10(np.sum((fd - md) ** 2) / np.sum(fd ** 2)))
    # partial frequencies in the simulation against the modal formula
    Y = np.abs(np.fft.rfft(fd[: SR] * np.hanning(SR), 1 << 18))
    f = np.fft.rfftfreq(1 << 18, 1 / SR)
    cents = []
    for k in range(1, 26):                         # above about 25 the scheme drifts too far for this peak search
        fk = s.mode_freq(k)
        if fk > 12000:
            break
        win = (f > fk - 0.35 * s.f1) & (f < fk + 0.35 * s.f1)
        if not np.any(win) or k % 5 == 0:          # the pluck at 1/5 leaves every fifth partial missing
            continue
        fp = f[win][np.argmax(Y[win])]
        cents.append([k, float(1200 * np.log2(fp / fk))])
    c = concat([C(norm_rms(fade(md))), C(norm_rms(fade(fd)))], gap=0.8, names=["first", "second"])
    return {"answer": "second", "err_db": err, "cents": cents, "N": r.N, "courant": r.courant, "B": s.B, "modes": nm,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_pm("modal.two", c, detail="one stiff, damped string (G3) plucked at a fifth of its length: first as a sum of 80 modes, then bead by bead by finite differences")}}


# ---------------------------------------------------------------------------------------------------------- costs
def timed(fn, reps=3):
    fn()
    best = 1e9
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


def compute_costs() -> dict:
    n = SR
    s = STR.String.tuned(196.0, kappa=0.6, sigma0=1.2, sigma1=2e-4)
    coef = STR.sine_coefficients(STR.pluck_shape(np.linspace(0, s.L, 201), s.L, 0.2), 60)
    v = voice_line()
    rows = [
        ("additive, 40 sines", lambda: S1.saw_additive(110.0, n)),
        ("subtractive: PolyBLEP and ladder", lambda: S1.ladder(S1.saw_polyblep(110.0, n), 1000.0, 2.0)),
        ("FM, two operators", lambda: F.fm(220.0, 220.0, 3.0, n)),
        ("FM engine, four operators", lambda: F.operators("pairs", [1, 1, 1, 14], [1, 1.6, 0.35, 2.2], 220.0, n)),
        ("granular, 60 grains a second", lambda: F.grains(v, 1.0, 1.0, density=60, grain_ms=70, seed=0)),
        ("Karplus-Strong, tuned", lambda: F.ks_tuned(220.0, 1.0)),
        ("waveguide clarinet", lambda: F.clarinet(220.0, 1.0)),
        ("modal string, 60 modes", lambda: F.modal_string(s.f1, s.B, s.mode_decay(np.arange(1, 61)), coef, 1.0, SR)),
        ("finite-difference string", lambda: STR.simulate(s, lambda x: STR.pluck_shape(x, s.L, 0.2), 1.0, sr=SR)),
    ]
    out = [{"name": nm, "ms": 1000 * timed(fn)} for nm, fn in rows]
    return {"rows": out}


# ---------------------------------------------------------------------------------------------------------- Variation 52
def compute_tune52() -> dict:
    beat = 0.42
    keys = tune_notes(phrases=(0, 1), base=60, beat=beat)
    bells = tune_notes(phrases=(2, 3), base=72, beat=beat)
    off = 16 * beat
    ep = phrase(epiano, keys, 1.0)
    bl = phrase(fm_tbell, [(m, a, d) for m, a, d in bells], 2.0)
    seq = mix([(C(norm_rms(ep)), 0.0, 0.0), (C(norm_rms(bl)), off, -2.0)], duration=off + 16 * beat + 2.0).y
    L = len(seq) / SR
    # dissolve: grains read along the piece, scatter rising then falling, then the last phrase clean again
    dur = 10.0

    def pos(t):
        return 2.0 + 4.0 * t / dur
    # build the dissolve in three overlapping layers of rising scatter
    layers = []
    for k, (s_, j) in enumerate(((0.0, 0.0), (0.4, 3.0), (1.2, 12.0))):
        g = F.grains(seq, dur, pos, density=90, grain_ms=50, scatter_s=s_, pitch_jitter=j, seed=6 + k)["y"]
        layers.append(g)
    t = np.arange(int(dur * SR)) / SR
    u = np.sin(np.pi * t / dur) ** 2
    w0 = (1 - u) ** 2
    w2 = u ** 2
    w1 = 1 - w0 - w2
    diss = w0 * layers[0] + w1 * layers[1] + w2 * layers[2]
    tail = epiano(hz(60), 1.6)
    full = np.concatenate([norm_rms(seq), norm_rms(diss), np.zeros(int(0.3 * SR)), norm_rms(tail)])
    names = ["keys", "bells", "grains", "back"]
    starts = {"keys": 0.0, "bells": off, "grains": L, "back": L + dur + 0.3}
    c = Clip(fade(full), SR)
    for k, v in starts.items():
        c.events[k] = v
    ngr = int(sum(len(F.grains(seq, dur, pos, density=90, grain_ms=50, seed=6 + k)["grains"]) for k in range(3)))
    d = load("bessel")
    return {"names": names, "starts": starts, "seconds": c.duration, "keys": [list(x) for x in keys], "bells": [list(x) for x in bells],
            "beat": beat, "grains": ngr, "bessel_err": d["max_err"],
            "clips": {"variation52": save("tune.variation52", c, detail="the Tune's first two phrases on an FM electric piano, the next two on FM bells; then the whole dissolved into grains, scattering in time and pitch and gathering again; then one clean note")}}


def compute_variation() -> dict:
    t = load("tune52")
    return {"part": 52, "title": "on FM keys and bells, dissolved into grains and back", "seconds": round(t["seconds"], 1),
            "measure": f"FM's lines within {t['bessel_err']:.6f} of Bessel's; {t['grains']:,} grains in ten seconds",
            "clip": "tune.variation52"}


ITEMS = {"hook": compute_hook, "vib2fm": compute_vib2fm, "bessel": compute_bessel, "ratios": compute_ratios, "chowning": compute_chowning,
         "dx": compute_dx, "gabor": compute_gabor, "grains": compute_grains, "spectral": compute_spectral, "sampler": compute_sampler,
         "ks": compute_ks, "waveguide": compute_waveguide, "clarinet": compute_clarinet, "modal": compute_modal, "costs": compute_costs,
         "tune52": compute_tune52, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
