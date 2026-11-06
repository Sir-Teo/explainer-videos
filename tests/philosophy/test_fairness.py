"""Checks for the Reasoner's fairness module (Part 41)."""

import math

from explainer.philosophy.reasoner import fairness as F


def test_criteria_and_identity():
    c = F.criteria()
    r = c["rates"]
    assert r["A"]["base"] < r["B"]["base"]
    for g in "AB":
        assert abs(c["identity_fpr"][g] - r[g]["fpr"]) < 0.002
    assert c["balance"]["A"]["pos"] < c["balance"]["B"]["pos"]


def test_thresholds_trade_off():
    g = F.group_thresholds()
    assert abs(g["fpr"]["A"]["fpr"] - g["fpr"]["B"]["fpr"]) < 0.01
    assert abs(g["fpr"]["A"]["ppv"] - g["fpr"]["B"]["ppv"]) > 0.1
    assert abs(g["ppv"]["A"]["ppv"] - g["ppv"]["B"]["ppv"]) < 0.01
    assert abs(g["ppv"]["A"]["fpr"] - g["ppv"]["B"]["fpr"]) > 0.1


def test_counterfactual_dp_explain():
    assert F.counterfactual()["fair_u"]
    for m in F.laplace()["mechanisms"]:
        assert abs(m["max_ratio"] - math.exp(m["eps"])) < 1e-3
    rr = F.randomized_response()
    assert abs(rr["estimate"] - rr["true_p"]) < 3 * rr["se"] + 0.02
    rec = F.reconstruction()["results"]
    assert rec[0]["recovered"] == 1.0 and rec[-1]["recovered"] < 0.9
    e = F.explain()
    assert e["sum_ok"] and not e["accepted"] and e["best"]["feature"] in ("income", "history")
