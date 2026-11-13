"""Lab 3: a fast Fourier transform against the definition, the uncertainty product of a shape, and three tones for the ear."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.dsp import fourier as F

TITLE = "Taking sound apart: the fast transform, and Gabor's limit"
GOAL = ("Check a hand-written FFT against the definition and count its multiplications; measure how long and how "
        "wide a pulse is, and see that the product never falls below 1/(4 pi).")
TASKS = [
    "Change SHAPE to 'rect'. What happens to the product, and why does it depend on the sample rate?",
    "Halve WIDTH. What happens to the duration, the bandwidth, and the product?",
    "Analyse a tone at bin 100.5 with window 'rect' and with 'hann' (F.leakage shows the lobes). How far down is the spill 5 bins away?",
]
SHAPE = "gauss"
WIDTH = 0.004      # seconds
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the fast transform is the slow one
    n = int(2 ** rng.integers(8, 12))
    x = rng.standard_normal(n)
    count = [0]
    fast, slow = F.fft(x, count), F.dft(x)
    err = float(np.abs(fast - slow).max() / np.abs(slow).max())
    lab.row("samples", f"{n}")
    lab.row("multiplications, definition", f"{n * n:,}")
    lab.row("multiplications, fast", f"{count[0]:,}   (N/2 log2 N = {n // 2 * int(math.log2(n)):,})")
    lab.row("largest difference between them", f"{err:.1e}")
    assert err < 1e-9 and count[0] == n // 2 * int(math.log2(n))

    # 2. how long, how wide
    t = (np.arange(8192) - 4096) / SR
    if SHAPE == "gauss":
        pulse = np.exp(-0.5 * (t / WIDTH) ** 2)
    elif SHAPE == "rect":
        pulse = (np.abs(t) < WIDTH).astype(float)
    else:
        m = int(2 * WIDTH * SR)
        pulse = np.zeros(8192)
        pulse[4096 - m: 4096 + m] = F.window(SHAPE, 2 * m)
    dt, df = F.spreads(pulse, SR)
    floor = 1 / (4 * math.pi)
    lab.row("shape", f"{SHAPE}, width {1000 * WIDTH:.1f} ms")
    lab.row("duration (std dev)", f"{1000 * dt:.2f} ms")
    lab.row("bandwidth (std dev)", f"{df:.1f} Hz")
    lab.row("product", f"{dt * df:.4f}   ({dt * df / floor:.2f} times 1/(4 pi) = {floor:.4f})")
    assert dt * df >= floor * 0.999, "nothing beats the limit"

    # 3. three tones on one note (Problem 3): a dull sawtooth, a bright one, a square
    f0 = 196.0
    recipes = {"sawtooth, 4 harmonics": [1 / k for k in range(1, 5)],
               "sawtooth, 16 harmonics": [1 / k for k in range(1, 17)],
               "square, 16 harmonics (odd only)": [1 / k if k % 2 else 0.0 for k in range(1, 17)]}
    names = list(recipes)
    order = rng.permutation(3)
    tones = {k: F.additive(f0, a, 1.3, SR) for k, a in recipes.items()}
    lab.audio = concat([Clip(tones[names[j]]).fade(0.01, 0.08).at_level(-18.0) for j in order], gap=0.4)
    lab.row("ear problem, the order (listen first)", "; ".join(names[j] for j in order))
    for k in names:
        lab.row(f"  brightness of the {k}", f"{F.centroid(tones[k][4800:], SR):.0f} Hz")

    fig, (a, b) = labs.figure(2)
    spec = np.abs(fast[: n // 2])
    a.plot(np.arange(n // 2), 20 * np.log10(np.maximum(spec / spec.max(), 1e-6)), color=labs.BLUE, lw=1.0)
    a.set_title("A stretch of noise, by the fast transform")
    a.set_xlabel("frequency bin")
    a.set_ylabel("level (dB)")
    widths = np.array([0.5, 1, 2, 4, 8]) * 1e-3
    prods = []
    for w in widths:
        g = np.exp(-0.5 * (t / w) ** 2)
        d1, d2 = F.spreads(g, SR)
        prods.append((1000 * d1, d2))
    prods = np.array(prods)
    b.loglog(prods[:, 0], prods[:, 1], "o-", color=labs.GOLD, label="Gaussian pulses")
    b.loglog([1000 * dt], [df], "s", color=labs.RED, label=f"this lab's {SHAPE}")
    xs = np.array([0.2, 10.0])
    b.loglog(xs, floor / (xs / 1000), "--", color=labs.BLUE, label="the limit: dt df = 1/(4 pi)")
    b.set_title("Duration against bandwidth")
    b.set_xlabel("duration (ms)")
    b.set_ylabel("bandwidth (Hz)")
    b.legend()
    lab.fig = fig
    lab.note = ("The fast transform gives the definition's numbers with N/2 log2 N multiplications instead of N squared. "
                "A pulse cannot be both short and narrow in frequency: a Gaussian sits exactly on Gabor's limit.")
    return lab
