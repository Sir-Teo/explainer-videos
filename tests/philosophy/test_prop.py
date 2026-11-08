"""The Reasoner's propositional core, checked against brute force."""

from __future__ import annotations

import itertools
import random

from explainer.philosophy.reasoner.prop import (
    And, Imp, Not, Or, Var, atoms_of, cdcl, check_fitch, cnf_clauses, dpll, entails, evaluate, hitting_sets,
    mus_mcs, parse, pigeonhole, post_complete, random_ksat, resolution_refute, satisfiable, satisfiable_bf, show,
    solve, tautology, tseitin, valuations,
)


def _bf_clauses(clauses, n):
    for bits in itertools.product((True, False), repeat=n):
        if all(any((bits[abs(l) - 1] if l > 0 else not bits[abs(l) - 1]) for l in c) for c in clauses):
            return True
    return False


def _random_formula(rng, names, depth):
    if depth == 0 or rng.random() < 0.25:
        return Var(rng.choice(names))
    op = rng.choice(["not", "and", "or", "imp", "iff"])
    if op == "not":
        return Not(_random_formula(rng, names, depth - 1))
    return (op, _random_formula(rng, names, depth - 1), _random_formula(rng, names, depth - 1))


def test_parse_and_show_roundtrip():
    for s in ["p -> q -> r", "(p -> q) -> r", "~(p & q) | r", "p <-> q & r", "¬¬p ∨ (q → r)", "p & (q & r)"]:
        f = parse(s)
        assert parse(show(f)) == f, (s, show(f))
    rng = random.Random(1)
    for _ in range(300):
        f = _random_formula(rng, ["p", "q", "r"], 4)
        assert parse(show(f)) == f


def test_classics():
    assert tautology(parse("((p -> q) -> p) -> p"))  # Peirce's law
    assert tautology(parse("p | ~p"))
    assert not tautology(parse("(p -> q) -> (q -> p)"))
    ok, cm = entails([parse("p -> q"), parse("q")], parse("p"))  # affirming the consequent
    assert not ok and cm == {"p": False, "q": True}
    assert entails([parse("p -> q"), parse("~q")], parse("~p"))[0]


def test_cnf_tseitin_equisatisfiable():
    rng = random.Random(2)
    for _ in range(200):
        f = _random_formula(rng, ["a", "b", "c", "d"], 4)
        names = atoms_of([f])
        sat = satisfiable_bf([f]) is not None
        cl = cnf_clauses(f, names)
        assert _bf_clauses(cl, len(names)) == sat
        # CNF is equivalent, not just equisatisfiable
        for v in valuations(names):
            lits = {i + 1 if v[n] else -(i + 1) for i, n in enumerate(names)}
            assert all(c & lits for c in cl) == evaluate(f, v)
        tc, tn = tseitin(f, names)
        assert (cdcl(tc, len(tn))[0] is not None) == sat


def test_dpll_cdcl_agree_with_brute_force():
    rng = random.Random(3)
    for trial in range(250):
        n = rng.randint(3, 9)
        m = rng.randint(1, 5 * n)
        cl = random_ksat(n, m, 3, rng)
        truth = _bf_clauses(cl, n)
        m1, _ = dpll(cl, n, record=True)
        m2, st = cdcl(cl, n)
        assert (m1 is not None) == truth == (m2 is not None)
        for model in (m1, m2):
            if model is not None:
                assert all(any(model[abs(l)] == (l > 0) for l in c) for c in cl)
        # learned clauses are consequences of the formula
        for lc in st["learned"]:
            neg = [frozenset([-l]) for l in lc]
            assert not _bf_clauses(cl + neg, n)


def test_pigeonhole_unsat_and_resolution():
    for n in (1, 2, 3):
        cl, nv = pigeonhole(n)
        assert cdcl(cl, nv)[0] is None
        assert resolution_refute(cl)["refuted"]
    cl, nv = pigeonhole(4)
    assert cdcl(cl, nv)[0] is None


def test_solve_formulas():
    f = parse("(p | q) & (~p | r) & (~q | r) & ~r")
    assert solve([f]) is None
    g = parse("(p | q) & (~p | r)")
    v = solve([g])
    assert evaluate(g, v)


def test_post():
    assert post_complete(["↑"])[0]
    assert post_complete(["¬", "∧"])[0]
    assert post_complete(["→", "⊥"])[0]
    assert not post_complete(["∧", "∨"])[0]  # monotone
    assert not post_complete(["↔", "¬"])[0]  # affine
    assert not post_complete(["→"])[0]       # T1


def test_mus_mcs_duality():
    rng = random.Random(4)
    for _ in range(60):
        names = [f"c{i}" for i in range(rng.randint(2, 6))]
        claims = {n: _random_formula(rng, ["p", "q", "r"], 2) for n in names}
        r = mus_mcs(claims)
        if r["consistent"]:
            assert r["mus"] == [] and r["mcs"] == [()]
            continue
        hs = {tuple(sorted(h)) for h in hitting_sets(r["mus"])}
        assert hs == {tuple(sorted(m)) for m in r["mcs"]}
    # the problem of evil
    o, k, g, e = Var("o"), Var("k"), Var("g"), Var("e")
    claims = {"omnipotent": o, "omniscient": k, "good": g, "evil": e}
    bg = [Imp(And(o, k, g), Not(e))]
    r = mus_mcs(claims, bg)
    assert r["mus"] == [("omnipotent", "omniscient", "good", "evil")]
    assert r["mcs"] == [("omnipotent",), ("omniscient",), ("good",), ("evil",)]


def test_fitch():
    # modus tollens: p -> q, ~q |- ~p
    proof = [
        (0, "p -> q", "premise", []),
        (0, "~q", "premise", []),
        (1, "p", "assume", []),
        (1, "q", "impE", [1, 3]),
        (1, "⊥", "notE", [4, 2]),
        (0, "~p", "notI", [(3, 5)]),
    ]
    assert check_fitch(proof, ["p -> q", "~q"], "~p")[0]
    # a broken one: citing a closed subproof line
    bad = proof[:-1] + [(0, "q", "reit", [4])]
    assert not check_fitch(bad)[0]
    # contraposition, with nested subproofs
    contra = [
        (0, "p -> q", "premise", []),
        (1, "~q", "assume", []),
        (2, "p", "assume", []),
        (2, "q", "impE", [1, 3]),
        (2, "⊥", "notE", [4, 2]),
        (1, "~p", "notI", [(3, 5)]),
        (0, "~q -> ~p", "impI", [(2, 6)]),
    ]
    assert check_fitch(contra, ["p -> q"], "~q -> ~p")[0]
    # excluded middle, classically
    lem = [
        (1, "~(p | ~p)", "assume", []),
        (2, "p", "assume", []),
        (2, "p | ~p", "orI", [2]),
        (2, "⊥", "notE", [3, 1]),
        (1, "~p", "notI", [(2, 4)]),
        (1, "p | ~p", "orI", [5]),
        (1, "⊥", "notE", [6, 1]),
        (0, "~~(p | ~p)", "notI", [(1, 7)]),
        (0, "p | ~p", "dne", [8]),
    ]
    assert check_fitch(lem, [], "p | ~p")[0]
