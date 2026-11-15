"""Monochord's second synthesizer (Part 52 of *Music, Built*): frequency modulation, grains, spectral models, samplers,
and physical models (Karplus-Strong, digital waveguides, modes).

    fm(fc, fm, index, n)                    Chowning's simple FM: sin(2 pi fc t + I(t) sin(2 pi fm t)); ``index`` may move
    sidebands(fc, fm, I, count)             the predicted lines: frequency fc + k fm, amplitude J_k(I) (negative
                                            frequencies fold back with a sign change)
    line_levels(y, freqs)                   measured amplitudes at given frequencies (Hann window, peak of three bins)
    operators(algorithm, ratios, levels, f, n, envs)
                                            a small DX-style engine: sine operators, each with a ratio, an output level
                                            and an envelope, wired as stacks or in parallel, with feedback on one
    grains(source, ...)                     granular synthesis: Hann grains read from a source at moving positions, at a
                                            chosen density, length, pitch and scatter
    gabor_grain(f, ms)                      one Gaussian-windowed sine: Gabor's acoustic quantum
    track_harmonics(y, f0)                  a spectral model: each harmonic's amplitude frame by frame
    resynth(track, n)                       additive resynthesis of the tracks
    split_partials(y, partials, f0)         the note near its partials, and the rest (the residual)
    ks_tuned(hz, seconds, ...)              Karplus-Strong with Jaffe and Smith's all-pass for exact tuning and a
                                            decay control
    waveguide(L, c, shape, ...)             a string as two delay lines carrying d'Alembert's travelling waves
    modal_string(string, shape, ...)        the same string as a sum of modes, each a damped sinusoid

No manim here.  Checked in ``tests/music/test_synth2.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, sosfilt
from scipy.special import jv

try:  # the loops below are compiled when numba is there; they are the same loops without it
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap(a[0]) if a and callable(a[0]) else wrap

SR = 48000

# --------------------------------------------------------------------------------------------- FM


def fm(fc: float, fmod: float, index, n: int, sr: float = SR, phase: float = 0.0) -> np.ndarray:
    """Chowning's FM: a carrier at fc whose phase is pushed back and forth by I sin(2 pi fm t)."""
    t = np.arange(n) / sr
    I = np.broadcast_to(np.asarray(index, float), (n,)) if np.ndim(index) else float(index)
    return np.sin(2 * np.pi * fc * t + I * np.sin(2 * np.pi * fmod * t + phase))


def sidebands(fc: float, fmod: float, I: float, count: int = 8) -> list[tuple[float, float]]:
    """The predicted spectrum: lines at fc + k fm with amplitude J_k(I), k = -count..count; a negative frequency
    reflects to positive with its sign flipped; lines that land on the same frequency add."""
    lines: dict[float, float] = {}
    for k in range(-count, count + 1):
        f = fc + k * fmod
        a = float(jv(k, I))
        if f < 0:
            f, a = -f, -a
        key = round(f, 6)
        lines[key] = lines.get(key, 0.0) + a
    return sorted(lines.items())


def line_levels(y, freqs, sr: float = SR) -> np.ndarray:
    """Amplitudes (as fractions of a full-scale sine) at the given frequencies, from a Hann-windowed FFT."""
    y = np.asarray(y, float)
    w = np.hanning(len(y))
    Y = np.abs(np.fft.rfft(y * w)) * 2 / w.sum()
    out = []
    for f in freqs:
        b = int(round(f * len(y) / sr))
        out.append(float(Y[max(b - 1, 0):b + 2].max()) if b + 1 < len(Y) else 0.0)
    return np.array(out)


def env_adsr(n: int, sr: float, a: float, d: float, s: float, r: float, gate: float) -> np.ndarray:
    t = np.arange(n) / sr
    e = np.where(t < a, t / max(a, 1e-6), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-6)))
    g = float(np.interp(gate, t, e)) if gate < n / sr else s
    return np.where(t >= gate, g * np.exp(-(t - gate) / max(r, 1e-6)), e)


