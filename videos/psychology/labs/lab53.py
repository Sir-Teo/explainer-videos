"""Lab 53: people at work: range restriction and its corrections, Taylor-Russell, utility, adverse impact, the
validity-diversity frontier, and interviews combined by judgement or by rule."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "People at Work"
GOAL = ("Watch selection hide a test's validity, correct it in the right order, turn validity into outcomes and money, "
        "and find where an organization can stand between validity and adverse impact.")
TASKS = [
    "Hire the top 5% instead of 20%. How low does the observed validity fall, and does the correction still recover "
    "the truth?",
    "Apply the Case II correction to an unrestricted study with u = 2. How far does it overshoot?",
    "Make the interview's group difference 0.6 SD instead of 0.3. What happens to the frontier?",
]


def run(seed=0):
    out = labs.Lab()
    s = Wk.selection(n=100000, seed=seed + 1)
    assert s["r_obs"] < 0.3 and abs(s["r_both"] - s["r_all_true"]) < 0.05
    out.row("observed among hires; corrected (rel., then Case II); truth",
            f"{s['r_obs']:.2f}; {s['r_both']:.2f}; {s['r_all_true']:.2f}")
    out.row("overshoot: unrestricted 0.39 corrected with u = 2.1", f"{Wk.case2(0.39 / np.sqrt(0.6), 2.1):.2f}")
    tr = Wk.taylor_russell(0.3, 0.5, 0.2)
    assert 0.64 < tr < 0.70
    out.row("Taylor-Russell: r 0.3, top 20%, base rate 0.5", f"{tr:.3f}")
    u = Wk.bcg_utility(0.42, 0.2, 20000, n_hired=100, years=5, cost_per_applicant=100)
    out.row("utility: structured interview, net", f"{u['net']:,.0f}")
    ai = Wk.adverse_impact(0.8, 0.2)
    assert ai["impact_ratio"] < 0.8
    out.row("impact ratio at d = 0.8, 20% hired", f"{ai['impact_ratio']:.2f}")
    fr = Wk.frontier()
    k = int(np.argmax(fr["validity"]))
    out.row("frontier: best validity and its impact ratio", f"{fr['validity'][k]:.3f}; {fr['impact'][k]:.2f}")
    iv = Wk.interviews(n=20000, seed=seed + 2)
    assert iv["mechanical"] > iv["holistic"]
    out.row("test; unstructured; holistic; mechanical", f"{iv['test']:.2f}; {iv['unstructured']:.2f}; "
            f"{iv['holistic']:.2f}; {iv['mechanical']:.2f}")

    out.note = ("Selection and unreliable criteria hide validity; corrections restore it only when they model what "
                "actually happened; the same information combined by rule predicts better than by impression.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    x, y, h = s["x"], s["y"], s["hired"].astype(bool)
    ax[0].scatter(x[~h], y[~h], s=3, color="lightgrey")
    ax[0].scatter(x[h], y[h], s=4, color=labs.BLUE)
    ax[0].set(title="the hired are a narrow slice", xlabel="test (z)", ylabel="rating (z)")
    ax[1].plot(fr["impact"], fr["validity"], "o-", ms=3)
    ax[1].set(title="validity against impact ratio", xlabel="impact ratio", ylabel="validity")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
