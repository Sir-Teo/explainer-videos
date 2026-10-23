"""Fields that evolve (Part 25, chapters 13 and 14): Burgers' equation and a Fourier neural operator trained on it, with
a convolutional network for comparison, both evaluated at resolutions they never saw; and a two-dimensional "weather"
(forced vorticity on a periodic square) rolled forward by a small encoder-processor-decoder graph network on a
multi-level mesh, after GraphCast.  Spectral solvers in numpy; models in torch; seeded.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


# ===========================================================================
# Burgers' equation u_t + u u_x = nu u_xx on [0, 1), periodic
# ===========================================================================
NU = 0.01
FINE = 1024


def grf(rng, n_samples, N=FINE):
    """Initial conditions from the Gaussian random field N(0, 625 (-Laplacian + 25 I)^-2) (Li et al. 2021)."""
    k = np.fft.rfftfreq(N, 1.0 / N)
    lam = 625.0 * (4 * math.pi ** 2 * k ** 2 + 25.0) ** -2
    coef = (rng.normal(size=(n_samples, len(k))) + 1j * rng.normal(size=(n_samples, len(k)))) * np.sqrt(lam / 2)
    coef[:, 0] = 0.0
    return np.fft.irfft(coef * N, n=N)


def burgers(u0, T=1.0, nu=NU, dt=1e-4):
    """Pseudo-spectral solution with an integrating factor for the viscous term and RK4 for the rest (2/3 dealiased)."""
    N = u0.shape[-1]
    k = 2 * math.pi * np.fft.rfftfreq(N, 1.0 / N)
    E = np.exp(-nu * k ** 2 * dt / 2)
    E2 = E ** 2
    mask = np.abs(np.fft.rfftfreq(N, 1.0 / N)) < N / 3

    def nonlin(vh):
        u = np.fft.irfft(vh * mask, n=N)
        return -0.5j * k * np.fft.rfft(u * u)

    v = np.fft.rfft(u0)
    for _ in range(int(round(T / dt))):
        k1 = dt * nonlin(v)
        k2 = dt * nonlin(E * (v + k1 / 2))
        k3 = dt * nonlin(E * v + k2 / 2)
        k4 = dt * nonlin(E2 * v + E * k3)
        v = E2 * v + (E2 * k1 + 2 * E * (k2 + k3) + k4) / 6
    return np.fft.irfft(v, n=N)


def subsample(u, res):
    return u[..., :: u.shape[-1] // res]


class SpectralConv1d(nn.Module):
    """Fourier layer (Li et al. 2021): FFT, multiply the lowest ``modes`` frequencies by learned complex weights, drop
    the rest, inverse FFT.  The weights live on frequencies, not grid points: any grid fine enough to hold ``modes``
    frequencies can use them."""

    def __init__(self, c_in, c_out, modes):
        super().__init__()
        scale = 1 / (c_in * c_out)
        self.modes = modes
        self.w = nn.Parameter(scale * torch.randn(c_in, c_out, modes, 2))

    def forward(self, x):
        N = x.shape[-1]
        xh = torch.fft.rfft(x)
        out = torch.zeros(x.shape[0], self.w.shape[1], N // 2 + 1, dtype=torch.cfloat)
        w = torch.view_as_complex(self.w)
        out[:, :, : self.modes] = torch.einsum("bik,iok->bok", xh[:, :, : self.modes], w)
        return torch.fft.irfft(out, n=N)


class FNO1d(nn.Module):
    def __init__(self, modes=16, width=32, layers=4):
        super().__init__()
        self.lift = nn.Linear(2, width)
        self.spec = nn.ModuleList([SpectralConv1d(width, width, modes) for _ in range(layers)])
        self.local = nn.ModuleList([nn.Conv1d(width, width, 1) for _ in range(layers)])
        self.proj = nn.Sequential(nn.Linear(width, 128), nn.GELU(), nn.Linear(128, 1))

    def forward(self, u):  # u: (B, N) on [0, 1)
        B, N = u.shape
        x = torch.linspace(0, 1, N + 1)[:-1].expand(B, N)
        h = self.lift(torch.stack([u, x], -1)).transpose(1, 2)
        for k, (s, l) in enumerate(zip(self.spec, self.local)):
            h = s(h) + l(h)
            if k < len(self.spec) - 1:
                h = F.gelu(h)
        return self.proj(h.transpose(1, 2)).squeeze(-1)


class CNN1d(nn.Module):
    """The same layout with ordinary convolutions (kernel 5, circular padding): its kernels are measured in grid
    points, so on a finer grid they see a narrower stretch of the line."""

    def __init__(self, width=32, layers=4, kernel=5):
        super().__init__()
        self.lift = nn.Linear(2, width)
        self.convs = nn.ModuleList([nn.Conv1d(width, width, kernel, padding=kernel // 2, padding_mode="circular")
                                    for _ in range(layers)])
        self.proj = nn.Sequential(nn.Linear(width, 128), nn.GELU(), nn.Linear(128, 1))

    def forward(self, u):
        B, N = u.shape
        x = torch.linspace(0, 1, N + 1)[:-1].expand(B, N)
        h = self.lift(torch.stack([u, x], -1)).transpose(1, 2)
        for k, c in enumerate(self.convs):
            h = c(h)
            if k < len(self.convs) - 1:
                h = F.gelu(h)
        return self.proj(h.transpose(1, 2)).squeeze(-1)


def rel_l2(pred, true) -> np.ndarray:
    return np.linalg.norm(pred - true, axis=-1) / np.linalg.norm(true, axis=-1)


def train_operator(kind, U0, UT, seed, epochs=300, batch=20, lr=1e-3, snaps=(), snap_fn=None, val=None):
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(6000 + seed)
    m = FNO1d() if kind == "fno" else CNN1d()
    opt = torch.optim.Adam(m.parameters(), lr, weight_decay=1e-4)
    steps = epochs * (len(U0) // batch)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    X, Y = torch.from_numpy(U0).float(), torch.from_numpy(UT).float()
    curve, frames = [], []
    t0 = time.time()
    for s in range(steps + 1):
        if s in snaps and snap_fn is not None:
            m.eval()
            frames.append(snap_fn(m))
            m.train()
        if val is not None and (s % 250 == 0 or s == steps):
            m.eval()
            with torch.no_grad():
                curve.append((s, float(rel_l2(m(val[0]).numpy(), val[1].numpy()).mean())))
            m.train()
        if s == steps:
            break
        j = torch.randint(0, len(X), (batch,), generator=gen)
        pred = m(X[j])
        loss = (torch.linalg.norm(pred - Y[j], dim=-1) / torch.linalg.norm(Y[j], dim=-1)).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    return m, dict(curve=curve, frames=frames, secs=time.time() - t0, params=n_params(m), steps=steps)


# ===========================================================================
# A two-dimensional "weather": forced, damped vorticity on a periodic square
# ===========================================================================
GRID = 32
VISC = 2e-3
DRAG = 0.05
FORCE_K = 2
DT_SOLVE = 0.02
SUB = 5  # solver steps per model step: one model step is 0.1 time units


class Vorticity:
    """omega_t + u . grad omega = nu Lap omega - mu omega + f(x, y), u = curl psi, Lap psi = -omega, on [0, 2 pi)^2,
    pseudo-spectral with 2/3 dealiasing and RK4.  The forcing is a fixed pattern (a 'climate'), the eddies are not."""

    def __init__(self, N=GRID):
        k = np.fft.fftfreq(N, 1.0 / N)
        self.kx, self.ky = np.meshgrid(k, k)
        self.k2 = self.kx ** 2 + self.ky ** 2
        self.k2i = np.where(self.k2 > 0, 1 / np.maximum(self.k2, 1e-12), 0)
        self.mask = (np.abs(self.kx) < N / 3) & (np.abs(self.ky) < N / 3)
        x = np.linspace(0, 2 * np.pi, N, endpoint=False)
        X, Y = np.meshgrid(x, x)
        self.f = 0.8 * (np.sin(FORCE_K * Y) + 0.5 * np.cos(FORCE_K * X + 1.0))
        self.N = N

    def rhs(self, wh):
        psih = wh * self.k2i
        u = np.real(np.fft.ifft2(1j * self.ky * psih))
        v = np.real(np.fft.ifft2(-1j * self.kx * psih))
        wx = np.real(np.fft.ifft2(1j * self.kx * wh))
        wy = np.real(np.fft.ifft2(1j * self.ky * wh))
        adv = np.fft.fft2(u * wx + v * wy) * self.mask
        return -adv - VISC * self.k2 * wh - DRAG * wh + np.fft.fft2(self.f)

    def step(self, w, n=SUB):
        wh = np.fft.fft2(w)
        for _ in range(n):
            k1 = self.rhs(wh)
            k2 = self.rhs(wh + 0.5 * DT_SOLVE * k1)
            k3 = self.rhs(wh + 0.5 * DT_SOLVE * k2)
            k4 = self.rhs(wh + DT_SOLVE * k3)
            wh = wh + DT_SOLVE / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return np.real(np.fft.ifft2(wh))


def weather_runs(n_runs, length, seed, spinup=150):
    """``n_runs`` trajectories of ``length`` model steps after a spin-up from random small eddies."""
    rng = np.random.default_rng(seed)
    sim = Vorticity()
    out = np.zeros((n_runs, length, GRID, GRID), np.float32)
    for r in range(n_runs):
        w = rng.normal(0, 1, (GRID, GRID))
        wh = np.fft.fft2(w) * np.exp(-sim.k2 / 8.0)
        w = np.real(np.fft.ifft2(wh)) * 3
        for _ in range(spinup):
            w = sim.step(w)
        for t in range(length):
            out[r, t] = w
            w = sim.step(w)
    return out


# ---------------------------------------------------------------------------
# The mesh: grid points -> mesh nodes (several levels) -> grid points
# ---------------------------------------------------------------------------
def build_mesh(levels=(16, 8, 4), N=GRID):
    """Mesh nodes on a regular 16 x 16 lattice of the periodic square; the 'multimesh' keeps the edges of the 16, 8
    and 4 lattices on the same nodes, so a message can cross the square in a few steps (GraphCast refines an
    icosahedron six times and keeps every level's edges).  Returns mesh positions, mesh edges (src, dst, offset), and
    the grid->mesh and mesh->grid edges with their offsets."""
    M = levels[0]
    pos = np.stack(np.meshgrid(np.arange(M), np.arange(M)), -1).reshape(-1, 2) * (2 * np.pi / M)
    edges = set()
    for L in levels:
        step = M // L
        for i in range(0, M, step):
            for j in range(0, M, step):
                for di, dj in ((step, 0), (0, step)):
                    a = i * M + j
                    b = ((i + di) % M) * M + (j + dj) % M
                    edges.add((a, b))
                    edges.add((b, a))
    edges = np.array(sorted(edges))

    def offset(p, q):
        d = q - p
        return (d + np.pi) % (2 * np.pi) - np.pi

    m_off = offset(pos[edges[:, 0]], pos[edges[:, 1]])
    gpos = np.stack(np.meshgrid(np.arange(N), np.arange(N)), -1).reshape(-1, 2) * (2 * np.pi / N)
    g2m, m2g = [], []
    cell = 2 * np.pi / M
    for g, p in enumerate(gpos):
        d = np.abs(offset(p, pos)).max(1)
        for mnode in np.flatnonzero(d <= cell * 0.75 + 1e-9):
            g2m.append((g, mnode))
        for mnode in np.argsort(np.linalg.norm(offset(p, pos), axis=1))[:4]:
            m2g.append((mnode, g))
    g2m, m2g = np.array(g2m), np.array(m2g)
    return dict(pos=pos, edges=edges, m_off=m_off.astype(np.float32), gpos=gpos, g2m=g2m,
                g2m_off=offset(gpos[g2m[:, 0]], pos[g2m[:, 1]]).astype(np.float32), m2g=m2g,
                m2g_off=offset(pos[m2g[:, 0]], gpos[m2g[:, 1]]).astype(np.float32))


def emlp(a, b, h):
    return nn.Sequential(nn.Linear(a, h), nn.SiLU(), nn.Linear(h, b), nn.LayerNorm(b))


class MeshGNN(nn.Module):
    """Encoder (grid -> mesh), processor (``layers`` rounds of message passing on the mesh), decoder (mesh -> grid),
    every edge an MLP of its endpoints and its offset, residual updates; the output is the change of the field over
    one step.  Static inputs: sin and cos of each grid point's position (GraphCast gives its grid nodes latitude,
    longitude and the land-sea mask)."""

    def __init__(self, mesh, hidden=32, layers=6, inputs=2):
        super().__init__()
        self.mesh = {k: (torch.from_numpy(v) if isinstance(v, np.ndarray) else v) for k, v in mesh.items()}
        self.n_mesh = len(mesh["pos"])
        self.g_in = emlp(inputs + 4, hidden, hidden)
        self.m_in = emlp(4, hidden, hidden)
        self.enc_e = emlp(2 * hidden + 2, hidden, hidden)
        self.enc_n = emlp(2 * hidden, hidden, hidden)
        self.proc_e = nn.ModuleList([emlp(2 * hidden + 2, hidden, hidden) for _ in range(layers)])
        self.proc_n = nn.ModuleList([emlp(2 * hidden, hidden, hidden) for _ in range(layers)])
        self.dec_e = emlp(2 * hidden + 2, hidden, hidden)
        self.dec_n = emlp(2 * hidden, hidden, hidden)
        self.out = nn.Sequential(nn.Linear(hidden, hidden), nn.SiLU(), nn.Linear(hidden, 1))
        gp, mp = mesh["gpos"], mesh["pos"]
        self.register_buffer("g_static", torch.from_numpy(np.c_[np.sin(gp), np.cos(gp)].astype(np.float32)))
        self.register_buffer("m_static", torch.from_numpy(np.c_[np.sin(mp), np.cos(mp)].astype(np.float32)))

    @staticmethod
    def scatter(msg, dst, n):
        out = torch.zeros(msg.shape[0], n, msg.shape[-1])
        return out.index_add_(1, dst, msg)

    def forward(self, w_now, w_prev):
        B = w_now.shape[0]
        g = torch.stack([w_now.reshape(B, -1), w_prev.reshape(B, -1)], -1)
        hg = self.g_in(torch.cat([g, self.g_static.expand(B, -1, -1)], -1))
        hm = self.m_in(self.m_static.expand(B, -1, -1))
        s, d = self.mesh["g2m"][:, 0], self.mesh["g2m"][:, 1]
        e = self.enc_e(torch.cat([hg[:, s], hm[:, d], self.mesh["g2m_off"].expand(B, -1, -1)], -1))
        hm = hm + self.enc_n(torch.cat([hm, self.scatter(e, d, self.n_mesh)], -1))
        s, d = self.mesh["edges"][:, 0], self.mesh["edges"][:, 1]
        off = self.mesh["m_off"].expand(B, -1, -1)
        for fe, fn in zip(self.proc_e, self.proc_n):
            e = fe(torch.cat([hm[:, s], hm[:, d], off], -1))
            hm = hm + fn(torch.cat([hm, self.scatter(e, d, self.n_mesh)], -1))
        s, d = self.mesh["m2g"][:, 0], self.mesh["m2g"][:, 1]
        e = self.dec_e(torch.cat([hm[:, s], hg[:, d], self.mesh["m2g_off"].expand(B, -1, -1)], -1))
        hg = hg + self.dec_n(torch.cat([hg, self.scatter(e, d, hg.shape[1])], -1))
        return self.out(hg).reshape(B, GRID, GRID)


def train_weather(mesh, runs, seed, steps, batch=8, lr=1e-3, rollout_from=None, scale=None, snaps=(), snap_fn=None):
    """One-step training on (state t-1, state t) -> change to t+1, normalized; for the last steps (``rollout_from``)
    two steps are rolled out and both are scored, as GraphCast lengthens its rollouts during training."""
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(7000 + seed)
    m = MeshGNN(mesh)
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    W = torch.from_numpy(runs)
    sw, sd = scale
    R, T = W.shape[:2]
    curve, frames = [], []
    t0 = time.time()
    run = None
    for s in range(steps + 1):
        if s in snaps and snap_fn is not None:
            m.eval()
            frames.append(snap_fn(m))
            m.train()
        if s == steps:
            break
        k = 2 if (rollout_from is not None and s >= rollout_from) else 1
        r = torch.randint(0, R, (batch,), generator=gen)
        t = torch.randint(1, T - k, (batch,), generator=gen)
        prev, now = W[r, t - 1] / sw, W[r, t] / sw
        loss = 0
        for j in range(1, k + 1):
            delta = m(now, prev)
            target = (W[r, t + j] - W[r, t + j - 1]) / sd
            loss = loss + F.mse_loss(delta, target)
            prev, now = now, now + delta * sd / sw
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run = float(loss.detach()) / k if run is None else 0.98 * run + 0.02 * float(loss.detach()) / k
        if s % 100 == 0:
            curve.append((s, run))
    m.eval()
    return m, dict(curve=curve, frames=frames, secs=time.time() - t0, params=n_params(m))


def rollout(m, w_prev, w_now, steps, scale):
    sw, sd = scale
    out = []
    prev, now = torch.from_numpy(w_prev) / sw, torch.from_numpy(w_now) / sw
    with torch.no_grad():
        for _ in range(steps):
            delta = m(now, prev)
            prev, now = now, now + delta * sd / sw
            out.append((now * sw).numpy())
    return np.stack(out, 1)  # (B, steps, N, N)
