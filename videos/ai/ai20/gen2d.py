"""The 2D experiments of Part 20: three toy densities in the plane, and every family of generative model trained on
them, small and on the CPU.

* the data: two moons, a ring of eight Gaussians, a checkerboard (``DATA``), each with its exact density
  (``density``), a fixed training set of 20,000 points and a test set of 5,000, seeded;
* the families, each a small multilayer perceptron (two hidden layers of 128 or 64 units):
  ``MDN2D`` (autoregressive: a mixture for x1, then a mixture for x2 given x1), ``VAE2D``, the GAN family
  (``train_gan``: the original minimax loss, the non-saturating loss, WGAN-GP), ``RealNVP2D`` (affine couplings),
  ``CNF2D`` (a neural ODE, with the exact trace or Hutchinson's estimate) and ``EBM2D`` (an energy, sampled by
  Langevin dynamics);
* the measurements that compare them (``modes``, ``prec_rec``, ``frechet``).

Every function takes its seed; nothing here reads the clock or the machine.
"""

from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

BOX = 3.0  # the plane shown: [-BOX, BOX]^2
GRID = 64  # density images: GRID x GRID cells
N_TRAIN, N_TEST = 20_000, 5_000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def tseed(seed: int) -> torch.Generator:
    torch.manual_seed(seed)
    return torch.Generator().manual_seed(seed)


# ---------------------------------------------------------------------------
# The data
# ---------------------------------------------------------------------------
RING_R, RING_S = 2.0, 0.1
RING_C = np.array([[RING_R * math.cos(2 * math.pi * k / 8), RING_R * math.sin(2 * math.pi * k / 8)] for k in range(8)])
MOON_NOISE, MOON_SCALE, MOON_SHIFT = 0.12, 1.8, np.array([0.5, 0.25])


def ring(n, g):
    k = g.integers(0, 8, n)
    return RING_C[k] + RING_S * g.normal(size=(n, 2))


def _moon(t, w):
    a = np.c_[np.cos(t), np.sin(t)]
    b = np.c_[1 - np.cos(t), 0.5 - np.sin(t)]
    return (np.where(np.asarray(w)[:, None] == 0, a, b) - MOON_SHIFT) * MOON_SCALE


def moons(n, g):
    return _moon(g.uniform(0, math.pi, n), g.integers(0, 2, n)) + MOON_NOISE * g.normal(size=(n, 2))


