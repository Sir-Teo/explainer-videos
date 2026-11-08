"""Precompute everything in Part 5 of *Philosophy, Built* ("Beyond True and False": non-classical logics, vagueness).

    python -m videos.philosophy.philosophy5.compute            # everything missing (about half a minute)

Items:
    tables      the tables of the connectives in K3, Ł3, B3, G3, RM3, and FDE's four values
    compare     nine inferences against CL, K3, LP, Ł3 and FDE, with a countermodel for every failure
    duality     K3 and LP are duals (A ⊨K3 B iff ¬B ⊨LP ¬A) on all 144 pairs of 12 formulas; FDE is weaker than both
    database    Belnap's computer: two sources disagree about a door; queries answered in FDE, and classically
    four        FOUR's truth and information orders; ∧ and ∨ are the truth lattice's meet and join
    corners     the catuṣkoṭi in FDE, and Priest's fifth value: which inferences survive emptiness
    jaina       the seven predications of the saptabhaṅgī from three values
    explosion   Lewis's proof of explosion step by step in LP: the step that fails is disjunctive syllogism
    lpm         minimally inconsistent LP: classical where the premises are consistent, quarantined where not
    relevance   RM3 against the paradoxes of implication: weakening and explosion fail, modus ponens holds
    intkripke   Kripke's semantics for intuitionistic logic (1965) on two stages of knowledge: excluded middle fails
    godel       Gödel's disjunctions D_n: valid in n values, refuted in n + 1, so intuitionistic logic has no finite
                matrix
    tnorms      the Gödel, product and Łukasiewicz t-norms and residua: residuation checked on a grid
    fuzzy       the train controller: its fuzzy sets, one inference step, two simulated stops
    sorites     101 men, 102 premises: classically inconsistent, and every premise is needed (CDCL)
    superval    supervaluation on 21 men with the penumbra 7..13
    degrees     Łukasiewicz degrees on 101 men; how chained modus ponens uses up its guarantee
    margin      Williamson's margin for error: a sharp cutoff that no one can know
    higher      higher-order vagueness: 'definitely' as a box over nearby sharpenings, in the modal module
    quartet     the sorites quartet as a Price List, and five theories' verdicts computed in their own semantics
    linear      the coffee machine in linear logic: six sequents, and the proofs of the provable ones
    quantum     the lattice of subspaces: three lines in a plane break distributivity
    invariance  the permutation-invariant relations and quantifiers on small domains
"""

from __future__ import annotations

import itertools
import time
from fractions import Fraction

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import linear as L
from explainer.philosophy.reasoner import matrix as mx
from explainer.philosophy.reasoner import modal
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy5")
load = CACHE.load


def _v(x) -> str:
    """A value as a short string: Fractions as 0, 1/2, 1; FDE values as they are."""
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)


def _cm(cm):
    return None if cm is None else {k: _v(v) for k, v in cm.items()}


def compute_tables() -> dict:
    out = {}
    for M in (mx.K3, mx.L3, mx.B3, mx.G3, mx.RM3, mx.FDE):
        out[M.name] = {"values": [_v(x) for x in M.values], "designated": sorted(_v(x) for x in M.designated),
                       "not": [_v(r[1]) for r in mx.table(M, "not")],
                       **{op: [[_v(x) for x in row] for row in mx.table(M, op)] for op in ("and", "or", "imp")}}
    # K3 and LP share their tables; they differ only in what counts as holding
    assert mx.table(mx.K3, "imp") == mx.table(mx.LP, "imp")
    return out


COMPARE = ["explosion", "LEM", "noncontradiction", "identity", "MP", "DS"]


def compute_compare() -> dict:
    Ms = [mx.CL, mx.K3, mx.LP, mx.L3, mx.FDE]
    rows = []
    for k in COMPARE:
        ps, c = mx.INFERENCES[k]
        rows.append({"key": k, "premises": ps, "conclusion": c,
                     "cells": [{"valid": v, "cm": _cm(cm)} for v, cm in (mx.consequence(ps, c, M) for M in Ms)]})
    return {"logics": [M.name for M in Ms], "rows": rows,
            "rows_needed": {M.name: len(M.values) ** 2 for M in Ms}}


