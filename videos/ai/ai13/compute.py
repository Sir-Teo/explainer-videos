"""Precompute everything numerical in Part 13 of the AI series ("Attention as Geometry").

    python -m videos.ai.ai13.compute              # everything missing (Part 1's books: .cache/ai1; Part 7's data)
    python -m videos.ai.ai13.compute --force heads

Results are cached in ``.cache/ai13/<name>.json`` (+ ``.npz``); the trained transformer's weights in
``.cache/ai13/tf.pt``. Scenes call ``load(name)``. Every random choice is seeded; the long items resume after an
interruption (the transformer from ``.cache/ai13/tf.ckpt.pt``, saved every 250 steps with the random state; the
items made of many small runs piece by piece, ``CACHE.partial``). Torch threads: ``AI13_THREADS`` (default 2; on a
busy machine 1 is often faster).

Items:
    smoother   Nadaraya and Watson's kernel smoother on Part 7's data (how often "her" appears on each page of *Great
               Expectations*): the estimate at three bandwidths, and the weights one query puts on every page
    dotscale   why attention divides by the square root of d: for random queries and 64 random keys, the spread of the
               scores, the entropy of the softmax weights and the size of the softmax's gradient, as d grows, with and
               without the division
    hopfield   associative memory: a classical Hopfield network (Hebbian weights, sign updates) against a modern one
               (one softmax step, which is attention), recalling stored patterns from corrupted cues as more are stored;
               the inverse temperature beta, from averaging to recall; letters recalled in one step
    rope       rotary position embeddings: the frequencies of a 32-number head, the check that a rotated query and key
               score depends only on their distance, the long-range decay; sinusoidal positions' shift as a rotation
    tf         our own transformer, trained on Part 1's books: characters in, 4 blocks of attention and MLP, 4 heads
               of 32 dimensions, rotary positions, 256 characters of context; bits per character on the passage (the
               scoreboard), the training curve, and a replay of training (samples, every head's attention, copying,
               induction and composition scores, sinks, at 11 checkpoints); attention maps on a sentence of the
               passage, attention by distance, sinks, in-context copying of repeated strings, samples
    heads      our transformer's heads as low-rank maps (singular values of W_Q W_K^T and W_V W_O), the QK/OV composition
               scores against random matrices, the causal mask checked (changing the future changes nothing), and
               the cost of a block: parameters counted and FLOPs measured against the formulas
    extend     the same transformer at 4x its training context, without retraining: rotary positions as trained,
               position interpolation, NTK-aware scaling, YaRN, log-n scaling; bits per character by position; then
               100 steps of fine-tuning at the long context for interpolation and YaRN
    positions  four ways to tell a small transformer where things are (sinusoidal, RoPE, ALiBi, none), each trained
               on the novels at 128 characters with three seeds at equal budgets, then read at 512
    sinks      attention sinks on the bigram-backcopy task (a head that is needed only after a trigger): plain softmax,
               a learned sink logit (gpt-oss), an output gate (Qwen), differential attention; three seeds each
    qkscale    QK-norm and soft caps against blow-up: our transformer's queries and keys scaled up, the entropy of its
               attention and its bits, plain, soft-capped and normalized
    induction  a two-layer attention-only transformer on random tokens with a repeated stretch (three seeds): the
               sudden drop in loss on the repeat, K-composition between the heads through training, the same for one
               layer, and the two heads' patterns
    icl        in-context linear regression: one layer of linear self-attention, trained, against one step of gradient
               descent (von Oswald et al., 2023); its learned matrices, and 1-3 layers against 1-3 steps
    rasp       what attention can compute: RASP's histogram compiled by hand into one attention layer and run exactly;
               then small transformers trained on histograms and on parity at lengths up to 20, tested up to 60
"""

from __future__ import annotations

import math
import os
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai13")
load = CACHE.load

# our transformer
CTX, D, LAYERS, HEADS, BASE = 256, 128, 4, 4, 10000.0
DH = D // HEADS
STEPS, BATCH = 3000, 32
TF_SNAPS = (0, 50, 100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000)  # the training replay's checkpoints
TF_CKPT = 250  # steps between checkpoints
PROMPT = "Spade sat down in the armchair, and "


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def threads(default: int = 2) -> None:
    """Torch threads for this computation (never at import: other parts import this module)."""
    import torch

    torch.set_num_threads(int(os.environ.get("AI13_THREADS", default)))


# ---------------------------------------------------------------------------
def compute_smoother():
    from videos.ai.ai7 import compute as c7

    gp = c7.load("gp")
    x, y = np.asarray(gp["x"], float), np.asarray(gp["y"], float)
    xs = np.linspace(0, x[-1], 400)

    def nw(h, at):
        s = -0.5 * (at[:, None] - x[None]) ** 2 / h ** 2  # the score of each page, for each query
        w = np.exp(s - s.max(1, keepdims=True))
        w /= w.sum(1, keepdims=True)
        return w @ y, w

    out = dict(x=x, y=y, xs=xs, hs=[0.6, 2.5, 10.0])
    for h in out["hs"]:
        out[f"fit{h:g}"] = nw(h, xs)[0]
    q = 120.0  # one query page
    for h in out["hs"]:
        f, w = nw(h, np.array([q]))
        out[f"w{h:g}"], out[f"at{h:g}"] = w[0], float(f[0])
        assert abs(w[0].sum() - 1) < 1e-9
    out["q"] = q
    # a small bandwidth follows the noise, a large one flattens everything
    r = [float(np.mean((nw(h, x)[0] - y) ** 2)) for h in out["hs"]]
    out["fit_mse"] = r
    # leave-one-out error by bandwidth: the bandwidth a smoother would pick for itself
    hs = np.exp(np.linspace(np.log(0.4), np.log(30), 40))
    loo = []
    for h in hs:
        s = -0.5 * (x[:, None] - x[None]) ** 2 / h ** 2
        np.fill_diagonal(s, -np.inf)
        w = np.exp(s - s.max(1, keepdims=True))
        w /= w.sum(1, keepdims=True)
        loo.append(float(np.mean((w @ y - y) ** 2)))
    out["loo_h"], out["loo"] = hs, np.array(loo)
    out["best_h"] = float(hs[int(np.argmin(loo))])
    return out