CHECK = [(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == 0]  # filled unit squares of [-2, 2]^2


def checker(n, g):
    k = g.integers(0, len(CHECK), n)
    ij = np.array(CHECK)[k]
    return -2.0 + ij + g.uniform(size=(n, 2))


DATA = {"moons": moons, "ring": ring, "checker": checker}
NAMES = list(DATA)


def density(name: str, X) -> np.ndarray:
    """The exact density of each toy at the points X (n, 2)."""
    X = np.asarray(X, float)
    if name == "ring":
        d2 = ((X[:, None, :] - RING_C[None]) ** 2).sum(-1)
        return np.exp(-d2 / (2 * RING_S ** 2)).mean(1) / (2 * math.pi * RING_S ** 2)
    if name == "checker":
        inside = np.all((X > -2) & (X < 2), 1)
        i, j = np.floor(X[:, 0] + 2), np.floor(X[:, 1] + 2)
        return np.where(inside & ((i + j) % 2 == 0), 1.0 / len(CHECK), 0.0)
    # two moons: the noise blurs each arc; average the Gaussian over the arc
    ts = np.linspace(0, math.pi, 721)
    out = np.zeros(len(X))
    for w in (0, 1):
        C = _moon(ts, np.full(len(ts), w))
        for a in range(0, len(X), 2048):
            d2 = ((X[a:a + 2048, None, :] - C[None]) ** 2).sum(-1)
            out[a:a + 2048] += 0.5 * np.exp(-d2 / (2 * MOON_NOISE ** 2)).mean(1) / (2 * math.pi * MOON_NOISE ** 2)
    return out


def grid_points(n=GRID, box=BOX):
    xs = np.linspace(-box, box, n)
    X, Y = np.meshgrid(xs, xs)  # row i is y = xs[i]
    return xs, np.c_[X.ravel(), Y.ravel()]


def dataset(name: str, seed: int = 0):
    g = rng(1000 + NAMES.index(name) * 7 + seed)
    return DATA[name](N_TRAIN, g).astype(np.float32), DATA[name](N_TEST, g).astype(np.float32)


def entropy(name: str) -> float:
    """The data's own differential entropy, -E log p, in nats: the best NLL any model can reach."""
    X = DATA[name](200_000, rng(77))
    p = density(name, X)
    return float(-np.log(np.maximum(p, 1e-300)).mean())


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------
def mlp(i, o, h=128, depth=2, act=nn.SiLU) -> nn.Sequential:
    layers, d = [], i
    for _ in range(depth):
        layers += [nn.Linear(d, h), act()]
        d = h
    layers.append(nn.Linear(d, o))
    return nn.Sequential(*layers)


def n_params(m: nn.Module) -> int:
    return int(sum(p.numel() for p in m.parameters()))


LOG2PI = math.log(2 * math.pi)


def normal_lp(x, mu, log_s):
    return -0.5 * ((x - mu) / log_s.exp()) ** 2 - log_s - 0.5 * LOG2PI


def mix_lp(params, x):
    """log density of a 1D mixture of Gaussians; params (..., 3K) = logits, means, log-scales."""
    lg, mu, ls = params.chunk(3, -1)
    ls = ls.clamp(-6, 2)
    return torch.logsumexp(F.log_softmax(lg, -1) + normal_lp(x[..., None], mu, ls), -1)


def mix_sample(params, gen):
    lg, mu, ls = params.chunk(3, -1)
    k = torch.multinomial(F.softmax(lg, -1), 1, generator=gen).squeeze(-1)
    m, s = mu.gather(-1, k[:, None])[:, 0], ls.clamp(-6, 2).exp().gather(-1, k[:, None])[:, 0]
    return m + s * torch.randn(m.shape, generator=gen)


def batches(X: np.ndarray, bs: int, g: np.random.Generator):
    T = torch.from_numpy(X)
    while True:
        idx = torch.from_numpy(g.permutation(len(X)))
        for a in range(0, len(X) - bs + 1, bs):
            yield T[idx[a:a + bs]]


def checkpoints(steps: int, n: int = 12) -> list[int]:
    return sorted(set([0] + [int(round(v)) for v in np.geomspace(10, steps, n - 1)]))


# ---------------------------------------------------------------------------
# Autoregressive: p(x1) p(x2 | x1), each a mixture of Gaussians
# ---------------------------------------------------------------------------
class MDN2D(nn.Module):
    def __init__(self, K=10, h=128):
        super().__init__()
        self.K = K
        self.p1 = nn.Parameter(torch.cat([torch.zeros(K), torch.linspace(-2.5, 2.5, K), torch.full((K,), -0.7)]))
        self.c = mlp(1, 3 * K, h)

    def log_prob(self, X):
        lp1 = mix_lp(self.p1.expand(len(X), -1), X[:, 0])
        lp2 = mix_lp(self.c(X[:, :1]), X[:, 1])
        return lp1 + lp2

    @torch.no_grad()
    def sample(self, n, gen):
        x1 = mix_sample(self.p1.expand(n, -1), gen)
        x2 = mix_sample(self.c(x1[:, None]), gen)
        return torch.stack([x1, x2], 1)

    @torch.no_grad()
    def marginal1(self, xs):
        t = torch.as_tensor(xs, dtype=torch.float32)
        return mix_lp(self.p1.expand(len(t), -1), t).exp().numpy()

    @torch.no_grad()
    def conditional(self, x1, xs):
        t = torch.as_tensor(xs, dtype=torch.float32)
        par = self.c(torch.full((len(t), 1), float(x1)))
        return mix_lp(par, t).exp().numpy()


def train_ar(name, seed, steps=3000, bs=512, lr=2e-3, snaps=True):
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    m = MDN2D()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    it = batches(Xtr, bs, rng(seed))
    te = torch.from_numpy(Xte)
    curve, frames = [], []
    xs, P = grid_points()
    marks = checkpoints(steps, 10)
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                curve.append((s, float(-m.log_prob(te).mean())))
            if snaps:
                frames.append(dict(step=s, nll=curve[-1][1], dens=density_of(m.log_prob, P)))
        if s == steps:
            break
        x = next(it)
        loss = -m.log_prob(x).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return m, dict(curve=curve, frames=frames, params=n_params(m), gen=gen)


@torch.no_grad()
def density_of(logp_fn, P) -> np.ndarray:
    lp = logp_fn(torch.as_tensor(P, dtype=torch.float32))
    return lp.exp().numpy().reshape(GRID, GRID).astype(np.float32)


# ---------------------------------------------------------------------------
# The VAE in the plane: a 2D latent, Gaussian encoder and decoder
# ---------------------------------------------------------------------------
class VAE2D(nn.Module):
    def __init__(self, h=128, zd=2):
        super().__init__()
        self.zd = zd
        self.enc, self.dec = mlp(2, 2 * zd, h), mlp(zd, 4, h)

    def decode(self, z):
        mu, ls = self.dec(z).chunk(2, -1)
        return mu, ls.clamp(math.log(0.02), 1.0)

    def elbo(self, X, gen=None):
        mu, lv = self.enc(X).chunk(2, -1)
        z = mu + (0.5 * lv).exp() * torch.randn(mu.shape, generator=gen)
        dm, dl = self.decode(z)
        rec = normal_lp(X, dm, dl).sum(-1)
        kl = 0.5 * (mu ** 2 + lv.exp() - lv - 1).sum(-1)
        return rec - kl, rec, kl

    def log_prob(self, X, K=64, gen=None):
        """Importance-weighted estimate of log p(x) (IWAE bound with K samples)."""
        mu, lv = self.enc(X).chunk(2, -1)
        out = []
        for _ in range(K):
            eps = torch.randn(mu.shape, generator=gen)
            z = mu + (0.5 * lv).exp() * eps
            dm, dl = self.decode(z)
            lw = normal_lp(X, dm, dl).sum(-1) + normal_lp(z, torch.zeros_like(z), torch.zeros_like(z)).sum(-1) \
                - normal_lp(z, mu, 0.5 * lv).sum(-1)
            out.append(lw)
        return torch.logsumexp(torch.stack(out), 0) - math.log(K)

    @torch.no_grad()
    def sample(self, n, gen):
        z = torch.randn(n, self.zd, generator=gen)
        dm, dl = self.decode(z)
        return dm + dl.exp() * torch.randn(dm.shape, generator=gen)


def train_vae(name, seed, steps=3000, bs=512, lr=2e-3, snaps=True):
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    m = VAE2D()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    it = batches(Xtr, bs, rng(seed))
    te = torch.from_numpy(Xte[:2000])
    curve, frames = [], []
    xs, P = grid_points()
    marks = checkpoints(steps, 10)
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                e, r, k = m.elbo(te, gen)
                curve.append((s, float(-e.mean()), float(-r.mean()), float(k.mean())))
            if snaps:
                with torch.no_grad():
                    frames.append(dict(step=s, nll=curve[-1][1],
                                       dens=density_of(lambda t: m.log_prob(t, 32, gen), P)))
        if s == steps:
            break
        e, _, _ = m.elbo(next(it), gen)
        loss = -e.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return m, dict(curve=curve, frames=frames, params=n_params(m), gen=gen)


# ---------------------------------------------------------------------------
# Posterior collapse in the plane: the same VAE with a decoder that can model x by itself
# ---------------------------------------------------------------------------
class CollapseVAE(nn.Module):
    """A 2D latent; the decoder gives a mixture for x1 and one for x2, either both from z alone (factorized), or
    x2's from z and x1 (autoregressive, so it can model the data without z)."""

    def __init__(self, ar: bool, K=10, h=128):
        super().__init__()
        self.ar = ar
        self.enc = mlp(2, 4, h)
        self.d1 = mlp(2, 3 * K, h)
        self.d2 = mlp(3 if ar else 2, 3 * K, h)

    def elbo(self, X, gen=None):
        mu, lv = self.enc(X).chunk(2, -1)
        z = mu + (0.5 * lv).exp() * torch.randn(mu.shape, generator=gen)
        lp1 = mix_lp(self.d1(z), X[:, 0])
        lp2 = mix_lp(self.d2(torch.cat([z, X[:, :1]], 1) if self.ar else z), X[:, 1])
        kl = 0.5 * (mu ** 2 + lv.exp() - lv - 1).sum(-1)
        return lp1 + lp2 - kl, lp1 + lp2, kl, mu


def train_collapse(ar: bool, seed: int, name="moons", steps=4000, bs=512, lr=2e-3):
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    m = CollapseVAE(ar)
    opt = torch.optim.Adam(m.parameters(), lr)
    it = batches(Xtr, bs, rng(seed))
    te = torch.from_numpy(Xte[:2000])
    marks = sorted(set(np.linspace(0, steps, 41).astype(int)))
    curve = []
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                e, r, k, _ = m.elbo(te, gen)
            curve.append((s, float(-e.mean()), float(-r.mean()), float(k.mean())))
        if s == steps:
            break
        e, _, _, _ = m.elbo(next(it), gen)
        opt.zero_grad()
        (-e.mean()).backward()
        opt.step()
    with torch.no_grad():
        _, _, _, mu = m.elbo(te[:600], gen)
    return dict(curve=curve, codes=mu.numpy(), points=Xte[:600], params=n_params(m))


# ---------------------------------------------------------------------------
# GANs: the original minimax loss, the non-saturating loss, and WGAN-GP
# ---------------------------------------------------------------------------
ZD = 8


def gan_nets(h=128):
    G = mlp(ZD, 2, h, act=nn.ReLU)
    D = mlp(2, 1, h, act=lambda: nn.LeakyReLU(0.2))
    return G, D


def grad_penalty(D, real, fake, gen):
    a = torch.rand(len(real), 1, generator=gen)
    xh = (a * real + (1 - a) * fake).requires_grad_(True)
    g, = torch.autograd.grad(D(xh).sum(), xh, create_graph=True)
    return ((g.norm(dim=1) - 1) ** 2).mean()


def modes(S, centers=RING_C, sigma=RING_S, min_frac=0.01):
    """How many of the ring's eight modes get at least 1% of the samples (within three standard deviations), and the
    share of samples that are that close to some mode."""
    S = np.asarray(S)
    d = np.sqrt(((S[:, None, :] - centers[None]) ** 2).sum(-1))
    k, dm = d.argmin(1), d.min(1)
    good = dm < 3 * sigma
    counts = np.bincount(k[good], minlength=len(centers))
    return int((counts >= min_frac * len(S)).sum()), float(good.mean()), counts.tolist()


def train_gan(loss: str, name: str, seed: int, steps=6000, bs=256, replay=False, n_frames=48):
    """loss: 'mm' (minimax, saturating), 'ns' (non-saturating), 'wgan' (WGAN-GP, five critic steps per generator
    step).  Every variant: the same two networks, the same number of generator steps."""
    gen = tseed(seed)
    Xtr, _ = dataset(name)
    G, D = gan_nets()
    if loss == "wgan":
        oG = torch.optim.Adam(G.parameters(), 1e-4, betas=(0.5, 0.9))
        oD = torch.optim.Adam(D.parameters(), 1e-4, betas=(0.5, 0.9))
        n_critic, lam = 5, 0.1
    else:
        oG = torch.optim.Adam(G.parameters(), 2e-4, betas=(0.5, 0.999))
        oD = torch.optim.Adam(D.parameters(), 2e-4, betas=(0.5, 0.999))
        n_critic, lam = 1, 0.0
    it = batches(Xtr, bs, rng(seed))
    z_fix = torch.randn(1000, ZD, generator=torch.Generator().manual_seed(4242))
    xs, P = grid_points(40)
    Pt = torch.as_tensor(P, dtype=torch.float32)
    marks = sorted(set(np.linspace(0, steps, n_frames).astype(int)))
    curve, frames, gnorm = [], [], []
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                S = G(z_fix).numpy()
                nm, q, counts = modes(S)
                curve.append((s, nm, q))
                if replay:
                    dv = D(Pt)[:, 0]
                    dv = torch.sigmoid(dv) if loss != "wgan" else dv
                    frames.append(dict(step=s, samples=S[:500].astype(np.float32),
                                       d=dv.numpy().reshape(40, 40).astype(np.float32), modes=nm, counts=counts))
        if s == steps:
            break
        for _ in range(n_critic):
            real = next(it)
            fake = G(torch.randn(bs, ZD, generator=gen)).detach()
            if loss == "wgan":
                lD = D(fake).mean() - D(real).mean() + lam * grad_penalty(D, real, fake, gen)
            else:
                lD = F.softplus(-D(real)).mean() + F.softplus(D(fake)).mean()
            oD.zero_grad()
            lD.backward()
            oD.step()
        out = D(G(torch.randn(bs, ZD, generator=gen)))
        if loss == "wgan":
            lG = -out.mean()
        elif loss == "ns":
            lG = F.softplus(-out).mean()  # -log D(G(z))
        else:
            lG = -F.softplus(out).mean()  # log(1 - D(G(z)))
        oG.zero_grad()
        lG.backward()
        if s < 400 and s % 20 == 0:  # how hard the generator is pushed early on
            gnorm.append((s, float(torch.sqrt(sum((p.grad ** 2).sum() for p in G.parameters())))))
        oG.step()
    with torch.no_grad():
        S = G(torch.randn(2000, ZD, generator=torch.Generator().manual_seed(99))).numpy()
    return G, dict(curve=curve, frames=frames, final=S.astype(np.float32), gnorm=gnorm,
                   params=n_params(G) + n_params(D))


# ---------------------------------------------------------------------------
# RealNVP in the plane: affine coupling layers
# ---------------------------------------------------------------------------
class Coupling2D(nn.Module):
    """Moves coordinate j by an affine map whose scale and shift depend on the other coordinate."""

    def __init__(self, j, h=64):
        super().__init__()
        self.j = j
        self.net = mlp(1, 2, h, act=nn.Tanh)
        self.scale = nn.Parameter(torch.zeros(1))
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)

    def st(self, other):
        s, t = self.net(other).chunk(2, -1)
        return self.scale.exp() * torch.tanh(s), t

    def forward(self, x):  # data -> base
        o, k = x[:, 1 - self.j:2 - self.j], x[:, self.j:self.j + 1]
        s, t = self.st(o)
        y = k * s.exp() + t
        out = torch.cat([y, o], 1) if self.j == 0 else torch.cat([o, y], 1)
        return out, s[:, 0]

    def inverse(self, y):  # base -> data
        o, k = y[:, 1 - self.j:2 - self.j], y[:, self.j:self.j + 1]
        s, t = self.st(o)
        x = (k - t) * (-s).exp()
        return torch.cat([x, o], 1) if self.j == 0 else torch.cat([o, x], 1)


