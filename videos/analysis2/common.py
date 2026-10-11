"""Helpers shared by the scenes of Part 2 ("Limits: Sequences, Series, Continuity and the Derivative").

Part 2 reuses Part 1's helpers (the zoomable Window with its rational ruler, pinned labels, interval endpoints)
and the series' instruments from ``explainer/analysis``, including the epsilon-delta game boards.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import SQRT2, Window, endpoint, interval_bar, pin, polyline  # noqa: F401

from .compute import load  # noqa: F401


def plain_axes(x_range, y_range, x_length, y_length, numbers=False, font_size=22, **kw) -> Axes:
    cfg = {"stroke_color": GREY_C, "include_numbers": numbers, "font_size": font_size}
    cfg.update(kw.pop("axis_config", {}))
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False, axis_config=cfg, **kw)


def hop(start, end, color, up=True, stroke_width=3, tip=0.14) -> VMobject:
    """A curved arrow above (or below) a number line from one point to another."""
    ang = (-TAU / 5 if end[0] > start[0] else TAU / 5) * (1 if up else -1)
    return CurvedArrow(np.asarray(start) + UP * 0.08 * (1 if up else -1), np.asarray(end) + UP * 0.08 * (1 if up else -1),
                       angle=ang, color=color, stroke_width=stroke_width, tip_length=tip)


def sum_plot(ax: Axes, sums, color=C.SEQ, stroke_width=2.5, k0=1) -> VMobject:
    """Partial sums s_k against k as a polyline on ``ax`` (k starting at k0)."""
    k = np.arange(k0, k0 + len(sums))
    return polyline(ax, k, sums, color=color, stroke_width=stroke_width)
