"""Helpers shared by the scenes of Part 10 ("The Mathematics of Scale")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

WIDTH_COLORS = ["#7FD3FF", C.BITS, C.MODEL_Q]  # widths 32, 256, 2,048
SP, MUP = C.SURPRISE, C.INTERVAL
BUDGET_COLORS = ["#7FD3FF", C.BITS, C.MODEL_Q]


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def log_axes(x_range, y_range, x_length=8.0, y_length=4.6, center=ORIGIN, x_ticks=(), y_ticks=(), y_fmt="{:.1f}"):
    """Axes whose x coordinate is log10 of the quantity; tick labels written as powers of ten (or given)."""
    ax = Axes(x_range=[*x_range, 1], y_range=[*y_range, (y_range[1] - y_range[0]) / 4], x_length=x_length,
              y_length=y_length, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
    ax.move_to(center)
    labels = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.1)
                      for t, v in x_ticks],
                    *[MathTex(y_fmt.format(v), font_size=22, color=GREY_B).next_to(ax.c2p(x_range[0], v), LEFT, buff=0.1)
                      for v in y_ticks])
    return ax, labels
