"""Monochord's effects rack (Part 49 of *Music, Built*): filters, delays and reverberation, all as delay and addition.

    convolve(x, h)                         y = x * h (by FFT)
    biquad(kind, f0, sr, q, gain_db)       RBJ 'cookbook' second-order sections: lowpass, highpass, bandpass, notch, peak,
                                           lowshelf, highshelf -> (b, a)
    response(b, a, sr, freqs)              magnitude (dB) and phase of a filter; poles and zeros
    butter2_bilinear(fc, sr)               a second-order Butterworth low-pass from its analog prototype, by the bilinear
                                           transform with prewarping
    allpass_chain(x, coeffs)               first-order all-passes in series (dispersion)
    comb_ff, comb_fb                       feedforward and feedback combs
    flanger, chorus, phaser                modulated delays and all-pass notches
    room_ir(...)                           a shoebox room's impulse response by the image-source method (Allen and Berkley)
    sabine, eyring                         reverberation time from volume, surface and absorption
    edc(ir), rt60(ir, sr)                  Schroeder's backward-integrated energy decay and the time to fall 60 dB
    ess(...), ess_inverse(...)             Farina's exponential sine sweep and its inverse filter
    schroeder(x, sr)                       Schroeder's 1962 reverberator: four combs and two all-passes
    fdn(x, sr, delays, t60)                a feedback delay network (Jot and Chaigne) with a Hadamard matrix
    plate_ir(...)                          a steel plate (an EMT 140's size) by finite differences
    spring_ir(...)                         a spring as a dispersive loop of all-passes

No manim here.  Checked in ``tests/music/test_effects.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import fftconvolve, freqz, lfilter

C_AIR = 343.0


def convolve(x, h) -> np.ndarray:
    return fftconvolve(np.asarray(x, float), np.asarray(h, float))


# --------------------------------------------------------------------------------------------- filters


def biquad(kind: str, f0: float, sr: float, q: float = 0.7071, gain_db: float = 0.0):
    """Robert Bristow-Johnson's cookbook formulas; returns normalised (b, a) with a[0] = 1."""
    A = 10 ** (gain_db / 40)
    w = 2 * math.pi * f0 / sr
    cw, sw = math.cos(w), math.sin(w)
    al = sw / (2 * q)
    if kind == "lowpass":
        b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "highpass":
        b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "bandpass":
        b = [al, 0.0, -al]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "notch":
        b = [1.0, -2 * cw, 1.0]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "peak":
        b = [1 + al * A, -2 * cw, 1 - al * A]
        a = [1 + al / A, -2 * cw, 1 - al / A]
    elif kind in ("lowshelf", "highshelf"):
        s = 1 if kind == "lowshelf" else -1
        sq = 2 * math.sqrt(A) * al
        b = [A * ((A + 1) - s * (A - 1) * cw + sq), s * 2 * A * ((A - 1) - s * (A + 1) * cw), A * ((A + 1) - s * (A - 1) * cw - sq)]
        a = [(A + 1) + s * (A - 1) * cw + sq, -s * 2 * ((A - 1) + s * (A + 1) * cw), (A + 1) + s * (A - 1) * cw - sq]
    else:
        raise ValueError(kind)
    b, a = np.array(b) / a[0], np.array(a) / a[0]
    return b, a


def response(b, a, sr: float, freqs) -> dict:
    w, h = freqz(b, a, worN=np.asarray(freqs, float), fs=sr)
    return {"f": w.tolist(), "db": (20 * np.log10(np.abs(h) + 1e-12)).tolist(), "phase": np.unwrap(np.angle(h)).tolist(),
            "zeros": [[float(z.real), float(z.imag)] for z in np.roots(b)], "poles": [[float(p.real), float(p.imag)] for p in np.roots(a)]}


def group_delay(b, a, sr: float, freqs) -> np.ndarray:
    """-d(phase)/d(omega), in seconds, by a finite difference of the unwrapped phase."""
    f = np.asarray(freqs, float)
    _, h = freqz(b, a, worN=f, fs=sr)
    ph = np.unwrap(np.angle(h))
    return -np.gradient(ph, 2 * np.pi * f)


