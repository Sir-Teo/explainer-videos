"""Lab 5: decide six inferences in five logics by their tables, test the K3/LP duality on random formulas, and run the sorites three ways."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import matrix as mx

TITLE = "Gaps, gluts, and the heap"
GOAL = ("Check explosion, excluded middle, non-contradiction, identity, modus ponens and disjunctive syllogism in "
        "classical logic, K3, LP, Ł3 and FDE; test the duality 'A entails B in K3 exactly when not-B entails not-A in "
        "LP' on random formulas; then run the sorites classically, by supervaluation and by degrees.")
TASKS = [
    "Add mx.G3 and mx.RM3 to the list of logics. Which of the six inferences does each keep, and what is the "
    "countermodel for the first one each loses?",
    "Change the degree theory's penumbra from men 30-70 to men 45-55. What happens to the lowest conditional and "
    "to the man at which the guarantee of modus ponens runs out?",
    "Use mx.lpm_consequence to test disjunctive syllogism from the premises 'p | q', '~p', and again after adding "
    "the premise 'p'. Where does the inference come back, and where does it stay lost?",
]

SIX = ["explosion", "LEM", "noncontradiction", "identity", "MP", "DS"]
SHOWN = {"explosion": "explosion: p, ¬p ⊨ q", "LEM": "excluded middle: ⊨ p ∨ ¬p", "noncontradiction": "⊨ ¬(p ∧ ¬p)",
         "identity": "identity: ⊨ p → p", "MP": "modus ponens: p, p → q ⊨ q", "DS": "p ∨ q, ¬p ⊨ q"}


def random_formula(rng, depth):
    """A random formula in p, q with negation, conjunction and disjunction, as a string for the Reasoner."""
    if depth == 0 or rng.random() < 0.25:
        return str(rng.choice(["p", "q"]))
    kind = rng.integers(3)
    if kind == 0:
        return f"~({random_formula(rng, depth - 1)})"
    return f"({random_formula(rng, depth - 1)}) {'&|'[kind - 1]} ({random_formula(rng, depth - 1)})"


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    logics = [mx.CL, mx.K3, mx.LP, mx.L3, mx.FDE]
    table = mx.compare({k: mx.INFERENCES[k] for k in SIX}, logics)
    grid = np.array([[table[k][M.name][0] for M in logics] for k in SIX])
    strength = grid.sum(axis=0).tolist()
    lab.row("inferences kept (of 6): CL, K3, LP, Ł3, FDE", f"{strength}   (the film: 6, 3, 3, 4, 0)")
    cm = table["explosion"]["LP"][1]
    lab.row("LP's countermodel to explosion", ", ".join(f"{k} = {v}" for k, v in sorted(cm.items())))
    assert strength == [6, 3, 3, 4, 0]
    assert not (grid[:, 1] & grid[:, 2]).any() and (grid[:, 1] | grid[:, 2]).all(), "K3 and LP keep opposite halves"
    assert cm == {"p": mx.H, "q": 0} and not mx.consequence(["p", "p -> q"], "q", mx.LP)[0]
    assert not mx.tautology("p | ~p", mx.K3)[0] and mx.tautology("p | ~p", mx.LP)[0]

    # The duality theorem on random pairs: A entails B in K3 iff not-B entails not-A in LP.
    pairs, agree, k3_valid = 150, 0, 0
    for _ in range(pairs):
        a, b = random_formula(rng, 3), random_formula(rng, 3)
        k3 = mx.consequence([a], b, mx.K3)[0]
        lp_dual = mx.consequence([f"~({b})"], f"~({a})", mx.LP)[0]
        agree += k3 == lp_dual
        k3_valid += k3
        if mx.consequence([a], b, mx.FDE)[0]:
            assert k3 and mx.consequence([a], b, mx.LP)[0], "what FDE validates, K3 and LP validate"
    lab.row(f"duality on {pairs} random pairs of formulas", f"agrees on {agree}   ({k3_valid} of the pairs are valid in K3)")
    assert agree == pairs and 5 < k3_valid < pairs - 5

    # The sorites.
    classical = mx.sorites_classical(30)
    sv = mx.supervaluation_report(20, 6, 13)
    deg = mx.degree_report(100, 30, 70)
    out_at = deg["mp_bound"].index(0.0)
    lab.row("31 men, classically", f"{classical['premises']} premises, consistent: {classical['consistent']}, "
                                   f"every premise needed: {classical['every_premise_needed']}")
    lab.row("21 men, 7 sharpenings: 'man i is bald'", "".join(sv["bald"]) + "   (T super-true, I neither, F super-false)")
    lab.row("'there is a last bald man'", f"super-true: {sv['cutoff'] == 'T'}; super-true of some particular man: {not sv['no_witness']}")
    lab.row("101 men by degrees: lowest tolerance conditional", f"{deg['min_conditional']:.3f}   (1 - 1/40 = {1 - 1 / 40:.3f})")
    lab.row("modus ponens guarantees nothing from man", f"{out_at}   (the film: 70)")
    assert not classical["consistent"] and classical["every_premise_needed"] and classical["premises"] == 32
    assert sv["sharpenings"] == 7 and sv["bald"].count("I") == 6 and sv["conditionals"].count("I") == 7
    assert sv["cutoff"] == "T" and sv["no_witness"] and set(sv["lem"]) == {"T"}
    assert abs(deg["min_conditional"] - 0.975) < 1e-12 and out_at == 70
    lab.note = ("K3 and LP share their tables and keep opposite halves of classical logic; the sorites is "
                "inconsistent classically, loses tolerance under supervaluation, and under degrees is an argument "
                "whose almost-true premises leak a little at every step.")

    fig, ax = labs.figure(2, size=(11, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
    from matplotlib.colors import ListedColormap

    ax[0].imshow(grid, cmap=ListedColormap([labs.PANEL, labs.GREEN]), aspect="auto", vmin=0, vmax=1)
    for i in range(6):
        for j in range(5):
            ax[0].text(j, i, "valid" if grid[i, j] else "fails", ha="center", va="center", fontsize=9,
                       color=labs.BG if grid[i, j] else labs.MUTED)
    ax[0].set_xticks(range(5), [M.name for M in logics])
    ax[0].set_yticks(range(6), [SHOWN[k] for k in SIX], fontsize=8.5)
    ax[0].grid(False)
    ax[0].set(title="Six inferences in five logics")
    men = np.arange(101)
    ax[1].plot(men, deg["degrees"], color=labs.BLUE, label="degree of 'man i is bald'")
    ax[1].plot(men[:-1], deg["conditionals"], color=labs.GOLD, label="degree of 'if man i is bald, so is man i + 1'")
    ax[1].plot(men, deg["mp_bound"], color=labs.RED, ls="--", label="what chained modus ponens still guarantees")
    ax[1].axvspan(30, 70, color=labs.GREY, alpha=0.12)
    ax[1].text(50, 0.5, "penumbra", ha="center", color=labs.MUTED, fontsize=9)
    ax[1].set(title="The heap by degrees (Łukasiewicz), 101 men", xlabel="man i", ylabel="degree of truth",
              ylim=(-0.04, 1.3), yticks=[0, 0.25, 0.5, 0.75, 1])
    ax[1].legend(loc="upper right", ncols=1)
    lab.fig = fig
    return lab
