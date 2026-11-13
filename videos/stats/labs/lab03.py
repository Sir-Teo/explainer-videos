"""Lab 3: the horse kicks against Poisson's formula, and how fast many rare chances become a Poisson."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import limits

TITLE = "The law of rare events, with Le Cam's bound"
GOAL = ("Compare Bortkiewicz's 200 corps-years with 200 x Poisson(0.61), then measure the exact total variation "
        "distance between a sum of rare Bernoulli trials and a Poisson, with equal and with unequal chances, against "
        "Le Cam's bound: the sum of the squared chances.")
TASKS = [
    "Give a tenth of the 600 soldiers ten times the risk of the rest, keeping the total at 0.61. How much does the "
    "distance to the Poisson grow, and does Le Cam's bound still hold?",
    "Make the kicks contagious: draw each corps-year's rate from a gamma distribution with mean 0.61. Compare the "
    "variance of the counts with their mean.",
    "Replace lambda = 2 by lambda = 0.61 in the right-hand panel. Does the distance still fall like 1 / n?",
]


def bernoulli_sum_pmf(ps) -> np.ndarray:
    """The exact distribution of a sum of independent Bernoulli(p_i): one convolution per trial."""
    pmf = np.array([1.0])
    for p in ps:
        pmf = np.convolve(pmf, [1 - p, p])
    return pmf


def tv_to_poisson(pmf, lam) -> float:
    k = np.arange(len(pmf))
    return float(0.5 * (np.abs(pmf - stats.poisson.pmf(k, lam)).sum() + stats.poisson.sf(k[-1], lam)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Bortkiewicz's horse kicks against 200 x Poisson(lambda).
    k, counts = np.array(museum.HORSEKICK_K), np.array(museum.HORSEKICK_N)
    total = counts.sum()
    lam = (k * counts).sum() / total
    var = ((k - lam) ** 2 * counts).sum() / (total - 1)
    expected = total * stats.poisson.pmf(k, lam)
    expected[-1] = total * stats.poisson.sf(k[-2], lam)  # 4 or more
    lab.row("corps-years with 0, 1, 2, 3, 4 deaths", "  ".join(str(c) for c in counts))
    lab.row("200 x Poisson(0.61)", "  ".join(f"{e:.1f}" for e in expected))
    lab.row("mean and variance of the counts", f"{lam:.3f} and {var:.3f}   (a Poisson's are equal)")
    obs3 = np.append(counts[:3], counts[3:].sum())  # pool 3 and more, so every expected count is near 5 or above
    exp3 = np.append(expected[:3], expected[3:].sum())
    chi2 = ((obs3 - exp3) ** 2 / exp3).sum()
    pval = stats.chi2.sf(chi2, len(obs3) - 2)
    lab.row("chi-squared distance from the Poisson", f"{chi2:.2f} on 2 df   (p = {pval:.2f})")
    assert abs(lam - 0.61) < 1e-9 and abs(var - lam) < 0.01, "mean and variance both round to 0.61"
    assert np.allclose(expected, [108.7, 66.3, 20.2, 4.1, 0.7], atol=0.06), "the film's table"
    assert pval > 0.2, "the horse kicks are consistent with a Poisson"

    # 2. Equal chances: Binomial(n, lambda / n) against Poisson(lambda), exactly.
    lam2 = 2.0
    ns = np.unique(np.round(np.logspace(np.log10(4), 4, 40)).astype(int))
    tv = np.array([limits.tv_binomial_poisson(int(n), lam2 / n) for n in ns])
    bound = np.array([limits.le_cam_bound(np.full(int(n), lam2 / n)) for n in ns])
    tv4, tv1000 = limits.tv_binomial_poisson(4, 0.5), limits.tv_binomial_poisson(1000, 0.002)
    lab.row("TV(Binomial(4, 1/2), Poisson(2))", f"{tv4:.3f}   Le Cam's bound {min(1.0, lam2 ** 2 / 4):.3f}")
    lab.row("TV(Binomial(1000, 1/500), Poisson(2))", f"{tv1000:.5f}   Le Cam's bound {lam2 ** 2 / 1000:.5f}")
    slope = np.polyfit(np.log(ns[ns >= 100]), np.log(tv[ns >= 100]), 1)[0]
    lab.row("log-log slope of the distance for n >= 100", f"{slope:.3f}   (1 / n would be -1)")
    assert abs(tv4 - 0.174) < 0.001 and abs(tv1000 - 0.0005) < 0.0001, "the film's two distances"
    assert np.all(tv <= bound), "Le Cam's bound holds at every n"
    assert abs(slope + 1) < 0.02, "the distance falls like 1 / n"

    # 3. Unequal chances: 600 soldiers whose risks differ, summing to 0.61.
    raw = rng.gamma(0.5, 1.0, 600)  # a few careless riders carry much of the risk
    ps = 0.61 * raw / raw.sum()
    pmf = bernoulli_sum_pmf(ps)
    tv_unequal, bound_unequal = tv_to_poisson(pmf, ps.sum()), limits.le_cam_bound(ps)
    tv_equal = limits.tv_binomial_poisson(600, 0.61 / 600)
    lab.row("600 unequal risks summing to 0.61: TV", f"{tv_unequal:.5f}   Le Cam's bound {bound_unequal:.5f}   (equal risks: {tv_equal:.5f})")
    assert tv_equal < tv_unequal <= bound_unequal, "unequal risks are further from the Poisson, but inside the bound"
    assert bound_unequal < 0.02, "and still close: the count is nearly Poisson"
    simulated = (rng.random((200, 600)) < ps).sum(1)  # one simulated table of 200 corps-years
    sim_counts = np.array([(simulated == j).sum() for j in range(4)] + [(simulated >= 4).sum()])
    lab.note = ("Rare, independent chances add up to a Poisson whether or not they are equal: the distance is at most "
                "the sum of the squared chances, and for equal chances it falls like 1 / n.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].bar(k - 0.2, counts, width=0.4, color=labs.BLUE, alpha=0.8, label="Bortkiewicz's 200 corps-years")
    ax[0].bar(k + 0.2, sim_counts, width=0.4, color=labs.TEAL, alpha=0.6, label="one simulation, 600 unequal risks")
    ax[0].plot(k, expected, "o", color=labs.GOLD, ms=8, label="200 x Poisson(0.61)")
    ax[0].set(title="Deaths by horse kick per corps per year", xlabel="deaths (the last bar is 4 or more)",
              ylabel="corps-years", xticks=k)
    ax[0].legend()
    ax[1].loglog(ns, tv, color=labs.BLUE, label="exact TV, Binomial(n, 2/n) to Poisson(2)")
    ax[1].loglog(ns, np.minimum(bound, 1), color=labs.GOLD, label="Le Cam's bound, 4 / n")
    ax[1].set(title="How fast the binomial becomes a Poisson", xlabel="number of trials n",
              ylabel="total variation distance")
    ax[1].legend()
    lab.fig = fig
    return lab
