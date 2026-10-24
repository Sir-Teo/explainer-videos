"""Part 22, chapters 15-16: 3D from pictures. One synthetic scene: a gold letter A, extruded, and a blue ball, as a
density and a colour on a 64^3 grid, photographed from 24 cameras on a circle; 8 cameras in between are held out.

    nerf    the volume-rendering integral checked on a uniform ball (exact answer known): the Riemann sum against
            NeRF's alpha-compositing sum, by the number of samples; then a small NeRF (positional encoding, an MLP of
            four layers of 64) trained on the 24 photographs, replayed on a held-out view, three seeds
    splat   3D Gaussian splatting: the projected covariance J W Sigma W^T J^T against Monte Carlo through the exact
            perspective projection, for Gaussians from small to large against their depth; then 500 Gaussians fitted
            to the same 24 photographs by differentiable rasterization (depth-sorted alpha compositing), three seeds
"""

from __future__ import annotations

import math
import time

import numpy as np

from videos.ai.ai22.base import CACHE, font_files, render, steps, threads

RES, N_TRAIN, N_TEST = 32, 24, 8
NEAR, FAR = 1.4, 4.0
RADIUS, ELEV = 2.7, 0.42  # the cameras' circle, and their height angle (radians)
FOCAL = RES / (2 * math.tan(math.radians(20)))  # a 40-degree field of view
SEEDS = (0, 1, 2)
GRID = 64
BOX = 0.9  # the scene lives in [-BOX, BOX]^3


def scene_grid():
    """Density (64^3) and colour (64^3 x 3) of the scene: an extruded letter A (gold) and a ball (blue)."""
    from scipy.ndimage import gaussian_filter

    bold = next(f for f in font_files() if f.endswith("DejaVuSans-Bold.ttf"))
    a = render(bold, "A", GRID)  # the letter, 64 x 64
    a = gaussian_filter(a, 0.6)
    xs = np.linspace(-BOX, BOX, GRID)
    X, Yy, Z = np.meshgrid(xs, xs, xs, indexing="ij")  # x right, y up, z towards the first camera
    # the letter stands in the x-y plane (rows of the picture run down in y), 0.3 thick in z
    letter = np.zeros_like(X)
    yi = (GRID - 1) - np.round((Yy + BOX) / (2 * BOX) * (GRID - 1)).astype(int)
    xi = np.round((X + BOX) / (2 * BOX) * (GRID - 1)).astype(int)
    letter = a[yi, xi] * (np.abs(Z + 0.15) < 0.16)
    ball = np.clip((0.26 - np.sqrt((X - 0.42) ** 2 + (Yy + 0.38) ** 2 + (Z - 0.38) ** 2)) / 0.03, 0, 1)
    sig = 22.0 * np.clip(letter, 0, 1) + 22.0 * ball
    gold, blue = np.array([1.0, 0.78, 0.25]), np.array([0.3, 0.55, 1.0])
    # a little shading by height, so the pictures carry more than a silhouette
    shade = 0.75 + 0.25 * (Yy + BOX) / (2 * BOX)
    w = letter + ball + 1e-9
    col = ((letter / w)[..., None] * gold + (ball / w)[..., None] * blue) * shade[..., None]
    return sig.astype(np.float32), col.astype(np.float32)


def cameras(n, offset=0.0):
    """Cameras on a circle around the scene, looking at its centre: (R world->camera, centre) each."""
    out = []
    for k in range(n):
        th = 2 * math.pi * (k + offset) / n
        c = RADIUS * np.array([math.sin(th) * math.cos(ELEV), math.sin(ELEV), math.cos(th) * math.cos(ELEV)])
        fwd = -c / np.linalg.norm(c)
        right = np.cross(fwd, [0, 1, 0])
        right /= np.linalg.norm(right)
        upv = np.cross(right, fwd)
        R = np.stack([right, -upv, fwd])  # camera axes: x right, y down, z forward
        out.append((R, c))
    return out


