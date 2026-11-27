"""The Works' shipping market (Part 27): the cycle, the owner's two rules and slow steaming."""

import numpy as np

from explainer.industry.works import ship


def test_earnings_are_convex_in_utilization():
    m = ship.Market()
    assert m.earnings(0.7) == m.floor
    assert m.earnings(1.0) == m.top
    assert m.earnings(0.95) - m.earnings(0.9) > m.earnings(0.9) - m.earnings(0.85)


def test_orders_follow_earnings_and_arrive_late():
    m = ship.Market()
    P = m.path()
    boom = int(np.argmax(P["orders"]))
    assert P["earn"][boom] >= m.breakeven
    # what is ordered in a boom arrives into lower earnings
    later = boom + m.lag
    if later < len(P["earn"]):
        assert P["earn"][later] < P["earn"][boom]


def test_ordering_against_the_market_beats_following_it():
    m = ship.Market()
    f, a = m.owner("follow"), m.owner("against")
    assert a["ret"] > f["ret"]
    assert a["avg_price"] < f["avg_price"]
    assert all(s["delivery"] == s["order"] + m.lag for s in f["ships"] + a["ships"])


def test_slow_steaming_pays_when_fuel_is_dear():
    v = [ship.best_speed(p) for p in (300, 600, 900)]
    assert v[0] > v[1] > v[2]
    fast, slow = ship.voyage(speed=20), ship.voyage(speed=16)
    assert slow["fuel_t"] / fast["fuel_t"] < 0.66 and slow["days"] > fast["days"]
