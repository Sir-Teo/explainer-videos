"""Lab 9: search for proofs as programs, type-check them, and refute what has no program with a Kripke model."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import mathphil
from explainer.philosophy.reasoner import types as ty

TITLE = "Proofs as programs, and what Hume's principle demands"
GOAL = ("Run the Reasoner's proof search on the film's ten propositions and on random ones, check every program it "
        "finds with the type checker, and check that no proposition has both a program and a Kripke countermodel. "
        "Then count the objects that Hume's principle and Basic Law V need on a world of n objects.")
TASKS = [
    "Prove '(A -> B) -> ~B -> ~A' with ty.prove, print the program with ty.show_term, and read it as contraposition.",
    "Find a countermodel to '(A -> B) | (B -> A)' with ty.countermodel(max_worlds=3). Why does it need three worlds?",
    "Call mathphil.frege_numbers(5) and compare class_sizes with a row of Pascal's triangle (Problem 1).",
]


def size(term):
    """The number of nodes of a lambda term."""
    return 1 + sum(size(x) for x in term[1:] if isinstance(x, tuple) and x and x[0] in ty._OPS)


def random_type(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return ty.BOT if rng.random() < 0.15 else ("var", "AB"[int(rng.integers(2))])
    op = ("->", "->", "&", "|")[int(rng.integers(4))]
    return (op, random_type(rng, depth - 1), random_type(rng, depth - 1))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # the film's ten propositions
    found = []
    for text, name in ty.EXAMPLES:
        goal = ty.parse_type(text)
        term, model = ty.prove(goal), ty.countermodel(goal)
        assert (term is None) != (model is None), f"{name}: exactly one of a program and a countermodel"
        if term is not None:
            assert ty.type_of(term) == goal, f"{name}: the program has the wrong type"
        found.append((name, term, model))
    programs = [f for f in found if f[1] is not None]
    refuted = [f for f in found if f[2] is not None]
    assert len(programs) == 7 and [f[0] for f in refuted] == ["excluded middle", "Peirce's law", "double negation out"]
    assert all(f[2]["worlds"] == 2 for f in refuted), "each is refuted on the two-world model"
    k = ty.prove(ty.parse_type("A -> B -> A"))
    lab.row("the film's ten propositions", f"{len(programs)} programs, each type-checked; {len(refuted)} Kripke countermodels")
    lab.row("A -> B -> A", f"{ty.show_term(ty.rename(k))}   (Curry's K)")
    lab.row("A | ~A", f"no program; refuted at the root of {refuted[0][2]['worlds']} worlds, A true only later")

    # random propositions: soundness of the search against Kripke semantics
    counts = {"program": 0, "countermodel": 0, "neither found": 0}
    for _ in range(60):
        goal = random_type(rng, 3)
        term, model = ty.prove(goal), ty.countermodel(goal)
        assert term is None or model is None, f"{ty.show_type(goal)} has a program and a countermodel"
        if term is not None:
            assert ty.type_of(term) == goal
            counts["program"] += 1
        elif model is not None:
            counts["countermodel"] += 1
        else:
            counts["neither found"] += 1
    lab.row("60 random propositions", f"{counts['program']} with a program, {counts['countermodel']} with a countermodel, "
            f"{counts['neither found']} with neither found; never both")
    assert counts["program"] > 0 and counts["countermodel"] > 0

    # a proof with a detour, run to its normal form: every step keeps the type
    a, b = ("var", "A"), ("var", "B")
    swap = ("lam", "p", ("&", a, b), ("pair", ("snd", ("v", "p")), ("fst", ("v", "p"))))
    ctx = {"a": a, "b": b}
    seq = ty.normalize(("app", swap, ("pair", ("v", "a"), ("v", "b"))))
    assert all(ty.type_of(t, ctx) == ("&", b, a) for t in seq) and seq[-1] == ("pair", ("v", "b"), ("v", "a"))
    lab.row("swap applied to ⟨a, b⟩", f"normal form {ty.show_term(seq[-1])} after {len(seq) - 1} steps, type B ∧ A at every step")

    # Frege's numbers, and what abstraction principles demand
    frege = mathphil.frege_numbers(4)
    demands = mathphil.abstraction_demands(5)
    assert frege["class_sizes"] == [1, 4, 6, 4, 1] and frege["successor"] == [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert all(d["HP"] == d["n"] + 1 > d["n"] and d["BLV"] == 2 ** d["n"] > d["n"] for d in demands)
    assert mathphil.hp_model_on_naturals(7) == {"ok": True, "rule": "#F = 0 if F is infinite, else |F| + 1", "checked": 127}
    lab.row("16 concepts on four objects", f"fall into numbers of sizes {frege['class_sizes']}: five numbers, four objects")
    lab.note = ("Every program the search returns passes the type checker, and no proposition has both a program and "
                "a Kripke countermodel: excluded middle, Peirce's law and double negation elimination have "
                "countermodels and no program. Hume's principle always needs one object more than a finite world has.")

    fig, ax = labs.figure(2, size=(11, 4.6))
    names = [f[0] for f in found]
    vals = [size(f[1]) if f[1] is not None else 0 for f in found]
    y = np.arange(len(found))[::-1]
    ax[0].barh(y, vals, color=labs.GREEN, label="size of the program found (nodes)")
    ax[0].barh(y, [-f[2]["worlds"] if f[2] else 0 for f in found], color=labs.RED, label="worlds in the countermodel")
    ax[0].set_yticks(y, names, fontsize=9)
    ax[0].set_xticks(range(-2, max(vals) + 1, 2), [str(abs(v)) for v in range(-2, max(vals) + 1, 2)])
    ax[0].axvline(0, color=labs.MUTED, lw=1)
    ax[0].set_axisbelow(True)
    ax[0].set(title="Ten propositions: a program, or a countermodel")
    ax[0].legend(loc="lower right")
    n = [d["n"] for d in demands]
    ax[1].plot(n, n, color=labs.MUTED, ls="--", label="objects available: n")
    ax[1].plot(n, [d["HP"] for d in demands], "o-", color=labs.GOLD, label="Hume's principle needs n + 1")
    ax[1].plot(n, [d["BLV"] for d in demands], "o-", color=labs.RED, label="Basic Law V needs $2^n$")
    ax[1].plot(n, [d["NP"] for d in demands], "o-", color=labs.BLUE, label="nuisance principle needs 1")
    ax[1].set(title="Objects an abstraction principle demands", xlabel="objects in the world, n", yscale="log", xticks=n)
    ax[1].legend()
    lab.fig = fig
    return lab
