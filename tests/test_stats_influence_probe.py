"""The influence probe refits as its point moves."""

import numpy as np

from explainer.stats import InfluenceProbe, axes


def test_probe_refits():
    A = axes([0, 10], [0, 30])
    xs = np.arange(10.0)
    ys = 2 * xs + 1
    p = InfluenceProbe(A.ax, xs, ys, index=-1)
    assert np.isclose(p._fit().coef[1], 2.0)
    p.py.set_value(29.0)
    assert p._fit().coef[1] > 2.0
    assert p._fit().cooks[-1] > 0.1
    p.stop()
