"""Small networks of Part 11: the spirals (Part 9) for the edge of stability and for the natural gradient, and a
one-layer attention model of Part 1's books for QK-clip.

Every run is seeded; nothing sets torch's thread count at import time.
"""

from __future__ import annotations

import math

import numpy as np


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# The edge of stability
# ---------------------------------------------------------------------------
def eos_run(eta: float, steps: int = 4000, every: int = 40, seed: int = 0):
    """Full-batch gradient descent on the spirals (squared error against one-hot targets, as in Cohen et al.'s
    cleanest examples); every ``every`` steps the loss and the sharpness, the Hessian's largest eigenvalue, by power
    iteration on Hessian-vector products."""
    import torch

    from videos.ai.ai9.compute import spirals

    X, y = spirals(n=200, seed=1)
    Xt, yt = torch.tensor(X, dtype=torch.float64), torch.tensor(y)
    Yt = torch.nn.functional.one_hot(yt, 2).double()
    torch.manual_seed(seed)
    net = torch.nn.Sequential(torch.nn.Linear(2, 64), torch.nn.Tanh(), torch.nn.Linear(64, 64), torch.nn.Tanh(),
                              torch.nn.Linear(64, 2)).double()
    params = list(net.parameters())
    gen = torch.Generator().manual_seed(seed + 99)

    def loss_fn():
        return 0.5 * ((net(Xt) - Yt) ** 2).sum(1).mean()

    def sharpness(iters=20):
        v = [torch.randn(p.shape, generator=gen, dtype=p.dtype) for p in params]
        nv = math.sqrt(sum(float((a * a).sum()) for a in v))
        v = [a / nv for a in v]
        lam = 0.0
        for _ in range(iters):
            g = torch.autograd.grad(loss_fn(), params, create_graph=True)
            hv = torch.autograd.grad(sum((a * b).sum() for a, b in zip(g, v)), params)
            lam = sum(float((a * b).sum()) for a, b in zip(hv, v))
            nh = math.sqrt(sum(float((a * a).sum()) for a in hv))
            v = [a / nh for a in hv]
        return lam

    curve = []
    for step in range(steps + 1):
        if step % every == 0:
            curve.append((step, float(loss_fn()), sharpness()))
        net.zero_grad()
        loss_fn().backward()
        with torch.no_grad():
            for p in params:
                p -= eta * p.grad
    return np.array(curve)


# ---------------------------------------------------------------------------
# The natural gradient and K-FAC, on the spirals
# ---------------------------------------------------------------------------
NG_HID = 24
NG_SNAP = (0, 10, 30, 100, 300)


def ng_data():
    from videos.ai.ai9.compute import spirals

    return spirals(n=200, seed=3)


