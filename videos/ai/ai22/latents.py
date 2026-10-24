"""Part 22, chapters 3 and 8: latent spaces, the training noise levels, and the resolution shift.

    latents   convolutional autoencoders that squeeze a 20 x 20 letter into a grid of g x g cells with c numbers each
              (16 to 100 numbers): rebuild error against the number of numbers; at equal numbers, a coarse grid with
              many channels against a fine grid with few; then flow matching in each latent space (two seeds)
    tsample   uniform against logit-normal noise levels in training (three seeds each), sampled with 1 to 40 steps
    shift     the resolution shift: the same letters drawn at 20, 40 and 80 pixels; the exact posterior over them says
              how much a noise level destroys at each size, and the shifted levels line the three sizes up
"""

from __future__ import annotations

import math

import numpy as np

from videos.ai.ai22.base import CACHE, GL, LETTERS, dataset, font_files, render, score, steps, threads

# (grid side, channels): the number of numbers is side^2 x channels
CONFIGS = [(10, 1), (5, 4), (5, 2), (5, 1), (2, 16), (2, 4), (1, 64), (1, 16)]


def autoencoder(side: int, ch: int):
    """Encoder: 20 -> 10 -> 5 by strided convolutions, then to a side x side x ch grid; the decoder mirrors it.
    The decoder outputs logits (the pixels are mostly black or white)."""
    import torch.nn as nn

    act = nn.SiLU
    enc = [nn.Conv2d(1, 32, 3, padding=1), act(), nn.Conv2d(32, 64, 4, 2, 1), act()]  # 10 x 10
    dec_tail = [nn.ConvTranspose2d(64, 32, 4, 2, 1), act(), nn.Conv2d(32, 32, 3, padding=1), act(), nn.Conv2d(32, 1, 3, padding=1)]
    if side == 10:
        enc += [nn.Conv2d(64, ch, 1)]
        dec = [nn.Conv2d(ch, 64, 3, padding=1), act()]
    else:
        enc += [nn.Conv2d(64, 64, 4, 2, 1), act()]  # 5 x 5
        dec_mid = [nn.ConvTranspose2d(64, 64, 4, 2, 1), act()]  # 5 -> 10
        if side == 5:
            enc += [nn.Conv2d(64, ch, 1)]
            dec = [nn.Conv2d(ch, 64, 3, padding=1), act()]
        elif side == 2:
            enc += [nn.Conv2d(64, 96, 3, 2, 0), act(), nn.Conv2d(96, ch, 1)]  # 5 -> 2
            dec = [nn.Conv2d(ch, 96, 1), act(), nn.ConvTranspose2d(96, 64, 3, 2, 0), act()]  # 2 -> 5
        else:
            enc += [nn.Conv2d(64, 128, 5), act(), nn.Conv2d(128, ch, 1)]  # 5 -> 1
            dec = [nn.Conv2d(ch, 128, 1), act(), nn.ConvTranspose2d(128, 64, 5), act()]  # 1 -> 5
        dec += dec_mid
    return nn.Sequential(*enc), nn.Sequential(*dec, *dec_tail)


