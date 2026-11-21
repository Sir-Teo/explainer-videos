"""Helpers shared by the scenes of Part 52 of *Economics, Built* ("Many Agents"): the chapter card, axes, curves and
colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import hetero  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, TRUTH, film_time, load  # noqa: F401

PART = 52
ASK = r"What does macroeconomics get wrong by treating a country as one household?"

HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
GAIN = "#7BD88F"
LOSS = "#F25F5C"
REP = "#FFFFFF"            # the representative household
MANY = "#7FD1B9"           # many households
POOR = "#F2A65A"           # households near their limit
RICH = "#7EC8F5"           # wealthy households
DIRECT = "#7EC8F5"         # the direct effect of a rate
INDIRECT = "#F2C14E"       # the indirect effect, through incomes
SUPPLY = "#7FD1B9"         # households' supply of capital
DEMAND = "#E8A0B4"         # firms' demand for capital
DIST = "#C9A0FF"           # distributions
RULE = "#F2C14E"           # forecasting rules
FIRM = "#E8A0B4"
ERR = "#F25F5C"
THEORY = "#7FD1B9"         # formulas
DATA = "#F2C14E"
GRID = "#9AA3B2"
RECESS = "#3A3F4B"
CONTROL = "#9AA3B2"
CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4", "#C9A0FF")
FIFTHS = ("#F2A65A", "#F2C14E", "#7FD1B9", "#7EC8F5", "#C9A0FF")


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("world",), horizon=("a century",),
         hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def plane(x_range, y_range, center=ORIGIN, x_length=5.6, y_length=5.2, xticks=None, yticks=None, xlabel="",
          ylabel="", font_size=19, xfmt=None, yfmt=None):
    from explainer.ai.viz import axes

    return axes(list(x_range), list(y_range), x_length=x_length, y_length=y_length, xticks=xticks, yticks=yticks,
                xlabel=xlabel, ylabel=ylabel, font_size=font_size, center=center, xfmt=xfmt, yfmt=yfmt)


def path(ax, xs, ys, color=WHITE, width=3.0, xr=None, yr=None, smooth=True):
    """A curve through (x, y) on axes ``ax``, keeping the points inside the ranges given."""
    a = ax.ax
    pts = []
    for x, y in zip(xs, ys):
        if x is None or y is None or not (np.isfinite(x) and np.isfinite(y)):
            continue
        if xr and not (xr[0] <= x <= xr[1]):
            continue
        if yr and not (yr[0] <= y <= yr[1]):
            continue
        pts.append(a.c2p(x, y))
    m = VMobject(stroke_color=color, stroke_width=width)
    if len(pts) > 3 and smooth:
        m.set_points_smoothly(pts)
    elif len(pts) > 1:
        m.set_points_as_corners(pts)
    return m


def band(ax, xs, lo, hi, color, opacity=0.18):
    """A shaded band between ``lo`` and ``hi``."""
    a = ax.ax
    up = [a.c2p(x, y) for x, y in zip(xs, hi)]
    dn = [a.c2p(x, y) for x, y in zip(xs, lo)][::-1]
    return Polygon(*up, *dn, stroke_width=0, fill_color=color, fill_opacity=opacity)


def seg(ax, x0, y0, x1, y1, color=WHITE, width=3.0, dashed=False):
    a = ax.ax
    cls = DashedLine if dashed else Line
    return cls(a.c2p(x0, y0), a.c2p(x1, y1), color=color, stroke_width=width)


def dot(ax, x, y, color=WHITE, r=0.07):
    return Dot(ax.ax.c2p(x, y), radius=r, color=color)


def shade(ax, spans, y0, y1, color=RECESS, opacity=0.55):
    """Bands over the x-intervals ``spans``, from y0 to y1."""
    g = VGroup()
    for a, b in spans:
        p0, p1 = ax.ax.c2p(a, y0), ax.ax.c2p(b, y1)
        if p1[0] - p0[0] < 0.02:
            p1 = p0 + np.array([0.02, p1[1] - p0[1], 0])
        g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=color, fill_opacity=opacity,
                        stroke_width=0).move_to((p0 + p1) / 2))
    return g


def vline(ax, x, y0, y1, color=GREY_B, width=2.0):
    return DashedLine(ax.ax.c2p(x, y0), ax.ax.c2p(x, y1), color=color, stroke_width=width)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def crowd(n_cols: int = 25, n_rows: int = 12, width: float = 10.0, height: float = 4.6, seed: int = 52,
          colors=(MANY,), radius: float = 0.045):
    """Households as a field of dots, jittered on a grid."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n_rows):
        for j in range(n_cols):
            x = -width / 2 + width * (j + 0.5 + 0.3 * rng.uniform(-1, 1)) / n_cols
            y = -height / 2 + height * (i + 0.5 + 0.3 * rng.uniform(-1, 1)) / n_rows
            g.add(Dot([x, y, 0], radius=radius, color=colors[rng.integers(len(colors))]))
    return g


def hbars(ax, rows, y0=0.5, h=0.6):
    """Horizontal bars on axes ``ax`` from zero: ``rows`` of (value, color), the first at the top."""
    a = ax.ax
    g = VGroup()
    n = len(rows)
    for i, (v, col) in enumerate(rows):
        y = n - 1 - i + y0
        p0, p1 = a.c2p(0, y - h / 2), a.c2p(v, y + h / 2)
        w = p1[0] - p0[0]
        r = Rectangle(width=max(abs(w), 0.01), height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                      fill_opacity=0.85)
        r.move_to((p0 + p1) / 2)
        g.add(r)
    return g
