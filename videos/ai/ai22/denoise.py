"""Part 22, chapters 4-6: what does the denoising, how the condition goes in, and borrowed representations.

    denoisers   five denoisers trained by Part 21's flow matching on the letter pictures, class-conditional (label
                dropped 10% of the time, for guidance), at equal steps, batches and data order, three seeds each:
                  zero     a diffusion transformer with adaLN-Zero (Peebles & Xie 2023)
                  ada      the same with plain adaLN (scale and shift, no gate, ordinary initialization)
                  context  the same with the time and the letter as two extra tokens (in-context conditioning)
                  unet     a small U-Net (convolutions, skips, attention at 5 x 5; adaptive group norm)
                  repa     adaLN-Zero plus REPA: block 2's tokens aligned with chapter 1's frozen vision transformer
                Every model is scored at checkpoints on 260 pictures (ten of each letter, the same noise for all) by
                the judge: the share read as the requested letter, and the Frechet distance of the judge's features.
    showcase    adaLN-Zero, seed 0, trained four times as long (8,000 steps): samples from fixed noise at
                checkpoints, its gates opening, the alphabet with its denoising path (resumable: checkpoints)
    guidance    classifier-free guidance weights on the showcase model: accuracy, distance, variety
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from videos.ai.ai22.base import CACHE, GL, NP, P, dataset, patches, score, steps, threads, unpatch

CONFIGS = ("zero", "ada", "context", "unet", "repa")
SEEDS = (0, 1, 2)
D, L, H = 64, 4, 4
BATCH, LR = 64, 1e-3
N_STEPS = 2000
EVAL_FRACS = (0.1, 0.2, 0.4, 0.6, 1.0)
SNAP_FRACS = (0.0, 0.04, 0.1, 0.2, 0.4, 1.0)
REPA_LAYER, REPA_W = 2, 0.5  # align the tokens after block 2 of 4
GUIDE = 2.0  # classifier-free guidance weight for every sample here


def nets():
    import torch
    import torch.nn as nn

    class Cond(nn.Module):
        """The condition c: random Fourier features of the time t through a small MLP, plus the letter's vector
        (26 letters and 'no letter')."""

        def __init__(self):
            super().__init__()
            self.freq = nn.Parameter(torch.randn(D // 2) * 4.0, requires_grad=False)
            self.tmlp = nn.Sequential(nn.Linear(D, D), nn.SiLU(), nn.Linear(D, D))
            self.lab = nn.Embedding(27, D)

        def parts(self, t, y):
            a = t[:, None] * self.freq[None] * 2 * math.pi
            return self.tmlp(torch.cat([torch.sin(a), torch.cos(a)], 1)), self.lab(y)

        def forward(self, t, y):
            ct, cy = self.parts(t, y)
            return ct + cy

    class Block(nn.Module):
        def __init__(self, mode):
            super().__init__()
            self.mode = mode
            aff = mode == "plain"
            self.n1 = nn.LayerNorm(D, elementwise_affine=aff)
            self.n2 = nn.LayerNorm(D, elementwise_affine=aff)
            self.att = nn.MultiheadAttention(D, H, batch_first=True)
            self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
            if mode != "plain":
                self.ada = nn.Linear(D, (6 if mode == "zero" else 4) * D)
                if mode == "zero":  # every block starts as the identity: its gates are zero
                    nn.init.zeros_(self.ada.weight)
                    nn.init.zeros_(self.ada.bias)

        def forward(self, h, c):
            if self.mode == "plain":
                a = self.n1(h)
                h = h + self.att(a, a, a, need_weights=False)[0]
                return h + self.mlp(self.n2(h))
            m = self.ada(c)[:, None]
            if self.mode == "zero":
                s1, b1, g1, s2, b2, g2 = m.chunk(6, -1)
            else:
                (s1, b1, s2, b2), g1, g2 = m.chunk(4, -1), 1.0, 1.0
            a = self.n1(h) * (1 + s1) + b1
            h = h + g1 * self.att(a, a, a, need_weights=False)[0]
            return h + g2 * self.mlp(self.n2(h) * (1 + s2) + b2)

    class DiT(nn.Module):
        """Patch tokens (4 x 4 pixels), learned positions, four blocks; out: the velocity, patch by patch."""

        def __init__(self, cond="zero", repa=False):
            super().__init__()
            self.kind = cond
            mode = {"zero": "zero", "ada": "ada", "context": "plain"}[cond]
            self.embed = nn.Linear(P * P, D)
            self.pos = nn.Parameter(torch.randn(1, NP + (2 if cond == "context" else 0), D) * 0.02)
            self.cond = Cond()
            self.blocks = nn.ModuleList([Block(mode) for _ in range(L)])
            self.nf = nn.LayerNorm(D, elementwise_affine=cond == "context")
            if cond != "context":
                self.fada = nn.Linear(D, 2 * D)
            self.out = nn.Linear(D, P * P)
            if cond == "zero":
                for lin in (self.fada, self.out):
                    nn.init.zeros_(lin.weight)
                    nn.init.zeros_(lin.bias)
            self.proj = nn.Sequential(nn.Linear(D, 128), nn.SiLU(), nn.Linear(128, 128), nn.SiLU(),
                                      nn.Linear(128, 64)) if repa else None

        def forward(self, x, t, y, keep=False):
            h = self.embed(patches(x))
            if self.kind == "context":  # the time and the letter as two more tokens in the sequence
                ct, cy = self.cond.parts(t, y)
                h = torch.cat([ct[:, None], cy[:, None], h], 1) + self.pos
                c = None
            else:
                h = h + self.pos
                c = self.cond(t, y)
            mid = None
            for k, b in enumerate(self.blocks):
                h = b(h, c)
                if k + 1 == REPA_LAYER:
                    mid = h
            if self.kind == "context":
                h = self.nf(h)[:, 2:]
            else:
                sh, sc = self.fada(c)[:, None].chunk(2, -1)
                h = self.nf(h) * (1 + sc) + sh
            v = unpatch(self.out(h))
            if keep:
                return v, (self.proj(mid) if self.proj is not None else mid)
            return v

        def gates(self, c):
            """Mean |gate| of the attention and MLP branches of each block, for conditions c (adaLN-Zero only)."""
            out = []
            for b in self.blocks:
                _, _, g1, _, _, g2 = b.ada(c).chunk(6, -1)
                out.append([float(g1.abs().mean()), float(g2.abs().mean())])
            return out

    class ResBlock(nn.Module):
        def __init__(self, cin, cout):
            super().__init__()
            self.n1 = nn.GroupNorm(8, cin)
            self.c1 = nn.Conv2d(cin, cout, 3, padding=1)
            self.emb = nn.Linear(D, 2 * cout)  # the condition sets each block's scale and shift (adaptive group norm)
            self.n2 = nn.GroupNorm(8, cout, affine=False)
            self.c2 = nn.Conv2d(cout, cout, 3, padding=1)
            self.skip = nn.Conv2d(cin, cout, 1) if cin != cout else nn.Identity()

        def forward(self, x, c):
            h = self.c1(nn.functional.silu(self.n1(x)))
            s, b = self.emb(c)[:, :, None, None].chunk(2, 1)
            h = self.c2(nn.functional.silu(self.n2(h) * (1 + s) + b))
            return self.skip(x) + h

    class UNet(nn.Module):
        """20 x 20 (24 channels) -> 10 x 10 (48) -> 5 x 5 (64, with self-attention) and back up, with skips."""

        def __init__(self):
            super().__init__()
            self.kind = "unet"
            self.cond = Cond()
            self.inp = nn.Conv2d(1, 24, 3, padding=1)
            self.r1 = ResBlock(24, 24)
            self.d1 = nn.Conv2d(24, 48, 3, 2, 1)
            self.r2 = ResBlock(48, 48)
            self.d2 = nn.Conv2d(48, 64, 3, 2, 1)
            self.r3 = ResBlock(64, 64)
            self.an = nn.GroupNorm(8, 64)
            self.att = nn.MultiheadAttention(64, 4, batch_first=True)
            self.u2 = nn.ConvTranspose2d(64, 48, 4, 2, 1)
            self.r5 = ResBlock(96, 48)
            self.u1 = nn.ConvTranspose2d(48, 24, 4, 2, 1)
            self.r6 = ResBlock(48, 24)
            self.on = nn.GroupNorm(8, 24)
            self.out = nn.Conv2d(24, 1, 3, padding=1)
            nn.init.zeros_(self.out.weight)
            nn.init.zeros_(self.out.bias)

        def forward(self, x, t, y, keep=False):
            c = self.cond(t, y)
            h1 = self.r1(self.inp(x[:, None]), c)
            h2 = self.r2(self.d1(h1), c)
            h3 = self.r3(self.d2(h2), c)
            B = len(x)
            a = self.an(h3).flatten(2).transpose(1, 2)
            h3 = h3 + self.att(a, a, a, need_weights=False)[0].transpose(1, 2).reshape(B, 64, 5, 5)
            u = self.r5(torch.cat([self.u2(h3), h2], 1), c)
            u = self.r6(torch.cat([self.u1(u), h1], 1), c)
            v = self.out(nn.functional.silu(self.on(u)))[:, 0]
            return (v, None) if keep else v

    return DiT, UNet


def make(cfg):
    DiT, UNet = nets()
    if cfg == "unet":
        return UNet()
    if cfg == "repa":
        return DiT("zero", repa=True)
    return DiT(cfg)


def sample(m, letters, n_steps=20, w=GUIDE, seed=7, z=None, path=None, every=2):
    """Euler steps of the learned flow from noise (t = 0) to letters (t = 1), with classifier-free guidance."""
    import torch

    y = torch.tensor(np.asarray(letters))
    x = z.clone() if z is not None else torch.randn(len(y), GL, GL, generator=torch.Generator().manual_seed(seed))
    u = torch.full_like(y, 26)
    with torch.no_grad():
        for k in range(n_steps):
            if path is not None and k % every == 0:
                path.append(((x.numpy() + 1) / 2).clip(0, 1))
            t = torch.full((len(y),), k / n_steps)
            vc, vu = m(x, t, y), m(x, t, u)
            x = x + (vu + w * (vc - vu)) / n_steps
    out = ((x.numpy() + 1) / 2).clip(0, 1)
    if path is not None:
        path.append(out)
    return out


def train(cfg, seed, X, Y, n_steps, vit=None, on_step=None, ckpt=None, state=None, every=500):
    """Flow matching: x_t = (1 - t) noise + t data, the velocity data - noise as the target. The batches, the noise
    and the times depend only on the seed, so every configuration of a seed sees exactly the same data.
    With ``ckpt`` (a path), the model, optimizer, schedule, generators, curves and ``state`` (a dict ``on_step``
    fills) are saved every ``every`` steps, and a run that finds the file resumes from it."""
    import torch

    torch.manual_seed(2023 + seed)  # Peebles & Xie, Scalable Diffusion Models with Transformers
    m = make(cfg)
    opt = torch.optim.AdamW(m.parameters(), lr=LR, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=LR, total_steps=n_steps, pct_start=0.05)
    g = torch.Generator().manual_seed(seed)
    curve, run, align = [], [], []
    start = 1
    if ckpt is not None and ckpt.exists():
        c = torch.load(ckpt, weights_only=False)
        m.load_state_dict(c["m"])
        opt.load_state_dict(c["opt"])
        sched.load_state_dict(c["sched"])
        g.set_state(c["g"])
        torch.set_rng_state(c["rng"])
        curve, run, align = c["curve"], c["run"], c["align"]
        if state is not None:
            state.clear()
            state.update(c["state"])
        start = c["st"] + 1
        print(f"      resumed at step {c['st']}", flush=True)
    elif on_step is not None:
        on_step(0, m)
    for st in range(start, n_steps + 1):
        i = torch.randint(0, len(X), (BATCH,), generator=g)
        x1, y = X[i], Y[i]
        y = torch.where(torch.rand(BATCH, generator=g) < 0.1, torch.full_like(y, 26), y)
        x0 = torch.randn(BATCH, GL, GL, generator=g)
        t = torch.rand(BATCH, generator=g)
        xt = (1 - t[:, None, None]) * x0 + t[:, None, None] * x1
        if cfg == "repa":
            v, z = m(xt, t, y, keep=True)
            with torch.no_grad():
                f = vit.features((x1 + 1) / 2)  # the clean picture's tokens, by the frozen vision transformer
            cos = torch.nn.functional.cosine_similarity(z, f, dim=-1).mean()
            loss = ((v - (x1 - x0)) ** 2).mean()
            total = loss + REPA_W * (1 - cos)
            align.append(float(cos))
        else:
            loss = ((m(xt, t, y) - (x1 - x0)) ** 2).mean()
            total = loss
        opt.zero_grad()
        total.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        sched.step()
        run.append(float(loss))
        if st % 50 == 0:
            curve.append((st, float(np.mean(run)), float(np.mean(align[-50:])) if align else 0.0))
            run = []
        if on_step is not None:
            on_step(st, m)
        if ckpt is not None and st % every == 0 and st < n_steps:
            torch.save(dict(m=m.state_dict(), opt=opt.state_dict(), sched=sched.state_dict(), g=g.get_state(),
                            rng=torch.get_rng_state(), curve=curve, run=run, align=align, state=state, st=st),
                       str(ckpt) + ".tmp")
            Path(str(ckpt) + ".tmp").replace(ckpt)
    m.eval()
    return m, curve


def macs(m) -> int:
    import torch
    from torch.utils.flop_counter import FlopCounterMode

    x = torch.zeros(1, GL, GL)
    with FlopCounterMode(display=False) as fc, torch.no_grad():
        m(x, torch.zeros(1), torch.zeros(1, dtype=torch.long))
    return int(fc.get_total_flops() // 2)


def compute_denoisers():
    import time

    import torch

    from videos.ai.ai22.vision import load_vit

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test] * 2 - 1, dtype=torch.float32)
    Y = torch.tensor(labels[~test])
    n = steps(N_STEPS)
    eval_at = sorted({max(1, int(round(f * n))) for f in EVAL_FRACS})
    snap_at = sorted({int(round(f * n)) for f in SNAP_FRACS})
    want = np.repeat(np.arange(26), 10)
    vit = load_vit()
    part = CACHE.partial("denoisers", dict(configs=CONFIGS, seeds=SEEDS, steps=n, D=D, L=L, batch=BATCH, lr=LR,
                                           repa=[REPA_LAYER, REPA_W], guide=GUIDE))
    z_snap = torch.randn(10, GL, GL, generator=torch.Generator().manual_seed(11))
    show = np.zeros((10,), int) + np.arange(10)  # A to J
    cg = torch.Generator().manual_seed(5)
    c_t, c_y = torch.rand(64, generator=cg), torch.randint(0, 26, (64,), generator=cg)
    for seed in SEEDS:
        for cfg in CONFIGS:
            key = f"{cfg}_s{seed}"
            if key in part and (key != "zero_s0" or (CACHE.dir / "dit_showcase.npz").exists()):
                continue
            t0 = time.time()
            evals, snaps, gates, snap_read = [], [], [], []

            def on_step(st, m, cfg=cfg, seed=seed):
                if cfg == "zero" and seed == 0:
                    if st % 25 == 0:
                        with torch.no_grad():
                            gates.append([st] + sum(m.gates(m.cond(c_t, c_y)), []))
                    if st in snap_at:
                        m.eval()
                        snaps.append(sample(m, show, z=z_snap))
                        m.train()
                        snap_read.append(score(snaps[-1], show)["acc"])
                if st in eval_at:
                    m.eval()
                    q = score(sample(m, want, seed=7), want)
                    m.train()
                    evals.append(dict(step=st, acc=q["acc"], fd=q["fd"]))
                    print(f"      {cfg} s{seed} step {st}: right letter {q['acc']:.3f}, FD {q['fd']:.1f}", flush=True)

            m, curve = train(cfg, seed, X, Y, n, vit=vit, on_step=on_step)
            final = sample(m, show, z=z_snap)
            part_val = dict(curve=curve, evals=evals, params=int(sum(p.numel() for p in m.parameters()
                                                                    if p.requires_grad)) -
                            (sum(p.numel() for p in m.proj.parameters()) if cfg == "repa" else 0),
                            macs=macs(m), final=final.tolist(), secs=time.time() - t0)
            if cfg == "zero" and seed == 0:
                path = []
                alphabet = sample(m, list(range(26)) * 2, n_steps=40, seed=1, path=path, every=4)
                many_a = sample(m, [0] * 8, n_steps=40, seed=3)
                torch.save(m.state_dict(), CACHE.dir / "dit_zero_s0.pt")
                np.savez_compressed(CACHE.dir / "dit_showcase.npz", snaps=np.array(snaps), snap_at=np.array(snap_at),
                                    snap_read=np.array(snap_read), snap_ink=np.array(snaps).mean((1, 2, 3)),
                                    gates=np.array(gates), alphabet=alphabet, alphabet_path=np.array(path)[:, :26],
                                    many_a=many_a)
            part[key] = part_val
            print(f"    {key}: {part_val['params']:,} weights, {part_val['macs']:,} multiply-adds a picture; "
                  f"{time.time() - t0:.0f}s", flush=True)
    out = dict(configs=list(CONFIGS), seeds=list(SEEDS), steps=n, batch=BATCH, D=D, L=L, eval_at=eval_at, guide=GUIDE,
               repa_layer=REPA_LAYER, repa_w=REPA_W)
    for cfg in CONFIGS:
        ps = [part[f"{cfg}_s{s}"] for s in SEEDS]
        out[f"{cfg}_params"], out[f"{cfg}_macs"] = ps[0]["params"], ps[0]["macs"]
        out[f"{cfg}_acc"] = np.array([[e["acc"] for e in p_["evals"]] for p_ in ps])
        out[f"{cfg}_fd"] = np.array([[e["fd"] for e in p_["evals"]] for p_ in ps])
        out[f"{cfg}_curve"] = np.array([np.array(p_["curve"]) for p_ in ps])  # (seeds, points, [step, loss, align])
        out[f"{cfg}_final"] = np.array(ps[0]["final"])
        out[f"{cfg}_secs"] = float(np.mean([p_["secs"] for p_ in ps]))
    with np.load(CACHE.dir / "dit_showcase.npz") as z:
        out.update({k: z[k] for k in z.files})
    print("    final right-letter rates: " + ", ".join(f"{c} {out[f'{c}_acc'][:, -1].mean():.3f}" for c in CONFIGS),
          flush=True)
    return out


# ---------------------------------------------------------------------------
SHOW_STEPS = 8000
SHOW_SNAP_FRACS = (0.0, 0.0125, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0)  # steps 0, 100, 250, 500, ... 8,000
SHOW_EVAL_FRACS = (0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0)


def compute_showcase():
    """The showcase: adaLN-Zero, seed 0, the same recipe and data order as the comparisons but trained four times as
    long, checkpointed every 500 steps so an interrupted run resumes. Recorded: samples of A to J from fixed noise at
    checkpoints and the judge's reading of them, the gates opening, the 260-letter score at checkpoints, the alphabet
    twice with its denoising path, and eight A's."""
    import torch

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test] * 2 - 1, dtype=torch.float32)
    Y = torch.tensor(labels[~test])
    n = steps(SHOW_STEPS)
    snap_at = sorted({int(round(f * n)) for f in SHOW_SNAP_FRACS})
    eval_at = sorted({max(1, int(round(f * n))) for f in SHOW_EVAL_FRACS})
    want = np.repeat(np.arange(26), 10)
    z_snap = torch.randn(10, GL, GL, generator=torch.Generator().manual_seed(11))
    show = np.arange(10)  # A to J
    cg = torch.Generator().manual_seed(5)
    c_t, c_y = torch.rand(64, generator=cg), torch.randint(0, 26, (64,), generator=cg)
    state = dict(snaps=[], snap_read=[], gates=[], evals=[])

    def on_step(st, m):
        if st % 25 == 0:
            with torch.no_grad():
                state["gates"].append([st] + sum(m.gates(m.cond(c_t, c_y)), []))
        if st in snap_at:
            m.eval()
            state["snaps"].append(sample(m, show, z=z_snap).tolist())
            state["snap_read"].append(score(np.array(state["snaps"][-1]), show)["acc"])
            m.train()
        if st in eval_at:
            m.eval()
            q = score(sample(m, want, seed=7), want)
            m.train()
            state["evals"].append(dict(step=st, acc=q["acc"], fd=q["fd"]))
            print(f"      showcase step {st}: right letter {q['acc']:.3f}, FD {q['fd']:.1f}", flush=True)

    ck = CACHE.dir / "showcase.ckpt"
    m, curve = train("zero", 0, X, Y, n, on_step=on_step, ckpt=ck, state=state)
    path = []
    alphabet = sample(m, list(range(26)) * 2, n_steps=40, seed=1, path=path, every=4)
    many_a = sample(m, [0] * 8, n_steps=40, seed=3)
    torch.save(m.state_dict(), CACHE.dir / "dit_showcase.pt")
    ck.unlink(missing_ok=True)
    snaps = np.array(state["snaps"])
    return dict(steps=n, params=int(sum(p.numel() for p in m.parameters() if p.requires_grad)), guide=GUIDE,
                batch=BATCH, snap_at=snap_at, snaps=snaps, snap_read=state["snap_read"], snap_ink=snaps.mean((1, 2, 3)),
                gates=np.array(state["gates"]), eval_at=[e["step"] for e in state["evals"]],
                acc=[e["acc"] for e in state["evals"]], fd=[e["fd"] for e in state["evals"]], curve=np.array(curve),
                alphabet=alphabet, alphabet_path=np.array(path)[:, :26], many_a=many_a)


