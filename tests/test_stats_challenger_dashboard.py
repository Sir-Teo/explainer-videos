"""The Challenger dashboard draws the flights, the fitted curve and a probe that follows its tracker."""

import numpy as np

from explainer.stats import ChallengerDashboard, axes, museum
from explainer.stats.kit import glm


def test_dashboard():
    t = np.asarray(museum.CHALLENGER_TEMP, float)
    y = (np.asarray(museum.CHALLENGER_DISTRESS) > 0).astype(float)
    f = glm.logistic(np.column_stack([np.ones(23), t]), y)
    A = axes([25, 85], [0, 1])
    d = ChallengerDashboard(A.ax, t, y, f, x0=70)
    assert len(d.dots) == 23
    d.tx.set_value(31)
    d.probe.update()
    assert d.probe[1].get_y() > A.ax.c2p(0, 0.99)[1]
    d.stop()
