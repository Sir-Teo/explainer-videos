"""Monochord's live sound (Part 59 of *Music, Built*): feedback and ringing out, point and line sources and their
field maps, curved and steered arrays, cardioid subwoofers, delay towers, air absorption, transfer-function
measurement, a wireless channel planner, speech intelligibility, and noise dose.

    loop_response(f, gain_db, ...)          the open loop microphone -> amplifier -> loudspeaker -> room -> microphone
    feedback(...)                           the gain at which the loop first reaches 1, and the frequency that howls
    closed_loop(x, h, g)                    the loop run in time: y = x + g (h * y)
    field(sources, f, xs, ys)               the pressure of many point sources on a grid (magnitude, dB)
    line_array(n, spacing, ...)             source positions of a straight or curved (J) array
    on_axis_levels(sources, f, dists)       level against distance along a line of seats
    cardioid_sub(f, d, ...)                 a front and a delayed, inverted rear subwoofer: front/back levels
    delay_time(d_main, d_tower, temp_c)     a delay tower's delay, with 10 ms of precedence, at a temperature
    speed_of_sound(temp_c)                  331.3 + 0.606 T
    air_absorption_db_per_m(f, T, RH)       ISO 9613-1
    transfer_function(x, y, nfft)           dual-channel measurement: H = Sxy / Sxx, coherence, delay
    plan_channels(lo, hi, n, ...)           wireless frequencies with no third-order intermodulation product nearby
    sti(T, snr_db)                          the speech transmission index from reverberation time and noise
    dose(levels_dba, hours)                 noise dose (NIOSH: 85 dBA for 8 h, 3 dB exchange)

No manim here.  Checked in ``tests/music/test_live.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import fftconvolve

SR = 48000


def speed_of_sound(temp_c: float = 20.0) -> float:
    return 331.3 + 0.606 * temp_c


C = speed_of_sound(20.0)


# --------------------------------------------------------------------------------------------- feedback
def loop_response(f, ir, gain_db: float) -> np.ndarray:
    """The open-loop transfer function G H(f): an amplifier of ``gain_db`` and the acoustic path ``ir`` (loudspeaker to
    microphone, including the room)."""
    n = 1 << int(math.ceil(math.log2(len(ir) * 2)))
    H = np.fft.rfft(ir, n)
    ff = np.fft.rfftfreq(n, 1 / SR)
    Hf = np.interp(f, ff, H.real) + 1j * np.interp(f, ff, H.imag)
    return 10 ** (gain_db / 20) * Hf


def feedback(ir, fmin: float = 100.0, fmax: float = 8000.0, notches=()) -> dict:
    """The gain before feedback, by Nyquist's criterion: the closed loop 1 / (1 - G H) first becomes unstable as G grows
    where G H(f) reaches +1 on the real axis, so the maximum stable gain is -20 log10 of the largest positive real part
    of H, and the howl starts at that frequency.  (The largest |H| is a quick estimate that ignores phase.)
    ``notches``: (frequency, depth dB, Q) filters in the loop."""
    n = 1 << int(math.ceil(math.log2(len(ir) * 4)))
    H = np.fft.rfft(ir, n)
    f = np.fft.rfftfreq(n, 1 / SR)
    for fc, depth, q in notches:
        H = H * notch_response(f, fc, depth, q)
    sel = (f >= fmin) & (f <= fmax)
    re = H[sel].real
    i = int(np.argmax(re))
    mag = np.abs(H[sel])
    j = int(np.argmax(mag))
    return {"max_gain_db": float(-20 * np.log10(re[i])), "howl_hz": float(f[sel][i]), "f": f[sel], "mag_db": 20 * np.log10(mag + 1e-12),
            "peak_gain_db": float(-20 * np.log10(mag[j])), "peak_hz": float(f[sel][j])}


def notch_response(f, fc: float, depth_db: float, q: float):
    """A peaking cut of ``depth_db`` at fc (the analogue prototype)."""
    s = 1j * np.asarray(f, float) / fc
    A = 10 ** (-abs(depth_db) / 40)
    return (s ** 2 + s * A / q + 1) / (s ** 2 + s / (A * q) + 1)


def closed_loop(x, ir, gain_db: float, seconds: float | None = None) -> np.ndarray:
    """y[n] = x[n] + g sum_k h[k] y[n-k], computed block by block (the acoustic path's first tap is at least one block
    away, so each block depends only on the past).  The output is the microphone signal."""
    g = 10 ** (gain_db / 20)
    h = np.asarray(ir, float)
    first = int(np.argmax(np.abs(h) > 1e-6 * np.max(np.abs(h))))
    B = max(1, min(first, 256))
    n = int(seconds * SR) if seconds else len(x)
    x = np.r_[np.asarray(x, float), np.zeros(max(0, n + B - len(x)))][: n + B]
    y = np.zeros(n + len(h) + B)
    fb = np.zeros(n + len(h) + B)
    for a in range(0, n, B):
        y[a:a + B] = x[a:a + B] + fb[a:a + B]
        if np.max(np.abs(y[a:a + B])) > 1e6:
            y[a:] = np.clip(y[a:], -1e6, 1e6)
            break
        contrib = g * np.convolve(y[a:a + B], h)
        fb[a:a + len(contrib)] += contrib
    return y[:n]


def ring_out(ir, notches: int = 6, depth_db: float = 9.0, q: float = 10.0, fmin: float = 100.0, fmax: float = 8000.0) -> list:
    """Ringing out: find the frequency that would howl first, cut it with a narrow notch, and repeat.  Returns, notch by
    notch, the frequency cut and the maximum stable gain after it."""
    cuts = []
    out = [{"notches": 0, "max_gain_db": feedback(ir, fmin, fmax)["max_gain_db"], "howl_hz": feedback(ir, fmin, fmax)["howl_hz"]}]
    for i in range(notches):
        fb = feedback(ir, fmin, fmax, cuts)
        cuts.append((fb["howl_hz"], depth_db, q))
        after = feedback(ir, fmin, fmax, cuts)
        out.append({"notches": i + 1, "cut_hz": fb["howl_hz"], "max_gain_db": after["max_gain_db"], "howl_hz": after["howl_hz"]})
    return out


def pag_nag(d0: float, d1: float, ds: float, d2: float, nom: int = 1, fsm: float = 6.0) -> dict:
    """Davis's potential and needed acoustic gain (inverse-square only): PAG = 20 log (D0 D1 / Ds D2) - 10 log NOM - FSM;
    D0 talker to listener, D1 microphone to loudspeaker, Ds talker to microphone, D2 loudspeaker to listener; NAG is the
    gain needed for the listener to hear the talker as if from distance EAD (here 1 m)."""
    pag = 20 * math.log10(d0 * d1 / (ds * d2)) - 10 * math.log10(nom) - fsm
    nag = 20 * math.log10(d0 / 1.0)
    return {"pag": pag, "nag": nag}


# --------------------------------------------------------------------------------------------- sources and arrays
def field(sources, f: float, xs, ys, amps=None, delays=None, air: bool = True) -> np.ndarray:
    """The level (dB, re one source at 1 m) of point sources at (x, y) positions, on a grid xs by ys, at frequency f:
    each contributes amp e^{-jk r} / r, delayed by its delay."""
    X, Y = np.meshgrid(np.asarray(xs, float), np.asarray(ys, float))
    k = 2 * np.pi * f / C
    p = np.zeros_like(X, dtype=complex)
    amps = np.ones(len(sources)) if amps is None else np.asarray(amps, float)
    delays = np.zeros(len(sources)) if delays is None else np.asarray(delays, float)
    a_db = air_absorption_db_per_m(f) if air else 0.0
    for (sx, sy), a, d in zip(sources, amps, delays):
        r = np.maximum(np.hypot(X - sx, Y - sy), 0.05)
        p += a * np.exp(-1j * (k * r + 2 * np.pi * f * d)) / r * 10 ** (-a_db * r / 20)
    return 20 * np.log10(np.abs(p) + 1e-12)


def line_array(n: int, spacing: float, top=(0.0, 12.0), splay_deg=None):
    """Element positions hanging down from ``top``: straight (vertical) if ``splay_deg`` is None, otherwise each
    element tilted further by the given angles (a J-shaped, progressively curved array).  Returns positions and each
    element's aiming angle (degrees below horizontal)."""
    pos = [np.array(top, float)]
    ang = [0.0]
    tilt = 0.0
    for i in range(1, n):
        if splay_deg is not None:
            tilt += splay_deg[i - 1]
        a = math.radians(tilt)
        step = np.array([math.sin(a), -math.cos(a)]) * spacing
        pos.append(pos[-1] + step)
        ang.append(tilt)
    return [tuple(p) for p in pos], ang


