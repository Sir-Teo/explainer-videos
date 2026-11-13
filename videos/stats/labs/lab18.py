"""Lab 18: rerun the Literary Digest on the World, and check Meng's identity against a random sample of 1,000."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import survey
from explainer.stats.world import World

TITLE = "A huge biased sample against a small random one"
GOAL = ("Mail a ballot to everyone on the World's telephone-and-car registers, let people answer with their own "
        "propensities, and compare the error of the tens of thousands of returns with Meng's identity and with "
        "two thousand simple random samples of 1,000.")
TASKS = [
    "Mail every adult instead of the registers (drop `listed`). How much of the error was the frame's?",
    "Stratify the random sample by region with proportional allocation (survey.stratified_mean). How much does the SD fall?",
    "Rake the returns to the population's income bands with survey.rake and recompute the error and Kish's n_eff.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    w = World()
    adult = w.adult
    s = w.survey
    y = s["vote_blue"][adult].astype(float)  # 1 = votes Blue
    listed, prop = s["listed"][adult], s["propensity"][adult]
    N, truth = len(y), y.mean()
    lab = labs.Lab()

    # the Digest: a ballot to every listed adult; each returns it with their own propensity
    returned = listed & (rng.random(N) < prop)
    m = survey.meng(y, returned)
    digest = y[returned].mean()
    frame_bias = y[listed].mean() - truth
    n_eff = m["sigma"] ** 2 / m["error"] ** 2  # the SRS size with the same mean squared error
    lab.row("Blue's true share of the adults", f"{truth:.1%}   (N = {N:,})")
    lab.row("the Digest's returns", f"{digest:.1%} from {m['n']:,} ballots   (the listed alone: {truth + frame_bias:.1%})")
    lab.row("Meng: rho x sqrt((1-f)/f) x sigma", f"{m['rho']:.4f} x {np.sqrt((1 - m['f']) / m['f']):.2f} x {m['sigma']:.3f} = "
            f"{m['identity']:+.4f}   (actual error {m['error']:+.4f})")
    lab.row("the returns are worth a random sample of", f"{n_eff:.1f} people")
    assert abs(m["error"] - m["identity"]) < 1e-9, "Meng's identity is exact"
    assert abs(m["error"] - (digest - truth)) < 1e-12 and m["error"] > 0.15, "the Digest is far off, towards Blue"
    assert 0 < frame_bias < m["error"], "the frame explains part of the error, nonresponse the rest"
    assert n_eff < 12 and abs(n_eff - m["n_eff"]) < 0.5, "tens of thousands of ballots are worth a handful of voters"

    # simple random samples of 1,000, without replacement
    n, reps = 1000, 2000
    polls = np.array([y[rng.choice(N, n, replace=False)].mean() for _ in range(reps)])
    sd_theory = np.sqrt((1 - n / N) * y.var(ddof=1) / n)
    one = survey.srs_mean(y[rng.choice(N, n, replace=False)], N)
    cover = np.mean(np.abs(polls - truth) < 1.96 * np.sqrt((1 - n / N) * polls * (1 - polls) / (n - 1)))
    lab.row("2,000 random samples of 1,000: sd", f"{polls.std(ddof=1):.4f}   (theory with the fpc {sd_theory:.4f})")
    lab.row("one random sample of 1,000", f"{one['mean']:.1%}, 95% CI [{one['ci'][0]:.1%}, {one['ci'][1]:.1%}]")
    lab.row("95% intervals that cover the truth", f"{cover:.1%}")
    assert abs(polls.mean() - truth) < 0.002 and abs(polls.std(ddof=1) / sd_theory - 1) < 0.06, "unbiased, with the SRS variance"
    assert 0.93 < cover < 0.97 and m["error"] > 8 * sd_theory, "1,000 random voters beat the Digest by an order of magnitude"
    lab.note = ("The size of a sample multiplies its error only through sqrt((1 - f)/f); a correlation of 0.09 between "
                "answering and voting Blue is enough to make tens of thousands of ballots worth fewer than a dozen random voters.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].hist(100 * polls, bins=40, color=labs.BLUE, alpha=0.7, label="2,000 random samples of 1,000")
    ax[0].axvline(100 * truth, color=labs.GREEN, label=f"truth {truth:.1%}")
    ax[0].axvline(100 * (truth + frame_bias), color=labs.ORANGE, ls="--", label=f"everyone listed {truth + frame_bias:.1%}")
    ax[0].axvline(100 * digest, color=labs.RED, label=f"the Digest's returns {digest:.1%}")
    ax[0].set(title="Blue's share: random samples and the Digest", xlabel="estimate of Blue's share (%)", ylabel="samples",
              xlim=(32, 84))
    ax[0].legend(loc="upper right")
    f = np.logspace(-4, np.log10(0.9), 200)
    for rho, color in ((m["rho"], labs.RED), (0.02, labs.ORANGE), (0.005, labs.GOLD)):
        ax[1].plot(f * N, 100 * rho * np.sqrt((1 - f) / f) * m["sigma"], color=color, label=f"self-selected, rho = {rho:.3f}")
    ax[1].plot(f * N, 100 * np.sqrt((1 - f) / (f * N)) * m["sigma"], color=labs.BLUE, label="random sample: sd")
    ax[1].scatter([m["n"]], [100 * m["error"]], color=labs.RED, zorder=5)
    ax[1].set(xscale="log", yscale="log", title="Error against sample size (Meng's identity)", xlabel="sample size n",
              ylabel="error in Blue's share (points)", ylim=(0.01, 100))
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
