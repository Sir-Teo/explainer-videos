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
    sig = np.exp(np.linspace(np.log(0.1), np.log(300), 60))
    qq = g.normal(size=(trials, n))
    out["sig"] = sig
    out["jac_by_sig"] = np.array([stats(qq * s_)[2] for s_ in sig])
    out["ent_by_sig"] = np.array([stats(qq * s_)[0] for s_ in sig])
    assert abs(out["sd"][-1] / math.sqrt(ds[-1]) - 1) < 0.05  # the scores spread like sqrt(d)
    return out


# ---------------------------------------------------------------------------
GLYPHS = {  # ten letters on a 10 x 10 grid, drawn by hand (so every machine stores the same patterns)
    "A": ["...####...", "..##..##..", ".##....##.", ".##....##.", ".##....##.", ".########.", ".##....##.",
          ".##....##.", ".##....##.", ".##....##."],
    "E": [".########.", ".##.......", ".##.......", ".##.......", ".#######..", ".##.......", ".##.......",
          ".##.......", ".##.......", ".########."],
    "H": [".##....##.", ".##....##.", ".##....##.", ".##....##.", ".########.", ".########.", ".##....##.",
          ".##....##.", ".##....##.", ".##....##."],
    "K": [".##....##.", ".##...##..", ".##..##...", ".##.##....", ".####.....", ".####.....", ".##.##....",
          ".##..##...", ".##...##..", ".##....##."],
    "M": ["##......##", "###....###", "####..####", "##.####.##", "##..##..##", "##......##", "##......##",
          "##......##", "##......##", "##......##"],
    "O": ["..######..", ".##....##.", "##......##", "##......##", "##......##", "##......##", "##......##",
          "##......##", ".##....##.", "..######.."],
    "S": ["..######..", ".##....##.", ".##.......", "..##......", "...####...", "......##..", ".......##.",
          ".......##.", ".##....##.", "..######.."],
    "T": ["##########", "##########", "....##....", "....##....", "....##....", "....##....", "....##....",
          "....##....", "....##....", "....##...."],
    "X": ["##......##", ".##....##.", "..##..##..", "...####...", "....##....", "...####...", "..##..##..",
          ".##....##.", "##......##", "#........#"],
    "Z": ["##########", "##########", ".......##.", "......##..", ".....##...", "....##....", "...##.....",
          "..##......", "##########", "##########"],
}


def glyphs():
    """The letters as patterns of +1 (ink) and -1 (paper), 100 numbers each."""
    return np.array([[1.0 if c == "#" else -1.0 for row in GLYPHS[k] for c in row] for k in GLYPHS])


def compute_hopfield():
    """Classical (Hopfield 1982) against modern (Ramsauer et al. 2020) associative memory."""
    g = rng(1982)  # Hopfield, Neural networks and physical systems with emergent collective computational abilities
    N = 100  # neurons (numbers per pattern)
    flip = 0.15  # the cue: a stored pattern with 15% of its signs flipped
    trials = 60
    Ms = [2, 4, 6, 8, 10, 12, 14, 16, 20, 25, 30, 40, 60, 80, 120, 160, 240, 320]

    def classical(X, x, sweeps=20):
        W = X.T @ X / N
        np.fill_diagonal(W, 0)
        x = x.copy()
        for _ in range(sweeps):  # asynchronous updates, in a random order
            old = x.copy()
            for i in g.permutation(N):
                h = W[i] @ x
                x[i] = 1.0 if h >= 0 else -1.0
            if np.array_equal(old, x):
                break
        return x

    def modern(X, x, beta, steps=1):
        for _ in range(steps):  # xi <- X^T softmax(beta X xi): one step of attention, the cue as the query
            s = beta * (X @ x)
            p = np.exp(s - s.max())
            x = X.T @ (p / p.sum())
        return np.sign(x)

    beta = 0.25  # patterns have length sqrt(N) = 10: attention's 1/sqrt(d) would be 0.1
    out = dict(N=N, flip=flip, trials=trials, Ms=Ms, classical=[], modern=[], beta=beta)
    for M in Ms:
        ok_c, ok_m = 0, 0
        for _ in range(trials):
            X = g.choice([-1.0, 1.0], size=(M, N))
            mu = int(g.integers(M))
            x = X[mu].copy()
            idx = g.choice(N, int(flip * N), replace=False)
            x[idx] *= -1
            ok_c += np.array_equal(classical(X, x), X[mu])
            ok_m += np.array_equal(modern(X, x, beta), X[mu])
        out["classical"].append(ok_c / trials)
        out["modern"].append(ok_m / trials)
        print(f"    M = {M}: classical {ok_c / trials:.2f}, modern {ok_m / trials:.2f}", flush=True)
    # the inverse temperature: from the average of everything (small beta) to one pattern (large beta)
    X = g.choice([-1.0, 1.0], size=(20, N))
    x = X[3].copy()
    x[g.choice(N, 30, replace=False)] *= -1
    betas = np.exp(np.linspace(np.log(0.002), np.log(1.0), 40))
    weights, overlap = [], []
    for b in betas:
        s = b * (X @ x)
        p = np.exp(s - s.max())
        p /= p.sum()
        weights.append(p)
        overlap.append(float((X.T @ p) @ X[3] / N))
    out.update(betas=betas, beta_weights=np.array(weights), beta_overlap=np.array(overlap), beta_target=3)
    # letters: stored as 144-pixel patterns, recalled from a corrupted cue by one softmax step and by the classical net
    L = glyphs()
    out["letters"] = L
    gl = rng(7)
    cues, rec_c, rec_m = [], [], []
    for i in range(len(L)):
        x = L[i].copy()
        x[gl.choice(len(x), int(0.25 * len(x)), replace=False)] *= -1
        cues.append(x)
        Wc = L.T @ L / len(x)
        np.fill_diagonal(Wc, 0)
        y = x.copy()
        for _ in range(20):
            old = y.copy()
            for j in gl.permutation(len(y)):
                y[j] = 1.0 if Wc[j] @ y >= 0 else -1.0
            if np.array_equal(old, y):
                break
        rec_c.append(y)
        s = 0.2 * (L @ x)
        p = np.exp(s - s.max())
        rec_m.append(np.sign(L.T @ (p / p.sum())))
    out.update(cues=np.array(cues), rec_classical=np.array(rec_c), rec_modern=np.array(rec_m))
    out["letters_ok_classical"] = int(sum(np.array_equal(a, b) for a, b in zip(rec_c, L)))
    out["letters_ok_modern"] = int(sum(np.array_equal(a, b) for a, b in zip(rec_m, L)))
    out["capacity_classical"] = 0.138 * N  # Amit, Gutfreund & Sompolinsky (1985), for comparison
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