def rays(cam):
    R, c = cam
    j, i = np.meshgrid(np.arange(RES) + 0.5, np.arange(RES) + 0.5)
    d_cam = np.stack([(j - RES / 2) / FOCAL, (i - RES / 2) / FOCAL, np.ones_like(i)], -1).reshape(-1, 3)
    d = d_cam @ R  # back to world
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    return np.repeat(c[None], len(d), 0), d


def grid_field(sig, col):
    """The scene as a function of points (trilinear on the grid)."""
    import torch
    import torch.nn.functional as F

    S = torch.tensor(sig)[None, None]
    Cc = torch.tensor(col).permute(3, 0, 1, 2)[None]

    def f(p):  # p (N, 3) world points -> density (N,), colour (N, 3)
        q = (p / BOX).clamp(-1.5, 1.5)
        g = q[:, [2, 1, 0]].reshape(1, -1, 1, 1, 3)  # grid_sample wants (z, y, x) order for an (x, y, z) volume
        s = F.grid_sample(S, g, align_corners=True, padding_mode="zeros").reshape(-1)
        c = F.grid_sample(Cc, g, align_corners=True, padding_mode="zeros").reshape(3, -1).T
        return s, c

    return f


def composite(sigma, color, t):
    """NeRF's sum: C = sum_i T_i (1 - exp(-sigma_i delta_i)) c_i, T_i = exp(-sum_{j<i} sigma_j delta_j).
    sigma (R, N), color (R, N, 3), t (R, N) sample depths. Returns colour (R, 3), weights (R, N)."""
    import torch

    delta = torch.cat([t[:, 1:] - t[:, :-1], torch.full_like(t[:, :1], 1e10)], 1)
    alpha = 1 - torch.exp(-sigma * delta)
    T = torch.cumprod(torch.cat([torch.ones_like(alpha[:, :1]), 1 - alpha + 1e-10], 1), 1)[:, :-1]
    w = T * alpha
    return (w[..., None] * color).sum(1), w


def render_field(f, cam, n_samples=192, stratified=None):
    import torch

    o, d = rays(cam)
    o, d = torch.tensor(o, dtype=torch.float32), torch.tensor(d, dtype=torch.float32)
    t = torch.linspace(NEAR, FAR, n_samples)[None].expand(len(o), -1)
    p = o[:, None] + d[:, None] * t[..., None]
    s, c = f(p.reshape(-1, 3))
    rgb, w = composite(s.reshape(len(o), -1), c.reshape(len(o), -1, 3), t)
    depth = (w * t).sum(1)
    return rgb.reshape(RES, RES, 3), depth.reshape(RES, RES), w.sum(1).reshape(RES, RES)


def photographs():
    import torch

    sig, col = scene_grid()
    f = grid_field(sig, col)
    tr, te = cameras(N_TRAIN), cameras(N_TEST, offset=0.5)
    with torch.no_grad():
        I_tr = np.array([render_field(f, c, 384)[0].numpy() for c in tr])
        I_te = np.array([render_field(f, c, 384)[0].numpy() for c in te])
    return tr, te, I_tr, I_te


def psnr(a, b):
    return float(-10 * np.log10(max(np.mean((np.asarray(a) - np.asarray(b)) ** 2), 1e-12)))


# ---------------------------------------------------------------------------
def quadrature_check():
    """A ball of radius 1 and uniform density sigma, colour 1, a ray through its centre: C = 1 - exp(-2 sigma).
    The Riemann sum and NeRF's sum, with N samples evenly spread over [0, 4] (the ball from 1 to 3)."""
    out = {}
    Ns = [4, 8, 16, 32, 64, 128, 256]
    for s0 in (0.5, 2.0, 8.0):
        exact = 1 - math.exp(-2 * s0)
        rie, ner = [], []
        for N in Ns:
            t = (np.arange(N) + 0.5) * 4.0 / N
            dl = 4.0 / N
            sg = np.where(np.abs(t - 2) < 1, s0, 0.0)
            T_r = np.exp(-np.concatenate([[0], np.cumsum(sg * dl)[:-1]]))
            rie.append(float(np.sum(T_r * sg * dl) - exact))
            a = 1 - np.exp(-sg * dl)
            T_n = np.concatenate([[1], np.cumprod(1 - a)[:-1]])
            ner.append(float(np.sum(T_n * a) - exact))
        out[f"s{s0:g}"] = dict(exact=exact, riemann=rie, nerf=ner)
    return dict(Ns=Ns, **out)


