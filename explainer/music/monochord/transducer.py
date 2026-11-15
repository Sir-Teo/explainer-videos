"""Monochord's transducers (Part 54 of *Music, Built*): microphones and loudspeakers as lumped circuits, polar patterns,
proximity, noise, balanced lines, boxes and horns, crossovers, and an adaptive noise canceller.

    pattern(A, theta)                       first-order microphone patterns: A + (1 - A) cos(theta)
    directivity(A)                          directivity factor and index, random-energy efficiency, distance factor
    proximity(f, r, A)                      a gradient microphone's bass rise near a point source, |A + (1 - A)(1 + 1/(jkr))|
    apply_response(x, H_fn)                 filter a signal by a frequency response given as a function of frequency
    thermal_noise(R, B, T)                  Johnson noise of a resistance, volts RMS
    balanced(signal, hum, imbalance)        what a receiver sees at the end of a balanced or unbalanced line
    Driver                                  Thiele-Small parameters with the derived electro-mechanical ones
    response(driver, f, box)                a lumped-element simulation of a driver on an infinite baffle, in a sealed box
                                            or in a vented box: pressure response and electrical impedance
    sealed_alignment, vented_b4             the closed forms the simulation is checked against
    horn_throat(f, S, m)                    the throat resistance of an infinite exponential horn
    crossover(f, kind, fc)                  low- and high-pass sections and their sum: Butterworth or Linkwitz-Riley
    headphone_as_mic(f, driver)             a dynamic driver run backwards: the voltage a sound pressure makes
    fxlms(noise, ...)                       an active noise canceller: filtered-x LMS through a secondary path
    delay_and_sum(signals, positions, ...)  an array steered at one direction

No manim here.  Checked in ``tests/music/test_transducer.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

try:  # the loops below are compiled when numba is there; they are the same loops without it
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap(a[0]) if a and callable(a[0]) else wrap

SR = 48000
RHO = 1.204          # air, kg/m^3, 20 C
C = 343.0            # m/s

# --------------------------------------------------------------------------------------------- microphones

PATTERNS = {"omni": 1.0, "subcardioid": 0.7, "cardioid": 0.5, "supercardioid": 0.366, "hypercardioid": 0.25, "figure-8": 0.0}


def pattern(A: float, theta):
    return A + (1 - A) * np.cos(theta)


def directivity(A: float) -> dict:
    """For r(theta) = A + (1 - A) cos theta: the random-energy efficiency REE = (1/2) int r^2 sin theta dtheta
    = A^2 + (1 - A)^2 / 3; the directivity factor DF = 1 / REE; the index 10 log10 DF; the distance factor sqrt(DF)
    (how much farther than an omni it can stand for the same ratio of direct to reverberant sound)."""
    ree = A * A + (1 - A) ** 2 / 3
    df = 1 / ree
    return {"REE": ree, "DF": df, "DI": 10 * math.log10(df), "distance": math.sqrt(df),
            "rear_db": 20 * math.log10(abs(2 * A - 1)) if abs(2 * A - 1) > 1e-12 else -np.inf,
            "null_deg": math.degrees(math.acos(-A / (1 - A))) if A < 0.5 + 1e-12 and A < 1 else None}


def proximity(f, r: float, A: float = 0.0):
    """Response near a point source at distance r, relative to the same microphone far away: the gradient part sees
    the pressure gradient of a spherical wave, (1 + 1/(jkr)) times the plane-wave gradient."""
    k = 2 * np.pi * np.asarray(f, float) / C
    return A + (1 - A) * (1 + 1 / (1j * k * r))


def apply_response(x, H_fn, sr: float = SR):
    """Filter x by H(f) in the frequency domain (zero-padded, so no wrap-around for short responses)."""
    x = np.asarray(x, float)
    n = 1 << int(math.ceil(math.log2(2 * len(x))))
    X = np.fft.rfft(x, n)
    f = np.fft.rfftfreq(n, 1 / sr)
    H = H_fn(np.maximum(f, 1.0))
    y = np.fft.irfft(X * H, n)[: len(x)]
    return y


def thermal_noise(R: float, B: float = 20000.0, T: float = 293.15) -> float:
    return math.sqrt(4 * 1.380649e-23 * T * R * B)


def balanced(signal, hum, imbalance: float = 0.0, balanced_line: bool = True):
    """A line picks up hum equally on both conductors (common mode).  A balanced receiver takes the difference of hot
    and cold, which carry the signal with opposite signs: the hum cancels, except for the ``imbalance`` fraction by
    which the two conductors pick it up differently.  An unbalanced line has only one conductor and a ground."""
    s = np.asarray(signal, float)
    h = np.asarray(hum, float)
    if not balanced_line:
        return s + h
    hot = 0.5 * s + h * (1 + imbalance / 2)
    cold = -0.5 * s + h * (1 - imbalance / 2)
    return hot - cold


# --------------------------------------------------------------------------------------------- loudspeakers


@dataclass
class Driver:
    """Thiele-Small parameters (SI units): free-air resonance, total Q (with electrical and mechanical parts), the
    equivalent volume of the suspension's compliance, the cone's area, the voice coil's resistance and inductance."""
    fs: float = 40.0
    Qes: float = 0.40
    Qms: float = 4.0
    Vas: float = 0.050
    Sd: float = 0.022
    Re: float = 6.0
    Le: float = 0.0

    @property
    def Qts(self) -> float:
        return self.Qes * self.Qms / (self.Qes + self.Qms)

    @property
    def Cms(self) -> float:
        return self.Vas / (RHO * C * C * self.Sd ** 2)

    @property
    def Mms(self) -> float:
        return 1 / ((2 * np.pi * self.fs) ** 2 * self.Cms)

    @property
    def Rms(self) -> float:
        return 2 * np.pi * self.fs * self.Mms / self.Qms

    @property
    def Bl(self) -> float:
        return math.sqrt(2 * np.pi * self.fs * self.Mms * self.Re / self.Qes)

    def with_(self, **kw):
        return Driver(**{**self.__dict__, **kw})


