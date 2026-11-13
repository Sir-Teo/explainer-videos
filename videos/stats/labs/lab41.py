"""Lab 41: lose 40% of an outcome at random given a covariate, and compare three ways of estimating its mean."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import mi

TITLE = "Complete cases, one imputation, and Rubin's rules"
GOAL = ("Simulate 500 samples of n = 300 with y = 1 + x + noise, hide y for 40% of rows with a probability that rises "
        "with x (missing at random), and compare the complete-case mean, a single regression imputation with its "
        "naive standard error, and multiple imputation (m = 10) pooled by Rubin's rules: bias, and coverage of 90% "
        "intervals.")
TASKS = [
    "Change the mask to kind 'mnar' with y itself as the driver. Which of the three methods still covers?",
    "Set m = 2, then m = 50. How do the interval's width and the fraction of missing information change?",
    "Replace kind='proper' by kind='stochastic' in the imputations (no draw of beta and sigma). What happens to coverage?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps, m, mu, rate = 300, 500, 10, 1.0, 0.4
    z = stats.norm.ppf(0.95)
    names = ("complete cases", "single imputation", "multiple imputation")
    est = {k: np.empty(reps) for k in names}
    se = {k: np.empty(reps) for k in names}
    cover = {k: np.empty(reps, bool) for k in names}
    fmi = np.empty(reps)
    for r in range(reps):
        x = rng.standard_normal(n)
        y = mu + x + rng.standard_normal(n)
        miss = mi.mask("mar", n, rate, rng, driver=x)["miss"]
        y_obs = np.where(miss, np.nan, y)
        cc = y[~miss]
        single = mi.impute_norm(y_obs, x, rng, kind="mean")
        draws = [mi.impute_norm(y_obs, x, rng, kind="proper") for _ in range(m)]
        pooled = mi.rubin([d.mean() for d in draws], [d.var(ddof=1) / n for d in draws], level=0.90)
        fmi[r] = pooled["fmi"]
        for k, e, s, ci in (("complete cases", cc.mean(), cc.std(ddof=1) / np.sqrt(len(cc)), None),
                            ("single imputation", single.mean(), single.std(ddof=1) / np.sqrt(n), None),
                            ("multiple imputation", pooled["est"], pooled["se"], pooled["ci"])):
            est[k][r], se[k][r] = e, s
            lo, hi = ci if ci is not None else (e - z * s, e + z * s)
            cover[k][r] = lo < mu < hi

    lab = labs.Lab()
    for k in names:
        lab.row(k, f"mean {est[k].mean():.3f} (truth {mu:.0f})   sd {est[k].std(ddof=1):.3f}   "
                   f"mean SE {se[k].mean():.3f}   90% CI covers {cover[k].mean():.1%}")
    lab.row("fraction of missing information (MI)", f"{fmi.mean():.2f}")
    lab.note = ("Complete cases are biased because the rows that remain have smaller x. Imputing from the regression "
                "removes the bias, but one imputation treated as data claims a standard error that is too small; "
                "Rubin's between-imputation variance puts the missing uncertainty back.")
    cc, single, multi = names
    assert est[cc].mean() < mu - 0.2 and cover[cc].mean() < 0.2, "complete cases are biased under MAR"
    assert abs(est[single].mean() - mu) < 0.02 and abs(est[multi].mean() - mu) < 0.02, "imputation removes the bias"
    assert se[single].mean() / est[single].std(ddof=1) < 0.85 and cover[single].mean() < 0.84, "one imputation is overconfident"
    assert abs(se[multi].mean() / est[multi].std(ddof=1) - 1) < 0.12 and abs(cover[multi].mean() - 0.90) < 0.04, "Rubin's rules cover"

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = rng.standard_normal(n)
    y = mu + x + rng.standard_normal(n)
    miss = mi.mask("mar", n, rate, rng, driver=x)["miss"]
    ax[0].scatter(x[~miss], y[~miss], s=12, color=labs.BLUE, alpha=0.8, label="observed")
    ax[0].scatter(x[miss], y[miss], s=12, color=labs.RED, alpha=0.5, marker="x", label="hidden (missing at random given x)")
    ax[0].axhline(y[~miss].mean(), color=labs.BLUE, ls="--", lw=1.2, label="complete-case mean")
    ax[0].axhline(mu, color=labs.INK, ls="--", lw=1.2, label="true mean")
    ax[0].set(title="One sample: rows with large x are hidden more often", xlabel="x (always seen)", ylabel="y")
    ax[0].legend(loc="upper left")
    colors = (labs.RED, labs.ORANGE, labs.GREEN)
    for i, (k, color) in enumerate(zip(names, colors)):
        ax[1].bar(i, 100 * cover[k].mean(), color=color, width=0.6)
        ax[1].text(i, 100 * cover[k].mean() + 2, f"{cover[k].mean():.1%}", ha="center", fontsize=9)
    ax[1].axhline(90, color=labs.INK, ls="--", lw=1)
    ax[1].set_axisbelow(True)
    ax[1].set_xticks(range(3))
    ax[1].set_xticklabels(["complete cases", "one regression\nimputation, naive SE", "multiple imputation,\nRubin's rules"])
    ax[1].set(title="Coverage of 90% intervals for the mean (dashed: 90%)", ylabel="coverage over 500 samples (%)", ylim=(0, 105))
    lab.fig = fig
    return lab
