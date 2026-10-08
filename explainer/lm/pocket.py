"""A pocket-sized but *modern* decoder-only transformer and its training loop.

Used to film real, miniature versions of the experiments frontier labs run:
IsoFLOP scaling-law sweeps, AdamW vs Muon, cosine vs warmup-stable-decay
schedules, learning-rate stability sweeps with and without QK-norm, and
mixture-of-experts load balancing.  Same ingredients as a 2025-26 open model,
just ~10^6 times smaller: RMSNorm (pre-norm), rotary position embeddings,
SwiGLU MLPs, no biases, optional QK-norm, optional top-k routed experts.

Every run is a plain function of a JSON-able config, single-threaded, so four
of them can train side by side on a 4-core CPU.  Results are returned as plain
Python data (loss curves, eval losses, diagnostics) for caching.
"""

from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass, field

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class Config:
    vocab: int = 2048
    d: int = 128
    layers: int = 4
    heads: int = 4
    seq: int = 256
    qk_norm: bool = False
    # Mixture of experts (experts = 0 means a dense SwiGLU MLP)
    experts: int = 0
    top_k: int = 2
    expert_hidden: int = 0  # 0 -> same total hidden width as the dense MLP divided by top_k
    balance: str = "none"  # "none" | "aux" (Switch-style loss) | "bias" (DeepSeek-V3 aux-loss-free)
    aux_coef: float = 0.01
    bias_speed: float = 0.001

    @property
    def hidden(self) -> int:  # SwiGLU width with ~the parameter count of a 4d GELU MLP
        return int(round(8 * self.d / 3 / 16)) * 16


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def rope_tables(seq: int, head_dim: int, base: float = 10_000.0):
    inv = 1.0 / base ** (torch.arange(0, head_dim, 2).float() / head_dim)
    ang = torch.outer(torch.arange(seq).float(), inv)
    return ang.cos()[None, None], ang.sin()[None, None]


def apply_rope(x, cos, sin):
    x1, x2 = x[..., ::2], x[..., 1::2]
    T = x.shape[-2]
    c, s = cos[..., :T, :], sin[..., :T, :]
    return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1).flatten(-2)


