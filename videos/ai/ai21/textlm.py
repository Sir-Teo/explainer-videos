"""Part 21's text models (the ``textlm`` item): a masked-diffusion language model and an autoregressive one of exactly
the same size, trained on the thirty novels (Part 13's characters and rotary positions) with the same initial weights,
the same batches and the same number of steps, two seeds each.

    mdm   two-way attention; a string of T characters with k of them blanked (k uniform from 1 to T, the blanks at
          random), trained to guess every blank: the loss, the average over the blanks, is an unbiased estimate of
          the variational bound per character (Part 21's derivation: the 1/t-weighted cross-entropy, with t's weight
          turned into the blanks' count)
    ar    causal attention, the next character from the ones before (a start symbol first): the exact log-likelihood

Measured: held-out bits per character through training (the bound, the exact value); the bound on the scoreboard's
passage, in blocks of T characters, and the autoregressive model's bits on the same blocks; three estimates of the
bound that the derivation says agree (1/t-weighted random blanks, a fixed count of blanks, one random order); the
diffusion model read left to right; writing: samples of T characters by unmasking (the surest guesses first, as in
LLaDA, or at random), with 1 to T rounds, and in blocks left to right; each judged by an autoregressive model of the
other seed (bits per character; lower reads more like the novels).  Replay: the diffusion model filling in a passage
with half its characters blanked, and both models writing, at checkpoints.

Resumable: each run checkpoints every 100 steps (model, optimizer, schedule and random states) in .cache/ai21/.
"""

from __future__ import annotations

import math
import os
import time

import numpy as np

QUICK = os.environ.get("AI21_QUICK") == "1"
T, D, LAYERS, HEADS = 64, 128, 4, 4
STEPS = 80 if QUICK else 4000
BATCH = 32
SEEDS = (0, 1)
EVAL_AT = sorted({0, 100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, STEPS}) if not QUICK else [0, 40, STEPS]
CKPT_EVERY = 100
FILL = "Spade sat down in the armchair beside the table and looked at h"  # replaced by a passage line below


def rng(seed):
    return np.random.Generator(np.random.PCG64(seed))


