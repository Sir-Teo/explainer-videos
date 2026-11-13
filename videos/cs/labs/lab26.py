"""Lab 26: carry random 3-SAT formulas through two reductions, and watch satisfiability fall off near 4.27 clauses per variable."""

from videos.coursekit import labs

import random

import numpy as np

from explainer.cs.algo import complexity as X

TITLE = "Reductions that preserve the answer, and the 3-SAT threshold"
GOAL = ("Decide small random 3-SAT formulas three ways (a truth table, an independent set of size m in the reduced "
        "graph, a 3-colouring of Karp's gadget graph found by the series' CDCL solver) and check that all three "
        "agree; then measure how the fraction of satisfiable formulas and the solver's conflicts change with m / n.")
TASKS = [
    "Set N to 60 and TRIALS to 30. Does the drop from mostly satisfiable to mostly unsatisfiable get steeper, and where is the conflict peak?",
    "Add the subset-sum reduction: for each satisfiable formula check that X.subset_from_model picks numbers summing to the target of X.sat_to_subset_sum.",
    "Replace X.cdcl by X.dpll in the threshold experiment and plot nodes instead of conflicts. At which ratio does plain DPLL suffer most?",
]
N, TRIALS = 40, 20
RATIOS = (3.0, 3.5, 4.0, 4.25, 4.5, 5.0, 5.5, 6.0)


def truth_table(n, clauses):
    return any(all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in clauses) for a in range(1 << n))


def independent_set_of_size_m(clauses):
    """Search the reduced graph itself: one vertex from each clause triangle, no edge inside the chosen set."""
    verts, edges, _, m = X.sat_to_is(clauses)
    adj = {v: set() for v in verts}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    tri = [[v for v in verts if v[0] == j] for j in range(m)]

    blocked = dict.fromkeys(verts, 0)        # how many chosen vertices are adjacent to each vertex

    def go(left, chosen):
        if not left:
            return chosen
        free = {j: [v for v in tri[j] if not blocked[v]] for j in left}
        j = min(left, key=lambda k: len(free[k]))              # the triangle with the fewest usable vertices
        for v in free[j]:
            for u in adj[v]:
                blocked[u] += 1
            found = go(left - {j}, chosen + [v])
            for u in adj[v]:
                blocked[u] -= 1
            if found:
                return found
        return None
    S = go(frozenset(range(m)), [])
    assert S is None or (len(S) == m and X.is_independent(S, edges))
    return S is not None, len(verts), len(edges)


def run(seed=0):
    rng = random.Random(int(np.random.default_rng(seed).integers(2 ** 31)))
    lab = labs.Lab()

    # 1. three deciders, one answer
    n, sat, sizes = 5, 0, []
    for _ in range(30):
        clauses = X.random_ksat(n, rng.randint(18, 34), 3, rng)
        truth = truth_table(n, clauses)
        model, stats = X.cdcl(n, clauses)
        assert (stats["status"] == "sat") == truth and (model is None or X.check(model, clauses))
        has_is, nv, ne = independent_set_of_size_m(clauses)
        assert has_is == truth, "satisfiable iff an independent set of size m exists"
        V, E = X.sat_to_3col(n, clauses)
        nvar, cnf, var = X.coloring_cnf(V, E, 3)
        cmodel, cstats = X.cdcl(nvar, cnf)
        assert (cstats["status"] == "sat") == truth, "satisfiable iff the gadget graph is 3-colourable"
        if cmodel is not None:
            colour = X.decode_coloring(V, cmodel, var, 3)
            assert all(colour[u] != colour[v] for u, v in E)
            back = [False] + [colour[f"x{v}"] == colour["T"] for v in range(1, n + 1)]
            assert X.check(back, clauses), "the colouring maps back to a satisfying assignment"
        sat += truth
        sizes.append((len(clauses), nv, ne, len(V), len(E)))
    m, nv, ne, cv, ce = max(sizes)
    lab.row("30 random formulas on 5 variables", f"{sat} satisfiable, {30 - sat} not; three deciders agree on all 30")
    lab.row(f"largest: {m} clauses", f"independent-set graph {nv} vertices, {ne} edges; colouring graph {cv} vertices, {ce} edges")
    assert 3 <= sat <= 27, "the sample holds both kinds of formula"

    # 2. the threshold
    frac, med = [], []
    for r in RATIOS:
        conflicts, ok = [], 0
        for _ in range(TRIALS):
            model, stats = X.cdcl(N, X.random_ksat(N, round(r * N), 3, rng))
            assert stats["status"] != "unknown"
            ok += stats["status"] == "sat"
            conflicts.append(stats["conflicts"])
        frac.append(ok / TRIALS)
        med.append(float(np.median(conflicts)))
        lab.row(f"m / n = {r:<4}  (n = {N})", f"satisfiable {ok}/{TRIALS}   median conflicts {med[-1]:.0f}")
    assert frac[0] >= 0.9 and frac[-1] <= 0.15, "satisfiable well below the threshold, unsatisfiable well above"
    assert max(med[2:6]) > 3 * max(med[0], 1), "the hard formulas sit near the threshold, not at low density"
    lab.note = ("A reduction is checked by running it: the answer survives the trip to a graph and back. The drop "
                "near 4.27 at n = 40 is a finite-size picture of the threshold, not a proof of it.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    se = [np.sqrt(max(f * (1 - f), 1e-9) / TRIALS) for f in frac]
    ax[0].errorbar(RATIOS, frac, yerr=se, fmt="o-", color=labs.BLUE, capsize=3, label=f"n = {N}, {TRIALS} formulas per point")
    ax[0].axvline(4.267, color=labs.GOLD, ls="--", label="predicted threshold, about 4.27")
    ax[0].set(title="Fraction of random 3-SAT formulas that are satisfiable", xlabel="clauses per variable, m / n",
              ylabel="fraction satisfiable", ylim=(-0.05, 1.05))
    ax[0].legend(loc="upper right")
    ax[1].plot(RATIOS, med, "o-", color=labs.RED, label="median CDCL conflicts")
    ax[1].axvline(4.267, color=labs.GOLD, ls="--")
    ax[1].set(title="Work to decide them: easy, hard, easier", xlabel="clauses per variable, m / n", ylabel="conflicts")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
