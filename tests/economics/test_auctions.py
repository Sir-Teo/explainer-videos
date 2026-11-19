"""Agora's auction house (Part 16)."""

import numpy as np
import pytest

from explainer.economics.agora import auctions as au


def test_first_price_bid_shades_and_risk_aversion_raises_it():
    assert au.first_price_bid(0.8, 4) == pytest.approx(0.6)
    assert au.first_price_bid(0.8, 4, alpha=0.5) > au.first_price_bid(0.8, 4)
    # with a reserve, the lowest serious bidder bids the reserve
    assert au.first_price_bid(0.5, 2, reserve=0.5) == pytest.approx(0.5)


def test_revenue_equivalence_in_simulation():
    s = au.simulate_formats(n=4, draws=200000, seed=1)
    th = s["theory"]
    for name in ("first-price", "second-price", "all-pay"):
        f = s["formats"][name]
        assert abs(f["mean"] - th) < 4 * f["se"] + 1e-3


def test_myerson_reserve_is_a_half_and_raises_revenue():
    m = au.myerson(n=2)
    assert m["r_star"] == pytest.approx(0.5)
    assert m["rev_star"] == pytest.approx(5 / 12) and m["rev_zero"] == pytest.approx(1 / 3)


def test_winners_curse_grows_with_bidders():
    w = au.winners_curse(ns=(2, 8, 32), noise=3.0, draws=100000, seed=3)
    over = [r["overestimate"] for r in w["rows"]]
    assert over[0] < over[1] < over[2]
    for r in w["rows"]:
        assert r["overestimate"] == pytest.approx(r["exact"], abs=0.03)


def test_gsp_equilibrium_matches_vcg_and_truth_is_not_an_equilibrium():
    g = au.gsp((10, 8, 6, 4), (200, 120, 60))
    # VCG totals: slot 1 pays (200-120)*8 + (120-60)*6 + 60*4 = 640 + 360 + 240
    assert g["vcg_total"][0] == pytest.approx(1240)
    assert g["gsp_price_per_click"][0] == pytest.approx(6.2)
    # if the others bid their values, the top bidder earns 400 in slot 1 but 480 by dropping to slot 2
    assert g["deviation_profits_top"][:2] == pytest.approx([400, 480]) and g["best_slot_for_top_if_truthful"] == 1


def test_exposure_problem():
    win = au.exposure(10, 1, (4, 4))
    assert win["efficient"] == "national" and win["bold"]["national_profit"] == pytest.approx(2)
    assert win["cautious"]["welfare"] < win["efficient_welfare"]
    lose = au.exposure(10, 1, (2, 9))
    assert lose["efficient"] == "locals" and lose["bold"]["national_profit"] < 0


def test_demand_reduction_pays_under_a_uniform_price():
    m = au.multi_unit(supply=2, big=(10.0, 10.0), small=6.0)
    truthful, best = m["truthful"], m["best"]
    assert truthful["big_units"] == 2 and truthful["price"] == 6.0 and truthful["big_profit"] == 8.0
    assert best["k"] == 1 and best["big_profit"] == 10.0 and best["revenue"] == 0.0
    assert best["surplus"] < truthful["surplus"]
    v = m["vickrey"]
    assert v["big_units"] == 2 and v["big_pays"] == 6.0 and v["big_profit"] == 14.0


def test_play_it_curves_peak_at_the_equilibrium_and_pay_the_same():
    e = au.expected_profit(70.0, 3, 100.0)
    assert abs(e["grid_best_first"] - 52.5) < 0.3 and abs(e["grid_best_second"] - 70.0) < 0.3
    assert abs(e["profit_first"] - e["profit_second"]) < 1e-9          # payoff equivalence


def test_clock_price_is_the_second_highest_value():
    c = au.clock([0.3, 0.8, 0.55, 0.7])
    assert c["winner"] == 1 and abs(c["price"] - 0.7) < 1e-9
