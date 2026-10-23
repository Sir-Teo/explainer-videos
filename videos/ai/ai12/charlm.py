"""The character models of Part 12 ("The Mathematics of Scale"), and how they are trained and measured.

The workhorse is Part 11's character model: 8 characters of context, each a 16-number vector, a hidden layer of width
n (tanh), a second n x n hidden layer (tanh) added back onto the first (a residual connection), and a softmax over
the 167 characters of Part 1's books; scored in bits per character on held-out text. Here it comes in three
parametrizations (the usual one, "SP"; muP; and, for the depth experiment, a deep residual version with CompleteP's
branch multipliers), with its hidden layer optionally split into experts (Part 16's mixture of experts).

Everything is seeded. Training data is read in the order of a seeded permutation of the training text, so a run
never sees the same window twice until it has seen them all ("fresh" data); ``Stream(subset=U)`` instead repeats a
fixed set of U windows epoch after epoch (the data-constrained experiment).

Nothing here sets torch's thread count at import time: ``threads()`` is called by each job.
"""

from __future__ import annotations

import math
import os

import numpy as np

CTX, EMB = 8, 16
BASE = 64  # muP's base width: a width-64 model is the same in both parametrizations
BATCH = 256
WARMUP = 50  # steps of linear warmup in every schedule
COOL = 0.2  # the last fifth of a run decays the learning rate linearly to zero (warmup-stable-decay)


def threads(n: int | None = None) -> None:
    import torch

    torch.set_num_threads(int(n or os.environ.get("AI12_THREADS", 1)))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


_data: dict = {}


def char_data():
    """(train codes, held-out codes, vocabulary size): Part 11's split of Part 1's books (100,000 held-out)."""
    if "d" not in _data:
        from videos.ai.ai11.compute import char_data as cd

        _data["d"] = cd()
    return _data["d"]


def tensors():
    import torch

    if "t" not in _data:
        tr, va, K = char_data()
        _data["t"] = (torch.from_numpy(np.asarray(tr, np.int64)), torch.from_numpy(np.asarray(va, np.int64)), K)
    return _data["t"]


_OFF = None


def windows(seq, pos):
    """The 8 characters before each position (a batch of contexts)."""
    import torch

    global _OFF
    if _OFF is None:
        _OFF = torch.arange(-CTX, 0)
    return seq[pos[:, None] + _OFF]


class Stream:
    """Training positions in a seeded random order. ``subset``: only the first ``subset`` positions of that order,
    repeated epoch after epoch, each epoch reshuffled (seeded)."""

    _perms: dict = {}

    def __init__(self, seed: int = 0, subset: int | None = None):
        import torch

        tr, _, _ = char_data()
        n = len(tr) - CTX
        key = (seed, n)
        if key not in Stream._perms:
            Stream._perms.clear()  # one permutation in memory at a time (95 MB)
            Stream._perms[key] = (rng(10_000 + seed).permutation(n).astype(np.int32) + CTX)
        self.perm = Stream._perms[key]
        self.subset = subset
        self.seed = seed
        self._epoch, self._order = -1, None
        self.torch = torch

    def batch(self, step: int, B: int = BATCH):
        """The positions of training step ``step`` (0-based): a pure function of the step, so a resumed run reads the
        same data."""
        if self.subset is None:
            i = step * B
            return self.torch.from_numpy(self.perm[i:i + B].astype(np.int64))
        U = self.subset
        i = step * B
        out = np.empty(B, np.int64)
        for j in range(B):  # an epoch boundary can fall inside a batch
            e, r = divmod(i + j, U)
            if e != self._epoch:
                self._epoch = e
                self._order = rng(20_000 + 7919 * self.seed + e).permutation(U)
            out[j] = self.perm[self._order[r]]
        return self.torch.from_numpy(out)


