"""Agora's price maker (Part 10), each result checked against a closed form or a second method."""

import numpy as np
import pytest

from explainer.economics.agora import pricing as pr


def test_monopoly_closed_forms_and_lerner():
    d = pr.Linear(100.0, 10.0)
    m = pr.monopoly(d, 2.0)
    assert m["p"] == pytest.approx((100 / 10 + 2) / 2)               # (a/b + c) / 2
    assert m["lerner"] == pytest.approx(m["inv_elasticity"])
    assert m["dwl"] == pytest.approx(0.5 * (m["p"] - 2) * (m["q_competitive"] - m["q"]))
    ce = pr.ConstantElasticity(1000.0, 3.0)
    mc = pr.monopoly(ce, 2.0)
    assert mc["p"] == pytest.approx(3.0) and mc["lerner"] == pytest.approx(1 / 3)


def test_pass_through():
    assert pr.pass_through(pr.Linear(100.0, 10.0), 2.0) == pytest.approx(0.5, abs=1e-6)
    assert pr.pass_through(pr.ConstantElasticity(1000.0, 3.0), 2.0) == pytest.approx(1.5, abs=1e-6)


def test_ferry_revenue_peak():
    rng = np.random.default_rng(0)
    v = rng.uniform(0, 10, 20000)
    f = pr.ferry(v, [5.0])
    assert f["best_fare"] == pytest.approx(5.0, abs=0.2)              # uniform values: revenue peaks at half the top
    assert f["rows"][0]["revenue"] + f["rows"][0]["surplus"] + f["rows"][0]["lost"] == pytest.approx(f["total_value"])


def test_discrimination():
    d = pr.Linear(100.0, 10.0)
    fd = pr.first_degree(d, 2.0)
    assert fd["profit"] == pytest.approx(float(d.cs(2.0))) and fd["dwl"] == 0
    t = pr.third_degree(pr.Linear(60.0, 10.0), pr.Linear(100.0, 5.0), 1.0)
    assert t["discriminate"]["profit"] >= t["uniform"]["profit"] - 1e-9
    # Varian: welfare can rise only if output rises; here the students are priced out by one price
    assert t["discriminate"]["q"] > t["uniform"]["q"] and t["discriminate"]["welfare"] > t["uniform"]["welfare"]


def test_screening_is_incentive_compatible():
    s = pr.screening(1.0, 2.0, 0.3)
    uH_own = 2.0 * s["qH"] - s["pH"]
    uH_mimic = 2.0 * s["qL"] - s["pL"]
    uL_own = 1.0 * s["qL"] - s["pL"]
    assert uH_own >= uH_mimic - 1e-12 and uL_own == pytest.approx(0)
    assert s["qH"] == pytest.approx(2.0) and s["qL"] < 1.0           # no distortion at the top; the bottom cut
    # a brute-force search over menus does no better
    best = 0.0
    for qL in np.linspace(0, 1.2, 241):
        pL = 1.0 * qL
        qH = 2.0
        pH = 2.0 * qH - (2.0 - 1.0) * qL
        best = max(best, 0.7 * (pL - qL ** 2 / 2) + 0.3 * (pH - qH ** 2 / 2))
    assert s["profit"] == pytest.approx(best, abs=1e-4)


def test_two_part_tariffs():
    one = pr.two_part([pr.Linear(10.0, 1.0)], 2.0)
    assert one["p"] == pytest.approx(2.0, abs=1e-5) and one["fee"] == pytest.approx(32.0, abs=1e-4)
    assert one["profit"] > one["profit_one_price"]
    small, keen = pr.Linear(10.0, 1.0), pr.Linear(16.0, 1.0)
    two = pr.two_part([small, small, keen], 2.0)                         # two ordinary visitors to one keen one
    # profit 1.5 (10 - p)^2 + (p - 2)(36 - 3p) peaks at p = 4, fee 18, profit 102
    assert two["p"] == pytest.approx(4.0, abs=1e-5) and two["fee"] == pytest.approx(18.0, abs=1e-4)
    assert two["profit"] == pytest.approx(102.0, abs=1e-4) and two["profit_at_cost"] == pytest.approx(96.0)
    assert two["profit_without_smallest"] == pytest.approx(98.0, abs=1e-4)   # shutting the ordinary visitors out
    pair = pr.two_part([small, keen], 2.0)
    assert pair["profit_without_smallest"] > pair["profit"]                  # ... pays when they are as many as the keen


def test_bundling_pays_with_negative_correlation():
    rng = np.random.default_rng(2)
    v1 = rng.uniform(0, 10, 300)
    neg = np.clip(10 - v1 + rng.normal(0, 0.5, 300), 0, None)
    b = pr.bundling(v1, neg)
    assert b["bundle"]["profit"] > 1.3 * b["separate"]["profit"]
    assert b["mixed"]["profit"] >= max(b["bundle"]["profit"], b["separate"]["profit"]) - 1e-9


def test_coase_conjecture():
    prices = [pr.coase(d, 4000)["first_price"] for d in (0.0, 0.5, 0.9, 0.99)]
    assert prices[0] == pytest.approx(0.5)
    assert all(a > b for a, b in zip(prices, prices[1:]))
    two = pr.coase(0.5, 2)
    # two periods by hand: cutoff s solves the seller's problem; the first price is s (1 - delta + delta / 2)
    m = 1 - 0.5 + 0.5 * 0.5
    s = m / (2 * m - 2 * 0.5 * 0.25)
    assert two["first_price"] == pytest.approx(s * m)


def test_ramsey_inverse_elasticity():
    r = pr.ramsey(pr.ConstantElasticity(100.0, 1.5), pr.ConstantElasticity(100.0, 4.0), 1.0, 1.0, 40.0)
    m1, m2 = r["markups"]
    assert m1 * 1.5 == pytest.approx(m2 * 4.0)                      # (p - c)/p = k / eps
    assert r["loss_ramsey"] < r["loss_uniform"]


def test_averch_johnson_and_monopsony():
    aj = pr.averch_johnson(2.0, 0.3, 0.4, 10.0, 1.0, 1.0, 1.4)
    assert aj["free"]["ratio"] == pytest.approx(aj["efficient_ratio"], rel=1e-4)
    assert aj["regulated"]["ratio"] > 1.2 * aj["efficient_ratio"]
    m = pr.monopsony(5.0, 0.1, 25.0, 18.0)
    assert m["monopsony"]["L"] == pytest.approx(100) and m["monopsony"]["w"] == pytest.approx(15)
    assert m["minimum"]["L"] > m["monopsony"]["L"] and m["minimum"]["w"] > m["monopsony"]["w"]


def test_littlewood_rule_matches_simulation():
    lw = pr.littlewood(40, 4.0, 10.0, 12, 5)
    assert abs(lw["protect_rule"] - lw["protect_best"]) <= 1
    assert lw["revenue_rule"] > lw["revenue_none"]


def test_personalized_pricing_learns_and_pays():
    r = pr.personalized(n_train=8000, n_test=50_000)
    # the logit recovers the true model's coefficients: features beta / scale, log price -1 / scale
    assert r["coef"][-1] == pytest.approx(r["true"]["price"], rel=0.1)
    assert r["coef"][1] == pytest.approx(r["true"]["beta"][0] / 0.35, rel=0.15)
    # personal prices earn more than the best single price, and never more than taking every buyer's value
    assert r["personal"]["profit"] > r["uniform"]["profit"]
    assert r["personal"]["total"] <= r["first_degree"]["total"] + 1e-12
    assert r["first_degree"]["cs"] == 0.0
