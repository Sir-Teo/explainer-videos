"""A minimal GPT (decoder-only transformer) trained on characters.

Same blueprint as GPT-2, just tiny: token + learned position embeddings,
pre-norm blocks of causal multi-head attention and a GELU MLP, tied
unembedding.  Trained from scratch on CPU in a few minutes so the video can
show real samples and a real loss curve as a model learns.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, d, n_head, ctx):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d)
        self.proj = nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        self.n_head = n_head
        self.register_buffer("mask", torch.tril(torch.ones(ctx, ctx, dtype=torch.bool)))

    def attn(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=2)
        q, k, v = (t.view(B, T, self.n_head, D // self.n_head).transpose(1, 2) for t in (q, k, v))
        att = (q @ k.transpose(-2, -1)) / math.sqrt(D // self.n_head)
        att = att.masked_fill(~self.mask[:T, :T], float("-inf")).softmax(-1)
        return self.proj((att @ v).transpose(1, 2).reshape(B, T, D))

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.mlp(self.ln2(x))


class TinyGPT(nn.Module):
    def __init__(self, vocab, d=128, n_layer=4, n_head=4, ctx=128):
        super().__init__()
        self.ctx = ctx
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(ctx, d)
        self.blocks = nn.ModuleList(Block(d, n_head, ctx) for _ in range(n_layer))
        self.ln_f = nn.LayerNorm(d)
        self.apply(self._init)

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
        if isinstance(m, nn.Linear) and m.bias is not None:
            nn.init.zeros_(m.bias)

    def forward(self, idx):
        T = idx.shape[1]
        x = self.tok(idx) + self.pos(torch.arange(T))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T  # tied unembedding

    @torch.no_grad()
    def sample(self, prompt_ids, n, temperature=0.8, seed=0):
        g = torch.Generator().manual_seed(seed)
        idx = torch.tensor([prompt_ids])
        for _ in range(n):
            logits = self(idx[:, -self.ctx :])[0, -1] / temperature
            nxt = torch.multinomial(logits.softmax(-1), 1, generator=g)
            idx = torch.cat([idx, nxt[None]], dim=1)
        return idx[0].tolist()


def train(text, steps=3000, batch=32, lr=2e-3, sample_at=(0, 100, 300, 1000, 3000), sample_len=240,
          prompt="\n", seed=1337, log=print, **model_kw):
    """Train on ``text``; return the loss curve and samples taken along the way."""
    torch.manual_seed(seed)
    chars = sorted(set(text))
    stoi = {c: i for i, c in enumerate(chars)}
    data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
    split = int(0.9 * len(data))
    train_data, val_data = data[:split], data[split:]
    model = TinyGPT(len(chars), **model_kw)
    ctx = model.ctx
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.99), weight_decay=0.1)
    warm = 100

    def lr_at(s):
        if s < warm:
            return lr * (s + 1) / warm
        return 0.1 * lr + 0.9 * lr * 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, steps - warm)))

    def get_batch(d, gen):
        ix = torch.randint(len(d) - ctx - 1, (batch,), generator=gen)
        x = torch.stack([d[i : i + ctx] for i in ix])
        y = torch.stack([d[i + 1 : i + ctx + 1] for i in ix])
        return x, y

    @torch.no_grad()
    def val_loss(n=20):
        gen = torch.Generator().manual_seed(0)
        losses = []
        for _ in range(n):
            x, y = get_batch(val_data, gen)
            losses.append(F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item())
        return float(np.mean(losses))

    gen = torch.Generator().manual_seed(seed)
    curve, val_curve, samples = [], [], {}
    prompt_ids = [stoi[c] for c in prompt]
    t0 = time.time()
    for step in range(steps + 1):
        if step in sample_at:
            model.eval()
            out = model.sample(prompt_ids, sample_len, seed=seed)
            samples[step] = "".join(chars[i] for i in out[len(prompt_ids):])
            val_curve.append((step, val_loss()))
            log(f"step {step:5d}  val {val_curve[-1][1]:.3f}  ({time.time() - t0:.0f}s)\n{samples[step][:160]!r}")
            model.train()
        elif step % 100 == 0:
            model.eval()
            val_curve.append((step, val_loss(8)))
            model.train()
        if step == steps:
            break
        for group in opt.param_groups:
            group["lr"] = lr_at(step)
        x, y = get_batch(train_data, gen)
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        curve.append(loss.item())
    n_params = sum(p.numel() for p in model.parameters())
    return {
        "chars": "".join(chars),
        "n_params": n_params,
        "train_loss": curve,
        "val_loss": val_curve,
        "samples": {str(k): v for k, v in samples.items()},
        "uniform_loss": math.log(len(chars)),
        "config": dict(steps=steps, batch=batch, lr=lr, **model_kw),
    }