def compute_tfwords():
    """How much of what the transformer writes at each checkpoint of its training are real words: the share of its
    words (runs of three or more letters) that occur in the training text."""
    import re

    from videos.ai.ai1 import compute as c1

    t = load("tf")
    vocab = set(re.findall(r"[A-Za-z]{3,}", c1.text("train")))
    out = dict(steps=list(t["snap_steps"]), real=[], words=[])
    for smp in t["snap_samples"]:
        ws = re.findall(r"[A-Za-z]{3,}", str(smp))
        out["words"].append(len(ws))
        out["real"].append(float(np.mean([w in vocab for w in ws])) if ws else 0.0)
    return out


# ---------------------------------------------------------------------------
def compute_heads():
    """Our transformer's heads as low-rank maps, its composition scores, the causal mask checked, and its cost."""
    import torch
    import torch.nn.functional as F
    from torch.utils.flop_counter import FlopCounterMode

    threads()
    load("tf")
    model, chars, enc, data = load_tf()
    K = len(chars)
    out = dict(L=LAYERS, H=HEADS, d=D, dh=DH, K=K)
    # 1. every head's two matrices on the residual stream, and their singular values
    sv_qk, sv_ov, layer_qk = np.zeros((LAYERS, HEADS, D)), np.zeros((LAYERS, HEADS, D)), np.zeros((LAYERS, D))
    mats = []
    for l_ in range(LAYERS):
        tot = np.zeros((D, D))
        for h in range(HEADS):
            qk, ov = head_mats(model, l_, h)
            mats.append((qk, ov))
            sv_qk[l_, h] = np.linalg.svd(qk, compute_uv=False)
            sv_ov[l_, h] = np.linalg.svd(ov, compute_uv=False)
            tot += qk
        layer_qk[l_] = np.linalg.svd(tot, compute_uv=False)
    out.update(sv_qk=sv_qk, sv_ov=sv_ov, layer_qk=layer_qk)
    rel = sv_qk / sv_qk[..., :1]
    out["rank_qk"] = int((rel > 1e-9).sum(-1).max())  # numerically nonzero singular values: at most d_head
    out["rank_ov"] = int((sv_ov / sv_ov[..., :1] > 1e-9).sum(-1).max())
    out["layer_rank"] = int((layer_qk / layer_qk[:, :1] > 1e-9).sum(-1).min())

    def k90(sv):  # singular values needed for 90% of the matrix's squared size
        c = np.cumsum(sv ** 2, -1) / (sv ** 2).sum(-1, keepdims=True)
        return (c < 0.9).sum(-1) + 1

    out["k90_qk"], out["k90_ov"] = k90(sv_qk), k90(sv_ov)
    # one head's bilinear form, for the picture: the 128 x 128 matrix and its rank-32 factors
    li, hi = 0, int(np.argmax(sv_qk[0, :, 0]))
    out["qk_example"] = mats[li * HEADS + hi][0].astype(np.float32)
    out["qk_layer"], out["qk_head"] = li, hi
    comp = composition_scores(mats, LAYERS, HEADS)
    out.update({f"comp_{k}": v for k, v in comp.items()})
    out["comp_base"], out["comp_base_sd"] = composition_baseline(D, DH)
    # 2. the causal mask: change the future, and nothing before it moves
    ps = data["passage"]
    x = ps[1000:1000 + 128][None].clone()
    y = x.clone()
    y[0, 64:] = torch.tensor(rng(5).integers(0, K, 64))
    with torch.no_grad():
        za, zb = model(x), model(y)
        out["mask_past"] = float((za[0, :64] - zb[0, :64]).abs().max())  # positions 0-63: should not move at all
        out["mask_future"] = float((za[0, 64:] - zb[0, 64:]).abs().max())

        # the same model with the mask (and the rotations) removed: every position sees everything
        def unmasked(idx, perm=None):
            h = model.emb(idx)
            if perm is not None:
                h = h[:, perm]
            B, T, _ = h.shape
            for b in model.blocks:
                q, k, v = b.qkv(b.n1(h)).view(B, T, 3, HEADS, DH).permute(2, 0, 3, 1, 4)
                p = torch.softmax(q @ k.transpose(-1, -2) / math.sqrt(DH), -1)
                h = h + b.o((p @ v).transpose(1, 2).reshape(B, T, D))
                h = h + b.f2(F.gelu(b.f1(b.n2(h))))
            return model.out(model.nf(h))

        ua, ub = unmasked(x), unmasked(y)
        out["nomask_past"] = float((ua[0, :64] - ub[0, :64]).abs().max())
        perm = torch.tensor(rng(6).permutation(128))
        out["perm_dev"] = float((unmasked(x)[0, perm] - unmasked(x, perm)[0]).abs().max())  # f(Px) = P f(x)
        out["perm_scale"] = float(unmasked(x).abs().max())
    # 3. the cost of a block: parameters, counted by kind, and floating-point operations, measured
    groups = {"attention": 0, "mlp": 0, "norm": 0, "embed": 0}
    for n_, p_ in model.named_parameters():
        kind = ("attention" if (".qkv." in n_ or ".o." in n_) else "mlp" if (".f1." in n_ or ".f2." in n_)
                else "norm" if (".n1." in n_ or ".n2." in n_ or n_.startswith("nf.")) else "embed")
        groups[kind] += p_.numel()
    out["params"] = groups
    out["n_params"] = int(sum(groups.values()))
    out["formula_block"] = 12 * D * D  # attention 4 d^2 + MLP 8 d^2 (Kaplan et al. 2020)
    out["formula_total"] = LAYERS * (12 * D * D + 9 * D) + 2 * K * D + 2 * D
    assert out["formula_total"] == out["n_params"]
    Ts = [64, 128, 256, 512, 1024]
    fl, fl_formula = [], []
    for T in Ts:
        xx = data["valid"][:T][None]
        with FlopCounterMode(display=False) as fc, torch.no_grad():
            model(xx, keep=False)  # the explicit path: the masked square is computed in full
        fl.append(fc.get_total_flops() / T)
        fl_formula.append(2 * 12 * LAYERS * D * D + 2 * D * K + 4 * LAYERS * T * D)
    out.update(Ts=Ts, flops_per_token=fl, flops_formula=fl_formula, flops_kaplan=[
        2 * 12 * LAYERS * D * D + 2 * LAYERS * T * D for T in Ts])
    # forward and backward, at the training length
    xx = data["train"][:CTX + 1]
    with FlopCounterMode(display=False) as fc:
        z = model(xx[None, :-1], keep=False)[0]
        F.cross_entropy(z[0], xx[1:]).backward()
    out["flops_train_token"] = fc.get_total_flops() / CTX
    model.zero_grad()
    out["crossover_T"] = 12 * D  # where the attention term 2 L T d equals the weights' 2 * 12 L d^2
    return out


