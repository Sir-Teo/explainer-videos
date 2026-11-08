from explainer.philosophy.reasoner import worlds as W


def test_translation_agrees_with_counterpart_semantics():
    r = W.census()
    assert r["translation_checks"] > 1000
    assert r["translation_agree"] == r["translation_checks"]


def test_census_matches_the_textbook():
    p = W.census()["principles"]
    # Kripke, constant domains: every principle is valid
    assert all(v["k_const_counter"] == 0 for v in p.values())
    # varying domains: the Barcan formula, its converse, and necessary existence fail
    assert {k for k, v in p.items() if v["k_var_counter"]} == {"BF", "CBF", "NE"}
    # counterpart theory: identity, distinctness, 4, B and the Barcan formula fail; T, CBF and NE hold
    assert {k for k, v in p.items() if v["cp_counter"]} == {"NI", "ND", "4", "B", "BF"}


def test_humphrey():
    rows = {r["key"]: r for r in W.humphrey()["rows"]}
    assert rows["might"]["direct"] and rows["might"]["translated"]
    assert not rows["NI"]["direct"] and not rows["ND"]["direct"]
    assert all(r["direct"] == r["translated"] for r in rows.values())


def test_de_re_de_dicto_and_rigidity():
    rows = W.cyclist()["rows"]
    assert [r["value"] for r in rows] == [True, True, False, False, True]
    r = W.rigid()
    assert r["might_not_name"] and not r["might_not_desc"]


def test_two_dimensional_classes():
    cls = {s["sentence"]: s["class"] for s in W.twod()["sentences"]}
    assert cls["water = H2O"] == "necessary a posteriori"
    assert cls["Hesperus = Phosphorus"] == "necessary a posteriori"
    assert cls["the length of S = one metre"] == "contingent a priori"
    assert cls["water = the watery stuff"] == "contingent a priori"
    assert cls["the evening star = Venus"] == "contingent a posteriori"
    assert cls["H2O = H2O"] == "necessary a priori"


def test_aliens_barcan_essence():
    a = W.alien_properties()
    assert a["genuine"] == 256 and a["ersatz"] < a["genuine"]
    rows = W.barcan()["rows"]
    assert [r["contingentist"] for r in rows] == [False, False, False]
    assert [r["necessitist"] for r in rows] == [True, True, True]
    assert W.essence()["mismatch"] == 3


def test_counterpossibles_and_dispositions():
    c = W.counterpossibles()
    assert all(r["standard"] and r["vacuous"] for r in c["rows"])
    assert [r["impossible"] for r in c["rows"]] == [False, True]
    assert c["same_possible"] and not c["same_all"]
    d = {r["case"]: r for r in W.dispositions()["rows"]}
    assert d["finked glass"]["simple"] is False and d["finked glass"]["reformed"] is True
    assert d["reverse-finked steel"]["simple"] is True and d["reverse-finked steel"]["reformed"] is False
    assert d["masked glass"]["reformed"] is False and d["masked glass"]["fragile"] is True


def test_counterfactual_explanation_has_ties():
    r = W.counterfactual_explanation()
    assert r["score"] < 0
    assert len(r["closest"]) > 1
