"""Helpers shared by the scenes of Part 40 of *Economics, Built* ("Inequality and Mobility"): the chapter card, axes,
curves and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import distribution  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, HEIGHT, film_time, load  # noqa: F401

PART = 40
ASK = r"How unequal are incomes and wealth, why, and do children escape where they started?"

HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
TOP = "#F2C14E"            # the top: top shares, the rich
BOTTOM = "#7EC8F5"         # the bottom half
MIDDLE = "#7FD1B9"         # the middle
WEALTH = "#C9A0FF"         # wealth
INCOME = "#F2C14E"         # income
PARENT = "#7EC8F5"         # parents
CHILD = "#E8A0B4"          # children
LORENZ = "#F2C14E"         # Lorenz curves
SOC_A = "#7EC8F5"          # society A
SOC_B = "#E8A0B4"          # society B
PURE = "#9AA3B2"           # pure random growth
TYPES = "#F25F5C"          # type dependence
THEORY = "#7FD1B9"         # theory lines
DATA = "#F2C14E"           # data
GAIN = "#7BD88F"
LOSS = "#F25F5C"
RECESS = "#3A3F4B"
COUNTRY = {"United States": "#F2C14E", "United Kingdom": "#E8A0B4", "France": "#7EC8F5", "Sweden": "#7FD1B9",
           "Germany": "#9AA3B2", "China": "#F25F5C", "India": "#FFB86B", "Russia": "#C9A0FF"}
CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4", "#C9A0FF")


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("nation",), horizon=("a year",),
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
