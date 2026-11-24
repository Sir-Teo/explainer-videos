import numpy as np
import pytest

from explainer.industry.works import mine


def test_rock_per_tonne():
    assert mine.rock_per_tonne(1.0, 1.0, 0.0) == pytest.approx(100)
    assert mine.rock_per_tonne(0.5, 0.85, 2.0) == pytest.approx(3 / (0.005 * 0.85))
    assert mine.rock_per_tonne(0.3) > mine.rock_per_tonne(1.0)


def test_mine_output_and_cost_follow_grade():
    m = mine.Mine("model", ore_mt=600, grade=0.8, mill_mtpa=40)
    assert m.life == 15
    cu = m.copper_kt()
    assert cu[0] == pytest.approx(40e6 * 0.008 * 0.87 / 1e3)
    assert np.all(np.diff(cu) < 0)                      # grades fall, so output falls
    assert np.all(np.diff(m.unit_cost()) > 0)          # and cost a pound rises
    rich = mine.Mine("rich", ore_mt=600, grade=1.6, mill_mtpa=40)
    assert rich.unit_cost()[0] < m.unit_cost()[0]


def test_breakeven_and_npv():
    m = mine.Mine("model", ore_mt=600, grade=0.8, mill_mtpa=40)
    p = m.breakeven()
    assert abs(m.npv(p)) < 1e-6 * m.capex
    assert m.npv(p + 0.5) > 0 > m.npv(p - 0.5)


def test_wait_value_is_an_option():
    m = mine.Mine("model", ore_mt=600, grade=0.8, mill_mtpa=40)
    p = m.breakeven()
    w = mine.wait_value(m, p, vol=0.3, n=500)
    assert w["now"] == pytest.approx(0, abs=1e-3 * m.capex)
    assert w["wait"] > 0                                 # at the margin, waiting is worth something
    w0 = mine.wait_value(m, p * 1.5, vol=1e-6, n=50)
    assert w0["wait"] == pytest.approx(m.npv(p * 1.5) / 1.08, rel=1e-3)


def test_cost_curve_and_bet():
    c = mine.cost_curve([("b", 2.0, 5), ("a", 1.0, 3)])
    assert c[0][0] == "a" and c[1][2] == 3 and c[1][3] == 8
    start = {"x": 1.0, "y": 2.0}
    assert mine.basket(start, start) == pytest.approx(400)
    assert mine.basket(start, {"x": 0.5, "y": 1.0}) == pytest.approx(200)
    w = mine.bet_windows({"x": {2000: 1, 2010: 2, 2001: 1, 2011: 1}, "y": {2000: 1, 2010: 1, 2001: 1, 2011: 1}})
    assert w == [(2000, 1.5), (2001, 1.0)]