FORMS = ["p", "~p", "q", "~q", "p & q", "p | q", "p & ~p", "q | ~q", "~(p & q)", "~p | q", "p & (q | ~q)",
         "(p & ~p) | q"]


def compute_duality() -> dict:
    pairs = mism = 0
    gaps = []
    for A, B in itertools.product(FORMS, repeat=2):
        k = mx.consequence([A], B, mx.K3)[0]
        lp = mx.consequence([A], B, mx.LP)[0]
        dual = mx.consequence([f"~({B})"], f"~({A})", mx.LP)[0]
        pairs += 1
        mism += k != dual
        f, cm = mx.consequence([A], B, mx.FDE)
        if k and lp and not f:
            gaps.append({"A": A, "B": B, "cm": _cm(cm)})
    assert mism == 0 and gaps
    return {"pairs": pairs, "mismatches": mism, "fde_gaps": gaps}


def compute_database() -> dict:
    """Source 1 says the door is open (o); source 2 says it is not; nobody says anything about the light (l); the
    safe is locked (s), source 1 says. In FDE each atom is what the computer was told."""
    told = {"o": "b", "l": "n", "s": "t"}
    queries = ["o", "~o", "o & ~o", "s", "l", "l | ~l", "o | l", "~s"]
    rows = [{"q": q, "value": mx.evaluate(q, told, mx.FDE)} for q in queries]
    classical = prop.satisfiable([prop.parse("o"), prop.parse("~o")])
    expl, _ = mx.consequence(["o", "~o"], "~s", mx.FDE)
    return {"told": told, "rows": rows, "classical_consistent": classical, "fde_explodes": expl}


def compute_four() -> dict:
    vals = "tbnf"
    t_edges = [(a, b) for a in vals for b in vals if a != b and mx.truth_leq(a, b) and
               not any(c not in (a, b) and mx.truth_leq(a, c) and mx.truth_leq(c, b) for c in vals)]
    i_edges = [(a, b) for a in vals for b in vals if a != b and mx.info_leq(a, b) and
               not any(c not in (a, b) and mx.info_leq(a, c) and mx.info_leq(c, b) for c in vals)]
    ok = all(mx.FDE.conj(a, b) == mx.lattice_meet(a, b, mx.truth_leq) and
             mx.FDE.disj(a, b) == mx.lattice_join(a, b, mx.truth_leq) for a in vals for b in vals)
    neg_flip = all(mx.truth_leq(a, b) == mx.truth_leq(mx.FDE.neg(b), mx.FDE.neg(a)) and
                   mx.info_leq(a, b) == mx.info_leq(mx.FDE.neg(a), mx.FDE.neg(b)) for a in vals for b in vals)
    tauts = [f for f in ("p | ~p", "p -> p", "~(p & ~p)", "(p & q) -> p") if mx.tautology(f, mx.FDE)[0]]
    return {"truth_edges": t_edges, "info_edges": i_edges, "lattice": ok, "negation": neg_flip,
            "tautologies": tauts, "consensus": mx.lattice_meet("t", "f", mx.info_leq),
            "gullibility": mx.lattice_join("t", "f", mx.info_leq)}


def compute_corners() -> dict:
    inf = [(["p"], "p"), (["p & q"], "p"), (["p"], "p | q"), (["p"], "~~p"), (["~(p | q)"], "~p & ~q")]
    rows = []
    for ps, c in inf:
        a, _ = mx.consequence(ps, c, mx.FDE)
        b, cm = mx.consequence(ps, c, mx.FDE_E)
        rows.append({"premises": ps, "conclusion": c, "fde": a, "fde_e": b, "cm": _cm(cm)})
    e_inf = all(mx.FDE_E.conj("e", x) == "e" and mx.FDE_E.disj("e", x) == "e" for x in "tbnfe")
    return {"rows": rows, "e_infects": e_inf, "values": len(mx.FDE_E.values)}