@njit(cache=True)
def _ops_loop(n, sr, f, ratios, levels, envs, mod_of, fb_op, fb):
    """Run up to six operators in order 0..5; operator j's phase is modulated by the sum of the operators listed in
    mod_of[j] (indices, -1 for none).  Outputs of carriers are summed by the caller."""
    m = len(ratios)
    out = np.zeros((m, n))
    ph = np.zeros(m)
    prev = 0.0
    prev2 = 0.0
    for i in range(n):
        for j in range(m - 1, -1, -1):              # modulators have higher indices, so run them first
            mod = 0.0
            for q in range(mod_of.shape[1]):
                src = mod_of[j, q]
                if src >= 0:
                    mod += out[src, i]
            if j == fb_op:
                mod += fb * 0.5 * (prev + prev2)
            v = envs[j, i] * levels[j] * math.sin(2 * math.pi * ph[j] + mod)
            out[j, i] = v
            if j == fb_op:
                prev2 = prev
                prev = v
            ph[j] += f * ratios[j] / sr
            if ph[j] >= 1.0:
                ph[j] -= 1.0
    return out


ALGORITHMS = {
    # name: (carriers, {operator: [operators modulating it]}, feedback operator)
    "stack2": ((0,), {0: [1]}, 1),
    "stack3": ((0,), {0: [1], 1: [2]}, 2),
    "pairs": ((0, 2), {0: [1], 2: [3]}, 3),
    "y": ((0,), {0: [1, 2]}, 2),
    "parallel": ((0, 1, 2, 3), {}, -1),
}


def operators(algorithm: str, ratios, levels, f: float, n: int, envs=None, feedback: float = 0.0, sr: float = SR):
    """A small DX-style engine.  ``levels`` of carriers are output amplitudes; of modulators, modulation indices
    (radians).  ``envs`` is a list of arrays (one per operator, each length n) or None for constant."""
    carriers, wiring, fb_op = ALGORITHMS[algorithm]
    m = len(ratios)
    mod_of = -np.ones((m, 3), dtype=np.int64)
    for j, srcs in wiring.items():
        for q, s in enumerate(srcs):
            mod_of[j, q] = s
    E = np.ones((m, n)) if envs is None else np.array([np.ones(n) if e is None else np.asarray(e, float) for e in envs])
    out = _ops_loop(int(n), float(sr), float(f), np.asarray(ratios, float), np.asarray(levels, float), E, mod_of, int(fb_op), float(feedback))
    return out[list(carriers)].sum(axis=0)


# --------------------------------------------------------------------------------------------- grains


def gabor_grain(f: float, ms: float, sr: float = SR) -> np.ndarray:
    n = int(ms / 1000 * sr * 3)
    t = (np.arange(n) - n / 2) / sr
    s = ms / 1000 / 2.355                       # ``ms`` is the full width at half maximum
    return np.exp(-0.5 * (t / s) ** 2) * np.cos(2 * np.pi * f * t)


def grains(source, seconds: float, position, density: float = 40.0, grain_ms: float = 60.0, pitch: float = 1.0,
           scatter_s: float = 0.0, pitch_jitter: float = 0.0, sync: bool = False, sr: float = SR, seed: int = 0) -> dict:
    """Granular synthesis.  ``position(t)`` (seconds into the source, a function or a number) says where each grain
    is read; grains start ``density`` times a second (regularly if ``sync``, else at random, a Poisson cloud), last
    ``grain_ms``, are read at ``pitch`` times the speed (each jittered by up to ``pitch_jitter`` semitones), and their
    read positions are scattered by up to ``scatter_s``.  Returns the sound and every grain's (start, position, pitch)."""
    rng = np.random.default_rng(seed)
    src = np.asarray(source, float)
    n = int(seconds * sr)
    out = np.zeros(n + int(grain_ms / 1000 * sr * 4) + 8)
    pos_fn = position if callable(position) else (lambda t, p=float(position): p)
    starts = []
    t = 0.0
    while t < seconds:
        starts.append(t)
        t += (1.0 / density) if sync else rng.exponential(1.0 / density)
    log = []
    for t0 in starts:
        p = pos_fn(t0) + (rng.uniform(-scatter_s, scatter_s) if scatter_s else 0.0)
        r = pitch * 2 ** ((rng.uniform(-pitch_jitter, pitch_jitter) if pitch_jitter else 0.0) / 12)
        L = int(grain_ms / 1000 * sr)
        idx = p * sr + np.arange(L) * r
        if idx[0] < 0 or idx[-1] >= len(src) - 1:
            continue
        i0 = np.floor(idx).astype(int)
        fr = idx - i0
        g = (src[i0] * (1 - fr) + src[i0 + 1] * fr) * np.hanning(L)
        a = int(t0 * sr)
        out[a:a + L] += g
        log.append((t0, p, r))
    return {"y": out[:n], "grains": log}