# ---------------------------------------------------------------------------
def compute_dotscale():
    g = rng(1706)  # Vaswani et al., arXiv 1706.03762
    ds = [2, 8, 32, 128, 512]
    n, trials = 64, 2000

    def stats(s):
        s = s - s.max(1, keepdims=True)
        p = np.exp(s)
        p /= p.sum(1, keepdims=True)
        ent = (-(p * np.log2(np.maximum(p, 1e-300))).sum(1)).mean()
        # the softmax's Jacobian diag(p) - p p^T: its size (Frobenius norm) is how much the weights still respond
        jac = np.sqrt(np.maximum((p ** 2).sum(1) - 2 * (p ** 3).sum(1) + ((p ** 2).sum(1)) ** 2, 0))
        return float(ent), float(p.max(1).mean()), float(jac.mean())

    out = dict(ds=ds, n=n, raw_ent=[], scaled_ent=[], raw_max=[], scaled_max=[], sd=[], sd_scaled=[], raw_jac=[],
               scaled_jac=[])
    for d in ds:
        q = g.normal(size=(trials, d))
        k = g.normal(size=(trials, n, d))
        s = np.einsum("td,tnd->tn", q, k)
        out["sd"].append(float(s.std()))
        out["sd_scaled"].append(float((s / math.sqrt(d)).std()))
        e, m, j = stats(s)
        out["raw_ent"].append(e)
        out["raw_max"].append(m)
        out["raw_jac"].append(j)
        e, m, j = stats(s / math.sqrt(d))
        out["scaled_ent"].append(e)
        out["scaled_max"].append(m)
        out["scaled_jac"].append(j)
    out["max_ent"] = math.log2(n)
    # the Jacobian's size as the spread of the scores grows, on one grid (for the saturation picture)
    sig = np.exp(np.linspace(np.log(0.1), np.log(30), 50))
    qq, kk = g.normal(size=(trials, n)), None
    out["sig"] = sig
    out["jac_by_sig"] = np.array([stats(qq * s_)[2] for s_ in sig])
    out["ent_by_sig"] = np.array([stats(qq * s_)[0] for s_ in sig])
    assert abs(out["sd"][-1] / math.sqrt(ds[-1]) - 1) < 0.05  # the scores spread like sqrt(d)
    return out


# ---------------------------------------------------------------------------
def rope_freqs(dh=DH, base=BASE):
    return base ** (-np.arange(0, dh, 2) / dh)  # one angle per pair of numbers


