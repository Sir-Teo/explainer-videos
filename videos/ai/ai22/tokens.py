"""Part 22, chapters 9-10: pictures as tokens, written in raster order, by MaskGIT, and coarse to fine (VAR).

    tokens   Two tokenizers trained here (vector quantization with a straight-through gradient, Part 23's codebooks):
             one scale (a 5 x 5 grid of tokens from 128 codes), and VAR's five scales of residual tokens (1, 2, 3, 4
             and 5 a side, 55 tokens, one shared codebook of 128), each scale coding what the coarser ones missed.
             Three generators of the same size (4 layers, width 64), the same steps and batches, three seeds:
               raster   next-token prediction, left to right and top to bottom: 25 passes
               maskgit  bidirectional, trained to fill a random share of masked tokens; drawn in 8 passes, surest
                        first (Chang et al. 2022)
               var      next-scale prediction with a block-causal mask: 5 passes (Tian et al. 2024)
             Scored by the judge on 260 pictures (ten per letter), with guidance 2 for all three.
"""

from __future__ import annotations

import math

import numpy as np

from videos.ai.ai22.base import CACHE, GL, dataset, score, steps, threads

K, CD = 128, 8  # codes, numbers per code
SCALES = (1, 2, 3, 4, 5)
D, L, H = 64, 4, 4
SEEDS = (0, 1, 2)
KINDS = ("raster", "maskgit", "var")
N_TOK, N_GEN, BATCH = 3000, 2000, 64
GUIDE = 2.0
MASKGIT_STEPS = 8


def tokenizer_nets():
    import torch.nn as nn

    enc = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.SiLU(), nn.Conv2d(32, 64, 4, 2, 1), nn.SiLU(),
                        nn.Conv2d(64, 64, 4, 2, 1), nn.SiLU(), nn.Conv2d(64, CD, 1))  # 20 -> 5 x 5 x 8
    dec = nn.Sequential(nn.Conv2d(CD, 64, 3, padding=1), nn.SiLU(), nn.ConvTranspose2d(64, 64, 4, 2, 1), nn.SiLU(),
                        nn.ConvTranspose2d(64, 32, 4, 2, 1), nn.SiLU(), nn.Conv2d(32, 1, 3, padding=1))
    return enc, dec


def nearest(z, book):
    """z (B, CD, h, w) -> code indices (B, h, w)."""
    import torch

    f = z.permute(0, 2, 3, 1).reshape(-1, CD)
    d = (f ** 2).sum(1, keepdim=True) - 2 * f @ book.T + (book ** 2).sum(1)[None]
    return torch.argmin(d, 1).reshape(z.shape[0], z.shape[2], z.shape[3])


def lookup(idx, book):
    return book[idx].permute(0, 3, 1, 2)


def down(f, s):
    import torch.nn.functional as F

    return f if s == f.shape[-1] else F.interpolate(f, size=(s, s), mode="area")


def up(e, s=5):
    import torch.nn.functional as F

    return e if e.shape[-1] == s else F.interpolate(e, size=(s, s), mode="bilinear", align_corners=False)


def multiscale(f, book):
    """VAR's residual quantization: at each scale, quantize what is still missing, averaged down to that scale."""
    fhat = 0 * f
    idxs, partial, losses = [], [], 0.0
    for s in SCALES:
        r = down(f - fhat, s)
        idx = nearest(r, book)
        e = lookup(idx, book)
        losses = losses + ((e - r.detach()) ** 2).mean() + 0.25 * ((r - e.detach()) ** 2).mean()
        fhat = fhat + up(e)
        idxs.append(idx)
        partial.append(fhat)
    return idxs, partial, losses