# ---------------------------------------------------------------------------
# The models
# ---------------------------------------------------------------------------
def make_model(width: int, mup: bool = True, experts: int = 1, seed: int = 0, base: int = BASE):
    """Part 11's character model at a given width. In muP the output is scaled by base/width and starts at zero,
    and the hidden n x n matrix (each expert's, if split) learns at base/width times the rate."""
    import torch

    _, _, K = char_data()
    torch.manual_seed(seed)

    class CharMLP(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = torch.nn.Embedding(K, EMB)
            self.h1 = torch.nn.Linear(CTX * EMB, width)
            self.experts = experts
            if experts == 1:
                self.h2 = torch.nn.Linear(width, width)
            else:  # Part 16's mixture of experts: E hidden matrices, one chosen per character by a router
                self.w2 = torch.nn.Parameter(torch.empty(experts, width, width))
                self.b2 = torch.nn.Parameter(torch.zeros(experts, width))
                for e in range(experts):
                    torch.nn.init.kaiming_uniform_(self.w2.data[e], a=math.sqrt(5))
                    self.b2.data[e].uniform_(-1 / math.sqrt(width), 1 / math.sqrt(width))
                self.router = torch.nn.Linear(width, experts)
                torch.nn.init.zeros_(self.router.weight)
            self.out = torch.nn.Linear(width, K)
            self.mult = base / width if mup else 1.0
            if mup:
                torch.nn.init.zeros_(self.out.weight)
            self.aux = None

        def hidden(self, ctx):
            h = torch.tanh(self.h1(self.emb(ctx).reshape(len(ctx), -1)))
            if self.experts == 1:
                return torch.tanh(self.h2(h)) + h
            p = torch.softmax(self.router(h), -1)
            g, e = p.max(-1)  # top-1 ("switch") routing
            y = torch.empty_like(h)
            for k in range(self.experts):
                m = e == k
                if m.any():
                    y[m] = torch.tanh(h[m] @ self.w2[k].T + self.b2[k]) * g[m, None]
            f = torch.bincount(e, minlength=self.experts).float() / len(e)
            self.aux = self.experts * (f * p.mean(0)).sum()  # Switch's load-balancing loss (1 when even)
            self.load = f.detach()
            return y + h

        def forward(self, ctx):
            return self.out(self.hidden(ctx)) * self.mult

        def groups(self, lr):
            hid = [self.h2.weight] if experts == 1 else [self.w2]
            rest = [p for p in self.parameters() if all(p is not q for q in hid)]
            k = base / width if mup else 1.0
            return [dict(params=rest, lr=lr, base_lr=lr), dict(params=hid, lr=lr * k, base_lr=lr * k)]

    m = CharMLP()
    m.width, m.mup = width, mup
    return m


def make_deep(width: int, depth: int, alpha: float, seed: int = 0, base_depth: int = 2):
    """A deep residual character model: an input layer, ``depth`` pre-norm blocks h <- h + m W2 relu(W1 norm(h)),
    a final norm and the softmax. ``alpha`` sets the depth scaling (Dey et al. 2025, Table 1): the branch multiplier
    m = (L/L_base)^-alpha and the blocks' learning rate times (L/L_base)^(alpha-1). alpha = 0: no depth scaling
    (muP alone); 1/2: depth-muP; 1: CompleteP. The width is fixed, so muP's width factors are all 1."""
    import torch

    _, _, K = char_data()
    torch.manual_seed(seed)
    mL = depth / base_depth

    class Block(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.norm = torch.nn.LayerNorm(width)
            self.w1 = torch.nn.Linear(width, width)
            self.w2 = torch.nn.Linear(width, width)

        def forward(self, h):
            return self.w2(torch.relu(self.w1(self.norm(h))))

    class Deep(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = torch.nn.Embedding(K, EMB)
            self.inp = torch.nn.Linear(CTX * EMB, width)
            self.blocks = torch.nn.ModuleList([Block() for _ in range(depth)])
            self.norm = torch.nn.LayerNorm(width)
            self.out = torch.nn.Linear(width, K)
            torch.nn.init.zeros_(self.out.weight)
            self.m = mL ** -alpha

        def forward(self, ctx):
            h = self.inp(self.emb(ctx).reshape(len(ctx), -1))
            for b in self.blocks:
                h = h + self.m * b(h)
            return self.out(self.norm(h))

        def groups(self, lr):
            blk = [p for b in self.blocks for p in b.parameters()]
            rest = [p for p in self.parameters() if all(p is not q for q in blk)]
            k = mL ** (alpha - 1)
            return [dict(params=rest, lr=lr, base_lr=lr), dict(params=blk, lr=lr * k, base_lr=lr * k)]

    return Deep()


def n_params(model) -> int:
    return sum(p.numel() for p in model.parameters())


def active_params(model) -> int:
    """Parameters used per character (one expert of a mixture)."""
    n = n_params(model)
    if getattr(model, "experts", 1) > 1:
        w = model.width
        n -= (model.experts - 1) * (w * w + w)
    return n


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def lr_factor(step: int, steps: int, decay_from: int | None = None) -> float:
    """Warmup-stable-decay: linear warmup over WARMUP steps, constant, then (from ``decay_from``, by default the last
    fifth) linear decay to zero at ``steps``."""
    w = min(1.0, (step + 1) / WARMUP)
    d0 = int(round((1 - COOL) * steps)) if decay_from is None else decay_from
    if step >= d0:
        w *= max(0.0, (steps - step) / max(1, steps - d0))
    return w


def set_lr(opt, f: float) -> None:
    for g in opt.param_groups:
        g["lr"] = g["base_lr"] * f


def adam(model, lr, betas=(0.9, 0.95)):
    import torch

    return torch.optim.Adam(model.groups(lr), betas=betas)


def step_once(model, opt, pos, seq, aux_weight=0.01):
    import torch

    logits = model(windows(seq, pos))
    loss = torch.nn.functional.cross_entropy(logits, seq[pos])
    total = loss + aux_weight * model.aux if getattr(model, "aux", None) is not None else loss
    if not torch.isfinite(total):
        return float("nan")
    opt.zero_grad(set_to_none=True)
    total.backward()
    opt.step()
    return float(loss)


def bits(model, seq=None, n: int = 100_000, start: int = CTX) -> float:
    """Held-out bits per character on the first ``n`` predictions of the held-out text."""
    import torch

    if seq is None:
        seq = tensors()[1]
    end = min(len(seq), start + n)
    tot, cnt = 0.0, 0
    with torch.no_grad():
        for a in range(start, end, 20_000):
            pos = torch.arange(a, min(end, a + 20_000))
            lg = model(windows(seq, pos))
            tot += float(torch.nn.functional.cross_entropy(lg, seq[pos], reduction="sum"))
            cnt += len(pos)
    return tot / cnt / math.log(2)


def train_run(model, lr, steps, stream: Stream, eval_at=(), eval_n=20_000, betas=(0.9, 0.95)):
    """One run with the warmup-stable-decay schedule; returns the final held-out bits and the curve at ``eval_at``."""
    tr_t, va_t, _ = tensors()
    opt = adam(model, lr, betas)
    curve = []
    for s in range(steps):
        set_lr(opt, lr_factor(s, steps))
        if not math.isfinite(step_once(model, opt, stream.batch(s), tr_t)):
            return dict(final=float("nan"), curve=curve, diverged=s)
        if s + 1 in eval_at:
            curve.append((s + 1, bits(model, va_t, eval_n)))
    return dict(final=bits(model, va_t), curve=curve)


# ---------------------------------------------------------------------------
# Measurements on a trained model
# ---------------------------------------------------------------------------
def quantized_bits(model, nbits: int, n: int = 30_000) -> float:
    """Post-training quantization: every weight matrix rounded to ``nbits`` (symmetric, one scale per output row,
    round to nearest); the held-out bits of the rounded model (the original weights are restored)."""
    import torch

    mats = [p for name, p in model.named_parameters() if p.ndim >= 2 and not name.startswith("emb")]
    saved = [p.detach().clone() for p in mats]
    q = 2 ** (nbits - 1) - 1
    with torch.no_grad():
        for p in mats:
            s = p.abs().amax(dim=-1, keepdim=True).clamp_min(1e-12) / q
            p.copy_(torch.round(p / s) * s)
    try:
        return bits(model, n=n)
    finally:
        with torch.no_grad():
            for p, s0 in zip(mats, saved):
                p.copy_(s0)


TASK_N, TASK_LEN = 2000, 8


def task_positions() -> np.ndarray:
    """The checkable task: from 2,000 held-out places (seeded), guess the next 8 characters exactly."""
    _, va, _ = char_data()
    return np.sort(rng(4242).choice(np.arange(CTX, len(va) - TASK_LEN), TASK_N, replace=False))


def task_scores(model) -> dict:
    """For each place and each target length L = 1..8: the log-probability (natural log) that sampling at temperature
    1 writes exactly the true characters (teacher-forced, so exact), whether the most likely character is right at
    each step (teacher-forced), and whether greedy decoding writes the true characters (exact match)."""
    import torch

    _, va_t, _ = tensors()
    P = torch.from_numpy(task_positions())
    with torch.no_grad():
        lp = torch.zeros(len(P), TASK_LEN)
        top = torch.zeros(len(P), TASK_LEN, dtype=torch.bool)
        for j in range(TASK_LEN):
            lg = torch.log_softmax(model(windows(va_t, P + j)), -1)
            tgt = va_t[P + j]
            lp[:, j] = lg.gather(1, tgt[:, None])[:, 0]
            top[:, j] = lg.argmax(1) == tgt
        # greedy decoding: feed the model's own guesses back in
        ctx = windows(va_t, P).clone()
        ok = torch.ones(len(P), dtype=torch.bool)
        greedy = torch.zeros(len(P), TASK_LEN, dtype=torch.bool)
        for j in range(TASK_LEN):
            g = model(ctx).argmax(1)
            ok &= g == va_t[P + j]
            greedy[:, j] = ok
            ctx = torch.cat([ctx[:, 1:], g[:, None]], 1)
    return dict(logp=lp.numpy().astype(np.float32), top=top.numpy(), greedy=greedy.numpy())
