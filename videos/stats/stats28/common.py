"""Helpers shared by the scenes of Part 28 of *Statistics, Built* ("Which Model?")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 28

DATA = S.MUSEUM
EXACT = S.TRUTH
SIM = S.EST
NULLC = S.NULL  # the null distribution
ALTC = S.ALT  # the alternative
REJ = S.RESID  # the rejection region
OBS = S.ACCENT  # the observed statistic




def fit_rows(rows: VGroup, width: float, buff: float, pos) -> VGroup:
    for r in rows:
        if r.width > width:
            r.width = width
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(pos)
    return rows




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

# treatments: one colour each, in the order of their letters
TRT = [S.CTRL, S.TREAT, S.ALT, S.PRIOR, S.POST]
LETTERS = "ABCDE"
BLOCK = S.ACCENT


def field_from(values, cell=0.38, center=ORIGIN, lo=None, hi=None, gap=0.04):
    """A ``FieldPlot`` already painted with ``values`` (rows x cols)."""
    v = np.asarray(values, float)
    return FieldPlot(v.shape[0], v.shape[1], cell=cell, gap=gap, center=center).painted(v, lo, hi)


def soil_key(lo, hi, center, width=2.6, text=r"yield", font_size=20):
    """A small colour bar from soil to leaf for a ``FieldPlot``."""
    n = 24
    bar = VGroup(*[Rectangle(width=width / n, height=0.18, stroke_width=0, fill_opacity=1,
                             fill_color=FieldPlot.colour(lo + (hi - lo) * (k + 0.5) / n, lo, hi)) for k in range(n)])
    bar.arrange(RIGHT, buff=0).move_to(center)
    a = label(rf"{lo:.0f}", font_size=font_size, color=GREY_B).next_to(bar, LEFT, buff=0.12)
    b = label(rf"{hi:.0f}", font_size=font_size, color=GREY_B).next_to(bar, RIGHT, buff=0.12)
    t = label(text, font_size=font_size, color=GREY_B).next_to(bar, UP, buff=0.1)
    return VGroup(bar, a, b, t)


def table_rows(rows, font_size=24, col_buff=0.5, row_buff=0.22, colors=None):
    """A simple table: ``rows`` of TeX strings, columns aligned; ``colors[i]`` colours row i."""
    cells = [[label(c, font_size=font_size) if isinstance(c, str) else c for c in r] for r in rows]
    ncol = max(len(r) for r in cells)
    widths = [max(r[j].width for r in cells if j < len(r)) for j in range(ncol)]
    g = VGroup()
    y = 0.0
    for i, r in enumerate(cells):
        row = VGroup()
        x = 0.0
        for j, c in enumerate(r):
            c.move_to([x + widths[j] / 2, y, 0])
            if colors and colors[i]:
                c.set_color(colors[i])
            row.add(c)
            x += widths[j] + col_buff
        g.add(row)
        y -= max(c.height for c in r) + row_buff
    return g


PRIOR, LIKE, POST = S.PRIOR, S.LIK, S.POST


def density(ax, xs, ys, color, stroke_width=3, fill=0.25):
    """A density curve with its area shaded."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    c = curve(ax, xs, ys, color, stroke_width)
    y0 = bounds(ax)[2]
    pts = [ax.c2p(xs[0], y0)] + [ax.c2p(a, b) for a, b in zip(xs, ys)] + [ax.c2p(xs[-1], y0)]
    return VGroup(Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=fill), c)

BOOT = S.EST  # bootstrap replicates
REAL = S.WORLD
SERIES = S.DATA  # an observed series
MODEL = S.FIT  # a fitted model, its forecasts
SHOCK = S.ACCENT  # the shocks e_t
FC = S.EST  # forecasts and their intervals


def series_line(ax, t, y, color=None, stroke_width=2.5, opacity=1.0):
    """A time series as a polyline on ``ax`` (NaNs skipped)."""
    t, y = np.asarray(t, float), np.asarray(y, float)
    k = np.isfinite(y)
    return polyline(ax, t[k], y[k], color or SERIES, stroke_width, opacity)


def band(ax, t, lo, hi, color, opacity=0.25):
    """A shaded band between ``lo`` and ``hi`` over ``t`` (forecast intervals)."""
    pts = [ax.c2p(a, b) for a, b in zip(t, lo)] + [ax.c2p(a, b) for a, b in zip(t[::-1], hi[::-1])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

RAW = S.EST  # unpooled estimates
SHRUNK = S.KEPT  # shrunk / partially pooled: green
POOLED = S.ALT  # complete pooling
TRUE = S.TRUTH
PRIOR, POST = S.PRIOR, S.POST
BLUE = S.CTRL
RED = S.TREAT
TEAL = S.ALT
PATH = S.ACCENT
FIT = S.FIT
RES = S.RESID
HIT, MISS = S.KEPT, S.BROKEN
MODEL = S.EST
OBSC = S.DATA


LIKE = S.LIK
SCHOOL = [S.CTRL, S.TREAT, S.ALT, S.PRIOR, S.POST, S.KEPT, S.ACCENT, S.MUSEUM]  # schools A-H


AICC = S.EST  # AIC
BICC = S.PRIOR  # BIC
CVC = S.KEPT  # cross-validation
LOOC = S.POST  # Bayesian LOO
TRAIN = S.ALT  # training error
TEST = S.RESID  # test error


def schools_tag(corner=DR):
    return historical_tag(r"Rubin (1981): \ the eight schools", corner=corner)


def prostate_tag(corner=DR):
    return historical_tag(r"Stamey et al.\ (1989), \ via Hastie, Tibshirani \& Friedman", corner=corner)


def seeded_tag(corner=DR):
    return simulated_tag(r"simulated: \ a seeded example", corner=corner)


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0):
    m=VMobject(stroke_color=color,stroke_width=stroke_width,stroke_opacity=opacity)
    last=None
    for p,q in clipped_segments(xs,ys,bounds(ax)):
        if last is None or not np.allclose(last,p,atol=1e-12,rtol=0):
            m.start_new_path(ax.c2p(*p))
        m.add_line_to(ax.c2p(*q))
        last=q
    return m


def clip_curve(ax,xs,ys,color,stroke_width=3,ymin=None,ymax=None):
    rectangle=list(bounds(ax))
    if ymin is not None:rectangle[2]=max(rectangle[2],ymin)
    if ymax is not None:rectangle[3]=min(rectangle[3],ymax)
    m=VMobject(stroke_color=color,stroke_width=stroke_width)
    last=None
    for p,q in clipped_segments(xs,ys,rectangle):
        if last is None or not np.allclose(last,p,atol=1e-12,rtol=0):m.start_new_path(ax.c2p(*p))
        m.add_line_to(ax.c2p(*q));last=q
    return m


def curve(ax,xs,ys,color,stroke_width=3):
    return polyline(ax,xs,ys,color,stroke_width)


def clipped_segments(xs, ys, rectangle):
    """Intersect segments with the viewport, preserving crossings and missing breaks."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end-start
        lo, hi = 0., 1.
        for j, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[j] == 0:
                if not lower <= start[j] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower-start[j])/delta[j], (upper-start[j])/delta[j]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start+lo*delta, start+hi*delta))
    return result