def yarn_theta(s, L=CTX, alpha=1.0, beta=32.0):
    """YaRN's 'NTK-by-parts': fast-turning pairs keep their angles, slow ones are interpolated, a ramp between."""
    th = rope_freqs()
    r = L / (2 * np.pi / th)  # how many turns each pair makes over the training context
    gam = np.clip((r - alpha) / (beta - alpha), 0, 1)
    return (1 - gam) * th / s + gam * th, gam


EXT_S = 4  # the extension factor
FT_STEPS, FT_BATCH = 100, 4  # the brief fine-tuning at the long context


def extend_methods(s=EXT_S):
    import torch

    T = s * CTX
    ntk = rope_freqs(base=BASE * s ** (DH / (DH - 2)))
    yth, _ = yarn_theta(s)
    n = torch.arange(1, T + 1, dtype=torch.float32)
    logn = torch.clamp(torch.log(n) / math.log(CTX), min=1.0)[:, None]  # each query's scores times log_L(n), n > L
    return {
        "plain": dict(),
        "pi": dict(pos_scale=float(s)),
        "ntk": dict(theta=ntk),
        "yarn": dict(theta=yth, temp=(0.1 * math.log(s) + 1) ** 2),
        "logn": dict(temp=logn),
        "ntk_logn": dict(theta=ntk, temp=logn),
    }


def ext_eval(model, x, y, kw):
    import torch
    import torch.nn.functional as F

    T = x.shape[1]
    ce = np.zeros(T)
    with torch.no_grad():
        for i in range(0, len(x), 4):
            z = model(x[i:i + 4], **kw)
            ce += F.cross_entropy(z.reshape(-1, z.shape[-1]), y[i:i + 4].reshape(-1),
                                  reduction="none").view(-1, T).sum(0).numpy()
    return ce / len(x) / math.log(2)


def compute_extend():
    import torch
    import torch.nn.functional as F

    threads()
    load("tf")
    model, chars, enc, data = load_tf()
    va, tr = data["valid"], data["train"]
    s = EXT_S
    T = s * CTX
    g = rng(3)
    starts = g.integers(0, len(va) - T - 1, 32)
    th = rope_freqs()
    yth, gam = yarn_theta(s)
    methods = extend_methods(s)
    out = dict(s=s, T=T, theta=th, theta_ntk=methods["ntk"]["theta"], theta_yarn=yth, ramp=gam,
               buckets=list(range(0, T + 1, 64)), methods=list(methods))
    x = torch.stack([va[a:a + T] for a in starts])
    y = torch.stack([va[a + 1:a + T + 1] for a in starts])
    for name, kw in methods.items():
        ce = ext_eval(model, x, y, kw)
        out[f"pos_{name}"] = ce
        out[f"bucket_{name}"] = [float(ce[a:a + 64].mean()) for a in range(0, T, 64)]
        print(f"    {name}: " + " ".join(f"{v:.2f}" for v in out[f"bucket_{name}"]), flush=True)
    # the honest baseline: the model as trained, always on the last 256 characters
    base = []
    with torch.no_grad():
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
    # then a brief fine-tuning at the long context, as real models do: the same steps for each rescaling
    sd0 = {k: v.clone() for k, v in model.state_dict().items()}
    part = CACHE.partial("extend", dict(steps=FT_STEPS, batch=FT_BATCH, T=T, lr=2e-4))
    for name in ("pi", "yarn"):
        if name not in part:
            model.load_state_dict(sd0)
            model.train()
            torch.manual_seed(2023)
            gg = rng(2023)  # the same windows for both
            opt = torch.optim.AdamW(model.parameters(), lr=2e-4, betas=(0.9, 0.95), weight_decay=0.0)
            curve = []
            for step in range(1, FT_STEPS + 1):
                st = torch.tensor(gg.integers(0, len(tr) - T - 1, FT_BATCH))
                idx = st[:, None] + torch.arange(T + 1)[None]
                xb, yb = tr[idx[:, :-1]], tr[idx[:, 1:]]
                loss = F.cross_entropy(model(xb, **methods[name]).reshape(-1, len(chars)), yb.reshape(-1))
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                curve.append(float(loss.detach()) / math.log(2))
            model.eval()
            ce = ext_eval(model, x, y, methods[name])
            part[name] = dict(pos=ce.tolist(), curve=curve)
            print(f"    fine-tuned {name}: " + " ".join(f"{ce[a:a + 64].mean():.2f}" for a in range(0, T, 64)),
                  flush=True)
        ce = np.array(part[name]["pos"])
        out[f"pos_ft_{name}"] = ce
        out[f"bucket_ft_{name}"] = [float(ce[a:a + 64].mean()) for a in range(0, T, 64)]
        out[f"ft_curve_{name}"] = np.array(part[name]["curve"])
    out["ft_steps"], out["ft_batch"] = FT_STEPS, FT_BATCH
    out["ft_chars"] = FT_STEPS * FT_BATCH * T
    model.load_state_dict(sd0)
    plain_far = np.mean(out["bucket_plain"][-4:])
    assert plain_far > np.mean(out["bucket_plain"][:4]) + 0.3  # beyond its training length, it breaks
    return out


