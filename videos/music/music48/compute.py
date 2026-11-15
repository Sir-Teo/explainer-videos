"""Precompute everything numerical, and every sound, in Part 48 of *Music, Built* ("Digital Audio").

    python -m videos.music.music48.compute              # everything missing (a few minutes)
    python -m videos.music.music48.compute --force hook

Numbers are cached in ``.cache/music48/<name>.json``, sounds in ``.cache/music48/audio/``.  The tools are Monochord's
(``explainer/music/monochord/digital.py``).  The music is the Tune on Part 7's piano (a physical model) and a groove on
Part 40's drums; every converter, dither and modulator is simulated here.  Differences near the threshold of hearing
(16 bits, dither at 8 bits, noise shaping) are played as residues, the difference from the original, amplified by a
stated gain, as the series' rule for a lossy video soundtrack requires (SYLLABUS §3).

Items:
    hook        an ear question: the Tune stored as 16-bit samples and as one bit at 64 times the rate; which is which?
    rate44      why 44,100: three samples a video line
    sampling    a band-limited signal, its samples, and Whittaker-Shannon reconstruction; error against filter length
    tones       three tones sampled at 8 kHz with no filter: 3, 5 and 7 kHz come out as 3, 3 and 1 kHz
    alias       an ear question: a rising sweep sampled at 8 kHz without and with an anti-aliasing filter
    stairstep   the zero-order hold: its images and its droop
    quant       measured SNR against 6.02 N + 1.76 dB; an ear question: the Tune at 4 bits without and with dither
    moments     the quantization error's mean and variance against the input: none, RPDF, TPDF
    fade        a piano note at 8 bits, without and with dither, played as residues (+30 dB)
    lowsine     a sine smaller than half a step at 8 bits: silence without dither, a tone in noise with it
    shaping     error spectra with noise shaping of order 0, 1, 2; residues of flat and shaped (+24 dB)
    deltasigma  one-bit modulators: in-band SNR against oversampling; a bitstream drawn
    jitter      SNR of a 10 kHz sine sampled with timing jitter, measured and predicted
    rate        an ear question: a groove sampled at 16 kHz and at 48 kHz
    stairs      the Tune sampled at 8 kHz, played as a stair-step (zero-order hold, no filter) and as the smooth curve
    speeds      one bit at 1, 8 and 64 times 48 kHz, each filtered back to 48 kHz
    sidebands   a 10 kHz sine sampled with periodic jitter: the sidebands, measured and predicted
    tune48      Variation 48: the Tune at 16, 8, 4 and 1 bit, with and without dither (residues where needed)
    variation   the Variations ledger, row 48
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import resample_poly

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import digital as D
from explainer.music.monochord import tune as T
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music48")
CLIPS = ClipStore("music48")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano = P38.piano
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
OSR = 64


def tune_signal(phrases=(0, 1), beat=0.42, peak=0.45, tail=1.0) -> np.ndarray:
    """The Tune on Part 7's piano at 48 kHz, scaled to ``peak``."""
    p = []
    for e in T.events(beat, list(phrases)):
        p.append((arr(piano(60 + MAJOR[e["degree"]], e["dur"] * 0.97, 0.7)), e["t"], 0.0))
    end = max(e["t"] + e["dur"] for e in T.events(beat, list(phrases)))
    y = mix(p, duration=end + tail).y
    return peak * y / np.abs(y).max()


def one_bit(x, order=2) -> np.ndarray:
    """``x`` at 48 kHz, upsampled 64 times, through a one-bit delta-sigma modulator, and decimated back."""
    up = resample_poly(x, OSR, 1)
    return D.decimate(D.delta_sigma(up, order), OSR)[: len(x)]


