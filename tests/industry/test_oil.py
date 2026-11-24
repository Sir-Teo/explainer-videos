import numpy as np
import pytest

from explainer.industry.works import oil


def test_arps_starts_at_qi_and_integrates():
    for b in (0.0, 0.5, 1.0):
        assert oil.arps(0, 1000, 0.8, b) == pytest.approx(1000)
        t = np.linspace(0, 3, 30001)
        num = np.trapezoid(oil.arps(t, 1000, 0.8, b), t) * oil.DAYS
        assert oil.arps_cum(3, 1000, 0.8, b) == pytest.approx(num, rel=1e-6)


def test_shale_declines_faster_than_conventional():
    conv, deep, shale = oil.prospects()
    assert oil.first_year_decline(shale.di, shale.b) > 0.5 > oil.first_year_decline(conv.di, conv.b)


def test_breakeven_makes_npv_zero_and_order_is_sensible():
    for f in oil.prospects():
        p = f.breakeven(0.10)
        assert abs(f.npv(p, 0.10)) < 1e-6 * f.capex
        assert f.npv(p + 5, 0.10) > 0 > f.npv(p - 5, 0.10)
    # cash only arrives after the build, so a slower field needs a higher price at a higher discount rate
    deep = oil.prospects()[1]
    assert deep.breakeven(0.15) > deep.breakeven(0.05)


def test_treadmill_holds_level_with_the_computed_rate():
    level = 500_000
    n = oil.wells_to_hold(level)
    out = oil.treadmill(np.full(600, n))
    assert out[-1] == pytest.approx(level, rel=0.02)
    stop = oil.treadmill(np.r_[np.full(480, n), np.zeros(12)])
    assert stop[-1] < 0.8 * stop[479]  # stop drilling and a shale basin falls fast


def test_clearing_multiple():
    assert oil.clearing_multiple(0.0) == pytest.approx(1.0)
    m = oil.clearing_multiple(0.05, -0.05, 0.05)
    assert m == pytest.approx(0.95 ** -10)
    assert oil.clearing_multiple(0.05, -0.3, 0.2) < m  # more elastic, smaller jump


def test_crack_and_refinery():
    assert oil.crack_321(70, 70 / 42, 70 / 42) == pytest.approx(0)
    r = oil.Refinery()
    prices = {k: 80.0 for k in r.yields}
    assert r.margin(70, prices) == pytest.approx(10 - r.cash_cost)
    assert r.profit(70, prices) > 0


def test_price_paths_shape_and_start():
    p = oil.price_paths(50, 10, p0=60, seed=1)
    assert p.shape == (50, 10) and np.allclose(p[:, 0], 60)
