"""The ear, as far as a film needs it (Part 4, *The Ear*).  Each model is checked against something that does not
share its code (``tests/music/test_ear.py``).

* the middle ear as a transformer, and the ear canal as a quarter-wave tube;
* :func:`cochlea`: the basilar membrane as a row of masses on springs coupled by fluid (the "long-wave" model),
  solved for one frequency at a time: a travelling wave that peaks at a place set by the frequency;
* :func:`erb`, :func:`gammatone`, :func:`filterbank`, :func:`cochleagram`: the auditory filters (Glasberg and
  Moore's bandwidths, Patterson's gammatone shape);
* :func:`threshold_db`, :func:`a_weight_db`, :func:`sones`: loudness;
* :func:`masked_threshold`: the power-spectrum model of masking (Fletcher, 1940);
* :func:`pitch`: an autocorrelation model of pitch (Licklider, 1951; Meddis and Hewitt, 1991);
* :func:`shepard`: tones whose pitch class is clear and whose octave is not;
* :func:`safe_hours`: the noise dose;
* :func:`hopf_response`: one active hair-cell oscillator poised at the edge of oscillation.

Published constants are marked as such; everything else is computed.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import fftconvolve

from .physics import air

# ---------------------------------------------------------------------------
# Outer and middle ear (published dimensions: Pickles, An Introduction to the Physiology of Hearing, ch. 2)
# ---------------------------------------------------------------------------
CANAL_LENGTH = 0.025           # m
EARDRUM_AREA = 55e-6           # m^2, the part of the eardrum that moves the ossicles
STAPES_AREA = 3.2e-6           # m^2, the footplate in the oval window
LEVER = 1.3                    # the malleus is that much longer than the incus
COCHLEA_Z = 1.5e5              # Pa s / m: the input impedance of the cochlea, roughly (much less than water's rho c)


def canal_resonance(celsius: float = 37.0) -> float:
    """The ear canal as a pipe closed by the eardrum: its quarter-wave resonance."""
    return air.speed(celsius) / (4 * CANAL_LENGTH)


def middle_ear() -> dict:
    """The pressure gain of the middle ear as a transformer (area ratio times lever ratio), and what it does for
    the share of the sound's power that enters the cochlea."""
    gain = EARDRUM_AREA / STAPES_AREA * LEVER
    z_air = air.impedance(37.0)

    def through(z1, z2):
        return 4 * z1 * z2 / (z1 + z2) ** 2

    # the cochlea as the air at the eardrum sees it: pressure is multiplied by the gain, velocity divided by the lever
    z_seen = COCHLEA_Z / (gain * LEVER)
    return {"area_ratio": EARDRUM_AREA / STAPES_AREA, "lever": LEVER, "pressure_gain": gain, "gain_db": 20 * math.log10(gain),
            "without": through(z_air, COCHLEA_Z), "with": through(z_air, z_seen), "z_air": z_air, "z_cochlea": COCHLEA_Z,
            "z_seen": z_seen, "power_gain_db": 10 * math.log10(EARDRUM_AREA / STAPES_AREA * through(z_air, z_seen) / through(z_air, COCHLEA_Z))}


# ---------------------------------------------------------------------------
# The cochlea: a travelling wave
# ---------------------------------------------------------------------------
COCHLEA_LENGTH = 0.035         # m (human)


def greenwood(x_from_base: float | np.ndarray) -> np.ndarray:
    """Greenwood's map of the human cochlea (1990): the frequency whose place is ``x`` metres from the base."""
    frac = 1.0 - np.asarray(x_from_base) / COCHLEA_LENGTH
    return 165.4 * (10 ** (2.1 * frac) - 0.88)


def resonance(x: np.ndarray, f_base: float = 20_000.0, f_apex: float = 100.0) -> np.ndarray:
    """The model membrane's own frequency at each place: stiff and quick at the base, slack and slow at the apex."""
    return f_base * (f_apex / f_base) ** (np.asarray(x) / COCHLEA_LENGTH)


