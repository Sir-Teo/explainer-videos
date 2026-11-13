"""Lab 20: the capstone's regression on the World, where the effect of sodium on blood pressure is known."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import capstone
from explainer.stats.world import World

TITLE = "One day's recall against usual intake"
GOAL = ("Survey 300,000 of the World's adults, regress measured systolic pressure on sodium with age, BMI and sex held "
        "fixed, and compare four exposures: one 24-hour recall, the mean of two, the recall calibrated on its "
        "replicate, and the intake itself. The World's effect is 1.5 mm Hg per gram.")
TASKS = [
    "Drop the adults on blood-pressure medicine (h['bp_meds']). Which slopes move, and why is that a different estimand?",
    "Add recalled energy (h['kcal_day1']) to the covariates. What happens to lambda and to the calibrated slope's stability?",
    "Cut the survey to 5,000 adults and rerun with ten seeds. How wide is the spread of the calibrated slope?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    w = World()
    h = w.health
    i = rng.choice(np.flatnonzero(w.adult), 300_000, replace=False)  # a simple random sample of adults
    age = w.age[i].astype(float)
    female = (~w.male[i]).astype(float)
    Z = np.column_stack([age, (age - 18) ** 2, h["bmi"][i], female * (age < 60)])
    y = h["sbp_read"][i].mean(1)  # the mean of three readings
    day1, day2, intake = h["na_day1"][i] / 1000, h["na_day2"][i] / 1000, h["na_current"][i] / 1000  # grams

    def slope(x):
        D = np.column_stack([x, np.ones(len(x)), Z])
        return float(np.linalg.lstsq(D, y, rcond=None)[0][0])

    rc = capstone.regression_calibration(day1, day2, Z)
    lam = rc["lam"]
    lam2 = 2 * lam / (1 + lam)  # the reliability of a two-day mean
    b1, b2, bcal, btrue = slope(day1), slope((day1 + day2) / 2), slope(rc["xhat"]), slope(intake)
    truth = w.SODIUM_EFFECT
    lab = labs.Lab()
    lab.row("the World's effect of sodium", f"{truth:.2f} mm Hg per g")
    lab.row("slope on the intake itself", f"{btrue:.2f}")
    lab.row("slope on one day's recall", f"{b1:.2f}   (lambda x intake slope = {lam:.2f} x {btrue:.2f} = {lam * btrue:.2f})")
    lab.row("slope on the mean of two recalls", f"{b2:.2f}   (2 lambda/(1 + lambda) = {lam2:.2f}, predicts {lam2 * btrue:.2f})")
    lab.row("regression calibration", f"{bcal:.2f}")
    lab.row("two recalls: correlation", f"{capstone.reliability(day1, day2):.2f}")
    assert b1 < 0.45 * btrue, "one day's recall loses more than half of the slope"
    assert abs(b1 / (lam * btrue) - 1) < 0.15, "the loss is the attenuation factor lambda"
    assert abs(b2 / (lam2 * btrue) - 1) < 0.15 and b2 > b1, "a second day buys back 2 lambda/(1 + lambda)"
    assert abs(bcal - btrue) < 0.25, "calibration recovers the slope on the intake itself"
    assert 1.0 < btrue < truth - 0.05, "which is still below the structural effect: diagnosis changes diet and treatment"
    lab.note = ("Day-to-day variation in what people eat shrinks the slope by the reliability lambda; a replicate recall "
                "measures lambda and undoes it. What is left, the gap to 1.5, is not noise: the diagnosed cut their salt "
                "and take medicine, and no adjustment of the exposure repairs that.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = ["one day's\nrecall", "mean of\ntwo days", "calibrated", "the intake\nitself"]
    vals = [b1, b2, bcal, btrue]
    ax[0].bar(names, vals, color=[labs.RED, labs.ORANGE, labs.BLUE, labs.GREEN], width=0.6)
    for k, v in enumerate(vals):
        ax[0].text(k, v + 0.03, f"{v:.2f}", ha="center", color=labs.INK)
    ax[0].axhline(truth, color=labs.GOLD, ls="--", label="the World's effect, 1.5")
    ax[0].set(title="Sodium's slope by how intake is measured", ylabel="mm Hg per g of sodium", ylim=(0, 1.8))
    ax[0].legend(loc="upper left")
    days = np.arange(1, 15)
    ax[1].plot(days, btrue * days * lam / (1 + (days - 1) * lam), "o-", color=labs.BLUE, ms=4,
               label="theory: k λ/(1 + (k − 1)λ) × intake slope")
    ax[1].scatter([1, 2], [b1, b2], color=labs.RED, zorder=5, s=50, label="measured: one and two recalls")
    ax[1].axhline(btrue, color=labs.GREEN, ls="--", label="slope on the intake itself")
    ax[1].set(title="What more recall days would buy", xlabel="recall days averaged, k", ylabel="expected slope",
              ylim=(0, 1.8))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