def build(K, causal):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    from videos.ai.ai13 import compute as c13

    th = torch.tensor(c13.rope_freqs(D // HEADS), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)
    dh = D // HEADS

    def rot(t):
        a, b = t[..., : dh // 2], t[..., dh // 2:]
        return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1, self.n2 = nn.LayerNorm(D), nn.LayerNorm(D)
            self.qkv = nn.Linear(D, 3 * D, bias=False)
            self.o = nn.Linear(D, D, bias=False)
            self.f1, self.f2 = nn.Linear(D, 4 * D), nn.Linear(4 * D, D)

        def forward(self, x):
            B = x.shape[0]
            q, k, v = self.qkv(self.n1(x)).view(B, T, 3, HEADS, dh).permute(2, 0, 3, 1, 4)
            a = F.scaled_dot_product_attention(rot(q), rot(k), v, is_causal=causal)
            x = x + self.o(a.transpose(1, 2).reshape(B, T, D))
            return x + self.f2(F.gelu(self.f1(self.n2(x))))

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(K + 1, D)  # + the blank (diffusion) or the start symbol (autoregressive)
            self.blocks = nn.ModuleList([Block() for _ in range(LAYERS)])
            self.nf = nn.LayerNorm(D)
            self.out = nn.Linear(D, K)

        def forward(self, x):
            h = self.emb(x)
            for b in self.blocks:
                h = b(h)
            return self.out(self.nf(h))

    return Net()


def blank(x, k, g, special):
    """Blank exactly k[i] random positions of row i (numpy generator g)."""
    import torch

    r = torch.tensor(g.random(x.shape))
    rank = r.argsort(1).argsort(1)
    m = rank < k[:, None]
    return torch.where(m, torch.full_like(x, special), x), m


def ar_input(x, special):
    import torch

    return torch.cat([torch.full_like(x[:, :1], special), x[:, :-1]], 1)


def loss_of(kind, net, x, g, K):
    """nats per character: the bound's estimate (diffusion) or the exact log-loss (autoregressive)."""
    import torch
    import torch.nn.functional as F

    if kind == "ar":
        return F.cross_entropy(net(ar_input(x, K)).reshape(-1, K), x.reshape(-1))
    k = torch.tensor(g.integers(1, T + 1, len(x)))
    xm, m = blank(x, k, g, K)
    ce = F.cross_entropy(net(xm).reshape(-1, K), x.reshape(-1), reduction="none").view(len(x), T)
    return ((ce * m).sum(1) / k).mean()


# ---------------------------------------------------------------------------
# Scoring blocks of T characters
def ar_bits(net, blocks, K, chunk=256):
    """Per block: -log2 p(block), the autoregressive model's exact code length."""
    import torch
    import torch.nn.functional as F

    out = []
    with torch.no_grad():
        for i in range(0, len(blocks), chunk):
            x = blocks[i:i + chunk]
            ce = F.cross_entropy(net(ar_input(x, K)).reshape(-1, K), x.reshape(-1), reduction="none").view(len(x), T)
            out.append(ce.sum(1).numpy() / math.log(2))
    return np.concatenate(out)


def mdm_bound(net, blocks, K, seed=0, chunk=256):
    """Per block: the bound, sum over k = 1..T of (1/k) E[sum of the cross-entropy of k random blanks], one random set
    of blanks for each k (a stratified estimate), in bits."""
    import torch
    import torch.nn.functional as F

    g = rng(seed)
    per = np.zeros(len(blocks))
    with torch.no_grad():
        X = blocks.repeat_interleave(T, 0)
        k = torch.arange(1, T + 1).repeat(len(blocks))
        for i in range(0, len(X), chunk):
            x, kk = X[i:i + chunk], k[i:i + chunk]
            xm, m = blank(x, kk, g, K)
            ce = F.cross_entropy(net(xm).reshape(-1, K), x.reshape(-1), reduction="none").view(len(x), T)
            v = ((ce * m).sum(1) / kk).numpy() / math.log(2)
            np.add.at(per, np.arange(i, i + len(x)) // T, v)
    return per


def mdm_bound_t(net, blocks, K, draws=64, seed=0, chunk=256):
    """The same bound in its training-paper form: t uniform (stratified), each character blanked with probability t,
    (1/t) times the blanks' cross-entropy."""
    import torch
    import torch.nn.functional as F

    g = rng(seed)
    per = np.zeros(len(blocks))
    with torch.no_grad():
        X = blocks.repeat_interleave(draws, 0)
        u = (np.arange(draws)[None] + g.random((len(blocks), draws))) / draws
        t = torch.tensor(u.reshape(-1), dtype=torch.float32)
        for i in range(0, len(X), chunk):
            x, tt = X[i:i + chunk], t[i:i + chunk]
            m = torch.tensor(g.random(x.shape)) < tt[:, None]
            xm = torch.where(m, torch.full_like(x, K), x)
            ce = F.cross_entropy(net(xm).reshape(-1, K), x.reshape(-1), reduction="none").view(len(x), T)
            v = ((ce * m).sum(1) / tt).numpy() / math.log(2)
            np.add.at(per, np.arange(i, i + len(x)) // draws, v / draws)
    return per


def mdm_order(net, blocks, K, order="random", seed=0, chunk=256):
    """The diffusion model as an autoregressive model in one order: reveal the characters one at a time (in a random
    order, or left to right), each predicted from those revealed so far; bits per block."""
    import torch
    import torch.nn.functional as F

    g = rng(seed)
    per = np.zeros(len(blocks))
    with torch.no_grad():
        rows, pos = [], []
        for b in range(len(blocks)):
            o = g.permutation(T) if order == "random" else np.arange(T)
            for j in range(T):
                hidden = np.zeros(T, bool)
                hidden[o[j:]] = True
                rows.append(hidden)
                pos.append((b, o[j]))
        H = torch.tensor(np.array(rows))
        P = np.array(pos)
        X = blocks[torch.tensor(P[:, 0])]
        for i in range(0, len(X), chunk):
            x, h = X[i:i + chunk], H[i:i + chunk]
            xm = torch.where(h, torch.full_like(x, K), x)
            lp = F.log_softmax(net(xm), -1)
            j = torch.tensor(P[i:i + chunk, 1])
            v = -lp[torch.arange(len(x)), j, x[torch.arange(len(x)), j]].numpy() / math.log(2)
            np.add.at(per, P[i:i + chunk, 0], v)
    return per


# ---------------------------------------------------------------------------
def mdm_write(net, K, n, steps, order="confidence", blocks=1, seed=0, temp=1.0, frames=False):
    """Write n strings of T characters from all blanks in `steps` rounds (split evenly over `blocks` blocks, left to
    right): each round guesses every blank and keeps the surest guesses (or random ones)."""
    import torch

    gen = torch.Generator().manual_seed(seed)
    x = torch.full((n, T), K)
    bl = T // blocks
    per_block = max(1, steps // blocks)
    hist = [x[0].clone()]
    with torch.no_grad():
        for b in range(blocks):
            inb = torch.zeros(T, dtype=torch.bool)
            inb[b * bl:(b + 1) * bl] = True
            for r in range(per_block):
                p = torch.softmax(net(x) / temp, -1)
                choice = torch.multinomial(p.view(-1, K), 1, generator=gen).view(n, T)
                conf = p.gather(2, choice[..., None])[..., 0]
                masked = (x == K) & inb[None]
                left = int(masked[0].sum())
                k = left // (per_block - r)
                if k == 0:
                    continue
                if order == "confidence":
                    score = torch.where(masked, conf, torch.full_like(conf, -1.0))
                else:
                    score = torch.where(masked, torch.rand(n, T, generator=gen), torch.full_like(conf, -1.0))
                idx = torch.topk(score, k, dim=1).indices
                x.scatter_(1, idx, choice.gather(1, idx))
                hist.append(x[0].clone())
    return (x, hist) if frames else x


def ar_write(net, K, n, seed=0, temp=1.0):
    import torch

    gen = torch.Generator().manual_seed(seed)
    x = torch.full((n, T), K)
    out = torch.zeros((n, T), dtype=torch.long)
    with torch.no_grad():
        for j in range(T):
            inp = torch.cat([torch.full((n, 1), K), out[:, :T - 1]], 1)
            p = torch.softmax(net(inp)[:, j] / temp, -1)
            out[:, j] = torch.multinomial(p, 1, generator=gen)[:, 0]
    del x
    return out


def text_of(chars, row, K):
    return "".join("_" if int(c) == K else chars[int(c)] for c in row)


def unigram_entropy(rows, K):
    c = np.bincount(np.asarray(rows).reshape(-1), minlength=K + 1)[:K].astype(float)
    p = c[c > 0] / c.sum()
    return float(-(p * np.log2(p)).sum())


# ---------------------------------------------------------------------------
def threads():
    import torch

    torch.set_num_threads(int(os.environ.get("AI21_THREADS", "2")))


def train_run(kind, seed, data, chars, enc, K, cache_dir, fill):
    """One model, resumable; returns its curve and replay."""
    import torch

    tr, va = data["train"], data["valid"]
    vblocks = va[: 64 * T].view(64, T)
    torch.manual_seed(2025 + seed)  # the same initial weights for both kinds (Nie et al., LLaDA, 2025)
    net = build(K, causal=(kind == "ar"))
    n_params = sum(p_.numel() for p_ in net.parameters())
    decay = [p_ for p_ in net.parameters() if p_.dim() >= 2]
    other = [p_ for p_ in net.parameters() if p_.dim() < 2]
    opt = torch.optim.AdamW([dict(params=decay, weight_decay=0.1), dict(params=other, weight_decay=0.0)], lr=2e-3,
                            betas=(0.9, 0.95))
    warm = max(1, STEPS // 40)

    def lr_at(s):
        if s < warm:
            return (s + 1) / warm
        return 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, STEPS - warm)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_at)
    g_data, g_mask = rng(1000 + seed), rng(2000 + seed)  # the same batches for both kinds
    ckpt = cache_dir / f"lm_{kind}{seed}.ckpt.pt"
    config = dict(kind=kind, seed=seed, T=T, D=D, L=LAYERS, H=HEADS, steps=STEPS, batch=BATCH)
    ck = torch.load(ckpt, weights_only=False) if ckpt.exists() else None
    if ck is not None and ck["config"] == config:
        net.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        sched.load_state_dict(ck["sched"])
        g_data.bit_generator.state, g_mask.bit_generator.state = ck["g_data"], ck["g_mask"]
        torch.set_rng_state(ck["torch_rng"])
        curve, replay, train_curve, start = ck["curve"], ck["replay"], ck["train_curve"], ck["step"] + 1
        print(f"    {kind}{seed}: resuming at step {start}", flush=True)
    else:
        curve, replay, train_curve, start = [], [], [], 1
    fill_x, fill_m = fill

    def evaluate(step):
        net.eval()
        if kind == "ar":
            b = ar_bits(net, vblocks, K).mean() / T
        else:
            b = mdm_bound(net, vblocks, K, seed=step).mean() / T
        curve.append((step, float(b)))
        r = dict(step=step, bits=float(b))
        with torch.no_grad():
            if kind == "mdm":
                xm = torch.where(fill_m, torch.full_like(fill_x, K), fill_x)
                guess = net(xm[None])[0].argmax(-1)
                r["fill"] = text_of(chars, torch.where(fill_m, guess, fill_x), K)
                r["fill_right"] = float((guess[fill_m] == fill_x[fill_m]).float().mean())
                r["write"] = text_of(chars, mdm_write(net, K, 1, 16, seed=3)[0], K)
            else:
                r["write"] = text_of(chars, ar_write(net, K, 1, seed=3)[0], K)
        replay.append(r)
        print(f"    {kind}{seed} step {step}: held-out {'bound' if kind == 'mdm' else 'bits'} {b:.3f}  "
              f"[{r['write'][:48]!r}]", flush=True)
        net.train()

    t0 = time.time()
    if start == 1:
        evaluate(0)
    net.train()
    run = []
    for step in range(start, STEPS + 1):
        st = g_data.integers(0, len(tr) - T - 1, BATCH)
        x = tr[torch.tensor(st)[:, None] + torch.arange(T)[None]]
        loss = loss_of(kind, net, x, g_mask, K)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()
        run.append(loss.item() / math.log(2))
        if step % 50 == 0:
            train_curve.append((step, float(np.mean(run))))
            run = []
        if step in EVAL_AT:
            evaluate(step)
            print(f"      ({(time.time() - t0) / max(1, step - start + 1):.2f} s/step)", flush=True)
        if step % CKPT_EVERY == 0 and step < STEPS:
            tmp = ckpt.with_suffix(".tmp")
            torch.save(dict(config=config, model=net.state_dict(), opt=opt.state_dict(), sched=sched.state_dict(),
                            g_data=g_data.bit_generator.state, g_mask=g_mask.bit_generator.state,
                            torch_rng=torch.get_rng_state(), curve=curve, replay=replay, train_curve=train_curve,
                            step=step), tmp)
            tmp.replace(ckpt)
    net.eval()
    torch.save(net.state_dict(), cache_dir / f"lm_{kind}{seed}.pt")
    ckpt.unlink(missing_ok=True)
    return dict(curve=curve, replay=replay, train_curve=train_curve, n_params=int(n_params))


def load_lm(kind, seed, K, cache_dir):
    import torch

    net = build(K, causal=(kind == "ar"))
    net.load_state_dict(torch.load(cache_dir / f"lm_{kind}{seed}.pt"))
    net.eval()
    return net


def compute_textlm():
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai21.compute import CACHE

    threads()
    chars, enc, data = c13.corpus()
    K = len(chars)
    ps, va = data["passage"], data["valid"]
    # the replay's fill-in: a line of the passage, every other character (at random) blanked
    text = "".join(chars[int(i)] for i in ps[:3000])
    s0 = text.index(". ", 1200) + 2
    fill_x = ps[s0:s0 + T].clone()
    fill_m = torch.tensor(rng(5).random(T) < 0.5)
    part = CACHE.partial("textlm", dict(steps=STEPS, batch=BATCH, T=T, D=D, L=LAYERS, seeds=list(SEEDS)))
    for seed in SEEDS:
        for kind in ("mdm", "ar"):
            key = f"{kind}{seed}"
            if key in part and (CACHE.dir / f"lm_{key}.pt").exists():
                continue
            part[key] = train_run(kind, seed, data, chars, enc, K, CACHE.dir, (fill_x, fill_m))
    out = dict(T=T, d=D, layers=LAYERS, heads=HEADS, steps=STEPS, batch=BATCH, seeds=list(SEEDS), K=K,
               tokens=STEPS * BATCH * T, eval_at=EVAL_AT, fill_src=text_of(chars, fill_x, K),
               fill_mask=fill_m.numpy().astype(int))
    for key in part.done:
        p = part[key]
        out[f"{key}_curve"] = np.array(p["curve"])
        out[f"{key}_train"] = np.array(p["train_curve"])
        out[f"{key}_replay"] = p["replay"]
        out["n_params"] = p["n_params"]
    # ---- the scoreboard's passage, in blocks of T characters, and held-out blocks
    nb = len(ps) // T
    pblocks = ps[: nb * T].view(nb, T)
    vb = va[200_000: 200_000 + 512 * T].view(512, T)
    nets = {f"{k}{s}": load_lm(k, s, K, CACHE.dir) for s in SEEDS for k in ("mdm", "ar")}
    for s in SEEDS:
        m, a = nets[f"mdm{s}"], nets[f"ar{s}"]
        pb = (mdm_bound(m, pblocks, K, seed=11) + mdm_bound(m, pblocks, K, seed=12)) / 2
        out[f"mdm{s}_passage"] = float(pb.mean() / T)
        out[f"mdm{s}_passage_se"] = float(pb.std() / math.sqrt(len(pb)) / T)
        out[f"ar{s}_passage"] = float(ar_bits(a, pblocks, K).mean() / T)
        vm, va_ = mdm_bound(m, vb, K, seed=13), ar_bits(a, vb, K)
        out[f"mdm{s}_valid"], out[f"ar{s}_valid"] = float(vm.mean() / T), float(va_.mean() / T)
        out[f"mdm{s}_valid_se"], out[f"ar{s}_valid_se"] = float(vm.std() / math.sqrt(len(vm)) / T), float(va_.std() / math.sqrt(len(va_)) / T)
        print(f"    seed {s}: passage bound {out[f'mdm{s}_passage']:.3f} +- {out[f'mdm{s}_passage_se']:.3f}, "
              f"autoregressive {out[f'ar{s}_passage']:.3f}; held-out {out[f'mdm{s}_valid']:.3f} vs {out[f'ar{s}_valid']:.3f}",
              flush=True)
    # ---- three estimates of the same bound, and the left-to-right reading (seed 0, 256 held-out blocks)
    m = nets["mdm0"]
    vb2 = vb[:256]
    for name, per in (("est_k", mdm_bound(m, vb2, K, seed=21)), ("est_t", mdm_bound_t(m, vb2, K, seed=22)),
                      ("est_order", mdm_order(m, vb2, K, "random", seed=23)), ("l2r", mdm_order(m, vb2, K, "l2r"))):
        out[name], out[f"{name}_se"] = float(per.mean() / T), float(per.std() / math.sqrt(len(per)) / T)
        print(f"    {name}: {out[name]:.3f} +- {out[name + '_se']:.3f}", flush=True)
    out["ar0_vb2"] = float(ar_bits(nets["ar0"], vb2, K).mean() / T)
    # ---- writing: judged by the autoregressive model of the other seed
    judge = nets["ar1"]
    out["judge_real"] = float(ar_bits(judge, vb[:128], K).mean() / T)
    out["real_unigram"] = unigram_entropy(vb[:128].numpy(), K)
    rows = []
    configs = [(st, "confidence", 1) for st in (64, 32, 16, 8, 4, 2, 1)] + [(st, "random", 1) for st in (64, 16, 4, 1)] \
        + [(16, "confidence", 4), (64, "confidence", 4)]
    for st, order, blocks in configs:
        x = mdm_write(m, K, 64, st, order=order, blocks=blocks, seed=100 + st)
        jb = ar_bits(judge, x, K) / T
        rows.append(dict(steps=st, order=order, blocks=blocks, judge=float(jb.mean()), judge_se=float(jb.std() / 8),
                         unigram=unigram_entropy(x.numpy(), K), sample=text_of(chars, x[0], K)))
        print(f"    write {st:2d} rounds, {order}, {blocks} block(s): judge {jb.mean():.3f}; '{rows[-1]['sample'][:50]}'",
              flush=True)
    x = ar_write(nets["ar0"], K, 64, seed=7)
    jb = ar_bits(judge, x, K) / T
    out["ar_write"] = dict(judge=float(jb.mean()), judge_se=float(jb.std() / 8), unigram=unigram_entropy(x.numpy(), K),
                           sample=text_of(chars, x[0], K))
    out["writes"] = rows
    # the chapter's writing animation: three strings, 16 rounds, the surest first, every round kept
    frames = []
    for sd in (1, 2, 3):
        _, hist = mdm_write(m, K, 1, 16, seed=sd, frames=True)
        frames.append([text_of(chars, h, K) for h in hist])
    out["frames"] = frames
    return out
