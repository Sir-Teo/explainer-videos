"""Agora's appraisal module (Part 58): the bridge, values without prices, scoring, microsimulation, general
equilibrium, risk and CBO's record."""

import numpy as np
import pytest

from explainer.economics.agora import appraisal as A


def test_rule_of_a_half_is_the_area_under_linear_demand():
    y = A.bridge_year()
    g = np.linspace(y["g1"], y["g0"], 20001)
    q = A.BRIDGE["a"] - A.BRIDGE["b"] * g
    area = np.sum((q[1:] + q[:-1]) / 2 * np.diff(g))
    assert y["surplus"] == pytest.approx(area, rel=1e-6)
    # fares saved and Bo's lost profit net to the ferry's running costs
    assert y["fares"] + y["Bo's profit"] == pytest.approx(A.BRIDGE["ferry_unit_cost"] * y["q0"] +
                                                         A.BRIDGE["ferry_fixed"])


def test_npv_falls_with_the_rate_and_irr_is_its_root():
    r = np.linspace(0.0, 0.1, 21)
    v = A.npv_curve(None, r)
    assert np.all(np.diff(v) < 0)
    assert A.npv_at(None, A.irr()) == pytest.approx(0.0, abs=1e-6)
    assert A.appraise(rate=0.03)["npv"] > 0 > A.appraise(rate=0.07)["npv"]


def test_green_book_schedule_and_weitzman():
    df = A.discount_factors(200, schedule=A.GREEN_BOOK_2003)
    assert df[30] == pytest.approx(1.035 ** -30)
    assert df[31] == pytest.approx(df[30] / 1.03)
    W = A.weitzman([0.01, 0.07], [0.5, 0.5], [50, 200])
    assert W["rate"][0] == pytest.approx(0.0230, abs=2e-4) and W["rate"][1] == pytest.approx(0.0135, abs=2e-4)
    assert W["forward"][1] == pytest.approx(0.01, abs=1e-4)
    assert A.stpr() == pytest.approx(3.5)


def test_hedonic_and_wage_risk_biases():
    H = A.hedonic_houses()
    assert H["naive"] > 0 > H["full"] and abs(H["full"] - H["truth"]) < 3 * H["full_se"]
    V = A.wage_risk()
    assert V["naive"] < V["noisy"] < V["controls"] and abs(V["controls"] - V["truth"]) < 3 * V["controls_se"]


def test_score_top_rate_matches_saez():
    T = A.taxpayers()
    assert np.sum(T["w"] * T["z"]) == pytest.approx(T["pop_total"], rel=0.02)
    s = A.score_top_rate(T)
    assert 0 < s["behavioural"] < s["static"]
    assert s["ratio"] == pytest.approx(s["formula"], abs=0.04)


def test_dynamic_toy_costs_more_than_conventional():
    D = A.dynamic_score()
    assert D["sum_growth"] < 0 < D["sum_rates"] and D["sum_dynamic"] > D["sum_conventional"]


def test_distribution_table_and_cost():
    H = A.households()
    base = A.net_income(H)
    t = A.distribution_table(H, base, A.net_income(H, A.with_allowance(A.SCHEDULE, 18000.0)))
    assert t["rows"][0]["gain"] == pytest.approx(0.0, abs=1.0) and t["cost"] > 0
    t2 = A.distribution_table(H, base, A.net_income(H, A.reform_schedule()))
    assert t2["rows"][-1]["pct"] < 0 < t2["rows"][4]["pct"] and t2["cost"] < t["cost"]


def test_cge_balances_and_loss_is_second_order():
    eq = A.cge(0.1)
    S = A.sam(eq)
    assert S["balanced"]
    w1, w2 = A.cge_welfare(0.05)["dwl"], A.cge_welfare(0.10)["dwl"]
    assert 3.5 < w2 / w1 < 4.5                           # the loss grows with the square of the tax
    h = A.harberger_check(0.02)
    assert h["ratio"] == pytest.approx(1.0, abs=0.15)


def test_reference_class_monte_carlo_and_option():
    M = A.monte_carlo()
    assert M["mean"] < M["forecast"] and 0.3 < M["p_negative"] < 0.9
    W = A.wait_option()
    assert W["value"] > 0 and W["build_if_wait"]["high"] and not W["build_if_wait"]["low"]


def test_cbo_record_reproduces_cbo():
    R = A.cbo_record()
    for h in R["horizon"]:
        s = R["stats"][("deficit", h["year"])]
        assert h["mae"] == pytest.approx(s["mae"], abs=0.051)
        assert h["n"] == s["n"]


def test_target_gaming_moves_the_share_not_the_median():
    g = A.target_gaming()
    assert g["within_after"] > g["within_before"] + 0.05
    assert g["median_after"] == pytest.approx(g["median_before"])
    assert g["spike_after"] > 3 * g["spike_before"]
