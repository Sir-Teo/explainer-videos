"""Lab 39: Cohen's kappa and why reliability caps validity, counting symptom combinations, a positive screen in
natural frequencies, a symptom network with hysteresis, and formulas against a wandering clinician."""

from itertools import combinations

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import clinic as K

TITLE = "What Is a Disorder?"
GOAL = ("Compute Cohen's kappa by hand and for two simulated clinicians; count the symptom combinations a "
        "five-of-nine rule allows; work a screen at several base rates; sweep stress up and down through a symptom "
        "network; and compare a formula with a clinician whose weights wander.")
TASKS = [
    "Change the depression rule to six of nine symptoms. How many combinations qualify now, and what is the "
    "smallest overlap between two people with the diagnosis?",
    "Find the prevalence at which the screen's positive predictive value reaches 50%.",
    "Lower the connection strength c of the symptom network step by step. At what value does the hysteresis loop "
    "close?",
]


def run(seed=0):
    out = labs.Lab()

    out.row("kappa for the table [[20, 5], [10, 65]]", f"{K.kappa([[20, 5], [10, 65]]):.3f}")
    assert abs(K.kappa([[20, 5], [10, 65]]) - 0.625) < 1e-9
    for nz in (0.25, 0.5, 1.0, 2.0):
        r = K.two_clinicians(noise=nz, seed=seed)
        out.row(f"two clinicians, noise {nz}: kappa between them; kappa with the truth",
                f"{r['kappa']:.2f}; {r['validity']:.2f}")

    sets = [set(c) for r in range(5, 10) for c in combinations(range(9), r) if 0 in c or 1 in c]
    out.row("combinations meeting five of nine, with symptom 1 or 2", str(len(sets)))
    assert len(sets) == 227

    for prev in (0.01, 0.1, 0.3):
        s = K.screen(prevalence=prev)
        out.row(f"screen, sensitivity 0.9, specificity 0.91, prevalence {prev}: positive predictive value",
                f"{s['ppv']:.3f}")

    strong = K.sweep(c=1.0, reps=10, seed=seed)
    weak = K.sweep(c=0.2, reps=10, seed=seed)
    out.row("largest gap between the way down and the way up: strong; weak network",
            f"{np.max(strong['down'] - strong['up']):.1f}; {np.max(weak['down'] - weak['up']):.1f} symptoms")

    m = K.clinician_vs_formula(seed=seed)
    out.row("correlation with the outcome on new cases: true weights; fitted; equal; clinician",
            f"{m['ceiling']:.2f}; {m['fitted']:.2f}; {m['unit']:.2f}; {m['clinician']:.2f}")

    out.note = ("Kappa removes chance agreement; as clinicians' noise grows, they agree less with each other and with "
                "the truth; a five-of-nine rule admits 227 combinations; a screen's meaning depends on the base rate; "
                "a strongly connected symptom network shows hysteresis; and a consistent formula beats a clinician "
                "who weighs the same cues a little differently each time.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    noise = np.linspace(0, 2.5, 11)
    rs = [K.two_clinicians(noise=float(n), seed=seed) for n in noise]
    ax[0].plot(noise, [r["kappa"] for r in rs], "o-", color=labs.BLUE, label="clinician with clinician")
    ax[0].plot(noise, [r["validity"] for r in rs], "o-", color=labs.GREEN, label="clinician with truth")
    ax[0].set(title="Reliability caps validity", xlabel="observation noise (SD)", ylabel="kappa")
    ax[0].legend(fontsize=8)
    ax[1].plot(strong["levels"], strong["up"], color=labs.RED, label="strong, stress rising")
    ax[1].plot(strong["levels"], strong["down"], color=labs.BLUE, label="strong, stress falling")
    ax[1].plot(weak["levels"], weak["up"], color=labs.GOLD, ls="--", label="weak")
    ax[1].set(title="Hysteresis", xlabel="stress", ylabel="active symptoms")
    ax[1].legend(fontsize=8)
    prevs = np.linspace(0.005, 0.5, 100)
    ax[2].plot(prevs, [K.screen(prevalence=p)["ppv"] for p in prevs], color=labs.GOLD)
    ax[2].set(title="Positive predictive value", xlabel="prevalence", ylabel="P(case | positive)")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
