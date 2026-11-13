"""Lab 33: run Benjamini-Hochberg on a thousand studies, and see that the rate it controls is an average."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import multiple

TITLE = "The false discovery rate is pi0 times q, on average"
GOAL = ("Simulate 1,000 studies of 1,000 one-sided tests (900 nulls, 100 effects of 2.5) and apply Benjamini-Hochberg "
        "at q = 0.1: check that the mean false discovery proportion is pi0 q when the tests are independent, and see "
        "how one shared factor spreads the proportion without raising its mean.")
TASKS = [
    "Call fdp_sim with method='by'. How much power does protection against arbitrary dependence cost here?",
    "Estimate pi0 with multiple.storey_pi0 and run BH at q / pi0-hat. Does the FDR rise from 0.09 to 0.10?",
    "Lower the effect from 2.5 to 1.5. What happens to the power, and to the chance that a study's FDP exceeds 0.2?",
]

M, PI0, EFFECT, Q = 1000, 0.9, 2.5, 0.1


def run(seed=0):
    rng = np.random.default_rng(seed)
    reps = 1000
    lab = labs.Lab()
    m0 = int(PI0 * M)

    # no correction: call every p < q a discovery
    V, R = [], []
    for _ in range(reps):
        z = rng.standard_normal(M)
        z[m0:] += EFFECT
        hit = stats.norm.sf(z) < Q
        V.append(hit[:m0].sum())
        R.append(hit.sum())
    fdr_raw = float(np.mean(np.array(V) / np.maximum(R, 1)))
    ev, es = m0 * Q, (M - m0) * stats.norm.sf(stats.norm.isf(Q) - EFFECT)
    lab.row("no correction (each p < 0.1): mean FDP", f"{fdr_raw:.3f}   (expected about {ev / (ev + es):.3f})")

    ind = multiple.fdp_sim(M, PI0, EFFECT, 0.0, Q, reps, rng)
    dep = multiple.fdp_sim(M, PI0, EFFECT, 0.5, Q, reps, rng)
    for name, r in (("independent", ind), ("correlated 0.5", dep)):
        lab.row(f"BH, {name}: mean FDP", f"{r['fdr']:.3f}   (theory {'= ' if r is ind else '<= '}{PI0 * Q:.3f})")
        lab.row(f"BH, {name}: P(FDP > 0.2), P(no discoveries)", f"{r['p_fdp_gt_2q']:.1%}, {r['p_zero']:.1%}")
        lab.row(f"BH, {name}: discoveries, mean and SD", f"{r['R'].mean():.0f}, {r['R'].std():.0f}")
    se = ind["fdp"].std(ddof=1) / np.sqrt(reps)
    assert abs(fdr_raw - ev / (ev + es)) < 0.02 and fdr_raw > 0.4, "uncorrected, half the discoveries are false"
    assert abs(ind["fdr"] - PI0 * Q) < 4 * se, "BH's FDR is pi0 q under independence"
    assert dep["fdr"] < PI0 * Q + 0.01, "positive dependence does not break the bound"
    assert ind["p_fdp_gt_2q"] < 0.03 < 0.05 < dep["p_fdp_gt_2q"], "but one study's FDP can be far from the average"
    assert dep["R"].std() > 4 * ind["R"].std() and dep["p_zero"] > 0.1
    lab.note = ("BH holds the average share of false discoveries at pi0 q = 0.09. Under a shared factor the average is "
                "lower still, but one study in ten has more than 20% false discoveries and one in five finds nothing.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    z = rng.standard_normal(M)
    z[m0:] += EFFECT
    p = stats.norm.sf(z)
    o = np.argsort(p)
    k = multiple.bh(p, Q)["k"]
    show = 160
    rank = np.arange(1, show + 1)
    null = o[:show] < m0
    ax[0].plot(rank[~null], p[o[:show]][~null], ".", color=labs.BLUE, label="real effects")
    ax[0].plot(rank[null], p[o[:show]][null], ".", color=labs.RED, label="true nulls")
    ax[0].plot(rank, Q * rank / M, color=labs.GOLD, label="the BH line  q i / m")
    ax[0].axvline(k, color=labs.MUTED, ls="--", label=f"last p-value under the line: {k} discoveries")
    ax[0].set(title="One study: the 160 smallest of 1,000 p-values", xlabel="rank i", ylabel="p-value")
    ax[0].legend(loc="upper left")
    bins = np.linspace(0, 1, 41)
    ax[1].hist(ind["fdp"], bins=bins, color=labs.BLUE, alpha=0.7, label=f"independent (mean {ind['fdr']:.3f})")
    ax[1].hist(dep["fdp"], bins=bins, color=labs.ORANGE, alpha=0.6, label=f"correlated 0.5 (mean {dep['fdr']:.3f})")
    ax[1].axvline(PI0 * Q, color=labs.GOLD, ls="--", label="pi0 q = 0.09")
    ax[1].set(title="The false discovery proportion in 1,000 studies", xlabel="FDP of one study", ylabel="studies",
              yscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