def cochlea(hz: float, n: int = 2000, damping: float = 0.08, mass: float = 0.5, height: float = 1e-3) -> dict:
    """The long-wave model of the cochlea at one frequency.

    The fluid above and below the membrane is driven at the base (the stapes) and can only move along the duct;
    wherever it squeezes, it pushes the membrane, whose response at each place is that of a mass on a spring with
    friction.  The pressure difference ``p(x)`` across the membrane then obeys
    ``p'' = (2 i omega rho / (h Z(x))) p`` with ``Z = s/(i omega) + r + i omega m``, ``p'(0)`` set by the stapes and
    ``p = 0`` at the apex.  Returns the membrane's displacement along the cochlea (complex), its envelope and the
    place of its peak."""
    rho = 1000.0
    w = 2 * math.pi * hz
    x = np.linspace(0.0, COCHLEA_LENGTH, n)
    dx = x[1] - x[0]
    s = mass * (2 * math.pi * resonance(x)) ** 2
    r = 2 * damping * np.sqrt(s * mass)
    Z = s / (1j * w) + r + 1j * w * mass
    k2 = 2j * w * rho / (height * Z)
    # tridiagonal system for p'' - k2 p = 0
    main = -2.0 / dx ** 2 - k2
    off = np.full(n - 1, 1.0 / dx ** 2, dtype=complex)
    rhs = np.zeros(n, dtype=complex)
    main = main.astype(complex)
    upper, lower = off.copy(), off.copy()
    main[0] = -1.0 / dx                       # p'(0) = -2 i omega rho u_stapes, with the stapes velocity as the unit
    upper[0] = 1.0 / dx
    rhs[0] = -2j * w * rho
    main[-1] = 1.0                            # p = 0 at the helicotrema
    lower[-1] = 0.0
    # Thomas algorithm
    cp, dp = np.zeros(n - 1, dtype=complex), np.zeros(n, dtype=complex)
    cp[0] = upper[0] / main[0]
    dp[0] = rhs[0] / main[0]
    for i in range(1, n):
        den = main[i] - lower[i - 1] * cp[i - 1]
        if i < n - 1:
            cp[i] = upper[i] / den
        dp[i] = (rhs[i] - lower[i - 1] * dp[i - 1]) / den
    p = np.zeros(n, dtype=complex)
    p[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        p[i] = dp[i] - cp[i] * p[i + 1]
    disp = p / Z / (1j * w)
    env = np.abs(disp)
    k = int(np.argmax(env))
    return {"x": x, "displacement": disp, "envelope": env, "peak_x": float(x[k]), "peak": float(env[k]),
            "resonant_x": float(x[int(np.argmin(np.abs(resonance(x) - hz)))])}


def sharpness(hz: float, damping: float, n: int = 2000) -> float:
    """How selective one place is: the frequency of its peak response divided by the width of the response 10 dB
    down (the Q10 of physiology), found by sweeping the tone at the place where ``hz`` peaks."""
    place = cochlea(hz, n, damping)["peak_x"]
    k = int(round(place / COCHLEA_LENGTH * (n - 1)))
    fs = hz * 2 ** np.linspace(-1.5, 0.7, 111)
    resp = np.array([cochlea(f, n, damping)["envelope"][k] for f in fs])
    top = int(np.argmax(resp))
    above = np.where(resp >= resp[top] / math.sqrt(10))[0]
    return float(fs[top] / (fs[above[-1]] - fs[above[0]]))


# ---------------------------------------------------------------------------
# Auditory filters
# ---------------------------------------------------------------------------
def erb(hz) -> np.ndarray:
    """The equivalent rectangular bandwidth of the auditory filter centred on ``hz`` (Glasberg and Moore, 1990)."""
    return 24.7 * (4.37 * np.asarray(hz, dtype=float) / 1000.0 + 1.0)


def erb_number(hz) -> np.ndarray:
    """How many auditory filters fit below ``hz`` (the ERB-rate scale)."""
    return 21.4 * np.log10(4.37 * np.asarray(hz, dtype=float) / 1000.0 + 1.0)


def erb_space(lo: float, hi: float, n: int) -> np.ndarray:
    """``n`` centre frequencies equally spaced on the ERB-rate scale."""
    e = np.linspace(erb_number(lo), erb_number(hi), n)
    return (10 ** (e / 21.4) - 1.0) * 1000.0 / 4.37


def bark(hz) -> np.ndarray:
    """Zwicker's critical-band rate, by Traunmueller's formula (1990)."""
    f = np.asarray(hz, dtype=float)
    return 26.81 * f / (1960.0 + f) - 0.53


def gammatone(hz: float, sr: int = 48_000, order: int = 4) -> np.ndarray:
    """The impulse response of one auditory filter: a tone that swells and dies, ``t^(n-1) exp(-2 pi b t) cos(2 pi f t)``
    with ``b = 1.019 ERB(f)`` (Patterson and Holdsworth).  Scaled so that a tone at ``hz`` passes at 1."""
    b = 1.019 * float(erb(hz))
    n = int(sr * min(0.3, 25.0 / (2 * math.pi * b)))          # until the swell has died to a millionth
    t = np.arange(n) / sr
    g = t ** (order - 1) * np.exp(-2 * math.pi * b * t) * np.cos(2 * math.pi * hz * t)
    gain = abs(np.sum(g * np.exp(-2j * math.pi * hz * t)))
    return g / gain


def filterbank(y: np.ndarray, sr: int, centres) -> np.ndarray:
    """A sound through a row of auditory filters: one row of output per centre frequency."""
    y = np.asarray(y, dtype=float)
    return np.array([fftconvolve(y, gammatone(f, sr))[: len(y)] for f in centres])


def filter_response_db(centre: float, hz, sr: int = 48_000) -> np.ndarray:
    """How much (dB) of a tone at each frequency in ``hz`` passes the auditory filter centred on ``centre``."""
    g = gammatone(centre, sr)
    t = np.arange(len(g)) / sr
    hz = np.atleast_1d(np.asarray(hz, dtype=float))
    h = np.array([abs(np.sum(g * np.exp(-2j * math.pi * f * t))) for f in hz])
    return 20 * np.log10(np.maximum(h, 1e-12))


def cochleagram(y: np.ndarray, sr: int, centres, hop: int = 480) -> np.ndarray:
    """The level (dB) in each auditory filter, frame by frame: what the cochlea hands the nerve."""
    bank = filterbank(y, sr, centres)
    frames = bank.shape[1] // hop
    e = (bank[:, : frames * hop] ** 2).reshape(len(centres), frames, hop).mean(axis=2)
    return 10 * np.log10(np.maximum(e, 1e-14))


# ---------------------------------------------------------------------------
# Loudness
# ---------------------------------------------------------------------------
def threshold_db(hz) -> np.ndarray:
    """The quietest pure tone a young listener hears, in dB SPL (Terhardt's fit, 1979)."""
    f = np.asarray(hz, dtype=float) / 1000.0
    return 3.64 * f ** -0.8 - 6.5 * np.exp(-0.6 * (f - 3.3) ** 2) + 1e-3 * f ** 4


def a_weight_db(hz) -> np.ndarray:
    """The A-weighting curve of sound-level meters (IEC 61672): roughly the ear's sensitivity at moderate levels."""
    f2 = np.asarray(hz, dtype=float) ** 2
    ra = 12194.0 ** 2 * f2 ** 2 / ((f2 + 20.6 ** 2) * np.sqrt((f2 + 107.7 ** 2) * (f2 + 737.9 ** 2)) * (f2 + 12194.0 ** 2))
    return 20 * np.log10(ra) + 2.0


def sones(phons) -> np.ndarray:
    """Stevens's scale of loudness: 40 phons is one sone, and every 10 phons more doubles it."""
    return 2.0 ** ((np.asarray(phons, dtype=float) - 40.0) / 10.0)


# ---------------------------------------------------------------------------
# Masking
# ---------------------------------------------------------------------------
def masked_threshold(masker_hz: float, masker_db: float, probe_hz, k_db: float = -4.0, sr: int = 48_000) -> np.ndarray:
    """The level a probe tone must reach to be heard beside a masker tone, by the power-spectrum model: the probe
    is heard through the auditory filter centred on it, and must exceed the masker's power in that same filter by
    ``k_db``; it can never be quieter than the threshold in quiet."""
    probe_hz = np.atleast_1d(np.asarray(probe_hz, dtype=float))
    out = []
    for f in probe_hz:
        leak = float(filter_response_db(f, masker_hz, sr)[0])
        out.append(max(masker_db + leak + k_db, float(threshold_db(f))))
    return np.array(out)


# ---------------------------------------------------------------------------
# Pitch
# ---------------------------------------------------------------------------
def neural(bank: np.ndarray, sr: int, corner: float = 1200.0) -> np.ndarray:
    """What the nerve carries from each filter: only the upward half of the motion, smoothed so that fine timing
    is lost above a few kilohertz (two one-pole stages at ``corner``)."""
    v = np.maximum(bank, 0.0)
    a = math.exp(-2 * math.pi * corner / sr)
    from scipy.signal import lfilter

    for _ in range(2):
        v = lfilter([1 - a], [1, -a], v, axis=1)
    return v


def summary_acf(y: np.ndarray, sr: int, centres=None, max_lag: float = 0.03,
                corner: float = 1200.0) -> tuple[np.ndarray, np.ndarray]:
    """The summary autocorrelation of a sound: for each auditory filter, how well the nerve's signal matches
    itself a lag later; then the sum over filters.  Returns ``(lags in seconds, summary)`` with the value at lag 0
    equal to 1.  ``corner`` is the frequency above which the nerve model loses fine timing."""
    centres = erb_space(80.0, 8000.0, 40) if centres is None else centres
    v = neural(filterbank(y, sr, centres), sr, corner)
    v = v[:, int(0.03 * sr):]                             # after the filters have started ringing
    n = v.shape[1]
    spec = np.fft.rfft(v, 2 * n, axis=1)
    ac = np.fft.irfft(np.abs(spec) ** 2, axis=1)[:, : int(max_lag * sr)]
    summ = ac.sum(axis=0)
    return np.arange(len(summ)) / sr, summ / summ[0]


def pitch(y: np.ndarray, sr: int, lo: float = 50.0, hi: float = 1000.0, centres=None,
          corner: float = 1200.0) -> tuple[float, float]:
    """The pitch the autocorrelation model assigns to a sound, in hertz, and how salient it is: how far the
    summary's peak stands above its lowest point (near 1 when the nerve's timing follows the wave closely, near 0
    when it carries no timing at all)."""
    lags, s = summary_acf(y, sr, centres, max_lag=1.0 / lo + 0.002, corner=corner)
    a, b = int(sr / hi), int(sr / lo)
    k = a + int(np.argmax(s[a:b]))
    # a peak at lag T also appears at 2T, 3T...: prefer the first one that is nearly as high
    for j in range(a + 1, k):
        if s[j] > s[j - 1] and s[j] >= s[j + 1] and s[j] > 0.97 * s[k] - 0.0:
            k = j
            break
    y0, y1, y2 = s[k - 1], s[k], s[k + 1]
    off = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) != 0 else 0.0
    floor = float(np.min(s[a:b]))
    return sr / (k + off), float(s[k] - floor)


