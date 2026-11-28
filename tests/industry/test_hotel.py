"""The Works' hotel and roulette table (Part 35)."""

import doctest

from explainer.industry.works import hotel as H


def test_doctest():
    assert doctest.testmod(H).failed == 0


def test_hotel_year_adds_up():
    h = H.Hotel()
    y = h.year(180.0)
    assert abs(y["revpar"] - y["occupancy"] * y["adr"]) < 1e-6
    assert 0.6 < y["occupancy"] < 0.8 and 0.2 < y["margin"] < 0.4
    parts = y["room_rev"] + y["other_rev"] * h.other_margin - y["dist"] - y["fees"] - y["var"] - y["fixed"]
    assert abs(parts - y["ebitda"]) < 1e-3


def test_revenue_management_and_brand():
    h = H.Hotel()
    flat, monthly = h.best_flat(), h.best_monthly()
    assert monthly["ebitda"] >= flat["ebitda"]
    assert max(monthly["rates"]) > min(monthly["rates"])
    indep = h.with_(branded=False).best_monthly()
    assert indep["fees"] == 0 and indep["dist"] > monthly["dist"]
    assert monthly["ebitda"] > indep["ebitda"]
    assert h.with_(branded=False, lift=0.0).best_monthly()["ebitda"] > monthly["ebitda"]


def test_flow_through_and_roulette():
    f = H.flow_through(H.Hotel(), 180.0)
    assert f["from_rate"] > f["from_rooms"] > 0
    r = H.roulette(players=4000, seed=1)
    assert 0.08 < r["hold"] < 0.16 and r["win_share"] < 0.5
    assert abs(r["house"] - r["expected"]) / r["expected"] < 0.3
