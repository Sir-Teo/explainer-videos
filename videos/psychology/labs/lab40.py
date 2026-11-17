"""Lab 40: Mowrer's avoidance loop and response prevention, renewal after context-bound extinction, the triadic
design as a belief about control, and a model of momentary mood fitted to a gambling task."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import clinic as K

TITLE = "Fear and Sadness"
GOAL = ("Let a Rescorla-Wagner learner avoid a feared signal and watch its fear survive; prevent the response and "
        "watch it fall; extinguish fear in one context and test it in others; run the triadic design as a belief "
        "about control; and fit a model of momentary mood, then blunt its prediction errors.")
TASKS = [
    "Raise the avoidance threshold from 0.3 to 0.6. How much fear is left after 60 trials, and why?",
    "In the renewal model, extinguish in two contexts in turn and test in a third. Which version of the model would "
    "predict less renewal, and what would it need?",
    "Give the inescapable group 16 pretreatment trials instead of 64. How much of the helplessness remains?",
]


def run(seed=0):
    out = labs.Lab()

    runs = [K.avoidance(seed=seed + s) for s in range(21)]
    finals = np.array([r["fear"][-1] for r in runs])
    prevent = K.avoidance(prevent=True)
    out.row("fear after 60 trials without shock: allowed to avoid (median of 21); response prevention",
            f"{np.median(finals):.2f}; {prevent['fear'][-1]:.2f}")
    assert np.median(finals) > 0.5 and prevent["fear"][-1] < 0.05
    exposures = int(np.ceil(np.log(0.3 / 0.9) / np.log(0.92)))
    out.row("full exposures to bring fear from 0.9 below 0.3 at extinction rate 0.08", str(exposures))
    assert exposures == 14

    r = K.renewal()
    out.row("fear at test: context B (extinction); A (acquisition); C (new)",
            f"{r['test']['B']:.2f}; {r['test']['A']:.2f}; {r['test']['C']:.2f}")
    assert r["test"]["B"] < 0.05 and r["test"]["A"] > 0.9

    groups = {p: K.helplessness(p, seed=seed) for p in ("escapable", "inescapable", "none")}
    out.row("share escaping across 10 test trials: escapable first; inescapable first; no shock first",
            "; ".join(f"{100 * groups[p].mean():.0f}%" for p in ("escapable", "inescapable", "none")))
    assert groups["escapable"].mean() > groups["none"].mean() > groups["inescapable"].mean()
    out.row("Beta(1, 1) after 10 failures; after 10 successes: probability of trying",
            f"{1 / 12:.3f}; {11 / 12:.3f}")

    ctx = K.renewal_contexts()
    out.row("fear in a new place after extinction in 1, 3 and 6 contexts",
            "; ".join(f"{ctx['fear'][i]:.2f}" for i in (0, 2, 5)))
    stuck = np.median([K.activation(0, seed=seed + s)["active"][-30:].mean() for s in range(21)])
    freed = np.median([K.activation(14, seed=seed + s)["active"][-30:].mean() for s in range(21)])
    out.row("share of active days in the last month: left alone; activity scheduled for 14 days",
            f"{100 * stuck:.0f}%; {100 * freed:.0f}%")
    assert stuck < 0.2 and freed > 0.8

    d = K.mood_task(seed=seed)
    f = K.fit_mood(d)
    b = K.mood_task(seed=seed, rpe_scale=0.4)
    out.row("mood model: true and fitted prediction-error weight; fitted forgetting; R squared",
            f"{d['true_w'][3]:.2f}, {f['w'][3]:.2f}; {f['gamma']:.2f}; {f['r2']:.2f}")
    out.row("SD of happiness: normal; prediction errors blunted to 40%",
            f"{np.std(d['happy']):.2f}; {np.std(b['happy']):.2f}")
    assert np.std(b["happy"]) < np.std(d["happy"])
    h10 = 0.5 + 0.6 * 0.5 * (1 - 0.7 ** 10) / (1 - 0.7)
    out.row("H_10 when every prediction error is 0.5 (gamma 0.7, w0 0.5, w3 0.6)", f"{h10:.2f}")

    out.note = ("Avoidance protects fear from the test that would extinguish it; extinction learned in one context "
                "leaves fear intact in others; a learner that finds its actions do nothing stops trying; and a model "
                "of mood built on recent prediction errors fits momentary ratings, with blunted errors flattening "
                "mood.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    k = int(np.argsort(finals)[len(finals) // 2])
    ax[0].plot(runs[k]["fear"], color=labs.RED, label="allowed to avoid")
    ax[0].plot(prevent["fear"], color=labs.GREEN, label="response prevention")
    ax[0].axvline(20, color="grey", ls=":")
    ax[0].set(title="Avoidance keeps fear alive", xlabel="trial", ylabel="fear V")
    ax[0].legend(fontsize=8)
    for p, c in (("escapable", labs.GREEN), ("none", labs.BLUE), ("inescapable", labs.RED)):
        ax[1].plot(np.arange(1, 11), groups[p], "o-", color=c, label=p)
    ax[1].set(title="The triadic design", xlabel="test trial", ylabel="share escaping", ylim=(0, 1.05))
    ax[1].legend(fontsize=8)
    ax[2].plot(d["happy"], color=labs.GOLD, alpha=0.6, label="ratings")
    ax[2].plot(f["fit"], color=labs.BLUE, label="model")
    ax[2].plot(b["happy"], color=labs.RED, alpha=0.5, label="blunted")
    ax[2].set(title="Momentary mood", xlabel="trial", ylabel="happiness")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
