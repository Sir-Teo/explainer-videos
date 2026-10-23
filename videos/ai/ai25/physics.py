"""Point clouds that move: the charged n-body system, E(3)-equivariant and plain networks for it, invariant energy
networks, and the spherical harmonics' rotation blocks (Part 25, chapters 2 and 7, and the hook).

The system follows Kipf et al. (2018) and Satorras, Hoogeboom & Welling (2021): five particles in 3D with charges +-1
pushing and pulling by a softened Coulomb force; given the positions, velocities and charges at time 0, predict the
positions at time 1 (1,000 leapfrog steps).  Everything is seeded; nothing here runs at import.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

N_PART = 5
EPS = 0.1  # softening length of the Coulomb force
DT, STEPS = 0.001, 1000  # leapfrog step and number of steps: the target is the state at t = 1


# ---------------------------------------------------------------------------
# The simulator
# ---------------------------------------------------------------------------
def forces(x: np.ndarray, q: np.ndarray) -> np.ndarray:
    """(B, n, 3) positions, (B, n) charges -> (B, n, 3) forces q_i q_j (x_i - x_j) / (r^2 + eps^2)^{3/2}."""
    d = x[:, :, None, :] - x[:, None, :, :]
    r2 = (d ** 2).sum(-1) + EPS ** 2
    w = (q[:, :, None] * q[:, None, :]) / r2 ** 1.5
    idx = np.arange(x.shape[1])
    w[:, idx, idx] = 0.0
    return (w[..., None] * d).sum(2)


def potential(x: np.ndarray, q: np.ndarray) -> np.ndarray:
    """The softened Coulomb energy sum_{i<j} q_i q_j / sqrt(r^2 + eps^2) of each system, (B,)."""
    d = x[:, :, None, :] - x[:, None, :, :]
    r = np.sqrt((d ** 2).sum(-1) + EPS ** 2)
    w = (q[:, :, None] * q[:, None, :]) / r
    iu = np.triu_indices(x.shape[1], 1)
    return w[:, iu[0], iu[1]].sum(-1)


def simulate(B: int, seed: int, keep_every: int = 0):
    """B systems from random starts; returns x0, v0, q, xT (and the trajectories every ``keep_every`` steps)."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 1.0, (B, N_PART, 3))
    v = rng.normal(0.0, 0.5, (B, N_PART, 3))
    q = rng.choice([-1.0, 1.0], (B, N_PART))
    x0, v0 = x.copy(), v.copy()
    f = forces(x, q)
    traj = [x.copy()] if keep_every else None
    for s in range(1, STEPS + 1):
        v = v + 0.5 * DT * f
        x = x + DT * v
        f = forces(x, q)
        v = v + 0.5 * DT * f
        if keep_every and s % keep_every == 0:
            traj.append(x.copy())
    out = dict(x0=x0.astype(np.float32), v0=v0.astype(np.float32), q=q.astype(np.float32), xT=x.astype(np.float32))
    if keep_every:
        out["traj"] = np.stack(traj, 1).astype(np.float32)  # (B, frames, n, 3)
    return out


