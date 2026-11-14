"""Precompute every number in Part 15 of *Psychology, Built* ("The Other Senses").

    python -m videos.psychology.psych15.compute            # everything missing (about a minute)
    python -m videos.psychology.psych15.compute --force pitch

Results are cached in ``.cache/psych15/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The sounds the film
plays are written as WAV files into ``.cache/psych15/sounds/`` (``sound_path(name)``).  The models are Psyche's
(``explainer.psychology.psyche.hearing``).

Items:
    sounds      the sounds the film plays: a harmonic complex with and without its fundamental, a pure tone at the
                missing pitch, two streaming sequences, two intervals
    levels      decibels and pressures for everyday sounds
    cochlea     Greenwood's map; travelling-wave snapshots; a gammatone filter bank's excitation patterns
    masking     the band-widening experiment under the power-spectrum model
    pitch       spectra and summary autocorrelations for complexes with and without the fundamental
    itd         Woodworth's interaural delays; a Jeffress array's counts
    speech      identification and predicted discrimination along a continuum; McGurk fusion across simulated
                listeners
    music       sensory dissonance of two harmonic tones against their interval
    gate        the gate circuit's output against injury and touch input
    smell       how a count of discriminable mixtures depends on the threshold of overlap
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from explainer.ai.cache import Cache
from explainer.psychology.psyche import hearing as H

CACHE = Cache("psych15")
load = CACHE.load
FS = 16000
SOUNDS = Path(".cache/psych15/sounds")


def sound_path(name: str) -> str:
    return str(SOUNDS / f"{name}.wav")


def _write(name, x, fs=FS, peak=0.35, ramp=0.01):
    x = np.asarray(x, float).copy()
    n = int(ramp * fs)
    w = np.ones_like(x)
    w[:n] = np.linspace(0, 1, n)
    w[-n:] = np.linspace(1, 0, n)
    x = x * w
    x = peak * x / (np.abs(x).max() + 1e-12)
    SOUNDS.mkdir(parents=True, exist_ok=True)
    wavfile.write(sound_path(name), fs, (x * 32767).astype(np.int16))
    return float(len(x) / fs)


def _seq(freqs, tone_dur=0.1, gap=0.02, fs=FS):
    parts = []
    for f in freqs:
        parts.append(H.tone(f, tone_dur, fs) * (np.hanning(int(tone_dur * fs)) ** 0.3) if f else np.zeros(int(tone_dur * fs)))
        parts.append(np.zeros(int(gap * fs)))
    return np.concatenate(parts)


def compute_sounds() -> dict:
    d = {}
    d["full"] = _write("full", H.harmonic_complex(200, range(1, 7), 1.2, FS))
    d["missing"] = _write("missing", H.harmonic_complex(200, range(3, 7), 1.2, FS))
    d["pure200"] = _write("pure200", H.tone(200, 1.2, FS))
    d["high"] = _write("high", H.harmonic_complex(200, range(5, 9), 1.2, FS))
    close = [500, 560, 500, 0] * 8
    far = [500, 1000, 500, 0] * 8
    d["stream_close"] = _write("stream_close", _seq(close))
    d["stream_far"] = _write("stream_far", _seq(far))
    fifth = H.harmonic_complex(220, range(1, 7), 1.5, FS) + H.harmonic_complex(330, range(1, 7), 1.5, FS)
    tritone = H.harmonic_complex(220, range(1, 7), 1.5, FS) + H.harmonic_complex(220 * 2 ** 0.5, range(1, 7), 1.5, FS)
    d["fifth"] = _write("fifth", fifth)
    d["tritone"] = _write("tritone", tritone)
    return {"durations": d}


def compute_levels() -> dict:
    # typical levels, as usually tabulated (approximate)
    items = [("threshold of hearing at 1 kHz", 0), ("rustling leaves", 20), ("quiet library", 40),
             ("conversation at 1 m", 60), ("busy street", 80), ("loud concert", 110), ("threshold of pain", 130)]
    return {"names": [n for n, _ in items], "db": [float(v) for _, v in items],
            "pa": [float(H.pressure(v)) for _, v in items], "ratio": float(H.pressure(130) / H.pressure(0)),
            "f": np.geomspace(20, 16000, 200), "tq": H.threshold_in_quiet(np.geomspace(20, 16000, 200)),
            "tq_min_f": float(np.geomspace(20, 16000, 2000)[np.argmin(H.threshold_in_quiet(np.geomspace(20, 16000, 2000)))]),
            "tq_min": float(H.threshold_in_quiet(np.geomspace(20, 16000, 2000)).min()),
            "tq_50": float(H.threshold_in_quiet(50.0)), "tq_1k": float(H.threshold_in_quiet(1000.0))}


def compute_cochlea() -> dict:
    x = np.linspace(0, 1, 300)
    bf = H.greenwood(x)
    xs = np.linspace(0, 1, 400)
    waves = {}
    for f in (250, 1000, 4000):
        waves[str(f)] = np.array([H.travelling_wave(f, xs, t) for t in np.linspace(0, 1 / f, 12, endpoint=False)])
    cfs = H.erb_space(80, 7000, 48)
    ex = {}
    for name, sig in (("500", H.tone(500, 0.2, FS)), ("2000", H.tone(2000, 0.2, FS)),
                      ("complex", H.harmonic_complex(200, range(1, 11), 0.2, FS))):
        e = H.excitation(sig, cfs, FS)
        ex[name] = 20 * np.log10(e / e.max() + 1e-6)
    return {"x": x, "bf": bf, "xs": xs, "w250": waves["250"], "w1000": waves["1000"], "w4000": waves["4000"],
            "cfs": cfs, "ex500": ex["500"], "ex2000": ex["2000"], "excomplex": ex["complex"],
            "place250": float(H.greenwood_place(250)), "place1000": float(H.greenwood_place(1000)),
            "place4000": float(H.greenwood_place(4000)), "erb1000": float(H.erb(1000)), "erb4000": float(H.erb(4000))}


def compute_masking() -> dict:
    bw = np.geomspace(10, 2000, 80)
    thr = np.array([H.masked_threshold(2000, b, 20.0) for b in bw])
    return {"bw": bw, "thr": thr, "erb": float(H.erb(2000))}


def compute_pitch() -> dict:
    out = {}
    for name, hs in (("full", range(1, 7)), ("missing", range(3, 7)), ("high", range(5, 9))):
        x = H.harmonic_complex(200, hs, 0.25, FS)
        f, A = H.spectrum(x, FS)
        lags, s = H.summary_autocorrelation(x, FS, max_lag=0.015)
        out[f"f_{name}"] = f[f <= 2000]
        out[f"A_{name}"] = A[f <= 2000]
        out[f"lag_{name}"] = lags
        out[f"sac_{name}"] = s
        out[f"pitch_{name}"] = H.pitch(x, FS)
        out[f"w_{name}"] = x[: int(0.015 * FS)]
    out["w_t"] = np.arange(int(0.015 * FS)) / FS * 1000
    out["w_pure"] = H.tone(200, 0.015, FS)
    return out


def compute_itd() -> dict:
    az = np.linspace(-90, 90, 181)
    rng = np.random.default_rng(1515)
    true = float(H.itd(30))
    L = H.phase_locked_spikes(500, 0.0, 3.0, rng, rate=0.5)
    R = H.phase_locked_spikes(500, true, 3.0, rng, rate=0.5)
    delays = np.arange(-700, 701, 25) * 1e-6
    counts = H.jeffress(L, R, delays)
    best = float(delays[np.argmax(counts)])
    return {"az": az, "itd_us": H.itd(az) * 1e6, "max_us": float(H.itd(90) * 1e6), "true_us": true * 1e6,
            "delays_us": delays * 1e6, "counts": counts, "best_us": best * 1e6,
            "best_az": H.azimuth_from_itd(best)}


def compute_speech() -> dict:
    steps = np.arange(1, 15)
    p = H.identification(steps, 7.5, 0.6)
    abx_pairs = steps[:-2]
    abx = H.abx_from_labels(p[:-2], p[2:])
    # McGurk across simulated listeners: each has their own visual reliability
    rng = np.random.default_rng(1516)
    scale = np.exp(rng.normal(np.log(0.45), 0.4, 300))  # how noisy a listener is overall
    trust = np.exp(rng.normal(0.0, 1.2, 300))  # how much more the lips are trusted than the voice
    res = np.array([H.mcgurk(0.0, 2.0, a, v, n=400, rng=rng) for a, v in zip(scale * np.sqrt(trust),
                                                                             scale / np.sqrt(trust))])
    fused = res[:, 1]
    typical = H.mcgurk(0.0, 2.0, 0.45, 0.45, n=20000, rng=rng)
    return {"steps": steps, "ident": p, "abx_x": abx_pairs + 1, "abx": abx, "fused": fused,
            "typical": typical, "median_fused": float(np.median(fused)), "share_never": float((fused < 0.05).mean()),
            "share_always": float((fused > 0.9).mean()), "mean_b": float(res[:, 0].mean()),
            "mean_g": float(res[:, 2].mean())}


def _dissonance(f1, f2, a1=1.0, a2=1.0):
    # Plomp and Levelt's roughness curve in Sethares's parametrisation
    fmin, fmax = min(f1, f2), max(f1, f2)
    s = 0.24 / (0.021 * fmin + 19)
    d = fmax - fmin
    return a1 * a2 * (math.exp(-3.5 * s * d) - math.exp(-5.75 * s * d))


def compute_music() -> dict:
    base = 220.0
    ratios = np.linspace(1.0, 2.05, 600)
    amps = [0.88 ** k for k in range(6)]
    diss = []
    for r in ratios:
        tot = 0.0
        for i, ai in enumerate(amps):
            for j, aj in enumerate(amps):
                tot += _dissonance(base * (i + 1), base * r * (j + 1), ai, aj)
        diss.append(tot)
    diss = np.array(diss)
    named = {"unison": 1.0, "minor third": 6 / 5, "major third": 5 / 4, "fourth": 4 / 3, "fifth": 3 / 2,
             "major sixth": 5 / 3, "octave": 2.0, "tritone": 2 ** 0.5}
    return {"ratio": ratios, "diss": diss / diss.max(), "names": list(named), "ratios_named": list(named.values())}


def compute_gate() -> dict:
    small = np.linspace(0, 2, 100)
    out = {f"T_{k}": H.gate(L, small) for k, L in (("none", 0.0), ("some", 0.6), ("rub", 1.2))}
    return {"small": small, **out, "at1_none": float(H.gate(0.0, 1.0)), "at1_rub": float(H.gate(1.2, 1.0))}


def compute_smell() -> dict:
    thr = np.linspace(0.3, 0.95, 40)
    est = np.array([H.bushdid_estimate(128, 30, t) for t in thr])
    marks = {str(t): float(H.bushdid_estimate(128, 30, t)) for t in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9)}
    return {"thr": thr, "log10_est": np.log10(est), "marks": marks}


ITEMS = {
    "sounds": compute_sounds,
    "levels": compute_levels,
    "cochlea": compute_cochlea,
    "masking": compute_masking,
    "pitch": compute_pitch,
    "itd": compute_itd,
    "speech": compute_speech,
    "music": compute_music,
    "gate": compute_gate,
    "smell": compute_smell,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
