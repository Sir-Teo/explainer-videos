"""Monochord's spaces (Part 55 of *Music, Built*): rooms' modes and reverberation, absorption, diffusers, early
reflections, localization, panning, Ambisonics and a binaural renderer.

    room_modes(dims, fmax)                  every mode of a rectangular room below fmax, with its kind
    weyl_count(dims, f)                     the asymptotic count of modes below f
    schroeder_frequency(T, V)               2000 sqrt(T / V): above it, modes overlap
    sabine_bands(surfaces, V)               Sabine's T in octave bands from areas and their absorption
    qrd_depths(N, f0)                       a quadratic-residue diffuser's well depths (n^2 mod N)
    scattering(depths, width, f, angles)    the far-field polar response of a row of wells (or a flat panel)
    diffusion_coefficient(levels)           the AES autocorrelation diffusion coefficient
    image_sources(dims, src, mic, order)    image sources with their delays, gains and arrival directions
    lateral_fraction(...)                   early lateral energy fraction (5 to 80 ms), the measure of spaciousness
    woodworth_itd(theta)                    the interaural time difference round a sphere
    head_shadow(f, theta)                   Brown and Duda's spherical-head filter for one ear
    binaural(x, azimuths)                   a mono signal moving through azimuths, rendered for headphones
    pan_gains(p, law)                       linear and constant-power panning
    tangent_law(gL, gR, half_angle)         where a phantom image appears between two loudspeakers
    ambisonic_decode(theta_src, speakers, kind)   first-order (2-D) encoding and basic or max-rE decoding
    gerzon_vectors(gains, speakers)         the velocity and energy vectors (rV, rE) of a decoded source

No manim here.  Checked in ``tests/music/test_space.py``.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

SR = 48000
C = 343.0
HEAD_A = 0.0875            # head radius, m


# --------------------------------------------------------------------------------------------- modes


def room_modes(dims, fmax: float):
    Lx, Ly, Lz = dims
    out = []
    nmax = [int(2 * fmax * L / C) + 1 for L in dims]
    for nx in range(nmax[0] + 1):
        for ny in range(nmax[1] + 1):
            for nz in range(nmax[2] + 1):
                if nx == ny == nz == 0:
                    continue
                f = C / 2 * math.sqrt((nx / Lx) ** 2 + (ny / Ly) ** 2 + (nz / Lz) ** 2)
                if f <= fmax:
                    k = sum(1 for n in (nx, ny, nz) if n)
                    out.append((f, (nx, ny, nz), {1: "axial", 2: "tangential", 3: "oblique"}[k]))
    return sorted(out)


def weyl_count(dims, f):
    Lx, Ly, Lz = dims
    V = Lx * Ly * Lz
    S = 2 * (Lx * Ly + Ly * Lz + Lx * Lz)
    L = 4 * (Lx + Ly + Lz)
    f = np.asarray(f, float)
    return 4 * np.pi * V * f ** 3 / (3 * C ** 3) + np.pi * S * f ** 2 / (4 * C ** 2) + L * f / (8 * C)


def schroeder_frequency(T: float, V: float) -> float:
    return 2000.0 * math.sqrt(T / V)


def sabine_bands(surfaces, V: float, extra=None) -> np.ndarray:
    """``surfaces``: list of (area m^2, [alpha per band]); ``extra``: list of [absorption m^2 per band] (people,
    cushions).  Returns Sabine's T per band: 0.161 V / A."""
    A = np.zeros(len(surfaces[0][1]))
    for S, a in surfaces:
        A += S * np.asarray(a, float)
    for e in extra or []:
        A += np.asarray(e, float)
    return 0.161 * V / A


# --------------------------------------------------------------------------------------------- diffusers


def qrd_depths(N: int, f0: float):
    """Schroeder's quadratic-residue diffuser (1975): well n has depth (n^2 mod N) / N times half a wavelength at f0."""
    lam0 = C / f0
    return np.array([(n * n % N) * lam0 / (2 * N) for n in range(N)])


def scattering(depths, width: float, f: float, angles_deg, periods: int = 4, incidence_deg: float = 0.0):
    """The far-field pressure (Fraunhofer) of ``periods`` repeats of a row of wells of the given depths, each
    ``width`` wide, lit at normal incidence: each well reflects with a phase delay of 2 k d."""
    k = 2 * np.pi * f / C
    d = np.tile(np.asarray(depths, float), periods)
    x = (np.arange(len(d)) + 0.5) * width
    x -= x.mean()
    a = np.radians(np.asarray(angles_deg, float))
    refl = np.exp(-2j * k * d)
    elem = np.sinc(k * width * np.sin(a) / (2 * np.pi))       # each well's own width
    s = np.array([np.sum(refl * np.exp(1j * k * x * (np.sin(ai) + np.sin(math.radians(incidence_deg))))) for ai in a])
    return np.abs(s * elem)