# ---------------------------------------------------------------------------
# Shepard tones
# ---------------------------------------------------------------------------
def shepard(step: float, seconds: float = 0.5, sr: int = 48_000, base: float = 27.5, octaves: int = 9,
            centre: float = 440.0, width: float = 1.6) -> np.ndarray:
    """A Shepard tone ``step`` semitones up from the reference: partials an octave apart across the whole range,
    under a fixed bell-shaped envelope of loudness against log-frequency.  Twelve steps up is the same sound."""
    t = np.arange(int(seconds * sr)) / sr
    y = np.zeros(len(t))
    for k in range(octaves):
        f = base * 2 ** (k + (step % 12) / 12.0)
        if f > 0.45 * sr:
            continue
        a = math.exp(-0.5 * (math.log2(f / centre) / width) ** 2)
        y += a * np.sin(2 * math.pi * f * t)
    ramp = int(0.02 * sr)
    y[:ramp] *= np.linspace(0, 1, ramp)
    y[-ramp:] *= np.linspace(1, 0, ramp)
    return y


# ---------------------------------------------------------------------------
# The noise dose
# ---------------------------------------------------------------------------
def safe_hours(dba: float, limit: float = 85.0, exchange: float = 3.0) -> float:
    """The daily exposure that reaches the recommended limit (NIOSH, 1998): eight hours at 85 dBA, halved for
    every 3 dB more."""
    return 8.0 / 2.0 ** ((dba - limit) / exchange)