def butter2_bilinear(fc: float, sr: float):
    """H(s) = 1 / (s^2 + sqrt2 s + 1) at cutoff wc, with wc prewarped to 2 sr tan(pi fc / sr), mapped by s = 2 sr (1 - z^-1)/(1 + z^-1)."""
    wc = 2 * sr * math.tan(math.pi * fc / sr)
    K = 2 * sr / wc
    a0 = K * K + math.sqrt(2) * K + 1
    b = np.array([1.0, 2.0, 1.0]) / a0
    a = np.array([a0, 2 - 2 * K * K, K * K - math.sqrt(2) * K + 1]) / a0
    return b, a


def onepole(x, a: float) -> np.ndarray:
    """y[n] = (1 - a) x[n] + a y[n-1]: the simplest low-pass, one pole at z = a."""
    return lfilter([1 - a], [1, -a], np.asarray(x, float))


def allpass1(x, c: float) -> np.ndarray:
    """H(z) = (c + z^-1) / (1 + c z^-1): unit gain at every frequency, frequency-dependent delay."""
    return lfilter([c, 1.0], [1.0, c], np.asarray(x, float))


def allpass_chain(x, coeffs) -> np.ndarray:
    y = np.asarray(x, float)
    for c in coeffs:
        y = allpass1(y, c)
    return y


# --------------------------------------------------------------------------------------------- delays


def comb_ff(x, delay: int, g: float) -> np.ndarray:
    """y[n] = x[n] + g x[n - D]: notches at odd multiples of sr / 2D (for g > 0)."""
    b = np.zeros(delay + 1)
    b[0], b[delay] = 1.0, g
    return lfilter(b, [1.0], np.asarray(x, float))


def comb_fb(x, delay: int, g: float) -> np.ndarray:
    """y[n] = x[n] + g y[n - D]: peaks at multiples of sr / D, a pitch."""
    a = np.zeros(delay + 1)
    a[0], a[delay] = 1.0, -g
    return lfilter([1.0], a, np.asarray(x, float))


def _vdelay(x, d):
    """Read x at fractional delays d[n] (samples), by linear interpolation."""
    n = np.arange(len(x)) - d
    i = np.floor(n).astype(int)
    f = n - i
    i0 = np.clip(i, 0, len(x) - 1)
    i1 = np.clip(i + 1, 0, len(x) - 1)
    y = (1 - f) * x[i0] + f * x[i1]
    y[i < 0] = 0.0
    return y


def flanger(x, sr: float, depth_ms: float = 3.0, base_ms: float = 1.0, rate: float = 0.25, mix: float = 0.7, feedback: float = 0.5) -> np.ndarray:
    """A comb whose delay sweeps between ``base_ms`` and ``base_ms + depth_ms`` (feedback applied in a loop)."""
    x = np.asarray(x, float)
    t = np.arange(len(x)) / sr
    d = (base_ms + depth_ms * 0.5 * (1 - np.cos(2 * np.pi * rate * t))) * sr / 1000
    y = np.zeros(len(x))
    buf = np.zeros(len(x))
    for n in range(len(x)):
        p = n - d[n]
        i = int(math.floor(p))
        f = p - i
        dl = 0.0
        if i >= 0:
            dl = (1 - f) * buf[i] + (f * buf[i + 1] if i + 1 < n else 0.0)
        buf[n] = x[n] + feedback * dl
        y[n] = x[n] + mix * dl
    return y / (1 + mix)


def chorus(x, sr: float, voices: int = 3, base_ms: float = 20.0, depth_ms: float = 4.0, rate: float = 0.6, seed: int = 0) -> np.ndarray:
    """Several copies, each delayed by its own slowly wandering 15-30 ms: detuned doublings."""
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    t = np.arange(len(x)) / sr
    y = x.copy()
    for v in range(voices):
        ph = rng.uniform(0, 2 * np.pi)
        r = rate * (0.8 + 0.4 * rng.random())
        d = (base_ms + depth_ms * np.sin(2 * np.pi * r * t + ph)) * sr / 1000
        y += 0.7 * _vdelay(x, d)
    return y / (1 + 0.7 * voices)


