"""Psyche's other senses: hearing, touch, pain and smell (Part 15 of *Psychology, Built*).

Sound in the units of physics (decibels re 20 µPa); the cochlea as a bank of gammatone filters spaced on the ERB
scale and placed along the membrane by Greenwood's function; pitch by summary autocorrelation, which hears the
missing fundamental; masking by the power-spectrum model; the interaural time difference of a spherical head and a
Jeffress array of coincidence detectors; categorical identification and the discrimination predicted from labels;
the McGurk effect as cue combination over places of articulation; Melzack and Wall's gate as a small circuit; and a
model nose for testing how many odours an estimator says can be told apart.

Everything here is a model with its parameters chosen, not fitted to a person; Part 15's scenes say which numbers are
published and which are Psyche's.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import signal as _sig
from scipy.special import comb as _comb

P_REF = 20e-6  # pascals: 0 dB SPL
C_AIR = 343.0  # m/s


# ============================================================================================== sound and level
def db_spl(pressure_pa) -> np.ndarray:
    """Sound pressure level of an RMS pressure, in dB re 20 µPa."""
    return 20 * np.log10(np.asarray(pressure_pa, float) / P_REF)


def pressure(db) -> np.ndarray:
    return P_REF * 10 ** (np.asarray(db, float) / 20)


def threshold_in_quiet(f) -> np.ndarray:
    """Terhardt's (1979) approximation to the absolute threshold of hearing, in dB SPL, as used in perceptual audio
    coders: 3.64 (f/kHz)^-0.8 − 6.5 exp(−0.6 (f/kHz − 3.3)²) + 10⁻³ (f/kHz)⁴."""
    k = np.asarray(f, float) / 1000
    return 3.64 * k ** -0.8 - 6.5 * np.exp(-0.6 * (k - 3.3) ** 2) + 1e-3 * k ** 4


def tone(f: float, dur: float = 0.25, fs: int = 16000, phase: float = 0.0) -> np.ndarray:
    t = np.arange(int(dur * fs)) / fs
    return np.sin(2 * np.pi * f * t + phase)


def harmonic_complex(f0: float, harmonics, dur: float = 0.25, fs: int = 16000, seed: int | None = None) -> np.ndarray:
    """A sum of equal-amplitude harmonics of ``f0`` (sine phase, or random phases with ``seed``)."""
    rng = np.random.default_rng(seed) if seed is not None else None
    t = np.arange(int(dur * fs)) / fs
    x = np.zeros_like(t)
    for h in harmonics:
        ph = rng.uniform(0, 2 * np.pi) if rng is not None else 0.0
        x += np.sin(2 * np.pi * h * f0 * t + ph)
    return x / max(len(list(harmonics)), 1)


def spectrum(x, fs: int = 16000):
    """One-sided amplitude spectrum: (frequencies, amplitudes)."""
    n = len(x)
    X = np.abs(np.fft.rfft(x * np.hanning(n))) / (n / 4)
    return np.fft.rfftfreq(n, 1 / fs), X


# ============================================================================================== the cochlea
def erb(f) -> np.ndarray:
    """Equivalent rectangular bandwidth of the human auditory filter (Glasberg and Moore 1990), in Hz."""
    return 24.7 * (4.37 * np.asarray(f, float) / 1000 + 1)


def erb_rate(f) -> np.ndarray:
    """Number of ERBs below frequency ``f``."""
    return 21.4 * np.log10(4.37 * np.asarray(f, float) / 1000 + 1)


def erb_space(lo: float, hi: float, n: int) -> np.ndarray:
    """``n`` centre frequencies equally spaced on the ERB-rate scale."""
    e = np.linspace(erb_rate(lo), erb_rate(hi), n)
    return (10 ** (e / 21.4) - 1) * 1000 / 4.37


def greenwood(x) -> np.ndarray:
    """Greenwood's (1990) place-frequency map for the human cochlea: ``x`` is the distance from the apex as a fraction
    of the membrane's length (0 apex, 1 base); returns the best frequency in Hz."""
    return 165.4 * (10 ** (2.1 * np.asarray(x, float)) - 0.88)