# ---------------------------------------------------------------------------
GUIDES = (0.0, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0)


def compute_guidance():
    """Classifier-free guidance on the showcase transformer (adaLN-Zero, seed 0, 8,000 steps): for each weight w, 260
    letters (ten of each) from the same noise; the share read as requested, the Frechet distance, and the variety (the
    average distance between two drawings of the same letter, root mean square over pixels)."""
    import torch

    threads()
    if not (CACHE.dir / "dit_showcase.pt").exists():
        CACHE.load("showcase")
    m = make("zero")
    m.load_state_dict(torch.load(CACHE.dir / "dit_showcase.pt"))
    m.eval()
    want = np.repeat(np.arange(26), 10)
    out = dict(guides=list(GUIDES))
    acc, fd, var, shows = [], [], [], []
    for w in GUIDES:
        x = sample(m, want, w=w, seed=7)
        q = score(x, want)
        g = x.reshape(26, 10, -1)
        d = np.sqrt(((g[:, :, None] - g[:, None]) ** 2).mean(-1))  # (26, 10, 10)
        var.append(float(d.sum() / (26 * 10 * 9)))
        acc.append(q["acc"])
        fd.append(q["fd"])
        shows.append(x[want == 17][:6])  # six R's
        print(f"    w = {w:g}: right letter {q['acc']:.3f}, FD {q['fd']:.1f}, variety {var[-1]:.3f}", flush=True)
    out.update(acc=acc, fd=fd, variety=var, shows=np.array(shows))
    return out
