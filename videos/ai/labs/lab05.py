"""Lab 5: run an Ornstein-Uhlenbeck process three ways: particles, the Fokker-Planck equation on a grid, the formula."""

import numpy as np
from scipy import stats

from videos.coursekit import labs

TITLE = "Particles against their density's own law"
GOAL = ("Simulate dx = -x dt + sqrt(2) dW from x = 2 with the Euler-Maruyama scheme, solve the Fokker-Planck "
        "equation for the same process on a grid, and compare both with the exact Gaussian solution; then take "
        "steps that are too large and predict the bias they cause.")
TASKS = [
    "Replace the drift -x by the score of a two-bump density (the sum of two Gaussians): Langevin dynamics. Does "
    "the histogram reach both bumps, and how long does it take?",
    "Halve dt four times and plot the error of the variance at t = 1 against dt on log axes. What is the slope, "
    "and which order of convergence (strong or weak) is it?",
    "Run the process backwards from t = 3 with Anderson's reverse-time SDE, using the exact score of the "
    "Gaussian at each time, and check that the particles return to a tight cloud around x = 2.",
]
THETA, SIGMA, X0 = 1.0, np.sqrt(2.0), 2.0


def exact(t):
    """Mean and variance of x_t: the solution of the Fokker-Planck equation from a point mass at X0."""
    return X0 * np.exp(-THETA * t), SIGMA ** 2 / (2 * THETA) * (1 - np.exp(-2 * THETA * t))


def fokker_planck(grid, p, t0, t1, dt):
    """Explicit finite volumes for dp/dt = d(theta x p)/dx + (sigma^2 / 2) d2p/dx2, with no flux at the ends."""
    dx, D = grid[1] - grid[0], SIGMA ** 2 / 2
    faces = (grid[:-1] + grid[1:]) / 2
    for _ in range(int(round((t1 - t0) / dt))):
        flux = -THETA * faces * (p[:-1] + p[1:]) / 2 - D * (p[1:] - p[:-1]) / dx  # probability moving right
        p = p - dt / dx * np.diff(np.concatenate([[0.0], flux, [0.0]]))
    return p


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, dt, checks = 20000, 0.01, (0.25, 1.0, 3.0)
    lab = labs.Lab()
    x, paths, snaps = np.full(n, X0), [np.full(40, X0)], {}
    for k in range(1, int(round(checks[-1] / dt)) + 1):
        x = x - THETA * x * dt + SIGMA * np.sqrt(dt) * rng.standard_normal(n)  # one Euler-Maruyama step
        paths.append(x[:40].copy())
        for t in checks:
            if k == int(round(t / dt)):
                snaps[t] = x.copy()
    for t in checks:
        m, v = exact(t)
        xs = snaps[t]
        ks = stats.kstest((xs - m) / np.sqrt(v), "norm").statistic
        lab.row(f"t = {t}: mean, variance of 20,000 particles", f"{xs.mean():+.3f}, {xs.var():.3f}   (exact {m:+.3f}, {v:.3f});  "
                                                                 f"KS distance {ks:.4f}")
        assert abs(xs.mean() - m) < 0.03 + 4 * np.sqrt(v / n), "the mean decays like exp(-t)"
        assert abs(xs.var() / v - 1) < 0.05, "the variance follows 1 - exp(-2t)"
        assert ks < 0.02, "the particles are Gaussian with the predicted mean and variance"

    # The same law on a grid, started from the exact density at t = 0.05 (a point mass has no grid density).
    grid = np.linspace(-6, 6, 241)
    m0, v0 = exact(0.05)
    p = fokker_planck(grid, stats.norm.pdf(grid, m0, np.sqrt(v0)), 0.05, 1.0, 5e-4)
    m1, v1 = exact(1.0)
    gap = np.abs(p - stats.norm.pdf(grid, m1, np.sqrt(v1))).max()
    lab.row("t = 1: Fokker-Planck on a grid against the exact density", f"largest difference {gap:.4f}   (peak height "
                                                                         f"{stats.norm.pdf(0, 0, np.sqrt(v1)):.3f})")
    assert gap < 0.01 and abs(p.sum() * (grid[1] - grid[0]) - 1) < 1e-6, "the grid solution matches and conserves probability"

    # Too large a step: the scheme has its own stationary variance, sigma^2 / (2 theta - theta^2 dt).
    big = 0.5
    y = rng.standard_normal(n) * SIGMA / np.sqrt(2 * THETA)
    for _ in range(60):
        y = y - THETA * y * big + SIGMA * np.sqrt(big) * rng.standard_normal(n)
    predicted = SIGMA ** 2 / (2 * THETA - THETA ** 2 * big)
    lab.row("dt = 0.5: stationary variance", f"{y.var():.3f}   (the scheme's own {predicted:.3f}; the process's "
                                             f"{SIGMA ** 2 / (2 * THETA):.3f})")
    assert abs(y.var() / predicted - 1) < 0.05 and y.var() > 1.2, "a coarse step inflates the stationary variance"
    lab.note = ("The particles, the grid solution of the Fokker-Planck equation and the formula describe the same "
                "bell sliding to zero and widening to variance 1; the discretization is exact only as dt goes to "
                "zero, and with dt = 0.5 it settles to a bell a third too wide.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ts = np.arange(len(paths)) * dt
    ax[0].plot(ts, np.array(paths), color=labs.BLUE, alpha=0.25, lw=0.6)
    m, v = exact(ts)
    ax[0].plot(ts, m, color=labs.GOLD, label="exact mean")
    ax[0].fill_between(ts, m - np.sqrt(v), m + np.sqrt(v), color=labs.GOLD, alpha=0.18, label="mean ± one standard deviation")
    ax[0].set(title="40 Euler-Maruyama paths of dx = -x dt + √2 dW", xlabel="time t", ylabel="x")
    ax[0].legend(loc="upper right")
    bins = np.linspace(-4, 4.5, 70)
    for t, color in zip(checks, (labs.RED, labs.GREEN, labs.BLUE)):
        mt, vt = exact(t)
        ax[1].hist(snaps[t], bins=bins, density=True, color=color, alpha=0.35)
        ax[1].plot(grid, stats.norm.pdf(grid, mt, np.sqrt(vt)), color=color, label=f"t = {t}: exact density")
    ax[1].plot(grid, p, "--", color=labs.INK, lw=1.2, label="t = 1: Fokker-Planck on the grid")
    ax[1].set(title="Histograms of the particles against the density", xlabel="x", ylabel="density", xlim=(-4, 4.5))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
