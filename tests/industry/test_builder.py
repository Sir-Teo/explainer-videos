"""The Works' builder (Part 25): owning a lot against optioning it, and the mortgage payment."""

import math

from explainer.industry.works import builder as B


def test_owning_wins_a_boom_and_loses_a_bust():
    d = B.LandDeal()
    assert d.own("boom") > d.option("boom") > 0
    assert d.own("bust") < 0 and d.option("bust") == -d.deposit


def test_the_option_ties_up_a_tenth_of_the_money_and_earns_more_on_it():
    t = B.LandDeal().table()
    assert t["option"]["capital"] == B.LandDeal().deposit < t["own"]["capital"]
    assert t["option"]["return"] > t["own"]["return"]


def test_the_breakeven_chance_of_a_bust():
    d = B.LandDeal()
    p = d.breakeven_bust()
    e = B.LandDeal(p_bust=p)
    assert math.isclose(e.expected("own"), e.expected("option"), abs_tol=1e-9)
    assert 0 < p < 1


def test_mortgage_payment_and_balance():
    assert math.isclose(B.payment(300_000, 0.06), 1798.65, rel_tol=1e-5)
    assert math.isclose(B.payment(120_000, 0.0), 120_000 / 360)
    assert abs(B.balance(300_000, 0.06, 360)) < 1e-6
    assert B.balance(300_000, 0.06, 60) < 300_000
