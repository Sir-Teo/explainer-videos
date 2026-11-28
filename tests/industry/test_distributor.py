"""The Works' distributor and delivery route (Part 33)."""

import pytest

from explainer.industry.works.distributor import Distributor, Route, margin_turns


def test_base_year_runs_on_other_peoples_money():
    y = Distributor().year()
    assert y["capital"] < 0 and y["payables"] > y["inventory"] + y["receivables"]
    assert 0.01 < y["margin"] < 0.02
    assert y["profit"] == pytest.approx(y["op"] - y["charge"])


def test_service_has_an_interior_best():
    d = Distributor()
    best = d.best_z()
    assert 0.98 < d.fill(best) < 0.995
    assert d.year(best)["profit"] > d.year(1.0)["profit"] and d.year(best)["profit"] > d.year(3.5)["profit"]
    assert d.stock_days(3.0) > d.stock_days(2.0) > d.stock_days(0.0) == pytest.approx(7.0)


def test_holding_stock_beats_drop_shipping():
    d = Distributor()
    assert d.year()["profit"] > d.drop_ship()["profit"] and d.drop_ship()["inventory"] == 0.0


def test_density_cuts_the_cost_of_a_stop():
    r = Route()
    assert r.stops(0.4) > r.stops(0.1) and r.cost_per_stop(0.4) < r.cost_per_stop(0.1)
    assert margin_turns(0.015, 10) == pytest.approx(0.15)
