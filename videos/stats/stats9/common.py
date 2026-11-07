"""Helpers shared by the scenes of Part 9 of *Statistics, Built* ("Estimation")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import clipped_segments, histogram_density, load  # noqa: F401

PART = 9

DATA = S.MUSEUM
EXACT = S.TRUTH
SIM = S.EST
LIK = S.LIK
MOM, MAX, UMVUE = S.POST, S.RESID, S.EST  # the tank estimators: 2 xbar - 1, the maximum, the UMVUE
EST_COL = {"mom": MOM, "max": MAX, "umvue": UMVUE}
EST_TEX = {"mom": r"$2\bar x - 1$", "max": r"$\max$", "umvue": r"$m(1 + \tfrac1k) - 1$"}


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    m.set_points_as_corners([ax.c2p(a, b) for a, b in zip(xs, ys)])
    return m


def fit_rows(rows: VGroup, width: float, buff: float, pos) -> VGroup:
    for r in rows:
        if r.width > width:
            r.width = width
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(pos)
    return rows


def clip_curve(ax, xs, ys, color, stroke_width=3, ymin=None, ymax=None):
    xmin, xmax, bottom, top = bounds(ax)
    rectangle = (xmin, xmax, max(bottom, ymin) if ymin is not None else bottom,
                 min(top, ymax) if ymax is not None else top)
    result = VMobject(stroke_color=color, stroke_width=stroke_width)
    previous = None
    for start, end in clipped_segments(xs, ys, rectangle):
        if previous is None or not np.allclose(previous, start, atol=1e-12, rtol=0):
            result.start_new_path(ax.c2p(*start))
        result.add_line_to(ax.c2p(*end))
        previous = end
    return result
