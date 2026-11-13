"""Lab 3: look at the sawtooth's Fourier series through four lenses: sup error, mean-square error, Gibbs, Fejér."""

from math import pi

import numpy as np
from scipy.special import sici

from videos.coursekit import labs

TITLE = "The sawtooth under four lenses"
GOAL = ("Sum sin(kx)/k toward (pi - x)/2 on (0, 2 pi) and measure the convergence four ways: the sup error (it does "
        "not shrink), the mean-square error (exactly the tail of 1/k²), the Gibbs overshoot, and the best-approximation property.")
TASKS = [
    "Replace the sawtooth by the triangle wave |x| on [-pi, pi]. Show that its sup error now goes to 0, and at what rate.",
    "Replace the partial sums by Fejér means in the mean-square table. Are they better or worse than s_N in that lens, and why must they be?",
    "Measure the L1 norm of the Dirichlet kernel for N up to 500 and fit it against (4/pi²) ln N.",
]


def partial_sum(x, n):
    k = np.arange(1, n + 1)
    return (np.sin(np.outer(x, k)) / k).sum(axis=1)


def fejer(x, n):
    k = np.arange(1, n + 1)
    return (np.sin(np.outer(x, k)) / k * (1 - k / (n + 1))).sum(axis=1)


def integral(y, x):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    x = np.linspace(0, 2 * pi, 20_001)
    f = (pi - x) / 2  # the one-sided values at the two ends, where every partial sum is 0
    si_pi = sici(pi)[0]
    gibbs = si_pi / pi - 0.5

    energy = integral(f * f, x) / pi
    lab.row("Parseval: (1/pi) ∫ f²", f"{energy:.6f}   (pi²/6 = {pi * pi / 6:.6f})")
    assert abs(energy - pi * pi / 6) < 1e-6

    ns = [4, 16, 64, 256]
    sup, mse, tail, over, fej_max, fej_far = [], [], [], [], [], []
    for n in ns:
        s = partial_sum(x, n)
        sup.append(np.abs(s - f)[1:-1].max())
        mse.append(integral((s - f) ** 2, x) / pi)
        tail.append(pi * pi / 6 - np.sum(1.0 / np.arange(1, n + 1) ** 2))
        near = np.linspace(0, 3 * pi / (n + 1), 2001)[1:]  # the first peak sits at pi / (n + 1)
        over.append((partial_sum(near, n) - (pi - near) / 2).max() / pi)
        sg = fejer(x, n)
        fej_max.append(sg.max())
        far = (x > 0.5) & (x < 2 * pi - 0.5)
        fej_far.append(np.abs(sg - f)[far].max())
        lab.row(f"N = {n:>3}: sup error, mean-square error", f"{sup[-1]:.3f}   {mse[-1]:.5f}   (tail of 1/k²: {tail[-1]:.5f})")
    assert all(e > 1.4 for e in sup), "no uniform convergence: the sup error stays near pi/2"
    assert np.allclose(mse, tail, rtol=2e-3), "the missing energy is exactly the tail"
    lab.row("largest s_N - f near the jump, over the jump", "   ".join(f"{o:.4f}" for o in over) + f"   (Si(pi)/pi - 1/2 = {gibbs:.4f})")
    assert abs(over[-1] - gibbs) < 1e-3 and all(o > 0.08 for o in over), "Gibbs: the overshoot does not shrink"
    lab.row("largest value of the Fejér mean", "   ".join(f"{m:.4f}" for m in fej_max) + f"   (sup f = pi/2 = {pi / 2:.4f})")
    assert all(m < pi / 2 for m in fej_max), "Fejér's kernel is nonnegative: no overshoot"
    assert fej_far[-1] < 0.02 and fej_far[-1] < fej_far[0], "Fejér means converge uniformly away from the jump"

    # Best approximation: among trigonometric polynomials of degree 8, the Fourier partial sum has the least error.
    n, trials = 8, 500
    k = np.arange(1, n + 1)
    xs = x[::10]
    fs, s8 = f[::10], partial_sum(x[::10], n)
    basis = np.hstack([np.ones((xs.size, 1)), np.cos(np.outer(xs, k)), np.sin(np.outer(xs, k))])
    base = integral((fs - s8) ** 2, xs)
    worst_gap, pyth = np.inf, 0.0
    for _ in range(trials):
        d = basis @ (rng.normal(0, 0.15, 2 * n + 1))
        err = integral((fs - s8 - d) ** 2, xs)
        worst_gap = min(worst_gap, err - base)
        pyth = max(pyth, abs(err - base - integral(d * d, xs)))
    lab.row("degree 8: error of s_8, least error of 500 rivals", f"{base:.4f}   {base + worst_gap:.4f}")
    lab.row("Pythagoras: largest |err - (best + distance²)|", f"{pyth:.1e}")
    assert worst_gap > 0 and pyth < 1e-3
    lab.note = ("The series converges to the sawtooth in mean square, with the missing energy equal to the tail of "
                "1/k², but not uniformly: the overshoot stays at 8.95% of the jump. Averaging (Fejér) removes the overshoot.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    z = np.linspace(0, 0.9, 1500)
    ax[0].plot(z, (pi - z) / 2, color=labs.INK, lw=2, label="the sawtooth")
    for n, color in zip((16, 64, 256), (labs.BLUE, labs.PURPLE, labs.PINK)):
        ax[0].plot(z, partial_sum(z, n), color=color, lw=1.2, label=f"s_N, N = {n}")
    ax[0].plot(z, fejer(z, 64), color=labs.GREEN, lw=1.4, label="Fejér mean, N = 64")
    ax[0].axhline(si_pi, color=labs.GOLD, ls="--", lw=1, label="Si(pi) = 1.8519")
    ax[0].set(title="Near the jump: the peak moves in, its height stays", xlabel="x", ylim=(0.65, 2.0))
    ax[0].legend(loc="lower right", ncols=2)
    ax[1].loglog(ns, sup, "o-", color=labs.PINK, label="sup error of s_N")
    ax[1].loglog(ns, np.sqrt(mse), "o-", color=labs.BLUE, label="root-mean-square error of s_N")
    ax[1].loglog(ns, np.sqrt(tail), "--", color=labs.GOLD, label="square root of the tail of 1/k²")
    ax[1].loglog(ns, fej_far, "o-", color=labs.GREEN, label="sup error of Fejér, 0.5 away from the jump")
    ax[1].set(title="Two lenses, two verdicts", xlabel="N", ylim=(3e-3, 20))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
