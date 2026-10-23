"""The self-supervised learners of Part 24 ("Learning Without Labels"), trained on MNIST on the CPU.

* the data: MNIST (LeCun, Cortes & Burges 1998) through Part 10's checked download (``videos.ai.ai10.data``),
  28 x 28 pixels in [0, 1];
* views (``augment``): a random affine crop (rotation, zoom, shear, shift), contrast, blur, an erased rectangle and
  noise, drawn for a whole batch at once from a seeded ``torch.Generator``; ``light=True`` keeps only the crop (what
  MAE and I-JEPA use);
* one encoder for every method: a three-layer convolutional network (``CNN``: a 4 x 4 map of 128 numbers, averaged
  to 128 numbers);
* the methods (``METHODS``): supervised, rotation prediction (Gidaris et al. 2018), SimCLR (Chen et al. 2020), MoCo
  (He et al. 2020), BYOL (Grill et al. 2020), SimSiam (Chen & He 2021), a naive siamese net, Barlow Twins (Zbontar et
  al. 2021), VICReg (Bardes, Ponce & LeCun 2022), DINO (Caron et al. 2021), and three masked methods on the same
  network: MAE (after He et al. 2022), a BEiT-style model predicting k-means codes of hidden patches (after Bao et
  al. 2022), and I-JEPA (after Assran et al. 2023);
* the measurements: a linear probe, a weighted k-nearest-neighbour vote (Wu et al. 2018), a probe from ten labels
  per class, the effective rank (Roy & Vetterli 2007; Garrido et al. 2023), alignment and uniformity (Wang & Isola
  2020), linear CKA (Kornblith et al. 2019) and mutual nearest neighbours (Huh et al. 2024).

Every method gets the same budget: ``STEPS`` updates of 256 encoder passes each (128 digits seen twice, or 256 once),
the same optimizer and schedule, several seeds. Everything random comes from a generator seeded per run.
"""

from __future__ import annotations

import copy
import math
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SCALE = float(os.environ.get("AI24_SCALE", "1.0"))  # AI24_SCALE=0.02: a quick smoke test of every code path
STEPS = max(30, int(round(800 * SCALE)))  # updates per run
B = 128  # digits per update, two views each: 256 encoder passes
N_CURVE = 12 if SCALE == 1.0 else 3  # evaluation points along a run
LR, WD, WARM = 2e-3, 1e-5, 0.05


def log(msg: str) -> None:
    print(f"    {time.strftime('%H:%M:%S')} {msg}", flush=True)


# ---------------------------------------------------------------------------
# The data
# ---------------------------------------------------------------------------
_D: dict = {}


def data() -> dict:
    """{'xtr', 'ytr', 'xte', 'yte'}: uint8 images (n, 28, 28) as tensors, and int64 labels."""
    if not _D:
        from videos.ai.ai10.data import mnist  # Part 10's download, checked against its SHA-256

        m = mnist()
        _D.update(xtr=torch.from_numpy(np.ascontiguousarray(m["xtr"])),
                  ytr=torch.from_numpy(m["ytr"].astype(np.int64)),
                  xte=torch.from_numpy(np.ascontiguousarray(m["xte"])),
                  yte=torch.from_numpy(m["yte"].astype(np.int64)))
        if SCALE < 1.0:  # the smoke test: a tenth of the digits
            for k, n in (("xtr", 6000), ("ytr", 6000), ("xte", 3000), ("yte", 3000)):
                _D[k] = _D[k][:n]
    return _D


def fl(x: torch.Tensor) -> torch.Tensor:
    """uint8 (n, H, W) -> float (n, 1, H, W) in [0, 1]."""
    return x.float().div(255.0).unsqueeze(1)


_K3 = torch.tensor([[1.0, 2.0, 1.0], [2.0, 4.0, 2.0], [1.0, 2.0, 1.0]]).div(16).view(1, 1, 3, 3)