def train_ae(side, ch, X, n_steps, seed):
    import torch
    import torch.nn.functional as F

    torch.manual_seed(seed)
    enc, dec = autoencoder(side, ch)
    params = [*enc.parameters(), *dec.parameters()]
    opt = torch.optim.Adam(params, lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_steps)
    g = torch.Generator().manual_seed(seed)
    curve, run = [], []
    for st in range(1, n_steps + 1):
        x = X[torch.randint(0, len(X), (128,), generator=g)][:, None]
        z = enc(x)
        loss = F.binary_cross_entropy_with_logits(dec(z), x) + 1e-4 * (z ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if st % 100 == 0:
            curve.append((st, float(np.mean(run))))
            run = []
    enc.eval()
    dec.eval()
    return enc, dec, curve, sum(p.numel() for p in params)


def train_flow(Z, n_steps, seed, t_sampler="uniform", width=256):
    """Part 21's flow matching on vectors Z (N, d): t drawn uniformly or logit-normally."""
    import torch

    from videos.ai.ai21.compute import mlp

    torch.manual_seed(seed)
    net = mlp(Z.shape[1], Z.shape[1], width=width)
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_steps)
    g = torch.Generator().manual_seed(seed)
    for _ in range(n_steps):
        z1 = Z[torch.randint(0, len(Z), (256,), generator=g)]
        z0 = torch.randn(z1.shape, generator=g)
        if t_sampler == "logit-normal":  # SD3: t = sigmoid(u), u ~ N(0, 1): more training in the middle
            t = torch.sigmoid(torch.randn(len(z1), generator=g))
        else:
            t = torch.rand(len(z1), generator=g)
        zt = (1 - t[:, None]) * z0 + t[:, None] * z1
        loss = ((net(zt, t) - (z1 - z0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    net.eval()
    return net


def sample_flow(net, n, d, n_steps=40, seed=5):
    import torch

    z = torch.tensor(np.random.default_rng(seed).normal(size=(n, d)), dtype=torch.float32)
    with torch.no_grad():
        for k in range(n_steps):
            z = z + net(z, torch.full((n,), k / n_steps)) / n_steps
    return z


def decode(dec, z, side, ch):
    import torch

    with torch.no_grad():
        return torch.sigmoid(dec(z.reshape(-1, ch, side, side))).numpy()[:, 0]


# ---------------------------------------------------------------------------
def compute_latents():
    import torch

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test], dtype=torch.float32)
    Xte = torch.tensor(imgs[test], dtype=torch.float32)
    show = np.where(test)[0][::13][:8]
    n_ae, n_fl = steps(2000), steps(3000)
    part = CACHE.partial("latents", dict(configs=CONFIGS, n_ae=n_ae, n_fl=n_fl, seeds=[0, 1]))
    for side, ch in CONFIGS:
        key = f"g{side}c{ch}"
        if key in part:
            continue
        enc, dec, curve, n_params = train_ae(side, ch, X, n_ae, seed=2022)  # Rombach et al., latent diffusion
        with torch.no_grad():
            rec = torch.sigmoid(dec(enc(Xte[:, None]))).numpy()[:, 0]
            Ztr = enc(X[:, None]).reshape(len(X), -1)
        rmse = float(np.sqrt(((rec - imgs[test]) ** 2).mean()))
        mu, sd = Ztr.mean(0), Ztr.std(0) + 1e-6
        r = dict(side=side, ch=ch, numbers=side * side * ch, rmse=rmse, curve=curve, params=int(n_params),
                 rec=rec[np.searchsorted(np.where(test)[0], show)].tolist())
        for seed in (0, 1):
            net = train_flow((Ztr - mu) / sd, n_fl, seed=10 + seed)
            smp = decode(dec, sample_flow(net, 400, Ztr.shape[1], seed=50 + seed) * sd + mu, side, ch)
            q = score(smp)
            r[f"fd_s{seed}"], r[f"clear_s{seed}"], r[f"letters_s{seed}"] = q["fd"], q["clear"], q["letters"]
            if seed == 0:
                r["samples"] = smp[:16].tolist()
        part[key] = r
        print(f"    {side}x{side}x{ch} = {side * side * ch} numbers: rebuild RMSE {rmse:.3f}; samples FD "
              f"{r['fd_s0']:.1f}/{r['fd_s1']:.1f}, clear {r['clear_s0']:.2f}/{r['clear_s1']:.2f}", flush=True)
    out = dict(configs=[list(c) for c in CONFIGS], orig=imgs[show], n_ae=n_ae, n_fl=n_fl)
    for side, ch in CONFIGS:
        k = f"g{side}c{ch}"
        r = part[k]
        for f_ in ("rmse", "numbers", "params"):
            out[f"{k}_{f_}"] = r[f_]
        out[f"{k}_fd"] = [r["fd_s0"], r["fd_s1"]]
        out[f"{k}_clear"] = [r["clear_s0"], r["clear_s1"]]
        out[f"{k}_letters"] = [r["letters_s0"], r["letters_s1"]]
        out[f"{k}_rec"] = np.array(r["rec"])
        out[f"{k}_samples"] = np.array(r["samples"])
        out[f"{k}_curve"] = np.array(r["curve"])
    return out


# ---------------------------------------------------------------------------
TS_STEPS = [1, 2, 4, 8, 16, 40]


def compute_tsample():
    """In the 2 x 2 x 4 latent space (16 numbers), the same flow trained with uniform and with logit-normal t."""
    import torch

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test], dtype=torch.float32)
    side, ch = 2, 4
    enc, dec, _, _ = train_ae(side, ch, X, steps(2000), seed=2022)
    with torch.no_grad():
        Z = enc(X[:, None]).reshape(len(X), -1)
    mu, sd = Z.mean(0), Z.std(0) + 1e-6
    Zn = (Z - mu) / sd
    part = CACHE.partial("tsample", dict(steps=steps(3000), seeds=[0, 1, 2], sampling=TS_STEPS))
    for ts in ("uniform", "logit-normal"):
        for seed in (0, 1, 2):
            key = f"{ts}_s{seed}"
            if key in part:
                continue
            net = train_flow(Zn, steps(3000), seed=20 + seed, t_sampler=ts)
            fd, cl = [], []
            for k in TS_STEPS:
                q = score(decode(dec, sample_flow(net, 400, Z.shape[1], n_steps=k, seed=60 + seed) * sd + mu, side, ch))
                fd.append(q["fd"])
                cl.append(q["clear"])
            part[key] = dict(fd=fd, clear=cl)
            print(f"    {key}: FD by steps {np.round(fd, 1)}", flush=True)
    out = dict(sampling=TS_STEPS, side=side, ch=ch)
    for ts in ("uniform", "logit-normal"):
        out[f"{ts}_fd"] = np.array([part[f"{ts}_s{s}"]["fd"] for s in (0, 1, 2)])
        out[f"{ts}_clear"] = np.array([part[f"{ts}_s{s}"]["clear"] for s in (0, 1, 2)])
    return out


