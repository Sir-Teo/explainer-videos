"""Lab 9: play the tank factory game, Rao-Blackwellize the moment estimator, and watch a 1/k rate beat 1/sqrt(k)."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import estimation as est

TITLE = "The tank factory game"
GOAL = ("Grade three estimators of the number of tanks N on simulated factories (N = 300, k = 6 captured), check "
        "their bias and spread against the exact formulas, average the moment estimator within each value of the "
        "maximum to recover the best unbiased estimator, and measure how each one's spread falls as k grows.")
TASKS = [
    "Grade the recipes under model='newer' and model='offset' in est.tank_game. Which one survives serials that "
    "start at 1,001, and what does it pay for that under the textbook model?",
    "Grade a * max - 1 for a between 1.10 and 1.25 at k = 5. Where is the RMSE least, and is that recipe unbiased?",
    "Write your own recipe as a function of the (reps, k) array of serials and try to beat the UMVUE's RMSE.",
]


def run(seed=0):
    lab = labs.Lab()
    N, k, reps = 300, 6, 20_000
    games = {name: est.tank_game(est.TANK_ESTIMATORS[name], N=N, k=k, reps=reps, seed=seed) for name in ("mom", "max", "umvue")}
    exact = {"mom": (0.0, est.mom_sd(N, k)), "max": ((k - N) / (k + 1), None), "umvue": (0.0, est.umvue_sd(N, k))}
    names = {"mom": "2 x-bar - 1 (moments)", "max": "max (MLE)", "umvue": "max (1 + 1/k) - 1 (UMVUE)"}
    for name, g in games.items():
        bias, sd = exact[name]
        lab.row(names[name], f"bias {g['bias']:+6.1f} (exact {bias:+.1f})   SD {g['sd']:5.1f}"
                + (f" (exact {sd:.1f})" if sd else "") + f"   RMSE {g['rmse']:.1f}")
        assert abs(g["bias"] - bias) < 4 * g["bias_mcse"] + 0.01, f"{name}: bias as derived"
        if sd:
            assert abs(g["sd"] / sd - 1) < 0.04, f"{name}: SD matches the exact formula"
    assert games["umvue"]["rmse"] < games["max"]["rmse"] < games["mom"]["rmse"], "the UMVUE wins under the textbook model"

    # Rao-Blackwell: the same seed gives the same factories, so the estimates are paired.  Average the moment
    # estimator over all captures that share a maximum: the result is the UMVUE, a function of the maximum alone.
    m = games["max"]["estimates"].astype(int)
    mom = games["mom"]["estimates"]
    counts = np.bincount(m)
    big = np.flatnonzero(counts >= 40)
    cond_mean = np.array([mom[m == v].mean() for v in big])
    cond_se = np.array([mom[m == v].std(ddof=1) / np.sqrt(counts[v]) for v in big])
    zscore = (cond_mean - (big * (1 + 1 / k) - 1)) / cond_se
    lab.row("E(2 x-bar - 1 | max) against max (1 + 1/k) - 1", f"mean squared z-score {np.mean(zscore ** 2):.2f} over {len(big)} values of the max (1 if equal)")
    assert np.mean(zscore ** 2) < 1.6 and abs(zscore.mean()) < 0.5, "conditioning on the maximum gives the UMVUE"

    # Rates: the moment estimator's SD falls like 1/sqrt(k), the UMVUE's nearly like 1/k.
    ks = np.array([2, 3, 5, 8, 12, 20, 30])
    sd_mom = np.array([est.tank_game(est.TANK_ESTIMATORS["mom"], N=N, k=int(q), reps=4000, seed=seed + 1)["sd"] for q in ks])
    sd_umv = np.array([est.tank_game(est.TANK_ESTIMATORS["umvue"], N=N, k=int(q), reps=4000, seed=seed + 1)["sd"] for q in ks])
    slope_mom = np.polyfit(np.log(ks), np.log(sd_mom), 1)[0]
    slope_umv = np.polyfit(np.log(ks), np.log(sd_umv), 1)[0]
    lab.row("log-log slope of SD against k, k = 2..30", f"moments {slope_mom:.2f} (1/sqrt(k) is -0.5)   UMVUE {slope_umv:.2f} (1/k is -1)")
    lab.row("SD at k = 20", f"UMVUE {sd_umv[5]:.1f} (exact {est.umvue_sd(N, 20):.1f})   a 1/sqrt(k) law matched at k = 2: {est.umvue_sd(N, 2) * np.sqrt(2 / 20):.1f}")
    assert np.allclose(sd_umv, [est.umvue_sd(N, int(q)) for q in ks], rtol=0.08), "UMVUE SDs match the formula"
    assert slope_mom > -0.62 and slope_umv < -0.8, "the tanks beat the 1/sqrt(k) rate"
    lab.note = ("Conditioning the moment estimator on the sufficient maximum removes its extra noise and lands on "
                "the UMVUE, whose spread falls nearly like 1/k: faster than the Cramer-Rao rate, because the "
                "support 1..N moves with the parameter.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.arange(99.5, 561, 7)  # width 7 holds six values of the UMVUE, so the histogram has no comb
    for name, color in (("mom", labs.BLUE), ("max", labs.RED), ("umvue", labs.GOLD)):
        ax[0].hist(games[name]["estimates"], bins=bins, density=True, histtype="stepfilled", alpha=0.45, color=color, label=names[name])
    ax[0].axvline(N, color=labs.INK, ls="--", lw=1)
    ax[0].set(title="20,000 factories of 300 tanks, 6 captured", xlabel="estimate of N (dashed: the truth)", ylabel="density")
    ax[0].legend()
    kk = np.linspace(2, 30, 100)
    ax[1].loglog(kk, [est.mom_sd(N, q) for q in kk], color=labs.BLUE, label="moments, exact")
    ax[1].loglog(kk, [est.umvue_sd(N, q) for q in kk], color=labs.GOLD, label="UMVUE, exact")
    ax[1].loglog(kk, est.umvue_sd(N, 2) * np.sqrt(2 / kk), color=labs.MUTED, ls="--", label="1/sqrt(k), matched at k = 2")
    ax[1].loglog(ks, sd_mom, "o", color=labs.BLUE)
    ax[1].loglog(ks, sd_umv, "o", color=labs.GOLD, label="simulated")
    ax[1].set(title="Spread against the number of tanks captured", xlabel="k", ylabel="SD of the estimate")
    ax[1].set_xticks([2, 3, 5, 10, 20, 30], labels=["2", "3", "5", "10", "20", "30"])
    ax[1].set_xticks([], minor=True)
    ax[1].legend()
    lab.fig = fig
    return lab
