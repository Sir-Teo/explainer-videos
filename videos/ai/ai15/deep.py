"""Part 15's deeper experiments (registered as cache items in compute.py).

Images: what a latent space trades (an autoencoder against variational autoencoders with a growing KL weight: how well
each rebuilds a picture, and how good the pictures are when Part 14's flow matching is run in its latent space); how
the training noise levels are drawn (uniform against SD3's logit-normal); next-scale prediction's residual tokens.

Video: clips of a letter moving and bouncing in a 20 x 20 box. A causal autoencoder that squeezes 9 frames into 3;
a clip model (one noise level for the whole clip, every frame attending to every other) against frames drawn one at a
time; and models that write frame after frame, trained with clean earlier frames (teacher forcing) or with earlier
frames at their own random noise levels (diffusion forcing), rolled out four times longer than they were trained.

A "judge" (a small classifier trained on the same pictures) scores generated pictures: how many it recognizes
confidently, and as which letters. Set AI15_QUICK=1 for a fast smoke test with tiny step counts.
"""

from __future__ import annotations

import math
import os

import numpy as np

GL = 20
QUICK = os.environ.get("AI15_QUICK") == "1"


def steps(n: int) -> int:
    return 20 if QUICK else n


# ---------------------------------------------------------------------------
def train_judge(X, Y, n_steps=2000, seed=0, shift=0):
    """A small classifier, pictures (N, 400) in [0, 1] -> 26 letters; ``shift`` pixels of random translation."""
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.manual_seed(seed)
    net = nn.Sequential(nn.Linear(GL * GL, 384), nn.ReLU(), nn.Linear(384, 192), nn.ReLU(), nn.Linear(192, 26))
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    g = torch.Generator().manual_seed(seed)
    for _ in range(steps(n_steps)):
        i = torch.randint(0, len(X), (256,), generator=g)
        x = X[i].view(-1, GL, GL)
        if shift:
            s = torch.randint(-shift, shift + 1, (2,), generator=g)
            x = torch.roll(x, (int(s[0]), int(s[1])), (1, 2))
        x = (x + 0.06 * torch.randn(x.shape, generator=g)).view(-1, GL * GL)
        loss = F.cross_entropy(net(x), Y[i])
        opt.zero_grad()
        loss.backward()
        opt.step()
    net.eval()
    return net


def judge_scores(net, imgs01):
    """How many pictures the judge recognizes with confidence above 0.8, and which letters."""
    import torch

    with torch.no_grad():
        p = torch.softmax(net(torch.tensor(np.asarray(imgs01).reshape(len(imgs01), -1), dtype=torch.float32)), 1).numpy()
    conf, pred = p.max(1), p.argmax(1)
    sure = conf > 0.8
    return dict(clear=float(sure.mean()), letters=int(len(set(pred[sure].tolist()))), pred=pred, conf=conf)


def flow_mlp(d, width=256):
    from videos.ai.ai14.compute import mlp

    return mlp(d, d, width=width)


