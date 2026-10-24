"""Part 22, chapters 12-14: video. Clips of a letter moving one pixel a frame in a 20 x 20 box, bouncing off the walls.

    vae3d   a causal video autoencoder: frame 0 squeezed alone, then every 4 frames into one latent frame, 4x in space
    clips   video diffusion in a frame autoencoder's latents (each frame squeezed to 5 x 5 x 4 numbers, as video
            models work in their autoencoder's latents). Three models of one size, three seeds each, all trained on
            8-frame clips with the first 1 or 2 frames given:
              clip     one noise level for the whole clip, every frame attending to every other (full sequence)
              teacher  frame by frame: earlier frames clean, one frame noised (teacher forcing)
              forcing  frame by frame, every frame at its own noise level (diffusion forcing, Chen et al. 2024)
            Frames that agree: from one given frame, the clip model's frames drawn together against frames taken from
            different samples. Rolling forward: from two given frames (which fix the motion), 30 more frames, 4x the
            training length; the letter's identity and its distance from where physics puts it, frame by frame.
"""

from __future__ import annotations

import math

import numpy as np

from videos.ai.ai22.compute import CACHE, GL, QUICK, dataset, steps, threads, train_judge

S_LET = 12  # the letter's size in the box
T_TRAIN = 8
LONG = 32
SEEDS = (0, 1, 2)
MODES = ("clip", "teacher", "forcing")
D, L, H = 96, 4, 4
N_STEPS, BATCH = 3000, 64
LAT_SIDE, LAT_CH = 5, 4


def small_letters():
    """Every letter picture shrunk to 12 x 12, with its label and whether its font is held out."""
    from PIL import Image

    imgs, labels, test, _, _ = dataset()
    small = np.array([np.asarray(Image.fromarray((im * 255).astype(np.uint8)).resize((S_LET, S_LET), Image.BILINEAR),
                                 float) / 255 for im in imgs])
    return small, labels, test


def physics(p, v, T):
    """Positions (T, 2) of the letter's corner: one pixel a frame, bouncing off the walls."""
    room = GL - S_LET
    p, v = np.array(p, float), np.array(v, float)
    out = []
    for _ in range(T):
        out.append(p.copy())
        for a in range(2):
            if not 0 <= p[a] + v[a] <= room:
                v[a] = -v[a]
        p = p + v
    return np.array(out)


def make_clips(n, T, seed, split="train"):
    """n clips of T frames; the letter, its start and its velocity are random. Returns clips, labels, starts, vels."""
    small, labels, test = small_letters()
    pool = np.where(~test if split == "train" else test)[0]
    g = np.random.default_rng(seed)
    clips = np.zeros((n, T, GL, GL), np.float32)
    lab, P0, V0 = np.zeros(n, int), np.zeros((n, 2)), np.zeros((n, 2))
    room = GL - S_LET
    for i in range(n):
        j = int(g.choice(pool))
        lab[i] = labels[j]
        P0[i] = g.integers(0, room + 1, 2)
        V0[i] = [g.choice([-1, 1]), g.choice([-1, 0, 1])]
        for t, (y, x) in enumerate(physics(P0[i], V0[i], T).astype(int)):
            clips[i, t, y:y + S_LET, x:x + S_LET] = small[j]
    return clips, lab, P0, V0


def centers(frames):
    """Each frame's centre of brightness (..., 2) in pixels."""
    f = np.clip(np.asarray(frames), 0, None)
    w = f.sum((-1, -2)) + 1e-9
    yy, xx = np.mgrid[:GL, :GL]
    return np.stack([(f * yy).sum((-1, -2)) / w, (f * xx).sum((-1, -2)) / w], -1)


def jerk_of(clips):
    """Median over clips of the mean |second difference| of the letter's centre (pixels, both axes summed)."""
    c = centers(clips)
    return float(np.median(np.abs(np.diff(c, 2, axis=1)).sum(-1).mean(1)))


_VJ = {}


def video_judge():
    """A judge for single frames: the small letters placed anywhere in the box (training fonts)."""
    import torch

    if "net" not in _VJ:
        small, labels, test = small_letters()
        g = np.random.default_rng(7)
        idx = np.where(~test)[0]
        X = np.zeros((len(idx) * 4, GL, GL), np.float32)
        Y = np.repeat(labels[idx], 4)
        for i, im in enumerate(np.repeat(small[idx], 4, 0)):
            y, x = g.integers(0, GL - S_LET + 1, 2)
            X[i, y:y + S_LET, x:x + S_LET] = im
        _VJ["net"] = train_judge(torch.tensor(X), torch.tensor(Y), 3000, seed=2, shift=0)
    return _VJ["net"]


