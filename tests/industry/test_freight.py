"""The Works' freight: lanes, the trucking cycle, rail density and the delivery route."""

import numpy as np

from explainer.industry.works.freight import Lane, Market, Railway, Route, Truck, lanes


def test_truck_and_lane():
    t = Truck()
    assert abs(t.per_mile() - (2.05 + 3.65 / 6.5)) < 1e-12
    L = Lane()
    empty, back = L.trip(take_back=False), L.trip(take_back=True)
    assert empty["empty_share"] == 0.5 and back["empty_share"] < 0.5
    # a backhaul below cost still beats driving home empty
    assert L.back < t.per_mile() and back["profit"] > empty["profit"]
    assert abs(L.breakeven_head(False) - 2 * t.per_mile()) < 1e-9
    assert L.breakeven_head(True) < L.breakeven_head(False)
    assert abs(L.needed(0.5) - 2 * t.per_mile()) < 1e-9 and L.needed(0.139) < L.head * 1.1


def test_market_cycle():
    M = Market().path()
    r = M["rate"]
    peak, trough = int(r.argmax()), int(r.argmin())
    assert Market().boom_start <= peak < trough            # the bust follows the boom
    assert r.max() > 1.3 * Market().cost and r.min() < 0.8 * Market().cost
    slow = Market(entry=12).path()["rate"]
    assert slow.max() >= r.max() - 1e-9                    # slower entry, higher peak


def test_railway_density():
    R = Railway()
    d = R.density()
    assert abs(R.avg_cost(d) - R.opex / R.rtm) < 1e-12      # calibrated: average cost at UP's density
    assert R.avg_cost(1e6) > R.rate > R.avg_cost(d)
    assert abs(R.avg_cost(R.breakeven_density()) - R.rate) < 1e-12


def test_route_and_hubs():
    Ro = Route()
    c = Ro.per_package(np.array([0.05, 0.5, 5.0]))
    assert c[0] < c[1] < c[2]
    assert lanes(10) == dict(direct=90, hub=18)
