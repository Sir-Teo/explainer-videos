"""Part 21's toy denoiser, watched while it learns (the ``toytrain`` item).

    toytrain   the toy item's training run again (same seed, same 8,000 steps), stopping at checkpoints to draw 600
               points from the same noise with 50 deterministic (DDIM) steps; the loss along the way
"""

from __future__ import annotations

import math

import numpy as np

CHECKS = [0, 50, 150, 400, 1000, 2500, 8000]


def compute_toytrain():
    import torch

    from videos.ai.ai21.compute import ai_points, mlp, rng, sw_distance, vp

    torch.set_num_threads(2)
    torch.manual_seed(2020)  # as in the toy item
    data = ai_points()
    X = torch.tensor(data, dtype=torch.float32)
    net = mlp(2, 2)
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, CHECKS[-1])
    g = torch.Generator().manual_seed(0)
    z = rng(1).normal(size=(600, 2))

    def draw():
        x = z.copy()
        ts = np.linspace(1, 0, 51)
        with torch.no_grad():
            for i in range(50):
                (a, s), (an, sn) = vp(ts[i]), vp(ts[i + 1])
                e = net(torch.tensor(x, dtype=torch.float32), torch.full((len(x),), float(ts[i]))).numpy().astype(float)
                x0 = np.clip((x - s * e) / max(a, 1e-3), -4, 4)
                x = an * x0 + sn * e
        return x

    snaps, losses, run = [draw()], [], []
    for step in range(1, CHECKS[-1] + 1):
        x0 = X[torch.randint(0, len(X), (512,), generator=g)]
        t = torch.rand(512, generator=g) * 0.999 + 0.001
        eps = torch.randn(512, 2, generator=g)
        a, s = torch.cos(math.pi * t / 2)[:, None], torch.sin(math.pi * t / 2)[:, None]
        loss = ((net(a * x0 + s * eps, t) - eps) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if step % 25 == 0:
            losses.append((step, float(np.mean(run))))
            run = []
        if step in CHECKS:
            snaps.append(draw())
    snaps = np.array(snaps)
    sw = [sw_distance(x, data) for x in snaps]
    print("    distance from the data at each checkpoint: " + " ".join(f"{v:.3f}" for v in sw), flush=True)
    assert sw[-1] < sw[0]
    return dict(checks=CHECKS, snaps=snaps, losses=np.array(losses), sw=sw)
