"""Lab 3: count the structures where 'everyone loves someone' and 'someone is loved by everyone' hold, and let a tableau find the countermodel."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import fol

TITLE = "The order of quantifiers, counted"
GOAL = ("Evaluate 'for all x there is y with L(x, y)' and 'there is y such that for all x, L(x, y)' on every relation "
        "over 1, 2 and 3 people and on random relations over more, compare the counts with their closed forms, and "
        "let the tableau prover close one direction and return a countermodel for the other.")
TASKS = [
    "Add the sentence 'forall x L(x, x)' as a premise. Does 'forall x exists y L(x, y)' now entail 'exists y forall x "
    "L(x, y)'? Ask fol.countermodel.",
    "Count the relations on 3 people that are symmetric and satisfy 'forall x exists y L(x, y)'. Find the closed "
    "form before you run it.",
    "Give fol.prove De Morgan's argument with the premise changed to 'exists x (H(x) & A(x))'. Read the countermodel "
    "it returns.",
]

AE = "forall x exists y L(x, y)"   # everyone loves someone
EA = "exists y forall x L(x, y)"   # someone is loved by everyone
HORSES = (["forall x (H(x) -> A(x))"],
          "forall x ((exists y (Hd(x, y) & H(y))) -> exists y (Hd(x, y) & A(y)))")


def at_least(n):
    xs = [f"x{i}" for i in range(1, n + 1)]
    diff = " & ".join(f"~{a} = {b}" for i, a in enumerate(xs) for b in xs[i + 1:]) or "x1 = x1"
    return "".join(f"exists {x} " for x in xs) + f"({diff})"


def run(seed=0):
    rng = np.random.default_rng(seed)
    ae, ea = fol.parse(AE), fol.parse(EA)
    sig = fol.signature([ae])
    lab = labs.Lab()

    # Exhaustive: every relation on n people.  Closed forms: (2^n - 1)^n and 2^(n^2) - (2^n - 1)^n.
    exact = {}
    for n in (1, 2, 3):
        a = e = total = 0
        for M in fol.all_structures(sig, n):
            x, y = fol.holds(ae, M), fol.holds(ea, M)
            assert x or not y, "exists-forall entails forall-exists on every structure"
            a, e, total = a + x, e + y, total + 1
        exact[n] = (a, e, total)
        assert total == 2 ** (n * n) and a == (2 ** n - 1) ** n and e == total - (2 ** n - 1) ** n
    a3, e3, t3 = exact[3]
    lab.row("relations on 3 people", f"{t3}")
    lab.row("everyone loves someone", f"{a3}   (closed form 7^3 = {7 ** 3})")
    lab.row("someone is loved by everyone", f"{e3}   (closed form 512 - 7^3 = {512 - 7 ** 3})")

    # Monte Carlo on larger domains: a uniformly random relation on n people.
    reps, mc = 3000, {}
    for n in (4, 5, 6):
        a = e = 0
        for _ in range(reps):
            bits = rng.random((n, n)) < 0.5
            M = fol.Structure(range(n), {"L": {(i, j) for i in range(n) for j in range(n) if bits[i, j]}})
            x, y = fol.holds(ae, M), fol.holds(ea, M)
            assert x or not y
            a, e = a + x, e + y
        pa, pe = (1 - 2.0 ** -n) ** n, 1 - (1 - 2.0 ** -n) ** n
        mc[n] = (a / reps, e / reps, pa, pe)
        assert abs(a / reps - pa) < 0.035 and abs(e / reps - pe) < 0.035, "the sample agrees with the closed form"
    lab.row("6 people, random relation: P(everyone loves someone)", f"{mc[6][0]:.3f}   (exact {mc[6][2]:.3f})")
    lab.row("6 people, random relation: P(someone loved by all)", f"{mc[6][1]:.3f}   (exact {mc[6][3]:.3f})")

    # The tableau: one direction closes, the other grows without closing; the model finder gives the countermodel.
    forward, back = fol.prove([ea], ae), fol.prove([ae], ea)
    cm = fol.countermodel([ae], ea)
    horses = fol.prove([fol.parse(HORSES[0][0])], fol.parse(HORSES[1]))
    lab.row("tableau: exists-forall to forall-exists", f"closed in {len(forward.steps)} steps")
    lab.row("tableau: forall-exists to exists-forall", f"not closed; countermodel on {len(cm.domain)} people: L = {sorted(cm.preds['L'])}")
    lab.row("De Morgan's horse heads", f"closed: {len(horses.steps)} steps, {horses.branches} branches   (the film: 29 and 9)")
    assert forward.closed and not back.closed
    assert len(cm.domain) == 2 and fol.holds(ae, cm) and not fol.holds(ea, cm), "a two-person countermodel"
    assert horses.closed and len(horses.steps) == 29 and horses.branches == 9

    # The ladder behind compactness: 'at least n things' holds at size k exactly when k >= n.
    ladder = np.array([[fol.holds(fol.parse(at_least(n)), fol.Structure(range(k), {})) for k in range(1, 7)]
                       for n in range(1, 6)])
    assert all(ladder[n - 1, k - 1] == (k >= n) for n in range(1, 6) for k in range(1, 7))
    lab.note = ("Swapping the quantifiers changes the count on every domain: one sentence entails the other and "
                "never the reverse, and the tableau turns the failed proof into a two-person countermodel.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ns = np.arange(1, 9)
    ax[0].plot(ns, (1 - 2.0 ** -ns) ** ns, color=labs.BLUE, label=r"$\forall x\,\exists y\,L$: $(1-2^{-n})^n$")
    ax[0].plot(ns, 1 - (1 - 2.0 ** -ns) ** ns, color=labs.GOLD, label=r"$\exists y\,\forall x\,L$: $1-(1-2^{-n})^n$")
    ax[0].plot([1, 2, 3], [exact[n][0] / exact[n][2] for n in (1, 2, 3)], "o", color=labs.BLUE, label="every relation counted")
    ax[0].plot([1, 2, 3], [exact[n][1] / exact[n][2] for n in (1, 2, 3)], "o", color=labs.GOLD)
    ax[0].plot([4, 5, 6], [mc[n][0] for n in (4, 5, 6)], "s", mfc="none", color=labs.BLUE, label=f"{reps} random relations")
    ax[0].plot([4, 5, 6], [mc[n][1] for n in (4, 5, 6)], "s", mfc="none", color=labs.GOLD)
    ax[0].set(title="Share of relations on n people where each sentence holds", xlabel="people n",
              ylabel="share of relations", ylim=(-0.03, 1.03))
    ax[0].legend(loc="center right")
    from matplotlib.colors import ListedColormap

    ax[1].imshow(ladder, cmap=ListedColormap([labs.PANEL, labs.GREEN]), origin="lower", extent=(0.5, 6.5, 0.5, 5.5),
                 aspect="auto")
    for n in range(1, 6):
        for k in range(1, 7):
            ax[1].text(k, n, "true" if ladder[n - 1, k - 1] else "false", ha="center", va="center", fontsize=9,
                       color=labs.BG if ladder[n - 1, k - 1] else labs.MUTED)
    ax[1].grid(False)
    ax[1].set(title="'There are at least n things' on a domain of k things", xlabel="domain size k",
              ylabel="n", xticks=range(1, 7), yticks=range(1, 6))
    lab.fig = fig
    return lab
