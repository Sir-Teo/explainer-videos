"""Toy proteins (Part 25, chapters 8-12): chains of C-alpha atoms built from bond lengths, angles and torsions; a
structure recovered from its distances (classical MDS, and gradient descent on noisy partial distances, as AlphaFold 1
did with its predicted distances); frames and the frame-aligned point error (FAPE); a pair representation completed by
triangle updates with recycling (AlphaFold 2's Evoformer, in miniature); and denoising diffusion on 2D chains, with an
E(2)-equivariant denoiser against a plain one trained with random rotations (AlphaFold 3's choice).  Seeded throughout.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

BOND = 3.8  # angstroms between consecutive C-alpha atoms
SS = {  # virtual C-alpha bond angle and torsion (degrees) of a helix and a strand
    "H": (91.0, 50.0),
    "E": (120.0, -170.0),
}


# ---------------------------------------------------------------------------
# Building chains
# ---------------------------------------------------------------------------
def place(a, b, c, r, theta, phi):
    """The next atom d after a, b, c: |cd| = r, angle bcd = theta, dihedral abcd = phi (radians), the NeRF rule."""
    bc = c - b
    bc /= np.linalg.norm(bc)
    n = np.cross(b - a, bc)
    n /= np.linalg.norm(n)
    m = np.stack([bc, np.cross(n, bc), n], 1)
    d2 = np.array([-r * math.cos(theta), r * math.sin(theta) * math.cos(phi), r * math.sin(theta) * math.sin(phi)])
    return c + m @ d2


def build(angles, torsions, r=BOND) -> np.ndarray:
    """A chain from bond angles (len N-2) and torsions (len N-3), degrees."""
    N = len(angles) + 2
    X = np.zeros((N, 3))
    X[1] = [r, 0, 0]
    th = math.radians(angles[0])
    X[2] = X[1] + r * np.array([-math.cos(th), math.sin(th), 0])
    for i in range(3, N):
        X[i] = place(X[i - 3], X[i - 2], X[i - 1], r, math.radians(angles[i - 2]), math.radians(torsions[i - 3]))
    return X - X.mean(0)


def rg(X) -> float:
    return float(np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean()))


def min_nonbonded(X, sep=3) -> float:
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    N = len(X)
    i, j = np.triu_indices(N, sep)
    return float(D[i, j].min())


def bundle(seed=0, tries=4000):
    """A three-helix bundle of 52 C-alpha atoms: helices of 14, loops of 5 whose angles and torsions are chosen (by a
    seeded random search) to pack the helices tightly without clashes."""
    rng = np.random.default_rng(seed)
    pattern = "H" * 14 + "L" * 5 + "H" * 14 + "L" * 5 + "H" * 14
    loops = [i for i, s in enumerate(pattern) if s == "L"]
    best, best_score = None, float("inf")
    for _ in range(tries):
        la = rng.uniform(85, 130, len(loops))
        lt = rng.uniform(-180, 180, len(loops))
        ang, tor = [], []
        k = 0
        for i, s in enumerate(pattern):
            if s == "L":
                a_, t_ = la[k], lt[k]
                k += 1
            else:
                a_, t_ = SS["H"]
            ang.append(a_)
            tor.append(t_)
        X = build(ang[1:-1], tor[2:-1])
        clash = min_nonbonded(X)
        score = rg(X) + (100.0 if clash < 4.0 else 0.0)
        if score < best_score:
            best, best_score = X, score
    return best, pattern


def random_chain(rng, N=24):
    """A random protein-like chain: segments of helix, strand and loop."""
    ang, tor = [], []
    while len(ang) < N:
        kind = rng.choice(["H", "E", "L"], p=[0.45, 0.25, 0.30])
        L = int(rng.integers(3, 9))
        for _ in range(L):
            if kind == "L":
                ang.append(rng.uniform(80, 140))
                tor.append(rng.uniform(-180, 180))
            else:
                a_, t_ = SS[kind]
                ang.append(a_ + rng.normal(0, 4))
                tor.append(t_ + rng.normal(0, 10))
    return build(ang[1:N - 1], tor[2:N - 1])


def dist(X) -> np.ndarray:
    return np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))


# ---------------------------------------------------------------------------
# Coordinates from distances
# ---------------------------------------------------------------------------
def mds(D: np.ndarray, k=3):
    """Classical multidimensional scaling (Torgerson 1952): double-centre the squared distances into the Gram matrix
    and keep its top k eigenvectors.  Returns coordinates and all eigenvalues."""
    N = len(D)
    J = np.eye(N) - 1.0 / N
    Gm = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(Gm)
    order = np.argsort(w)[::-1]
    w, V = w[order], V[:, order]
    return V[:, :k] * np.sqrt(np.maximum(w[:k], 0)), w


def kabsch(P, Q, allow_reflection=False):
    """Superpose P onto Q (both centred inside): returns RMSD and the aligned P."""
    P0, Q0 = P - P.mean(0), Q - Q.mean(0)
    H = P0.T @ Q0
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    if allow_reflection:
        d = 1.0
    Dm = np.diag([1, 1, d])
    R = Vt.T @ Dm @ U.T
    A = P0 @ R.T
    return float(np.sqrt(((A - Q0) ** 2).sum(1).mean())), A + Q.mean(0)


def fold_by_descent(D_obs, W, seed, steps=1500, lr=0.05, snaps=()):
    """Gradient descent on the stress sum_{(i,j) observed} (|x_i - x_j| - d_ij)^2 from random coordinates, with a soft
    repulsion between atoms closer than 4 angstroms; AlphaFold 1 did this on a learned potential."""
    torch.manual_seed(seed)
    N = len(D_obs)
    X = (torch.randn(N, 3) * 8.0).requires_grad_(True)
    Dt, Wt = torch.from_numpy(D_obs).float(), torch.from_numpy(W).float()
    opt = torch.optim.Adam([X], lr)
    frames, curve = [], []
    iu = torch.triu_indices(N, N, 1)
    for s in range(steps + 1):
        if s in snaps:
            frames.append(X.detach().numpy().copy())
        d = torch.sqrt(((X[:, None] - X[None]) ** 2).sum(-1) + 1e-8)
        stress = (Wt * (d - Dt) ** 2)[iu[0], iu[1]].sum() / Wt[iu[0], iu[1]].sum()
        rep = (F.relu(4.0 - d) ** 2)[iu[0], iu[1]].mean()
        loss = stress + rep
        if s % 25 == 0:
            curve.append((s, float(stress.detach())))
        if s == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    return X.detach().numpy(), frames, curve


def frames_of(X):
    """A frame (rotation R_i, origin t_i) at every inner residue, from its neighbours: e1 along the next bond, e2 in the
    plane of the two bonds, e3 = e1 x e2 (right-handed by construction).  AlphaFold builds its frames from N, C-alpha
    and C the same way."""
    t = X[1:-1]
    e1 = X[2:] - t
    e1 /= np.linalg.norm(e1, axis=1, keepdims=True)
    u = X[:-2] - t
    e2 = u - (u * e1).sum(1, keepdims=True) * e1
    e2 /= np.linalg.norm(e2, axis=1, keepdims=True)
    e3 = np.cross(e1, e2)
    return np.stack([e1, e2, e3], 2), t  # R: columns e1 e2 e3


def fape(Xp, Xt, clamp=10.0, Z=10.0) -> float:
    """Frame-aligned point error (Jumper et al. 2021): every atom seen from every frame, predicted against true,
    clamped at 10 angstroms and divided by Z = 10."""
    Rp, tp = frames_of(Xp)
    Rt, tt = frames_of(Xt)
    lp = np.einsum("fji,fnj->fni", Rp, Xp[None] - tp[:, None])  # R_f^T (x_n - t_f)
    lt = np.einsum("fji,fnj->fni", Rt, Xt[None] - tt[:, None])
    e = np.sqrt(((lp - lt) ** 2).sum(-1) + 1e-8)
    return float(np.minimum(e, clamp).mean() / Z)


def drmsd(Xp, Xt) -> float:
    """Root-mean-square difference of all pairwise distances: blind to reflections."""
    i, j = np.triu_indices(len(Xp), 1)
    return float(np.sqrt(((dist(Xp)[i, j] - dist(Xt)[i, j]) ** 2).mean()))


# ---------------------------------------------------------------------------
# The pair representation: completing a distance matrix
# ---------------------------------------------------------------------------
PAIR_N = 24
RELPOS = 8  # relative position, clipped to +-8: 17 one-hot bins


def pair_batch(rng, B, N=PAIR_N, frac=0.25, noise=1.0):
    """B random chains; each pair's distance is seen (with noise) with probability ``frac``; consecutive atoms are
    always seen (3.8 angstroms).  Returns inputs (B, N, N, 2), true distances (B, N, N), the mask of seen pairs."""
    D = np.stack([dist(random_chain(rng, N)) for _ in range(B)])
    M = rng.uniform(size=D.shape) < frac
    M = np.triu(M, 1)
    M = M | M.transpose(0, 2, 1)
    idx = np.arange(N - 1)
    M[:, idx, idx + 1] = M[:, idx + 1, idx] = True
    Dn = D + rng.normal(0, noise, D.shape)
    Dn = (Dn + Dn.transpose(0, 2, 1)) / 2
    Dn[:, idx, idx + 1] = Dn[:, idx + 1, idx] = BOND
    inp = np.stack([np.where(M, Dn, 0.0) / 10.0, M.astype(float)], -1)
    return inp.astype(np.float32), D.astype(np.float32), M


def relpos(N=PAIR_N):
    r = np.clip(np.arange(N)[None] - np.arange(N)[:, None], -RELPOS, RELPOS) + RELPOS
    return torch.from_numpy(np.eye(2 * RELPOS + 1, dtype=np.float32)[r])


class TriangleMult(nn.Module):
    """AlphaFold 2's triangle multiplicative update: z_ij += g_ij * Lin(LN(sum_k a_ik b_jk)) ('outgoing': edges ik and
    jk close the triangle) or sum_k a_ki b_kj ('incoming')."""

    def __init__(self, c, outgoing=True):
        super().__init__()
        self.ln, self.ln_out = nn.LayerNorm(c), nn.LayerNorm(c)
        self.a, self.b, self.ga, self.gb = (nn.Linear(c, c) for _ in range(4))
        self.g, self.o = nn.Linear(c, c), nn.Linear(c, c)
        self.outgoing = outgoing

    def forward(self, z):
        x = self.ln(z)
        a = torch.sigmoid(self.ga(x)) * self.a(x)
        b = torch.sigmoid(self.gb(x)) * self.b(x)
        n = z.shape[1]
        if self.outgoing:
            t = torch.einsum("bikc,bjkc->bijc", a, b) / n
        else:
            t = torch.einsum("bkic,bkjc->bijc", a, b) / n
        return z + torch.sigmoid(self.g(x)) * self.o(self.ln_out(t))


class Transition(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.ln, self.f = nn.LayerNorm(c), nn.Sequential(nn.Linear(c, 2 * c), nn.ReLU(), nn.Linear(2 * c, c))

    def forward(self, z):
        return z + self.f(self.ln(z))


class PairModel(nn.Module):
    """Pair features z_ij from the seen distance, the mask and the relative position; then ``blocks`` of updates; a
    head reads the distance of every pair.  ``triangle=False``: each pair is updated on its own (transitions only),
    so it can't use what the other pairs know.  ``recycle``: the previous pass's pair features and distances come
    back in, as AlphaFold 2 recycles its outputs."""

    def __init__(self, c=32, blocks=3, triangle=True, recycle=False):
        super().__init__()
        self.embed = nn.Linear(2 + 2 * RELPOS + 1, c)
        self.blocks = nn.ModuleList()
        for _ in range(blocks):
            if triangle:
                self.blocks.append(nn.ModuleList([TriangleMult(c, True), TriangleMult(c, False), Transition(c)]))
            else:
                self.blocks.append(nn.ModuleList([Transition(c), Transition(c), Transition(c)]))
        self.head = nn.Sequential(nn.LayerNorm(c), nn.Linear(c, c), nn.ReLU(), nn.Linear(c, 1))
        self.recycle = recycle
        if recycle:
            self.ln_prev = nn.LayerNorm(c)
            self.d_prev = nn.Linear(16, c)

    def one(self, inp, prev=None):
        B, N = inp.shape[:2]
        z = self.embed(torch.cat([inp, relpos(N).expand(B, N, N, -1)], -1))
        if self.recycle and prev is not None:
            zp, dp = prev
            bins = torch.linspace(0.0, 3.0, 16)
            dh = torch.exp(-((dp.unsqueeze(-1) - bins) ** 2) / 0.02)
            z = z + self.ln_prev(zp) + self.d_prev(dh)
        for blk in self.blocks:
            for f in blk:
                z = f(z)
        d = F.softplus(self.head(z).squeeze(-1))
        d = (d + d.transpose(1, 2)) / 2
        return z, d

    def forward(self, inp, cycles=1):
        prev = None
        for c in range(cycles):
            if c < cycles - 1:
                with torch.no_grad():
                    z, d = self.one(inp, prev)
                prev = (z.detach(), d.detach())
            else:
                z, d = self.one(inp, prev)
        return d * 10.0  # angstroms


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


def train_pair(kind: str, seed: int, steps=3000, batch=32, lr=1e-3, val=None, max_cycles=4):
    torch.manual_seed(seed)
    rng = np.random.default_rng(3000 + seed)
    m = PairModel(triangle=kind != "pairwise", recycle=kind == "recycle",
                  blocks=3 if kind != "pairwise" else 4)
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    eye = torch.eye(PAIR_N, dtype=torch.bool)
    curve = []
    t0 = time.time()
    for s in range(steps + 1):
        if val is not None and (s % 250 == 0 or s == steps):
            curve.append((s, pair_error(m, val, cycles=max_cycles if kind == "recycle" else 1)["hidden"]))
        if s == steps:
            break
        inp, D, M = pair_batch(rng, batch)
        cyc = int(rng.integers(1, max_cycles + 1)) if kind == "recycle" else 1
        pred = m(torch.from_numpy(inp), cycles=cyc)
        Dt = torch.from_numpy(D)
        loss = ((pred - Dt) ** 2)[:, ~eye].mean() / 100.0
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    return m, dict(curve=curve, secs=time.time() - t0, params=n_params(m))


def pair_error(m, val, cycles=1):
    inp, D, M = val
    with torch.no_grad():
        P = m(torch.from_numpy(inp), cycles=cycles).numpy()
    N = D.shape[1]
    sep = np.abs(np.arange(N)[None] - np.arange(N)[:, None])
    hid = (~M) & (sep[None] >= 3)
    seen = M & (sep[None] >= 3)
    err = (P - D) ** 2
    viol = triangle_violations(P)
    return dict(hidden=float(np.sqrt(err[hid].mean())), seen=float(np.sqrt(err[seen].mean())), viol=viol)


def triangle_violations(P, tol=0.5) -> float:
    """Fraction of triples (i, j, k) whose predicted distances break the triangle inequality by more than ``tol``."""
    a = P[:, :, :, None]
    b = P[:, :, None, :]
    c = P[:, None, :, :]  # d_jk (= d_kj) with axes (i, j, k)
    bad = a > b + c + tol  # d_ij > d_ik + d_kj ... computed for all triples
    return float(bad.mean())


# ---------------------------------------------------------------------------
# Diffusion on 2D chains
# ---------------------------------------------------------------------------
CHAIN_N = 12
T_DIFF = 200


def chain2d(rng, n=CHAIN_N):
    """A compact self-avoiding chain in the plane with unit bonds: turning angles of 50-110 degrees, mostly one way,
    kept only if no two atoms come closer than 0.8 and the radius of gyration is below 1.35."""
    while True:
        sgn = 1 if rng.uniform() < 0.5 else -1
        ang = 0.0
        P = [np.zeros(2)]
        for i in range(1, n):
            turn = rng.uniform(50, 110) * (sgn if rng.uniform() < 0.8 else -sgn)
            ang += math.radians(turn) if i > 1 else rng.uniform(0, 2 * math.pi)
            P.append(P[-1] + np.array([math.cos(ang), math.sin(ang)]))
        P = np.array(P)
        D = np.sqrt(((P[:, None] - P[None]) ** 2).sum(-1))
        i, j = np.triu_indices(n, 2)
        if D[i, j].min() > 0.8 and rg(np.c_[P, np.zeros(n)]) < 1.35:
            return P - P.mean(0)


def chain_dataset(count, seed):
    rng = np.random.default_rng(seed)
    return np.array([chain2d(rng) for _ in range(count)], np.float32)


def schedule(T=T_DIFF):
    """The cosine noise schedule (Nichol & Dhariwal 2021): alpha-bar from 1 down to almost 0."""
    s = 0.008
    t = np.linspace(0, T, T + 1)
    f = np.cos((t / T + s) / (1 + s) * math.pi / 2) ** 2
    ab = f / f[0]
    beta = np.clip(1 - ab[1:] / ab[:-1], 1e-5, 0.999)
    return torch.tensor(np.cumprod(1 - beta), dtype=torch.float32), torch.tensor(beta, dtype=torch.float32)


def t_embed(t, dim=16):
    freqs = torch.exp(torch.linspace(0, math.log(100.0), dim // 2))
    a = t.float().unsqueeze(-1) / T_DIFF * freqs
    return torch.cat([torch.sin(a), torch.cos(a)], -1)


class EGNNDenoiser(nn.Module):
    """Predicts the noise in a noisy chain, equivariantly: messages see distances, the noise level and how far apart
    two atoms are along the chain; the output is a sum of difference vectors, so it turns as the chain turns."""

    def __init__(self, hidden=64, layers=4, n=CHAIN_N):
        super().__init__()
        self.idx = nn.Embedding(n, hidden)
        self.temb = nn.Linear(16, hidden)
        self.sep = nn.Embedding(n, 8)
        self.phi_e = nn.ModuleList([nn.Sequential(nn.Linear(2 * hidden + 1 + 8, hidden), nn.SiLU(),
                                                  nn.Linear(hidden, hidden), nn.SiLU()) for _ in range(layers)])
        self.phi_x = nn.ModuleList([nn.Sequential(nn.Linear(hidden, hidden), nn.SiLU(), nn.Linear(hidden, 1))
                                    for _ in range(layers)])
        self.phi_h = nn.ModuleList([nn.Sequential(nn.Linear(2 * hidden, hidden), nn.SiLU(), nn.Linear(hidden, hidden))
                                    for _ in range(layers)])
        ar = torch.arange(n)
        self.register_buffer("seps", (ar[None] - ar[:, None]).abs())

    def forward(self, x, t):
        B, n, _ = x.shape
        h = self.idx.weight[None].expand(B, n, -1) + self.temb(t_embed(t)).unsqueeze(1)
        se = self.sep(self.seps)[None].expand(B, n, n, -1)
        eye = torch.eye(n).unsqueeze(0).unsqueeze(-1)
        out = torch.zeros_like(x)
        for pe, px, ph in zip(self.phi_e, self.phi_x, self.phi_h):
            d = x[:, :, None] - x[:, None]
            d2 = (d ** 2).sum(-1, keepdim=True)
            m = pe(torch.cat([h[:, :, None].expand(B, n, n, -1), h[:, None].expand(B, n, n, -1), d2, se], -1))
            m = m * (1 - eye)
            out = out + (d / torch.sqrt(d2 + 1.0) * px(m)).sum(2) / (n - 1)
            h = h + ph(torch.cat([h, m.sum(2)], -1))
        return out


class MLPDenoiser(nn.Module):
    """All 24 coordinates and the noise level in, 24 numbers out; it learns rotations only from augmented data."""

    def __init__(self, hidden=512, n=CHAIN_N):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2 * n + 16, hidden), nn.SiLU(), nn.Linear(hidden, hidden), nn.SiLU(),
                                 nn.Linear(hidden, hidden), nn.SiLU(), nn.Linear(hidden, 2 * n))

    def forward(self, x, t):
        B = x.shape[0]
        return self.net(torch.cat([x.reshape(B, -1), t_embed(t)], -1)).reshape(B, -1, 2)


def rot2(gen, B):
    th = torch.rand(B, generator=gen) * 2 * math.pi
    c, s = torch.cos(th), torch.sin(th)
    return torch.stack([torch.stack([c, -s], -1), torch.stack([s, c], -1)], -2)


def train_diffusion(kind, data, seed, steps, batch=128, lr=1e-3, snaps=(), snap_fn=None):
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(4000 + seed)
    m = EGNNDenoiser() if kind == "egnn" else MLPDenoiser()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    ab, _ = schedule()
    X = torch.from_numpy(data)
    curve, frames = [], []
    t0 = time.time()
    run = 0.0
    for s in range(steps + 1):
        if s in snaps and snap_fn is not None:
            m.eval()
            frames.append(snap_fn(m))
            m.train()
        if s == steps:
            break
        j = torch.randint(0, len(X), (batch,), generator=gen)
        x0 = X[j]
        x0 = torch.einsum("bij,bnj->bni", rot2(gen, batch), x0)  # every model sees every orientation
        t = torch.randint(1, T_DIFF + 1, (batch,), generator=gen)
        eps = torch.randn(x0.shape, generator=gen)
        a = ab[t - 1].view(-1, 1, 1)
        xt = a.sqrt() * x0 + (1 - a).sqrt() * eps
        loss = F.mse_loss(m(xt, t), eps)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run = 0.98 * run + 0.02 * float(loss) if s else float(loss)
        if s % 200 == 0:
            curve.append((s, run))
    m.eval()
    return m, dict(curve=curve, frames=frames, secs=time.time() - t0, params=n_params(m))


def sample(m, count, seed, keep=()):
    """Ancestral DDPM sampling (Ho et al. 2020) from pure noise; ``keep``: the steps whose states are returned."""
    gen = torch.Generator().manual_seed(seed)
    ab, beta = schedule()
    x = torch.randn(count, CHAIN_N, 2, generator=gen)
    path = {}
    with torch.no_grad():
        for t in range(T_DIFF, 0, -1):
            if t in keep:
                path[t] = x.numpy().copy()
            tt = torch.full((count,), t)
            eps = m(x, tt)
            a, b = ab[t - 1], beta[t - 1]
            mean = (x - b / (1 - a).sqrt() * eps) / (1 - b).sqrt()
            if t > 1:
                var = b * (1 - ab[t - 2]) / (1 - a)
                x = mean + var.sqrt() * torch.randn(x.shape, generator=gen)
            else:
                x = mean
    if 0 in keep:
        path[0] = x.numpy().copy()
    return x.numpy(), path


def chain_stats(S):
    """Bond lengths' mean absolute deviation from 1, the share of chains with two atoms closer than 0.6, radii of
    gyration."""
    b = np.linalg.norm(S[:, 1:] - S[:, :-1], axis=-1)
    D = np.sqrt(((S[:, :, None] - S[:, None]) ** 2).sum(-1))
    i, j = np.triu_indices(S.shape[1], 2)
    clash = (D[:, i, j].min(1) < 0.6).mean()
    R = np.sqrt(((S - S.mean(1, keepdims=True)) ** 2).sum(-1).mean(1))
    return dict(bond_mad=float(np.abs(b - 1).mean()), clash=float(clash), rg=R)
