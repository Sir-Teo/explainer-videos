"""Part 23's codebook experiments on Part 21's letter pictures.

* k-means codebooks for 4 x 4 patches (the codebook idea, no network), and residual quantization in stages,
  compared at equal bits;
* a small VQ autoencoder trained five ways at the same budget and the same number of codes (256 for each of the 25
  cells of a letter): plain VQ (codebook and commitment losses, straight-through gradient), VQ with EMA codebook
  updates, EMA plus restarts of dead codes, finite scalar quantization (FSQ, levels 4 x 4 x 4 x 4), and lookup-free
  quantization (LFQ, 8 signs, with its entropy term).  Usage and perplexity of the codes, and the reconstruction
  error, are measured through training.
"""

from __future__ import annotations

import math
import os

import numpy as np

SCALE = float(os.environ.get("AI23_SCALE", "1"))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nearest(X, C):
    """The index of each row of X's nearest code in C (squared distances by |x|^2 - 2 x.c + |c|^2), in chunks."""
    out = np.empty(len(X), np.int64)
    cc = (C * C).sum(1)[None]
    for i in range(0, len(X), 4096):
        out[i:i + 4096] = (cc - 2 * X[i:i + 4096] @ C.T).argmin(1)
    return out


def kmeans(X, k, seed=0, iters=30):
    g = rng(seed)
    C = X[g.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        a = nearest(X, C)
        sums = np.zeros_like(C)
        np.add.at(sums, a, X)
        n = np.bincount(a, minlength=k)
        empty = n == 0
        C[~empty] = sums[~empty] / n[~empty, None]
        if empty.any():  # an empty cluster restarts at a random point
            C[empty] = X[g.integers(len(X), size=int(empty.sum()))]
    return C, nearest(X, C)


def patches_of(imgs, P=4):
    n = imgs.shape[1] // P
    return imgs.reshape(len(imgs), n, P, n, P).transpose(0, 1, 3, 2, 4).reshape(-1, P * P)


def rebuild(codes_patches, n=5, P=4):
    return codes_patches.reshape(n, n, P, P).transpose(0, 2, 1, 3).reshape(n * P, n * P)


def compute_codebooks():
    """k-means codebooks of 4 x 4 patches; residual stages of 16 codes against one codebook, at equal bits."""
    from videos.ai.ai21.compute import glyph_images

    imgs, labels, _ = glyph_images()
    P, n = 4, imgs.shape[1] // 4
    patches = patches_of(imgs)
    g = rng(2017)  # van den Oord et al., VQ-VAE
    fit = patches[g.choice(len(patches), min(len(patches), int(16_000 * max(SCALE, 0.25))), replace=False)]
    evalp = patches[g.choice(len(patches), 6_000, replace=False)]
    test_img = imgs[labels == 0][7]  # an A
    tp = patches_of(test_img[None])
    out = dict(image=test_img, sizes=[16, 64, 256, 1024])
    for k in out["sizes"]:
        C, _ = kmeans(fit, k, seed=k, iters=30 if k < 1024 else 15)
        out[f"err_vq{k}"] = float(np.sqrt(((C[nearest(evalp, C)] - evalp) ** 2).mean()))
        out[f"img_vq{k}"] = rebuild(C[nearest(tp, C)])
        if k == 16:
            out["codebook16"] = C.reshape(-1, P, P)
            out["code16"] = nearest(tp, C)
    res_fit, res_eval, res_t, rec_eval, rec_t = fit.copy(), evalp.copy(), tp.copy(), 0 * evalp, 0 * tp
    out["rvq_errs"] = []
    for stage in range(4):  # quantize, then quantize what's left, with a fresh codebook of 16 each time
        C, _ = kmeans(res_fit, 16, seed=100 + stage)
        res_fit = res_fit - C[nearest(res_fit, C)]
        qe, qt = C[nearest(res_eval, C)], C[nearest(res_t, C)]
        rec_eval, rec_t = rec_eval + qe, rec_t + qt
        res_eval, res_t = res_eval - qe, res_t - qt
        out["rvq_errs"].append(float(np.sqrt(((rec_eval - evalp) ** 2).mean())))
        out[f"img_rvq{stage + 1}"] = rebuild(rec_t)
    out["err_none"] = float(np.sqrt(((evalp - evalp.mean(0)) ** 2).mean()))
    out["n_patches"] = int(len(patches))
    print("    codebooks {}; residual stages of 16 {}".format(
        [round(out[f'err_vq{k}'], 3) for k in out["sizes"]], np.round(out["rvq_errs"], 3)), flush=True)
    assert out["rvq_errs"][-1] < out["rvq_errs"][0] and out["err_vq256"] < out["err_vq16"]
    return out


# ---------------------------------------------------------------------------
# A VQ autoencoder, five ways
# ---------------------------------------------------------------------------
VQ_METHODS = ["vq", "ema", "restart", "fsq", "lfq"]
VQ_SEEDS = [0, 1, 2]
VQ_K = 256
VQ_D = 16
VQ_STEPS = 3000
VQ_BATCH = 64
VQ_CHECKS = [0, 25, 100, 300, 800, 1600, 3000]


def make_vq_nets(D=VQ_D):
    import torch.nn as nn

    enc = nn.Sequential(nn.Conv2d(1, 32, 4, 2, 1), nn.ReLU(), nn.Conv2d(32, 64, 4, 2, 1), nn.ReLU(),
                        nn.Conv2d(64, 64, 3, 1, 1), nn.ReLU(), nn.Conv2d(64, D, 1))
    dec = nn.Sequential(nn.Conv2d(D, 64, 3, 1, 1), nn.ReLU(), nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.ReLU(),
                        nn.ConvTranspose2d(32, 16, 4, 2, 1), nn.ReLU(), nn.Conv2d(16, 1, 3, 1, 1))
    return enc, dec


class Quantizer:
    """One of the five quantizers.  ``__call__(z)`` takes the encoder's vectors (N x D) and returns the quantized
    vectors (straight-through), the codes, and the extra loss terms."""

    def __init__(self, method: str, seed: int):
        import torch
        import torch.nn as nn

        self.method = method
        g = torch.Generator().manual_seed(seed)
        self.params = []
        if method in ("vq", "ema", "restart"):
            # the textbook initialization (an embedding table, uniform in +-1/K) sits far from the encoder's outputs
            self.C = (torch.rand(VQ_K, VQ_D, generator=g) * 2 - 1) / VQ_K
            if method == "vq":
                self.C = nn.Parameter(self.C)
                self.params = [self.C]
            else:
                self.ema_n = torch.ones(VQ_K)  # as if each code had been chosen once, by itself: unused codes stay put
                self.ema_sum = self.C.clone()
                self.idle = torch.zeros(VQ_K)
        elif method == "fsq":
            self.levels = [4, 4, 4, 4]
            self.pin = nn.Linear(VQ_D, 4)
            self.pout = nn.Linear(4, VQ_D)
            self.params = [*self.pin.parameters(), *self.pout.parameters()]
        elif method == "lfq":
            self.bits = 8
            self.pin = nn.Linear(VQ_D, self.bits)
            self.pout = nn.Linear(self.bits, VQ_D)
            self.params = [*self.pin.parameters(), *self.pout.parameters()]
            self.corners = torch.tensor([[1.0 if (c >> b) & 1 else -1.0 for b in range(self.bits)]
                                         for c in range(2 ** self.bits)])
        self.g = g

    def codebook(self):
        import torch

        if self.method in ("vq", "ema", "restart"):
            return self.C.detach().clone()
        if self.method == "fsq":
            grid = torch.stack(torch.meshgrid(*[torch.arange(L) for L in self.levels], indexing="ij"), -1).reshape(-1, 4)
            return self.pout((grid.float() - 1.5) / 2).detach()  # levels -1.5 .. 1.5 (even L), scaled by L // 2
        return self.pout(self.corners).detach()

    def __call__(self, z, train=True):
        import torch
        import torch.nn.functional as F

        m = self.method
        if m in ("vq", "ema", "restart"):
            C = self.C
            d = (z * z).sum(1, keepdim=True) - 2 * z @ C.T + (C * C).sum(1)[None]
            codes = d.argmin(1)
            e = C[codes]
            aux = 0.25 * F.mse_loss(z, e.detach())  # commitment: keep z near its code (beta = 0.25)
            if m == "vq":
                aux = aux + F.mse_loss(e, z.detach())  # the codebook loss: pull the chosen codes toward z
            elif train:
                with torch.no_grad():  # EMA: each code becomes a running average of the vectors that chose it
                    onehot = F.one_hot(codes, VQ_K).float()
                    n = onehot.sum(0)
                    self.ema_n.mul_(0.99).add_(n, alpha=0.01)
                    self.ema_sum.mul_(0.99).add_(onehot.T @ z.detach(), alpha=0.01)
                    self.C = self.ema_sum / self.ema_n.clamp_min(1e-5)[:, None]
                    if m == "restart":  # a code unused for 50 steps restarts at a random vector of this batch
                        self.idle = torch.where(n > 0, torch.zeros_like(self.idle), self.idle + 1)
                        dead = (self.idle >= 50).nonzero()[:, 0]
                        if len(dead):
                            pick = torch.randint(0, len(z), (len(dead),), generator=self.g)
                            self.C[dead] = z.detach()[pick]
                            self.ema_sum[dead] = z.detach()[pick]
                            self.ema_n[dead] = 1.0
                            self.idle[dead] = 0
            zq = z + (e - z).detach()  # straight through: forward e, backward as if z
            return zq, codes, aux
        if m == "fsq":
            h = self.pin(z)
            half = 1.5 * (1 - 1e-3)
            shift = math.atanh(0.5 / half)
            b = torch.tanh(h + shift) * half - 0.5  # in (-2, 1): rounds to -2, -1, 0, 1
            q = b + (torch.round(b) - b).detach()
            idx = (torch.round(b).long() + 2)
            codes = ((idx[:, 0] * 4 + idx[:, 1]) * 4 + idx[:, 2]) * 4 + idx[:, 3]
            return self.pout((q + 0.5) / 2), codes, torch.zeros(())
        h = self.pin(z)  # LFQ: each of 8 numbers becomes its sign
        q = h + (torch.sign(h) + (h == 0).float() - h).detach()
        bits = (h > 0).long()
        codes = (bits * (2 ** torch.arange(self.bits))).sum(1)
        logits = 2 * h @ self.corners.T  # -|h - c|^2 up to terms that don't depend on c
        p = F.softmax(logits, 1)
        per = -(p * F.log_softmax(logits, 1)).sum(1).mean()
        avg = p.mean(0)
        batch_h = -(avg * (avg + 1e-9).log()).sum()
        aux = 0.1 * (per - batch_h) + 0.25 * F.mse_loss(h, q.detach())
        return self.pout(q), codes, aux


def vq_data():
    from videos.ai.ai21.compute import glyph_images

    imgs, labels, _ = glyph_images()
    g = rng(20)
    perm = g.permutation(len(imgs))
    n_test = len(imgs) // 8
    return imgs[perm[n_test:]], imgs[perm[:n_test]], labels[perm[:n_test]]


def run_vq(method: str, seed: int, threads: int = 1):
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(threads)
    train, test, _ = vq_data()
    Xtr = torch.tensor(train[:, None], dtype=torch.float32)
    Xte = torch.tensor(test[:, None], dtype=torch.float32)
    torch.manual_seed(seed)
    enc, dec = make_vq_nets()
    qz = Quantizer(method, seed)
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters(), *qz.params], lr=1e-3)
    g = torch.Generator().manual_seed(1000 + seed)
    steps = max(50, int(VQ_STEPS * SCALE))
    checks = sorted({min(c, steps) for c in VQ_CHECKS})
    show = Xte[:6]
    zfix = torch.randperm(len(Xte), generator=torch.Generator().manual_seed(7))[:16]
    curve, snaps = [], []

    def flat(x):
        z = enc(x)
        return z.permute(0, 2, 3, 1).reshape(-1, VQ_D), z.shape

    def recon(x, train_mode=False):
        zf, shp = flat(x)
        zq, codes, aux = qz(zf, train=train_mode)
        zq = zq.reshape(shp[0], shp[2], shp[3], VQ_D).permute(0, 3, 1, 2)
        return torch.sigmoid(dec(zq)), codes, aux, zf

    def measure():
        with torch.no_grad():
            y, codes, _, zf = recon(Xte)
            cnt = np.bincount(codes.numpy(), minlength=VQ_K)
            p = cnt / cnt.sum()
            ppl = float(np.exp(-(p[p > 0] * np.log(p[p > 0])).sum()))
            ys, _, _, _ = recon(show)
            zs = flat(Xte[zfix])[0]
            return dict(mse=float(F.mse_loss(y, Xte)), used=int((cnt > 0).sum()), ppl=ppl, counts=cnt,
                        recon=ys[:, 0].numpy(), z=zs.numpy(), book=qz.codebook().numpy())

    for step in range(steps + 1):
        if step in checks:
            m = measure()
            m["step"] = step
            snaps.append(m)
        if step == steps:
            break
        x = Xtr[torch.randint(0, len(Xtr), (VQ_BATCH,), generator=g)]
        y, codes, aux, _ = recon(x, train_mode=True)
        rec = F.mse_loss(y, x)
        loss = rec + aux
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 25 == 0:
            curve.append([step, float(rec), int(len(torch.unique(codes)))])
    last = snaps[-1]
    return dict(method=method, seed=seed, curve=curve, checks=checks,
                used=[s["used"] for s in snaps], ppl=[s["ppl"] for s in snaps], mse=[s["mse"] for s in snaps],
                final_used=last["used"], final_ppl=last["ppl"], final_mse=last["mse"],
                counts=last["counts"].tolist(), recon=[s["recon"].tolist() for s in snaps],
                z=[s["z"].tolist() for s in snaps], book=[s["book"].tolist() for s in snaps])
