"""Lab 61: compute one Wasserstein distance four ways, and watch Sinkhorn's cost approach it."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import ot

TITLE = "Transport on a line: quantiles, areas, a linear program and Sinkhorn"
GOAL = ("Draw two samples on a line and compute W1 by the quantile formula, as the area between the two CDFs and "
        "as a Kantorovich linear program with its dual; then check W2 against the normal closed form and watch "
        "the entropic plan's cost fall to the exact one as the regularization shrinks.")
TASKS = [
    "Change the cost to the squared distance (p = 2) in the linear program. Which potentials change, and does the "
    "sorted pairing stay optimal?",
    "Give the two samples different sizes (60 and 45) and unequal weights. How many entries of the optimal plan "
    "are positive, against the bound n + m - 1?",
    "Move to the plane: use ot.empirical_rate with d = 1, 2, 4 and fit the slope of log W1 against log n.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, m1, s1, m2, s2 = 60, 0.0, 1.0, 1.5, 1.8
    x, y = m1 + s1 * rng.standard_normal(n), m2 + s2 * rng.standard_normal(n)
    a = np.full(n, 1 / n)
    lab = labs.Lab()

    # W1 four ways: quantiles, CDF area, sorted pairing, the linear program and its dual
    w_quant, w_area = ot.wasserstein_1d(x, y, 1), ot.w1_cdf_area(x, y)
    w_sort = float(np.mean(np.abs(np.sort(x) - np.sort(y))))
    C = ot.cost_matrix(x[:, None], y[:, None], 1)
    lp = ot.kantorovich_lp(a, a, C)
    dual = float(a @ lp["f"] + a @ lp["g"])
    slack = float(np.max(lp["f"][:, None] + lp["g"][None, :] - C))
    lab.row("W1 by the quantile formula", f"{w_quant:.6f}")
    lab.row("W1 as the area between the CDFs", f"{w_area:.6f}")
    lab.row("W1 by pairing the sorted samples", f"{w_sort:.6f}")
    lab.row("Kantorovich LP: primal, dual", f"{lp['cost']:.6f}, {dual:.6f}   (largest f_i + g_j - C_ij: {slack:.1e})")
    assert abs(w_quant - w_area) < 1e-9 and abs(w_quant - w_sort) < 1e-9, "three formulas for W1 on a line agree"
    assert abs(lp["cost"] - w_quant) < 1e-7, "the linear program finds the monotone plan's cost"
    assert abs(dual - lp["cost"]) < 1e-7 and slack < 1e-7, "strong duality with a feasible dual"
    positive = int(np.sum(lp["P"] > 1e-12))
    lab.row("positive entries of the optimal plan", f"{positive}   (at most n + m - 1 = {2 * n - 1})")
    assert positive <= 2 * n - 1

    # W2 between large samples against the normal closed form
    big = 20000
    xb, yb = m1 + s1 * rng.standard_normal(big), m2 + s2 * rng.standard_normal(big)
    w2_emp, w2_true = ot.wasserstein_1d(xb, yb, 2), ot.gaussian_w2(m1, s1 ** 2, m2, s2 ** 2)
    lab.row("W2, two samples of 20,000", f"{w2_emp:.4f}   (closed form sqrt(1.5^2 + 0.8^2) = {w2_true:.4f})")
    assert abs(w2_true - np.hypot(m2 - m1, s2 - s1)) < 1e-12 and abs(w2_emp - w2_true) < 0.06

    # Sinkhorn: the entropic plan's transport cost decreases to the LP's as eps shrinks
    eps = np.array([2.0, 1.0, 0.5, 0.25, 0.12])
    sk = [ot.sinkhorn(a, a, C, e, iters=40000, tol=1e-7) for e in eps]
    costs = np.array([s["cost"] for s in sk])
    lab.row("Sinkhorn plan cost at eps = 2, 0.5, 0.12", f"{costs[0]:.4f}, {costs[2]:.4f}, {costs[-1]:.4f}   (exact {lp['cost']:.4f})")
    lab.row("Sinkhorn iterations at eps = 2, 0.5, 0.12", f"{sk[0]['iters']}, {sk[2]['iters']}, {sk[-1]['iters']}")
    assert all(s["errs"][-1] < 1e-7 for s in sk), "Sinkhorn converged at every eps"
    assert np.all(costs >= lp["cost"] - 1e-9) and np.all(np.diff(costs) < 0), "cost falls monotonically to the LP's"
    assert costs[-1] - lp["cost"] < 0.05 * lp["cost"] and sk[-1]["iters"] > sk[0]["iters"]
    lab.note = ("On a line every route to W1 gives the same number, and the dual prices certify it; smoothing the "
                "plan with entropy costs extra transport that vanishes with eps, at the price of more iterations.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    z = np.sort(np.r_[x, y])
    F = np.searchsorted(np.sort(x), z, side="right") / n
    G = np.searchsorted(np.sort(y), z, side="right") / n
    ax[0].step(z, F, where="post", color=labs.BLUE, label="CDF of the first sample")
    ax[0].step(z, G, where="post", color=labs.GOLD, label="CDF of the second sample")
    ax[0].fill_between(z, F, G, step="post", color=labs.GREEN, alpha=0.3, label=f"area between them = W1 = {w_quant:.3f}")
    ax[0].set(title="W1 is the area between two CDFs", xlabel="x", ylabel="cumulative probability")
    ax[0].legend(loc="lower right")
    ax[1].plot(eps, costs, "o-", color=labs.BLUE, label="transport cost of the Sinkhorn plan")
    ax[1].axhline(lp["cost"], color=labs.GOLD, ls="--", label="exact cost (linear program)")
    ax[1].set(xscale="log", title="Entropic smoothing: the cost of the plan against eps",
              xlabel="regularization eps (log scale)", ylabel="sum of P_ij C_ij")
    ax[1].set_xticks(eps, [f"{e:g}" for e in eps])
    ax[1].minorticks_off()
    ax[1].legend()
    lab.fig = fig
    return lab