def directional_field(sources, aims_deg, f: float, xs, ys, width_deg: float = 90.0, air: bool = True, floor_db: float = -20.0):
    """As ``field`` but each element radiates mostly along its aiming direction (a cos^q lobe whose -6 dB width is
    ``width_deg``) above a floor of ``floor_db`` (its side and rear radiation)."""
    X, Y = np.meshgrid(np.asarray(xs, float), np.asarray(ys, float))
    k = 2 * np.pi * f / C
    q = math.log(0.5) / math.log(math.cos(math.radians(width_deg / 2)))
    p = np.zeros_like(X, dtype=complex)
    a_db = air_absorption_db_per_m(f) if air else 0.0
    for (sx, sy), aim in zip(sources, aims_deg):
        dx, dy = X - sx, Y - sy
        r = np.maximum(np.hypot(dx, dy), 0.05)
        ang = np.arctan2(-dy, dx) - math.radians(aim)
        fl = 10 ** (floor_db / 20)
        lobe = fl + (1 - fl) * np.clip(np.cos(ang), 0, None) ** q
        p += lobe * np.exp(-1j * k * r) / r * 10 ** (-a_db * r / 20)
    return 20 * np.log10(np.abs(p) + 1e-12)


def on_axis_levels(sources, f: float, dists, height: float = 1.5, aims_deg=None, width_deg: float = 90.0):  # noqa: D401
    """Level at listener height along the floor, at each distance."""
    if aims_deg is None:
        return field(sources, f, dists, [height])[0]
    return directional_field(sources, aims_deg, f, dists, [height], width_deg)[0]


