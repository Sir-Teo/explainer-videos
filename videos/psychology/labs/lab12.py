"""Lab 12: d' and c from rates, payoffs that move only the criterion, ROCs and their area, rating ROCs fitted by
maximum likelihood with a test of equal variances, the ideal criterion and the accuracy trap, forced choice, the
high-threshold model's straight ROC, base rates, and the prevalence effect."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.psychology.psyche import sdt as D

TITLE = "Signal detection: seeing, saying and the ROC"
GOAL = ("Build an observer with normal evidence and a criterion; recover d' and c from its rates and see payoffs "
        "move only c; trace ROCs and check that their area is the two-choice score; simulate a rating study, fit "
        "it by maximum likelihood with equal and unequal variances and test between them; find the ideal criterion "
        "for base rates and payoffs and see accuracy reward silence when signals are rare; compare the "
        "high-threshold model's straight ROC with curved data; and work out what a positive test means at "
        "different base rates.")
TASKS = [
    "Fit the rating study at 30, 100 and 300 trials of each kind, 200 times each, with sigma_s = 1.25. Plot the "
    "spread of the fitted zROC slope against trials. How many trials does one person need for the slope to mean "
    "anything?",
    "Give the ideal observer a payoff where a miss costs ten times a false alarm, at a base rate of 1%. Where is "
    "the criterion, and what are the hit rate and the share of positives that are real?",
    "Simulate a high-threshold observer (p = 0.5) at five guessing rates and compute d' at each. Then simulate a "
    "signal-detection observer at five criteria. Which one keeps d' constant, and why?",
]


def run(seed=0):
    out = labs.Lab()
    rng = lambda k: np.random.default_rng(seed + k)  # noqa: E731

    # 1. two rates, two numbers
    h, f = D.rates(1.5, 1.0)
    out.row("d' = 1.5, criterion at 1.0: hit and false-alarm rates; d' and c recovered",
            f"{h:.3f}, {f:.3f}; {D.dprime(h, f):.2f}, {D.criterion_c(h, f):.2f}")
    obs = D.Observer(d=1.5, criterion=1.0)
    xs, xn = obs.evidence(True, 400, rng(2)), obs.evidence(False, 400, rng(3))
    r = D.from_counts(int((xs > 1.0).sum()), 400, int((xn > 1.0).sum()), 400)
    out.row("the same from 400 + 400 simulated trials: d', c", f"{r['d']:.2f}, {r['c']:.2f}")

    # 2. payoffs move only the criterion
    ks = [D.optimal_criterion(1.5, 0.5, c_miss=4.0), D.optimal_criterion(1.5, 0.5), D.optimal_criterion(1.5, 0.5, c_fa=4.0)]
    hh, ff = D.rates(1.5, np.array(ks))
    out.row("misses costly / even / false alarms costly: hit rates", ", ".join(f"{v:.2f}" for v in hh))
    out.row("... and d' in each", ", ".join(f"{D.dprime(a, b):.2f}" for a, b in zip(hh, ff)))
    assert all(abs(D.dprime(a, b) - 1.5) < 1e-9 for a, b in zip(hh, ff)), "payoffs must leave d' alone"

    # 3. ROC area and the two-choice score
    out.row("area under the ROC for d' = 1.5; Phi(d'/sqrt 2); simulated 2AFC",
            f"{D.auc(1.5):.3f}; {D.pc_2afc(1.5):.3f}; {np.mean(rng(4).normal(1.5, 1, 20000) > rng(5).normal(0, 1, 20000)):.3f}")

    assert abs(D.auc(1.5) - D.pc_2afc(1.5)) < 1e-12, "the ROC's area is the two-choice score"

    # 4. a rating study fitted two ways
    o2 = D.Observer(d=1.25, sigma_s=1.25)
    cs, cn = D.simulate_ratings(o2, [-0.4, 0.2, 0.7, 1.2, 1.8], 300, 300, rng(6))
    u, e = D.fit_rating(cs, cn), D.fit_rating(cs, cn, equal_variance=True)
    lr = 2 * (u["loglik"] - e["loglik"])
    out.row("rating study (sigma_s = 1.25): fitted d', sigma_s, zROC slope",
            f"{u['d']:.2f}, {u['sigma_s']:.2f}, {u['slope']:.2f}")
    out.row("equal against unequal variance: chi-square, p", f"{lr:.1f}, {stats.chi2.sf(lr, 1):.3f}")

    # 5. the ideal observer and the accuracy trap
    for p in (0.5, 0.2, 0.05):
        k = D.optimal_criterion(1.5, p)
        out.row(f"signals {100 * p:.0f}% of the time: ideal criterion; hit rate; share correct",
                f"{k:.2f}; {D.rates(1.5, k)[0]:.2f}; {D.expected_value(1.5, k, p):.3f}")

    # 6. forced choice
    out.row("2AFC at d' = 1; 4AFC; d' from 75% correct", f"{D.pc_2afc(1.0):.3f}; {D.pc_mafc(1.0, 4):.3f}; "
            f"{D.d_from_2afc(0.75):.2f}")

    # 7. the high-threshold model
    g = np.array([0.1, 0.4])
    fa, hit = D.high_threshold_roc(0.5, g)
    out.row("high-threshold observer, p = 0.5, guessing 0.1 and 0.4: d'", ", ".join(f"{D.dprime(a, b):.2f}" for a, b in zip(hit, fa)))

    # 8. base rates
    nf = D.natural_frequencies(0.01, 0.8, 0.096)
    assert abs(nf["ppv"] - 8 / 103.04) < 1e-9
    out.row("mammogram: positives per 1,000; real; share real", f"{nf['positives']:.0f}; {nf['true_positive']:.0f}; {nf['ppv']:.3f}")
    out.row("prevalence where a positive is right half the time", f"{0.096 / (0.8 + 0.096):.3f}")

    # 9. the prevalence effect
    kp = D.prevalence_criteria(2.5, [0.5, 0.1, 0.01], shift=0.5)
    out.row("criterion moved half way to the ideal, prevalence 50%, 10%, 1%: misses",
            ", ".join(f"{1 - v:.2f}" for v in D.rates(2.5, kp)[0]))

    out.note = ("Two rates give two numbers: payoffs move c and leave d' alone. The ROC's area equals the "
                "two-choice score. A rating study of a few hundred trials can tell unequal variances from equal; a "
                "few dozen cannot. When signals are rare the ideal criterion climbs and accuracy rewards silence. "
                "The high-threshold model's d' changes with the guessing rate, because its ROC is straight. A "
                "positive mammogram at 1% prevalence is right about one time in thirteen.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    fg = np.linspace(1e-4, 1 - 1e-4, 300)
    for d, col in ((0.5, labs.GREY), (1.0, labs.BLUE), (1.5, labs.GREEN), (2.5, labs.PINK)):
        ax[0].plot(fg, 1 - stats.norm.cdf(stats.norm.ppf(1 - fg) - d), color=col, lw=1.6, label=f"d' = {d}")
    hr, fr = D.rating_rates(cs, cn)
    ax[0].plot(fr, hr, "o", color=labs.PINK, label="rating study")
    ax[0].plot([0, 1], [0, 1], ":", color=labs.GREY)
    ax[0].set(title="ROCs, and a rating study", xlabel="false-alarm rate", ylabel="hit rate")
    ax[0].legend(fontsize=8)
    zf, zh = stats.norm.ppf(fr), stats.norm.ppf(hr)
    ax[1].plot(zf, zh, "o", color=labs.BLUE)
    x = np.linspace(-2, 1, 10)
    ax[1].plot(x, u["slope"] * x + u["d"] * u["slope"], color=labs.GREEN, lw=1.6, label=f"unequal: slope {u['slope']:.2f}")
    ax[1].plot(x, x + e["d"], color=labs.GREY, lw=1.2, ls="--", label="equal: slope 1")
    ax[1].set(title="The same study in z coordinates", xlabel="z(F)", ylabel="z(H)")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
