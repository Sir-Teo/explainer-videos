"""Lab 55: behaviour change at scale: the algebra of a default, a megastudy's winner's curse and shrinkage, and a
publication filter that separates journals from nudge units."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "Behaviour Change at Scale"
GOAL = ("Solve a default for its inertia, watch a megastudy crown a lucky winner and shrink it back, and see how a "
        "publication filter triples the average effect.")
TASKS = [
    "Double the people per arm in the megastudy. How much smaller is the winner's curse?",
    "Make every arm's true effect zero. What does the winner look like, and what does shrinkage do?",
    "Let academic trials publish every result. How close do the two literatures come?",
]


def run(seed=0):
    out = labs.Lab()
    d = Wk.default_inertia(0.37, 0.86)
    assert abs(d["inertia"] - 0.49) < 1e-9
    out.row("default: inertia q; preference p", f"{d['inertia']:.2f}; {d['prefer']:.2f}")
    m = Wk.megastudy(seed=seed + 1)
    out.row("megastudy winner: estimate; truth; shrunk (points)",
            f"{100 * m['winner_est']:+.1f}; {100 * m['winner_true']:+.1f}; {100 * m['winner_shrunk']:+.1f}")
    est, tru, shr = [], [], []
    for r in range(150):
        mm = Wk.megastudy(seed=seed + 100 + r)
        est.append(mm["winner_est"]); tru.append(mm["winner_true"]); shr.append(mm["winner_shrunk"])
    est, tru, shr = map(np.array, (est, tru, shr))
    assert est.mean() > tru.mean() and np.mean((shr - tru) ** 2) < np.mean((est - tru) ** 2)
    out.row("150 megastudies: mean winner estimate, truth, shrunk",
            f"{100 * est.mean():+.1f}, {100 * tru.mean():+.1f}, {100 * shr.mean():+.1f}")
    g = Wk.publication_gap(seed=seed + 2)
    assert g["academic"]["mean_reported"] > 2 * g["units"]["mean_reported"]
    out.row("published academic average; nudge units (points)",
            f"{100 * g['academic']['mean_reported']:.1f}; {100 * g['units']['mean_reported']:.1f}")

    out.note = ("Selecting the best arm, or the significant study, selects luck; shrinkage and complete reporting "
                "take it back out.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(100 * m["true"], 100 * m["est"], s=12, label="estimate")
    ax[0].scatter(100 * m["true"], 100 * m["shrunk"], s=12, label="shrunk")
    lim = [-4, 8]
    ax[0].plot(lim, lim, "k:")
    ax[0].set(title="53 arms", xlabel="true effect (points)", ylabel="estimate (points)")
    ax[0].legend()
    ax[1].bar(["published", "units", "truth"], [100 * g["academic"]["mean_reported"], 100 * g["units"]["mean_reported"],
                                                100 * g["truth"]], color=labs.BLUE)
    ax[1].set(title="one distribution of effects, two literatures", ylabel="average effect (points)")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
