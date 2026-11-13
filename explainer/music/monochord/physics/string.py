"""The string of Part 1: a stretched wire, by finite differences and by modes.

The model is the linear stiff, damped string (Bilbao, *Numerical Sound Synthesis*, ch. 7; Fletcher & Rossing ch. 2)::

    u_tt = c^2 u_xx - kappa^2 u_xxxx - 2 sigma0 u_t + 2 sigma1 u_txx,        u(0) = u(L) = 0

with ``c = sqrt(T / mu)``.  With ``kappa = sigma0 = sigma1 = 0`` it is the ideal string of d'Alembert (1747).

Three independent routes to the same motion, so each checks the others (``tests/music/test_string.py``):

* :func:`simulate`: an explicit finite-difference scheme.  Each grid point is a bead obeying Newton's law under the
  pull of its neighbours; nothing about pitch or harmonics is put in.  For the ideal string at Courant number 1 the
  scheme is exact.
* :func:`dalembert`: the travelling-wave solution of the ideal string.
* :func:`modal`: the sum of modes, each a sine in space and a damped cosine in time.

Units are SI throughout: metres, newtons, kilograms per metre, seconds.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

try:  # numba makes the time loop about a hundred times faster; the pure-numpy fallback gives the same numbers
    from numba import njit
except Exception:  # pragma: no cover
    njit = None


@dataclass(frozen=True)
class String:
    L: float = 0.65          # length, m (a guitar's scale)
    T: float = 70.0          # tension, N
    mu: float = 0.0035       # mass per unit length, kg/m
    kappa: float = 0.0       # stiffness, m^2/s: sqrt(E I / mu)
    sigma0: float = 0.0      # loss at all frequencies, 1/s
    sigma1: float = 0.0      # loss that grows with frequency, m^2/s

    @property
    def c(self) -> float:
        """Wave speed on the string, m/s."""
        return float(np.sqrt(self.T / self.mu))

    @property
    def f1(self) -> float:
        """Fundamental of the ideal string: Mersenne's law, ``(1 / 2L) sqrt(T / mu)``."""
        return self.c / (2 * self.L)

    @property
    def B(self) -> float:
        """Inharmonicity coefficient: ``f_n = n f1 sqrt(1 + B n^2)``."""
        return (self.kappa * np.pi / (self.c * self.L)) ** 2

    @classmethod
    def tuned(cls, f1: float, L: float = 0.65, mu: float = 0.0035, **kw) -> "String":
        """The string of this length and mass whose tension gives the fundamental ``f1``."""
        return cls(L=L, T=mu * (2 * L * f1) ** 2, mu=mu, **kw)

    def with_(self, **kw) -> "String":
        return String(**{**self.__dict__, **kw})

    # -- modes ----------------------------------------------------------
    def mode_omega0(self, n) -> np.ndarray:
        """Undamped angular frequency of mode n (simply supported ends)."""
        beta = np.asarray(n, dtype=np.float64) * np.pi / self.L
        return np.sqrt(self.c ** 2 * beta ** 2 + self.kappa ** 2 * beta ** 4)

    def mode_freq(self, n) -> np.ndarray:
        return self.mode_omega0(n) / (2 * np.pi)

    def mode_decay(self, n) -> np.ndarray:
        """Amplitude decay rate of mode n, 1/s: ``sigma0 + sigma1 (n pi / L)^2``."""
        beta = np.asarray(n, dtype=np.float64) * np.pi / self.L
        return self.sigma0 + self.sigma1 * beta ** 2


# ---------------------------------------------------------------------------
# Shapes
# ---------------------------------------------------------------------------
def pluck_shape(x: np.ndarray, L: float, beta: float, h: float = 1.0) -> np.ndarray:
    """A string pulled aside by ``h`` at the point ``beta L`` and held: two straight lines."""
    x = np.asarray(x, dtype=np.float64)
    xp = beta * L
    return np.where(x <= xp, h * x / xp, h * (L - x) / (L - xp))


def pluck_modes(n_modes: int, beta: float, h: float = 1.0) -> np.ndarray:
    """Sine coefficients of the pluck: ``a_n = 2h sin(n pi beta) / (n^2 pi^2 beta (1 - beta))``, n = 1..n_modes.
    They fall as 1/n^2, and every mode with a node at the plucking point is missing."""
    n = np.arange(1, n_modes + 1, dtype=np.float64)
    return 2 * h * np.sin(n * np.pi * beta) / (n ** 2 * np.pi ** 2 * beta * (1 - beta))