def compute_rope():
    th = rope_freqs()
    g = rng(2021)  # Su et al., RoFormer
    q, k = g.normal(size=DH), g.normal(size=DH)

    def rot(v, m):
        a, b = v[: DH // 2], v[DH // 2:]
        c, s = np.cos(m * th), np.sin(m * th)
        return np.concatenate([a * c - b * s, a * s + b * c])

    # the score of query at m and key at n depends only on m - n
    grid = np.array([[rot(q, m) @ rot(k, n) for n in range(0, 40)] for m in range(0, 40)])
    dev = max(abs(grid[m, n] - grid[m - n, 0]) for m in range(40) for n in range(m + 1))
    assert dev < 1e-9
    r = np.arange(0, 2001)
    decay = np.cos(r[:, None] * th[None]).mean(1)  # a query scored against itself, moved r characters away
    # the same, averaged over distances within 10% of r (the fast pairs make it jitter from one r to the next)
    rs = np.unique(np.round(np.logspace(0, np.log10(2000), 160)).astype(int))
    smooth = np.array([decay[max(1, int(v * 0.9)):int(v * 1.1) + 1].mean() for v in rs])
    # sinusoidal positions (2017): PE(t + k) is a fixed linear map of PE(t), the same rotation for every t
    dm = 16
    om = 10000.0 ** (-np.arange(0, dm, 2) / dm)

    def pe(t):
        return np.stack([np.sin(t * om), np.cos(t * om)], 1).ravel()

    kk = 7
    M = np.zeros((dm, dm))
    for i, w in enumerate(om):
        c, s = math.cos(kk * w), math.sin(kk * w)
        M[2 * i:2 * i + 2, 2 * i:2 * i + 2] = [[c, s], [-s, c]]
    sin_dev = max(float(np.abs(M @ pe(t) - pe(t + kk)).max()) for t in range(0, 300, 7))
    assert sin_dev < 1e-9
    pes = np.array([pe(t) for t in range(64)])
    return dict(theta=th, wavelength=2 * np.pi / th, dev=float(dev), r=r, decay=decay, rs=rs, smooth=smooth,
                scores=grid[:, 0], sin_dev=sin_dev, sin_k=kk, pe=pes, pe_dot=pes @ pes.T)


# ---------------------------------------------------------------------------
# Our transformer
# ---------------------------------------------------------------------------
def build_tf(K):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1, self.n2 = nn.LayerNorm(D), nn.LayerNorm(D)
            self.qkv = nn.Linear(D, 3 * D, bias=False)
            self.o = nn.Linear(D, D, bias=False)
            self.f1, self.f2 = nn.Linear(D, 4 * D), nn.Linear(4 * D, D)

        def attend(self, x, cos, sin, temp, keep):
            B, T, _ = x.shape
            q, k, v = self.qkv(self.n1(x)).view(B, T, 3, HEADS, DH).permute(2, 0, 3, 1, 4)

            def rot(t):
                a, b = t[..., : DH // 2], t[..., DH // 2:]
                return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

            q, k = rot(q) * temp, rot(k)
            if keep is None:
                a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
                return a, None, (q, k)
            s = (q @ k.transpose(-1, -2)) / math.sqrt(DH)
            s = s.masked_fill(~torch.ones(T, T, dtype=torch.bool).tril(), float("-inf"))
            p = torch.softmax(s, -1)
            return p @ v, (p if keep else None), (q, k)

        def forward(self, x, cos, sin, temp=1.0, keep=None):
            a, p, qk = self.attend(x, cos, sin, temp, keep)
            x = x + self.o(a.transpose(1, 2).reshape(x.shape))
            return x + self.f2(F.gelu(self.f1(self.n2(x)))), p, qk

    class TF(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(K, D)
            self.blocks = nn.ModuleList([Block() for _ in range(LAYERS)])
            self.nf = nn.LayerNorm(D)
            self.out = nn.Linear(D, K, bias=False)

        def forward(self, idx, theta=None, pos_scale=1.0, temp=1.0, keep=None):
            T = idx.shape[1]
            th = torch.tensor(rope_freqs() if theta is None else theta, dtype=torch.float32)
            ang = (torch.arange(T, dtype=torch.float32) / pos_scale)[:, None] * th[None]
            cos, sin = torch.cos(ang), torch.sin(ang)
            x = self.emb(idx)
            maps, qks = [], []
            for b in self.blocks:
                x, p, qk = b(x, cos, sin, temp, keep)
                maps.append(p)
                qks.append(qk)
            z = self.out(self.nf(x))
            return (z, maps, qks) if keep is not None else z

    return TF()


def corpus():
    import torch

    from videos.ai.ai1 import compute as c1

    texts = {k: c1.text(k) for k in ("train", "valid", "passage")}
    chars = sorted(set("".join(texts.values())))
    cp = np.array([ord(c) for c in chars])
    order = np.argsort(cp)

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return torch.tensor(order[np.searchsorted(cp[order], a)])

    return chars, enc, {k: enc(v) for k, v in texts.items()}


def tf_bits(model, seq, ctx=CTX, stride=None, **kw):
    """Bits per character on ``seq``: windows of ``ctx`` characters, ``stride`` apart; the first window is scored
    whole, each later one on its last ``stride`` characters (which have at least ctx - stride of context)."""
    import torch
    import torch.nn.functional as F

    stride = stride or ctx // 2
    starts = list(range(0, len(seq) - ctx, stride))
    tot, n = 0.0, 0
    with torch.no_grad():
        for i in range(0, len(starts), 16):
            ss = starts[i:i + 16]
            x = torch.stack([seq[s:s + ctx] for s in ss])
            y = torch.stack([seq[s + 1:s + ctx + 1] for s in ss])
            z = model(x, **kw)
            ce = F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1), reduction="none").view(len(ss), ctx)
            keep = torch.zeros_like(ce, dtype=torch.bool)
            keep[:, ctx - stride:] = True
            if i == 0:
                keep[0] = True
            tot += float(ce[keep].sum())
            n += int(keep.sum())
    return tot / n / math.log(2)


def tf_sample(model, chars, enc, prompt, n, seed, temperature=0.8):
    import torch

    gen = torch.Generator().manual_seed(seed)
    ctx = enc(prompt)
    outc = []
    with torch.no_grad():
        for _ in range(n):
            z = model(ctx[None, -CTX:])[0, -1]
            c = int(torch.multinomial(torch.softmax(z / temperature, 0), 1, generator=gen))
            ctx = torch.cat([ctx, torch.tensor([c])])
            outc.append(chars[c])
    return "".join(outc)


def head_mats(model, layer, head):
    """One head of our transformer as matrices on the residual stream (D numbers), with its layer norm's gain and
    centring folded in: W_QK (D x D, a query's and a key's residual vectors -> their score before rotation and
    1/sqrt(d)) and W_OV (D x D, a residual vector -> what the head writes back)."""
    b = model.blocks[layer]
    W = b.qkv.weight.detach().double().numpy()
    g = b.n1.weight.detach().double().numpy()
    P = np.eye(D) - 1.0 / D  # LayerNorm subtracts the mean
    fold = np.diag(g) @ P
    sl = slice(head * DH, (head + 1) * DH)
    Wq, Wk, Wv = W[:D][sl] @ fold, W[D:2 * D][sl] @ fold, W[2 * D:][sl] @ fold
    Wo = b.o.weight.detach().double().numpy()[:, sl]
    return Wq.T @ Wk, Wo @ Wv


def composition_scores(mats_by_head, L, H):
    """Elhage et al.'s composition scores between every head of an earlier layer and every head of a later one:
    Q, K and V composition, ||M W_OV^(1)||_F / (||M||_F ||W_OV^(1)||_F) with M = W_QK^T, W_QK, W_OV of the later
    head. Returns three (L*H, L*H) arrays (row: the earlier head, column: the later head; NaN where not earlier)."""
    n = L * H
    out = {k: np.full((n, n), np.nan) for k in ("q", "k", "v")}
    for a in range(n):
        for b_ in range(n):
            if a // H >= b_ // H:
                continue
            _, ov1 = mats_by_head[a]
            qk2, ov2 = mats_by_head[b_]
            n1 = np.linalg.norm(ov1)
            for key, M in (("q", qk2.T), ("k", qk2), ("v", ov2)):
                out[key][a, b_] = np.linalg.norm(M @ ov1) / (np.linalg.norm(M) * n1)
    return out


def composition_baseline(d, dh, draws=200, seed=0):
    """The composition score of random heads of the same shapes (Gaussian W_Q, W_K, W_V, W_O): mean and spread."""
    g = rng(seed)
    s = []
    for _ in range(draws):
        Wv, Wo = g.normal(size=(dh, d)), g.normal(size=(d, dh))
        Wq2, Wk2 = g.normal(size=(dh, d)), g.normal(size=(dh, d))
        ov1, qk2 = Wo @ Wv, Wq2.T @ Wk2
        s.append(np.linalg.norm(qk2 @ ov1) / (np.linalg.norm(qk2) * np.linalg.norm(ov1)))
    return float(np.mean(s)), float(np.std(s))


def tf_probe(model, chars, data, snip, copy_x):
    """What the transformer does at one moment of training: every head's attention on the passage's sentence, its
    copying of repeated text (bits on the first and second copy, and each head's induction and previous-character
    scores), how much attention the first position draws (sinks), and the heads' composition scores."""
    import torch
    import torch.nn.functional as F

    out = {}
    with torch.no_grad():
        _, maps, _ = model(snip[None], keep=True)
        out["maps"] = torch.stack([m[0] for m in maps]).numpy().astype(np.float16)  # layer, head, query, key
        z, maps, _ = model(copy_x, keep=True)
        n = copy_x.shape[1] // 2
        ce = F.cross_entropy(z[:, :-1].reshape(-1, z.shape[-1]), copy_x[:, 1:].reshape(-1), reduction="none")
        ce = ce.view(len(copy_x), -1).numpy() / math.log(2)  # position i predicts character i + 1
        out["copy1"] = float(ce[:, 4:n - 1].mean())  # predicting characters 5 ... n-1 of the first copy
        out["copy2"] = float(ce[:, n + 4:2 * n - 1].mean())  # the same characters, the second time
        ind, prev = np.zeros((LAYERS, HEADS)), np.zeros((LAYERS, HEADS))
        for l_, m in enumerate(maps):
            P = m.numpy()  # batch, head, query, key
            ind[l_] = np.mean([P[:, :, n + j, j + 1] for j in range(4, n - 1)], axis=(0, 1))
            prev[l_] = np.mean([P[:, :, i, i - 1] for i in range(1, 2 * n)], axis=(0, 1))
        out["induction"], out["prev"] = ind, prev
        # attention on the first position, from queries 64 ... 255, over 8 windows of held-out text
        va = data["valid"]
        starts = rng(11).integers(0, len(va) - CTX - 1, 8)
        x = torch.stack([va[s:s + CTX] for s in starts])
        _, maps, _ = model(x, keep=True)
        out["sink"] = np.array([m[:, :, 64:, 0].mean((0, 2)).numpy() for m in maps])
    mats = [head_mats(model, l_, h) for l_ in range(LAYERS) for h in range(HEADS)]
    comp = composition_scores(mats, LAYERS, HEADS)
    out.update({f"comp_{k}": v for k, v in comp.items()})
    return out


def tf_setup():
    """The fixed inputs of the transformer's probes: a sentence of the passage, and repeated stretches of held-out
    text (100 characters, shown twice)."""
    import torch

    chars, enc, data = corpus()
    ps, va = data["passage"], data["valid"]
    text = "".join(chars[int(i)] for i in ps[:4000])
    s0 = text.index(". ", 400) + 2
    snip = ps[s0:s0 + 64]
    g = rng(77)
    n = 100
    starts = g.integers(0, len(va) - n - 1, 16)
    copy_x = torch.stack([torch.cat([va[s:s + n], va[s:s + n]]) for s in starts])
    return chars, enc, data, snip, copy_x


def compute_tf():
    import torch
    import torch.nn.functional as F

    threads()
    torch.manual_seed(2017)  # Vaswani et al., Attention Is All You Need
    chars, enc, data, snip, copy_x = tf_setup()
    K = len(chars)
    tr, va, ps = data["train"], data["valid"], data["passage"]
    model = build_tf(K)
    n_params = sum(p.numel() for p in model.parameters())
    config = dict(K=K, ctx=CTX, d=D, layers=LAYERS, heads=HEADS, steps=STEPS, batch=BATCH, snaps=list(TF_SNAPS))
    saved = CACHE.dir / "tf.pt"
    meta = CACHE.dir / "tf_train.pt"  # the curve and the replay, kept with the weights so analysis can be redone
    if saved.exists() and meta.exists() and torch.load(meta, weights_only=False)["config"] == config:
        model.load_state_dict(torch.load(saved))
        m_ = torch.load(meta, weights_only=False)
        curve, snaps = m_["curve"], m_["snaps"]
        print("    reusing the trained weights in", saved, flush=True)
    else:
        decay = [p for n_, p in model.named_parameters() if p.dim() >= 2]
        other = [p for n_, p in model.named_parameters() if p.dim() < 2]
        opt = torch.optim.AdamW([dict(params=decay, weight_decay=0.1), dict(params=other, weight_decay=0.0)],
                                lr=2e-3, betas=(0.9, 0.95))
        warm, cool = 200, int(0.2 * STEPS)  # Part 11's warmup-stable-decay schedule

        def lr_at(s):
            if s < warm:
                return (s + 1) / warm
            if s < STEPS - cool:
                return 1.0
            return 0.05 + 0.95 * (STEPS - s) / cool

        sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_at)
        g = rng(2017)
        ckpt = CACHE.dir / "tf.ckpt.pt"
        ck = torch.load(ckpt, weights_only=False) if ckpt.exists() else None
        if ck is not None and ck["config"] == config:
            model.load_state_dict(ck["model"])
            opt.load_state_dict(ck["opt"])
            sched.load_state_dict(ck["sched"])
            g.bit_generator.state = ck["rng"]
            torch.set_rng_state(ck["torch_rng"])
            curve, snaps, start = ck["curve"], ck["snaps"], ck["step"] + 1
            print(f"    resuming at step {start}", flush=True)
        else:
            curve, snaps, start = [], [], 1

        def checkpoint(step):
            model.eval()
            if step in (0, 50, 100) or step % 250 == 0:
                curve.append((step, tf_bits(model, va[:60_000]), tf_bits(model, ps)))
                print(f"    step {step}: valid {curve[-1][1]:.3f}  passage {curve[-1][2]:.3f}  "
                      f"({(time.time() - t0) / max(step - start + 1, 1):.2f}s/step)", flush=True)
            if step in TF_SNAPS:
                pr = tf_probe(model, chars, data, snip, copy_x)
                bits = curve[-1][2] if curve and curve[-1][0] == step else tf_bits(model, ps)
                pr.update(step=step, bits=bits, sample=tf_sample(model, chars, enc, PROMPT, 100, seed=1))
                snaps.append(pr)
            model.train()

        t0 = time.time()
        if start == 1:
            checkpoint(0)
        model.train()
        for step in range(start, STEPS + 1):
            st = torch.tensor(g.integers(0, len(tr) - CTX - 1, BATCH))
            idx = st[:, None] + torch.arange(CTX + 1)[None]
            x, y = tr[idx[:, :-1]], tr[idx[:, 1:]]
            loss = F.cross_entropy(model(x).reshape(-1, K), y.reshape(-1))
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            checkpoint(step)
            if step % TF_CKPT == 0 and step < STEPS:
                tmp = ckpt.with_suffix(".tmp")
                torch.save(dict(config=config, model=model.state_dict(), opt=opt.state_dict(),
                                sched=sched.state_dict(), rng=g.bit_generator.state, torch_rng=torch.get_rng_state(),
                                curve=curve, snaps=snaps, step=step), tmp)
                tmp.replace(ckpt)
        model.eval()
        torch.save(model.state_dict(), saved)
        torch.save(dict(config=config, curve=curve, snaps=snaps), meta)
        ckpt.unlink(missing_ok=True)
    model.eval()
    passage_bits, valid_bits = tf_bits(model, ps), tf_bits(model, va[:400_000])
    out = dict(K=K, ctx=CTX, d=D, layers=LAYERS, heads=HEADS, n_params=int(n_params), steps=STEPS, batch=BATCH,
               tokens=STEPS * BATCH * CTX, curve=np.array(curve), passage_bits=passage_bits, valid_bits=valid_bits)
    # the replay: one array per probe, stacked over the checkpoints
    out["snap_steps"] = [int(s["step"]) for s in snaps]
    out["snap_bits"] = [float(s["bits"]) for s in snaps]
    out["snap_samples"] = [s["sample"] for s in snaps]
    for k in ("maps", "induction", "prev", "sink", "comp_q", "comp_k", "comp_v"):
        out[f"snap_{k}"] = np.array([s[k] for s in snaps])
    out["snap_copy1"] = [float(s["copy1"]) for s in snaps]
    out["snap_copy2"] = [float(s["copy2"]) for s in snaps]
    out["prompt"] = PROMPT
    out.update(analyse_tf(model, chars, enc, data, snip, copy_x))
    return out


