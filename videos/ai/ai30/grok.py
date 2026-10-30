"""Grokking, mechanistically: Nanda et al.'s one-layer transformer on (a + b) mod p, and their progress measures.

    the model    tokens a, b, "=" (vocabulary p + 1); learned positions; one attention layer (4 heads of 32), a ReLU MLP of
                 512 units, no layer norm; the logits over the p answers read at "="
    training     full batch on 30% of the p^2 pairs, AdamW (lr 1e-3, weight decay 1, betas 0.9 / 0.98), as in Nanda,
                 Chan, Lieberum, Smith & Steinhardt, "Progress measures for grokking via mechanistic interpretability"
                 (ICLR 2023)
    the size     p = 59 (Nanda et al. used 113), to fit a laptop: about 20 minutes on one thread
    measured     every ``SNAP`` steps: train and test loss and accuracy; the embedding's Fourier spectrum (how much of
                 W_E lies along cos(wk a) and sin(wk a) for each frequency k); the key frequencies; the restricted loss
                 (the logits with everything but the key frequencies' cos(w(a + b - c)) terms removed) and the excluded
                 loss (the training loss with exactly those terms removed); the weights' total size

Resumable: a checkpoint every ``CKPT`` steps holds the model, the optimizer and the measurements so far.
"""

from __future__ import annotations

import math
import os

import numpy as np

P, D, H, DMLP = 59, 128, 4, 512
FRAC, LR, WD = 0.3, 1e-3, 1.0
STEPS, SNAP, CKPT = 15000, 100, 1000
SEED = 2023  # Nanda et al. (2023)