def sine_coefficients(u0: np.ndarray, n_modes: int | None = None) -> np.ndarray:
    """Sine coefficients of a shape sampled on a uniform grid including both (zero) ends, by the trapezoid rule:
    ``u0(x) = sum a_n sin(n pi x / L)``."""
    N = len(u0) - 1
    n_modes = N - 1 if n_modes is None else n_modes
    l = np.arange(N + 1)
    n = np.arange(1, n_modes + 1)
    return (2.0 / N) * (np.sin(np.pi * np.outer(n, l) / N) @ np.asarray(u0, dtype=np.float64))


# ---------------------------------------------------------------------------
# Route 1: the travelling waves of d'Alembert
# ---------------------------------------------------------------------------
def dalembert(shape, L: float, c: float, x, t) -> np.ndarray:
    """Ideal string released from rest in the shape ``shape(x)`` (a function on [0, L]):
    ``u = [F(x - ct) + F(x + ct)] / 2`` with F the odd, 2L-periodic extension.  Returns ``(len(t), len(x))``."""
    x = np.atleast_1d(np.asarray(x, dtype=np.float64))
    t = np.atleast_1d(np.asarray(t, dtype=np.float64))

    def F(z):
        z = np.mod(z, 2 * L)
        return np.where(z <= L, shape(np.minimum(z, L)), -shape(np.clip(2 * L - z, 0, L)))

    return 0.5 * (F(x[None, :] - c * t[:, None]) + F(x[None, :] + c * t[:, None]))


# ---------------------------------------------------------------------------
# Route 2: the sum of modes
# ---------------------------------------------------------------------------
def modal(string: String, a: np.ndarray, x, t) -> np.ndarray:
    """Displacement from modal amplitudes ``a`` (released from rest): ``(len(t), len(x))``.

    Each mode is ``a_n sin(n pi x / L) e^{-s t} [cos(w t) + (s / w) sin(w t)]`` with ``s`` its decay rate and
    ``w = sqrt(w0^2 - s^2)``: the exact solution of the damped model for zero initial velocity."""
    x = np.atleast_1d(np.asarray(x, dtype=np.float64))
    t = np.atleast_1d(np.asarray(t, dtype=np.float64))
    n = np.arange(1, len(a) + 1)
    s = string.mode_decay(n)
    w = np.sqrt(np.maximum(string.mode_omega0(n) ** 2 - s ** 2, 0.0))
    shape = np.sin(np.pi * np.outer(n, x) / string.L)                       # (modes, x)
    wt = np.outer(t, w)
    time = np.exp(-np.outer(t, s)) * (np.cos(wt) + (s / np.maximum(w, 1e-12)) * np.sin(wt))  # (t, modes)
    return (time * a[None, :]) @ shape


def modal_bridge_force(string: String, a: np.ndarray, t) -> np.ndarray:
    """The transverse force the string exerts on its end at x = 0, ``T du/dx``: what drives a soundboard.
    Mode n contributes ``T a_n (n pi / L)``, so a pluck's 1/n^2 becomes 1/n here."""
    t = np.atleast_1d(np.asarray(t, dtype=np.float64))
    n = np.arange(1, len(a) + 1)
    s = string.mode_decay(n)
    w = np.sqrt(np.maximum(string.mode_omega0(n) ** 2 - s ** 2, 0.0))
    wt = np.outer(t, w)
    time = np.exp(-np.outer(t, s)) * (np.cos(wt) + (s / np.maximum(w, 1e-12)) * np.sin(wt))
    return time @ (string.T * a * n * np.pi / string.L)


# ---------------------------------------------------------------------------
# Route 3: beads and Newton's law (finite differences)
# ---------------------------------------------------------------------------
def grid_for(string: String, sr: float) -> int:
    """The largest number of segments the explicit scheme can run stably at sample rate ``sr``
    (Bilbao eq. 7.21, with a hair of margin)."""
    k = 1.0 / sr
    g = string.c ** 2 * k ** 2 + 4 * string.sigma1 * k
    hmin = np.sqrt(0.5 * (g + np.sqrt(g ** 2 + 16 * string.kappa ** 2 * k ** 2)))
    return max(4, int(np.floor(string.L / (hmin * (1 + 1e-9)))))


def exact_rate(string: String, N: int) -> float:
    """The sample rate at which an ideal string on N segments has Courant number 1 (the scheme is then exact)."""
    return string.c * N / string.L


