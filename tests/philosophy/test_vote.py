"""Checks for the Reasoner's vote module (Part 39)."""

import math

from explainer.philosophy.reasoner import vote as V


def test_rules_and_paradox():
    z = V.zoo()
    winners = [z[k]["winner"] for k in ("plurality", "runoff", "irv", "borda")] + [z["condorcet"]]
    assert winners == ["A", "B", "C", "D", "E"]
    assert V.condorcet_paradox()["winner"] is None
    assert abs(V.paradox_exact(3) - 1 / 18) < 1e-12
    assert abs(V.GUILBAUD - 0.08774) < 1e-5


def test_may_and_arrow():
    assert V.may_theorem()["is_majority"]
    a = V.arrow_sat()
    assert not a["satisfiable"] and len(a["mus"]) == 1 and len(a["mcs"]) == 5
    m = V.arrow_models()
    assert m["models"] == 2 and m["dictator_of_each"] == [[1], [2]]


def test_manipulation_and_peaks():
    m = V.manipulation()
    assert m["dictator"]["manipulable"] == 0 and m["a_or_b"]["manipulable"] == 0
    assert all(m[k]["manipulable"] > 0 for k in ("plurality", "borda", "irv", "copeland"))
    b = V.black()
    assert b["with_winner"] == b["profiles"] == b["winner_is_median"] == 4096


def test_juries_judgments_seats_and_bt():
    j = V.jury()
    assert j["independent"]["0.6"][-1] > 0.99 and abs(j["correlated"][-1] - 0.6) < 0.01
    assert not V.list_pettit()["any_ok"] and not V.doctrinal()["majority_consistent"]
    al = V.alabama()
    assert al["hamilton"][1][2] < al["hamilton"][0][2] and al["webster"][1][2] >= al["webster"][0][2]
    bt = V.bradley_terry()
    assert bt["bt_order"] == bt["borda_order"] and bt["condorcet_winner"] != bt["bt_order"][0]


def test_irv_monotonicity_and_qv():
    m = V.irv_monotonicity()
    assert m["n"] == 21 and m["winner_before"] == "C" and m["winner_after"] == "A"
    q = V.quadratic()
    assert q["majority"] == "pass" and q["qv"] == "fail"