def nerf_net():
    import torch
    import torch.nn as nn

    class NeRF(nn.Module):
        """Positional encoding with 6 frequencies (Mildenhall et al. 2020), then an MLP: density and colour."""

        def __init__(self, n_freq=6, W=64):
            super().__init__()
            self.register_buffer("freqs", 2.0 ** torch.arange(n_freq) * math.pi)
            din = 3 + 6 * n_freq
            self.mlp = nn.Sequential(nn.Linear(din, W), nn.ReLU(), nn.Linear(W, W), nn.ReLU(), nn.Linear(W, W),
                                     nn.ReLU(), nn.Linear(W, W), nn.ReLU(), nn.Linear(W, 4))

        def forward(self, p):
            q = p / BOX
            a = q[..., None] * self.freqs  # (N, 3, F)
            h = torch.cat([q, torch.sin(a).flatten(1), torch.cos(a).flatten(1)], 1)
            o = self.mlp(h)
            return torch.nn.functional.softplus(o[:, 0] - 1.0) * 10, torch.sigmoid(o[:, 1:])

    return NeRF()


def compute_nerf():
    import torch

    threads()
    tr, te, I_tr, I_te = photographs()
    O, Dd = zip(*[rays(c) for c in tr])
    O = torch.tensor(np.concatenate(O), dtype=torch.float32)
    Dd = torch.tensor(np.concatenate(Dd), dtype=torch.float32)
    C = torch.tensor(I_tr.reshape(-1, 3), dtype=torch.float32)
    n = steps(2000)
    checks = sorted({0, n // 40, n // 10, n // 4, n})
    NS, NR = 48, 512
    part = CACHE.partial("nerf", dict(steps=n, seeds=SEEDS, NS=NS, NR=NR, res=RES))
    for seed in SEEDS:
        key = f"s{seed}"
        if key in part:
            continue
        torch.manual_seed(2020 + seed)  # Mildenhall et al., NeRF (2020)
        m = nerf_net()
        opt = torch.optim.Adam(m.parameters(), lr=5e-3)
        sched = torch.optim.lr_scheduler.ExponentialLR(opt, 0.1 ** (1 / n))
        g = torch.Generator().manual_seed(seed)
        replay, curve, run = [], [], []
        t0 = time.time()
        for st in range(n + 1):
            if st in checks:
                with torch.no_grad():
                    imgs = [render_field(m, c, NS)[0].numpy() for c in te]
                replay.append(dict(step=st, psnr=float(np.mean([psnr(a, b) for a, b in zip(imgs, I_te)])),
                                   view=imgs[1].tolist()))
            if st == n:
                break
            i = torch.randint(0, len(O), (NR,), generator=g)
            # stratified samples: one at random in each of NS equal bins between the near and far planes
            edges = torch.linspace(NEAR, FAR, NS + 1)
            t = edges[:-1] + (edges[1:] - edges[:-1]) * torch.rand(NR, NS, generator=g)
            p = O[i, None] + Dd[i, None] * t[..., None]
            s, c = m(p.reshape(-1, 3))
            rgb, _ = composite(s.reshape(NR, NS), c.reshape(NR, NS, 3), t)
            loss = ((rgb - C[i]) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            run.append(float(loss))
            if (st + 1) % 50 == 0:
                curve.append((st + 1, psnr_of_mse(np.mean(run))))
                run = []
        secs = time.time() - t0
        with torch.no_grad():
            tt = time.time()
            for _ in range(3):
                rgb, depth, acc = render_field(m, te[1], NS)
            ms = (time.time() - tt) / 3 * 1000
        part[key] = dict(replay=replay, curve=curve, secs=secs, render_ms=ms, depth=depth.numpy().tolist(),
                         acc=acc.numpy().tolist(), test_psnr=replay[-1]["psnr"],
                         params=int(sum(p_.numel() for p_ in m.parameters())))
        print(f"    nerf s{seed}: held-out PSNR {replay[-1]['psnr']:.1f} dB after {n} steps ({secs:.0f}s); "
              f"a view in {ms:.0f} ms", flush=True)
    p0 = part["s0"]
    out = dict(res=RES, n_train=N_TRAIN, n_test=N_TEST, steps=n, checks=checks, NS=NS, NR=NR, quad=quadrature_check(),
               train_imgs=I_tr, test_imgs=I_te, replay_psnr=[r["psnr"] for r in p0["replay"]],
               replay_views=np.array([r["view"] for r in p0["replay"]]), depth=np.array(p0["depth"]),
               acc=np.array(p0["acc"]), params=p0["params"], cams=np.array([c for _, c in tr]),
               test_psnr=[part[f"s{s}"]["test_psnr"] for s in SEEDS], secs=[part[f"s{s}"]["secs"] for s in SEEDS],
               render_ms=[part[f"s{s}"]["render_ms"] for s in SEEDS],
               curve=np.array([np.array(part[f"s{s}"]["curve"]) for s in SEEDS]))
    return out


def psnr_of_mse(m):
    return float(-10 * np.log10(max(m, 1e-12)))


# ---------------------------------------------------------------------------
def rot(q):
    """Quaternions (N, 4) -> rotation matrices (N, 3, 3)."""
    import torch

    q = q / q.norm(dim=1, keepdim=True)
    w, x, y, z = q.unbind(1)
    return torch.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y),
                        2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x),
                        2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], 1).reshape(-1, 3, 3)


