"""Helpers shared by the scenes of Part 58 of *Economics, Built* ("Scoring the Bill"): the chapter card, axes, curves
and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import appraisal  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, TRUTH, film_time, load  # noqa: F401

PART = 58
ASK = r"How does a government decide whether a project or a law is worth it?"

HOLD = E.MISS              # caveats
GAIN = "#7BD88F"
LOSS = "#F25F5C"
TRUTHC = "#FFFFFF"         # the planted truth
EST = "#F2C14E"            # estimates
DATA = "#7EC8F5"           # data
MODEL = "#C9A0FF"          # models
THEORY = "#7FD1B9"         # formulas
OUT = "#7EC8F5"            # output
INFL = "#F2A65A"           # inflation and prices
RATE = "#E8A0B4"           # the policy rate
SUPPLY = "#7FD1B9"
DEMAND = "#F2C14E"
MONEY = "#E8A0B4"
ERR = "#F25F5C"
GRID = "#9AA3B2"
RECESS = "#3A3F4B"
CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4", "#C9A0FF")
BEN = "#7FD1B9"            # benefits
COST = "#F25F5C"           # costs
TRAV = "#7EC8F5"           # travellers
BO = "#9FB8F2"             # Bo and his ferry
SAFE = "#F2C14E"           # lives
NOISE = "#C9A0FF"          # noise and other unpriced things
RATE = "#E8A0B4"           # discount rates
STATIC = "#9AA3B2"         # static scores
BEHAV = "#F2C14E"          # scores with behaviour
DYN = "#E8A0B4"            # dynamic scores
CBO = "#7EC8F5"            # the Congressional Budget Office
ISL = "#F2A65A"            # the Island's numbers


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


def band(ax, xs, lo, hi, color, opacity=0.18, yr=None):
    """A shaded band between ``lo`` and ``hi``, clipped to ``yr`` when given."""
    a = ax.ax
    if yr is not None:
        lo, hi = np.clip(lo, *yr), np.clip(hi, *yr)
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



def strait(width: float = 9.0, height: float = 2.6, label_size: int = 18):
    """The Island's strait: the harbour town on the west shore, the north shore across the water, Bo's ferry on its
    route, and the planned bridge (``.bridge``, dashed until built)."""
    water = Rectangle(width=width * 0.62, height=height, fill_color="#1E3550", fill_opacity=0.95, stroke_width=0)
    west = RoundedRectangle(width=width * 0.2, height=height + 0.3, corner_radius=0.25, fill_color="#3A4F36",
                            fill_opacity=1.0, stroke_width=0).next_to(water, LEFT, buff=-0.12)
    east = RoundedRectangle(width=width * 0.2, height=height + 0.3, corner_radius=0.25, fill_color="#3A4F36",
                            fill_opacity=1.0, stroke_width=0).next_to(water, RIGHT, buff=-0.12)
    tw = label(r"the harbour \\ town", font_size=label_size, color=WHITE).move_to(west)
    te = label(r"the north \\ shore", font_size=label_size, color=WHITE).move_to(east)
    route = DashedLine(west.get_right() + DOWN * 0.55, east.get_left() + DOWN * 0.55, color=BO, stroke_width=2,
                       dash_length=0.12)
    hull = Polygon([-0.28, 0, 0], [0.28, 0, 0], [0.2, -0.13, 0], [-0.2, -0.13, 0], fill_color=BO, fill_opacity=1,
                   stroke_width=0)
    cabin = Rectangle(width=0.2, height=0.12, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).next_to(hull, UP,
                                                                                                        buff=0)
    ferry = VGroup(hull, cabin).move_to(route.get_start() + RIGHT * 0.5 + UP * 0.05)
    deck = DashedLine(west.get_right() + UP * 0.55, east.get_left() + UP * 0.55, color=GREY_B, stroke_width=5,
                      dash_length=0.18)
    d0, d1 = west.get_right() + UP * 0.55, east.get_left() + UP * 0.55
    piers = VGroup(*[Line(d0 + f * (d1 - d0) + DOWN * 0.02, d0 + f * (d1 - d0) + DOWN * 0.45, color=GREY_C,
                          stroke_width=3) for f in (0.25, 0.5, 0.75)])
    g = VGroup(water, west, east, tw, te, route, ferry, deck, piers)
    g.water, g.route, g.ferry, g.deck, g.piers = water, route, ferry, deck, piers
    g.bridge = VGroup(deck, piers)
    return g
