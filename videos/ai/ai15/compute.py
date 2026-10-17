"""Precompute everything numerical in Part 15 of the AI series ("Images and Video").

    python -m videos.ai.ai15.compute              # everything missing
    python -m videos.ai.ai15.compute --force dit

Results are cached in ``.cache/ai15/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

The pictures are Part 14's: 20 x 20 capital letters drawn from the system's fonts. Every model is trained here.

Items:
    vit        a small vision transformer reading 4 x 4 patches (25 tokens and a summary token) to name the letter:
               accuracy on fonts it never saw, where the summary token looks, and how its learned position vectors
               resemble each other (they rediscover the 2D grid)
    latent     an autoencoder squeezing each picture into 16 numbers and back; flow matching in those 16 numbers, decoded
    dit        a diffusion transformer: the same patches as tokens, the noise level and the letter fed in by adaptive
               layer norm, trained by flow matching; the whole alphabet drawn on request, with guidance
    scales     next-scale prediction's view of a picture: the same letter at 1, 2, 4, 5, 10 and 20 pixels a side, and
               what each scale adds to the one before
    video      the token arithmetic of a video model with a typical compression (8x in space, 4x in time, 2 x 2
               patches): tokens for clips of different lengths and sizes
    vae        (deep.py) an autoencoder against variational ones with a growing KL weight: rebuild error, KL, and the
               quality of flow-matching samples in each latent space (scored by a judge classifier); uniform against
               logit-normal noise levels in training, sampled with 1 to 40 steps
    var        (deep.py) next-scale prediction's tokens: residuals at 1, 2, 4, 5, 10 and 20 pixels a side, each
               quantized to 16 levels; rebuild error after each scale
    vae3d      (deep.py) a causal video autoencoder on clips of a bouncing letter: 9 frames into 3 latent frames
    clips      (deep.py) a clip model against frames drawn independently; frame-by-frame models trained with teacher
               forcing or diffusion forcing, rolled out 4x longer than trained
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai15")
load = CACHE.load
P, GL = 4, 20  # patch size, picture size
NP = (GL // P) ** 2


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def dataset():
    """Part 14's letter pictures, split by font: the last fonts are kept for testing."""
    from videos.ai.ai14.compute import glyph_images

    imgs, labels, _ = glyph_images()
    per_font = 26 * 3
    n_fonts = len(imgs) // per_font  # the fonts that actually loaded
    font = np.arange(len(imgs)) // per_font
    test = font >= n_fonts - 4
    return imgs, labels, test, n_fonts


