"""Monochord's nonlinear and time-varying effects (Part 50 of *Music, Built*): distortion, dynamics, time and pitch.

    shape(x, kind, drive)                  memoryless waveshapers: hard clip, tanh, a cubic soft clip
    chebyshev(n, x), cheb_shaper(amps)     T_n(cos t) = cos(n t): a shaper whose harmonics are exactly ``amps``
    harmonics(y, f0, sr, count)            levels of the first harmonics of a periodic signal, dB re the fundamental
    adaa_tanh(x, drive)                    first-order antiderivative antialiasing for tanh
    compressor(x, sr, ...)                 Giannoulis, Massberg and Reiss's feedforward design: a gain computer with a soft
                                           knee, a smoothed level detector with attack and release
    static_curve(...)                      the gain computer's input-output curve in dB
    gate(x, sr, ...)                       a noise gate (a downward expander with a large ratio)
    ola_stretch(x, factor)                 overlap-add time stretching (windows moved, not re-phased)
    pv_stretch(x, factor)                  the phase vocoder (Flanagan and Golden 1966), with Laroche and Dolson's
                                           identity phase locking
    yin(x, sr, ...)                        de Cheveigne and Kawahara's YIN pitch estimate, frame by frame
    psola(x, sr, f0_track, ratio_track)    pitch-synchronous overlap-add: shift pitch, keep timing and formants
    correct(f0, scale, speed)              a pitch corrector's target: the nearest note of a scale, approached at ``speed``
    vocoder(mod, car, sr, bands)           Dudley's channel vocoder: the modulator's band envelopes imposed on the carrier
    ring(x, sr, f)                         ring modulation: multiply by a sine

No manim here.  Checked in ``tests/music/test_dynamics.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, sosfilt

# --------------------------------------------------------------------------------------------- distortion


def shape(x, kind: str = "tanh", drive: float = 1.0) -> np.ndarray:
    x = np.asarray(x, float) * drive
    if kind == "hard":
        return np.clip(x, -1.0, 1.0)
    if kind == "tanh":
        return np.tanh(x)
    if kind == "cubic":
        y = np.clip(x, -1.0, 1.0)
        return 1.5 * y - 0.5 * y ** 3
    raise ValueError(kind)


def chebyshev(n: int, x) -> np.ndarray:
    """T_n by the recurrence T_{k+1} = 2x T_k - T_{k-1}."""
    x = np.asarray(x, float)
    t0, t1 = np.ones_like(x), x
    if n == 0:
        return t0
    for _ in range(n - 1):
        t0, t1 = t1, 2 * x * t1 - t0
    return t1


def cheb_shaper(amps, x) -> np.ndarray:
    """sum_k amps[k] T_{k+1}(x): fed a full-scale cosine, it outputs harmonic k+1 at amplitude amps[k], exactly."""
    x = np.clip(np.asarray(x, float), -1.0, 1.0)
    return sum(a * chebyshev(k + 1, x) for k, a in enumerate(amps))


def harmonics(y, f0: float, sr: float, count: int = 8) -> list[float]:
    """Levels of harmonics 1..count in dB relative to the fundamental (Hann window, peak bins)."""
    y = np.asarray(y, float)
    w = np.hanning(len(y))
    Y = np.abs(np.fft.rfft(y * w))
    f = np.fft.rfftfreq(len(y), 1 / sr)
    out = []
    for k in range(1, count + 1):
        i = int(round(k * f0 * len(y) / sr))
        if i + 3 >= len(Y):
            break
        out.append(float(Y[max(i - 3, 0):i + 4].max()))
    ref = out[0]
    return [float(20 * np.log10(v / ref + 1e-12)) for v in out]


def alias_energy(y, f0: float, sr: float, tol: float = 2.0) -> float:
    """Share of a signal's energy (dB) that is NOT at a harmonic of f0: for a shaped sine, that is aliasing."""
    y = np.asarray(y, float)
    w = np.hanning(len(y))
    P = np.abs(np.fft.rfft(y * w)) ** 2
    f = np.fft.rfftfreq(len(y), 1 / sr)
    k = np.round(f / f0)
    on = np.abs(f - k * f0) < tol * sr / len(y) * 3
    return float(10 * np.log10(P[~on].sum() / P.sum() + 1e-30))


