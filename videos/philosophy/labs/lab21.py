"""Lab 21: simulate a lifetime of memories and watch connectedness fade while continuity holds."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import persist

TITLE = "Connectedness fades, continuity holds"
GOAL = ("Simulate eighty years of memories that each survive a year with probability 0.95, and compare the share of "
        "the ten-year-old's memories still held at each age with 0.95 to the power of the years between; then check "
        "Reid's officer and Evans's count of indeterminate identities against their closed forms.")
TASKS = [
    "Lower keep to 0.80. At what age is half of the ten-year-old gone, and does year-to-year continuity still hold "
    "if a link needs an overlap of 0.9?",
    "Add a fourth person to persist.reid's chain in your own copy (a boy, an officer, a general, a pensioner) and "
    "count the pairs that memory links directly and the pairs its ancestral links.",
    "Run persist.weight_drift(step=0.1) and compare the step at which similarity to the original falls below one "
    "half with the film's twenty-fourth.",
]


def run(seed=0):
    lab = labs.Lab()
    keep, ref = 0.95, 10
    life = persist.memory_chain(keep=keep, ref_age=ref, seed=seed)
    ages = np.arange(ref, life["years"])
    conn = np.array(life["connectedness"][ref:], float)
    theory = keep ** (ages - ref)
    half_theory = ref + int(np.ceil(np.log(0.5) / np.log(keep)))
    lab.row("ten-year-old's memories held at 24", f"{conn[14]:.3f}   (theory 0.95^14 = {theory[14]:.3f})")
    lab.row("first age with under half of them", f"{life['half_at']}   (theory {half_theory})")
    lab.row("held at 79", f"{conn[-1]:.3f}   (theory {theory[-1]:.3f})")
    lab.row("smallest year-to-year overlap", f"{life['year_to_year_min']:.3f}   (theory about {keep})")
    assert np.max(np.abs(conn - theory)) < 0.04, "connectedness decays geometrically"
    assert abs(life["half_at"] - half_theory) <= 2
    assert conn[-1] < 0.08 and life["year_to_year_min"] > 0.92, "connectedness is nearly gone, continuity never breaks"

    reid = persist.reid()
    lab.row("Reid: general remembers the boy", f"directly {reid['direct_boy_general']}, through a chain "
            f"{reid['closure_boy_general']}")
    assert not reid["direct_transitive"] and not reid["direct_boy_general"] and reid["closure_boy_general"]

    for n, k in ((3, 3), (2, 2), (2, 4)):
        e = persist.evans(n, k)
        closed = n ** k * (n ** k - 1 - (n - 1) ** k)  # pairs of name-assignments equal somewhere, not everywhere
        assert e["rigid_vague"] == 0, "rigid names never make identity indeterminate"
        assert e["nonrigid_vague"] == closed and e["all_pairs"] == n ** (2 * k)
    e = persist.evans()
    lab.row("Evans: indeterminate identities", f"{e['rigid_vague']} of {e['rigid_pairs']} with rigid names, "
            f"{e['nonrigid_vague']} of {e['all_pairs']} with shifting names")
    lab.note = ("Direct connections to an earlier self decay like keep^years, so the old man shares almost nothing "
                "with the boy, yet each year overlaps the next by about 95%: the chain, not the direct link, carries "
                "a person through a life.")

    drift = persist.weight_drift(seed=seed)
    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(ages, conn, color=labs.BLUE, label="memories of the ten-year-old still held")
    ax[0].plot(ages, theory, color=labs.GOLD, ls="--", label="0.95^(age - 10)")
    ax[0].axhline(life["year_to_year_min"], color=labs.GREEN, label="smallest year-to-year overlap")
    ax[0].axhline(0.5, color=labs.MUTED, lw=0.8, ls=":")
    ax[0].set(title="A simulated life: connectedness and continuity", xlabel="age", ylabel="share", ylim=(0, 1.05))
    ax[0].legend(loc="center right")
    ax[1].plot(drift["to_original"], color=labs.BLUE, label="similarity to the original weights")
    ax[1].plot(range(1, len(drift["to_previous"]) + 1), drift["to_previous"], color=labs.GREEN,
               label="similarity to the previous version")
    ax[1].axhline(0.5, color=labs.MUTED, lw=0.8, ls=":")
    ax[1].set(title="A model's weights through forty updates", xlabel="update", ylabel="cosine similarity",
              ylim=(0, 1.05))
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
