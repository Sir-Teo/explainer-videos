"""Part 15's sequence mixers in PyTorch: the memories the part compares, small enough to train on a CPU.

Every mixer maps (B, T, D) to (B, T, D) causally and has the same projections (queries, keys, values and an output,
after a short causal convolution), so models built from them have the same parameters, give or take a few gates:

    softmax   attention over every earlier token (no positions: the short convolution carries order), or with
              rotary positions (``rope=True``)
    linear    linear attention, features elu + 1, normalized (Katharopoulos et al. 2020): the memory only adds
    mamba2    a selective state-space layer in Mamba-2's form (Dao & Gu 2024): S_t = a_t S_{t-1} + dt_t v_t k_t^T,
              a_t = exp(-dt_t A), the step dt_t chosen by the input
    delta     the delta rule (DeltaNet; Schlag et al. 2021, Yang et al. 2024): S_t = S_{t-1} - beta_t (S_{t-1} k_t - v_t) k_t^T
    gdn       the gated delta rule (Gated DeltaNet; Yang, Kautz & Hatamizadeh 2025): decay alpha_t, then a delta step

The delta rules train in parallel by chunks (the WY / UT form, ``chunk_gated_delta``), checked against the step-by-step
recurrence (``recurrent_gated_delta``) in compute.py; linear attention and the decaying rule train in their masked
"attention" form, (L o QK^T) V, which is exact.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# The gated delta rule, two ways
# ---------------------------------------------------------------------------
def recurrent_gated_delta(q, k, v, beta, la, S0=None):
    """Step by step.  q, k: (B, H, T, dk); v: (B, H, T, dv); beta, la (log alpha <= 0): (B, H, T).
    S (B, H, dv, dk): S @ k is the memory's answer for key k.  Returns (outputs (B, H, T, dv), final S)."""
    B, H, T, dk = q.shape
    dv = v.shape[-1]
    S = q.new_zeros(B, H, dv, dk) if S0 is None else S0
    out = []
    for t in range(T):
        S = S * la[:, :, t, None, None].exp()
        err = torch.einsum("bhij,bhj->bhi", S, k[:, :, t]) - v[:, :, t]
        S = S - beta[:, :, t, None, None] * torch.einsum("bhi,bhj->bhij", err, k[:, :, t])
        out.append(torch.einsum("bhij,bhj->bhi", S, q[:, :, t]))
    return torch.stack(out, 2), S


def chunk_gated_delta(q, k, v, beta, la, chunk=64, S0=None):
    """The same, a chunk at a time: within a chunk, the product of the (I - beta k k^T) steps and their decays is the
    identity minus a low-rank matrix whose factors come from one triangular solve (the WY / UT form; Yang et al.
    2024); only the chunk-to-chunk hand-over of the state is sequential."""
    B, H, T, dk = q.shape
    dv = v.shape[-1]
    pad = (-T) % chunk
    if pad:  # zero keys, values and gates change nothing
        q, k, v = (F.pad(x, (0, 0, 0, pad)) for x in (q, k, v))
        beta, la = F.pad(beta, (0, pad)), F.pad(la, (0, pad))
    n = (T + pad) // chunk
    q, k, v = (x.reshape(B, H, n, chunk, x.shape[-1]) for x in (q, k, v))
    beta, la = beta.reshape(B, H, n, chunk), la.reshape(B, H, n, chunk)
    cs = la.cumsum(-1)
    G = cs.exp()  # decay from the chunk's start to step i
    low = torch.ones(chunk, chunk, dtype=torch.bool, device=q.device).tril()
    D = (cs[..., :, None] - cs[..., None, :]).clamp(max=0).exp() * low  # decay from step j to step i (j <= i), else 0
    A = (D * (k @ k.transpose(-1, -2))).tril(-1) * beta[..., :, None]
    M = torch.eye(chunk, dtype=q.dtype, device=q.device) + A
    W = torch.linalg.solve_triangular(M, (beta * G)[..., None] * k, upper=False)
    U = torch.linalg.solve_triangular(M, beta[..., None] * v, upper=False)
    QK = D * (q @ k.transpose(-1, -2))  # already zero above the diagonal
    S = q.new_zeros(B, H, dv, dk) if S0 is None else S0
    outs = []
    for c in range(n):
        St = S.transpose(-1, -2)  # (dk, dv)
        Un = U[:, :, c] - W[:, :, c] @ St
        outs.append(G[:, :, c, :, None] * (q[:, :, c] @ St) + QK[:, :, c] @ Un)
        S = G[:, :, c, -1, None, None] * S + (Un * D[:, :, c, -1, :, None]).transpose(-1, -2) @ k[:, :, c]
    o = torch.stack(outs, 2).reshape(B, H, n * chunk, dv)
    return o[:, :, :T], S