def ng_run(opt: str, lr: float, steps: int = 300, seed: int = 0, damping: float = 1e-3, snaps=()):
    """Full-batch training of a 2-24-24-2 tanh network on the spirals (cross-entropy), by gradient descent
    (``gd``), Adam (``adam``), the exact natural gradient (``ng``: the Fisher of the model's own predictions, all
    722 x 722 of it, damped) or K-FAC (``kfac``: each layer's Fisher block as a Kronecker product of its inputs'
    and its output gradients' second moments, the gradients for labels sampled from the model). Returns the training
    loss and accuracy per step, and the predicted probability of class 1 on a grid at ``snaps``."""
    import torch

    X, y = ng_data()
    Xt, yt = torch.tensor(X, dtype=torch.float64), torch.tensor(y)
    n = len(yt)
    torch.manual_seed(seed)
    layers = [torch.nn.Linear(2, NG_HID), torch.nn.Linear(NG_HID, NG_HID), torch.nn.Linear(NG_HID, 2)]
    for L in layers:
        L.double()
    params = [p for L in layers for p in (L.weight, L.bias)]
    P = sum(p.numel() for p in params)
    gs = np.linspace(-3.6, 3.6, 41)
    grid = torch.tensor(np.stack(np.meshgrid(gs, gs), -1).reshape(-1, 2), dtype=torch.float64)

    def forward(x, keep=False):
        acts, pre = [], []
        h = x
        for i, L in enumerate(layers):
            acts.append(h)
            s = L(h)
            if keep:
                s.retain_grad()
            pre.append(s)
            h = torch.tanh(s) if i < len(layers) - 1 else s
        return h, acts, pre

    adam_m = [torch.zeros_like(p) for p in params]
    adam_v = [torch.zeros_like(p) for p in params]
    gen = torch.Generator().manual_seed(seed + 7)
    curve, snap = [], {}
    for t in range(steps + 1):
        logits, acts, pre = forward(Xt)
        loss = torch.nn.functional.cross_entropy(logits, yt)
        acc = float((logits.argmax(1) == yt).double().mean())
        curve.append((t, loss.item(), acc))
        if t in snaps:
            with torch.no_grad():
                snap[str(t)] = torch.softmax(forward(grid)[0], -1)[:, 1].numpy().astype(np.float32).tolist()
        if t == steps or not math.isfinite(loss.item()):
            break
        grads = torch.autograd.grad(loss, params, retain_graph=opt in ("ng", "kfac"))
        with torch.no_grad():
            if opt == "gd":
                upd = list(grads)
            elif opt == "adam":
                upd = []
                for i, g in enumerate(grads):
                    adam_m[i].mul_(0.9).add_(g, alpha=0.1)
                    adam_v[i].mul_(0.999).addcmul_(g, g, value=0.001)
                    upd.append((adam_m[i] / (1 - 0.9 ** (t + 1))) / ((adam_v[i] / (1 - 0.999 ** (t + 1))).sqrt() + 1e-8))
            elif opt == "ng":
                pass
        if opt == "ng":
            # F = (1/n) sum_i J_i^T (diag p_i - p_i p_i^T) J_i; for two classes = (1/n) sum_i p0 p1 d_i d_i^T, d = J0 - J1
            p_ = torch.softmax(logits, -1).detach()
            diff = logits[:, 0] - logits[:, 1]
            # row i: the gradient of example i's logit gap. diff_i depends on example i alone, so one backward
            # pass gives each layer's d diff_i / d s_i, and the weight gradient is its outer product with the input
            dpre = torch.autograd.grad(diff.sum(), pre, retain_graph=True)
            cols = []
            for a, dp in zip(acts, dpre):
                cols += [(dp[:, :, None] * a.detach()[:, None, :]).reshape(n, -1), dp]
            D = torch.cat(cols, 1) * (p_[:, 0] * p_[:, 1]).sqrt()[:, None]
            gvec = torch.cat([g.reshape(-1) for g in grads])
            K_ = D @ D.T / n  # F = D^T D / n has the same nonzero eigenvalues as this n x n matrix
            lam = damping * float(torch.linalg.eigvalsh(K_).max())
            # (D^T D / n + lam I)^-1 g, by Woodbury: (g - D^T (n lam I + D D^T)^-1 D g) / lam
            nat = (gvec - D.T @ torch.linalg.solve(n * lam * torch.eye(n, dtype=D.dtype) + D @ D.T, D @ gvec)) / lam
            upd, k = [], 0
            for p in params:
                upd.append(nat[k:k + p.numel()].reshape(p.shape))
                k += p.numel()
        elif opt == "kfac":
            # gradients for labels drawn from the model: the true Fisher's factors
            ys = torch.multinomial(torch.softmax(logits.detach(), -1), 1, generator=gen)[:, 0]
            sl = torch.nn.functional.cross_entropy(logits, ys, reduction="sum")
            gpre = torch.autograd.grad(sl, pre)
            upd = []
            with torch.no_grad():
                for L, a, gp, (gw, gb) in zip(layers, acts, gpre, zip(grads[0::2], grads[1::2])):
                    a1 = torch.cat([a, torch.ones(n, 1, dtype=a.dtype)], 1)
                    A = a1.T @ a1 / n
                    G = gp.T @ gp / n
                    dA = math.sqrt(damping * float(torch.linalg.eigvalsh(A).max()))
                    dG = math.sqrt(damping * float(torch.linalg.eigvalsh(G).max()))
                    Wg = torch.cat([gw, gb[:, None]], 1)
                    U = torch.linalg.solve(G + dG * torch.eye(len(G), dtype=G.dtype), Wg)
                    U = torch.linalg.solve(A + dA * torch.eye(len(A), dtype=A.dtype), U.T).T
                    upd += [U[:, :-1], U[:, -1]]
        with torch.no_grad():
            for p, u in zip(params, upd):
                p -= lr * u
    return dict(curve=curve, snaps=snap, P=P)


# ---------------------------------------------------------------------------
# A one-layer attention model, for QK-clip
# ---------------------------------------------------------------------------
QT, QD, QH = 32, 64, 2  # context, width, heads


