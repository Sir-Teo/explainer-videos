import numpy as np

from explainer.stats import axes
from explainer.stats.viz import Correlogram, RootPlane, YulePendulum


def test_correlogram_marks_bars_outside_the_band():
    A = axes([0, 10], [-1, 1])
    r = np.r_[1.0, 0.5, 0.05, -0.3, np.zeros(7)]
    c = Correlogram(A.ax, r, band=0.2, theory=r)
    assert len(c.bars) == 10 and len(c.bands) == 2 and len(c.theory) == 10
    hot = [b.get_fill_color().to_hex() for b in c.bars]
    assert hot[0] == hot[2] != hot[1]


def test_root_plane_colours_by_the_unit_circle():
    rp = RootPlane([2.0, 0.5, (0.0, 1.5)], scale=1.0)
    cols = [d.get_color().to_hex() for d in rp.dots]
    assert cols[0] == cols[2] != cols[1]
    assert np.allclose(rp.point(1j), rp.c + np.array([0, 1.0, 0]))


def test_pendulum_follows_the_series():
    x = np.array([0.0, 1.0, -1.0])
    p = YulePendulum(x, pivot=np.zeros(3), length=2.0, max_angle=0.5)
    assert np.allclose(p.at(0).bob.get_center(), [0, -2, 0])
    assert p.at(1).bob.get_center()[0] > 0 > p.at(2).bob.get_center()[0]


def test_l1_geometry_touches_a_corner_and_the_circle():
    from explainer.stats.viz import L1Geometry

    g = L1Geometry([2.0, 0.6], Q=[[1.0, 0.3], [0.3, 1.0]])
    b1 = g.touch(1, 1.0)
    assert np.isclose(abs(b1[0]) + abs(b1[1]), 1.0, atol=1e-3) and abs(b1[1]) < 1e-3  # the corner (1, 0)
    b2 = g.touch(2, 1.0)
    assert np.isclose(np.hypot(*b2), 1.0, atol=1e-3) and b2[1] > 0.05  # ridge shrinks, keeps both
    assert np.allclose(g.touch(1, 10.0), [2.0, 0.6])
