"""Reading activations out of the series' two transformers (Part 13's character model and the novels model).

Every function takes the model as its owner's ``load`` gives it (``videos.ai.ai13.compute.load_tf``,
``explainer.ai.novels.load_base``) and runs it layer by layer, so the scenes' numbers come from the real forward pass.
"""

from __future__ import annotations

import numpy as np


def threads(n: int = 1) -> None:
    """Torch threads for this process (called inside compute items, never at import)."""
    import torch

    torch.set_num_threads(n)


# ---------------------------------------------------------------------------
# Part 13's character transformer
# ---------------------------------------------------------------------------
def tf_rope(c13, T):
    import torch

    th = torch.tensor(c13.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    return torch.cos(ang), torch.sin(ang)


def tf_layers(model, x, c13, keep_attn=False):
    """One forward pass of the character transformer on ids ``x`` (B, T), recording for every block the residual
    stream before it (``pre``), after its attention (``mid``), its MLP's input after the layer norm (``mlp_in``), the
    MLP's output (``mlp_out``) and, if asked, each head's output written to the residual (``heads``, B, H, T, D) and
    attention pattern (``attn``).  Returns the per-block records and the logits."""
    import torch
    import torch.nn.functional as F

    cos, sin = tf_rope(c13, x.shape[1])
    h = model.emb(x)
    recs = []
    for b in model.blocks:
        r = {"pre": h}
        a, p, _ = b.attend(h, cos, sin, 1.0, True if keep_attn else None)
        B, H, T, dh = a.shape
        if keep_attn:
            W = b.o.weight  # (D, D): the heads' outputs, each through its slice of W_O
            r["heads"] = torch.einsum("bhtd,ehd->bhte", a, W.view(W.shape[0], H, dh))
            r["attn"] = p
        h = h + b.o(a.transpose(1, 2).reshape(h.shape))
        r["mid"] = h
        u = b.n2(h)
        r["mlp_in"] = u
        m = b.f2(F.gelu(b.f1(u)))
        r["mlp_out"] = m
        h = h + m
        r["post"] = h
        recs.append(r)
    return recs, model.out(model.nf(h))


def tf_windows(c13, data, n, seed, ctx=None):
    """``n`` windows of held-out text (starts drawn with ``seed``), as ids (n, ctx)."""
    import torch

    va = data["valid"]
    ctx = ctx or c13.CTX
    starts = np.random.Generator(np.random.PCG64(seed)).integers(0, len(va) - ctx - 1, n)
    return starts, torch.stack([va[s:s + ctx] for s in starts])


def tf_collect(model, c13, X, keys=("post",), layers=(1,), skip=64, batch=16, dtype=None):
    """Concatenate the recorded vectors ``keys`` of blocks ``layers`` over windows ``X`` (positions ``skip`` on, which
    have enough context): {(key, layer): (N, D)}."""
    import torch

    out = {(k, l_): [] for k in keys for l_ in layers}
    with torch.no_grad():
        for i in range(0, len(X), batch):
            recs, _ = tf_layers(model, X[i:i + batch], c13)
            for k in keys:
                for l_ in layers:
                    v = recs[l_][k][:, skip:].reshape(-1, recs[l_][k].shape[-1])
                    out[(k, l_)].append(v.to(dtype) if dtype is not None else v)
    return {k: torch.cat(v) for k, v in out.items()}


def tf_bits_with(model, c13, X, layer, fn, skip=64, batch=16):
    """Bits per character on windows ``X`` (positions ``skip`` on) when the residual stream after block ``layer`` is
    replaced by ``fn(h)`` (``fn=None``: the model as it is)."""
    import math

    import torch
    import torch.nn.functional as F

    cos, sin = tf_rope(c13, X.shape[1] - 1)
    tot, n = 0.0, 0
    with torch.no_grad():
        for i in range(0, len(X), batch):
            x = X[i:i + batch, :-1]
            y = X[i:i + batch, 1:]
            h = model.emb(x)
            for li, b in enumerate(model.blocks):
                h, _, _ = b(h, cos, sin)
                if li == layer and fn is not None:
                    sh = h.shape
                    h = fn(h.reshape(-1, sh[-1])).reshape(sh)
            z = model.out(model.nf(h))
            ce = F.cross_entropy(z[:, skip:].reshape(-1, z.shape[-1]), y[:, skip:].reshape(-1), reduction="sum")
            tot += float(ce)
            n += y[:, skip:].numel()
    return tot / n / math.log(2)


# ---------------------------------------------------------------------------
# The novels model (explainer.lm.pocket.PocketGPT)
# ---------------------------------------------------------------------------
def nov_resid(model, ids, layers=None):
    """The residual stream of the novels model on ids (B, T): a list with the embedding (index 0) and the output of
    every block (1 ... L), and the logits."""
    import torch

    with torch.no_grad():
        h = model.emb(ids)
        out = [h]
        for b in model.blocks:
            h = b(h)
            out.append(h)
        z = model.head(model.norm(h))
    return out, z


def nov_run_from(model, h, start):
    """Run the novels model from the residual ``h`` entering block ``start`` to the logits (with gradients)."""
    for b in model.blocks[start:]:
        h = b(h)
    return model.head(model.norm(h))


def nov_windows(valid, n, T, seed):
    """``n`` windows of the novels model's held-out tokens (int64 tensor (n, T))."""
    import torch

    g = np.random.Generator(np.random.PCG64(seed))
    starts = g.integers(0, len(valid) - T - 1, n)
    return starts, torch.tensor(np.stack([valid[s:s + T] for s in starts]).astype(np.int64))


def token_strings(ids) -> list[str]:
    from explainer.ai import novels as N

    tok = N.tokenizer()
    return [tok.decode([int(i)]) for i in ids]
