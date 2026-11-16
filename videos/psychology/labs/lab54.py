"""Lab 54: the science of learning: review schedules on Part 21's memory model, the value of spacing against more
reviews, and the simple view of reading."""

import warnings

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

warnings.filterwarnings("ignore", category=RuntimeWarning)
TITLE = "The Science of Learning"
GOAL = ("Race massed, expanding, equal and model-chosen review schedules at equal study time, and see that where a "
        "review goes matters more than how many there are.")
TASKS = [
    "Move the test from day 60 to day 30. Which schedule wins now, and why?",
    "Give the learner six reviews instead of four. How much does each policy gain?",
    "Make the items easier (base 0.3). Does spacing still matter as much?",
]


def run(seed=0):
    out = labs.Lab()
    res = {p: Wk.schedule(p, seed=seed + 1, base=0.6, n_items=40) for p in ("massed", "expanding", "fixed", "model")}
    assert res["massed"]["recall"] < res["expanding"]["recall"] <= res["fixed"]["recall"] + 0.02
    for p, r in res.items():
        out.row(f"{p}: recall on day 60; review days", f"{r['recall']:.2f}; " +
                ", ".join(f"{t:.1f}" for t in r["first_item_times"][1:]))
    one_spaced = Wk.schedule("fixed", reviews=1, seed=seed + 2, base=0.6, n_items=40)["recall"]
    eight_massed = Wk.schedule("massed", reviews=8, seed=seed + 2, base=0.6, n_items=40)["recall"]
    assert one_spaced > eight_massed
    out.row("one spaced review against eight massed", f"{one_spaced:.2f} against {eight_massed:.2f}")
    out.row("simple view: decoding 0.4, comprehension 0.9", f"{float(Wk.simple_view(0.4, 0.9)):.2f}")

    out.note = ("Spacing at all is most of the gain; the shape of the schedule matters less and depends on when the "
                "knowledge is needed.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].bar(list(res), [r["recall"] for r in res.values()], color=labs.BLUE)
    ax[0].set(title="recall on day 60, four reviews each", ylabel="recall")
    ks = [1, 2, 4, 8]
    ax[1].plot(ks, [Wk.schedule("massed", reviews=k, seed=seed + 3, base=0.6, n_items=30)["recall"] for k in ks],
               "o-", label="massed")
    ax[1].plot(ks, [Wk.schedule("fixed", reviews=k, seed=seed + 3, base=0.6, n_items=30)["recall"] for k in ks],
               "o-", label="spaced")
    ax[1].set(title="reviews per item", xlabel="reviews", ylabel="recall on day 60")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