# --------------------------------------------------------------------------------------------- spectral model


def partial_freqs(y, f0: float, count: int = 20, sr: float = SR, n: int = 1 << 17) -> np.ndarray:
    """Each partial's frequency in the whole note's spectrum, found in turn: partial k is sought near the last one
    plus the last spacing (so a piano's stretched partials are followed, not lost), refined by a parabola."""
    y = np.asarray(y, float)[:n]
    Y = np.log(np.abs(np.fft.rfft(y * np.hanning(len(y)), n)) + 1e-12)
    df = sr / n
    out = []
    for k in range(1, count + 1):
        guess = k * f0 if k <= 2 else out[-1] + (out[-1] - out[-2])
        lo, hi = int((guess - 0.3 * f0) / df), int((guess + 0.3 * f0) / df) + 1
        if hi + 1 >= len(Y):
            break
        b = lo + int(np.argmax(Y[lo:hi]))
        a, bb, c = Y[b - 1:b + 2]
        d = 0.5 * (a - c) / (a - 2 * bb + c) if (a - 2 * bb + c) != 0 else 0.0
        out.append((b + d) * df)
    return np.array(out)


def track_harmonics(y, f0: float, sr: float = SR, count: int = 20, frame: int = 4096, hop: int = 512):
    """Each partial's amplitude and frequency frame by frame: the peak within an eighth of f0 of the partial's
    frequency in the whole note (``partial_freqs``), refined by a parabola through the log-magnitudes (Serra and
    Smith's sinusoidal analysis, for a single note)."""
    y = np.asarray(y, float)
    pf = partial_freqs(y, f0, count, sr)
    w = np.hanning(frame)
    norm = 2 / w.sum()
    starts = np.arange(0, len(y) - frame, hop)
    amps = np.zeros((len(pf), len(starts)))
    freqs = np.tile(pf[:, None], (1, len(starts)))
    for j, s in enumerate(starts):
        Y = np.abs(np.fft.rfft(y[s:s + frame] * w)) * norm
        for k, fk in enumerate(pf):
            lo = int((fk - f0 / 8) * frame / sr)
            hi = int((fk + f0 / 8) * frame / sr) + 1
            b = lo + int(np.argmax(Y[lo:hi]))
            a, bb, c = np.log(Y[b - 1:b + 2] + 1e-12)
            d = 0.5 * (a - c) / (a - 2 * bb + c) if (a - 2 * bb + c) != 0 else 0.0
            freqs[k, j] = (b + d) * sr / frame
            amps[k, j] = float(np.exp(bb - 0.25 * (a - c) * d))
    times = (starts + frame / 2) / sr
    return {"t": times, "amps": amps, "freqs": freqs, "partials": pf}


def split_partials(y, partials, f0: float, sr: float = SR, frame: int = 4096, hop: int = 512, width: float = 0.12):
    """Split a note into the part near its partials and the rest, by masking the short-time spectrum within
    ``width`` times f0 of each partial; the two add back to the note exactly."""
    from scipy.signal import istft, stft
    f, t, Z = stft(np.asarray(y, float), sr, nperseg=frame, noverlap=frame - hop)
    mask = np.zeros(len(f), bool)
    for fk in partials:
        mask |= np.abs(f - fk) < width * f0
    _, near = istft(Z * mask[:, None], sr, nperseg=frame, noverlap=frame - hop)
    _, rest = istft(Z * (~mask)[:, None], sr, nperseg=frame, noverlap=frame - hop)
    n = len(y)
    return near[:n], rest[:n]