def compute_jaina() -> dict:
    return {"bhangas": [list(b) for b in mx.saptabhangi()]}


def compute_explosion() -> dict:
    steps = [(["p & ~p"], "p", r"$\land$E"), (["p & ~p"], "~p", r"$\land$E"), (["p"], "p | q", r"$\lor$I"),
             (["p | q", "~p"], "q", r"disjunctive syllogism")]
    rows = []
    for ps, c, rule in steps:
        v, cm = mx.consequence(ps, c, mx.LP)
        rows.append({"premises": ps, "conclusion": c, "rule": rule, "lp": v, "cm": _cm(cm)})
    assert [r["lp"] for r in rows] == [True, True, True, False]
    return {"rows": rows}


LPM = [(["p | q", "~p"], "q"), (["p", "p -> q"], "q"), (["p", "~p"], "q"), (["p", "~p", "p | q"], "q"),
       (["p", "~p", "r | q", "~r"], "q")]


def compute_lpm() -> dict:
    rows = []
    for ps, c in LPM:
        a, _ = mx.consequence(ps, c, mx.LP)
        b, cm = mx.lpm_consequence(ps, c)
        cl = prop.entails([prop.parse(x) for x in ps], prop.parse(c))[0]
        rows.append({"premises": ps, "conclusion": c, "cl": cl, "lp": a, "lpm": b, "cm": _cm(cm)})
    assert [r["lpm"] for r in rows] == [True, True, False, False, True]
    return {"rows": rows}


def compute_relevance() -> dict:
    fs = ["p -> p", "p -> (q -> p)", "(p & ~p) -> q", "p -> (q | ~q)", "(p & (p -> q)) -> q", "(p -> q) -> (~q -> ~p)"]
    rows = []
    for f in fs:
        c = mx.tautology(f, mx.CL)[0]
        r, cm = mx.tautology(f, mx.RM3)
        rows.append({"f": f, "cl": c, "rm3": r, "cm": _cm(cm)})
    mp, _ = mx.consequence(["p", "p -> q"], "q", mx.RM3)
    # variable sharing: every RM3-valid conditional here has an atom common to antecedent and consequent
    share = all(set(prop.atoms(prop.parse(f)[1])) & set(prop.atoms(prop.parse(f)[2])) for f in fs
                if mx.tautology(f, mx.RM3)[0])
    # RM3 is only semi-relevant: this theorem's two sides share no atom (R-mingle's known defect)
    mingle = mx.tautology("(p & ~p) -> (q | ~q)", mx.RM3)[0]
    assert mingle
    return {"rows": rows, "mp": mp, "sharing": share, "mingle": mingle}


def _forces(f, w, W, up, V):
    """Intuitionistic forcing on a preorder of stages (Kripke 1965): implication and negation look at every later
    stage; atoms, once forced, stay forced."""
    op = f[0]
    if op == "var":
        return w in V[f[1]]
    if op == "bot":
        return False
    if op == "and":
        return _forces(f[1], w, W, up, V) and _forces(f[2], w, W, up, V)
    if op == "or":
        return _forces(f[1], w, W, up, V) or _forces(f[2], w, W, up, V)
    if op == "imp":
        return all(not _forces(f[1], v, W, up, V) or _forces(f[2], v, W, up, V) for v in up[w])
    if op == "not":
        return all(not _forces(f[1], v, W, up, V) for v in up[w])
    raise ValueError(op)


def compute_intkripke() -> dict:
    W = [0, 1]
    up = {0: [0, 1], 1: [1]}
    V = {"p": {1}}
    forms = ["p", "~p", "p | ~p", "~~p", "~~p -> p", "p -> ~~p"]
    table = {f: [_forces(prop.parse(f), w, W, up, V) for w in W] for f in forms}
    assert table["p | ~p"] == [False, True] and table["~~p"] == [True, True]
    return {"forms": forms, "table": table}