def train_tokenizer(kind, X, n_steps, seed):
    """kind 'single' (one 5 x 5 grid) or 'multi' (VAR's five scales). Rebuild loss, codebook and commitment losses,
    straight-through gradients; codes unused for 250 steps are restarted at encoder outputs."""
    import torch
    import torch.nn.functional as F

    torch.manual_seed(seed)
    enc, dec = tokenizer_nets()
    book = torch.nn.Parameter(torch.randn(K, CD) * 0.5)
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters(), book], lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_steps)
    g = torch.Generator().manual_seed(seed)
    used = torch.zeros(K)
    for st in range(1, n_steps + 1):
        x = X[torch.randint(0, len(X), (128,), generator=g)][:, None]
        f = enc(x)
        if kind == "single":
            idx = nearest(f, book)
            e = lookup(idx, book)
            vq = ((e - f.detach()) ** 2).mean() + 0.25 * ((f - e.detach()) ** 2).mean()
            fq = f + (e - f).detach()
            idxs = [idx]
        else:
            idxs, partial, vq = multiscale(f, book)
            fq = f + (partial[-1] - f).detach()
            vq = vq + ((partial[-1].detach() - f) ** 2).mean()
        loss = F.binary_cross_entropy_with_logits(dec(fq), x) + vq
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        with torch.no_grad():
            for i_ in idxs:
                used += torch.bincount(i_.flatten(), minlength=K).float()
            if st % 250 == 0 and st < 0.8 * n_steps:
                dead = torch.where(used == 0)[0]
                if len(dead):
                    pool = f.permute(0, 2, 3, 1).reshape(-1, CD)
                    book.data[dead] = pool[torch.randint(0, len(pool), (len(dead),), generator=g)]
                used.zero_()
    enc.eval()
    dec.eval()
    return enc, dec, book.detach()


def encode(kind, enc, book, X):
    import torch

    with torch.no_grad():
        f = enc(X[:, None])
        if kind == "single":
            return [nearest(f, book)], None
        idxs, partial, _ = multiscale(f, book)
        return idxs, partial


def decode_feat(dec, f):
    import torch

    with torch.no_grad():
        return torch.sigmoid(dec(f)).numpy()[:, 0]


def gen_net(kind):
    import torch
    import torch.nn as nn

    T = 25 if kind != "var" else sum(s * s for s in SCALES)

    class Gen(nn.Module):
        def __init__(self):
            super().__init__()
            self.kind = kind
            self.cls = nn.Embedding(27, D)
            self.tok = nn.Embedding(K + 1, D)  # code K is MaskGIT's [MASK]
            self.feat = nn.Linear(CD, D)  # VAR: the coarser scales' picture so far, as input
            self.lvl = nn.Embedding(len(SCALES), D)
            self.pos = nn.Parameter(torch.randn(1, T + (1 if kind == "maskgit" else 0), D) * 0.02)
            self.layers = nn.ModuleList([nn.TransformerEncoderLayer(D, H, 4 * D, dropout=0.0, batch_first=True,
                                                                    norm_first=True) for _ in range(L)])
            self.nf = nn.LayerNorm(D)
            self.head = nn.Linear(D, K)
            if kind == "raster":
                mask = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
            elif kind == "maskgit":
                mask = torch.zeros(T + 1, T + 1, dtype=torch.bool)
            else:  # block-causal: every token of a scale sees its own scale and the coarser ones
                lev = torch.cat([torch.full((s * s,), k) for k, s in enumerate(SCALES)])
                mask = lev[None, :] > lev[:, None]
                self.register_buffer("lev", lev)
            self.register_buffer("mask", mask)

        def forward(self, y, inp):
            """raster: inp (B, 25) tokens (the last one unused); maskgit: (B, 25) tokens or K; var: (B, 54, CD)
            interpolated features of the coarser scales. Returns logits (B, 25 or 55, K)."""
            c = self.cls(y)[:, None]
            if self.kind == "raster":
                h = torch.cat([c, self.tok(inp[:, :-1])], 1)
            elif self.kind == "maskgit":
                h = torch.cat([c, self.tok(inp)], 1)
            else:
                h = torch.cat([c, self.feat(inp)], 1)
                h = h + self.lvl(self.lev[:h.shape[1]])[None]
            n = h.shape[1]
            h = h + self.pos[:, :n]
            for lyr in self.layers:
                h = lyr(h, src_mask=self.mask[:n, :n])
            out = self.head(self.nf(h))
            return out[:, 1:] if self.kind == "maskgit" else out

    return Gen()


