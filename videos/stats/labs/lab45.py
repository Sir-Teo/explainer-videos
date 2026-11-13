"""Lab 45: draw a whole decision problem's risk set, find its minimax rule, and check James-Stein's exact risk."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import decision

TITLE = "A risk set, its minimax rule, and Stein's paradox"
GOAL = ("Enumerate all sixteen rules for deciding whether a coin tossed three times is fair or biased, find the "
        "admissible edge, the Bayes rules and the minimax rule, and check the minimax theorem; then simulate the "
        "James-Stein estimator in ten dimensions against its exact risk.")
TASKS = [
    "Change the cost of missing a biased coin from 2 to 5. Which threshold rules does the minimax rule mix now, and what is the least favourable prior?",
    "Toss the coin five times instead of three (six possible counts, so 2**6 = 64 rules). How many corners does the lower edge have?",
    "Set p = 2 in the James-Stein simulation with the factor (1 - c / |x|**2) for a few c > 0. Can you find a c that beats X at every theta?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. The coin problem of chapter 2: states fair (0.5) and biased (0.8), X = heads in 3 tosses, actions fair/biased.
    x = np.arange(4)
    px = np.array([stats.binom.pmf(x, 3, 0.5), stats.binom.pmf(x, 3, 0.8)])
    loss = np.array([[0.0, 1.0], [2.0, 0.0]])  # calling a fair coin biased costs 1; missing a biased coin costs 2
    rp = decision.risk_points(px, loss)
    R = rp["R"]
    edge = decision.lower_boundary(R)
    thresholds = np.array([[px[0, c:].sum(), 2 * px[1, :c].sum()] for c in range(5)])[::-1]  # "biased if X >= c"
    mm = decision.minimax(R)
    priors = np.linspace(0, 1, 2001)
    bayes = np.array([decision.bayes_rule(R, pi)["bayes_risk"] for pi in priors])
    lab.row("rules, corners of the admissible edge", f"{len(R)}, {len(edge)}")
    lab.row("minimax risk (linear programme)", f"{mm['value']:.4f}   at risk point ({mm['point'][0]:.4f}, {mm['point'][1]:.4f})")
    lab.row("largest Bayes risk over all priors", f"{bayes.max():.4f}   at P(fair) = {priors[bayes.argmax()]:.3f}")
    lab.row("least favourable prior (LP dual)", f"P(fair) = {mm['least_favourable'][0]:.3f}")
    assert np.allclose(edge, thresholds[np.argsort(thresholds[:, 0])]), "the admissible corners are the threshold rules"
    assert abs(mm["value"] - bayes.max()) < 1e-4, "the minimax theorem: min max risk = max Bayes risk"
    assert abs(mm["point"][0] - mm["point"][1]) < 1e-8, "the minimax rule is an equalizer"
    assert abs(mm["least_favourable"][0] - priors[bayes.argmax()]) < 2e-3

    # 2. James-Stein in p = 10 dimensions: exact risk p - (p - 2)^2 E[1 / (p - 2 + 2K)], K ~ Poisson(|theta|^2 / 2).
    p, reps = 10, 100_000
    norms2 = np.array([0.0, 4.0, 10.0, 40.0])
    exact = decision.js_risk(p, norms2)
    mc, mc_pp = [], []
    for n2 in norms2:
        theta = np.zeros(p)
        theta[0] = np.sqrt(n2)
        X = theta + rng.standard_normal((reps, p))
        s = np.sum(X ** 2, axis=1, keepdims=True)
        mc.append(np.mean(np.sum(((1 - (p - 2) / s) * X - theta) ** 2, axis=1)))
        mc_pp.append(np.mean(np.sum((np.maximum(1 - (p - 2) / s, 0) * X - theta) ** 2, axis=1)))
    for n2, e, m, mp in zip(norms2, exact, mc, mc_pp):
        lab.row(f"|theta|^2 = {n2:g}: James-Stein risk", f"simulated {m:.3f}   exact {e:.3f}   positive part {mp:.3f}   (X: {p})")
    assert np.all(np.abs(np.array(mc) - exact) < 0.1), "the Poisson-mixture formula"
    assert np.all(decision.js_risk(p, np.linspace(0, 400, 81)) < p), "James-Stein dominates X"
    assert abs(exact[0] - 2) < 1e-9 and mc_pp[0] < mc[0] - 0.2, "risk 2 at the origin; the positive part does better"
    lab.note = ("The admissible rules are the threshold rules and their mixtures, the minimax rule equalizes the two "
                "risks at the largest Bayes risk, and in ten dimensions James-Stein's risk stays below 10 everywhere.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].scatter(R[:, 0], R[:, 1], s=22, color=labs.BLUE, label="the 16 rules", zorder=3)
    ax[0].plot(edge[:, 0], edge[:, 1], color=labs.GOLD, label="admissible edge (threshold rules)")
    ax[0].plot([0, 1.2], [0, 1.2], color=labs.MUTED, ls=":", lw=1, label="equal risks")
    ax[0].scatter(*mm["point"], s=70, color=labs.RED, zorder=4, label=f"minimax: {mm['value']:.3f}")
    pi = mm["least_favourable"][0]
    r1 = np.array([0, 1.0])
    ax[0].plot(r1, (mm["value"] - pi * r1) / (1 - pi), color=labs.RED, lw=1, ls="--", label=f"least favourable prior {pi:.3f}")
    ax[0].set(title="Fair or biased? The risk set", xlabel="risk if the coin is fair", ylabel="risk if it is biased",
              xlim=(-0.03, 1.05), ylim=(-0.05, 3.1))
    ax[0].legend()
    g = np.linspace(0, 40, 201)
    ax[1].plot(g, decision.js_risk(p, g), color=labs.GOLD, label="James-Stein, exact")
    ax[1].axhline(p, color=labs.BLUE, label="X itself")
    ax[1].scatter(norms2, mc, color=labs.GOLD, s=28, zorder=3, label="James-Stein, simulated")
    ax[1].scatter(norms2, mc_pp, color=labs.GREEN, s=28, marker="s", zorder=3, label="positive part, simulated")
    ax[1].set(title="Ten normal means: risk against |theta|^2", xlabel="|theta|^2", ylabel="expected squared error", ylim=(0, 11))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
