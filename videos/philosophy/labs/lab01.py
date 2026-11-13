"""Lab 1: check all 256 syllogistic moods by Venn regions, then by Leibniz's characteristic numbers."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import syllogism as syl

TITLE = "The 256 moods, by regions and by numbers"
GOAL = ("Check every mood against all 256 arrangements of the eight Venn regions, with and without the assumption "
        "that every term is inhabited, and compare the survivors with the moods that no assignment of Leibniz's "
        "characteristic numbers refutes.")
TASKS = [
    "Require only the middle term M to be inhabited (filter syl.models() yourself). Which of the nine extra moods "
    "become valid, and which need S or P instead?",
    "Call syl.leibniz_countermodel(mood, primes=(2,)) for every mood. How many moods survive with one prime, and "
    "name one invalid mood that slips through.",
    "Add a fifth sentence form of your own to syl.holds (for example 'most x are y' on region counts) and recount "
    "the valid moods.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    moods = syl.all_moods()
    boolean = [m for m in moods if syl.valid(m)]
    trad = [m for m in moods if syl.valid(m, existential=True)]
    leib = [m for m in moods if syl.leibniz_countermodel(m) is None]
    extra = [m for m in trad if m not in boolean]

    # A seeded spot check on a larger stock of numbers: random term numbers over the primes 2, 3, 5, 7, 11.
    pairs = syl.leibniz_pairs((2, 3, 5, 7, 11))
    trials, refuted_valid, refuted_invalid = 3000, 0, set()
    for _ in range(trials):
        val = dict(zip("SMP", (pairs[i] for i in rng.integers(len(pairs), size=3))))
        for m in moods:
            prem, concl = syl.premises(m)
            if all(syl.leibniz_holds(k, val[x], val[y]) for k, x, y in prem) and not syl.leibniz_holds(
                    concl[0], val["S"], val["P"]):
                if m in trad:
                    refuted_valid += 1
                else:
                    refuted_invalid.add(m)

    darapti = syl.countermodel((3, "AAI"))
    lab = labs.Lab()
    by = lambda ms: [sum(1 for f, _ in ms if f == k) for k in (1, 2, 3, 4)]  # noqa: E731
    lab.row("moods", f"{len(moods)}   (4 figures x 4^3)")
    lab.row("valid in every arrangement", f"{len(boolean)}   by figure {by(boolean)}   (the film: 15 = 4+4+4+3)")
    lab.row("valid when S, M, P are inhabited", f"{len(trad)}   by figure {by(trad)}   (the film: 24)")
    lab.row("the nine that need an inhabited term", ", ".join(sorted(syl.NAMES[m] for m in extra)))
    lab.row("Darapti's countermodel", f"{len(darapti)} inhabited regions (the empty world)")
    lab.row("unrefuted by Leibniz's numbers (primes 2, 3, 5)", f"{len(leib)}   same set as the 24: {set(leib) == set(trad)}")
    lab.row(f"{trials} random assignments over five primes",
            f"traditional moods refuted {refuted_valid} times; other moods refuted: {len(refuted_invalid)} of {256 - len(trad)}")
    lab.note = ("Region models and Leibniz's arithmetic agree mood for mood: the numbers have existential import "
                "built in, so they give the tradition's 24 and not the modern 15.")

    assert len(moods) == 256 and len(boolean) == 15 and by(boolean) == [4, 4, 4, 3]
    assert len(trad) == 24 and by(trad) == [6, 6, 6, 6] and set(trad) == set(syl.NAMES)
    assert set(boolean) < set(trad) and len(extra) == 9
    assert darapti == frozenset(), "the empty world refutes Darapti"
    assert set(leib) == set(trad), "Leibniz's numbers pick out exactly the traditional moods"
    assert refuted_valid == 0, "no assignment of numbers refutes a traditional mood"
    assert len(refuted_invalid) > 200, "random numbers refute most of the invalid moods"

    fig, ax = labs.figure(2, size=(11, 4.2), gridspec_kw={"width_ratios": [1.9, 1]})
    kinds = ["".join(t) for t in __import__("itertools").product("AEIO", repeat=3)]
    grid = np.zeros((4, 64))
    for f, k in moods:
        grid[f - 1, kinds.index(k)] = 2 if (f, k) in boolean else 1 if (f, k) in trad else 0
    from matplotlib.colors import ListedColormap

    ax[0].imshow(grid, aspect="auto", cmap=ListedColormap([labs.PANEL, labs.BLUE, labs.GOLD]), vmin=0, vmax=2)
    ax[0].set_xticks(range(0, 64, 4), [kinds[i] for i in range(0, 64, 4)], rotation=90, fontsize=8)
    ax[0].set_yticks(range(4), ["figure 1", "figure 2", "figure 3", "figure 4"])
    ax[0].grid(False)
    ax[0].set(title="All 256 moods: gold valid, blue valid only with inhabited terms",
              xlabel="mood (major, minor, conclusion); every fourth one labelled")
    x = np.arange(1, 5)
    ax[1].bar(x, by(boolean), color=labs.GOLD, label="valid in every arrangement")
    ax[1].bar(x, by(extra), bottom=by(boolean), color=labs.BLUE, label="needs an inhabited term")
    ax[1].plot(x, by(leib), "o", color=labs.RED, ms=7, label="unrefuted by Leibniz's numbers")
    ax[1].set(title="Valid moods by figure", xlabel="figure", ylabel="moods", xticks=x, ylim=(0, 9))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
