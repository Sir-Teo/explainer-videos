"""Part 17's Reasoner: INUS conditions, SCMs, do, counterfactuals, d-separation, adjustment, Markov equivalence,
actual causation, PC."""

from explainer.philosophy.reasoner import causal as C


def test_inus():
    f = lambda sc, fl, sp, ar: int((sc and fl and not sp) or (ar and fl))  # noqa: E731
    r = C.inus(f, ["sc", "fl", "sp", "ar"], "sc")
    assert r["inus"] and {"fl": 1, "ar": 1} in r["prime_implicants"]


def test_dsep_and_equivalence():
    g = C.DAG([("A", "B"), ("B", "C")])
    assert C.DAG([("A", "B"), ("B", "C")]).dsep({"A"}, {"C"}, {"B"})
    assert not g.dsep({"A"}, {"C"}, set())
    collider = C.DAG([("A", "B"), ("C", "B")])
    assert collider.dsep({"A"}, {"C"}, set()) and not collider.dsep({"A"}, {"C"}, {"B"})
    assert C.markov_equivalent(g, C.DAG([("B", "A"), ("C", "B")]))
    assert not C.markov_equivalent(g, collider)
    assert len(C.equivalence_class(g)) == 3


def test_adjustment():
    d = C.adjustment_demo()
    assert abs(d["backdoor"]["adjusted"] - d["backdoor"]["truth"]) < 1e-9
    assert abs(d["backdoor"]["naive"] - d["backdoor"]["truth"]) > 0.05
    assert d["backdoor"]["criterion_A"] and not d["backdoor"]["criterion_empty"]
    assert abs(d["frontdoor"]["front"] - d["frontdoor"]["truth"]) < 1e-9


def test_counterfactuals():
    d = C.pn_ps_demo()
    assert abs(d["PN"] - 0.6) < 1e-9 and abs(d["PNS"] - 0.3) < 1e-9


def test_actual_causation():
    cases = {(c["case"], c["candidate"]): c for c in C.classic_cases()}
    assert cases[("rock throwing", "ST")]["hp"] and not cases[("rock throwing", "BT")]["hp"]
    assert not cases[("rock throwing", "ST")]["but_for"]
    assert cases[("forest fire (disjunctive)", "L")]["conjunction_L_and_M"]
    assert cases[("forest fire (conjunctive)", "L")]["hp"]
    assert not cases[("bogus prevention", "B")]["hp"]


def test_pc():
    d = C.pc_demo(n=8000)
    assert d["oracle"]["directed"] == [("R", "W"), ("S", "W"), ("W", "L")]
    assert sorted(d["oracle"]["undirected"]) == [("C", "R"), ("C", "S")]


def test_do_calculus():
    d = C.frontdoor_derivation()
    assert all(s["ok"] for s in d["steps"])
    assert not any(d["bow"].values()) and not d["wrong_P(c|do s)=P(c|s)"]
    m = C.m_bias()
    assert abs(m["naive"] - m["truth"]) < 1e-9 and abs(m["adjusted_M"] - m["truth"]) > 0.05
    assert m["criterion_empty"] and not m["criterion_M"]


def test_responsibility_and_bell():
    assert [C.responsibility(a, b)["k"] for a, b in ((6, 5), (7, 4), (11, 0))] == [0, 1, 5]
    b = C.chsh()
    assert b["local_max"] == 2 and abs(b["quantum"] - 2 * 2 ** 0.5) < 1e-9


def test_designs():
    d = C.perfect_doctor()
    assert abs(d["rand_mean"] - d["ate"]) < 1e-9 and d["naive"] > 0 > d["ate"]
    iv = C.instrumental(n=20000)
    assert abs(iv["iv"] - iv["beta"]) < 0.05 and iv["ols"] > iv["beta"] + 0.3
    assert abs(C.diff_in_diff()["did"] - 2.7) < 1e-9
    u = C.uplift_demo(n=50000)
    assert u["gain_uplift"] > 0 > u["gain_response"]
    icp = C.icp_demo()
    assert abs(icp["1"]["Y_on_X"] - icp["2"]["Y_on_X"]) < 0.05
    assert abs(icp["1"]["Y_on_Z"] - icp["2"]["Y_on_Z"]) > 0.5
    lg = C.lingam_demo(n=3000)
    assert lg["uniform"]["backward_dep"] > 5 * lg["uniform"]["forward_dep"]