def resynth(track: dict, n: int, sr: float = SR) -> np.ndarray:
    """Additive resynthesis: each harmonic a sine whose amplitude and frequency follow its track (interpolated
    between frames), phases accumulated."""
    t = np.arange(n) / sr
    y = np.zeros(n)
    for k in range(track["amps"].shape[0]):
        a = np.interp(t, track["t"], track["amps"][k], left=track["amps"][k, 0], right=0.0)
        f = np.interp(t, track["t"], track["freqs"][k], left=track["freqs"][k, 0], right=track["freqs"][k, -1])
        if not np.any(a > 0):
            continue
        y += a * np.sin(2 * np.pi * np.cumsum(f) / sr)
    return y


# --------------------------------------------------------------------------------------------- Karplus-Strong, tuned


@njit(cache=True)
def _ks_tuned(buf, n_out, c, rho, stretch):
    n = len(buf)
    out = np.empty(n_out)
    k = 0
    prev = 0.0
    ap_x1 = 0.0
    ap_y1 = 0.0
    for i in range(n_out):
        x = buf[k]
        lp = rho * ((1.0 - stretch) * x + stretch * prev)
        prev = x
        ap = c * lp + ap_x1 - c * ap_y1        # first-order all-pass: a fractional delay
        ap_x1 = lp
        ap_y1 = ap
        buf[k] = ap
        out[i] = x
        k += 1
        if k == n:
            k = 0
    return out


def ks_tuned(hz: float, seconds: float, sr: float = SR, seed: int = 0, rho: float = 0.999, stretch: float = 0.5,
             tuned: bool = True) -> np.ndarray:
    """Karplus-Strong with Jaffe and Smith's extensions (1983): the loop's delay is N samples, plus the averaging
    filter's half sample, plus a first-order all-pass supplying the fractional rest, so the pitch is exact; ``rho``
    shortens the decay.  ``tuned=False`` drops the all-pass (the delay is rounded)."""
    P = sr / hz                                  # the loop's total delay, samples
    if tuned:
        N = int(math.floor(P - stretch - 0.1))
        frac = P - stretch - N
        c = (1 - frac) / (1 + frac)
    else:
        N = max(int(round(P - stretch)), 2)
        c = 0.0
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, N)
    buf -= buf.mean()
    y = _ks_tuned(buf, int(seconds * sr), c, rho, stretch)
    return y / np.max(np.abs(y))


def ks_loop_delay(hz: float, sr: float = SR, stretch: float = 0.5, tuned: bool = True) -> float:
    """The loop delay at low frequencies (samples), so the pitch is sr / delay."""
    P = sr / hz
    if tuned:
        N = int(math.floor(P - stretch - 0.1))
        frac = P - stretch - N
        return N + stretch + frac
    return max(int(round(P - stretch)), 2) + stretch