# ---------------------------------------------------------------------------
# A small configurable transformer, for the experiments run side by side
# ---------------------------------------------------------------------------
def alibi_slopes(H):
    """ALiBi's head slopes (Press et al. 2021): the geometric sequence 2^(-8/H), 2^(-16/H), ..., 2^(-8)."""
    return 2.0 ** (-8.0 * np.arange(1, H + 1) / H)


def build_small(K, d=64, L=3, H=4, pos="rope", sink=False, gate=False, diff=False, qknorm=False, cap=0.0,
                causal=True):
    """A pre-norm transformer (LayerNorm, GELU MLP of width 4d) whose attention can be switched between the variants
    this part compares. ``pos``: 'rope', 'alibi', 'sin' (2017's sinusoids, added to the input) or 'nope'.
    ``sink``: a learned logit per head in the softmax's denominator (gpt-oss). ``gate``: each head's output times a
    sigmoid of the input, elementwise (Qiu et al. 2025). ``diff``: differential attention (Ye et al. 2024), the
    difference of two softmax maps with a learned lambda, normed per head. ``qknorm``: queries and keys RMS-normed
    per head. ``cap``: scores soft-capped at cap * tanh(s / cap). forward(idx, keep) returns the logits, and with
    ``keep`` each layer's attention weights and extras (the sink's share, the gate's openness)."""
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    dh = d // H

    def rotate(t):
        T, e = t.shape[-2], t.shape[-1]
        th = torch.tensor(rope_freqs(e), dtype=torch.float32)
        ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
        c, s_ = torch.cos(ang), torch.sin(ang)
        a, b = t[..., : e // 2], t[..., e // 2:]
        return torch.cat([a * c - b * s_, a * s_ + b * c], -1)

    slopes = torch.tensor(alibi_slopes(H), dtype=torch.float32)

    class Attn(nn.Module):
        def __init__(self, layer):
            super().__init__()
            self.qkv = nn.Linear(d, 3 * d, bias=False)
            self.o = nn.Linear(d, d, bias=False)
            if sink:
                self.sink = nn.Parameter(torch.zeros(H))
            if gate:
                self.g = nn.Linear(d, d)
            if qknorm:
                self.qn, self.kn = nn.RMSNorm(dh), nn.RMSNorm(dh)
            if diff:
                e = dh // 2
                self.lam = nn.Parameter(torch.randn(4, e) * 0.1)
                self.lam_init = 0.8 - 0.6 * math.exp(-0.3 * layer)  # layer counted from 0: (l - 1) for l from 1
                self.hn = nn.RMSNorm(dh)

        def scores(self, q, k):
            T = q.shape[-2]
            if qknorm:
                q, k = self.qn(q), self.kn(k)
            if pos == "rope":
                q, k = rotate(q), rotate(k)
            s = q @ k.transpose(-1, -2) / math.sqrt(q.shape[-1])
            if cap:
                s = cap * torch.tanh(s / cap)
            i = torch.arange(T)
            if pos == "alibi":
                s = s - slopes[:, None, None] * (i[:, None] - i[None]).clamp(min=0).float()
            if causal:
                s = s.masked_fill(~torch.ones(T, T, dtype=torch.bool).tril(), float("-inf"))
            return s

        def forward(self, x, keep=False):
            B, T, _ = x.shape
            q, k, v = self.qkv(x).view(B, T, 3, H, dh).permute(2, 0, 3, 1, 4)
            extra = {}
            if diff:
                e = dh // 2
                p1 = torch.softmax(self.scores(q[..., :e], k[..., :e]), -1)
                p2 = torch.softmax(self.scores(q[..., e:], k[..., e:]), -1)
                lq1, lk1, lq2, lk2 = self.lam
                lam = torch.exp((lq1 * lk1).sum()) - torch.exp((lq2 * lk2).sum()) + self.lam_init
                p = p1 - lam * p2
                a = self.hn(p @ v) * (1 - self.lam_init)
                if keep:
                    extra.update(p1=p1, p2=p2, lam=float(lam))
            else:
                s = self.scores(q, k)
                if sink:
                    full = torch.cat([s, self.sink.view(1, H, 1, 1).expand(B, H, T, 1)], -1)
                    P = torch.softmax(full, -1)
                    p = P[..., :-1]
                    if keep:
                        extra["null"] = P[..., -1]
                else:
                    p = torch.softmax(s, -1)
                a = p @ v
            if gate:
                gt = torch.sigmoid(self.g(x)).view(B, T, H, dh).transpose(1, 2)
                a = a * gt
                if keep:
                    extra["gate"] = gt.mean(-1)
            if keep:
                extra["v"] = v
            return self.o(a.transpose(1, 2).reshape(B, T, d)), (p if keep else None), extra

    class Block(nn.Module):
        def __init__(self, layer):
            super().__init__()
            self.n1, self.n2 = nn.LayerNorm(d), nn.LayerNorm(d)
            self.attn = Attn(layer)
            self.f1, self.f2 = nn.Linear(d, 4 * d), nn.Linear(4 * d, d)

        def forward(self, x, keep=False):
            a, p, extra = self.attn(self.n1(x), keep)
            x = x + a
            return x + self.f2(F.gelu(self.f1(self.n2(x)))), p, extra

    class Small(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(K, d)
            self.blocks = nn.ModuleList([Block(i) for i in range(L)])
            self.nf = nn.LayerNorm(d)
            self.out = nn.Linear(d, K, bias=False)

        def forward(self, idx, keep=False):
            T = idx.shape[1]
            x = self.emb(idx)
            if pos == "sin":
                om = 10000.0 ** (-torch.arange(0, d, 2, dtype=torch.float32) / d)
                ang = torch.arange(T, dtype=torch.float32)[:, None] * om[None]
                x = x + torch.stack([ang.sin(), ang.cos()], -1).reshape(T, d)
            maps, extras = [], []
            for b in self.blocks:
                x, p, extra = b(x, keep)
                maps.append(p)
                extras.append(extra)
            z = self.out(self.nf(x))
            return (z, maps, extras) if keep else z

    return Small()


def make_opt(model, lr, steps, warm):
    import torch

    decay = [p for p in model.parameters() if p.dim() >= 2]
    other = [p for p in model.parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([dict(params=decay, weight_decay=0.1), dict(params=other, weight_decay=0.0)], lr=lr,
                            betas=(0.9, 0.95))
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / warm if s < warm else 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * (s - warm) / (steps - warm))))
    return opt, sched


