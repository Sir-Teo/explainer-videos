"""Monochord's mastering bench (Part 57 of *Music, Built*): meters, gating, true peak, a look-ahead limiter, a mastering
chain, platform normalization, dither and the RIAA curve.

    k_response(f)                           BS.1770's K-weighting filter, its magnitude in dB
    blocks(y)                               momentary (400 ms) block loudness, 75 % overlap, with the gates
    short_term(y) / loudness_range(y)       3 s loudness and EBU Tech 3342's loudness range (LRA)
    sample_peak_db / true_peak_db           the largest sample, and the largest reconstructed value (4x oversampled)
    vu(y) / ppm(y)                          a VU meter's 300 ms average and a peak programme meter's quick rise
    limiter(y, ceiling, ...)                a look-ahead brick-wall limiter that never lets a true peak through
    master(y, target, ...)                  a mastering chain: tilt EQ, glue compression, limiter, to a loudness
    normalize(y, target)                    what a streaming service does: one gain to its target
    tpdf_dither / quantize / shaped         rounding to a word length, with and without dither and noise shaping
    riaa_db(f)                              the RIAA playback curve, 0 dB at 1 kHz

No manim here.  Checked in ``tests/music/test_master.py`` (and the meter against ffmpeg's ebur128).
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import freqz, lfilter, resample_poly

from explainer.music.monochord import loudness as LN
from explainer.music.monochord import effects as E
from explainer.music.monochord import dynamics as D
from explainer.music.monochord import Clip

SR = 48000


def stereo(y) -> np.ndarray:
    y = np.asarray(y, float)
    return np.stack([y, y], axis=1) / math.sqrt(2) if y.ndim == 1 else y


def lufs(y, sr: int = SR) -> float:
    return LN.integrated(Clip(stereo(y), sr))


# --------------------------------------------------------------------------------------------- meters
def k_response(f, sr: int = SR) -> np.ndarray:
    """The K-weighting filter's magnitude (dB) at frequencies ``f``: a +4 dB shelf above about 1.5 kHz (the head) and
    a high-pass near 40 Hz (the revised low-frequency B curve)."""
    f = np.asarray(f, float)
    w = 2 * np.pi * f / sr
    _, h1 = freqz(LN._SHELF_B, LN._SHELF_A, worN=w)
    _, h2 = freqz(LN._HP_B, LN._HP_A, worN=w)
    return 20 * np.log10(np.abs(h1 * h2) + 1e-12)


def blocks(y, sr: int = SR) -> dict:
    """Every 400 ms block's loudness (LUFS), 100 ms apart, and BS.1770's two gates: -70 LUFS absolute, then 10 LU
    below the loudness of the blocks that passed the first."""
    c = Clip(stereo(y), sr)
    p = LN.block_power(c)
    lk = -0.691 + 10 * np.log10(p + 1e-20)
    first = lk > LN.ABS_GATE
    ungated = -0.691 + 10 * np.log10(np.mean(p[first]) + 1e-20) if first.any() else -np.inf
    rel = ungated + LN.REL_GATE
    second = first & (lk > rel)
    integ = -0.691 + 10 * np.log10(np.mean(p[second]) + 1e-20) if second.any() else -np.inf
    return {"t": (np.arange(len(p)) * LN.BLOCK * (1 - LN.OVERLAP)).tolist(), "lk": lk, "abs_gate": LN.ABS_GATE, "rel_gate": rel,
            "kept": second, "integrated": float(integ), "ungated": float(ungated)}


def short_term(y, sr: int = SR, hop: float = 0.1) -> np.ndarray:
    """3 s windows, every ``hop`` seconds: the short-term loudness of EBU R 128."""
    yk = np.stack([LN.k_weight(c, sr) for c in stereo(y).T], axis=1)
    n, h = int(3.0 * sr), int(hop * sr)
    out = []
    for a in range(0, max(1, len(yk) - n + 1), h):
        ms = np.mean(yk[a:a + n] ** 2, axis=0).sum()
        out.append(-0.691 + 10 * math.log10(ms + 1e-20))
    return np.array(out)


def loudness_range(y, sr: int = SR) -> float:
    """EBU Tech 3342: short-term levels, gated at -70 LUFS and 20 LU below their own mean, from the 10th to the 95th
    percentile."""
    st = short_term(y, sr)
    st = st[st > -70]
    if not len(st):
        return 0.0
    mean = 10 * math.log10(np.mean(10 ** (st / 10)))
    st = st[st > mean - 20]
    return float(np.percentile(st, 95) - np.percentile(st, 10))


def sample_peak_db(y) -> float:
    return float(20 * np.log10(np.max(np.abs(y)) + 1e-12))


def true_peak_db(y, sr: int = SR, oversample: int = 4) -> float:
    y = np.asarray(y, float)
    return LN.true_peak_db(Clip(np.stack([y, y], axis=1) if y.ndim == 1 else y, sr), oversample)


def vu(y, sr: int = SR) -> np.ndarray:
    """A VU meter: full-wave rectified and averaged, about 300 ms to settle (a second-order low-pass); dB re full scale
    of a sine."""
    m = np.abs(np.asarray(y, float) if np.asarray(y).ndim == 1 else np.asarray(y).mean(axis=1))
    a = math.exp(-1 / (0.065 * sr))
    e = lfilter([1 - a], [1, -a], lfilter([1 - a], [1, -a], m))
    return 20 * np.log10(e * math.pi / 2 + 1e-9)


def ppm(y, sr: int = SR, rise_ms: float = 10.0, fall_db_per_s: float = 8.6) -> np.ndarray:
    """A peak programme meter: a quick rise, a slow fall (about 20 dB in 2.8 s, the BBC's)."""
    m = np.abs(np.asarray(y, float) if np.asarray(y).ndim == 1 else np.asarray(y).mean(axis=1))
    out = np.empty(len(m))
    e = 0.0
    ar = math.exp(-1 / (rise_ms * 1e-3 * sr))
    fall = 10 ** (-fall_db_per_s / 20 / sr)
    for i, v in enumerate(m):
        e = ar * e + (1 - ar) * v if v > e else e * fall
        out[i] = e
    return 20 * np.log10(out + 1e-9)


# --------------------------------------------------------------------------------------------- the limiter
def limiter(y, ceiling_db: float = -1.0, lookahead_ms: float = 1.5, release_ms: float = 80.0, sr: int = SR, oversample: int = 4) -> dict:
    """A look-ahead brick-wall limiter.  The detector is the true (4x oversampled) peak across channels; the gain
    needed at each sample is min(1, ceiling / peak); a minimum filter over the look-ahead window starts every
    reduction before the peak it is for, a one-pole release lets it go, and the signal is delayed by the look-ahead so
    that the gain arrives in time.  A final safety clip at the ceiling catches what the smoothing lets through."""
    x = np.asarray(y, float)
    st = x if x.ndim == 2 else x[:, None]
    up = np.max(np.abs(resample_poly(st, oversample, 1, axis=0)), axis=1)
    pk = np.max(up.reshape(-1, oversample), axis=1)[: len(st)] if len(up) >= oversample * len(st) else np.max(np.abs(st), axis=1)
    c = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, c / np.maximum(pk, 1e-12))
    L = 2 * max(1, int(lookahead_ms * 1e-3 * sr / 2))          # even, so the window [n, n + L] is exact
    from scipy.ndimage import minimum_filter1d
    mins = minimum_filter1d(np.r_[need, np.ones(L)], size=L + 1, origin=-(L // 2))[: len(need)]   # min over [n, n + L]
    ramp = np.convolve(np.r_[np.ones(L - 1), mins], np.ones(L) / L, mode="valid")              # glides down in time
    g = np.minimum(mins, ramp)
    ar = math.exp(-1 / (release_ms * 1e-3 * sr))
    gain = np.empty(len(g))
    e = 1.0
    for i, v in enumerate(g):
        e = v if v < e else ar * e + (1 - ar) * v
        gain[i] = e
    ylim = np.clip(st * gain[:, None], -c, c)
    return {"y": ylim if x.ndim == 2 else ylim[:, 0], "gain_db": 20 * np.log10(gain + 1e-12), "latency": L}


def clipper(y, ceiling_db: float = -1.0) -> np.ndarray:
    c = 10 ** (ceiling_db / 20)
    return np.clip(np.asarray(y, float), -c, c)


# --------------------------------------------------------------------------------------------- the chain
def tilt(y, db: float = 1.0, sr: int = SR) -> np.ndarray:
    """A gentle tilt: a low shelf at 120 Hz by +db/2 and a high shelf at 8 kHz by +db."""
    x = np.asarray(y, float)
    b1, a1 = E.biquad("lowshelf", 120.0, sr, 0.7, db / 2)
    b2, a2 = E.biquad("highshelf", 8000.0, sr, 0.7, db)
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)


def glue(y, sr: int = SR, threshold: float = -18.0, ratio: float = 2.0) -> np.ndarray:
    x = np.asarray(y, float)
    det = np.max(np.abs(x), axis=1) if x.ndim == 2 else np.abs(x)
    r = D.compressor(det, sr, threshold=threshold, ratio=ratio, attack_ms=20.0, release_ms=200.0)
    g = np.where(det > 1e-9, r["y"] / np.maximum(det, 1e-12), 1.0)
    return x * (g[:, None] if x.ndim == 2 else g)


def master(y, target_lufs: float, ceiling_db: float = -1.0, sr: int = SR, eq_db: float = 1.0, iters: int = 16) -> dict:
    """Tilt, glue, then push into the limiter until the result reaches ``target_lufs`` (the gain found by a few secant
    steps).  Returns the master and how hard it was pushed."""
    pre = glue(tilt(y, eq_db, sr), sr)
    g0 = target_lufs - lufs(pre, sr)
    g = g0
    for _ in range(iters):
        out = limiter(pre * 10 ** (g / 20), ceiling_db, sr=sr)["y"]
        err = target_lufs - lufs(out, sr)
        if abs(err) < 0.05:
            break
        g += err
    lim = limiter(pre * 10 ** (g / 20), ceiling_db, sr=sr)
    return {"y": lim["y"], "drive_db": g, "gain_db": lim["gain_db"], "lufs": lufs(lim["y"], sr), "true_peak": true_peak_db(lim["y"], sr)}


def normalize(y, target_lufs: float = -14.0, sr: int = SR, allow_up: bool = False) -> dict:
    """A streaming service's playback gain: down to its target; up only if ``allow_up`` (and then only as far as the
    true peak allows, -1 dBTP)."""
    L = lufs(y, sr)
    g = target_lufs - L
    if g > 0:
        g = min(g, -1.0 - true_peak_db(y, sr)) if allow_up else 0.0
    return {"y": np.asarray(y, float) * 10 ** (g / 20), "gain_db": g, "lufs_in": L}


def plr(y, sr: int = SR) -> float:
    """The peak-to-loudness ratio: true peak minus integrated loudness (Tech 3342's companion number)."""
    return true_peak_db(y, sr) - lufs(y, sr)


# --------------------------------------------------------------------------------------------- word length
def quantize(y, bits: int) -> np.ndarray:
    q = 2.0 ** (1 - bits)
    return np.round(np.asarray(y, float) / q) * q


def tpdf_dither(y, bits: int, rng=None) -> np.ndarray:
    """Triangular dither of two LSBs peak to peak, then rounding: the error becomes a steady, signal-independent hiss."""
    rng = rng or np.random.default_rng(0)
    q = 2.0 ** (1 - bits)
    d = (rng.random(np.shape(y)) - rng.random(np.shape(y))) * q
    return quantize(np.asarray(y, float) + d, bits)


def shaped(y, bits: int, rng=None, coeffs=(1.623, -0.982, 0.109)) -> np.ndarray:
    """Dither with error feedback: the rounding error, filtered, is subtracted from the next samples, pushing the
    noise towards the top of the band where the ear is least sensitive (a simple three-tap shaper)."""
    rng = rng or np.random.default_rng(0)
    x = np.asarray(y, float)
    q = 2.0 ** (1 - bits)
    out = np.empty_like(x)
    e = [0.0, 0.0, 0.0]
    for i, v in enumerate(x):
        w = v - (coeffs[0] * e[0] + coeffs[1] * e[1] + coeffs[2] * e[2])
        d = (rng.random() - rng.random()) * q
        o = round((w + d) / q) * q
        out[i] = o
        e = [o - w, e[0], e[1]]
    return out


# --------------------------------------------------------------------------------------------- vinyl
T1, T2, T3 = 3180e-6, 318e-6, 75e-6     # the RIAA time constants


def riaa_db(f) -> np.ndarray:
    """The RIAA playback (de-emphasis) curve, 0 dB at 1 kHz: poles at 50 Hz and 2122 Hz, a zero at 500 Hz.  Cutting
    uses its inverse."""
    f = np.asarray(f, float)

    def h(ff):
        s = 2j * np.pi * ff
        return (1 + s * T2) / ((1 + s * T1) * (1 + s * T3))
    return 20 * np.log10(np.abs(h(f)) / np.abs(h(1000.0)))


def riaa_filters(sr: int = SR):
    """Digital playback and cutting filters by the bilinear transform (the pre-warp is ignored; fine at 48 kHz below 10
    kHz)."""
    from scipy.signal import bilinear
    b, a = bilinear([T2, 1.0], np.polymul([T1, 1.0], [T3, 1.0]), sr)
    return (b, a), (a, b)


def groove_excursion_um(f, velocity_cm_s: float = 5.0) -> np.ndarray:
    """A lateral groove's peak excursion (micrometres) at frequency ``f`` for a given peak velocity: v / (2 pi f)."""
    return 1e4 * velocity_cm_s / (2 * np.pi * np.asarray(f, float))
