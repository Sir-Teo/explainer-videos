"""Pruning our trained dense transformer: 2:4 structured sparsity (two of every four consecutive weights feeding an
output kept, as NVIDIA's sparse tensor cores need), chosen by magnitude or by Wanda's |W| x ||x|| score (Sun et al.
2023), against unstructured 50% magnitude pruning and random 2:4; then a short retraining with the mask held.  And
activation sparsity: how many of the feed-forward layer's activations are near zero, and what skipping them costs."""

from __future__ import annotations

import math

import numpy as np

FT_STEPS, FT_LR = 300, 1e-3


def linears(model):
    """The weight matrices a token multiplies through in the blocks (attention's and the feed-forward layer's)."""
    out = []
    for i, b in enumerate(model.blocks):
        out += [(f"b{i}.qkv", b.attn.qkv), (f"b{i}.o", b.attn.o), (f"b{i}.w1", b.ffn.w1), (f"b{i}.w2", b.ffn.w2)]
    return out


def input_norms(model, x):
    """The norm of each input feature of each linear layer over a calibration batch (Wanda's ||X_j||)."""
    import torch

    norms, hooks = {}, []
    for name, L in linears(model):
        def hook(mod, inp, out_, name=name):
            a = inp[0].reshape(-1, inp[0].shape[-1])
            norms[name] = norms.get(name, 0) + (a ** 2).sum(0)
        hooks.append(L.register_forward_hook(hook))
    model.eval()
    with torch.no_grad():
        model(x)
    for h in hooks:
        h.remove()
    return {k: v.sqrt() for k, v in norms.items()}


def mask_nm(score, n=2, m=4):
    """Keep the ``n`` highest scores in every group of ``m`` consecutive inputs of each output row."""
    import torch

    out_f, in_f = score.shape
    s = score.reshape(out_f, in_f // m, m)
    idx = s.topk(n, -1).indices
    mk = torch.zeros_like(s).scatter_(-1, idx, 1.0)
    return mk.reshape(out_f, in_f)


def mask_unstructured(score, frac=0.5):
    import torch

    thr = torch.kthvalue(score.reshape(-1), int(frac * score.numel())).values
    return (score > thr).float()


def masks(model, method, norms=None, seed=0):
    import torch

    g = torch.Generator().manual_seed(seed)
    out = {}
    for name, L in linears(model):
        W = L.weight.detach()
        if method == "magnitude_24":
            out[name] = mask_nm(W.abs())
        elif method == "wanda_24":
            out[name] = mask_nm(W.abs() * norms[name][None, :])
        elif method == "unstructured":
            out[name] = mask_unstructured(W.abs())
        elif method == "random_24":
            out[name] = mask_nm(torch.rand(W.shape, generator=g))
        else:
            raise ValueError(method)
    return out


def apply(model, mk):
    import torch

    with torch.no_grad():
        for name, L in linears(model):
            L.weight.mul_(mk[name])


def finetune(model, mk, seed, steps=FT_STEPS):
    """A short retraining with the mask held (the weights pruned stay zero): the recipe NVIDIA's ASP uses."""
    import torch
    import torch.nn.functional as F

    from videos.ai.ai16 import runs as R

    tr, va, K, _, _ = R.lm_data()
    T = model.c.ctx
    opt = torch.optim.AdamW(model.parameters(), lr=FT_LR, betas=(0.9, 0.95), weight_decay=0.0)
    g = np.random.default_rng(4000 + seed)
    model.train()
    curve = []
    for step in range(steps):
        f = min(1.0, (step + 1) / 30) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / steps)))
        for gr in opt.param_groups:
            gr["lr"] = FT_LR * f
        x, y = R.windows(tr, g.integers(0, len(tr) - T - 2, R.BATCH), T)
        loss = F.cross_entropy(model(x).reshape(-1, K), y.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        apply(model, mk)
        if step % 50 == 0 or step == steps - 1:
            curve.append((step + 1, R.lm_bits(model, va, T, 64)))
    return curve


def gelu_acts(model, x):
    """Every feed-forward activation (after GELU) of every block on a batch: one array per block."""
    import torch

    model.eval()
    with torch.no_grad():
        model(x, probe=True)
    return [b.ffn.acts.reshape(-1, b.ffn.acts.shape[-1]).numpy() for b in model.blocks]


def sparsify_bits(model, va, T, frac, thr_by_block):
    """Held-out bits when each block's feed-forward activations smaller in size than its threshold are set to zero
    (TEAL-style magnitude thresholds, chosen on a calibration batch to hit ``frac``)."""
    import torch

    from videos.ai.ai16 import runs as R

    for b, thr in zip(model.blocks, thr_by_block):
        b.ffn.sparsify = (lambda a, t=thr: a * (a.abs() >= t)) if frac > 0 else None
    out = R.lm_bits(model, va, T, 200)
    for b in model.blocks:
        b.ffn.sparsify = None
    return out