def rms_db(e) -> float:
    return float(20 * np.log10(np.sqrt(np.mean(np.asarray(e) ** 2)) + 1e-30))


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    x = tune_signal()
    a = D.quantize(x, 16, "tpdf", np.random.default_rng(16))
    b = one_bit(x)
    c = concat([C(b), C(a)], gap=1.0, names=["first", "second"])
    mid = len(x) // 3
    up = resample_poly(x[mid:mid + 40], OSR, 1)
    bits = D.delta_sigma(up, 2)
    return {"order": ["one bit", "16 bits"], "answer": "first", "residue_db": {"one bit": rms_db(b - x), "16 bits": rms_db(a - x)},
            "signal_db": rms_db(x), "snr": {"one bit": D.snr_db(x, b), "16 bits": D.snr_db(x, a)},
            "bits": bits[:512].astype(int).tolist(), "input": up[:512].round(5).tolist(),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("hook.two", c, detail="the Tune's first two phrases on Part 7's piano, stored as one bit at 3.072 MHz by a second-order delta-sigma modulator and filtered back to 48 kHz, then as 16-bit samples with dither")}}


def compute_rate44() -> dict:
    return {"ntsc": {"lines": 245, "fields": 60, "per_line": 3, "rate": 245 * 60 * 3},
            "pal": {"lines": 294, "fields": 50, "per_line": 3, "rate": 294 * 50 * 3},
            "ntsc_colour": 3 * 245 * 60 / 1.001, "cd_bits": 16, "cd_rate": 44100, "cd_bytes_per_hour": 44100 * 2 * 2 * 3600}


def band_signal(t):
    return 0.55 * np.sin(2 * np.pi * 1.0 * t + 0.3) + 0.3 * np.sin(2 * np.pi * 2.3 * t + 1.1) + 0.2 * np.sin(2 * np.pi * 3.6 * t + 2.0)


def compute_sampling() -> dict:
    fs = 8.0                                         # samples per unit time; the signal stays below 3.6 < fs / 2
    n = np.arange(0, 33)
    x = band_signal(n / fs)
    t = np.linspace(0.5, 3.5, 400)
    full = D.sinc_interp(x, fs, t)
    errs = {}
    nn = np.arange(0, 400)
    xx = band_signal(nn / fs)
    tt = np.linspace(20, 30, 800)
    for taps in (4, 8, 16, 32, 64, 128):
        r = D.sinc_interp(xx, fs, tt, taps=taps)
        errs[str(taps)] = float(np.max(np.abs(r - band_signal(tt))))
    return {"fs": fs, "n": n.tolist(), "x": x.tolist(), "t": t.tolist(), "true": band_signal(t).tolist(), "full": full.tolist(),
            "max_err_full": float(np.max(np.abs(full - band_signal(t)))), "taps_error": errs, "top": 3.6}


def tone(f, seconds, amp=0.3, sr=SR):
    t = np.arange(int(seconds * sr)) / sr
    env = np.clip(t / 0.02, 0, 1) * np.clip((seconds - t) / 0.05, 0, 1)
    return amp * env * np.sin(2 * np.pi * f * t)


