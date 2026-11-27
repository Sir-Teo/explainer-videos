"""The Works' power system (Part 13)."""

import numpy as np

from explainer.industry.works import power


def test_load_factor_and_insull():
    # Insull's block, 1910: 33,000 kWh a year; customers' own peaks 68.5 kW; the transformer's peak 20 kW
    assert abs(33000 / (68.5 * 8760) - 0.055) < 0.001
    assert abs(33000 / (20 * 8760) - 0.19) < 0.005
    assert power.load_factor([1, 1, 1, 1]) == 1.0
    assert abs(power.load_factor([0, 0, 0, 4]) - 0.25) < 1e-12
    assert abs(power.diversity([2, 2, 2], 3) - 2.0) < 1e-12


def test_screening_curve():
    peaker = power.Tech("peaker", 1158, 7.18, 4.17, 9142, fuel=3.5)
    ccgt = power.Tech("ccgt", 1032, 12.69, 3.57, 6226, fuel=3.5)
    nuke = power.Tech("nuclear", 8255, 163.40, 2.62, 10445, life=40)
    # fixed cost ranks nuclear > peaker ~ ccgt; running cost peaker > ccgt > nuclear
    assert nuke.fixed() > ccgt.fixed() and peaker.running() > ccgt.running() > nuke.running()
    x = power.crossover(peaker, ccgt)
    assert x is not None and x < 0.2           # on EIA's 2025 costs a combined cycle beats a frame turbine at any use
    y = power.crossover(ccgt, nuke)
    assert y is None or y > 1.0                  # at $3.50 gas, nuclear never beats a combined cycle on cost
    assert abs(power.annuity(0.07, 30) - 0.0806) < 1e-3


def test_dispatch_and_cap():
    units = [power.Unit("wind", 30, 0), power.Unit("nuclear", 5, 10), power.Unit("gas", 40, 35), power.Unit("peaker", 10, 120)]
    assert power.dispatch(units, 50)["price"] == 35
    assert power.dispatch(units, 80)["price"] == 120
    r = power.dispatch(units, 90)
    assert r["price"] == 9000 and abs(r["shed"] - 5) < 1e-9
    r = power.dispatch(units, 60, available={"wind": 0.2, "gas": 0.5})
    assert r["price"] == 9000 and r["shed"] > 0


def test_rate_case():
    u = power.Utility(rate_base=10000, roe=0.10, equity=0.5, debt_cost=0.05)
    rq = u.requirement()
    assert abs(u.wacc() - 0.075) < 1e-12
    assert abs(rq["return"] - 750) < 1e-9
    assert rq["total"] > rq["return"] + rq["om"]
    # a higher allowed return raises the price
    assert power.Utility(rate_base=10000, roe=0.11).requirement()["cents"] > power.Utility(rate_base=10000, roe=0.10).requirement()["cents"]


def test_run_it_week():
    out = power.run_it()
    assert out["spot, runs"]["total"] > out["hedged, runs"]["total"]
    assert out["hedged, freezes"]["total"] < 0 < out["spot, runs"]["total"]
    assert out["hedged, freezes"]["total"] < out["spot, freezes"]["total"]


def test_battery_and_retailer():
    p = np.array([10] * 6 + [50] * 12 + [200] * 4 + [20] * 2, dtype=float)
    b = power.battery(np.tile(p, 2), mw=100, hours=4, efficiency=0.9)
    assert b["profit"] > 0 and len(b["charge"]) == len(b["discharge"]) == 8
    r = power.retailer([50, 50, 300], fixed_price=80, hedge=0.0, hedge_price=0)
    assert r["margin"][-1] < 0
    r2 = power.retailer([50, 50, 300], fixed_price=80, hedge=1.0, hedge_price=55)
    assert min(r2["margin"]) > 0