# ---------------------------------------------------------------------------
POS_METHODS = ("sin", "rope", "alibi", "nope")
POS_SEEDS = (1, 2, 3)
POS_CFG = dict(d=64, L=3, H=4, ctx=128, batch=16, steps=1000, lr=3e-3, warm=100, read=512)


def compute_positions():
    """Four ways of telling a small transformer where things are, trained side by side on the novels: the same
    shape, the same data in the same order, the same steps; three seeds each. Then each reads 4x longer texts."""
    import torch
    import torch.nn.functional as F

    threads()
    chars, enc, data = corpus()
    K = len(chars)
    tr, va = data["train"], data["valid"]
    c = POS_CFG
    T, R = c["ctx"], c["read"]
    ev = rng(55).integers(0, len(va) - R - 1, 48)
    xe = torch.stack([va[a:a + R] for a in ev])
    ye = torch.stack([va[a + 1:a + R + 1] for a in ev])
    part = CACHE.partial("positions", c)
    for seed in POS_SEEDS:
        for m in POS_METHODS:
            key = f"{m}_{seed}"
            if key in part:
                continue
            t0 = time.time()
            torch.manual_seed(seed)
            model = build_small(K, c["d"], c["L"], c["H"], pos=m)
            opt, sched = make_opt(model, c["lr"], c["steps"], c["warm"])
            g = rng(1000 + seed)  # the same windows, in the same order, for every method
            curve = []
            for step in range(1, c["steps"] + 1):
                st = torch.tensor(g.integers(0, len(tr) - T - 1, c["batch"]))
                idx = st[:, None] + torch.arange(T + 1)[None]
                loss = F.cross_entropy(model(tr[idx[:, :-1]]).reshape(-1, K), tr[idx[:, 1:]].reshape(-1))
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                sched.step()
                if step % 100 == 0:
                    with torch.no_grad():
                        z = model(xe[:16, :T])
                        curve.append((step, float(F.cross_entropy(z.reshape(-1, K), ye[:16, :T].reshape(-1))) / math.log(2)))
            model.eval()
            with torch.no_grad():
                ce = np.zeros(R)
                for i in range(0, len(xe), 8):
                    z = model(xe[i:i + 8])
                    ce += F.cross_entropy(z.reshape(-1, K), ye[i:i + 8].reshape(-1), reduction="none").view(-1, R).sum(0).numpy()
                ce /= len(xe) * math.log(2)
            part[key] = dict(curve=curve, pos=ce.tolist(), seconds=time.time() - t0)
            print(f"    {key}: in context {ce[:T].mean():.3f}, far {ce[3 * T:].mean():.3f} "
                  f"({time.time() - t0:.0f}s)", flush=True)
    out = dict(cfg=c, methods=list(POS_METHODS), seeds=list(POS_SEEDS))
    for m in POS_METHODS:
        P = np.array([part[f"{m}_{s_}"]["pos"] for s_ in POS_SEEDS])  # seed, position
        out[f"pos_{m}"] = P
        out[f"curve_{m}"] = np.array([[b for _, b in part[f"{m}_{s_}"]["curve"]] for s_ in POS_SEEDS])
        out[f"in_{m}"] = P[:, :T].mean(1)  # bits within the training length, one per seed
        out[f"far_{m}"] = P[:, 3 * T:].mean(1)  # bits at 3-4x the training length
        out[f"bucket_{m}"] = P.reshape(len(POS_SEEDS), -1, 32).mean(-1)
    out["curve_steps"] = [s_ for s_, _ in part[f"rope_{POS_SEEDS[0]}"]["curve"]]
    out["slopes"] = alibi_slopes(c["H"])
    return out


# ---------------------------------------------------------------------------
SINK_VARIANTS = ("softmax", "sink", "gate", "diff")
SINK_SEEDS = (1, 2, 3)
SINK_CFG = dict(V=64, T=64, d=64, steps=1500, batch=32, lr=3e-3, warm=100)


def bb_task():
    """The bigram-backcopy task (Guo et al. 2024), on the novels' 64 commonest characters: a sequence starts with
    <s>; each next character follows the novels' bigram statistics, except after a trigger (the three commonest
    characters), where it copies the character before the trigger."""
    from collections import Counter

    from videos.ai.ai1 import compute as c1

    t = c1.text("train")[:4_000_000]
    common = [ch for ch, _ in Counter(t).most_common(SINK_CFG["V"])]
    ix = {ch: i for i, ch in enumerate(common)}
    a = np.array([ix.get(ch, -1) for ch in t])
    ok = (a[:-1] >= 0) & (a[1:] >= 0)
    V = len(common)
    Pm = np.zeros((V, V))
    np.add.at(Pm, (a[:-1][ok], a[1:][ok]), 1)
    Pm = (Pm + 1e-3) / (Pm + 1e-3).sum(1, keepdims=True)
    uni = np.bincount(a[a >= 0], minlength=V).astype(float)
    trig = [0, 1, 2]  # the three commonest characters
    return common, Pm, uni / uni.sum(), trig


