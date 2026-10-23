"""Precompute everything numerical in Part 21 of the AI series ("Diffusion and Flow").

    python -m videos.ai.ai21.compute              # everything missing (about 2.5 CPU-hours; Part 13's characters for
                                                  # the text models, which read Part 1's books)
    python -m videos.ai.ai21.compute flow --force
    AI21_THREADS=1 python -m videos.ai.ai21.compute   # torch threads (default 2; on a busy machine 1 is often faster)
    AI21_QUICK=1 python -m videos.ai.ai21.compute     # a quick smoke test into .cache/ai21_quick (tiny budgets)

Results are cached in ``.cache/ai21/<name>.json`` (+ ``.npz``); trained weights beside them (``*.pt``, small).  Every
random choice is seeded.  The long items resume after an interruption: those made of many small trainings piece by
piece (``CACHE.partial``), the text models from checkpoints every 100 steps (``.cache/ai21/lm_*.ckpt.pt``).  Items
that need another item's trained models load (or compute) it first, so this module alone rebuilds the part.

The data: Part 5's letters "AI" as a smooth density, a mixture of 400 small Gaussians (exact.py), so that the score,
the best denoiser and flow matching's velocity are all known exactly; pictures of capital letters drawn from the
system's fonts; Part 1's thirty novels, through Part 13's characters.

Items, in order (exact.py: no network; train2d.py: small networks in the plane; discrete.py; textlm.py):
    mix         the mixture: centres, a sample, its density at six noise levels, the sampling floor
    forward     DDPM's forward chain against its closed form; the ELBO's weights
    tweedie     Tweedie's formula against brute-force posterior means (1D, 2D); the best denoiser's guesses
    sde         the reverse SDE and the probability-flow ODE with the exact score
    solvers     DDPM, Euler, DDIM, Heun, DPM-Solver-2 and DPM-Solver++(2M) with the exact denoiser, by evaluations
    schedules   log-SNR curves, training's noise levels, the terminal SNR, DDIM's step spacings
    edmtargets  EDM's preconditioning: target sizes, error amplification, the irreducible loss
    transport   optimal transport against flow matching's exact marginal flow; the marginal-field theorem checked
    discrete    masked diffusion's bound, exactly, on a tiny language (discrete.py)
    denoiser    the trained noise-guesser, three seeds: replay, denoising score matching checked, the learned score
    solvers_net the samplers with the trained network
    ablate      four noise schedules and three targets, trained at equal budgets, three seeds
    flow        flow matching, minibatch-OT pairs, reflow twice; straightness and transport cost
    fewstep     MeanFlow and shortcut models (fewstep.py)
    distill     progressive, consistency and distribution-matching distillation of the flow teacher
    guidance    classifier-free guidance, classifier guidance, autoguidance; precision and recall
    glyphs      20 x 20 letter pictures by flow matching, with a replay of training
    textlm      a masked-diffusion language model and an autoregressive one of the same size (textlm.py)
"""

from __future__ import annotations

import math
import os

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai21_quick" if os.environ.get("AI21_QUICK") == "1" else "ai21")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai_points(n=4000, text="AI", seed=0):
    from videos.ai.ai5.compute import glyph_points

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


# ---------------------------------------------------------------------------
GL = 20  # glyph images are GL x GL


def glyph_images(seed=0):
    import glob

    from PIL import Image, ImageDraw, ImageFont

    from explainer.ai.fonts import font_files

    files = font_files("**/*.ttf")
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
    """Flow matching in 400 dimensions: the letter pictures, with the samples from fixed noise at checkpoints."""
    import torch

    from videos.ai.ai21.train2d import threads

    threads()
    imgs, labels, n_fonts = glyph_images()
    X = torch.tensor(imgs.reshape(len(imgs), -1) * 2 - 1, dtype=torch.float32)  # pixels in [-1, 1]
    torch.manual_seed(2023)
    net = mlp(GL * GL, GL * GL, width=768, tdim=64)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    steps = 400 if os.environ.get("AI21_QUICK") == "1" else 12000
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    g = torch.Generator().manual_seed(0)
    zw = torch.tensor(rng(5).normal(size=(16, GL * GL)), dtype=torch.float32)
    checks = sorted({0, steps // 48, steps // 12, steps // 4, steps // 2, steps})

    def draw(z, n=50):
        x = z.clone()
        with torch.no_grad():
            for k in range(n):
                x = x + net(x, torch.full((len(x),), k / n)) / n
        return ((x.numpy() + 1) / 2).clip(0, 1).reshape(-1, GL, GL)

    snaps, curve, run = [draw(zw)], [], []
    for step in range(1, steps + 1):
        x1 = X[torch.randint(0, len(X), (256,), generator=g)]
        x0 = torch.randn(256, GL * GL, generator=g)
        t = torch.rand(256, generator=g)
        xt = (1 - t[:, None]) * x0 + t[:, None] * x1
        loss = ((net(xt, t) - (x1 - x0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if step % 100 == 0:
            curve.append((step, float(np.mean(run))))
            run = []
        if step in checks[1:]:
            snaps.append(draw(zw))
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
    # and, for scale, how far the training pictures are from their own nearest neighbours
    sub = flat[::7][:300]
    dd = np.sqrt(((sub[:, None] - flat[None]) ** 2).mean(-1))
    dd[dd < 1e-9] = np.inf
    out = dict(samples=samples, journey=((np.array(journey) + 1) / 2).clip(0, 1).reshape(-1, GL, GL), train=imgs[::37][:48],
               n_train=len(imgs), n_fonts=n_fonts, nearest=near, loss=float(loss), snaps=np.array(snaps), checks=checks,
               curve=np.array(curve), train_nearest=float(dd.min(1).mean()), steps=steps, batch=256)
    print(f"    {len(imgs)} images from {n_fonts} fonts; nearest training image, mean distance {near.mean():.3f} "
          f"(training pictures to each other: {out['train_nearest']:.3f})", flush=True)
    assert samples.std() > 0.2 or os.environ.get("AI21_QUICK") == "1"  # not a grey blur
    return out


from videos.ai.ai21 import discrete, exact, fewstep, textlm, train2d  # noqa: E402

ITEMS = {
    "mix": exact.compute_mix,
    "forward": exact.compute_forward,
    "tweedie": exact.compute_tweedie,
    "sde": exact.compute_sde,
    "solvers": exact.compute_solvers,
    "schedules": exact.compute_schedules,
    "edmtargets": exact.compute_edmtargets,
    "transport": exact.compute_transport,
    "discrete": discrete.compute_discrete,
    "denoiser": train2d.compute_denoiser,
    "solvers_net": train2d.compute_solvers_net,
    "ablate": train2d.compute_ablate,
    "flow": train2d.compute_flow,
    "fewstep": fewstep.compute_fewstep,
    "distill": train2d.compute_distill,
    "guidance": train2d.compute_guidance,
    "glyphs": compute_glyphs,
    "textlm": textlm.compute_textlm,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
