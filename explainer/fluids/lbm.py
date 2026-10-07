"""D2Q9 lattice-Boltzmann solver for 2D incompressible flow past obstacles.

The lattice-Boltzmann method recovers the incompressible Navier–Stokes
equations in the low-Mach limit, and it is simple, robust and fast, which makes
it ideal for producing footage like the Kármán vortex street.

* BGK collision with an optional Smagorinsky sub-grid model (keeps high-Re
  runs stable on a modest grid).
* Equilibrium inlet on the left, zero-gradient outlet on the right, periodic
  top/bottom, full-way bounce-back on solid cells.
* A passive dye field is advected with the flow (semi-Lagrangian) and
  continuously injected around the obstacle, mimicking smoke/dye experiments.

All lengths in lattice units; Re = U * D / nu, nu = (tau - 1/2) / 3.
"""

from __future__ import annotations

import numpy as np
from numba import njit, prange

EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4, dtype=np.float64)
OPP = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int64)


@njit(parallel=True, cache=True, fastmath=True)
def _step(f, fnew, solid, tau0, cs2, U, rho_out, ux_out, uy_out):
    ny, nx = solid.shape
    for y in prange(ny):
        fl = np.empty(9)
        feq = np.empty(9)
        for x in range(nx):
            # --- pull-streaming -------------------------------------------
            for i in range(9):
                xs = x - EX[i]
                ys = (y - EY[i]) % ny
                if xs < 0:
                    xs = 0
                elif xs >= nx:
                    xs = nx - 1
                fl[i] = f[i, ys, xs]
            if solid[y, x]:
                for i in range(9):
                    fnew[i, y, x] = fl[OPP[i]]
                rho_out[y, x] = 1.0
                ux_out[y, x] = 0.0
                uy_out[y, x] = 0.0
                continue
            # --- macroscopic moments --------------------------------------
            rho = 0.0
            mx = 0.0
            my = 0.0
            for i in range(9):
                rho += fl[i]
                mx += fl[i] * EX[i]
                my += fl[i] * EY[i]
            ux = mx / rho
            uy = my / rho
            if x == 0:  # equilibrium inlet
                rho = 1.0
                ux = U
                uy = 0.0
            usq = ux * ux + uy * uy
            for i in range(9):
                eu = EX[i] * ux + EY[i] * uy
                feq[i] = W[i] * rho * (1.0 + 3.0 * eu + 4.5 * eu * eu - 1.5 * usq)
            # --- Smagorinsky effective relaxation time ---------------------
            tau = tau0
            if cs2 > 0.0:
                pxx = 0.0
                pyy = 0.0
                pxy = 0.0
                for i in range(9):
                    d = fl[i] - feq[i]
                    pxx += EX[i] * EX[i] * d
                    pyy += EY[i] * EY[i] * d
                    pxy += EX[i] * EY[i] * d
                pi_mag = np.sqrt(pxx * pxx + pyy * pyy + 2.0 * pxy * pxy)
                tau = 0.5 * (tau0 + np.sqrt(tau0 * tau0 + 18.0 * 1.41421356 * cs2 * pi_mag / rho))
            if x == 0:
                for i in range(9):
                    fnew[i, y, x] = feq[i]
            else:
                om = 1.0 / tau
                for i in range(9):
                    fnew[i, y, x] = fl[i] + om * (feq[i] - fl[i])
            rho_out[y, x] = rho
            ux_out[y, x] = ux
            uy_out[y, x] = uy


@njit(parallel=True, cache=True, fastmath=True)
def _advect_dye(c, cnew, ux, uy, source, solid, decay):
    ny, nx = c.shape
    for y in prange(ny):
        for x in range(nx):
            if solid[y, x]:
                cnew[y, x] = 0.0
                continue
            # backtrace one step
            px = x - ux[y, x]
            py = y - uy[y, x]
            if px < 0:
                px = 0.0
            if px > nx - 1.001:
                px = nx - 1.001
            x0 = int(np.floor(px))
            y0f = np.floor(py)
            tx = px - x0
            ty = py - y0f
            y0 = int(y0f) % ny
            y1 = (y0 + 1) % ny
            x1 = x0 + 1
            v = (
                (1 - tx) * (1 - ty) * c[y0, x0]
                + tx * (1 - ty) * c[y0, x1]
                + (1 - tx) * ty * c[y1, x0]
                + tx * ty * c[y1, x1]
            )
            v *= decay
            if source[y, x] > v:
                v = source[y, x]
            cnew[y, x] = v