def compute_godel() -> dict:
    rows = []
    for n in (2, 3, 4):
        f = mx.godel_disjunction(n)
        a, _ = mx.tautology(f, mx.godel_matrix(n))
        b, cm = mx.tautology(f, mx.godel_matrix(n + 1))
        rows.append({"n": n, "atoms": n + 1, "valid_n": a, "valid_n1": b, "cm": _cm(cm),
                     "disjuncts": (n + 1) * n // 2})
    g3 = {k: mx.consequence(*mx.INFERENCES[k], mx.G3)[0] for k in ("LEM", "DNE", "noncontradiction", "identity")}
    dn = mx.consequence(["p"], "~~p", mx.G3)[0]
    return {"rows": rows, "g3": g3, "p_to_nnp": dn}


def compute_tnorms() -> dict:
    return {"residuation": {k: mx.residuum_check(k) for k in mx.TNORMS}}


def compute_fuzzy() -> dict:
    xs_d = list(range(0, 401, 5))
    xs_s = [i * 0.25 for i in range(0, 89)]
    xs_b = [i / 100 for i in range(101)]
    sets = {"dist": {k: [mx.tri(x, *v) for x in xs_d] for k, v in mx.DIST.items()},
            "speed": {k: [mx.tri(x, *v) for x in xs_s] for k, v in mx.SPEED.items()},
            "brake": {k: [mx.tri(x, *v) for x in xs_b] for k, v in mx.BRAKE.items()}}
    ex = mx.fuzzy_brake(120.0, 15.0)
    sims = {}
    for c in ("fuzzy", "bang"):
        r = mx.simulate_stop(c)
        k = 4
        sims[c] = {"t": r["t"][::k], "x": r["x"][::k], "v": r["v"][::k], "a": r["a"][::k], "error": r["error"],
                   "jerk": r["jerk"], "time": r["time"]}
    return {"xs": {"dist": xs_d, "speed": xs_s, "brake": xs_b}, "sets": sets, "rules": mx.RULES,
            "example": {"d": 120.0, "v": 15.0, "fire": ex["fire"], "agg": ex["agg"], "brake": ex["brake"]},
            "sims": sims}


def compute_sorites() -> dict:
    t = time.time()
    r = mx.sorites_classical(100)
    r["seconds"] = round(time.time() - t, 2)
    assert not r["consistent"] and r["every_premise_needed"]
    small = mx.sorites_classical(5)
    return {"big": r, "small": small}


def compute_superval() -> dict:
    return mx.supervaluation_report(20, 6, 13)


def compute_degrees() -> dict:
    r = mx.degree_report(100, 30, 70)
    r["exhausted_at"] = next(i for i, b in enumerate(r["mp_bound"]) if b == 0.0)
    return r


def compute_margin() -> dict:
    r = mx.margin_report(40, 20, 3)
    r.update({"n": 40, "cutoff": 20, "margin": 3})
    return r


def compute_higher() -> dict:
    """Worlds are the admissible sharpenings k = 7..14 of `bald' on men 0..20 (man i is bald at k iff i < k). A
    sharpening sees those within 2 of it: what we cannot tell apart. 'Definitely φ' is the box: φ on every
    sharpening in view. Each man gets a status for B, DB and DDB: T (at every sharpening), F (at none), I."""
    n, lo, hi, mrg = 20, 6, 14, 2
    W = list(range(lo + 1, hi + 1))
    R = {(a, b) for a in W for b in W if abs(a - b) <= mrg}
    V = {f"B{i}": {k for k in W if i < k} for i in range(n + 1)}
    M = modal.Model(W, R, V)
    rows = {}
    for name, pre in (("B", ""), ("DB", "[]"), ("DDB", "[][]")):
        st = []
        for i in range(n + 1):
            vals = {modal.holds(modal.parse(f"{pre}B{i}"), M, k) for k in W}
            st.append("T" if vals == {True} else "F" if vals == {False} else "I")
        rows[name] = st
    bd = []
    for i in range(n + 1):
        f = modal.parse(f"~[]B{i} & ~[]~B{i}")
        vals = {modal.holds(f, M, k) for k in W}
        bd.append("T" if vals == {True} else "F" if vals == {False} else "I")
    rows["borderline"] = bd
    return {"n": n, "worlds": W, "margin": mrg, "rows": rows}


QUARTET = [
    ("T", r"tolerance: \ one hair never makes the difference to baldness", "t"),
    ("E", r"the extremes: \ a man with no hair is bald; \ one with 100{,}000 is not", "e"),
    ("B", r"bivalence: \ each `man $i$ is bald' is true or false", "b"),
    ("L", r"classical logic: \ modus ponens may be chained", "l"),
]


def compute_quartet() -> dict:
    claims = {k: prop.parse(f) for k, _, f in QUARTET}
    # the Reasoner's classical check (item `sorites'): with bivalence and classical logic, tolerance and the
    # extremes are jointly unsatisfiable
    bg = [prop.parse("(t & e & b & l) -> F"), prop.parse("~F")]
    r = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in QUARTET], "mus": [sorted(x) for x in r["mus"]],
            "mcs": [sorted(x) for x in r["mcs"]], "theories": mx.tolerance_table(10, 3, 7)}