class Attention(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        self.h, self.hd = cfg.heads, cfg.d // cfg.heads
        self.qkv = nn.Linear(cfg.d, 3 * cfg.d, bias=False)
        self.out = nn.Linear(cfg.d, cfg.d, bias=False)
        self.qk_norm = cfg.qk_norm
        if cfg.qk_norm:
            self.q_norm, self.k_norm = nn.RMSNorm(self.hd), nn.RMSNorm(self.hd)
        cos, sin = rope_tables(cfg.seq, self.hd)
        self.register_buffer("cos", cos, persistent=False)
        self.register_buffer("sin", sin, persistent=False)
        self.max_logit = 0.0  # filled when probing

    def qk(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(x).view(B, T, 3, self.h, self.hd).permute(2, 0, 3, 1, 4)
        if self.qk_norm:
            q, k = self.q_norm(q), self.k_norm(k)
        return apply_rope(q, self.cos, self.sin), apply_rope(k, self.cos, self.sin), v

    def forward(self, x, probe=False):
        B, T, D = x.shape
        q, k, v = self.qk(x)
        if probe:  # largest pre-softmax attention logit (a classic instability symptom)
            logits = (q @ k.transpose(-2, -1)) / math.sqrt(self.hd)
            mask = torch.ones(T, T, dtype=torch.bool).tril()
            self.max_logit = float(logits.masked_fill(~mask, float("-inf")).amax())
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.out(y.transpose(1, 2).reshape(B, T, D))


class SwiGLU(nn.Module):
    def __init__(self, d: int, hidden: int):
        super().__init__()
        self.gate = nn.Linear(d, hidden, bias=False)
        self.up = nn.Linear(d, hidden, bias=False)
        self.down = nn.Linear(hidden, d, bias=False)

    def forward(self, x):
        return self.down(F.silu(self.gate(x)) * self.up(x))


class MoE(nn.Module):
    """Top-k routed experts.  ``balance``: none, a Switch-style auxiliary loss, or
    DeepSeek-V3's auxiliary-loss-free bias (added to the routing scores only for
    choosing experts, nudged after every step toward under-loaded experts)."""

    def __init__(self, cfg: Config):
        super().__init__()
        self.E, self.k, self.balance = cfg.experts, cfg.top_k, cfg.balance
        hid = cfg.expert_hidden or max(16, cfg.hidden // cfg.top_k)
        self.router = nn.Linear(cfg.d, cfg.experts, bias=False)
        self.experts = nn.ModuleList(SwiGLU(cfg.d, hid) for _ in range(cfg.experts))
        self.register_buffer("bias", torch.zeros(cfg.experts), persistent=False)
        self.load = torch.zeros(cfg.experts)  # fraction of routed slots per expert (last batch)
        self.aux = torch.tensor(0.0)

    def forward(self, x):
        B, T, D = x.shape
        flat = x.reshape(-1, D)
        scores = torch.sigmoid(self.router(flat)) if self.balance == "bias" else self.router(flat).softmax(-1)
        choose = scores + self.bias if self.balance == "bias" else scores
        top = choose.topk(self.k, dim=-1).indices  # (n, k)
        gate = scores.gather(1, top)
        if self.balance == "bias":
            gate = gate / gate.sum(-1, keepdim=True)
        counts = torch.bincount(top.flatten(), minlength=self.E).float()
        self.load = (counts / counts.sum()).detach()
        if self.balance == "aux":  # Switch Transformer: E * sum_i f_i * P_i  (=1 when perfectly balanced)
            self.aux = self.E * (self.load * scores.mean(0)).sum()
        out = torch.zeros_like(flat)
        for e, expert in enumerate(self.experts):
            rows, slot = (top == e).nonzero(as_tuple=True)
            if len(rows):
                out.index_add_(0, rows, expert(flat[rows]) * gate[rows, slot, None])
        return out.view(B, T, D)

    @torch.no_grad()
    def update_bias(self, speed: float):
        self.bias += speed * torch.sign(self.load.mean() - self.load)


class Block(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        self.n1, self.n2 = nn.RMSNorm(cfg.d), nn.RMSNorm(cfg.d)
        self.attn = Attention(cfg)
        self.mlp = MoE(cfg) if cfg.experts else SwiGLU(cfg.d, cfg.hidden)

    def forward(self, x, probe=False):
        x = x + self.attn(self.n1(x), probe)
        return x + self.mlp(self.n2(x))


class PocketGPT(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        self.emb = nn.Embedding(cfg.vocab, cfg.d)
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.layers))
        self.norm = nn.RMSNorm(cfg.d)
        self.head = nn.Linear(cfg.d, cfg.vocab, bias=False)
        for name, p in self.named_parameters():
            if p.dim() == 2:
                std = 0.02 if name.startswith(("emb", "head")) else 1 / math.sqrt(p.shape[1])
                if name.endswith(("out.weight", "down.weight")):
                    std /= math.sqrt(2 * cfg.layers)
                nn.init.normal_(p, std=std)

    def forward(self, idx, probe=False):
        x = self.emb(idx)
        for b in self.blocks:
            x = b(x, probe)
        return self.head(self.norm(x))

    def moe_layers(self) -> list[MoE]:
        return [b.mlp for b in self.blocks if isinstance(b.mlp, MoE)]

    def count(self) -> dict:
        """Parameter counts.  'compute' = the matrices every token multiplies through
        (body + unembedding; the embedding is a lookup).  For MoE, 'active' counts
        only top_k experts per layer."""
        body = sum(p.numel() for n, p in self.named_parameters() if n.startswith("blocks"))
        head = self.head.weight.numel()
        out = dict(total=sum(p.numel() for p in self.parameters()), body=body, head=head, compute=body + head)
        if self.cfg.experts:
            per_expert = sum(p.numel() for p in self.moe_layers()[0].experts[0].parameters())
            idle = (self.cfg.experts - self.cfg.top_k) * per_expert * self.cfg.layers
            out["active"] = body + head - idle
        return out


# ---------------------------------------------------------------------------
# Optimizers
# ---------------------------------------------------------------------------
NS_COEFFS = (3.4445, -4.7750, 2.0315)  # Keller Jordan's quintic Newton-Schulz (github.com/KellerJordan/Muon)


def newton_schulz(G: torch.Tensor, steps: int = 5, coeffs=NS_COEFFS, history: list | None = None) -> torch.Tensor:
    """Approximately replace G = U S V^T by U V^T (all singular values -> ~1)."""
    a, b, c = coeffs
    X = G.float()
    tall = X.shape[0] > X.shape[1]
    if tall:
        X = X.T
    X = X / (X.norm() + 1e-7)
    if history is not None:
        history.append(X.clone())
    for _ in range(steps):
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X
        if history is not None:
            history.append(X.clone())
    return X.T if tall else X


class Muon(torch.optim.Optimizer):
    """Momentum SGD whose update for each 2D matrix is orthogonalized by Newton-Schulz.
    Update RMS is matched to AdamW's (0.2 * sqrt(max(rows, cols)), Moonlight 2025) so
    one learning rate can serve both."""

    def __init__(self, params, lr=0.02, momentum=0.95, weight_decay=0.0, ns_steps=5):
        super().__init__(params, dict(lr=lr, momentum=momentum, weight_decay=weight_decay, ns_steps=ns_steps))

    @torch.no_grad()
    def step(self):
        for g in self.param_groups:
            for p in g["params"]:
                if p.grad is None:
                    continue
                st = self.state[p]
                buf = st.setdefault("buf", torch.zeros_like(p))
                buf.mul_(g["momentum"]).add_(p.grad)
                upd = p.grad.add(buf, alpha=g["momentum"])  # Nesterov
                o = newton_schulz(upd, g["ns_steps"])
                o *= 0.2 * math.sqrt(max(p.shape))
                p.mul_(1 - g["lr"] * g["weight_decay"]).add_(o, alpha=-g["lr"])


def make_optimizers(model: PocketGPT, name: str, lr: float, weight_decay: float = 0.1):
    matrices = [p for n, p in model.named_parameters() if p.dim() == 2 and n.startswith("blocks") and "router" not in n]
    mat_ids = {id(p) for p in matrices}
    rest_decay = [p for p in model.parameters() if p.dim() == 2 and id(p) not in mat_ids]
    rest_nodecay = [p for p in model.parameters() if p.dim() < 2]
    betas = (0.9, 0.95)
    if name == "adamw":
        return [torch.optim.AdamW([dict(params=matrices + rest_decay, weight_decay=weight_decay),
                                   dict(params=rest_nodecay, weight_decay=0.0)], lr=lr, betas=betas, eps=1e-8)]
    if name == "muon":
        return [Muon(matrices, lr=lr, weight_decay=weight_decay),
                torch.optim.AdamW([dict(params=rest_decay, weight_decay=weight_decay),
                                   dict(params=rest_nodecay, weight_decay=0.0)], lr=lr, betas=betas, eps=1e-8)]
    raise ValueError(name)


def lr_factor(step: int, total: int, schedule: str, warmup: int, decay_frac: float = 0.2, final: float = 0.1,
              decay_start: int | None = None) -> float:
    """Multiplier on the peak learning rate.  'cosine' decays to ``final`` over the
    whole run; 'wsd' holds the peak (stable) and decays linearly to ``final`` over the
    last ``decay_frac`` of the run (or from ``decay_start``); 'constant' never decays."""
    if step < warmup:
        return (step + 1) / warmup
    if schedule == "cosine":
        t = (step - warmup) / max(1, total - warmup)
        return final + (1 - final) * 0.5 * (1 + math.cos(math.pi * t))
    if schedule == "wsd":
        start = decay_start if decay_start is not None else int(total * (1 - decay_frac))
        if step < start:
            return 1.0
        return 1.0 - (1 - final) * (step - start) / max(1, total - start)
    return 1.0


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
class TokenStream:
    """Random fixed-length windows from a 1-D token array (train) and a fixed
    set of held-out windows (val)."""

    def __init__(self, train: np.ndarray, val: np.ndarray, seq: int, seed: int = 0):
        self.train, self.val, self.seq = train, val, seq
        self.rng = np.random.default_rng(seed)

    def batch(self, B: int):
        ix = self.rng.integers(0, len(self.train) - self.seq - 1, B)
        x = np.stack([self.train[i:i + self.seq + 1] for i in ix]).astype(np.int64)
        t = torch.from_numpy(x)
        return t[:, :-1], t[:, 1:]

    def val_batches(self, B: int, n: int):
        stride = max(1, (len(self.val) - self.seq - 1) // (B * n))
        starts = np.arange(B * n) * stride
        for k in range(n):
            x = np.stack([self.val[i:i + self.seq + 1] for i in starts[k * B:(k + 1) * B]]).astype(np.int64)
            t = torch.from_numpy(x)
            yield t[:, :-1], t[:, 1:]


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
@dataclass
class Run:
    model: Config = field(default_factory=Config)
    optimizer: str = "adamw"
    lr: float = 3e-3
    weight_decay: float = 0.1
    schedule: str = "cosine"
    warmup: int = 50
    decay_frac: float = 0.2
    final_lr: float = 0.1
    batch: int = 16
    tokens: int = 1_000_000  # training horizon in tokens
    clip: float = 1.0
    z_loss: float = 0.0
    seed: int = 0
    eval_every: int = 0  # steps; 0 -> ~40 evals per run
    eval_batches: int = 8
    log_every: int = 10
    probe_every: int = 0  # steps between attention-logit probes (0 = never)
    branch_decays: list = field(default_factory=list)  # WSD: also decay from these fractions (cooldown branches)
    samples: list = field(default_factory=list)  # [(step, prompt_ids)] to sample from during training


def evaluate(model: PocketGPT, data: TokenStream, B: int, n: int) -> float:
    model.eval()
    tot = 0.0
    with torch.no_grad():
        for x, y in data.val_batches(B, n):
            tot += F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train()
    return tot / n


def train(run: Run, data: TokenStream, *, threads: int = 1, verbose: bool = False, state: dict | None = None) -> dict:
    """Train from scratch (or from ``state``) and return curves + diagnostics."""
    torch.set_num_threads(threads)
    torch.manual_seed(run.seed)
    cfg = run.model
    model = PocketGPT(cfg)
    if state is not None:
        model.load_state_dict(state["model"])
    opts = make_optimizers(model, run.optimizer, run.lr, run.weight_decay)
    if state is not None:
        for o, s in zip(opts, state["opts"]):
            o.load_state_dict(s)
    counts = model.count()
    tokens_per_step = run.batch * cfg.seq
    steps = max(1, run.tokens // tokens_per_step)
    eval_every = run.eval_every or max(1, steps // 40)
    curve, evals, probes, loads, bias_hist = [], [], [], [], []
    t0 = time.time()
    diverged = False
    for step in range(steps):
        f = lr_factor(step, steps, run.schedule, run.warmup, run.decay_frac, run.final_lr)
        for o in opts:
            for g in o.param_groups:
                g["lr"] = run.lr * f
        x, y = data.batch(run.batch)
        probe = run.probe_every and step % run.probe_every == 0
        logits = model(x, probe=bool(probe))
        loss = F.cross_entropy(logits.flatten(0, 1), y.flatten())
        total = loss
        if run.z_loss:
            total = total + run.z_loss * torch.logsumexp(logits.float(), -1).pow(2).mean()
        moes = model.moe_layers()
        if moes and cfg.balance == "aux":
            total = total + cfg.aux_coef * sum(m.aux for m in moes) / len(moes)
        for o in opts:
            o.zero_grad(set_to_none=True)
        total.backward()
        gn = float(torch.nn.utils.clip_grad_norm_(model.parameters(), run.clip if run.clip else 1e9))
        for o in opts:
            o.step()
        if moes and cfg.balance == "bias":
            for m in moes:
                m.update_bias(cfg.bias_speed)
        lv = loss.item()
        if not math.isfinite(lv) or lv > 20:
            diverged = True
        if step % run.log_every == 0 or step == steps - 1:
            curve.append([step, lv, gn, f])
        if probe:
            probes.append([step, max(b.attn.max_logit for b in model.blocks),
                           float(logits.detach().abs().amax())])
        if moes and (step % run.log_every == 0 or step == steps - 1):
            loads.append([step] + [m.load.tolist() for m in moes])
            if cfg.balance == "bias":
                bias_hist.append([step] + [m.bias.tolist() for m in moes])
        if (step + 1) % eval_every == 0 or step == steps - 1:
            ev = evaluate(model, data, run.batch, run.eval_batches)
            evals.append([step + 1, (step + 1) * tokens_per_step, ev])
            if verbose:
                print(f"step {step + 1}/{steps} loss {lv:.3f} val {ev:.3f} lr {run.lr * f:.2e} "
                      f"{(time.time() - t0) / (step + 1):.3f}s/step", flush=True)
        if diverged:
            break
    out = dict(run=asdict(run), counts=counts, steps=steps, tokens_per_step=tokens_per_step, curve=curve,
               evals=evals, final_val=evals[-1][2] if evals else float("nan"), diverged=diverged,
               seconds=time.time() - t0, probes=probes)
    if loads:
        out["loads"] = loads
    if bias_hist:
        out["bias"] = bias_hist
    out["_model"] = model
    out["_opts"] = opts
    return out


def flops_per_token(counts: dict, cfg: Config) -> float:
    """6N rule on the matrices each token multiplies through, plus attention's
    QK^T and AV (6 * layers * seq * d, averaged over causal positions)."""
    n = counts.get("active", counts["compute"])
    return 6 * n + 6 * cfg.layers * cfg.seq * cfg.d / 2


@torch.no_grad()
def sample(model: PocketGPT, prompt: list[int], n: int, temperature: float = 0.8, seed: int = 0, top_k: int = 0):
    g = torch.Generator().manual_seed(seed)
    ids = list(prompt)
    model.eval()
    for _ in range(n):
        x = torch.tensor([ids[-model.cfg.seq:]])
        logits = model(x)[0, -1] / max(temperature, 1e-6)
        if top_k:
            v, _ = logits.topk(top_k)
            logits[logits < v[-1]] = -float("inf")
        ids.append(int(torch.multinomial(logits.softmax(-1), 1, generator=g)))
    model.train()
    return ids[len(prompt):]
