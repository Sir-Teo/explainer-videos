"""Lab 38: conformist and prestige-biased transmission, Henrich's model of population size and skill, the
reference-group effect, and an additive model of trolley judgments across countries."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import culture as C

TITLE = "Culture and Morals"
GOAL = ("Iterate conformist transmission and find its fixed points; compute Henrich's critical population and run "
        "small and large populations; simulate two cultures whose self-reports hide a real difference; and fit an "
        "additive logistic model to simulated trolley judgments in 42 countries.")
TASKS = [
    "Set the conformist bias D to a negative value (anti-conformity). What happens to a variant that starts at 45%, "
    "and why?",
    "Double beta, the luck in copying, in Henrich's model. How does the critical population change, and what does "
    "that say about innovation and population size?",
    "In the reference-group simulation, let culture B rate itself against culture A instead of against itself. "
    "Does the self-report gap come back?",
]


def run(seed=0):
    out = labs.Lab()

    for p0 in (0.3, 0.45, 0.55, 0.7):
        path = C.conformist_path(p0, 0.3, 40)
        out.row(f"conformist transmission, D = 0.3, start {p0}: share after 10 and 40 generations",
                f"{path[10]:.3f}; {path[40]:.3f}")
    sims = np.array([C.conformist_sim(400, 0.4, 0.3, 1, seed=seed + s)[1] for s in range(200)])
    out.row("finite learners, one generation from 0.40: mean share against the expected step",
            f"{sims.mean():.4f} vs {float(C.conformist_step(0.4, 0.3)):.4f}")
    assert abs(sims.mean() - C.conformist_step(0.4, 0.3)) < 0.01

    n_star = C.critical_size()
    out.row("Henrich's model, alpha 4.5, beta 1: critical population", f"{n_star:.1f}")
    for n in (20, 50, 200):
        z = C.tasmania(n, seed=seed + 38)
        out.row(f"best skill after 60 generations, N = {n} (start 10)", f"{max(z[-1], 0.0):.1f}")
    assert C.skill_change(20) < 0 < C.skill_change(200)

    r = C.reference_group(seed=seed)
    out.row("reference-group effect: true gap; self-report gap; behavioural gap (SD)",
            f"{r['gap_trait']:.2f}; {r['gap_report']:.2f}; {r['gap_behaviour']:.2f}")
    assert abs(r["gap_report"]) < 0.1 < r["gap_behaviour"]

    t = C.trolley(seed=seed + 38)
    f = C.fit_trolley(t["share"])
    out.row("trolley, 42 simulated countries: mean acceptance of Switch, Loop, Footbridge",
            "; ".join(f"{v:.2f}" for v in t["share"].mean(axis=0)))
    out.row("share of countries keeping the order Switch > Loop > Footbridge", f"{f['order_same']:.2f}")
    out.row("footbridge acceptance across countries: lowest; highest",
            f"{t['share'][:, 2].min():.2f}; {t['share'][:, 2].max():.2f}")

    out.note = ("Conformity pushes a population to whichever variant leads; a small population loses a skill that a "
                "large one improves; rating yourself against your own group can erase a real difference; and a "
                "shared case effect with country levels keeps the order of the trolley cases everywhere while the "
                "levels spread.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    for p0 in (0.3, 0.45, 0.55, 0.7):
        ax[0].plot(C.conformist_path(p0, 0.3, 40), color=labs.BLUE if p0 < 0.5 else labs.GOLD)
    ax[0].set(title="Conformist transmission", xlabel="generation", ylabel="share")
    for n, col in ((20, labs.RED), (50, labs.GOLD), (200, labs.GREEN)):
        ax[1].plot(np.maximum(C.tasmania(n, seed=seed + 38), 0), color=col, label=f"N = {n}")
    ax[1].set(title="Henrich's model", xlabel="generation", ylabel="best skill")
    ax[1].legend(fontsize=8)
    order = np.argsort(t["share"][:, 0])
    for k, col in enumerate((labs.BLUE, labs.GOLD, labs.RED)):
        ax[2].plot(t["share"][order, k], "o", ms=3, color=col, label=t["cases"][k])
    ax[2].set(title="Trolley cases, 42 countries", xlabel="country (ordered)", ylabel="share accepting")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
