"""Monochord's synthesizer (Part 51 of *Music, Built*): oscillators, a ladder filter, envelopes and modulation, drum
circuits, and fitting a patch to a sound.

    saw_naive, saw_polyblep, saw_blit,      the same sawtooth four ways: aliasing; a polynomial correction at each jump
    saw_additive                            (Valimaki and Huovilainen); an integrated band-limited impulse train (Stilson
                                            and Smith); a sum of harmonics below Nyquist
    triangle                                odd harmonics as 1/k^2
    pulse(f, width, ...)                    a PolyBLEP pulse whose width may move (PWM)
    sync_saw(f_master, f_slave, ...)        hard sync: the slave restarts whenever the master does
    unison(f, voices, detune)               detuned copies summed (a supersaw)
    drawbars(f, settings)                   a Hammond organ's nine drawbars (16' to 1') as additive synthesis, tempered
    ladder(x, fc, k, sr)                    a Moog ladder: four tanh one-poles and global feedback k (Huovilainen's model)
    ladder_trap(x, fc, k, sr)               the same circuit by the trapezoidal rule and Newton (zero-delay feedback)
    ladder_ode(x, fc, k, sr)                the same circuit equations integrated finely, for checking
    ladder_response(fc, k, f)               the linear ladder's magnitude, 1 / |(1 + s/wc)^4 + k|
    adsr(n, sr, a, d, s, r, gate_s)         an envelope
    wavetable(f, tables, position, ...)     scanning through stored single cycles
    resonator(x, f, q)                      a two-pole resonator, struck: the heart of an analog drum
    kick_circuit, snare_circuit, clap_circuit  drum circuits, schematically (the hats are Part 40's six square waves)
    fit_patch(target, f)                    search a small subtractive patch for the closest harmonic levels

No manim here.  Checked in ``tests/music/test_synth.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, sosfilt

try:  # the loops below are compiled when numba is there; they are the same loops without it
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap(a[0]) if a and callable(a[0]) else wrap

SR = 48000

# --------------------------------------------------------------------------------------------- oscillators


def _phase(f, n, sr):
    f = np.broadcast_to(np.asarray(f, float), (n,)) if np.ndim(f) else np.full(n, float(f))
    return np.cumsum(f / sr) % 1.0, f / sr


def saw_naive(f, n: int, sr: float = SR) -> np.ndarray:
    ph, _ = _phase(f, n, sr)
    return 2 * ph - 1


def _polyblep(t, dt):
    """The polynomial band-limited step's correction near a jump at phase 0 (t in [0, 1), increment dt): two
    quadratic pieces, one sample either side of the jump (Valimaki and Huovilainen 2007)."""
    dt = np.broadcast_to(np.asarray(dt, float), np.shape(t))
    y = np.zeros_like(t)
    a = t < dt
    u = t[a] / dt[a]
    y[a] = 2 * u - u * u - 1
    b = t > 1 - dt
    u = (t[b] - 1) / dt[b]
    y[b] = u * u + 2 * u + 1
    return y


def saw_polyblep(f, n: int, sr: float = SR) -> np.ndarray:
    ph, dt = _phase(f, n, sr)
    return 2 * ph - 1 - _polyblep(ph, dt)


def saw_additive(f: float, n: int, sr: float = SR) -> np.ndarray:
    t = np.arange(n) / sr
    y = np.zeros(n)
    k = 1
    while k * f < sr / 2:
        y += np.sin(2 * np.pi * k * f * t) / k * (-1) ** (k + 1)
        k += 1
    return 2 / np.pi * y


def pulse(f, width, n: int, sr: float = SR) -> np.ndarray:
    """A pulse wave as the difference of two band-limited saws offset by the width."""
    ph, dt = _phase(f, n, sr)
    w = np.broadcast_to(np.asarray(width, float), (n,)) if np.ndim(width) else np.full(n, float(width))
    ph2 = (ph + w) % 1.0
    s1 = 2 * ph - 1 - _polyblep(ph, dt)
    s2 = 2 * ph2 - 1 - _polyblep(ph2, dt)
    return 0.5 * (s1 - s2)


def saw_blit(f: float, n: int, sr: float = SR, leak: float = 0.999) -> np.ndarray:
    """Stilson and Smith's route: a band-limited impulse train (the closed-form sum of M harmonics, M odd, every one
    below Nyquist) integrated by a leaky integrator, less its mean: a sawtooth with almost no aliasing (falling)."""
    P = sr / f
    M = 2 * int(P / 2) + 1
    t = np.arange(n)
    x = M * t / P
    num = np.sin(np.pi * x)
    den = M * np.sin(np.pi * x / M)
    small = np.abs(den) < 1e-9
    b = np.where(small, 1.0, num / np.where(small, 1.0, den)) * M / P
    b -= 1.0 / P
    y = _leaky(b, leak)
    y -= y.mean()
    return -2 * y / max(np.max(np.abs(y)), 1e-12)


@njit(cache=True)
def _leaky(b, leak):
    y = np.empty(len(b))
    acc = 0.0
    for i in range(len(b)):
        acc = leak * acc + b[i]
        y[i] = acc
    return y


def triangle(f: float, n: int, sr: float = SR) -> np.ndarray:
    """Odd harmonics falling as 1/k^2, summed below Nyquist."""
    t = np.arange(n) / sr
    y = np.zeros(n)
    k = 1
    while k * f < sr / 2:
        y += (-1) ** ((k - 1) // 2) * np.sin(2 * np.pi * k * f * t) / k ** 2
        k += 2
    return 8 / np.pi ** 2 * y


def sync_saw(f_master: float, f_slave, n: int, sr: float = SR) -> np.ndarray:
    """Hard sync: the slave's phase is reset to zero whenever the master's wraps (naive; for the picture and the ear)."""
    fs = np.broadcast_to(np.asarray(f_slave, float), (n,)) if np.ndim(f_slave) else np.full(n, float(f_slave))
    return _sync_loop(float(f_master), np.ascontiguousarray(fs, dtype=float), float(sr))


@njit(cache=True)
def _sync_loop(fm, fs, sr):
    n = len(fs)
    pm = 0.0
    ps = 0.0
    y = np.empty(n)
    for i in range(n):
        pm += fm / sr
        ps += fs[i] / sr
        if pm >= 1.0:
            pm -= 1.0
            ps = pm * fs[i] / fm
        ps = ps % 1.0
        y[i] = 2 * ps - 1
    return y


def unison(f: float, n: int, voices: int = 7, detune_cents: float = 18.0, sr: float = SR, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for v in range(voices):
        c = 0.0 if voices == 1 else detune_cents * (2 * v / (voices - 1) - 1)
        fv = f * 2 ** (c / 1200)
        ph0 = rng.random()
        ph = (ph0 + np.cumsum(np.full(n, fv / sr))) % 1.0
        y += 2 * ph - 1 - _polyblep(ph, fv / sr)
    return y / math.sqrt(voices)


DRAWBAR_RATIOS = (0.5, 1.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0)      # 16', 5 1/3', 8', 4', 2 2/3', 2', 1 3/5', 1 1/3', 1'
DRAWBAR_SEMIS = (-12, 7, 0, 12, 19, 24, 28, 31, 36)                 # the tonewheels they really come from
DRAWBAR_NAMES = ("16'", "5 1/3'", "8'", "4'", "2 2/3'", "2'", "1 3/5'", "1 1/3'", "1'")


def drawbar_ratios(tempered: bool = True):
    """A Hammond takes every drawbar from the tonewheel of the nearest equal-tempered note, so its 'harmonics' are
    tempered: the 2 2/3' fifth about 2 cents flat, the 1 3/5' third about 14 cents sharp."""
    return tuple(2 ** (s / 12) for s in DRAWBAR_SEMIS) if tempered else DRAWBAR_RATIOS


def drawbars(f: float, settings, n: int, sr: float = SR, tempered: bool = True) -> np.ndarray:
    """Each drawbar adds a sine at its footage's pitch; positions 0 to 8, about 3 dB a step (8 is full)."""
    t = np.arange(n) / sr
    y = np.zeros(n)
    for r, s in zip(drawbar_ratios(tempered), settings):
        if s > 0:
            y += 10 ** (-3 * (8 - s) / 20) * np.sin(2 * np.pi * r * f * t)
    return y / max(np.max(np.abs(y)), 1e-12)


