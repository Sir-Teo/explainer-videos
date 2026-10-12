"""Helpers shared by the scenes of Part 5 ("Measure: The Lebesgue Integral").

Part 5 draws sets on a line as bands of intervals, functions sliced into horizontal layers, and the three ways mass
can escape a sequence of functions.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import heatmap, square_axes  # noqa: F401

from .compute import load  # noqa: F401


def interval_band(ax: Axes, intervals, y, color, height=0.12, opacity=0.85, min_width=0.012) -> VGroup:
    """Intervals [a, b] (data coordinates on ax's x-axis) drawn as bars at scene height y."""
    g = VGroup()
    for a, b in intervals:
        pa, pb = ax.c2p(a, 0)[0], ax.c2p(b, 0)[0]
        g.add(Rectangle(width=max(pb - pa, min_width), height=height, stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([(pa + pb) / 2, y, 0]))
    return g


def area_under(ax: Axes, x, y, color, opacity=0.4) -> Polygon:
    pts = [ax.c2p(x[0], 0)] + [ax.c2p(a, b) for a, b in zip(x, y)] + [ax.c2p(x[-1], 0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def step_graph(ax: Axes, edges, heights, color, stroke_width=3) -> VGroup:
    """A step function: horizontal segments of the given heights over [edges[i], edges[i+1]]."""
    return VGroup(*[Line(ax.c2p(a, h), ax.c2p(b, h), color=color, stroke_width=stroke_width)
                    for a, b, h in zip(edges[:-1], edges[1:], heights)])
