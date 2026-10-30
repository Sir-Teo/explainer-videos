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
@torch.no_grad()
def stream(model: pocket.PocketGPT, ids, policy: str, budget: int, sinks: int = 4, collect_attn: int = 0) -> dict:
    """Read ``ids`` one token at a time with a cache of at most ``budget`` tokens per head; return the loss (nats) of
    each next-token prediction.  policy: 'full' (keep all, original positions), 'window', 'sinks', 'h2o'.
    Keys are cached before their rotation and rotated by their place in the cache at every step."""
    cfg = model.cfg
    H, hd = cfg.heads, cfg.d // cfg.heads
    T = len(ids)
    nL = len(model.blocks)
    Kc = [torch.zeros(H, T, hd) for _ in range(nL)]
    Vc = [torch.zeros(H, T, hd) for _ in range(nL)]
    keep = [torch.zeros(H, T, dtype=torch.bool) for _ in range(nL)]
    score = [torch.zeros(H, T) for _ in range(nL)]  # attention each cached token has drawn so far (H2O)
    losses = np.zeros(T - 1)
    first_share = []
    for t in range(T):
        x = model.emb(torch.tensor([ids[t]]))[None]  # (1, 1, d)
        for li, b in enumerate(model.blocks):
            a = b.attn
            h = b.n1(x)
            q, k, v = a.qkv(h).view(1, 1, 3, H, hd).permute(2, 0, 3, 1, 4)  # each (1, H, 1, hd)
            if a.qk_norm:
                q, k = a.q_norm(q), a.k_norm(k)
            Kc[li][:, t] = k[0, :, 0]
            Vc[li][:, t] = v[0, :, 0]
            kp = keep[li]
            kp[:, t] = True
            # evict, per head, down to the budget
            if policy != "full":
                n_kept = int(kp[0].sum())
                if n_kept > budget:
                    if policy == "window":
                        kp[:, t - budget] = False
                    elif policy == "sinks":
                        kp[:, t - budget + sinks] = False
                    elif policy == "h2o":  # drop, per head, the weakest of the older half (the recent half is kept)
                        recent = budget // 2
                        cand = kp.clone()
                        cand[:, max(0, t - recent + 1):] = False
                        sc = score[li].masked_fill(~cand, float("inf"))
                        kp[torch.arange(H), sc.argmin(-1)] = False
            idx = torch.arange(t + 1)
            m = kp[:, :t + 1]
            if policy == "full":
                pos_k = idx.expand(H, -1)
                pos_q = torch.full((H, 1), t)
            else:  # positions inside the cache: 0 .. n-1 in order
                pos_k = m.long().cumsum(-1) - 1
                pos_q = m.sum(-1, keepdim=True) - 1
            kr = rope_at(Kc[li][:, :t + 1], pos_k)
            qr = rope_at(q[0], pos_q)  # (H, 1, hd)
            att = (qr @ kr.transpose(-1, -2))[:, 0] / math.sqrt(hd)  # (H, t+1)
            att = att.masked_fill(~m, -float("inf")).softmax(-1)
            if policy == "h2o":
                score[li][:, :t + 1] += att
            if collect_attn and li == 0 and t >= 16:
                pass
            if t >= 64 and t < 64 + collect_attn:
                first_share.append([float(att[hh, m[hh].nonzero()[0, 0]]) for hh in range(H)])
            y = (att[:, None, :] @ Vc[li][:, :t + 1])[:, 0]  # (H, hd)
            x = x + a.out(y.reshape(1, 1, H * hd))
            x = x + b.mlp(b.n2(x))
        if t < T - 1:
            logits = model.head(model.norm(x))[0, 0]
            losses[t] = float(F.cross_entropy(logits[None], torch.tensor([ids[t + 1]])))
    return dict(losses=losses)


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
