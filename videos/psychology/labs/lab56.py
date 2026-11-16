"""Lab 56: psychology and law: simultaneous and sequential line-ups by ROC, confidence and feedback, a calibrated
risk score across groups, and the error around a test score."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "Psychology and Law"
GOAL = ("Compare line-up procedures by their whole ROC rather than one ratio, see confidence inflate after feedback, "
        "and find why a calibrated risk score cannot have equal error rates across groups.")
TASKS = [
    "Lower the culprit's memory strength (d' = 1.0). Does the simultaneous advantage grow or shrink?",
    "Make the feedback boost two levels. What happens to accuracy at the top confidence level?",
    "Give the two groups equal base rates. Do the error rates now match?",
]


def run(seed=0):
    out = labs.Lab()
    s = Wk.lineup_roc("simultaneous", n=60000, seed=seed + 1)
    q = Wk.lineup_roc("sequential", n=60000, seed=seed + 2)
    up = float(min(s["fa"].max(), q["fa"].max()))
    ps, pq = Wk.partial_auc(s["fa"], s["hit"], up), Wk.partial_auc(q["fa"], q["hit"], up)
    assert ps > pq
    out.row("partial ROC area: simultaneous; sequential", f"{ps:.3f}; {pq:.3f}")
    c = Wk.confidence_feedback(n=100000, seed=seed + 3)
    assert c["initial"][-1] > c["after"][-1]
    out.row("top-level accuracy: initial; after feedback", f"{c['initial'][-1]:.3f}; {c['after'][-1]:.3f}")
    r = Wk.risk_groups(n=200000, seed=seed + 4)
    assert r[0.5]["fpr"] > r[0.3]["fpr"]
    out.row("false-positive rate, base 0.3; base 0.5", f"{r[0.3]['fpr']:.2f}; {r[0.5]['fpr']:.2f}")
    iv = Wk.score_interval(71, 0.97)
    out.row("IQ 71, reliability 0.97: 95% interval", f"{iv['lo']:.1f} to {iv['hi']:.1f}")

    out.note = ("A procedure is judged by the trade-off it offers, not one ratio; the first confidence is the useful "
                "one; fairness definitions conflict whenever base rates differ.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].plot(s["fa"], s["hit"], label="simultaneous")
    ax[0].plot(q["fa"], q["hit"], label="sequential")
    ax[0].set(xlim=(0, 0.2), title="line-up ROC", xlabel="innocent-suspect IDs", ylabel="culprit IDs")
    ax[0].legend()
    ax[1].plot(c["levels"], c["initial"], "o-", label="initial")
    ax[1].plot(c["levels"][1:], c["after"][1:], "o-", label="after feedback")
    ax[1].set(title="confidence-accuracy", xlabel="confidence level", ylabel="suspect IDs correct")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
