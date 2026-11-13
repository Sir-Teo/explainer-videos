"""Lab 35: re-randomize a trial whose science table is known, and check Neyman's variance and Fisher's test."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import causal

TITLE = "One science table, four thousand coins"
GOAL = ("Fix both potential outcomes of 200 patients, assign 100 to treatment by a coin four thousand times, and compare "
        "the spread of the difference in means with Neyman's exact variance and with the conservative estimate a "
        "real trial can compute; then let a doctor choose who is treated and measure the selection bias.")
TASKS = [
    "Set the effect's SD to 0 (a constant effect). Check that the conservative variance becomes exact and coverage falls to 90%.",
    "Block on the baseline: sort by y0's baseline covariate, randomize within ten blocks, and use causal.blocked. How much smaller is the SD?",
    "Enumerate all 924 assignments of 12 patients with causal.fisher_test (reps=None) under the sharp null. Is the p-value exactly uniform on its grid?",
]

N, N1 = 200, 100


def science(rng, sd_tau):
    """Potential outcomes (systolic pressure, mm Hg): a baseline, an untreated outcome, an effect that varies."""
    base = rng.normal(150, 12, N)
    y0 = 0.7 * (base - 150) + 148 + rng.normal(0, 8, N)
    tau = -8 - 0.25 * (base - 150) * (sd_tau / 4.75) + rng.normal(0, 0.77 * sd_tau, N)  # sicker patients gain more
    return base, y0, y0 + tau


def rerandomize(y0, y1, rng, reps):
    est, se, cover = np.empty(reps), np.empty(reps), 0
    sate = float(np.mean(y1 - y0))
    for r, z in enumerate(causal.complete_assignments(N, N1, rng, reps)):
        d = causal.diff_means(np.where(z, y1, y0), z)
        est[r], se[r] = d["est"], d["se"]
        cover += d["lo"] <= sate <= d["hi"]
    return est, se, cover / reps


def run(seed=0):
    rng = np.random.default_rng(seed)
    reps = 4000
    lab = labs.Lab()
    base, y0, y1 = science(rng, 4.75)
    v = causal.neyman_true_var(y0, y1, N1)
    est, se, cover = rerandomize(y0, y1, rng, reps)
    lab.row("average effect in this table (SATE), SD of the effects", f"{v['ate']:.2f}, {np.sqrt(v['S_tau2']):.2f} mm Hg")
    lab.row("mean of 4,000 randomized estimates", f"{est.mean():.2f}   (unbiased: {v['ate']:.2f})")
    lab.row("SD of the estimates", f"{est.std(ddof=1):.3f}   (Neyman's exact {np.sqrt(v['true']):.3f})")
    lab.row("root mean estimated variance", f"{np.sqrt(np.mean(se ** 2)):.3f}   (conservative {np.sqrt(v['conservative']):.3f})")
    lab.row("90% interval covers the SATE", f"{cover:.1%}   (at least 90%)")
    sd = est.std(ddof=1)
    assert abs(est.mean() - v["ate"]) < 4 * sd / np.sqrt(reps), "the difference in means is unbiased over the coin"
    assert abs(sd / np.sqrt(v["true"]) - 1) < 0.05, "its variance is S1^2/n1 + S0^2/n0 - S_tau^2/n"
    assert abs(np.mean(se ** 2) / v["conservative"] - 1) < 0.02, "the estimator's expectation drops the last term"
    assert v["conservative"] > v["true"] and cover > 0.885, "so intervals are conservative"

    # a doctor instead of a coin: treat the 100 patients with the highest baseline pressure
    zd = base >= np.sort(base)[N - N1]
    naive = causal.diff_means(np.where(zd, y1, y0), zd)["est"]
    att = float(np.mean((y1 - y0)[zd]))
    bias = float(y0[zd].mean() - y0[~zd].mean())
    lab.row("doctor treats the 100 highest baselines: difference in means", f"{naive:.2f}")
    lab.row("  = effect on the treated + selection bias", f"{att:.2f} + {bias:.2f}")
    assert abs(naive - (att + bias)) < 1e-9 and bias > 5, "the identity is exact, and the bias is large"

    # Fisher: under the sharp null the randomization p-value is uniform
    pv = []
    for _ in range(300):
        z = np.zeros(N, bool)
        z[rng.choice(N, N1, replace=False)] = True
        pv.append(causal.fisher_test(y0, z, reps=199, rng=rng)["p"])  # outcome y0 for everyone: no effect at all
    size = float(np.mean(np.array(pv) <= 0.1))
    lab.row("Fisher's test when the drug does nothing: share of p <= 0.1", f"{size:.1%}   (theory 10%)")
    assert abs(size - 0.1) < 0.06
    lab.note = ("Over the coin the difference in means is unbiased with exactly Neyman's variance; the variance a trial "
                "can estimate is larger by S_tau^2/n, which no trial can see. Without the coin the same subtraction "
                "measures mostly who was chosen.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(est.min(), est.max(), 200)
    ax[0].hist(est, bins=50, density=True, color=labs.BLUE, alpha=0.6, label="4,000 re-randomizations")
    ax[0].plot(grid, stats.norm.pdf(grid, v["ate"], np.sqrt(v["true"])), color=labs.GREEN, label="normal, Neyman's exact SD")
    ax[0].plot(grid, stats.norm.pdf(grid, v["ate"], np.sqrt(v["conservative"])), color=labs.RED, ls="--",
               label="normal, conservative SD")
    ax[0].axvline(v["ate"], color=labs.GOLD, label="the SATE")
    ax[0].axvline(naive, color=labs.ORANGE, ls=":", label="the doctor's comparison")
    ax[0].set(title="The difference in means over the coin", xlabel="estimated effect (mm Hg)", ylabel="density",
              ylim=(0, 1.75 * stats.norm.pdf(0, 0, np.sqrt(v["true"]))))
    ax[0].legend(loc="upper center", ncol=2)
    sds = np.array([0.0, 2.0, 4.75, 8.0, 12.0])
    ratio_th, ratio_mc = [], []
    for s in sds:
        _, a0, a1 = science(rng, s)
        w = causal.neyman_true_var(a0, a1, N1)
        z = rng.permuted(np.tile(np.arange(N) < N1, (8000, 1)), axis=1)  # 8,000 coins at once
        e = (z @ a1) / N1 - (~z @ a0) / (N - N1)
        ratio_th.append(np.sqrt(w["conservative"] / w["true"]))
        ratio_mc.append(np.sqrt(w["conservative"]) / e.std(ddof=1))
    ax[1].plot(sds, ratio_th, "o-", color=labs.GOLD, label="theory: conservative SD / exact SD")
    ax[1].plot(sds, ratio_mc, "s", color=labs.BLUE, label="conservative SD / simulated SD (8,000 coins)")
    ax[1].axhline(1, color=labs.MUTED, ls="--")
    ax[1].set(title="How conservative, as effects vary more", xlabel="SD of the individual effects (mm Hg)",
              ylabel="ratio of standard deviations", ylim=(0.97, 1.25))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