def augment(x: torch.Tensor, g: torch.Generator, light: bool = False) -> torch.Tensor:
    """Random views of a batch ``x`` (n, 1, H, W) in [0, 1]: one random affine crop each (rotation within 20 degrees,
    zoom 0.85-1.5, shear, shift), then (unless ``light``) contrast and brightness, a blur for half of them, an erased
    rectangle for half of them, and pixel noise."""
    n, _, H, W = x.shape

    def U(a, b):
        return a + (b - a) * torch.rand(n, generator=g)

    th = U(-20.0, 20.0) * (math.pi / 180)
    zoom = U(0.85, 1.5)
    sh = U(-0.25, 0.25)
    tmax = (1 - 1 / zoom).clamp(min=0) + 0.12
    tx = (2 * torch.rand(n, generator=g) - 1) * tmax
    ty = (2 * torch.rand(n, generator=g) - 1) * tmax
    c, s = torch.cos(th), torch.sin(th)
    A = torch.stack([torch.stack([c / zoom, (c * sh - s) / zoom, tx], 1),
                     torch.stack([s / zoom, (s * sh + c) / zoom, ty], 1)], 1)
    grid = F.affine_grid(A, [n, 1, H, W], align_corners=False)
    v = F.grid_sample(x, grid, mode="bilinear", padding_mode="zeros", align_corners=False).clamp(0, 1)
    if light:
        return v
    gamma = torch.exp(U(-0.5, 0.5)).view(n, 1, 1, 1)
    v = v.pow(gamma) * U(0.5, 1.0).view(n, 1, 1, 1)
    blur = F.conv2d(F.pad(v, (1, 1, 1, 1)), _K3)
    wb = ((torch.rand(n, generator=g) < 0.5).float() * U(0.4, 1.0)).view(n, 1, 1, 1)
    v = v + wb * (blur - v)
    eh, ew, cy, cx = U(0.2, 0.45) * H, U(0.2, 0.45) * W, U(0, H), U(0, W)
    yy = torch.arange(H, dtype=torch.float32).view(1, H, 1)
    xx = torch.arange(W, dtype=torch.float32).view(1, 1, W)
    box = ((yy - cy.view(n, 1, 1)).abs() < eh.view(n, 1, 1) / 2) & ((xx - cx.view(n, 1, 1)).abs() < ew.view(n, 1, 1) / 2)
    on = (torch.rand(n, generator=g) < 0.5).view(n, 1, 1)
    v = v * (~(box & on)).unsqueeze(1).float()
    return v + U(0.0, 0.12).view(n, 1, 1, 1) * torch.randn(v.shape, generator=g)


# ---------------------------------------------------------------------------
# Encoders
# ---------------------------------------------------------------------------
class CNN(nn.Module):
    """Three strided convolutions (32, 64, 128 channels), a 4 x 4 map of 128 numbers, and its average: 128 numbers
    per image. Every method in this part trains this network."""

    def __init__(self, dim: int = 128):
        super().__init__()
        self.dim = dim
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 5, 2, 2, bias=False), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 3, 2, 1, bias=False), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.Conv2d(64, dim, 3, 2, 1, bias=False), nn.BatchNorm2d(dim), nn.ReLU(inplace=True))

    def fmap(self, x):
        return self.body(x)

    def forward(self, x):
        return self.body(x).mean((2, 3))


PATCH, SIDE = 4, 7  # 4 x 4 patches, a 7 x 7 grid on 28 x 28


def patchify(x: torch.Tensor) -> torch.Tensor:
    """(n, 1, 28, 28) -> (n, 49, 16), patches in reading order."""
    n = x.shape[0]
    return x.view(n, SIDE, PATCH, SIDE, PATCH).permute(0, 1, 3, 2, 4).reshape(n, SIDE * SIDE, PATCH * PATCH)


def unpatchify(p: torch.Tensor) -> torch.Tensor:
    n = p.shape[0]
    return p.view(n, SIDE, SIDE, PATCH, PATCH).permute(0, 1, 3, 2, 4).reshape(n, 1, SIDE * PATCH, SIDE * PATCH)


def mlp(dims, bn=True, last_bn=False, act=nn.ReLU) -> nn.Sequential:
    layers: list = []
    for i in range(len(dims) - 1):
        last = i == len(dims) - 2
        layers.append(nn.Linear(dims[i], dims[i + 1], bias=not bn or (last and not last_bn)))
        if not last:
            if bn:
                layers.append(nn.BatchNorm1d(dims[i + 1]))
            layers.append(act())
        elif last_bn:
            layers.append(nn.BatchNorm1d(dims[i + 1], affine=False))
    return nn.Sequential(*layers)


@torch.no_grad()
def ema(target: nn.Module, online: nn.Module, m: float) -> None:
    for pt, po in zip(target.parameters(), online.parameters()):
        pt.mul_(m).add_(po.detach(), alpha=1 - m)
    for bt, bo in zip(target.buffers(), online.buffers()):
        bt.copy_(bo)


def ema_m(t: float, base: float = 0.99) -> float:
    """BYOL's schedule: from ``base`` up to 1 along a half cosine."""
    return 1 - (1 - base) * (math.cos(math.pi * t) + 1) / 2


def nt_xent(z1, z2, tau):
    """SimCLR's normalized-temperature cross-entropy: each of the 2n views must pick its partner out of the other
    2n - 1."""
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    n = len(z1)
    s = (z @ z.t() / tau).masked_fill(torch.eye(2 * n, dtype=torch.bool), float("-inf"))
    tgt = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(s, tgt)


# ---------------------------------------------------------------------------
# Methods: each has .enc (the encoder evaluated), .loss(x, y, g, t) -> (loss, logs), .after(t)
# ---------------------------------------------------------------------------
class Method(nn.Module):
    views = 2  # augmented views per digit (256 passes per update)
    light = False  # crop-only views
    masked_input = False  # trained on blanked images: batch-norm statistics recomputed before evaluation

    def __init__(self, enc: nn.Module):
        super().__init__()
        self.enc = enc

    def after(self, t: float) -> None:
        pass

    def embed(self, x):
        """The normalized vector the loss compares (for alignment, uniformity and the sphere)."""
        return F.normalize(self.enc(x), dim=1)

    def two(self, x, g):
        v = augment(torch.cat([x, x]), g, light=self.light)
        return v[: len(x)], v[len(x):]


