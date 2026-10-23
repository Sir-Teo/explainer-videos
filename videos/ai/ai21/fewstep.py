"""One-step generation on the "AI" mixture (the ``fewstep`` item of Part 21).

Both models learn the average velocity between two times, u(z_s, s, t), so that one jump z_t = z_s + (t - s) u lands
where many small flow-matching steps would. Time runs as in the rest of Part 21: s = 0 is noise, 1 is data.

    meanflow   (Geng et al., 2025) the identity u = v + (t - s) du/ds along the path, its derivative taken by one
               forward-mode pass (a Jacobian-vector product); half the pairs have s = t, which is plain flow matching;
               the paper's adaptive loss weighting (each squared error divided by itself, held fixed, plus 0.001)
    shortcut   (Frans et al., 2024) self-consistency: one jump of size 2d must equal two jumps of size d, for d a
               power of two; jumps of size 0 are plain flow matching

Recorded, for three seeds at the same budget as every other model of the part: samples after 1, 2 and 4 jumps, their
sliced Wasserstein distance from the data, one-jump paths, and (seed 0) one jump from the same noise during training.
"""

from __future__ import annotations

import math

import numpy as np

from videos.ai.ai21.train2d import BATCH, SEEDS, STEPS, mixture_torch

JUMPS = [1, 2, 4]


def uvnet(width=256, tdim=32):
    """u(z, s, t): the average velocity from time s to time t, starting at z."""
    import torch
    import torch.nn as nn

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.freq = nn.Parameter(torch.randn(tdim // 2) * 4.0, requires_grad=False)
            self.net = nn.Sequential(nn.Linear(2 + 2 * tdim, width), nn.SiLU(), nn.Linear(width, width), nn.SiLU(),
                                     nn.Linear(width, width), nn.SiLU(), nn.Linear(width, 2))

        def emb(self, t):
            a = t[:, None] * self.freq[None] * 2 * math.pi
            return [torch.sin(a), torch.cos(a)]

        def forward(self, z, s, t):
            return self.net(torch.cat([z, *self.emb(s), *self.emb(t - s)], 1))

    return Net()


def train(kind, seed=2025, z_watch=None, snaps=None):
    import torch

    torch.manual_seed(seed)
    net = uvnet()
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, STEPS)
    g = torch.Generator().manual_seed(seed)
    draw = mixture_torch(g)
    B = BATCH
    marks = sorted({max(1, STEPS * k // 24) for k in (1, 2, 4, 8, 16, 24)})
    for step in range(STEPS):
        x1 = draw(B)
        x0 = torch.randn(B, 2, generator=g)
        v = x1 - x0
        if kind == "meanflow":
            a, b = torch.rand(B, generator=g), torch.rand(B, generator=g)
            same = torch.rand(B, generator=g) < 0.5
            s = torch.where(same, a, torch.minimum(a, b))
            t = torch.where(same, a, torch.maximum(a, b))
            z = (1 - s[:, None]) * x0 + s[:, None] * x1
            # u and its derivative along the path, d/ds u(z_s, s, t) = v . grad_z u + du/ds, in one forward-mode pass
            u, du = torch.func.jvp(net, (z, s, t), (v, torch.ones_like(s), torch.zeros_like(t)))
            target = (v + (t - s)[:, None] * du).detach()
            err = ((u - target) ** 2).sum(1)
            loss = (err / (err.detach() + 1e-3)).mean()  # MeanFlow's adaptive weighting (power 1): no sample dominates
        else:
            # half plain flow matching (jumps of size 0), half self-consistency: one jump of 2d = two jumps of d
            n = B // 2
            s0 = torch.rand(n, generator=g)
            z0 = (1 - s0[:, None]) * x0[:n] + s0[:, None] * x1[:n]
            fm = ((net(z0, s0, s0) - v[:n]) ** 2).mean()
            k = torch.randint(0, 7, (n,), generator=g)
            d = 2.0 ** (-k.float())  # 2d is the jump trained, 1 down to 1/64
            s1 = torch.floor(torch.rand(n, generator=g) * (1 / d)) * d  # start on the grid of that size
            s1 = torch.minimum(s1, 1 - d)
            h = d / 2
            z1 = (1 - s1[:, None]) * x0[n:] + s1[:, None] * x1[n:]
            with torch.no_grad():
                u1 = net(z1, s1, s1 + h)
                zm = z1 + h[:, None] * u1
                u2 = net(zm, s1 + h, s1 + d)
                target = (u1 + u2) / 2
            sc = ((net(z1, s1, s1 + d) - target) ** 2).mean()
            loss = fm + sc
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if snaps is not None and (step + 1) in marks:  # how it learns: one jump, as training goes
            snaps.append((step + 1, jump(net, z_watch, 1)[0]))
        if (step + 1) % 2000 == 0:
            print(f"    {kind} step {step + 1}: loss {float(loss):.4f}", flush=True)
    return net


def jump(net, z, n):
    import torch

    x = torch.tensor(z, dtype=torch.float32)
    path = [x.numpy().copy()]
    with torch.no_grad():
        for i in range(n):
            s = torch.full((len(x),), i / n)
            x = x + net(x, s, s + 1 / n) / n
            path.append(x.numpy().copy())
    return x.numpy().astype(float), np.array(path)


def compute_fewstep():
    import torch

    from videos.ai.ai21 import exact as E
    from videos.ai.ai21.compute import CACHE, sw_distance
    from videos.ai.ai21.train2d import threads

    threads()
    part = CACHE.partial("fewstep", dict(steps=STEPS, seeds=list(SEEDS)))
    data = E.sample(1500, 41)
    z = E.rng(1).normal(size=(1500, 2))  # the same noise as the flow item
    for kind in ("meanflow", "shortcut"):
        for seed in SEEDS:
            key = f"{kind}_s{seed}"
            if key in part:
                continue
            sn = []
            net = train(kind, seed=2025 + seed, z_watch=z[:400] if seed == 0 else None, snaps=sn if seed == 0 else None)
            r = dict(snap_steps=[s_ for s_, _ in sn], snaps=[x_.tolist() for _, x_ in sn])
            for n in JUMPS:
                xs, p = jump(net, z, n)
                r[f"sw{n}"] = sw_distance(xs, data)
                r[f"x{n}"] = xs[:600].tolist()
                if n == 1:
                    r["path"] = p[:, :300].tolist()
            part[key] = r
            print(f"    {key}: " + ", ".join(f"{n} jumps {r[f'sw{n}']:.3f}" for n in JUMPS), flush=True)
    out = dict(jumps=JUMPS, steps=STEPS, seeds=list(SEEDS), sw_noise=sw_distance(z, data))
    for kind in ("meanflow", "shortcut"):
        rs = [part[f"{kind}_s{s}"] for s in SEEDS]
        out[f"{kind}_sw"] = np.array([[r[f"sw{n}"] for n in JUMPS] for r in rs])  # seed, jumps
        for n in JUMPS:
            out[f"sw_{kind}{n}"] = float(np.mean([r[f"sw{n}"] for r in rs]))
            out[f"{kind}{n}"] = np.array(rs[0][f"x{n}"])
        out[f"{kind}_path"] = np.array(rs[0]["path"])
        out[f"{kind}_snap_steps"] = rs[0]["snap_steps"]
        out[f"{kind}_snaps"] = np.array(rs[0]["snaps"])
    return out
