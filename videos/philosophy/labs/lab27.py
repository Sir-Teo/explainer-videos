"""Lab 27: check determiners for conservativity, play the game that 'most' wins, and run the donkey sentence."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import semantics as sem

TITLE = "Quantifiers as relations between sets"
GOAL = ("Test seven candidate determiners for conservativity on every pair of subsets of a four-element universe, "
        "count the conservative relations on two elements by brute force, play Ehrenfeucht-Fraïssé games on "
        "structures that differ only in whether most things are P, and compare dynamic predicate logic with "
        "first-order translations of the donkey sentence.")
TASKS = [
    "Add 'not all' and 'fewer than half' to sem.GQ and rerun sem.quantifiers(4). Are they conservative, and what "
    "are their monotonicity profiles?",
    "Add 'an even number of' (len(A & B) % 2 == 0) and find, with sem.ef_duplicator_wins, two structures that "
    "disagree on it but that Duplicator can defend for k rounds.",
    "Lower the chance of a 'beats' pair in sem._random_model from 0.35 to 0.05 and rerun sem.donkeys. Why does the "
    "naive translation now agree more often?",
]


def _rank(m1, m2):
    """The fewest rounds in which Spoiler tells m1 from m2: theory says a colour with n1 != n2 elements is exposed
    in min(n1, n2) + 1 rounds."""
    return min((min(a, b) + 1 for a, b in zip(m1, m2) if a != b), default=None)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. conservativity: Q(A, B) iff Q(A, A & B)
    q = sem.quantifiers(4)
    S = sem._subsets(range(4))
    breaks = {name: sum(Q(A, B) != Q(A, A & B) for A in S for B in S) for name, Q in sem.GQ.items()}
    passed = [n for n, r in q["rows"].items() if r["conservative"]]
    lab.row(f"conservative on all {q['pairs']} pairs", ", ".join(passed))
    lab.row("'only': pairs where Q(A, B) differs from Q(A, A & B)", f"{breaks['only']} of {q['pairs']}")
    assert set(passed) == set(sem.GQ) - {"only"} and breaks["only"] > 0
    assert all((breaks[n] == 0) == q["rows"][n]["conservative"] for n in sem.GQ), "the count agrees with the library"
    every, most = q["rows"]["every"], q["rows"]["most"]
    assert every["left_down"] and every["right_up"] and not every["left_up"]
    assert most["right_up"] and not most["left_up"] and not most["left_down"], "'most' is monotone in the verb only"
    cc = sem.count_conservative(2)
    lab.row("conservative relations on 2 elements", f"{cc['conservative']} of {cc['all']}   (theory 2^(3^2) = {cc['formula']})")
    assert cc["conservative"] == cc["formula"] == 512

    # 2. Ehrenfeucht-Fraisse games: Duplicator survives k rounds iff every colour has equal counts or both >= k
    checked = 0
    for _ in range(150):
        m1, m2 = tuple(rng.integers(0, 6, 2)), tuple(rng.integers(0, 6, 2))
        k = int(rng.integers(1, 6))
        r = _rank(m1, m2)
        assert sem.ef_duplicator_wins(m1, m2, k) == (r is None or k < r), (m1, m2, k)
        checked += 1
    lab.row("random games against the counting criterion", f"{checked} of {checked} agree")
    ks = list(range(1, 7))
    grid = np.array([[sem.ef_duplicator_wins((m + 1, m), (m, m + 1), k) for k in ks] for m in ks])
    for m in ks:
        assert all(grid[m - 1, k - 1] == (k <= m) for k in ks), "Duplicator wins exactly the games of at most m rounds"
    lab.row("(m+1 P, m others) against (m P, m+1 others)", "Duplicator wins k rounds iff k <= m, for m = 1..6")

    # 3. donkey sentences
    d = sem.donkeys(trials=400, seed=seed)
    lab.row("DPL donkey sentence = 'for all x, y' translation", f"{d['dpl_vs_fo']} of {d['trials']} random models")
    lab.row("DPL = static reading with y left free", f"{d['dpl_vs_naive']} of {d['trials']}")
    lab.row("DPL discourse = 'exists x, y' translation", f"{d['discourse']} of {d['trials']}")
    assert d["dpl_vs_fo"] == d["trials"] == d["discourse"] and d["dpl_vs_naive"] < 0.95 * d["trials"]
    lab.note = ("Every determiner tested looks only at the noun's set, 'only' does not; 'most' separates structures "
                "that no first-order sentence of bounded depth can; and a dynamic existential binds the pronoun "
                "that a static one leaves free.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = list(sem.GQ)
    ax[0].barh(names[::-1], [breaks[n] for n in names[::-1]],
               color=[labs.RED if breaks[n] else labs.GREEN for n in names[::-1]])
    for i, n in enumerate(names[::-1]):
        ax[0].text(breaks[n] + 2, i, str(breaks[n]), va="center", color=labs.INK)
    ax[0].set_axisbelow(True)
    ax[0].set(title="Pairs (A, B) that break conservativity, of 256", xlabel="pairs where Q(A, B) differs from Q(A, A and B)",
              xlim=(0, max(breaks.values()) * 1.15))
    ax[0].grid(False, axis="y")
    ax[1].imshow(grid, origin="lower", cmap="RdYlGn", vmin=-0.4, vmax=1.4, extent=(0.5, 6.5, 0.5, 6.5), aspect="auto")
    for m in ks:
        for k in ks:
            ax[1].text(k, m, "D" if grid[m - 1, k - 1] else "S", ha="center", va="center", color=labs.BG,
                       fontweight="bold")
    ax[1].set(title="Who wins: Duplicator (D) or Spoiler (S)", xlabel="rounds k (quantifier depth)",
              ylabel="m: (m+1 P, m others) vs (m P, m+1 others)")
    ax[1].grid(False)
    lab.fig = fig
    return lab
