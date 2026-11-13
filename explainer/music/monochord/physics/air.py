"""Air: the second layer of Monochord (Part 2, *Waves in Air*).

Three simulators, each checked against something that does not share its code (``tests/music/test_air.py``):

* :func:`gas_chain`: a row of parcels of gas that push on each other through the gas law, with no wave equation in
  it.  Small disturbances travel at ``sqrt(gamma P / rho)`` (Laplace) or ``sqrt(P / rho)`` (Newton) according to
  the law the gas is given; large ones steepen, as the Fubini solution says they must.
* :func:`fdtd2d`: sound in a plane (pressure and velocity on a staggered grid, rigid walls, a sponge at the edge):
  spreading, diffraction, interference, a moving source.
* :func:`tube`: sound in a tube whose cross-section may vary (Webster's equation): open and stopped pipes, a
  bottle, and, with the area growing as the square of the distance, the spherical wave of a point source.

Units are SI throughout: pascals, metres, seconds, kilograms.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

try:  # the loops below are compiled when numba is there; they are the same loops without it
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap(a[0]) if a and callable(a[0]) else wrap

P_ATM = 101_325.0          # one standard atmosphere, Pa
GAMMA = 1.4                # ratio of specific heats of dry air
R_AIR = 287.05             # specific gas constant of dry air, J / (kg K)
KELVIN = 273.15
P_REF = 20e-6              # the reference pressure of the decibel (SPL), Pa rms
I_REF = 1e-12              # the reference intensity, W / m^2


def density(celsius: float = 20.0, pressure: float = P_ATM) -> float:
    """The density of dry air from the gas law."""
    return pressure / (R_AIR * (celsius + KELVIN))


def speed(celsius: float = 20.0, law: str = "adiabatic") -> float:
    """The speed of sound: Laplace's ``sqrt(gamma P / rho)``, or Newton's ``sqrt(P / rho)`` with ``law="isothermal"``."""
    g = GAMMA if law == "adiabatic" else 1.0
    return math.sqrt(g * R_AIR * (celsius + KELVIN))


def impedance(celsius: float = 20.0) -> float:
    """The characteristic impedance of air, rho c, in rayl (Pa s / m)."""
    return density(celsius) * speed(celsius)


def spl(p_rms: float) -> float:
    """Sound pressure level in decibels re 20 micropascals."""
    return 20.0 * math.log10(max(p_rms, 1e-30) / P_REF)


def pressure_of(spl_db: float) -> float:
    """The rms pressure of a level in dB SPL."""
    return P_REF * 10 ** (spl_db / 20.0)


def intensity(p_rms: float, celsius: float = 20.0) -> float:
    """The intensity of a plane wave of rms pressure ``p_rms``, W / m^2."""
    return p_rms ** 2 / impedance(celsius)


# ---------------------------------------------------------------------------
# A row of parcels: the gas law and Newton's second law, nothing else
# ---------------------------------------------------------------------------
@njit(cache=True)
def _chain_loop(x, v, h, m, p0, expo, dt, steps, piston_v, probes, out, snap_every, snaps):
    n = len(x)
    k = 0
    for s in range(steps):
        # the wall on the left moves as it is told; the wall on the right stands still
        v[0] = piston_v[s]
        v[n - 1] = 0.0
        for i in range(1, n - 1):
            left = p0 * (h / (x[i] - x[i - 1])) ** expo
            right = p0 * (h / (x[i + 1] - x[i])) ** expo
            v[i] += dt * (left - right) / m
        for i in range(n):
            x[i] += dt * v[i]
        for j in range(len(probes)):
            out[j, s] = v[probes[j]]
        if snap_every > 0 and s % snap_every == 0 and k < snaps.shape[0]:
            for i in range(n):
                snaps[k, i] = x[i] - i * h
            k += 1
    return k


@dataclass
class ChainRun:
    h: float
    dt: float
    probes: np.ndarray          # indices of the parcels whose velocity was recorded
    velocity: np.ndarray        # (len(probes), steps)
    snaps: np.ndarray           # (frames, parcels): each parcel's displacement from rest
    snap_dt: float


def gas_chain(length: float, n: int, piston, seconds: float, law: str = "adiabatic", celsius: float = 0.0,
              probes=(), snapshot_every: int = 0, courant: float = 0.4) -> ChainRun:
    """Parcels of air in a tube of unit cross-section, ``n`` walls ``length / (n - 1)`` apart at rest.

    Each wall has the mass of the air between two walls; the gas between neighbours pushes them apart with the
    pressure ``P (h / gap) ** gamma`` (``gamma = 1`` for ``law="isothermal"``: Boyle's law).  The first wall is a
    piston whose velocity is ``piston(t)`` (m/s); the last is fixed.  There is no speed of sound in this code."""
    expo = GAMMA if law == "adiabatic" else 1.0
    rho = density(celsius)
    h = length / (n - 1)
    c = math.sqrt(GAMMA * P_ATM / rho)           # only to choose a safe time step
    dt = courant * h / c
    steps = int(round(seconds / dt))
    t = np.arange(steps) * dt
    pv = np.asarray([piston(tt) for tt in t], dtype=np.float64) if callable(piston) else np.asarray(piston, float)
    x = np.arange(n, dtype=np.float64) * h
    v = np.zeros(n)
    probes = np.asarray(probes, dtype=np.int64)
    out = np.zeros((len(probes), steps))
    frames = steps // snapshot_every + 1 if snapshot_every else 0
    snaps = np.zeros((frames, n))
    k = _chain_loop(x, v, h, rho * h, P_ATM, expo, dt, steps, pv, probes, out, snapshot_every, snaps)
    return ChainRun(h=h, dt=dt, probes=probes, velocity=out, snaps=snaps[:k], snap_dt=dt * max(snapshot_every, 1))


def fubini(n: int, sigma: float) -> float:
    """The amplitude of harmonic ``n`` of a sine wave that has travelled the fraction ``sigma`` of its shock
    distance, relative to the amplitude it started with (Fubini, 1935): ``2 J_n(n sigma) / (n sigma)``."""
    from scipy.special import jv

    return 1.0 if (sigma == 0 and n == 1) else (0.0 if sigma == 0 else 2.0 * jv(n, n * sigma) / (n * sigma))


def shock_distance(u0: float, hz: float, celsius: float = 20.0) -> float:
    """How far a sine wave of particle-velocity amplitude ``u0`` travels before it first becomes vertical:
    ``c^2 / (beta omega u0)`` with ``beta = (gamma + 1) / 2``."""
    c = speed(celsius)
    return c * c / (0.5 * (GAMMA + 1.0) * 2 * math.pi * hz * u0)


# ---------------------------------------------------------------------------
# Sound in a plane
# ---------------------------------------------------------------------------
@dataclass
class Field2D:
    h: float
    dt: float
    c: float
    shape: tuple
    receivers: np.ndarray       # (n_receivers, steps): pressure
    snaps: np.ndarray           # (frames, ny', nx'): pressure, coarsened by ``snap_stride``
    snap_dt: float
    snap_stride: int
    solid: np.ndarray           # the walls, on the full grid

    def cell(self, x: float, y: float) -> tuple[int, int]:
        """The grid cell (row, column) of a point in metres; the origin is the bottom-left corner."""
        return int(round(y / self.h)), int(round(x / self.h))


def fdtd2d(width: float, height: float, h: float, seconds: float, sources=(), solid=None, receivers=(),
           snapshot_every: int = 0, snap_stride: int = 1, celsius: float = 20.0, sponge: int = 24,
           courant: float = 0.5, moving=None) -> Field2D:
    """Linear sound in a rectangle ``width`` by ``height`` metres on a grid of step ``h``.

    Pressure sits at cell centres and the two velocity components on the cell faces (a staggered grid).  ``solid``
    is a boolean array of rigid cells, or a function ``solid(X, Y)`` of the cell-centre coordinates: no air crosses
    their faces.  The outer ``sponge`` cells soak up what reaches them, so the rectangle behaves as open space.
    ``sources`` is a list of ``(x, y, fn)`` with ``fn(t)`` the rate at which air is pumped in at that point (any
    units: the field is linear); ``moving`` is ``(path, fn)`` with ``path(t) -> (x, y)`` for a source that travels.
    ``receivers`` is a list of ``(x, y)``."""
    c = speed(celsius)
    rho = density(celsius)
    nx, ny = int(round(width / h)), int(round(height / h))
    dt = courant * h / c
    steps = int(round(seconds / dt))
    xs = (np.arange(nx) + 0.5) * h
    ys = (np.arange(ny) + 0.5) * h
    X, Y = np.meshgrid(xs, ys)
    if solid is None:
        mask = np.zeros((ny, nx), dtype=bool)
    elif callable(solid):
        mask = np.asarray(solid(X, Y), dtype=bool)
    else:
        mask = np.asarray(solid, dtype=bool)
    p = np.zeros((ny, nx))
    vx = np.zeros((ny, nx + 1))
    vy = np.zeros((ny + 1, nx))
    # faces that touch a wall carry no flow
    open_x = np.ones_like(vx, dtype=bool)
    open_x[:, 1:-1] = ~(mask[:, 1:] | mask[:, :-1])
    open_x[:, 0] = open_x[:, -1] = False
    open_y = np.ones_like(vy, dtype=bool)
    open_y[1:-1, :] = ~(mask[1:, :] | mask[:-1, :])
    open_y[0, :] = open_y[-1, :] = False
    # the sponge: a damping that grows towards the edge
    d = np.minimum.reduce([np.arange(nx)[None, :] + 0 * Y, (nx - 1 - np.arange(nx))[None, :] + 0 * Y,
                           np.arange(ny)[:, None] + 0 * X, (ny - 1 - np.arange(ny))[:, None] + 0 * X])
    damp = np.where(d < sponge, ((sponge - d) / max(sponge, 1)) ** 2, 0.0) * (0.35 * c / h) if sponge else 0.0 * X
    keep = np.exp(-damp * dt)
    a_v = dt / (rho * h)
    a_p = rho * c * c * dt / h
    src = [(int(y / h), int(x / h), fn) for x, y, fn in sources]
    rec = [(int(y / h), int(x / h)) for x, y in receivers]
    out = np.zeros((len(rec), steps))
    frames = []
    for s in range(steps):
        t = s * dt
        vx[:, 1:-1] -= a_v * (p[:, 1:] - p[:, :-1])
        vy[1:-1, :] -= a_v * (p[1:, :] - p[:-1, :])
        vx *= open_x
        vy *= open_y
        p -= a_p * ((vx[:, 1:] - vx[:, :-1]) + (vy[1:, :] - vy[:-1, :]))
        for j, i, fn in src:
            p[j, i] += fn(t) * dt
        if moving is not None:
            path, fn = moving
            mx, my = path(t)
            fx, fy = mx / h - 0.5, my / h - 0.5
            i0, j0 = int(math.floor(fx)), int(math.floor(fy))
            ax, ay = fx - i0, fy - j0
            q = fn(t) * dt
            if 0 <= i0 < nx - 1 and 0 <= j0 < ny - 1:      # shared among the four nearest cells
                p[j0, i0] += q * (1 - ax) * (1 - ay)
                p[j0, i0 + 1] += q * ax * (1 - ay)
                p[j0 + 1, i0] += q * (1 - ax) * ay
                p[j0 + 1, i0 + 1] += q * ax * ay
        p *= keep
        p[mask] = 0.0
        for k, (j, i) in enumerate(rec):
            out[k, s] = p[j, i]
        if snapshot_every and s % snapshot_every == 0:
            frames.append(p[::snap_stride, ::snap_stride].astype(np.float32))
    return Field2D(h=h, dt=dt, c=c, shape=(ny, nx), receivers=out, snaps=np.array(frames),
                   snap_dt=dt * max(snapshot_every, 1), snap_stride=snap_stride, solid=mask)


def ricker(f0: float, delay: float | None = None):
    """A short pulse with most of its energy round ``f0`` (the second derivative of a Gaussian), as ``fn(t)``."""
    t0 = 1.5 / f0 if delay is None else delay

    def fn(t):
        a = (math.pi * f0 * (t - t0)) ** 2
        return (1 - 2 * a) * math.exp(-a)

    return fn


def tone_burst(hz: float, ramp: float = 2.0):
    """A sine that fades in over ``ramp`` periods, as ``fn(t)``."""
    def fn(t):
        return math.sin(2 * math.pi * hz * t) * min(1.0, t * hz / ramp)

    return fn


# ---------------------------------------------------------------------------
# Sound in a tube of varying cross-section (Webster's equation)
# ---------------------------------------------------------------------------
@njit(cache=True)
def _tube_loop(p, U, S, Sf, a_p, a_u, steps, drive, where, left_open, right_open, r_left, r_right, loss, out_u, out_p,
               probe, snap_every, snaps):
    n = len(p)
    k = 0
    for s in range(steps):
        for i in range(1, n):
            U[i] = (U[i] - a_u * Sf[i] * (p[i] - p[i - 1])) * loss
        # an open end: the pressure just outside is what the air there pushes back with (a small resistance
        # stands for the sound that is radiated); a closed end lets nothing through
        if left_open:
            U[0] = (U[0] - 2 * a_u * Sf[0] * p[0]) / (1 + 2 * a_u * Sf[0] * r_left)
        else:
            U[0] = 0.0
        if right_open:
            U[n] = (U[n] + 2 * a_u * Sf[n] * p[n - 1]) / (1 + 2 * a_u * Sf[n] * r_right)
        else:
            U[n] = 0.0
        for i in range(n):
            p[i] -= a_p * (U[i + 1] - U[i]) / S[i]
        p[where] += drive[s]
        out_u[s] = U[n] if right_open else U[0]
        out_p[s] = p[probe]
        if snap_every > 0 and s % snap_every == 0 and k < snaps.shape[0]:
            for i in range(n):
                snaps[k, i] = p[i]
            k += 1
    return k


@dataclass
class TubeRun:
    h: float
    dt: float
    x: np.ndarray               # cell centres
    flow: np.ndarray            # volume velocity out of the open end (the right one if both are open)
    pressure: np.ndarray        # pressure at the probe
    snaps: np.ndarray
    snap_dt: float
    sr: float = field(default=0.0)

    @property
    def radiated(self) -> np.ndarray:
        """What a listener outside hears, up to a constant: the rate of change of the flow out of the mouth."""
        return np.gradient(self.flow, self.dt)


def tube(area, length: float, seconds: float, drive, where: float = 0.0, left: str = "closed", right: str = "open",
         sr: float = 96_000.0, celsius: float = 20.0, q_loss: float = 0.0, radiation: float = 0.0, probe: float = 0.0,
         snapshot_every: int = 0, n: int | None = None) -> TubeRun:
    """Plane waves in a tube ``length`` long whose cross-section at ``x`` is ``area(x)`` (a number for a plain pipe).

    ``left`` and ``right`` are ``"open"`` or ``"closed"``.  ``drive`` is ``fn(t)`` or an array (one value per
    step): pressure added per step at the cell nearest ``where``.  ``radiation`` is the resistance met by the flow
    at an open end, as a fraction of the tube's own impedance ``rho c / S`` there (0: an ideal open end, which
    radiates nothing); ``q_loss`` is the fraction of the flow lost per second to the walls."""
    c = speed(celsius)
    rho = density(celsius)
    dt = 1.0 / sr
    if n is None:
        n = max(8, int(math.floor(length / (c * dt / 0.98))))    # Courant number just under one
    h = length / n
    if c * dt / h > 1.0:
        raise ValueError(f"{n} cells in {length} m need a sample rate above {c / h:.0f} Hz (got {sr:.0f})")
    x = (np.arange(n) + 0.5) * h
    xf = np.arange(n + 1) * h
    fn = area if callable(area) else (lambda _x: float(area))
    S = np.array([fn(v) for v in x], dtype=np.float64)
    Sf = np.array([fn(min(max(v, 0.5 * h), length - 0.5 * h)) for v in xf], dtype=np.float64)
    Sf[1:-1] = 2.0 / (1.0 / S[1:] + 1.0 / S[:-1])              # two cells in series share a face
    steps = int(round(seconds * sr))
    t = np.arange(steps) * dt
    d = np.asarray([drive(v) for v in t], dtype=np.float64) if callable(drive) else np.asarray(drive, float)[:steps]
    if len(d) < steps:
        d = np.concatenate([d, np.zeros(steps - len(d))])
    p = np.zeros(n)
    U = np.zeros(n + 1)
    frames = steps // snapshot_every + 1 if snapshot_every else 0
    snaps = np.zeros((frames, n))
    out_u = np.zeros(steps)
    out_p = np.zeros(steps)
    z_l, z_r = rho * c / Sf[0], rho * c / Sf[-1]
    k = _tube_loop(p, U, S, Sf, rho * c * c * dt / h, dt / (rho * h), steps, d, int(min(n - 1, where / h)),
                   left == "open", right == "open", radiation * z_l, radiation * z_r, math.exp(-q_loss * dt), out_u,
                   out_p, int(min(n - 1, probe / h)), snapshot_every, snaps)
    return TubeRun(h=h, dt=dt, x=x, flow=out_u, pressure=out_p, snaps=snaps[:k],
                   snap_dt=dt * max(snapshot_every, 1), sr=sr)


def pipe_modes(length: float, count: int = 6, stopped: bool = False, celsius: float = 20.0) -> np.ndarray:
    """The resonances of an ideal pipe: ``n c / 2L`` open at both ends, ``(2n - 1) c / 4L`` stopped at one."""
    c = speed(celsius)
    k = np.arange(1, count + 1)
    return (2 * k - 1) * c / (4 * length) if stopped else k * c / (2 * length)


def helmholtz(neck_area: float, neck_length: float, volume: float, celsius: float = 20.0) -> float:
    """Helmholtz's resonator: the air in the neck as a mass, the air in the body as its spring."""
    return speed(celsius) / (2 * math.pi) * math.sqrt(neck_area / (volume * neck_length))