SEQUENTS = [(["$", "$ -o coffee"], "coffee"), (["$", "$ -o coffee", "$ -o tea"], "coffee * tea"),
            (["$", "$", "$ -o coffee", "$ -o tea"], "coffee * tea"), (["$", "$ -o (coffee & tea)"], "tea"),
            (["$", "$ -o (coffee & tea)"], "coffee * tea"), (["$", "$ -o (coffee + tea)"], "coffee")]


def _tree(p):
    return {"rule": p[0], "seq": L.sequent_tex(p[1]), "kids": [_tree(q) for q in p[2]]} if p else None


def compute_linear() -> dict:
    rows = []
    for h, g in SEQUENTS:
        p = L.prove(h, g)
        cl = lambda x: prop.parse(x.replace("-o", "->").replace("$", "d").replace("*", "&").replace("+", "|"))  # noqa
        classical = prop.entails([cl(x) for x in h], cl(g))[0]
        rows.append({"hyps": [L.show(L.parse(x), True) for x in h], "goal": L.show(L.parse(g), True),
                     "provable": p is not None, "classical": classical, "proof": _tree(p), "size": L.size(p)})
    structural = {"contraction": L.provable(["A"], "A * A"), "weakening": L.provable(["A", "B"], "A"),
                  "exchange": L.provable(["A * B"], "B * A")}
    return {"rows": rows, "structural": structural}


def compute_quantum() -> dict:
    r = mx.distributivity_counterexample()
    return {**r, "p": [1, 0, 0], "q": [0, 1, 0], "r": [0.7071, 0.7071, 0]}


def compute_invariance() -> dict:
    rel = mx.invariant_relations(3)
    names = {0: "empty", 3: "identity", 6: "distinctness", 9: "everything"}
    return {"relations": [{"size": len(R), "name": names[len(R)]} for R in sorted(rel, key=len)],
            "quantifiers": [mx.invariant_quantifiers(n) for n in (1, 2, 3, 4)]}


ITEMS = {"tables": compute_tables, "compare": compute_compare, "duality": compute_duality,
         "database": compute_database, "four": compute_four, "corners": compute_corners, "jaina": compute_jaina,
         "explosion": compute_explosion, "lpm": compute_lpm, "relevance": compute_relevance, "intkripke": compute_intkripke, "godel": compute_godel,
         "tnorms": compute_tnorms, "fuzzy": compute_fuzzy, "sorites": compute_sorites, "superval": compute_superval,
         "degrees": compute_degrees, "margin": compute_margin, "higher": compute_higher, "quartet": compute_quartet,
         "linear": compute_linear, "quantum": compute_quantum, "invariance": compute_invariance}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