def phaser(x, sr: float, stages: int = 6, lo: float = 300.0, hi: float = 3000.0, rate: float = 0.3, mix: float = 1.0) -> np.ndarray:
    """All-passes whose break frequency sweeps between lo and hi; summed with the dry signal, their phase shifts make
    moving notches (stages/2 of them)."""
    x = np.asarray(x, float)
    t = np.arange(len(x)) / sr
    fc = lo * (hi / lo) ** (0.5 - 0.5 * np.cos(2 * np.pi * rate * t))
    w = np.tan(np.pi * fc / sr)
    c = (w - 1) / (w + 1)
    y = x.copy()
    for _ in range(stages):
        z = np.zeros(len(x))
        xm1 = ym1 = 0.0
        for n in range(len(x)):
            v = c[n] * y[n] + xm1 - c[n] * ym1
            xm1, ym1 = y[n], v
            z[n] = v
        y = z
    return (x + mix * y) / (1 + mix)


# --------------------------------------------------------------------------------------------- rooms


def room_ir(dims, src, mic, alpha: float, sr: float = 48000, seconds: float = 1.0, air: bool = True) -> np.ndarray:
    """Allen and Berkley's image-source method for a rectangular room with every wall absorbing a fraction ``alpha`` of
    the energy (pressure reflection sqrt(1 - alpha)).  Each image arrives after r / c with amplitude beta^k / r; with
    ``air``, a gentle loss with distance stands in for air and wall absorption at high frequencies.  The result is
    high-passed at 40 Hz, as by a real loudspeaker and microphone."""
    L = np.array(dims, float)
    s = np.array(src, float)
    m = np.array(mic, float)
    beta = math.sqrt(1 - alpha)
    n_len = int(seconds * sr)
    h = np.zeros(n_len + 2)
    rmax = C_AIR * seconds
    N = [int(math.ceil(rmax / L[i])) + 1 for i in range(3)]
    ny = np.arange(-N[1], N[1] + 1)
    nz = np.arange(-N[2], N[2] + 1)
    Ny, Nz = np.meshgrid(ny, nz, indexing="ij")
    for nx in range(-N[0], N[0] + 1):
        for px in (0, 1):
            ix = (1 - 2 * px) * s[0] + 2 * nx * L[0] - m[0]
            kx = abs(2 * nx - px)
            for py in (0, 1):
                iy = (1 - 2 * py) * s[1] + 2 * Ny * L[1] - m[1]
                ky = np.abs(2 * Ny - py)
                for pz in (0, 1):
                    iz = (1 - 2 * pz) * s[2] + 2 * Nz * L[2] - m[2]
                    kz = np.abs(2 * Nz - pz)
                    r = np.sqrt(ix * ix + iy * iy + iz * iz)
                    ok = r < rmax
                    if not ok.any():
                        continue
                    rr = r[ok]
                    k = (kx + ky + kz)[ok]
                    amp = beta ** k / np.maximum(rr, 0.1)
                    tt = rr / C_AIR * sr
                    i0 = np.floor(tt).astype(int)
                    f = tt - i0
                    np.add.at(h, i0, amp * (1 - f))
                    np.add.at(h, i0 + 1, amp * f)
    h = h[:n_len]
    if air:
        # a one-pole low-pass that closes slowly with time: later sound has travelled further and lost its top
        out = np.zeros(n_len)
        seg = int(0.05 * sr)
        for a0 in range(0, n_len, seg):
            t = a0 / sr
            a = min(0.15 + 0.6 * t, 0.85)
            blk = h[a0:a0 + seg]
            out[a0:a0 + len(blk)] = lfilter([1 - a], [1, -a], blk)
        h = out
    # no loudspeaker or microphone passes DC: a gentle high-pass at 40 Hz, as a measurement chain would apply
    from scipy.signal import butter, sosfilt
    h = sosfilt(butter(2, 40.0, btype="high", fs=sr, output="sos"), h)
    return h / np.max(np.abs(h))


def sabine(dims, alpha: float) -> float:
    L = np.array(dims, float)
    V = L.prod()
    S = 2 * (L[0] * L[1] + L[1] * L[2] + L[0] * L[2])
    return float(0.161 * V / (S * alpha))


def eyring(dims, alpha: float) -> float:
    L = np.array(dims, float)
    V = L.prod()
    S = 2 * (L[0] * L[1] + L[1] * L[2] + L[0] * L[2])
    return float(0.161 * V / (-S * math.log(1 - alpha)))


def edc(ir) -> np.ndarray:
    """Schroeder's energy decay curve: the energy still to come, in dB relative to the total."""
    e = np.cumsum(np.asarray(ir, float)[::-1] ** 2)[::-1]
    return 10 * np.log10(e / e[0] + 1e-30)


