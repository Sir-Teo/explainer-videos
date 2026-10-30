"""Memory around the series' own language model (``explainer.ai.novels``: 6.8 million parameters, 256 tokens of context).

Two experiments on the trained model, nothing retrained:

* **Reading with a smaller cache** (``stream``): the model reads a text one token at a time, keeping keys and values
  for only some of the past, as a server would: the last W tokens (window attention), the first four tokens plus the
  last W - 4 (StreamingLLM's attention sinks, Xiao et al. 2023), or the tokens that have drawn the most attention so
  far plus the most recent (H2O's heavy hitters, Zhang et al. 2023).  Positions are counted inside the cache, as
  StreamingLLM does, so the model never sees a position it wasn't trained on.  Or it keeps everything, and the
  positions run past the 256 it was trained on.
* **A nearest-neighbour memory** (``knn``): every token of the thirty novels, stored as the model's last hidden state
  and the token that came next; at test time, the nearest stored states vote for the next token, and the vote is
  mixed with the model's own prediction (kNN-LM, Khandelwal et al. 2020).
"""

from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn.functional as F

from explainer.ai import novels as N
from explainer.lm import pocket


def rope_at(x, pos, base=10_000.0):
    """pocket's rotary positions for x (..., T, hd) at integer positions pos (T,) or (H, T)."""
    hd = x.shape[-1]
    inv = 1.0 / base ** (torch.arange(0, hd, 2).float() / hd)
    ang = pos[..., None].float() * inv
    c, s = ang.cos(), ang.sin()
    x1, x2 = x[..., ::2], x[..., 1::2]
    return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1).flatten(-2)


# ---------------------------------------------------------------------------
# Reading token by token with a policy for the cache
# ---------------------------------------------------------------------------
def _rope_table(n, hd, base=10_000.0):
    inv = 1.0 / base ** (torch.arange(0, hd, 2).float() / hd)
    ang = torch.outer(torch.arange(n).float(), inv)
    return ang.cos(), ang.sin()


def _rot(x, c, s):
    x1, x2 = x[..., ::2], x[..., 1::2]
    return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1).flatten(-2)


@torch.no_grad()
def stream(model: pocket.PocketGPT, ids, policies: list[str], budget: int, sinks: int = 4) -> np.ndarray:
    """Read ``ids`` one token at a time, once per policy (side by side, as a batch), keeping keys and values for at
    most ``budget`` tokens per head: 'window' (the last ``budget``), 'sinks' (the first four and the last budget - 4),
    'h2o' (the recent half, and of the older tokens those that have drawn the most attention so far).  Keys are kept
    before their rotation and rotated by their place in the cache, 0 .. n-1, at every step (as StreamingLLM does).
    Returns each policy's loss (nats) on every next-token prediction."""
    cfg = model.cfg
    H, hd = cfg.heads, cfg.d // cfg.heads
    T, R = len(ids), len(policies)
    nL = len(model.blocks)
    cos, sin = _rope_table(budget + 1, hd)
    Kc = [torch.zeros(R, H, T, hd) for _ in range(nL)]
    Vc = [torch.zeros(R, H, T, hd) for _ in range(nL)]
    slots = [torch.zeros(R, H, 0, dtype=torch.long) for _ in range(nL)]  # the kept tokens, oldest first
    score = [torch.zeros(R, H, T) for _ in range(nL)]
    losses = np.zeros((R, T - 1))
    tgt = torch.tensor(ids[1:] + [0])
    for t in range(T):
        x = model.emb(torch.full((R,), ids[t]))[:, None]
        for li, b in enumerate(model.blocks):
            a = b.attn
            q, k, v = a.qkv(b.n1(x)).view(R, 1, 3, H, hd).permute(2, 0, 3, 1, 4)
            if a.qk_norm:
                q, k = a.q_norm(q), a.k_norm(k)
            Kc[li][:, :, t], Vc[li][:, :, t] = k[:, :, 0], v[:, :, 0]
            sl = torch.cat([slots[li], torch.full((R, H, 1), t)], -1)
            if sl.shape[-1] > budget:  # evict one per head
                drop = torch.zeros(R, H, dtype=torch.long)
                for r, pol in enumerate(policies):
                    if pol == "window":
                        drop[r] = 0
                    elif pol == "sinks":
                        drop[r] = sinks
                    else:  # h2o: the weakest of the slots older than the recent half
                        old = sl.shape[-1] - budget // 2
                        sc = score[li][r].gather(-1, sl[r, :, :old])
                        drop[r] = sc.argmin(-1)
                keepm = torch.ones_like(sl, dtype=torch.bool)
                keepm.scatter_(-1, drop[..., None], False)
                sl = sl[keepm].view(R, H, -1)
            slots[li] = sl
            n = sl.shape[-1]
            idx = sl[..., None].expand(-1, -1, -1, hd)
            kk = _rot(Kc[li].gather(2, idx), cos[:n], sin[:n])
            vv = Vc[li].gather(2, idx)
            qr = _rot(q, cos[n - 1:n], sin[n - 1:n])
            att = ((qr @ kk.transpose(-1, -2)) / math.sqrt(hd)).softmax(-1)  # (R, H, 1, n)
            score[li].scatter_add_(-1, sl, att[:, :, 0])
            y = (att @ vv)[:, :, 0]
            x = x + a.out(y.reshape(R, 1, H * hd))
            x = x + b.mlp(b.n2(x))
        if t < T - 1:
            logits = model.head(model.norm(x))[:, 0]
            losses[:, t] = F.cross_entropy(logits, tgt[t].expand(R), reduction="none").numpy()
    return losses


