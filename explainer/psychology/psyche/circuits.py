"""Synapses and small circuits: what neurons do to each other (videos/psychology/SYLLABUS.md, Part 6).

Part 5 built one cell.  This module connects cells, in the order the part does.

**A synapse** opens a conductance for a few milliseconds.  On a passive membrane,

    C dV/dt = -g_L (V - E_L) - g_E(t) (V - E_E) - g_I(t) (V - E_I),      g(t) = g_max (t / tau) e^(1 - t / tau),

an excitatory conductance (E_E = 0 mV) lifts the voltage and an inhibitory one pulls it toward E_I.  Inputs add
in time and across synapses, but less than linearly, because each one reduces the driving force of the others.
An inhibitory synapse whose battery sits at rest moves nothing by itself and *divides* what excitation does
(:func:`steady_voltage`): shunting inhibition.

**Learning rules** for a linear unit y = w . x:

    Hebb     dw = eta y x                          grows without bound, along the input's first principal component
    Oja      dw = eta y (x - y w)                  the same direction, with |w| -> 1  (Oja 1982)
    BCM      dw = eta x y (y - theta),  theta = <y^2>     a sliding threshold: selectivity, and stability
    STDP     dw = +A_plus e^(-dt / tau_plus) if the input precedes the output spike by dt > 0,
                  -A_minus e^(dt / tau_minus) if it follows                (the window of Bi and Poo 1998)

**Lateral inhibition** (Hartline and Ratliff 1957): each unit's response is its excitation less a weighted sum of
its neighbours' responses, r = e - K r, so r = (I + K)^(-1) e.  A step of light comes out with a bright band on
its bright side and a dark band on its dark side: Mach bands.  The same idea in two dimensions is a
centre-surround filter, a difference of two Gaussians; on a grid of white streets it responds less at the
crossings than along the streets (the textbook account of the Hermann grid).

**Winner-take-all**: two units that excite themselves and inhibit each other,

    tau dr_i/dt = -r_i + f(I_i + w_self r_i - w_cross r_j),

settle with one on and one off, and stay there after the inputs are made equal: the circuit holds a choice.

**A half-centre oscillator** (Matsuoka 1985): the same mutual inhibition, plus fatigue,

    tau dx_i/dt = -x_i - beta v_i - a y_j + s,     T dv_i/dt = -v_i + y_i,     y = max(x, 0),

alternates for 1 + tau/T < a < 1 + beta: a rhythm from a steady drive, as in the spinal circuits of locomotion.

**Populations** (Wilson and Cowan 1972): an excitatory and an inhibitory population,

    tau_E dE/dt = -E + S(w_EE E - w_EI I + P),     tau_I dI/dt = -I + S(w_IE E - w_II I + Q),

rest at a fixed point for weak drive and oscillate for stronger drive.

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------------------------------------------------------
# Synapses on a passive membrane
# ---------------------------------------------------------------------------------------------------------------


def alpha(t, tau: float = 1.0):
    """The conductance time course of one synaptic event: 0 before t = 0, peaking at 1 when t = tau (ms)."""
    t = np.asarray(t, float)
    return np.where(t > 0, (t / tau) * np.exp(1 - t / tau), 0.0)


@dataclass(frozen=True)
class Membrane:
    """A passive patch: capacitance (uF/cm^2), leak (mS/cm^2) and the three batteries (mV)."""

    c: float = 1.0
    g_l: float = 0.1
    e_l: float = -65.0
    e_e: float = 0.0
    e_i: float = -80.0

    @property
    def tau(self) -> float:
        return self.c / self.g_l

    def steady_voltage(self, g_e: float = 0.0, g_i: float = 0.0, e_i: float | None = None) -> float:
        """The voltage with steady conductances: the conductance-weighted mean of the batteries."""
        e_i = self.e_i if e_i is None else e_i
        return (self.g_l * self.e_l + g_e * self.e_e + g_i * e_i) / (self.g_l + g_e + g_i)

    def response(self, exc=(), inh=(), g_e: float = 0.02, g_i: float = 0.04, tau_syn: float = 1.0, t_end: float = 60.0,
                 dt: float = 0.02, e_i: float | None = None) -> dict:
        """The voltage after excitatory events at times ``exc`` and inhibitory ones at ``inh`` (ms), each an alpha
        conductance of peak ``g_e`` / ``g_i`` (mS/cm^2)."""
        e_i = self.e_i if e_i is None else e_i
        t = np.arange(0, t_end + dt / 2, dt)
        ge = g_e * sum((alpha(t - t0, tau_syn) for t0 in exc), np.zeros_like(t))
        gi = g_i * sum((alpha(t - t0, tau_syn) for t0 in inh), np.zeros_like(t))
        v = np.empty_like(t)
        v[0] = self.e_l
        for k in range(len(t) - 1):  # exponential Euler: exact for conductances held over the step
            g = self.g_l + ge[k] + gi[k]
            v_inf = (self.g_l * self.e_l + ge[k] * self.e_e + gi[k] * e_i) / g
            v[k + 1] = v_inf + (v[k] - v_inf) * math.exp(-dt * g / self.c)
        return {"t": t, "v": v, "g_e": ge, "g_i": gi, "peak": float(v.max() - self.e_l), "trough": float(v.min() - self.e_l)}


# ---------------------------------------------------------------------------------------------------------------
# Learning rules
# ---------------------------------------------------------------------------------------------------------------
def hebb(x, eta: float = 0.01, w0=None, rule: str = "hebb", epochs: int = 1, rng=None) -> dict:
    """Train a linear unit y = w . x on the rows of ``x`` with ``rule`` in {"hebb", "oja"}; returns the final
    weights and the history of their length and of their cosine with the input's first principal component."""
    x = np.asarray(x, float)
    rng = rng or np.random.default_rng(0)
    w = rng.standard_normal(x.shape[1]) * 0.1 if w0 is None else np.array(w0, float)
    pc = principal_component(x)
    norms, cosines, path = [], [], [w.copy()]
    for _ in range(epochs):
        for row in x[rng.permutation(len(x))]:
            y = w @ row
            w = w + eta * y * (row - y * w if rule == "oja" else row)
            n = np.linalg.norm(w)
            norms.append(n)
            path.append(w.copy())
            cosines.append(abs(w @ pc) / max(n, 1e-300))
            if n > 1e6:  # plain Hebb has diverged
                break
        if norms[-1] > 1e6:
            break
    return {"w": w, "norm": np.array(norms), "cosine": np.array(cosines), "pc": pc, "path": np.array(path)}