# ---------------------------------------------------------------------------
# One active oscillator
# ---------------------------------------------------------------------------
def hopf_response(force, mu: float = 0.0) -> np.ndarray:
    """The steady response of a Hopf oscillator driven at its own frequency: the amplitude ``r`` that solves
    ``r^3 - mu r = F``.  At ``mu = 0`` (poised exactly at the edge of oscillating by itself) ``r = F^(1/3)``: faint
    sounds are amplified enormously and loud ones hardly at all."""
    force = np.atleast_1d(np.asarray(force, dtype=float))
    out = []
    for f in force:
        roots = np.roots([1.0, 0.0, -mu, -f])
        real = roots[np.abs(roots.imag) < 1e-9].real
        out.append(float(real[real > 0].max()))
    return np.array(out)


def hopf_run(force: np.ndarray, sr: int, hz: float, mu: float = 0.0, scale: float = 1.0) -> np.ndarray:
    """A Hopf oscillator of natural frequency ``hz`` driven by ``force`` (real), stepped in time:
    ``dz/dt = (mu + i omega) z - |z|^2 z + F``.  Returns the real part of ``z``.  Fed two tones, it answers with
    tones that were not in the input (``2 f1 - f2`` first of all)."""
    w = 2 * math.pi * hz
    dt = 1.0 / sr
    z = 0j
    out = np.empty(len(force))
    for i, f in enumerate(force):
        # exact rotation for the linear part, Euler for the rest (the rate is far above the frequencies involved)
        z = z * np.exp((mu * scale + 1j * w) * dt) + dt * scale * (f - abs(z) ** 2 * z)
        out[i] = z.real
    return out
