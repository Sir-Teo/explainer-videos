"""Lab 30: an ideal learner's surprisal and the Goldilocks effect, ManyBabies recomputed with its meta-regression,
number by ratio, the infant statistician, and the A-not-B error made and outgrown by a dynamic neural field."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import develop as D
from explainer.psychology.psyche import drive as Dr

TITLE = "The Infant Mind"
GOAL = ("Compute an ideal learner's surprisal and see attention favour the middle; recompute ManyBabies 1 from its "
        "open table, with age and method as moderators; derive number discrimination from Weber's law; work out "
        "the infant statistician's box of balls; and simulate the A-not-B error as a dynamic field.")
TASKS = [
    "Refit the ManyBabies meta-regression with an interaction between age and method. Does the age slope differ "
    "for the head-turn preference procedure?",
    "Give the dynamic field a memory trace that decays between trials (multiply it by 0.8 before each trial). "
    "How does the error change with the number of A trials?",
    "Change the Goldilocks observer's best surprisal from 1.1 to 0.5 bits. Which kind of sequence is now watched "
    "longest, and why?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. surprisal and Goldilocks
    g = D.goldilocks(seed=seed)
    out.row("events watched before looking away: predictable, intermediate, random",
            ", ".join(f"{g['mean_length'][k]:.1f}" for k in ("predictable", "intermediate", "random")))
    i = int(np.nanargmin(g["rate"]))
    out.row("surprisal with the lowest look-away rate (bits)", f"{g['surprisal'][i]:.2f}")

    # 2. ManyBabies
    d = opendata.manybabies_2020()
    y, v, age, meth = d["yi"], d["vi"], d["age_mo"], np.array(d["method"])
    re = Dr.random_effects(y, v)
    out.row("ManyBabies: estimates; pooled d [95% CI]; I^2",
            f"{re['k']}; {re['estimate']:.2f} [{re['lo']:.2f}, {re['hi']:.2f}]; {100 * re['I2']:.0f}%")
    assert re["k"] == 108 and abs(re["estimate"] - 0.35) < 0.01
    X = np.column_stack([np.ones_like(y), age - age.mean(), (meth == "HPP").astype(float),
                         (meth == "Eye tracking").astype(float)])
    mr = D.meta_regression(y, v, X)
    out.row("meta-regression: age slope per month (SE); head-turn preference over central fixation (SE)",
            f"{mr['b'][1]:.3f} ({mr['se'][1]:.3f}); {mr['b'][2]:.2f} ({mr['se'][2]:.2f})")
    assert mr["b"][1] > 0 and mr["b"][2] > 0

    # 3. number
    for age_, w in D.WEBER.items():
        out.row(f"{age_} (w = {w}): ratio told apart 75% of the time; P(8 v 12)",
                f"{D.ratio_threshold(w):.2f}; {float(D.ans_correct(12, 8, w)):.2f}")

    # 4. the statistician
    a, b = D.sample_surprise(0.1, 4, 5), D.sample_surprise(0.1, 1, 5)
    out.row("box 90% white: P(4 red, 1 white), P(1 red, 4 white), ratio",
            f"{a['p']:.5f}, {b['p']:.3f}, {b['p'] / a['p']:.0f}")

    # 5. A not B
    delays = [0.0, 1.0, 2.0, 3.0, 5.0, 8.0]
    young = [D.a_not_b(-6.0, dl, n=150, seed=seed)["error"] for dl in delays]
    old = [D.a_not_b(-3.0, dl, n=150, seed=seed)["error"] for dl in delays]
    out.row("A-not-B errors by delay 0, 1, 2, 3, 5, 8 s: younger field", ", ".join(f"{e:.2f}" for e in young))
    out.row("the same: older field", ", ".join(f"{e:.2f}" for e in old))
    assert young[0] < 0.1 and max(young) > 0.8 and max(old) < 0.05

    out.note = ("Attention favours events of middling surprisal; ManyBabies pools to d = 0.35 and grows with age; "
                "number is judged by ratio, more finely with age; a sample of four red from a mostly white box is "
                "729 times less likely than the reverse; and a field that cannot hold a peak through a delay falls "
                "back on its memory of A.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(age, y, s=12, c=[{"HPP": labs.GOLD, "Central fixation": labs.BLUE}.get(m, "#888888") for m in meth])
    xs = np.linspace(age.min(), age.max(), 50)
    ax[0].plot(xs, mr["b"][0] + mr["b"][1] * (xs - age.mean()), color=labs.BLUE)
    ax[0].set(title="ManyBabies 1: each lab and age group", xlabel="mean age (months)", ylabel="Cohen's d")
    ax[1].plot(delays, young, "o-", color=labs.GOLD, label="younger field")
    ax[1].plot(delays, old, "o-", color=labs.BLUE, label="older field")
    ax[1].set(title="A-not-B in a dynamic field", xlabel="delay (s)", ylabel="share reaching to A on B")
    ax[1].legend()
    out.fig = fig
    return out
