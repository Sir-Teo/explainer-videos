"""Lab 36: Tajfel's matrices, an illusory correlation, the list experiment, an IAT model with its reliability and
prediction, the power of an audit study, and a promotion ladder on which small biases compound."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import social as S

TITLE = "Us and Them"
GOAL = ("Find the columns of Tajfel's matrix that each motive picks; model an illusory correlation; estimate a "
        "sensitive prevalence by the list experiment and see its cost in precision; give simulated people an IAT "
        "twice and see what reliability does to prediction; size an audit study; and watch a small bias compound on a "
        "promotion ladder.")
TASKS = [
    "Raise the IAT's occasion-to-occasion variation until test-retest reliability falls to 0.3. What happens to the "
    "correlation with behaviour, and to the group's mean D?",
    "Halve the callback gap (9.6% against 8.0%). How many applications per group does the audit now need?",
    "On the ladder, keep only the top 20% at each level instead of half. Does the same 0.1 SD advantage do more or "
    "less damage? Explain why.",
]


def audit_n(p1, p2, power=0.8):
    from scipy.stats import norm
    z = norm.ppf(0.975) + norm.ppf(power)
    return int(np.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2))


def run(seed=0):
    out = labs.Lab()

    M = S.tajfel_matrix()
    picks = {k: S.allocate(M, **{k: 1}) for k in ("joint", "ingroup", "difference", "fairness")}
    out.row("Tajfel's matrix 7..19 / 1..25: column for joint, ingroup, difference, fairness",
            ", ".join(f"{k} {v} ({M[0, v]:.0f}/{M[1, v]:.0f})" for k, v in picks.items()))
    assert picks["difference"] == 0 and picks["joint"] == 12

    for b in (0.0, 0.6, 1.0):
        ic = S.illusory_correlation(boost=b)
        out.row(f"illusory correlation, boost {b}: judged undesirable share A, B",
                f"{ic['judged'][0]:.2f}, {ic['judged'][1]:.2f}")

    est = np.array([S.list_experiment(n=1000, prevalence=0.2, seed=seed + s)["estimate"] for s in range(400)])
    out.row("list experiment, 400 surveys of 1,000: mean and SD of the estimate",
            f"{est.mean():.3f}, {est.std():.3f} (a direct question: {np.sqrt(0.16 / 1000):.3f})")

    for sd in (0.0, 0.07, 0.15):
        r = S.iat_study(n=300, state_sd=sd, seed=seed + 36)
        out.row(f"IAT, state SD {sd}: retest; r with behaviour; ceiling; mean D (t)",
                f"{r['retest']:.2f}; {r['r_behaviour']:.2f}; {r['ceiling']:.2f}; {r['mean_d']:.2f} ({r['t']:.0f})")

    out.row("audit: applications per group for 80% power, 9.6% vs 6.4%", str(audit_n(0.096, 0.064)))

    for a in (0.05, 0.1, 0.2):
        out.row(f"ladder, advantage {a} SD: the other group's share by level",
                ", ".join(f"{v:.2f}" for v in S.pipeline(levels=8, keep=0.5, advantage=a)))

    out.note = ("Favouritism for a mere label shows in which column people choose; a rare group's rare acts can "
                "earn it a bad name; privacy costs precision; a measure with retest near .5 can be clear for a crowd "
                "and weak for a person; an audit needs about a thousand applications per group to see a 50% gap in "
                "callbacks; and a bias too small to notice in any one decision compounds across a ladder.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    r = S.iat_study(n=400, seed=seed + 36)
    ax[0].scatter(r["d1"], r["d2"], s=6, color=labs.PURPLE, alpha=0.6)
    ax[0].set(title=f"IAT twice: r = {r['retest']:.2f}", xlabel="D, session 1", ylabel="D, session 2")
    ax[1].hist(est, bins=30, color=labs.BLUE)
    ax[1].axvline(0.2, color="k", lw=1)
    ax[1].set(title="List experiment estimates", xlabel="estimated prevalence", ylabel="surveys")
    for a, col in ((0.05, labs.BLUE), (0.1, labs.GOLD), (0.2, labs.RED)):
        ax[2].plot(np.arange(1, 9), S.pipeline(advantage=a), "o-", color=col, label=f"{a} SD")
    ax[2].set(title="The ladder", xlabel="level", ylabel="other group's share")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
