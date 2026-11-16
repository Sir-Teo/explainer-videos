"""Lab 60: minds and machines: contamination, a benchmark as a test, silicon samples and a specification curve."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import machines as M

TITLE = "Minds and Machines"
GOAL = ("Simulate the traps of testing machines, treat a benchmark as a test, see what silicon samples lose, and "
        "run every defensible analysis of screen time and well-being.")
TASKS = [
    "Let the memorizer see only 30% of the items. Can you still detect contamination from the two scores?",
    "Give the silicon respondents their full spread (shrink = 1). Which errors remain?",
    "Drop the confounders from the simulated survey. What happens to the specification curve?",
]


def run(seed=0):
    out = labs.Lab()
    c = M.contamination(seed=seed)
    assert c["memorizer"][0] > c["memorizer"][1] + 0.3
    out.row("memorizer: published; reworded", f"{c['memorizer'][0]:.2f}; {c['memorizer'][1]:.2f}")
    out.row("reasoner: published; reworded", f"{c['reasoner'][0]:.2f}; {c['reasoner'][1]:.2f}")
    b = M.benchmark_irt(seed=seed, boot=200)
    out.row("leaderboard top stable under item bootstrap", f"{b['top_stable']:.2f}")
    out.row("information in the best fifth of items", f"{b['useful_share_info']:.2f}")
    s = M.silicon(seed=seed)
    assert s["silicon_sd"] < s["human_sd"]
    out.row("SD: people; silicon", f"{s['human_sd']:.2f}; {s['silicon_sd']:.2f}")
    sc = M.specification_curve(M.screen_data(seed=seed))
    out.row("specification curve: median beta; share p < .05; median R^2",
            f"{sc['median_beta']:.3f}; {sc['share_sig']:.2f}; {sc['median_r2']:.3f}")

    out.note = ("A new kind of subject needs psychology's old cautions: fresh items, many subjects, the full "
                "distribution, and every analysis reported.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].bar(np.arange(5) - 0.2, s["human_group"], 0.4, label="people")
    ax[0].bar(np.arange(5) + 0.2, s["silicon_group"], 0.4, label="silicon")
    ax[0].set(title="group means", xticks=range(5), xticklabels=[f"{100 * x:.0f}%" for x in s["shares"]])
    ax[0].legend()
    ax[1].plot(sc["beta"], ".", ms=3)
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="specification curve", xlabel="analysis (sorted)", ylabel="standardized effect")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