def train_flow(Z, n_steps=3000, seed=0, t_sampler="uniform"):
    """Flow matching (Part 14) in a latent space Z (N, d); t drawn uniformly or logit-normally."""
    import torch

    torch.manual_seed(seed)
    net = flow_mlp(Z.shape[1])
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    g = torch.Generator().manual_seed(seed)
    for _ in range(steps(n_steps)):
        z1 = Z[torch.randint(0, len(Z), (512,), generator=g)]
        z0 = torch.randn(z1.shape, generator=g)
        if t_sampler == "logit-normal":  # SD3: t = sigmoid(u), u ~ N(0, 1): more training where the middle is hardest
            t = torch.sigmoid(torch.randn(len(z1), generator=g))
        else:
            t = torch.rand(len(z1), generator=g)
        zt = (1 - t[:, None]) * z0 + t[:, None] * z1
        loss = ((net(zt, t) - (z1 - z0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    net.eval()
    return net


def sample_flow(net, n, d, n_steps=40, seed=5):
    import torch

    z = torch.tensor(np.random.default_rng(seed).normal(size=(n, d)), dtype=torch.float32)
    with torch.no_grad():
        for k in range(n_steps):
            z = z + net(z, torch.full((n,), k / n_steps)) / n_steps
    return z


# ---------------------------------------------------------------------------
def compute_vae():
    import torch
    import torch.nn as nn

    from videos.ai.ai15.compute import dataset

    torch.set_num_threads(2)
    imgs, labels, test, _ = dataset()
    X = torch.tensor(imgs.reshape(len(imgs), -1), dtype=torch.float32)
    Y = torch.tensor(labels)
    judge = train_judge(X, Y, seed=1)
    jt = judge_scores(judge, imgs[test])
    print(f"    judge: {100 * float((jt['pred'] == labels[test]).mean()):.0f}% right on held-out fonts", flush=True)
    Zd = 16
    betas = [0.0, 0.003, 0.01, 0.03, 0.1]
    out = dict(betas=betas, Z=Zd, judge_acc=float((jt["pred"] == labels[test]).mean()))
    keep = None
    for b in betas:
        torch.manual_seed(2013)  # Kingma & Welling, Auto-Encoding Variational Bayes
        enc = nn.Sequential(nn.Linear(GL * GL, 256), nn.SiLU(), nn.Linear(256, 128), nn.SiLU(), nn.Linear(128, 2 * Zd))
        dec = nn.Sequential(nn.Linear(Zd, 128), nn.SiLU(), nn.Linear(128, 256), nn.SiLU(), nn.Linear(256, GL * GL))
        opt = torch.optim.Adam([*enc.parameters(), *dec.parameters()], lr=2e-3)
        g = torch.Generator().manual_seed(0)
        tr = torch.tensor(np.where(~test)[0])
        for _ in range(steps(5000)):
            x = X[tr[torch.randint(0, len(tr), (256,), generator=g)]]
            mu, logv = enc(x).chunk(2, 1)
            z = mu + torch.exp(0.5 * logv) * torch.randn(mu.shape, generator=g) if b > 0 else mu
            rec = ((torch.sigmoid(dec(z)) - x) ** 2).sum(1).mean()
            kl = 0.5 * (mu ** 2 + logv.exp() - logv - 1).sum(1).mean()
            loss = rec + b * kl
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            mu, logv = enc(X).chunk(2, 1)
            xh = torch.sigmoid(dec(mu))
            rmse = float(((xh - X)[torch.tensor(test)] ** 2).mean().sqrt())
            kl = float((0.5 * (mu ** 2 + logv.exp() - logv - 1).sum(1)).mean()) if b > 0 else float("nan")
        m_, s_ = mu.mean(0), mu.std(0)
        net = train_flow((mu - m_) / s_, seed=3)
        z = sample_flow(net, 400, Zd) * s_ + m_
        with torch.no_grad():
            smp = torch.sigmoid(dec(z)).numpy().reshape(-1, GL, GL)
        q = judge_scores(judge, smp)
        tag = f"{b:g}"
        out[f"rmse_{tag}"], out[f"kl_{tag}"], out[f"clear_{tag}"], out[f"letters_{tag}"] = rmse, kl, q["clear"], q["letters"]
        out[f"samples_{tag}"] = smp[:24]
        out[f"recon_{tag}"] = xh.numpy().reshape(-1, GL, GL)[np.where(test)[0][::40][:8]]
        print(f"    beta {tag}: rebuild error {rmse:.3f}, KL {kl:.1f} nats; samples clear {100 * q['clear']:.0f}%, "
              f"{q['letters']} letters", flush=True)
        if b == 0.01:
            keep = (mu.detach(), dec)
    out["orig"] = imgs[np.where(test)[0][::40][:8]]
    # how the training noise levels are drawn: uniform against SD3's logit-normal, in the beta = 0.01 latent space
    mu, dec = keep
    m_, s_ = mu.mean(0), mu.std(0)
    Zn = (mu - m_) / s_
    sampling = [1, 2, 4, 8, 16, 40]
    out["ts_steps"] = sampling
    for ts in ("uniform", "logit-normal"):
        net = train_flow(Zn, seed=4, t_sampler=ts)
        cl = []
        for k in sampling:
            z = sample_flow(net, 400, Zd, n_steps=k) * s_ + m_
            with torch.no_grad():
                cl.append(judge_scores(judge, torch.sigmoid(dec(z)).numpy().reshape(-1, GL, GL))["clear"])
        out[f"ts_{ts}"] = cl
        print(f"    t {ts}: clear at {sampling} steps: {np.round(cl, 2)}", flush=True)
    return out


# ---------------------------------------------------------------------------
def nearest(x, cb):
    """Index of the nearest entry of a sorted 1-D codebook, for every number in x."""
    return np.searchsorted((cb[1:] + cb[:-1]) / 2, x)


def compute_var():
    """Next-scale prediction's tokens: the residual at each scale, quantized to one of 16 levels."""
    from videos.ai.ai15.compute import dataset

    imgs, labels, test, _ = dataset()
    sizes = [1, 2, 4, 5, 10, 20]
    g = np.random.default_rng(2024)  # Tian et al., Visual Autoregressive Modeling (2024)
    recon = np.zeros_like(imgs)
    errs, books, toks = [], [], []
    for s in sizes:
        k = GL // s
        target = (imgs - recon).reshape(len(imgs), s, k, s, k).mean((2, 4))  # what this scale still has to add
        vals = target[~test].ravel()
        cb = np.quantile(vals, np.linspace(0.02, 0.98, 16))  # 16 levels, then a few rounds of k-means
        for _ in range(12):
            idx = nearest(vals, cb)
            n_ = np.bincount(idx, minlength=16)
            cb = np.where(n_ > 0, np.bincount(idx, weights=vals, minlength=16) / np.maximum(n_, 1), cb)
            cb = np.sort(cb)
        q = cb[nearest(target, cb)]
        recon = recon + np.kron(q, np.ones((1, k, k)))
        errs.append(float(np.sqrt(((recon - imgs)[test] ** 2).mean())))
        books.append(cb)
        toks.append(s * s)
    ex = int(np.where(test & (labels == 0))[0][0])
    steps_shown = []
    rec = np.zeros(GL * GL).reshape(GL, GL)
    for s, cb in zip(sizes, books):
        k = GL // s
        target = (imgs[ex] - rec).reshape(s, k, s, k).mean((1, 3))
        rec = rec + np.kron(cb[nearest(target, cb)], np.ones((k, k)))
        steps_shown.append(rec.copy())
    out = dict(sizes=sizes, errs=errs, tokens=toks, total=int(sum(toks)), example=np.array(steps_shown), image=imgs[ex])
    print(f"    rebuild error after each scale: {np.round(errs, 3)}; {sum(toks)} tokens in {len(sizes)} steps", flush=True)
    assert errs[-1] < errs[0]
    return out


# ---------------------------------------------------------------------------
def small_letters():
    """Every letter picture shrunk to 12 x 12, with its label and whether its font is held out."""
    from PIL import Image

    from videos.ai.ai15.compute import dataset

    imgs, labels, test, _ = dataset()
    small = np.array([np.asarray(Image.fromarray((im * 255).astype(np.uint8)).resize((12, 12), Image.BILINEAR), float) / 255
                      for im in imgs])
    return small, labels, test


def make_clips(n, T, seed, split="train"):
    """Clips of a 12 x 12 letter moving one pixel a frame in a 20 x 20 box, bouncing off the walls."""
    small, labels, test = small_letters()
    pool = np.where(~test if split == "train" else test)[0]
    g = np.random.default_rng(seed)
    clips = np.zeros((n, T, GL, GL), np.float32)
    lab = np.zeros(n, int)
    room = GL - 12
    for i in range(n):
        j = int(g.choice(pool))
        lab[i] = labels[j]
        p = g.integers(0, room + 1, 2).astype(float)
        v = np.array([g.choice([-1, 1]), g.choice([-1, 0, 1])], float)
        for t in range(T):
            y, x = int(p[0]), int(p[1])
            clips[i, t, y:y + 12, x:x + 12] = small[j]
            for a in range(2):  # bounce
                if not 0 <= p[a] + v[a] <= room:
                    v[a] = -v[a]
            p = p + v
    return clips, lab


def clip_judge():
    import torch

    small, labels, test = small_letters()
    g = np.random.default_rng(7)
    X = np.zeros((len(small) * 4, GL, GL), np.float32)
    Y = np.repeat(labels, 4)
    for i, im in enumerate(np.repeat(small, 4, 0)):
        y, x = g.integers(0, GL - 12 + 1, 2)
        X[i, y:y + 12, x:x + 12] = im
    return train_judge(torch.tensor(X.reshape(len(X), -1)), torch.tensor(Y), n_steps=2500, seed=2)


def centers(frames):
    """Each frame's centre of brightness, (T, 2) in pixels."""
    f = np.clip(np.asarray(frames), 0, None)
    w = f.sum((-1, -2)) + 1e-9
    yy, xx = np.mgrid[:GL, :GL]
    return np.stack([(f * yy).sum((-1, -2)) / w, (f * xx).sum((-1, -2)) / w], -1)


def coherence(judge, clips, want):
    """Per clip: does every frame show the letter asked for, and how jerky is the motion (mean |second difference|)."""
    T = clips.shape[1]
    s = judge_scores(judge, clips.reshape(-1, GL, GL))
    pred, conf = s["pred"].reshape(-1, T), s["conf"].reshape(-1, T)
    right = (pred == np.asarray(want)[:, None]) & (conf > 0.5)
    c = np.stack([centers(cl) for cl in clips])
    jerk = np.abs(np.diff(c, 2, axis=1)).sum(-1).mean(1)
    return dict(all_right=float(right.all(1).mean()), frame_right=right.mean(0), jerk=float(np.median(jerk)))


class ClipNet:
    """A small diffusion transformer over (frame, patch) tokens, conditioned on the letter and on each frame's noise
    level through adaptive layer norm; attention across frames either full or causal (each frame sees itself and
    the past)."""

    def __new__(cls, T=8, D=96, L=4, H=4, causal=False):
        import torch
        import torch.nn as nn

        P, NP = 4, 25

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
                self.embed = nn.Linear(P * P, D)
                self.pos_s = nn.Parameter(torch.randn(1, 1, NP, D) * 0.02)
                self.pos_t = nn.Parameter(torch.randn(1, T, 1, D) * 0.02)
                self.freq = nn.Parameter(torch.randn(D // 2) * 4.0, requires_grad=False)
                self.tmlp = nn.Sequential(nn.Linear(D, D), nn.SiLU(), nn.Linear(D, D))
                self.lab = nn.Embedding(26, D)
                self.blocks = nn.ModuleList([Block() for _ in range(L)])
                self.nf = nn.LayerNorm(D, elementwise_affine=False)
                self.out = nn.Linear(D, P * P)
                fr = torch.arange(T).repeat_interleave(NP)
                self.register_buffer("mask", (fr[None, :] > fr[:, None]) if causal else torch.zeros(T * NP, T * NP, dtype=torch.bool))

            def forward(self, x, t, y):
                """x (B, F, 20, 20) with F <= T frames; t (B, F) each frame's noise level; y (B,) the letter."""
                B, Fr = x.shape[:2]
                p = x.reshape(B, Fr, 5, P, 5, P).permute(0, 1, 2, 4, 3, 5).reshape(B, Fr, NP, P * P)
                h = self.embed(p) + self.pos_s + self.pos_t[:, :Fr]
                a = t[..., None] * self.freq * 2 * math.pi
                c = self.tmlp(torch.cat([torch.sin(a), torch.cos(a)], -1)) + self.lab(y)[:, None]
                c = c[:, :, None].expand(B, Fr, NP, D).reshape(B, Fr * NP, D)
                h = h.reshape(B, Fr * NP, D)
                m = self.mask[:Fr * NP, :Fr * NP]
                for b in self.blocks:
                    h = b(h, c, m)
                o = self.out(self.nf(h)).reshape(B, Fr, 5, 5, P, P).permute(0, 1, 2, 4, 3, 5).reshape(B, Fr, GL, GL)
                return o

        return Net()


def train_clipnet(mode, clips, lab, n_steps, seed=0):
    """mode: 'clip' (full attention, one noise level for the clip), 'teacher' (causal; earlier frames clean, one frame
    noised, loss on it), 'forcing' (causal; every frame its own noise level, loss on all)."""
    import torch

    torch.manual_seed(seed)
    T = clips.shape[1]
    m = ClipNet(T=T, causal=mode != "clip")
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=steps(n_steps), pct_start=0.3 if QUICK else 0.05)
    X = torch.tensor(clips * 2 - 1)
    Yl = torch.tensor(lab)
    g = torch.Generator().manual_seed(seed)
    B = 24
    for _ in range(steps(n_steps)):
        i = torch.randint(0, len(X), (B,), generator=g)
        x1, y = X[i], Yl[i]
        x0 = torch.randn(x1.shape, generator=g)
        if mode == "clip":
            t = torch.rand(B, 1, generator=g).expand(B, T)
            w = torch.ones(B, T)
        elif mode == "forcing":
            t = torch.rand(B, T, generator=g)
            w = torch.ones(B, T)
        else:
            f = torch.randint(0, T, (B,), generator=g)
            ar = torch.arange(T)[None]
            t = torch.where(ar < f[:, None], torch.ones(B, T), torch.rand(B, 1, generator=g).expand(B, T))
            w = (ar == f[:, None]).float()
        xt = (1 - t[..., None, None]) * x0 + t[..., None, None] * x1
        err = ((m(xt, t, y) - (x1 - x0)) ** 2).mean((-1, -2))
        loss = (err * w).sum() / w.sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    return m


def sample_clip(m, y, T, n_steps=30, seed=0):
    import torch

    gen = torch.Generator().manual_seed(seed)
    B = len(y)
    x = torch.randn(B, T, GL, GL, generator=gen)
    yy = torch.tensor(y)
    with torch.no_grad():
        for k in range(n_steps):
            t = torch.full((B, T), k / n_steps)
            x = x + m(x, t, yy) / n_steps
    return ((x.numpy() + 1) / 2).clip(0, 1)


def rollout(m, y, n_frames, window, n_steps=24, seed=0):
    """Write frames one after another: the earlier frames (at most window - 1 of them) clean, the new one denoised."""
    import torch

    gen = torch.Generator().manual_seed(seed)
    B = len(y)
    yy = torch.tensor(y)
    done = []
    with torch.no_grad():
        for f in range(n_frames):
            ctx = done[-(window - 1):]
            new = torch.randn(B, 1, GL, GL, generator=gen)
            for k in range(n_steps):
                x = torch.cat(ctx + [new], 1)
                t = torch.cat([torch.ones(B, len(ctx)), torch.full((B, 1), k / n_steps)], 1)
                new = new + m(x, t, yy)[:, -1:] / n_steps
            done.append(new.clamp(-1, 1))
    return ((torch.cat(done, 1).numpy() + 1) / 2).clip(0, 1)


def compute_clips():
    import torch

    torch.set_num_threads(3)
    T = 8
    clips, lab = make_clips(6000 if not QUICK else 64, T, seed=0)
    test_clips, test_lab = make_clips(8, T, seed=1, split="test")
    judge = clip_judge()
    real = coherence(judge, make_clips(200, T, seed=2, split="test")[0], make_clips(200, T, seed=2, split="test")[1])
    out = dict(T=T, real_all_right=real["all_right"], real_jerk=real["jerk"], examples=test_clips[:4])
    print(f"    real clips: every frame recognized {100 * real['all_right']:.0f}%, jerk {real['jerk']:.2f}px", flush=True)
    want = np.arange(16) % 26
    # 1. the clip model, against the same model's frames taken from 8 different samples (frame by frame, independently)
    m = train_clipnet("clip", clips, lab, 3500, seed=0)
    S = sample_clip(m, want, T, seed=3)
    indep = np.stack([sample_clip(m, want, T, seed=10 + f)[:, f] for f in range(T)], 1)
    for name, c in (("joint", S), ("indep", indep)):
        r = coherence(judge, c, want)
        out[f"{name}_all_right"], out[f"{name}_jerk"], out[f"{name}_clips"] = r["all_right"], r["jerk"], c[:6]
        print(f"    {name}: every frame right {100 * r['all_right']:.0f}%, jerk {r['jerk']:.2f}px", flush=True)
    # 2. frame after frame, trained 8 frames long, rolled out to 32: teacher forcing against diffusion forcing
    long = 4 * T
    for mode in ("teacher", "forcing"):
        mm = train_clipnet(mode, clips, lab, 3500, seed=1)
        R = rollout(mm, want, long, window=T, seed=4)
        r = coherence(judge, R, want)
        out[f"{mode}_frame_right"], out[f"{mode}_jerk"], out[f"{mode}_rollout"] = r["frame_right"], r["jerk"], R[:6]
        print(f"    {mode}: recognized in the first 8 frames {100 * r['frame_right'][:T].mean():.0f}%, "
              f"in the last 8 {100 * r['frame_right'][-T:].mean():.0f}%; jerk {r['jerk']:.2f}px", flush=True)
    out["long"] = long
    return out


# ---------------------------------------------------------------------------
def compute_vae3d():
    """A causal video autoencoder: frame 0 squeezed alone, then every 4 frames into one latent frame; 4x in space."""
    import torch
    import torch.nn as nn

    torch.set_num_threads(2)
    torch.manual_seed(2024)
    T, C = 9, 4
    clips, _ = make_clips(3000 if not QUICK else 32, T, seed=5)
    test, _ = make_clips(64, T, seed=6, split="test")

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
            return torch.sigmoid(torch.cat([f0, g1, g2], 1))

    enc, dec = Enc(), Dec()
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters()], lr=2e-3)
    X = torch.tensor(clips)
    g = torch.Generator().manual_seed(0)
    for _ in range(steps(4000)):
        x = X[torch.randint(0, len(X), (32,), generator=g)]
        loss = ((dec(enc(x)) - x) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        Xt = torch.tensor(test)
        z = enc(Xt)
        rec = dec(z).numpy()
    rmse = float(np.sqrt(((rec - test) ** 2).mean()))
    per_frame = np.sqrt(((rec - test) ** 2).mean((0, 2, 3)))
    out = dict(T=T, C=C, latent_shape=list(z.shape[1:]), pixels=T * GL * GL, numbers=int(np.prod(z.shape[1:])),
               rmse=rmse, per_frame=per_frame, orig=test[:3], rec=rec[:3])
    print(f"    {T} frames x 400 pixels -> {out['numbers']} numbers ({out['pixels'] / out['numbers']:.0f}x); "
          f"rebuild error {rmse:.3f}", flush=True)
    return out
