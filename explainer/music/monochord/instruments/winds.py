"""Pipes, reeds, lips and voices (Part 8, *Pipes, Reeds and Voices*).

A wind instrument is two things joined in a loop: a column of air that resonates, and a valve that lets breath
through in time with it.  This module has both.

    Bore                the column: any chain of cylinders and cones, side holes and an open or closed end.  Its input
                        impedance comes from transfer matrices (plane waves with wall losses), and from the impedance
                        the reflection function: what comes back to the mouthpiece when one pulse is sent in.
    reed_tone           a clarinet-like reed (McIntyre, Schumacher and Woodhouse, 1983): the flow through the reed slit
                        as a function of the pressure across it, closed by a time-stepped bore.
    lip_tone            a brass player's lips: a mass on a spring that the pressure blows open, on the same bore.
    jet_tone            a flute's jet, in the schematic form used for synthesis: a delay and a saturating curve.
    Voice               a pulsing source and a filter with formants; ``tract_formants`` finds the formants of a tube.

No manim.  Everything is checked in ``tests/music/test_winds.py`` against textbook values (pipe resonances, the
reed's threshold at a third of its closing pressure, Peterson and Barney's vowels).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

try:
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap if not (a and callable(a[0])) else a[0]

SR = 48_000
RHO, C = 1.2, 343.0


# ---------------------------------------------------------------------------
# The column of air
# ---------------------------------------------------------------------------
def _wavenumber(f: np.ndarray, a: float) -> np.ndarray:
    """The complex wavenumber of plane waves in a tube of radius ``a`` (m): sound is slowed and damped by the
    viscous and thermal layers at the wall, by an amount that grows as the square root of the frequency."""
    alpha = 3.0e-5 * np.sqrt(np.maximum(f, 1e-9)) / a            # nepers per metre
    return 2 * np.pi * f / C + (1.0 - 1.0j) * alpha


def radiation(f: np.ndarray, a: float) -> np.ndarray:
    """The impedance that an open, unflanged end of radius ``a`` presents (Levine and Schwinger's result in Norris
    and Sheng's fit): at low frequencies almost a pressure node a little beyond the end (0.61 a), with a small
    resistance, the sound that escapes, growing as the frequency squared."""
    ka = np.minimum(2 * np.pi * f * a / C, 3.8)
    mag = (1 + 0.2 * ka - 0.084 * ka ** 2) / (1 + 0.2 * ka + (0.5 - 0.084) * ka ** 2)
    delta = a * (0.6133 * (1 + 0.044 * ka ** 2) / (1 + 0.19 * ka ** 2) - 0.02 * np.sin(2 * ka) ** 2)
    r = -mag * np.exp(-2j * (2 * np.pi * f / C) * delta)
    return (RHO * C / (np.pi * a * a)) * (1 + r) / (1 - r)


@dataclass
class Bore:
    """A chain of pieces, from the mouthpiece to the far end.  Each piece is ``("tube", length, r_in, r_out)`` (a
    cylinder if the radii are equal, else a cone, cut into short cylinders) or ``("hole", radius, chimney)``: an
    open side hole.  ``end`` is "open" or "closed"."""
    pieces: list = field(default_factory=list)
    end: str = "open"
    slices_per_metre: float = 800.0

    def tube(self, length: float, r_in: float, r_out: float | None = None) -> "Bore":
        self.pieces.append(("tube", float(length), float(r_in), float(r_in if r_out is None else r_out)))
        return self

    def hole(self, radius: float, chimney: float = 0.003) -> "Bore":
        self.pieces.append(("hole", float(radius), float(chimney)))
        return self

    def horn(self, length: float, r_in: float, r_out: float, flare: float = 0.7, steps: int = 60) -> "Bore":
        """A flaring bell: a Bessel horn, radius = b / (x + x0)^flare, measured back from the open end."""
        x0 = length / ((r_out / r_in) ** (1 / flare) - 1)
        b = r_out * x0 ** flare
        xs = np.linspace(length + x0, x0, steps + 1)
        rs = b / xs ** flare
        for i in range(steps):
            self.tube(length / steps, rs[i], rs[i + 1])
        return self

    @property
    def length(self) -> float:
        return sum(p[1] for p in self.pieces if p[0] == "tube")

    @property
    def r_in(self) -> float:
        return next(p[2] for p in self.pieces if p[0] == "tube")

    @property
    def r_out(self) -> float:
        return [p[3] for p in self.pieces if p[0] == "tube"][-1]

    @property
    def z0(self) -> float:
        """The characteristic impedance at the mouthpiece end."""
        return RHO * C / (np.pi * self.r_in ** 2)

    def profile(self, n: int = 400) -> tuple[np.ndarray, np.ndarray]:
        """Radius against distance along the bore."""
        xs, rs, x = [], [], 0.0
        for p in self.pieces:
            if p[0] == "tube":
                xs += [x, x + p[1]]
                rs += [p[2], p[3]]
                x += p[1]
        return np.array(xs), np.array(rs)

    def _matrices(self, f: np.ndarray):
        """The chain's transfer matrix (A, B, C, D) at each frequency: [p_in, U_in] = M [p_out, U_out]."""
        a_ = np.ones(len(f), dtype=complex)
        b_ = np.zeros(len(f), dtype=complex)
        c_ = np.zeros(len(f), dtype=complex)
        d_ = np.ones(len(f), dtype=complex)

        def mul(a2, b2, c2, d2):
            nonlocal a_, b_, c_, d_
            a_, b_, c_, d_ = a_ * a2 + b_ * c2, a_ * b2 + b_ * d2, c_ * a2 + d_ * c2, c_ * b2 + d_ * d2

        for p in self.pieces:
            if p[0] == "tube":
                _, length, r1, r2 = p
                n = 1 if abs(r1 - r2) < 1e-12 else max(int(math.ceil(length * self.slices_per_metre)), 8)
                for i in range(n):
                    r = r1 + (r2 - r1) * (i + 0.5) / n
                    k = _wavenumber(f, r)
                    zc = RHO * C / (np.pi * r * r)
                    kl = k * (length / n)
                    cs, sn = np.cos(kl), np.sin(kl)
                    mul(cs, 1j * zc * sn, 1j * sn / zc, cs)
            else:
                _, r, chimney = p
                # an open side hole: a short tube (its chimney, with end corrections inside and out) to the open air
                t_eff = chimney + 1.5 * r
                zh = 1j * 2 * np.pi * f * RHO * t_eff / (np.pi * r * r) + (RHO * C / (np.pi * r * r)) * 0.25 * (2 * np.pi * f * r / C) ** 2
                mul(np.ones(len(f)), np.zeros(len(f)), 1.0 / zh, np.ones(len(f)))
        return a_, b_, c_, d_

    def impedance(self, f) -> np.ndarray:
        """The input impedance (pressure over volume flow at the mouthpiece), in units of the bore's own z0."""
        f = np.atleast_1d(np.asarray(f, dtype=float))
        a_, b_, c_, d_ = self._matrices(f)
        if self.end == "open":
            zl = radiation(f, self.r_out)
            z = (a_ * zl + b_) / (c_ * zl + d_)
        else:
            z = a_ / c_
        return z / self.z0

    def peaks(self, f_max: float = 4000.0, df: float = 0.25, admittance: bool = False, floor: float = 0.0) -> list[tuple[float, float]]:
        """The resonances a player can use: the peaks of the input impedance (reeds and lips, which sit at a
        pressure antinode) or of the admittance (flutes, open at the mouth).  Returns (Hz, height)."""
        f = np.arange(20.0, f_max, df)
        z = np.abs(self.impedance(f))
        y = 1.0 / z if admittance else z
        out = []
        for i in range(1, len(y) - 1):
            if y[i] > y[i - 1] and y[i] >= y[i + 1] and y[i] > floor:
                a, b, c = y[i - 1], y[i], y[i + 1]
                out.append((float(f[i] + 0.5 * df * (a - c) / (a - 2 * b + c)), float(b)))
        return out

    def reflection(self, n: int = 8192, sr: int = SR) -> np.ndarray:
        """What comes back: the pressure wave returning to the mouthpiece after a unit pulse is sent down the bore,
        sampled at ``sr``.  The inverse Fourier transform of (Z - z0)/(Z + z0), tapered at the top of the band."""
        f = np.fft.rfftfreq(2 * n, 1.0 / sr)
        z = self.impedance(np.maximum(f, 1.0))
        r = (z - 1.0) / (z + 1.0)
        taper = 0.5 * (1 + np.cos(np.pi * np.clip((f - 0.25 * sr) / (0.2 * sr), 0, 1)))
        h = np.fft.irfft(r * taper)[:n]
        h[0] = 0.0
        return h

    def transfer(self, f) -> np.ndarray:
        """Radiated sound for a unit pressure at the mouthpiece: the volume flow leaving the open end (times the
        frequency, since a small source radiates in proportion to how fast its flow changes)."""
        f = np.atleast_1d(np.asarray(f, dtype=float))
        a_, b_, c_, d_ = self._matrices(f)
        zl = radiation(f, self.r_out)
        u_out = 1.0 / (a_ * zl + b_)
        return u_out * f * self.z0


def cylinder(length: float, radius: float, end: str = "open") -> Bore:
    return Bore(end=end).tube(length, radius)


def cone(length: float, r_in: float, r_out: float, end: str = "open") -> Bore:
    return Bore(end=end).tube(length, r_in, r_out)


def clarinet(length: float = 0.60, radius: float = 0.0075, register_hole: bool = False) -> Bore:
    """A clarinet with every tone hole closed: a cylinder.  With ``register_hole``, a pinhole a quarter of the
    way down, which moves the lowest resonance out of tune with the rest and leaves the next one in charge."""
    b = Bore()
    if register_hole:
        b.tube(length * 0.25, radius).hole(0.0015, 0.004).tube(length * 0.75, radius)
    else:
        b.tube(length, radius)
    return b


def saxophone(length: float = 0.60, r_in: float = 0.005, r_out: float = 0.03, r_mouthpiece: float = 0.008) -> Bore:
    """A conical reed instrument.  The cone cannot run to its point (there has to be a reed), so the tip is cut off
    and replaced by a mouthpiece whose volume equals that of the missing tip; then the resonances stay close to a
    whole harmonic series."""
    x1 = r_in * length / (r_out - r_in)
    volume = math.pi * r_in ** 2 * x1 / 3.0
    return Bore().tube(volume / (math.pi * r_mouthpiece ** 2), r_mouthpiece).tube(length, r_in, r_out)


def trumpet(tube: float = 1.37, radius: float = 0.0058, bell: float = 0.56, bell_radius: float = 0.061, mouthpiece: bool = True) -> Bore:
    """A trumpet's shape: a mouthpiece (a cup and a narrow throat), a long narrow cylinder, and a flaring bell."""
    b = Bore()
    if mouthpiece:
        b.tube(0.008, 0.008).tube(0.004, 0.008, 0.0018).tube(0.07, 0.0018, radius)
    b.tube(tube - bell - (0.082 if mouthpiece else 0.0), radius)
    b.horn(bell, radius, bell_radius, flare=0.7)
    return b


def harmonicity(peaks, lowest: int = 2, count: int = 6) -> tuple[float, list[float]]:
    """How nearly a set of resonances is a harmonic series: the fundamental that best fits peaks number
    ``lowest`` and up as its multiples 2, 3, 4 ..., and each peak's distance from its multiple in cents."""
    fs = [p[0] for p in peaks][lowest - 1: lowest - 1 + count]
    ns = np.arange(lowest, lowest + len(fs))
    f0 = float(np.sum(np.array(fs) * ns) / np.sum(ns * ns))
    return f0, [float(1200 * math.log2(f / (n * f0))) for f, n in zip(fs, ns)]


# ---------------------------------------------------------------------------
# The reed: a valve that the pressure closes
# ---------------------------------------------------------------------------
def reed_flow(dp, zeta: float = 0.35):
    """The flow through a reed slit against the pressure across it (mouth minus mouthpiece), both in the reed's own
    units: pressure as a fraction of the pressure that holds the reed shut, flow in units of that pressure over
    the bore's impedance.  Bernoulli's flow (the square root) through a slit that the same pressure narrows (the
    factor 1 - dp): it rises, reaches a top at one third, and falls to nothing at 1."""
    dp = np.asarray(dp, dtype=float)
    return np.where(dp < 1.0, zeta * (1.0 - dp) * np.sqrt(np.abs(dp)) * np.sign(dp), 0.0)


@njit(cache=True)
def _reed(steps, r, gamma, zeta, noise):
    n = len(r)
    hist = np.zeros(n)                   # p + u at earlier steps, newest first (a ring)
    p_out = np.empty(steps)
    u_out = np.empty(steps)
    head = 0
    p = 0.0
    for s in range(steps):
        ph = 0.0
        for k in range(1, n):
            ph += r[k] * hist[(head - k + 1) % n]
        g = gamma[s]
        # solve p = ph + u(g - p): the function p - ph - u is increasing in p for zeta < 1; bisect
        lo, hi = ph - 2.0, ph + 2.0
        for _ in range(48):
            mid = 0.5 * (lo + hi)
            dp = g - mid
            if dp < 1.0:
                u = zeta * (1.0 - dp) * math.sqrt(abs(dp)) * (1.0 if dp >= 0 else -1.0)
            else:
                u = 0.0
            if mid - ph - u > 0:
                hi = mid
            else:
                lo = mid
        p = 0.5 * (lo + hi)
        dp = g - p
        u = zeta * (1.0 - dp) * math.sqrt(abs(dp)) * (1.0 if dp >= 0 else -1.0) if dp < 1.0 else 0.0
        u += noise[s]
        p_out[s] = p
        u_out[s] = u
        head = (head + 1) % n
        hist[head] = p + u
    return p_out, u_out


def reed_tone(bore: Bore, gamma=0.45, seconds: float = 1.0, zeta: float = 0.35, sr: int = SR, attack: float = 0.03, seed: int = 0,
              taps: int = 8192) -> dict:
    """Blow a reed on a bore.  ``gamma`` is the mouth pressure as a fraction of the pressure that would hold the reed
    shut (a number, or an array over time).  At every step the pressure in the mouthpiece is what returns from the
    bore plus what the flow through the reed adds, and the flow depends on that pressure: one equation, solved by
    bisection.  Returns the mouthpiece pressure and the flow (reed units), and the radiated sound."""
    steps = int(seconds * sr)
    g = np.full(steps, float(gamma)) if np.isscalar(gamma) else np.asarray(gamma, dtype=float)[:steps]
    g = g * np.clip(np.arange(steps) / max(attack * sr, 1.0), 0.0, 1.0)
    rng = np.random.default_rng(seed)
    noise = 1e-4 * rng.standard_normal(steps)                       # breath is never perfectly smooth
    r = bore.reflection(taps, sr)
    p, u = _reed(steps, r, g, zeta, noise)
    return {"p": p, "u": u, "gamma": g, "sr": sr, "sound": radiate(bore, p, sr)}


def radiate(bore: Bore, p: np.ndarray, sr: int = SR) -> np.ndarray:
    """The sound outside, from the pressure in the mouthpiece: through the bore's transfer function."""
    n = len(p)
    f = np.fft.rfftfreq(n, 1.0 / sr)
    h = bore.transfer(np.maximum(f, 1.0))
    h[f < 30.0] = 0.0
    h = h * 0.5 * (1 + np.cos(np.pi * np.clip((f - 0.3 * sr) / (0.15 * sr), 0, 1)))
    y = np.fft.irfft(np.fft.rfft(p) * h, n)
    return y / max(np.abs(y).max(), 1e-12)


def playing(p: np.ndarray, sr: int = SR, tail: float = 0.3) -> dict:
    """What a simulated note settled into: its frequency (by autocorrelation), its size, and the strengths of its
    first ten harmonics in dB relative to the first."""
    x = np.asarray(p, dtype=float)[-int(tail * sr):]
    x = x - x.mean()
    amp = float(np.sqrt(np.mean(x * x)))
    if amp < 1e-4:
        return {"hz": 0.0, "amp": amp, "harmonics_db": [-120.0] * 10}
    n = len(x)
    spec = np.abs(np.fft.rfft(x * np.hanning(n), 8 * n))
    ac = np.fft.irfft(np.abs(np.fft.rfft(x, 2 * n)) ** 2)[: n // 2]
    lo = int(sr / 3000.0)
    k = lo + int(np.argmax(ac[lo:]))
    # the first strong peak, not a multiple of the period
    for cand in range(lo + 1, k):
        if ac[cand] > 0.9 * ac[k] and ac[cand] >= ac[cand - 1] and ac[cand] >= ac[cand + 1]:
            k = cand
            break
    a, b, c = ac[k - 1], ac[k], ac[k + 1]
    hz = sr / (k + (0.5 * (a - c) / (a - 2 * b + c) if abs(a - 2 * b + c) > 1e-300 else 0.0))
    if not (20.0 < hz < 5000.0):
        return {"hz": 0.0, "amp": amp, "harmonics_db": [-120.0] * 10}
    df = sr / (8 * n)
    levels = []
    for h in range(1, 11):
        i = int(round(h * hz / df))
        w = max(int(0.03 * hz / df), 2)
        levels.append(float(spec[max(i - w, 0): i + w + 1].max()) if 0 < i and i + w < len(spec) else 0.0)
    ref = max(levels[0], 1e-12)
    return {"hz": float(hz), "amp": amp, "harmonics_db": [float(20 * math.log10(max(v, 1e-12) / ref)) for v in levels]}


# ---------------------------------------------------------------------------
# Lips: a valve that the pressure opens
# ---------------------------------------------------------------------------
@njit(cache=True)
def _lips(steps, r, pm, f_lip, q, mu, h0, w, sr, noise):
    n = len(r)
    hist = np.zeros(n)
    p_out = np.empty(steps)
    h_out = np.empty(steps)
    head = 0
    x, v = 0.0, 0.0
    dt = 1.0 / sr
    p = 0.0
    for s in range(steps):
        ph = 0.0
        for k in range(1, n):
            ph += r[k] * hist[(head - k + 1) % n]
        om = 2 * math.pi * f_lip[s]
        # the lip: a mass on a spring, pushed open by the pressure in the mouth and shut by the pressure in the cup
        acc = om * om * (mu * (pm[s] - p) - x) - (om / q) * v
        v += acc * dt
        x += v * dt
        h = h0 + x
        if h < 0.0:
            h = 0.0
        # the flow through the opening (Bernoulli), with p = ph + u: a quadratic in sqrt(pm - p)
        a = w * h
        d0 = pm[s] - ph
        if d0 >= 0:
            sq = 0.5 * (-a + math.sqrt(a * a + 4.0 * d0))
            u = a * sq
        else:
            sq = 0.5 * (-a + math.sqrt(a * a - 4.0 * d0))
            u = -a * sq
        u += noise[s]
        p = ph + u
        p_out[s] = p
        h_out[s] = h
        head = (head + 1) % n
        hist[head] = p + u
    return p_out, h_out


def lip_tone(bore: Bore, f_lip, seconds: float = 1.0, pressure: float = 1.0, q: float = 6.0, mu: float = 0.1, h0: float = 0.0, w: float = 3.0,
             sr: int = SR, attack: float = 0.04, seed: int = 0, taps: int = 8192) -> dict:
    """Buzz lips on a bore.  The lips are one mass on a spring with its own frequency ``f_lip`` (a number or an
    array: the player's embouchure), blown open by the mouth pressure; the flow through them obeys Bernoulli.  In
    scaled units (pressure in units of the mouth pressure asked for, flow in that over the bore's impedance)."""
    steps = int(seconds * sr)
    fl = np.full(steps, float(f_lip)) if np.isscalar(f_lip) else np.asarray(f_lip, dtype=float)[:steps]
    pm = pressure * np.clip(np.arange(steps) / max(attack * sr, 1.0), 0.0, 1.0)
    rng = np.random.default_rng(seed)
    noise = 1e-4 * rng.standard_normal(steps)
    r = bore.reflection(taps, sr)
    p, h = _lips(steps, r, pm, fl, q, mu, h0, w, float(sr), noise)
    return {"p": p, "h": h, "sr": sr, "sound": radiate(bore, p, sr)}


# ---------------------------------------------------------------------------
# A jet
# ---------------------------------------------------------------------------
@njit(cache=True)
def _jet(steps, n_bore, delay, strength, noise, gain, g_end, a_end, smooth, offset):
    n_jet = int(delay.max()) + 3
    bore = np.zeros(n_bore)
    jet = np.zeros(n_jet)
    out = np.empty(steps)
    ib, ij = 0, 0
    lp, dl = 0.0, 0.0
    t_off = math.tanh(offset)
    for s in range(steps):
        back = bore[ib]                                  # the wave that left one round trip ago: turned over at each open end
        lp = (1.0 - a_end) * back + a_end * lp           # and a little of it, mostly the high frequencies, lost outside
        ret = g_end * lp
        jet[ij] = ret                                    # the air moving in the mouth hole pushes the jet aside ...
        pos = ij - delay[s]                              # ... and the push takes time to ride the jet across to the edge
        while pos < 0:
            pos += n_jet
        i0 = int(pos)
        frac = pos - i0
        d = (1.0 - frac) * jet[i0 % n_jet] + frac * jet[(i0 + 1) % n_jet]
        ij += 1
        if ij == n_jet:
            ij = 0
        aj = math.exp(-1.0 / (smooth * delay[s]))        # a jet carries slow wiggles; fast ones wash out on the way
        dl = (1.0 - aj) * d + aj * dl
        y = -strength[s] * (math.tanh(gain * dl + noise[s] + offset) - t_off)   # which side of the edge it goes: in, or out
        bore[ib] = ret + y
        ib += 1
        if ib == n_bore:
            ib = 0
        out[s] = ret + y
    return out


def jet_tone(hz: float, seconds: float = 1.0, pressure=1.0, sr: int = SR, noise: float = 0.03, attack: float = 0.05, seed: int = 0,
             gain: float = 3.0, smooth: float = 0.25, travel: float = 0.4, offset: float = 0.3) -> np.ndarray:
    """A flute, schematically (after Coltman, and McIntyre, Schumacher and Woodhouse).  The pipe is open at both
    ends: a loop of delay one period long.  The player's jet crosses the mouth hole to an edge; the air moving in
    the hole pushes the jet aside, the push rides along the jet, and when it arrives the jet flips into the pipe or
    out of it (a little more one way than the other, since the edge is never quite central).  The flip feeds the
    pipe at the right moment when the jet's travel time is a little under half a period.
    ``pressure`` is the blowing pressure (1 is normal; a number or an array): the jet's speed goes as its square
    root, so blowing harder shortens the travel time, and the pipe's octave, whose half period is shorter, takes
    over."""
    from scipy.signal import firwin, lfilter

    n_bore = max(int(round(4 * sr / hz - 0.67)), 8)                  # stepped four times as finely as the sound is sampled,
    sr_sim = hz * (n_bore + 0.67)                                    # at a rate that makes the loop a whole number of steps
    steps = int(seconds * sr_sim)
    if np.isscalar(pressure):
        pr = np.full(steps, float(pressure))
    else:
        pa = np.asarray(pressure, dtype=float)
        pr = np.interp(np.arange(steps) / sr_sim, np.arange(len(pa)) / sr, pa)
    delay = travel * n_bore / np.sqrt(np.maximum(pr, 0.05))
    rng = np.random.default_rng(seed)
    ramp = np.clip(np.arange(steps) / max(attack * sr_sim, 1.0), 0.0, 1.0)
    strength = 0.25 * np.sqrt(np.maximum(pr, 0.0)) * ramp
    y = _jet(steps, n_bore, delay, strength, noise * rng.standard_normal(steps), gain, 0.97, 0.4, smooth, offset)
    taps = firwin(63, 0.45 * sr, fs=sr_sim)
    y = lfilter(taps, 1.0, np.concatenate([y, np.zeros(31)]))[31:]
    return np.interp(np.arange(int(seconds * sr)) / sr, np.arange(len(y)) / sr_sim, y)


def jet_delay(pressure: float, travel: float = 0.4) -> float:
    """The jet's travel time as a fraction of the pipe's fundamental period."""
    return travel / math.sqrt(max(pressure, 0.05))


# ---------------------------------------------------------------------------
# The voice
# ---------------------------------------------------------------------------
VOWELS = {  # Peterson and Barney (1952): average formants of 33 men, Hz
    "i": (270, 2290, 3010), "I": (390, 1990, 2550), "E": (530, 1840, 2480), "ae": (660, 1720, 2410), "a": (730, 1090, 2440),
    "O": (570, 840, 2410), "U": (440, 1020, 2240), "u": (300, 870, 2240), "V": (640, 1190, 2390), "er": (490, 1350, 1690),
}
VOWEL_WORDS = {"i": "heed", "I": "hid", "E": "head", "ae": "had", "a": "hod", "O": "hawed", "U": "hood", "u": "who'd", "V": "hud", "er": "heard"}


def glottal_pulse(hz, seconds: float, sr: int = SR, open_quotient: float = 0.6, speed: float = 2.0, jitter: float = 0.004, shimmer: float = 0.02,
                  breath: float = 0.01, seed: int = 0) -> np.ndarray:
    """The flow through the vocal folds (Rosenberg's pulse): in each period the folds part, the flow rises, falls
    faster than it rose, and stops while the folds are closed.  ``hz`` may vary in time.  A little jitter, shimmer
    and breath keep it from sounding like a machine."""
    n = int(seconds * sr)
    f = np.full(n, float(hz)) if np.isscalar(hz) else np.asarray(hz, dtype=float)[:n]
    rng = np.random.default_rng(seed)
    out = np.zeros(n)
    t = 0.0
    while True:
        i0 = int(t)
        if i0 >= n:
            break
        period = sr / (f[i0] * (1 + jitter * rng.standard_normal()))
        amp = 1 + shimmer * rng.standard_normal()
        n_open = open_quotient * period
        n_rise = n_open * speed / (1 + speed)
        n_fall = n_open - n_rise
        k = np.arange(i0, min(int(t + n_open) + 1, n))
        x = k - t
        rise = x < n_rise
        out[k] = amp * np.where(rise, 0.5 * (1 - np.cos(np.pi * x / n_rise)), np.cos(0.5 * np.pi * np.clip((x - n_rise) / n_fall, 0, 1)))
        t += period
    out += breath * rng.standard_normal(n) * (0.3 + out)
    return out


def formant_filter(x: np.ndarray, formants, bandwidths=None, sr: int = SR) -> np.ndarray:
    """A chain of two-pole resonators, one for each formant (Klatt's cascade); each has unit gain at zero frequency.
    ``formants`` is a list of frequencies, or of arrays for formants that move."""
    y = np.asarray(x, dtype=float).copy()
    n = len(y)
    for j, f in enumerate(formants):
        fa = np.full(n, float(f)) if np.isscalar(f) else np.asarray(f, dtype=float)[:n]
        bw = (50.0 + f_mean(fa) / 20.0) if bandwidths is None else bandwidths[j]
        ba = np.full(n, float(bw)) if np.isscalar(bw) else np.asarray(bw, dtype=float)[:n]
        y = _resonator(y, fa, ba, float(sr))
    return y


def f_mean(a) -> float:
    return float(np.mean(a))


@njit(cache=True)
def _resonator(x, f, bw, sr):
    y = np.empty(len(x))
    y1, y2 = 0.0, 0.0
    for i in range(len(x)):
        r = math.exp(-math.pi * bw[i] / sr)
        c = -r * r
        b = 2.0 * r * math.cos(2.0 * math.pi * f[i] / sr)
        a = 1.0 - b - c
        v = a * x[i] + b * y1 + c * y2
        y2 = y1
        y1 = v
        y[i] = v
    return y


def voice(hz, formants, seconds: float, sr: int = SR, bandwidths=None, higher=(3500.0, 4500.0), seed: int = 0, **source) -> np.ndarray:
    """A sung vowel: the pulses of the folds, through the formants of the tract, and out of the mouth (which favours
    high frequencies: a difference)."""
    g = glottal_pulse(hz, seconds, sr, seed=seed, **source)
    y = formant_filter(g, list(formants) + list(higher), bandwidths, sr)
    y = np.diff(y, prepend=y[0])
    return y / max(np.abs(y).max(), 1e-12)


def spectrum_envelope(formants, f, bandwidths=None, higher=(3500.0, 4500.0), sr: int = SR) -> np.ndarray:
    """The gain (dB) of the formant chain at the frequencies ``f``."""
    f = np.asarray(f, dtype=float)
    z = np.exp(-2j * np.pi * f / sr)
    h = np.ones(len(f), dtype=complex)
    for j, fk in enumerate(list(formants) + list(higher)):
        bw = (50.0 + fk / 20.0) if bandwidths is None or j >= len(bandwidths) else bandwidths[j]
        r = math.exp(-math.pi * bw / sr)
        b, c = 2 * r * math.cos(2 * math.pi * fk / sr), -r * r
        h *= (1 - b - c) / (1 - b * z - c * z * z)
    return 20 * np.log10(np.abs(h))


def tract(areas_cm2, section_cm: float) -> Bore:
    """A vocal tract as a tube from the folds (closed) to the lips (open): ``areas_cm2`` are its cross-sections in
    order, each ``section_cm`` long."""
    b = Bore(end="open")
    for a in areas_cm2:
        b.tube(section_cm / 100.0, math.sqrt(a * 1e-4 / math.pi))
    return b


def tract_formants(bore: Bore, count: int = 3, f_max: float = 4500.0) -> list[float]:
    """The formants of a tube closed at the folds: the frequencies at which a flow at the closed end produces the
    most flow at the lips, which are the peaks of the input impedance seen from the folds."""
    return [p[0] for p in bore.peaks(f_max, df=1.0)][:count]


TWO_TUBE = {  # Fant's two-tube vowels: (back area, back length, front area, front length), cm2 and cm
    "neutral": (4.0, 8.75, 4.0, 8.75),
    "a": (1.0, 9.0, 9.0, 9.0),          # a narrow throat opening into a wide mouth
    "i": (8.0, 7.5, 1.0, 5.5),          # a wide throat behind a narrow gap at the palate
}


def two_tube(name: str) -> Bore:
    a1, l1, a2, l2 = TWO_TUBE[name]
    return tract([a1] * 1, l1).tube(l2 / 100.0, math.sqrt(a2 * 1e-4 / math.pi))


def overtone_formants(harmonic: int, drone: float) -> tuple[float, float, float]:
    """The tract of an overtone singer on one note: the second and third formants drawn together onto one harmonic
    of the drone, the first kept low and out of the way."""
    f = harmonic * drone
    return (min(0.45 * f, 420.0), f * 0.985, f * 1.015)
