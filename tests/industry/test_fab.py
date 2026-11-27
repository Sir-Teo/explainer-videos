"""The Works' fab (Part 15): dies, yield, utilization and the build-or-book choice."""

import math

from explainer.industry.works import fab


def test_dies_and_yield():
    assert 630 < fab.dies_per_wafer(100) < 650           # a 1 cm2 die on a 300 mm wafer
    assert fab.dies_per_wafer(800) < fab.dies_per_wafer(100) / 8
    assert abs(fab.yield_poisson(100, 0.1) - math.exp(-0.1)) < 1e-12
    assert fab.yield_poisson(800, 0.1) < fab.yield_poisson(100, 0.1)  # big dies yield worse
    assert fab.learning(0.5, 0.1, 0, 1000) == 0.5 and abs(fab.learning(0.5, 0.1, 1000, 1000) - 0.3) < 1e-12


def test_utilization_and_run_it():
    f = fab.Fab()
    assert f.cost_per_wafer(5_000) > f.cost_per_wafer(20_000) > f.cost_per_wafer(50_000)
    g = fab.run_it()
    assert g[(5_000, False)]["profit"] > 0 > g[(5_000, True)]["profit"]       # a small designer should book a foundry
    assert g[(20_000, False)]["profit"] > g[(20_000, True)]["profit"]
    assert g[(50_000, True)]["profit"] > g[(50_000, False)]["profit"]         # only a full fab pays for itself