class CylinderFlow:
    def __init__(self, nx=720, ny=240, diameter=36, re=150.0, u0=0.08, smagorinsky=0.0, cx=None, cy=None, seed=0):
        self.nx, self.ny, self.D = nx, ny, diameter
        self.U = u0
        self.nu = u0 * diameter / re
        self.tau = 3 * self.nu + 0.5
        self.cs2 = smagorinsky**2
        cx = 4.5 * diameter if cx is None else cx
        cy = ny / 2 + 0.5 if cy is None else cy
        yy, xx = np.mgrid[0:ny, 0:nx]
        r2 = (xx - cx) ** 2 + (yy - cy) ** 2
        self.solid = r2 <= (diameter / 2) ** 2
        ring = (r2 <= (diameter / 2 + 2.5) ** 2) & ~self.solid
        self.source = ring.astype(np.float64)
        self.center = (cx, cy)

        rng = np.random.default_rng(seed)
        ux = np.full((ny, nx), u0)
        uy = 1e-3 * u0 * rng.standard_normal((ny, nx))
        # Asymmetric kick to trigger shedding quickly.
        uy += 0.1 * u0 * np.exp(-((xx - cx - diameter) ** 2 + (yy - cy - diameter / 3) ** 2) / (diameter**2))
        ux[self.solid] = 0
        uy[self.solid] = 0
        self.f = self.equilibrium(np.ones((ny, nx)), ux, uy)
        self.fnew = np.empty_like(self.f)
        self.rho = np.ones((ny, nx))
        self.ux = ux.copy()
        self.uy = uy.copy()
        self.dye = np.zeros((ny, nx))
        self.dye_new = np.zeros((ny, nx))

    @staticmethod
    def equilibrium(rho, ux, uy):
        usq = ux**2 + uy**2
        f = np.empty((9,) + rho.shape)
        for i in range(9):
            eu = EX[i] * ux + EY[i] * uy
            f[i] = W[i] * rho * (1 + 3 * eu + 4.5 * eu**2 - 1.5 * usq)
        return f

    def step(self, n=1, dye=True, dye_decay=0.9995):
        for _ in range(n):
            _step(self.f, self.fnew, self.solid, self.tau, self.cs2, self.U, self.rho, self.ux, self.uy)
            self.f, self.fnew = self.fnew, self.f
            if dye:
                _advect_dye(self.dye, self.dye_new, self.ux, self.uy, self.source, self.solid, dye_decay)
                self.dye, self.dye_new = self.dye_new, self.dye

    def vorticity(self):
        """Vorticity in units of U/D (so values are comparable across runs)."""
        dvdx = (np.roll(self.uy, -1, 1) - np.roll(self.uy, 1, 1)) / 2
        dudy = (np.roll(self.ux, -1, 0) - np.roll(self.ux, 1, 0)) / 2
        w = dvdx - dudy
        w[self.solid] = 0
        return w * self.D / self.U


def run_cylinder(re, n_frames, steps_per_frame, warmup_steps, smagorinsky=0.0, dye_fade_length=450.0, **kw):
    """Simulate and return a dict of float16 frame stacks + metadata.

    Dye fades by 1/e over ``dye_fade_length`` lattice cells of free-stream
    travel, independent of the lattice velocity.
    """
    sim = CylinderFlow(re=re, smagorinsky=smagorinsky, **kw)
    decay = float(np.exp(-sim.U / dye_fade_length))
    sim.step(warmup_steps, dye_decay=decay)
    vort = np.empty((n_frames, sim.ny, sim.nx), dtype=np.float16)
    dye = np.empty((n_frames, sim.ny, sim.nx), dtype=np.float16)
    for k in range(n_frames):
        sim.step(steps_per_frame, dye_decay=decay)
        vort[k] = sim.vorticity()
        dye[k] = sim.dye
    # Final snapshot of the velocity field (for streamlines / arrows).
    return {
        "vorticity": vort,
        "dye": dye,
        "solid": sim.solid,
        "ux": (sim.ux / sim.U).astype(np.float32),
        "uy": (sim.uy / sim.U).astype(np.float32),
        "center": np.array(sim.center),
        "diameter": np.array(sim.D),
        "re": np.array(re),
    }
