"""Lab 13: find the Dutch book against random credences by linear programming, and check accuracy dominance."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import credence as Cr

TITLE = "Two arguments for the probability axioms, run on random credences"
GOAL = ("Draw 150 credence assignments over three exclusive, exhaustive worlds. For each, let the Reasoner's linear "
        "program look for a Dutch book and project the credence onto the simplex, then check both theorems: the "
        "sure loss is |sum - 1|, and the projection has a smaller Brier score in every world.")
TASKS = [
    "Add a fourth proposition, 'world a or world b', with its own credence, and find a book against a credence "
    "that sums to 1 on the worlds but breaks additivity on the disjunction.",
    "Replace the Brier score by absolute error (sum of |c_i - v_i|) and find an incoherent credence that its "
    "projection does not dominate.",
    "Copy Cr.dutch_book and widen its stake bounds from 1 to 5. How does the sure loss scale, and why is a bound needed?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    worlds = ["a", "b", "c"]
    props = {w: {w} for w in worlds}
    lab = labs.Lab()

    # the film's first book: credence 0.6 in A and 0.6 in not-A
    film = Cr.dutch_book(["A", "notA"], {"A": {"A"}, "notA": {"notA"}}, {"A": 0.6, "notA": 0.6})
    assert abs(film["sure_loss"] - 0.2) < 1e-6, "the film's 20-cent book"
    lab.row("credences (0.6, 0.6) in A and not-A", f"sure loss {film['sure_loss']:.2f}   stakes {film['stakes']}")

    n = 150
    excess, loss, gain = [], [], []
    for _ in range(n):
        c = rng.uniform(0, 1, 3)
        book = Cr.dutch_book(worlds, props, dict(zip(worlds, c)))
        sure = book["sure_loss"] if book else 0.0
        if book:  # the agent loses in every world, and by exactly the same amount when the stakes are +-1
            assert max(book["payoff"].values()) < 0, "a book loses in every world"
        d = Cr.dominance(list(c))
        assert d["dominates"], "the projection is closer to the truth in every world"
        assert abs(sum(d["projection"]) - 1) < 1e-9 and min(d["projection"]) >= 0
        excess.append(abs(c.sum() - 1))
        loss.append(sure)
        gain.append(min(bc - bp for bc, bp in zip(d["brier_c"], d["brier_p"])))
    excess, loss, gain = np.array(excess), np.array(loss), np.array(gain)
    assert np.max(np.abs(loss - excess)) < 1e-5, "the sure loss is |sum of credences - 1|"

    coherent = rng.dirichlet(np.ones(3), 50)
    n_books = sum(not Cr.coherent(worlds, props, dict(zip(worlds, p))) for p in coherent)
    assert n_books == 0, "no book against a probability"

    lab.row("incoherent credences tried", f"{n}")
    lab.row("largest |LP sure loss - |sum - 1||", f"{np.max(np.abs(loss - excess)):.1e}   (theory 0)")
    lab.row("projection dominates in every world", f"{n} of {n}   (theory: all)")
    lab.row("smallest Brier improvement, worst world", f"{gain.min():.4f}   (theory: > 0)")
    lab.row("books found against 50 probabilities", f"{n_books}   (theory 0)")
    lab.note = ("Off the simplex a bookie has a sure profit equal to the distance of the credences' sum from 1, and "
                "the nearest coherent credence is more accurate whatever the truth is; on the simplex neither "
                "complaint can be made.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot([0, 2], [0, 2], color=labs.MUTED, ls="--", lw=1, label="theory: loss = |sum - 1|")
    ax[0].scatter(excess, loss, s=16, color=labs.GOLD, label="LP's guaranteed loss", zorder=3)
    ax[0].set(title="The Dutch book: the bookie's sure profit", xlabel="|sum of the three credences - 1|",
              ylabel="sure loss (stakes at most 1)", xlim=(0, max(excess) * 1.05), ylim=(0, max(excess) * 1.05))
    ax[0].legend(loc="upper left")
    ax[1].scatter(excess, gain, s=16, color=labs.GREEN, label="Brier(c) - Brier(projection), worst world")
    ax[1].axhline(0, color=labs.RED, lw=1, label="no improvement")
    ax[1].set(title="Accuracy: the projection wins in every world", xlabel="|sum of the three credences - 1|",
              ylabel="smallest improvement over the 3 worlds")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
