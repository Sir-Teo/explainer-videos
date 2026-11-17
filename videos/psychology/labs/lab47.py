"""Lab 47: people over time: the language-as-fixed-effect fallacy, stimuli and power, partial pooling, Simpson's
paradox within persons, a non-ergodic population, inertia's bias and critical slowing down."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import within as Wi

TITLE = "People over Time"
GOAL = ("Simulate studies with words as a sample and see the by-participant test fail, pool person-level slopes, "
        "separate within from between, build a population that describes no one, and look for early warnings.")
TASKS = [
    "Make the words more alike (item SD 0.2). How far does the by-participant false-positive rate fall?",
    "Give each person 40 observations instead of 15. How much does partial pooling still help?",
    "Change the diary to two prompts a day (thin = 8). Do the warnings separate from the false alarms?",
]


def run(seed=0):
    out = labs.Lab()
    fp = Wi.false_positive_rates(reps=150, seed=seed + 1)
    assert fp["F1"] > 0.25 and fp["minF"] < 0.1
    out.row("null studies significant: by participants; by items; min F'", f"{fp['F1']:.2f}; {fp['F2']:.2f}; {fp['minF']:.2f}")
    pw = Wi.stimulus_power(0.4, [10, 20, 40], n_subj=30, reps=60, seed=seed + 2)
    out.row("power for an effect of 0.4 with 10, 20, 40 words", ", ".join(f"{v:.2f}" for v in pw["power"]))
    p = Wi.person_slopes(n_obs=15, seed=seed + 3)
    out.row("person slopes: RMSE own lines; multilevel", f"{p['rmse_ols']:.3f}; {p['rmse_blup']:.3f}")
    s = Wi.simpson_cloud(between=-1.0, within=0.6, seed=seed + 4)
    assert s["between"] < 0 < s["within"]
    out.row("slopes: pooled; between; within", f"{s['pooled']:.2f}; {s['between']:.2f}; {s['within']:.2f}")
    e = Wi.nonergodic(seed=seed + 5)
    out.row("group correlation; share of people within 0.1 of it", f"{e['cross_mean']:.2f}; {e['share_near']:.2f}")
    ib = Wi.inertia_bias(phi=0.4, Ts=(10, 20, 50, 100), reps=800, seed=seed + 6)
    out.row("inertia 0.4 estimated from 10, 20, 50, 100 occasions", ", ".join(f"{v:.2f}" for v in ib["mean_est"]))
    wr = Wi.warning_rates(n=40, seed=seed + 7)
    wd = Wi.warning_rates(n=40, window=30, threshold=0.3, seed=seed + 7, thin=15, noise_obs=0.3)
    out.row("early warnings: continuous (hit, false); diary (hit, false)",
            f"{wr['hit']:.2f}, {wr['false_alarm']:.2f}; {wd['hit']:.2f}, {wd['false_alarm']:.2f}")

    out.note = ("Ignoring the words' variation makes nothing look like something; a relation across people can run "
                "the other way within each; and short noisy diaries cannot tell a warning from noise.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    for i in range(s["g"].max() + 1):
        m = s["g"] == i
        ax[0].scatter(s["x"][m], s["y"][m], s=10)
    ax[0].set(title="between negative, within positive", xlabel="x", ylabel="y")
    d = Wi.double_well(T=3000, seed=seed + 4)
    ind = Wi.rolling_indicators(d["x"], 300)
    ax[1].plot(d["x"], color=labs.BLUE, lw=0.6)
    ax2 = ax[1].twinx()
    ax2.plot(ind["ac"], color=labs.RED)
    ax[1].axvline(d["tip"], color="grey", ls=":")
    ax[1].set(title="critical slowing down before a tip", xlabel="time", ylabel="state")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
