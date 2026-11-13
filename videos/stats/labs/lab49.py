"""Lab 49: project a gradient onto a tangent space, then break the one-step estimator one nuisance at a time."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import semipar

TITLE = "The efficient influence function as a projection, and double robustness as a product"
GOAL = ("On a 2 x 2 table under independence, project the gradient of P(X1 = 1, X2 = 1) onto the tangent space and "
        "check that two estimators have n times variance equal to the two squared norms. Then run the ATE's one-step "
        "estimator with one nuisance wrong, then both, and compare its bias with the product formula.")
TASKS = [
    "Make the table dependent (add 0.05 to the (1,1) and (0,0) cells, subtract it from the others). Which estimator "
    "is now biased, and by how much?",
    "Replace semipar.ate_one_step by semipar.ate_tmle in the four scenarios. Do the biases change beyond Monte Carlo "
    "error?",
    "Use semipar.corrupt(w, a, b) with a = b = 0.25 and then 0.4 at n = 500, 2,000, 8,000, and watch root-n times "
    "the one-step's bias.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # ---- the geometry: cells (x1, x2) in row-major order, X1 and X2 independent with P(X1=1)=0.3, P(X2=1)=0.6
    p1, q1 = 0.3, 0.6
    p = np.array([(1 - p1) * (1 - q1), (1 - p1) * q1, p1 * (1 - q1), p1 * q1])
    phi = semipar.gradient_discrete(lambda q: q[3], p)  # the nonparametric gradient: 1{x = (1,1)} - p11
    star = semipar.project(p, phi, semipar.independence_scores(2, 2))  # its projection onto {a(x1) + b(x2)}
    b_np, b_eff = semipar.bound(p, phi), semipar.bound(p, star)
    closed = q1 ** 2 * p1 * (1 - p1) + p1 ** 2 * q1 * (1 - q1)
    n, reps = 400, 20000
    counts = rng.multinomial(n, p, size=reps) / n
    freq = counts[:, 3]
    prod = (counts[:, 2] + counts[:, 3]) * (counts[:, 1] + counts[:, 3])
    v_freq, v_prod = n * freq.var(), n * prod.var()
    lab.row("||phi||^2, the nonparametric bound", f"{b_np:.4f}   n Var of the cell frequency {v_freq:.4f}")
    lab.row("||phi*||^2, the bound under independence", f"{b_eff:.4f}   n Var of the product of margins {v_prod:.4f}")
    lab.row("closed form q1^2 p1(1-p1) + p1^2 q1(1-q1)", f"{closed:.4f}")
    assert abs(b_np - p[3] * (1 - p[3])) < 1e-6 and abs(b_eff - closed) < 1e-6, "the projection's norm"
    assert semipar.inner(p, phi - star, star) < 1e-9, "the residual is orthogonal to the tangent space"
    assert abs(v_freq / b_np - 1) < 0.05 and abs(v_prod / b_eff - 1) < 0.05, "each estimator attains its bound"

    # ---- double robustness: the ATE's one-step with the truth, one wrong nuisance, and both wrong
    m, sims = 2000, 400
    names = ["both right", "outcome wrong", "propensity wrong", "both wrong"]
    est = {k: [] for k in names}
    for _ in range(sims):
        w = semipar.rate_world(m, rng)
        x1 = w["X"][:, 0]
        bad_mu1, bad_mu0, bad_e = w["mu1"] + 1.5 * (x1 - 0.2), w["mu0"] + x1, np.full(m, 0.5)
        for k, (mu0, mu1, e) in zip(names, ((w["mu0"], w["mu1"], w["e"]), (bad_mu0, bad_mu1, w["e"]),
                                           (w["mu0"], w["mu1"], bad_e), (bad_mu0, bad_mu1, bad_e))):
            est[k].append(semipar.ate_one_step(w["y"], w["t"], mu0, mu1, e)["est"])
    bias = {k: np.mean(v) - 1.5 for k, v in est.items()}
    mcse = {k: np.std(v) / np.sqrt(sims) for k, v in est.items()}
    # the product formula E[(e - ê)(mu1 - mû1)/ê] - E[(ê - e)(mu0 - mû0)/(1 - ê)] on a fine grid of x1
    g = (np.arange(200000) + 0.5) / 200000
    e = 0.2 + 0.6 * g
    formula = np.mean((e - 0.5) * (-1.5 * (g - 0.2)) / 0.5) - np.mean((0.5 - e) * (-g) / 0.5)
    for k in names:
        lab.row(f"one-step bias, {k}", f"{bias[k]:+.4f} ± {mcse[k]:.4f}"
                + (f"   product formula {formula:+.4f}" if k == "both wrong" else "   theory 0"))
    assert all(abs(bias[k]) < 0.015 for k in names[:3]), "one correct nuisance is enough"
    assert abs(bias["both wrong"] - formula) < 0.02 and abs(formula) > 0.2, "the bias is the product of the errors"
    lab.note = ("The projection shortens the gradient, and the estimator that uses the model attains the shorter "
                "length; the one-step is unbiased when either nuisance is right, and with both wrong its bias is "
                "the product formula's.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.arange(0.11 - 0.5 / n, 0.25, 2 / n)  # two lattice steps of the cell frequency per bin
    ax[0].hist(freq, bins=bins, density=True, color=labs.BLUE, alpha=0.55, label=f"cell frequency: n Var {v_freq:.3f}")
    ax[0].hist(prod, bins=bins, density=True, color=labs.GOLD, alpha=0.55,
               label=f"product of margins: n Var {v_prod:.3f}")
    ax[0].axvline(p[3], color=labs.MUTED, ls="--")
    ax[0].set(title="Two estimators of P(X1 = 1, X2 = 1) = 0.18, n = 400", xlabel="estimate", ylabel="density")
    ax[0].legend(loc="upper left")
    ax[0].set_ylim(0, ax[0].get_ylim()[1] * 1.3)
    xs = np.arange(4)
    ax[1].bar(xs, [bias[k] for k in names], yerr=[2 * mcse[k] for k in names], color=[labs.GREEN] * 3 + [labs.RED],
              ecolor=labs.INK, width=0.6)
    ax[1].plot([2.6, 3.4], [formula, formula], color=labs.GOLD, label="the product formula")
    ax[1].axhline(0, color=labs.MUTED, lw=1)
    ax[1].set_xticks(xs, ["both right", "outcome\nwrong", "propensity\nwrong", "both wrong"])
    ax[1].set(title="Bias of the ATE's one-step estimator (truth 1.5)", ylabel="bias")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