def qk_run(lr: float, clip_tau: float | None, steps: int = 2000, seed: int = 0, every: int = 10, opt_name: str = "muon",
           gclip: float | None = None):
    """A one-layer, two-head transformer on Part 1's books (32 characters of context, width 64, pre-norm, no
    normalization of queries or keys), its matrices trained by Muon (as in charopt) and the rest by AdamW, or
    (``opt_name="adam"``) all of it by AdamW at ``lr``; ``gclip``: the gradient's norm clipped to that. Every step
    the largest attention score of each head is measured; with ``clip_tau``, QK-clip (Kimi K2): a head whose largest
    score exceeds tau has its query and key weights each multiplied by sqrt(tau / score). Returns the training loss
    and the largest score per ``every`` steps, and the held-out bits at the end."""
    import torch

    from .charopt import newton_schulz, tensors

    tr, va, K = tensors()
    dh = QD // QH
    torch.manual_seed(seed)
    m = torch.nn.ModuleDict(dict(
        emb=torch.nn.Embedding(K, QD), pos=torch.nn.Embedding(QT, QD), q=torch.nn.Linear(QD, QD, bias=False),
        k=torch.nn.Linear(QD, QD, bias=False), v=torch.nn.Linear(QD, QD, bias=False), o=torch.nn.Linear(QD, QD, bias=False),
        f1=torch.nn.Linear(QD, 4 * QD), f2=torch.nn.Linear(4 * QD, QD), ln1=torch.nn.LayerNorm(QD),
        ln2=torch.nn.LayerNorm(QD), ln3=torch.nn.LayerNorm(QD), out=torch.nn.Linear(QD, K)))
    mask = torch.triu(torch.ones(QT, QT, dtype=torch.bool), 1)

    def fwd(x):
        B = x.shape[0]
        h = m["emb"](x) + m["pos"].weight[None]
        a = m["ln1"](h)
        q = m["q"](a).view(B, QT, QH, dh).transpose(1, 2)
        k = m["k"](a).view(B, QT, QH, dh).transpose(1, 2)
        v = m["v"](a).view(B, QT, QH, dh).transpose(1, 2)
        s = q @ k.transpose(-1, -2) / math.sqrt(dh)
        smax = s.detach().masked_fill(mask, -1e9).amax(dim=(0, 2, 3))
        s = s.masked_fill(mask, float("-inf"))
        h = h + m["o"]((torch.softmax(s, -1) @ v).transpose(1, 2).reshape(B, QT, QD))
        h = h + m["f2"](torch.relu(m["f1"](m["ln2"](h))))
        return m["out"](m["ln3"](h)), smax

    mats = [m[n].weight for n in ("q", "k", "v", "o", "f1", "f2")]
    rest = [p for p in m.parameters() if all(p is not q for q in mats)]
    if opt_name == "muon":
        opt = torch.optim.AdamW(rest, lr=3e-3, betas=(0.9, 0.95), weight_decay=0.0)
    else:
        opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.0)
    mom = [torch.zeros_like(p) for p in mats]
    g = rng(seed + 1)
    ar = torch.arange(QT)
    log, clipped = [], 0
    for s_ in range(1, steps + 1):
        pos = torch.from_numpy(g.integers(0, len(tr) - QT - 1, 32))
        x, yy = tr[pos[:, None] + ar], tr[pos[:, None] + ar + 1]
        lg, smax = fwd(x)
        loss = torch.nn.functional.cross_entropy(lg.reshape(-1, K), yy.reshape(-1))
        if not torch.isfinite(loss):
            log.append((s_, float("nan"), float("nan")))
            break
        opt.zero_grad()
        for p in mats:
            p.grad = None
        loss.backward()
        if gclip:
            torch.nn.utils.clip_grad_norm_(m.parameters(), gclip)
        with torch.no_grad():
            for p, b in zip(mats if opt_name == "muon" else [], mom):
                b.mul_(0.95).add_(p.grad)
                p.add_(newton_schulz(p.grad + 0.95 * b), alpha=-lr * 0.2 * math.sqrt(max(p.shape)))
        opt.step()
        if clip_tau is not None:
            with torch.no_grad():
                for hh in range(QH):
                    if float(smax[hh]) > clip_tau:
                        gam = math.sqrt(clip_tau / float(smax[hh]))
                        m["q"].weight[hh * dh:(hh + 1) * dh] *= gam
                        m["k"].weight[hh * dh:(hh + 1) * dh] *= gam
                        clipped += 1
        if s_ % every == 0:
            log.append((s_, float(loss), float(smax.max())))
    with torch.no_grad():  # held-out bits on 200 windows of 32
        P_ = torch.arange(0, 200 * QT * 4, QT * 4)
        lg, _ = fwd(va[P_[:, None] + ar])
        held = float(torch.nn.functional.cross_entropy(lg.reshape(-1, K), va[P_[:, None] + ar + 1].reshape(-1))) / math.log(2)
    return dict(log=log, held=held, clipped=clipped)