# --------------------------------------------------------------------------------------------- the ladder


def ladder_response(fc: float, k: float, f) -> np.ndarray:
    s = 1j * np.asarray(f, float) / fc
    return 20 * np.log10(np.abs(1.0 / ((1 + s) ** 4 + k)))


@njit(cache=True)
def _ladder_loop(x, g, k, half, nonlinear):
    n = len(x)
    s0 = s1 = s2 = s3 = 0.0
    prev = 0.0
    y = np.empty(n)
    for i in range(n):
        fb = 0.5 * (s3 + prev) if half else s3
        prev = s3
        if nonlinear:
            u = math.tanh(x[i] - k * fb)
            s0 += g[i] * (u - math.tanh(s0))
            t0 = math.tanh(s0)
            s1 += g[i] * (t0 - math.tanh(s1))
            t1 = math.tanh(s1)
            s2 += g[i] * (t1 - math.tanh(s2))
            t2 = math.tanh(s2)
            s3 += g[i] * (t2 - math.tanh(s3))
        else:
            u = x[i] - k * fb
            s0 += g[i] * (u - s0)
            s1 += g[i] * (s0 - s1)
            s2 += g[i] * (s1 - s2)
            s3 += g[i] * (s2 - s3)
        y[i] = s3
    return y


def ladder(x, fc, k: float, sr: float = SR, oversample: int = 2, half: bool = True, nonlinear: bool = True) -> np.ndarray:
    """Huovilainen's nonlinear model: four one-pole stages, each driven through tanh, with the output fed back to the
    input multiplied by k (k = 4 is the edge of self-oscillation), the feedback averaged over the last two steps (his
    half-sample correction); run at ``oversample`` times the rate.  ``nonlinear=False`` drops every tanh."""
    x = np.asarray(x, float)
    n = len(x)
    fcs = np.broadcast_to(np.asarray(fc, float), (n,)) if np.ndim(fc) else np.full(n, float(fc))
    fs = sr * oversample
    g = 1 - np.exp(-2 * np.pi * np.repeat(fcs, oversample) / fs)
    y = _ladder_loop(np.repeat(x, oversample), g, float(k), bool(half), bool(nonlinear))
    return y[oversample - 1::oversample]