def read(frames, want):
    """Per frame, whether the judge reads the right letter (confidence above 0.5). frames (B, T, 20, 20)."""
    import torch

    B, T = frames.shape[:2]
    with torch.no_grad():
        p = torch.softmax(video_judge()(torch.tensor(np.asarray(frames, np.float32).reshape(-1, GL, GL))), 1).numpy()
    pred, conf = p.argmax(1).reshape(B, T), p.max(1).reshape(B, T)
    return (pred == np.asarray(want)[:, None]) & (conf > 0.5)


# ---------------------------------------------------------------------------
# The frame autoencoder
# ---------------------------------------------------------------------------
def frame_ae():
    from videos.ai.ai22.latents import autoencoder

    return autoencoder(LAT_SIDE, LAT_CH)


def train_frame_ae(frames, n_steps, seed=2025):
    import torch

    from videos.ai.ai22.latents import train_ae

    enc, dec, curve, _ = train_ae(LAT_SIDE, LAT_CH, torch.tensor(frames), n_steps, seed)
    return enc, dec


# ---------------------------------------------------------------------------
# The video model: one token per frame (its 100 latent numbers), adaLN-Zero from each frame's own noise level
# ---------------------------------------------------------------------------
def video_net(causal: bool, T=T_TRAIN, dz=LAT_SIDE * LAT_SIDE * LAT_CH):
    import torch
    import torch.nn as nn

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1 = nn.LayerNorm(D, elementwise_affine=False)
            self.n2 = nn.LayerNorm(D, elementwise_affine=False)
            self.att = nn.MultiheadAttention(D, H, batch_first=True)
            self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
            self.ada = nn.Linear(D, 6 * D)
            nn.init.zeros_(self.ada.weight)
            nn.init.zeros_(self.ada.bias)

        def forward(self, h, c, mask):
            s1, b1, g1, s2, b2, g2 = self.ada(c).chunk(6, -1)
            a = self.n1(h) * (1 + s1) + b1
            h = h + g1 * self.att(a, a, a, attn_mask=mask, need_weights=False)[0]
            return h + g2 * self.mlp(self.n2(h) * (1 + s2) + b2)

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.T = T
            self.inp = nn.Linear(dz, D)
            self.pos = nn.Parameter(torch.randn(1, T, D) * 0.02)
            self.freq = nn.Parameter(torch.randn(D // 2) * 4.0, requires_grad=False)
            self.tmlp = nn.Sequential(nn.Linear(D, D), nn.SiLU(), nn.Linear(D, D))
            self.blocks = nn.ModuleList([Block() for _ in range(L)])
            self.nf = nn.LayerNorm(D, elementwise_affine=False)
            self.out = nn.Linear(D, dz)
            nn.init.zeros_(self.out.weight)
            nn.init.zeros_(self.out.bias)
            fr = torch.arange(T)
            self.register_buffer("mask", (fr[None, :] > fr[:, None]) if causal else torch.zeros(T, T, dtype=torch.bool))

        def forward(self, z, t):
            """z (B, F, dz) frame latents at noise levels t (B, F); F <= T. Returns each frame's velocity."""
            Fr = z.shape[1]
            a = t[..., None] * self.freq * 2 * math.pi
            c = self.tmlp(torch.cat([torch.sin(a), torch.cos(a)], -1))
            h = self.inp(z) + self.pos[:, :Fr]
            for b in self.blocks:
                h = b(h, c, self.mask[:Fr, :Fr])
            return self.out(self.nf(h))

    return Net()


def levels(mode, B, T, g):
    """Each training clip's noise levels t (B, T) (1 = clean) and loss weights (B, T). The first k frames (k = 1 or
    2) are given clean and never learned."""
    import torch

    ar = torch.arange(T)[None]
    k = torch.randint(1, 3, (B, 1), generator=g)
    given = ar < k
    if mode == "clip":  # the frames after the given ones share one noise level
        t = torch.rand(B, 1, generator=g).expand(B, T)
        w = torch.ones(B, T)
    elif mode == "forcing":  # every frame its own noise level
        t = torch.rand(B, T, generator=g)
        w = torch.ones(B, T)
    else:  # teacher forcing: frames before f clean, frame f noised and learned
        f = k[:, 0] + (torch.rand(B, generator=g) * (T - k[:, 0])).long()
        t = torch.where(ar < f[:, None], torch.ones(B, T), torch.rand(B, 1, generator=g).expand(B, T))
        w = (ar == f[:, None]).float()
    return torch.where(given, torch.ones(B, T), t), torch.where(given, torch.zeros(B, T), w)


def train_video(mode, Z, n_steps, seed):
    import torch

    torch.manual_seed(2024 + seed)  # Chen et al., Diffusion Forcing (2024)
    m = video_net(causal=mode != "clip")
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=n_steps, pct_start=0.05)
    g = torch.Generator().manual_seed(seed)
    curve, run = [], []
    T = Z.shape[1]
    for st in range(1, n_steps + 1):
        z1 = Z[torch.randint(0, len(Z), (BATCH,), generator=g)]
        z0 = torch.randn(z1.shape, generator=g)
        t, w = levels(mode, BATCH, T, g)
        zt = (1 - t[..., None]) * z0 + t[..., None] * z1
        err = ((m(zt, t) - (z1 - z0)) ** 2).mean(-1)
        loss = (err * w).sum() / w.sum()
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


def sample_joint(m, given, n_new, seed, n_steps=20):
    """The clip model: the given frames held clean, n_new frames denoised together."""
    import torch

    g = torch.Generator().manual_seed(seed)
    B, k, dz = given.shape
    x = torch.cat([given, torch.randn(B, n_new, dz, generator=g)], 1)
    with torch.no_grad():
        for s in range(n_steps):
            t = torch.cat([torch.ones(B, k), torch.full((B, n_new), s / n_steps)], 1)
            v = m(x, t)
            x = torch.cat([given, x[:, k:] + v[:, k:] / n_steps], 1)
    return x


def rollout(m, mode, given, n_frames, seed, n_steps=20, ctx_level=1.0):
    """Extend the given frames to n_frames. The frame-by-frame models write one frame at a time, seeing at most the
    last T - 1 frames (generated ones at ``ctx_level``: 1 = taken as clean, below 1 = slightly re-noised, diffusion
    forcing's way to steady a long rollout); the clip model writes 6 frames at a time from the last 2."""
    import torch

    g = torch.Generator().manual_seed(seed)
    B, k, dz = given.shape
    done = given.clone()
    real = torch.zeros(B, n_frames, dtype=torch.bool)
    real[:, :k] = True
    with torch.no_grad():
        while done.shape[1] < n_frames:
            if mode == "clip":
                n_new = min(m.T - 2, n_frames - done.shape[1])
                new = sample_joint(m, done[:, -2:], n_new, seed=int(torch.randint(0, 10 ** 6, (1,), generator=g)),
                                   n_steps=n_steps)[:, 2:]
                done = torch.cat([done, new], 1)
                continue
            ctx = done[:, -(m.T - 1):]
            rc = real[:, max(0, done.shape[1] - (m.T - 1)):done.shape[1]]
            lv = torch.where(rc, torch.ones(rc.shape), torch.full(rc.shape, ctx_level))
            if ctx_level < 1:
                ctx = lv[..., None] * ctx + (1 - lv[..., None]) * torch.randn(ctx.shape, generator=g)
            x = torch.randn(B, 1, dz, generator=g)
            for s in range(n_steps):
                t = torch.cat([lv, torch.full((B, 1), s / n_steps)], 1)
                x = x + m(torch.cat([ctx, x], 1), t)[:, -1:] / n_steps
            done = torch.cat([done, x], 1)
    return done


def compute_clips():
    import time

    import torch

    threads()
    T, n_test = T_TRAIN, 64
    clips, lab, _, _ = make_clips(200 if QUICK else 6000, T, seed=0)
    # the frame autoencoder, trained on the training clips' frames
    fae = CACHE.dir / "frame_ae.pt"
    enc, dec = frame_ae()
    if fae.exists():
        st_ = torch.load(fae)
        enc.load_state_dict(st_["enc"])
        dec.load_state_dict(st_["dec"])
        enc.eval()
        dec.eval()
    else:
        enc, dec = train_frame_ae(clips[:, ::2].reshape(-1, GL, GL), steps(2500))
        torch.save(dict(enc=enc.state_dict(), dec=dec.state_dict()), fae)
    dz = LAT_SIDE * LAT_SIDE * LAT_CH

    def enc_frames(c):
        with torch.no_grad():
            z = enc(torch.tensor(c.reshape(-1, 1, GL, GL)))
        return z.reshape(c.shape[0], c.shape[1], dz)

    def dec_frames(z):
        with torch.no_grad():
            x = torch.sigmoid(dec((z * sd + mu).reshape(-1, LAT_CH, LAT_SIDE, LAT_SIDE)))
        return x.numpy().reshape(z.shape[0], z.shape[1], GL, GL)

    Zr = enc_frames(clips)
    mu, sd = Zr.reshape(-1, dz).mean(0), Zr.reshape(-1, dz).std(0) + 1e-6
    Z = (Zr - mu) / sd
    test_clips, test_lab, tP, tV = make_clips(n_test, LONG, seed=1, split="test")  # unseen fonts
    Zt = (enc_frames(test_clips) - mu) / sd
    rec = dec_frames(Zt)
    out = dict(T=T, long=LONG, n_test=n_test, dz=dz, ae_rmse=float(np.sqrt(((rec - test_clips) ** 2).mean())),
               real_right=float(read(test_clips, test_lab).mean()), rec_right=float(read(rec, test_lab).mean()),
               real_jerk=jerk_of(test_clips[:, 1:T]), examples=test_clips[:4, :T], rec_examples=rec[:4, :T])
    print(f"    frame autoencoder: rebuild RMSE {out['ae_rmse']:.3f}; judge right on real frames "
          f"{out['real_right']:.3f}, on rebuilt {out['rec_right']:.3f}", flush=True)
    true_c = centers(test_clips)
    n = steps(N_STEPS)
    part = CACHE.partial("clips", dict(modes=MODES, seeds=SEEDS, steps=n, D=D, L=L, batch=BATCH, T=T, long=LONG))
    for seed in SEEDS:
        for mode in MODES:
            key = f"{mode}_s{seed}"
            if key in part:
                continue
            t0 = time.time()
            m, curve = train_video(mode, Z, n, seed)
            r = dict(curve=curve, secs=time.time() - t0)
            if mode == "clip":  # frames that agree: one given frame, seven drawn together or separately
                joint = dec_frames(sample_joint(m, Zt[:, :1], T - 1, seed=30 + seed))
                indep = joint.copy()
                for f in range(1, T):
                    indep[:, f] = dec_frames(sample_joint(m, Zt[:, :1], T - 1, seed=40 + 10 * seed + f))[:, f]
                for nm, c in (("joint", joint), ("indep", indep)):
                    rr = read(c[:, 1:], test_lab)
                    r[f"{nm}_right"] = float(rr.mean())
                    r[f"{nm}_all_right"] = float(rr.all(1).mean())
                    r[f"{nm}_jerk"] = jerk_of(c[:, 1:])
                    if seed == 0:
                        r[f"{nm}_clips"] = c[:6].tolist()
            variants = [("", 1.0)] + ([("_noisy", 0.9)] if mode == "forcing" else [])
            for suf, lv in variants:  # rolling forward from two given frames, to 4x the training length
                R = dec_frames(rollout(m, mode, Zt[:, :2], LONG, seed=50 + seed, ctx_level=lv))
                rr = read(R, test_lab)
                err = np.linalg.norm(centers(R) - true_c, axis=-1)
                r[f"roll{suf}_right"] = rr.mean(0).tolist()
                r[f"roll{suf}_pos"] = np.median(err, 0).tolist()
                r[f"roll{suf}_rmse"] = np.sqrt(((R - test_clips) ** 2).mean((0, 2, 3))).tolist()
                if seed == 0:
                    r[f"roll{suf}_clips"] = R[:3].tolist()
            part[key] = r
            pr = np.array(r["roll_pos"])
            print(f"    {key}: rollout position error (px) at frames 2-7 {pr[2:T].mean():.2f}, 24-31 "
                  f"{pr[-8:].mean():.2f}; right letter {np.mean(r['roll_right'][2:T]):.2f} -> "
                  f"{np.mean(r['roll_right'][-8:]):.2f}; {r['secs']:.0f}s", flush=True)
    for mode in MODES:
        ps = [part[f"{mode}_s{s}"] for s in SEEDS]
        for suf in ("", "_noisy"):
            if f"roll{suf}_pos" not in ps[0]:
                continue
            for f_ in ("right", "pos", "rmse"):
                out[f"{mode}{suf}_{f_}"] = np.array([p_[f"roll{suf}_{f_}"] for p_ in ps])
            out[f"{mode}{suf}_clips"] = np.array(ps[0][f"roll{suf}_clips"])
        out[f"{mode}_curve"] = np.array([np.array(p_["curve"]) for p_ in ps])
    cp = [part[f"clip_s{s}"] for s in SEEDS]
    for nm in ("joint", "indep"):
        for f_ in ("right", "all_right", "jerk"):
            out[f"{nm}_{f_}"] = [p_[f"{nm}_{f_}"] for p_ in cp]
        out[f"{nm}_clips"] = np.array(cp[0][f"{nm}_clips"])
    out["given"], out["given_labels"] = test_clips[:6, :T], test_lab[:6]
    out["truth"] = test_clips[:3]
    out["steps"], out["seeds"], out["params"] = n, list(SEEDS), int(sum(p.numel() for p in video_net(True).parameters()
                                                                        if p.requires_grad))
    return out


# ---------------------------------------------------------------------------
def compute_vae3d():
    """A causal video autoencoder: frame 0 squeezed alone, then every 4 frames into one latent frame; 4x in space."""
    import torch
    import torch.nn as nn

    threads()
    torch.manual_seed(2024)
    T, C = 9, 4
    clips, _, _, _ = make_clips(32 if QUICK else 3000, T, seed=5)
    test, _, _, _ = make_clips(64, T, seed=6, split="test")

    class Enc(nn.Module):
        def __init__(self):
            super().__init__()
            self.first = nn.Sequential(nn.Conv2d(1, 32, 4, 2, 1), nn.SiLU(), nn.Conv2d(32, C, 4, 2, 1))  # 20 -> 5
            self.group = nn.Sequential(nn.Conv3d(1, 32, (4, 4, 4), (4, 2, 2), (0, 1, 1)), nn.SiLU(),
                                       nn.Conv3d(32, C, (1, 4, 4), (1, 2, 2), (0, 1, 1)))  # (4, 20, 20) -> (1, 5, 5)

        def forward(self, x):  # (B, 9, 20, 20) -> (B, C, 3, 5, 5); latent frame k sees only frames up to 4k
            z0 = self.first(x[:, :1])[:, :, None]
            z1 = self.group(x[:, None, 1:5])
            z2 = self.group(x[:, None, 5:9])
            return torch.cat([z0, z1, z2], 2)

    class Dec(nn.Module):
        def __init__(self):
            super().__init__()
            self.first = nn.Sequential(nn.ConvTranspose2d(C, 32, 4, 2, 1), nn.SiLU(), nn.ConvTranspose2d(32, 1, 4, 2, 1))
            self.group = nn.Sequential(nn.ConvTranspose3d(C, 32, (1, 4, 4), (1, 2, 2), (0, 1, 1)), nn.SiLU(),
                                       nn.ConvTranspose3d(32, 1, (4, 4, 4), (4, 2, 2), (0, 1, 1)))

        def forward(self, z):
            f0 = self.first(z[:, :, 0])
            g1 = self.group(z[:, :, 1:2])[:, 0]
            g2 = self.group(z[:, :, 2:3])[:, 0]
            return torch.cat([f0, g1, g2], 1)  # logits: the pixels are mostly black, so train with cross-entropy

    enc, dec = Enc(), Dec()
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters()], lr=2e-3)
    X = torch.tensor(clips)
    g = torch.Generator().manual_seed(0)
    n = steps(3000)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n)
    for _ in range(n):
        x = X[torch.randint(0, len(X), (32,), generator=g)]
        loss = torch.nn.functional.binary_cross_entropy_with_logits(dec(enc(x)), x)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    with torch.no_grad():
        Xt = torch.tensor(test)
        z = enc(Xt)
        rec = torch.sigmoid(dec(z)).numpy()
        # a still picture is a one-frame video: the first frame goes through the same encoder and decoder alone
        still = torch.sigmoid(dec.first(enc.first(Xt[:, :1]))).numpy()[:, 0]
    rmse = float(np.sqrt(((rec - test) ** 2).mean()))
    per_frame = np.sqrt(((rec - test) ** 2).mean((0, 2, 3)))
    out = dict(T=T, C=C, latent_shape=list(z.shape[1:]), pixels=T * GL * GL, numbers=int(np.prod(z.shape[1:])),
               rmse=rmse, per_frame=per_frame, orig=test[:3], rec=rec[:3], still_rmse=float(np.sqrt(((still - test[:, 0]) ** 2).mean())),
               steps=n)
    print(f"    {T} frames x 400 pixels -> {out['numbers']} numbers ({out['pixels'] / out['numbers']:.0f}x); "
          f"rebuild error {rmse:.3f}", flush=True)
    return out
