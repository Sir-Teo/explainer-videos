"""Helpers shared by the scenes of Part 10 of *Economics, Built* ("The Price Maker")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import pricing as pr  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 10
ASK = r"What does a seller do when the price is hers to set?"

BO = island.CAST["bo"].color
DEM = "#7EC8F5"         # demand
MR = "#F2A65A"          # marginal revenue
MC = WHITE              # marginal cost
PROFIT = E.ACCENT       # profit
CS = "#7BD88F"          # consumer surplus
DWL = E.MISS            # deadweight loss
STUD = "#C9A0FF"        # students
TOWN = "#F29E8E"        # townsfolk
BEAN = "#C89B6D"        # green coffee
SHELF = "#E8E8E8"       # the shelf price
HOLD = E.MISS           # caveats


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("firm", "market"), horizon=("a year",),
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
        if not (np.isfinite(x) and np.isfinite(y)):
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


def region(ax, pts, color, opacity=0.3):
    """A filled polygon through data points."""
    return Polygon(*[ax.ax.c2p(x, y) for x, y in pts], stroke_width=0, fill_color=color, fill_opacity=opacity)


def ferry_glyph(width: float = 1.6, color=BO) -> VGroup:
    hull = Polygon([-width / 2, 0, 0], [width / 2, 0, 0], [width * 0.38, -0.28 * width / 1.6, 0],
                   [-width * 0.38, -0.28 * width / 1.6, 0], stroke_color=WHITE, stroke_width=2, fill_color=color,
                   fill_opacity=0.7)
    cabin = Rectangle(width=width * 0.4, height=0.22 * width / 1.6, stroke_color=WHITE, stroke_width=1.5,
                      fill_color="#2E3440", fill_opacity=0.9).next_to(hull, UP, buff=0)
    waves = VGroup(*[ArcBetweenPoints(LEFT * 0.18 + RIGHT * k * 0.36, RIGHT * 0.18 + RIGHT * k * 0.36, angle=-PI / 2,
                                      color="#5DADEC", stroke_width=2) for k in range(-2, 3)]
                   ).next_to(hull, DOWN, buff=0.05)
    return VGroup(waves, hull, cabin)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def signed(x: float, digits: int = 2) -> str:
    v = round(x, digits)
    if v == 0:
        return f"{0.0:.{digits}f}"
    return ("$+$" if v > 0 else "$-$") + f"{abs(v):.{digits}f}"