def greenwood_place(f) -> np.ndarray:
    """Inverse of :func:`greenwood`: fraction of the length from the apex for frequency ``f``."""
    return np.log10(np.asarray(f, float) / 165.4 + 0.88) / 2.1


def gammatone_ir(fc: float, fs: int = 16000, dur: float = 0.05, order: int = 4) -> np.ndarray:
    """Impulse response of a gammatone filter at ``fc`` with bandwidth 1.019 ERB, normalised to unit peak gain."""
    t = np.arange(int(dur * fs)) / fs
    b = 1.019 * erb(fc)
    g = t ** (order - 1) * np.exp(-2 * np.pi * b * t) * np.cos(2 * np.pi * fc * t)
    H = np.abs(np.fft.rfft(g, 8192)).max()
    return g / H


def filterbank(x, cfs, fs: int = 16000) -> np.ndarray:
    """Pass ``x`` through gammatone filters at ``cfs``: (channels, samples)."""
    return np.array([_sig.fftconvolve(x, gammatone_ir(fc, fs), mode="full")[: len(x)] for fc in cfs])


def hair_cells(bm, compress: float = 0.3) -> np.ndarray:
    """Inner hair cells as half-wave rectification with power-law compression: a crude neural activity pattern."""
    return np.maximum(bm, 0) ** compress


def excitation(x, cfs, fs: int = 16000) -> np.ndarray:
    """RMS output of each channel: the excitation pattern along the membrane."""
    return np.sqrt((filterbank(x, cfs, fs) ** 2).mean(axis=1))


def travelling_wave(f: float, x, t, speed_scale: float = 1.0):
    """A schematic travelling wave on the basilar membrane for a tone of frequency ``f``: displacement at places ``x``
    (0 apex, 1 base) and time ``t``; its envelope peaks at Greenwood's place for ``f`` and dies just beyond it."""
    x = np.asarray(x, float)
    xp = greenwood_place(f)
    d = 1 - x  # distance from the base
    dp = 1 - xp
    env = np.where(d <= dp, np.exp(-((d - dp) / (0.35 * dp + 0.05)) ** 2), np.exp(-((d - dp) / 0.03) ** 2))
    # phase accumulates as the wave slows toward its place
    k = 40.0 * speed_scale
    phase = k * np.log1p(d / (dp + 1e-3) * 4)
    return env * np.cos(2 * np.pi * f * t - phase)


# ============================================================================================== pitch
def summary_autocorrelation(x, fs: int = 16000, cfs=None, max_lag: float = 0.02):
    """Summary autocorrelation (Licklider 1951; Meddis and Hewitt 1991): autocorrelate each channel's hair-cell output
    and sum.  Returns (lags in seconds, summary)."""
    cfs = erb_space(100, 4000, 40) if cfs is None else cfs
    hc = hair_cells(filterbank(x, cfs, fs))
    L = int(max_lag * fs)
    s = np.zeros(L)
    for ch in hc:
        ch = ch - ch.mean()
        r = _sig.fftconvolve(ch, ch[::-1], mode="full")[len(ch) - 1: len(ch) - 1 + L]
        s += r / (r[0] + 1e-12)
    return np.arange(L) / fs, s / len(cfs)


def pitch(x, fs: int = 16000, lo: float = 60.0, hi: float = 500.0, cfs=None) -> float:
    """The pitch the summary autocorrelation hears: the lag of its highest peak between 1/hi and 1/lo seconds."""
    lags, s = summary_autocorrelation(x, fs, cfs, max_lag=1.2 / lo)
    ok = np.flatnonzero((lags >= 1 / hi) & (lags <= 1 / lo))
    seg = s[ok]
    peaks = [k for k in range(1, len(seg) - 1) if seg[k] >= seg[k - 1] and seg[k] >= seg[k + 1]]
    if not peaks:
        return 1.0 / lags[ok[np.argmax(seg)]]
    top = max(seg[k] for k in peaks)
    k = min(k for k in peaks if seg[k] >= 0.9 * top)  # the shortest lag near the top: no octave errors downward
    return 1.0 / lags[ok[k]]