def rt60(ir, sr: float, lo: float = -5.0, hi: float = -25.0) -> float:
    """Fit a line to the energy decay between ``lo`` and ``hi`` dB (T20 by default) and extrapolate to 60 dB."""
    d = edc(ir)
    t = np.arange(len(d)) / sr
    k = (d <= lo) & (d >= hi)
    slope, _ = np.polyfit(t[k], d[k], 1)
    return float(-60.0 / slope)


def ess(f1: float, f2: float, seconds: float, sr: float) -> np.ndarray:
    """Farina's exponential sweep: instantaneous frequency f1 (f2/f1)^(t/T)."""
    t = np.arange(int(seconds * sr)) / sr
    R = math.log(f2 / f1)
    return np.sin(2 * np.pi * f1 * seconds / R * (np.exp(t * R / seconds) - 1))


def ess_inverse(f1: float, f2: float, seconds: float, sr: float) -> np.ndarray:
    """The sweep reversed in time and tilted by -6 dB an octave, so that sweep * inverse is (nearly) an impulse."""
    t = np.arange(int(seconds * sr)) / sr
    R = math.log(f2 / f1)
    inv = ess(f1, f2, seconds, sr)[::-1] * np.exp(-t * R / seconds)
    peak = np.max(np.abs(convolve(ess(f1, f2, seconds, sr), inv)))
    return inv / peak


# --------------------------------------------------------------------------------------------- artificial reverberation

SCHROEDER_COMBS_MS = (29.7, 37.1, 41.1, 43.7)
SCHROEDER_ALLPASS = ((5.0, 0.7), (1.7, 0.7))


def schroeder(x, sr: float, t60: float = 2.0) -> np.ndarray:
    """Four feedback combs in parallel, gains set for ``t60``, then two all-passes in series (Schroeder 1962)."""
    x = np.asarray(x, float)
    y = np.zeros(len(x))
    for ms in SCHROEDER_COMBS_MS:
        D = int(round(ms * sr / 1000))
        g = 10 ** (-3 * D / (sr * t60))
        y += comb_fb(x, D, g)
    y /= len(SCHROEDER_COMBS_MS)
    for ms, g in SCHROEDER_ALLPASS:
        D = int(round(ms * sr / 1000))
        b = np.zeros(D + 1)
        a = np.zeros(D + 1)
        b[0], b[D] = -g, 1.0
        a[0], a[D] = 1.0, -g
        y = lfilter(b, a, y)
    return y


def hadamard(n: int) -> np.ndarray:
    H = np.array([[1.0]])
    while H.shape[0] < n:
        H = np.block([[H, H], [H, -H]])
    return H / math.sqrt(n)


FDN_MS = (29.3, 34.7, 41.1, 47.9, 53.3, 61.7, 67.9, 73.1)


def fdn(x, sr: float, t60: float = 2.0, delays_ms=FDN_MS, damping: float = 0.3) -> np.ndarray:
    """A feedback delay network: N delay lines mixed through an orthogonal (Hadamard) matrix and fed back; each line's
    gain 10^(-3 D / (sr t60)) makes every loop decay by 60 dB in ``t60`` seconds.  A one-pole low-pass in each loop
    (``damping``) makes the highs die sooner, as in a real hall."""
    x = np.asarray(x, float)
    D = [int(round(ms * sr / 1000)) for ms in delays_ms]
    N = len(D)
    A = hadamard(N)
    g = np.array([10 ** (-3 * d / (sr * t60)) for d in D])
    bufs = [np.zeros(d) for d in D]
    idx = [0] * N
    lp = np.zeros(N)
    y = np.zeros(len(x))
    for n in range(len(x)):
        outs = np.array([bufs[i][idx[i]] for i in range(N)])
        lp = (1 - damping) * outs + damping * lp
        y[n] = outs.sum() / N
        fb = A @ (g * lp)
        for i in range(N):
            bufs[i][idx[i]] = x[n] + fb[i]
            idx[i] = (idx[i] + 1) % D[i]
    return y