def response(d: Driver, f, box: dict | None = None, volts: float = 2.83, r: float = 1.0) -> dict:
    """Solve the driver's circuit at each frequency.  Mechanical side: the cone's mass, the suspension's compliance and
    loss, and the air load of the box (a sealed volume's compliance Vb / (rho c^2 Sd^2) in series; or, vented, that
    compliance in parallel with the port's mass of air, with a small leakage loss).  Electrical side: the coil's
    resistance and inductance, coupled by Bl.  Out come the cone velocity, the volume velocity that radiates (the
    cone's, plus the port's, which moves in the opposite sense inside the box), the sound pressure at r in half space,
    and the electrical impedance."""
    f = np.asarray(f, float)
    w = 2 * np.pi * f
    s = 1j * w
    Sd = d.Sd
    Zm = s * d.Mms + 1 / (s * d.Cms) + d.Rms
    Zbox = 0.0
    kind = (box or {}).get("kind", "baffle")
    if kind == "sealed":
        Cab = box["Vb"] / (RHO * C * C)
        Za_box = 1 / (s * Cab)
        Zbox = Za_box * Sd ** 2
    elif kind == "vented":
        Cab = box["Vb"] / (RHO * C * C)
        fb = box["fb"]
        Map = 1 / ((2 * np.pi * fb) ** 2 * Cab)             # the port's air mass that tunes the box to fb
        Ql = box.get("Ql", 7.0)
        Ral = Ql / (2 * np.pi * fb * Cab)                     # leakage, as a resistance across the box
        Zc = 1 / (s * Cab)
        Zp = s * Map
        Za_box = 1 / (1 / Zc + 1 / Zp + 1 / Ral)
        Zbox = Za_box * Sd ** 2
    Ze = d.Re + s * d.Le
    Zmt = Zm + Zbox
    # electrical: v = i Ze + Bl u;  mechanical: Bl i = Zmt u  ->  u = Bl v / (Ze Zmt + Bl^2)
    u = d.Bl * volts / (Ze * Zmt + d.Bl ** 2)
    i = (volts - d.Bl * u) / Ze
    U = Sd * u
    if kind == "vented":
        # the box pressure drives the port; the port's volume velocity (outward) is -p_box / Zp
        p_box = U * Za_box
        Up = -p_box / (s * Map)
        Utot = U + Up
    else:
        Utot = U
    p = RHO * s * Utot / (2 * np.pi * r)
    spl = 20 * np.log10(np.abs(p) / 20e-6)
    return {"f": f, "spl": spl, "Z": volts / i, "u": u, "U": Utot, "x": u / s}