def project(mu, cov, cam):
    """EWA splatting (Zwicker et al. 2001), as 3D Gaussian splatting uses it: means and covariances to the image.
    Sigma' = J W Sigma W^T J^T, W the camera's rotation, J the Jacobian of the perspective projection at the mean."""
    import torch

    R, c = cam
    W = torch.tensor(R, dtype=torch.float32)
    pc = (mu - torch.tensor(c, dtype=torch.float32)) @ W.T  # camera coordinates
    x, y, z = pc.unbind(1)
    zc = z.clamp(min=0.05)
    u = FOCAL * x / zc + RES / 2
    v = FOCAL * y / zc + RES / 2
    J = torch.zeros(len(mu), 2, 3)
    J[:, 0, 0] = FOCAL / zc
    J[:, 0, 2] = -FOCAL * x / zc ** 2
    J[:, 1, 1] = FOCAL / zc
    J[:, 1, 2] = -FOCAL * y / zc ** 2
    cov2 = J @ W @ cov @ W.T @ J.transpose(1, 2)
    return torch.stack([u, v], 1), cov2, z


def splat_render(mu, cov, col, opa, cam):
    """Every Gaussian at every pixel, sorted front to back: C = sum_i c_i a_i prod_{j<i} (1 - a_j)."""
    import torch

    uv, cov2, z = project(mu, cov, cam)
    cov2 = cov2 + 0.3 * torch.eye(2)  # a low-pass filter of 0.3 pixels^2, as in the paper
    keep = z > 0.2
    order = torch.argsort(torch.where(keep, z, torch.full_like(z, 1e9)))
    uv, cov2, col, opa, keep = uv[order], cov2[order], col[order], opa[order], keep[order]
    a, b, d = cov2[:, 0, 0], cov2[:, 0, 1], cov2[:, 1, 1]
    det = a * d - b * b
    ia, ib, id_ = d / det, -b / det, a / det
    j, i = torch.meshgrid(torch.arange(RES) + 0.5, torch.arange(RES) + 0.5, indexing="xy")
    px = torch.stack([j.reshape(-1), i.reshape(-1)], 1)  # (P, 2)
    dx = px[:, None, 0] - uv[None, :, 0]
    dy = px[:, None, 1] - uv[None, :, 1]
    power = -0.5 * (ia * dx * dx + 2 * ib * dx * dy + id_ * dy * dy)
    alpha = (opa[None] * torch.exp(power.clamp(max=0))).clamp(max=0.99) * keep[None]
    T = torch.cumprod(torch.cat([torch.ones_like(alpha[:, :1]), 1 - alpha], 1), 1)[:, :-1]
    rgb = ((T * alpha)[..., None] * col[None]).sum(1)
    return rgb.reshape(RES, RES, 3)