# ============================================================================================== masking
def masked_threshold(signal_f: float, noise_bandwidth: float, noise_level_per_hz: float = 0.0, k_db: float = -4.0):
    """Fletcher's band-widening experiment under the power-spectrum model: the threshold (dB) of a tone at
    ``signal_f`` in a noise band of that width centred on it, with spectrum level ``noise_level_per_hz`` dB/Hz.  Only
    the noise inside one auditory filter (one ERB wide) masks; ``k_db`` is the signal-to-noise ratio at threshold."""
    inside = min(noise_bandwidth, float(erb(signal_f)))
    return noise_level_per_hz + 10 * math.log10(inside) + k_db


# ============================================================================================== where is it?
def itd(azimuth_deg, head_radius: float = 0.0875, c: float = C_AIR) -> np.ndarray:
    """Woodworth's interaural time difference for a spherical head, in seconds: (r/c)(θ + sin θ)."""
    th = np.radians(np.asarray(azimuth_deg, float))
    return head_radius / c * (th + np.sin(th))


def azimuth_from_itd(delay: float, head_radius: float = 0.0875, c: float = C_AIR) -> float:
    """Invert :func:`itd` by bisection (degrees, -90 to 90)."""
    lo, hi = -90.0, 90.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if itd(mid, head_radius, c) < delay:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def phase_locked_spikes(f: float, delay: float, dur: float, rng, rate: float = 0.3, jitter: float = 5e-5):
    """Spike times of a fibre phase-locked to a tone of frequency ``f`` arriving with ``delay``: on each cycle it fires
    with probability ``rate`` near the peak, with Gaussian jitter."""
    n = int(dur * f)
    fire = rng.random(n) < rate
    t = (np.arange(n) + 0.25) / f + delay
    return np.sort(t[fire] + rng.normal(0, jitter, fire.sum()))


def jeffress(left, right, delays, window: float = 3e-5) -> np.ndarray:
    """A Jeffress (1948) array: detector ``k`` delays the left input by ``delays[k]`` and counts left-right spike pairs
    that arrive within ``window`` of each other.  Its most active detector reads out the interaural delay."""
    right = np.asarray(right)
    out = []
    for d in delays:
        shifted = np.asarray(left) + d
        j = np.searchsorted(right, shifted)
        near = np.zeros(len(shifted), bool)
        for jj in (j - 1, j):
            ok = (jj >= 0) & (jj < len(right))
            near[ok] |= np.abs(right[jj[ok]] - shifted[ok]) < window
        out.append(int(near.sum()))
    return np.array(out)


# ============================================================================================== speech
def identification(continuum, boundary: float, slope: float) -> np.ndarray:
    """The probability of labelling each step of a continuum as the second category (a logistic)."""
    return 1 / (1 + np.exp(-(np.asarray(continuum, float) - boundary) / slope))


def abx_from_labels(p_a, p_b) -> np.ndarray:
    """Haskins prediction: ABX discrimination when listeners can compare only covert labels,
    P(correct) = ½[1 + (p_a − p_b)²]."""
    p_a, p_b = np.asarray(p_a, float), np.asarray(p_b, float)
    return 0.5 * (1 + (p_a - p_b) ** 2)


PLACES = ("b", "d", "g")  # places of articulation, front to back: lips, ridge, velum