class RealNVP2D(nn.Module):
    def __init__(self, L=8, h=64):
        super().__init__()
        self.layers = nn.ModuleList([Coupling2D(k % 2, h) for k in range(L)])

    def forward(self, x):
        ld = torch.zeros(len(x))
        for l in self.layers:
            x, s = l(x)
            ld = ld + s
        return x, ld

    def log_prob(self, x):
        z, ld = self(x)
        return normal_lp(z, torch.zeros_like(z), torch.zeros_like(z)).sum(-1) + ld

    @torch.no_grad()
    def generate_layers(self, z):
        """The base points z pushed through the inverse layers one at a time: [z, after layer 1, ..., x]."""
        out = [z.numpy().copy()]
        for l in reversed(self.layers):
            z = l.inverse(z)
            out.append(z.numpy().copy())
        return out

    @torch.no_grad()
    def sample(self, n, gen):
        return torch.from_numpy(self.generate_layers(torch.randn(n, 2, generator=gen))[-1])


def train_flow(name, seed, steps=4000, bs=512, lr=2e-3, snaps=True):
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    m = RealNVP2D()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    it = batches(Xtr, bs, rng(seed))
    te = torch.from_numpy(Xte)
    curve, frames = [], []
    xs, P = grid_points()
    marks = checkpoints(steps, 10)
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                curve.append((s, float(-m.log_prob(te).mean())))
            if snaps:
                frames.append(dict(step=s, nll=curve[-1][1], dens=density_of(m.log_prob, P)))
        if s == steps:
            break
        loss = -m.log_prob(next(it)).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return m, dict(curve=curve, frames=frames, params=n_params(m), gen=gen)


