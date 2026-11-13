"""Lab 30: replay Tukey's duel between two measures of spread, then contaminate a sample and see which estimates survive."""

import numpy as np
from scipy import optimize

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import robust

TITLE = "A little contamination: efficiency, variance and breakdown"
GOAL = ("Under Tukey's contaminated normal (1 - eps) N(0, 1) + eps N(0, 9), compare the standard deviation with the mean "
        "absolute deviation by formula and by simulation. Then estimate a centre under 5% contamination with the mean, "
        "the median and Huber's estimator, and find the breakdown point of each estimate on Newcomb's data.")
TASKS = [
    "Change Huber's k from 1.345 to robust.huber_k(0.05) = 1.398 and then to 0.5 and 3. Which k gives the smallest variance at 5%?",
    "Add robust.m_location(x, 'biweight') to the three estimators. Does a redescending psi beat Huber when the contaminant is N(0, 10^2)?",
    "Make the contamination one-sided (add 10 instead of multiplying by 10). Which estimates are now biased, and by how much?",
]


def duel(eps):
    """Asymptotic relative efficiency of the mean absolute deviation d to the standard deviation s (Tukey 1960)."""
    m2, m4, m1 = 1 + 8 * eps, 3 + 240 * eps, np.sqrt(2 / np.pi) * (1 + 2 * eps)
    return ((m4 / m2 ** 2 - 1) / 4) / ((m2 - m1 ** 2) / m1 ** 2)


def contaminated(rng, shape, eps, scale):
    return rng.standard_normal(shape) * np.where(rng.random(shape) < eps, scale, 1.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Tukey's duel: s against d.
    even = optimize.brentq(lambda e: duel(e) - 1, 1e-6, 0.05)
    lab.row("ARE(d : s) at eps = 0, 0.01, 0.05, by formula", f"{duel(0):.3f}, {duel(0.01):.2f}, {duel(0.05):.2f}   (film: 0.876, 1.44, 2.03)")
    lab.row("the two break even at eps =", f"{even:.4f}, one gross error in {1 / even:.0f}   (film: 0.0018, 1 in 570)")
    assert abs(duel(0) - 0.876) < 1e-3 and abs(duel(0.01) - 1.44) < 0.01 and abs(duel(0.05) - 2.03) < 0.01
    assert abs(even - 0.0018) < 1e-4
    n, reps, sim = 100, 4000, {}
    for eps in (0.0, 0.05):
        x = contaminated(rng, (reps, n), eps, 3.0)
        s = x.std(axis=1, ddof=1)
        d = np.abs(x - x.mean(axis=1, keepdims=True)).mean(axis=1)
        sim[eps] = (s.var() / s.mean() ** 2) / (d.var() / d.mean() ** 2)
    lab.row("the same ratio simulated at n = 100: eps = 0, 0.05", f"{sim[0.0]:.2f}, {sim[0.05]:.2f}")
    assert abs(sim[0.0] - duel(0)) < 0.08 and sim[0.05] > 1.5, "five gross errors in a hundred reverse the ranking"

    # 2. Location under 5% contamination by N(0, 10^2): n times the variance of each estimate.
    eps, reps2 = 0.05, 2000
    x = contaminated(rng, (reps2, n), eps, 10.0)
    est = {"mean": x.mean(axis=1), "median": np.median(x, axis=1),
           "Huber": np.array([robust.m_location(row, "huber")["mu"] for row in x])}
    nvar = {k: n * v.var() for k, v in est.items()}
    huber_theory = robust.contaminated_variance(lambda t: robust.psi_huber(t, 1.345), eps, 10.0)
    lab.row("n Var of the mean at 5% contamination", f"{nvar['mean']:.2f}   (theory 0.95 + 0.05 x 100 = 5.95)")
    lab.row("n Var of the median", f"{nvar['median']:.2f}   (film: 1.72)")
    lab.row("n Var of Huber's estimate, k = 1.345", f"{nvar['Huber']:.2f}   (known-scale theory {huber_theory:.2f})")
    assert abs(nvar["mean"] / 5.95 - 1) < 0.2 and abs(nvar["median"] / 1.72 - 1) < 0.2
    assert nvar["Huber"] < nvar["median"] < nvar["mean"] and abs(nvar["Huber"] / huber_theory - 1) < 0.2

    # 3. Breakdown on Newcomb's 64 clean passage times: replace m points by a huge value.
    clean = np.sort(museum.newcomb())[2:]
    bd = {"mean": robust.empirical_breakdown(np.mean, clean), "Hodges-Lehmann": robust.empirical_breakdown(robust.hodges_lehmann, clean),
          "median": robust.empirical_breakdown(np.median, clean)}
    lab.row("breakdown on Newcomb's 64: mean, Hodges-Lehmann, median",
            f"{bd['mean'] * 64:.0f}, {bd['Hodges-Lehmann'] * 64:.0f}, {bd['median'] * 64:.0f} points   (film: 1, 19, 32)")
    assert bd["mean"] == 1 / 64 and bd["median"] == 0.5
    assert abs(bd["Hodges-Lehmann"] - (1 - 1 / np.sqrt(2))) < 1 / 64, "Hodges-Lehmann breaks down at 1 - 1/sqrt(2)"
    lab.note = ("The classical estimates are the most efficient at the exact normal and the first to fail away from it: "
                "two gross errors in a thousand are enough to reverse Tukey's duel, and one point can carry the mean anywhere.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    e = np.linspace(0, 0.1, 200)
    ax[0].plot(e, duel(e), color=labs.GOLD, label="ARE(d : s), asymptotic")
    ax[0].plot(list(sim), list(sim.values()), "o", color=labs.BLUE, label="simulated, n = 100")
    ax[0].axhline(1, color=labs.MUTED, ls="--")
    ax[0].axvline(even, color=labs.RED, lw=0.9, ls=":", label=f"break-even at eps = {even:.4f}")
    ax[0].set(title="Tukey's duel: mean absolute deviation against s", xlabel="share eps of N(0, 9) contamination",
              ylabel="efficiency of d relative to s")
    ax[0].legend()
    bins = np.linspace(-0.7, 0.7, 57)
    for name, color in (("mean", labs.RED), ("median", labs.BLUE), ("Huber", labs.GOLD)):
        ax[1].hist(est[name], bins=bins, density=True, histtype="step", lw=1.6, color=color,
                   label=f"{name}: n Var = {nvar[name]:.2f}")
    ax[1].set(title="Estimates of a centre of 0, 5% contamination", xlabel="estimate (n = 100)", ylabel="density")
    ax[1].legend()
    lab.fig = fig
    return lab
