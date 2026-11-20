"""Helpers shared by the scenes of Part 28 of *Economics, Built* ("Inflation and Expectations"): the chapter card, axes,
curves and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import expectations as ex  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 28
ASK = r"Can a country buy lower unemployment with higher inflation?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
INFL = "#F25F5C"             # inflation
UNEMP = "#7EC8F5"            # unemployment
EXPECT = "#F2C14E"           # expectations, forecasts
CB = "#7FD1B9"               # the central bank, policy
RATE = "#E8A0B4"             # interest rates
OUTPUT = "#7BD88F"           # output, the natural rate
WAGE = "#C9A66B"             # wages
SURPRISE = "#C9A0FF"         # surprises, noise
TRUTH_C = "#7BD88F"        # the Island's planted truth


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("market",), horizon=("a year",),
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


def seg(ax, x0, y0, x1, y1, color=WHITE, width=3.0, dashed=False):
    a = ax.ax
    cls = DashedLine if dashed else Line
    return cls(a.c2p(x0, y0), a.c2p(x1, y1), color=color, stroke_width=width)


def dot(ax, x, y, color=WHITE, r=0.07):
    return Dot(ax.ax.c2p(x, y), radius=r, color=color)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def commas(v) -> str:
    """12345 -> '12{,}345' for TeX."""
    return f"{v:,.0f}".replace(",", "{,}")


def pc(v, nd=1) -> str:
    """0.0123 -> '1.2\\%' for TeX."""
    return f"{100 * v:.{nd}f}\\%"


def rows_card(rows, buff=0.42, center=UP * 0.1):
    """A column of (text, colour, size) labels, centred."""
    g = VGroup(*[label(t, font_size=fs, color=c) for t, c, fs in rows]).arrange(DOWN, buff=buff)
    if g.width > 13.2:
        g.width = 13.2
    return g.move_to(center)
