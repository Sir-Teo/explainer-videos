"""Lab 57: health and care: placebo analgesia as inference, and a stepped-care service's capacity."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "Health and Care"
GOAL = ("Model placebo analgesia as a prior on a noisy bodily signal, and find the capacity a stepped-care service "
        "needs to keep its waiting lists from growing.")
TASKS = [
    "Make the expectation more confident (prior SD 0.8). How large is the placebo effect now?",
    "Raise the share of severe referrals to 50%. Which step runs out of places first?",
    "Halve natural recovery while waiting. Which policy suffers most?",
]


def run(seed=0):
    out = labs.Lab()
    p = Wk.placebo_pain()
    assert 0 < p["effect"] < 2
    out.row("felt pain without and with placebo", f"{p['no_placebo']:.2f}; {p['placebo']:.2f}")
    b = Wk.placebo_by_noise()
    assert np.all(np.diff(b["effect"]) > 0)
    out.row("placebo effect by sensory noise", ", ".join(f"{e:.2f}" for e in b["effect"]))
    res = {k: Wk.stepped_care(k, weeks=78, seed=seed + 1) for k in ("high_only", "matched", "stepped")}
    res["rebalanced"] = Wk.stepped_care("stepped", weeks=78, low_slots=100, high_slots=60, seed=seed + 1)
    for k, r in res.items():
        out.row(f"{k}: wait (weeks); recovered in 26 weeks", f"{r['mean_wait']:.1f}; {r['recovered_26']:.2f}")
    assert res["rebalanced"]["mean_wait"] < res["stepped"]["mean_wait"] < res["high_only"]["mean_wait"]
    assert res["rebalanced"]["recovered_26"] > res["stepped"]["recovered_26"]

    out.note = ("Expectation matters most where the body's signal is vague; services fail most often not by "
                "choosing the wrong treatment but by queues that capacity cannot clear.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].plot(b["sensory_sd"], b["effect"], "o-")
    ax[0].set(title="placebo effect", xlabel="sensory noise (SD)", ylabel="pain reduction")
    ax[1].bar(list(res), [r["recovered_26"] for r in res.values()], color=labs.BLUE)
    ax[1].set(title="recovered within 26 weeks", ylabel="share")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
