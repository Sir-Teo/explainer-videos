"""Agora's platform (Part 61): the Island's ride-hailing app and marketplace, checked against definitions, closed
forms and the truths the simulations plant."""

import numpy as np
import pytest
from scipy import stats

from explainer.economics.agora import platform as PL


def test_surge_clears_the_market_and_completes_more_rides():
    on, off = PL.surge_night(True), PL.surge_night(False)
    assert on["rate_peak"] == pytest.approx(1.0)
    assert off["rate_peak"] < 0.4
    assert max(on["m"]) > 1.5 and max(off["m"]) == 1.0
    # with surge off, completed trips never exceed the drivers on the road
    assert all(d <= s + 1e-9 for d, s in zip(off["done"], off["drivers"]))


def test_surge_surplus_recovers_the_planted_demand_curve():
    S = PL.surge_surplus()
    assert S["mu_hat"] == pytest.approx(S["mu"], rel=0.05)
    assert S["elasticity_at_base"] == pytest.approx(-15 / 25, abs=0.05)


def test_commission_equilibrium_is_consistent_and_interior():
    m = PL.commission_market(0.25)
    P = PL.COMMISSION
    u = m["trips"] / (m["drivers"] * P["cap"])
    wait = P["w_min"] + P["w_k"] * u / (1 - u)
    assert m["wait"] == pytest.approx(wait)
    ride = 1 / (1 + np.exp(-(P["a_r"] - P["b_r"] * P["fare"] - P["w_r"] * wait)))
    assert m["trips"] == pytest.approx(P["riders"] * ride, rel=1e-6)
    drive = 1 / (1 + np.exp(-((1 - 0.25) * P["fare"] * m["trips"] / m["drivers"] - P["w0"]) / P["s_d"]))
    assert m["drivers"] == pytest.approx(P["drivers"] * drive, rel=1e-6)
    C = PL.commission()
    assert 0.15 < C["best_c"] < 0.45
    assert np.all(np.diff(C["trips"]) < 0)
    # the platform's optimum: the elasticity of trips with respect to the commission is -1 there
    c0 = C["best_c"]
    lo, hi = PL.commission_market(c0 - 0.005), PL.commission_market(c0 + 0.005)
    el = (np.log(hi["trips"]) - np.log(lo["trips"])) / (np.log(c0 + 0.005) - np.log(c0 - 0.005))
    assert el == pytest.approx(-1.0, abs=0.1)


def test_ranking_and_sponsored_slot():
    R = PL.ranking()
    assert R["examine"][0] == 1.0 and np.all(np.diff(R["examine"]) < 0)
    assert R["total_sponsored"] < R["total"] and R["quality_sponsored"] < R["quality"]


def test_reputation_effective_percent_positive_tracks_quality_better():
    R = PL.reputation()
    assert R["pp_median"] > 0.97
    assert R["corr_epp"] > R["corr_pp"]


def test_gsp_prices_are_the_least_bids_that_keep_each_slot():
    G = PL.gsp()
    b, q = np.array([4.0, 3.0, 2.5, 1.0]), np.array([0.5, 1.0, 0.7, 0.9])
    Q = G["quality"]
    assert Q["order"] == [1, 0, 2]
    for k, i in enumerate(Q["order"]):
        nxt = [1, 0, 2, 3][k + 1]
        assert Q["prices"][k] == pytest.approx(b[nxt] * q[nxt] / q[i])
        assert Q["prices"][k] <= b[i]
    assert Q["revenue"] > G["bid only"]["revenue"]
    assert PL.gsp(reserve=1.5)["quality"]["prices"][-1] == pytest.approx(1.5)


def test_search_ads_attribution_misleads_and_the_experiment_does_not():
    A = PL.search_ads(reps=60)
    assert A["true_roi"] < 0 < A["attributed_roi"]
    assert A["ols_roi"] > 5
    assert abs(A["experiment_roi"] - A["true_roi"]) < 3 * A["experiment_sd"] / np.sqrt(60)


def test_ad_power_matches_the_two_sample_formula():
    P = PL.ad_power()
    z = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)
    assert P["n_detect_effect"] == pytest.approx(2 * z ** 2 * 75.0 ** 2 / 0.125 ** 2)


def test_peeking_inflates_false_positives():
    P = PL.peeking(reps=1500)
    assert P["last"] == pytest.approx(0.05, abs=0.02)
    assert P["ever"] > 3 * P["last"]


def test_cuped_cuts_variance_by_one_minus_rho_squared():
    C = PL.cuped(reps=600)
    assert C["ratio"] == pytest.approx(1 - 0.7 ** 2, abs=0.08)


def test_interference_inflates_the_user_level_test():
    S = PL.switchback(reps=100)
    assert S["user"] > 2 * S["truth"]
    assert abs(S["switchback"] - S["truth"]) < 4 * S["switchback_sd"]
    assert abs(S["city"] - S["truth"]) < 4 * S["city_sd"]


def test_uplift_targeting_beats_targeting_likely_buyers():
    g = PL.uplift()["gains"]
    assert g["true effect"] >= g["estimated effect"] > g["at random"] > g["likeliest buyers"]


def test_surrogate_index_recovers_the_long_run_sign():
    L = PL.long_term()
    assert L["short"] > 0.2 and L["truth"] < 0
    assert abs(L["surrogate"] - L["truth"]) < 4 * L["surrogate_se"] + 0.01


def test_flexibility_is_worth_more_than_a_fixed_shift():
    F = PL.flexibility()
    assert F["flex"] > 2 * F["fixed"]


def test_wta_survey_recovers_the_median():
    W = PL.wta_survey()
    assert W["median_hat"] == pytest.approx(W["median"], rel=0.15)
