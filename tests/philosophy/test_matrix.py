"""The non-classical Reasoner against facts from the textbooks (Priest, *Introduction to Non-Classical Logic*)."""

from explainer.philosophy.reasoner import linear as L
from explainer.philosophy.reasoner import matrix as mx
from explainer.philosophy.reasoner import prop


def valid(ps, c, M):
    return mx.consequence(ps, c, M)[0]


def test_classical_matrix_agrees_with_prop():
    for ps, c in mx.INFERENCES.values():
        want = prop.entails([prop.parse(p) for p in ps], prop.parse(c))[0]
        assert valid(ps, c, mx.CL) == want


def test_k3_lp_duality():
    # K3 has no tautologies; LP has no explosion and no modus ponens; both keep De Morgan
    assert not valid([], "p | ~p", mx.K3) and not valid([], "p -> p", mx.K3)
    assert valid([], "p | ~p", mx.LP) and not valid(["p", "~p"], "q", mx.LP)
    assert not valid(["p", "p -> q"], "q", mx.LP) and valid(["p", "p -> q"], "q", mx.K3)
    assert not valid(["p | q", "~p"], "q", mx.LP)
    for M in (mx.K3, mx.LP, mx.FDE):
        assert valid(["~(p & q)"], "~p | ~q", M) and valid(["~p | ~q"], "~(p & q)", M)


def test_lukasiewicz_and_godel():
    assert valid([], "p -> p", mx.L3) and not valid([], "p | ~p", mx.L3)
    assert not valid([], "p | ~p", mx.G3) and not valid(["~~p"], "p", mx.G3) and valid(["p"], "~~p", mx.G3)
    for n in (2, 3, 4):
        f = mx.godel_disjunction(n)
        assert mx.tautology(f, mx.godel_matrix(n))[0] and not mx.tautology(f, mx.godel_matrix(n + 1))[0]


def test_fde_has_no_tautologies_and_is_the_truth_lattice():
    for f in ("p | ~p", "p -> p", "~(p & ~p)"):
        assert not mx.tautology(f, mx.FDE)[0]
    for a in "tbnf":
        for b in "tbnf":
            assert mx.FDE.conj(a, b) == mx.lattice_meet(a, b, mx.truth_leq)
            assert mx.FDE.disj(a, b) == mx.lattice_join(a, b, mx.truth_leq)
    assert mx.lattice_join("t", "f", mx.info_leq) == "b" and mx.lattice_meet("t", "f", mx.info_leq) == "n"


def test_relevance_and_weak_kleene():
    assert not valid(["p"], "q -> p", mx.RM3) and not valid(["p & ~p"], "q", mx.RM3)
    assert valid(["p", "p -> q"], "q", mx.RM3)
    assert not valid(["p"], "p | q", mx.B3)
    assert not valid(["p"], "p | q", mx.FDE_E) and valid(["p"], "p", mx.FDE_E)


def test_saptabhangi_and_invariance():
    assert len(mx.saptabhangi()) == 7
    assert [len(R) for R in mx.invariant_relations(3)] == [0, 6, 3, 9]
    for n in (1, 2, 3):
        q = mx.invariant_quantifiers(n)
        assert q["invariant"] == q["by_cardinality"] == 2 ** (n + 1)


def test_tnorm_residuation():
    for name in mx.TNORMS:
        assert mx.residuum_check(name)


def test_sorites():
    c = mx.sorites_classical(30)
    assert not c["consistent"] and c["every_premise_needed"]
    sv = mx.supervaluation_report(10, 3, 7)
    assert sv["cutoff"] == "T" and sv["no_witness"] and set(sv["lem"]) == {"T"}
    assert sv["bald"][0] == "T" and sv["bald"][-1] == "F" and "I" in sv["bald"]
    d = mx.degree_report(100, 20, 80)
    assert 0.98 < d["min_conditional"] < 1 and d["mp_bound"][-1] == 0.0
    t = mx.tolerance_table()
    assert all(sum(not v for v in row.values()) >= 1 for row in t.values())


def test_quantum_distributivity_fails():
    r = mx.distributivity_counterexample()
    assert r["lhs_dim"] == 1 and r["rhs_dim"] == 0 and not r["equal"]


def test_fuzzy_controller_is_smoother():
    f, b = mx.simulate_stop("fuzzy"), mx.simulate_stop("bang")
    assert abs(f["error"]) < 3 and f["jerk"] < b["jerk"] / 3


def test_linear_logic_counts_resources():
    assert L.provable(["$", "$ -o coffee"], "coffee")
    assert not L.provable(["$", "$ -o coffee", "$ -o tea"], "coffee * tea")
    assert L.provable(["$", "$", "$ -o coffee", "$ -o tea"], "coffee * tea")
    assert L.provable(["$", "$ -o (coffee & tea)"], "tea")
    assert not L.provable(["$", "$ -o (coffee + tea)"], "coffee")
    assert not L.provable(["A"], "A * A") and not L.provable(["A", "B"], "A")
    assert L.provable(["A -o B", "B -o C"], "A -o C") and L.provable(["A * B"], "B * A")