def principal_component(x) -> np.ndarray:
    """The unit eigenvector of the inputs' second-moment matrix with the largest eigenvalue."""
    x = np.asarray(x, float)
    vals, vecs = np.linalg.eigh(x.T @ x / len(x))
    return vecs[:, -1]


def bcm(patterns, eta: float = 0.02, tau_theta: float = 50.0, steps: int = 20_000, w0=None, rng=None) -> dict:
    """The Bienenstock-Cooper-Munro rule on a unit shown the rows of ``patterns`` at random: the threshold
    ``theta`` follows the running mean of y^2.  Returns the weights, the response to each pattern in time and the
    threshold in time."""
    p = np.asarray(patterns, float)
    rng = rng or np.random.default_rng(0)
    w = np.full(p.shape[1], 0.5) + 0.05 * rng.standard_normal(p.shape[1]) if w0 is None else np.array(w0, float)
    theta, resp, thetas = 1.0, [], []
    for k in range(steps):
        x = p[rng.integers(len(p))]
        y = w @ x
        w = w + eta * x * y * (y - theta)
        theta += (y * y - theta) / tau_theta
        if k % 50 == 0:
            resp.append(p @ w)
            thetas.append(theta)
    r = p @ w
    return {"w": w, "response": np.array(resp), "theta": np.array(thetas), "final": r,
            "selectivity": float(1 - r.mean() / max(r.max(), 1e-12)) * len(r) / (len(r) - 1)}


def stdp(dt_ms, a_plus: float = 1.0, a_minus: float = 0.5, tau_plus: float = 17.0, tau_minus: float = 34.0):
    """The change in a synapse (relative units) when the input spike precedes the output spike by ``dt_ms``
    (negative: it follows).  Potentiation for dt > 0, depression for dt < 0; the time constants are of the order
    Bi and Poo measured (tens of milliseconds) and are illustrative."""
    d = np.asarray(dt_ms, float)
    return np.where(d > 0, a_plus * np.exp(-d / tau_plus), np.where(d < 0, -a_minus * np.exp(d / tau_minus), 0.0))


