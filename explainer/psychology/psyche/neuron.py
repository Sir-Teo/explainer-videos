"""The neuron: Psyche's smallest moving part (videos/psychology/SYLLABUS.md, Part 5).

Everything a membrane does in the film is computed here, in the order the part builds it.

**Ions.**  An ion at concentrations ``out`` and ``inn`` sits in equilibrium at the Nernst potential, and several
ions with permeabilities ``P`` settle at the Goldman-Hodgkin-Katz voltage:

    E = (R T / z F) ln(out / inn)                                         (mV, with RT/F in mV)
    V = (R T / F) ln( (P_K K_o + P_Na Na_o + P_Cl Cl_i) / (P_K K_i + P_Na Na_i + P_Cl Cl_o) )

**The membrane as a circuit.**  A capacitance ``C`` in parallel with a leak ``R`` charges as
``V(t) = I R (1 - exp(-t / RC))``.

**Hodgkin and Huxley (1952).**  With V in mV (rest near -65), t in ms, currents in uA/cm^2, conductances in
mS/cm^2 and C = 1 uF/cm^2:

    C dV/dt = I - g_Na m^3 h (V - E_Na) - g_K n^4 (V - E_K) - g_L (V - E_L)
    dx/dt   = phi [ alpha_x(V) (1 - x) - beta_x(V) x ]      for x in m, h, n;    phi = 3^((T - 6.3) / 10)

    alpha_m = 0.1 (V + 40) / (1 - exp(-(V + 40) / 10))      beta_m = 4 exp(-(V + 65) / 18)
    alpha_h = 0.07 exp(-(V + 65) / 20)                      beta_h = 1 / (1 + exp(-(V + 35) / 10))
    alpha_n = 0.01 (V + 55) / (1 - exp(-(V + 55) / 10))     beta_n = 0.125 exp(-(V + 65) / 80)

    g_Na = 120, g_K = 36, g_L = 0.3;    E_Na = 50, E_K = -77, E_L = -54.4

These are the 1952 rate functions with the voltage axis shifted and reversed to the modern convention (their
V = 0 at rest and positive for hyperpolarization).  The gates are advanced by the exponential rule (exact for a
voltage held over the step) and the voltage by the same rule, so a step of 0.01 ms is ample.

**Propagation.**  On an axon of radius ``a`` and axoplasm resistivity ``R_i`` the membrane equation gains the
cable term ``(a / 2 R_i) d2V/dx2``.  :func:`propagate` solves it on a chain of compartments, implicitly in space.
With the axon of the 1952 paper (a = 238 um, R_i = 35.4 ohm cm, 18.5 C) the computed speed is close to the
18.8 m/s Hodgkin and Huxley computed by hand, against 21.2 m/s measured.

**Reductions.**  FitzHugh-Nagumo keeps a fast voltage and one slow recovery variable,

    dv/dt = v - v^3 / 3 - w + I,        dw/dt = eps (v + a - b w),          a = 0.7, b = 0.8, eps = 0.08,

and the leaky integrate-and-fire neuron keeps only the charging curve and a threshold, which gives its firing
rate in closed form:

    tau dV/dt = -(V - E_L) + R I;   spike and reset at V_th;      f = 1 / ( t_ref + tau ln( R I / (R I - (V_th - E_L)) ) )

**Codes and computation.**  Poisson spike trains and the Fano factor; a point neuron against a neuron whose
dendritic branches each apply a threshold of their own (a two-layer network in one cell).

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.linalg import solve_banded

R_GAS, FARADAY = 8.314462618, 96485.33212  # J / (mol K), C / mol

# Concentrations (mM) usually quoted for the squid giant axon and its sea-water bath.
SQUID = {"K": (20.0, 400.0), "Na": (440.0, 50.0), "Cl": (560.0, 52.0)}  # (outside, inside)


# ---------------------------------------------------------------------------------------------------------------
# Ions
# ---------------------------------------------------------------------------------------------------------------
def thermal_voltage(temp_c: float = 6.3) -> float:
    """RT/F in millivolts."""
    return 1000 * R_GAS * (temp_c + 273.15) / FARADAY


def nernst(out: float, inn: float, z: int = 1, temp_c: float = 6.3) -> float:
    """The equilibrium potential (mV, inside relative to outside) of an ion of valence ``z``."""
    return thermal_voltage(temp_c) / z * math.log(out / inn)


def goldman(p_k: float, p_na: float, p_cl: float = 0.0, conc: dict | None = None, temp_c: float = 6.3) -> float:
    """The Goldman-Hodgkin-Katz voltage (mV) for relative permeabilities to K, Na and Cl."""
    c = conc or SQUID
    num = p_k * c["K"][0] + p_na * c["Na"][0] + p_cl * c["Cl"][1]
    den = p_k * c["K"][1] + p_na * c["Na"][1] + p_cl * c["Cl"][0]
    return thermal_voltage(temp_c) * math.log(num / den)


# ---------------------------------------------------------------------------------------------------------------
# The membrane as a circuit
# ---------------------------------------------------------------------------------------------------------------
def rc_step(t, current: float, resistance: float, capacitance: float):
    """The voltage change of a leaky capacitor ``t`` after a current step: I R (1 - exp(-t / RC))."""
    return current * resistance * (1 - np.exp(-np.asarray(t, float) / (resistance * capacitance)))


# ---------------------------------------------------------------------------------------------------------------
# Hodgkin and Huxley
# ---------------------------------------------------------------------------------------------------------------
def _vtrap(x, y):
    """x / (1 - exp(-x / y)), with its limit y at x = 0."""
    x = np.asarray(x, float)
    small = np.abs(x / y) < 1e-6
    return np.where(small, y * (1 + x / y / 2), x / (1 - np.exp(-np.where(small, 1.0, x) / y)))


def rates(v) -> dict:
    """The six rate functions (per ms, at 6.3 C) at membrane potential ``v`` (mV)."""
    v = np.asarray(v, float)
    return {
        "am": 0.1 * _vtrap(v + 40, 10), "bm": 4 * np.exp(-(v + 65) / 18),
        "ah": 0.07 * np.exp(-(v + 65) / 20), "bh": 1 / (1 + np.exp(-(v + 35) / 10)),
        "an": 0.01 * _vtrap(v + 55, 10), "bn": 0.125 * np.exp(-(v + 65) / 80),
    }


def steady(v, temp_c: float = 6.3) -> dict:
    """Each gate's steady value and time constant (ms) at ``v``."""
    r, phi = rates(v), 3 ** ((temp_c - 6.3) / 10)
    out = {}
    for x in "mhn":
        a, b = r["a" + x], r["b" + x]
        out[x] = a / (a + b)
        out["tau_" + x] = 1 / (phi * (a + b))
    return out