def cardioid_sub(f, spacing: float = 0.9) -> dict:
    """Two subwoofers, one behind the other ``spacing`` apart, the rear one inverted and delayed by spacing / c: in front
    the two add (exactly in time); behind, the rear one's delayed, inverted sound meets the front one's and cancels."""
    f = np.asarray(f, float)
    k = 2 * np.pi * f / C
    tau = spacing / C
    front = np.abs(1 - np.exp(-1j * (2 * np.pi * f * tau + k * spacing)))        # rear's path is longer by spacing
    back = np.abs(np.exp(-1j * k * spacing) - np.exp(-1j * 2 * np.pi * f * tau))
    return {"front_db": 20 * np.log10(front / 2 + 1e-12), "back_db": 20 * np.log10(back / 2 + 1e-12)}


def delay_time(d_main: float, d_tower: float, temp_c: float = 20.0, haas_ms: float = 10.0) -> float:
    """The delay (s) for a tower ``d_tower`` from the listener when the main system is ``d_main`` away: the main sound's
    extra travel, plus a few ms so the stage arrives first and the ear localizes there (the precedence effect)."""
    c = speed_of_sound(temp_c)
    return (d_main - d_tower) / c + haas_ms / 1000


# --------------------------------------------------------------------------------------------- air
def air_absorption_db_per_m(f, temp_c: float = 20.0, rh: float = 50.0, pa_kpa: float = 101.325):
    """ISO 9613-1 (1993): the attenuation of sound by the atmosphere, dB per metre."""
    f = np.asarray(f, float)
    T = temp_c + 273.15
    T0, T01 = 293.15, 273.16
    pr = pa_kpa / 101.325
    psat = 10 ** (-6.8346 * (T01 / T) ** 1.261 + 4.6151)
    h = rh * psat / pr
    fro = pr * (24 + 4.04e4 * h * (0.02 + h) / (0.391 + h))
    frn = pr * (T / T0) ** -0.5 * (9 + 280 * h * math.exp(-4.170 * ((T / T0) ** (-1 / 3) - 1)))
    a = 8.686 * f ** 2 * (1.84e-11 / pr * (T / T0) ** 0.5 + (T / T0) ** -2.5 * (
        0.01275 * math.exp(-2239.1 / T) / (fro + f ** 2 / fro) + 0.1068 * math.exp(-3352.0 / T) / (frn + f ** 2 / frn)))
    return a


def air_filter(x, distance: float, temp_c: float = 20.0, rh: float = 50.0) -> np.ndarray:
    """Apply the air's absorption over ``distance`` metres to a signal (zero-phase, by FFT)."""
    x = np.asarray(x, float)
    n = len(x)
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = 10 ** (-air_absorption_db_per_m(f, temp_c, rh) * distance / 20)
    return np.fft.irfft(X * (g[:, None] if x.ndim == 2 else g), n, axis=0)