def logdet_check(m: RealNVP2D, X) -> float:
    """The largest gap between the coupling stack's log-determinant (the sum of its scales) and autograd's."""
    X = torch.as_tensor(X, dtype=torch.float32)
    worst = 0.0
    for x in X:
        J = torch.autograd.functional.jacobian(lambda v: m(v[None])[0][0], x)
        worst = max(worst, abs(float(torch.slogdet(J)[1]) - float(m(x[None])[1][0])))
    return worst


# ---------------------------------------------------------------------------
# A continuous normalizing flow: a neural ODE, its divergence exact or by Hutchinson's estimator
# ---------------------------------------------------------------------------
class ODEFunc(nn.Module):
    def __init__(self, h=64):
        super().__init__()
        self.net = mlp(3, 2, h, act=nn.Tanh)

    def forward(self, z, t):
        return self.net(torch.cat([z, torch.full((len(z), 1), float(t))], 1))


def divergence(f, z, t, eps=None, create_graph=True):
    """f(z, t) and its divergence tr(df/dz): exact (one backward pass per dimension) or, given eps, Hutchinson's
    eps^T (df/dz) eps (one backward pass)."""
    with torch.enable_grad():
        z = z if z.requires_grad else z.requires_grad_(True)
        out = f(z, t)
        if eps is None:
            tr = 0.0
            for i in range(z.shape[1]):
                g, = torch.autograd.grad(out[:, i].sum(), z, create_graph=create_graph)
                tr = tr + g[:, i]
        else:
            g, = torch.autograd.grad((out * eps).sum(), z, create_graph=create_graph)
            tr = (g * eps).sum(1)
    return out, tr


