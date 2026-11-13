"""Lab 20: test every small partial order against the axioms of mereology, and count objects on three answers."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import dl, mereo

TITLE = "Parthood, axiom by axiom"
GOAL = ("Enumerate every partial order on up to five elements, find which satisfy classical extensional mereology, "
        "check that removing any one element from a Boolean model breaks it, and count the objects among n blocks "
        "in a row on the nihilist, contact and universalist answers.")
TASKS = [
    "Raise the census to six elements (mereo.mereology_census(6), about eight seconds). Is there a model of size 6?",
    "Change the row of blocks to a 2 x 3 grid (mereo.composition_counts(2, 3)). Why does contact now give 40 "
    "rather than 21?",
    "Ask the tableau whether Grandmother is subsumed by Mother (dl.subsumes('Grandmother', 'Mother', dl.FAMILY)), "
    "then whether Mother is subsumed by Grandmother, and read the counter-model.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    rows = mereo.mereology_census(5)["rows"]
    counts = [r["posets"] for r in rows]
    sizes = [r["n"] for r in rows if r["cem"]]
    lab.row("partial orders on 1..5 elements", f"{counts}   (known: [1, 2, 5, 16, 63])")
    lab.row("sizes with a model of classical mereology", f"{sizes}   (theory: 2^k - 1, so 1 and 3)")
    assert counts == [1, 2, 5, 16, 63]
    assert sizes == [1, 3] and all(r["cem"] <= 1 for r in rows), "one model at 1 and at 3, none at 2, 4, 5"

    # the Boolean algebras without their zero are models; take one element away and they are not
    broken = []
    for k in (2, 3):
        full = mereo.boolean_minus_bottom(k)
        prof = full.profile()
        assert full.n == 2 ** k - 1 and prof["ssp"] and prof["uf"], "nonempty subsets of k atoms model CEM"
        for gone in rng.permutation(full.n)[:4]:
            keep = [i for i in range(full.n) if i != gone]
            sub = mereo.Poset(len(keep), [[full.le[i][j] for j in keep] for i in keep])
            p = sub.profile()
            broken.append((k, int(gone), p["ssp"], p["uf"]))
            assert not (p["ssp"] and p["uf"]), "a model cannot have 2^k - 2 elements"
    lab.row("Boolean models with one element removed", f"{len(broken)} tried, "
            f"{sum(not (s and u) for _, _, s, u in broken)} fail strong supplementation or fusion")

    ns = list(range(3, 10))  # a row of one or two blocks has no scattered group for the library to show
    line = [mereo.composition_counts(1, n) for n in ns]
    for n, c in zip(ns, line):
        assert c["contact"] == n * (n + 1) // 2, "connected groups of n blocks in a row are its intervals"
        assert c["nihilism"] == n and c["universalism"] == 2 ** n - 1
    six = mereo.composition_counts(2, 3)
    lab.row("six blocks, 2 x 3", f"nihilism {six['nihilism']}, contact {six['contact']}, "
            f"universalism {six['universalism']}   (film: 6, 40, 63)")
    assert (six["nihilism"], six["contact"], six["universalism"]) == (6, 40, 63)

    yes = dl.subsumes("Mother", "Parent", dl.FAMILY)
    no = dl.subsumes("Parent", "Mother", dl.FAMILY)
    lab.row("tableau: Mother within Parent", f"{yes['subsumed']} in {yes['steps']} rule applications")
    lab.row("tableau: Parent within Mother", f"{no['subsumed']}, counter-model {no['model']['nodes']}")
    assert yes["subsumed"] and not no["subsumed"] and no["model"] is not None
    lab.note = ("Classical mereology has finite models only at sizes 2^k - 1, the Boolean algebras without a zero; "
                "how many objects there are among n blocks depends entirely on the answer to the composition question.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(1, 6)
    for key, color, name, off in (("posets", labs.GREY, "all partial orders", -0.3),
                                  ("uf", labs.BLUE, "unrestricted fusion", -0.1),
                                  ("wsp", labs.GOLD, "weak supplementation", 0.1),
                                  ("cem", labs.GREEN, "classical mereology", 0.3)):
        ax[0].bar(x + off, [r[key] for r in rows], 0.2, color=color, label=name)
    ax[0].set(title="Partial orders that satisfy each axiom", xlabel="number of elements",
              ylabel="orders, up to isomorphism", yscale="log", ylim=(0.5, 400))
    ax[0].legend(loc="upper left")
    ax[1].plot(ns, [c["universalism"] for c in line], "o-", color=labs.PURPLE, label="universalism: 2^n - 1")
    ax[1].plot(ns, [c["contact"] for c in line], "o-", color=labs.GOLD, label="contact: n(n+1)/2")
    ax[1].plot(ns, [c["nihilism"] for c in line], "o-", color=labs.BLUE, label="nihilism: n")
    ax[1].set(title="Objects among n blocks in a row", xlabel="blocks n", ylabel="objects", yscale="log")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