# ---------------------------------------------------------------------------
SHIFT_SIGMAS = np.round(np.linspace(0.30, 0.985, 30), 4)


def shift_sigma(sigma, alpha):
    """SD3's resolution shift, with sigma the share of noise: sigma' = alpha sigma / (1 + (alpha - 1) sigma)."""
    return alpha * sigma / (1 + (alpha - 1) * sigma)


def compute_shift():
    """The same 520 letters (20 training fonts, one of each letter) drawn at 20, 40 and 80 pixels. Noise them,
    z = (1 - sigma) x + sigma e, and ask the exact posterior over the 520 which letter picture it was: the
    probability it gives the right one says how much of the picture the noise has destroyed. Then the higher
    resolutions at the shifted levels sigma' = alpha sigma / (1 + (alpha - 1) sigma), alpha = side / 20."""
    import torch

    threads()
    files = font_files()[:20]
    g = np.random.default_rng(2024)  # Esser et al., Scaling Rectified Flow Transformers (2024)
    offs = g.uniform(-1.5, 1.5, (len(files), 26, 2))
    sizes = (20, 40, 80)
    data = {s: np.array([[render(f, ch, s, *offs[i, j]) for j, ch in enumerate(LETTERS)] for i, f in enumerate(files)])
            .reshape(-1, s * s) for s in sizes}
    N = len(data[20])
    n_mc = steps(400)
    pick = g.integers(0, N, n_mc)

    def p_right(s, sig, seed):
        """Posterior probability of the right picture, averaged over noisy versions of n_mc pictures."""
        X = torch.tensor(data[s], dtype=torch.float64)
        x = X[torch.tensor(pick)]
        e = torch.tensor(np.random.default_rng(seed).normal(size=x.shape))
        z = (1 - sig) * x + sig * e
        d2 = (z ** 2).sum(1)[:, None] + ((1 - sig) ** 2) * (X ** 2).sum(1)[None] - 2 * (1 - sig) * z @ X.T
        logw = -d2 / (2 * sig ** 2)
        logw = logw - logw.max(1, keepdim=True).values
        w = torch.exp(logw)
        w = w / w.sum(1, keepdim=True)
        return float(w[torch.arange(len(pick)), torch.tensor(pick)].mean())

    out = dict(sizes=list(sizes), sigmas=SHIFT_SIGMAS.tolist(), N=N, n_mc=n_mc)
    for s in sizes:
        out[f"ex_{s}"] = data[s].reshape(-1, s, s)[[0, 26 * 5 + 7]]
    for s in sizes:
        out[f"p_{s}"] = [p_right(s, float(sig), 7) for sig in SHIFT_SIGMAS]
        alpha = s / 20
        out[f"pshift_{s}"] = [p_right(s, float(shift_sigma(sig, alpha)), 7) for sig in SHIFT_SIGMAS]
    base = np.array(out["p_20"])
    out["gap_before"] = {str(s): float(np.max(np.abs(np.array(out[f"p_{s}"]) - base))) for s in sizes[1:]}
    out["gap_after"] = {str(s): float(np.max(np.abs(np.array(out[f"pshift_{s}"]) - base))) for s in sizes[1:]}
    # the noise level at which the posterior is still right half the time, at each size
    for s in sizes:
        p = np.array(out[f"p_{s}"])
        out[f"half_{s}"] = float(np.interp(0.5, p[::-1], SHIFT_SIGMAS[::-1]))
    # the same noise on a 20-pixel letter and its 80-pixel drawing; the 80-pixel one averaged back down
    x20, x80 = data[20][0].reshape(20, 20), data[80][0].reshape(80, 80)
    sig = 0.75
    n20 = (1 - sig) * x20 + sig * np.random.default_rng(3).normal(size=x20.shape)
    n80 = (1 - sig) * x80 + sig * np.random.default_rng(4).normal(size=x80.shape)
    pooled = n80.reshape(20, 4, 20, 4).mean((1, 3))
    out.update(demo_sigma=sig, demo20=n20, demo80=n80, demo_pooled=pooled, demo_clean80=x80,
               demo_left=float(np.std(pooled - (1 - sig) * x80.reshape(20, 4, 20, 4).mean((1, 3)))))
    print(f"    sigma right half the time: {[round(out[f'half_{s}'], 3) for s in sizes]}; largest gap to 20 px before "
          f"the shift {out['gap_before']}, after {out['gap_after']}", flush=True)
    return out