def echo_density(ir, sr: float, window_ms: float = 20.0) -> np.ndarray:
    """Abel and Huang's normalised echo density: the share of samples in a window outside one standard deviation,
    divided by the Gaussian's 0.3173 (1 means as dense as noise)."""
    ir = np.asarray(ir, float)
    w = int(window_ms * sr / 1000)
    out = []
    for i in range(0, len(ir) - w, w // 2):
        seg = ir[i:i + w]
        s = seg.std()
        out.append(float(np.mean(np.abs(seg) > s) / 0.3173) if s > 0 else 0.0)
    return np.array(out)


# --------------------------------------------------------------------------------------------- plates and springs

STEEL = {"E": 2.0e11, "rho": 7850.0, "nu": 0.3}


def plate_ir(lx: float = 2.0, ly: float = 1.0, thickness: float = 0.0005, sr: float = 48000, seconds: float = 2.0,
             t60: float = 3.0, hf: float = 1.4e-4, drive=(0.37, 0.43), pick=(0.71, 0.61), mu_target: float = 0.24) -> dict:
    """A simply supported steel plate, struck at ``drive`` and listened to at ``pick`` (fractions of the sides), by an
    explicit finite-difference scheme for u_tt = -k^2 D4 u - 2 s0 u_t + 2 s1 D2 u_t (Bilbao's frequency-dependent loss).
    The grid spacing is set by the scheme's stability: mu = k dt / h^2 <= 1/4.  Loss: sigma(omega) = s0 + s1 omega / kappa,
    so ``t60`` holds at the lowest frequencies and ``hf`` = 1.4e-4 shortens 4 kHz to about a second."""
    E, rho, nu = STEEL["E"], STEEL["rho"], STEEL["nu"]
    kap = math.sqrt(E * thickness ** 2 / (12 * rho * (1 - nu ** 2)))
    dt = 1.0 / sr
    h = math.sqrt(kap * dt / mu_target)
    nx, ny = int(lx / h), int(ly / h)
    h = lx / nx
    mu = kap * dt / h ** 2
    s0 = 3 * math.log(10) / t60
    s1 = hf
    u0 = np.zeros((nx + 1, ny + 1))
    u1 = np.zeros_like(u0)
    di, dj = int(drive[0] * nx), int(drive[1] * ny)
    pi_, pj = int(pick[0] * nx), int(pick[1] * ny)
    u1[di, dj] = 1.0 / h ** 2 * dt ** 2

    def lap(u):
        L = np.zeros_like(u)
        L[1:-1, 1:-1] = u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1]
        # simply supported edges: u = 0 and the Laplacian = 0 there (odd mirror)
        return L

    steps = int(seconds * sr)
    out = np.zeros(steps)
    a = 1 + s0 * dt
    c1 = 2 * s1 * dt / h ** 2
    for n in range(steps):
        L1 = lap(u1)
        L0 = lap(u0)
        B = lap(L1)
        u2 = (2 * u1 - (1 - s0 * dt) * u0 - mu ** 2 * B + c1 * (L1 - L0)) / a
        u2[0, :] = u2[-1, :] = 0.0
        u2[:, 0] = u2[:, -1] = 0.0
        out[n] = u2[pi_, pj] - u1[pi_, pj]                 # velocity at the pickup
        u0, u1 = u1, u2
    out /= np.max(np.abs(out))
    return {"ir": out, "kappa": kap, "h": h, "grid": [nx + 1, ny + 1], "mu": mu}


def spring_ir(sr: float = 48000, seconds: float = 2.0, loop_ms: float = 35.0, feedback: float = 0.85, stages: int = 80,
              c: float = -0.6, lowpass: float = 0.4) -> np.ndarray:
    """A spring as a loop: an impulse passes through ``stages`` first-order all-passes (each delays low frequencies more
    than high ones, the spring's dispersion), a delay and a gentle low-pass, and returns with gain ``feedback``.  Each
    trip round the loop arrives as a chirp."""
    n = int(seconds * sr)
    D = int(loop_ms * sr / 1000)
    x = np.zeros(n)
    x[0] = 1.0
    trip = allpass_chain(np.r_[1.0, np.zeros(D * 3)], [c] * stages)
    trip = lfilter([1 - lowpass], [1, -lowpass], trip)
    y = np.zeros(n)
    pulse = trip
    t0 = 0
    k = 0
    while t0 < n and k < 200:
        seg = pulse[: n - t0]
        y[t0:t0 + len(seg)] += (feedback ** k) * seg
        t0 += D
        k += 1
        pulse = lfilter([1 - lowpass], [1, -lowpass], allpass_chain(pulse, [c] * (stages // 4)))
    return y / np.max(np.abs(y))