def compute_tones() -> dict:
    fs = 8000
    clips, heard = [], []
    for f in (3000, 5000, 7000):
        hi = tone(f, 1.2)
        low = D.drop_samples(hi, SR // fs)                       # sampled at 8 kHz with no filter
        back = D.resample(low, fs, SR, filtered=True)             # a good reconstruction back to 48 kHz
        clips.append(C(np.concatenate([hi, np.zeros(int(0.3 * SR)), back])))
        heard.append(D.alias(f, fs))
    c = concat(clips, gap=0.8, names=["3000", "5000", "7000"])
    return {"fs": fs, "tones": [3000, 5000, 7000], "heard": heard, "starts": {k: float(c.events[k]) for k in ("3000", "5000", "7000")},
            "each": 1.5, "clips": {"three": save_synth("tones.three", c, detail="tones at 3, 5 and 7 kHz, each heard as it is and then after sampling at 8 kHz with no filter and reconstructing")}}


def compute_alias() -> dict:
    fs, secs = 8000, 6.0
    t = np.arange(int(secs * SR)) / SR
    f0, f1 = 200.0, 12000.0
    phase = 2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * secs))
    x = 0.3 * np.sin(phase) * np.clip(t / 0.05, 0, 1) * np.clip((secs - t) / 0.1, 0, 1)
    raw = D.resample(D.drop_samples(x, SR // fs), fs, SR, filtered=True)
    filt = D.resample(D.resample(x, SR, fs, filtered=True), fs, SR, filtered=True)
    c = concat([C(raw), C(filt)], gap=1.2, names=["first", "second"])
    ts = np.linspace(0, secs, 121)
    fin = f0 + (f1 - f0) * ts / secs
    return {"fs": fs, "seconds": secs, "f0": f0, "f1": f1, "track_t": ts.tolist(), "track_in": fin.tolist(),
            "track_raw": [D.alias(f, fs) for f in fin], "track_filtered": [f if f < fs / 2 * 0.95 else None for f in fin],
            "answer": "first", "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("alias.two", c, detail="a sine sweeping from 200 Hz to 12 kHz in six seconds, sampled at 8 kHz without a filter, then with an anti-aliasing filter; each reconstructed at 48 kHz")}}


def compute_stairstep() -> dict:
    fs = 44100.0
    droop = {str(f): float(20 * np.log10(abs(np.sinc(f / fs)))) for f in (1000, 10000, 20000)}
    f = 1000.0
    images = []
    for k in (1, 2):
        for s in (-1, 1):
            g = k * fs + s * f
            images.append({"hz": g, "db": float(20 * np.log10(abs(np.sinc(g / fs))))})
    fs2 = 8.0
    n = np.arange(0, 17)
    x = band_signal(n / fs2)
    return {"fs": fs, "droop": droop, "images": images, "fs2": fs2, "n": n.tolist(), "x": x.tolist()}


def compute_quant() -> dict:
    t = np.arange(SR) / SR
    rows = []
    for b in range(2, 17):
        amp = 1.0 - D.lsb(b)
        x = amp * np.sin(2 * np.pi * 997 * t)
        rows.append({"bits": b, "measured": D.snr_db(x, D.quantize(x, b)), "theory": D.theory_snr(b)})
    x = 0.9 * np.sin(2 * np.pi * 997 * t[:4800])
    e = (D.quantize(x, 8) - x) / D.lsb(8)
    hist, edges = np.histogram(e, bins=20, range=(-0.5, 0.5))
    tu = tune_signal(peak=0.9)
    a = D.quantize(tu, 4, "none")
    b = D.quantize(tu, 4, "tpdf", np.random.default_rng(4))
    c = concat([C(a), C(b)], gap=1.0, names=["first", "second"])
    return {"rows": rows, "hist": hist.tolist(), "edges": edges.tolist(), "snr4": {"none": D.snr_db(tu, a), "tpdf": D.snr_db(tu, b)},
            "answer": "second", "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("quant.two", c, detail="the Tune's first two phrases on Part 7's piano quantized to 4 bits, without dither and then with triangular dither")}}


def compute_moments() -> dict:
    return {k: D.error_moments(8, k, 61, 3000, seed=8) for k in ("none", "rpdf", "tpdf")}


def piano_note(m=60, seconds=3.0, peak=0.5):
    y = arr(piano(m, seconds - 0.5, 0.7)).y
    y = np.concatenate([y, np.zeros(max(0, int(seconds * SR) - len(y)))])[: int(seconds * SR)]
    return peak * y / np.abs(y).max()


def compute_fade() -> dict:
    x = piano_note(60, 3.5)
    a = D.quantize(x, 8, "none")
    b = D.quantize(x, 8, "tpdf", np.random.default_rng(8))
    g = 10 ** (30 / 20)
    c = concat([C(g * (a - x)), C(g * (b - x))], gap=1.0, names=["first", "second"])
    k = next(i for i in range(0, len(x) - 480, 480) if np.max(np.abs(x[i:i + 480])) < 3.5 * D.lsb(8) and i > SR // 2)
    return {"gain_db": 30, "tail_at": k / SR, "residue_db": {"none": rms_db(a - x), "tpdf": rms_db(b - x)},
            "tail": {"x": x[k:k + 480].tolist(), "none": a[k:k + 480].tolist(), "tpdf": b[k:k + 480].tolist()},
            "env": [float(np.sqrt(np.mean(x[i:i + 2400] ** 2))) for i in range(0, len(x) - 2400, 2400)],
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"residues": save_synth("fade.residues", c, detail="a piano note quantized to 8 bits: the error without dither, then with triangular dither, each amplified by 30 dB; Part 7's piano")}}


def compute_lowsine() -> dict:
    t = np.arange(int(2.0 * SR)) / SR
    amp = 0.4 * D.lsb(8)
    x = amp * np.sin(2 * np.pi * 1000 * t) * np.clip(t / 0.02, 0, 1) * np.clip((2.0 - t) / 0.05, 0, 1)
    a = D.quantize(x, 8, "none")
    b = D.quantize(x, 8, "tpdf", np.random.default_rng(1))
    f, Pa = D.noise_spectrum(a + 1e-12, SR, 4096)
    _, Pb = D.noise_spectrum(b, SR, 4096)
    keep = f <= 6000
    c = concat([C(a), C(b)], gap=1.0, names=["first", "second"])
    return {"amp_lsb": 0.4, "nonzero_none": int(np.count_nonzero(a)), "f": f[keep].tolist(), "none": Pa[keep].tolist(), "tpdf": Pb[keep].tolist(),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("lowsine.two", c, detail="a 1 kHz sine 0.4 of a step high, quantized to 8 bits without dither (silence) and with triangular dither (the tone in noise)")}}


def threshold_db(f_hz):
    """Terhardt's approximation of the threshold of hearing, dB SPL."""
    f = np.asarray(f_hz, float) / 1000.0
    f = np.maximum(f, 0.02)
    return 3.64 * f ** -0.8 - 6.5 * np.exp(-0.6 * (f - 3.3) ** 2) + 1e-3 * f ** 4


def compute_shaping() -> dict:
    x = tune_signal(peak=0.7)
    out, res = {}, {}
    for order in (0, 1, 2):
        y = D.shaped(x, 8, order, "tpdf", np.random.default_rng(order))
        e = y - x
        f, P = D.noise_spectrum(e, SR, 2048)
        res[order] = e
        lo = f < 4000
        tot = 10 * np.log10(np.sum(10 ** (P / 10)))
        low = 10 * np.log10(np.sum(10 ** (P[lo] / 10)))
        out[str(order)] = {"P": P[::4].tolist(), "total_db": float(tot), "below4k_db": float(low)}
    out["f"] = f[::4].tolist()
    out["threshold"] = threshold_db(np.array(out["f"]) + 1).tolist()
    g = 10 ** (24 / 20)
    c = concat([C(g * res[0]), C(g * res[2])], gap=1.0, names=["first", "second"])
    out["gain_db"] = 24
    out["starts"] = {"first": float(c.events["first"]), "second": float(c.events["second"])}
    out["clips"] = {"residues": save_synth("shaping.residues", c, detail="the error of the Tune quantized to 8 bits with dither, flat and then shaped by (1 - z^-1)^2, each amplified by 24 dB")}
    return out


def compute_deltasigma() -> dict:
    rows = {}
    for order in (1, 2):
        r = []
        for osr in (8, 16, 32, 64, 128):
            fsr = 48000 * osr
            n = int(0.2 * fsr)
            tt = np.arange(n) / fsr
            r.append({"osr": osr, "snr": D.band_snr_db(D.delta_sigma(0.5 * np.sin(2 * np.pi * 1000 * tt), order), 1000, fsr, 20000)})
        rows[str(order)] = r
    k = np.arange(600)
    slow = 0.8 * np.sin(2 * np.pi * k / 600)
    bits = D.delta_sigma(slow, 1)
    dens = np.convolve(bits, np.ones(24) / 24, mode="same")
    return {"rows": rows, "slow": slow.tolist(), "bits": bits.astype(int).tolist(), "density": dens.tolist(), "dsd_rate": 64 * 44100}


def compute_jitter() -> dict:
    out = []
    for sigma in (1e-10, 1e-9, 1e-8, 1e-7):
        a, b = D.jitter_sample(10000.0, 48000.0, sigma, 48000, np.random.default_rng(int(sigma * 1e12)))
        out.append({"sigma": sigma, "measured": D.snr_db(a, b), "theory": D.jitter_snr_theory(10000.0, sigma)})
    return {"f": 10000.0, "rows": out}


def groove(seconds_bars=4, bpm=100):
    parts = []
    P40.drums(parts, "rock", bpm, seconds_bars, gain=-2.0)
    beat = 60 / bpm
    for e in T.events(beat / 2, [0, 1]):
        parts.append((arr(piano(72 + MAJOR[e["degree"]], e["dur"] * 0.95, 0.75)), e["t"], -2.0))
    return mix(parts, duration=seconds_bars * 4 * beat + 0.8).y


def compute_rate() -> dict:
    y = groove()
    y = 0.5 * y / np.abs(y).max()
    low = D.resample(D.resample(y, SR, 16000, filtered=True), 16000, SR, filtered=True)[: len(y)]
    c = concat([C(low), C(y)], gap=1.0, names=["first", "second"])
    f, Py = D.noise_spectrum(y, SR, 4096)
    _, Pl = D.noise_spectrum(low, SR, 4096)
    return {"order": ["16 kHz", "48 kHz"], "answer": "first", "f": f[::8].tolist(), "full": Py[::8].tolist(), "low": Pl[::8].tolist(),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "ratio_441": [147, 160],
            "clips": {"two": save("rate.two", c, detail="a groove on Part 40's drums with the Tune on Part 7's piano, sampled at 16 kHz and then at 48 kHz")}}


def compute_stairs() -> dict:
    x = tune_signal((0,), peak=0.45, tail=0.5)
    fs = 8000
    low = D.resample(x, SR, fs, filtered=True)
    stair = D.zero_order_hold(low, SR // fs)[: len(x)]
    smooth = D.resample(low, fs, SR, filtered=True)[: len(x)]
    c = concat([C(stair), C(smooth)], gap=1.0, names=["first", "second"])
    f, Ps = D.noise_spectrum(stair, SR, 4096)
    _, Pm = D.noise_spectrum(smooth, SR, 4096)
    hf = f > 4500
    return {"fs": fs, "f": f[::8].tolist(), "stair": Ps[::8].tolist(), "smooth": Pm[::8].tolist(),
            "image_db": float(10 * np.log10(np.sum(10 ** (Ps[hf] / 10)) / np.sum(10 ** (Ps / 10)))),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("stairs.two", c, detail="the Tune's first phrase sampled at 8 kHz, played as held steps with no reconstruction filter, then as the band-limited curve; Part 7's piano")}}


def compute_speeds() -> dict:
    x = tune_signal((0,), peak=0.4, tail=0.5)
    clips, snr = [], {}
    for osr in (1, 8, 64):
        up = resample_poly(x, osr, 1) if osr > 1 else x
        y = D.decimate(D.delta_sigma(up, 2), osr)[: len(x)] if osr > 1 else D.delta_sigma(x, 2) * 0.4
        clips.append(C(y))
        snr[str(osr)] = D.snr_db(x, y) if osr > 1 else D.snr_db(x, y * np.dot(x, y) / max(np.dot(y, y), 1e-12) / 1.0)
    c = concat(clips, gap=1.0, names=["1", "8", "64"])
    return {"snr": snr, "starts": {k: float(c.events[k]) for k in ("1", "8", "64")},
            "clips": {"three": save_synth("speeds.three", c, detail="the Tune's first phrase as one bit from a second-order delta-sigma modulator running at 1, 8 and 64 times 48 kHz, each filtered back to 48 kHz; Part 7's piano")}}


def compute_sidebands() -> dict:
    fs, f, fj, a = 48000.0, 10000.0, 1000.0, 1e-8
    t = np.arange(48000) / fs
    ideal = np.sin(2 * np.pi * f * t)
    jit = np.sin(2 * np.pi * f * (t + a * np.sin(2 * np.pi * fj * t)))
    fr, P = D.noise_spectrum(jit, fs, 8192)
    _, P0 = D.noise_spectrum(ideal, fs, 8192)
    k0 = int(np.argmin(np.abs(fr - f)))
    k1 = int(np.argmin(np.abs(fr - (f + fj))))
    measured = float(P[k1 - 2:k1 + 3].max() - P[k0 - 2:k0 + 3].max())
    predicted = float(20 * np.log10(np.pi * f * a))
    keep = (fr > 7000) & (fr < 13000)
    return {"f": f, "fj": fj, "a": a, "measured": measured, "predicted": predicted, "fr": fr[keep].tolist(), "P": P[keep].tolist(), "P0": P0[keep].tolist()}


def compute_tune48() -> dict:
    x = tune_signal((0,), peak=0.45, tail=0.6)
    rng = np.random.default_rng(48)
    segs, names, info = [], [], []
    def add(name, y, gain_db, what):
        segs.append(C(y * 10 ** (gain_db / 20)))
        names.append(name)
    q16n, q16t = D.quantize(x, 16, "none"), D.quantize(x, 16, "tpdf", rng)
    q8n, q8t = D.quantize(x, 8, "none"), D.quantize(x, 8, "tpdf", rng)
    q4n, q4t = D.quantize(x, 4, "none"), D.quantize(x, 4, "tpdf", rng)
    q1n = D.quantize(x, 1, "none")
    ds = one_bit(x)
    add("16n", q16n - x, 60, "residue")
    add("16t", q16t - x, 60, "residue")
    add("8n", q8n - x, 24, "residue")
    add("8t", q8t - x, 24, "residue")
    add("4n", q4n, 0, "signal")
    add("4t", q4t, 0, "signal")
    add("1n", np.where(x >= 0, 0.3, -0.3), 0, "signal")
    add("ds", ds, 0, "signal")
    c = concat(segs, gap=0.7, names=names)
    snr = {"16": D.snr_db(x, q16t), "8": D.snr_db(x, q8t), "4": D.snr_db(x, q4t), "1": D.snr_db(x, np.sign(x) * np.abs(x).max()),
           "ds": D.snr_db(x, ds)}
    return {"names": names, "gains": {"16n": 60, "16t": 60, "8n": 24, "8t": 24}, "snr": snr, "seconds": c.duration,
            "starts": {k: float(c.events[k]) for k in names}, "each": float(len(x) / SR),
            "clips": {"variation48": save_synth("tune.variation48", c, detail="the Tune's first phrase on Part 7's piano: the error at 16 bits and at 8 bits, without and with dither (amplified by 60 and 24 dB); then the Tune itself at 4 bits without and with dither, at 1 bit, and as a one-bit delta-sigma stream at 64 times the rate")}}


def compute_variation() -> dict:
    t = load("tune48")
    s = t["snr"]
    return {"part": 48, "title": "at 16, 8, 4 and 1 bit, with and without dither", "seconds": round(t["seconds"], 1),
            "measure": f"signal to error {s['16']:.0f} dB at 16 bits, {s['8']:.0f} at 8, {s['4']:.0f} at 4; one bit at 64 times the rate {s['ds']:.0f} dB",
            "clip": "tune.variation48"}


ITEMS = {"hook": compute_hook, "rate44": compute_rate44, "sampling": compute_sampling, "tones": compute_tones, "alias": compute_alias,
         "stairstep": compute_stairstep, "quant": compute_quant, "moments": compute_moments, "fade": compute_fade,
         "lowsine": compute_lowsine, "shaping": compute_shaping, "deltasigma": compute_deltasigma, "jitter": compute_jitter,
         "rate": compute_rate, "stairs": compute_stairs, "speeds": compute_speeds, "sidebands": compute_sidebands, "tune48": compute_tune48, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
