"""Checks for the Reasoner's justice module (Part 38)."""

from explainer.philosophy.reasoner import justice as J


def test_veil_and_difference_principle():
    v = J.veil()
    assert v["by_eta"][0]["choice"] == v["avg_choice"] and v["by_eta"][-1]["choice"] == v["maximin_choice"]
    d = J.difference_principle()["points"]
    assert d["difference"]["uL"] > d["equality"]["uL"] > d["utilitarian"]["uL"]


def test_markets_and_paradox():
    c = J.ceei()
    assert c["envy_free"] and all(abs(x - 1) < 1e-3 for x in c["spent"])
    lp = J.liberal_paradox()
    assert lp["pairs_checked"] == 6 and lp["all_cycle"]


def test_fair_division():
    assert J.selfridge_conway()["envy_free"]
    r = J.rent_division()
    assert abs(sum(r["prices"]) - r["rent"]) < 1e-6 and r["min_utility"] == 165.0


def test_three_societies_and_gini():
    t = J.three_societies()
    assert (t["total"], t["maximin"], t["equality"]) == ("C", "B", "A")
    assert abs(J.gini([0, 0, 0, 1]) - 0.75) < 1e-12 and J.gini([1, 1, 1, 1]) == 0.0
    w = J.wilt()
    assert w["gini_before"] == 0.0 and w["share_of_wilt"] == 0.01


def test_stable_matching():
    m = J.stable_matching()
    assert J.is_stable(m["student_match"], m["student_prefs"], m["school_priority"])
    assert m["student_match"] in m["stable"] and m["school_match"] in m["stable"]
    assert m["student_optimal"] and m["worst_for_students"] and len(m["stable"]) == 3