class Supervised(Method):
    views = 1

    def __init__(self, enc):
        super().__init__(enc)
        self.head = nn.Linear(enc.dim, 10)

    def loss(self, x, y, g, t):
        z = self.head(self.enc(augment(x, g, light=self.light)))
        return F.cross_entropy(z, y), {"acc": float((z.argmax(1) == y).float().mean())}


class Rotation(Method):
    """Gidaris, Singh & Komodakis (2018): which of four rotations was applied?"""
    views = 4

    def __init__(self, enc):
        super().__init__(enc)
        self.head = nn.Linear(enc.dim, 4)

    def loss(self, x, y, g, t):
        v = augment(x, g, light=True)
        r = torch.cat([torch.rot90(v, k, (2, 3)) for k in range(4)])
        lab = torch.arange(4).repeat_interleave(len(x))
        z = self.head(self.enc(r))
        return F.cross_entropy(z, lab), {"acc": float((z.argmax(1) == lab).float().mean())}


class SimCLR(Method):
    def __init__(self, enc, tau=0.2, out=128, nested=None, light=False):
        super().__init__(enc)
        self.tau, self.nested, self.light = tau, nested, light
        self.proj = mlp([enc.dim, 256, out])

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        z1, z2 = self.proj(self.enc(a)), self.proj(self.enc(b))
        if self.nested:  # Matryoshka: the same loss on every prefix, summed (Kusupati et al. 2022)
            L = sum(nt_xent(z1[:, :m], z2[:, :m], self.tau) for m in self.nested) / len(self.nested)
        else:
            L = nt_xent(z1, z2, self.tau)
        return L, {}


class MoCo(Method):
    """He et al. (2020), v2's recipe: a momentum key encoder and a queue of past keys as the negatives."""

    def __init__(self, enc, tau=0.2, K=4096, out=128, m=0.99):
        super().__init__(enc)
        self.tau, self.m = tau, m
        self.proj = mlp([enc.dim, 256, out])
        self.kenc, self.kproj = copy.deepcopy(self.enc), copy.deepcopy(self.proj)
        for p in list(self.kenc.parameters()) + list(self.kproj.parameters()):
            p.requires_grad_(False)
        self.register_buffer("queue", F.normalize(torch.randn(K, out, generator=torch.Generator().manual_seed(7)), dim=1))
        self.ptr = 0
        self._keys = None

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        q1, q2 = F.normalize(self.proj(self.enc(a)), dim=1), F.normalize(self.proj(self.enc(b)), dim=1)
        with torch.no_grad():
            k1, k2 = F.normalize(self.kproj(self.kenc(a)), dim=1), F.normalize(self.kproj(self.kenc(b)), dim=1)

        def ctr(q, k):
            logits = torch.cat([(q * k).sum(1, keepdim=True), q @ self.queue.t()], 1) / self.tau
            return F.cross_entropy(logits, torch.zeros(len(q), dtype=torch.long))

        self._keys = torch.cat([k1, k2])
        return (ctr(q1, k2) + ctr(q2, k1)) / 2, {}

    def after(self, t):
        ema(self.kenc, self.enc, self.m)
        ema(self.kproj, self.proj, self.m)
        k = self._keys
        K = len(self.queue)
        idx = (self.ptr + torch.arange(len(k))) % K
        self.queue[idx] = k
        self.ptr = int((self.ptr + len(k)) % K)


def neg_cos(p, z):
    return -(F.normalize(p, dim=1) * F.normalize(z, dim=1)).sum(1).mean()


class Naive(Method):
    """Pull the two views' vectors together, and nothing else: no negatives, no predictor, no stop-gradient."""

    def __init__(self, enc, out=128):
        super().__init__(enc)
        self.proj = mlp([enc.dim, 256, out])

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        return neg_cos(self.proj(self.enc(a)), self.proj(self.enc(b))), {}


class SimSiam(Method):
    """Chen & He (2021): a predictor on one side, a stop-gradient on the other; symmetric."""

    def __init__(self, enc, stopgrad=True, out=128):
        super().__init__(enc)
        self.sg = stopgrad
        self.proj = mlp([enc.dim, 256, 256, out], last_bn=True)
        self.pred = mlp([out, 64, out])

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        z1, z2 = self.proj(self.enc(a)), self.proj(self.enc(b))
        p1, p2 = self.pred(z1), self.pred(z2)
        if self.sg:
            z1, z2 = z1.detach(), z2.detach()
        return (neg_cos(p1, z2) + neg_cos(p2, z1)) / 2, {}