def _loop(u, up, steps, lam2, mu2, s0k, s1, every, pick, snaps, force, out, ld, dk, n_on, gam, tens):
    """One bead at a time: the scalar loop numba compiles.

    ``ld``, ``dk``, ``n_on``: a damper at bead ``ld`` (extra loss ``dk`` per step) from step ``n_on`` on, or
    ``ld < 0`` for none.  ``gam``: the stretching nonlinearity, as (EA / 2 L T) / h; ``tens`` records the tension
    factor ``1 + gam * sum (du)^2`` at every step."""
    N = len(u) - 1
    un = np.zeros_like(u)
    j = 0
    for n in range(steps):
        if every > 0 and n % every == 0:
            snaps[j, :] = u
            j += 1
        force[n] = u[1] - u[0]
        out[n] = u[pick]
        f = 1.0
        if gam != 0.0:
            acc = 0.0
            for l in range(N):
                d = u[l + 1] - u[l]
                acc += d * d
            f = 1.0 + gam * acc
        tens[n] = f
        for l in range(1, N):
            dxx = u[l + 1] - 2.0 * u[l] + u[l - 1]
            dxxp = up[l + 1] - 2.0 * up[l] + up[l - 1]
            if mu2 != 0.0:
                um2 = -u[1] if l == 1 else u[l - 2]          # simply supported: the ghost point mirrors with a sign
                up2 = -u[N - 1] if l == N - 1 else u[l + 2]
                dxxxx = up2 - 4.0 * u[l + 1] + 6.0 * u[l] - 4.0 * u[l - 1] + um2
            else:
                dxxxx = 0.0
            loss = s0k + dk if (l == ld and n >= n_on) else s0k
            un[l] = (2.0 * u[l] - (1.0 - loss) * up[l] + f * lam2 * dxx - mu2 * dxxxx + s1 * (dxx - dxxp)) / (1.0 + loss)
        for l in range(1, N):
            up[l] = u[l]
            u[l] = un[l]
    return j


def _loop_numpy(u, up, steps, lam2, mu2, s0k, s1, every, pick, snaps, force, out, ld, dk, n_on, gam, tens):
    """The same update with whole-array arithmetic, for machines without numba (the labs)."""
    loss = np.full(len(u) - 2, s0k)
    j = 0
    for n in range(steps):
        if every > 0 and n % every == 0:
            snaps[j, :] = u
            j += 1
        force[n] = u[1] - u[0]
        out[n] = u[pick]
        f = 1.0 + gam * float(np.sum(np.diff(u) ** 2)) if gam != 0.0 else 1.0
        tens[n] = f
        if ld >= 0 and n == n_on:
            loss[ld - 1] = s0k + dk
        dxx = u[2:] - 2.0 * u[1:-1] + u[:-2]
        dxxp = up[2:] - 2.0 * up[1:-1] + up[:-2]
        new = 2.0 * u[1:-1] - (1.0 - loss) * up[1:-1] + f * lam2 * dxx + s1 * (dxx - dxxp)
        if mu2 != 0.0:
            ext = np.concatenate(([-u[1]], u, [-u[-2]]))
            new -= mu2 * (ext[4:] - 4.0 * ext[3:-1] + 6.0 * ext[2:-2] - 4.0 * ext[1:-3] + ext[:-4])
        up[1:-1] = u[1:-1]
        u[1:-1] = new / (1.0 + loss)
    return j


_loop_fast = njit(cache=True)(_loop) if njit is not None else _loop_numpy


@dataclass
class Run:
    string: String
    sr: float
    N: int
    x: np.ndarray            # grid, (N+1,)
    t_snap: np.ndarray       # times of the stored shapes
    snaps: np.ndarray        # (frames, N+1) displacement
    force: np.ndarray        # T du/dx at x = 0, one value per time step (newtons per unit of displacement amplitude)
    pickup: np.ndarray       # displacement at the pickup point, one value per time step
    courant: float
    tension: np.ndarray      # tension as a multiple of the string's own, one value per time step (1 when linear)


def stretch_gamma(string: String, EA: float) -> float:
    """The Kirchhoff-Carrier coefficient: the tension rises by the factor ``1 + gamma * integral of (du/dx)^2 dx``
    when the string is stretched by its own displacement.  ``EA`` is Young's modulus times the wire's area, in N."""
    return EA / (2.0 * string.L * string.T)


