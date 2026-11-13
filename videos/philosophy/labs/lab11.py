"""Lab 11: score seven beliefs for sensitivity and safety, and strip margins off knowledge on the unmarked clock."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import knowledge as kn

TITLE = "Sensitivity, safety and margins for error"
GOAL = ("Run Nozick's and Sosa's conditions on the film's cases and find where they part; then check on the "
        "unmarked clock, and on random margin models, that each further 'I know that' strips one margin, so that "
        "knowing does not bring knowing that you know.")
TASKS = [
    "In kn.safe, change radius from 2 to 9 for the vat model. Which verdict flips, and what is the skeptic claiming?",
    "Call kn.luminosity_series(n=100, margin=0.02). How many moments are cold but not knowably cold?",
    "Use kn.iterate_k with margin=0. Which principle now holds, and what would such a knower be like?",
]
CASES = [("coins", "p", "Gettier's coins"), ("clock", "eight", "Russell's stopped clock"), ("barns", "barn", "Barn County"),
         ("lottery", "lose", "the lottery ticket"), ("chute", "basement", "the garbage chute"),
         ("biv", "not_biv", "not a brain in a vat"), ("biv", "hands", "I have hands")]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # the scorecard
    card = []
    for model, prop, name in CASES:
        v = kn.verdicts(kn.SCENARIOS[model], [prop])[0]
        assert v["true"] and v["believed"], name
        card.append((name, v["sensitive"], v["safe"]))
    table = {name: (s, f) for name, s, f in card}
    for name in ("Gettier's coins", "Russell's stopped clock", "Barn County", "the lottery ticket"):
        assert table[name] == (False, False), f"{name}: a true belief that is neither sensitive nor safe"
    assert table["the garbage chute"] == (False, True) and table["not a brain in a vat"] == (False, True)
    assert table["I have hands"] == (True, True)
    apart = [name for name, s, f in card if s != f]
    lab.row("seven true beliefs", f"{sum(s for _, s, _ in card)} sensitive, {sum(f for _, _, f in card)} safe")
    lab.row("sensitivity and safety disagree on", "; ".join(apart))

    # Zagzebski's recipe
    z = kn.zagzebski()
    assert not z["step1"]["true"] and z["step2"] == {"believes": True, "justified": True, "reliable": True, "true": True}
    assert not z["safe"]
    lab.row("Zagzebski's doctor after step two", f"believed, justified, {z['reliability']:.0%} reliable, true; safe: {z['safe']}")

    # the unmarked clock: p, Kp, KKp, KKKp
    levels = kn.iterate_k(range(31), lambda w: w <= 20, margin=1, depth=3)
    edges = [max(s) for s in levels]
    assert edges == [20, 19, 18, 17]
    assert 19 in levels[1] and 19 not in levels[2], "at 19 the hand's position is known, but not known to be known"
    lab.row("unmarked clock, p = 'at most 20'", f"p, Kp, KKp, KKKp end at marks {edges}")

    # random margin models: the edge after n iterations is c - n m, against the definition by brute force
    for _ in range(20):
        size, m = int(rng.integers(30, 60)), int(rng.integers(1, 4))
        c = int(rng.integers(15, size - 5))
        got = kn.iterate_k(range(size), lambda w, c=c: w <= c, margin=m, depth=4)
        for n, s in enumerate(got):
            brute = {w for w in range(size) if all(v <= c for v in range(size) if abs(v - w) <= n * m)}
            assert s == brute and max(s) == c - n * m, (size, m, c, n)
    lab.row("20 random margin models", "after n iterations the edge is c − n·m in every one; KK fails at the edge")

    # anti-luminosity on a cold morning
    lum = kn.luminosity_series()
    assert lum["gap"] == [10, 11] and lum["first_warm"] == 12 == lum["chain_breaks_at"]
    n, margin = int(rng.integers(30, 200)), float(rng.uniform(0.02, 0.2))
    other = kn.luminosity_series(n=n, margin=margin)
    assert other["gap"] and all(other["cold"][t] and not other["known"][t] for t in other["gap"])
    lab.row("cold morning, 25 moments", f"cold but not knowably cold at moments {lum['gap']}")
    lab.row(f"a morning of {n + 1} moments, margin {margin:.2f}", f"{len(other['gap'])} such moments: luminosity fails again")
    lab.note = ("Sensitivity and safety agree that Gettier's beliefs are not knowledge and part on the chute and the "
                "vat. With any margin for error, knowledge stops one margin short of the truth, and each further "
                "'I know that' stops one margin shorter.")

    from matplotlib.colors import ListedColormap
    fig, ax = labs.figure(2, size=(11, 4.4))
    grid = np.array([[1, s, f] for _, s, f in card], dtype=float)
    ax[0].imshow(grid, cmap=ListedColormap([labs.RED, labs.GREEN]), vmin=0, vmax=1, aspect="auto")
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            ax[0].text(j, i, "yes" if v else "no", ha="center", va="center", color=labs.BG, fontweight="bold")
    ax[0].set_xticks(range(3), ["true", "sensitive", "safe"])
    ax[0].set_yticks(range(len(card)), [name for name, _, _ in card])
    ax[0].set(title="The scorecard: seven true beliefs")
    ax[0].grid(False)
    names = ["p", "Kp", "KKp", "KKKp"]
    for i, s in enumerate(levels):
        ax[1].barh(len(levels) - 1 - i, max(s) + 1, left=-0.5, color=labs.CYCLE[i], height=0.6)
        ax[1].text(21.5, len(levels) - 1 - i, f"ends at mark {max(s)}", va="center", color=labs.INK, fontsize=9)
    ax[1].axvline(19, color=labs.INK, ls="--", lw=1.2, label="the hand, at mark 19")
    ax[1].set_yticks(range(len(levels)), names[::-1])
    ax[1].set(title="The unmarked clock (margin: one mark)", xlabel="mark the hand points at", xlim=(-0.5, 30.5))
    ax[1].set_axisbelow(True)
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
