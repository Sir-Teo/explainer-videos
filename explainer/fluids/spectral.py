"""Pseudo-spectral solver for 2D incompressible Navier–Stokes on a periodic box.

Vorticity form (taking the curl of Navier–Stokes eliminates pressure):

    d(omega)/dt + (u . grad) omega = nu * Laplacian(omega)
    u = (d psi/dy, -d psi/dx),   Laplacian(psi) = -omega

Time stepping: classic RK4 with an exact integrating factor for the viscous
term, 2/3-rule dealiasing, CFL-adaptive step.  Optionally advects a passive
scalar ("dye") with diffusivity ``kappa``.
"""

from __future__ import annotations

import numpy as np
import scipy.fft as sfft

WORKERS = 4


def _fft2(a):
    return sfft.rfft2(a, workers=WORKERS)


def _ifft2(a, n):
    return sfft.irfft2(a, s=(n, n), workers=WORKERS)


class Spectral2D:
    def __init__(self, n=256, nu=1e-3, kappa=None, length=2 * np.pi):
        self.n, self.nu, self.L = n, nu, length
        self.kappa = nu if kappa is None else kappa
        k = np.fft.fftfreq(n, d=length / n) * 2 * np.pi
        kr = np.fft.rfftfreq(n, d=length / n) * 2 * np.pi
        self.ky, self.kx = np.meshgrid(k, kr, indexing="ij")
        self.k2 = self.kx**2 + self.ky**2
        self.k2_inv = np.where(self.k2 == 0, 0.0, 1.0 / np.where(self.k2 == 0, 1, self.k2))
        kmax = np.abs(k).max()
        self.dealias = (np.abs(self.kx) < 2 / 3 * kmax) & (np.abs(self.ky) < 2 / 3 * kmax)
        x = np.arange(n) * length / n
        self.y, self.x = np.meshgrid(x, x, indexing="ij")
        self.w_hat = np.zeros_like(self.k2, dtype=complex)
        self.c_hat = None
        self.t = 0.0

    # -- state ---------------------------------------------------------------
    def set_vorticity(self, w):
        self.w_hat = _fft2(w) * self.dealias

    def set_scalar(self, c):
        self.c_hat = _fft2(c) * self.dealias

    def vorticity(self):
        return _ifft2(self.w_hat, self.n)

    def scalar(self):
        return None if self.c_hat is None else _ifft2(self.c_hat, self.n)

    def velocity(self, w_hat=None):
        w_hat = self.w_hat if w_hat is None else w_hat
        psi = w_hat * self.k2_inv
        u = _ifft2(1j * self.ky * psi, self.n)
        v = _ifft2(-1j * self.kx * psi, self.n)
        return u, v

    def energy(self):
        u, v = self.velocity()
        return 0.5 * np.mean(u**2 + v**2)

    # -- dynamics ------------------------------------------------------------
    def _rhs(self, w_hat, c_hat):
        u, v = self.velocity(w_hat)
        wx = _ifft2(1j * self.kx * w_hat, self.n)
        wy = _ifft2(1j * self.ky * w_hat, self.n)
        nw = -_fft2(u * wx + v * wy) * self.dealias
        nc = None
        if c_hat is not None:
            cx = _ifft2(1j * self.kx * c_hat, self.n)
            cy = _ifft2(1j * self.ky * c_hat, self.n)
            nc = -_fft2(u * cx + v * cy) * self.dealias
        return nw, nc

    def step(self, dt):
        Ew = np.exp(-self.nu * self.k2 * dt / 2)
        Ec = np.exp(-self.kappa * self.k2 * dt / 2)
        w0, c0 = self.w_hat, self.c_hat
        has_c = c0 is not None

        k1w, k1c = self._rhs(w0, c0)
        w1 = Ew * (w0 + dt / 2 * k1w)
        c1 = Ec * (c0 + dt / 2 * k1c) if has_c else None
        k2w, k2c = self._rhs(w1, c1)
        w2 = Ew * w0 + dt / 2 * k2w
        c2 = Ec * c0 + dt / 2 * k2c if has_c else None
        k3w, k3c = self._rhs(w2, c2)
        w3 = Ew * Ew * w0 + dt * Ew * k3w
        c3 = Ec * Ec * c0 + dt * Ec * k3c if has_c else None
        k4w, k4c = self._rhs(w3, c3)
        self.w_hat = Ew * Ew * w0 + dt / 6 * (Ew * Ew * k1w + 2 * Ew * (k2w + k3w) + k4w)
        if has_c:
            self.c_hat = Ec * Ec * c0 + dt / 6 * (Ec * Ec * k1c + 2 * Ec * (k2c + k3c) + k4c)
        self.t += dt

    def cfl_dt(self, cfl=0.5, dt_max=0.05):
        u, v = self.velocity()
        umax = max(np.abs(u).max(), np.abs(v).max(), 1e-9)
        return min(dt_max, cfl * (self.L / self.n) / umax)

    def advance(self, duration, cfl=0.5, dt_max=0.05):
        t_end = self.t + duration
        while self.t < t_end - 1e-12:
            dt = min(self.cfl_dt(cfl, dt_max), t_end - self.t)
            self.step(dt)


# ---------------------------------------------------------------------------
# Initial conditions
# ---------------------------------------------------------------------------
def shear_layer_ic(sim: Spectral2D, delta=0.08, amp=0.05, modes=2, seed=1):
    """Double shear layer (Kelvin–Helmholtz).  Returns (vorticity, dye)."""
    y, x = sim.y, sim.x
    L = sim.L
    u = np.where(y <= L / 2, np.tanh((y - L / 4) / delta), np.tanh((3 * L / 4 - y) / delta))
    rng = np.random.default_rng(seed)
    v = amp * np.sin(modes * x)
    for m in range(1, 6):
        v += 0.2 * amp * rng.standard_normal() * np.sin(m * x + rng.uniform(0, 2 * np.pi))
    u_hat, v_hat = _fft2(u), _fft2(v)
    w = _ifft2(1j * sim.kx * v_hat - 1j * sim.ky * u_hat, sim.n)
    dye = 0.5 * (1 + np.where(y <= L / 2, np.tanh((y - L / 4) / delta), np.tanh((3 * L / 4 - y) / delta)))
    return w, dye


def random_vorticity_ic(sim: Spectral2D, k_peak=12.0, rms=1.0, seed=0):
    """Random vorticity with an energy spectrum peaked at ``k_peak``."""
    rng = np.random.default_rng(seed)
    k = np.sqrt(sim.k2)
    amp = k ** 2 * np.exp(-((k / k_peak) ** 2))
    phase = np.exp(2j * np.pi * rng.uniform(size=k.shape))
    w_hat = amp * phase * sim.dealias
    w_hat[0, 0] = 0
    w = _ifft2(w_hat, sim.n)
    w *= rms / w.std()
    return w


def record(sim: Spectral2D, n_frames, frame_dt, cfl=0.5, scalar=False, every_callback=None):
    frames = np.empty((n_frames, sim.n, sim.n), dtype=np.float16)
    dye = np.empty((n_frames, sim.n, sim.n), dtype=np.float16) if scalar else None
    energy = np.empty(n_frames)
    for k in range(n_frames):
        frames[k] = sim.vorticity()
        if scalar:
            dye[k] = sim.scalar()
        energy[k] = sim.energy()
        sim.advance(frame_dt, cfl=cfl)
    return frames, dye, energy