def var_inputs(idxs, book):
    """The input of each scale after the first: the picture so far (sum of the coarser scales' codes, at 5 x 5),
    averaged down to this scale's size. Returns (B, 54, CD)."""
    import torch

    fhat = 0
    ins = []
    for k, s in enumerate(SCALES[:-1]):
        fhat = fhat + up(lookup(idxs[k], book))
        ins.append(down(fhat, SCALES[k + 1]).flatten(2).transpose(1, 2))
    return torch.cat(ins, 1)


def train_gen(kind, toks, Y, book, n_steps, seed):
    import torch
    import torch.nn.functional as F

    torch.manual_seed(2024 + seed)  # Tian et al., VAR (2024)
    m = gen_net(kind)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=n_steps, pct_start=0.05)
    g = torch.Generator().manual_seed(seed)
    curve, run = [], []
    for st in range(1, n_steps + 1):
        i = torch.randint(0, len(Y), (BATCH,), generator=g)
        y = torch.where(torch.rand(BATCH, generator=g) < 0.1, torch.full_like(Y[i], 26), Y[i])
        if kind == "raster":
            tgt = toks[0][i].flatten(1)
            loss = F.cross_entropy(m(y, tgt).reshape(-1, K), tgt.reshape(-1))
        elif kind == "maskgit":
            tgt = toks[0][i].flatten(1)
            r = torch.cos(math.pi / 2 * torch.rand(BATCH, generator=g))  # MaskGIT's cosine schedule of mask ratios
            n_mask = torch.clamp((r * 25).ceil(), 1, 25)
            order = torch.argsort(torch.rand(BATCH, 25, generator=g), 1)
            masked = torch.argsort(order, 1) < n_mask[:, None]
            logits = m(y, torch.where(masked, torch.full_like(tgt, K), tgt))
            loss = F.cross_entropy(logits[masked], tgt[masked])
        else:
            idxs = [t_[i] for t_ in toks]
            tgt = torch.cat([t_.flatten(1) for t_ in idxs], 1)
            loss = F.cross_entropy(m(y, var_inputs(idxs, book)).reshape(-1, K), tgt.reshape(-1))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        sched.step()
        run.append(float(loss))
        if st % 50 == 0:
            curve.append((st, float(np.mean(run))))
            run = []
    m.eval()
    return m, curve


def guided(m, y, inp, w=GUIDE):
    import torch

    lc = m(y, inp)
    lu = m(torch.full_like(y, 26), inp)
    return lu + w * (lc - lu)


