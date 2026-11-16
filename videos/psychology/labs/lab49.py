"""Lab 49: the brain's data: fixed against random effects, a leaky decoder, ERP windows chosen from the answer,
global-signal regression, the population vector and brain-behaviour correlations by sample size."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import neurodata as N

TITLE = "Modelling the Brain's Data"
GOAL = ("Run the analysis choices that mislead on a brain whose truth is known: fixed effects, leaky decoding, "
        "windows chosen from the data, global-signal regression and small samples.")
TASKS = [
    "Shrink the person-to-person spread (between = 0.2). How far do fixed effects' false positives fall?",
    "Select 200 voxels instead of 50 in the leaky decoder. Does the leak grow or shrink?",
    "Run the brain-behaviour simulation with a true r of 0.3. At what sample size do reported correlations stop "
    "being inflated?",
]


def run(seed=0):
    out = labs.Lab()
    fx = N.fixed_vs_random(reps=60, seed=seed + 1)
    assert fx["fixed"] > fx["random"]
    out.row("null voxels below p < .001: fixed effects; random effects", f"{fx['fixed']:.3f}; {fx['random']:.4f}")
    dc = N.decoding(trials=30, voxels=500, reps=20, seed=seed + 2)
    assert dc["leaky"] > dc["nested"]
    out.row("decoding noise: all voxels; selected inside folds; selected first", f"{dc['all']:.2f}; {dc['nested']:.2f}; "
            f"{dc['leaky']:.2f}")
    e = N.erp_windows(reps=400, seed=seed + 3)
    out.row("ERP false positives: fixed window; peak of difference; peak of average",
            f"{e['a_priori']:.3f}; {e['double_dip']:.3f}; {e['orthogonal']:.3f}")
    g = N.global_signal(seed=seed + 4)
    out.row("between-network r: raw; after global-signal regression", f"{g['between_raw']:.2f}; {g['between_gsr']:.2f}")
    p = N.population_vector_error(seed=seed + 5)
    out.row("population vector error (deg) with 4, 64, 256 neurons",
            ", ".join(f"{p['error_deg'][list(p['n']).index(k)]:.1f}" for k in (4, 64, 256)))
    b = N.bwas(true_r=0.1, seed=seed + 6)
    out.row("reported |r| among significant results at n = 25, 500, 4000",
            ", ".join(f"{b['reported'][list(b['n']).index(k)]:.2f}" for k in (25, 500, 4000)))

    out.note = ("Each misleading choice looks reasonable in a single analysis; only a known truth, or a fixed plan, "
                "shows what it does.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].bar(["all", "nested", "leaky"], [dc["all"], dc["nested"], dc["leaky"]],
              color=[labs.BLUE, labs.BLUE, labs.RED])
    ax[0].axhline(0.5, color="grey", ls=":")
    ax[0].set(title="decoding pure noise", ylabel="cross-validated accuracy")
    ax[1].plot(b["n"], b["reported"], "o-", color=labs.RED, label="reported |r| (significant)")
    ax[1].axhline(0.1, color="grey", ls=":")
    ax[1].set(xscale="log", title="the winner's curse in brain-behaviour studies", xlabel="people", ylabel="|r|")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
