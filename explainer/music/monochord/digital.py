"""Monochord's converters (Part 48 of *Music, Built*): sampling, reconstruction, quantization, dither, noise shaping,
one-bit conversion, jitter and resampling, computed rather than assumed.

    alias(f, fs)                          the frequency a tone at f appears at when sampled at fs
    sinc_interp(x, fs, t, taps)           Whittaker-Shannon reconstruction from samples (truncated, Hann-windowed)
    zero_order_hold(x, up)                the 'stair-step': each sample held for ``up`` output samples
    resample(x, sr_in, sr_out, ...)       band-limited resampling by windowed-sinc interpolation (with or without the
                                          anti-aliasing low-pass), and naive sample dropping
    quantize(x, bits, dither, rng)        a mid-tread quantizer on [-1, 1) with no dither, rectangular (RPDF) or triangular
                                          (TPDF) dither
    error_moments(bits, dither)           the mean and variance of the quantization error as functions of the input
                                          (Lipshitz, Wannamaker and Vanderkooy 1992)
    shaped(x, bits, order, rng)           error-feedback noise shaping, noise transfer function (1 - z^-1)^order
    delta_sigma(x, order)                 a one-bit delta-sigma modulator, first or second order
    decimate(bits, osr)                   an exact low-pass, then keep every osr-th sample
    snr_db(ref, y), band_snr_db(...)      signal-to-error ratios, broadband and in a band
    jitter_sample(f, fs, sigma, n, rng)   a sine sampled at instants with random timing error

No manim here.  Checked in ``tests/music/test_digital.py``.
"""

from __future__ import annotations

import math

import numpy as np

# --------------------------------------------------------------------------------------------- sampling


def alias(f: float, fs: float) -> float:
    """Fold f into [0, fs/2]: the frequency of the samples of a sine at f."""
    r = f % fs
    return float(min(r, fs - r))


def sinc_interp(x, fs: float, t, taps: int | None = None) -> np.ndarray:
    """sum_n x[n] sinc(fs t - n): exact for a signal band-limited below fs/2 if every sample is used.  With ``taps``,
    only the samples within taps/2 of each instant are used, weighted by a Hann window (as a real filter must)."""
    x = np.asarray(x, float)
    t = np.atleast_1d(np.asarray(t, float))
    u = t * fs
    out = np.zeros(len(t))
    if taps is None:
        n = np.arange(len(x))
        for i, ui in enumerate(u):
            out[i] = np.dot(x, np.sinc(ui - n))
        return out
    h = taps / 2.0
    for i, ui in enumerate(u):
        lo, hi = max(int(np.floor(ui - h)) + 1, 0), min(int(np.ceil(ui + h)), len(x))
        n = np.arange(lo, hi)
        d = ui - n
        w = 0.5 + 0.5 * np.cos(np.pi * d / h)
        out[i] = np.dot(x[lo:hi], np.sinc(d) * w)
    return out


def zero_order_hold(x, up: int) -> np.ndarray:
    return np.repeat(np.asarray(x, float), up)


def lowpass_taps(cutoff: float, fs: float, n: int = 255, beta: float = 8.6) -> np.ndarray:
    """A Kaiser-windowed sinc low-pass, ``cutoff`` in Hz at rate fs (unity gain at DC)."""
    m = np.arange(n) - (n - 1) / 2
    h = 2 * cutoff / fs * np.sinc(2 * cutoff / fs * m) * np.kaiser(n, beta)
    return h / h.sum()