def bb_batch(g, n, Pm, uni, trig, T):
    V = len(Pm)
    BOS = V
    x = np.zeros((n, T), int)
    x[:, 0] = BOS
    u0 = uni.copy()
    u0[trig] = 0
    x[:, 1] = g.choice(V, size=n, p=u0 / u0.sum())
    cum = np.cumsum(Pm, 1)
    is_t = np.zeros(V + 1, bool)
    is_t[trig] = True
    for t in range(1, T - 1):
        nxt = np.minimum((cum[x[:, t]] < g.random(n)[:, None]).sum(1), V - 1)
        x[:, t + 1] = np.where(is_t[x[:, t]], x[:, t - 1], nxt)
    return x, is_t[x]


def compute_sinks():
    """Where a head looks when it has nothing to do: plain softmax against a sink logit, an output gate and
    differential attention, each a one-layer transformer trained on the bigram-backcopy task, three seeds."""
    import torch
    import torch.nn.functional as F

    threads()
    c = SINK_CFG
    common, Pm, uni, trig = bb_task()
    V, T = len(common), c["T"]
    K = V + 1
    xt, tt = bb_batch(rng(999), 256, Pm, uni, trig, T)
    xt_ = torch.tensor(xt)
    # the best possible: bits of the bigram's next character, and 0 after a trigger
    ent = -(Pm * np.log2(Pm)).sum(1)
    opt_bigram = float(np.mean([ent[xt[b, t]] for b in range(len(xt)) for t in range(1, T - 1) if not tt[b, t]]))
    part = CACHE.partial("sinks", c)
    for seed in SINK_SEEDS:
        for vname in SINK_VARIANTS:
            key = f"{vname}_{seed}"
            if key in part:
                continue
            t0 = time.time()
            torch.manual_seed(seed)
            model = build_small(K, c["d"], 1, 1, pos="rope", sink=vname == "sink", gate=vname == "gate",
                                diff=vname == "diff")
            opt, sched = make_opt(model, c["lr"], c["steps"], c["warm"])
            g = rng(2000 + seed)
            hist = []
            for step in range(1, c["steps"] + 1):
                xb = torch.tensor(bb_batch(g, c["batch"], Pm, uni, trig, T)[0])
                loss = F.cross_entropy(model(xb[:, :-1]).reshape(-1, K), xb[:, 1:].reshape(-1))
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                sched.step()
                if step % 100 == 0:
                    hist.append((step, *bb_measure(model, xt_, tt, K)[:3]))
            model.eval()
            r = bb_measure(model, xt_, tt, K, full=True)
            part[key] = dict(hist=hist, **r[3], seconds=time.time() - t0)
            print(f"    {key}: bigram {r[3]['loss_bigram']:.3f} (best {opt_bigram:.3f}), copy {r[3]['loss_copy']:.3f}, "
                  f"<s> share dormant {r[3]['bos_dormant']:.2f} active {r[3]['bos_active']:.2f} "
                  f"({time.time() - t0:.0f}s)", flush=True)
    out = dict(cfg=c, variants=list(SINK_VARIANTS), seeds=list(SINK_SEEDS), chars=common, trig=trig,
               opt_bigram=opt_bigram)
    keys = [k for k in part[f"softmax_{SINK_SEEDS[0]}"] if k not in ("hist", "seconds", "map", "x")]
    for vname in SINK_VARIANTS:
        for k in keys:
            vals = [part[f"{vname}_{s_}"].get(k) for s_ in SINK_SEEDS]
            if all(v_ is not None for v_ in vals):
                out[f"{vname}_{k}"] = np.array(vals, dtype=float)
        out[f"{vname}_hist"] = np.array([part[f"{vname}_{s_}"]["hist"] for s_ in SINK_SEEDS])  # seed, t, (step, ...)
        out[f"{vname}_map"] = np.array(part[f"{vname}_{SINK_SEEDS[0]}"]["map"], dtype=np.float32)
    out["example"] = np.array(part[f"softmax_{SINK_SEEDS[0]}"]["x"])
    return out


def bb_measure(model, x, is_trig, K, full=False):
    """Bits on the bigram part and on the copies; the attention <s> draws from queries with nothing to copy
    (dormant) and from triggers (active); and, with ``full``, what each variant does instead."""
    import torch
    import torch.nn.functional as F

    with torch.no_grad():
        z, maps, extras = model(x[:, :-1], keep=True)
        ce = F.cross_entropy(z.reshape(-1, K), x[:, 1:].reshape(-1), reduction="none").view(len(x), -1).numpy()
        ce /= math.log(2)
        P = maps[0][:, 0].numpy()  # batch, query, key (one head)
        tq = is_trig[:, :-1].copy()
        valid = np.zeros_like(tq)
        valid[:, 2:] = True  # queries at positions 2 ... (position 1's previous token is <s> itself)
        dorm, act = valid & ~tq, valid & tq
        bos = P[:, :, 0]
        prev = np.zeros_like(bos)
        prev[:, 1:] = P[:, np.arange(1, P.shape[1]), np.arange(0, P.shape[1] - 1)]
        r = (float(ce[:, 1:][~tq[:, 1:]].mean()), float(ce[act].mean()), float(bos[dorm].mean()))
        if not full:
            return r
        ex = extras[0]
        v = ex["v"][:, 0].norm(dim=-1).numpy()  # batch, position
        out = dict(loss_bigram=r[0], loss_copy=r[1], bos_dormant=r[2], bos_active=float(bos[act].mean()),
                   prev_active=float(prev[act].mean()), prev_dormant=float(prev[dorm].mean()),
                   v_bos=float(v[:, 0].mean()), v_rest=float(v[:, 1:].mean()))
        if "null" in ex:
            nl = ex["null"][:, 0].numpy()
            out.update(null_dormant=float(nl[dorm].mean()), null_active=float(nl[act].mean()))
        if "gate" in ex:
            gt = ex["gate"][:, 0].numpy()
            out.update(gate_dormant=float(gt[dorm].mean()), gate_active=float(gt[act].mean()))
        if "p1" in ex:
            p1, p2 = ex["p1"][:, 0].numpy(), ex["p2"][:, 0].numpy()
            out.update(lam=ex["lam"], p1_bos_dormant=float(p1[:, :, 0][dorm].mean()),
                       p2_bos_dormant=float(p2[:, :, 0][dorm].mean()), sum_dormant=float(P.sum(-1)[dorm].mean()))
        out["map"] = P[0, :24, :24].tolist()
        out["x"] = x[0, :25].tolist()
        return r + (out,)