def bottle_exact(neck_area: float, neck_length: float, body_area: float, body_length: float,
                 celsius: float = 20.0) -> float:
    """The lowest resonance of a neck on a body, both treated as tubes: the smallest root of
    ``tan(k L_neck) tan(k L_body) = neck_area / body_area``.  Helmholtz's formula is its long-wavelength limit."""
    from scipy.optimize import brentq

    c = speed(celsius)
    ratio = neck_area / body_area

    def g(k):
        return math.tan(k * neck_length) * math.tan(k * body_length) - ratio

    k_hi = 0.999 * (math.pi / 2) / max(neck_length, body_length)
    return c * brentq(g, 1e-6, k_hi) / (2 * math.pi)


def resonances(y: np.ndarray, sr: float, count: int = 6, fmin: float = 20.0, fmax: float | None = None,
               sep: float = 40.0, floor: float = 0.03) -> np.ndarray:
    """The frequencies of the strongest peaks in the spectrum of a response, lowest first.  A peak within ``sep``
    hertz of a stronger one is a side lobe of it and is dropped; each survivor is refined by a parabola."""
    n = 1 << int(math.ceil(math.log2(len(y) * 4)))
    spec = np.abs(np.fft.rfft(y * np.hanning(len(y)), n))
    hz = np.fft.rfftfreq(n, 1 / sr)
    lo, hi = np.searchsorted(hz, fmin), np.searchsorted(hz, fmax or sr / 2 * 0.9)
    peaks = [i for i in range(max(lo, 1), min(hi, len(spec) - 1)) if spec[i] > spec[i - 1] and spec[i] >= spec[i + 1]]
    top = max((spec[i] for i in peaks), default=0.0)
    kept = []
    for i in sorted(peaks, key=lambda j: -spec[j]):
        if spec[i] < floor * top:
            break
        if all(abs(hz[i] - hz[j]) > sep for j in kept):
            kept.append(i)
    out = []
    for i in kept:
        a, b, cc = np.log(spec[i - 1] + 1e-300), np.log(spec[i] + 1e-300), np.log(spec[i + 1] + 1e-300)
        out.append(hz[i] + 0.5 * (a - cc) / (a - 2 * b + cc) * (hz[1] - hz[0]))
    return np.array(sorted(out)[:count])


