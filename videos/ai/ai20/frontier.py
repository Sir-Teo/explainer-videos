"""Sparse autoencoders, then and now (the ``frontier`` item of Part 20).

    frontier   the SAE item's activations (block 2's residual stream of Part 11's transformer) taken apart again by
               sparse autoencoders trained two ways: with an L1 penalty at four strengths (Bricken et al., 2023) and
               with TopK, keeping exactly k features per vector (Gao et al., 2024), k = 4 to 32; for each, how many
               features fire per vector, the variance left unexplained, the dead features, and how much the
               reconstruction shrinks (the L1 penalty pulls every activation toward zero; TopK doesn't)
"""

from __future__ import annotations

import math

import numpy as np

F_, STEPS = 512, 3000
L1S = [1e-3, 3e-3, 1e-2, 3e-2]
KS = [4, 8, 16, 32]


def train_sae(X, kind, param, seed=0):
    import torch

    D = X.shape[1]
    torch.manual_seed(seed)
    Wd = torch.nn.Parameter(torch.randn(F_, D) / math.sqrt(D))
    We = torch.nn.Parameter(Wd.detach().clone().T)
    be = torch.nn.Parameter(torch.zeros(F_))
    bd = torch.nn.Parameter(torch.zeros(D))
    opt = torch.optim.Adam([Wd, We, be, bd], lr=1e-3)
    g = torch.Generator().manual_seed(seed)

    def encode(x):
        z = x @ We + be
        if kind == "l1":
            return torch.relu(z)
        v, i = torch.topk(z, int(param), dim=1)  # keep the k largest, zero the rest
        return torch.zeros_like(z).scatter(1, i, torch.relu(v))

    for _ in range(STEPS):
        x = X[torch.randint(0, len(X), (1024,), generator=g)]
        f = encode(x)
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        xh = f @ dec + bd
        loss = ((xh - x) ** 2).sum(1).mean()
        if kind == "l1":
            loss = loss + param * f.sum(1).mean() * D
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        f = encode(X)
        xh = f @ dec + bd
        l0 = float((f > 0).float().sum(1).mean())
        fvu = float(((xh - X) ** 2).sum(1).mean() / ((X - X.mean(0)) ** 2).sum(1).mean())
        dead = int(((f > 0).float().sum(0) == 0).sum())
        # shrinkage: the best single factor to scale the reconstruction by (1 = no shrinkage)
        xc, hc = X - bd, xh - bd
        shrink = float((hc * xc).sum() / (hc * hc).sum())
    return dict(l0=l0, fvu=fvu, dead=dead, shrink=shrink)


def compute_frontier():
    import torch

    from videos.ai.ai11 import compute as c11
    from videos.ai.ai20.compute import residuals, rng

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    g = rng(2023)  # the same windows as the SAE item
    starts = g.integers(0, len(va) - c11.CTX - 1, 1100)
    A = residuals(model, va, 1, starts, c11)
    mu = A.mean(0)
    X = (A - mu) / (A - mu).norm(dim=1).mean()
    out = dict(F=F_, steps=STEPS, l1s=L1S, ks=KS)
    for kind, params in (("l1", L1S), ("topk", KS)):
        for p in params:
            r = train_sae(X, kind, p)
            for k, v in r.items():
                out[f"{kind}_{p:g}_{k}"] = v
            print(f"    {kind} {p:g}: {r['l0']:.1f} active, unexplained {r['fvu']:.3f}, {r['dead']} dead, "
                  f"best rescale {r['shrink']:.2f}", flush=True)
    assert out[f"topk_{KS[-1]:g}_fvu"] < out[f"topk_{KS[0]:g}_fvu"]
    return out
