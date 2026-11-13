"""Lab 52: PCA on pure noise against Marchenko-Pastur, and a spike crossing the BBP threshold."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import hdstat

TITLE = "The bulk, its edges, and the spike that PCA can or cannot see"
GOAL = ("Compute the sample eigenvalues of 1,000 observations of 500 independent variables and compare their range "
        "with the Marchenko-Pastur edges. Then plant a spike of size ell in the covariance (p/n = 1/2) and compare "
        "the top sample eigenvalue and the eigenvector's squared overlap with the BBP limits on both sides of the "
        "threshold sqrt(1/2).")
TASKS = [
    "Invert the map with hdstat.spike_invert on the top eigenvalue at ell = 3. How close is the estimate to 3, and "
    "how far off is the raw eigenvalue minus one?",
    "Compare hdstat.anderson_ci and hdstat.spike_ci over 200 samples at ell = 3: which covers 1 + ell = 4?",
    "Draw the noise from a t distribution with 5 degrees of freedom scaled to variance one. Do the edges and the "
    "threshold move?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    X = rng.standard_normal((1000, 500))
    ev = np.linalg.eigvalsh(X.T @ X / 1000)
    lo, hi = hdstat.mp_edges(0.5)
    lab.row("pure noise, n = 1,000, p = 500: smallest / largest eigenvalue",
            f"{ev[0]:.3f} / {ev[-1]:.3f}   Marchenko-Pastur edges {lo:.3f} / {hi:.3f}   (every true eigenvalue is 1)")
    assert abs(ev[0] - lo) < 0.02 and abs(ev[-1] - hi) < 0.12, "the noise spectrum fills the MP support"
    grid = np.linspace(lo, hi, 4001)
    mass = float(np.sum(hdstat.mp_pdf(grid, 0.5)) * (grid[1] - grid[0]))
    assert abs(mass - 1) < 0.01, "the MP density integrates to one"

    n, p, gamma, reps = 300, 150, 0.5, 12
    ells = [0.3, 0.5, 1.0, 2.0, 3.0, 4.0]
    top, over = [], []
    for ell in ells:
        t, o = [], []
        for _ in range(reps):
            lam, v = hdstat.top_eig(hdstat.spiked_sample(n, p, ell, rng))
            t.append(lam)
            o.append(v[0] ** 2)
        top.append(np.mean(t))
        over.append(np.mean(o))
        lab.row(f"spike ell = {ell}: top eigenvalue, overlap^2",
                f"{top[-1]:.2f}, {over[-1]:.2f}   BBP limits {float(hdstat.spike_eigenvalue(ell, gamma)):.2f}, "
                f"{float(hdstat.spike_overlap(ell, gamma)):.2f}")
    lim_top = hdstat.spike_eigenvalue(np.array(ells), gamma)
    lim_over = hdstat.spike_overlap(np.array(ells), gamma)
    lab.row("threshold sqrt(p/n)", f"{np.sqrt(gamma):.3f}")
    assert over[0] < 0.08 and abs(top[0] / hi - 1) < 0.04, "below the threshold the spike is invisible to PCA"
    assert all(abs(t / l - 1) < 0.08 for t, l in zip(top[3:], lim_top[3:])), "above it, the eigenvalue is biased upward"
    assert all(abs(o - l) < 0.08 for o, l in zip(over[3:], lim_over[3:])), "and the eigenvector is partly right"
    assert top[-1] > 1 + ells[-1] + 0.3, "the top eigenvalue overstates the spike 1 + ell"
    lab.note = ("With p/n fixed the sample spectrum of pure noise spreads over [(1 - sqrt g)^2, (1 + sqrt g)^2]; a "
                "spike below sqrt g stays inside it, and above it the top eigenvalue lands at (1 + ell)(1 + g/ell) "
                "with an eigenvector only partly aligned with the truth.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].hist(ev, bins=50, density=True, color=labs.BLUE, alpha=0.6, label="sample eigenvalues")
    ax[0].plot(grid, hdstat.mp_pdf(grid, 0.5), color=labs.GOLD, label="Marchenko-Pastur, p/n = 1/2")
    ax[0].axvline(1, color=labs.MUTED, ls="--", label="every true eigenvalue")
    ax[0].set(title="PCA on pure noise: n = 1,000, p = 500", xlabel="eigenvalue", ylabel="density")
    ax[0].legend()
    fine = np.linspace(0.05, 4.2, 300)
    ax[1].plot(fine, hdstat.spike_overlap(fine, gamma), color=labs.GOLD, label="limit of the squared overlap")
    ax[1].plot(ells, over, "o", color=labs.BLUE, label="simulated, n = 300, p = 150")
    ax[1].axvline(np.sqrt(gamma), color=labs.RED, ls="--", label="threshold sqrt(p/n) = 0.707")
    ax[1].set(title="Does the top eigenvector find the spike?", xlabel="spike ell", ylabel="squared overlap with the truth",
              ylim=(-0.03, 1))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