def diffusion_coefficient(levels_db) -> float:
    """AES-4id-2001: d = ((sum 10^{L/10})^2 - sum (10^{L/10})^2) / ((n - 1) sum (10^{L/10})^2): 1 for an even
    spread over every receiver, 0 for all the energy in one."""
    p = 10 ** (np.asarray(levels_db, float) / 10)
    n = len(p)
    return float((p.sum() ** 2 - (p ** 2).sum()) / ((n - 1) * (p ** 2).sum()))


# --------------------------------------------------------------------------------------------- image sources


def image_sources(dims, src, mic, order: int, beta: float = 0.9):
    """Every image of ``src`` in a rectangular room up to ``order`` reflections: delay (s), amplitude (1/r times beta
    per reflection) and the direction it arrives from at the microphone (unit vector)."""
    L = np.asarray(dims, float)
    s = np.asarray(src, float)
    m = np.asarray(mic, float)
    out = []
    rng = range(-order, order + 1)
    for nx, ny, nz in itertools.product(rng, rng, rng):
        for px, py, pz in itertools.product((0, 1), repeat=3):
            refl = abs(2 * nx - px) + abs(2 * ny - py) + abs(2 * nz - pz)
            if refl > order:
                continue
            img = np.array([(1 - 2 * px) * s[0] + 2 * nx * L[0], (1 - 2 * py) * s[1] + 2 * ny * L[1], (1 - 2 * pz) * s[2] + 2 * nz * L[2]])
            v = img - m
            r = float(np.linalg.norm(v))
            out.append((r / C, beta ** refl / max(r, 1e-3), v / r, refl))
    return sorted(out, key=lambda e: e[0])


def lateral_fraction(images, t0: float = 0.005, t1: float = 0.080, side=(0.0, 1.0, 0.0)):
    """Barron and Marshall's early lateral energy fraction: energy from 5 to 80 ms weighted by cos^2 of the angle to
    the listener's side (what a figure-8 microphone facing sideways would pick up), over all energy from 0 to 80 ms."""
    direct = images[0][0]
    side = np.asarray(side, float)
    num = sum(g * g * float(np.dot(u, side)) ** 2 for t, g, u, n in images if t0 <= t - direct <= t1)
    den = sum(g * g for t, g, u, n in images if t - direct <= t1)
    return num / den


# --------------------------------------------------------------------------------------------- the head


def woodworth_itd(theta, a: float = HEAD_A):
    """The extra path round a rigid sphere to the far ear, for a distant source at azimuth theta (0 = ahead):
    (a / c)(theta + sin theta), for |theta| up to 90 degrees."""
    th = np.abs(np.asarray(theta, float))
    th = np.where(th > np.pi / 2, np.pi - th, th)
    return a / C * (th + np.sin(th))


def head_shadow(f, theta_ear, a: float = HEAD_A, amin: float = 0.1, thmin_deg: float = 150.0):
    """Brown and Duda's one-pole, one-zero model of a sphere's effect at one ear: theta_ear is the angle between the
    source and the ear's axis (0: the source is beside this ear).  Boost up to 6 dB on the near side, a shadow on the
    far side, above about c / (2 pi a)."""
    w = 2 * np.pi * np.asarray(f, float)
    w0 = C / a
    alpha = (1 + amin / 2) + (1 - amin / 2) * np.cos(np.radians(np.degrees(theta_ear) / thmin_deg * 180.0))
    return (1 + 1j * alpha * w / (2 * w0)) / (1 + 1j * w / (2 * w0))


def ear_filters(az, n: int = 512, sr: float = SR):
    """Left and right impulse responses for a source at azimuth ``az`` (radians, positive to the right): head shadow
    and the interaural delay (applied to the far ear)."""
    f = np.fft.rfftfreq(n, 1 / sr)
    thL = abs(((az + np.pi / 2) + np.pi) % (2 * np.pi) - np.pi)      # angle from the left ear's axis (at -90 deg)
    thR = abs(((az - np.pi / 2) + np.pi) % (2 * np.pi) - np.pi)
    itd = float(woodworth_itd(az))
    dl = itd / 2 if math.sin(az) > 0 else -itd / 2
    HL = head_shadow(f, thL) * np.exp(-2j * np.pi * f * (0.002 + dl))
    HR = head_shadow(f, thR) * np.exp(-2j * np.pi * f * (0.002 - dl))
    return np.fft.irfft(HL, n), np.fft.irfft(HR, n)


def binaural(x, az_fn, sr: float = SR, block: int = 1024):
    """Render a mono signal for headphones as it moves: ``az_fn(t)`` gives the azimuth (radians) at time t; blocks
    are filtered by the head model at their azimuth and overlap-added with a Hann crossfade."""
    x = np.asarray(x, float)
    n = len(x)
    hop = block // 2
    win = np.hanning(block + 1)[:block]
    L = np.zeros(n + 2048)
    R = np.zeros(n + 2048)
    for a in range(0, n, hop):
        seg = x[a:a + block]
        if len(seg) < block:
            seg = np.r_[seg, np.zeros(block - len(seg))]
        hl, hr = ear_filters(az_fn((a + block / 2) / sr), sr=sr)
        yl = np.convolve(seg * win, hl)
        yr = np.convolve(seg * win, hr)
        L[a:a + len(yl)] += yl
        R[a:a + len(yr)] += yr
    return np.stack([L[:n], R[:n]], axis=1)