def measured_pitch(y, sr: float = SR, guess: float | None = None) -> float:
    """The fundamental by autocorrelation with parabolic refinement, over the middle of the note."""
    y = np.asarray(y, float)
    seg = y[len(y) // 8: len(y) // 8 + 16384] if len(y) > 20000 else y
    seg = seg - seg.mean()
    ac = np.fft.irfft(np.abs(np.fft.rfft(seg, 2 * len(seg))) ** 2)[: len(seg)]
    lo = int(sr / (guess * 1.3)) if guess else 20
    hi = int(sr / (guess / 1.3)) if guess else len(seg) // 2
    b = lo + int(np.argmax(ac[lo:hi]))
    a, bb, c = ac[b - 1:b + 2]
    d = 0.5 * (a - c) / (a - 2 * bb + c)
    return sr / (b + d)


# --------------------------------------------------------------------------------------------- waveguides and modes


@njit(cache=True)
def _wg_loop(right, left, steps, pick, refl, out):
    """Two rails (right-going and left-going), one sample of travel per step; at each fixed end the displacement
    stays zero, so the arriving wave returns inverted (at the bridge end multiplied by ``refl``, a loss)."""
    M = len(right)
    for i in range(steps):
        out[i] = right[pick] + left[pick]
        for j in range(M - 1, 0, -1):
            right[j] = right[j - 1]
        for j in range(0, M - 1):
            left[j] = left[j + 1]
        right[0] = -left[0]
        left[M - 1] = -refl * right[M - 1]


def waveguide(shape, seconds: float, sr: float, refl: float = 1.0, pickup: float = 0.2371) -> np.ndarray:
    """d'Alembert's solution on a computer: the string's initial shape (sampled at M points, the string one sample
    of travel per point) is split into two halves travelling left and right; each step every value moves one place;
    at each end the wave comes back inverted.  The output is the displacement at the pickup."""
    u = np.asarray(shape, float)
    M = len(u)
    right = 0.5 * u.copy()
    left = 0.5 * u.copy()
    steps = int(round(seconds * sr))
    out = np.zeros(steps)
    pick = int(np.clip(round(pickup * (M - 1)), 1, M - 2))
    _wg_loop(right, left, steps, pick, float(refl), out)
    return out


def modal_string(f1: float, B: float, decays, shape_coeffs, seconds: float, sr: float, pickup: float = 0.2371) -> np.ndarray:
    """A string as a sum of modes: mode n at n f1 sqrt(1 + B n^2), amplitude its shape's sine coefficient times its
    shape at the pickup, dying at its own rate."""
    t = np.arange(int(round(seconds * sr))) / sr
    y = np.zeros(len(t))
    for n, a in enumerate(shape_coeffs, start=1):
        if a == 0:
            continue
        fn = n * f1 * math.sqrt(1 + B * n * n)
        y += a * math.sin(n * math.pi * pickup) * np.cos(2 * np.pi * fn * t) * np.exp(-decays[n - 1] * t)
    return y


@njit(cache=True)
def _clarinet_loop(pm, L, a, out):
    """A bore of L samples (one way and back), a reed at one end, an open bell at the other (after Smith's
    waveguide clarinet, as in Cook and Scavone's toolkit).  The wave returning from the bell comes back inverted and
    smoothed by a one-pole low-pass, ``bell`` (the bell lets the highs out); the pressure difference across the reed, dp, sets
    how much of it is reflected: the reed table r = 0.7 - 0.3 dp, clipped to [-1, 1]."""
    buf = np.zeros(L)
    k = 0
    prev = 0.0
    for i in range(len(pm)):
        back = buf[k]
        prev = (1.0 - a) * back + a * prev
        p_in = -0.95 * prev
        dp = p_in - pm[i]
        r = 0.7 - 0.3 * dp
        if r > 1.0:
            r = 1.0
        elif r < -1.0:
            r = -1.0
        new = pm[i] + dp * r
        buf[k] = new
        out[i] = new
        k += 1
        if k == L:
            k = 0


def clarinet(hz: float, seconds: float, sr: float = SR, pressure: float = 0.9, breath: float = 0.02, seed: int = 0,
             attack: float = 0.03, release: float = 0.05, bell: float = 0.5, oversample: int = 4, normalize: bool = True) -> np.ndarray:
    """A waveguide clarinet: a cylindrical bore (a delay line; the wave's round trip and inversion at the bell give a
    period of two round trips, so the closed-open pipe sounds at sr / (2 L)), a nonlinear reed, a lossy bell.
    ``pressure`` is the player's mouth pressure (about 0.9 of the reed's closing pressure plays well; a third of it
    barely sounds).  Run at ``oversample`` times the rate so that the whole-sample delay tunes finely."""
    from scipy.signal import resample_poly
    fs = sr * oversample
    rng = np.random.default_rng(seed)
    n = int(seconds * fs)
    t = np.arange(n) / fs
    env = np.clip(t / attack, 0, 1) * np.clip((seconds - t) / release, 0, 1)
    pm = pressure * env * (1 + breath * rng.standard_normal(n))
    a = bell ** (1.0 / oversample)                                 # the same bell filter at the higher rate
    L = max(int(round(fs / hz / 2 - a / (1 - a))), 2)             # the low-pass delays by about a / (1 - a) samples
    out = np.zeros(n)
    _clarinet_loop(pm, L, float(a), out)
    out = resample_poly(out, 1, oversample)[: int(seconds * sr)]
    out = sosfilt(butter(1, 20.0, btype="high", fs=sr, output="sos"), out)
    return out / (np.max(np.abs(out)) + 1e-12) if normalize else out
