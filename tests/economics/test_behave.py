"""Agora's behavioural economics (Part 45): the gym, reference dependence, present bias, inattention, social
preferences, a filtered literature and forecasters."""

import numpy as np
import pytest

from explainer.economics.agora import behave as B


def test_gym_contract_prices_visits_below_cost():
    for beta_hat in (0.5, 1.0):
        mono = B.gym_contract(0.5, beta_hat, 20, 60, 30, m=2.0)
        comp = B.gym_contract(0.5, beta_hat, 20, 60, 30, m=2.0, competitive=True)
        assert mono["p"] == pytest.approx(2.0 - 0.5 * 20, abs=1e-5)
        assert comp["p"] == pytest.approx(mono["p"], abs=1e-5)
        assert comp["profit"] == pytest.approx(0.0, abs=1e-6)
    naive = B.gym_contract(0.5, 1.0, 20, 60, 30, m=2.0)
    soph = B.gym_contract(0.5, 0.5, 20, 60, 30, m=2.0)
    assert naive["F"] > soph["F"] and naive["realized_surplus"] < 0 < naive["perceived_surplus"] + 1e-9


def test_island_gym_pays_more_per_visit_than_the_pass():
    g = B.island_gym(n=1500)
    assert g["monthly_forecast"] > 2 * g["monthly_visits"]
    assert g["price_per_visit"] > g["per_visit"]
    assert g["monthly_naive_share"] > 0.9


def test_endowment_effect_halves_trade():
    plain = B.mug_market(lam_goods=1.0, reps=400)
    loss = B.mug_market(lam_goods=2.0, reps=400)
    assert plain["share_traded"] == pytest.approx(0.5, abs=0.03)
    assert loss["share_traded"] < 0.3 and loss["ratio"] == pytest.approx(2.0, rel=0.1)
    exp = B.experienced_traders(reps=200)
    assert exp["share_traded"][-1] > exp["share_traded"][0] + 0.15


def test_marathon_bunches_below_round_times():
    M = B.marathon(n=200_000)
    r = B.bunching_at(M["T"], 240.0)
    assert r["excess"] > 1.0 and r["missing"] > 1.0
    assert M["share_bunched"] > 0.05


def test_golf_distance_confounds_the_raw_gap():
    G = B.golf(n=150_000)
    assert G["raw"] > 5 * G["effect"]
    assert G["within"] == pytest.approx(G["effect"], abs=0.01)


def test_condo_regressions_bracket_the_loss_coefficient():
    for s in range(3):
        c = B.condos(seed=s)
        assert c["lower"] < c["m"] < c["upper"]
    assert c["weeks_losers"] > c["weeks_gainers"]


def test_odonoghue_rabin_examples():
    assert B.odr([3, 5, 8, 13], 0.5, "cost") == {"tc": 1, "naif": 4, "soph": 2, "values": [3.0, 5.0, 8.0, 13.0],
                                                 "beta": 0.5, "kind": "cost"}
    r = B.odr([3, 5, 8, 13], 0.5, "reward")
    assert (r["tc"], r["naif"], r["soph"]) == (4, 3, 1)


def test_defaults_stick_for_naifs_only():
    opt_in = B.enrolment(default=0.0, naive=True, cost_mean=300, months=12)
    auto = B.enrolment(default=0.03, naive=True, cost_mean=300, months=12)
    tc_in = B.enrolment(default=0.0, naive=False, cost_mean=300, months=12)
    tc_auto = B.enrolment(default=0.03, naive=False, cost_mean=300, months=12)
    assert auto["final_participation"] > opt_in["final_participation"] + 0.2
    assert abs(tc_auto["final_participation"] - tc_in["final_participation"]) < 0.02


def test_commitment_takers_are_the_present_biased():
    t = B.commitment_trial()
    assert 0.2 < t["take_up"] < 0.5 and t["itt"] > 0
    assert t["tot"] == pytest.approx(t["itt"] / t["take_up"])
    assert t["beta_takers"] < t["beta_others"]


def test_left_digit_bias_recovered():
    u = B.used_cars(theta=0.25)
    assert u["theta_hat"] == pytest.approx(0.25, abs=0.04)
    assert u["jump"] > 0


def test_rational_inattention_and_sparsity():
    xs = np.linspace(-1, 1, 21)
    U = np.column_stack([np.zeros(21), xs])
    prior = np.ones(21) / 21
    cheap, dear = B.ri_choice(prior, U, 0.05), B.ri_choice(prior, U, 1.0)
    assert cheap["info"] > dear["info"]
    assert cheap["cond"][-1, 1] > dear["cond"][-1, 1]
    skew = B.ri_choice(np.r_[np.full(15, 0.9 / 15), np.full(6, 0.1 / 6)], U, 2.0)
    assert skew["pa"].min() < 1e-6          # a rationally inattentive chooser can ignore an option altogether
    assert np.allclose(B.sparse_weights([4, 1, 0.5], 0.6), [0.85, 0.4, 0.0])


def test_fehr_schmidt_ultimatum_and_shrouding():
    u = B.ultimatum([1.0], [0.6, 0.2])
    assert u["thresholds"][0] == pytest.approx(1 / 3)
    assert u["offers"][0] == pytest.approx(0.5) and u["offers"][1] == pytest.approx(1 / 3, abs=0.01)
    s = B.shrouded()
    assert s["base_price"] < 20 and s["myope_pays"] > s["soph_pays"]


def test_selection_model_corrects_a_filtered_literature():
    L = B.nudge_literature(k=3000, n_lo=300, n_hi=8000, seed=2)
    pub = np.array(L["published"])
    r = B.selection_mle(np.array(L["x"])[pub], np.array(L["se"])[pub])
    assert L["mean_published"] > 1.5 * L["mu"]
    assert abs(r["mu"] - L["mu"]) < 0.5 * abs(r["naive"] - L["mu"])


def test_forecasters_over_and_under_react():
    rational = B.forecasters(theta=0.0, T=600)
    diag = B.forecasters(theta=0.6, T=600)
    assert abs(rational["individual"]) < 0.1 and rational["consensus"] > 0.3
    assert diag["individual"] < -0.2


def test_welfare_range():
    assert B.welfare_range({"a": 30, "b": 80}, 20)["verdict"] == "improves"
    assert B.welfare_range({"a": 30, "b": 80}, 50)["verdict"] == "ambiguous"
