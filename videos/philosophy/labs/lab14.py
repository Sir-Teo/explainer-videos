"""Lab 14: check the AGM and Darwiche-Pearl postulates exhaustively for revision operators on random belief states."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import revision as R

TITLE = "Which revision operators keep the postulates?"
GOAL = ("Draw random belief states over three atoms and random rankings over two. Let the Reasoner check every "
        "pair of propositions: sphere and Dalal revision must satisfy all six AGM postulates, Satoh's must break "
        "subexpansion somewhere, and of four iterated operators only natural and lexicographic revision must keep "
        "all of DP1 to DP4.")
TASKS = [
    "Write an operator that returns all of A whenever A contradicts K (full meet revision) and find which "
    "postulates R.check_agm reports as broken.",
    "Raise Spohn conditionalization's strength from 1 to 5 in the iterated table. Which Darwiche-Pearl postulates "
    "recover, and why?",
    "Print R.check_agm's counterexample for Winslett's update from a two-world belief state, and explain why an "
    "update should break vacuity (K*4).",
]

AGM = [k for k, _, _ in R.POSTULATES]
DP = [k for k, _, _ in R.DP]


def run(seed=0):
    rng = np.random.default_rng(seed)
    atoms = ("p", "q", "r")
    W = R.worlds(atoms)
    lab = labs.Lab()

    names = ["spheres", "Dalal", "Satoh", "Winslett"]
    n1 = 16
    agm = np.zeros((4, len(AGM)))
    identities = 0
    for _ in range(n1):
        K = frozenset(rng.choice(W, int(rng.integers(1, 4)), replace=False))
        rank = {w: (0 if w in K else int(rng.integers(1, 4))) for w in W}
        ops = [lambda A, rank=rank: R.revise(rank, A), R.dalal(K, atoms)[0], R.satoh(K, atoms), R.winslett(K, atoms)]
        for i, op in enumerate(ops):
            res = R.check_agm(K, op, W)
            agm[i] += [res[k]["holds"] for k in AGM]
        ok = R.identities_hold(rank)
        identities += ok["levi"] and ok["harper"]
    assert (agm[0] == n1).all() and (agm[1] == n1).all(), "a ranking gives an AGM revision (Grove)"
    assert identities == n1, "Levi and Harper identities"
    k8 = AGM.index("K*8")
    assert agm[2, k8] < n1 and (np.delete(agm[2], k8) == n1).all(), "Satoh breaks only subexpansion"
    assert agm[3, k8] < n1, "Winslett's update is not a revision"

    names2 = ["natural", "lexicographic", "Spohn (1)", "amnesic"]
    ops2 = [R.natural, R.lexicographic, lambda r, A: R.spohn(r, A, 1), R.amnesic]
    n2 = 30
    dp = np.zeros((4, len(DP)))
    W2 = R.worlds(("p", "q"))
    for _ in range(n2):
        ranks = rng.integers(0, 4, 4)
        rank = {w: int(r - ranks.min()) for w, r in zip(W2, ranks)}
        for i, op in enumerate(ops2):
            res = R.check_dp(rank, op)
            dp[i] += [res[k]["holds"] for k in DP]
    assert (dp[0] == n2).all() and (dp[1] == n2).all(), "natural and lexicographic revision satisfy DP1-DP4"
    assert dp[3].min() < n2 / 2, "the amnesic operator forgets"
    g = R.gardenfors()
    assert g["survivors"] == [], "Gärdenfors: no candidate for H * (B v C) survives"

    lab.row("belief states tried (3 atoms, 255 x 255 pairs each)", f"{n1}")
    lab.row("spheres, Dalal: all six AGM postulates", f"{int(agm[0].min())} and {int(agm[1].min())} of {n1}   (theory: all)")
    lab.row("Levi and Harper identities hold", f"{identities} of {n1}   (theory: all)")
    lab.row("Satoh keeps subexpansion (K*8)", f"{int(agm[2, k8])} of {n1}   (theory: not always)")
    lab.row("Winslett keeps vacuity, subexpansion", f"{int(agm[3, AGM.index('K*4')])}, {int(agm[3, k8])} of {n1}")
    lab.row("rankings tried for iterated revision", f"{n2}")
    for i, name in enumerate(names2):
        lab.row(f"{name}: DP1, DP2, DP3, DP4 hold in", ", ".join(str(int(x)) for x in dp[i]) + f" of {n2}")
    lab.row("Gärdenfors: surviving candidates for H * (B v C)", f"{len(g['survivors'])}   (theory 0)")
    lab.note = ("Any ranking of worlds yields a revision that meets every AGM postulate; operators built another "
                "way can fail, and the AGM postulates alone do not stop an agent from forgetting everything but "
                "her newest belief.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    for a, table, n, rows, cols, title in ((ax[0], agm, n1, names, AGM, "AGM postulates: share of belief states"),
                                           (ax[1], dp, n2, names2, DP, "Darwiche-Pearl: share of rankings")):
        a.imshow(table / n, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        a.set_xticks(range(len(cols)), cols)
        a.set_yticks(range(len(rows)), rows)
        a.grid(False)
        for i in range(len(rows)):
            for j in range(len(cols)):
                a.text(j, i, f"{table[i, j] / n:.0%}", ha="center", va="center", color="#0E1117", fontsize=10,
                       fontweight="bold")
        a.set(title=title + " where it holds")
    lab.fig = fig
    return lab
