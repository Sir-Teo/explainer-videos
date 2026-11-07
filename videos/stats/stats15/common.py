"""Helpers shared by the scenes of Part 15 of *Statistics, Built* ("First Bayes")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import clipped_segments, load  # noqa: F401

PART = 15

DATA = S.MUSEUM
EXACT = S.TRUTH
SIM = S.EST
NULLC = S.NULL  # the null distribution
ALTC = S.ALT  # the alternative
REJ = S.RESID  # the rejection region
OBS = S.ACCENT  # the observed statistic


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    return clip_curve(ax, xs, ys, color, stroke_width).set_stroke(opacity=opacity)


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


def curve(ax, xs, ys, color, stroke_width=3):
    return clip_curve(ax, xs, ys, color, stroke_width)


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
    """A geometrically clipped outline and visible area under the density."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    xmin, xmax, ymin, ymax = bounds(ax)
    keep = np.isfinite(xs) & np.isfinite(ys) & (xs >= xmin) & (xs <= xmax)
    xs, ys = xs[keep], ys[keep]
    outline = curve(ax, xs, ys, color, stroke_width)
    if not len(xs):
        return VGroup(outline)
    pts = [ax.c2p(xs[0], ymin)] + [ax.c2p(x, h) for x, h in zip(xs, np.clip(ys, ymin, ymax))] + [ax.c2p(xs[-1], ymin)]
    return VGroup(Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=fill), outline)