def energy_drift(B=200, seed=123) -> float:
    """Relative change of total energy over the 1,000 steps (a check on the integrator)."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 1.0, (B, N_PART, 3))
    v = rng.normal(0.0, 0.5, (B, N_PART, 3))
    q = rng.choice([-1.0, 1.0], (B, N_PART))
    e0 = 0.5 * (v ** 2).sum((1, 2)) + potential(x, q)
    f = forces(x, q)
    for _ in range(STEPS):
        v = v + 0.5 * DT * f
        x = x + DT * v
        f = forces(x, q)
        v = v + 0.5 * DT * f
    e1 = 0.5 * (v ** 2).sum((1, 2)) + potential(x, q)
    return float(np.median(np.abs(e1 - e0) / np.abs(e0).clip(1e-3)))


# ---------------------------------------------------------------------------
# Rotations
# ---------------------------------------------------------------------------
def random_rotations(n: int, gen: torch.Generator) -> torch.Tensor:
    """n rotation matrices, uniform on SO(3) (QR of a Gaussian matrix, signs fixed, determinant +1)."""
    A = torch.randn(n, 3, 3, generator=gen)
    Q, R = torch.linalg.qr(A)
    Q = Q * torch.sign(torch.diagonal(R, dim1=-2, dim2=-1)).unsqueeze(-2)
    det = torch.linalg.det(Q)
    Q[det < 0, :, 0] *= -1
    return Q


def rot_axis(axis, theta: float) -> np.ndarray:
    """Rotation by ``theta`` about a unit ``axis`` (Rodrigues)."""
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * K @ K


# ---------------------------------------------------------------------------
# Networks for the dynamics: (x0, v0, q) -> xT
# ---------------------------------------------------------------------------
def mlp(sizes, act=nn.SiLU, last_act=False) -> nn.Sequential:
    layers = []
    for i, (a, b) in enumerate(zip(sizes, sizes[1:])):
        layers.append(nn.Linear(a, b))
        if i < len(sizes) - 2 or last_act:
            layers.append(act())
    return nn.Sequential(*layers)


class EGNN(nn.Module):
    """E(n)-equivariant graph network with velocities (Satorras, Hoogeboom & Welling 2021, eq. 7), fully connected.

        m_ij = phi_e(h_i, h_j, |x_i - x_j|^2, q_i q_j)
        v_i <- phi_v(h_i) v_i + (1/(n-1)) sum_j (x_i - x_j) phi_x(m_ij)
        x_i <- x_i + v_i
        h_i <- h_i + phi_h(h_i, sum_j m_ij)
    Only distances and products of charges enter the messages, and positions are moved along x_i - x_j and v_i, so a
    rotation or translation of the input moves the output the same way."""

    def __init__(self, hidden=64, layers=4):
        super().__init__()
        self.embed = nn.Linear(2, hidden)  # |v_i| and q_i
        self.phi_e = nn.ModuleList([mlp([2 * hidden + 2, hidden, hidden], last_act=True) for _ in range(layers)])
        self.phi_x = nn.ModuleList()
        for _ in range(layers):
            lin = nn.Linear(hidden, 1, bias=False)
            nn.init.xavier_uniform_(lin.weight, gain=0.001)
            self.phi_x.append(nn.Sequential(nn.Linear(hidden, hidden), nn.SiLU(), lin))
        self.phi_v = nn.ModuleList([mlp([hidden, hidden, 1]) for _ in range(layers)])
        self.phi_h = nn.ModuleList([mlp([2 * hidden, hidden, hidden]) for _ in range(layers)])

    def forward(self, x, v, q):
        B, n, _ = x.shape
        h = self.embed(torch.stack([v.norm(dim=-1), q], -1))
        a = (q[:, :, None] * q[:, None, :]).unsqueeze(-1)
        eye = torch.eye(n, dtype=x.dtype).unsqueeze(0).unsqueeze(-1)
        for pe, px, pv, ph in zip(self.phi_e, self.phi_x, self.phi_v, self.phi_h):
            d = x[:, :, None, :] - x[:, None, :, :]
            d2 = (d ** 2).sum(-1, keepdim=True)
            hi = h[:, :, None, :].expand(B, n, n, h.shape[-1])
            hj = h[:, None, :, :].expand(B, n, n, h.shape[-1])
            m = pe(torch.cat([hi, hj, d2, a], -1)) * (1 - eye)
            v = pv(h) * v + (d * px(m)).sum(2) / (n - 1)
            x = x + v
            h = h + ph(torch.cat([h, m.sum(2)], -1))
        return x


class PlainGNN(nn.Module):
    """The same message passing with the coordinates fed in as ordinary numbers: permutation-equivariant, but not
    rotation- or translation-equivariant."""

    def __init__(self, hidden=64, layers=4):
        super().__init__()
        self.embed = nn.Linear(7, hidden)  # x, v, q
        self.phi_e = nn.ModuleList([mlp([2 * hidden + 1, hidden, hidden], last_act=True) for _ in range(layers)])
        self.phi_h = nn.ModuleList([mlp([2 * hidden, hidden, hidden]) for _ in range(layers)])
        self.out = mlp([hidden, hidden, 3])

    def forward(self, x, v, q):
        B, n, _ = x.shape
        h = self.embed(torch.cat([x, v, q.unsqueeze(-1)], -1))
        a = (q[:, :, None] * q[:, None, :]).unsqueeze(-1)
        eye = torch.eye(n, dtype=x.dtype).unsqueeze(0).unsqueeze(-1)
        for pe, ph in zip(self.phi_e, self.phi_h):
            hi = h[:, :, None, :].expand(B, n, n, h.shape[-1])
            hj = h[:, None, :, :].expand(B, n, n, h.shape[-1])
            m = pe(torch.cat([hi, hj, a], -1)) * (1 - eye)
            h = h + ph(torch.cat([h, m.sum(2)], -1))
        return x + self.out(h)


class PlainMLP(nn.Module):
    """All 35 numbers in, 15 out: no symmetry at all (not even the particles' order)."""

    def __init__(self, hidden=256):
        super().__init__()
        self.net = mlp([N_PART * 7, hidden, hidden, hidden, N_PART * 3])

    def forward(self, x, v, q):
        B = x.shape[0]
        z = torch.cat([x.reshape(B, -1), v.reshape(B, -1), q], -1)
        return x + self.net(z).reshape(B, N_PART, 3)


DYN_MODELS = {"egnn": EGNN, "gnn": PlainGNN, "mlp": PlainMLP, "mlp_aug": PlainMLP}


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


def augment(x, v, y, gen):
    """A random rotation and translation of a batch (inputs and targets alike)."""
    R = random_rotations(x.shape[0], gen)
    t = torch.randn(x.shape[0], 1, 3, generator=gen)
    rot = lambda a: torch.einsum("bij,bnj->bni", R, a)  # noqa: E731
    return rot(x) + t, rot(v), rot(y) + t


def train_dynamics(kind: str, data: dict, n_train: int, seed: int, steps: int, batch=100, lr=1e-3,
                   snaps=(), snap_fn=None, val=None):
    """Train one dynamics model on the first ``n_train`` training systems.  Returns the model and a record: the
    validation MSE every 100 steps, and ``snap_fn(model)`` at the steps in ``snaps``."""
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(1000 + seed)
    m = DYN_MODELS[kind]()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    X0, V0, Q, XT = (torch.from_numpy(data[k][:n_train]) for k in ("x0", "v0", "q", "xT"))
    curve, frames, best = [], [], (float("inf"), None)
    t0 = time.time()
    for s in range(steps + 1):
        if s in snaps and snap_fn is not None:
            m.eval()
            frames.append(snap_fn(m))
            m.train()
        if val is not None and (s % 100 == 0 or s == steps):
            m.eval()
            with torch.no_grad():
                e = float(F.mse_loss(m(*val[:3]), val[3]))
            m.train()
            curve.append((s, e))
            if e < best[0]:
                best = (e, {k: t.clone() for k, t in m.state_dict().items()})
        if s == steps:
            break
        j = torch.randint(0, n_train, (min(batch, n_train),), generator=gen)
        x, v, q, y = X0[j], V0[j], Q[j], XT[j]
        if kind == "mlp_aug":
            x, v, y = augment(x, v, y, gen)
        loss = F.mse_loss(m(x, v, q), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    if best[1] is not None:  # early stopping on the validation set, as Satorras et al.
        m.load_state_dict(best[1])
    m.eval()
    return m, dict(curve=curve, frames=frames, secs=time.time() - t0, params=n_params(m))


# ---------------------------------------------------------------------------
# Networks for the energy: (x, q) -> U, which must not change when the molecule turns
# ---------------------------------------------------------------------------
class EnergyMLP(nn.Module):
    def __init__(self, hidden=256):
        super().__init__()
        self.net = mlp([N_PART * 4, hidden, hidden, hidden, 1])

    def forward(self, x, q):
        return self.net(torch.cat([x.reshape(x.shape[0], -1), q], -1)).squeeze(-1)


class InvariantNet(nn.Module):
    """SchNet-style (Schutt et al. 2017): features from distances only (radial basis functions), continuous-filter
    messages between particles, a sum over particles at the end.  Rotations, translations and reorderings of the
    particles leave every input it sees unchanged."""

    def __init__(self, hidden=64, rbf=24, layers=3, cutoff=6.0):
        super().__init__()
        self.register_buffer("mu", torch.linspace(0.0, cutoff, rbf))
        self.gamma = (rbf / cutoff) ** 2
        self.embed = nn.Linear(1, hidden)
        self.filt = nn.ModuleList([mlp([rbf + 1, hidden, hidden]) for _ in range(layers)])
        self.upd = nn.ModuleList([mlp([2 * hidden, hidden, hidden]) for _ in range(layers)])
        self.out = mlp([hidden, hidden, 1])

    def forward(self, x, q):
        B, n, _ = x.shape
        d = torch.sqrt(((x[:, :, None] - x[:, None]) ** 2).sum(-1) + 1e-9)
        e = torch.exp(-self.gamma * (d.unsqueeze(-1) - self.mu) ** 2)
        a = (q[:, :, None] * q[:, None, :]).unsqueeze(-1)
        mask = (1 - torch.eye(n, dtype=x.dtype)).unsqueeze(0).unsqueeze(-1)
        h = self.embed(q.unsqueeze(-1))
        for f, u in zip(self.filt, self.upd):
            w = f(torch.cat([e, a], -1)) * mask
            msg = (w * h[:, None, :, :]).sum(2)
            h = h + u(torch.cat([h, msg], -1))
        return self.out(h).sum((1, 2))


ENERGY_MODELS = {"mlp": EnergyMLP, "mlp_aug": EnergyMLP, "inv": InvariantNet}


def train_energy(kind: str, x, q, u, seed: int, steps: int, batch=100, lr=1e-3, val=None):
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(2000 + seed)
    m = ENERGY_MODELS[kind]()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    curve = []
    t0 = time.time()
    for s in range(steps + 1):
        if val is not None and (s % 100 == 0 or s == steps):
            with torch.no_grad():
                curve.append((s, float(F.mse_loss(m(val[0], val[1]), val[2]))))
        if s == steps:
            break
        j = torch.randint(0, len(x), (batch,), generator=gen)
        xb, qb, ub = x[j], q[j], u[j]
        if kind == "mlp_aug":
            R = random_rotations(len(j), gen)
            xb = torch.einsum("bij,bnj->bni", R, xb) + torch.randn(len(j), 1, 3, generator=gen)
        loss = F.mse_loss(m(xb, qb), ub)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    return m, dict(curve=curve, secs=time.time() - t0, params=n_params(m))


# ---------------------------------------------------------------------------
# Spherical harmonics: how a rotation acts on them
# ---------------------------------------------------------------------------
def real_sh(P: np.ndarray) -> np.ndarray:
    """The nine real spherical harmonics of degree 0, 1, 2 at unit vectors P (N, 3), orthonormal on the sphere."""
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    c0 = 0.5 * math.sqrt(1 / math.pi)
    c1 = math.sqrt(3 / (4 * math.pi))
    c2 = 0.5 * math.sqrt(15 / math.pi)
    c20 = 0.25 * math.sqrt(5 / math.pi)
    return np.stack([np.full_like(x, c0),
                     c1 * y, c1 * z, c1 * x,
                     c2 * x * y, c2 * y * z, c20 * (3 * z ** 2 - 1), c2 * x * z, 0.5 * c2 * (x ** 2 - y ** 2)], 1)


def wigner_blocks(R: np.ndarray, n=20000, seed=0) -> np.ndarray:
    """The 9 x 9 matrix D with Y(R^T p) = D Y(p), found by least squares over random points of the sphere: a rotation
    only mixes harmonics of the same degree (blocks of 1, 3 and 5)."""
    rng = np.random.default_rng(seed)
    P = rng.normal(size=(n, 3))
    P /= np.linalg.norm(P, axis=1, keepdims=True)
    A = real_sh(P)
    Bm = real_sh(P @ R)  # rows: Y(R^T p)
    D, *_ = np.linalg.lstsq(A, Bm, rcond=None)
    return D.T