def projection_check(n=200_000):
    """Sample a 3D Gaussian, project every sample exactly (u = f x / z), and compare the samples' covariance with
    J W Sigma W^T J^T, for Gaussians of growing size at depth 2.5 (and off the axis)."""
    import torch

    g = np.random.default_rng(2023)  # Kerbl et al., 3D Gaussian Splatting (2023)
    rel = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3]
    cam = cameras(1)[0]
    R, c = cam
    errs = []
    show = None
    for r_ in rel:
        e_ = []
        for k in range(4):
            q = torch.tensor(g.normal(size=(1, 4)), dtype=torch.float32)
            s = torch.tensor(np.array([1.0, 0.6, 0.3]) * r_ * 2.5, dtype=torch.float32)
            Rq = rot(q)[0]
            cov = Rq @ torch.diag(s ** 2) @ Rq.T
            mu = torch.tensor(c + 2.5 * R[2] + 0.4 * R[0] - 0.25 * R[1], dtype=torch.float32)  # depth 2.5, off-axis
            uv, cov2, _ = project(mu[None], cov[None], cam)
            X = np.random.default_rng(7 + k).multivariate_normal(mu.numpy(), cov.numpy(), n)
            pc = (X - c) @ R.T
            UV = np.stack([FOCAL * pc[:, 0] / pc[:, 2] + RES / 2, FOCAL * pc[:, 1] / pc[:, 2] + RES / 2], 1)
            emp = np.cov(UV, rowvar=False)
            e_.append(float(np.linalg.norm(emp - cov2[0].numpy()) / np.linalg.norm(emp)))
            if k == 0 and r_ == 0.1:
                show = dict(samples=UV[:3000], mean=uv[0].numpy(), cov=cov2[0].numpy(), emp_mean=UV.mean(0), emp=emp)
        errs.append(float(np.median(e_)))
    return dict(rel=rel, errs=errs, show=show)