def generate(kind, m, book, letters, seed, trace=None):
    """Tokens for the requested letters. Returns the token lists (as the tokenizer's) and the number of passes."""
    import torch

    g = torch.Generator().manual_seed(seed)
    y = torch.tensor(np.asarray(letters))
    B = len(y)
    with torch.no_grad():
        if kind == "raster":
            tok = torch.zeros(B, 25, dtype=torch.long)
            for k in range(25):
                p = torch.softmax(guided(m, y, tok)[:, k], -1)
                tok[:, k] = torch.multinomial(p, 1, generator=g)[:, 0]
            return [tok.reshape(B, 5, 5)], 25
        if kind == "maskgit":
            tok = torch.full((B, 25), K, dtype=torch.long)
            for k in range(MASKGIT_STEPS):
                masked = tok == K
                logits = guided(m, y, tok)
                p = torch.softmax(logits, -1)
                cand = torch.multinomial(p.reshape(-1, K), 1, generator=g).reshape(B, 25)
                conf = torch.log(torch.gather(p, 2, cand[..., None])[..., 0] + 1e-12)
                temp = 4.5 * (1 - (k + 1) / MASKGIT_STEPS)  # MaskGIT's annealed randomness in the choice
                gum = -torch.log(-torch.log(torch.rand(B, 25, generator=g).clamp(1e-9, 1 - 1e-9)))
                conf = torch.where(masked, conf + temp * gum, torch.full_like(conf, math.inf))
                left = int(math.floor(25 * math.cos(math.pi / 2 * (k + 1) / MASKGIT_STEPS)))  # still masked after
                keep = torch.argsort(conf, 1, descending=True)[:, :25 - left]
                new = tok.clone()
                rows = torch.arange(B)[:, None]
                new[rows, keep] = torch.where(tok[rows, keep] == K, cand[rows, keep], tok[rows, keep])
                if trace is not None:
                    guess = torch.where(new == K, logits.argmax(-1), new)
                    trace.append(((new != K).numpy().copy(), guess.reshape(B, 5, 5).clone()))
                tok = new
            return [tok.reshape(B, 5, 5)], MASKGIT_STEPS
        idxs = []
        for k, s in enumerate(SCALES):
            inp = var_inputs(idxs + [torch.zeros(B, 5, 5, dtype=torch.long)] * (len(SCALES) - len(idxs)), book)
            start = sum(q * q for q in SCALES[:k])
            n_in = start + s * s  # positions up to and including this scale
            logits = guided(m, y, inp[:, :max(0, n_in - 1)])[:, start:n_in]
            p = torch.softmax(logits, -1)
            idx = torch.multinomial(p.reshape(-1, K), 1, generator=g).reshape(B, s, s)
            idxs.append(idx)
        return idxs, len(SCALES)


def to_feat(kind, idxs, book):
    f = 0
    if kind == "single":
        return lookup(idxs[0], book)
    for idx in idxs:
        f = f + up(lookup(idx, book))
    return f


