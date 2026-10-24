"""Shared pieces of Part 22's computations: the cache, the letter pictures, the judge. See compute.py."""

from __future__ import annotations

import math
import os

import numpy as np

from explainer.ai.cache import Cache

QUICK = os.environ.get("AI22_QUICK") == "1"
CACHE = Cache("ai22_quick" if QUICK else "ai22")
load = CACHE.load
P, GL = 4, 20  # patch size, picture size
NP = (GL // P) ** 2
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def steps(n: int) -> int:
    """A training budget, cut to almost nothing for the smoke test."""
    return max(50, n // 100) if QUICK else n


def threads():
    import torch

    torch.set_num_threads(int(os.environ.get("AI22_THREADS", "1")))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def dataset():
    """Part 21's letter pictures, split by font: the last four fonts are kept for testing.
    Returns (images (N, 20, 20) in [0, 1], labels, test mask, number of fonts, font index of each picture)."""
    from videos.ai.ai21.compute import glyph_images

    imgs, labels, _ = glyph_images()
    per_font = 26 * 3
    n_fonts = len(imgs) // per_font  # the fonts that actually loaded
    font = np.arange(len(imgs)) // per_font
    test = font >= n_fonts - 4
    return imgs, labels, test, n_fonts, font


def font_files() -> list[str]:
    """The font files behind ``dataset()``'s pictures, in the same order (Part 21's choice of fonts)."""
    from PIL import ImageFont

    from explainer.ai.fonts import font_files as ff

    files = ff("**/*.ttf")
    files = [f for f in files if "DejaVu" in f or "Liberation" in f or "Latin" in f] or files
    out = []
    for f in files[:24]:
        try:
            ImageFont.truetype(f, 15)
        except Exception:
            continue
        out.append(f)
    return out


def render(font_file: str, ch: str, size: int = GL, dx=0.0, dy=0.0) -> np.ndarray:
    """One letter drawn as Part 21 draws them (font size 15 on 20 pixels), at any size: 40 pixels uses size 30."""
    from PIL import Image, ImageDraw, ImageFont

    k = size / GL
    font = ImageFont.truetype(font_file, int(round(15 * k)))
    im = Image.new("L", (size, size), 0)
    ImageDraw.Draw(im).text((size / 2 + dx * k, size / 2 + dy * k), ch, fill=255, font=font, anchor="mm")
    return np.asarray(im, float) / 255.0


def patches(x):
    """(B, 20, 20) -> (B, 25, 16): the picture cut into 4 x 4 patches, row by row."""
    B = x.shape[0]
    if isinstance(x, np.ndarray):
        return x.reshape(B, GL // P, P, GL // P, P).transpose(0, 1, 3, 2, 4).reshape(B, NP, P * P)
    return x.reshape(B, GL // P, P, GL // P, P).permute(0, 1, 3, 2, 4).reshape(B, NP, P * P)


def unpatch(t):
    B = t.shape[0]
    return t.reshape(B, GL // P, GL // P, P, P).permute(0, 1, 3, 2, 4).reshape(B, GL, GL)


# ---------------------------------------------------------------------------
# The judge: a small CNN that reads letters, and scores generated pictures
# ---------------------------------------------------------------------------
def judge_net():
    import torch.nn as nn

    class Judge(nn.Module):
        def __init__(self):
            super().__init__()
            self.body = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.Conv2d(32, 64, 3, 2, 1), nn.ReLU(),
                                      nn.Conv2d(64, 64, 3, 2, 1), nn.ReLU(), nn.Flatten(), nn.Linear(1600, 128), nn.ReLU())
            self.head = nn.Linear(128, 26)

        def features(self, x):
            return self.body(x.reshape(-1, 1, GL, GL))

        def forward(self, x):
            return self.head(self.features(x))

    return Judge()


def train_judge(X, Y, n_steps, seed, shift=2):
    """X (N, 20, 20) float tensor in [0, 1]; random shifts of up to ``shift`` pixels and a little noise."""
    import torch
    import torch.nn.functional as F

    torch.manual_seed(seed)
    net = judge_net()
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    torch.set_grad_enabled(True)
    g = torch.Generator().manual_seed(seed)
    for _ in range(steps(n_steps)):
        i = torch.randint(0, len(X), (128,), generator=g)
        x = X[i]
        if shift:
            s = torch.randint(-shift, shift + 1, (2,), generator=g)
            x = torch.roll(x, (int(s[0]), int(s[1])), (1, 2))
        x = x + 0.06 * torch.randn(x.shape, generator=g)
        loss = F.cross_entropy(net(x), Y[i])
        opt.zero_grad()
        loss.backward()
        opt.step()
    net.eval()
    return net


def compute_judge():
    import torch

    threads()
    imgs, labels, test, _, _ = dataset()
    X = torch.tensor(imgs[~test], dtype=torch.float32)
    net = train_judge(X, torch.tensor(labels[~test]), 3000, seed=26)
    torch.save(net.state_dict(), CACHE.dir / "judge.pt")
    with torch.no_grad():
        acc = float((net(torch.tensor(imgs[test], dtype=torch.float32)).argmax(1).numpy() == labels[test]).mean())
        f = net.features(torch.tensor(imgs, dtype=torch.float32)).numpy()
    # the floor of the Frechet distance: real held-out fonts against the training fonts' statistics
    floor = frechet(f[test], f[~test])
    print(f"    judge: {100 * acc:.1f}% right on held-out fonts; FD(held-out fonts, training fonts) {floor:.2f}", flush=True)
    return dict(acc=acc, fd_floor=floor, n_train=int((~test).sum()))


_JUDGE = {}


def judge():
    """The trained judge (computed and cached on first use)."""
    import torch

    if "net" not in _JUDGE:
        if not (CACHE.dir / "judge.pt").exists() or not CACHE.path("judge").exists():
            CACHE.save("judge", compute_judge())
        net = judge_net()
        net.load_state_dict(torch.load(CACHE.dir / "judge.pt"))
        net.eval()
        imgs, labels, test, _, _ = dataset()
        with torch.no_grad():
            f = net.features(torch.tensor(imgs[~test], dtype=torch.float32)).numpy().astype(np.float64)
        _JUDGE.update(net=net, mu=f.mean(0), cov=np.cov(f, rowvar=False))
    return _JUDGE


def frechet(a, b) -> float:
    """Frechet distance between Gaussians fitted to two sets of features (FID's formula, on the judge's features)."""
    from scipy import linalg

    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    m1, m2 = a.mean(0), b.mean(0)
    c1, c2 = np.cov(a, rowvar=False), np.cov(b, rowvar=False)
    s = linalg.sqrtm(c1 @ c2)
    return float(((m1 - m2) ** 2).sum() + np.trace(c1 + c2 - 2 * np.real(s)))


def score(imgs01, want=None) -> dict:
    """How the judge reads generated pictures: the share it reads as the requested letter (or, without requests, the
    share it reads with confidence above 0.8), how many letters appear, and the Frechet distance of its features to
    the training fonts' pictures."""
    import torch
    from scipy import linalg

    J = judge()
    x = torch.tensor(np.clip(np.asarray(imgs01, np.float32), 0, 1).reshape(-1, GL, GL))
    with torch.no_grad():
        f = J["net"].features(x)
        p = torch.softmax(J["net"].head(f), 1).numpy()
    f = f.numpy().astype(np.float64)
    pred, conf = p.argmax(1), p.max(1)
    c1 = np.cov(f, rowvar=False)
    s = linalg.sqrtm(c1 @ J["cov"])
    fd = float(((f.mean(0) - J["mu"]) ** 2).sum() + np.trace(c1 + J["cov"] - 2 * np.real(s)))
    out = dict(fd=fd, clear=float((conf > 0.8).mean()), letters=int(len(set(pred[conf > 0.8].tolist()))))
    if want is not None:
        out["acc"] = float((pred == np.asarray(want)).mean())
    return out


# ---------------------------------------------------------------------------
def compute_video():
    """The token arithmetic of a video model with a typical squeeze (4x in time, the first frame alone; 8x in space;
    2 x 2 patches): tokens and attention pairs for clips of different lengths and sizes."""
    fps, sec = 16, [2, 5, 10]
    rows = []
    for (w, h, name) in ((640, 360, "360p"), (1280, 720, "720p"), (1920, 1080, "1080p")):
        for s in sec:
            frames = fps * s
            lat_t = frames // 4 + 1
            tok = lat_t * (h // 8 // 2) * (w // 8 // 2)
            rows.append(dict(res=name, sec=s, frames=frames, lat_t=lat_t, tokens=int(tok), pixels=int(frames * w * h * 3)))
    t720 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 5)
    assert 50_000 < t720["tokens"] < 100_000
    return dict(rows=rows, fps=fps)