# --------------------------------------------------------------------------------------------- measurement
def transfer_function(x, y, nfft: int = 8192) -> dict:
    """Dual-channel FFT measurement, as Smaart and SysTune do it: average the cross- and auto-spectra over Hann-windowed,
    half-overlapped blocks; H = Sxy / Sxx; coherence |Sxy|^2 / (Sxx Syy); the delay from the impulse response's peak."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    w = np.hanning(nfft)
    Sxx = np.zeros(nfft // 2 + 1)
    Syy = np.zeros(nfft // 2 + 1)
    Sxy = np.zeros(nfft // 2 + 1, dtype=complex)
    for a in range(0, len(x) - nfft, nfft // 2):
        X = np.fft.rfft(w * x[a:a + nfft])
        Y = np.fft.rfft(w * y[a:a + nfft])
        Sxx += np.abs(X) ** 2
        Syy += np.abs(Y) ** 2
        Sxy += np.conj(X) * Y
    H = Sxy / (Sxx + 1e-20)
    coh = np.abs(Sxy) ** 2 / (Sxx * Syy + 1e-20)
    ir = np.fft.irfft(H, nfft)
    return {"f": np.fft.rfftfreq(nfft, 1 / SR), "H": H, "coherence": coh, "ir": ir, "delay_s": float(np.argmax(np.abs(ir)) / SR)}


# --------------------------------------------------------------------------------------------- wireless
def imd3(freqs) -> list:
    """Third-order intermodulation products of a set of carriers: 2 f1 - f2 for every ordered pair, and f1 + f2 - f3
    for every triple."""
    fs = list(freqs)
    out = []
    for i, a in enumerate(fs):
        for j, b in enumerate(fs):
            if i != j:
                out.append(2 * a - b)
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            for k in range(len(fs)):
                if k != i and k != j:
                    out.append(fs[i] + fs[j] - fs[k])
    return out


def plan_channels(lo: float, hi: float, n: int, step: float = 0.025, spacing: float = 0.35, guard: float = 0.1, exclude=()) -> list:
    """Choose up to n carrier frequencies (MHz) between lo and hi on a ``step`` grid, at least ``spacing`` apart, with no
    third-order product of the chosen set within ``guard`` of any of them, greedily from the bottom, avoiding the
    ``exclude`` ranges (occupied TV channels)."""
    grid = np.arange(lo, hi + 1e-9, step)
    chosen: list = []
    for f in grid:
        if any(a - 1e-6 <= f <= b + 1e-6 for a, b in exclude):
            continue
        if any(abs(f - c) < spacing for c in chosen):
            continue
        trial = chosen + [float(f)]
        prods = imd3(trial)
        if any(abs(p - c) < guard for p in prods for c in trial):
            continue
        chosen = trial
        if len(chosen) == n:
            break
    return [round(c, 3) for c in chosen]


# --------------------------------------------------------------------------------------------- intelligibility and dose
OCTAVES = [125, 250, 500, 1000, 2000, 4000, 8000]
MOD_F = [0.63, 0.8, 1.0, 1.25, 1.6, 2.0, 2.5, 3.15, 4.0, 5.0, 6.3, 8.0, 10.0, 12.5]
MALE_W = [0.085, 0.127, 0.230, 0.233, 0.309, 0.224, 0.173]       # IEC 60268-16 (2003) male octave weights (alpha)


def mtf(T: float, snr_db: float):
    """Houtgast and Steeneken's modulation transfer for an exponential decay of reverberation time T and a steady
    noise: m(F) = [1 + (2 pi F T / 13.8)^2]^(-1/2) / (1 + 10^(-SNR/10))."""
    F = np.asarray(MOD_F, float)
    return 1 / np.sqrt(1 + (2 * np.pi * F * T / 13.8) ** 2) / (1 + 10 ** (-snr_db / 10))


def sti(T: float, snr_db: float) -> float:
    """The speech transmission index, with the same T and SNR in every octave: each m becomes an apparent SNR, clipped to
    +-15 dB, averaged, and mapped to 0..1; then weighted across octaves (equal here, so the weights sum out)."""
    m = np.clip(mtf(T, snr_db), 1e-6, 1 - 1e-6)
    snr_app = np.clip(10 * np.log10(m / (1 - m)), -15, 15)
    ti = (snr_app + 15) / 30
    return float(np.mean(ti))


def allowed_hours(level_dba: float, criterion: float = 85.0, exchange: float = 3.0) -> float:
    return 8.0 / 2 ** ((level_dba - criterion) / exchange)


def dose(levels_dba, hours) -> float:
    """Noise dose, per cent: the sum of each exposure's time over the time allowed at its level."""
    return float(100 * sum(t / allowed_hours(L) for L, t in zip(levels_dba, hours)))