class BYOL(Method):
    """Grill et al. (2020): an online network with a predictor chases a slowly moving average of itself."""

    def __init__(self, enc, out=64, base=0.99):
        super().__init__(enc)
        self.base = base
        self.proj = mlp([enc.dim, 256, out])
        self.pred = mlp([out, 256, out])
        self.tenc, self.tproj = copy.deepcopy(self.enc), copy.deepcopy(self.proj)
        for p in list(self.tenc.parameters()) + list(self.tproj.parameters()):
            p.requires_grad_(False)

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        p1, p2 = self.pred(self.proj(self.enc(a))), self.pred(self.proj(self.enc(b)))
        with torch.no_grad():
            z1, z2 = self.tproj(self.tenc(a)), self.tproj(self.tenc(b))
        return 2 + (neg_cos(p1, z2) + neg_cos(p2, z1)), {}

    def after(self, t):
        m = ema_m(t, self.base)
        ema(self.tenc, self.enc, m)
        ema(self.tproj, self.proj, m)


def standardize(z):
    return (z - z.mean(0)) / (z.std(0) + 1e-5)


class Barlow(Method):
    """Zbontar et al. (2021): the two views' cross-correlation matrix pushed to the identity."""

    def __init__(self, enc, out=512, lam=5e-3):
        super().__init__(enc)
        self.lam = lam
        self.proj = mlp([enc.dim, 512, out])
        self.C = None

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        z1, z2 = standardize(self.proj(self.enc(a))), standardize(self.proj(self.enc(b)))
        c = z1.t() @ z2 / len(z1)
        d = torch.diagonal(c)
        on = (d - 1).pow(2).sum()
        off = c.pow(2).sum() - d.pow(2).sum()
        self.C = c.detach()
        return on + self.lam * off, {"on": float(on.detach()), "off": float(off.detach())}