def analyse_tf(model, chars, enc, data, snip, copy_x):
    import torch
    import torch.nn.functional as F

    va = data["valid"]
    out = {}
    # attention maps on a sentence of the passage (its first 64 characters after a sentence start)
    with torch.no_grad():
        z, maps, qks = model(snip[None], keep=True)
    out["snip"] = "".join(chars[int(i)] for i in snip)
    out["maps"] = torch.stack([m[0] for m in maps]).numpy()  # layer, head, query, key
    # every head's query and key vectors on the snippet (after rotation), for the geometry picture
    out["q"] = torch.stack([qk[0][0] for qk in qks]).numpy()  # layer, head, position, DH
    out["k"] = torch.stack([qk[1][0] for qk in qks]).numpy()
    # attention by distance, and the first position's share (attention sinks), over windows of held-out text
    g = rng(11)
    starts = g.integers(0, len(va) - CTX - 1, 48)
    dist = np.zeros((LAYERS, HEADS, CTX))
    first = np.zeros((LAYERS, HEADS))
    top_key = np.zeros((LAYERS, HEADS))  # the share of the single most-attended key, averaged over queries
    space = np.zeros((LAYERS, HEADS))  # attention on spaces and line breaks, against their share of the keys
    sp_ids = torch.tensor([chars.index(c) for c in (" ", "\n") if c in chars])
    sp_share = 0.0
    qnorm = np.zeros((LAYERS, HEADS, DH // 2))  # each rotation pair's share of the queries' and keys' size
    knorm = np.zeros((LAYERS, HEADS, DH // 2))
    with torch.no_grad():
        for i in range(0, len(starts), 8):
            x = torch.stack([va[s:s + CTX] for s in starts[i:i + 8]])
            _, maps, qks = model(x, keep=True)
            is_sp = torch.isin(x, sp_ids).numpy()  # batch, key
            sp_share += float(is_sp[:, 64:].mean()) * len(x)
            for l_, m in enumerate(maps):
                P = m.numpy()  # batch, head, query, key
                for d_ in range(CTX):
                    dist[l_, :, d_] += np.einsum("bhq->h", np.diagonal(P, offset=-d_, axis1=2, axis2=3)) / (CTX - d_)
                first[l_] += P[:, :, 64:, 0].mean((0, 2)) * len(x)
                top_key[l_] += P[:, :, 64:, :].max(-1).mean((0, 2)) * len(x)
                space[l_] += np.einsum("bhqk,bk->bhq", P[:, :, 64:, :], is_sp.astype(float)).mean((0, 2)) * len(x)
                q_, k_ = qks[l_]
                for nm, t_, acc in (("q", q_, qnorm), ("k", k_, knorm)):
                    t_ = t_.numpy()
                    e = t_[..., : DH // 2] ** 2 + t_[..., DH // 2:] ** 2  # each pair's squared size (rotation-proof)
                    acc[l_] += e.mean((0, 2)) * len(x)
    out["by_dist"] = dist / len(starts)
    out["sink"] = first / len(starts)  # mean attention on position 0, for queries at positions 64 ... 255
    out["sink_uniform"] = float(np.mean(1 / (np.arange(64, CTX) + 1)))
    out["top_key"] = top_key / len(starts)
    out["space_att"] = space / len(starts)
    out["space_share"] = sp_share / len(starts)
    out["pair_q"] = qnorm / len(starts)
    out["pair_k"] = knorm / len(starts)
    # in-context copying: a random string of lowercase letters, shown twice; and repeated held-out text
    letters = [chars.index(c) for c in "abcdefghijklmnopqrstuvwxyz"]
    L = 60
    bits1, bits2, ind = [], [], np.zeros((LAYERS, HEADS))
    with torch.no_grad():
        for t in range(24):
            r = torch.tensor(np.asarray(letters)[rng(500 + t).integers(0, 26, L)])
            x = torch.cat([r, r])[None]
            z, maps, _ = model(x, keep=True)
            ce = F.cross_entropy(z[0, :-1], x[0, 1:], reduction="none").numpy() / math.log(2)
            bits1.append(ce[: L - 1])
            bits2.append(ce[L:])
            for l_, m in enumerate(maps):  # induction: from the 2nd copy's position i to the 1st copy's i + 1
                P = m[0].numpy()
                ind[l_] += np.mean([P[:, L + i, i + 1] for i in range(L - 1)], axis=0)
        out["copy_bits1"] = np.mean(bits1, 0)
        out["copy_bits2"] = np.mean(bits2, 0)
        out["induction_score"] = ind / 24
        li, hi = np.unravel_index(np.argmax(out["induction_score"]), out["induction_score"].shape)
        out["ind_layer"], out["ind_head"] = int(li), int(hi)
        r = torch.tensor(np.asarray(letters)[rng(9).integers(0, 26, 24)])
        x = torch.cat([r, r])[None]
        _, maps, _ = model(x, keep=True)
        out["ind_text"] = "".join(chars[int(i)] for i in x[0])
        out["ind_map"] = maps[li][0, hi].numpy()
        # repeated held-out text: bits by position on both copies, and the best induction head's map on one
        z, maps, _ = model(copy_x, keep=True)
        n = copy_x.shape[1] // 2
        ce = F.cross_entropy(z[:, :-1].reshape(-1, z.shape[-1]), copy_x[:, 1:].reshape(-1), reduction="none")
        ce = ce.view(len(copy_x), -1).numpy() / math.log(2)
        out["text_bits1"], out["text_bits2"] = ce[:, : n - 1].mean(0), ce[:, n:].mean(0)
        nind = np.zeros((LAYERS, HEADS))
        for l_, m in enumerate(maps):
            P = m.numpy()
            nind[l_] = np.mean([P[:, :, n + j, j + 1] for j in range(4, n - 1)], axis=(0, 1))
        out["text_induction"] = nind
        li2, hi2 = np.unravel_index(np.argmax(nind), nind.shape)
        out["text_ind_layer"], out["text_ind_head"] = int(li2), int(hi2)
        out["text_ind_map"] = maps[li2][0, hi2].numpy().astype(np.float32)
        out["text_ind_text"] = "".join(chars[int(i)] for i in copy_x[0])
    # samples
    out["samples"] = [[p, tf_sample(model, chars, enc, p, 200, seed)]
                      for seed, p in ((1, PROMPT), (2, "It was the best of times, "), (3, "The telephone rang. "),
                                      (4, "\"I don't know,\" he said. "))]
    return out


def load_tf():
    import torch

    chars, enc, data = corpus()
    model = build_tf(len(chars))
    model.load_state_dict(torch.load(CACHE.dir / "tf.pt"))
    model.eval()
    return model, chars, enc, data


# ---------------------------------------------------------------------------
def yarn_theta(s, L=CTX, alpha=1.0, beta=32.0):
    """YaRN's 'NTK-by-parts': fast-turning pairs keep their angles, slow ones are interpolated, a ramp between."""
    th = rope_freqs()
    r = L / (2 * np.pi / th)  # how many turns each pair makes over the training context
    gam = np.clip((r - alpha) / (beta - alpha), 0, 1)
    return (1 - gam) * th / s + gam * th, gam


def compute_extend():
    import torch
    import torch.nn.functional as F

    threads()
    load("tf")
    model, chars, enc, data = load_tf()
    va = data["valid"]
    s = 4
    T = s * CTX
    g = rng(3)
    starts = g.integers(0, len(va) - T - 1, 32)
    th = rope_freqs()
    ntk = rope_freqs(base=BASE * s ** (DH / (DH - 2)))
    yth, gam = yarn_theta(s)
    methods = {
        "plain": dict(),
        "pi": dict(pos_scale=float(s)),
        "ntk": dict(theta=ntk),
        "yarn": dict(theta=yth, temp=(0.1 * math.log(s) + 1) ** 2),
    }
    out = dict(s=s, T=T, theta=th, theta_ntk=ntk, theta_yarn=yth, ramp=gam, buckets=list(range(0, T + 1, 64)))
    with torch.no_grad():
        x = torch.stack([va[a:a + T] for a in starts])
        y = torch.stack([va[a + 1:a + T + 1] for a in starts])
        for name, kw in methods.items():
            ce = np.zeros(T)
            for i in range(0, len(x), 4):
                z = model(x[i:i + 4], **kw)
                ce += F.cross_entropy(z.reshape(-1, z.shape[-1]), y[i:i + 4].reshape(-1),
                                      reduction="none").view(-1, T).sum(0).numpy()
            ce = ce / len(x) / math.log(2)
            out[f"pos_{name}"] = ce
            out[f"bucket_{name}"] = [float(ce[a:a + 64].mean()) for a in range(0, T, 64)]
            print(f"    {name}: " + " ".join(f"{v:.2f}" for v in out[f"bucket_{name}"]), flush=True)
        # the honest baseline: the model as trained, always on the last 256 characters
        base = []
        for a in range(0, T, 64):
            if a + 64 <= CTX:
                base.append(out["bucket_plain"][a // 64])
                continue
            xs = torch.stack([x[:, b - CTX + 1:b + 1] for b in range(a, a + 64)], 1).reshape(-1, CTX)
            ys = torch.stack([y[:, b] for b in range(a, a + 64)], 1).reshape(-1)
            tot = 0.0
            for i in range(0, len(xs), 256):
                z = model(xs[i:i + 256])[:, -1]
                tot += float(F.cross_entropy(z, ys[i:i + 256], reduction="sum"))
            base.append(tot / len(xs) / math.log(2))
        out["bucket_window"] = base
    plain_far = np.mean(out["bucket_plain"][-4:])
    assert plain_far > np.mean(out["bucket_plain"][:4]) + 0.3  # beyond its training length, it breaks
    return out


# ---------------------------------------------------------------------------
def compute_induction():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    threads()
    V, T, Dm, H = 64, 96, 64, 4

    def batch(g, n):
        x = g.integers(0, V, (n, T))
        mask = np.zeros((n, T), bool)  # positions whose next token is predictable from the repeat
        for b in range(n):
            ln = int(g.integers(12, 30))
            src = int(g.integers(0, T // 2 - ln))
            dst = int(g.integers(src + ln + 1, T - ln + 1))
            x[b, dst:dst + ln] = x[b, src:src + ln]
            mask[b, dst:dst + ln - 1] = True  # predicting dst + 1 ... from the copy
        return torch.tensor(x), torch.tensor(mask)

    class AttnOnly(nn.Module):
        def __init__(self, layers):
            super().__init__()
            self.emb = nn.Embedding(V, Dm)
            self.pos = nn.Parameter(torch.randn(T, Dm) * 0.1)
            self.qkv = nn.ModuleList([nn.Linear(Dm, 3 * Dm, bias=False) for _ in range(layers)])
            self.o = nn.ModuleList([nn.Linear(Dm, Dm, bias=False) for _ in range(layers)])
            self.out = nn.Linear(Dm, V, bias=False)

        def forward(self, x, keep=False):
            B = x.shape[0]
            h = self.emb(x) + self.pos[None]
            maps = []
            for qkv, o in zip(self.qkv, self.o):
                q, k, v = qkv(h).view(B, T, 3, H, Dm // H).permute(2, 0, 3, 1, 4)
                s = (q @ k.transpose(-1, -2)) / math.sqrt(Dm // H)
                s = s.masked_fill(~torch.ones(T, T, dtype=torch.bool).tril(), float("-inf"))
                p = torch.softmax(s, -1)
                maps.append(p)
                h = h + o((p @ v).transpose(1, 2).reshape(B, T, Dm))
            z = self.out(h)
            return (z, maps) if keep else z

        def mats(self, layer, head):
            W = self.qkv[layer].weight.detach().double().numpy()
            sl = slice(head * (Dm // H), (head + 1) * (Dm // H))
            Wq, Wk, Wv = W[:Dm][sl], W[Dm:2 * Dm][sl], W[2 * Dm:][sl]
            Wo = self.o[layer].weight.detach().double().numpy()[:, sl]
            return Wq.T @ Wk, Wo @ Wv

    out = dict(V=V, T=T, d=Dm, H=H)
    test_x, test_m = batch(rng(99), 128)
    seeds = (2022, 2023, 2024)
    part = CACHE.partial("induction", dict(V=V, T=T, d=Dm, H=H, steps=5000, seeds=list(seeds)))
    for layers, seed in [(1, 2022)] + [(2, s_) for s_ in seeds]:
        key = f"{layers}_{seed}"
        if key in part:
            r = part[key]
        else:
            torch.manual_seed(seed)  # Olsson et al., In-context Learning and Induction Heads (2022)
            m = AttnOnly(layers)
            opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=0.01)
            g = rng(seed)
            steps, curve = 5000, []
            ex_ = torch.tensor(rng(7).integers(0, V, T))
            ex_[60:80] = ex_[10:30]
            snaps, comp = [], []
            for step in range(steps + 1):
                if layers == 2 and step % 250 == 0:  # how it learns: both layers' attention on the example
                    with torch.no_grad():
                        _, mp = m(ex_[None], keep=True)
                    snaps.append((step, mp[0][0].numpy().astype(np.float16).tolist(),
                                  mp[1][0].numpy().astype(np.float16).tolist()))
                    mats = [m.mats(l_, h) for l_ in range(2) for h in range(H)]
                    cs = composition_scores(mats, 2, H)
                    comp.append([step, cs["k"][:H, H:].tolist(), cs["q"][:H, H:].tolist(), cs["v"][:H, H:].tolist()])
                if step % 100 == 0:
                    with torch.no_grad():
                        z = m(test_x)
                        ce = F.cross_entropy(z[:, :-1].reshape(-1, V), test_x[:, 1:].reshape(-1), reduction="none")
                        ce = ce.view(len(test_x), T - 1) / math.log(2)
                        mk = test_m[:, :-1]
                        curve.append((step, float(ce[mk].mean()), float(ce[~mk].mean())))
                if step == steps:
                    break
                x, _ = batch(g, 64)
                z = m(x)
                loss = F.cross_entropy(z[:, :-1].reshape(-1, V), x[:, 1:].reshape(-1))
                opt.zero_grad()
                loss.backward()
                opt.step()
            r = dict(curve=curve)
            print(f"    {layers} layer(s), seed {seed}: repeat {curve[0][1]:.2f} -> {curve[-1][1]:.2f} bits", flush=True)
            if layers == 2:
                # the two heads, scored over 64 examples: previous-token heads in layer 1, induction heads in layer 2
                xb, mb = batch(rng(123), 64)
                with torch.no_grad():
                    _, maps = m(xb, keep=True)
                P1, P2 = maps[0].numpy(), maps[1].numpy()  # batch, head, query, key
                prev = [float(np.mean([P1[:, h, i, i - 1] for i in range(1, T)])) for h in range(H)]
                ind = np.zeros(H)
                cnt = 0
                xn = xb.numpy()
                for b in range(len(xn)):
                    for p in np.where(mb[b].numpy())[0]:
                        src = [j for j in range(p) if xn[b, j] == xn[b, p] and j + 1 < p]
                        if src:  # the earlier copy of this token: attend to the position just after it
                            ind += P2[b, :, p, src[0] + 1]
                            cnt += 1
                ind = list(ind / max(cnt, 1))
                hp, hi = int(np.argmax(prev)), int(np.argmax(ind))
                with torch.no_grad():
                    _, maps1 = m(ex_[None], keep=True)
                r.update(prev_scores=prev, ind_scores=ind, prev_head=hp, ind_head=hi,
                         map_prev=maps1[0][0, hp].numpy().tolist(), map_ind=maps1[1][0, hi].numpy().tolist(),
                         snaps=snaps, comp=comp)
                print(f"      previous-token {np.round(prev, 2)}; induction {np.round(ind, 2)}", flush=True)
            part[key] = r
    ex = np.asarray(rng(7).integers(0, V, T))
    ex[60:80] = ex[10:30]
    out["ex"] = ex
    out["curve1"] = np.array(part["1_2022"]["curve"])
    out["seeds"] = list(seeds)
    for s_ in seeds:
        out[f"curve2_{s_}"] = np.array(part[f"2_{s_}"]["curve"])
    r = part["2_2022"]  # the replayed run: the first seed (all three are shown together elsewhere)
    out["curve2"] = np.array(r["curve"])
    out.update(prev_scores=r["prev_scores"], ind_scores=r["ind_scores"], prev_head=r["prev_head"],
               ind_head=r["ind_head"], map_prev=np.array(r["map_prev"]), map_ind=np.array(r["map_ind"]))
    out["snap_steps"] = [a for a, _, _ in r["snaps"]]
    out["snap_l1"] = np.array([b for _, b, _ in r["snaps"]], dtype=np.float32)  # (checkpoints, heads, query, key)
    out["snap_l2"] = np.array([c for _, _, c in r["snaps"]], dtype=np.float32)
    out["comp_steps"] = [c[0] for c in r["comp"]]
    out["comp_k"] = np.array([c[1] for c in r["comp"]])  # checkpoint, layer-1 head, layer-2 head
    out["comp_q"] = np.array([c[2] for c in r["comp"]])
    out["comp_v"] = np.array([c[3] for c in r["comp"]])
    out["comp_base"], out["comp_base_sd"] = composition_baseline(Dm, Dm // H)
    # the jump: where each seed's loss on the repeat falls fastest
    out["jump_steps"] = []
    for s_ in seeds:
        c2 = out[f"curve2_{s_}"]
        d = np.diff(c2[:, 1])
        out["jump_steps"].append(int(c2[int(np.argmin(d)) + 1, 0]))
    out["jump_step"] = out["jump_steps"][0]
    out["final2"] = [float(out[f"curve2_{s_}"][-1, 1]) for s_ in seeds]
    return out


# ---------------------------------------------------------------------------
def compute_icl():
    import torch

    threads()
    d, N = 4, 20

    def tasks(g, n):
        w = g.normal(size=(n, d))
        x = g.normal(size=(n, N + 1, d))
        y = np.einsum("nd,ntd->nt", w, x)
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

    def lsa(params, x, y):
        """Linear self-attention layers on tokens (x_i, y_i); the query token is (x_q, 0); prediction: its last entry."""
        e = torch.cat([x, torch.cat([y[:, :N], torch.zeros_like(y[:, N:])], 1)[..., None]], -1)
        for Wkq, Wpv in params:
            ctx = e[:, :N]
            att = ctx @ Wkq @ e.transpose(1, 2) / N  # (context i, every token j)
            e = e + (att.transpose(1, 2) @ (ctx @ Wpv.T))
        return e[:, N, -1]

    def gd(x, y, steps, eta):
        w = torch.zeros(x.shape[0], d)
        X, Y = x[:, :N], y[:, :N]
        for _ in range(steps):
            r = torch.einsum("nd,ntd->nt", w, X) - Y
            w = w - eta * torch.einsum("nt,ntd->nd", r, X) / N
        return torch.einsum("nd,nd->n", w, x[:, N])

    xt, yt = tasks(rng(1), 4000)
    out = dict(d=d, N=N)
    for layers in (1, 2, 3):
        torch.manual_seed(2023)  # von Oswald et al., Transformers Learn In-Context by Gradient Descent
        params = [(torch.nn.Parameter(torch.randn(d + 1, d + 1) * 0.05), torch.nn.Parameter(torch.randn(d + 1, d + 1) * 0.05))
                  for _ in range(layers)]
        opt = torch.optim.Adam([p for pr in params for p in pr], lr=3e-3)
        g = rng(2023)
        curve = []
        for step in range(6000):
            x, y = tasks(g, 256)
            loss = ((lsa(params, x, y) - y[:, N]) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if layers == 1 and step % 200 == 0:
                curve.append((step, float(loss)))
        with torch.no_grad():
            pred = lsa(params, xt, yt)
            out[f"lsa{layers}"] = float(((pred - yt[:, N]) ** 2).mean())
            etas = np.linspace(0.05, 1.5, 59)
            errs = [float(((gd(xt, yt, layers, e) - yt[:, N]) ** 2).mean()) for e in etas]
            eta = float(etas[int(np.argmin(errs))])
            out[f"gd{layers}"] = min(errs)
            out[f"eta{layers}"] = eta
            gp = gd(xt, yt, layers, eta)
            out[f"agree{layers}"] = float(torch.corrcoef(torch.stack([pred, gp]))[0, 1])
            if layers == 1:
                out["Wkq"], out["Wpv"] = params[0][0].detach().numpy(), params[0][1].detach().numpy()
                out["pred_lsa"], out["pred_gd"], out["truth"] = pred[:200].numpy(), gp[:200].numpy(), yt[:200, N].numpy()
                out["curve1"] = np.array(curve)
        print(f"    {layers} layer(s): lsa {out[f'lsa{layers}']:.3f}  gd {out[f'gd{layers}']:.3f}  "
              f"agree {out[f'agree{layers}']:.4f}", flush=True)
    out["zero"] = float((yt[:, N] ** 2).mean())  # always guessing 0
    # least squares on the 20 examples: exact here (no noise, 20 > 4)
    X, Y = xt[:, :N].numpy(), yt[:, :N].numpy()
    w = np.stack([np.linalg.lstsq(X[i], Y[i], rcond=None)[0] for i in range(len(X))])
    out["lstsq"] = float(((np.einsum("nd,nd->n", w, xt[:, N].numpy()) - yt[:, N].numpy()) ** 2).mean())
    return out


ITEMS = {
    "smoother": compute_smoother,
    "dotscale": compute_dotscale,
    "rope": compute_rope,
    "tf": compute_tf,
    "extend": compute_extend,
    "induction": compute_induction,
    "icl": compute_icl,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
