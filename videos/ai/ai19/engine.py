"""A small inference engine for the series' novels model (``explainer.lm.pocket.PocketGPT``), the way a server runs it:
a key-value cache, a prefill of the whole prompt in one pass, then one decode step per token for a batch of
sequences.  It does the model's own arithmetic (its layers are called directly), and ``check`` confirms that a prefill
followed by decode steps gives the logits of the model's full forward pass.

Hooks for the experiments of Part 19:
    ``kv_quant``   a function applied to each new key and value before it is written to the cache (KV quantization)
    ``act_quant``  a function applied to the input of every linear layer (activation quantization)

Also here: timing that copes with a shared machine (``interleaved_min``: every configuration timed in turn, in a
shuffled order, many rounds, keeping the fastest of each), and the novels data helpers the compute items share.
"""

from __future__ import annotations

import math
import time

import numpy as np


# ---------------------------------------------------------------------------
# Timing on a busy machine
# ---------------------------------------------------------------------------
def interleaved_min(configs, fn, rounds=7, min_time=0.03, seed=0, setup=None):
    """Time ``fn(c)`` for every configuration ``c``: ``rounds`` rounds, each visiting every configuration once in a
    shuffled order; within a visit ``fn`` is repeated until ``min_time`` seconds pass.  Other jobs only ever slow a
    measurement down, so the fastest round of each configuration is the best estimate of its cost (and the median is
    kept to show the noise).  Returns {c: (min seconds per call, median seconds per call)}."""
    g = np.random.default_rng(seed)
    reps = {}
    for c in configs:  # warm up, and choose how many calls make one visit
        if setup:
            setup(c)
        fn(c)
        t = time.perf_counter()
        fn(c)
        one = max(time.perf_counter() - t, 1e-6)
        reps[c] = max(1, int(math.ceil(min_time / one)))
    times = {c: [] for c in configs}
    for _ in range(rounds):
        for i in g.permutation(len(configs)):
            c = configs[i]
            if setup:
                setup(c)
            t = time.perf_counter()
            for _ in range(reps[c]):
                fn(c)
            times[c].append((time.perf_counter() - t) / reps[c])
    return {c: (float(np.min(v)), float(np.median(v))) for c, v in times.items()}


def loadavg() -> list[float]:
    import os

    try:
        return [round(x, 2) for x in os.getloadavg()]
    except (OSError, AttributeError):
        return []


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------
class Cache:
    """Keys and values of every layer, preallocated for ``T`` positions: ``k[l]``, ``v[l]`` of shape (B, H, T, dh)."""

    def __init__(self, layers, B, H, T, dh, dtype=None):
        import torch

        dtype = dtype or torch.float32
        self.k = [torch.zeros(B, H, T, dh, dtype=dtype) for _ in range(layers)]
        self.v = [torch.zeros(B, H, T, dh, dtype=dtype) for _ in range(layers)]
        self.len = 0

    def nbytes(self, upto=None) -> int:
        n = self.len if upto is None else upto
        return int(sum(2 * t.shape[0] * t.shape[1] * n * t.shape[3] * t.element_size() for t in self.k))


