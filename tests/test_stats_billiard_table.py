"""Bayes's billiard table maps the unit square onto its felt and rolls balls to their spots."""

import numpy as np

from explainer.stats import BilliardTable


def test_table():
    t = BilliardTable(width=6, height=4, center=[1, 0, 0])
    assert np.allclose(t.point(0, 0), [-2, -2, 0]) and np.allclose(t.point(1, 1), [4, 2, 0])
    ball, anim = t.roll(0.3, 0.7)
    anim.interpolate(1.0)
    assert np.allclose(ball.get_center(), t.point(0.3, 0.7), atol=1e-6)
    assert abs(t.line(0.25).get_x() - t.point(0.25, 0.5)[0]) < 1e-6