def build():
    import torch
    import torch.nn as nn

    class Grok(nn.Module):
        def __init__(self):
            super().__init__()
            self.WE = nn.Parameter(torch.randn(P + 1, D) / math.sqrt(D))
            self.pos = nn.Parameter(torch.randn(3, D) / math.sqrt(D))
            self.Wq, self.Wk, self.Wv = (nn.Parameter(torch.randn(H, D, D // H) / math.sqrt(D)) for _ in range(3))
            self.Wo = nn.Parameter(torch.randn(H, D // H, D) / math.sqrt(D))
            self.W1 = nn.Parameter(torch.randn(D, DMLP) / math.sqrt(D))
            self.b1 = nn.Parameter(torch.zeros(DMLP))
            self.W2 = nn.Parameter(torch.randn(DMLP, D) / math.sqrt(DMLP))
            self.b2 = nn.Parameter(torch.zeros(D))
            self.WU = nn.Parameter(torch.randn(D, P) / math.sqrt(D))

        def forward(self, x, keep=False):
            """x: (B, 3) ids; only the last position ("=") is read, so only its query is computed."""
            h = self.WE[x] + self.pos[None]  # (B, 3, D)
            q = torch.einsum("bd,hde->bhe", h[:, -1], self.Wq)
            k = torch.einsum("btd,hde->bhte", h, self.Wk)
            v = torch.einsum("btd,hde->bhte", h, self.Wv)
            att = torch.softmax(torch.einsum("bhe,bhte->bht", q, k) / math.sqrt(D // H), -1)
            z = torch.einsum("bht,bhte->bhe", att, v)
            r = h[:, -1] + torch.einsum("bhe,hed->bd", z, self.Wo)
            pre = r @ self.W1 + self.b1
            act = torch.relu(pre)
            r2 = r + act @ self.W2 + self.b2
            logits = r2 @ self.WU
            return (logits, dict(att=att, act=act, resid=r)) if keep else logits

    return Grok()


def dataset(seed=SEED):
    import torch

    a, b = np.meshgrid(np.arange(P), np.arange(P), indexing="ij")
    a, b = a.ravel(), b.ravel()
    x = np.stack([a, b, np.full_like(a, P)], 1)
    y = (a + b) % P
    perm = np.random.Generator(np.random.PCG64(seed)).permutation(len(a))
    n_tr = int(FRAC * len(a))
    tr, te = perm[:n_tr], perm[n_tr:]
    return torch.tensor(x), torch.tensor(y), torch.tensor(tr), torch.tensor(te)


def fourier_basis():
    """Orthonormal Fourier basis on Z_p: the constant, then cos and sin of each frequency k = 1 ... (p - 1) / 2."""
    t = np.arange(P)
    rows, names = [np.ones(P) / math.sqrt(P)], ["const"]
    for k in range(1, (P - 1) // 2 + 1):
        for f, nm in ((np.cos, "cos"), (np.sin, "sin")):
            v = f(2 * np.pi * k * t / P)
            rows.append(v / np.linalg.norm(v))
            names.append(f"{nm}{k}")
    return np.array(rows), names


def restricted(L, key):
    """The part of a logit table L (a, b, c) along cos and sin of w_k (a + b), for each c and each key frequency k."""
    a = np.arange(P)
    sab = (a[:, None] + a[None, :]) % P
    keep = np.zeros_like(L)
    for k in key:
        for f in (np.cos, np.sin):
            w = f(2 * np.pi * k * sab / P)
            coef = np.einsum("ab,abc->c", w, L) / (w ** 2).sum()
            keep += w[:, :, None] * coef[None, None, :]
    return keep


def measure(model, x, y, tr, te, n_key=5):
    """Losses, accuracies, the embedding's spectrum, key frequencies, restricted and excluded losses."""
    import torch
    import torch.nn.functional as F

    with torch.no_grad():
        z = model(x)
        lp = torch.log_softmax(z.double(), -1)
        nll = -lp[torch.arange(len(y)), y]
        acc = (z.argmax(-1) == y).float()
        out = dict(train_loss=float(nll[tr].mean()), test_loss=float(nll[te].mean()),
                   train_acc=float(acc[tr].mean()), test_acc=float(acc[te].mean()))
        B, _ = fourier_basis()
        WE = model.WE[:P].double().numpy()
        coef = B @ WE  # (p, D): the embedding along each basis vector
        nk = (P - 1) // 2
        spec = np.array([np.sum(coef[2 * k - 1] ** 2 + coef[2 * k] ** 2) for k in range(1, nk + 1)])
        out["spectrum"] = spec / spec.sum()
        key = np.argsort(-spec)[:n_key] + 1  # the key frequencies (1-based)
        out["key"] = [int(k) for k in key]
        # the logits as a p x p x p table, (a, b) -> c; for each answer c, its part along the waves cos(w_k (a + b))
        # and sin(w_k (a + b)) of the key frequencies (Nanda et al.'s restricted logits)
        L = z.double().numpy().reshape(P, P, P)
        L = L - L.mean(-1, keepdims=True)
        keep = restricted(L, key)
        y_np = y.numpy()

        def ce(logits, idx):
            lt = torch.tensor(logits.reshape(P * P, P))[idx]
            return float(F.cross_entropy(lt, torch.tensor(y_np)[idx]))

        out["restricted_loss"] = ce(keep, te)  # only the key frequencies' waves kept: test loss
        out["excluded_loss"] = ce(L - keep, tr)  # those waves removed: training loss
        out["weight_norm"] = float(sum((p_.double() ** 2).sum() for p_ in model.parameters()) ** 0.5)
    return out


def train(ckpt_path, steps=STEPS, log=print):
    import torch
    import torch.nn.functional as F

    x, y, tr, te = dataset()
    torch.manual_seed(SEED)
    model = build()
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD, betas=(0.9, 0.98))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(s / 10, 1.0))
    hist, start = [], 0
    if os.path.exists(ckpt_path):
        ck = torch.load(ckpt_path, weights_only=False)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        sched.load_state_dict(ck["sched"])
        hist, start = ck["hist"], ck["step"]
        torch.set_rng_state(ck["rng"])
        log(f"    resuming grokking at step {start}")
    xt, yt = x[tr], y[tr]
    for s in range(start, steps + 1):
        if s % SNAP == 0 and (not hist or hist[-1]["step"] < s):
            m = measure(model, x, y, tr, te)
            m["step"] = s
            if s % 1000 == 0 or s in (100, 200, 500) or s == steps:
                m["WE"] = model.WE[:P].detach().numpy().astype(np.float16)  # the embedding at a few moments
            hist.append(m)
            if s % 1000 == 0:
                log(f"    step {s}: train {m['train_loss']:.3g} test {m['test_loss']:.3g} acc {m['test_acc']:.2f} "
                    f"key {m['key']} restricted {m['restricted_loss']:.3g} excluded {m['excluded_loss']:.3g}")
        if s % CKPT == 0 and s > start:
            tmp = str(ckpt_path) + ".tmp"
            torch.save(dict(model=model.state_dict(), opt=opt.state_dict(), sched=sched.state_dict(), hist=hist,
                            step=s, rng=torch.get_rng_state()), tmp)
            os.replace(tmp, ckpt_path)
        if s == steps:
            break
        loss = F.cross_entropy(model(xt), yt)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return model, hist, (x, y, tr, te)


def analyse(model, x, y):
    """The finished circuit: the embedding's spectrum, each MLP neuron's frequency, the logits against the cos(w(a+b-c))
    fit, and one neuron's activation over the (a, b) grid."""
    import torch

    B, names = fourier_basis()
    with torch.no_grad():
        _, c = model(x, keep=True)
        act = c["act"].double().numpy().reshape(P, P, DMLP)  # neuron activations over the grid of (a, b)
        z = model(x).double().numpy().reshape(P, P, P)
    # each neuron's activation in the 2D Fourier basis: its energy per frequency (a's and b's waves, and products)
    A2 = np.einsum("ia,jb,abn->ijn", B, B, act)  # (p, p, neurons)
    nk = (P - 1) // 2
    energy = np.zeros((nk, DMLP))
    for k in range(1, nk + 1):
        idx = [2 * k - 1, 2 * k]
        energy[k - 1] = (A2[np.ix_(idx, idx)] ** 2).sum((0, 1)) + (A2[np.ix_([0], idx)] ** 2).sum((0, 1)) + \
            (A2[np.ix_(idx, [0])] ** 2).sum((0, 1))
    tot = (A2 ** 2).sum((0, 1)) - A2[0, 0] ** 2
    frac = energy / np.maximum(tot, 1e-12)
    nfreq = frac.argmax(0) + 1
    nshare = frac.max(0)
    # the logits fit by the key frequencies' waves cos(w_k (a + b - c)) alone
    L = z - z.mean(-1, keepdims=True)
    a = np.arange(P)
    s = (a[:, None, None] + a[None, :, None] - a[None, None, :]) % P
    return dict(neuron_freq=nfreq, neuron_share=nshare, act=act, L=L, s=s)