def adaa_tanh(x, drive: float = 1.0) -> np.ndarray:
    """y[n] = (F(u[n]) - F(u[n-1])) / (u[n] - u[n-1]) with F = log cosh, the antiderivative of tanh (Parker, Zavalishin
    and Le Bivic 2016): the shaper applied to the straight line between samples, averaged; aliasing falls."""
    u = np.asarray(x, float) * drive
    F = np.log(np.cosh(u))
    out = np.empty(len(u))
    out[0] = math.tanh(u[0])
    du = np.diff(u)
    small = np.abs(du) < 1e-6
    mid = 0.5 * (u[1:] + u[:-1])
    val = np.where(small, np.tanh(mid), (F[1:] - F[:-1]) / np.where(small, 1.0, du))
    out[1:] = val
    return out


# --------------------------------------------------------------------------------------------- dynamics


def static_curve(level_db, threshold: float = -20.0, ratio: float = 4.0, knee: float = 6.0) -> np.ndarray:
    """The gain computer: below threshold - knee/2, out = in; above threshold + knee/2, out = T + (in - T) / R; a
    quadratic in between (Giannoulis, Massberg and Reiss 2012, eq. 4)."""
    x = np.asarray(level_db, float)
    y = x.copy()
    lo, hi = threshold - knee / 2, threshold + knee / 2
    over = x > hi
    y[over] = threshold + (x[over] - threshold) / ratio
    mid = (x >= lo) & (x <= hi)
    if knee > 0:
        y[mid] = x[mid] + (1 / ratio - 1) * (x[mid] - lo) ** 2 / (2 * knee)
    return y


def compressor(x, sr: float, threshold: float = -20.0, ratio: float = 4.0, knee: float = 6.0, attack_ms: float = 5.0,
               release_ms: float = 120.0, makeup: float = 0.0, sidechain=None) -> dict:
    """Feedforward compression in the log domain: a peak level (instant rise, 30 ms fall) -> gain computer -> smoothed gain reduction (a branched
    one-pole: fast when the reduction grows, slow when it shrinks) -> applied.  ``sidechain`` drives the detector
    instead of the input (ducking)."""
    x = np.asarray(x, float)
    det = np.abs(x if sidechain is None else np.asarray(sidechain, float))
    pk = np.empty(len(det))                                          # a peak envelope: instant rise, 30 ms fall
    rel = math.exp(-1 / (0.03 * sr))
    e = 0.0
    for n in range(len(det)):
        e = det[n] if det[n] > e else rel * e + (1 - rel) * det[n]
        pk[n] = e
    lvl = 20 * np.log10(pk + 1e-9)
    gr_target = lvl - static_curve(lvl, threshold, ratio, knee)        # dB of reduction wanted (>= 0)
    aa = math.exp(-1 / (attack_ms * 1e-3 * sr))
    ar = math.exp(-1 / (release_ms * 1e-3 * sr))
    gr = np.empty(len(x))
    g = 0.0
    for n in range(len(x)):
        t = gr_target[n]
        g = aa * g + (1 - aa) * t if t > g else ar * g + (1 - ar) * t
        gr[n] = g
    gain = 10 ** ((makeup - gr) / 20)
    return {"y": x * gain, "gr_db": gr}


def gate(x, sr: float, threshold: float = -45.0, ratio: float = 10.0, attack_ms: float = 1.0, release_ms: float = 80.0) -> np.ndarray:
    """A downward expander: below the threshold, each dB under becomes ``ratio`` dB under."""
    x = np.asarray(x, float)
    lvl = 20 * np.log10(np.abs(x) + 1e-9)
    env = np.empty(len(x))
    e = -120.0
    aa = math.exp(-1 / (attack_ms * 1e-3 * sr))
    ar = math.exp(-1 / (release_ms * 1e-3 * sr))
    for n in range(len(x)):
        e = aa * e + (1 - aa) * lvl[n] if lvl[n] > e else ar * e + (1 - ar) * lvl[n]
        env[n] = e
    red = np.where(env < threshold, (env - threshold) * (ratio - 1), 0.0)
    return x * 10 ** (red / 20)


def crest_db(x) -> float:
    x = np.asarray(x, float)
    return float(20 * np.log10(np.max(np.abs(x)) / (np.sqrt(np.mean(x ** 2)) + 1e-12)))


def short_term_levels(x, sr: float, win_ms: float = 50.0) -> np.ndarray:
    x = np.asarray(x, float)
    w = int(win_ms * sr / 1000)
    return np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + w] ** 2)) + 1e-9) for i in range(0, len(x) - w, w)])