@njit(cache=True)
def _trap_loop(x, wc, k, h, iters):
    v = np.zeros(4)
    out = np.empty(len(x))
    f0 = np.empty(4)
    f1 = np.empty(4)
    w = np.empty(4)
    F = np.empty(4)
    diag = np.empty(4)
    sub = np.empty(4)
    dl = np.empty(4)
    a = 0.5 * h * wc
    for i in range(len(x)):
        xi = x[i]
        prev = math.tanh(xi - k * v[3])
        for j in range(4):
            tj = math.tanh(v[j])
            f0[j] = wc * (prev - tj)
            prev = tj
            w[j] = v[j] + h * f0[j]          # a forward step as the first guess
        for _ in range(iters):
            tu = math.tanh(xi - k * w[3])
            prev = tu
            for j in range(4):
                tj = math.tanh(w[j])
                f1[j] = wc * (prev - tj)
                diag[j] = 1.0 + a * (1 - tj * tj)
                sub[j] = -a * (1 - prev * prev) if j > 0 else 0.0
                prev = tj
                F[j] = w[j] - v[j] - 0.5 * h * (f0[j] + f1[j])
            corner = a * k * (1 - tu * tu)
            # the Jacobian is lower bidiagonal plus one corner (the feedback): write each step as p + q * step_0
            p = 0.0
            q = 1.0
            for j in range(1, 4):
                p, q = (F[j] - sub[j] * p) / diag[j], -sub[j] * q / diag[j]
            d0 = (F[0] - corner * p) / (diag[0] + corner * q)
            dl[0] = d0
            for j in range(1, 4):
                dl[j] = (F[j] - sub[j] * dl[j - 1]) / diag[j]
            for j in range(4):
                w[j] -= dl[j]
        for j in range(4):
            v[j] = w[j]
        out[i] = v[3]
    return out


