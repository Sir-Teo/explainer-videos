"""Lab 47: compute Hodges's risk bump, simulate it, and watch a Cauchy likelihood ratio become a Gaussian shift."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import asymptotics

TITLE = "Hodges's bump and local asymptotic normality"
GOAL = ("Simulate Hodges's estimator (the sample mean, set to zero when it is within n^(-1/4) of zero) at local "
        "parameters theta = h / sqrt(n), compare its scaled risk with the exact formula and with the sample mean's 1, "
        "and check that Cauchy log-likelihood ratios at h / sqrt(n) approach N(-h^2 I / 2, h^2 I).")
TASKS = [
    "Change the threshold exponent from 1/4 to 0.4 (power=0.4). Where does the peak move, and how fast does it grow with n?",
    "Replace the hard threshold by soft thresholding at n**-0.25 and simulate its local risk. Is the bump smaller?",
    "Repeat the LAN check for the Laplace location family (information 1). Does the variance of the log ratio approach h**2?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Hodges: n E(T - theta)^2 at theta = h / sqrt(n), simulated against the exact formula.
    reps = 400_000
    sims = {}
    for n in (100, 10_000):
        hs = np.array([0.0, 0.5, 1.0, n ** 0.25, 2 * n ** 0.25])
        mc = []
        for h in hs:
            theta = h / np.sqrt(n)
            xbar = theta + rng.standard_normal(reps) / np.sqrt(n)
            T = np.where(np.abs(xbar) >= n ** -0.25, xbar, 0.0)
            mc.append(n * np.mean((T - theta) ** 2))
        exact = asymptotics.hodges_local(hs, n)
        sims[n] = (hs, np.array(mc), exact)
        lab.row(f"n = {n}: scaled risk at h = 0, 0.5, 1", "  ".join(f"{m:.3f} ({e:.3f})" for m, e in zip(mc[:3], exact[:3])) + "   simulated (exact)")
        lab.row(f"n = {n}: at h = n^(1/4) and 2 n^(1/4)", "  ".join(f"{m:.2f} ({e:.2f})" for m, e in zip(mc[3:], exact[3:])) + "   the sample mean: 1")
        assert np.allclose(mc, exact, rtol=0.03, atol=0.01), "simulation agrees with the exact risk"
    grid = np.linspace(0, 60, 6001)
    peaks = {n: asymptotics.hodges_local(grid, n) for n in (100, 10_000, 1_000_000)}
    pk = {n: (grid[r.argmax()], r.max()) for n, r in peaks.items()}
    for n, (h, r) in pk.items():
        lab.row(f"n = {n:,}: peak of the bump", f"{r:.1f} at h = {h:.1f}   (n^(1/4) = {n ** 0.25:.1f})")
    worst = [asymptotics.hodges_local(np.linspace(-c, c, 2001), 10 ** 8).max() for c in (0.5, 1, 2, 4)]
    lab.row("n = 10^8: worst risk over |h| <= 0.5, 1, 2, 4", "  ".join(f"{w:.2f}" for w in worst) + "   (limit c^2; the sample mean: 1)")
    assert asymptotics.hodges_local(0.0, 10_000) < 0.01, "superefficient at zero"
    assert 8 < pk[10_000][1] / pk[100][1] < 16 and 8 < pk[1_000_000][1] / pk[10_000][1] < 16, "the peak grows like sqrt(n)"
    assert np.allclose(worst, [0.25, 1, 4, 16], rtol=0.02), "the local risk tends to h^2: below 1 only for |h| < 1"

    # 2. LAN: the Cauchy location family, information 1/2.
    h = 1.5
    rows = {n: asymptotics.cauchy_local_llr(n, h, 40_000, rng) for n in (25, 400)}
    for n, r in rows.items():
        lab.row(f"Cauchy log ratio, n = {n}, h = {h}", f"mean {r['mean']:.3f} (LAN {r['lan_mean']:.4f})   variance {r['var']:.3f} (LAN {r['lan_var']:.3f})")
    r = rows[400]
    assert abs(r["mean"] - r["lan_mean"]) < 0.03 and abs(r["var"] - r["lan_var"]) < 0.06, "LAN's Gaussian shift"
    lab.note = ("Hodges's estimator beats the bound at zero and pays beside it: its local risk tends to h squared, so its "
                "worst case over a wide neighbourhood is unbounded, while the Cauchy model already looks like one normal "
                "observation with variance 1 / I.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    for (n, rr), color in zip(peaks.items(), (labs.BLUE, labs.GOLD, labs.RED)):
        ax[0].semilogy(grid, rr, color=color, label=f"n = {n:,}")
    for n, color in ((100, labs.BLUE), (10_000, labs.GOLD)):
        ax[0].scatter(sims[n][0], sims[n][1], color=color, s=26, zorder=3, edgecolor=labs.INK, linewidth=0.5)
    ax[0].axhline(1, color=labs.MUTED, ls="--", label="the sample mean")
    ax[0].set(title="Hodges's scaled risk at theta = h / sqrt(n) (dots: simulated)", xlabel="local parameter h",
              ylabel="n x mean squared error", ylim=(1e-3, 3e3))
    ax[0].legend(loc="lower right")
    x = np.linspace(-4.5, 3.5, 300)
    ax[1].hist(r["llr"], bins=80, range=(-4.5, 3.5), density=True, color=labs.BLUE, alpha=0.6, label="40,000 log ratios, n = 400")
    ax[1].plot(x, stats.norm.pdf(x, r["lan_mean"], np.sqrt(r["lan_var"])), color=labs.GOLD, label="LAN: N(-h²I/2, h²I)")
    ax[1].set(title="Cauchy location: log likelihood ratio at h = 1.5", xlabel="log likelihood ratio", ylabel="density")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
