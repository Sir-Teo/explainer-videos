"""Precompute everything numerical in Part 13 of the AI series ("Sparsity").

    python -m videos.ai.ai13.compute              # everything missing (Part 1's books; Part 11's transformer)
    python -m videos.ai.ai13.compute --force moe

Results are cached in ``.cache/ai13/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    configs    mixture-of-experts models as published: total and active parameters, experts, experts per token
    moe        a character model (8 characters of context, like Part 10's) whose hidden layer is 8 experts, 2 used per
               character, trained three ways: no balancing, Switch's auxiliary loss, and DeepSeek's loss-free bias;
               each expert's share of the characters during training, held-out bits, the dense models with the same
               active and the same total size, and which experts the characters go to
    topk       sparse attention in Part 11's transformer: how much of each query's attention its top k keys hold, and
               the bits per character when every query may attend only to k keys, chosen by score (as DeepSeek's
               sparse attention does) or as the last k (a sliding window)
    row        one query of that transformer (one head) and its weights over the last 48 keys, for the picture of what
               a window, NSA's blocks and DSA's top k each keep
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai13")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# published configurations: (name, year, total parameters, active per token, routed experts, experts per token, shared)
CONFIGS = [
    ("Mixtral 8x7B", 2023, 46.7e9, 12.9e9, 8, 2, 0),
    ("DeepSeek-V3", 2024, 671e9, 37e9, 256, 8, 1),
    ("Qwen3-235B-A22B", 2025, 235e9, 22e9, 128, 8, 0),
    ("gpt-oss-120b", 2025, 117e9, 5.1e9, 128, 4, 0),
    ("Kimi K2", 2025, 1.04e12, 32e9, 384, 8, 1),
    ("Qwen3-Next-80B-A3B", 2025, 80e9, 3e9, 512, 10, 1),
]


def compute_configs():
    rows = [dict(name=n, year=y, total=t, active=a, experts=e, k=k, shared=s, frac=a / t) for n, y, t, a, e, k, s in CONFIGS]
    assert all(r["active"] < r["total"] for r in rows)
    return dict(rows=rows)


# ---------------------------------------------------------------------------
CTX, EMB, E, TOPK, HID = 8, 16, 8, 2, 96


CURVE_EVERY, ROUTE_AT = 150, (100, 300, 1000, 3000)


def compute_moe():
    import torch
    import torch.nn.functional as F

    from videos.ai.ai9.compute import char_data
    from videos.ai.ai1 import compute as c1

    torch.set_num_threads(2)
    tr, va, K = char_data()
    tr_t, va_t = torch.tensor(tr), torch.tensor(va)
    chars = sorted(set(c1.text("train") + c1.text("valid")))

    def windows(seq, pos):
        return torch.stack([seq[pos - CTX + j] for j in range(CTX)], 1)

    class Model(torch.nn.Module):
        def __init__(self, n_exp, hid):
            super().__init__()
            self.emb = torch.nn.Embedding(K, EMB)
            self.inp = torch.nn.Linear(CTX * EMB, 128)
            self.router = torch.nn.Linear(128, n_exp, bias=False)
            torch.nn.init.normal_(self.router.weight, std=0.01)
            self.w1 = torch.nn.Parameter(torch.randn(n_exp, 128, hid) / math.sqrt(128))
            self.w2 = torch.nn.Parameter(torch.randn(n_exp, hid, 128) / math.sqrt(hid))
            self.out = torch.nn.Linear(128, K)
            self.register_buffer("bias", torch.zeros(n_exp))
            self.n_exp = n_exp

        def forward(self, ctx, k=TOPK):
            x = torch.tanh(self.inp(self.emb(ctx).reshape(len(ctx), -1)))
            if self.n_exp == 1:
                y = torch.tanh(x @ self.w1[0]) @ self.w2[0]
                return self.out(x + y), None, None
            logits = self.router(x)
            probs = torch.softmax(logits, -1)
            top = torch.topk(logits + self.bias, k, -1).indices  # the bias only steers the choice
            gate = torch.gather(probs, 1, top)
            gate = gate / gate.sum(1, keepdim=True)
            h = torch.tanh(torch.einsum("bd,edh->beh", x, self.w1))  # every expert, for clarity; only k are used
            ys = torch.einsum("beh,ehd->bed", h, self.w2)
            y = (torch.gather(ys, 1, top[..., None].expand(-1, -1, 128)) * gate[..., None]).sum(1)
            return self.out(x + y), probs, top

    def bits(m, n=60_000):
        with torch.no_grad():
            pos = torch.arange(CTX, min(len(va_t), n))
            z, _, _ = m(windows(va_t, pos))
            return float(F.cross_entropy(z, va_t[pos])) / math.log(2)

    show = [c for c in "etaoinshrdlcumwfgypbvk .,;\"'?!" if c in chars]

    def route(m):
        """Where the characters go: the expert chosen first, by the last character of the context."""
        with torch.no_grad():
            pos = torch.arange(CTX, 60_000)
            _, probs, top = m(windows(va_t, pos))
            last = va_t[pos - 1].numpy()
            first = top[:, 0].numpy()
        M = np.zeros((len(show), E))
        for i, ch in enumerate(show):
            sel = last == chars.index(ch)
            M[i] = np.bincount(first[sel], minlength=E) / max(sel.sum(), 1)
        return M

    def train(mode, n_exp=E, hid=HID, steps=3000, watch=False):
        torch.manual_seed(2021)  # Fedus, Zoph & Shazeer, Switch Transformers
        m = Model(n_exp, hid)
        opt = torch.optim.Adam([p for p in m.parameters()], lr=3e-3)
        g = rng(2021)
        loads = []
        curve, routes = [(0, bits(m, 20_000))], [route(m)] if watch and n_exp > 1 else []
        for step in range(1, steps + 1):
            pos = torch.tensor(g.integers(CTX, len(tr), 256))
            z, probs, top = m(windows(tr_t, pos))
            loss = F.cross_entropy(z, tr_t[pos])
            if probs is not None:
                f = torch.zeros(n_exp).scatter_add_(0, top.reshape(-1), torch.ones(top.numel())) / top.numel()
                if mode == "aux":  # Switch: penalize experts that get both many characters and much probability
                    loss = loss + 0.01 * n_exp * (f * probs.mean(0)).sum()
                if mode == "bias":  # DeepSeek: nudge each expert's bias against its load, no extra loss
                    with torch.no_grad():
                        m.bias += 0.002 * torch.sign(1 / n_exp - f)
                if step % 50 == 0:
                    loads.append(f.numpy().copy())
            opt.zero_grad()
            loss.backward()
            opt.step()
            if watch and step % CURVE_EVERY == 0:  # held-out bits on a shorter stretch, as it trains
                curve.append((step, bits(m, 20_000)))
            if watch and n_exp > 1 and step in ROUTE_AT:
                routes.append(route(m))
        if watch:
            out[f"curve_{mode if n_exp > 1 else ('dense_active' if hid == HID * TOPK else 'dense_total')}"] = np.array(curve)
            if routes:
                out["route_steps"], out["routes"] = [0, *ROUTE_AT], np.array(routes)
        return m, bits(m), np.array(loads)

    out = dict(E=E, k=TOPK, hid=HID)
    for mode in ("none", "aux", "bias"):
        m, b, loads = train(mode, watch=mode == "bias")
        out[f"bits_{mode}"], out[f"load_{mode}"] = b, loads
        print(f"    {mode}: {b:.3f} bits, final loads " + " ".join(f"{v:.2f}" for v in loads[-1]), flush=True)
        if mode == "bias":
            out["route_chars"], out["route"] = show, route(m)
    # dense models: as many active numbers as the MoE uses per character (2 experts' worth), and as many in total (8)
    _, out["bits_dense_active"], _ = train("none", n_exp=1, hid=HID * TOPK, watch=True)
    _, out["bits_dense_total"], _ = train("none", n_exp=1, hid=HID * E, watch=True)
    print("    dense: active-matched {:.3f}, total-matched {:.3f}".format(out["bits_dense_active"], out["bits_dense_total"]))
    imb = {mde: float(out[f"load_{mde}"][-10:].mean(0).max() * E) for mde in ("none", "aux", "bias")}
    out["imbalance"] = imb  # the busiest expert's share, in multiples of a fair share
    assert imb["bias"] < 1.5 and imb["bias"] < imb["none"]  # the bias evens the work out (the penalty, at Switch's
    # strength, may only partly: the narration says which)
    assert out["bits_bias"] < out["bits_dense_active"]  # same compute per character, more knowledge
    return out


# ---------------------------------------------------------------------------
def compute_topk():
    import torch
    import torch.nn.functional as F

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    T = c11.CTX
    g = rng(5)
    starts = g.integers(0, len(va) - T - 1, 24)
    x = torch.stack([va[s:s + T] for s in starts])
    y = torch.stack([va[s + 1:s + T + 1] for s in starts])
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)
    ks = [1, 2, 4, 8, 16, 32, 64]

    def rot(t):
        a, b = t[..., : c11.DH // 2], t[..., c11.DH // 2:]
        return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

    def run(keep=None, mode="all", mass=None):
        h = model.emb(x)
        B = len(x)
        causal = torch.ones(T, T, dtype=torch.bool).tril()
        for li, blk in enumerate(model.blocks):
            q, k, v = blk.qkv(blk.n1(h)).view(B, T, 3, c11.HEADS, c11.DH).permute(2, 0, 3, 1, 4)
            q, k = rot(q), rot(k)
            s = (q @ k.transpose(-1, -2)) / math.sqrt(c11.DH)
            s = s.masked_fill(~causal, float("-inf"))
            if mode == "topk":
                kth = torch.topk(s, min(keep, T), -1).values[..., -1:]
                s = s.masked_fill(s < kth, float("-inf"))
            elif mode == "window":
                win = causal & ~torch.ones(T, T, dtype=torch.bool).tril(-keep)
                s = s.masked_fill(~win, float("-inf"))
            p = torch.softmax(s, -1)
            if mass is not None:
                srt = torch.sort(p[:, :, 128:], -1, descending=True).values.cumsum(-1)
                mass[li] = np.stack([srt[..., k_ - 1].mean((0, 2)).numpy() for k_ in ks], -1)  # head, k
            a = (p @ v).transpose(1, 2).reshape(B, T, -1)
            h = h + blk.o(a)
            h = h + blk.f2(F.gelu(blk.f1(blk.n2(h))))
        z = model.out(model.nf(h))
        ce = F.cross_entropy(z[:, 128:].reshape(-1, z.shape[-1]), y[:, 128:].reshape(-1))
        return float(ce) / math.log(2)

    with torch.no_grad():
        mass = {}
        full = run(mass=mass)
        out = dict(ks=ks, full=full, mass=np.stack([mass[i] for i in range(c11.LAYERS)]))
        kk = [4, 8, 16, 32, 64]
        out["kk"] = kk
        out["bits_topk"] = [run(k_, "topk") for k_ in kk]
        out["bits_window"] = [run(k_, "window") for k_ in kk]
    print("    full {:.3f}; top-k {}; window {}".format(full, np.round(out["bits_topk"], 3), np.round(out["bits_window"], 3)))
    assert out["bits_topk"][-1] - full < 0.05  # 64 keys chosen by score: almost nothing lost
    assert out["bits_topk"][1] < out["bits_window"][1]  # chosen by score beats the most recent, at k = 8
    return out


# ---------------------------------------------------------------------------
NROW, KEEP, BLOCK = 48, 8, 8


def compute_row():
    import torch
    import torch.nn.functional as F

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(2)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    T = c11.CTX
    starts = rng(13).integers(0, len(va) - T - 1, 48)
    x = torch.stack([va[s:s + T] for s in starts])
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)

    def rot(t):
        a, b = t[..., : c11.DH // 2], t[..., c11.DH // 2:]
        return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

    rows = []  # layer, batch, head: the last query's weights over all T keys
    with torch.no_grad():
        h = model.emb(x)
        B = len(x)
        causal = torch.ones(T, T, dtype=torch.bool).tril()
        for blk in model.blocks:
            q, k, v = blk.qkv(blk.n1(h)).view(B, T, 3, c11.HEADS, c11.DH).permute(2, 0, 3, 1, 4)
            q, k = rot(q), rot(k)
            s = ((q @ k.transpose(-1, -2)) / math.sqrt(c11.DH)).masked_fill(~causal, float("-inf"))
            p = torch.softmax(s, -1)
            rows.append(p[:, :, -1].numpy())
            h = h + blk.o((p @ v).transpose(1, 2).reshape(B, T, -1))
            h = h + blk.f2(F.gelu(blk.f1(blk.n2(h))))
    best = None
    for li, P in enumerate(rows):
        for b in range(P.shape[0]):
            for hh in range(P.shape[1]):
                r = P[b, hh]
                strip = r[-NROW:]
                if strip.sum() < 0.85:  # the picture shows only the last 48 keys: they must hold nearly all of it
                    continue
                top, win = np.sort(strip)[-KEEP:].sum(), strip[-KEEP:].sum()
                if strip.max() > 0.4 or top < 0.6:  # spread over several keys, most of it in a few
                    continue
                far = int((np.argsort(-strip)[:KEEP] < NROW - KEEP).sum())
                score = top - win + 0.02 * far
                if best is None or score > best[0]:
                    best = (score, li, b, hh)
    _, li, b, hh = best
    r = rows[li][b, hh].astype(float)
    strip = r[-NROW:]
    text = "".join(chars[i] for i in x[b, -NROW:].tolist())  # the last 48 keys; the last one is the query's own character
    top = np.argsort(-strip)[:KEEP]
    blocks = strip.reshape(-1, BLOCK).sum(1)
    chosen = np.argsort(-blocks)[:2]
    nsa = np.zeros(NROW, bool)
    for c in chosen:
        nsa[c * BLOCK:(c + 1) * BLOCK] = True
    nsa[-KEEP:] = True
    out = dict(layer=li, head=hh, text=text, weights=strip, strip_mass=float(strip.sum()),
               window=float(strip[-KEEP:].sum()), topk=float(strip[top].sum()), top=np.sort(top),
               blocks=blocks, chosen=np.sort(chosen), nsa=float(strip[nsa].sum()), nsa_keys=int(nsa.sum()))
    print("    layer {} head {}: strip {:.2f}; window {:.2f}, NSA {:.2f} ({} keys), top-{} {:.2f}; {!r}".format(
        li + 1, hh + 1, out["strip_mass"], out["window"], out["nsa"], out["nsa_keys"], KEEP, out["topk"], text))
    assert out["topk"] > out["window"]
    return out


ITEMS = {
    "configs": compute_configs,
    "moe": compute_moe,
    "topk": compute_topk,
    "row": compute_row,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
