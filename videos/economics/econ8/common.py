"""Helpers shared by the scenes of Part 8 of *Economics, Built* ("The Firm")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import firm as fm  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 8
ASK = r"How does a firm decide what to make and how, and why is there a firm at all?"

OUT = "#F6C453"         # output
LAB = "#7EC8F5"         # labour
CAP = "#F28C6F"         # capital
ISO = "#C9A0FF"         # an isoquant
COST = "#7BD88F"        # an isocost line, a cost curve
MC = WHITE              # marginal cost
ATC = "#F2A65A"         # average total cost
AVC = "#5BD1C4"         # average variable cost
PRICE = E.ACCENT        # a price line
MARKET = "#9FB8F2"      # the market (Coase)
FIRM = "#E9A3C9"        # the firm (Coase)
HOLD = E.MISS           # hold-up
PASS = E.TRUTH
WHO = {k: island.CAST[k].color for k in ("crusoe", "friday", "ana", "bo", "chidi", "dara")}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("firm",), horizon=("a year",),
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


def slipway(width: float = 1.2, color="#9C7A4B") -> VGroup:
    """A slipway with a hull on it: the boatyard's capital."""
    ramp = Polygon([-width / 2, -0.15, 0], [width / 2, -0.15, 0], [width / 2 + 0.25, -0.35, 0],
                   [-width / 2 - 0.25, -0.35, 0], stroke_color=color, stroke_width=2, fill_color=color,
                   fill_opacity=0.5)
    hull = VMobject(stroke_color=WHITE, stroke_width=2.5, fill_color="#5DADEC", fill_opacity=0.35)
    hull.set_points_as_corners([[-width * 0.42, 0.25, 0], [width * 0.42, 0.25, 0], [width * 0.3, -0.12, 0],
                                [-width * 0.3, -0.12, 0], [-width * 0.42, 0.25, 0]])
    return VGroup(ramp, hull)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def signed(x: float, digits: int = 2) -> str:
    v = round(x, digits)
    if v == 0:
        return f"{0.0:.{digits}f}"
    return ("$+$" if v > 0 else "$-$") + f"{abs(v):.{digits}f}"
