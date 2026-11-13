"""Lab 53: how fast a Gaussian-prior posterior contracts, and when its credible ball stops covering."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import bnp

TITLE = "Contraction rates and credible balls in the Gaussian sequence model"
GOAL = ("With a truth of regularity beta = 1 and priors theta_k ~ N(0, k^(-1-2 alpha)), fit the posterior mean's rate "
        "from its exact risk and compare it with n^(-min(alpha, beta)/(1 + 2 alpha)); then measure how often the 95% "
        "credible ball contains the truth as alpha passes beta, and how fast a Beta posterior becomes normal.")
TASKS = [
    "Choose alpha by empirical Bayes (bnp.eb_alpha) on each simulated dataset and recompute the credible ball's "
    "coverage with the chosen alpha.",
    "Use bnp.functional_coverage with a_k = 1/k and then a_k = k^(-0.6) at alpha = 3. Which linear functional keeps "
    "its 95%?",
    "Change the truth's regularity beta to 2 and find the alpha with the fastest rate. Is it still alpha = beta?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    beta, K = 1.0, 20000
    theta = bnp.sobolev_truth(K, beta)
    ns = np.array([10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6])
    alphas = (0.5, 1.0, 2.0)
    rms = {a: np.array([np.sqrt(bnp.risk(theta, int(n), bnp.prior_var(K, a))["risk"]) for n in ns]) for a in alphas}
    for a in alphas:
        slope = np.polyfit(np.log(ns), np.log(rms[a]), 1)[0]
        theory = -min(a, beta) / (1 + 2 * a)
        lab.row(f"prior alpha = {a}: fitted exponent of the posterior mean's error", f"{slope:.3f}   theory {theory:.3f}")
        assert abs(slope - theory) < 0.03, "the contraction rate n^(-min(alpha, beta)/(1 + 2 alpha))"
    assert rms[1.0][-1] < rms[0.5][-1] and rms[1.0][-1] < rms[2.0][-1], "matching the truth's smoothness is fastest"

    # one simulated check of the exact risk
    n, Ks = 10 ** 4, 1500
    th, lam = theta[:Ks], bnp.prior_var(Ks, 1.0)
    Y = th + rng.standard_normal((400, Ks)) / np.sqrt(n)
    sim = float(np.mean(np.sum((bnp.posterior(Y, n, lam)["mean"] - th) ** 2, axis=1)))
    exact = bnp.risk(th, n, lam)["risk"]
    lab.row("alpha = 1, n = 10^4: simulated risk of the posterior mean", f"{sim:.6f}   exact {exact:.6f}")
    assert abs(sim / exact - 1) < 0.05, "the simulated risk is the exact one"

    grid = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    cover = [bnp.credible_ball_coverage(th, n, bnp.prior_var(Ks, a), reps=1500, rng=rng) for a in grid]
    for a, c in zip(grid, cover):
        lab.row(f"alpha = {a}: 95% credible ball covers the truth", f"{c['coverage']:.1%}   radius {c['radius']:.4f}   "
                f"mean distance to the truth {c['dist']:.4f}")
    assert all(c["coverage"] > 0.97 for c in cover[:3]), "a rougher prior than the truth is conservative"
    assert cover[4]["coverage"] < 0.05 and cover[5]["coverage"] < 0.01, "a smoother prior is confidently wrong"

    tv = [bnp.bvm_tv_beta(int(round(0.3 * m)), m) for m in (10, 100, 1000, 10000)]
    lab.row("Bernstein-von Mises, p = 0.3: TV(Beta posterior, normal) at n = 10 ... 10^4", "  ".join(f"{t:.4f}" for t in tv))
    assert all(x > 2.5 * y for x, y in zip(tv, tv[1:])) and tv[-1] < 0.005, "TV falls like n^(-1/2)"
    lab.note = ("The posterior contracts at the minimax rate only when the prior's smoothness matches the truth's; "
                "an oversmoothing prior is slower and its credible ball, too small for its own bias, misses the "
                "truth almost always.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for a, color in zip(alphas, (labs.BLUE, labs.GOLD, labs.RED)):
        ax[0].loglog(ns, rms[a], "o-", color=color, label=f"alpha = {a}: theory n^(-{min(a, beta) / (1 + 2 * a):.2f})")
    ax[0].set(title="Error of the posterior mean, truth of regularity 1", xlabel="n", ylabel="root of the exact risk")
    ax[0].legend()
    ax[1].plot(grid, [c["coverage"] for c in cover], "o-", color=labs.GOLD, label="coverage of the 95% credible ball")
    ax[1].axhline(0.95, color=labs.MUTED, ls="--")
    ax[1].axvline(beta, color=labs.GREEN, ls=":", label="the truth's regularity beta = 1")
    ax[1].set(title="Is the credible ball honest? n = 10,000", xlabel="prior regularity alpha", ylabel="coverage",
              ylim=(-0.03, 1.05))
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
