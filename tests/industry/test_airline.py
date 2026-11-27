"""The Works' airline (Part 28): one flight, two fares, Littlewood's rule and overbooking."""

from explainer.industry.works import airline as A


def test_first_come_low_fare_fills_the_plane_and_loses_money():
    f = A.Flight()
    r = f.sell(protect=0)
    assert r["sold"] > 0.99 * f.seats
    assert r["turned_away"] > 0.8 * f.business
    assert r["profit"] < 0


def test_littlewood_protection_is_the_best_protection_level():
    f = A.Flight()
    y = f.littlewood()
    sw = f.sweep_protect(step=1, top=70)
    best = max(sw, key=sw.get)
    assert abs(best - y) <= 2
    assert f.sell(protect=y)["profit"] > 0


def test_overbooking_pays_up_to_a_point():
    f = A.Flight()
    so = f.sweep_oversell(top=30)
    best = max(so, key=so.get)
    assert 0 < best < 30
    assert so[best] > so[0] and so[30] < so[best]


def test_breakeven_load():
    assert abs(A.breakeven_load(200.0, 0.16, 1000.0) - 0.8) < 1e-9
