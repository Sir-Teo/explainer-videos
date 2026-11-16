"""Lab 42: a therapy trial with four arms and regression to the mean, the effect against each control, researcher
allegiance, a random-effects meta-analysis by hand, a publication filter, and reliable change."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import clinic as K

TITLE = "Does Therapy Work?"
GOAL = ("Run a therapy trial in which everyone enrols at their worst; compare one therapy with three controls; let "
        "loyal teams compare two equal therapies; pool trials with DerSimonian and Laird; filter a literature by "
        "significance; and decide whether one client changed reliably.")
TASKS = [
    "Lower the enrolment threshold from 20 to 14 (everyone enrols). How much does the untreated arm improve now?",
    "Make every trial in the publication filter four times larger. How much of the inflation remains, and why?",
    "Find the reliability a scale needs for a 5-point change to count as reliable when its SD is 7.",
]


def run(seed=0):
    out = labs.Lab()

    for a in K.ARMS:
        r = K.therapy_trial(a, seed=seed)
        out.row(f"arm '{a}': mean at entry; at the end", f"{r['pre'].mean():.1f}; {r['post'].mean():.1f}")
    none = K.therapy_trial("none", seed=seed)
    assert none["change"] < -3
    for b in ("waitlist", "none", "placebo"):
        out.row(f"active therapy against {b}: d (2,000 per arm)", f"{K.trial_effect('active', b, n=2000, seed=seed):.2f}")

    al = K.allegiance(seed=seed)
    out.row("allegiance: pooled; by A's loyalists; by B's",
            f"{K.random_effects(al['d'], al['v'])['mu']:+.2f}; "
            f"{K.random_effects(al['d'][al['loyal'] > 0], al['v'][al['loyal'] > 0])['mu']:+.2f}; "
            f"{K.random_effects(al['d'][al['loyal'] < 0], al['v'][al['loyal'] < 0])['mu']:+.2f}")

    small = K.random_effects([0.4, 0.6, 0.2], [0.04, 0.02, 0.05])
    out.row("three trials by hand: fixed estimate; Q; tau^2; random-effects estimate",
            f"{small['fixed']:.3f}; {small['Q']:.2f}; {small['tau2']:.4f}; {small['mu']:.3f}")
    assert abs(small["fixed"] - 44 / 95) < 1e-9

    p = K.publication_filter(seed=seed)
    allr, pub = K.random_effects(p["d"], p["v"]), K.random_effects(p["d"][p["published"]], p["v"][p["published"]])
    out.row("400 trials of d = 0.3: published; pooled published effect; pooled all",
            f"{int(p['published'].sum())}; {pub['mu']:.2f}; {allr['mu']:.2f}")
    assert pub["mu"] > allr["mu"]

    thr = 1.96 * np.sqrt(2) * 7 * np.sqrt(1 - 0.85)
    out.row("reliable change for SD 7, reliability 0.85; cut-off for 28 (6) against 7 (5)",
            f"{thr:.1f} points; {K.jt_cutoff(28, 6, 7, 5):.1f}")
    out.row("RCI for 26 to 20", f"{float(K.reliable_change(26, 20, 7, 0.85)):.2f}")

    out.note = ("Every arm improves because people enrol at their worst; the effect depends on the control; loyal "
                "teams find their own therapy ahead; random-effects weights pool trials; a significance filter "
                "inflates the published effect; and the reliable change index separates change from measurement "
                "error.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    names = list(K.ARMS)
    ax[0].bar(range(4), [K.therapy_trial(a, seed=seed)["post"].mean() for a in names],
              color=[labs.GOLD, labs.RED, labs.BLUE, labs.GREEN])
    ax[0].axhline(none["pre"].mean(), color="grey", ls=":")
    ax[0].set_xticks(range(4), names)
    ax[0].set(title="Every arm improves", ylabel="symptoms at the end")
    se = np.sqrt(p["v"])
    ax[1].scatter(p["d"][~p["published"]], se[~p["published"]], s=6, color="lightgrey", label="unpublished")
    ax[1].scatter(p["d"][p["published"]], se[p["published"]], s=6, color=labs.GOLD, label="published")
    ax[1].invert_yaxis()
    ax[1].set(title="A filtered literature", xlabel="d", ylabel="SE")
    ax[1].legend(fontsize=8)
    s = np.linspace(0, 52, 200)
    ax[2].plot(s, K.dose_response(s), color=labs.GREEN)
    ax[2].set(title="Dose and response", xlabel="sessions", ylabel="share improved")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
