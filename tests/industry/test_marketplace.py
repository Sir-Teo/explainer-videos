"""The Works' marketplace and direct brand (Part 32)."""

import pytest

from explainer.industry.works.marketplace import Brand, Marketplace, cost_per_order


def test_baseline_settles():
    s = Marketplace().solve()
    assert 30e9 < s["gmv"] < 45e9 and s["profit"] > 0
    assert s["revenue"] == pytest.approx(s["fees"] + s["ads"])
    assert s["seller_keep"] == pytest.approx(0.55 - 0.30 - 0.06)


def test_take_rate_has_an_interior_best():
    m = Marketplace()
    prof = {t: m.with_(take=t).solve()["profit"] for t in (0.15, 0.30, 0.45)}
    assert prof[0.30] > prof[0.15] and prof[0.30] > prof[0.45]
    sellers = [m.with_(take=t).solve()["sellers"] for t in (0.15, 0.30, 0.45)]
    assert sellers[0] > sellers[1] > sellers[2]


def test_ads_crowd_out_buyers():
    m = Marketplace()
    lo, hi = m.with_(ad=0.0).solve(), m.with_(ad=0.12).solve()
    assert lo["buyers"] > hi["buyers"] and lo["gmv"] > hi["gmv"]


def test_speed_is_a_fixed_cost_game():
    assert cost_per_order(4e9, 1) < cost_per_order(1e9, 1)
    small = Marketplace().with_(days=1).solve()["cost_per_order"]
    big = Marketplace(buyers_max=400e6, sellers_max=4e6).with_(days=1).solve()["cost_per_order"]
    assert big < small


def test_brand_payback():
    b = Brand()
    assert b.payback_year() == 2
    assert b.lifetime() == pytest.approx(b.cumulative(200)[-1], abs=1e-6)
    assert b.with_(cac=120).payback_year() is None
