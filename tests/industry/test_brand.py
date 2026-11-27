"""The Works' brand (Part 22): a branded product against a store label, with an advertising stock that wears off."""

import math

from explainer.industry.works import brand as B


def test_the_brand_is_calibrated_to_its_target_share():
    b = B.Brand()
    assert math.isclose(b.share(b.steady_stock()), b.target, rel_tol=1e-9)
    hold = b.run([b.ads] * 8)
    assert all(math.isclose(r["share"], b.target, rel_tol=1e-9) for r in hold["rows"])


def test_cutting_the_advertising_wins_a_year_and_loses_the_decade():
    c = B.Brand().choices()
    assert c["cut"]["rows"][0]["profit"] > c["hold"]["rows"][0]["profit"]
    assert c["cut"]["npv"] < c["hold"]["npv"]
    shares = [r["share"] for r in c["cut"]["rows"]]
    assert all(a > b for a, b in zip(shares, shares[1:]))
    stocks = [r["stock"] for r in c["cut"]["rows"]]
    assert math.isclose(stocks[-1], B.Brand().steady_stock() * 0.8 ** 8)


def test_a_price_cut_wins_share_and_loses_margin():
    c = B.Brand().choices(promo_price=8.0)
    assert c["promote"]["rows"][0]["share"] > c["hold"]["rows"][0]["share"]
    assert c["promote"]["rows"][0]["profit"] < c["hold"]["rows"][0]["profit"]


def test_a_cheaper_store_label_takes_share():
    b = B.Brand()
    assert b.run([100] * 8, store_price=4.0)["rows"][-1]["share"] < b.target < b.run([100] * 8, store_price=6.0)["rows"][-1]["share"]
    assert math.isclose(B.premium(87.0, 43.362), 2.0063, rel_tol=1e-3)
