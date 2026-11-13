"""Lab 61: measure what noise alone does to a timing experiment, to twenty comparisons and to a mean of speedups."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np
from scipy import integrate, special, stats

from explainer.cs.research import method

TITLE = "How not to fool yourself with a stopwatch"
GOAL = ("Simulate a timing experiment in which no setting differs (33 settings, the median of 5 runs each) and "
        "compare the spread of the medians with its exact expectation; count how often 20 null comparisons produce a "
        "'significant' one; watch a bootstrap interval narrow with runs; and settle Goldbach's small cases.")
TASKS = [
    "Report the fastest of each five runs instead of the median (np.min). Does the noise-only spread of 33 settings "
    "shrink or grow, and what does the minimum assume about the noise?",
    "Make the noise skewed (1 + sigma * rng.exponential()) as real run times are. Which of the lab's assertions "
    "still hold, and which closed form needs replacing?",
    "Raise the comparisons from 20 to 100 and apply Bonferroni's threshold 0.05 / 100. What is the chance of a "
    "false alarm now, and what did it cost in power?",
]


def expected_range(k: int, r: int = 5) -> float:
    """E[max - min] of k independent medians of r standard normal runs (r odd), by quadrature."""
    h = (r + 1) // 2

    def integrand(x):
        g = special.betainc(h, h, stats.norm.cdf(x))  # the CDF of the median of r
        return 1 - g ** k - (1 - g) ** k

    return integrate.quad(integrand, -8, 8)[0]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. noise alone: K settings that do not differ, the median of r runs each, 4,000 experiments
    sigma, r, reps = 0.04, 5, 4000
    spread, theory = {}, {}
    for k in (2, 33):
        med = np.median(1 + sigma * rng.standard_normal((reps, k, r)), axis=2)
        spread[k] = (med.max(axis=1) - med.min(axis=1)) / med.min(axis=1)
        theory[k] = sigma * expected_range(k, r)
        measured = (med.max(axis=1) - med.min(axis=1)).mean()
        lab.row(f"{k} identical settings: mean gap, slowest - fastest median", f"{measured:.2%} of the run time   "
                                                                              f"(exact {theory[k]:.2%})")
        assert abs(measured / theory[k] - 1) < 0.06, "the range of k medians has a known expectation"
    assert spread[33].mean() > 3 * spread[2].mean(), "more settings, more spread, with no effect anywhere"
    lab.row("33 settings: experiments whose 'speedup' exceeds 8%", f"{(spread[33] > 0.08).mean():.0%}   "
                                                                    f"(2 settings: {(spread[2] > 0.08).mean():.0%})")

    # 2. the garden of forking paths: 20 comparisons of two identical settings, 30 runs each
    studies, tests = 3000, 20
    a = 1 + sigma * rng.standard_normal((studies, tests, 30))
    b = 1 + sigma * rng.standard_normal((studies, tests, 30))
    p = stats.ttest_ind(a, b, axis=2, equal_var=False).pvalue
    hit = (p < 0.05).any(axis=1).mean()
    lab.row("at least one of 20 null comparisons 'significant'", f"{hit:.1%}   (1 - 0.95^20 = {1 - 0.95 ** 20:.1%})")
    assert abs(hit - (1 - 0.95 ** 20)) < 0.035, "twenty looks at noise find something about two times in three"

    # 3. a bootstrap interval for the mean narrows like 1 / sqrt(runs)
    times = 0.907 + 0.028 * rng.standard_normal(80)
    ks = (5, 10, 20, 40, 80)
    width, predicted = [], []
    for k in ks:
        lo, hi = method.bootstrap(times[:k], np.mean, B=2000, seed=seed)
        width.append(hi - lo)
        predicted.append(2 * 1.96 * times[:k].std(ddof=1) / np.sqrt(k))
        assert lo < times[:k].mean() < hi
    lab.row("bootstrap 95% interval for the mean, 5 ... 80 runs", "  ".join(f"{1000 * w:.0f}" for w in width) + " ms wide")
    lab.row("2 x 1.96 s / sqrt(n)", "  ".join(f"{1000 * w:.0f}" for w in predicted) + " ms")
    assert all(abs(w / q - 1) < 0.25 for w, q in zip(width[1:], predicted[1:])), "the bootstrap agrees with the formula"
    assert 0.35 < width[4] / width[2] < 0.7, "four times the runs, about half the width"

    # 4. averaging speedups, and two conjectures' small cases
    sm = method.speedup_means()
    lab.row("A against B, B against A: arithmetic mean of ratios", f"{sm['arith_b_over_a']:.2f} and "
                                                                    f"{sm['arith_a_over_b']:.2f}   (geometric: "
                                                                    f"{sm['geo_b_over_a']:.2f} and {sm['geo_a_over_b']:.2f})")
    assert sm["arith_b_over_a"] > 1 and sm["arith_a_over_b"] > 1, "each looks slower than the other"
    assert abs(sm["geo_b_over_a"] * sm["geo_a_over_b"] - 1) < 1e-12 and abs(sm["geo_b_over_a"] - 1) < 1e-12
    gb = method.goldbach(2_000_000)
    lab.row("Goldbach, every even number from 4 to 2,000,000", f"holds: {gb['all_hold']}; hardest {gb['worst']:,} = "
                                                               f"{gb['worst_p']} + {gb['worst'] - gb['worst_p']:,}")
    assert gb["all_hold"] and (gb["worst"], gb["worst_p"]) == (1_077_422, 601)
    assert 27 ** 5 + 84 ** 5 + 110 ** 5 + 133 ** 5 == 144 ** 5 == 61_917_364_224, "Lander and Parkin against Euler"
    lab.note = ("With nothing differing, the slowest of 33 medians is several percent behind the fastest, and one "
                "comparison in twenty passes a 5% test: a spread or a significant result means little until it is "
                "set beside what noise alone produces.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    bins = np.linspace(0, max(spread[33].max(), 0.01), 60)
    ax[0].hist(spread[2], bins=bins, color=labs.GREY, alpha=0.7, label="2 settings")
    ax[0].hist(spread[33], bins=bins, color=labs.BLUE, alpha=0.7, label="33 settings")
    for k, color in ((2, labs.GREY), (33, labs.BLUE)):
        ax[0].axvline(theory[k], color=color, ls="--", lw=1.4)
    ax[0].axvline(np.nan, color=labs.MUTED, ls="--", lw=1.4, label="exact mean gap")
    ax[0].set(xlabel="(slowest median - fastest median) / fastest", ylabel=f"experiments of {reps:,}",
              title="No setting differs: the spread of the medians")
    ax[0].set_xticks(np.arange(0, bins[-1], 0.02))
    ax[0].xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax[0].set_axisbelow(True)
    ax[0].legend()
    ax[1].plot(ks, 1000 * np.array(width), "o-", color=labs.GOLD, label="bootstrap interval's width")
    ax[1].plot(ks, 1000 * np.array(predicted), "s--", color=labs.MUTED, label="2 x 1.96 s / sqrt(n)")
    ax[1].set(xscale="log", yscale="log", xlabel="runs", ylabel="width of the 95% interval (ms)",
              title="Four times the runs, half the width", xticks=ks, xticklabels=[str(k) for k in ks])
    ax[1].minorticks_off()
    ax[1].set_yticks([10, 15, 20, 30, 40, 60], labels=["10", "15", "20", "30", "40", "60"])
    ax[1].legend()
    lab.fig = fig
    return lab
