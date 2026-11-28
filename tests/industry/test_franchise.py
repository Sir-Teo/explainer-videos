"""The Works' franchised store and franchisor (Part 34)."""

import pytest

from explainer.industry.works.franchise import Franchisor, Store


def test_store_dollar_adds_up():
    y = Store().year()
    parts = y["food"] + y["labour"] + y["fees"] + y["ad"] + y["other"] + y["apps"] + y["profit"]
    assert parts == pytest.approx(y["sales"])
    assert 0.05 < y["margin"] < 0.15 and 3 < y["payback"] < 6


def test_operating_leverage_and_wages():
    s = Store()
    assert s.year(0.9 * s.sales)["margin"] < s.year()["margin"]
    assert s.with_(wage=1.2).year()["profit"] < s.year()["profit"]
    assert s.with_(delivery=0.3).year()["profit"] < s.year()["profit"]


def test_franchisor_take_has_an_interior_best():
    F = Franchisor()
    tot = {t: F.run(t)["total"] for t in (0.06, 0.128, 0.18)}
    assert tot[0.128] > tot[0.06] and tot[0.128] > tot[0.18]
    assert F.opening_rate(0.06) > F.opening_rate(0.18)