def resample(x, sr_in: float, sr_out: float, filtered: bool = True, taps: int = 64) -> np.ndarray:
    """Evaluate the band-limited interpolation of ``x`` at the new rate.  When going down, ``filtered`` first narrows
    the interpolating sinc to the new Nyquist frequency (the anti-aliasing low-pass); unfiltered, it does not."""
    x = np.asarray(x, float)
    n_out = int(len(x) * sr_out / sr_in)
    t = np.arange(n_out) / sr_out
    scale = min(1.0, sr_out / sr_in) if filtered else 1.0
    u = t * sr_in
    out = np.zeros(n_out)
    h = taps / 2.0 / scale
    for i, ui in enumerate(u):
        lo, hi = max(int(np.floor(ui - h)) + 1, 0), min(int(np.ceil(ui + h)), len(x))
        n = np.arange(lo, hi)
        d = ui - n
        w = 0.5 + 0.5 * np.cos(np.pi * d / h)
        out[i] = scale * np.dot(x[lo:hi], np.sinc(scale * d) * w)
    return out


def drop_samples(x, step: int) -> np.ndarray:
    """Naive decimation: keep every ``step``-th sample, with no filter."""
    return np.asarray(x, float)[::step]


# --------------------------------------------------------------------------------------------- quantization


def lsb(bits: int) -> float:
    return 2.0 / 2 ** bits


def dither_noise(n: int, bits: int, kind: str, rng) -> np.ndarray:
    d = lsb(bits)
    if kind == "none":
        return np.zeros(n)
    if kind == "rpdf":
        return rng.uniform(-d / 2, d / 2, n)
    if kind == "tpdf":
        return rng.uniform(-d / 2, d / 2, n) + rng.uniform(-d / 2, d / 2, n)
    raise ValueError(kind)


def quantize(x, bits: int, dither: str = "none", rng=None) -> np.ndarray:
    """Round to the nearest of 2^bits levels spaced one LSB apart (zero is a level), after adding dither; clip to the
    range a ``bits``-bit word can hold."""
    rng = rng or np.random.default_rng(0)
    x = np.asarray(x, float)
    d = lsb(bits)
    v = x + dither_noise(len(x), bits, dither, rng)
    q = d * np.round(v / d)
    return np.clip(q, -1.0, 1.0 - d)


def error_moments(bits: int, dither: str, points: int = 101, draws: int = 4000, seed: int = 0) -> dict:
    """The quantization error's mean and variance (in LSB and LSB^2) for inputs spread over one LSB, estimated by
    averaging over dither draws."""
    rng = np.random.default_rng(seed)
    d = lsb(bits)
    xs = np.linspace(-0.5, 0.5, points) * d
    mean, var = [], []
    for x in xs:
        e = (quantize(np.full(draws, x), bits, dither, rng) - x) / d
        mean.append(float(e.mean()))
        var.append(float(e.var()))
    return {"x": (xs / d).tolist(), "mean": mean, "var": var}


def snr_db(ref, y) -> float:
    ref, y = np.asarray(ref, float), np.asarray(y, float)
    return float(10 * np.log10(np.sum(ref ** 2) / max(np.sum((y - ref) ** 2), 1e-300)))


def theory_snr(bits: int) -> float:
    """A full-scale sine against uniform error of variance LSB^2/12: 6.02 N + 1.76 dB."""
    return 6.0206 * bits + 1.7609


def shaped(x, bits: int, order: int = 1, dither: str = "tpdf", rng=None) -> np.ndarray:
    """Error-feedback quantization: the error is fed back so that it reaches the output filtered by (1 - z^-1)^order,
    pushing its power toward high frequencies."""
    rng = rng or np.random.default_rng(0)
    x = np.asarray(x, float)
    d = lsb(bits)
    coeffs = {0: [], 1: [1.0], 2: [2.0, -1.0], 3: [3.0, -3.0, 1.0]}[order]
    past = [0.0] * len(coeffs)
    dn = dither_noise(len(x), bits, dither, rng)
    out = np.empty(len(x))
    for n in range(len(x)):
        u = x[n] - sum(c * e for c, e in zip(coeffs, past))
        q = min(max(d * round((u + dn[n]) / d), -1.0), 1.0 - d)
        e = q - u
        if past:
            past = [e] + past[:-1]
        out[n] = q
    return out


