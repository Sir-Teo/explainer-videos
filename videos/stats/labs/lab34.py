"""Lab 34: climb the score ladder: split conformal's coverage, exactly and given the calibration set."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import conformal

TITLE = "Split conformal: what 90% promises"
GOAL = ("With 19 calibration scores take the 18th smallest as the threshold, four thousand times, and compare the "
        "coverage with the quantile lemma's 18/20 and with the Beta(18, 2) law of coverage given the calibration set; "
        "then fit least squares with 20 predictors and compare intervals from in-sample residuals with split conformal.")
TASKS = [
    "Set N_CAL to 99 and to 999. How does the 5%-95% range of the conditional coverage narrow, and what is its Beta law?",
    "Multiply the test noise by 1.5 so calibration and test are no longer exchangeable. What does the 90% become?",
    "Replace split conformal by conformal.jackknife_plus with least squares. Compare its coverage and width with the split.",
]

N_CAL, ALPHA = 19, 0.1


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the ladder: scores |e| with e ~ N(0, 1), so coverage given the threshold q is exactly 2 Phi(q) - 1
    reps = 4000
    k = int(np.ceil((N_CAL + 1) * (1 - ALPHA)))
    q = np.array([conformal.conformal_quantile(np.abs(rng.standard_normal(N_CAL)), ALPHA) for _ in range(reps)])
    cond = 2 * stats.norm.cdf(q) - 1
    hit = np.abs(rng.standard_normal(reps)) <= q
    beta = stats.beta(k, N_CAL + 1 - k)
    lab.row(f"n = {N_CAL}: rank k = ceil((n + 1)(1 - alpha))", f"{k}")
    lab.row("coverage of one new case", f"{hit.mean():.3f}   (theory k/(n + 1) = {k / (N_CAL + 1):.3f})")
    lab.row("coverage given the calibration set, 5% and 95% points",
            f"{np.quantile(cond, 0.05):.3f}, {np.quantile(cond, 0.95):.3f}   (Beta({k}, {N_CAL + 1 - k}): "
            f"{beta.ppf(0.05):.3f}, {beta.ppf(0.95):.3f})")
    ks = stats.kstest(cond, beta.cdf)
    lab.row("Kolmogorov distance of that coverage from the Beta law", f"{ks.statistic:.3f}   (p = {ks.pvalue:.2f})")
    assert abs(cond.mean() - k / (N_CAL + 1)) < 0.004 and abs(hit.mean() - k / (N_CAL + 1)) < 0.02, "the quantile lemma"
    assert 1 - ALPHA <= k / (N_CAL + 1) <= 1 - ALPHA + 1 / (N_CAL + 1)
    assert ks.statistic < 0.035, "coverage given the calibration set is Beta(k, n + 1 - k)"
    assert abs(np.quantile(cond, 0.05) - 0.774) < 0.015 and abs(np.quantile(cond, 0.95) - 0.981) < 0.006

    # 2. a model that overfits: least squares, n = 100 training cases, p = 20 predictors
    n, p, trials, ntest = 100, 20, 400, 200
    cov_in, cov_split, width_in, width_split = [], [], [], []
    for _ in range(trials):
        b = rng.standard_normal(p) / np.sqrt(p)
        X, Xc, Xt = (rng.standard_normal((m, p)) for m in (n, n, ntest))
        y, yc, yt = (Z @ b + rng.standard_normal(len(Z)) for Z in (X, Xc, Xt))
        bh = np.linalg.lstsq(X, y, rcond=None)[0]
        q_in = np.quantile(np.abs(y - X @ bh), 1 - ALPHA)  # residuals of the cases the model was fitted to
        sc = conformal.split_conformal(Xc @ bh, yc, Xt @ bh, ALPHA)  # residuals of 100 cases it never saw
        cov_in.append(np.mean(np.abs(yt - Xt @ bh) <= q_in))
        cov_split.append(np.mean((sc["lo"] <= yt) & (yt <= sc["hi"])))
        width_in.append(2 * q_in)
        width_split.append(2 * sc["q"])
    ci, cs = float(np.mean(cov_in)), float(np.mean(cov_split))
    lab.row("least squares, p = 20, n = 100: in-sample residual band covers", f"{ci:.1%}   (nominal 90%), width {np.mean(width_in):.2f}")
    lab.row("split conformal with 100 fresh calibration cases covers", f"{cs:.1%}   (theory {91 / 101:.1%}), width {np.mean(width_split):.2f}")
    assert ci < 0.84, "in-sample residuals are too small: the band undercovers"
    assert abs(cs - 91 / 101) < 0.012, "split conformal covers ceil(101 * 0.9)/101 whatever the model"
    lab.note = ("The guarantee is exact and marginal: 18/20 on average over calibration sets, but any one calibration "
                "set of 19 gives coverage anywhere from 77% to 98%. Residuals of the training cases give no guarantee.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    s = np.sort(np.abs(np.random.default_rng(seed + 1).standard_normal(N_CAL)))
    colors = [labs.GOLD if i == k - 1 else labs.BLUE for i in range(N_CAL)]
    ax[0].bar(np.arange(1, N_CAL + 1), s, color=colors)
    ax[0].axhline(s[k - 1], color=labs.GOLD, ls="--", label=f"threshold: the {k}th of {N_CAL} scores")
    ax[0].set(title="The score ladder", xlabel="rank of the calibration score", ylabel="score |y - prediction|")
    ax[0].set_xticks([1, 5, 10, 15, 18, 19])
    ax[0].legend(loc="upper left")
    grid = np.linspace(0.6, 1, 300)
    ax[1].hist(cond, bins=np.linspace(0.6, 1, 41), density=True, color=labs.BLUE, alpha=0.6,
               label="4,000 calibration sets of 19")
    ax[1].plot(grid, beta.pdf(grid), color=labs.GOLD, label=f"Beta({k}, {N_CAL + 1 - k})")
    ax[1].axvline(1 - ALPHA, color=labs.MUTED, ls="--", label="nominal 90%")
    ax[1].set(title="Coverage given the calibration set", xlabel="coverage of new cases", ylabel="density")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