def ladder_trap(x, fc: float, k: float, sr: float = SR, oversample: int = 1, iters: int = 3) -> np.ndarray:
    """The same circuit equations by the trapezoidal rule, solved by Newton's method at every step: the feedback has no
    delay in it ('zero-delay feedback', Zavalishin's term), and the error falls four times for each doubling of the
    rate rather than twice."""
    x = np.repeat(np.asarray(x, float), oversample)
    y = _trap_loop(x, 2 * np.pi * fc, float(k), 1.0 / (sr * oversample), int(iters))
    return y[oversample - 1::oversample]


@njit(cache=True)
def _ode_loop(x, wc, k, h, sub):
    v = np.zeros(4)
    out = np.empty(len(x))
    a1 = np.empty(4)
    a2 = np.empty(4)
    a3 = np.empty(4)
    a4 = np.empty(4)
    w = np.empty(4)
    for i in range(len(x)):
        xi = x[i]
        for _ in range(sub):
            for stage in range(4):
                if stage == 0:
                    w[:] = v
                    dst = a1
                elif stage == 1:
                    for j in range(4):
                        w[j] = v[j] + h / 2 * a1[j]
                    dst = a2
                elif stage == 2:
                    for j in range(4):
                        w[j] = v[j] + h / 2 * a2[j]
                    dst = a3
                else:
                    for j in range(4):
                        w[j] = v[j] + h * a3[j]
                    dst = a4
                prev = math.tanh(xi - k * w[3])
                for j in range(4):
                    tj = math.tanh(w[j])
                    dst[j] = wc * (prev - tj)
                    prev = tj
            for j in range(4):
                v[j] += h / 6 * (a1[j] + 2 * a2[j] + 2 * a3[j] + a4[j])
        out[i] = v[3]
    return out


def ladder_ode(x, fc: float, k: float, sr: float = SR, sub: int = 16) -> np.ndarray:
    """The circuit equations dV_j/dt = wc (tanh(V_{j-1}) - tanh(V_j)), V_0 = x - k V_4, integrated by fourth-order
    Runge-Kutta with ``sub`` steps per sample (the input held between samples)."""
    return _ode_loop(np.asarray(x, float), 2 * np.pi * fc, float(k), 1.0 / (sr * sub), int(sub))


# --------------------------------------------------------------------------------------------- envelopes, tables, drums


def adsr(n: int, sr: float = SR, a: float = 0.01, d: float = 0.2, s: float = 0.6, r: float = 0.3, gate_s: float | None = None) -> np.ndarray:
    t = np.arange(n) / sr
    g = gate_s if gate_s is not None else n / sr - r
    env = np.where(t < a, t / max(a, 1e-6), s + (1 - s) * np.exp(-(t - a) / max(d / 4, 1e-6)))
    at_release = float(np.interp(g, t, env)) if g < n / sr else s
    env = np.where(t >= g, at_release * np.exp(-(t - g) / max(r / 5, 1e-6)), env)
    return env


def make_tables(count: int = 8, size: int = 2048, harmonics: int = 48):
    """Single-cycle tables morphing from a sine to a bright, hollow wave (odd harmonics, then all of them)."""
    ph = np.arange(size) / size
    tabs = []
    for j in range(count):
        a = j / (count - 1)
        y = np.zeros(size)
        for k in range(1, harmonics + 1):
            w = (a ** 0.7) / k if k > 1 else 1.0
            if k % 2 == 0:
                w *= max(0.0, 2 * a - 1)
            y += w * np.sin(2 * np.pi * k * ph)
        tabs.append(y / np.max(np.abs(y)))
    return np.array(tabs)


