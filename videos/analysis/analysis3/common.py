"""Helpers shared by the scenes of Part 3 ("Integration and the First Function Space").

Part 3 reuses the earlier parts' helpers and introduces two instruments from ``explainer/analysis``: the
convergence dashboard (one sequence of functions under several lenses at once) and the function-as-a-point camera.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import endpoint, polyline  # noqa: F401
from videos.analysis.analysis2.common import plain_axes, runs_in_range  # noqa: F401

from .compute import load  # noqa: F401


def int_axes(x_range, y_range, x_length, y_length, font_size=20, x_dec=0, y_dec=0, **kw) -> Axes:
    """Axes with numbered ticks (no '5.0'-style labels)."""
    return plain_axes(x_range, y_range, x_length, y_length, numbers=True, font_size=font_size,
                      x_axis_config={"decimal_number_config": {"num_decimal_places": x_dec}},
                      y_axis_config={"decimal_number_config": {"num_decimal_places": y_dec}}, **kw)


def rects(ax: Axes, edges, heights, color, opacity=0.55, stroke=1.2) -> VGroup:
    """Rectangles on the intervals [edges[i], edges[i+1]] with the given heights (from y = 0)."""
    g = VGroup()
    for a, b, h in zip(edges[:-1], edges[1:], heights):
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, h)
        g.add(Rectangle(width=max(p1[0] - p0[0], 1e-3), height=max(abs(p1[1] - p0[1]), 1e-3), stroke_color=color,
                        stroke_width=stroke, fill_color=color, fill_opacity=opacity).move_to((p0 + p1) / 2))
    return g


def saw(x):
    """(pi - x)/2 on (0, 2 pi), 0 at the jumps, period 2 pi."""
    y = np.mod(np.asarray(x, float), 2 * np.pi)
    return np.where(y == 0, 0.0, (np.pi - y) / 2)


def saw_partial(x, N):
    n = np.arange(1, N + 1)
    return (np.sin(np.outer(n, np.asarray(x, float))) / n[:, None]).sum(axis=0)
