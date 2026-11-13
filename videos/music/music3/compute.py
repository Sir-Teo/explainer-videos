"""Precompute everything numerical, and every sound, in Part 3 of *Music, Built* ("The Spectrum").

    python -m videos.music.music3.compute              # everything missing (about a minute)
    python -m videos.music.music3.compute --force gabor

Numbers are cached in ``.cache/music3/<name>.json`` (+ ``.npz``), sounds in ``.cache/music3/audio/``.  The transforms
are Monochord's own (``explainer/music/monochord/dsp/fourier.py``), each checked against numpy or scipy.

Items:
    square      Fourier's claim on a square wave: partial sums, the coefficients by projection, Gibbs's overshoot;
                the square built up as sound; a square and a sawtooth for the ear
    dft         the transform as a machine: the definition against the fast algorithm, their costs, a pluck's
                spectrum, and how long one must listen to tell two notes apart
    ohm         Ohm's law of hearing as Helmholtz tested it: a bank of resonators applied to a plucked string
    phase       the same partials with different phases, low and high: the waveforms, and the sounds
    stft        the spectrogram of the Tune's opening, by our transform and by scipy's
    windows     what a window costs: main lobes and side lobes; a weak tone beside a strong one
    gabor       the uncertainty product for four shapes; tone bursts from long to very short; two pictures of one
                signal with a short and a long window
    cq          a constant-Q transform of the Tune's opening beside the ordinary one
    noise       white, pink and brown noise, and their measured slopes
    timbre      one pluck forwards, backwards and with its attack removed: spectra, attack, brightness, flux
    reassign    the frontier: an ordinary and a reassigned spectrogram of a chirp, a click and a tone
    tune        Variation 3: the Tune assembled additively, more partials in every phrase
    variation   the Variations ledger, row 3
    missing     the last sound of the part: a tone with no fundamental (for Part 4)
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy import signal

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, QUIET_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord.dsp import fourier as F
from explainer.music.monochord.instruments.plucked import C3, MONOCHORD_STRING, pluck_partials
from explainer.music.monochord.partkit import envelope, play_tune, saver, string_note
from explainer.music.monochord.pitch import nearest_note

CACHE = Cache("music3")
CLIPS = ClipStore("music3")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
SOFT = QUIET_LEVEL - 2.5
save = saver(CLIPS, LEVEL)
G3 = 196.0
BETA = 0.11


def tone(y, fade=(0.01, 0.06)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def phrase_clip(phrases=(0, 1)) -> Clip:
    """The Tune's opening on Part 1's string."""
    return play_tune(lambda hz, dur, e: string_note(C3 / hz, dur + 0.3, release=None if e["last"] else dur - 0.04),
                     phrases=list(phrases), tail=1.0)


def db(a, floor=-120.0):
    return 20 * np.log10(np.maximum(np.abs(a), 10 ** (floor / 20)))


def resonator(y: np.ndarray, hz: float, q: float = 30.0) -> np.ndarray:
    """A sound heard through one resonator (a two-pole filter): Helmholtz's glass globe held to the ear."""
    w = 2 * np.pi * hz / SR
    r = math.exp(-w / (2 * q))
    a = [1, -2 * r * math.cos(w), r * r]
    gain = abs(1 / (1 - 2 * r * math.cos(w) * np.exp(-1j * w) + r * r * np.exp(-2j * w)))   # so that its own note passes at 1
    return signal.lfilter([1 / gain], a, y)


