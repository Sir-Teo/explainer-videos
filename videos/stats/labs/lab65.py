"""Lab 65: rerun one row of the dissertation's study and test its coverage bound."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import thesis

TITLE = "Weighted conformal under shift: coverage against the total-variation bound"
GOAL = ("Calibrate on X ~ N(0, 1), test on X ~ N(1, 1), with noise that grows with x. Run split conformal with no "
        "weights, half-strength weights, exact weights and weights estimated by a classifier, and compare each "
        "coverage with the theorem's lower bound 1 - alpha - TV.")
TASKS = [
    "Set gamma = 0, so the scores do not depend on x. Which methods now cover 90%, and how loose is the bound?",
    "Raise the shift mu to 1.5 and record the fraction of infinite intervals for the exact weights.",
    "Use method='misspecified' (a classifier that sees only |x|). Is its coverage above its bound, and is the "
    "bound useful?",
]

ALPHA, MU, GAMMA = 0.1, 1.0, 1.0


def cell(method, reps, rng, lam=0.5, gamma=GAMMA):
    r = [thesis.one_run(500, 500, MU, gamma, ALPHA, method, rng, lam=lam) for _ in range(reps)]
    c = np.array([x["coverage"] for x in r])
    return {"cov": float(c.mean()), "se": float(c.std(ddof=1) / np.sqrt(reps)),
            "bound": float(np.mean([x["bound"] for x in r])), "inf": float(np.mean([x["inf"] for x in r]))}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # the bound's penalty in closed form, against quadrature of the reweighted density
    for lam in (0.0, 0.5, 1.0):
        closed = 2 * stats.norm.cdf(abs(1 - lam) * MU / 2) - 1
        numeric = thesis.tv_reweighted(lambda x, lam=lam: np.exp(lam * MU * np.asarray(x, float)), MU)
        assert abs(closed - numeric) < 1e-4 and abs(thesis.coverage_bound(ALPHA, MU, lam) - (1 - ALPHA - closed)) < 1e-12
    lab.row("TV(N(lam mu, 1), N(mu, 1)) at lam = 0, 0.5, 1", ", ".join(
        f"{thesis.tv_gauss_shift(lam * MU, MU):.3f}" for lam in (0.0, 0.5, 1.0)))

    reps = 80
    cells = {"no weights (lam = 0)": cell("none", reps, rng), "tempered weights (lam = 0.5)": cell("tempered", reps, rng),
             "exact weights (lam = 1)": cell("oracle", reps, rng), "estimated weights": cell("estimated", reps, rng)}
    for name, c in cells.items():
        lab.row(name, f"coverage {c['cov']:.3f} ± {c['se']:.3f}   bound {c['bound']:.3f}   infinite intervals {c['inf']:.2%}")
        assert c["cov"] >= c["bound"] - 3 * c["se"], f"{name}: coverage is not below the theorem's bound"
    flat = cell("none", reps, rng, gamma=0.0)
    lab.row("no weights, scores independent of x (gamma = 0)", f"coverage {flat['cov']:.3f} ± {flat['se']:.3f}   bound {flat['bound']:.3f}")
    lab.note = ("Coverage stays above nominal minus the total variation between the reweighted source and the "
                "target; the bound is a floor, not a prediction, and it is loosest when the scores ignore x.")
    none, half, exact, est = cells.values()
    assert none["cov"] < 0.75 < half["cov"] < exact["cov"] + 0.02, "coverage rises as the weights approach the truth"
    assert abs(exact["cov"] - 0.9) < 0.03 and abs(est["cov"] - 0.9) < 0.04, "exact and estimated weights restore about 90%"
    assert est["bound"] < 0.9 and abs(exact["bound"] - 0.9) < 1e-6, "estimated weights pay a TV penalty in the bound"
    assert abs(flat["cov"] - 0.9) < 0.02 and flat["bound"] < 0.55, "with scores independent of x no weights are needed"

    fig, ax = labs.figure(2, size=(11, 4.2))
    lam = np.linspace(0, 1.3, 131)
    ax[0].plot(lam, [thesis.coverage_bound(ALPHA, MU, v) for v in lam], color=labs.RED, label="bound: 0.9 - TV(N(lam mu, 1), N(mu, 1))")
    ax[0].errorbar([0, 0.5, 1], [none["cov"], half["cov"], exact["cov"]], yerr=[2 * none["se"], 2 * half["se"], 2 * exact["se"]],
                   fmt="o", color=labs.BLUE, capsize=3, label=f"simulated coverage ± 2 SE ({reps} replicates)")
    ax[0].errorbar([1.12], [est["cov"]], yerr=[2 * est["se"]], fmt="s", color=labs.GREEN, capsize=3, label="estimated weights (drawn beside lam = 1)")
    ax[0].axhline(0.9, color=labs.MUTED, ls="--", lw=1.2, label="nominal 90%")
    ax[0].set(title="Coverage under a shift of one sd, noise growing with x", xlabel="temper lam of the weights exp(lam mu x)",
              ylabel="coverage on the target", ylim=(0.45, 1.0))
    ax[0].legend(loc="lower right")
    x = np.linspace(-3.5, 4.5, 400)
    src, mid, tgt = stats.norm.pdf(x), stats.norm.pdf(x, 0.5 * MU), stats.norm.pdf(x, MU)
    ax[1].plot(x, src, color=labs.BLUE, label="source N(0, 1)")
    ax[1].plot(x, mid, color=labs.GOLD, label="source reweighted with lam = 0.5")
    ax[1].plot(x, tgt, color=labs.GREEN, label="target N(1, 1)")
    ax[1].fill_between(x, mid, tgt, where=tgt > mid, color=labs.RED, alpha=0.35,
                       label=f"TV = {thesis.tv_gauss_shift(0.5 * MU, MU):.3f}")
    ax[1].set(title="The penalty: what the weights fail to move", xlabel="x", ylabel="density", ylim=(0, 0.62))
    ax[1].legend(loc="upper left", ncols=2)
    lab.fig = fig
    return lab
