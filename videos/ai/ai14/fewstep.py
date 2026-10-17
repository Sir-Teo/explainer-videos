"""One-step generation on Part 4's "AI" points (the ``fewstep`` item of Part 14).

Both models learn the average velocity between two times, u(z_s, s, t), so that one jump z_t = z_s + (t - s) u lands
where many small flow-matching steps would. Time runs as in the rest of Part 14: s = 0 is noise, 1 is data.

    meanflow   (Geng et al., 2025) the identity u = v + (t - s) du/ds along the path, its derivative taken by one
               forward-mode pass (a Jacobian-vector product); half the pairs have s = t, which is plain flow matching
    shortcut   (Frans et al., 2024) self-consistency: one jump of size 2d must equal two jumps of size d, for d a
               power of two; jumps of size 0 are plain flow matching

Recorded: samples after 1, 2 and 4 jumps, their sliced Wasserstein distance from the data, and one-jump paths.
"""

from __future__ import annotations

import math

import numpy as np

STEPS = 8000
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


def train(kind, X, seed=2025):
    import torch

    torch.manual_seed(seed)
    net = uvnet()
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, STEPS)
    g = torch.Generator().manual_seed(seed)
    B = 512
    for step in range(STEPS):
        x1 = X[torch.randint(0, len(X), (B,), generator=g)]
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
            loss = ((u - target) ** 2).mean()
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

    from videos.ai.ai14.compute import ai_points, rng, sw_distance

    torch.set_num_threads(2)
    data = ai_points()
    X = torch.tensor(data, dtype=torch.float32)
    z = rng(1).normal(size=(1500, 2))  # the same noise as the flow item
    out = dict(jumps=JUMPS, steps=STEPS)
    for kind in ("meanflow", "shortcut"):
        net = train(kind, X)
        for n in JUMPS:
            xs, p = jump(net, z, n)
            out[f"{kind}{n}"] = xs[:600]
            out[f"sw_{kind}{n}"] = sw_distance(xs, data)
            if n == 1:
                out[f"{kind}_path"] = p[:, :300]
        print(f"    {kind}: " + ", ".join(f"{n} jumps {out[f'sw_{kind}{n}']:.3f}" for n in JUMPS), flush=True)
    out["sw_noise"] = sw_distance(z, data)
    assert out["sw_meanflow1"] < 0.5 * out["sw_noise"]
    return out