# ---------------------------------------------------------------------------
def compute_square() -> dict:
    t = np.linspace(0, 2, 2001)                               # two periods
    target = np.sign(np.sin(2 * np.pi * t))
    counts = [1, 2, 3, 5, 10, 30]                             # how many odd harmonics
    sums = np.array([sum(4 / (np.pi * n) * np.sin(2 * np.pi * n * t) for n in range(1, 2 * k, 2)) for k in counts])
    # the coefficients by projection: how much of sin(n x) is in the square?
    x = np.linspace(0, 1, 200_001)
    sq = np.sign(np.sin(2 * np.pi * x))
    proj = [float(2 * np.trapezoid(sq * np.sin(2 * np.pi * n * x), x)) for n in range(1, 10)]
    want = [4 / (np.pi * n) if n % 2 else 0.0 for n in range(1, 10)]
    # Gibbs: the overshoot does not shrink
    fine = np.linspace(0, 0.5, 400_001)
    over = []
    for k in (10, 100, 1000):
        s = sum(4 / (np.pi * n) * np.sin(2 * np.pi * n * fine) for n in range(1, 2 * k, 2))
        over.append({"terms": k, "overshoot": float((s.max() - 1.0) / 2.0)})
    rms = [float(np.sqrt(np.mean((row - target) ** 2))) for row in sums]
    # as sound: G3 with more and more odd harmonics, at the level each sum really has
    secs = 1.0
    tt = np.arange(int(secs * SR)) / SR
    steps = [tone(sum(4 / (np.pi * n) * np.sin(2 * np.pi * n * G3 * tt) for n in range(1, 2 * k, 2) if n * G3 < 18_000))
             for k in counts]
    build = concat(steps, gap=0.12, names=[f"k{k}" for k in counts])
    saw = tone(sum(2 / (np.pi * n) * np.sin(2 * np.pi * n * G3 * tt) for n in range(1, 60) if n * G3 < 18_000))
    square = steps[-1]
    quiz = concat([saw.at_level(LEVEL), square.at_level(LEVEL)], gap=0.5, names=["A", "B"])
    # why sines: push a sine and a square through the same resonant system (a string, a pipe, a room)
    tt2 = np.arange(4800) / SR
    f_in = 400.0
    sin_in = np.sin(2 * np.pi * f_in * tt2)
    sq_in = np.sign(np.sin(2 * np.pi * f_in * tt2))
    sin_out, sq_out = resonator(sin_in, 1150.0, q=6.0), resonator(sq_in, 1150.0, q=6.0)
    seg = slice(4800 - 2 * int(SR / f_in), 4800)             # two periods, after the start has died away
    through = {k: v[seg] / np.abs(v[seg]).max() for k, v in (("sin_in", sin_in), ("sin_out", sin_out), ("sq_in", sq_in), ("sq_out", sq_out))}
    fit = np.linalg.lstsq(np.stack([sin_in[seg], np.cos(2 * np.pi * f_in * tt2[seg])], axis=1), sin_out[seg], rcond=None)
    sine_residual = float(np.sqrt(fit[1][0] / np.sum(sin_out[seg] ** 2))) if len(fit[1]) else 0.0
    # a wave that does not repeat: a pulse train with longer and longer gaps
    width = 1.0
    trains = {}
    for period in (4, 8, 32):
        k = np.arange(0, int(4 * period) + 1)
        trains[f"train_f_{period}"] = k / period
        trains[f"train_a_{period}"] = np.abs(np.sinc(k * width / period))
    env_f = np.linspace(0, 4, 400)
    return {"t": t, "target": target, "sums": sums, "counts": counts, "proj": proj, "proj_formula": want,
            **through, "sine_residual": sine_residual, **trains, "env_f": env_f, "env_a": np.abs(np.sinc(env_f)),
            "proj_worst": float(max(abs(a - b) for a, b in zip(proj, want))), "gibbs": over, "rms": rms, "f0": G3,
            "quiz_answer": "B",
            "clips": {"build": save("square.build", build, kind="synthesized", detail="sines added in the computer"),
                      "quiz": save("square.quiz", quiz, kind="synthesized", level=None)}}


