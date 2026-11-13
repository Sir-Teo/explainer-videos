"""Lab 25: shrink Efron and Morris's eighteen hitters, and check James-Stein's risk against its formula."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import shrink

TITLE = "James-Stein on the hitters, and its risk for every theta"
GOAL = ("Recompute the film's baseball numbers with the series' library, then simulate James-Stein in ten dimensions "
        "at true mean vectors of growing length and compare its risk with p - (p - 2)^2 E(1/|X|^2).")
TASKS = [
    "Set p = 2 in the risk study. What does the formula give, and why does the estimator stop helping?",
    "Shrink the hitters towards 0 instead of their mean (target=0.0 on the transformed scale). What happens to B?",
    "Put all of theta's length in one coordinate. The total risk is unchanged; what happens to that coordinate's own?",
]


def exact_risk(p, norm2):
    """p - (p - 2)^2 E(1/|X|^2): |X|^2 is noncentral chi-squared, a Poisson(norm2 / 2) mixture of chi-squared(p + 2K)."""
    k = np.arange(0, int(norm2 / 2 + 12 * np.sqrt(norm2 / 2 + 1) + 40))
    return p - (p - 2) ** 2 * float(np.sum(stats.poisson.pmf(k, norm2 / 2) / (p - 2 + 2 * k)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    names, hits, _, rest = museum.efron_morris()
    y = hits / 45
    x = np.sqrt(45) * np.arcsin(2 * y - 1)  # close to unit variance on this scale
    js = shrink.james_stein(x, 1.0)
    est = (np.sin(js["theta"] / np.sqrt(45)) + 1) / 2
    sse_raw, sse_js = float(np.sum((y - rest) ** 2)), float(np.sum((est - rest) ** 2))
    closer = int(np.sum(np.abs(est - rest) < np.abs(y - rest)))

    p, lengths = 10, np.array([0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0])
    mc, mc_plus, mle, theory = [], [], [], []
    for r in lengths:
        theta = np.full(p, r / np.sqrt(p))
        out = shrink.js_risk_exact(theta, R=40000, rng=rng)
        mc.append(out["js"])
        mc_plus.append(out["js_plus"])
        mle.append(out["mle"])
        theory.append(exact_risk(p, r * r))
    mc, mc_plus, mle, theory = map(np.array, (mc, mc_plus, mle, theory))

    lab = labs.Lab()
    lab.row("hitters: shrinkage factor B", f"{js['B']:.3f}   (the film: 0.791)")
    lab.row("hitters: total squared error, own average", f"{sse_raw:.4f}   (the film: 0.0753)")
    lab.row("hitters: total squared error, James-Stein", f"{sse_js:.4f}   (the film: 0.0215), {sse_raw / sse_js:.1f} times smaller")
    lab.row("hitters: James-Stein closer for", f"{closer} of 18")
    for i in (0, 3, 7):
        lab.row(f"p = 10, |theta| = {lengths[i]:g}: risk of James-Stein", f"{mc[i]:.3f}   (formula {theory[i]:.3f}; MLE {mle[i]:.2f})")
    lab.row("p = 10, theta = 0: positive part", f"{mc_plus[0]:.3f}")
    lab.note = ("James-Stein's total risk is below the MLE's p at every theta, by most when the means are close "
                "together, and the positive part improves on it again; the gain is in the total, not in each coordinate.")
    assert abs(js["B"] - 0.791) < 0.001 and abs(sse_raw - 0.0753) < 1e-4 and abs(sse_js - 0.0215) < 1e-4 and closer == 15
    assert abs(theory[0] - 2.0) < 1e-9, "at theta = 0 the risk is p - (p - 2) = 2"
    assert np.all(np.abs(mc - theory) < 0.12), "Monte Carlo risk matches p - (p-2)^2 E(1/|X|^2)"
    assert np.all(theory < p) and np.all(np.diff(theory) > 0), "below the MLE's risk everywhere, rising towards it"
    assert np.all(mc_plus <= mc + 1e-9) and mc_plus[0] < mc[0] - 0.4, "the positive part dominates"

    fig, ax = labs.figure(2, size=(11, 4.4))
    order = np.argsort(y)
    for i in order:
        ax[0].plot([y[i], est[i], rest[i]], [2, 1, 0], color=labs.MUTED, lw=0.8, alpha=0.8)
    ax[0].scatter(y, np.full(18, 2), color=labs.BLUE, s=22, zorder=3)
    ax[0].scatter(est, np.full(18, 1), color=labs.GOLD, s=22, zorder=3)
    ax[0].scatter(rest, np.full(18, 0), color=labs.GREEN, s=22, zorder=3)
    ax[0].set_yticks([0, 1, 2], ["rest of season", "James-Stein", "first 45 at-bats"])
    ax[0].set(title="Eighteen hitters, 1970", xlabel="batting average", ylim=(-0.4, 2.4))
    grid = np.linspace(0, 12, 80)
    ax[1].plot(grid, [exact_risk(p, r * r) for r in grid], color=labs.GOLD, label="James-Stein: formula")
    ax[1].scatter(lengths, mc, color=labs.GOLD, s=26, zorder=3, label="James-Stein: 40,000 draws")
    ax[1].plot(lengths, mc_plus, "o--", color=labs.GREEN, ms=4, lw=1.2, label="positive part: 40,000 draws")
    ax[1].axhline(p, color=labs.RED, label="MLE: p = 10")
    ax[1].set(title="Risk in ten dimensions", xlabel="length of the true mean vector |θ|", ylabel="expected total squared error",
              ylim=(0, 11.5))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
