"""Lab 54: uniform convergence for thresholds, the fast rate of ERM, and what selection does to an error bar."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import slt

TITLE = "Uniform deviations, ERM's excess risk, and the best of a thousand classifiers"
GOAL = ("For threshold classifiers with 10% label noise, measure the uniform deviation sup |R_n - R| and the excess "
        "risk of the empirical risk minimizer as n grows, against the VC and Rademacher bounds. Then pick the best of "
        "1,000 coin-flipping classifiers on 200 points and see which interval for its true error still covers.")
TASKS = [
    "Raise the label noise eta to 0.4. Does the excess risk still fall like 1/n, or closer to 1/sqrt(n) at these "
    "sample sizes?",
    "Change K from 1,000 to 10 and to 100,000. How does the optimism of the selected classifier grow with K, and how "
    "does sqrt(log K) compare?",
    "Replace the union bound by a kl PAC-Bayes bound (slt.gibbs_posterior, slt.kl_discrete, slt.pac_bayes_bounds) "
    "for a Gibbs posterior over the 1,000 classifiers.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    eta, reps = 0.1, 300
    ns = [25, 100, 400, 1600]
    dev, exc, q95 = [], [], []
    for n in ns:
        d, e = [], []
        for _ in range(reps):
            x, y = slt.threshold_data(n, rng, eta=eta)
            d.append(slt.uniform_deviation_threshold(x, y, eta=eta))
            e.append(float(slt.threshold_risk(slt.erm_threshold(x, y), eta=eta)) - eta)
        d, e = np.array(d), np.array(e)
        assert np.all(e <= 2 * d + 2e-3), "excess risk of ERM is at most twice the uniform deviation"
        dev.append(d.mean())
        exc.append(e.mean())
        q95.append(np.quantile(d, 0.95))
        lab.row(f"n = {n}: mean sup|R_n - R|, mean excess risk of ERM",
                f"{dev[-1]:.4f}, {exc[-1]:.4f}   Rademacher bound {slt.rademacher_vc_bound(n, 1):.3f}   "
                f"VC bound (95%) {slt.vc_bound(n, 1):.3f}")
        assert dev[-1] < slt.rademacher_vc_bound(n, 1) and q95[-1] < slt.vc_bound(n, 1), "the bounds hold"
    s_dev = np.polyfit(np.log(ns), np.log(dev), 1)[0]
    s_exc = np.polyfit(np.log(ns), np.log(exc), 1)[0]
    lab.row("fitted exponents in n: deviation, excess risk", f"{s_dev:.2f}, {s_exc:.2f}   (theory -1/2 and, with bounded noise, -1)")
    assert -0.6 < s_dev < -0.4 and s_exc < -0.8, "the deviation is slow, the excess risk is fast"

    # selection: K classifiers whose errors are independent coin flips with true error 0.49
    K, n, r, trials = 1000, 200, 0.49, 400
    z = 1.959964
    union = slt.finite_class_bound(n, K)
    best = rng.binomial(n, r, size=(trials, K)).min(axis=1) / n  # the lowest training error
    wald = z * np.sqrt(best * (1 - best) / n)
    hold = rng.binomial(n, r, size=trials) / n  # the selected classifier on fresh data
    cover = {"Wald on the training error": float(np.mean(np.abs(best - r) <= wald)),
             "Hoeffding + union bound": float(np.mean(np.abs(best - r) <= union)),
             "Wald on a fresh holdout": float(np.mean(np.abs(hold - r) <= z * np.sqrt(hold * (1 - hold) / n)))}
    for k, v in cover.items():
        lab.row(f"best of {K:,}, n = {n}: {k}", f"covers {v:.1%}   (nominal 95%)")
    lab.row("its mean training error against its true error", f"{best.mean():.3f} vs {r}   union half-width {union:.3f}")
    assert cover["Wald on the training error"] < 0.02, "the naive interval ignores the selection"
    assert cover["Hoeffding + union bound"] > 0.95 and abs(cover["Wald on a fresh holdout"] - 0.95) < 0.05
    lab.note = ("Uniform convergence explains why ERM works and its bounds hold, loosely; the excess risk itself falls "
                "faster than the deviation. After choosing among many rules, only a bound uniform over the class, or "
                "fresh data, gives an honest error bar.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(ns, dev, "o-", color=labs.BLUE, label=f"mean sup|R_n - R|  (slope {s_dev:.2f})")
    ax[0].loglog(ns, exc, "o-", color=labs.GOLD, label=f"mean excess risk of ERM  (slope {s_exc:.2f})")
    ax[0].loglog(ns, [slt.rademacher_vc_bound(n, 1) for n in ns], color=labs.MUTED, ls="--", label="Rademacher bound")
    ax[0].loglog(ns, [slt.vc_bound(n, 1) for n in ns], color=labs.RED, ls="--", label="VC bound, 95%")
    ax[0].set(title="Thresholds with 10% label noise", xlabel="n", ylabel="risk")
    ax[0].legend(loc="lower left")
    bins = np.arange(0.3475, 0.56, 0.005)
    ax[1].hist(best, bins=bins, color=labs.RED, alpha=0.65, label="training error of the selected classifier")
    ax[1].hist(hold, bins=bins, color=labs.GREEN, alpha=0.55, label="its error on a fresh holdout")
    ax[1].axvline(r, color=labs.INK, ls="--", label="its true error 0.49")
    ax[1].set(title="The best of 1,000 coin-flipping classifiers, n = 200", xlabel="error rate", ylabel="trials")
    ax[1].legend(loc="upper left")
    ax[1].set_ylim(0, ax[1].get_ylim()[1] * 1.45)
    lab.fig = fig
    return lab
