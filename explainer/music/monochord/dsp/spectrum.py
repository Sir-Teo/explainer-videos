"""Spectra and what can be read off them.

* :func:`spectrum_db`: one windowed, zero-padded FFT, in decibels;
* :func:`partials`: the frequency and level of each partial near ``n * f0``, to a fraction of a bin;
* :func:`f0_autocorr`: the period of a signal from its autocorrelation;
* :func:`stft_db`: the short-time transform a spectrogram draws.

Checked against closed forms in ``tests/music/test_spectrum.py`` (a sinusoid of known frequency and level).
"""

from __future__ import annotations

import numpy as np


def _hann(n: int) -> np.ndarray:
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / n)


def spectrum_db(y: np.ndarray, sr: float, pad: int = 4) -> tuple[np.ndarray, np.ndarray]:
    """Hann-windowed magnitude spectrum: ``(frequencies, level in dB)`` where a sinusoid of amplitude 1 reads 0 dB
    at its peak."""
    y = np.asarray(y, dtype=np.float64)
    n = len(y)
    w = _hann(n)
    nfft = int(2 ** np.ceil(np.log2(n * pad)))
    mag = np.abs(np.fft.rfft(y * w, nfft)) / (w.sum() / 2)
    return np.fft.rfftfreq(nfft, 1 / sr), 20 * np.log10(np.maximum(mag, 1e-12))


def _parabolic(mag_db: np.ndarray, k: int) -> tuple[float, float]:
    """Refine a peak at bin k of a dB spectrum by a parabola through it and its neighbours: (offset, height)."""
    a, b, c = mag_db[k - 1], mag_db[k], mag_db[k + 1]
    d = a - 2 * b + c
    off = 0.0 if d == 0 else 0.5 * (a - c) / d
    return off, b - 0.25 * (a - c) * off


def partials(y: np.ndarray, sr: float, f0: float, count: int = 12, search: float = 0.35, pad: int = 8,
             centers=None) -> list[dict]:
    """The strongest spectral peak within ``search * f0`` of each multiple of ``f0`` (or of each frequency in
    ``centers``, for a string whose partials are not harmonic): ``[{"n", "hz", "db"}]``.  A partial that is absent
    comes back at the level of the floor there."""
    freqs, db = spectrum_db(y, sr, pad)
    df = freqs[1]
    centers = [n * f0 for n in range(1, count + 1)] if centers is None else list(centers)[:count]
    out = []
    for n, fc in enumerate(centers, 1):
        lo = max(1, int((fc - search * f0) / df))
        hi = min(len(db) - 2, int((fc + search * f0) / df))
        if hi <= lo:
            break
        k = lo + int(np.argmax(db[lo:hi + 1]))
        k = min(max(k, 1), len(db) - 2)
        off, height = _parabolic(db, k)
        out.append({"n": n, "hz": float((k + off) * df), "db": float(height)})
    return out


def f0_autocorr(y: np.ndarray, sr: float, fmin: float = 40.0, fmax: float = 2000.0, up: int = 8) -> float:
    """Fundamental frequency from the autocorrelation: the first lag between those of ``fmax`` and ``fmin`` at which
    the signal lines up with itself again.  It knows nothing about strings: it only asks after how long the signal
    repeats.  The autocorrelation is evaluated ``up`` times finer than the sampling (band-limited interpolation) and
    the peak refined by a parabola, so the answer is good to a small fraction of a cent."""
    y = np.asarray(y, dtype=np.float64)
    y = y - y.mean()
    n = len(y)
    nfft = int(2 ** np.ceil(np.log2(2 * n)))
    spec = np.fft.rfft(y, nfft)
    ac = np.fft.irfft(spec * np.conj(spec), up * nfft)[: up * n] * up
    lag = np.arange(up * n) / up
    ac = ac / np.maximum(n - lag, 1.0)  # unbiased: each lag averaged over the samples that overlap
    lo, hi = max(1, int(up * sr / fmax)), min(int(up * sr / fmin), up * n - 2)
    seg = ac[lo:hi + 1]
    # a periodic signal repeats after one period, and after two, and three: take the first lag that is a local
    # maximum nearly as high as the highest
    top = seg.max()
    peaks = np.flatnonzero((seg[1:-1] >= seg[:-2]) & (seg[1:-1] > seg[2:]) & (seg[1:-1] >= 0.9 * top)) + 1
    k = lo + (int(peaks[0]) if peaks.size else int(np.argmax(seg)))
    k = min(max(k, 1), up * n - 2)
    a, b, c = ac[k - 1], ac[k], ac[k + 1]
    d = a - 2 * b + c
    off = 0.0 if d == 0 else 0.5 * (a - c) / d
    return float(up * sr / (k + off))


def stft_db(y: np.ndarray, sr: float, n_fft: int = 2048, hop: int = 256, floor_db: float = -90.0):
    """Short-time Fourier transform magnitudes in dB (a unit sinusoid peaks at 0 dB):
    ``(times, frequencies, S)`` with ``S`` of shape ``(frequencies, times)``."""
    y = np.asarray(y, dtype=np.float64)
    w = _hann(n_fft)
    pad = n_fft // 2
    yp = np.concatenate([np.zeros(pad), y, np.zeros(pad)])
    frames = 1 + (len(yp) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(frames)[:, None]
    S = np.abs(np.fft.rfft(yp[idx] * w, axis=1)).T / (w.sum() / 2)
    return (np.arange(frames) * hop / sr, np.fft.rfftfreq(n_fft, 1 / sr),
            np.maximum(20 * np.log10(np.maximum(S, 1e-12)), floor_db))