# --------------------------------------------------------------------------------------------- loudspeakers


def pan_gains(p, law: str = "power"):
    """p from -1 (left) to +1 (right)."""
    p = np.asarray(p, float)
    if law == "linear":
        return (1 - p) / 2, (1 + p) / 2
    th = (p + 1) * np.pi / 4
    return np.cos(th), np.sin(th)


def tangent_law(gL, gR, half_angle_deg: float = 30.0):
    """Bennett, Barker and Edeko's tangent law: tan(phi) / tan(phi0) = (gL - gR) / (gL + gR); phi measured from the
    centre, positive to the left."""
    t = (np.asarray(gL, float) - np.asarray(gR, float)) / (np.asarray(gL, float) + np.asarray(gR, float))
    return np.degrees(np.arctan(t * math.tan(math.radians(half_angle_deg))))


def ambisonic_decode(theta, speakers, kind: str = "basic"):
    """First-order horizontal Ambisonics: encode W = 1, X = cos theta, Y = sin theta; decode to loudspeakers at
    ``speakers`` (radians) by projection, g_i = (1/N)(1 + 2 w1 (X cos phi_i + Y sin phi_i)), with w1 = 1 (basic,
    'velocity') or 1/sqrt(2) (max-rE, Daniel's weighting for first order in 2-D)."""
    phi = np.asarray(speakers, float)
    w1 = 1.0 if kind == "basic" else 1 / math.sqrt(2)
    N = len(phi)
    return (1 + 2 * w1 * (math.cos(theta) * np.cos(phi) + math.sin(theta) * np.sin(phi))) / N


def gerzon_vectors(g, speakers):
    """Gerzon's localization vectors: rV = sum g u / sum g (low frequencies), rE = sum g^2 u / sum g^2 (high);
    their directions predict where the image is heard, their lengths how sharply (1 = a single loudspeaker)."""
    g = np.asarray(g, float)
    u = np.stack([np.cos(speakers), np.sin(speakers)], axis=1)
    rV = (g[:, None] * u).sum(axis=0) / g.sum()
    rE = ((g ** 2)[:, None] * u).sum(axis=0) / (g ** 2).sum()
    return {"rV": rV, "rE": rE, "|rV|": float(np.linalg.norm(rV)), "|rE|": float(np.linalg.norm(rE)),
            "dir_rE": float(np.degrees(math.atan2(rE[1], rE[0])))}


# --------------------------------------------------------------------------------------------- rendering rooms


def noise_tail(T: float, seconds: float, sr: float = SR, seed: int = 0, stereo: bool = False, start: float = 0.0, dark: float = 0.5):
    """A statistical reverberation tail: noise dying by 60 dB in T seconds, the highs dying sooner (a crossfade
    towards a low-passed copy over the tail, ``dark``), independent in each ear if ``stereo``.  Normalised to unit
    energy."""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(seed)
    n = int(seconds * sr)
    t = np.arange(n) / sr
    env = np.exp(-6.91 * t / T) * np.clip((t - start) / 0.01, 0, 1)
    out = []
    for ch in range(2 if stereo else 1):
        w = rng.standard_normal(n)
        lo = sosfilt(butter(2, 2500, fs=sr, output="sos"), w)
        mixw = np.clip(dark * t / max(T, 1e-3) * 2, 0, 1)
        y = ((1 - mixw) * w + mixw * lo) * env
        out.append(y / math.sqrt(np.sum(y ** 2) + 1e-12))
    return np.stack(out, axis=1) if stereo else out[0]


def binaural_room(images, tail_T: float, tail_level: float, seconds: float, facing=(-1.0, 0.0, 0.0), sr: float = SR, early_ms: float = 80.0, seed: int = 0):
    """A two-ear impulse response: every image source arriving within ``early_ms`` of the direct sound filtered by the
    head model from its own direction (azimuth in the horizontal plane, the listener facing ``facing``), then a
    statistical stereo tail."""
    n = int(seconds * sr)
    h = np.zeros((n + 1024, 2))
    t0 = images[0][0]
    fx, fy = facing[0], facing[1]
    for t, g, u, k in images:
        if t - t0 > early_ms / 1000:
            break
        az = math.atan2(fx * u[1] - fy * u[0], fx * u[0] + fy * u[1])     # positive: to the listener's left
        hl, hr = ear_filters(-az, n=256, sr=sr)
        i = int((t - t0) * sr)
        h[i:i + 256, 0] += g * hl
        h[i:i + 256, 1] += g * hr
    h = h[:n]
    direct_e = images[0][1] ** 2
    tail = noise_tail(tail_T, seconds, sr, seed=seed, stereo=True, start=0.02)
    h += math.sqrt(tail_level * direct_e) * tail
    return h