# ---------------------------------------------------------------------------------------------------------------
# Lateral inhibition
# ---------------------------------------------------------------------------------------------------------------
def inhibition_kernel(n: int, strength: float = 0.25, space: float = 2.0) -> np.ndarray:
    """K[i, j]: how much unit j's response is subtracted from unit i's; falls off with distance, zero on the
    diagonal."""
    i = np.arange(n)
    k = strength * np.exp(-np.abs(i[:, None] - i[None, :]) / space)
    np.fill_diagonal(k, 0.0)
    return k


def lateral(excitation, strength: float = 0.25, space: float = 2.0) -> np.ndarray:
    """The responses of a row of units with recurrent lateral inhibition, r = e - K r (Hartline and Ratliff).
    Solved exactly; valid while every response is positive, which the tests check for the film's inputs."""
    e = np.asarray(excitation, float)
    r = np.linalg.solve(np.eye(len(e)) + inhibition_kernel(len(e), strength, space), e)
    if r.min() < 0:  # some units silenced: iterate the rectified equations instead
        k = inhibition_kernel(len(e), strength, space)
        r = np.maximum(r, 0)
        for _ in range(2000):
            r = 0.5 * r + 0.5 * np.maximum(e - k @ r, 0)
    return r


def dog(image, centre: float, surround: float | None = None, balance: float = 1.0) -> np.ndarray:
    """A centre-surround filter: the image blurred at ``centre`` pixels less ``balance`` times the image blurred
    at ``surround`` (default 3 x centre)."""
    from scipy.ndimage import gaussian_filter

    img = np.asarray(image, float)
    return gaussian_filter(img, centre) - balance * gaussian_filter(img, surround or 3 * centre)


def hermann_grid(squares: int = 5, square: int = 40, street: int = 10, wave: float = 0.0) -> np.ndarray:
    """Black squares on white streets, as an array of 0 and 1.  ``wave`` (pixels) bends each street into a sine
    of that amplitude with one period per square, leaving the crossings where they were: Geier's curved grid."""
    period = square + street
    n = squares * period + street
    yy, xx = np.mgrid[0:n, 0:n].astype(float)
    centre = (np.arange(squares + 1) * period + street / 2 - 0.5)[:, None, None]
    horiz = np.abs(yy[None] - centre - wave * np.sin(2 * np.pi * (xx[None] - street / 2 + 0.5) / period)) < street / 2
    vert = np.abs(xx[None] - centre - wave * np.sin(2 * np.pi * (yy[None] - street / 2 + 0.5) / period)) < street / 2
    return (horiz.any(axis=0) | vert.any(axis=0)).astype(float)