# ---------------------------------------------------------------------------
# A source that moves (Doppler), by the time the sound left it
# ---------------------------------------------------------------------------
def passing_source(hz: float, v: float, closest: float, seconds: float, sr: int = 48_000, celsius: float = 20.0,
                   harmonics=(1.0,)) -> tuple[np.ndarray, np.ndarray]:
    """What a listener hears from a source of frequency ``hz`` moving in a straight line at ``v`` m/s that passes
    ``closest`` metres away at the middle of the clip.  Returns ``(signal, heard_frequency)``.

    For each instant at the listener the instant the sound left the source is found exactly (a quadratic), the
    source's phase then is what is heard, and the amplitude falls as one over the distance it travelled."""
    c = speed(celsius)
    t = np.arange(int(seconds * sr)) / sr - seconds / 2
    # the source is at x = v * te; sound emitted at te arrives at t = te + sqrt((v te)^2 + d^2) / c
    a = 1 - (v / c) ** 2
    te = (t - np.sqrt((t * v / c) ** 2 + a * (closest / c) ** 2)) / a if a != 1 else t - closest / c
    r = np.sqrt((v * te) ** 2 + closest ** 2)
    y = sum(w * np.sin(2 * math.pi * hz * (k + 1) * te) for k, w in enumerate(harmonics))
    heard = hz * np.gradient(te, 1 / sr)
    return y * (closest / r), heard


def doppler(hz: float, v: float, celsius: float = 20.0) -> tuple[float, float]:
    """The frequency heard from a source coming straight at the listener, and going straight away."""
    c = speed(celsius)
    return hz * c / (c - v), hz * c / (c + v)