def compute_tokens():
    import time

    import torch

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test], dtype=torch.float32)
    Xte = torch.tensor(imgs[test], dtype=torch.float32)
    Y = torch.tensor(labels[~test])
    nt, ng = steps(N_TOK), steps(N_GEN)
    want = np.repeat(np.arange(26), 10)
    part = CACHE.partial("tokens", dict(K=K, CD=CD, scales=SCALES, nt=nt, ng=ng, seeds=SEEDS, D=D, L=L, guide=GUIDE))
    tk = {}
    for kind in ("single", "multi"):
        path = CACHE.dir / f"tokenizer_{kind}.pt"
        if path.exists():
            enc, dec = tokenizer_nets()
            st_ = torch.load(path)
            enc.load_state_dict(st_["enc"])
            dec.load_state_dict(st_["dec"])
            enc.eval()
            dec.eval()
            book = st_["book"]
        else:
            enc, dec, book = train_tokenizer(kind, X, nt, seed=2021 if kind == "single" else 2024)  # VQGAN 2021; VAR
            torch.save(dict(enc=enc.state_dict(), dec=dec.state_dict(), book=book), path)
        tk[kind] = (enc, dec, book)
    out = dict(K=K, CD=CD, scales=list(SCALES), seeds=list(SEEDS), nt=nt, ng=ng, batch=BATCH, D=D, L=L, guide=GUIDE,
               maskgit_steps=MASKGIT_STEPS)
    # the tokenizers on held-out fonts: rebuild error, and for five scales the error after each one
    ex = np.where(test)[0][[0, 3 * 4 + 1, 3 * 17, 3 * 6 + 2]]  # A E R G
    for kind in ("single", "multi"):
        enc, dec, book = tk[kind]
        idxs, partial = encode(kind, enc, book, Xte)
        rec = decode_feat(dec, to_feat(kind, idxs, book))
        out[f"{kind}_rmse"] = float(np.sqrt(((rec - imgs[test]) ** 2).mean()))
        use = np.bincount(torch.cat([i_.flatten() for i_ in idxs]).numpy(), minlength=K)
        out[f"{kind}_used"] = int((use > 0).sum())
        pr = use / use.sum()
        out[f"{kind}_perplexity"] = float(np.exp(-(pr[pr > 0] * np.log(pr[pr > 0])).sum()))
        out[f"{kind}_rec"] = rec[np.searchsorted(np.where(test)[0], ex)]
        if kind == "multi":
            out["scale_errs"] = [float(np.sqrt(((decode_feat(dec, p_) - imgs[test]) ** 2).mean())) for p_ in partial]
            out["scale_imgs"] = np.array([decode_feat(dec, p_)[np.searchsorted(np.where(test)[0], ex)] for p_ in partial])
        print(f"    tokenizer {kind}: rebuild RMSE {out[f'{kind}_rmse']:.3f}, {out[f'{kind}_used']} codes used, "
              f"perplexity {out[f'{kind}_perplexity']:.0f}", flush=True)
    out["orig"] = imgs[ex]
    toks_tr = {kind: encode(kind, tk[kind][0], tk[kind][2], X)[0] for kind in ("single", "multi")}
    for seed in SEEDS:
        for kind in KINDS:
            key = f"{kind}_s{seed}"
            if key in part:
                continue
            tkind = "multi" if kind == "var" else "single"
            enc, dec, book = tk[tkind]
            t0 = time.time()
            m, curve = train_gen(kind, toks_tr[tkind], Y, book, ng, seed)
            secs = time.time() - t0
            t1 = time.time()
            idxs, passes = generate(kind, m, book, want, seed=70 + seed)
            gen_secs = time.time() - t1
            smp = decode_feat(dec, to_feat(tkind, idxs, book))
            q = score(smp, want)
            r = dict(acc=q["acc"], fd=q["fd"], curve=curve, passes=passes, secs=secs, gen_secs=gen_secs,
                     params=int(sum(p.numel() for p in m.parameters())), samples=smp[::26][:10].tolist())
            if seed == 0:  # the drawing, step by step, for four letters
                show = [0, 4, 17, 6]
                if kind == "maskgit":
                    tr = []
                    generate(kind, m, book, show, seed=90, trace=tr)
                    r["trace_mask"] = [t_[0].astype(int).tolist() for t_ in tr]
                    r["trace_imgs"] = [decode_feat(dec, to_feat("single", [t_[1]], book)).tolist() for t_ in tr]
                elif kind == "var":
                    ii, _ = generate(kind, m, book, show, seed=90)
                    r["trace_imgs"] = [decode_feat(dec, to_feat("multi", ii[:k + 1], book)).tolist()
                                       for k in range(len(SCALES))]
                else:
                    ii, _ = generate(kind, m, book, show, seed=90)
                    r["trace_imgs"] = [decode_feat(dec, to_feat("single", ii, book)).tolist()]
            part[key] = r
            print(f"    {key}: right letter {q['acc']:.3f}, FD {q['fd']:.1f}, {passes} passes "
                  f"({secs:.0f}s training)", flush=True)
    for kind in KINDS:
        ps = [part[f"{kind}_s{s}"] for s in SEEDS]
        out[f"{kind}_acc"] = [p_["acc"] for p_ in ps]
        out[f"{kind}_fd"] = [p_["fd"] for p_ in ps]
        out[f"{kind}_passes"] = ps[0]["passes"]
        out[f"{kind}_params"] = ps[0]["params"]
        out[f"{kind}_gen_secs"] = float(np.mean([p_["gen_secs"] for p_ in ps]))
        out[f"{kind}_curve"] = np.array([np.array(p_["curve"]) for p_ in ps])
        out[f"{kind}_samples"] = np.array(ps[0]["samples"])
        out[f"{kind}_trace"] = np.array(ps[0]["trace_imgs"])
    out["maskgit_trace_mask"] = np.array(part["maskgit_s0"]["trace_mask"])
    return out