@torch.no_grad()
def forward_masked(model: pocket.PocketGPT, ids, policy: str, budget: int = 0, sinks: int = 4) -> np.ndarray:
    """The same reading done in one parallel pass, for the policies whose cache doesn't depend on the attention:
    'full' (everything, positions 0, 1, 2, ... past the 256 trained on), 'window' (the last ``budget`` tokens; with
    positions counted inside the cache, a key's distance from the query is the same as in the text, so this is a
    banded mask), 'sinks' (the first four, at cache positions 0-3, and the last budget - 4).  Each token's keys and
    values are computed once, from what it could see when it was read, exactly as token by token."""
    cfg = model.cfg
    H, hd = cfg.heads, cfg.d // cfg.heads
    x = torch.tensor([ids[:-1]])
    T = x.shape[1]
    t = torch.arange(T)
    rel = t[:, None] - t[None, :]
    causal = rel >= 0
    if policy == "full":
        band = causal
    else:
        n = torch.clamp(t + 1, max=budget)  # how many tokens the cache holds when token t is read
        band = causal & (rel < (n - (sinks if policy == "sinks" else 0))[:, None])
    sink = torch.zeros(T, T, dtype=torch.bool)
    if policy == "sinks":
        sink[:, :sinks] = causal[:, :sinks] & ~band[:, :sinks]
    cos, sin = _rope_table(T + 1, hd)
    h = model.emb(x)
    for b in model.blocks:
        a = b.attn
        q, k, v = a.qkv(b.n1(h)).view(1, T, 3, H, hd).permute(2, 0, 3, 1, 4)
        if a.qk_norm:
            q, k = a.q_norm(q), a.k_norm(k)
        qr, kr = _rot(q, cos[:T], sin[:T]), _rot(k, cos[:T], sin[:T])
        sc = (qr @ kr.transpose(-1, -2)) / math.sqrt(hd)
        if policy == "sinks":  # the query sits at cache position n - 1, the sinks at 0 .. 3
            pq = torch.clamp(t + 1, max=budget) - 1
            qs = _rot(q, cos[pq], sin[pq])
            ks = _rot(k[:, :, :sinks], cos[:sinks], sin[:sinks])
            sc_s = (qs @ ks.transpose(-1, -2)) / math.sqrt(hd)
            sc[..., :sinks] = torch.where(sink[:, :sinks], sc_s, sc[..., :sinks])
        sc = sc.masked_fill(~(band | sink), -float("inf"))
        y = sc.softmax(-1) @ v
        h = h + a.out(y.transpose(1, 2).reshape(1, T, H * hd))
        h = h + b.mlp(b.n2(h))
    logits = model.head(model.norm(h))[0]
    return F.cross_entropy(logits, torch.tensor(ids[1:]), reduction="none").numpy()


@torch.no_grad()
def attention_on_first(model: pocket.PocketGPT, windows: torch.Tensor) -> np.ndarray:
    """Each layer's and head's mean attention weight on the first token of the window, for queries 64 to 255."""
    cfg = model.cfg
    out = np.zeros((cfg.layers, cfg.heads))
    for w in windows:
        x = model.emb(w[None])
        for li, b in enumerate(model.blocks):
            q, k, v = b.attn.qk(b.n1(x))
            T = x.shape[1]
            att = (q @ k.transpose(-1, -2)) / math.sqrt(q.shape[-1])
            att = att.masked_fill(~torch.ones(T, T, dtype=torch.bool).tril(), -float("inf")).softmax(-1)
            out[li] += att[0, :, 64:, 0].mean(-1).numpy()
            x = b(x)
    return out / len(windows)


# ---------------------------------------------------------------------------
# The kNN-LM
# ---------------------------------------------------------------------------
@torch.no_grad()
def hidden(model: pocket.PocketGPT, x: torch.Tensor):
    """The final hidden states (after the last norm: what the readout sees) and the log-probabilities."""
    h = model.emb(x)
    for b in model.blocks:
        h = b(h)
    h = model.norm(h)
    return h, model.head(h).log_softmax(-1)


@torch.no_grad()
def query_states(model, ids, window: int = 256, stride: int = 128):
    """Hidden states and the model's log-probability of the true next token, for every token of a text scored as
    Part 14 scores it (windows of 256 sliding by 128; each token once)."""
    H, lp, nxt = [], [], []
    done, lo = 0, 0
    while done < len(ids) - 1:
        hi = min(len(ids), lo + window + 1)
        x = torch.tensor([ids[lo:hi]])
        h, logp = hidden(model, x[:, :-1])
        tgt = x[0, 1:]
        sel = slice(done - lo, hi - 1 - lo)
        H.append(h[0, sel])
        lp.append(logp[0, sel].gather(-1, tgt[sel, None])[:, 0])
        nxt.append(tgt[sel])
        done = hi - 1
        lo += stride
    return torch.cat(H), torch.cat(lp), torch.cat(nxt)


def knn_prob(dists: torch.Tensor, vals: torch.Tensor, target: torch.Tensor, temp: float, k: int) -> torch.Tensor:
    """p_kNN(target): a softmax over the k nearest stored states' negative distances, summed over those whose next
    token is the target."""
    d, v = dists[:, :k], vals[:, :k]
    w = (-d / temp).softmax(-1)
    return (w * (v == target[:, None]).float()).sum(-1)
