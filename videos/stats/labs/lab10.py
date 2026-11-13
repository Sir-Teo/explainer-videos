"""Lab 10: check a test's size and power against theory, then break the size by pooling and by peeking."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import tests as skt

TITLE = "What a 5% test promises, and two ways to break it"
GOAL = ("Run 20,000 one-sample t-tests (n = 15) under the null and under two alternatives and compare the share of "
        "p-values below 0.05 with the exact power; then measure the size of Student's and Welch's two-sample tests "
        "when the spreads differ, and of a t-test that is checked after every observation.")
TASKS = [
    "Look only after every 10th observation up to 100. How much of the inflation goes away?",
    "Swap the group sizes in the two-sample study (40 with the large spread, 10 with the small). Which way does "
    "Student's size move now, and why?",
    "Replace the normal data in the first study by exponentials minus 1 (mean 0). Is the p-value still uniform at "
    "n = 15? At n = 200?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. The p-value: uniform under the null, and piled near zero with the power the noncentral t predicts.
    n, reps = 15, 20_000
    crit = stats.t.ppf(0.975, n - 1)
    pvals = {}
    for delta in (0.0, 0.3, 0.8):
        x = rng.normal(delta, 1, (reps, n))
        t = x.mean(1) / (x.std(1, ddof=1) / np.sqrt(n))
        p = 2 * stats.t.sf(np.abs(t), n - 1)
        assert abs(skt.t_test(x[0])["p"] - p[0]) < 1e-12, "the vectorized test is statkit's t_test"
        nc = delta * np.sqrt(n)
        power = stats.nct.sf(crit, n - 1, nc) + stats.nct.cdf(-crit, n - 1, nc) if delta else 0.05
        share = np.mean(p < 0.05)
        pvals[delta] = p
        lab.row(f"P(p < 0.05), true mean {delta} sd", f"{share:.3f}   (exact {power:.3f})")
        assert abs(share - power) < 4 * np.sqrt(power * (1 - power) / reps), "rejection rate matches the exact power"
    ks = stats.kstest(pvals[0.0], "uniform").statistic
    lab.row("null p-values: largest gap from the uniform CDF", f"{ks:.4f}   (noise level about {1.36 / np.sqrt(reps):.4f})")
    assert ks < 0.015, "under the null the p-value is uniform"

    # 2. Student against Welch when 10 observations have 2.7 times the spread of the other 40 (no true difference).
    R2 = 4000
    a, b = rng.normal(0, 2.7, (R2, 10)), rng.normal(0, 1, (R2, 40))
    size_student = np.mean([skt.t_test(u, v)["p"] < 0.05 for u, v in zip(a, b)])
    size_welch = np.mean([skt.welch_test(u, v)["p"] < 0.05 for u, v in zip(a, b)])
    # what the pooled variance does: the statistic's true variance over the variance the pooled formula assumes
    ratio = (2.7 ** 2 / 10 + 1 / 40) / ((9 * 2.7 ** 2 + 39) / 48 * (1 / 10 + 1 / 40))
    approx = 2 * stats.norm.sf(stats.t.ppf(0.975, 48) / np.sqrt(ratio))
    lab.row("two-sample size, unequal spreads", f"Student {size_student:.3f} (variance-ratio approximation {approx:.3f})   Welch {size_welch:.3f}")
    assert abs(size_student - approx) < 0.04 and size_student > 0.15, "the pooled test's 5% is really over 20%"
    assert abs(size_welch - 0.05) < 0.02, "Welch keeps the size"

    # 3. Peeking: a t-test after every observation from the 10th on, null true.
    R3, N = 5000, 500
    z = rng.standard_normal((R3, N))
    m = np.arange(1, N + 1)
    cs, cs2 = np.cumsum(z, 1), np.cumsum(z * z, 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        tpath = (cs / m) / np.sqrt((cs2 - cs ** 2 / m) / (m - 1) / m)
    single = np.abs(tpath) > stats.t.ppf(0.975, np.maximum(m - 1, 1))  # the test at each n, taken on its own
    hit = single.copy()
    hit[:, :9] = False  # the first look is at the 10th observation
    ever = np.maximum.accumulate(hit, axis=1).mean(0)  # ever[n - 1]: rejected at some look up to n
    film = {20: 0.13, 50: 0.22, 100: 0.29, 500: 0.42}
    lab.row("one look at n = 100", f"{hit[:, 99].mean():.3f}   (promise 0.050)")
    lab.row("ever significant, peeking up to n = 20, 50, 100, 500",
            "  ".join(f"{ever[e - 1]:.3f}" for e in film) + "   (the film: 0.13, 0.22, 0.29, 0.42)")
    assert abs(hit[:, 99].mean() - 0.05) < 0.015, "each single test keeps its 5%"
    assert all(abs(ever[e - 1] - v) < 0.03 for e, v in film.items()), "the procedure does not: the film's rates"
    lab.note = ("A single test at a fixed n keeps its 5%, and its power is what the noncentral t says. Pool unequal "
                "variances or stop at the first p < 0.05 and the same nominal 5% becomes 20% to 40%.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(0, 1, 21)
    for delta, color in ((0.0, labs.BLUE), (0.3, labs.GOLD), (0.8, labs.RED)):
        ax[0].hist(pvals[delta], bins=bins, density=True, histtype="step", lw=1.8, color=color, label=f"true mean {delta} sd")
    ax[0].set(title="20,000 p-values of a t-test, n = 15", xlabel="p-value", ylabel="density", yscale="log")
    ax[0].legend()
    ax[1].plot(m[9:], ever[9:], color=labs.RED, label="ever p < 0.05, looking after every observation")
    looks = np.array([10, 14, 20, 30, 50, 70, 100, 140, 200, 300, 500])
    ax[1].plot(looks, single[:, looks - 1].mean(0), "s-", color=labs.BLUE, lw=1.2, ms=4, label="one test at n, no peeking")
    ax[1].plot(list(film), list(film.values()), "o", color=labs.GOLD, label="the film's rates")
    ax[1].axhline(0.05, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="False-positive rate of a t-test with a true null", xlabel="largest sample size n", ylabel="rate", xscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