# ---------------------------------------------------------------------------
def compute_qkscale():
    """What happens to attention if queries and keys grow: our transformer's W_Q and W_K multiplied by c (every
    score by c^2), plain, with a soft cap, and with QK-norm."""
    import torch
    import torch.nn.functional as F

    threads()
    load("tf")
    model, chars, enc, data = load_tf()
    va = data["valid"]
    starts = rng(21).integers(0, len(va) - CTX - 1, 16)
    x = torch.stack([va[a:a + CTX] for a in starts])
    y = torch.stack([va[a + 1:a + CTX + 1] for a in starts])
    K = len(chars)
    cs = [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0]
    # the trained model's queries and keys: their typical size per head, and its largest score
    with torch.no_grad():
        _, maps, qks = model(x, keep=True)
        rms = [(qk[0].pow(2).mean((0, 2, 3)).sqrt(), qk[1].pow(2).mean((0, 2, 3)).sqrt()) for qk in qks]
        top = max(float((qk[0] @ qk[1].transpose(-1, -2)).abs().max()) / math.sqrt(DH) for qk in qks)
    cap = float(math.ceil(top))
    out = dict(cs=cs, cap=cap, max_logit=top)

    def run(c, mode):
        h = model.emb(x)
        B, T = x.shape
        th = torch.tensor(rope_freqs(), dtype=torch.float32)
        ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
        cos, sin = torch.cos(ang), torch.sin(ang)
        ents, peaks, logit = [], [], 0.0
        for li, b in enumerate(model.blocks):
            q, k, v = b.qkv(b.n1(h)).view(B, T, 3, HEADS, DH).permute(2, 0, 3, 1, 4)
            q, k = q * c, k * c  # W_Q and W_K grown by c
            if mode == "norm":  # QK-norm: each query and key rescaled to the trained head's typical size
                q = q / q.pow(2).mean(-1, keepdim=True).sqrt() * rms[li][0].view(1, HEADS, 1, 1)
                k = k / k.pow(2).mean(-1, keepdim=True).sqrt() * rms[li][1].view(1, HEADS, 1, 1)

            def rot(t):
                a_, b_ = t[..., : DH // 2], t[..., DH // 2:]
                return torch.cat([a_ * cos - b_ * sin, a_ * sin + b_ * cos], -1)

            s = rot(q) @ rot(k).transpose(-1, -2) / math.sqrt(DH)
            if mode == "cap":
                s = cap * torch.tanh(s / cap)
            mask = torch.ones(T, T, dtype=torch.bool).tril()
            logit = max(logit, float(s.masked_fill(~mask, 0).abs().max()))
            p = torch.softmax(s.masked_fill(~mask, float("-inf")), -1)
            pp = p[:, :, 32:]  # queries with at least 32 keys
            ents.append(float((-(pp * torch.log2(pp.clamp_min(1e-30))).sum(-1)).mean()))
            peaks.append(float((pp.max(-1).values > 0.9).float().mean()))
            h = h + b.o((p @ v).transpose(1, 2).reshape(B, T, D))
            h = h + b.f2(F.gelu(b.f1(b.n2(h))))
        z = model.out(model.nf(h))
        bits = float(F.cross_entropy(z.reshape(-1, K), y.reshape(-1))) / math.log(2)
        return float(np.mean(ents)), float(np.mean(peaks)), bits, logit

    with torch.no_grad():
        for mode in ("plain", "cap", "norm"):
            res = [run(c, mode) for c in cs]
            out[f"ent_{mode}"] = [r_[0] for r_ in res]
            out[f"peak_{mode}"] = [r_[1] for r_ in res]
            out[f"bits_{mode}"] = [r_[2] for r_ in res]
            out[f"logit_{mode}"] = [r_[3] for r_ in res]
            print(f"    {mode}: entropy " + " ".join(f"{v:.2f}" for v in out[f"ent_{mode}"]) + "; bits "
                  + " ".join(f"{v:.2f}" for v in out[f"bits_{mode}"]), flush=True)
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
# RASP, compiled by hand into attention weights
# ---------------------------------------------------------------------------
def softmax_rows(S):
    S = S - S.max(-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(-1, keepdims=True)


def count_decoder(n_max):
    """A one-hidden-layer ReLU network that reads a count c from the number 1/(c + 1): for each c a step at the
    midpoint between 1/(c + 1) and 1/(c + 2), two ReLUs each; the one-hot count is the difference of neighbouring
    steps. Returns (W1, b1, W2): onehot = W2 relu(W1 u + b1)."""
    u = 1.0 / (np.arange(0, n_max + 2) + 1)  # u[c] = 1/(c + 1)
    mids = (u[:-1] + u[1:]) / 2  # mids[c]: between counts c and c + 1
    eps = (u[n_max] - u[n_max + 1]) / 8
    W1, b1 = [], []
    for c in range(n_max + 1):  # step_c(u) = 1 when u > mids[c], i.e. the count is at most c
        W1 += [1 / eps, 1 / eps]
        b1 += [-mids[c] / eps, -mids[c] / eps - 1]
    W1, b1 = np.array(W1)[:, None], np.array(b1)
    W2 = np.zeros((n_max + 1, len(b1)))
    for c in range(n_max + 1):  # onehot(c) = step_c - step_(c-1)
        W2[c, 2 * c], W2[c, 2 * c + 1] = 1, -1
        if c > 0:
            W2[c, 2 * c - 2], W2[c, 2 * c - 1] = -1, 1
    return W1, b1, W2


def compute_rasp():
    """Two RASP programs (Weiss et al. 2021) compiled by hand into attention weights, in the manner of Tracr (Lindner
    et al. 2023), and run: the histogram (one layer) and sorting (two layers)."""
    g = rng(2021)
    beta = 40.0  # how sharply a head selects: e^-40 leaks nothing a float can see
    out = dict(beta=beta)
    # --- histogram: for each token, how many tokens equal it. select(tokens, tokens, ==), then selector_width,
    # which attends to the selected tokens and to <s> (always selected) and reads <s>'s share 1/(c + 1)
    V, n_max = 6, 40
    W1, b1, W2 = count_decoder(n_max)

    def histogram(x, dtype=np.float64):
        n = len(x)
        E = np.zeros((n + 1, V + 1))  # one-hot tokens, and a flag for <s> at position 0
        E[0, V] = 1
        E[np.arange(1, n + 1), x] = 1
        WQ = np.zeros((V + 1, V + 1))
        WQ[:V, :V] = beta * np.eye(V)  # a query matches keys of its own token ...
        Q = E @ WQ
        Q[:, V] = beta  # ... and always <s>
        S = Q @ E.T
        A = softmax_rows(S)
        o = (A @ E[:, V]).astype(dtype).astype(np.float64)  # <s>'s value is 1, every token's 0: o = 1/(c + 1)
        h = np.maximum(W1 @ o[None] + b1[:, None], 0)
        return (W2 @ h).argmax(0)[1:], A

    ok = 0
    for _ in range(2000):
        n = int(g.integers(1, n_max + 1))
        x = g.integers(0, V, n)
        ok += np.array_equal(histogram(x)[0], np.array([(x == t).sum() for t in x]))
    out["hist_ok"], out["hist_trials"] = ok, 2000
    ex = np.array([0, 2, 1, 0, 3, 0, 2, 1, 4, 0, 2, 5])
    cnt, A = histogram(ex)
    out.update(hist_x=ex, hist_counts=cnt, hist_A=A, hist_alphabet="abcdef")
    # precision: the largest count a 1/(c + 1) read in each float format still tells from c + 1
    for name, dt in (("bf16", "bf16"), ("fp16", np.float16), ("fp32", np.float32)):
        c = 1
        while c < 100000:
            u1, u2 = 1 / (c + 1), 1 / (c + 2)
            if dt == "bf16":  # bfloat16: float32 with the low 16 bits dropped (round to nearest)
                def r(v):
                    b = np.array([v], np.float32).view(np.uint32)
                    b = ((b + 0x8000) & 0xFFFF0000).astype(np.uint32)
                    return float(b.view(np.float32)[0])
            else:
                def r(v, dt=dt):
                    return float(np.array(v, dt))
            if r(u1) == r(u2):
                break
            c += 1
        out[f"prec_{name}"] = c  # counts up to c are told apart
    # --- sorting (unique tokens): layer 1 counts the smaller tokens (a rank, by selector_width on the predicate
    # key < query); layer 2, at output position p, selects the token whose rank is p and copies it
    Vs, nm = 26, 12
    W1s, b1s, W2s = count_decoder(nm)

    def sort_prog(x):
        n = len(x)
        E = np.zeros((n + 1, Vs + 1))
        E[0, Vs] = 1
        E[np.arange(1, n + 1), x] = 1
        M = np.zeros((Vs + 1, Vs + 1))
        M[:Vs, :Vs] = beta * (np.arange(Vs)[None] < np.arange(Vs)[:, None])  # query token a, key token b: b < a
        M[:, Vs] = beta  # every query also selects <s>
        A1 = softmax_rows(E @ M @ E.T)
        o = A1 @ E[:, Vs]
        rank = (W2s @ np.maximum(W1s @ o[None] + b1s[:, None], 0)).argmax(0)  # the rank, one-hot, into the stream
        R = np.zeros((n + 1, nm + 1))
        R[np.arange(n + 1), rank] = 1
        P = np.eye(nm + 1)[np.arange(1, n + 1) - 1]  # output position p asks for rank p
        A2 = softmax_rows(beta * P @ R[1:].T)  # among the tokens (not <s>)
        y = (A2 @ E[1:, :Vs]).argmax(1)
        return y, A1, A2, rank

    ok = 0
    for _ in range(2000):
        n = int(g.integers(1, nm + 1))
        x = g.choice(Vs, n, replace=False)
        ok += np.array_equal(sort_prog(x)[0], np.sort(x))
    out["sort_ok"], out["sort_trials"] = ok, 2000
    ex = np.array([ord(ch) - 97 for ch in "wordsclay"])
    y, A1, A2, rank = sort_prog(ex)
    out.update(sort_x=ex, sort_y=y, sort_A1=A1, sort_A2=A2, sort_rank=rank[1:])
    assert out["hist_ok"] == 2000 and out["sort_ok"] == 2000  # compiled programs are exact
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
    "hopfield": compute_hopfield,
    "rope": compute_rope,
    "rasp": compute_rasp,
    "tf": compute_tf,
    "tfwords": compute_tfwords,
    "heads": compute_heads,
    "qkscale": compute_qkscale,
    "extend": compute_extend,
    "positions": compute_positions,
    "sinks": compute_sinks,
    "induction": compute_induction,
    "icl": compute_icl,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