def sealed_alignment(d: Driver, Vb: float) -> dict:
    """The closed form: in a sealed box the system is a second-order high-pass with fc = fs sqrt(1 + Vas/Vb) and
    Qtc = Qts sqrt(1 + Vas/Vb) (Small, 1972); its -3 dB point follows from fc and Qtc."""
    a = d.Vas / Vb
    fc = d.fs * math.sqrt(1 + a)
    Q = d.Qts * math.sqrt(1 + a)
    q2 = 1 / (Q * Q)
    f3 = fc * math.sqrt(((q2 - 2) + math.sqrt((q2 - 2) ** 2 + 4)) / 2)
    return {"fc": fc, "Qtc": Q, "f3": f3}


def vented_b4(d: Driver) -> dict:
    """Thiele's fourth-order Butterworth alignment (B4) for a driver with Qts = 0.383 (lossless): Vb = Vas / 1.414,
    fb = fs, and the -3 dB point at fs."""
    return {"Vb": d.Vas / 1.4142, "fb": d.fs, "f3": d.fs}


def f_minus(f, spl, db: float = 3.0, ref=None) -> float:
    """The lowest frequency where the response comes within ``db`` of its passband level (by default its level at the
    top of the frequency grid, where a box's high-pass is flat)."""
    f = np.asarray(f)
    spl = np.asarray(spl)
    ref = ref if ref is not None else float(spl[-1])
    above = np.where(spl >= ref - db)[0]
    i = above[0]
    if i == 0:
        return float(f[0])
    a, b = spl[i - 1], spl[i]
    t = (ref - db - a) / (b - a)
    return float(np.exp(np.log(f[i - 1]) + t * (np.log(f[i]) - np.log(f[i - 1]))))


def horn_throat(f, S: float, m: float):
    """An infinite exponential horn (area S e^{mx}) has throat resistance rho c / S sqrt(1 - (fc/f)^2) above its cutoff
    fc = m c / (4 pi), and none below: a horn is a transformer that only works above its flare frequency."""
    f = np.asarray(f, float)
    fc = m * C / (4 * np.pi)
    out = np.where(f > fc, RHO * C / S * np.sqrt(np.maximum(1 - (fc / f) ** 2, 0)), 0.0)
    return out, fc


def piston_resistance(f, a: float):
    """The radiation resistance of a piston of radius a in a baffle, low-frequency form rho c pi a^2 (ka)^2 / 2,
    capped at rho c pi a^2: a small cone radiates bass very inefficiently."""
    k = 2 * np.pi * np.asarray(f, float) / C
    S = np.pi * a * a
    return np.minimum(RHO * C * S * (k * a) ** 2 / 2, RHO * C * S)


def crossover(f, kind: str = "lr4", fc: float = 2000.0):
    """Low- and high-pass sections at fc and their acoustic sum (drivers assumed ideal and coincident)."""
    s = 1j * np.asarray(f, float) / fc
    if kind == "bw2":
        lp = 1 / (s * s + math.sqrt(2) * s + 1)
        hp = s * s / (s * s + math.sqrt(2) * s + 1)
    elif kind == "bw2_inv":
        lp = 1 / (s * s + math.sqrt(2) * s + 1)
        hp = -s * s / (s * s + math.sqrt(2) * s + 1)
    elif kind == "lr4":
        b = 1 / (s * s + math.sqrt(2) * s + 1)
        lp = b * b
        hp = (s * s * b) ** 2
    else:
        raise ValueError(kind)
    return lp, hp, lp + hp