def cnf_logp(f, x, n_steps=10, hutch=False, gen=None, t0=1.0, create_graph=True):
    """log p(x) for the flow dz/dt = f(z, t) from z(0) ~ N(0, I) to x = z(t0): integrate back to t = 0 with RK4,
    adding up the divergence.  Hutchinson's probe (Rademacher) is drawn once per solve, as in FFJORD."""
    z, I = x, torch.zeros(len(x))
    eps = (torch.randint(0, 2, x.shape, generator=gen).float() * 2 - 1) if hutch else None
    h = t0 / n_steps
    for k in range(n_steps):
        t = t0 - k * h

        def rhs(zz, tt):
            v, tr = divergence(f, zz, tt, eps, create_graph)
            return -v, tr

        k1, d1 = rhs(z, t)
        k2, d2 = rhs(z + 0.5 * h * k1, t - 0.5 * h)
        k3, d3 = rhs(z + 0.5 * h * k2, t - 0.5 * h)
        k4, d4 = rhs(z + h * k3, t - h)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        I = I + h / 6 * (d1 + 2 * d2 + 2 * d3 + d4)
        if not create_graph:
            z, I = z.detach(), I.detach()
    return normal_lp(z, torch.zeros_like(z), torch.zeros_like(z)).sum(-1) - I


