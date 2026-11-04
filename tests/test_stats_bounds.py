"""``bounds(ax)`` reports an axis's data range even though ``CornerAxes`` stores it shifted to start at 0."""

import numpy as np

from explainer.stats import axes, bounds, ecdf_steps


def test_bounds_of_shifted_axes():
    A = axes([-3.2, 3.2], [150, 190])
    assert bounds(A.ax) == (-3.2, 3.2, 150.0, 190.0)
    assert A.ax.x_range[0] == 0  # the internal, shifted range


def test_scatter_keeps_negative_points():
    from videos.stats.stats5.common import scatter

    A = axes([-3, 3], [-3, 3])
    x = np.array([-2.0, -1.0, 0.5, 2.5, 4.0])
    assert len(scatter(A.ax, x, -x)) == 4  # only the point outside the range is dropped


def test_ecdf_starts_at_the_left_edge():
    A = axes([150, 200], [0, 1])
    m = ecdf_steps(A.ax, [160, 170, 180])
    assert np.isclose(m.get_start()[0], A.ax.c2p(150, 0)[0])
