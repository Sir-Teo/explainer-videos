"""Lab 59: computational psychiatry: the reliability paradox, biotypes that are not there, and prediction that
does not travel."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import precision as Pr

TITLE = "Computational Psychiatry"
GOAL = ("Measure the reliability of a robust task effect, expose a circular biotype pipeline with a stability "
        "check, and score a prediction model in sample, cross-validated and in a new trial.")
TASKS = [
    "Raise the trials per condition to 600. What is the retest correlation now?",
    "Plant subgroups (structure 1.5). How stable are the clusters?",
    "Remove the drift between trials. How close does the new-trial AUC come to the cross-validated one?",
]


def run(seed=0):
    out = labs.Lab()
    p = Pr.paradox(n_people=300, seed=seed)
    assert p["t"] > 20 and p["retest_r"] < 0.6
    out.row("group t; retest r (expected)", f"{p['t']:.0f}; {p['retest_r']:.2f} ({p['expected_r']:.2f})")
    need = 0.9 / 0.1 / (p["expected_r"] / (1 - p["expected_r"])) * 60
    out.row("trials per condition for reliability 0.9", f"{need:.0f}")
    none = [Pr.biotypes(structure=0.0, seed=seed + r) for r in range(4)]
    real = [Pr.biotypes(structure=1.5, seed=seed + 50 + r) for r in range(4)]
    a0, a1 = np.mean([b["stability_ari"] for b in none]), np.mean([b["stability_ari"] for b in real])
    assert a1 > a0 + 0.2
    out.row("no types: studies with p < 0.05; stability", f"{sum(b['symptom_p'] < 0.05 for b in none)} of 4; {a0:.2f}")
    out.row("real types: stability", f"{a1:.2f}")
    t = Pr.cross_trial(reps=15, seed=seed)
    assert t["apparent"] > t["cv"]
    out.row("AUC: same data; cross-validated; new trial", f"{t['apparent']:.2f}; {t['cv']:.2f}; {t['new_trial']:.2f}")
    s = Pr.pai_sample(0.3)
    out.row("patients for a main effect; for an interaction (d = 0.3)",
            f"{s['main_total']:.0f}; {s['interaction_total']:.0f}")

    out.note = ("Group effects are real; measuring individuals takes many trials, and a result found in a sample "
                "must be checked in a sample that did not choose it.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(p["s1"], p["s2"], s=8)
    ax[0].set(title="retest of a robust effect", xlabel="session 1 (ms)", ylabel="session 2 (ms)")
    ax[1].bar(["same data", "cross-validated", "new trial"], [t["apparent"], t["cv"], t["new_trial"]],
              color=labs.BLUE)
    ax[1].set(title="one model, three AUCs", ylim=(0.5, 0.8))
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
