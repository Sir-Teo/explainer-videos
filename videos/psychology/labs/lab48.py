"""Lab 48: modelling behaviour: jumping learners and their average, four models of a reversal bandit fitted by
maximum likelihood, parameter and model recovery, a posterior predictive check, and shrinkage across people."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import fit as F

TITLE = "Modelling Behaviour"
GOAL = ("Simulate learners, fit four models to their choices, check that the fits recover what was planted, and "
        "check that the winning model makes the effect it should.")
TASKS = [
    "Cut the trials from 200 to 60. How far do the recovered learning rates spread?",
    "Simulate a learner with negative perseveration (kappa = -1.5). Does the posterior predictive check still work?",
    "Give the group 200 trials each. How much does shrinkage still help?",
]


def run(seed=0):
    out = labs.Lab()
    j = F.jump_learners(seed=seed + 1)
    out.row("jumping learners: average correct on trials 1, 5, 20", ", ".join(f"{j['mean'][t - 1]:.2f}" for t in (1, 5, 20)))
    C, R = F.simulate("q", (0.3, 5.0), seed=seed + 2)
    fits = {m: F.fit(m, C, R) for m in F.MODELS}
    best = min(fits, key=lambda m: fits[m]["bic"])
    assert best in ("q", "q_persev")
    out.row("BIC: random; win-stay lose-shift; Q; Q with perseveration",
            "; ".join(f"{fits[m]['bic']:.1f}" for m in F.MODELS))
    out.row("Q-learner fitted (planted 0.3, 5)", f"alpha {fits['q']['params'][0]:.2f}, beta {fits['q']['params'][1]:.2f}")
    rec = F.recovery([0.2, 0.5, 0.8], [2.0, 5.0, 10.0], reps=2, seed=seed + 3)
    assert rec["r_alpha"] > 0.5
    out.row("recovery: correlation of true and fitted alpha; beta", f"{rec['r_alpha']:.2f}; {rec['r_beta']:.2f}")
    a = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q", n=10, seed=seed + 4)
    b = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q_persev", n=10, seed=seed + 4)
    out.row("stay after a loss: data; Q predicts; Q with perseveration predicts",
            f"{a['obs'][1]:.2f}; {a['pred'][1]:.2f}; {b['pred'][1]:.2f}")
    g = F.group_fit(n_people=20, seed=seed + 5)
    out.row("learning rates (logit): RMSE alone; shrunk", f"{g['rmse_ml']:.2f}; {g['rmse_eb']:.2f}")

    out.note = ("A smooth average can hide steps; a fit is only as good as its recovery; and the model that wins on "
                "BIC must still make the effect the data show.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    for row in j["each"][:6]:
        ax[0].step(j["t"], row, where="post", lw=1, alpha=0.6)
    ax[0].plot(j["t"], j["mean"], color="k", lw=2.5)
    ax[0].set(title="each learner jumps; the average glides", xlabel="trial", ylabel="P(correct)")
    ax[1].scatter(rec["true_alpha"], rec["est_alpha"], color=labs.BLUE)
    ax[1].plot([0, 1], [0, 1], color="grey", ls=":")
    ax[1].set(title="parameter recovery", xlabel="true alpha", ylabel="fitted alpha")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
