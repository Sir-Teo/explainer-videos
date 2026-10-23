"""Post-training machinery for Part 27, on the series' novels model (``explainer.ai.novels``).

Chat format: ``<|user|>question<|assistant|>answer<|end|>``.  Only the answer's tokens (and its <|end|>) are trained
on; the question is context.  Batches are right-padded: in a causal model, padding after a sequence cannot change
anything before it, and padded positions are masked out of every loss.
"""

from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from explainer.ai import novels as N

PAD = 0  # <|endoftext|>: never trained on as an answer token here


def chat(question: str, answer: str | None = None) -> list[int]:
    """Token ids of one exchange; with ``answer=None``, the prompt that asks the model to answer."""
    ids = [N.special("<|user|>")] + N.encode(question) + [N.special("<|assistant|>")]
    if answer is not None:
        ids += N.encode(answer) + [N.special("<|end|>")]
    return ids


def pack(examples: list[tuple[list[int], list[int]]], seq: int = 256):
    """(prompt ids, answer ids) pairs -> padded input, targets and a mask over the answer's targets."""
    rows = [(p + a)[:seq + 1] for p, a in examples]
    T = max(len(r) for r in rows) - 1
    x = torch.full((len(rows), T), PAD, dtype=torch.long)
    y = torch.full((len(rows), T), PAD, dtype=torch.long)
    m = torch.zeros((len(rows), T))
    for i, ((p, a), r) in enumerate(zip(examples, rows)):
        n = len(r) - 1
        x[i, :n] = torch.tensor(r[:-1])
        y[i, :n] = torch.tensor(r[1:])
        m[i, len(p) - 1:n] = 1.0  # targets from the first answer token on
    return x, y, m


def token_logprobs(model, x, y):
    logits = model(x)
    return torch.log_softmax(logits.float(), -1).gather(-1, y[..., None]).squeeze(-1)


def seq_logprob(model, examples) -> torch.Tensor:
    """Sum of log p(answer | prompt) for each (prompt, answer) pair, with gradients."""
    x, y, m = pack(examples)
    return (token_logprobs(model, x, y) * m).sum(-1)


# ---------------------------------------------------------------------------
# LoRA (Hu et al. 2021): W x  ->  W x + (alpha / r) B A x, with W frozen, A random, B zero at the start
# ---------------------------------------------------------------------------
class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, r: int, alpha: float):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad_(False)
        self.A = nn.Parameter(torch.randn(r, base.in_features) / math.sqrt(base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.t() @ self.B.t()) * self.scale

    def merged(self) -> torch.Tensor:
        return self.base.weight + self.scale * self.B @ self.A


TARGETS = ("qkv", "out", "gate", "up", "down")


def add_lora(model, r: int, alpha: float | None = None, targets=TARGETS):
    """Freeze the model and give every target matrix a rank-r adapter; returns the trainable parameters."""
    for p in model.parameters():
        p.requires_grad_(False)
    params = []
    for blk in model.blocks:
        for parent in (blk.attn, blk.mlp):
            for name in targets:
                lin = getattr(parent, name, None)
                if isinstance(lin, nn.Linear):
                    lora = LoRALinear(lin, r, alpha if alpha is not None else 2 * r)
                    setattr(parent, name, lora)
                    params += [lora.A, lora.B]
    return params


def merge_lora(model):
    """Fold every adapter into its matrix (B A added to W): an ordinary model again."""
    for blk in model.blocks:
        for parent in (blk.attn, blk.mlp):
            for name in TARGETS:
                lin = getattr(parent, name, None)
                if isinstance(lin, LoRALinear):
                    plain = lin.base
                    with torch.no_grad():
                        plain.weight.copy_(lin.merged())
                    plain.weight.requires_grad_(True)
                    setattr(parent, name, plain)
    return model


# ---------------------------------------------------------------------------
# Training and sampling
# ---------------------------------------------------------------------------
def sft(model, data: list[tuple[list[int], list[int]]], steps: int, lr: float = 1e-3, batch: int = 32, seed: int = 0,
        params=None, eval_fn=None, eval_every: int = 0, warmup: int = 20) -> list:
    """Supervised fine-tuning on the answers; returns [(step, loss)] and, if given, [(step, eval_fn())]."""
    g = np.random.default_rng(seed)
    params = list(params) if params is not None else [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.0)
    curve, evals = [], []
    model.train()
    for step in range(steps):
        for gr in opt.param_groups:
            gr["lr"] = lr * min(1.0, (step + 1) / warmup) * 0.5 * (1 + math.cos(math.pi * step / steps))
        idx = g.integers(0, len(data), batch)
        x, y, m = pack([data[i] for i in idx])
        loss = -(token_logprobs(model, x, y) * m).sum() / m.sum()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        curve.append((step, loss.item()))
        if eval_fn and eval_every and ((step + 1) % eval_every == 0 or step == steps - 1):
            model.eval()
            evals.append((step + 1, eval_fn(model)))
            model.train()
    model.eval()
    return curve, evals


@torch.no_grad()
def sample(model, prompt: list[int], n: int, max_new: int = 40, temperature: float = 1.0, seed: int = 0,
           top_k: int = 0) -> list[list[int]]:
    """n answers to one prompt (batched), each cut after its <|end|>."""
    end = N.special("<|end|>")
    g = torch.Generator().manual_seed(seed)
    x = torch.tensor([prompt] * n)
    done = torch.zeros(n, dtype=torch.bool)
    out = [[] for _ in range(n)]
    for _ in range(max_new):
        logits = model(x[:, -model.cfg.seq:])[:, -1].float() / max(temperature, 1e-6)
        if top_k:
            v, _ = logits.topk(top_k, -1)
            logits[logits < v[:, -1:]] = -float("inf")
        nxt = torch.multinomial(logits.softmax(-1), 1, generator=g).squeeze(1)
        for i in range(n):
            if not done[i]:
                out[i].append(int(nxt[i]))
        done |= nxt == end
        x = torch.cat([x, nxt[:, None]], 1)
        if bool(done.all()):
            break
    return out


@torch.no_grad()
def greedy(model, prompt: list[int], max_new: int = 24) -> list[int]:
    end = N.special("<|end|>")
    ids = list(prompt)
    for _ in range(max_new):
        nxt = int(model(torch.tensor([ids[-model.cfg.seq:]]))[0, -1].argmax())
        ids.append(nxt)
        if nxt == end:
            break
    return ids[len(prompt):]


def text_of(ids: list[int]) -> str:
    """An answer's text, without its <|end|>."""
    end = N.special("<|end|>")
    return N.decode([i for i in ids if i != end]).strip()


@torch.no_grad()
def heldout_loss(model, valid: np.ndarray, n: int = 16, seq: int = 256, B: int = 8) -> float:
    """Next-token loss on held-out novel text (forgetting is measured here)."""
    starts = np.linspace(0, len(valid) - seq - 2, n * B).astype(int)
    tot = 0.0
    for k in range(n):
        xs = np.stack([valid[s:s + seq + 1] for s in starts[k * B:(k + 1) * B]]).astype(np.int64)
        t = torch.from_numpy(xs)
        tot += float(F.cross_entropy(model(t[:, :-1]).flatten(0, 1), t[:, 1:].flatten()))
    return tot / n
