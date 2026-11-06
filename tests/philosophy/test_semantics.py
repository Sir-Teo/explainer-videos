"""Tests for the Reasoner's semantics toolkit (Part 27)."""

from explainer.philosophy.reasoner import semantics as M


def test_white_horse_medians_and_descriptions():
    w = M.white_horse()
    assert w["inclusion"] and not w["identity"] and w["yellow_answers_horse"] and not w["yellow_answers_white_horse"]
    m = M.medians()
    assert m["spread"] < 1e-12
    rows = {r["model"]: r["values"] for r in M.descriptions()["rows"]}
    assert rows["no king"] == {"the K is B": False, "wide: not (the K is B)": True, "narrow: the K is not B": False}
    assert rows["one bald king"]["the K is B"] and not rows["two kings"]["the K is B"]


def test_rigidity_two_d_and_kaplan():
    r = M.rigidity()
    assert r["name_rigid"] and not r["description_rigid"] and r["prover_de_re"] and not r["prover_de_dicto"]
    s = M.two_d()["sentences"]
    assert s["water = H2O"]["necessary"] and not s["water = H2O"]["a_priori"]
    assert s["water is the watery stuff"]["a_priori"] and not s["water is the watery stuff"]["necessary"]
    k = M.kaplan()
    assert k["a_priori"] and k["contingent_in"] > 0


def test_t_theory_and_fragment():
    t = M.t_theory()
    assert "T(" not in t["steps"][-1] and t["value"] is True
    fr = M.fragment()
    assert fr["Ann smokes"]["value"] is True
    assert fr["every student read a book (surface)"]["value"] is True
    assert fr["every student read a book (inverse)"]["value"] is False
    assert [n["rule"] for n in fr["Ann likes every student (QR)"]["nodes"]].count("PA") == 1
    assert M.sql_check()["all_agree"]


def test_quantifiers_ef_and_dpl():
    q = M.quantifiers()["rows"]
    assert all(q[k]["conservative"] for k in q if k != "only") and not q["only"]["conservative"]
    assert q["every"]["left_down"] and q["every"]["right_up"] and q["some"]["left_up"]
    c = M.count_conservative()
    assert c["all"] == 65536 and c["conservative"] == 512 == c["formula"]
    for r in M.ef_most(k_max=3)["rows"]:
        assert r["duplicator_k"] and not r["duplicator_k_plus_1"] and r["most_M1"] != r["most_M2"]
    d = M.donkeys(trials=200)
    assert d["dpl_vs_fo"] == 200 and d["discourse"] == 200 and d["dpl_vs_naive"] < 200
    o = M.omniscience()
    assert o["propositions"] <= 16 < o["formulas"]
