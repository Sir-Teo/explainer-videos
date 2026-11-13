"""Lab 42: test Case 1's analysis plan by simulation: randomize towns, then analyse adults or towns."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import causal, ols

TITLE = "A cluster trial analysed two ways"
GOAL = ("Simulate 1,500 trials of 42 towns of 50 adults (town effects of sd 3.8 mm Hg, adults of sd 16, so an "
        "intraclass correlation of 0.054), randomize 21 towns to treatment, and compare the individual-level and "
        "the cluster-level analyses: their type I error with no effect, and the cluster analysis's power for a fall "
        "of 4 mm Hg, each against its formula.")
TASKS = [
    "Use 8 towns per arm of 130 adults (about the same number of adults). What is the real power of the cluster analysis?",
    "Set the town sd to 0 (no clustering). Do the two analyses now agree, and which has more power?",
    "Add each town's pilot mean (its town effect plus noise of sd 16/sqrt(30)) as a covariate in a cluster-level regression and measure the gain in power.",
]

K, M, SD_TOWN, SD_ADULT, DELTA = 21, 50, float(np.hypot(3.5, 1.5)), 16.0, -4.0


def run(seed=0):
    rng = np.random.default_rng(seed)
    reps, towns = 1500, 2 * K
    cluster = np.repeat(np.arange(towns), M)
    rho = SD_TOWN ** 2 / (SD_TOWN ** 2 + SD_ADULT ** 2)
    de = causal.design_effect(M, rho)
    tcrit = stats.t.ppf(0.975, towns - 2)
    z_naive, t_clu, t_clu_alt, icc_hat = (np.empty(reps) for _ in range(4))
    for r in range(reps):
        y = 130 + np.repeat(SD_TOWN * rng.standard_normal(towns), M) + SD_ADULT * rng.standard_normal(towns * M)
        zc = np.zeros(towns, bool)
        zc[rng.choice(towns, K, replace=False)] = True
        null = causal.cluster_diff(y, zc, cluster)
        alt = causal.cluster_diff(y + DELTA * zc[cluster], zc, cluster)
        z_naive[r] = null["naive"]["est"] / null["naive"]["se"]
        t_clu[r] = null["cluster"]["est"] / null["cluster"]["se"]
        t_clu_alt[r] = alt["cluster"]["est"] / alt["cluster"]["se"]
        icc_hat[r] = ols.icc(y, cluster)
    size_naive, size_clu = np.mean(np.abs(z_naive) > 1.96), np.mean(np.abs(t_clu) > tcrit)
    power = np.mean(np.abs(t_clu_alt) > tcrit)
    size_theory = 2 * stats.norm.cdf(-1.96 / np.sqrt(de))  # the naive SE is too small by the factor sqrt(DE)
    se_clu = np.sqrt(2 * (SD_TOWN ** 2 + SD_ADULT ** 2 / M) / K)
    power_theory = stats.nct.sf(tcrit, towns - 2, abs(DELTA) / se_clu) + stats.nct.cdf(-tcrit, towns - 2, abs(DELTA) / se_clu)

    lab = labs.Lab()
    lab.row("intraclass correlation", f"{icc_hat.mean():.3f} estimated on average   (truth {rho:.3f})")
    lab.row("design effect 1 + (m - 1) rho", f"{de:.2f}")
    lab.row("type I error, adults as independent", f"{size_naive:.1%}   (formula {size_theory:.1%}; nominal 5%)")
    lab.row("type I error, town means", f"{size_clu:.1%}   (nominal 5%)")
    lab.row("power for -4 mm Hg, town means", f"{power:.1%}   (noncentral t {power_theory:.1%})")
    lab.note = ("Adults in one town share its effect, so 2,100 adults carry the information of about 2,100 / DE: "
                "the individual-level analysis rejects a true null about six times too often, and the analysis of "
                "town means has the size and the power the plan promised.")
    assert abs(icc_hat.mean() - rho) < 0.006, "the ANOVA estimator recovers the ICC"
    assert abs(size_naive - size_theory) < 0.04 and size_naive > 0.2, "the naive size is 2 Phi(-1.96 / sqrt(DE))"
    assert abs(size_clu - 0.05) < 0.02, "the cluster-level t test has size 5%"
    assert abs(power - power_theory) < 0.04, "its power matches the noncentral t"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-6, 6, 61)
    grid = np.linspace(-6, 6, 300)
    ax[0].hist(z_naive, bins=bins, density=True, color=labs.RED, alpha=0.55, label="adults as independent")
    ax[0].hist(t_clu, bins=bins, density=True, color=labs.GREEN, alpha=0.55, label="town means")
    ax[0].plot(grid, stats.norm.pdf(grid), color=labs.INK, lw=1.2, label="standard normal")
    for c in (-1.96, 1.96):
        ax[0].axvline(c, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="Test statistics when the programme does nothing", xlabel="estimate / its standard error", ylabel="density")
    ax[0].legend()
    m = np.arange(5, 501)
    base = 2 * (1.96 + 0.84) ** 2 * SD_ADULT ** 2 * (1 + (SD_TOWN / SD_ADULT) ** 2) / DELTA ** 2  # adults per arm if independent
    need = base * (1 + (m - 1) * rho) / m
    ax[1].plot(m, need, color=labs.GOLD, label="towns per arm for 80% power")
    ax[1].axhline(base * rho, color=labs.MUTED, ls="--", lw=1, label=f"floor as m grows: {base * rho:.1f}")
    ax[1].plot([M], [base * (1 + (M - 1) * rho) / M], "o", color=labs.BLUE, label=f"m = {M}: {base * (1 + (M - 1) * rho) / M:.1f}")
    ax[1].set(title="More adults per town cannot replace towns", xlabel="adults measured per town (m)",
              ylabel="towns per arm", xscale="log", ylim=(0, 80))
    ax[1].set_xticks([5, 10, 20, 50, 100, 200, 500])
    ax[1].set_xticklabels(["5", "10", "20", "50", "100", "200", "500"])
    ax[1].minorticks_off()
    ax[1].legend()
    lab.fig = fig
    return lab