class VICReg(Method):
    """Bardes, Ponce & LeCun (2022): invariance, a variance floor per dimension, decorrelated dimensions."""

    def __init__(self, enc, out=512, lam=25.0, mu=25.0, nu=1.0, variance=True):
        super().__init__(enc)
        self.lam, self.mu, self.nu, self.variance = lam, mu, nu, variance
        self.proj = mlp([enc.dim, 512, out])

    def embed(self, x):
        return F.normalize(self.proj(self.enc(x)), dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        z1, z2 = self.proj(self.enc(a)), self.proj(self.enc(b))
        inv = F.mse_loss(z1, z2)

        def var(z):
            return F.relu(1 - torch.sqrt(z.var(0) + 1e-4)).mean()

        def cov(z):
            z = z - z.mean(0)
            c = z.t() @ z / (len(z) - 1)
            return (c.pow(2).sum() - torch.diagonal(c).pow(2).sum()) / z.shape[1]

        v = (var(z1) + var(z2)) / 2
        cv = cov(z1) + cov(z2)
        L = self.lam * inv + (self.mu * v if self.variance else 0.0) + self.nu * cv
        return L, {"inv": float(inv.detach()), "var": float(v.detach()), "cov": float(cv.detach())}


class DINOHead(nn.Module):
    def __init__(self, dim, K=256, hidden=256, bottleneck=64):
        super().__init__()
        self.mlp = nn.Sequential(nn.Linear(dim, hidden), nn.GELU(), nn.Linear(hidden, hidden), nn.GELU(),
                                 nn.Linear(hidden, bottleneck))
        self.proto = nn.Parameter(torch.randn(K, bottleneck) * 0.1)

    def forward(self, h):
        return F.normalize(self.mlp(h), dim=1) @ F.normalize(self.proto, dim=1).t()


class DINO(Method):
    """Caron et al. (2021): a student matches a momentum teacher's softmax over K prototypes; the teacher's outputs are
    centred (a running mean subtracted) and sharpened (a low temperature)."""

    def __init__(self, enc, K=256, tau_s=0.1, tau_t=0.04, center=True, cm=0.9, base=0.99):
        super().__init__(enc)
        self.tau_s, self.tau_t, self.centering, self.cm, self.base = tau_s, tau_t, center, cm, base
        self.head = DINOHead(enc.dim, K)
        self.tenc, self.thead = copy.deepcopy(self.enc), copy.deepcopy(self.head)
        for p in list(self.tenc.parameters()) + list(self.thead.parameters()):
            p.requires_grad_(False)
        self.register_buffer("c", torch.zeros(1, K))
        self._tl = None

    def embed(self, x):
        return F.normalize(self.head.mlp(self.enc(x)), dim=1)

    def teacher_probs(self, logits):
        return F.softmax((logits - (self.c if self.centering else 0.0)) / self.tau_t, dim=1)

    def loss(self, x, y, g, t):
        a, b = self.two(x, g)
        s1, s2 = self.head(self.enc(a)), self.head(self.enc(b))
        with torch.no_grad():
            t1, t2 = self.thead(self.tenc(a)), self.thead(self.tenc(b))
            P1, P2 = self.teacher_probs(t1), self.teacher_probs(t2)
        ls1, ls2 = F.log_softmax(s1 / self.tau_s, 1), F.log_softmax(s2 / self.tau_s, 1)
        L = (-(P1 * ls2).sum(1).mean() - (P2 * ls1).sum(1).mean()) / 2
        self._tl = torch.cat([t1, t2])
        with torch.no_grad():
            P = torch.cat([P1, P2])
            H = float(-(P * P.clamp_min(1e-12).log()).sum(1).mean())
            kl = float(L.detach()) - H  # cross-entropy minus the teacher's entropy
            Pm = P.mean(0)
            Hm = float(-(Pm * Pm.clamp_min(1e-12).log()).sum())
        return L, {"H": H, "KL": kl, "Hmean": Hm}

    def after(self, t):
        self.c.mul_(self.cm).add_(self._tl.mean(0, keepdim=True), alpha=1 - self.cm)
        m = ema_m(t, self.base)
        ema(self.tenc, self.enc, m)
        ema(self.thead, self.head, m)


def patch_mask(g, n, ratio, side=SIDE):
    """round(ratio * side^2) patches hidden in each image, at random: bool (n, side * side)."""
    N = side * side
    k = int(round(N * ratio))
    order = torch.argsort(torch.rand(n, N, generator=g), dim=1)
    m = torch.zeros(n, N, dtype=torch.bool)
    m[torch.arange(n).unsqueeze(1), order[:, :k]] = True
    return m


def pixel_mask(m, patch=PATCH, side=SIDE):
    """A patch mask (n, side * side) as a pixel mask (n, 1, side * patch, side * patch)."""
    n = m.shape[0]
    return m.view(n, side, 1, side, 1).expand(n, side, patch, side, patch).reshape(n, 1, side * patch, side * patch)


class Up(nn.Module):
    """The decoder: the encoder's 4 x 4 map up to 7 x 7 (``to=7``) or on to 28 x 28, by transposed convolutions."""

    def __init__(self, cin=128, cout=1, to=28):
        super().__init__()
        layers = [nn.ConvTranspose2d(cin, 64, 3, 2, 1, bias=False), nn.BatchNorm2d(64), nn.ReLU(inplace=True)]
        if to == 7:
            layers.append(nn.Conv2d(64, cout, 1))
        else:
            layers += [nn.ConvTranspose2d(64, 32, 4, 2, 1, bias=False), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
                       nn.ConvTranspose2d(32, cout, 4, 2, 1)]
        self.net = nn.Sequential(*layers)

    def forward(self, f):
        return self.net(f)


class MAE(Method):
    """After He et al. (2022): hide most of the 49 patches (4 x 4 pixels) and reconstruct their pixels. Our encoder is
    the same convolutional network as every other method's, so hidden patches are blanked rather than dropped (a
    vision transformer can skip them, which is MAE's speed-up), and a small decoder paints the image back."""
    views = 1
    light = True
    masked_input = True

    def __init__(self, enc, ratio=0.75):
        super().__init__(enc)
        self.ratio = ratio
        self.dec = Up(enc.dim, 1, 28)

    def reconstruct(self, x, g):
        masked = patch_mask(g, len(x), self.ratio)
        pm = pixel_mask(masked)
        return self.dec(self.enc.fmap(x * (~pm).float())), masked

    def loss(self, x, y, g, t):
        v = augment(x, g, light=True)
        pred, masked = self.reconstruct(v, g)
        pm = pixel_mask(masked).float()
        return ((pred - v).pow(2) * pm).sum() / pm.sum(), {}


class BEiT(Method):
    """After Bao, Dong, Piao & Wei (2022): hide some patches and predict each hidden patch's discrete code, here from
    a k-means codebook of 4 x 4 patches (``kmeans_codebook``) in place of BEiT's learned tokenizer."""
    views = 1
    light = True
    masked_input = True

    def __init__(self, enc, codebook: torch.Tensor, ratio=0.4):
        super().__init__(enc)
        self.ratio = ratio
        self.register_buffer("cb", codebook)
        self.dec = Up(enc.dim, len(codebook), 7)

    def codes(self, x):
        p = patchify(x)
        return torch.cdist(p.reshape(-1, p.shape[-1]), self.cb).argmin(1).view(p.shape[0], -1)

    def loss(self, x, y, g, t):
        v = augment(x, g, light=True)
        masked = patch_mask(g, len(v), self.ratio)
        logits = self.dec(self.enc.fmap(v * (~pixel_mask(masked)).float())).flatten(2).transpose(1, 2)[masked]
        tgt = self.codes(v)[masked]
        return F.cross_entropy(logits, tgt), {"acc": float((logits.argmax(1) == tgt).float().mean())}


GRID = 4  # the encoder's final map is 4 x 4; each cell stands for a 7 x 7 square of the image


class IJEPA(Method):
    """After Assran et al. (2023): from the visible context, predict a slowly moving target encoder's representation of
    hidden blocks, never their pixels. On our network the representation is the final 4 x 4 map; the targets are two
    blocks of 2 x 2 cells; the predictor is two convolutions that see the context's map and where the targets are."""
    views = 1
    light = True
    masked_input = True

    def __init__(self, enc, base=0.99, ntgt=2):
        super().__init__(enc)
        self.base, self.ntgt = base, ntgt
        self.tenc = copy.deepcopy(enc)
        for p in self.tenc.parameters():
            p.requires_grad_(False)
        d = enc.dim
        self.pred = nn.Sequential(nn.Conv2d(d + 1, d, 3, 1, 1, bias=False), nn.BatchNorm2d(d), nn.ReLU(inplace=True),
                                  nn.Conv2d(d, d, 3, 1, 1, bias=False), nn.BatchNorm2d(d), nn.ReLU(inplace=True),
                                  nn.Conv2d(d, d, 1))

    def masks(self, g, n):
        m = torch.zeros(n, GRID, GRID, dtype=torch.bool)
        for _ in range(self.ntgt):
            r = torch.randint(0, GRID - 1, (n,), generator=g)
            c = torch.randint(0, GRID - 1, (n,), generator=g)
            for dr in (0, 1):
                for dc in (0, 1):
                    m[torch.arange(n), r + dr, c + dc] = True
        return m

    def loss(self, x, y, g, t):
        v = augment(x, g, light=True)
        m = self.masks(g, len(v))
        pm = m.repeat_interleave(7, 1).repeat_interleave(7, 2).unsqueeze(1)
        with torch.no_grad():
            tt = self.tenc.fmap(v).permute(0, 2, 3, 1)
            tt = F.layer_norm(tt, (tt.shape[-1],))
        c = self.enc.fmap(v * (~pm).float())
        p = self.pred(torch.cat([c, m.unsqueeze(1).float()], 1)).permute(0, 2, 3, 1)
        return F.mse_loss(p[m], tt[m]), {}

    def after(self, t):
        ema(self.tenc, self.enc, ema_m(t, self.base))


@torch.no_grad()
def recalibrate(enc: nn.Module, n: int = 4096, bs: int = 512) -> None:
    """Recompute the encoder's batch-norm statistics on clean training digits: a method that trains on blanked
    inputs would otherwise be evaluated with statistics of blanked images."""
    bns = [b for b in enc.modules() if isinstance(b, nn.BatchNorm2d)]
    mom = [b.momentum for b in bns]
    for b in bns:
        b.reset_running_stats()
        b.momentum = None  # a plain average over the batches
    was = enc.training
    enc.train()
    X = data()["xtr"][:n]
    for i in range(0, len(X), bs):
        enc(fl(X[i:i + bs]))
    for b, mo in zip(bns, mom):
        b.momentum = mo
    enc.train(was)


def kmeans_codebook(K=64, n=20000, iters=25, seed=0) -> torch.Tensor:
    """BEiT-style tokens for our patches: k-means on 4 x 4 patches of training digits (seeded k-means++)."""
    g = torch.Generator().manual_seed(seed)
    D = data()
    idx = torch.randperm(len(D["xtr"]), generator=g)[: n // 49 + 1]
    P = patchify(fl(D["xtr"][idx])).reshape(-1, PATCH * PATCH)[:n]
    C = P[torch.randint(0, len(P), (1,), generator=g)]
    for _ in range(K - 1):  # k-means++ seeding
        d = torch.cdist(P, C).min(1).values.pow(2)
        C = torch.cat([C, P[torch.multinomial(d / d.sum(), 1, generator=g)]])
    for _ in range(iters):
        a = torch.cdist(P, C).argmin(1)
        for k in range(K):
            m = a == k
            if m.any():
                C[k] = P[m].mean(0)
    return C


def make(name: str, **kw) -> Method:
    """A method by name, on a fresh encoder."""
    return METHODS[name](CNN(), **kw)


METHODS = {"supervised": Supervised, "rotation": Rotation, "simclr": SimCLR, "moco": MoCo, "naive": Naive,
           "simsiam": SimSiam, "byol": BYOL, "barlow": Barlow, "vicreg": VICReg, "dino": DINO, "mae": MAE,
           "beit": BEiT, "ijepa": IJEPA}


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------
@torch.no_grad()
def features(f, X: torch.Tensor, bs: int = 1000, module: nn.Module | None = None) -> torch.Tensor:
    """``f`` (a module, or a function of the images with its ``module``) applied to uint8 images ``X`` in eval
    mode, in batches."""
    mod = module if module is not None else f
    was = mod.training
    mod.eval()
    out = torch.cat([f(fl(X[i:i + bs])) for i in range(0, len(X), bs)])
    mod.train(was)
    return out


@torch.no_grad()
def knn_pred(ftr, ytr, fte, k=20, T=0.07) -> torch.Tensor:
    """Weighted k-nearest-neighbour vote by cosine similarity (Wu et al. 2018), after subtracting the training
    features' mean (a shared offset would otherwise dominate every cosine): the predicted labels."""
    mu = ftr.mean(0, keepdim=True)
    a, b = F.normalize(ftr - mu, dim=1), F.normalize(fte - mu, dim=1)
    out = []
    for i in range(0, len(b), 1000):
        s, j = (b[i:i + 1000] @ a.t()).topk(k, dim=1)
        out.append(torch.zeros(len(s), 10).scatter_add_(1, ytr[j], (s / T).exp()).argmax(1))
    return torch.cat(out)


def knn(ftr, ytr, fte, yte, k=20, T=0.07) -> float:
    return float((knn_pred(ftr, ytr, fte, k, T) == yte).float().mean())


def linear_probe(ftr, ytr, fte, yte, wd=1e-4, iters=200) -> float:
    """Multinomial logistic regression on standardized features (full batch, L-BFGS): test accuracy."""
    mu, sd = ftr.mean(0), ftr.std(0) + 1e-6
    a, b = (ftr - mu) / sd, (fte - mu) / sd
    W = torch.zeros(a.shape[1], 10, requires_grad=True)
    c = torch.zeros(10, requires_grad=True)
    opt = torch.optim.LBFGS([W, c], lr=1, max_iter=iters, history_size=20, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        L = F.cross_entropy(a @ W + c, ytr) + wd * W.pow(2).sum()
        L.backward()
        return L

    opt.step(closure)
    with torch.no_grad():
        return float(((b @ W + c).argmax(1) == yte).float().mean())


def few_label(ftr, ytr, fte, yte, per=10, draws=5, seed=0, wd=1e-2) -> list[float]:
    """The linear probe from ``per`` labelled digits of each class, ``draws`` random draws."""
    g = np.random.default_rng(seed)
    yn = ytr.numpy()
    out = []
    for _ in range(draws):
        idx = np.concatenate([g.choice(np.flatnonzero(yn == c), per, replace=False) for c in range(10)])
        t = torch.from_numpy(idx)
        out.append(linear_probe(ftr[t], ytr[t], fte, yte, wd=wd, iters=100))
    return out


def eff_rank(f: torch.Tensor) -> float:
    """exp(entropy of the normalized singular values): 1 for a collapsed (rank-one) set (RankMe, Garrido et al.
    2023, after Roy & Vetterli 2007)."""
    s = torch.linalg.svdvals(f.double())
    p = s / s.sum() + 1e-12
    return float(torch.exp(-(p * p.log()).sum()))


def spread(z: torch.Tensor) -> float:
    """The standard deviation of the unit vectors, averaged over coordinates (SimSiam's collapse meter: about
    1/sqrt(d) when spread out, 0 when collapsed)."""
    return float(F.normalize(z, dim=1).std(0).mean())


def align_uniform(z1, z2, t=2.0):
    """Wang & Isola (2020): E|f(x) - f(y)|^2 over positive pairs, and log E exp(-t |f(x) - f(y)|^2) over all pairs."""
    z1, z2 = F.normalize(z1, dim=1), F.normalize(z2, dim=1)
    al = float((z1 - z2).pow(2).sum(1).mean())
    d2 = torch.pdist(z1).pow(2)
    un = float(torch.log(torch.exp(-t * d2).mean()))
    return al, un


def cka(X, Y) -> float:
    """Linear centred kernel alignment (Kornblith et al. 2019)."""
    X, Y = X.double() - X.double().mean(0), Y.double() - Y.double().mean(0)
    return float((Y.t() @ X).pow(2).sum() / ((X.t() @ X).pow(2).sum().sqrt() * (Y.t() @ Y).pow(2).sum().sqrt()))


def mutual_knn(X, Y, k=10) -> float:
    """Huh, Cheung, Wang & Isola (2024): the average fraction of each point's k nearest neighbours (by cosine, after
    centring) that the two representations share."""
    def nn_sets(Z):
        Z = Z.double()
        Z = F.normalize(Z - Z.mean(0, keepdim=True), dim=1)
        s = Z @ Z.t()
        s.fill_diagonal_(-2)
        return s.topk(k, dim=1).indices

    a, b = nn_sets(X), nn_sets(Y)
    hit = (a.unsqueeze(2) == b.unsqueeze(1)).any(2).float().sum(1)
    return float((hit / k).mean())


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def lr_at(step: int, steps: int) -> float:
    w = max(1, int(WARM * steps))
    if step < w:
        return LR * (step + 1) / w
    return LR * 0.5 * (1 + math.cos(math.pi * (step - w) / max(1, steps - w)))


def curve_points(steps: int, n: int = N_CURVE) -> list[int]:
    return sorted(set([0] + [int(round(steps * (k / n) ** 1.5)) for k in range(1, n + 1)]))


def train(m: Method, seed: int, steps: int = None, pool=None, record=None, record_at=None, curve=True,
          half=None) -> dict:
    """Train ``m`` for ``steps`` updates on ``pool`` (indices into the training set; default all of it), seeded by
    ``seed``. Every ``curve_points`` step: the k-NN accuracy (a 5,000-digit bank, 1,000 test digits), the effective
    rank and the spread of the encoder's output. ``record(m, step)`` -> dict is called at the steps ``record_at``
    (snapshots for a replay). ``half``: 'top' or 'bottom' trains on that half of every image."""
    steps = steps or STEPS
    torch.manual_seed(seed)
    g = torch.Generator().manual_seed(seed)
    D = data()
    X = D["xtr"] if pool is None else D["xtr"][torch.as_tensor(pool)]
    Y = D["ytr"] if pool is None else D["ytr"][torch.as_tensor(pool)]
    crop = (lambda x: x[:, :14]) if half == "top" else (lambda x: x[:, 14:]) if half == "bottom" else (lambda x: x)
    ge = torch.Generator().manual_seed(1234)  # the evaluation subsets: the same for every run
    bank = torch.randperm(len(D["xtr"]), generator=ge)[:5000 if SCALE == 1.0 else 1000]
    tst = torch.randperm(len(D["xte"]), generator=ge)[:1000 if SCALE == 1.0 else 500]
    Xb, Yb = crop(D["xtr"][bank]), D["ytr"][bank]
    Xt, Yt = crop(D["xte"][tst]), D["yte"][tst]
    params = [p for p in m.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=LR, weight_decay=WD)
    n_img = 2 * B // m.views if m.views != 2 else B
    pts = set(curve_points(steps)) if curve else set()
    rec_at = set(record_at or [])
    has_z = type(m).embed is not Method.embed
    out = {"steps": [], "knn": [], "rank": [], "spread": [], "zrank": [], "zspread": [], "loss": [], "logs": [],
           "rec": [], "rec_steps": []}
    run_loss, run_n, logs_acc = 0.0, 0, {}
    t0 = time.time()

    def checkpoint(step):
        if step in pts:
            if m.masked_input:
                recalibrate(m.enc)
            fb, ft = features(m.enc, Xb), features(m.enc, Xt)
            out["steps"].append(step)
            out["knn"].append(knn(fb, Yb, ft, Yt))
            out["rank"].append(eff_rank(ft))
            out["spread"].append(spread(ft))
            if has_z:
                fz = features(m.embed, Xt, module=m)
                out["zrank"].append(eff_rank(fz))
                out["zspread"].append(spread(fz))
            out["loss"].append(run_loss / max(run_n, 1) if run_n else float("nan"))
            out["logs"].append({k: v / max(run_n, 1) for k, v in logs_acc.items()})
        if step in rec_at and record is not None:
            out["rec"].append(record(m, step))
            out["rec_steps"].append(step)

    for step in range(steps):
        if step in pts or step in rec_at:
            checkpoint(step)
            if step in pts:
                run_loss, run_n, logs_acc = 0.0, 0, {}
        for gr in opt.param_groups:
            gr["lr"] = lr_at(step, steps)
        idx = torch.randint(0, len(X), (n_img,), generator=g)
        x = fl(crop(X[idx]))
        L, logs = m.loss(x, Y[idx], g, step / steps)
        opt.zero_grad(set_to_none=True)
        L.backward()
        opt.step()
        m.after(step / steps)
        lv = float(L.detach())
        run_loss, run_n = run_loss + lv, run_n + 1
        for k, v in logs.items():
            logs_acc[k] = logs_acc.get(k, 0.0) + v
        if not math.isfinite(lv):
            log(f"non-finite loss at step {step}")
    checkpoint(steps)
    out["secs"] = time.time() - t0
    out["n_img"] = n_img
    return out


def evaluate(m: Method, few=True, half=None, extra_embed=True) -> tuple[dict, torch.Tensor]:
    """The full measurements of a trained encoder; returns (numbers, test features of the 2,000 CKA digits)."""
    D = data()
    if m.masked_input:
        recalibrate(m.enc)
    crop = (lambda x: x[:, :14]) if half == "top" else (lambda x: x[:, 14:]) if half == "bottom" else (lambda x: x)
    ftr, fte = features(m.enc, crop(D["xtr"])), features(m.enc, crop(D["xte"]))
    res = {"linear": linear_probe(ftr, D["ytr"], fte, D["yte"]), "knn": knn(ftr, D["ytr"], fte, D["yte"]),
           "rank": eff_rank(fte[:2000]), "spread": spread(fte[:2000]), "dim": int(fte.shape[1])}
    if few:
        res["few"] = few_label(ftr, D["ytr"], fte, D["yte"])
    g = torch.Generator().manual_seed(99)
    x = fl(crop(D["xte"][:1000]))
    with torch.no_grad():
        m.eval()
        a, b = augment(x, g, light=m.light), augment(x, g, light=m.light)
        res["align_h"], res["unif_h"] = align_uniform(m.enc(a), m.enc(b))
        if extra_embed and type(m).embed is not Method.embed:
            res["align_z"], res["unif_z"] = align_uniform(m.embed(a), m.embed(b))
            res["rank_z"] = eff_rank(m.embed(x))
        m.train()
    return res, fte[:2000].clone()


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())