def headphone_as_mic(f, d: Driver, Rload: float = 10000.0):
    """A dynamic driver run backwards: the sound pressure p pushes the diaphragm with force p Sd, the diaphragm moves
    at u = F / (Zm + Bl^2 / (Re + Rload)), and the coil makes the voltage Bl u (reduced by the divider into the load).
    Above resonance the moving mass dominates, u falls as 1/f, and the microphone sounds dull."""
    s = 1j * 2 * np.pi * np.asarray(f, float)
    Zm = s * d.Mms + 1 / (s * d.Cms) + d.Rms
    u = d.Sd / (Zm + d.Bl ** 2 / (d.Re + Rload))
    return d.Bl * u * Rload / (d.Re + Rload)


# --------------------------------------------------------------------------------------------- noise cancelling


@njit(cache=True)
def _fxlms(d, x, s_hat, s_true, L, mu, out_e, out_y, leak):
    """Filtered-x LMS.  d: the noise at the ear; x: the reference microphone's signal; the anti-noise y = w * x
    reaches the ear through the secondary path s_true (speaker to ear); the filter adapts on x filtered by the model
    s_hat of that path, normalised by its power."""
    w = np.zeros(L)
    xb = np.zeros(L)
    fx = np.zeros(L)
    Ls = len(s_true)
    yb = np.zeros(Ls)
    xs = np.zeros(len(s_hat))
    for n in range(len(d)):
        for k in range(L - 1, 0, -1):
            xb[k] = xb[k - 1]
        xb[0] = x[n]
        y = 0.0
        for k in range(L):
            y += w[k] * xb[k]
        for k in range(Ls - 1, 0, -1):
            yb[k] = yb[k - 1]
        yb[0] = y
        ys = 0.0
        for k in range(Ls):
            ys += s_true[k] * yb[k]
        e = d[n] + ys                                   # what the ear hears: the noise plus the anti-noise
        for k in range(len(s_hat) - 1, 0, -1):
            xs[k] = xs[k - 1]
        xs[0] = x[n]
        f0 = 0.0
        for k in range(len(s_hat)):
            f0 += s_hat[k] * xs[k]
        for k in range(L - 1, 0, -1):
            fx[k] = fx[k - 1]
        fx[0] = f0
        pw = 1e-6
        for k in range(L):
            pw += fx[k] * fx[k]
        g = mu / pw
        for k in range(L):
            w[k] = (1 - leak) * w[k] - g * e * fx[k]
        out_e[n] = e
        out_y[n] = ys
    return w


def fxlms(noise_at_ear, reference, secondary, taps: int = 64, mu: float = 0.02, model_error: float = 0.0, leak: float = 1e-6):
    s_true = np.asarray(secondary, float)
    s_hat = s_true * (1 + model_error)
    e = np.zeros(len(noise_at_ear))
    y = np.zeros(len(noise_at_ear))
    w = _fxlms(np.asarray(noise_at_ear, float), np.asarray(reference, float), s_hat, s_true, int(taps), float(mu), e, y, float(leak))
    return {"e": e, "anti": y, "w": w}


# --------------------------------------------------------------------------------------------- arrays


def delay_and_sum(signals, positions, angle_deg: float, sr: float = SR):
    """Steer a line of microphones at ``positions`` (metres along the line) towards ``angle_deg`` from broadside by
    delaying each by x sin(angle) / c, fractionally (in the frequency domain), and averaging."""
    out = np.zeros(len(signals[0]))
    for sig, x in zip(signals, positions):
        tau = x * math.sin(math.radians(angle_deg)) / C
        out += apply_response(sig, lambda f, tau=tau: np.exp(2j * np.pi * f * tau), sr)
    return out / len(signals)


def array_gain(f, positions, steer_deg: float, look_deg):
    """The array's response to a plane wave from ``look_deg`` when steered at ``steer_deg``: |mean of exp(jk x (sin a
    - sin b))|."""
    k = 2 * np.pi * np.asarray(f, float)[..., None] / C
    x = np.asarray(positions, float)
    ph = k * x * (math.sin(math.radians(look_deg)) - math.sin(math.radians(steer_deg)))
    return np.abs(np.exp(1j * ph).mean(axis=-1))
