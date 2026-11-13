"""Lab 29: simulate a kernel density estimate's integrated squared error and check it against the exact MISE."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import smooth

TITLE = "The bandwidth trade-off, exactly and by simulation"
GOAL = ("Draw 200 points from the film's two-humped stand-in for Old Faithful 150 times, estimate the density at twelve "
        "bandwidths, and compare the average integrated squared error with Marron and Wand's exact MISE from "
        "statkit.smooth. Then check the rate at which the best MISE falls, and what the normal-reference rule costs.")
TASKS = [
    "Change the kernel to 'epanechnikov' in smooth.kde. The exact curve is for the Gaussian kernel: how far off is it, and at which h?",
    "Replace the truth by one normal, NormalMixture([1], [0], [1]). How close is the normal-reference bandwidth to the best now?",
    "Add smooth.sheather_jones_h(x) and smooth.lscv_h(x, HS) to the selectors and compare their mean ISE with the film's table.",
]

TRUTH = smooth.NormalMixture([0.35, 0.65], [2.0, 4.3], [0.27, 0.42])  # short and long eruptions
HS = np.geomspace(0.04, 0.8, 12)


def best_h(n):
    hs = np.geomspace(0.01, 1.0, 400)
    m = np.array([TRUTH.kde_mise(h, n) for h in hs])
    return float(hs[m.argmin()]), float(m.min())


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    n, reps = 200, 150
    grid = np.linspace(0.5, 6.8, 316)
    dx, f = grid[1] - grid[0], TRUTH.pdf(grid)
    ise, ise_nr, ratio = np.zeros((reps, len(HS))), np.zeros(reps), np.zeros(reps)
    h_star, m_star = best_h(n)
    for r in range(reps):
        x = TRUTH.rvs(n, rng)
        for k, h in enumerate(HS):
            ise[r, k] = np.sum((smooth.kde(x, grid, h) - f) ** 2) * dx
        h_nr = smooth.normal_reference_h(x)
        ratio[r] = h_nr / h_star
        ise_nr[r] = np.sum((smooth.kde(x, grid, h_nr) - f) ** 2) * dx
    sim = ise.mean(0)
    se = ise.std(0, ddof=1) / np.sqrt(reps)
    exact = np.array([TRUTH.kde_mise(h, n) for h in HS])
    worst = np.max(np.abs(sim - exact) / exact)
    k_sim = int(sim.argmin())
    lab.row("mean ISE against exact MISE, twelve bandwidths", f"largest relative gap {worst:.1%}")
    lab.row("best bandwidth at n = 200: exact, AMISE formula", f"{h_star:.3f}, {TRUTH.kde_amise_h(n):.3f}   (film: 0.154)")
    lab.row("simulated ISE is lowest at h =", f"{HS[k_sim]:.3f}   (mean ISE {sim[k_sim]:.4f}; best possible MISE {m_star:.4f})")
    assert worst < 0.12, "the simulation agrees with Marron and Wand's formula"
    assert abs(np.log(HS[k_sim] / h_star)) < 0.45, "the simulated optimum is next to the exact one"

    ns = np.array([100, 1000, 10000])
    best = np.array([best_h(m)[1] for m in ns])
    slope = np.polyfit(np.log(ns), np.log(best), 1)[0]
    lab.row("slope of log best MISE in log n", f"{slope:.3f}   (film: -0.759; limit -4/5; histogram -2/3)")
    assert -0.8 < slope < -0.72, "the kernel estimate's rate is on its way to n^(-4/5)"

    lab.row("normal-reference h over the best h, median", f"{np.median(ratio):.2f}   (film: 2.77)")
    lab.row("mean ISE with the normal-reference h", f"{ise_nr.mean():.4f}   (film: 0.0511; best possible {m_star:.4f})")
    assert 2.4 < np.median(ratio) < 3.1 and ise_nr.mean() > 3 * m_star, "a one-hump rule oversmooths two humps"
    lab.note = ("Too small a bandwidth is all variance, too large is all bias, and the exact formula says where they "
                "balance. The normal-reference rule, tuned for one hump, is nearly three times too wide here.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = TRUTH.rvs(n, rng)
    ax[0].plot(grid, f, color=labs.MUTED, ls="--", label="truth")
    for h, color, name in ((0.04, labs.RED, "h = 0.04: variance"), (h_star, labs.GOLD, f"h = {h_star:.2f}: best"),
                           (smooth.normal_reference_h(x), labs.BLUE, "normal reference: bias")):
        ax[0].plot(grid, smooth.kde(x, grid, h), color=color, lw=1.4, label=name)
    ax[0].plot(x, np.full(n, -0.02), "|", color=labs.GREY, ms=5, alpha=0.5)
    ax[0].set(title="One sample of 200, three bandwidths", xlabel="eruption length (minutes)", ylabel="density")
    ax[0].legend()
    hs = np.geomspace(0.03, 1.0, 200)
    ax[1].plot(hs, [TRUTH.kde_mise(h, n) for h in hs], color=labs.GOLD, label="exact MISE (Marron & Wand)")
    ax[1].errorbar(HS, sim, yerr=2 * se, fmt="o", color=labs.BLUE, ms=4, label="mean ISE of 150 samples, with 2 SE")
    ax[1].axvline(h_star, color=labs.GOLD, lw=0.8, ls=":")
    ax[1].axvline(np.median(ratio) * h_star, color=labs.RED, lw=0.8, ls=":", label="normal-reference h (median)")
    ax[1].set(title="Integrated squared error against bandwidth", xlabel="bandwidth h", ylabel="MISE", xscale="log",
              yscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