def patches(x):
    """(B, 20, 20) -> (B, 25, 16): the picture cut into 4 x 4 patches, row by row."""
    B = x.shape[0]
    return x.reshape(B, GL // P, P, GL // P, P).transpose(0, 1, 3, 2, 4).reshape(B, NP, P * P) if isinstance(x, np.ndarray) \
        else x.reshape(B, GL // P, P, GL // P, P).permute(0, 1, 3, 2, 4).reshape(B, NP, P * P)


def unpatch(t):
    B = t.shape[0]
    return t.reshape(B, GL // P, GL // P, P, P).permute(0, 1, 3, 2, 4).reshape(B, GL, GL)


# ---------------------------------------------------------------------------
def compute_vit():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.set_num_threads(2)
    torch.manual_seed(2020)  # Dosovitskiy et al., An Image Is Worth 16x16 Words
    imgs, labels, test, n_fonts = dataset()
    X = torch.tensor(imgs, dtype=torch.float32)
    Y = torch.tensor(labels)
    D, H, L = 64, 4, 3

    class ViT(nn.Module):
        def __init__(self):
            super().__init__()
            self.embed = nn.Linear(P * P, D)
            self.cls = nn.Parameter(torch.zeros(1, 1, D))
            self.pos = nn.Parameter(torch.zeros(1, NP + 1, D))  # from zero, so what we see later is all learned
            self.layers = nn.ModuleList([nn.TransformerEncoderLayer(D, H, 4 * D, dropout=0.0, batch_first=True, norm_first=True)
                                         for _ in range(L)])
            self.head = nn.Linear(D, 26)

        def forward(self, x, keep=False):
            h = torch.cat([self.cls.expand(len(x), -1, -1), self.embed(patches(x))], 1) + self.pos
            maps = []
            for lyr in self.layers:
                if keep:
                    a = lyr.norm1(h)
                    _, w = lyr.self_attn(a, a, a, need_weights=True, average_attn_weights=True)
                    maps.append(w)
                h = lyr(h)
            return (self.head(h[:, 0]), maps) if keep else self.head(h[:, 0])

    m = ViT()
    opt = torch.optim.AdamW(m.parameters(), lr=2e-3, weight_decay=0.05)
    tr_idx = torch.tensor(np.where(~test)[0])
    te_idx = torch.tensor(np.where(test)[0])
    g = torch.Generator().manual_seed(0)
    steps = 4000
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=2e-3, total_steps=steps, pct_start=0.1)
    for step in range(steps):
        i = tr_idx[torch.randint(0, len(tr_idx), (128,), generator=g)]
        x = X[i] + 0.05 * torch.randn(len(i), GL, GL, generator=g)
        sh = torch.randint(-2, 3, (2,), generator=g)  # nudge the letters about: where a stroke is now matters
        x = torch.roll(x, shifts=(int(sh[0]), int(sh[1])), dims=(1, 2))
        loss = F.cross_entropy(m(x), Y[i])
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    with torch.no_grad():
        acc = float((m(X[te_idx]).argmax(1) == Y[te_idx]).float().mean())
        ex = te_idx[[0, 3 * 4, 3 * 8, 3 * 16]]  # A, E, I, Q from an unseen font
        _, maps = m(X[ex], keep=True)
        cls_att = maps[-1][:, 0, 1:].reshape(-1, GL // P, GL // P).numpy()
        pe = m.pos[0, 1:].numpy()
    pe = pe - pe.mean(0)  # what sets each position apart from the rest
    pe = pe / np.linalg.norm(pe, axis=1, keepdims=True)
    sim = pe @ pe.T  # each position's similarity to every other: (25, 25)
    # neighbours in the grid should be more alike than far-apart positions
    r, c = np.divmod(np.arange(NP), GL // P)
    dist = np.abs(r[:, None] - r[None]) + np.abs(c[:, None] - c[None])
    near, far = sim[dist == 1].mean(), sim[dist >= 4].mean()
    out = dict(acc=acc, n_test_fonts=4, n_fonts=n_fonts, cls_att=cls_att, ex_imgs=imgs[ex.numpy()], ex_labels=labels[ex.numpy()],
               pos_sim=sim, near=float(near), far=float(far), n_params=int(sum(p.numel() for p in m.parameters())))
    print(f"    accuracy on unseen fonts {acc:.1%}; position similarity: neighbours {near:.2f}, far {far:.2f}", flush=True)
    assert acc > 0.7  # the scene says whether the position vectors learned the grid (near vs far)
    return out


# ---------------------------------------------------------------------------
def compute_latent():
    import torch
    import torch.nn as nn

    from videos.ai.ai14.compute import mlp

    torch.set_num_threads(2)
    torch.manual_seed(2022)  # Rombach et al., latent diffusion
    imgs, labels, test, _ = dataset()
    X = torch.tensor(imgs.reshape(len(imgs), -1), dtype=torch.float32)
    Z = 16
    enc = nn.Sequential(nn.Linear(GL * GL, 256), nn.SiLU(), nn.Linear(256, 128), nn.SiLU(), nn.Linear(128, Z))
    dec = nn.Sequential(nn.Linear(Z, 128), nn.SiLU(), nn.Linear(128, 256), nn.SiLU(), nn.Linear(256, GL * GL))
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters()], lr=2e-3)
    g = torch.Generator().manual_seed(0)
    for step in range(6000):
        x = X[torch.randint(0, len(X), (256,), generator=g)]
        z = enc(x)
        loss = ((torch.sigmoid(dec(z)) - x) ** 2).mean() + 1e-4 * (z ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        Zs = enc(X)
        mu, sd = Zs.mean(0), Zs.std(0)
        Zn = (Zs - mu) / sd
        rec = torch.sigmoid(dec(Zs)).numpy().reshape(-1, GL, GL)
        rec_err = float(np.sqrt(((rec - imgs) ** 2).mean()))
    # flow matching in the 16 numbers
    net = mlp(Z, Z, width=256)
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    for step in range(6000):
        z1 = Zn[torch.randint(0, len(Zn), (512,), generator=g)]
        z0 = torch.randn(512, Z, generator=g)
        t = torch.rand(512, generator=g)
        zt = (1 - t[:, None]) * z0 + t[:, None] * z1
        loss = ((net(zt, t) - (z1 - z0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        z = torch.tensor(rng(5).normal(size=(32, Z)), dtype=torch.float32)
        for k in range(40):
            z = z + net(z, torch.full((32,), k / 40)) / 40
        samples = torch.sigmoid(dec(z * sd + mu)).numpy().reshape(-1, GL, GL)
    u, s_, vt = np.linalg.svd(Zn.numpy() - Zn.numpy().mean(0), full_matrices=False)
    xy = (Zn.numpy() @ vt[:2].T)[::5]
    # neighbours in the 16 numbers: for every picture, its 6 nearest others; how often they are the same letter
    Zq = Zn.numpy()
    d2 = (Zq ** 2).sum(1)[:, None] + (Zq ** 2).sum(1)[None] - 2 * Zq @ Zq.T
    np.fill_diagonal(d2, np.inf)
    nn6 = np.argsort(d2, 1)[:, :6]
    same = float((labels[nn6] == labels[:, None]).mean())
    chance = float(np.mean([(labels == l_).sum() - 1 for l_ in labels]) / (len(labels) - 1))
    queries = [int(np.where(labels == L_)[0][len(np.where(labels == L_)[0]) // 2]) for L_ in (0, 6, 14, 18)]  # A G O S
    out = dict(Z=Z, ratio=GL * GL / Z, rec=rec[::97][:12], orig=imgs[::97][:12], rec_err=rec_err, samples=samples,
               xy=xy, xy_labels=labels[::5], nn_same=same, nn_chance=chance, nn_query=imgs[queries],
               nn_imgs=imgs[nn6[queries]], nn_labels=labels[nn6[queries]], nn_qlabels=labels[queries])
    print(f"    nearest 6 in the 16 numbers: same letter {same:.0%} (chance {chance:.0%})", flush=True)
    print(f"    {GL * GL} -> {Z} numbers; reconstruction error {rec_err:.3f}", flush=True)
    assert rec_err < 0.2 and samples.std() > 0.2
    return out


# ---------------------------------------------------------------------------
def compute_dit():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.set_num_threads(3)
    torch.manual_seed(2023)  # Peebles & Xie, Scalable Diffusion Models with Transformers
    imgs, labels, test, _ = dataset()
    X = torch.tensor(imgs * 2 - 1, dtype=torch.float32)
    Y = torch.tensor(labels)
    D, H, L = 128, 4, 4

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1 = nn.LayerNorm(D, elementwise_affine=False)
            self.n2 = nn.LayerNorm(D, elementwise_affine=False)
            self.att = nn.MultiheadAttention(D, H, batch_first=True)
            self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
            self.ada = nn.Linear(D, 6 * D)  # adaptive layer norm: shift, scale and gate, from the condition
            nn.init.zeros_(self.ada.weight)
            nn.init.zeros_(self.ada.bias)

        def forward(self, h, c):
            s1, b1, g1, s2, b2, g2 = self.ada(c)[:, None].chunk(6, -1)
            a = self.n1(h) * (1 + s1) + b1
            h = h + g1 * self.att(a, a, a, need_weights=False)[0]
            return h + g2 * self.mlp(self.n2(h) * (1 + s2) + b2)

    class DiT(nn.Module):
        def __init__(self):
            super().__init__()
            self.embed = nn.Linear(P * P, D)
            self.pos = nn.Parameter(torch.randn(1, NP, D) * 0.02)
            self.freq = nn.Parameter(torch.randn(D // 2) * 4.0, requires_grad=False)
            self.tmlp = nn.Sequential(nn.Linear(D, D), nn.SiLU(), nn.Linear(D, D))
            self.lab = nn.Embedding(27, D)  # 26 letters, and "no letter"
            self.blocks = nn.ModuleList([Block() for _ in range(L)])
            self.nf = nn.LayerNorm(D, elementwise_affine=False)
            self.out = nn.Linear(D, P * P)

        def forward(self, x, t, y):
            a = t[:, None] * self.freq[None] * 2 * math.pi
            c = self.tmlp(torch.cat([torch.sin(a), torch.cos(a)], 1)) + self.lab(y)
            h = self.embed(patches(x)) + self.pos
            for b in self.blocks:
                h = b(h, c)
            return unpatch(self.out(self.nf(h)))

    m = DiT()
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.0)
    steps = 6000
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=steps, pct_start=0.05)
    g = torch.Generator().manual_seed(0)
    # how it learns: the same noise and the same requests (A to J), drawn at checkpoints along the way
    snap_at = [0, 150, 400, 1000, 2000, 4000, steps]
    snaps, losses, run = [], [], []
    z_snap = torch.randn(10, GL, GL, generator=torch.Generator().manual_seed(11))

    def snapshot():
        m.eval()
        x = z_snap.clone()
        y_ = torch.arange(10)
        with torch.no_grad():
            for k in range(20):
                t = torch.full((10,), k / 20)
                vc, vu = m(x, t, y_), m(x, t, torch.full_like(y_, 26))
                x = x + (vu + 2.0 * (vc - vu)) / 20
        m.train()
        return ((x.numpy() + 1) / 2).clip(0, 1)

    snaps.append(snapshot())
    for step in range(1, steps + 1):
        i = torch.randint(0, len(X), (128,), generator=g)
        x1, y = X[i], Y[i]
        y = torch.where(torch.rand(128, generator=g) < 0.15, torch.full_like(y, 26), y)
        x0 = torch.randn(128, GL, GL, generator=g)
        t = torch.rand(128, generator=g)
        xt = (1 - t[:, None, None]) * x0 + t[:, None, None] * x1
        loss = ((m(xt, t, y) - (x1 - x0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if step % 50 == 0:
            losses.append((step, float(np.mean(run))))
            run = []
        if step in snap_at:
            snaps.append(snapshot())
        if step % 1000 == 0:
            print(f"    step {step}: loss {float(loss):.4f}", flush=True)
    m.eval()

    def draw(letters, w=2.0, steps=40, seed=0, path=None):
        gen = torch.Generator().manual_seed(seed)
        x = torch.randn(len(letters), GL, GL, generator=gen)
        y = torch.tensor(letters)
        u = torch.full_like(y, 26)
        with torch.no_grad():
            for k in range(steps):
                if path is not None and k % 4 == 0:
                    path.append(((x.numpy() + 1) / 2).clip(0, 1))
                t = torch.full((len(x),), k / steps)
                vc, vu = m(x, t, y), m(x, t, u)
                x = x + (vu + w * (vc - vu)) / steps
        if path is not None:
            path.append(((x.numpy() + 1) / 2).clip(0, 1))
        return ((x.numpy() + 1) / 2).clip(0, 1)

    frames = []
    alphabet = draw(list(range(26)) * 2, seed=1, path=frames)
    out = dict(alphabet_path=np.array(frames)[:, :26], alphabet=alphabet, n_params=int(sum(p.numel() for p in m.parameters())), steps=steps, D=D, L=L)
    a_only = draw([0] * 8, w=2.0, seed=3)
    out["many_a"] = a_only
    out["snap_steps"], out["snaps"], out["losses"] = snap_at, np.array(snaps), np.array(losses)
    print(f"    {out['n_params']:,} parameters", flush=True)
    assert alphabet.std() > 0.2
    return out


# ---------------------------------------------------------------------------
def compute_scales():
    imgs, labels, test, _ = dataset()
    im = imgs[labels == 0][5]  # an A
    sizes = [1, 2, 4, 5, 10, 20]
    pyr, residuals = [], []
    prev = np.zeros_like(im)
    for s in sizes:
        k = GL // s
        small = im.reshape(s, k, s, k).mean((1, 3))
        up = np.kron(small, np.ones((k, k)))
        pyr.append(up)
        residuals.append(up - prev)
        prev = up
    assert np.allclose(pyr[-1], im)
    return dict(sizes=sizes, pyramid=np.array(pyr), residuals=np.array(residuals), image=im)


# ---------------------------------------------------------------------------
def compute_video():
    fps, sec = 16, [2, 5, 10]
    rows = []
    for (w, h, name) in ((640, 360, "360p"), (1280, 720, "720p"), (1920, 1080, "1080p")):
        for s in sec:
            frames = fps * s
            lat_t = frames // 4 + 1  # 4x in time (the first frame kept on its own)
            tok = lat_t * (h // 8 // 2) * (w // 8 // 2)
            rows.append(dict(res=name, sec=s, frames=frames, tokens=int(tok), pixels=int(frames * w * h)))
    t720 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 5)
    assert 50_000 < t720["tokens"] < 100_000
    return dict(rows=rows, fps=fps)


from videos.ai.ai15.deep import compute_clips, compute_vae, compute_vae3d, compute_var  # noqa: E402

ITEMS = {
    "vit": compute_vit,
    "latent": compute_latent,
    "dit": compute_dit,
    "scales": compute_scales,
    "video": compute_video,
    "vae": compute_vae,
    "var": compute_var,
    "vae3d": compute_vae3d,
    "clips": compute_clips,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