# --------------------------------------------------------------------------------------------- one bit


def delta_sigma(x, order: int = 2) -> np.ndarray:
    """A one-bit modulator: integrate the difference between the input and the last output bit, and output the sign.
    Second order: two integrators in a row.  Inputs should stay within about +/- 0.5 for the second order to be stable."""
    x = np.asarray(x, float)
    y = np.empty(len(x))
    s1 = s2 = 0.0
    prev = 0.0
    for n in range(len(x)):
        if order == 1:
            s1 += x[n] - prev
            prev = 1.0 if s1 >= 0 else -1.0
        else:
            s1 += x[n] - prev
            s2 += s1 - prev
            prev = 1.0 if s2 >= 0 else -1.0
        y[n] = prev
    return y


def decimate(y, osr: int, edge: float = 0.45, taper: float = 0.05) -> np.ndarray:
    """Low-pass the bitstream and keep every osr-th sample.  The low-pass is done exactly, in the frequency domain:
    pass everything below ``edge`` of the output rate, roll off with a raised cosine over ``taper``, stop the rest."""
    y = np.asarray(y, float)
    Y = np.fft.rfft(y)
    f = np.fft.rfftfreq(len(y), 1.0) * osr                      # in units of the output rate
    g = np.clip((edge + taper - f) / taper, 0.0, 1.0)
    g = 0.5 - 0.5 * np.cos(np.pi * g)
    return np.fft.irfft(Y * g, len(y))[::osr]


def blackman_harris(n: int) -> np.ndarray:
    k = 2 * np.pi * np.arange(n) / (n - 1)
    return 0.35875 - 0.48829 * np.cos(k) + 0.14128 * np.cos(2 * k) - 0.01168 * np.cos(3 * k)


def band_snr_db(y, ref_hz: float, sr: float, band: float, skip: int = 5) -> float:
    """In-band SNR of a recorded sine: the power in the bins at the sine against every other bin below ``band`` Hz
    (Blackman-Harris window; ``skip`` bins either side counted as the tone)."""
    y = np.asarray(y, float)
    n = len(y)
    w = blackman_harris(n)
    Y = np.abs(np.fft.rfft(y * w)) ** 2
    f = np.fft.rfftfreq(n, 1 / sr)
    k = int(round(ref_hz * n / sr))
    tone = Y[max(k - skip, 0):k + skip + 1].sum()
    inband = (f > 10) & (f <= band)
    inband[max(k - skip, 0):k + skip + 1] = False
    return float(10 * np.log10(tone / max(Y[inband].sum(), 1e-300)))


def noise_spectrum(e, sr: float, n: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    """Welch's averaged periodogram of an error signal, in dB per bin (Hann window)."""
    e = np.asarray(e, float)
    w = np.hanning(n)
    segs = [e[i:i + n] * w for i in range(0, len(e) - n + 1, n // 2)]
    P = np.mean([np.abs(np.fft.rfft(s)) ** 2 for s in segs], axis=0) / np.sum(w ** 2)
    return np.fft.rfftfreq(n, 1 / sr), 10 * np.log10(P + 1e-30)


# --------------------------------------------------------------------------------------------- jitter


def jitter_sample(f: float, fs: float, sigma: float, n: int, rng=None, amp: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """n samples of a sine at f, taken at nT + e with e ~ N(0, sigma^2): returns (ideal samples, jittered samples)."""
    rng = rng or np.random.default_rng(0)
    t = np.arange(n) / fs
    return amp * np.sin(2 * np.pi * f * t), amp * np.sin(2 * np.pi * f * (t + sigma * rng.standard_normal(n)))


def jitter_snr_theory(f: float, sigma: float) -> float:
    """-20 log10(2 pi f sigma): the error of a sine's slope times the timing error."""
    return float(-20 * np.log10(2 * np.pi * f * sigma))