@dataclass(frozen=True)
class HH:
    """A patch of squid axon membrane with the 1952 parameters."""

    g_na: float = 120.0
    g_k: float = 36.0
    g_l: float = 0.3
    e_na: float = 50.0
    e_k: float = -77.0
    e_l: float = -54.4
    c: float = 1.0
    temp_c: float = 6.3

    @property
    def rest(self) -> float:
        """The resting potential: where the three currents cancel with the gates at rest."""
        lo, hi = -80.0, -50.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if self.ionic(mid, **{k: steady(mid)[k] for k in "mhn"}) < 0 else (lo, mid)
        return (lo + hi) / 2

    def ionic(self, v, m, h, n):
        """The total ionic current (uA/cm^2, outward positive)."""
        return (self.g_na * m ** 3 * h * (v - self.e_na) + self.g_k * n ** 4 * (v - self.e_k)
                + self.g_l * (v - self.e_l))

    def _step(self, v, m, h, n, inj, dt, extra_g=0.0, extra_i=0.0):
        """One exponential-Euler step of the gates and then the voltage (``extra_*``: the cable's coupling)."""
        s = steady(v, self.temp_c)
        m = s["m"] + (m - s["m"]) * np.exp(-dt / s["tau_m"])
        h = s["h"] + (h - s["h"]) * np.exp(-dt / s["tau_h"])
        n = s["n"] + (n - s["n"]) * np.exp(-dt / s["tau_n"])
        g = self.g_na * m ** 3 * h + self.g_k * n ** 4 + self.g_l + extra_g
        v_inf = (self.g_na * m ** 3 * h * self.e_na + self.g_k * n ** 4 * self.e_k + self.g_l * self.e_l
                 + inj + extra_i) / g
        return v_inf + (v - v_inf) * np.exp(-dt * g / self.c), m, h, n

    def simulate(self, current, t_end: float, dt: float = 0.01, v0: float | None = None) -> dict:
        """Integrate for ``t_end`` ms under ``current`` (uA/cm^2: a number or a function of t in ms)."""
        inj = current if callable(current) else (lambda t: current)
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        v, m, h, n = (np.empty(k) for _ in range(4))
        v[0] = self.rest if v0 is None else v0
        s = steady(v[0], self.temp_c)
        m[0], h[0], n[0] = s["m"], s["h"], s["n"]
        for i in range(k - 1):
            v[i + 1], m[i + 1], h[i + 1], n[i + 1] = self._step(v[i], m[i], h[i], n[i], inj(t[i]), dt)
        return {"t": t, "v": v, "m": m, "h": h, "n": n, "g_na": self.g_na * m ** 3 * h, "g_k": self.g_k * n ** 4,
                "i_na": self.g_na * m ** 3 * h * (v - self.e_na), "i_k": self.g_k * n ** 4 * (v - self.e_k)}

    def clamp(self, v_step: float, t_end: float = 10.0, dt: float = 0.01, v_hold: float | None = None) -> dict:
        """The voltage clamp: hold at ``v_hold`` (rest), step to ``v_step``; conductances and currents in time.
        With the voltage fixed each gate relaxes exponentially, so this is exact."""
        t = np.arange(0, t_end + dt / 2, dt)
        a, b = steady(self.rest if v_hold is None else v_hold, self.temp_c), steady(v_step, self.temp_c)
        gate = {x: b[x] + (a[x] - b[x]) * np.exp(-t / b["tau_" + x]) for x in "mhn"}
        g_na, g_k = self.g_na * gate["m"] ** 3 * gate["h"], self.g_k * gate["n"] ** 4
        return {"t": t, **gate, "g_na": g_na, "g_k": g_k, "i_na": g_na * (v_step - self.e_na),
                "i_k": g_k * (v_step - self.e_k)}

    def pulse(self, amplitude: float, duration: float = 0.5, t_end: float = 20.0, start: float = 1.0,
              dt: float = 0.01) -> dict:
        """The response to one rectangular current pulse."""
        return self.simulate(lambda t: amplitude if start <= t < start + duration else 0.0, t_end, dt)

    def threshold(self, duration: float = 0.5, tol: float = 0.01) -> float:
        """The smallest pulse amplitude (uA/cm^2) of this duration that fires a spike."""
        lo, hi = 0.0, 200.0
        while hi - lo > tol:
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if self.pulse(mid, duration)["v"].max() > 0 else (mid, hi)
        return hi

    def refractory(self, delays, duration: float = 0.5, first: float | None = None, cap: float = 400.0) -> np.ndarray:
        """The threshold of a second pulse ``delays`` ms after a first one that fired (``inf`` if none below ``cap``
        fires a second spike: the absolute refractory period)."""
        first = 2 * self.threshold(duration) if first is None else first
        out = []
        for d in np.atleast_1d(delays):
            def fires(amp, d=d):
                r = self.simulate(lambda t: first if 1 <= t < 1 + duration else
                                  (amp if 1 + d <= t < 1 + d + duration else 0.0), 1 + d + 15)
                return len(spike_times(r["t"], r["v"])) >= 2
            if not fires(cap):
                out.append(math.inf)
                continue
            lo, hi = 0.0, cap
            while hi - lo > 0.05:
                mid = (lo + hi) / 2
                lo, hi = (lo, mid) if fires(mid) else (mid, hi)
            out.append(hi)
        return np.array(out)

    def firing_rate(self, current: float, t_end: float = 300.0) -> float:
        """Spikes per second under a steady current, counted after the first 50 ms."""
        r = self.simulate(current, t_end, dt=0.02)
        s = spike_times(r["t"], r["v"])
        s = s[s > 50]
        return 0.0 if len(s) < 2 else 1000 * (len(s) - 1) / (s[-1] - s[0])


