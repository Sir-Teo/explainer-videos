"""Taking a sound apart (Part 3, *The Spectrum*): the transforms, written out, each checked against a reference
that does not share its code (``tests/music/test_fourier.py``; the references are numpy and ``scipy.signal``).

* :func:`dft` is the definition, an N-by-N sum; :func:`fft` is Cooley and Tukey's radix-2 algorithm, written out;
* :func:`window` and :func:`leakage` are the window functions and what each costs;
* :func:`stft` slides a window along a sound; :func:`cqt` uses a window whose length shrinks as the frequency rises,
  so that every bin spans the same musical interval;
* :func:`spreads` measures how long and how wide a signal is, for the uncertainty product;
* :func:`colored_noise` makes noise whose power falls as ``1 / f ** beta``;
* :func:`reassigned` moves each cell of a spectrogram to where its energy actually sits (the frontier chapter);
* :func:`additive`, :func:`centroid`, :func:`flux` and :func:`attack_time` build a tone from partials and describe one.
"""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# The transform, twice
# ---------------------------------------------------------------------------
def dft(x) -> np.ndarray:
    """The discrete Fourier transform by its definition: ``X[k] = sum_n x[n] exp(-2 pi i k n / N)``.  N squared
    multiplications; here so that the fast one has something to agree with."""
    x = np.asarray(x, dtype=complex)
    n = len(x)
    k = np.arange(n)
    return np.exp(-2j * np.pi * np.outer(k, k) / n) @ x


def fft(x, count: list | None = None) -> np.ndarray:
    """Cooley and Tukey's algorithm for a length that is a power of two: transform the even and the odd samples
    separately (two problems of half the size), then combine them with N/2 multiplications.  ``count``, if given,
    is a one-element list that is incremented by the number of complex multiplications."""
    x = np.asarray(x, dtype=complex)
    n = len(x)
    if n & (n - 1):
        raise ValueError("this FFT wants a power of two")
    # the bit-reversed order is what the recursion would leave at its bottom
    bits = n.bit_length() - 1
    idx = np.arange(n)
    rev = np.zeros(n, dtype=int)
    for b in range(bits):
        rev |= ((idx >> b) & 1) << (bits - 1 - b)
    a = x[rev].copy()
    size = 2
    while size <= n:
        half = size // 2
        w = np.exp(-2j * np.pi * np.arange(half) / size)
        a = a.reshape(-1, size)
        t = a[:, half:] * w
        if count is not None:
            count[0] += t.size
        a = np.concatenate([a[:, :half] + t, a[:, :half] - t], axis=1).reshape(-1)
        size *= 2
    return a


# ---------------------------------------------------------------------------
# Windows
# ---------------------------------------------------------------------------
def window(name: str, n: int) -> np.ndarray:
    """A window of ``n`` samples: ``rect``, ``hann``, ``hamming``, ``blackman`` or ``gauss`` (periodic forms, as an
    analysis needs)."""
    k = np.arange(n)
    if name == "rect":
        return np.ones(n)
    if name == "hann":
        return 0.5 - 0.5 * np.cos(2 * np.pi * k / n)
    if name == "hamming":
        return 0.54 - 0.46 * np.cos(2 * np.pi * k / n)
    if name == "blackman":
        return 0.42 - 0.5 * np.cos(2 * np.pi * k / n) + 0.08 * np.cos(4 * np.pi * k / n)
    if name == "gauss":
        return np.exp(-0.5 * ((k - n / 2) / (n / 8)) ** 2)
    raise ValueError(name)


def leakage(name: str, n: int = 256, pad: int = 64) -> dict:
    """What a window does to a pure tone: the width of its main lobe (in bins, between the first zeros or minima)
    and the height of its highest side lobe (dB below the peak), from its own transform."""
    w = window(name, n)
    spec = np.abs(np.fft.rfft(w, n * pad))
    db = 20 * np.log10(np.maximum(spec / spec[0], 1e-12))
    i = 1
    while i < len(db) - 1 and db[i + 1] < db[i]:
        i += 1                                        # down the main lobe to its first minimum
    return {"name": name, "main_lobe_bins": 2 * i / pad, "side_lobe_db": float(db[i:].max()),
            "spectrum_db": db[: 12 * pad], "bins": np.arange(12 * pad) / pad}


