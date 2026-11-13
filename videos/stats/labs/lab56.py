"""Lab 56: report the largest of ten estimates, and compare the Wald, conditional and hybrid intervals for it."""

import numpy as np
from scipy import integrate, stats

from videos.coursekit import labs
from explainer.stats.kit import selective

TITLE = "The winner's curse and the interval that conditions on winning"
GOAL = ("Draw ten independent estimates whose true effects are all zero, report the largest, and measure how often "
        "the usual 95% interval, the conditional (truncated-normal) interval and the hybrid interval cover the "
        "winner's true effect, against the exact values.")
TASKS = [
    "Set K = 100 and then K = 1000. Check the Wald coverage against 0.975^K and the winner's bias against sqrt(2 log K).",
    "Give one effect the true value 4 (mu[0] = 4). How do the conditional interval's length and the Wald coverage change when the win is clear?",
    "Replace the winner by the estimates above a threshold of 2 and build each one's interval with selective.threshold_selective. Is coverage still 95% for each selected effect?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    K, reps, z = 10, 1000, stats.norm.ppf(0.975)
    mu = np.zeros(K)
    win, lead, length = np.empty(reps), np.empty(reps), np.empty(reps)
    cover = {"Wald": 0, "conditional": 0, "hybrid": 0}
    for r in range(reps):
        y = mu + rng.standard_normal(K)
        w = selective.winner_conditional(y)
        h = selective.winner_hybrid(y)
        truth = mu[w["j"]]
        win[r], lead[r], length[r] = w["y"], w["y"] - w["second"], w["hi"] - w["lo"]
        cover["Wald"] += abs(w["y"] - truth) <= z
        cover["conditional"] += w["lo"] <= truth <= w["hi"]
        cover["hybrid"] += h["lo"] <= truth <= h["hi"]
    cover = {k: v / reps for k, v in cover.items()}

    # theory for K nulls: the law of the maximum is Phi^K
    bias = integrate.quad(lambda t: t * K * stats.norm.pdf(t) * stats.norm.cdf(t) ** (K - 1), -8, 10)[0]
    wald = stats.norm.cdf(z) ** K - stats.norm.cdf(-z) ** K
    lab = labs.Lab()
    lab.row("mean of the winner's estimate (truth 0)", f"{win.mean():.3f}   exact {bias:.3f}   bound sqrt(2 log K) = {np.sqrt(2 * np.log(K)):.3f}")
    lab.row("Wald 95% interval covers", f"{cover['Wald']:.1%}   exact 0.975^K - 0.025^K = {wald:.1%}")
    lab.row("conditional interval covers", f"{cover['conditional']:.1%}   theory 95.0%")
    lab.row("hybrid interval covers", f"{cover['hybrid']:.1%}   theory at least 95.0%")
    lab.row("median length", f"Wald {2 * z:.2f}   conditional {np.median(length):.2f}")
    close, clear = length[lead < np.quantile(lead, 0.25)], length[lead > np.quantile(lead, 0.75)]
    lab.row("conditional median length by the lead", f"closest quarter {np.median(close):.1f}   clearest quarter {np.median(clear):.1f}")
    lab.note = ("Selecting the largest of ten estimates biases it upward by a standard deviation and a half and breaks "
                "the Wald interval; conditioning on the win restores 95%, at a price in length that is highest when "
                "the win is narrow.")
    assert abs(win.mean() - bias) < 0.08 and bias < np.sqrt(2 * np.log(K)), "the winner's curse matches the law of the maximum"
    assert abs(cover["Wald"] - wald) < 0.045 and cover["Wald"] < 0.85, "the Wald interval undercovers as 0.975^K predicts"
    assert abs(cover["conditional"] - 0.95) < 0.03, "the truncated-normal interval covers given the win"
    assert cover["hybrid"] > 0.92, "the hybrid interval covers"
    assert np.median(close) > 1.5 * np.median(clear), "a narrow win costs length"

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(-3.5, 4.5, 300)
    ax[0].hist(win, bins=40, density=True, color=labs.BLUE, alpha=0.6, label=f"the winner's estimate, {reps:,} draws")
    ax[0].plot(grid, K * stats.norm.pdf(grid) * stats.norm.cdf(grid) ** (K - 1), color=labs.GOLD, label="law of the maximum of 10")
    ax[0].plot(grid, stats.norm.pdf(grid), color=labs.MUTED, ls="--", label="law of one fixed estimate")
    ax[0].axvline(0, color=labs.RED, lw=1.2)
    ax[0].text(0.05, 0.47, "truth", color=labs.RED, fontsize=9)
    ax[0].set(title="Every true effect is 0; the reported one is not", xlabel="estimate", ylabel="density", ylim=(0, 0.95))
    ax[0].legend(loc="upper left")
    ax[1].scatter(lead, np.clip(length, None, 400), s=7, color=labs.BLUE, alpha=0.5, label="conditional interval")
    ax[1].axhline(2 * z, color=labs.RED, label=f"Wald interval: {2 * z:.2f}, covers {cover['Wald']:.0%}")
    ax[1].set(title="Length of the 95% interval against the winner's lead", xlabel="winner minus runner-up",
              ylabel="interval length (log scale)", yscale="log")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
