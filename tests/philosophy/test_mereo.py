from explainer.philosophy.reasoner import mereo as M


def test_poset_counts_match_oeis():
    # A000112: unlabeled posets on n elements
    assert [len(M.posets_up_to_iso(n)) for n in range(1, 6)] == [1, 2, 5, 16, 63]


def test_cem_models_are_boolean_minus_bottom():
    rows = M.mereology_census(5)["rows"]
    assert [r["cem"] for r in rows] == [1, 0, 1, 0, 0]
    for k, v in M.boolean_check(4).items():
        assert v["size"] == 2 ** k - 1 and v["ssp"] and v["uf"] and v["atoms"] == k


def test_supplementation_counterexamples():
    c = M.counterexamples()
    assert c["twin"]["wsp"] and not c["twin"]["ssp"] and not c["twin"]["ext"]
    assert not c["lonely"]["wsp"]


def test_composition_and_putnam():
    d = M.composition_counts(2, 3)
    assert d["nihilism"] == 6 and d["universalism"] == 63 and 6 < d["contact"] < 63
    assert M.putnam_world(3)["polish"] == 7


def test_goodman_and_geach_kaplan():
    g = M.goodman_demo()
    assert g["imperfect"]["spurious"] == [("a", "b", "c")]
    assert "F" in g["companionship"]["missing"]
    gk = M.geach_kaplan_demo()
    assert gk["a closed circle"]["true"] and not gk["everyone admires a self-admirer"]["true"]


def test_grounding_order():
    g = M.grounding_check()
    assert g["irreflexive"] and g["asymmetric"] and g["transitive"] and len(g["fundamental"]) == 5
    assert M.grounding_cycle_demo()["cyclic"]


def test_logic_of_ground():
    g = M.ground_demo()
    assert g["f1"]["fundamental"] == [r"\lnot r", "p", "q"]
    assert g["f3"]["grounds"] == [["p"], ["p"]]
    v = {"p": False, "q": False}
    assert M.immediate_grounds(("not", ("or", "p", "q")), v) == [[("not", "p"), ("not", "q")]]
