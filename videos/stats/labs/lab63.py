"""Lab 63: attack a noisy mean as a hypothesis test, then build an interval that knows about the noise."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import privacy

TITLE = "Privacy as a test, and its cost in coverage"
GOAL = ("Release a mean with Gaussian noise and let an attacker test whether one person's record is in it: the "
        "attack's error rates should trace the Gaussian trade-off curve. Then release a proportion with Laplace "
        "noise and compare the interval that ignores the noise with the one that adds its variance.")
TASKS = [
    "Compose the Gaussian release k = 4 times with the same noise. Check that the best attack on all four follows "
    "the curve with mu doubled, not multiplied by 4.",
    "Replace the central Laplace release by randomized response (privacy.randomized_response, privacy.rr_debias) and "
    "compare the two mean squared errors with privacy.mean_mse_central_local.",
    "Set n = 100 and eps = 0.05, where the noisy proportion often leaves [0, 1]. What does clipping it do to the "
    "noise-aware interval's coverage?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. membership inference against a noisy mean is a test of N(0, 1) against N(mu, 1)
    n, mu = 100, 1.0
    roc = privacy.membership_attack_roc(n, (1 / n) / mu, 20000, rng)
    alpha, beta = roc["fpr"], 1 - roc["tpr"]
    theory = privacy.tradeoff_gaussian(alpha, roc["mu"])
    gap = float(np.max(np.abs(beta - theory)))
    at = int(np.argmin(np.abs(alpha - 0.05)))
    lab.row("attack at type I error 5%: type II error", f"{beta[at]:.3f}   (Gaussian trade-off curve, mu = 1: {theory[at]:.3f})")
    lab.row("largest gap between the attack and the curve", f"{gap:.3f}")
    assert abs(roc["mu"] - mu) < 1e-12 and gap < 0.02, "the best attack traces the mu-GDP trade-off curve"

    # 2. the Laplace mechanism is eps-DP: its exact trade-off curve never goes below the eps-DP bound, and touches it
    a = np.linspace(0.001, 0.999, 999)
    for eps in (0.3, 2.0, 1.0):
        slack = privacy.tradeoff_laplace(a, eps) - privacy.tradeoff_eps_delta(a, eps)
        assert slack.min() > -1e-9 and slack.min() < 1e-6, "Laplace noise meets the eps-DP bound with equality somewhere"
    lab.row("Laplace against the eps-DP bound, eps = 1", f"smallest slack {slack.min():.1e}, largest {slack.max():.3f}")

    # 3. a confidence interval for a proportion released with Laplace noise
    n, p, reps = 1000, 0.3, 1500
    grid = (0.05, 0.1, 0.2, 0.5, 1.0, 2.0)
    cover = {}
    for eps in grid:
        hit = np.zeros(2)
        for _ in range(reps):
            out = privacy.private_proportion(rng.random(n) < p, eps, rng)
            hit += [out["naive"][0] <= p <= out["naive"][1], out["aware"][0] <= p <= out["aware"][1]]
        cover[eps] = hit / reps
        share = (2 / (n * eps) ** 2) / (2 / (n * eps) ** 2 + p * (1 - p) / n)
        lab.row(f"eps = {eps}: 95% interval covers", f"naive {cover[eps][0]:.1%}   noise-aware {cover[eps][1]:.1%}"
                                                      f"   (privacy's share of the variance {share:.0%})")
    lab.note = ("The attacker's best test is exactly as good as the privacy parameter says, and the analyst's interval "
                "is honest only when it adds the variance of the noise that bought that protection.")
    assert cover[0.1][0] < 0.90 and cover[0.05][0] < 0.75, "ignoring the noise loses coverage at small eps"
    assert all(abs(cover[e][1] - 0.95) < 0.025 for e in grid), "adding the Laplace variance restores it"
    assert abs(cover[2.0][0] - 0.95) < 0.025, "at large eps the noise is negligible"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(alpha, beta, color=labs.BLUE, lw=3, alpha=0.6, label="simulated attack on a noisy mean")
    ax[0].plot(a, privacy.tradeoff_gaussian(a, mu), color=labs.GOLD, ls="--", label="Gaussian trade-off curve, mu = 1")
    ax[0].plot(a, privacy.tradeoff_laplace(a, 1.0), color=labs.GREEN, label="Laplace mechanism, eps = 1")
    ax[0].plot(a, privacy.tradeoff_eps_delta(a, 1.0), color=labs.RED, ls=":", label="eps-DP bound, eps = 1")
    ax[0].plot([0, 1], [1, 0], color=labs.MUTED, lw=1, label="no information: type II = 1 - type I")
    ax[0].set(title="Privacy bounds every test of 'in' against 'out'", xlabel="type I error", ylabel="type II error")
    ax[0].legend()
    x = np.arange(len(grid))
    ax[1].bar(x - 0.2, [cover[e][0] for e in grid], 0.4, color=labs.RED, label="naive Wald interval")
    ax[1].bar(x + 0.2, [cover[e][1] for e in grid], 0.4, color=labs.GREEN, label="noise-aware interval")
    ax[1].axhline(0.95, color=labs.INK, ls="--", lw=1.2, label="nominal 95%")
    ax[1].set(title=f"Coverage for a private proportion, n = {n}", xlabel="privacy parameter eps", ylabel="coverage",
              xticks=x, xticklabels=[str(e) for e in grid], ylim=(0.3, 1.12))
    ax[1].legend(loc="upper center", ncols=3)
    lab.fig = fig
    return lab
