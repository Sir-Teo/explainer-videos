"""Lab 61: the next psychology: prediction ceilings, a design space, and the natural selection of bad science."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import community as Cm

TITLE = "The Next Psychology"
GOAL = ("Run a prediction challenge under a known ceiling, map an effect across a space of experiments with a "
        "surrogate model, and watch incentives select methods.")
TASKS = [
    "Raise the strong variables' effects so the ceiling is 0.5. Do the teams pull away from the baseline?",
    "Run only 40 cells of the design space. How well does the surrogate predict the rest?",
    "Under registered reports, lower the minimum effort to 10. What happens to the false share?",
]


def run(seed=0):
    out = labs.Lab()
    c = Cm.challenge(teams=80, seed=seed)
    assert c["best"] < c["ceiling"]
    out.row("best team; four-variable baseline; ceiling", f"{c['best']:.3f}; {c['baseline']:.3f}; {c['ceiling']:.3f}")
    i = Cm.integrative(seed=seed)
    out.row("surrogate: held-out correlation; share of cells with a negative effect",
            f"{i['held_out_r']:.2f}; {i['share_negative']:.2f}")
    a = Cm.bad_science(seed=seed)
    b = Cm.bad_science(rule="registered", seed=seed)
    assert a["fdr"][-20:].mean() > b["fdr"][-20:].mean()
    out.row("false share of positives: publish positives; registered reports",
            f"{a['fdr'][-20:].mean():.2f}; {b['fdr'][-20:].mean():.2f}")

    out.note = ("A field's results depend on what it can predict, which experiments it runs, and what it rewards; "
                "each can be modelled, and changed.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].plot(np.sort(c["scores"]), ".", ms=4)
    ax[0].axhline(c["baseline"], color="red", lw=1, label="four variables")
    ax[0].axhline(c["ceiling"], color="green", lw=1, label="ceiling")
    ax[0].set(title="the challenge", xlabel="team (sorted)", ylabel="held-out R^2")
    ax[0].legend()
    ax[1].plot(a["fdr"], label="publish positives")
    ax[1].plot(b["fdr"], label="registered reports")
    ax[1].set(title="false share of published positives", xlabel="generation")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
