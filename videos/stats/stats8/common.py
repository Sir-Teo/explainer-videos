"""Helpers shared by the scenes of Part 8 of *Statistics, Built* ("From Sample to Population")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401
from explainer.stats import hist_bars as _hist_bars

from .compute import clipped_segments, load  # noqa: F401

PART = 8

DATA = S.MUSEUM
EXACT = S.TRUTH  # exact sampling distributions: gold
SIM = S.EST  # simulated sampling distributions: blue
RESID = S.RESID
NORMAL = GREY_B  # the normal curve, when it is the wrong answer


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    previous = None
    for start, end in clipped_segments(xs, ys, bounds(ax)):
        if previous is None or not np.allclose(previous, start, atol=1e-12, rtol=0):
            m.start_new_path(ax.c2p(*start))
        m.add_line_to(ax.c2p(*end))
        previous = end
    return m


def curve(ax, xs, ys, color=WHITE, stroke_width=2.5, opacity=1.0) -> VMobject:
    """Sampled curves use the same honest viewport clipping as running paths."""
    return polyline(ax, xs, ys, color, stroke_width, opacity)


def fit_rows(rows: VGroup, width: float, buff: float, pos) -> VGroup:
    """Shrink any row wider than ``width``, left-align, and place the block's centre at ``pos``."""
    for r in rows:
        if r.width > width:
            r.width = width
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(pos)
    return rows


def pdf_curve(ax, xs, ys, color, stroke_width=3, ymax=None):
    # Curves leave and re-enter the viewport; never join across a removed peak.
    return curve(ax, xs, ys, color, stroke_width)


def normal_pdf_(x, mu=0.0, sd=1.0):
    return np.exp(-0.5 * ((np.asarray(x) - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def hist_bars(ax, edges, density, *args, **kwargs):
    """Crop displayed bins to the x viewport, preserving their full-sample heights."""
    edges, density = np.asarray(edges), np.asarray(density)
    xmin, xmax, _, _ = bounds(ax)
    visible = np.flatnonzero((edges[:-1] < xmax) & (edges[1:] > xmin))
    if not len(visible):
        return VGroup()
    lo, hi = visible[0], visible[-1] + 1
    return _hist_bars(ax, np.clip(edges[lo:hi + 1], xmin, xmax), density[lo:hi], *args, **kwargs)
