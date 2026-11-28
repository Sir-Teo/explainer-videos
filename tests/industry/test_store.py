"""The Works' store and the retailer's float."""

from explainer.industry.works.store import Store, float_days


def test_store_year():
    S = Store()
    y = S.year()
    assert abs(y["margin"] - (S.gm - S.labour - S.occupancy - S.other)) < 1e-12
    assert 0.015 < y["margin"] < 0.03
    # the price set by competition is close to the profit-maximizing one
    assert abs(S.best_price() - 1.0) < 0.02
    # a one per cent price cut needs several per cent more volume to pay
    assert S.breakeven_volume(0.01) > 0.04
    # cutting staff looks cheap and is not
    assert S.year(s=0.8)["profit"] < y["profit"] and S.year(s=1.2)["profit"] < y["profit"]


def test_float():
    f = float_days(58.851, 63.061, 535.395)
    assert f["pay_days"] > f["inv_days"] and f["funded"] > 0