def simulate(string: String, u0, seconds: float, sr: float | None = None, N: int | None = None,
             snapshot_every: int = 0, pickup: float = 0.2371, fast: bool = True, damper: tuple | None = None,
             EA: float = 0.0, headroom: float = 1.0) -> Run:
    """Release the string from rest in the shape ``u0`` and step it forward.

    ``u0`` is an array on the grid (N+1 points, both ends zero) or a function of x.  Give ``sr`` (the scheme then
    takes the finest stable grid) or ``N`` (an ideal string then runs at the exact rate).  ``snapshot_every`` keeps
    every k-th shape; ``pickup`` is where the displacement is read, as a fraction of the length.

    ``damper = (where, rate, from_seconds)``: a finger laid on the string at the fraction ``where`` from that moment,
    as a point loss of ``rate`` (m/s: the damping force per unit velocity, divided by the mass per unit length).

    ``EA > 0`` turns on the stretching nonlinearity (Kirchhoff 1883, Carrier 1945): the tension is no longer a
    constant but rises with the string's own elongation.  ``headroom`` (> 1) coarsens the grid so the scheme stays
    stable when the tension rises by up to that factor."""
    if sr is None and N is None:
        raise ValueError("give sr or N")
    if sr is None:
        sr = exact_rate(string, N)
    if N is None:
        N = grid_for(string.with_(T=string.T * headroom), sr)
    k, h = 1.0 / sr, string.L / N
    x = np.linspace(0.0, string.L, N + 1)
    u = np.array(u0(x) if callable(u0) else u0, dtype=np.float64)
    if u.shape != (N + 1,):
        raise ValueError(f"u0 must have {N + 1} points")
    u[0] = u[-1] = 0.0
    lam2 = (string.c * k / h) ** 2
    mu2 = (string.kappa * k / h ** 2) ** 2
    if lam2 > 1 + 1e-9 and string.kappa == 0:
        raise ValueError(f"unstable: Courant number {np.sqrt(lam2):.4f} > 1")
    s0k = string.sigma0 * k
    s1 = 2 * string.sigma1 * k / h ** 2
    gam = stretch_gamma(string, EA) / h if EA else 0.0
    f0 = 1.0 + gam * float(np.sum(np.diff(u) ** 2))
    if lam2 * f0 > 1 + 1e-9:
        raise ValueError(f"unstable: the stretched string needs headroom of at least {f0:.3f}")
    # the step before the start, for zero initial velocity (second order): u(-k) = u(+k)
    up = u.copy()
    dxx = np.zeros_like(u)
    dxx[1:-1] = u[2:] - 2 * u[1:-1] + u[:-2]
    d4 = np.zeros_like(u)
    if mu2:
        ext = np.concatenate([[-u[1]], u, [-u[-2]]])
        d4[1:-1] = ext[4:] - 4 * ext[3:-1] + 6 * ext[2:-2] - 4 * ext[1:-3] + ext[:-4]
    up[1:-1] = u[1:-1] + 0.5 * (f0 * lam2 * dxx[1:-1] - mu2 * d4[1:-1])
    steps = int(round(seconds * sr))
    frames = (steps + snapshot_every - 1) // snapshot_every if snapshot_every else 0
    snaps = np.zeros((max(frames, 1), N + 1))
    force, out, tens = np.zeros(steps), np.zeros(steps), np.ones(steps)
    pick = int(np.clip(round(pickup * N), 1, N - 1))
    ld, dk, n_on = -1, 0.0, 0
    if damper is not None:
        where, rate, t_on = damper
        ld = int(np.clip(round(where * N), 1, N - 1))
        dk = rate / h * k
        n_on = int(round(t_on * sr))
    (_loop_fast if fast else _loop_numpy)(u, up, steps, lam2, mu2, s0k, s1, snapshot_every, pick, snaps, force, out,
                                          ld, dk, n_on, gam, tens)
    t_snap = np.arange(frames) * snapshot_every / sr if snapshot_every else np.zeros(0)
    return Run(string, sr, N, x, t_snap, snaps[:frames], force * string.T / h, out, float(np.sqrt(lam2)), tens)


def energy(run_snaps: np.ndarray, string: String, sr: float) -> np.ndarray:
    """The discrete energy of an ideal string between consecutive stored steps (store every step):
    kinetic ``mu/2 (du/dt)^2`` plus potential ``T/2 (du/dx at n+1)(du/dx at n)``, summed over the grid.  The explicit
    scheme conserves this quantity exactly (Bilbao, sec. 6.2.6), which is why it cannot blow up below its limit."""
    N = run_snaps.shape[1] - 1
    h, k = string.L / N, 1.0 / sr
    a, b = run_snaps[:-1], run_snaps[1:]
    kin = 0.5 * string.mu * h * np.sum(((b - a) / k) ** 2, axis=1)
    pot = 0.5 * string.T / h * np.sum(np.diff(b, axis=1) * np.diff(a, axis=1), axis=1)
    return kin + pot
