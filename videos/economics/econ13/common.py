"""Helpers shared by the scenes of Part 13 of *Economics, Built* ("Lemons and Signals"): the chapter card,
axes and curves for markets where one side knows more."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import info  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 13
ASK = r"What happens to a market when one side knows more than the other?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
EQ = E.ACCENT              # an equilibrium
HOLD = E.MISS              # caveats
GOOD = "#7BD88F"           # good quality, low risk
LEMON = "#F2C14E"          # lemons, high risk
SIGNAL = "#7EC8F5"         # a signal, a screen
POOL = "#C9A0FF"           # pooling
LOSS = "#F2788F"           # welfare lost
USED = "#F2A65A"           # used cars
NEW = "#9FB8F2"            # new cars


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("person", "market"), horizon=("a year",),
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


def seg(ax, x0, y0, x1, y1, color=WHITE, width=3.0, dashed=False):
    a = ax.ax
    cls = DashedLine if dashed else Line
    return cls(a.c2p(x0, y0), a.c2p(x1, y1), color=color, stroke_width=width)


def pair(a="bo", b="ana", height=0.9):
    """Two islanders side by side: by default Bo, who sells, and Ana, who buys."""
    return VGroup(islander(a, height), islander(b, height)).arrange(RIGHT, buff=0.9)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def fmt(v, nd=1) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.{nd}f}"
