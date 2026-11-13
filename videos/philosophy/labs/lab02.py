"""Lab 2: run Socrates' elenchus as a search for minimal correction sets, and race DPLL against CDCL."""

import random

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import prop

TITLE = "The Price List engine and two SAT solvers"
GOAL = ("Feed the seven claims of Republic I to the Reasoner, list every minimal inconsistent set and every minimal "
        "way out, and check Reiter's duality between them. Then solve random 3-SAT formulas by DPLL and by CDCL, "
        "check both against the truth table, and count their decisions.")
TASKS = [
    "Add an eighth claim that Polemarchus might accept (for example 'j2 -> j') and rerun mus_mcs. How many minimal "
    "inconsistent sets and how many exits are there now?",
    "Change the ratio 4.26 to 3.0 and then to 6.0. What happens to the share of satisfiable formulas and to the "
    "number of decisions each solver needs?",
    "Push the pigeonhole formulas to n = 6 and 7 holes and compare CDCL's conflicts with prop.dpll's on the same "
    "formulas.",
]

REPUBLIC = {  # Republic I, as in the film's Chapter 14
    "D1": "o -> j",      # justice is giving back what is owed
    "o": "o",            # returning a mad friend's weapon is giving back what is owed
    "nj": "~j",          # returning it is not just
    "D2": "h -> j2",     # justice is helping friends and harming enemies
    "h": "h",            # the just will sometimes harm an enemy
    "H": "h -> w",       # harming a person makes them less just
    "N": "j2 -> ~w",     # it is not the work of justice to make anyone less just
}


def brute_force(clauses, n):
    """Is some row of the truth table a model?  (numpy over all 2^n rows)"""
    rows = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(bool)  # rows[r, v-1]: the value of atom v
    ok = np.ones(2 ** n, bool)
    for c in clauses:
        sat = np.zeros(2 ** n, bool)
        for lit in c:
            sat |= rows[:, abs(lit) - 1] == (lit > 0)
        ok &= sat
    return bool(ok.any())


def run(seed=0):
    lab = labs.Lab()
    r = prop.mus_mcs({k: prop.parse(f) for k, f in REPUBLIC.items()})
    hitting = {tuple(sorted(h)) for h in prop.hitting_sets(r["mus"])}
    lab.row("Republic I: subsets of the 7 claims checked", f"{2 ** len(REPUBLIC)}")
    lab.row("minimal inconsistent sets", f"{len(r['mus'])}:  " + "  ".join("{" + ", ".join(m) + "}" for m in r["mus"]))
    lab.row("minimal correction sets (the exits)", f"{len(r['mcs'])}   (3 x 4: one claim from each contradiction)")
    lab.row("exits = minimal hitting sets of the contradictions", f"{hitting == {tuple(sorted(m)) for m in r['mcs']}}")
    assert not r["consistent"] and len(r["mus"]) == 2 and sorted(map(len, r["mus"])) == [3, 4]
    assert len(r["mcs"]) == 12 and all(len(m) == 2 for m in r["mcs"])
    assert hitting == {tuple(sorted(m)) for m in r["mcs"]}, "Reiter's duality"
    assert ("D1", "D2") in r["mcs"], "Socrates' own exit: give up both definitions"

    # Random 3-SAT at 4.26 clauses per atom: DPLL and CDCL against the truth table (small n), then their work.
    sizes, per = (10, 14, 20, 30, 40), 9
    dpll_med, cdcl_med, agree, checked, sat_share = [], [], 0, 0, []
    dd_all, cc_all = [], []
    for n in sizes:
        dd, cc, sat = [], [], 0
        for k in range(per):
            cl = prop.random_ksat(n, round(4.26 * n), 3, random.Random(10_000 * seed + 100 * n + k))
            m1, s1 = prop.dpll(cl, n)
            m2, s2 = prop.cdcl(cl, n)
            assert (m1 is None) == (m2 is None), "the two solvers agree"
            for m in (m1, m2):  # a model, when returned, satisfies every clause
                assert m is None or all(any(m[abs(x)] == (x > 0) for x in c) for c in cl)
            if n <= 14:
                checked += 1
                agree += brute_force(cl, n) == (m1 is not None)
            sat += m1 is not None
            dd.append(s1["decisions"])
            cc.append(s2["decisions"])
        dpll_med.append(float(np.median(dd)))
        cdcl_med.append(float(np.median(cc)))
        dd_all.append(dd)
        cc_all.append(cc)
        sat_share.append(sat / per)
    lab.row("solvers agree with the truth table (n = 10, 14)", f"{agree} of {checked} formulas")
    lab.row("median decisions at n = 40", f"DPLL {dpll_med[-1]:.0f}   CDCL {cdcl_med[-1]:.0f}   (truth table: 2^40 rows)")
    assert agree == checked
    assert cdcl_med[-1] < dpll_med[-1], "learning pays on the larger formulas"
    assert dpll_med[-1] < 2 ** 20, "far fewer steps than rows"

    # The pigeonhole principle: obviously false, expensive to refute.
    holes, conflicts = [1, 2, 3, 4, 5], []
    for n in holes:
        cl, nv = prop.pigeonhole(n)
        model, st = prop.cdcl(cl, nv)
        assert model is None, "n + 1 pigeons do not fit in n holes"
        conflicts.append(st["conflicts"])
    growth = conflicts[-1] / conflicts[-2]
    lab.row("CDCL conflicts on PHP(n+1, n), n = 1 ... 5", "  ".join(str(c) for c in conflicts))
    lab.row("growth per added hole (last step)", f"x {growth:.1f}")
    assert all(b > a for a, b in zip(conflicts, conflicts[1:])) and growth > 2, "conflicts grow geometrically"
    lab.note = ("The machine finds every exit from Socrates' two contradictions and nothing else; the same search, "
                "scaled up, is a SAT solver, and the pigeonhole formulas show what it costs.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.array(sizes)
    for xs, ys, color in ((x - 0.6, dd_all, labs.BLUE), (x + 0.6, cc_all, labs.GOLD)):
        for xi, y in zip(xs, ys):
            ax[0].scatter(np.full(len(y), xi), np.maximum(y, 1), s=10, color=color, alpha=0.45)
    ax[0].plot(x, np.maximum(dpll_med, 1), "o-", color=labs.BLUE, label="DPLL (median)")
    ax[0].plot(x, np.maximum(cdcl_med, 1), "o-", color=labs.GOLD, label="CDCL (median)")
    ax[0].set(title="Random 3-SAT at 4.26 clauses per atom", xlabel="atoms n", ylabel="decisions", yscale="log",
              xticks=sizes)
    ax[0].legend(loc="upper left")
    ax[1].plot(holes, np.maximum(conflicts, 1), "o-", color=labs.RED, label="CDCL conflicts")
    ax[1].plot(holes, [2.0 ** ((n + 1) * n) for n in holes], "--", color=labs.MUTED, label="truth-table rows $2^{n(n+1)}$")
    ax[1].set(title="Pigeonhole formulas: n + 1 pigeons, n holes", xlabel="holes n", yscale="log", ylim=(0.5, 1e9),
              xticks=holes)
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