def spike_times(t, v, level: float = 0.0) -> np.ndarray:
    """Times at which ``v`` crosses ``level`` upward."""
    v = np.asarray(v)
    up = np.flatnonzero((v[:-1] < level) & (v[1:] >= level))
    return np.asarray(t)[up + 1]


# ---------------------------------------------------------------------------------------------------------------
# The cable
# ---------------------------------------------------------------------------------------------------------------
def length_constant(radius_cm: float, r_m: float, r_i: float) -> float:
    """lambda = sqrt(a R_m / (2 R_i)) in cm: how far a steady voltage spreads along a passive fibre
    (``r_m`` ohm cm^2, ``r_i`` ohm cm)."""
    return math.sqrt(radius_cm * r_m / (2 * r_i))


def propagate(axon: HH | None = None, radius_cm: float = 0.0238, r_i: float = 35.4, length_cm: float = 6.0,
              dx: float = 0.025, t_end: float = 6.0, dt: float = 0.005, stim: float = 400.0) -> dict:
    """An action potential started at the left end of a uniform axon.  Returns ``t``, ``x``, ``v[t, x]`` (every
    10th step) and the conduction ``velocity`` in m/s, measured between a third and two thirds of the way along."""
    axon = axon or HH(temp_c=18.5)
    n_x = int(round(length_cm / dx)) + 1
    x = np.arange(n_x) * dx
    d = 1000 * radius_cm / (2 * r_i) / dx ** 2  # mS/cm^2: the coupling between neighbouring compartments
    v = np.full(n_x, axon.rest)
    s = steady(v, axon.temp_c)
    m, h, n = s["m"], s["h"], s["n"]
    # backward Euler in space: (C/dt + g) V - d (V[i-1] - 2 V[i] + V[i+1]) = C V_old / dt + g E + I
    band = np.zeros((3, n_x))
    steps = int(round(t_end / dt))
    keep, frames, cross = max(1, steps // 600), [], np.full(n_x, np.nan)
    for k in range(steps):
        t = k * dt
        s = steady(v, axon.temp_c)
        m = s["m"] + (m - s["m"]) * np.exp(-dt / s["tau_m"])
        h = s["h"] + (h - s["h"]) * np.exp(-dt / s["tau_h"])
        n = s["n"] + (n - s["n"]) * np.exp(-dt / s["tau_n"])
        g_na, g_k = axon.g_na * m ** 3 * h, axon.g_k * n ** 4
        g = g_na + g_k + axon.g_l
        inj = np.zeros(n_x)
        if t < 0.3:
            inj[:4] = stim
        diag = axon.c / dt + g + 2 * d
        diag[0] -= d
        diag[-1] -= d  # sealed ends
        band[0, 1:], band[1], band[2, :-1] = -d, diag, -d
        new = solve_banded((1, 1), band, axon.c * v / dt + g_na * axon.e_na + g_k * axon.e_k + axon.g_l * axon.e_l + inj)
        first = np.isnan(cross) & (v < 0) & (new >= 0)
        cross[first] = t + dt
        v = new
        if k % keep == 0:
            frames.append(v.copy())
    i, j = n_x // 3, 2 * n_x // 3
    velocity = 10 * (x[j] - x[i]) / (cross[j] - cross[i]) if np.isfinite(cross[[i, j]]).all() else float("nan")
    return {"t": np.arange(len(frames)) * keep * dt, "x": x, "v": np.array(frames), "velocity": float(velocity),
            "arrival": cross}


# ---------------------------------------------------------------------------------------------------------------
# FitzHugh-Nagumo
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class FHN:
    a: float = 0.7
    b: float = 0.8
    eps: float = 0.08

    def nullclines(self, v, current: float = 0.0):
        """(w on the v-nullcline, w on the w-nullcline) at each ``v``."""
        v = np.asarray(v, float)
        return v - v ** 3 / 3 + current, (v + self.a) / self.b

    def fixed_point(self, current: float = 0.0) -> tuple:
        """The rest state: where the two nullclines cross (one crossing for these parameters)."""
        roots = np.roots([-1 / 3, 0, 1 - 1 / self.b, current - self.a / self.b])
        v = float(roots[np.argmin(np.abs(roots.imag))].real)
        return v, (v + self.a) / self.b

    def stable(self, current: float = 0.0) -> bool:
        """Is the rest state stable?  (Trace of the Jacobian negative; its determinant is positive here.)"""
        v, _ = self.fixed_point(current)
        return (1 - v * v) - self.eps * self.b < 0

    def simulate(self, current, t_end: float = 200.0, dt: float = 0.05, v0=None) -> dict:
        inj = current if callable(current) else (lambda t: current)
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        v, w = np.empty(k), np.empty(k)
        v[0], w[0] = self.fixed_point(0.0) if v0 is None else v0  # from the rest state of the unstimulated cell

        def f(tt, vv, ww):
            return vv - vv ** 3 / 3 - ww + inj(tt), self.eps * (vv + self.a - self.b * ww)

        for i in range(k - 1):  # classical Runge-Kutta
            k1 = f(t[i], v[i], w[i])
            k2 = f(t[i] + dt / 2, v[i] + dt / 2 * k1[0], w[i] + dt / 2 * k1[1])
            k3 = f(t[i] + dt / 2, v[i] + dt / 2 * k2[0], w[i] + dt / 2 * k2[1])
            k4 = f(t[i] + dt, v[i] + dt * k3[0], w[i] + dt * k3[1])
            v[i + 1] = v[i] + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            w[i + 1] = w[i] + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        return {"t": t, "v": v, "w": w}


# ---------------------------------------------------------------------------------------------------------------
# Leaky integrate-and-fire
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class LIF:
    tau: float = 10.0  # ms
    resistance: float = 10.0  # megohm, so that nA gives mV
    e_l: float = -65.0
    v_th: float = -50.0
    v_reset: float = -65.0
    t_ref: float = 2.0  # ms

    @property
    def rheobase(self) -> float:
        """The smallest steady current (nA) that ever reaches threshold."""
        return (self.v_th - self.e_l) / self.resistance

    def rate(self, current) -> np.ndarray:
        """The firing rate (spikes/s) under a steady current, in closed form."""
        ri = self.resistance * np.asarray(current, float)
        gap, drop = self.v_th - self.e_l, self.v_reset - self.e_l
        with np.errstate(divide="ignore", invalid="ignore"):
            period = self.t_ref + self.tau * np.log((ri - drop) / (ri - gap))
        return np.where(ri > gap, 1000 / period, 0.0)

    def simulate(self, current, t_end: float = 500.0, dt: float = 0.01, noise: float = 0.0, rng=None) -> dict:
        """Integrate under ``current`` (nA: a number, an array over time, or a function of t) with optional white
        noise of ``noise`` mV per sqrt(ms)."""
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        inj = (np.array([current(x) for x in t]) if callable(current)
               else np.broadcast_to(np.asarray(current, float), (k,)))
        rng = rng or np.random.default_rng(0)
        kick = noise * math.sqrt(dt) * rng.standard_normal(k) if noise else np.zeros(k)
        v, spikes, quiet = np.empty(k), [], -1.0
        v[0] = self.e_l
        decay = math.exp(-dt / self.tau)
        for i in range(k - 1):
            if t[i] < quiet:
                v[i + 1] = self.v_reset
                continue
            target = self.e_l + self.resistance * inj[i]
            v[i + 1] = target + (v[i] - target) * decay + kick[i]
            if v[i + 1] >= self.v_th:
                spikes.append(t[i + 1])
                v[i + 1] = self.v_reset
                quiet = t[i + 1] + self.t_ref
        return {"t": t, "v": v, "spikes": np.array(spikes)}

    def coincidence(self, delay: float, epsp: float = 11.0, tau_syn: float = 1.0) -> bool:
        """Two equal synaptic kicks ``delay`` ms apart, each too small to fire the cell alone: does it fire?"""
        amp = epsp / self.resistance * self.tau / tau_syn  # a current pulse that would lift a slow cell by ``epsp``

        def inj(t):
            return amp * (math.exp(-(t - 5) / tau_syn) * (t >= 5) + math.exp(-(t - 5 - delay) / tau_syn) * (t >= 5 + delay))

        return len(self.simulate(inj, 40 + delay, dt=0.02)["spikes"]) > 0


# ---------------------------------------------------------------------------------------------------------------
# Codes
# ---------------------------------------------------------------------------------------------------------------
def poisson_train(rate, t_end: float, rng=None, refractory: float = 0.0, dt: float = 0.001) -> np.ndarray:
    """Spike times (s) of a Poisson process with ``rate`` (spikes/s: a number, or a function of time in s),
    optionally with a dead time of ``refractory`` s after each spike."""
    rng = rng or np.random.default_rng(0)
    t = np.arange(0, t_end, dt)
    lam = np.array([rate(x) for x in t]) if callable(rate) else np.full(len(t), float(rate))
    fire = rng.random(len(t)) < lam * dt
    out, last = [], -math.inf
    for x in t[fire]:
        if x - last >= refractory:
            out.append(x)
            last = x
    return np.array(out)


def fano(counts) -> float:
    """Variance over mean of spike counts: 1 for a Poisson process, less for a regular one."""
    counts = np.asarray(counts, float)
    return float(counts.var(ddof=1) / counts.mean())


def counts(rate: float, window: float, trials: int, rng=None, refractory: float = 0.0) -> np.ndarray:
    """Spike counts in ``trials`` windows of ``window`` s."""
    rng = rng or np.random.default_rng(0)
    return np.array([len(poisson_train(rate, window, rng, refractory)) for _ in range(trials)])


def adrian(stretch, gain: float = 30.0, threshold: float = 0.1, top: float = 150.0) -> np.ndarray:
    """A rate code of the kind Adrian found in a stretch receptor (1926): no spikes below a threshold, then a
    rate that grows with the logarithm of the load and saturates.  Illustrative, not fitted to his records."""
    s = np.asarray(stretch, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = gain * np.log(np.where(s > threshold, s / threshold, 1.0))
    return np.minimum(r, top)


# ---------------------------------------------------------------------------------------------------------------
# What one neuron can compute
# ---------------------------------------------------------------------------------------------------------------
def point_neuron(x, weights, threshold: float) -> np.ndarray:
    """Fire when the weighted sum of the inputs reaches threshold: one linear boundary."""
    return (np.asarray(x, float) @ np.asarray(weights, float) >= threshold).astype(int)


def dendritic_neuron(x, branches, branch_threshold: float, soma_threshold: float = 1.0) -> np.ndarray:
    """A cell whose dendritic branches each fire a local spike when their own inputs reach ``branch_threshold``;
    the soma fires when ``soma_threshold`` branches have.  ``branches`` lists the input indices on each branch."""
    x = np.asarray(x, float)
    local = np.stack([x[..., list(b)].sum(axis=-1) >= branch_threshold for b in branches], axis=-1)
    return (local.sum(axis=-1) >= soma_threshold).astype(int)


def separable(x, y) -> bool:
    """Can any point neuron (any weights and threshold) give outputs ``y`` on inputs ``x``?  Decided exactly, by
    linear programming."""
    from scipy.optimize import linprog

    x, y = np.asarray(x, float), np.asarray(y, int)
    sign = np.where(y == 1, 1.0, -1.0)
    # find w, b with sign * (x w + b) >= 1
    a = -sign[:, None] * np.hstack([x, np.ones((len(x), 1))])
    res = linprog(np.zeros(x.shape[1] + 1), A_ub=a, b_ub=-np.ones(len(x)), bounds=[(None, None)] * (x.shape[1] + 1))
    return bool(res.success)
