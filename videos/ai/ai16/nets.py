"""The small networks Part 16 trains: one character transformer with every kind of sparsity this part is about.

    cfg = Cfg(vocab=K, ffn="moe", E=8, k=2, he=128, gate="sigmoid", balance="bias")
    model = Net(cfg)
    z = model(x)                 # logits; model.stats holds each MoE layer's loads, drops and routes

* the feed-forward layer is dense (hidden ``hidden``) or a mixture of ``E`` experts of hidden ``he``, ``k`` per token,
  with ``shared`` always-on experts of hidden ``hs`` (DeepSeekMoE); gates from a softmax over the chosen experts
  (Mixtral) or from sigmoids renormalized over the chosen (DeepSeek-V3); balancing by nothing, Switch's auxiliary
  loss or DeepSeek's loss-free bias; a capacity factor ``cf`` (tokens over an expert's capacity are dropped: they skip
  the layer);
* mixture-of-depths: the blocks in ``mod_layers`` process only a fraction ``mod_cap`` of the tokens, chosen by a
  router (the top ones of each sequence in training, the router's own verdict, a sigmoid over 1/2, when causal);
* attention is full, a sliding window of ``attn_k`` keys, block selection (MoBA, NSA's selection branch: blocks of
  ``block`` keys scored by their mean key, the best ``attn_k // block`` and the query's own block), or a learned
  indexer that picks ``attn_k`` keys (DeepSeek's sparse attention).

Everything is small (d = 64) and runs on one CPU thread; the dispatch to experts sorts the tokens by expert and runs
one batched matrix product, as real MoE kernels do.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class Cfg:
    vocab: int = 167
    d: int = 64
    layers: int = 2
    heads: int = 4
    ctx: int = 64
    ffn: str = "dense"  # dense | moe
    hidden: int = 256
    E: int = 8
    k: int = 2
    he: int = 128
    shared: int = 0
    hs: int = 0
    gate: str = "softmax"  # softmax | sigmoid
    balance: str = "none"  # none | aux | bias
    aux: float = 0.01
    bias_speed: float = 0.001
    cf: float = 0.0  # capacity factor; 0 = no limit
    mod_layers: tuple = ()
    mod_cap: float = 1.0
    attn: str = "full"  # full | window | blocks | index
    attn_k: int = 0
    block: int = 8
    index_heads: int = 2
    index_dim: int = 16

    def to_dict(self):
        return asdict(self)


def rope(T: int, dh: int):
    inv = 1.0 / 10000 ** (torch.arange(0, dh, 2).float() / dh)
    a = torch.outer(torch.arange(T).float(), inv)
    return a.cos(), a.sin()


def rot(x, cos, sin):
    h = x.shape[-1] // 2
    a, b = x[..., :h], x[..., h:]
    return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)


# ---------------------------------------------------------------------------
# attention
# ---------------------------------------------------------------------------
class Attention(nn.Module):
    def __init__(self, c: Cfg):
        super().__init__()
        self.c = c
        self.h, self.dh = c.heads, c.d // c.heads
        self.qkv = nn.Linear(c.d, 3 * c.d, bias=False)
        self.o = nn.Linear(c.d, c.d, bias=False)
        cos, sin = rope(max(c.ctx, 256), self.dh)
        self.register_buffer("cos", cos, persistent=False)
        self.register_buffer("sin", sin, persistent=False)
        if c.attn == "index":  # DeepSeek's lightning indexer: a few small ReLU heads, their own keys, weights per head
            self.iq = nn.Linear(c.d, c.index_heads * c.index_dim, bias=False)
            self.ik = nn.Linear(c.d, c.index_dim, bias=False)
            self.iw = nn.Linear(c.d, c.index_heads, bias=False)
        self.last = None  # filled when probing: the attention weights and the keys each query may use
        self.index_kl = torch.tensor(0.0)

    def index_scores(self, x):
        B, T, _ = x.shape
        q = self.iq(x).view(B, T, self.c.index_heads, self.c.index_dim)
        k = self.ik(x)
        w = self.iw(x)  # B, T, heads
        s = torch.relu(torch.einsum("bthd,bsd->bths", q, k))
        return torch.einsum("bth,bths->bts", w, s)  # I[t, s]

    def allowed(self, x, q, k, keep=None):
        """The keys each query may use: B (or 1), [H,] T, T booleans."""
        c, T = self.c, x.shape[1]
        causal = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        if c.attn == "full" or not c.attn_k:
            m = causal[None, None]
        elif c.attn == "window":
            m = (causal & ~torch.ones(T, T, dtype=torch.bool).tril(-c.attn_k))[None, None]
        elif c.attn == "blocks":
            nb, Bk = T // c.block, c.block
            kb = k.view(k.shape[0], self.h, nb, Bk, self.dh).mean(3)  # each block's mean key
            sc = q @ kb.transpose(-1, -2)  # B, H, T, nb
            qb = torch.arange(T) // Bk
            past = torch.arange(nb)[None, :] < qb[:, None]  # only whole blocks before the query's own
            sc = sc.masked_fill(~past[None, None], float("-inf"))
            nsel = max(c.attn_k // Bk - 1, 0)
            top = sc.topk(min(nsel, nb), -1).indices if nsel else None
            selb = torch.zeros(sc.shape, dtype=torch.bool)
            if top is not None:
                selb.scatter_(-1, top, True)
                selb &= past[None, None]
            selb |= (qb[:, None] == torch.arange(nb)[None, :])[None, None]  # the query's own block, causally
            m = selb.repeat_interleave(Bk, -1) & causal[None, None]
        elif c.attn == "topk":  # an oracle: the keys the query itself scores highest (per head)
            sc = (q @ k.transpose(-1, -2)).masked_fill(~causal[None, None], float("-inf"))
            top = sc.topk(min(c.attn_k, T), -1).indices
            m = torch.zeros(sc.shape, dtype=torch.bool).scatter_(-1, top, True) & causal[None, None]
        elif c.attn == "index":
            I = self.index_scores(x.detach())  # the indexer learns from its own loss only (DSA)
            I = I.masked_fill(~causal[None], float("-inf"))
            kk = min(c.attn_k, T)
            top = I.topk(kk, -1).indices
            sel = torch.zeros(I.shape, dtype=torch.bool).scatter_(-1, top, True) & causal[None]
            m = sel[:, None]
            self._I = I
        else:
            raise ValueError(c.attn)
        if keep is not None:  # mixture-of-depths: only the routed tokens are keys
            m = m & keep[:, None, None, :]
        return m

    def forward(self, x, keep=None, probe=False, index_target=False):
        B, T, D = x.shape
        q, k, v = self.qkv(x).view(B, T, 3, self.h, self.dh).permute(2, 0, 3, 1, 4)
        cos, sin = self.cos[:T], self.sin[:T]
        q, k = rot(q, cos, sin), rot(k, cos, sin)
        m = self.allowed(x, q, k, keep)
        s = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        eye = torch.eye(T, dtype=torch.bool)[None, None]
        p = torch.softmax(s.masked_fill(~(m | eye), float("-inf")), -1)
        if self.c.attn == "index" and self.training:
            # the indexer's loss: KL from the main attention (summed over heads, over the chosen keys) to its own
            # distribution over the same keys
            with torch.no_grad():
                tgt = p.sum(1)
                tgt = tgt / tgt.sum(-1, keepdim=True)
            if index_target:  # warm-up: match the dense attention over every key
                with torch.no_grad():
                    causal = torch.ones(T, T, dtype=torch.bool).tril()
                    pd = torch.softmax(s.masked_fill(~causal, float("-inf")), -1).sum(1)
                    tgt = pd / pd.sum(-1, keepdim=True)
                    msk = causal[None].expand(B, T, T)
            else:
                msk = m[:, 0]
            li = torch.log_softmax(self._I.masked_fill(~msk, float("-inf")), -1)
            self.index_kl = (tgt * (torch.log(tgt.clamp_min(1e-9)) - li.clamp_min(-1e4))).masked_fill(~msk, 0).sum(-1).mean()
        if probe:
            self.last = dict(p=p.detach(), m=m.detach())
        a = (p @ v).transpose(1, 2).reshape(B, T, D)
        return self.o(a)


# ---------------------------------------------------------------------------
# feed-forward: dense, or experts
# ---------------------------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.w1 = nn.Linear(d, h, bias=False)
        self.w2 = nn.Linear(h, d, bias=False)
        self.acts = None  # filled when probing

    def forward(self, x, probe=False):
        a = F.gelu(self.w1(x))
        if probe:
            self.acts = a.detach()
        if getattr(self, "sparsify", None) is not None:  # activation sparsity: zero the small activations
            a = self.sparsify(a)
        return self.w2(a)


class MoE(nn.Module):
    def __init__(self, c: Cfg):
        super().__init__()
        self.c = c
        E, d, h = c.E, c.d, c.he
        self.router = nn.Linear(d, E, bias=False)
        nn.init.normal_(self.router.weight, std=0.02)
        self.w1 = nn.Parameter(torch.randn(E, d, h) / math.sqrt(d))
        self.w2 = nn.Parameter(torch.randn(E, h, d) / math.sqrt(h) / math.sqrt(2 * c.layers))
        self.shared = MLP(d, c.hs * c.shared) if c.shared else None
        self.register_buffer("bias", torch.zeros(E))
        self.aux = torch.tensor(0.0)
        self.load = torch.zeros(E)
        self.dropped = 0.0
        self.top = None
        self.cf_eval = None  # a capacity factor to impose at evaluation time

    def forward(self, x, probe=False):
        c = self.c
        B, T, D = x.shape
        flat = x.reshape(-1, D)
        N, E, k = flat.shape[0], c.E, c.k
        logits = self.router(flat)
        scores = torch.sigmoid(logits) if c.gate == "sigmoid" else torch.softmax(logits, -1)
        choose = scores + self.bias if c.balance == "bias" else scores
        top = choose.topk(k, -1).indices  # N, k
        if c.gate == "sigmoid":
            g = scores.gather(1, top)
            gate = g / g.sum(-1, keepdim=True)
        else:  # softmax over the chosen experts' logits (Mixtral); for k = 1, Switch's p_i
            gate = torch.softmax(logits.gather(1, top), -1) if k > 1 else scores.gather(1, top)
        counts = torch.bincount(top.reshape(-1), minlength=E).float()
        self.load = (counts / counts.sum()).detach()
        if c.balance == "aux":  # Switch: E * sum_i f_i P_i, smallest (1) when every expert gets 1/E of both
            P = torch.softmax(logits, -1).mean(0)
            self.aux = E * (self.load * P).sum()
        # dispatch: sort the (token, slot) pairs by expert, give each a place in its expert's buffer
        e = top.reshape(-1)
        t = torch.arange(N).repeat_interleave(k)
        gs = gate.reshape(-1)
        order = torch.argsort(e, stable=True)
        e, t, gs = e[order], t[order], gs[order]
        start = torch.cumsum(counts, 0) - counts
        pos = torch.arange(len(e)) - start[e].long()
        cf = self.cf_eval if self.cf_eval is not None else c.cf
        cap = int(counts.max().item()) if not cf else max(1, int(math.ceil(cf * N * k / E)))
        keep = pos < cap
        self.dropped = float(1 - keep.float().mean())
        e, t, gs, pos = e[keep], t[keep], gs[keep], pos[keep]
        buf = flat.new_zeros(E, cap, D)
        buf[e, pos] = flat[t]
        hbuf = F.gelu(torch.bmm(buf, self.w1))
        ob = torch.bmm(hbuf, self.w2)
        y = flat.new_zeros(N, D).index_add_(0, t, ob[e, pos] * gs[:, None])
        if self.shared is not None:
            y = y + self.shared(flat)
        if probe:
            self.top = top.detach().view(B, T, k)
            self.scores = scores.detach().view(B, T, E)
            self.acts = hbuf.detach()
        return y.view(B, T, D)

    @torch.no_grad()
    def update_bias(self):
        self.bias += self.c.bias_speed * torch.sign(self.load.mean() - self.load)


# ---------------------------------------------------------------------------
class Block(nn.Module):
    def __init__(self, c: Cfg, i: int):
        super().__init__()
        self.c, self.i = c, i
        self.n1, self.n2 = nn.LayerNorm(c.d), nn.LayerNorm(c.d)
        self.attn = Attention(c)
        self.ffn = MoE(c) if c.ffn == "moe" else MLP(c.d, c.hidden)
        self.routed = i in tuple(c.mod_layers)
        if self.routed:
            self.mr = nn.Linear(c.d, 1, bias=True)
            nn.init.zeros_(self.mr.weight)
        self.mod_aux = torch.tensor(0.0)
        self.keep = None

    def forward(self, x, probe=False, causal_mod=False, index_target=False):
        if not self.routed:
            x = x + self.attn(self.n1(x), probe=probe, index_target=index_target)
            return x + self.ffn(self.n2(x), probe)
        # mixture-of-depths: a router scores every token; the chosen go through the block, the rest skip it
        B, T, D = x.shape
        r = self.mr(x).squeeze(-1)  # B, T
        n = max(1, int(round(self.c.mod_cap * T)))
        topk = torch.zeros(B, T, dtype=torch.bool).scatter_(1, r.topk(n, -1).indices, True)
        keep = (r > 0) if causal_mod else topk  # causal: the router's own verdict, no peeking at later tokens
        self.mod_aux = F.binary_cross_entropy_with_logits(r, topk.float())  # teach the router to predict top-k
        self.keep = keep.detach()
        w = torch.sigmoid(r)[..., None] * keep[..., None]
        h = x + self.attn(self.n1(x), keep=keep, probe=probe)
        f = (h - x) + self.ffn(self.n2(h), probe)
        return x + w * f


class Net(nn.Module):
    def __init__(self, c: Cfg):
        super().__init__()
        self.c = c
        self.emb = nn.Embedding(c.vocab, c.d)
        nn.init.normal_(self.emb.weight, std=0.1)
        self.blocks = nn.ModuleList(Block(c, i) for i in range(c.layers))
        self.nf = nn.LayerNorm(c.d)
        self.out = nn.Linear(c.d, c.vocab, bias=False)
        for b in self.blocks:
            nn.init.normal_(b.attn.o.weight, std=0.02 / math.sqrt(2 * c.layers))
            if isinstance(b.ffn, MLP):
                nn.init.normal_(b.ffn.w2.weight, std=1 / math.sqrt(c.hidden) / math.sqrt(2 * c.layers))

    def forward(self, x, probe=False, causal_mod=False, index_target=False):
        h = self.emb(x)
        for b in self.blocks:
            h = b(h, probe, causal_mod, index_target)
        return self.out(self.nf(h))

    def moes(self):
        return [b.ffn for b in self.blocks if isinstance(b.ffn, MoE)]

    def extra_loss(self):
        c, tot = self.c, torch.tensor(0.0)
        if c.ffn == "moe" and c.balance == "aux":
            tot = tot + c.aux * sum(m.aux for m in self.moes()) / len(self.moes())
        for b in self.blocks:
            if b.routed:
                tot = tot + 0.1 * b.mod_aux
            if c.attn == "index":
                tot = tot + b.attn.index_kl
        return tot

    def counts(self) -> dict:
        """Parameters in all, and those each token uses (the embedding is a lookup: it counts in the total only)."""
        c = self.c
        total = sum(p.numel() for p in self.parameters())
        active = total - self.emb.weight.numel()
        if c.ffn == "moe":
            idle = (c.E - c.k) * 2 * c.d * c.he * c.layers
            active -= idle
        return dict(total=int(total), active=int(active))

    def flops(self) -> float:
        """Training FLOPs per token, 6 x the parameters each token multiplies through (Part 12's rule), plus attention's
        QK and AV over the keys it may use; mixture-of-depths blocks count only their share of the tokens."""
        c = self.c
        att_lin = 4 * c.d * c.d
        ffn = 2 * c.d * c.hidden if c.ffn == "dense" else 2 * c.d * (c.k * c.he + c.shared * c.hs) + c.d * c.E
        keys = (c.ctx + 1) / 2 if c.attn == "full" or not c.attn_k else min(c.attn_k, (c.ctx + 1) / 2)
        per_block = att_lin + ffn + 2 * keys * c.d
        tot = 0.0
        for i in range(c.layers):
            frac = c.mod_cap if i in tuple(c.mod_layers) else 1.0
            tot += frac * per_block
        return 6 * (tot + c.d * c.vocab)


def upcycle(dense: Net, c: Cfg, noise: float = 0.01, seed: int = 0) -> Net:
    """Sparse upcycling (Komatsuzaki et al., 2022): every expert starts as a copy of the dense model's feed-forward
    layer (plus a little noise, to break the tie), the router from scratch, everything else copied.  With the gates
    renormalized over the chosen experts, the new model computes exactly what the dense one did."""
    assert c.he == dense.c.hidden and c.ffn == "moe"
    m = Net(c)
    sd = {k: v for k, v in dense.state_dict().items() if ".ffn." not in k}
    missing = m.load_state_dict(sd, strict=False)
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        for bm, bd in zip(m.blocks, dense.blocks):
            w1, w2 = bd.ffn.w1.weight.T, bd.ffn.w2.weight.T  # d x h, h x d
            for e in range(c.E):
                bm.ffn.w1[e] = w1 * (1 + noise * torch.randn(w1.shape, generator=g))
                bm.ffn.w2[e] = w2 * (1 + noise * torch.randn(w2.shape, generator=g))
    assert all(".ffn." in k for k in missing.missing_keys), missing
    return m
