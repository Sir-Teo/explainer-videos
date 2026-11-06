"""Part 6 histograms preserve the full sample's mass outside the plotting window."""
import numpy as np
from manim import Axes, BLUE

from videos.quant.quant6.common import hist_bars


def bar_heights_in_data_units(ax, bars):
    unit = (ax.c2p(0, 1) - ax.c2p(0, 0))[1]
    return np.array([b.height / unit for b in bars])


def test_density_window_does_not_move_tails_into_edge_bins_or_renormalize():
    ax = Axes(x_range=[0, 1], y_range=[0, 2], tips=False)
    edges = np.array([0, 0.25, 0.75])
    bars = hist_bars(ax, [-1, 0.1, 0.4, 1.2], edges, BLUE)
    heights = bar_heights_in_data_units(ax, bars)
    np.testing.assert_allclose(heights * np.diff(edges), [0.25, 0.25])
    assert np.dot(heights, np.diff(edges)) == 0.5


def test_counts_exclude_outside_values_and_include_the_rightmost_edge():
    ax = Axes(x_range=[0, 1], y_range=[0, 4], tips=False)
    bars = hist_bars(ax, [-1, 0.1, 0.2, 0.5, 0.75, 1.2], [0, 0.25, 0.75], BLUE, density=False)
    np.testing.assert_allclose(bar_heights_in_data_units(ax, bars), [2, 2])


def test_partial_reveal_uses_a_fixed_denominator_without_a_tall_initial_spike():
    ax = Axes(x_range=[0, 1], y_range=[0, 2], tips=False)
    edges = np.array([0, 0.25, 0.75])
    bars = hist_bars(ax, [0.1], edges, BLUE, total=4)
    # One of four eventual draws is revealed, contributing exactly one quarter.
    assert bar_heights_in_data_units(ax, bars)[0] * np.diff(edges)[0] == 0.25
