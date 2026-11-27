import numpy as np
import pytest

from explainer.industry.works import farm


def test_units():
    assert farm.BU_PER_T["corn"] == pytest.approx(39.368, rel=1e-3)
    assert farm.per_bushel(farm.BU_PER_T["wheat"], "wheat") == pytest.approx(1.0)


def test_acre():
    a = farm.Acre("corn", 200, 450, 450, land=190)
    assert a.net(4.5) == pytest.approx(0)
    assert a.breakeven_price() == pytest.approx(4.5)
    assert a.breakeven_price(operating_only=True) == pytest.approx(2.25)
    assert a.land_residual(4.5) == pytest.approx(190)


def test_sell():
    # no hedge, no storage: everything at harvest
    assert farm.sell(160, 150, 5, 6, 7) == pytest.approx(900)
    # a full hedge with a normal crop locks the planting price on the expected bushels
    assert farm.sell(150, 150, 5, 6, 7, hedge=1.0) == pytest.approx(750)
    # a drought: the shortfall must be bought back at harvest
    assert farm.sell(160, 118, 5.8, 6.79, 6.3, hedge=1.0) == pytest.approx(160 * 5.8 - 42 * 6.79)
    # storage pays the later price less the carrying cost
    assert farm.sell(100, 100, 3, 3, 4, store=1.0, months=8, carry=0.04) == pytest.approx(100 * (4 - 0.32))


def test_treadmill():
    t = farm.treadmill()
    assert t["share"][0] < 0.05 and t["share"][-1] > 0.95
    assert np.all(np.diff(t["price"]) < 0)
    assert t["adopter"][0] > t["laggard"][0]
    assert t["adopter"][-1] < t["adopter"][0]          # the early gain is competed away
    assert t["laggard"][-1] < 0                         # and those who never adopt lose money


def test_ladder():
    lad = farm.margin_ladder({"a": (10, 1), "b": (100, 2), "c": (5, -1)})
    assert [x[0] for x in lad] == ["c", "b", "a"]
