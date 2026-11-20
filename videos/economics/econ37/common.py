"""Helpers shared by the scenes of Part 37 of *Economics, Built* ("Cities and Regions"): the chapter card, axes,
curves, the checkerboard and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import city  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 37
ASK = r"Why is economic activity piled up in a few places, and what does that do to the people in them?"

HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
TEAL = "#7FD1B9"           # Schelling's first kind of coin
GOLD = "#F2C14E"           # the second kind
ISLAND = "#7FD1B9"         # the Island
CITY = "#7EC8F5"           # cities, density
RENT = "#F25F5C"           # rents, prices of land and floor space
WAGE = "#7BD88F"           # wages
AMENITY = "#C9A0FF"        # amenities, quality of life
FARM = "#B5865A"           # farmland
ROAD = "#E8A0B4"           # transport
GAIN = "#7BD88F"
LOSS = "#F25F5C"
WHITEISH = "#E6E6E6"
EMPTY = "#20242C"
RECESS = "#3A3F4B"
TOWN_COLORS = ("#7EC8F5", "#F2C14E", "#E8A0B4", "#7BD88F", "#B5865A", "#C9A0FF")
RING_COLORS = ("#7BD88F", "#B5865A", "#F2C14E", "#E8A0B4")


def board(grid, size: float = 6.0, gap: float = 0.08):
    """The checkerboard: one square per cell, teal and gold for the two kinds, dark for empty."""
    g = np.asarray(grid)
    n = g.shape[0]
    s = size / n
    sq = VGroup()
    for r in range(n):
        for c in range(n):
            sq.add(Square(side_length=s * (1 - gap), stroke_width=0, fill_opacity=1.0,
                          fill_color=(EMPTY, TEAL, GOLD)[int(g[r, c])]).move_to(
                np.array([(c - (n - 1) / 2) * s, ((n - 1) / 2 - r) * s, 0])))
    return sq


def recolour(sq, old, new):
    """The animations that turn the board ``sq`` from grid ``old`` into grid ``new`` (only the squares that change)."""
    a, b = np.asarray(old).ravel(), np.asarray(new).ravel()
    return [sq[k].animate.set_fill((EMPTY, TEAL, GOLD)[int(b[k])]) for k in np.flatnonzero(a != b)]


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
