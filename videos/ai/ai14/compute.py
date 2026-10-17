"""Precompute everything numerical in Part 14 of the AI series ("Diffusion and Flow").

    python -m videos.ai.ai14.compute              # everything missing (Part 1's books for the text model)
    python -m videos.ai.ai14.compute --force toy

Results are cached in ``.cache/ai14/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Every model here is a small network trained on this machine; the data are Part 4's "AI" points, letter images
drawn from the system's fonts, and Part 1's novels.

Items:
    toy        a denoiser (an MLP) trained on Part 4's "AI" points: the learned score field at four noise levels,
               samples by DDPM (stochastic, 200 steps) and DDIM (deterministic, 5 to 100 steps), the paths, and how
               far each set of samples is from the data
    flow       flow matching on the same points: straight-line training paths, Euler sampling with 1 to 100 steps,
               the learned paths; then reflow (a second model trained on the first one's noise-to-sample pairs), whose
               paths are straighter, so that one or two steps suffice
    guidance   a model of two letters, A and I, told which to draw (or not, one time in five): classifier-free guidance
               at weights 0, 1 and 4, how many samples land on the right letter and how spread out they are
    glyphs     a small image model: 20 x 20 pictures of capital letters from many fonts, generated from noise by flow
               matching; samples, and one sample's journey from noise
    masked     text by masked diffusion (as in LLaDA): a small two-way transformer trained to fill in masked characters
               of the novels, then writing 64 characters by unmasking a few at a time, most confident first
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai14")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai_points(n=4000, text="AI", seed=0):
    from videos.ai.ai4.compute import glyph_points

    return glyph_points(text, n, seed=seed) / 1.2  # about 4 units wide


def sw_distance(a, b, n_proj=128, seed=0):
    """Sliced Wasserstein distance between two point clouds: how far apart, on average over directions."""
    g = rng(seed)
    th = g.uniform(0, math.pi, n_proj)
    d = np.stack([np.cos(th), np.sin(th)], 1)
    m = min(len(a), len(b))
    pa = np.sort((a[:m] @ d.T), 0)
    pb = np.sort((b[:m] @ d.T), 0)
    return float(np.sqrt(((pa - pb) ** 2).mean()))


def mlp(din, dout, width=256, tdim=32):
    import torch
    import torch.nn as nn

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.freq = nn.Parameter(torch.randn(tdim // 2) * 4.0, requires_grad=False)
            self.net = nn.Sequential(nn.Linear(din + tdim, width), nn.SiLU(), nn.Linear(width, width), nn.SiLU(),
                                     nn.Linear(width, width), nn.SiLU(), nn.Linear(width, dout))

        def forward(self, x, t, extra=None):
            a = t[:, None] * self.freq[None] * 2 * math.pi
            h = torch.cat([x, torch.sin(a), torch.cos(a)] + ([extra] if extra is not None else []), 1)
            return self.net(h)

    return Net()


# ---------------------------------------------------------------------------
def vp(t):
    """The noise schedule: x_t = alpha x_0 + sigma eps, alpha = cos(pi t / 2), sigma = sin(pi t / 2)."""
    return np.cos(np.pi * t / 2), np.sin(np.pi * t / 2)


def compute_toy():
    import torch

    torch.set_num_threads(2)
    torch.manual_seed(2020)  # Ho, Jain & Abbeel, DDPM
    data = ai_points()
    X = torch.tensor(data, dtype=torch.float32)
    net = mlp(2, 2)
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, 8000)
    g = torch.Generator().manual_seed(0)
    for step in range(8000):
        x0 = X[torch.randint(0, len(X), (512,), generator=g)]
        t = torch.rand(512, generator=g) * 0.999 + 0.001
        eps = torch.randn(512, 2, generator=g)
        a, s = torch.cos(math.pi * t / 2)[:, None], torch.sin(math.pi * t / 2)[:, None]
        loss = ((net(a * x0 + s * eps, t) - eps) ** 2).mean()  # learn to guess the noise
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()

    def eps_hat(x, t):
        with torch.no_grad():
            return net(torch.tensor(x, dtype=torch.float32), torch.full((len(x),), float(t))).numpy().astype(float)

    out = {}
    # the exact density of the noised data, p_t(x), on a grid: the landscape the score climbs (a mixture of Gaussians)
    lx, ly = np.linspace(-3, 3, 61), np.linspace(-2, 2, 41)
    LX, LY = np.meshgrid(lx, ly)
    G = np.stack([LX.ravel(), LY.ravel()], 1)
    src = data[::3]
    out["land_x"], out["land_y"], out["land_ts"] = lx, ly, [1.0, 0.7, 0.5, 0.35, 0.22, 0.12]
    for t in out["land_ts"]:
        a, s = vp(t)
        var = s * s + 0.02 ** 2
        d2 = ((G[:, None, :] - a * src[None]) ** 2).sum(-1)
        dens = np.exp(-d2 / (2 * var)).mean(1) / (2 * np.pi * var)
        out[f"land{t:g}"] = dens.reshape(len(ly), len(lx))
    # the learned score, -eps / sigma, on a grid, at four noise levels
    gx, gy = np.meshgrid(np.linspace(-3, 3, 25), np.linspace(-2, 2, 17))
    grid = np.stack([gx.ravel(), gy.ravel()], 1)
    out["grid"] = grid
    out["field_ts"] = [0.8, 0.5, 0.25, 0.08]
    for t in out["field_ts"]:
        out[f"field{t:g}"] = -eps_hat(grid, t) / vp(t)[1]
    n = 1500
    gen = rng(1)
    z = gen.normal(size=(n, 2))
    # DDPM: ancestral sampling, 200 steps
    ts = np.linspace(1, 0, 201)
    x = z.copy()
    path = [x[:300].copy()]
    for i in range(200):
        t, tn = ts[i], ts[i + 1]
        a, s = vp(t)
        an, sn = vp(tn)
        e = eps_hat(x, t)
        x0 = np.clip((x - s * e) / max(a, 1e-3), -4, 4)
        # the posterior q(x_{t'} | x_t, x_0) of the forward process, its mean and variance
        a_ts = a / an
        s2_ts = s ** 2 - a_ts ** 2 * sn ** 2
        mean = (a_ts * sn ** 2 / s ** 2) * x + (an * s2_ts / s ** 2) * x0
        var = s2_ts * sn ** 2 / s ** 2
        x = mean + (math.sqrt(max(var, 0)) * gen.normal(size=x.shape) if i < 199 else 0)
        if (i + 1) % 10 == 0:
            path.append(x[:300].copy())
    out["ddpm"], out["ddpm_path"] = x, np.array(path)
    out["sw_ddpm"] = sw_distance(x, data)

    def ddim(steps, keep=False):
        ts = np.linspace(1, 0, steps + 1)
        x = z.copy()
        path = [x[:300].copy()]
        for i in range(steps):
            a, s = vp(ts[i])
            an, sn = vp(ts[i + 1])
            e = eps_hat(x, ts[i])
            x0 = np.clip((x - s * e) / max(a, 1e-3), -4, 4)  # at pure noise the clean guess is ill-posed: keep it in range
            x = an * x0 + sn * e  # deterministic: keep the same noise direction
            path.append(x[:300].copy())
        return x, np.array(path)

    out["ddim_steps"] = [5, 10, 20, 50, 100]
    for k in out["ddim_steps"]:
        xs, p = ddim(k)
        out[f"ddim{k}"] = xs[:600]
        out[f"sw_ddim{k}"] = sw_distance(xs, data)
        if k == 50:
            out["ddim_path"] = p
    out["data"] = data[:1500]
    out["sw_noise"] = sw_distance(z, data)
    out["sw_floor"] = sw_distance(ai_points(seed=7)[:n], data)  # two samples of the data itself
    print("    ddpm {:.3f}; ddim {}; noise {:.3f}; floor {:.3f}".format(
        out["sw_ddpm"], [round(out[f"sw_ddim{k}"], 3) for k in out["ddim_steps"]], out["sw_noise"], out["sw_floor"]), flush=True)
    assert out["sw_ddpm"] < 0.25 * out["sw_noise"] and out["sw_ddim50"] < 0.25 * out["sw_noise"]
    assert out["sw_ddim5"] > out["sw_ddim50"]
    return out


# ---------------------------------------------------------------------------
def compute_flow():
    import torch

    torch.set_num_threads(2)
    data = ai_points()
    X = torch.tensor(data, dtype=torch.float32)

    def train(pairs=None, seed=2022, steps=8000):
        torch.manual_seed(seed)  # Lipman et al.; Liu et al., flow matching and rectified flow
        net = mlp(2, 2)
        opt = torch.optim.Adam(net.parameters(), lr=2e-3)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
        g = torch.Generator().manual_seed(seed)
        for step in range(steps):
            if pairs is None:
                x1 = X[torch.randint(0, len(X), (512,), generator=g)]
                x0 = torch.randn(512, 2, generator=g)
            else:
                i = torch.randint(0, len(pairs[0]), (512,), generator=g)
                x0, x1 = pairs[0][i], pairs[1][i]
            t = torch.rand(512, generator=g)
            xt = (1 - t[:, None]) * x0 + t[:, None] * x1
            loss = ((net(xt, t) - (x1 - x0)) ** 2).mean()  # the velocity of the straight line from noise to data
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
        return net

    def sample(net, z, steps):
        x = torch.tensor(z, dtype=torch.float32)
        path = [x[:300].numpy().copy()]
        with torch.no_grad():
            for i in range(steps):
                t = torch.full((len(x),), i / steps)
                x = x + net(x, t) / steps
                path.append(x[:300].numpy().copy())
        return x.numpy().astype(float), np.array(path)

    out = {}
    z = rng(1).normal(size=(1500, 2))
    net = train()
    out["steps"] = [1, 2, 5, 10, 20, 100]
    for k in out["steps"]:
        xs, p = sample(net, z, k)
        out[f"fm{k}"] = xs[:600]
        out[f"sw_fm{k}"] = sw_distance(xs, data)
        if k == 100:
            out["fm_path"] = p
    # reflow: pair each noise with where the first model takes it, and learn those (straighter) paths
    zz = rng(2).normal(size=(20000, 2))
    x1, _ = sample(net, zz, 100)
    net2 = train(pairs=(torch.tensor(zz, dtype=torch.float32), torch.tensor(x1, dtype=torch.float32)), seed=2023)
    for k in out["steps"]:
        xs, p = sample(net2, z, k)
        out[f"rf{k}"] = xs[:600]
        out[f"sw_rf{k}"] = sw_distance(xs, data)
        if k == 100:
            out["rf_path"] = p

    def straightness(p):  # 1 = straight lines: the endpoint distance over the path length
        seg = np.linalg.norm(np.diff(p, axis=0), axis=-1).sum(0)
        return float((np.linalg.norm(p[-1] - p[0], axis=-1) / np.maximum(seg, 1e-9)).mean())

    out["straight_fm"], out["straight_rf"] = straightness(out["fm_path"]), straightness(out["rf_path"])
    out["sw_noise"] = sw_distance(z, data)
    print("    flow {}; reflow {}; straightness {:.3f} -> {:.3f}".format(
        [round(out[f"sw_fm{k}"], 3) for k in out["steps"]], [round(out[f"sw_rf{k}"], 3) for k in out["steps"]],
        out["straight_fm"], out["straight_rf"]), flush=True)
    assert out["straight_rf"] > out["straight_fm"]
    assert out["sw_rf1"] < out["sw_fm1"]
    return out


# ---------------------------------------------------------------------------
def compute_guidance():
    import torch

    torch.set_num_threads(2)
    A = ai_points(text="A", n=3000, seed=0) * 0.8 + np.array([-1.6, 0])
    I_ = ai_points(text="I", n=3000, seed=1) * 0.8 + np.array([1.6, 0])
    X = torch.tensor(np.concatenate([A, I_]), dtype=torch.float32)
    Y = torch.tensor([0] * len(A) + [1] * len(I_))
    torch.manual_seed(2022)  # Ho & Salimans, classifier-free guidance
    net = mlp(2, 2, tdim=32)
    net.net[0] = torch.nn.Linear(2 + 32 + 3, 256)  # + a one-hot label: A, I, or none
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, 8000)
    g = torch.Generator().manual_seed(0)
    for step in range(8000):
        i = torch.randint(0, len(X), (512,), generator=g)
        x1, y = X[i], Y[i]
        drop = torch.rand(512, generator=g) < 0.2  # one time in five, don't say which letter
        lab = torch.nn.functional.one_hot(torch.where(drop, torch.full_like(y, 2), y), 3).float()
        x0 = torch.randn(512, 2, generator=g)
        t = torch.rand(512, generator=g)
        xt = (1 - t[:, None]) * x0 + t[:, None] * x1
        loss = ((net(xt, t, lab) - (x1 - x0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()

    def sample(w, cls, z, steps=60):
        x = torch.tensor(z, dtype=torch.float32)
        c = torch.nn.functional.one_hot(torch.full((len(x),), cls), 3).float()
        u = torch.nn.functional.one_hot(torch.full((len(x),), 2), 3).float()
        with torch.no_grad():
            for k in range(steps):
                t = torch.full((len(x),), k / steps)
                vc, vu = net(x, t, c), net(x, t, u)
                x = x + (vu + w * (vc - vu)) / steps  # guidance: push past the conditional, away from the unconditional
        return x.numpy().astype(float)

    z = rng(3).normal(size=(800, 2))
    out = dict(ws=[0.0, 1.0, 4.0], A=A[:800], I=I_[:800])
    for w in out["ws"]:
        xs = sample(w, 0, z)
        out[f"w{w:g}"] = xs
        on_a = float((xs[:, 0] < 0).mean())
        spread = float(np.linalg.norm(xs[xs[:, 0] < 0] - xs[xs[:, 0] < 0].mean(0), axis=1).mean()) if on_a > 0 else 0.0
        out[f"onA{w:g}"], out[f"spread{w:g}"] = on_a, spread
        print(f"    w={w:g}: {on_a:.0%} on A, spread {spread:.3f}", flush=True)
    assert out["onA4"] >= out["onA1"] > out["onA0"] + 0.2
    assert out["spread4"] < out["spread1"]
    return out


# ---------------------------------------------------------------------------
GL = 20  # glyph images are GL x GL


def glyph_images(seed=0):
    import glob

    from PIL import Image, ImageDraw, ImageFont

    files = sorted(set(glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)))
    files = [f for f in files if "DejaVu" in f or "Liberation" in f or "Latin" in f] or files
    g = rng(seed)
    imgs, labels = [], []
    for f in files[:24]:
        try:
            font = ImageFont.truetype(f, 15)
        except Exception:
            continue
        for li, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            for _ in range(3):
                im = Image.new("L", (GL, GL), 0)
                dx, dy = g.uniform(-1.5, 1.5, 2)
                ImageDraw.Draw(im).text((GL / 2 + dx, GL / 2 + dy), ch, fill=255, font=font, anchor="mm")
                imgs.append(np.asarray(im, float) / 255.0)
                labels.append(li)
    return np.array(imgs), np.array(labels), len(files[:24])


def compute_glyphs():
    import torch

    torch.set_num_threads(2)
    imgs, labels, n_fonts = glyph_images()
    X = torch.tensor(imgs.reshape(len(imgs), -1) * 2 - 1, dtype=torch.float32)  # pixels in [-1, 1]
    torch.manual_seed(2023)
    net = mlp(GL * GL, GL * GL, width=768, tdim=64)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    steps = 12000
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    g = torch.Generator().manual_seed(0)
    for step in range(steps):
        x1 = X[torch.randint(0, len(X), (256,), generator=g)]
        x0 = torch.randn(256, GL * GL, generator=g)
        t = torch.rand(256, generator=g)
        xt = (1 - t[:, None]) * x0 + t[:, None] * x1
        loss = ((net(xt, t) - (x1 - x0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    z = torch.tensor(rng(4).normal(size=(48, GL * GL)), dtype=torch.float32)
    x = z.clone()
    journey = [x[0].numpy().copy()]
    with torch.no_grad():
        for k in range(50):
            x = x + net(x, torch.full((len(x),), k / 50)) / 50
            if (k + 1) % 5 == 0:
                journey.append(x[0].numpy().copy())
    samples = ((x.numpy() + 1) / 2).clip(0, 1).reshape(-1, GL, GL)
    # how close each sample is to its nearest training image (a check that it isn't just copying)
    flat = imgs.reshape(len(imgs), -1)
    near = np.array([np.sqrt(((flat - s.ravel()) ** 2).mean(1)).min() for s in samples])
    out = dict(samples=samples, journey=((np.array(journey) + 1) / 2).clip(0, 1).reshape(-1, GL, GL), train=imgs[::37][:48],
               n_train=len(imgs), n_fonts=n_fonts, nearest=near, loss=float(loss))
    print(f"    {len(imgs)} images from {n_fonts} fonts; nearest training image, mean distance {near.mean():.3f}", flush=True)
    assert samples.std() > 0.2  # not a grey blur
    return out


# ---------------------------------------------------------------------------
def compute_masked():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    torch.manual_seed(2025)  # Nie et al., LLaDA
    chars, enc, data = c11.corpus()
    K = len(chars)
    MASK = K  # one extra token: the blank
    T, D, L, H = 64, 128, 4, 4

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1, self.n2 = nn.LayerNorm(D), nn.LayerNorm(D)
            self.qkv = nn.Linear(D, 3 * D, bias=False)
            self.o = nn.Linear(D, D, bias=False)
            self.f1, self.f2 = nn.Linear(D, 4 * D), nn.Linear(4 * D, D)

        def forward(self, x):
            B = x.shape[0]
            q, k, v = self.qkv(self.n1(x)).view(B, T, 3, H, D // H).permute(2, 0, 3, 1, 4)
            a = F.scaled_dot_product_attention(q, k, v)  # no mask: every position sees every other
            x = x + self.o(a.transpose(1, 2).reshape(B, T, D))
            return x + self.f2(F.gelu(self.f1(self.n2(x))))

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(K + 1, D)
            self.pos = nn.Parameter(torch.randn(T, D) * 0.02)
            self.blocks = nn.ModuleList([Block() for _ in range(L)])
            self.nf = nn.LayerNorm(D)
            self.out = nn.Linear(D, K)

        def forward(self, x):
            h = self.emb(x) + self.pos[None]
            for b in self.blocks:
                h = b(h)
            return self.out(self.nf(h))

    net = Net()
    tr, va = data["train"], data["valid"]
    opt = torch.optim.AdamW(net.parameters(), lr=1e-3, weight_decay=0.1, betas=(0.9, 0.95))
    steps, B = 6000, 64
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=steps, pct_start=0.05)
    g = rng(2025)

    def masked_batch(seq, n, gen):
        st = torch.tensor(gen.integers(0, len(seq) - T, n))
        x = seq[st[:, None] + torch.arange(T)[None]]
        t = torch.tensor(gen.uniform(0.02, 1.0, n), dtype=torch.float32)
        m = torch.tensor(gen.random((n, T))) < t[:, None]
        return x, torch.where(m, torch.full_like(x, MASK), x), m, t

    curve = []
    for step in range(1, steps + 1):
        x, xm, m, t = masked_batch(tr, B, g)
        ce = F.cross_entropy(net(xm).reshape(-1, K), x.reshape(-1), reduction="none").view(B, T)
        # trained on the plain cross-entropy of the blanks: the 1/t weighting of the bound (below) multiplies the
        # loss by up to 50 at small t, too noisy for batches this small; the bound itself is what we report
        loss = (ce * m).sum() / m.sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if step % 500 == 0:
            curve.append((step, float(loss) / math.log(2)))
            print(f"    step {step}: masked cross-entropy {curve[-1][1]:.3f} bits/char", flush=True)
    # held-out: the bound, in bits per character
    with torch.no_grad():
        gv = rng(7)
        tot = 0.0
        for _ in range(20):
            x, xm, m, t = masked_batch(va, 64, gv)
            ce = F.cross_entropy(net(xm).reshape(-1, K), x.reshape(-1), reduction="none").view(64, T)
            tot += float(((ce * m).sum(1) / t).mean() / T)
        bound = tot / 20 / math.log(2)
    # writing: start from 64 blanks, and over 16 rounds reveal the characters the model is surest of
    texts = []
    with torch.no_grad():
        for seed in (1, 2, 3):
            torch.manual_seed(seed)
            x = torch.full((1, T), MASK)
            frames = ["".join("_" for _ in range(T))]
            for r in range(16):
                p = torch.softmax(net(x)[0] / 0.8, -1)
                choice = torch.multinomial(p, 1)[:, 0]
                conf = p.gather(1, choice[:, None])[:, 0]
                masked = x[0] == MASK
                conf = torch.where(masked, conf, torch.full_like(conf, -1.0))
                n_reveal = int(masked.sum()) // (16 - r)
                idx = torch.topk(conf, n_reveal).indices
                x[0, idx] = choice[idx]
                frames.append("".join("_" if int(c) == MASK else chars[int(c)] for c in x[0]))
            texts.append(frames)
    out = dict(T=T, steps=steps, batch=B, curve=np.array(curve), bound=bound, frames=texts,
               n_params=int(sum(p.numel() for p in net.parameters())))
    print(f"    held-out bound {bound:.3f} bits/char; sample: {texts[0][-1]!r}", flush=True)
    assert bound < 3.5 and "_" not in texts[0][-1]
    return out


ITEMS = {
    "toy": compute_toy,
    "flow": compute_flow,
    "guidance": compute_guidance,
    "glyphs": compute_glyphs,
    "masked": compute_masked,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