# ---------------------------------------------------------------------------
# Time and frequency together
# ---------------------------------------------------------------------------
def stft(x, sr: float, n: int = 2048, hop: int = 512, name: str = "hann"):
    """The short-time Fourier transform: the window slides along in steps of ``hop`` and each stretch is
    transformed.  Returns ``(frequencies, times, S)`` with ``S[k, m]`` complex; frame ``m`` is centred on
    ``times[m]`` (the signal is padded by half a window at each end)."""
    x = np.asarray(x, dtype=float)
    w = window(name, n)
    xp = np.concatenate([np.zeros(n // 2), x, np.zeros(n // 2)])
    frames = 1 + (len(xp) - n) // hop
    S = np.empty((n // 2 + 1, frames), dtype=complex)
    for m in range(frames):
        S[:, m] = np.fft.rfft(xp[m * hop: m * hop + n] * w)
    return np.fft.rfftfreq(n, 1 / sr), np.arange(frames) * hop / sr, S


def cqt(x, sr: float, fmin: float = 65.41, bins_per_octave: int = 12, n_bins: int = 60, hop: int = 512,
        name: str = "hann"):
    """A constant-Q transform by its definition (Brown, 1991): bin ``k`` is centred on
    ``fmin * 2 ** (k / bins_per_octave)`` and its window is ``Q`` periods long, with
    ``Q = 1 / (2 ** (1 / bins_per_octave) - 1)``, so a low bin looks at a long stretch of sound and a high bin at a
    short one.  Returns ``(frequencies, times, C)``."""
    x = np.asarray(x, dtype=float)
    q = 1.0 / (2 ** (1.0 / bins_per_octave) - 1.0)
    freqs = fmin * 2 ** (np.arange(n_bins) / bins_per_octave)
    longest = int(math.ceil(q * sr / fmin))
    xp = np.concatenate([np.zeros(longest // 2), x, np.zeros(longest // 2)])
    frames = 1 + len(x) // hop
    C = np.zeros((n_bins, frames), dtype=complex)
    for k, f in enumerate(freqs):
        nk = int(math.ceil(q * sr / f))
        kern = window(name, nk) * np.exp(-2j * np.pi * f * np.arange(nk) / sr) / nk
        start = longest // 2 - nk // 2
        for m in range(frames):
            a = start + m * hop
            seg = xp[a: a + nk]
            if len(seg) == nk:
                C[k, m] = np.dot(seg, kern)
    return freqs, np.arange(frames) * hop / sr, C, q


# ---------------------------------------------------------------------------
# How long, how wide
# ---------------------------------------------------------------------------
def spreads(x, sr: float) -> tuple[float, float]:
    """The duration and the bandwidth of a signal as Gabor defined them: the standard deviations of ``|x(t)|^2`` in
    time and of ``|X(f)|^2`` in frequency (two-sided, about its mean frequency).  Their product is never less
    than ``1 / (4 pi)``."""
    x = np.asarray(x, dtype=complex)
    n = len(x)
    t = np.arange(n) / sr
    p = np.abs(x) ** 2
    p = p / p.sum()
    t0 = float((t * p).sum())
    dt = math.sqrt(float(((t - t0) ** 2 * p).sum()))
    X = np.fft.fftshift(np.fft.fft(x, 8 * n))
    f = np.fft.fftshift(np.fft.fftfreq(8 * n, 1 / sr))
    q = np.abs(X) ** 2
    q = q / q.sum()
    f0 = float((f * q).sum())
    df = math.sqrt(float(((f - f0) ** 2 * q).sum()))
    return dt, df


def tone_burst(hz: float, seconds: float, sr: int = 48_000, shape: str = "gauss") -> np.ndarray:
    """A tone that lasts about ``seconds`` (the standard deviation of a Gaussian envelope times four, or the
    length of a Hann envelope)."""
    n = int(round(6 * seconds * sr)) if shape == "gauss" else int(round(seconds * sr))
    t = (np.arange(n) - n / 2) / sr
    env = np.exp(-0.5 * (t / (seconds / 4)) ** 2) if shape == "gauss" else window("hann", n)
    return env * np.sin(2 * np.pi * hz * t)


# ---------------------------------------------------------------------------
# Noise with a slope
# ---------------------------------------------------------------------------
def colored_noise(n: int, beta: float, sr: int = 48_000, seed: int = 0, fmin: float = 20.0) -> np.ndarray:
    """Noise whose power per hertz falls as ``1 / f ** beta``: 0 is white, 1 pink (equal power in every octave),
    2 brown (a random walk).  Made by shaping the spectrum of white noise; flat below ``fmin``."""
    rng = np.random.default_rng(seed)
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / sr)
    spec *= np.maximum(f, fmin) ** (-beta / 2.0)
    spec[0] = 0.0
    y = np.fft.irfft(spec, n)
    return y / np.abs(y).max()


def octave_slope(y, sr: float, lo: float = 100.0, hi: float = 8000.0) -> float:
    """The slope of a noise's power spectral density, in dB per octave (a line through its octave-band averages)."""
    n = 1 << 13
    hop = n // 2
    w = window("hann", n)
    frames = [np.abs(np.fft.rfft(y[a: a + n] * w)) ** 2 for a in range(0, len(y) - n, hop)]
    psd = np.mean(frames, axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    centres, levels = [], []
    fc = lo
    while fc <= hi:
        band = (f >= fc / math.sqrt(2)) & (f < fc * math.sqrt(2))
        centres.append(math.log2(fc))
        levels.append(10 * math.log10(psd[band].mean()))
        fc *= 2
    return float(np.polyfit(centres, levels, 1)[0])


# ---------------------------------------------------------------------------
# Reassignment
# ---------------------------------------------------------------------------
def reassigned(x, sr: float, n: int = 1024, hop: int = 64, bins: tuple[int, int] | None = None):
    """A reassigned spectrogram (Kodera, Gendrin and de Villedary, 1976; Auger and Flandrin, 1995).  Each cell of
    an ordinary spectrogram is the energy in a patch of time and frequency, credited to the patch's centre.  Two
    more transforms, with the window multiplied by time and with its derivative, say where inside the patch the
    energy really is; it is moved there.  Returns ``(frequencies, times, ordinary, reassigned)`` as energies."""
    x = np.asarray(x, dtype=float)
    w = window("hann", n)
    tw = (np.arange(n) - n / 2) / sr * w
    dw = np.gradient(w) * sr
    xp = np.concatenate([np.zeros(n // 2), x, np.zeros(n // 2)])
    frames = 1 + (len(xp) - n) // hop
    nf = n // 2 + 1
    freqs = np.fft.rfftfreq(n, 1 / sr)
    plain = np.zeros((nf, frames))
    out = np.zeros((nf, frames))
    for m in range(frames):
        seg = xp[m * hop: m * hop + n]
        X, Xt, Xd = np.fft.rfft(seg * w), np.fft.rfft(seg * tw), np.fft.rfft(seg * dw)
        e = np.abs(X) ** 2
        plain[:, m] = e
        ok = e > 1e-10 * e.max() if e.max() > 0 else np.zeros(nf, bool)
        t_hat = m * hop / sr + np.real(Xt[ok] / X[ok])
        f_hat = freqs[ok] - np.imag(Xd[ok] / X[ok]) / (2 * np.pi)
        mi = np.clip(np.round(t_hat * sr / hop).astype(int), 0, frames - 1)
        ki = np.clip(np.round(f_hat / (sr / n)).astype(int), 0, nf - 1)
        np.add.at(out, (ki, mi), e[ok])
    return freqs, np.arange(frames) * hop / sr, plain, out


def cells_for(E: np.ndarray, share: float = 0.9) -> int:
    """How many cells of a picture it takes to hold ``share`` of its energy: the fewer, the sharper the picture."""
    v = np.sort(E.ravel())[::-1]
    return int(np.searchsorted(np.cumsum(v), share * v.sum()) + 1)


# ---------------------------------------------------------------------------
# Building a tone, and describing one
# ---------------------------------------------------------------------------
def additive(f0: float, amps, seconds: float, sr: int = 48_000, phases=None, decays=None, attack: float = 0.005) -> np.ndarray:
    """A tone as a sum of partials: partial ``n`` at ``n * f0`` with amplitude ``amps[n - 1]``, a starting phase and
    (if given) its own rate of decay per second."""
    t = np.arange(int(seconds * sr)) / sr
    y = np.zeros(len(t))
    for i, a in enumerate(amps):
        f = (i + 1) * f0
        if a == 0 or f > 0.45 * sr:
            continue
        ph = 0.0 if phases is None else phases[i]
        env = 1.0 if decays is None else np.exp(-decays[i] * t)
        y += a * env * np.sin(2 * np.pi * f * t + ph)
    return y * np.minimum(1.0, t / attack)


def centroid(y, sr: float) -> float:
    """The spectral centroid: the centre of gravity of the power spectrum, in hertz ("brightness")."""
    spec = np.abs(np.fft.rfft(np.asarray(y, dtype=float) * window("hann", len(y)))) ** 2
    f = np.fft.rfftfreq(len(y), 1 / sr)
    return float((f * spec).sum() / spec.sum())


def flux(y, sr: float, n: int = 1024, hop: int = 256) -> np.ndarray:
    """Spectral flux: how much the (normalized) spectrum changes from one frame to the next, frame by frame."""
    _, _, S = stft(y, sr, n, hop)
    mag = np.abs(S)
    mag = mag / np.maximum(mag.sum(axis=0, keepdims=True), 1e-12)
    return np.sqrt((np.diff(mag, axis=1) ** 2).sum(axis=0))


def attack_time(y, sr: float, lo: float = 0.1, hi: float = 0.9) -> float:
    """The time the envelope takes to rise from 10 to 90 percent of its peak."""
    w = max(1, int(0.003 * sr))
    env = np.sqrt(np.convolve(np.asarray(y, dtype=float) ** 2, np.ones(w) / w, mode="same"))
    top = env.max()
    peak = int(np.argmax(env))
    a = int(np.argmax(env[: peak + 1] >= lo * top))
    b = int(np.argmax(env[: peak + 1] >= hi * top))
    return (b - a) / sr