def wavetable(f: float, tables, position, n: int, sr: float = SR) -> np.ndarray:
    """Read the tables at the oscillator's phase, cross-fading between neighbouring tables as ``position`` (0..1) moves
    (no band-limiting by octave here; the tables stop at 48 harmonics, so notes below 500 Hz do not alias)."""
    size = tables.shape[1]
    ph = (np.cumsum(np.full(n, f / sr)) % 1.0) * size
    i0 = np.floor(ph).astype(int) % size
    fr = ph - np.floor(ph)
    pos = np.broadcast_to(np.asarray(position, float), (n,)) if np.ndim(position) else np.full(n, float(position))
    p = pos * (len(tables) - 1)
    j0 = np.clip(np.floor(p).astype(int), 0, len(tables) - 2)
    w = p - j0
    def read(j):
        a = tables[j, i0]
        b = tables[j, (i0 + 1) % size]
        return a + fr * (b - a)
    return (1 - w) * read(j0) + w * read(j0 + 1)


def resonator(x, f, q: float, sr: float = SR) -> np.ndarray:
    """A two-pole resonator, y[n] = 2 r cos(w) y[n-1] - r^2 y[n-2] + x[n], with r = exp(-pi f / (q sr)): struck, it
    rings at f and dies with time constant 2q / (2 pi f); f may move sample by sample."""
    x = np.asarray(x, float)
    fs = np.broadcast_to(np.asarray(f, float), x.shape) if np.ndim(f) else np.full(len(x), float(f))
    r = np.exp(-np.pi * fs / (q * sr))
    a1 = 2 * r * np.cos(2 * np.pi * fs / sr)
    a2 = r * r
    return _two_pole(x, a1, a2)


@njit(cache=True)
def _two_pole(x, a1, a2):
    y = np.zeros(len(x))
    y1 = y2 = 0.0
    for i in range(len(x)):
        y0 = a1[i] * y1 - a2[i] * y2 + x[i]
        y[i] = y0
        y2 = y1
        y1 = y0
    return y


