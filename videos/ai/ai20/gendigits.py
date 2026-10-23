"""The image experiments of Part 20: MNIST digits at 14 x 14 with 16 grey levels, and one model of each family
trained on them, on the CPU, on equal arithmetic.

* the data (``digits``): MNIST (LeCun, Cortes & Burges 1998), through Part 10's checked download, averaged 2 x 2 to
  14 x 14 and cut to 16 grey levels (4 bits a pixel); binarized at level 8 for the Boltzmann machines;
* the families: ``PixelCNN`` (autoregressive, the two-stack layout of Gated PixelCNN, without the gates), ``VAE``
  (a multilayer perceptron with a discretized-logistic decoder), the GAN and WGAN-GP (``gan_nets``), ``RealNVP``
  (affine couplings on the dequantized, logit-transformed pixels), the restricted Boltzmann machine (``RBM``), and
  a small VQ-VAE with an autoregressive prior over its codes;
* the judge: a small convolutional digit classifier (``Classifier``), whose 128-dimensional penultimate layer gives
  the features for the Frechet distance and for precision and recall, as an ImageNet classifier's (Inception's)
  do for photographs;
* the budget: every family gets the same arithmetic, ``BUDGET`` floating-point operations of training, counted by
  PyTorch's FLOP counter on one real step of each model (``step_flops``).
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from videos.ai.ai20.gen2d import SCALE, n_params, rng, scaled, tseed

Q = 16  # grey levels
S = 14  # side
D = S * S
BUDGET = 6e12 * SCALE  # training FLOPs per model


# ---------------------------------------------------------------------------
# The data
# ---------------------------------------------------------------------------
_digits: dict = {}


def digits() -> dict:
    """{'xtr', 'ytr', 'xte', 'yte'}: uint8 levels 0..15 of shape (n, 14, 14), and labels."""
    if not _digits:
        from videos.ai.ai10.data import mnist  # Part 10's download, checked against its SHA-256

        m = mnist()

        def prep(x):
            x = x.reshape(-1, S, 2, S, 2).astype(np.float32).mean((2, 4))
            return np.clip(np.floor(x / 256 * Q), 0, Q - 1).astype(np.uint8)

        _digits.update(xtr=prep(m["xtr"]), ytr=m["ytr"].astype(np.int64), xte=prep(m["xte"]),
                       yte=m["yte"].astype(np.int64))
    return _digits


def as_float(q) -> torch.Tensor:
    """Levels 0..15 as pixel values in [0, 1], shape (n, 1, 14, 14)."""
    return torch.as_tensor(np.asarray(q), dtype=torch.float32).reshape(-1, 1, S, S) / (Q - 1)


def to_levels(x) -> np.ndarray:
    """Continuous pixels in [0, 1] to the 16 levels (what every model's samples are judged as)."""
    x = np.asarray(x, np.float32).reshape(-1, S, S)
    return np.clip(np.round(x * (Q - 1)), 0, Q - 1).astype(np.uint8)


def binarize(q) -> np.ndarray:
    return (np.asarray(q) >= Q // 2).astype(np.float32).reshape(len(q), -1)


def batches(X: np.ndarray, bs: int, g: np.random.Generator, Y=None):
    while True:
        idx = g.permutation(len(X))
        for a in range(0, len(X) - bs + 1, bs):
            j = idx[a:a + bs]
            yield (X[j], Y[j]) if Y is not None else X[j]


def checkpoints(steps: int, n: int = 12) -> list[int]:
    return sorted(set([0] + [int(round(v)) for v in np.geomspace(max(10, steps / 300), steps, n - 1)]))


def step_flops(fn) -> float:
    """Floating-point operations of one call of ``fn`` (a whole training step), counted by PyTorch."""
    from torch.utils.flop_counter import FlopCounterMode

    with FlopCounterMode(display=False) as fc:
        fn()
    return float(fc.get_total_flops())


# ---------------------------------------------------------------------------
# PixelCNN: masked convolutions; the plain stack and the two-stack (vertical + horizontal) layout
# ---------------------------------------------------------------------------
class MaskedConv(nn.Conv2d):
    def __init__(self, cin, cout, k, kind):
        super().__init__(cin, cout, k, padding=k // 2)
        m = torch.ones_like(self.weight)
        c = k // 2
        m[:, :, c, c + (kind == "B"):] = 0
        m[:, :, c + 1:] = 0
        self.register_buffer("mask", m)

    def forward(self, x):
        return F.conv2d(x, self.weight * self.mask, self.bias, padding=self.padding)


class PlainPixelCNN(nn.Module):
    """van den Oord et al. (2016a): a 7 x 7 mask-A convolution, then 3 x 3 mask-B ones.  It has a blind spot."""

    def __init__(self, ch=32, layers=5):
        super().__init__()
        mods = [MaskedConv(1, ch, 7, "A"), nn.ReLU()]
        for _ in range(layers):
            mods += [MaskedConv(ch, ch, 3, "B"), nn.ReLU()]
        mods += [nn.Conv2d(ch, Q, 1)]
        self.net = nn.Sequential(*mods)

    def forward(self, x, z=None):
        return self.net(x * 2 - 1)


def down(v):  # shift a feature map down one row: row i then holds what row i - 1 saw
    return F.pad(v, (0, 0, 1, 0))[:, :, :-1, :]


def right(x):  # shift right one column
    return F.pad(x, (1, 0, 0, 0))[:, :, :, :-1]


class PixelCNN(nn.Module):
    """van den Oord et al. (2016b): a vertical stack that sees every row above, a horizontal stack that sees the
    pixels to the left, the vertical one feeding the horizontal one, so no pixel above is missed.  Residual
    connections in the horizontal stack; ReLUs instead of the paper's gates.  Optionally conditioned on a code z
    (a learned bias per channel and layer), which makes it the decoder of a VAE."""

    def __init__(self, ch=32, layers=5, k=3, zdim=0):
        super().__init__()
        self.k, self.layers, self.ch = k, layers, ch
        self.v0 = nn.Conv2d(1, ch, (k // 2 + 1, k))
        self.h0 = nn.Conv2d(1, ch, (1, k // 2 + 1))
        self.v2h0 = nn.Conv2d(ch, ch, 1)
        self.vs = nn.ModuleList([nn.Conv2d(ch, ch, (k // 2 + 1, k)) for _ in range(layers)])
        self.hs = nn.ModuleList([nn.Conv2d(ch, ch, (1, k // 2 + 1)) for _ in range(layers)])
        self.v2h = nn.ModuleList([nn.Conv2d(ch, ch, 1) for _ in range(layers)])
        self.hout = nn.ModuleList([nn.Conv2d(ch, ch, 1) for _ in range(layers)])
        self.out = nn.Sequential(nn.ReLU(), nn.Conv2d(ch, 2 * ch, 1), nn.ReLU(), nn.Conv2d(2 * ch, Q, 1))
        self.zdim = zdim
        if zdim:
            self.zb = nn.Linear(zdim, 2 * ch * (layers + 1))

    def _vpad(self, v):
        k = self.k
        return F.pad(v, (k // 2, k // 2, k // 2, 0))

    def _hpad(self, h):
        return F.pad(h, (self.k // 2, 0, 0, 0))

    def forward(self, x, z=None):
        x = x * 2 - 1
        bias = self.zb(z).view(len(z), self.layers + 1, 2, self.ch, 1, 1) if self.zdim else None
        v = self.v0(self._vpad(x))
        h = self.h0(self._hpad(right(x))) + self.v2h0(down(v))
        if bias is not None:
            v, h = v + bias[:, 0, 0], h + bias[:, 0, 1]
        v, h = F.relu(v), F.relu(h)
        for i in range(self.layers):
            vn = self.vs[i](self._vpad(v))
            hn = self.hs[i](self._hpad(h)) + self.v2h[i](down(v))
            if bias is not None:
                vn, hn = vn + bias[:, i + 1, 0], hn + bias[:, i + 1, 1]
            h = h + self.hout[i](F.relu(hn))
            v = F.relu(vn)
        return self.out(h)  # (n, 16, 14, 14) logits


def ar_nll(net, q, z=None) -> torch.Tensor:
    """-log p(x) in nats per image, exactly: the sum over pixels of each one's cross-entropy."""
    q = torch.as_tensor(np.asarray(q), dtype=torch.long).reshape(-1, S, S)
    logits = net(q[:, None].float() / (Q - 1), z)
    return F.cross_entropy(logits, q, reduction="none").sum((1, 2))


@torch.no_grad()
def ar_sample(net, n, gen, z=None, trace=False):
    """Pixel by pixel in raster order: 196 passes through the network.  With ``trace``, each pixel's predicted
    distribution for the first image."""
    x = torch.zeros(n, 1, S, S)
    probs = []
    for i in range(S):
        for j in range(S):
            p = F.softmax(net(x, z)[:, :, i, j], -1)
            v = torch.multinomial(p, 1, generator=gen)[:, 0]
            x[:, 0, i, j] = v.float() / (Q - 1)
            if trace:
                probs.append(p[0].numpy().copy())
    q = np.round(x[:, 0].numpy() * (Q - 1)).astype(np.uint8)
    return (q, np.array(probs, np.float32)) if trace else q


def receptive_field(net, i=7, j=7, trials=8) -> np.ndarray:
    """Which input pixels the prediction at (i, j) depends on: |d logits(i, j) / d x| summed over random inputs."""
    tot = torch.zeros(S, S)
    for t in range(trials):
        x = torch.rand(1, 1, S, S, generator=torch.Generator().manual_seed(t), requires_grad=True)
        out = net(x)[0, :, i, j].abs().sum()
        g, = torch.autograd.grad(out, x)
        tot += g[0, 0].abs()
    return (tot > 1e-9 * tot.max()).numpy().astype(np.uint8)


# ---------------------------------------------------------------------------
# The VAE: a multilayer perceptron, a Gaussian code, a discretized-logistic decoder over the 16 levels
# ---------------------------------------------------------------------------
def dlogistic_lp(q, mu, log_s):
    """log P(level q) when the pixel is logistic(mu, s) cut into 16 bins of width 1/15 on [0, 1] (the two end bins
    take the tails): PixelCNN++'s likelihood, for 16 levels.  q: long (n, 196); mu, log_s: (n, 196)."""
    x = q.float() / (Q - 1)
    h = 0.5 / (Q - 1)
    inv = torch.exp(-log_s)
    plus, minus = inv * (x + h - mu), inv * (x - h - mu)
    cdf_plus, cdf_minus = torch.sigmoid(plus), torch.sigmoid(minus)
    log_cdf_plus = plus - F.softplus(plus)  # log sigmoid(plus), for the lowest bin
    log_one_minus = -F.softplus(minus)  # log (1 - sigmoid(minus)), for the highest bin
    mid = torch.log(torch.clamp(cdf_plus - cdf_minus, min=1e-12))
    return torch.where(q == 0, log_cdf_plus, torch.where(q == Q - 1, log_one_minus, mid))


class VAE(nn.Module):
    def __init__(self, zdim=16, h=512):
        super().__init__()
        self.zdim = zdim
        self.enc = nn.Sequential(nn.Linear(D, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(), nn.Linear(h, 2 * zdim))
        self.dec = nn.Sequential(nn.Linear(zdim, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(), nn.Linear(h, 2 * D))

    def encode(self, x):
        mu, lv = self.enc(x.reshape(len(x), -1)).chunk(2, -1)
        return mu, lv.clamp(-12, 6)

    def decode(self, z):
        m, ls = self.dec(z).chunk(2, -1)
        return torch.sigmoid(m), ls.clamp(-5, 1)

    def terms(self, q, gen, beta=1.0):
        """(-ELBO, reconstruction NLL, KL, per-dimension KL), each per image, in nats."""
        q = torch.as_tensor(np.asarray(q), dtype=torch.long).reshape(len(q), -1)
        mu, lv = self.encode(q.float() / (Q - 1))
        z = mu + (0.5 * lv).exp() * torch.randn(mu.shape, generator=gen)
        m, ls = self.decode(z)
        rec = -dlogistic_lp(q, m, ls).sum(1)
        kld = 0.5 * (mu ** 2 + lv.exp() - lv - 1)
        kl = kld.sum(1)
        return rec + beta * kl, rec, kl, kld

    @torch.no_grad()
    def iwae(self, q, gen, K=64):
        """log p(x) by importance sampling (Burda et al. 2015), K samples per image: a tighter bound."""
        q = torch.as_tensor(np.asarray(q), dtype=torch.long).reshape(len(q), -1)
        mu, lv = self.encode(q.float() / (Q - 1))
        lws = []
        for _ in range(K):
            z = mu + (0.5 * lv).exp() * torch.randn(mu.shape, generator=gen)
            m, ls = self.decode(z)
            lpz = (-0.5 * z ** 2 - 0.5 * math.log(2 * math.pi)).sum(1)
            lqz = (-0.5 * ((z - mu) ** 2) / lv.exp() - 0.5 * lv - 0.5 * math.log(2 * math.pi)).sum(1)
            lws.append(dlogistic_lp(q, m, ls).sum(1) + lpz - lqz)
        return torch.logsumexp(torch.stack(lws), 0) - math.log(K)

    @torch.no_grad()
    def sample(self, n, gen, z=None):
        z = torch.randn(n, self.zdim, generator=gen) if z is None else z
        m, _ = self.decode(z)
        return to_levels(m.numpy())  # the decoder's mean, on the 16 levels


# ---------------------------------------------------------------------------
# GANs on digits: multilayer perceptrons, the discriminator sees dequantized real digits
# ---------------------------------------------------------------------------
ZG = 32


def gan_nets(h=512):
    G = nn.Sequential(nn.Linear(ZG, h), nn.LeakyReLU(0.2), nn.Linear(h, h), nn.LeakyReLU(0.2), nn.Linear(h, D),
                      nn.Sigmoid())
    Dn = nn.Sequential(nn.Linear(D, h), nn.LeakyReLU(0.2), nn.Linear(h, h), nn.LeakyReLU(0.2), nn.Linear(h, 1))
    return G, Dn


def dequant(q, gen) -> torch.Tensor:
    """Levels to continuous pixels in [0, 1): (q + u) / 16 with u uniform, flattened."""
    q = torch.as_tensor(np.asarray(q), dtype=torch.float32).reshape(len(q), -1)
    return (q + torch.rand(q.shape, generator=gen)) / Q


# ---------------------------------------------------------------------------
# RealNVP on digits: affine couplings on logit pixels, checkerboard masks
# ---------------------------------------------------------------------------
ALPHA = 0.05


def logit_pre(y):
    """y in [0, 1) -> the logit of alpha + (1 - 2 alpha) y, and the log-determinant of that map (per image)."""
    p = ALPHA + (1 - 2 * ALPHA) * y
    x = torch.log(p) - torch.log1p(-p)
    ld = (math.log(1 - 2 * ALPHA) - torch.log(p) - torch.log1p(-p)).sum(1)
    return x, ld


class CouplingD(nn.Module):
    def __init__(self, mask, h=192):
        super().__init__()
        self.register_buffer("m", mask)
        self.net = nn.Sequential(nn.Linear(D, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(), nn.Linear(h, 2 * D))
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)
        self.scale = nn.Parameter(torch.zeros(D))

    def st(self, x):
        s, t = self.net(x * self.m).chunk(2, -1)
        s = self.scale.exp() * torch.tanh(s) * (1 - self.m)
        return s, t * (1 - self.m)

    def forward(self, x):
        s, t = self.st(x)
        return x * self.m + (1 - self.m) * (x * s.exp() + t), s.sum(1)

    def inverse(self, y):
        s, t = self.st(y)
        return y * self.m + (1 - self.m) * ((y - t) * (-s).exp())


class RealNVP(nn.Module):
    def __init__(self, L=8, h=192):
        super().__init__()
        ii, jj = np.meshgrid(range(S), range(S), indexing="ij")
        cb = torch.as_tensor(((ii + jj) % 2).ravel(), dtype=torch.float32)
        self.layers = nn.ModuleList([CouplingD(cb if k % 2 == 0 else 1 - cb, h) for k in range(L)])

    def log_prob_y(self, y):
        x, ld = logit_pre(y)
        for l in self.layers:
            x, s = l(x)
            ld = ld + s
        return (-0.5 * x ** 2 - 0.5 * math.log(2 * math.pi)).sum(1) + ld

    def bits(self, q, gen) -> torch.Tensor:
        """Bits per pixel of the 16-level digits (the dequantization bound): -[log p(y) - 196 log 16] / (196 ln 2)."""
        lp = self.log_prob_y(dequant(q, gen)) - D * math.log(Q)
        return -lp / (D * math.log(2))

    @torch.no_grad()
    def sample(self, n, gen, temp=1.0):
        x = temp * torch.randn(n, D, generator=gen)
        for l in reversed(self.layers):
            x = l.inverse(x)
        p = torch.sigmoid(x)
        y = ((p - ALPHA) / (1 - 2 * ALPHA)).clamp(0, 1 - 1e-6)
        return np.clip(np.floor(y.numpy() * Q), 0, Q - 1).astype(np.uint8).reshape(n, S, S)


# ---------------------------------------------------------------------------
# The judge: a digit classifier whose penultimate layer gives the features
# ---------------------------------------------------------------------------
class Classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.body = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                                  nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten(),
                                  nn.Linear(64 * 3 * 3, 128), nn.ReLU())
        self.head = nn.Linear(128, 10)

    def forward(self, x):
        return self.head(self.body(x))

    @torch.no_grad()
    def features(self, q, bs=1000):
        out = [self.body(as_float(q[a:a + bs])) for a in range(0, len(q), bs)]
        return torch.cat(out).numpy().astype(np.float64)

    @torch.no_grad()
    def classes(self, q, bs=1000):
        out = [self.head(self.body(as_float(q[a:a + bs]))).argmax(1) for a in range(0, len(q), bs)]
        return torch.cat(out).numpy()


def train_classifier(seed=0, epochs=3, bs=128):
    tseed(seed)
    d = digits()
    net = Classifier()
    opt = torch.optim.Adam(net.parameters(), 1e-3)
    it = batches(d["xtr"], bs, rng(seed), d["ytr"])
    steps = scaled(epochs * len(d["xtr"]) // bs)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, 3e-3, total_steps=steps)
    for s in range(steps):
        x, y = next(it)
        loss = F.cross_entropy(net(as_float(x)), torch.as_tensor(y))
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    acc = float((net.classes(d["xte"]) == d["yte"]).mean())
    return net, acc


# ---------------------------------------------------------------------------
# Metrics on features: Frechet distance (FID's formula), precision and recall
# ---------------------------------------------------------------------------
def gauss_stats(F_):
    F_ = np.asarray(F_, np.float64)
    return F_.mean(0), np.cov(F_, rowvar=False)


def fid_from(m1, S1, m2, S2) -> float:
    from scipy.linalg import sqrtm

    cs = sqrtm(S1 @ S2)
    cs = cs.real if np.iscomplexobj(cs) else cs
    return float(((m1 - m2) ** 2).sum() + np.trace(S1 + S2 - 2 * cs))


def sqd(A, B):
    return np.maximum((A * A).sum(1)[:, None] + (B * B).sum(1)[None] - 2 * A @ B.T, 0.0)


def prec_rec(real, fake, k=3):
    rr, ff, rf = sqd(real, real), sqd(fake, fake), sqd(real, fake)
    r_rad, f_rad = np.sort(rr, 1)[:, k], np.sort(ff, 1)[:, k]
    return float((rf <= r_rad[:, None]).any(0).mean()), float((rf <= f_rad[None, :]).any(1).mean())


class Judge:
    """The classifier's features of the 10,000 test digits (the reference for the Frechet distance), and of 2,000 of
    them (the real set for precision and recall).  ``judge(samples)`` scores any 2,000 generated digits."""

    def __init__(self, net: Classifier, n_ref=2000):
        d = digits()
        self.net = net
        self.f_test = net.features(d["xte"])
        self.mu, self.S = gauss_stats(self.f_test)
        self.f_real = self.f_test[:n_ref]

    def __call__(self, q) -> dict:
        f = self.net.features(q)
        m, S_ = gauss_stats(f)
        p, r = prec_rec(self.f_real, f)
        cls = np.bincount(self.net.classes(q), minlength=10)
        return dict(fid=fid_from(m, S_, self.mu, self.S), precision=p, recall=r, classes=cls.tolist())


# ---------------------------------------------------------------------------
# The restricted Boltzmann machine, small enough that its partition function can be summed exactly
# ---------------------------------------------------------------------------
class RBM:
    """Binary visible v (196) and hidden h; E(v, h) = -b.v - c.h - v^T W h.  Plain tensors, updated by hand."""

    def __init__(self, nv, nh, gen, base_rate=None):
        self.W = 0.01 * torch.randn(nv, nh, generator=gen)
        self.c = torch.zeros(nh)
        self.b = torch.zeros(nv) if base_rate is None else torch.log(base_rate / (1 - base_rate))

    def ph(self, v):
        return torch.sigmoid(v @ self.W + self.c)

    def pv(self, h):
        return torch.sigmoid(h @ self.W.T + self.b)

    def free_energy(self, v):
        return -(v @ self.b) - F.softplus(v @ self.W + self.c).sum(1)

    def gibbs(self, v, k, gen):
        for _ in range(k):
            h = torch.bernoulli(self.ph(v), generator=gen)
            v = torch.bernoulli(self.pv(h), generator=gen)
        return v

    def all_h(self):
        nh = self.W.shape[1]
        idx = torch.arange(2 ** nh)
        return ((idx[:, None] >> torch.arange(nh)) & 1).float()

    def log_z(self) -> float:
        """Exact: sum over all 2^nh hidden states of exp(c.h) prod_i (1 + exp(b_i + W_i h))."""
        H = self.all_h()
        return float(torch.logsumexp(H @ self.c + F.softplus(H @ self.W.T + self.b).sum(1), 0))

    def exact_sample(self, n, gen):
        """Exact samples: h from its marginal (all 2^nh states weighed), then v given h."""
        H = self.all_h()
        lw = H @ self.c + F.softplus(H @ self.W.T + self.b).sum(1)
        k = torch.multinomial(torch.softmax(lw, 0), n, replacement=True, generator=gen)
        return self.pv(H[k])

    def loglik(self, V) -> float:
        return float((-self.free_energy(V)).mean() - self.log_z())


def train_rbm(method: str, seed: int, nh=16, epochs=8, bs=100, lr=0.05, k=None, n_evals=16, chains=100, exact=True):
    """method: 'cd1', 'cd10' (Hinton 2002) or 'pcd' (Tieleman 2008).  Exact test log-likelihood along the way."""
    gen = tseed(seed)
    d = digits()
    Vtr, Vte = torch.as_tensor(binarize(d["xtr"])), torch.as_tensor(binarize(d["xte"]))
    rate = Vtr.mean(0).clamp(0.01, 0.99)
    m = RBM(D, nh, gen, rate)
    k = k or (10 if method == "cd10" else 1)
    persistent = torch.bernoulli(rate.expand(chains, -1), generator=gen)
    steps = scaled(epochs * len(Vtr) // bs)
    marks = sorted(set(np.linspace(0, steps, n_evals).astype(int))) if exact else []
    it = batches(Vtr.numpy(), bs, rng(seed))
    curve, snaps = [], []
    for s in range(steps + 1):
        if s in marks:
            curve.append((s, m.loglik(Vte[:2000])))
        if s == steps:
            break
        v0 = torch.as_tensor(next(it))
        ph0 = m.ph(v0)
        if method == "pcd":
            persistent = m.gibbs(persistent, k, gen)
            vk = persistent
        else:
            vk = m.gibbs(v0, k, gen)
        phk = m.ph(vk)
        a = lr * (1 - s / steps)
        m.W += a * (v0.T @ ph0 / len(v0) - vk.T @ phk / len(vk))
        m.b += a * (v0.mean(0) - vk.mean(0))
        m.c += a * (ph0.mean(0) - phk.mean(0))
    return m, dict(curve=curve, test_ll=m.loglik(Vte) if exact else None, steps=steps, k=k)


# ---------------------------------------------------------------------------
# A small VQ-VAE (codes on a 7 x 7 grid), and an autoregressive prior over its codes
# ---------------------------------------------------------------------------
class VQVAE(nn.Module):
    def __init__(self, K=32, dim=8, ch=32):
        super().__init__()
        self.K = K
        self.enc = nn.Sequential(nn.Conv2d(1, ch, 3, padding=1), nn.ReLU(), nn.Conv2d(ch, ch, 4, 2, 1), nn.ReLU(),
                                 nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(), nn.Conv2d(ch, dim, 1))
        self.code = nn.Parameter(torch.randn(K, dim) * 0.5)
        self.dec = nn.Sequential(nn.Conv2d(dim, ch, 3, padding=1), nn.ReLU(), nn.ConvTranspose2d(ch, ch, 4, 2, 1),
                                 nn.ReLU(), nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(), nn.Conv2d(ch, 2, 1))

    def quantize(self, e):
        flat = e.permute(0, 2, 3, 1).reshape(-1, e.shape[1])
        idx = torch.cdist(flat, self.code).argmin(1)
        qz = self.code[idx].view(e.shape[0], e.shape[2], e.shape[3], -1).permute(0, 3, 1, 2)
        return qz, idx.view(e.shape[0], e.shape[2], e.shape[3])

    def decode_codes(self, idx):
        qz = self.code[idx].permute(0, 3, 1, 2)
        m, ls = self.dec(qz).chunk(2, 1)
        return torch.sigmoid(m), ls.clamp(-5, 1)

    def loss(self, q, beta=0.25):
        q = torch.as_tensor(np.asarray(q), dtype=torch.long)
        e = self.enc(q[:, None].float() / (Q - 1))
        qz, idx = self.quantize(e)
        st = e + (qz - e).detach()  # the straight-through estimator
        m, ls = self.dec(st).chunk(2, 1)
        rec = -dlogistic_lp(q.reshape(len(q), -1), m.reshape(len(q), -1), ls.reshape(len(q), -1)).sum(1).mean()
        commit = ((e - qz.detach()) ** 2).mean()
        book = ((qz - e.detach()) ** 2).mean()
        return rec + book + beta * commit, rec, idx


class CodePrior(nn.Module):
    """p(code_1) p(code_2 | code_1) ...: a small causal transformer over the 49 codes in raster order."""

    def __init__(self, K=32, n=49, d=64, layers=2, heads=4):
        super().__init__()
        self.K, self.n = K, n
        self.tok = nn.Embedding(K + 1, d)  # K = the start symbol
        self.pos = nn.Parameter(torch.randn(n, d) * 0.02)
        layer = nn.TransformerEncoderLayer(d, heads, 4 * d, 0.0, batch_first=True, norm_first=True)
        self.tf = nn.TransformerEncoder(layer, layers)
        self.head = nn.Linear(d, K)
        self.register_buffer("causal", torch.triu(torch.full((n, n), float("-inf")), 1))

    def forward(self, codes):  # codes (b, 49) -> logits (b, 49, K) predicting each code from those before it
        x = torch.cat([torch.full((len(codes), 1), self.K, dtype=torch.long), codes[:, :-1]], 1)
        h = self.tf(self.tok(x) + self.pos, mask=self.causal)
        return self.head(h)

    @torch.no_grad()
    def sample(self, n, gen):
        codes = torch.zeros(n, self.n, dtype=torch.long)
        for i in range(self.n):
            p = F.softmax(self(codes)[:, i], -1)
            codes[:, i] = torch.multinomial(p, 1, generator=gen)[:, 0]
        return codes


def elapsed(t0: float) -> float:
    return time.time() - t0