def mcgurk(audio_place: float = 0.0, visual_place: float = 2.0, sd_audio: float = 1.0, sd_visual: float = 0.6,
           n: int = 4000, rng=None):
    """Audio-visual speech as cue combination on a one-dimensional place axis (b = 0, d = 1, g = 2).  Each trial draws
    a noisy auditory and visual estimate, combines them by reliability (Part 14's rule) and labels the nearest place.
    Returns the share of b, d and g responses."""
    rng = np.random.default_rng(0) if rng is None else rng
    a = audio_place + rng.normal(0, sd_audio, n)
    v = visual_place + rng.normal(0, sd_visual, n)
    w = (1 / sd_audio ** 2) / (1 / sd_audio ** 2 + 1 / sd_visual ** 2)
    c = w * a + (1 - w) * v
    lab = np.clip(np.rint(c), 0, 2).astype(int)
    return np.bincount(lab, minlength=3) / n


# ============================================================================================== touch and pain
def gate(large, small, w_large: float = 0.3, w_small: float = 1.0, w_gate: float = 3.0, k: float = 0.5):
    """Melzack and Wall's gate (1965) as a small circuit.  Large (touch) and small (injury) fibres both drive the
    transmission cell T; large fibres also excite an inhibitory interneuron in the substantia gelatinosa, which shuts
    the gate on T's inputs, and small fibres inhibit that interneuron:
    SG = relu(L − k·S), T = (w_large·L + w_small·S) / (1 + w_gate·SG)."""
    L, S = np.asarray(large, float), np.asarray(small, float)
    sg = np.maximum(L - k * S, 0)
    return (w_large * L + w_small * S) / (1 + w_gate * sg)


def two_point_threshold(receptive_field_mm: float, density_per_mm: float) -> float:
    """A crude two-point threshold: two points are felt as two when they lie in different receptive fields with an
    unexcited field between, roughly the larger of one field and two receptor spacings."""
    return max(receptive_field_mm, 2.0 / density_per_mm)


# ============================================================================================== smell
def nose(n_odorants: int = 128, dims: int = 10, seed: int = 0) -> np.ndarray:
    """A model nose: each of ``n_odorants`` molecules drives ``dims`` perceptual dimensions (non-negative); a mixture's
    percept is the normalised sum of its components.  Returns the (n_odorants, dims) loading matrix."""
    rng = np.random.default_rng(seed)
    return rng.gamma(0.6, 1.0, (n_odorants, dims))


def mixture_percept(M: np.ndarray, members) -> np.ndarray:
    v = M[np.asarray(members)].sum(axis=0)
    return v / np.linalg.norm(v)


def triangle_test(M, a, b, noise: float, rng, n: int = 20) -> float:
    """Share correct in ``n`` triangle tests between mixtures ``a`` and ``b``: two of one, one of the other, each
    percept with Gaussian noise; the odd one out is the one farthest from the other two's mean."""
    pa, pb = mixture_percept(M, a), mixture_percept(M, b)
    right = 0
    for _ in range(n):
        x = [pa + rng.normal(0, noise, pa.shape), pa + rng.normal(0, noise, pa.shape), pb + rng.normal(0, noise, pb.shape)]
        d = [np.linalg.norm(x[i] - (x[(i + 1) % 3] + x[(i + 2) % 3]) / 2) for i in range(3)]
        right += int(np.argmax(d) == 2)
    return right / n


def bushdid_estimate(n_total: int, n_components: int, overlap_threshold: float) -> float:
    """Bushdid et al.'s (2014) count: if mixtures of ``n_components`` (out of ``n_total``) can be told apart whenever
    they share less than ``overlap_threshold`` of their components, the number of discriminable mixtures is the number
    of mixtures divided by the size of one indiscriminable neighbourhood (mixtures sharing at least that many)."""
    N, K = n_total, n_components
    m = int(math.ceil(overlap_threshold * K))
    ball = sum(_comb(K, j, exact=True) * _comb(N - K, K - j, exact=True) for j in range(m, K + 1))
    return _comb(N, K, exact=True) / ball