def trigger(n: int, sr: float = SR, width_ms: float = 1.0) -> np.ndarray:
    """The drum machine's trigger: a short square pulse (the 808's is about a millisecond), smoothed at its edges."""
    x = np.zeros(n)
    k = max(int(width_ms * sr / 1000), 2)
    x[:k] = np.hanning(2 * k)[k // 2: k // 2 + k] if k > 4 else 1.0
    return x


def kick_circuit(sr: float = SR, f: float = 52.0, q: float = 74.0, bend: float = 0.6, seconds: float = 1.2) -> np.ndarray:
    """A bridged-T resonator struck by the trigger; while the pulse lasts it pulls the frequency up by ``bend``, so each
    kick starts with a downward chirp.  q = 74 at 52 Hz gives a time constant of 2q / (2 pi f) = 0.45 s."""
    n = int(seconds * sr)
    t = np.arange(n) / sr
    y = resonator(trigger(n, sr), f * (1 + bend * np.exp(-t / 0.02)), q, sr)
    return y / np.max(np.abs(y))


def snare_circuit(sr: float = SR, seconds: float = 0.4, seed: int = 0, snappy: float = 0.8) -> np.ndarray:
    """Two resonators about an octave apart (the drum's body) and high-passed noise with its own envelope (the
    'snappy' control: the wires)."""
    rng = np.random.default_rng(seed)
    n = int(seconds * sr)
    t = np.arange(n) / sr
    tr = trigger(n, sr)
    body = resonator(tr, 180.0, 8.0, sr) + 0.6 * resonator(tr, 330.0, 10.0, sr)
    body /= np.max(np.abs(body))
    noise = sosfilt(butter(2, 1800, btype="high", fs=sr, output="sos"), rng.standard_normal(n)) * np.exp(-t / 0.07)
    noise /= np.max(np.abs(noise))
    y = body + snappy * noise
    return y / np.max(np.abs(y))


def clap_circuit(sr: float = SR, seconds: float = 0.5, seed: int = 1) -> np.ndarray:
    """The 808's clap: band-passed noise in three quick bursts about 10 ms apart (many hands, not quite together), then a
    longer reverberant tail."""
    rng = np.random.default_rng(seed)
    n = int(seconds * sr)
    t = np.arange(n) / sr
    env = np.zeros(n)
    for k in range(3):
        a = k * 0.010
        env += np.where(t >= a, np.exp(-(t - a) / 0.004), 0.0) * (t < a + 0.010)
    env += 0.5 * np.where(t >= 0.03, np.exp(-(t - 0.03) / 0.09), 0.0)
    y = sosfilt(butter(2, [800, 1600], btype="band", fs=sr, output="sos"), rng.standard_normal(n)) * env
    return y / np.max(np.abs(y))


# --------------------------------------------------------------------------------------------- fitting a patch


def harmonic_levels(y, f: float, sr: float = SR, n: int = 8192, hi: float = 12000.0, floor: float = -60.0) -> np.ndarray:
    """Levels (dB re the loudest, clipped at ``floor``) at every multiple of f/2 up to ``hi``: the harmonics of f, and
    the slots between them, where a sub-octave or a fifth below would show (Hann window, peak of three bins)."""
    y = np.asarray(y, float)[:n]
    Y = np.abs(np.fft.rfft(y * np.hanning(len(y)), n))
    out = []
    j = 1
    while j * f / 2 <= hi:
        b = int(round(j * f / 2 * n / sr))
        out.append(Y[max(b - 1, 0):b + 2].max())
        j += 1
    L = 20 * np.log10(np.array(out) + 1e-12)
    return np.maximum(L - L.max(), floor)


def patch_distance(a: np.ndarray, b: np.ndarray, floor: float = -60.0) -> float:
    """The root-mean-square difference of two sets of harmonic levels, dB, over the slots where either sound has
    something above the floor."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = (a > floor) | (b > floor)
    return float(np.sqrt(np.mean((a[m] - b[m]) ** 2)))


def patch(f: float, n: int, cutoff: float, res: float, mix: float, sr: float = SR) -> np.ndarray:
    """A two-oscillator subtractive patch: a saw and a square (mix 0..1 toward the square) through the ladder."""
    src = (1 - mix) * saw_polyblep(f, n, sr) + mix * pulse(f, 0.5, n, sr)
    return ladder(0.5 * src, cutoff, res, sr)


def fit_patch(target, f: float, sr: float = SR, cutoffs=None, ress=(0.0, 1.0, 2.0, 3.0, 3.5), mixes=(0.0, 0.25, 0.5, 0.75, 1.0)) -> dict:
    """Grid search over cutoff, resonance and oscillator mix for the smallest distance between harmonic levels, then
    a finer search of cutoff around the best."""
    n = 8192
    tgt = harmonic_levels(target, f, sr)
    cutoffs = cutoffs if cutoffs is not None else np.geomspace(200, 8000, 14)
    best = None
    tried = []
    for c in cutoffs:
        for r in ress:
            for m in mixes:
                d = patch_distance(harmonic_levels(patch(f, n, c, r, m, sr), f, sr), tgt)
                tried.append((float(c), float(r), float(m), d))
                if best is None or d < best[3]:
                    best = (float(c), float(r), float(m), d)
    for c in np.geomspace(best[0] / 1.3, best[0] * 1.3, 9):
        d = patch_distance(harmonic_levels(patch(f, n, c, best[1], best[2], sr), f, sr), tgt)
        if d < best[3]:
            best = (float(c), best[1], best[2], d)
    return {"cutoff": best[0], "res": best[1], "mix": best[2], "distance_db": best[3], "tried": len(tried), "grid": tried}
