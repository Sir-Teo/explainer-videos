"""Lab 37: test Hume's law on random inferences in a logic of ought, and move a reflective equilibrium."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import metaethics as me

TITLE = "No ought from is, checked on every small model"
GOAL = ("Rerun the film's eight inferences in the deontic logic KD, then draw random inferences from a satisfiable "
        "is-only premise to a conclusion of the form O(...) or P(...) and check that each valid one is a logical "
        "truth. Then find the reflective equilibrium of the six trolley commitments as one weight is raised.")
TASKS = [
    "Allow a normative premise: add Cond(p, Ought(q)) to the premises of each random inference. How many "
    "conclusions now follow without being logical truths?",
    "Analyse p |- p and O(q or not q) with me.analyse. It is valid and not a theorem: is its ought idle in the "
    "module's sense, and what does Schurz's theorem replace instead?",
    "Give the principle D ('never kill an innocent') weight 9 in me.reflective_equilibrium. Which commitments "
    "survive, and at which weight does the answer change?",
]


def _formula(rng, depth):
    """A random propositional formula over p and q."""
    if depth == 0 or rng.random() < 0.25:
        return me.At("pq"[rng.integers(2)])
    kind = rng.integers(4)
    if kind == 0:
        return me.Neg(_formula(rng, depth - 1))
    return (me.Conj, me.Disj, me.Cond)[kind - 1](_formula(rng, depth - 1), _formula(rng, depth - 1))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    table = me.schurz_table()
    rows = {r["name"].split(":")[0]: r for r in table["rows"]}
    tea = rows["Prior's tea"]
    lab.row("models checked per inference", f"{table['models_checked']:,}   (film: 175,616)")
    lab.row("Prior's tea, p so p or Oq", f"valid {tea['valid']}, a logical truth {tea['theorem']}, ought idle {tea['idle']}")
    assert table["models_checked"] == 175616 and table["hume_pattern_holds"]
    assert tea["valid"] and tea["idle"] and not tea["theorem"], "Prior's ought does no work"
    assert not rows["is from ought"]["valid"] and rows["ought implies may"]["valid"]
    bad = me.analyse([me.At("p")], me.Ought(me.At("p")))
    assert not bad["valid"] and bad["countermodel"]["facts"]["p"], "p holds here"
    assert not all(f["p"] for f in bad["countermodel"]["ideal_facts"]), "... but not in every ideal world"

    # the special Hume thesis: a satisfiable is-only premise entails O(phi) or P(phi) only if that is a theorem
    counts = {"valid": 0, "invalid": 0, "skipped": 0}
    for _ in range(24):
        premise, body = _formula(rng, 2), _formula(rng, 2)
        concl = (me.Ought, me.May)[rng.integers(2)](body)
        if me.analyse([premise], me.BOT)["valid"]:  # an unsatisfiable premise entails everything
            counts["skipped"] += 1
            continue
        r = me.analyse([premise], concl)
        assert r["descriptive"] and r["normative_conclusion"]
        if r["valid"]:
            counts["valid"] += 1
            assert r["theorem"], f"{r['premises']} entails {r['conclusion']}, which is no theorem"
        else:
            counts["invalid"] += 1
            assert r["countermodel"] is not None
    lab.row("random is-to-ought inferences", f"{counts['invalid']} invalid (each with a countermodel), "
            f"{counts['valid']} valid, {counts['skipped']} skipped")
    lab.row("valid ones whose conclusion is a logical truth", f"{counts['valid']} of {counts['valid']}   (theory: all)")
    assert counts["invalid"] >= 5, "most random inferences should fail"

    pairs = me.norm_world_pairs()
    lab.row("Gibbard's pairs left by the two premises", f"{pairs['n_left']} of {pairs['n_pairs']}, all in the conclusion: {pairs['valid']}")
    assert pairs["n_pairs"] == 8 and pairs["n_left"] == 2 and pairs["valid"]

    ex = me.re_experiments()
    total = sum(c[3] for c in ex["commitments"])
    lab.row("reflective equilibrium, the film's weights", f"keep {', '.join(ex['base']['keep'])}: weight "
            f"{ex['base']['weight']} of {total}   (film: 16 of 22)")
    lab.row("after Greene's reweighting", f"keep {', '.join(ex['greene']['keep'])}: weight {ex['greene']['weight']}   (film: 10)")
    assert (ex["base"]["keep"], ex["base"]["weight"], total) == (["DDE", "S", "F", "H"], 16, 22)
    assert (ex["greene"]["keep"], ex["greene"]["weight"]) == (["U", "S"], 10) and len(ex["base"]["conflicts"]) == 6

    # the three maximal consistent sets, by hand, against the solver, as the weight of U rises
    w0 = {k: w for k, _, _, w in me.RE_COMMITMENTS}
    us = np.arange(0, 17)
    by_hand = {"welfare: U, S": us + w0["S"], "never kill: D, F, H": np.full(len(us), w0["D"] + w0["F"] + w0["H"]),
               "double effect: DDE, S, F, H": np.full(len(us), w0["DDE"] + w0["S"] + w0["F"] + w0["H"])}
    solver = np.array([me.reflective_equilibrium({"U": int(u)})["weight"] for u in us])
    assert np.array_equal(solver, np.max(list(by_hand.values()), axis=0)), "MaxSAT is the upper envelope"
    flip = int(us[np.argmax(by_hand["welfare: U, S"] > by_hand["double effect: DDE, S, F, H"])])
    lab.row("least whole weight of U at which welfare takes over", f"{flip}   (by hand: the first above 16 - 4 = 12)")
    assert flip == 13 and me.reflective_equilibrium({"U": 13})["keep"] == ["U", "S"]
    lab.note = ("An is-only premise never forces a working ought: the valid cases are logical truths. Which "
                "principles a reflective equilibrium keeps is the upper envelope of a few consistent sets, so it "
                "is settled by the weights, which the method does not supply.")

    deb = me.debunking(seed=2006 + seed)
    fig, ax = labs.figure(2, size=(11.5, 4.3))
    for name, color in zip(by_hand, (labs.BLUE, labs.RED, labs.GREEN)):
        ax[0].plot(us, by_hand[name], color=color, label=name)
    ax[0].plot(us, solver, "o", color=labs.GOLD, ms=5, label="the solver's equilibrium")
    ax[0].set(title="Reflective equilibrium as the weight of welfare rises", xlabel="weight given to U, maximize welfare",
              ylabel="total weight kept")
    ax[0].legend()
    f, a = np.array(deb["fitness"]), np.array(deb["approval"])
    ax[1].scatter(f, a, s=10, color=labs.BLUE, label=f"against fitness: r = {deb['corr_fitness']:+.2f}")
    ax[1].scatter(deb["t_indep"], a, s=10, color=labs.RED, alpha=0.6, label=f"against an independent truth: r = {deb['corr_independent']:+.2f}")
    ax[1].set(title="Street's dilemma, an analogy: approval of 200 acts", xlabel="fitness effect, or moral truth",
              ylabel="share approving after 400 generations")
    ax[1].legend(loc="center left")
    assert deb["corr_fitness"] > 0.7 and abs(deb["corr_independent"]) < 0.25
    assert abs(deb["corr_independent"]) < deb["corr_third_factor"] < deb["corr_fitness"]
    lab.fig = fig
    return lab