@torch.no_grad()
def cnf_paths(f, z, n_steps=40):
    """Points z(0) carried forward to t = 1: every intermediate position."""
    out = [z.numpy().copy()]
    h = 1.0 / n_steps
    for k in range(n_steps):
        t = k * h
        k1 = f(z, t)
        k2 = f(z + 0.5 * h * k1, t + 0.5 * h)
        k3 = f(z + 0.5 * h * k2, t + 0.5 * h)
        k4 = f(z + h * k3, t + h)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(z.numpy().copy())
    return np.array(out, np.float32)


def train_cnf(seed, hutch: bool, name="moons", steps=1500, bs=256, lr=3e-3, n_steps=8, evals=12):
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    f = ODEFunc()
    opt = torch.optim.Adam(f.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    it = batches(Xtr, bs, rng(seed))
    te = torch.from_numpy(Xte[:1000])
    marks = sorted(set(np.linspace(0, steps, evals).astype(int)))
    curve, train = [], []
    for s in range(steps + 1):
        if s in marks:  # judged the same way for both: the exact divergence, on held-out points
            lp = cnf_logp(f, te.clone(), n_steps, False, gen, create_graph=False)
            curve.append((s, float(-lp.mean())))
        if s == steps:
            break
        lp = cnf_logp(f, next(it).clone(), n_steps, hutch, gen)
        loss = -lp.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if s % 25 == 0:
            train.append((s, float(loss)))
    return f, dict(curve=curve, train=train, params=n_params(f))


# ---------------------------------------------------------------------------
# An energy-based model, sampled by Langevin dynamics
# ---------------------------------------------------------------------------
class EBM2D(nn.Module):
    def __init__(self, h=128):
        super().__init__()
        self.net = mlp(2, 1, h)

    def forward(self, x):
        return self.net(x)[:, 0]


def langevin(E, x, n, eta, gen, keep_every=0, clip=BOX + 0.5):
    """x <- x - (eta / 2) grad E(x) + sqrt(eta) noise, n times.  Returns the end points (and the path if asked)."""
    path = []
    for k in range(n):
        x = x.detach().requires_grad_(True)
        g, = torch.autograd.grad(E(x).sum(), x)
        x = (x - 0.5 * eta * g + math.sqrt(eta) * torch.randn(x.shape, generator=gen)).clamp(-clip, clip)
        if keep_every and k % keep_every == 0:
            path.append(x.detach().numpy().copy())
    return x.detach(), path


@torch.no_grad()
def grid_logz(E, n=160, box=BOX + 0.5):
    """In two dimensions the normalizer Z can be summed on a grid: log Z."""
    xs = np.linspace(-box, box, n)
    X, Y = np.meshgrid(xs, xs)
    e = E(torch.as_tensor(np.c_[X.ravel(), Y.ravel()], dtype=torch.float32))
    return float(torch.logsumexp(-e, 0) + 2 * math.log(xs[1] - xs[0]))


def train_ebm(name, seed, steps=2500, bs=256, lr=1e-3, k_steps=40, eta=0.005, alpha=0.1, snaps=True):
    """Persistent contrastive training (a replay buffer of Langevin chains, 5% restarted from uniform noise): lower
    the energy of data, raise it where the chains are."""
    gen = tseed(seed)
    Xtr, Xte = dataset(name)
    E = EBM2D()
    opt = torch.optim.Adam(E.parameters(), lr, betas=(0.0, 0.999))
    it = batches(Xtr, bs, rng(seed))
    buf = (torch.rand(10_000, 2, generator=gen) * 2 - 1) * BOX
    te = torch.from_numpy(Xte[:2000])
    xs, P = grid_points()
    Pt = torch.as_tensor(P, dtype=torch.float32)
    marks = checkpoints(steps, 10)
    curve, frames = [], []
    for s in range(steps + 1):
        if s in marks:
            lz = grid_logz(E)
            with torch.no_grad():
                nll = float(E(te).mean() + lz)
                curve.append((s, nll))
                if snaps:
                    d = torch.exp(-E(Pt) - lz).numpy().reshape(GRID, GRID).astype(np.float32)
                    frames.append(dict(step=s, nll=nll, dens=d, chains=buf[:400].numpy().copy()))
        if s == steps:
            break
        idx = torch.randint(0, len(buf), (bs,), generator=gen)
        x0 = buf[idx]
        fresh = torch.rand(bs, generator=gen) < 0.05
        x0[fresh] = (torch.rand(int(fresh.sum()), 2, generator=gen) * 2 - 1) * BOX
        xn, _ = langevin(E, x0, k_steps, eta, gen)
        buf[idx] = xn
        real = next(it)
        er, ef = E(real), E(xn)
        loss = er.mean() - ef.mean() + alpha * (er ** 2 + ef ** 2).mean()
        opt.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(E.parameters(), 1.0)
        opt.step()
    return E, dict(curve=curve, frames=frames, params=n_params(E), gen=gen)


# ---------------------------------------------------------------------------
# Measuring samples: precision and recall (k nearest neighbours), the Frechet distance of Gaussian fits
# ---------------------------------------------------------------------------
def _sqd(A, B):
    return np.maximum((A * A).sum(1)[:, None] + (B * B).sum(1)[None] - 2 * A @ B.T, 0.0)


def prec_rec(real, fake, k=3):
    """Kynkaanniemi et al. (2019): each sample's neighbourhood is a ball out to its k-th nearest neighbour in its own
    set.  Precision: the share of generated samples inside some real ball; recall: real samples inside some
    generated ball."""
    real, fake = np.asarray(real, np.float64), np.asarray(fake, np.float64)
    rr, ff, rf = _sqd(real, real), _sqd(fake, fake), _sqd(real, fake)
    r_rad = np.sort(rr, 1)[:, k]  # column 0 is the point itself
    f_rad = np.sort(ff, 1)[:, k]
    precision = float((rf <= r_rad[:, None]).any(0).mean())
    recall = float((rf <= f_rad[None, :]).any(1).mean())
    return precision, recall


def frechet(A, B) -> float:
    """The Frechet (2-Wasserstein) distance between the Gaussians fitted to two sample sets, squared: FID's formula."""
    from scipy.linalg import sqrtm

    A, B = np.asarray(A, np.float64), np.asarray(B, np.float64)
    m1, m2 = A.mean(0), B.mean(0)
    S1, S2 = np.cov(A, rowvar=False), np.cov(B, rowvar=False)
    cs = sqrtm(S1 @ S2)
    cs = cs.real if np.iscomplexobj(cs) else cs
    return float(((m1 - m2) ** 2).sum() + np.trace(S1 + S2 - 2 * cs))