# --------------------------------------------------------------------------------------------- time and pitch


def ola_stretch(x, factor: float, n: int = 2048, hop_out: int = 512) -> np.ndarray:
    """Overlap-add: read windows every hop_out / factor samples, write them every hop_out.  Phases are not adjusted, so
    the pieces of a steady tone add out of step: the sound warbles."""
    x = np.asarray(x, float)
    w = np.hanning(n)
    hop_in = hop_out / factor
    frames = int((len(x) - n) / hop_in)
    out = np.zeros(frames * hop_out + n)
    norm = np.zeros_like(out)
    for k in range(frames):
        a = int(round(k * hop_in))
        out[k * hop_out:k * hop_out + n] += x[a:a + n] * w
        norm[k * hop_out:k * hop_out + n] += w
    return out / np.maximum(norm, 1e-3)


def pv_stretch(x, factor: float, n: int = 2048, hop_out: int = 256, lock: bool = True) -> np.ndarray:
    """The phase vocoder: analyse with hop_out / factor, resynthesize with hop_out, advancing each bin's phase by its
    measured instantaneous frequency.  With ``lock``, bins near a spectral peak take the peak's phase advance
    (Laroche and Dolson 1999), so the partials stay coherent."""
    x = np.asarray(x, float)
    w = np.hanning(n)
    hop_in = hop_out / factor
    frames = int((len(x) - n) / hop_in)
    omega = 2 * np.pi * np.arange(n // 2 + 1) / n
    out = np.zeros(frames * hop_out + n)
    norm = np.zeros_like(out)
    prev_phase = None
    phase_acc = None
    for k in range(frames):
        a = k * hop_in
        i = int(a)
        seg = x[i:i + n]
        if len(seg) < n:
            break
        X = np.fft.rfft(seg * w)
        mag, ph = np.abs(X), np.angle(X)
        if prev_phase is None:
            phase_acc = ph.copy()
        else:
            dphi = ph - prev_phase - omega * hop_in
            dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
            inst = omega + dphi / hop_in
            if lock:
                peaks = np.flatnonzero((mag[1:-1] > mag[:-2]) & (mag[1:-1] >= mag[2:])) + 1
                adv = inst * hop_out
                new = phase_acc + adv
                if len(peaks):
                    owner = peaks[np.argmin(np.abs(np.arange(len(mag))[:, None] - peaks[None, :]), axis=1)]
                    new = (phase_acc[owner] + adv[owner]) + (ph - ph[owner])
                phase_acc = new
            else:
                phase_acc = phase_acc + inst * hop_out
        prev_phase = ph
        y = np.fft.irfft(mag * np.exp(1j * phase_acc), n) * w
        out[k * hop_out:k * hop_out + n] += y
        norm[k * hop_out:k * hop_out + n] += w ** 2
    return out / np.maximum(norm, 1e-3)


def yin(x, sr: float, fmin: float = 70.0, fmax: float = 1000.0, frame: int = 2048, hop: int = 256, thresh: float = 0.12):
    """YIN: the cumulative-mean-normalised difference function per frame; the first dip below ``thresh`` (refined by
    parabolic interpolation) is the period.  Returns times, f0 (0 when unvoiced) and the dip's depth."""
    x = np.asarray(x, float)
    tmin, tmax = int(sr / fmax), int(sr / fmin)
    times, f0s, conf = [], [], []
    floor = 1e-3 * np.max(np.abs(x)) if len(x) else 0.0
    for start in range(0, len(x) - frame - tmax, hop):
        seg = x[start:start + frame + tmax]
        if np.sqrt(np.mean(seg[:frame] ** 2)) < floor:
            times.append((start + frame / 2) / sr)
            f0s.append(0.0)
            conf.append(1.0)
            continue
        d = np.array([np.sum((seg[:frame] - seg[tau:tau + frame]) ** 2) for tau in range(tmax + 1)])
        cm = np.ones_like(d)
        cs = np.cumsum(d[1:])
        cm[1:] = d[1:] * np.arange(1, len(d)) / np.maximum(cs, 1e-12)
        tau = None
        for t in range(tmin, tmax):
            if cm[t] < thresh and cm[t] <= cm[t + 1]:
                tau = t
                break
        if tau is None:
            f, c = 0.0, float(cm[tmin:tmax].min())
        else:
            a, b, cc = cm[tau - 1], cm[tau], cm[tau + 1]
            den = a - 2 * b + cc
            shift = 0.5 * (a - cc) / den if den != 0 else 0.0
            f, c = sr / (tau + shift), float(b)
        times.append((start + frame / 2) / sr)
        f0s.append(f)
        conf.append(c)
    return np.array(times), np.array(f0s), np.array(conf)


def cents(f, ref: float = 440.0):
    return 1200 * np.log2(np.asarray(f, float) / ref)


def correct(f0, times, scale=(0, 2, 4, 5, 7, 9, 11), tonic_hz: float = 261.6256, speed_ms: float = 0.0) -> np.ndarray:
    """The target pitch for each frame: the nearest note of ``scale`` above ``tonic_hz`` (in any octave), approached by
    a one-pole glide with time constant ``speed_ms`` (0: instantly)."""
    f0 = np.asarray(f0, float)
    out = np.zeros_like(f0)
    cur = None
    dt = np.diff(times).mean() if len(times) > 1 else 0.01
    a = math.exp(-dt * 1000 / speed_ms) if speed_ms > 0 else 0.0
    notes = np.array([s + 12 * o for o in range(-3, 4) for s in scale], float)
    for i, f in enumerate(f0):
        if f <= 0:
            out[i] = 0.0
            cur = None
            continue
        c = 12 * math.log2(f / tonic_hz)
        tgt = notes[np.argmin(np.abs(notes - c))]
        cur = tgt if cur is None or a == 0 else a * cur + (1 - a) * tgt
        out[i] = tonic_hz * 2 ** (cur / 12)
    return out


def psola(x, sr: float, times, f0, ratio) -> np.ndarray:
    """Pitch-synchronous overlap-add (Moulines and Charpentier 1990).  Grains two periods long, centred on the analysis
    pitch marks (one per period of ``f0``), are laid down at synthesis marks spaced by period / ratio: the pitch moves,
    the timing and the formants (each grain's spectral envelope) stay."""
    x = np.asarray(x, float)
    times, f0, ratio = map(lambda a: np.asarray(a, float), (times, f0, ratio))

    def at(arr, t):
        return float(np.interp(t, times, arr))

    marks = []
    t = times[0]
    while t < times[-1]:
        f = at(f0, t)
        if f <= 0:
            t += 0.005
            continue
        marks.append(t)
        t += 1.0 / f
    out = np.zeros(len(x) + sr)
    if not marks:
        return x.copy()
    ts = marks[0]
    while ts < marks[-1]:
        k = int(np.argmin(np.abs(np.array(marks) - ts)))
        ta = marks[k]
        f = at(f0, ta)
        if f <= 0:
            ts += 0.005
            continue
        P = int(sr / f)
        c = int(ta * sr)
        if c - P < 0 or c + P >= len(x):
            ts += 1.0 / (f * max(at(ratio, ta), 0.25))
            continue
        g = x[c - P:c + P] * np.hanning(2 * P)
        o = int(ts * sr)
        out[o - P:o + P] += g
        ts += 1.0 / (f * max(at(ratio, ta), 0.25))
    return out[: len(x)]


def vocoder(mod, car, sr: float, bands: int = 16, lo: float = 100.0, hi: float = 8000.0, env_ms: float = 15.0) -> dict:
    """A channel vocoder (Dudley 1939): split modulator and carrier into the same band-pass bands; follow each
    modulator band's envelope; multiply the carrier's band by it; sum."""
    mod, car = np.asarray(mod, float), np.asarray(car, float)
    n = min(len(mod), len(car))
    edges = np.geomspace(lo, hi, bands + 1)
    a = math.exp(-1 / (env_ms * 1e-3 * sr))
    out = np.zeros(n)
    envs = []
    for k in range(bands):
        sos = butter(2, [edges[k], edges[k + 1]], btype="band", fs=sr, output="sos")
        mb = sosfilt(sos, mod[:n])
        cb = sosfilt(sos, car[:n])
        env = sosfilt(butter(1, 1 / (2 * np.pi * env_ms * 1e-3), fs=sr, output="sos"), np.abs(mb))
        envs.append(env[::480])
        out += cb * env
    out /= np.max(np.abs(out)) + 1e-12
    return {"y": out, "edges": edges.tolist(), "envs": np.array(envs).tolist()}


def ring(x, sr: float, f: float) -> np.ndarray:
    x = np.asarray(x, float)
    return x * np.sin(2 * np.pi * f * np.arange(len(x)) / sr)
