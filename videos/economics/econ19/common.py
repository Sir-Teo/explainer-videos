"""Helpers shared by the scenes of Part 19 of *Economics, Built* ("The Great Escape"): the chapter card, axes, curves
and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import malthus as ml  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 19
ASK = r"Why was almost everyone poor for almost all of history, and what changed?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
WAGE = "#F2C14E"           # real wages
GDP = "#7EC8F5"            # income (GDP) per head
POP = "#F2788F"            # population
BIRTH = "#7BD88F"          # births
DEATH = "#F29E8E"          # deaths
TECH = "#C9A0FF"           # technology
EDU = "#9FB8F2"            # education
LIFE = "#E8A0B4"           # life expectancy
HEIGHT = "#7FD1B9"         # heights
CN = "#F25F5C"             # China
UK = "#7EC8F5"             # Britain
NL = "#F2C14E"             # the Netherlands
IT = "#7BD88F"             # Italy
JP = "#C9A0FF"             # Japan
IN = "#F29E8E"             # India
COUNTRY = {"GBR": (r"Britain", UK), "NLD": (r"the Netherlands", NL), "ITA": (r"Italy", IT), "CHN": (r"China", CN),
           "JPN": (r"Japan", JP), "IND": (r"India", IN), "USA": (r"United States", "#9FB8F2"),
           "NGA": (r"Nigeria", "#7FD1B9"), "KOR": (r"South Korea", "#F7D154")}


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("nation",), horizon=("a century",),
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


def color_of(key):
    return YOU if key == "you" else island.CAST[key].color


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def fmt(v, nd=1) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.{nd}f}"


def ordinal(n: int) -> str:
    """4 -> '4th', 43 -> '43rd', 111 -> '111th'."""
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def log_axis(ax, xs, ys, color, width=3.0):
    """A curve on axes whose y range is in log10 units."""
    return path(ax, xs, [np.log10(v) if v and v > 0 else np.nan for v in ys], color=color, width=width, smooth=False)