class Engine:
    """Runs a PocketGPT with a KV cache.  ``forward(ids, cache)`` processes the new tokens ``ids`` (B, T) at positions
    cache.len ... cache.len + T - 1 of every row, writes their keys and values, and returns the logits (B, T, V)."""

    def __init__(self, model, max_len: int | None = None, kv_quant=None, act_quant=None):
        import torch

        self.m = model.eval()
        cfg = model.cfg
        self.L, self.H, self.d = cfg.layers, cfg.heads, cfg.d
        self.dh = cfg.d // cfg.heads
        self.max_len = max_len or cfg.seq
        inv = 1.0 / 10_000.0 ** (torch.arange(0, self.dh, 2).float() / self.dh)
        ang = torch.outer(torch.arange(self.max_len).float(), inv)
        self.cos, self.sin = ang.cos(), ang.sin()
        self.kv_quant, self.act_quant = kv_quant, act_quant
        self.window = 0  # > 0: a decode step attends only to the last `window` positions (a sliding window)

    def new_cache(self, B: int, T: int | None = None, dtype=None, fill: bool = False) -> Cache:
        """``fill``: random contents, so that timing reads real memory (untouched pages can all map to one)."""
        c = Cache(self.L, B, self.H, T or self.max_len, self.dh, dtype)
        if fill:
            for t in c.k + c.v:
                t.normal_()
        return c

    def rope(self, x, p0):
        import torch

        T = x.shape[-2]
        c, s = self.cos[p0:p0 + T], self.sin[p0:p0 + T]
        x1, x2 = x[..., ::2], x[..., 1::2]
        return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1).flatten(-2)

    def lin(self, layer, x):
        return layer(self.act_quant(x) if self.act_quant else x)

    def forward(self, ids, cache: Cache, logits: str = "all"):
        """``logits``: "all" (B, T, V), "last" (B, V), or "none" (the final hidden states, (B, T, d), before the norm)."""
        import torch
        import torch.nn.functional as F

        m = self.m
        B, T = ids.shape
        p0 = cache.len
        x = m.emb(ids)
        mask = None
        if T > 1:
            mask = (torch.arange(T)[:, None] + p0) >= torch.arange(p0 + T)[None, :]
        for l, blk in enumerate(m.blocks):
            a = blk.attn
            h = blk.n1(x)
            q, k, v = self.lin(a.qkv, h).view(B, T, 3, self.H, self.dh).permute(2, 0, 3, 1, 4)
            q, k = self.rope(q, p0), self.rope(k, p0)
            if self.kv_quant:
                k, v = self.kv_quant(k, "k", l), self.kv_quant(v, "v", l)
            cache.k[l][:, :, p0:p0 + T] = k
            cache.v[l][:, :, p0:p0 + T] = v
            lo = max(0, p0 + T - self.window) if (self.window and T == 1) else 0
            K, V = cache.k[l][:, :, lo:p0 + T], cache.v[l][:, :, lo:p0 + T]
            y = F.scaled_dot_product_attention(q, K, V, attn_mask=mask)
            x = x + self.lin(a.out, y.transpose(1, 2).reshape(B, T, self.d))
            h = blk.n2(x)
            mlp = blk.mlp
            x = x + self.lin(mlp.down, F.silu(self.lin(mlp.gate, h)) * self.lin(mlp.up, h))
        cache.len = p0 + T
        if logits == "none":
            return x
        if logits == "last":
            x = x[:, -1]
        return m.head(m.norm(x))

    def full(self, ids):
        """Logits for a whole sequence in one pass (teacher forcing), through a fresh cache."""
        c = self.new_cache(ids.shape[0], ids.shape[1])
        return self.forward(ids, c)


def check(model, ids, n_decode=8) -> float:
    """Largest difference between the model's own logits and the engine's (prefill, then one token at a time)."""
    import torch

    with torch.inference_mode():
        ref = model(ids)
        eng = Engine(model)
        c = eng.new_cache(ids.shape[0], ids.shape[1])
        T0 = ids.shape[1] - n_decode
        outs = [eng.forward(ids[:, :T0], c)]
        for t in range(T0, ids.shape[1]):
            outs.append(eng.forward(ids[:, t:t + 1], c))
        got = torch.cat(outs, 1)
    return float((got - ref).abs().max())


# ---------------------------------------------------------------------------
# Data: held-out windows of the novels, and the loss on them
# ---------------------------------------------------------------------------
def heldout(n=48, T=256, seed=0):
    """``n`` windows of ``T + 1`` tokens from the held-out novels text, evenly spread (the same ones every time)."""
    import torch

    from explainer.ai import novels as N

    _, va = N.token_arrays()
    starts = np.linspace(0, len(va) - T - 2, n).astype(int)
    return torch.from_numpy(np.stack([va[s:s + T + 1] for s in starts]).astype(np.int64))


def calibration(n=32, T=256, seed=1):
    """``n`` random windows of the training text: the data a quantizer may look at."""
    import torch

    from explainer.ai import novels as N

    tr, _ = N.token_arrays()
    g = np.random.default_rng(seed)
    starts = g.integers(0, len(tr) - T - 2, n)
    return torch.from_numpy(np.stack([tr[s:s + T + 1] for s in starts]).astype(np.int64))


def loss(model_or_engine, windows, batch=16) -> float:
    """Mean cross-entropy (nats per token) on the windows, every position scored."""
    import torch
    import torch.nn.functional as F

    eng = model_or_engine if isinstance(model_or_engine, Engine) else None
    tot, n = 0.0, 0
    with torch.inference_mode():
        for i in range(0, len(windows), batch):
            w = windows[i:i + batch]
            x, y = w[:, :-1], w[:, 1:]
            z = eng.full(x) if eng else model_or_engine(x)
            tot += float(F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1), reduction="sum"))
            n += y.numel()
    return tot / n