def compute_splat():
    import torch

    threads()
    tr, te, I_tr, I_te = photographs()
    n = steps(2000)
    checks = sorted({0, n // 40, n // 10, n // 4, n})
    N = 500
    part = CACHE.partial("splat", dict(steps=n, seeds=SEEDS, N=N, res=RES))
    It = torch.tensor(I_tr, dtype=torch.float32)
    for seed in SEEDS:
        key = f"s{seed}"
        if key in part:
            continue
        torch.manual_seed(2023 + seed)
        g = torch.Generator().manual_seed(seed)
        mu = ((torch.rand(N, 3, generator=g) * 2 - 1) * 0.7).requires_grad_()
        logs = torch.full((N, 3), math.log(0.05)).requires_grad_()
        quat = torch.cat([torch.ones(N, 1), torch.zeros(N, 3)], 1).requires_grad_()
        colr = torch.zeros(N, 3).requires_grad_()
        opal = torch.full((N,), -2.0).requires_grad_()
        opt = torch.optim.Adam([dict(params=[mu], lr=0.01), dict(params=[logs], lr=0.01), dict(params=[quat], lr=0.01),
                                dict(params=[colr], lr=0.03), dict(params=[opal], lr=0.05)])
        sched = torch.optim.lr_scheduler.ExponentialLR(opt, 0.1 ** (1 / n))

        def params():
            Rq = rot(quat)
            S = torch.exp(logs).clamp(max=0.4)
            return mu, Rq @ torch.diag_embed(S ** 2) @ Rq.transpose(1, 2), torch.sigmoid(colr), torch.sigmoid(opal)

        replay, curve, run = [], [], []
        t0 = time.time()
        for st in range(n + 1):
            if st in checks:
                with torch.no_grad():
                    imgs = [splat_render(*params(), c).numpy() for c in te]
                replay.append(dict(step=st, psnr=float(np.mean([psnr(a, b) for a, b in zip(imgs, I_te)])),
                                   view=imgs[1].tolist()))
            if st == n:
                break
            loss = 0
            for v in torch.randint(0, N_TRAIN, (1,), generator=g).tolist():
                loss = loss + ((splat_render(*params(), tr[v]) - It[v]) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            run.append(float(loss))
            if (st + 1) % 50 == 0:
                curve.append((st + 1, psnr_of_mse(np.mean(run))))
                run = []
            if (st + 1) % 300 == 0 and st + 1 < 0.75 * n:  # move faded Gaussians next to busy ones
                with torch.no_grad():
                    o = torch.sigmoid(opal)
                    dead = torch.where(o < 0.02)[0]
                    live = torch.where(o >= 0.02)[0]
                    if len(dead) and len(live):
                        src = live[torch.randint(0, len(live), (len(dead),), generator=g)]
                        mu[dead] = mu[src] + 0.02 * torch.randn(len(dead), 3, generator=g)
                        logs[dead] = logs[src]
                        quat[dead] = quat[src]
                        colr[dead] = colr[src]
                        opal[dead] = -2.0
        secs = time.time() - t0
        with torch.no_grad():
            tt = time.time()
            for _ in range(3):
                splat_render(*params(), te[1])
            ms = (time.time() - tt) / 3 * 1000
            m_, cv, cl, op = (x_.detach() for x_ in params())
            uv, cov2, z = project(m_, cv, te[1])
            top = torch.argsort(op, descending=True)[:150]
        part[key] = dict(replay=replay, curve=curve, secs=secs, render_ms=ms, test_psnr=replay[-1]["psnr"],
                         live=int((op > 0.02).sum()),
                         ell_uv=uv[top].numpy().tolist(), ell_cov=cov2[top].numpy().tolist(), ell_col=cl[top].numpy().tolist(),
                         ell_op=op[top].numpy().tolist(), ell_z=z[top].numpy().tolist(),
                         centres=m_.numpy().tolist(), colours=cl.numpy().tolist(), opac=op.numpy().tolist())
        print(f"    splat s{seed}: held-out PSNR {replay[-1]['psnr']:.1f} dB after {n} steps ({secs:.0f}s); "
              f"a view in {ms:.0f} ms; {part[key]['live']} Gaussians in use", flush=True)
    p0 = part["s0"]
    pc = projection_check()
    out = dict(res=RES, steps=n, checks=checks, N=N, proj_rel=pc["rel"], proj_errs=pc["errs"],
               proj_samples=pc["show"]["samples"], proj_mean=pc["show"]["mean"], proj_cov=pc["show"]["cov"],
               proj_emp_mean=pc["show"]["emp_mean"], proj_emp=pc["show"]["emp"],
               replay_psnr=[r["psnr"] for r in p0["replay"]], replay_views=np.array([r["view"] for r in p0["replay"]]),
               test_psnr=[part[f"s{s}"]["test_psnr"] for s in SEEDS], secs=[part[f"s{s}"]["secs"] for s in SEEDS],
               render_ms=[part[f"s{s}"]["render_ms"] for s in SEEDS], live=[part[f"s{s}"]["live"] for s in SEEDS],
               curve=np.array([np.array(part[f"s{s}"]["curve"]) for s in SEEDS]), test_view=I_te[1])
    for f_ in ("ell_uv", "ell_cov", "ell_col", "ell_op", "ell_z", "centres", "colours", "opac"):
        out[f_] = np.array(p0[f_])
    return out