def compute_dft() -> dict:
    rng = np.random.default_rng(0)
    x = rng.standard_normal(4096)
    count = [0]
    ours = F.fft(x, count)
    err = float(np.abs(ours - np.fft.fft(x)).max() / np.abs(ours).max())
    slow = float(np.abs(F.dft(x[:512]) - np.fft.fft(x[:512])).max())
    costs = [{"n": 2 ** k, "slow": (2 ** k) ** 2, "fast": (2 ** k // 2) * k} for k in (6, 10, 12, 16, 20)]
    # timings on this machine (the definition against the fast algorithm, both ours)
    timing = []
    for k in (8, 10, 12):
        n = 2 ** k
        v = rng.standard_normal(n)
        t0 = time.perf_counter()
        F.dft(v)
        t1 = time.perf_counter()
        for _ in range(20):
            F.fft(v)
        t2 = time.perf_counter()
        timing.append({"n": n, "slow_ms": 1000 * (t1 - t0), "fast_ms": 1000 * (t2 - t1) / 20})
    # a pluck, taken apart by our transform
    note = string_note(1.0, 1.0)
    n = 16384
    seg = note.mono[2400: 2400 + n] * F.window("hann", n)
    spec = np.abs(F.fft(seg))[: n // 2]
    f = np.arange(n // 2) * SR / n
    keep = f < 1700
    peaks = [float(f[int(np.argmax(np.where(np.abs(f - k * C3) < 40, spec, 0)))]) for k in range(1, 9)]
    # how long must one listen to tell A2 from the note a semitone above it?
    a2 = 110.0
    gap = a2 * (2 ** (1 / 12) - 1)
    return {"err": err, "slow_err": slow, "mults_4096": count[0], "costs": costs, "timing": timing,
            "f": f[keep], "spec_db": db(spec[keep] / spec.max()), "bin_hz": SR / n, "n": n, "peaks": peaks,
            "worked": {"a2": a2, "gap_hz": gap, "seconds": 1 / gap, "samples": SR / gap,
                       "pow2": int(2 ** math.ceil(math.log2(SR / gap)))}}


def compute_ohm() -> dict:
    note = string_note(1.0, 2.0)
    y = note.mono.astype(np.float64)
    hz = [C3 * k for k in range(1, 11)]
    seg = slice(4800, 4800 + 24000)                         # the same half second for both methods
    bank = np.array([np.sqrt(np.mean(resonator(y, f)[seg] ** 2)) for f in hz])
    # the reference: each partial cut out of the spectrum of the whole note, and its strength in that half second
    spec = np.fft.rfft(y)
    f = np.fft.rfftfreq(len(y), 1 / SR)
    direct = np.array([np.sqrt(np.mean(np.fft.irfft(np.where(np.abs(f - v) < 0.4 * C3, spec, 0), len(y))[seg] ** 2)) for v in hz])
    a, b = bank / bank.max(), direct / direct.max()
    strong = b > 0.1                                        # a resonator this sharp cannot isolate a partial 40 dB down
    worst = float(np.abs(20 * np.log10(a[strong] / b[strong])).max())
    heard = {k: tone(resonator(y, C3 * k, q=40.0)) for k in (3, 5)}
    seq = concat([note.at_level(LEVEL), heard[3].at_level(LEVEL), heard[5].at_level(LEVEL)], gap=0.2,
                 names=["all", "p3", "p5"])
    clar = 146.83
    worked = {"f0": clar, "globes": [clar * k for k in range(1, 7)], "sing": [1, 3, 5]}
    return {"hz": hz, "bank": a.tolist(), "fft": b.tolist(), "worst_db": worst, "strong": int(strong.sum()), "worked": worked,
            "notes": [nearest_note(v)[0] for v in hz],
            "clips": {"globe": save("ohm.globe", seq, level=None, detail="the string, then through one resonator")}}


def compute_phase() -> dict:
    rng = np.random.default_rng(4)
    out, clips = {}, {}
    for name, f0 in (("low", 65.41), ("high", 523.25)):
        n = int(4000 // f0)
        amps = [1.0 / k for k in range(1, n + 1)]
        rand = rng.uniform(0, 2 * np.pi, n)
        a = F.additive(f0, amps, 1.4, SR, phases=[np.pi / 2] * n)       # every partial starts at its crest
        b = F.additive(f0, amps, 1.4, SR, phases=rand)
        one = int(round(SR / f0))
        tt = np.arange(SR // 2) / SR                                      # half a second after the attack
        sa, sb = (np.array([abs(np.mean(v[SR // 4: SR // 4 + SR // 2] * np.exp(-2j * np.pi * k * f0 * tt)))
                            for k in range(1, n + 1)]) for v in (a, b))
        out[name] = {"f0": f0, "harmonics": n, "crest_a": float(np.abs(a).max() / np.sqrt(np.mean(a ** 2))),
                     "crest_b": float(np.abs(b).max() / np.sqrt(np.mean(b ** 2))),
                     "spectrum_gap_db": float(np.abs(20 * np.log10(sa / sb)).max()),
                     "note": nearest_note(f0)[0]}
        out[f"wave_{name}_a"] = a[SR // 2: SR // 2 + 2 * one]
        out[f"wave_{name}_b"] = b[SR // 2: SR // 2 + 2 * one]
        ca, cb = tone(a).at_level(LEVEL), tone(b)
        cb = cb.gain(20 * math.log10(np.sqrt(np.mean(ca.mono ** 2)) / np.sqrt(np.mean(cb.mono ** 2))))   # the same power
        clips[name] = save(f"phase.{name}", concat([ca, cb], gap=0.4, names=["A", "B"]), kind="synthesized", level=None,
                           detail="the same partials, different phases")
    flat = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
    return {"low": out["low"], "high": out["high"], **flat, "clips": clips}


def compute_stft() -> dict:
    c = phrase_clip().at_level(LEVEL)
    y = c.mono.astype(np.float64)
    f, t, S = F.stft(y, SR, 2048, 512)
    f2, t2, S2 = signal.stft(y, SR, window="hann", nperseg=2048, noverlap=1536, boundary="zeros", padded=False)
    m = min(S.shape[1], S2.shape[1])
    gap = float(np.abs(np.abs(S[:, 2:m - 2]) - np.abs(S2[:, 2:m - 2]) * 1024).max() / np.abs(S).max())
    from explainer.music.monochord.physics import air

    v_car = 28.0
    yp, heard = air.passing_source(392.0, v_car, 6.0, 5.0, harmonics=(1.0, 0.5, 0.33, 0.2))
    up, down = air.doppler(392.0, v_car)
    return {"scipy_gap": gap, "frames": int(S.shape[1]), "bins": int(S.shape[0]), "hop_ms": 1000 * 512 / SR,
            "window_ms": 1000 * 2048 / SR, "bin_hz": SR / 2048, "pass_kmh": v_car * 3.6, "pass_up": up, "pass_down": down,
            "clips": {"phrase": save("stft.phrase", c, level=None),
                      "glide": save("stft.glide", Clip(yp).fade(0.3, 0.3), kind="synthesized", detail="Part 2's passing horn")}}


def compute_windows() -> dict:
    rows, curves = [], {}
    for name in ("rect", "hann", "hamming", "blackman"):
        g = F.leakage(name)
        rows.append({"name": name, "side": g["side_lobe_db"], "lobe": g["main_lobe_bins"]})
        curves[f"curve_{name}"] = np.maximum(g["spectrum_db"], -100.0)
    bins = F.leakage("hann")["bins"]
    # a weak tone, 46 dB down, seven and a half bins from a strong one that falls between two bins
    n = 1024
    k = np.arange(n)
    x = np.sin(2 * np.pi * 100.5 * k / n) + 10 ** (-46 / 20) * np.sin(2 * np.pi * 108.0 * k / n)
    seen = {}
    for name in ("rect", "hann"):
        w = F.window(name, n)
        s = np.abs(np.fft.rfft(x * w)) / (w.sum() / 2)
        seen[f"two_{name}"] = db(s[80:130], -100.0)
    floor_rect = float(seen["two_rect"][26:30].min())
    return {"rows": rows, "bins": bins, **curves, **seen, "two_bins": np.arange(80, 130), "weak_db": -46.0,
            "weak_bin": 108.0, "strong_bin": 100.5, "rect_floor_near_weak": floor_rect,
            "hann_dip": float(seen["two_hann"][24:27].min())}


def compute_gabor() -> dict:
    floor = 1 / (4 * math.pi)
    t = (np.arange(8192) - 4096) / SR
    shapes = {"a Gaussian": np.exp(-0.5 * (t / 0.004) ** 2),
              "a Hann window": np.concatenate([np.zeros(3072), F.window("hann", 2048), np.zeros(3072)]),
              "a decaying ring": np.where(t >= 0, np.exp(-t / 0.004), 0.0),
              "a rectangle": np.concatenate([np.zeros(3072), np.ones(2048), np.zeros(3072)])}
    rows = []
    for name, x in shapes.items():
        dt, df = F.spreads(x, SR)
        rows.append({"name": name, "dt_ms": 1000 * dt, "df_hz": df, "product": dt * df, "times_floor": dt * df / floor})
    # bursts of a 440 Hz tone, from long to very short
    bursts, clips_, env = [], [], {}
    for ms in (200, 50, 12, 3):
        y = F.tone_burst(440.0, ms / 1000)
        e = np.exp(-0.5 * (((np.arange(len(y)) - len(y) / 2) / SR) / (ms / 4000)) ** 2)
        dt, df = F.spreads(e, SR)
        bursts.append({"ms": ms, "dt_ms": 1000 * dt, "df_hz": df, "semitones": 12 * math.log2((440 + df) / (440 - df)),
                       "cycles": 440 * ms / 1000})
        pad = np.zeros(int(0.25 * SR))
        clips_.append(Clip(np.concatenate([pad, y, pad, y, pad])))
    seq = concat(clips_, gap=0.1, names=[f"b{b['ms']}" for b in bursts])
    # the ear question: one pair is a semitone apart, the other is the same note twice
    def pair(f1, f2, ms):
        gap = np.zeros(int(0.35 * SR))
        return Clip(np.concatenate([gap, F.tone_burst(f1, ms / 1000), gap, F.tone_burst(f2, ms / 1000), gap]))

    semi = 440 * 2 ** (1 / 12)
    quiz = concat([pair(440, 440, 5), pair(440, semi, 5)], gap=0.5, names=["A", "B"])
    easy = concat([pair(440, 440, 120), pair(440, semi, 120)], gap=0.5, names=["A", "B"])
    # one signal, two windows: two clicks 30 ms apart, then two tones 40 Hz apart
    n = int(0.6 * SR)
    x = np.zeros(n)
    clicks = (90, 120)
    for ms in clicks:
        x[int(ms / 1000 * SR)] = 30.0
    tt = np.arange(n) / SR
    on = (tt > 0.3) & (tt < 0.55)
    x += on * (np.sin(2 * np.pi * 1000 * tt) + np.sin(2 * np.pi * 1040 * tt))
    pics = {}
    pad, hop = 8192, 64
    for name, win in (("short", 256), ("long", 4096)):
        w = F.window("hann", win)
        xp = np.concatenate([np.zeros(win // 2), x, np.zeros(win // 2)])
        cols = [np.abs(np.fft.rfft(xp[a: a + win] * w, pad)) for a in range(0, len(xp) - win, hop)]   # padded: a smooth picture
        S = np.array(cols).T
        f = np.fft.rfftfreq(pad, 1 / SR)
        band = (f >= 850) & (f <= 1200)
        pics[f"pic_{name}"] = db(S[band] / S[band].max(), -60.0).astype(np.float32)
        pics[f"{name}_ms"] = 1000 * win / SR
    pics["signal"] = x[:: 24].astype(np.float32)
    return {"floor": floor, "rows": rows, "bursts": bursts, **pics, "pic_seconds": 0.6, "pic_band": [850, 1200],
            "clicks_ms": clicks[1] - clicks[0], "tones_hz": 40, "quiz_answer": "B", "quiz_ms": 5, "easy_ms": 120,
            "clips": {"bursts": save("gabor.bursts", seq, kind="synthesized", detail="one tone, shorter and shorter"),
                      "quiz": save("gabor.quiz", quiz, kind="synthesized"),
                      "easy": save("gabor.easy", easy, kind="synthesized")}}


def compute_cq() -> dict:
    c = CLIPS.load("stft.phrase") if CLIPS.has("stft.phrase") else phrase_clip().at_level(LEVEL)
    y = c.mono.astype(np.float64)
    freqs, times, C, q = F.cqt(y, SR, fmin=C3 / 2, bins_per_octave=24, n_bins=24 * 5, hop=1024)
    f, t, S = F.stft(y, SR, 4096, 1024)
    band = f <= C3 * 16
    # every note of the Tune's first phrase lands on a bin a whole number of semitones above the tonic
    notes = [n for n in c.notes if n["phrase"] == 0]
    right = 0
    for n_ in notes:
        m = int(np.argmin(np.abs(times - (n_["t"] + 0.25))))
        lo, hi = int(np.searchsorted(freqs, n_["hz"] * 0.9)), int(np.searchsorted(freqs, n_["hz"] * 1.1))
        k = lo + int(np.argmax(np.abs(C[lo:hi, m])))
        right += k == int(round(24 * math.log2(n_["hz"] / (C3 / 2))))
    return {"q": q, "bins_per_octave": 24, "cq": db(C / np.abs(C).max(), -70.0).astype(np.float32),
            "lin": db(S[band] / np.abs(S).max(), -70.0).astype(np.float32), "cq_fmin": C3 / 2, "octaves": 5,
            "lin_fmax": C3 * 16, "seconds": float(c.duration), "notes_in_their_bin": right, "notes": len(notes),
            "window_low_ms": 1000 * q / (C3 / 2), "window_high_ms": 1000 * q / (C3 * 16)}


def compute_noise() -> dict:
    rows, parts, bands = [], [], {}
    for name, beta in (("white", 0.0), ("pink", 1.0), ("brown", 2.0)):
        y = F.colored_noise(int(2.0 * SR), beta, SR, seed=11)
        long_ = F.colored_noise(SR * 8, beta, SR, seed=12)
        slope = F.octave_slope(long_, SR)
        rows.append({"name": name, "beta": beta, "slope": slope, "want": -3.0103 * beta})
        parts.append(Clip(y).fade(0.05, 0.1).at_level(LEVEL))
        n = 1 << 13
        w = F.window("hann", n)
        psd = np.mean([np.abs(np.fft.rfft(long_[a: a + n] * w)) ** 2 for a in range(0, len(long_) - n, n // 2)], axis=0)
        f = np.fft.rfftfreq(n, 1 / SR)
        fc = [31.25 * 2 ** k for k in range(9)]
        lev = [10 * math.log10(psd[(f >= c / math.sqrt(2)) & (f < c * math.sqrt(2))].sum()) for c in fc]
        bands[f"oct_{name}"] = np.array(lev) - max(lev)
    seq = concat(parts, gap=0.3, names=["white", "pink", "brown"])
    pink = F.colored_noise(SR * 30, 1.0, SR, seed=21)
    n = 4096
    w = F.window("hann", n)
    frames = np.array([np.abs(np.fft.rfft(pink[a: a + n] * w)) ** 2 for a in range(0, len(pink) - n, n)])
    f = np.fft.rfftfreq(n, 1 / SR)
    keep = (f >= 60) & (f <= 12000)
    ref = frames.mean(axis=0)[keep].max()
    one_db = 10 * np.log10(frames[3][keep] / ref)
    mean_db = 10 * np.log10(frames.mean(axis=0)[keep] / ref)
    scatter = float(np.std(one_db - mean_db))
    return {"rows": rows, "centres": [31.25 * 2 ** k for k in range(9)], **bands, "avg_f": f[keep], "one_db": one_db,
            "mean_db": mean_db, "avg_frames": int(len(frames)), "one_scatter_db": scatter,
            "clips": {"colours": save("noise.colours", seq, kind="synthesized", level=None, detail="equal loudness")}}


def compute_timbre() -> dict:
    note = string_note(1.0, 1.8)
    y = note.mono.astype(np.float64)
    back = y[::-1].copy()
    cut_at = 0.12
    cut = y[int(cut_at * SR):].copy()
    ramp = int(0.25 * SR)
    cut[:ramp] *= np.linspace(0, 1, ramp) ** 2
    sa, sb = np.abs(np.fft.rfft(y)), np.abs(np.fft.rfft(back))
    gap = float(np.abs(sa - sb).max() / sa.max())
    # brightness over time: the centroid of each 50 ms
    hop = int(0.05 * SR)
    cen = [F.centroid(y[a: a + 2 * hop], SR) for a in range(0, len(y) - 2 * hop, hop)]
    fl = F.flux(y, SR)
    rows = []
    for name, v in (("forwards", y), ("backwards", back), ("attack removed", cut)):
        rows.append({"name": name, "attack_ms": 1000 * F.attack_time(v, SR), "centroid": F.centroid(v, SR)})
    clips_ = [Clip(v).fade(0.004, 0.05).at_level(LEVEL) for v in (y, back, cut)]
    seq = concat(clips_, gap=0.4, names=["fwd", "back", "cut"])
    return {"spectrum_gap": gap, "rows": rows, "centroid": np.array(cen), "centroid_dt": 0.05, "flux": fl,
            "flux_dt": 256 / SR, "cut_ms": 1000 * cut_at, "env_fwd": envelope(clips_[0]), "env_back": envelope(clips_[1]),
            "env_cut": envelope(clips_[2]),
            "clips": {"three": save("timbre.three", seq, level=None, detail="one pluck: forwards, backwards, without its attack")}}


def compute_reassign() -> dict:
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    x = signal.chirp(t, 600.0, t[-1], 5000.0) * np.hanning(n) ** 0.25 + 0.7 * np.sin(2 * np.pi * 5600 * t)
    x[int(0.25 * SR)] += 40.0
    freqs, times, plain, sharp = F.reassigned(x, SR, 1024, 64)
    band = freqs <= 6500

    def pic(E):
        return (10 * np.log10(np.maximum(E[band] / E[band].max(), 1e-7))).astype(np.float32)

    return {"plain": pic(plain), "sharp": pic(sharp), "cells_plain": F.cells_for(plain[band]),
            "cells_sharp": F.cells_for(sharp[band]), "ratio": F.cells_for(plain[band]) / F.cells_for(sharp[band]),
            "seconds": 0.5, "fmax": 6500.0, "window_ms": 1000 * 1024 / SR,
            "oppenheim": {"year": 2013, "best": 13, "subjects": 12}}


def compute_tune() -> dict:
    counts = [1, 2, 3, 5, 8, 16]                            # partials in each of the six phrases

    def voice(hz, dur, e):
        k = counts[e["phrase"]]
        s = MONOCHORD_STRING.with_(L=MONOCHORD_STRING.L * C3 / hz)
        p = pluck_partials(s, BETA)
        amps = np.abs(np.asarray(p["force"], dtype=float))[:k]
        y = F.additive(hz, amps / amps.max(), dur + 0.35, SR, decays=np.asarray(p["decay"], dtype=float)[:k], attack=0.004)
        return Clip(y).fade(0.002, 0.08).at_level(LEVEL)

    c = play_tune(voice, tail=1.2)
    y = c.mono.astype(np.float64)
    rows = []
    for ph, k in enumerate(counts):
        a, b = c.events[f"phrase{ph}"], (c.events[f"phrase{ph + 1}"] if ph < 5 else c.events["end"])
        seg = y[int(a * SR): int(b * SR)]
        f0s = [n["hz"] * n["dur"] for n in c.notes if n["phrase"] == ph]
        mean_f0 = sum(f0s) / sum(n["dur"] for n in c.notes if n["phrase"] == ph)
        rows.append({"phrase": ph, "partials": k, "centroid": F.centroid(seg, SR),
                     "brightness": F.centroid(seg, SR) / mean_f0})
    # count the partials in one note of each phrase from its spectrum
    seen = []
    for ph, k in enumerate(counts):
        n_ = next(n for n in c.notes if n["phrase"] == ph)
        seg = y[int((n_["t"] + 0.03) * SR): int((n_["t"] + 0.03) * SR) + 16384]
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        f = np.fft.rfftfreq(len(seg), 1 / SR)
        top = spec.max()
        seen.append(int(sum(spec[np.abs(f - j * n_["hz"]) < 12].max() > 0.02 * top for j in range(1, 25))))
    notes = [{**n, "partials": counts[n["phrase"]]} for n in c.notes]
    c = Clip(c.y, SR, c.events, notes)
    info = save("tune.variation3", c, kind="synthesized", detail="sums of sines, with the string's own decays")
    return {"clip": info, "notes": notes, "counts": counts, "rows": rows, "seen": seen, "seconds": c.duration,
            "brighter": rows[-1]["brightness"] / rows[0]["brightness"]}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 3, "title": r"assembled from pure tones: 1, 2, 3, 5, 8 and 16 partials, phrase by phrase",
            "seconds": t["seconds"],
            "measure": rf"its brightness rises {t['brighter']:.1f} times from the first phrase to the last",
            "clip": "tune.variation3"}


def compute_missing() -> dict:
    f0 = C3
    tt = 1.6
    upper = F.additive(f0, [0, 0, 0, 1, 1, 1, 1, 1], tt, SR)
    pure = F.additive(f0, [1], tt, SR)
    full = F.additive(f0, [1, 1, 1, 1, 1, 1, 1, 1], tt, SR)
    seq = concat([tone(full).at_level(LEVEL), tone(upper).at_level(LEVEL), tone(pure).at_level(LEVEL - 4)], gap=0.4,
                 names=["full", "upper", "pure"])
    spec = np.abs(np.fft.rfft(upper[4800: 4800 + 32768] * np.hanning(32768)))
    f = np.fft.rfftfreq(32768, 1 / SR)
    at_f0 = 20 * math.log10(spec[np.abs(f - f0) < 5].max() / spec.max())
    return {"f0": f0, "present": [4, 5, 6, 7, 8], "level_at_f0_db": at_f0,
            "clips": {"tease": save("missing.tease", seq, kind="synthesized", level=None)}}


ITEMS = {"square": compute_square, "dft": compute_dft, "ohm": compute_ohm, "phase": compute_phase,
         "stft": compute_stft, "windows": compute_windows, "gabor": compute_gabor, "cq": compute_cq,
         "noise": compute_noise, "timbre": compute_timbre, "reassign": compute_reassign, "tune": compute_tune,
         "variation": compute_variation, "missing": compute_missing}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
