"""Lab 5: watch mass escape from three sequences of integral 1, and integrate the sawtooth series under a lid."""

from math import pi

import numpy as np
from scipy.integrate import quad
from scipy.special import sici

from videos.coursekit import labs

TITLE = "Dominated convergence: a lid is all you need"
GOAL = ("Take three sequences with integral 1 that tend to 0 at every point and measure the integral of their "
        "smallest lid; then check two sequences that do have an integrable lid, where the limit passes through the integral.")
TASKS = [
    "Add the typewriter sequence (indicators sweeping [0, 1] at widths 1, 1/2, 1/4, ...). Its integrals go to 0: does it converge at any point? Does it have a lid?",
    "Compute the two iterated integrals of (x² - y²)/(x² + y²)² over the unit square and the integral of its absolute value over [eps, 1]² as eps shrinks.",
    "Replace the lid 2 for the sawtooth by the exact envelope: the largest partial sum at each x. How close to Si(pi) does it come, and where?",
]

H = lambda n: float(np.sum(1.0 / np.arange(1, n + 1)))  # noqa: E731


def escapes(n, x):
    """The three escaping sequences at index n, on the grid x of [0, 70]."""
    return {"tall spike": n * ((x > 0) & (x <= 1 / n)), "sliding block": 1.0 * ((x >= n) & (x <= n + 1)),
            "spreading slab": ((x >= 0) & (x <= n)) / n}


def integral(y, x):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    # a grid of [0, 70], fine near 0 where the spikes live
    x = np.unique(np.concatenate([np.geomspace(1e-7, 1, 30_000), np.linspace(1, 70, 30_000)]))
    n_max = 60
    probes = np.sort(rng.uniform(0.05, 50, 6))  # random points at which to watch f_n(x) -> 0
    lids = {name: np.zeros_like(x) for name in escapes(1, x)}
    lid_int = {name: [] for name in lids}
    for n in range(1, n_max + 1):
        for name, fn in escapes(n, x).items():
            if n in (5, 60):
                assert abs(integral(fn, x) - 1) < 2e-3, "every function has integral 1"
            lids[name] = np.maximum(lids[name], fn)
            lid_int[name].append(integral(lids[name], x))
    late = escapes(4000, probes)
    assert all(np.all(v == 0) or np.all(v < 1e-3) for v in late.values()), "f_n(x) -> 0 at every probe"
    theory = {"tall spike": H(n_max), "sliding block": float(n_max), "spreading slab": H(n_max)}
    for name in lids:
        lab.row(f"{name}: ∫ f_n = 1, ∫ limit = 0", f"∫ smallest lid for n <= 60: {lid_int[name][-1]:.3f}   (theory {theory[name]:.3f})")
        assert abs(lid_int[name][-1] - theory[name]) < 0.01 * theory[name]
        assert lid_int[name][-1] > 1.5 * lid_int[name][4], "the lid's integral keeps growing: no integrable lid"

    # A sequence with a lid: (1 - x/n)^n on [0, n] lies under e^(-x), and its integrals n/(n + 1) tend to 1.
    ns = [1, 2, 5, 20, 80, 320]
    ints, l1 = [], []
    for n in ns:
        fn = lambda s, n=n: (1 - s / n) ** n if s < n else 0.0  # noqa: E731
        assert all(fn(s) <= np.exp(-s) + 1e-15 for s in rng.uniform(0, 2 * n, 200)), "under the lid"
        ints.append(quad(fn, 0, n)[0])
        l1.append(quad(lambda s: np.exp(-s) - fn(s), 0, n, limit=200)[0] + np.exp(-n))
    assert np.allclose(ints, [n / (n + 1) for n in ns], atol=1e-9) and np.allclose(l1, [1 / (n + 1) for n in ns], atol=1e-8)
    lab.row("(1 - x/n)^n under e^(-x): ∫ f_n at n = 320", f"{ints[-1]:.5f} = n/(n + 1);   ∫ |f_n - e^(-x)| = {l1[-1]:.1e}")

    # The sawtooth series on [0, 1]: partial sums never exceed Si(pi) < 2, so the constant 2 is a lid.
    grid = np.linspace(0, 1, 2001)
    k = np.arange(1, 301)
    partial = np.cumsum(np.sin(np.outer(grid, k)) / k, axis=1)
    si_pi = sici(pi)[0]
    assert 0 <= partial.max() < si_pi < 2 and partial.min() >= 0, "the lid: 0 <= s_N <= Si(pi) on [0, 1]"
    sup_err = np.abs(partial[1:, -1] - (pi - grid[1:]) / 2).max()
    kk = np.arange(1, 2_000_001)
    termwise = float(np.sum((1 - np.cos(kk)) / kk ** 2))
    lab.row("sawtooth: largest partial sum on [0, 1], N <= 300", f"{partial.max():.4f}   (Si(pi) = {si_pi:.4f} < 2)")
    lab.row("  sum of the integrals, integral of the sum", f"{termwise:.6f}   {pi / 2 - 0.25:.6f}   (sup error of s_300 near 0: {sup_err:.2f})")
    assert abs(termwise - (pi / 2 - 0.25)) < 2e-6 and sup_err > 1, "the swap holds though the convergence is not uniform"
    lab.note = ("Without an integrable lid the integral of the limit (0) is smaller than the limit of the integrals "
                "(1), as Fatou allows; under a lid the two agree, even where the convergence is not uniform.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    idx = np.arange(1, n_max + 1)
    for name, color, width in zip(lids, (labs.BLUE, labs.PURPLE, labs.GOLD), (5, 1.8, 1.4)):
        ax[0].plot(idx, lid_int[name], color=color, lw=width, alpha=0.6 if width > 2 else 1,
                   label=f"{name}: ∫ of its smallest lid")
    ax[0].plot(idx, idx / (idx + 1), color=labs.GREEN, label="(1 - x/n)ⁿ: ∫ fₙ, under the lid e⁻ˣ")
    ax[0].axhline(1, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="The escaping sequences have no integrable lid", xlabel="n", yscale="log", ylim=(0.4, 900))
    ax[0].legend(loc="upper left")
    for n, color in zip((3, 10, 40, 300), (labs.BLUE, labs.PURPLE, labs.PINK, labs.ORANGE)):
        ax[1].plot(grid, partial[:, n - 1], color=color, lw=1.2, label=f"s_N, N = {n}")
    ax[1].plot(grid[1:], (pi - grid[1:]) / 2, color=labs.INK, lw=1.6, label="(pi - x)/2")
    ax[1].axhline(2, color=labs.GOLD, lw=1.4, label="the lid 2")
    ax[1].axhline(si_pi, color=labs.GOLD, ls="--", lw=1, label="Si(pi)")
    ax[1].set(title="The sawtooth's partial sums on [0, 1], under a lid", xlabel="x", ylim=(0, 2.6))
    ax[1].legend(loc="upper right", ncols=3)
    lab.fig = fig
    return lab
