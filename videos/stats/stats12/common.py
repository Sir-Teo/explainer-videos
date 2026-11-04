"""Helpers shared by the scenes of Part 12 of *Statistics, Built* ("Least Squares")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 12

DATA = S.MUSEUM
EXACT = S.TRUTH
SIM = S.EST
NULLC = S.NULL  # the null distribution
ALTC = S.ALT  # the alternative
REJ = S.RESID  # the rejection region
OBS = S.ACCENT  # the observed statistic


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
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    keep = np.isfinite(ys)
    if ymin is not None:
        keep &= ys >= ymin
    if ymax is not None:
        keep &= ys <= ymax
    return curve(ax, xs[keep], ys[keep], color, stroke_width)


def shade(ax, xs, ys, color, opacity=0.35):
    """The area under a curve over ``xs`` (a tail, a rejection region)."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    y0 = bounds(ax)[2]
    pts = [ax.c2p(xs[0], y0)] + [ax.c2p(a, b) for a, b in zip(xs, ys)] + [ax.c2p(xs[-1], y0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def bars_at(ax, xs, hs, width, color, opacity=0.8, highlight=None, hcolor=None):
    """Bars centred on ``xs`` (a pmf); indices in ``highlight`` drawn in ``hcolor``."""
    g = VGroup()
    y0 = bounds(ax)[2]
    w = ax.c2p(width, y0)[0] - ax.c2p(0, y0)[0]
    for i, (x, h) in enumerate(zip(xs, hs)):
        c = hcolor if highlight is not None and i in highlight else color
        hh = max(1e-3, ax.c2p(x, h)[1] - ax.c2p(x, y0)[1])
        g.add(Rectangle(width=w, height=hh, stroke_width=0, fill_color=c, fill_opacity=opacity).move_to(ax.c2p(x, y0), aligned_edge=DOWN))
    return g

FIT = S.FIT
RES = S.RESID
HIT, MISS = S.KEPT, S.BROKEN


def scatter(ax, xs, ys, color=None, radius=0.06, opacity=0.9):
    return VGroup(*[Dot(ax.c2p(a, b), radius=radius, color=color or DATA, fill_opacity=opacity) for a, b in zip(xs, ys)])


def fit_line(ax, a, b, x0, x1, color=None, stroke_width=4):
    return Line(ax.c2p(x0, a + b * x0), ax.c2p(x1, a + b * x1), color=color or FIT, stroke_width=stroke_width)
