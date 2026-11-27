"""The Works' season (Part 23): the newsvendor's buy, early and far, late and near, or a base and a chase."""

import math

import numpy as np
from scipy.stats import norm

from explainer.industry.works import fashion as F


def test_the_lognormal_demand_has_the_stated_mean_and_error():
    s = F.Season()
    sf, sn, s1 = s.sigmas()
    assert math.isclose(math.exp(s.mu0() + sf ** 2 / 2), s.mean, rel_tol=1e-12)
    assert math.isclose(math.sqrt(math.exp(sf ** 2) - 1), s.cv_far, rel_tol=1e-12)
    assert math.isclose(s1 ** 2 + sn ** 2, sf ** 2, rel_tol=1e-12)


def test_expected_sales_match_a_simulation():
    s = F.Season()
    sf = s.sigmas()[0]
    rng = np.random.default_rng(23)
    d = np.exp(s.mu0() + sf * rng.standard_normal(400_000))
    for q in (50_000, 100_000, 160_000):
        assert math.isclose(float(s.sold(q, s.mu0(), sf)), float(np.minimum(d, q).mean()), rel_tol=5e-3)


def test_the_best_single_order_sits_at_the_critical_ratio():
    s = F.Season()
    sf = s.sigmas()[0]
    q = s.best(s.cost_far, s.mu0(), sf)
    assert math.isclose(norm.cdf((math.log(q) - s.mu0()) / sf), s.ratio(s.cost_far), rel_tol=1e-9)

    def profit(x):
        sold = float(s.sold(x, s.mu0(), sf))
        return s.price * sold + s.clearance * (x - sold) - s.cost_far * x

    assert profit(q) > profit(0.97 * q) and profit(q) > profit(1.03 * q)


def test_the_chase_beats_both_single_orders():
    c = F.Season().choices()
    assert c["chase"]["profit"] > max(c["far"]["profit"], c["near"]["profit"])
    assert c["far"]["cleared"] > c["chase"]["cleared"] > c["near"]["cleared"]
    assert c["far"]["lost"] > c["chase"]["lost"]
    assert 0 < c["chase"]["topped"] < 1
    for v in c.values():
        assert math.isclose(v["sold"] + v["cleared"], v["ordered"], rel_tol=1e-9)
        assert 0 < v["sell_through"] < 1


def test_a_chase_with_no_base_is_the_near_order():
    s = F.Season()
    assert math.isclose(s.chase_at(0.0)["profit"], s.near()["profit"], rel_tol=1e-9)


def test_better_forecasts_are_worth_more_to_the_early_buyer():
    a, b = F.Season(cv_far=0.4).far(), F.Season(cv_far=0.8).far()
    assert a["profit"] > b["profit"] and a["cleared"] < b["cleared"]


def test_inventory_days():
    assert math.isclose(F.inventory_days(3.249, 16.641), 71.26, rel_tol=1e-3)