def hermann_response(squares: int = 5, square: int = 40, street: int = 10, centre: float | None = None,
                     wave: float = 0.0) -> dict:
    """The centre-surround response at a crossing and half-way along a street, for a centre matched to the
    street.  (With ``wave`` the street's mid-point is where the sine crosses zero, so the same two pixels are
    compared.)"""
    img = hermann_grid(squares, square, street, wave)
    out = dog(img, centre or street / 5)
    period = square + street
    mid = (squares // 2) * period + street // 2  # the centre line of a middle street
    return {"image": img, "filtered": out, "crossing": float(out[mid, mid]),
            "street": float(out[mid, mid + period // 2]), "row": out[mid], "at": mid}


# ---------------------------------------------------------------------------------------------------------------
# Winner-take-all
# ---------------------------------------------------------------------------------------------------------------
def sigmoid(x, gain: float = 1.0, mid: float = 0.0):
    return 1 / (1 + np.exp(-gain * (np.asarray(x, float) - mid)))


@dataclass(frozen=True)
class WTA:
    """Two rate units with self-excitation and mutual inhibition."""

    w_self: float = 6.0
    w_cross: float = 6.0
    gain: float = 1.0
    mid: float = 3.0
    tau: float = 10.0  # ms

    def simulate(self, inputs, t_end: float = 600.0, dt: float = 0.5, r0=(0.1, 0.1), noise: float = 0.0, rng=None) -> dict:
        """``inputs``: a pair of numbers, or a function of t (ms) returning a pair."""
        inj = inputs if callable(inputs) else (lambda t: inputs)
        rng = rng or np.random.default_rng(0)
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        r = np.empty((k, 2))
        r[0] = r0
        for i in range(k - 1):
            a, b = inj(t[i])
            drive = np.array([a + self.w_self * r[i, 0] - self.w_cross * r[i, 1],
                              b + self.w_self * r[i, 1] - self.w_cross * r[i, 0]])
            r[i + 1] = r[i] + dt / self.tau * (-r[i] + sigmoid(drive, self.gain, self.mid))
            if noise:
                r[i + 1] = np.clip(r[i + 1] + noise * math.sqrt(dt) * rng.standard_normal(2), 0, 1)
        return {"t": t, "r": r, "winner": int(np.argmax(r[-1])), "margin": float(abs(r[-1, 0] - r[-1, 1]))}


# ---------------------------------------------------------------------------------------------------------------
# A half-centre oscillator
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class HalfCentre:
    """Matsuoka's two-unit oscillator: mutual inhibition ``a`` and fatigue ``beta``."""

    a: float = 2.5
    beta: float = 2.5
    tau: float = 25.0  # ms
    t_fatigue: float = 300.0  # ms
    drive: float = 1.0

    @property
    def oscillates(self) -> bool:
        """Matsuoka's condition for a sustained alternation."""
        return 1 + self.tau / self.t_fatigue < self.a < 1 + self.beta

    def simulate(self, t_end: float = 4000.0, dt: float = 0.5, x0=(0.1, 0.0)) -> dict:
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        x, v = np.empty((k, 2)), np.zeros((k, 2))
        x[0] = x0
        for i in range(k - 1):
            y = np.maximum(x[i], 0)
            x[i + 1] = x[i] + dt / self.tau * (-x[i] - self.beta * v[i] - self.a * y[::-1] + self.drive)
            v[i + 1] = v[i] + dt / self.t_fatigue * (-v[i] + y)
        y = np.maximum(x, 0)
        half = k // 2
        on = y[half:, 0] > y[half:, 1]
        flips = np.flatnonzero(np.diff(on.astype(int)) == 1)
        period = float(np.diff(flips).mean() * dt) if len(flips) > 1 else float("nan")
        return {"t": t, "y": y, "fatigue": v, "period": period,
                "correlation": float(np.corrcoef(y[half:, 0], y[half:, 1])[0, 1]) if y[half:].std() > 1e-9 else 0.0}


# ---------------------------------------------------------------------------------------------------------------
# Wilson and Cowan
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class WilsonCowan:
    """An excitatory and an inhibitory population with sigmoid responses (their limit-cycle weights)."""

    w_ee: float = 16.0
    w_ei: float = 12.0
    w_ie: float = 15.0
    w_ii: float = 3.0
    gain_e: float = 1.3
    mid_e: float = 4.0
    gain_i: float = 2.0
    mid_i: float = 3.7
    tau_e: float = 8.0  # ms
    tau_i: float = 8.0

    def simulate(self, p: float, q: float = 0.0, t_end: float = 600.0, dt: float = 0.1, e0: float = 0.1, i0: float = 0.05) -> dict:
        k = int(round(t_end / dt)) + 1
        t = np.arange(k) * dt
        e, i = np.empty(k), np.empty(k)
        e[0], i[0] = e0, i0
        for n in range(k - 1):
            se = sigmoid(self.w_ee * e[n] - self.w_ei * i[n] + p, self.gain_e, self.mid_e)
            si = sigmoid(self.w_ie * e[n] - self.w_ii * i[n] + q, self.gain_i, self.mid_i)
            e[n + 1] = e[n] + dt / self.tau_e * (-e[n] + se)
            i[n + 1] = i[n] + dt / self.tau_i * (-i[n] + si)
        late = e[k // 2:]
        amp = float(late.max() - late.min())
        up = np.flatnonzero((late[:-1] < late.mean()) & (late[1:] >= late.mean()))
        freq = float(1000 / (np.diff(up).mean() * dt)) if amp > 0.05 and len(up) > 1 else 0.0
        return {"t": t, "e": e, "i": i, "amplitude": amp, "frequency": freq}