def masked_decay(q, k, v, la):
    """The decaying rule S_t = a_t S_{t-1} + v_t k_t^T in its masked form: O = (L o QK^T) V, L_ij = a_{j+1} ... a_i."""
    T = q.shape[-2]
    cs = la.cumsum(-1)
    low = torch.ones(T, T, dtype=torch.bool, device=q.device).tril()
    L = (cs[..., :, None] - cs[..., None, :]).clamp(max=0).exp() * low
    return (L * (q @ k.transpose(-1, -2))) @ v


def rope(x, pos0=0, base=10_000.0):
    """Rotary positions on the last dimension of (B, H, T, d), positions pos0, pos0 + 1, ..."""
    T, d = x.shape[-2], x.shape[-1]
    inv = 1.0 / base ** (torch.arange(0, d, 2, dtype=torch.float32) / d)
    ang = torch.outer(torch.arange(pos0, pos0 + T, dtype=torch.float32), inv)
    c, s = ang.cos(), ang.sin()
    x1, x2 = x[..., ::2], x[..., 1::2]
    return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], -1).flatten(-2)


# ---------------------------------------------------------------------------
# One mixer layer
# ---------------------------------------------------------------------------
KINDS = ("softmax", "linear", "mamba2", "delta", "gdn")


class Mixer(nn.Module):
    """A sequence mixer of the given kind: a short causal convolution, projections to queries and keys of ``dk``
    numbers per head and values of ``dv``, the memory, and an output projection."""

    def __init__(self, kind: str, d: int, dk: int, dv: int | None = None, heads: int = 1, conv: int = 3,
                 rope: bool = False, chunk: int = 64, out_gate: bool = False):
        super().__init__()
        assert kind in KINDS, kind
        self.kind, self.h, self.dk, self.dv = kind, heads, dk, (dv or d // heads)
        self.rope, self.chunk = rope, chunk
        self.conv = nn.Conv1d(d, d, conv, groups=d, padding=conv - 1) if conv else None
        self.q = nn.Linear(d, heads * dk, bias=False)
        self.k = nn.Linear(d, heads * dk, bias=False)
        self.v = nn.Linear(d, heads * self.dv, bias=False)
        self.o = nn.Linear(heads * self.dv, d, bias=False)
        if kind in ("delta", "gdn"):
            self.b = nn.Linear(d, heads)  # beta_t, the write strength
        if kind in ("gdn", "mamba2"):
            self.a = nn.Linear(d, heads)  # the step / gate
            # A > 0 per head, spread so that some heads remember for long and some for short (as Mamba initializes)
            self.A_log = nn.Parameter(torch.log(torch.linspace(1.0, 16.0, heads)))
            with torch.no_grad():  # initial steps between 0.001 and 0.1, as in Mamba
                dt = torch.exp(torch.linspace(math.log(1e-3), math.log(1e-1), heads))
                self.a.bias.copy_(dt + torch.log(-torch.expm1(-dt)))
        self.g = nn.Linear(d, heads * self.dv, bias=False) if out_gate else None
        self.norm = nn.RMSNorm(self.dv) if kind in ("delta", "gdn", "mamba2") else None

    def heads_(self, x, n):
        B, T, _ = x.shape
        return x.view(B, T, self.h, n).transpose(1, 2)

    def forward(self, x, pos0: int = 0):
        B, T, D = x.shape
        u = x
        if self.conv is not None:
            u = self.conv(x.transpose(1, 2))[..., :T].transpose(1, 2)
            u = F.silu(u)
        q, k, v = self.heads_(self.q(u), self.dk), self.heads_(self.k(u), self.dk), self.heads_(self.v(u), self.dv)
        kind = self.kind
        if kind == "softmax":
            if self.rope:
                q, k = rope(q, pos0), rope(k, pos0)
            o = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        elif kind == "linear":
            fq, fk = F.elu(q) + 1, F.elu(k) + 1
            Am = (fq @ fk.transpose(-1, -2)).tril()
            o = (Am @ v) / (Am.sum(-1, keepdim=True) + 1e-6)
        else:
            q, k = F.normalize(q, dim=-1), F.normalize(k, dim=-1)
            if kind == "mamba2":
                dt = F.softplus(self.a(u)).transpose(1, 2)  # (B, H, T)
                la = -dt * self.A_log.exp()[None, :, None]
                o = masked_decay(q, k, v * dt[..., None], la)
            else:
                beta = torch.sigmoid(self.b(u)).transpose(1, 2)
                if kind == "gdn":
                    la = -F.softplus(self.a(u)).transpose(1, 2) * self.A_log.exp()[None, :, None]
                else:
                    la = torch.zeros_like(beta)
                o, _ = chunk_gated_delta(q, k, v, beta, la, self.chunk)
            o = self.norm(o)
        o = o.transpose(1, 2).reshape(B, T, self.h * self.dv)
        if self.g is not None:
            o = o * torch.sigmoid(self.g(u))
        return self.o(o)

    def state_numbers(self, T: int) -> int:
        """How many numbers the memory holds after T tokens: a fixed matrix per head, or (softmax) the whole cache."""
        if self.kind == "softmax":
            return T * self.h * (self.dk + self.dv)
        return self.h * self.dk * self.dv


class SwiGLU(nn.Module):
    def __init__(self, d, hidden):
        super().__init__()
        self.gate, self.up, self.down = (nn.Linear(d, hidden, bias=False), nn.Linear(d, hidden, bias=False),
                                         nn.Linear(hidden, d, bias=False))

    def forward(self, x):
        return self.down(F.silu(self.gate(x)) * self.up(x))


class Net(nn.Module):
    """Embedding, a stack of (mixer, MLP) blocks with pre-norm residuals, a final norm and a readout."""

    def __init__(self, vocab: int, d: int, layers: list[str], dk: int, heads: int = 1, mlp: int | None = None,
                 rope_layers=(), chunk: int = 64, out_gate: bool = False, tie: bool = False, conv: int = 3,
                 attn_conv: int | None = None):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        cv = lambda kd: (conv if attn_conv is None else attn_conv) if kd == "softmax" else conv  # noqa: E731
        self.mix = nn.ModuleList(Mixer(kd, d, dk, heads=heads, rope=(i in rope_layers), chunk=chunk, out_gate=out_gate,
                                       conv=cv(kd)) for i, kd in enumerate(layers))
        self.n1 = nn.ModuleList(nn.RMSNorm(d) for _ in layers)
        self.mlp = nn.ModuleList(SwiGLU(d, mlp) for _ in layers) if mlp else None
        self.n2 = nn.ModuleList(nn.RMSNorm(d) for _ in layers) if mlp else None
        self.norm = nn.RMSNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        if tie:
            self.head.weight = self.emb.weight
        self.layers = list(layers)

    def forward(self, x, pos0: int = 0, hidden: bool = False):
        h = self.emb(x)
        for i, m in enumerate(self.mix):
            h = h + m(self.n1[i](h), pos0)
            if self.mlp is not None:
                h = h + self.mlp[i](self.n2[i](h))
        h = self.norm(h)
        return (self.head(h), h) if hidden else self.head(h)

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())
