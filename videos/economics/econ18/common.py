"""Helpers shared by the scenes of Part 18 of *Economics, Built* ("Social Choice and Welfare"): the chapter card, axes, curves, the
ballots and the islanders' cards."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import choice as ch  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 18
ASK = r"Can the wants of many people be added up into what society wants?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
EQ = E.ACCENT              # an equilibrium
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
VOTE = {"A": "#F2C14E", "B": "#7EC8F5", "C": "#F2788F", "D": "#7BD88F", "E": "#C9A0FF"}
PLAN = {"A": "a feast of fish", "B": "a feast of fruit", "C": "a dance", "D": "a boat race", "E": "a market fair"}
CYCLE = "#F2788F"          # cycles, paradoxes
RULE = "#9FB8F2"           # rules, axioms
WELF = "#7FD1B9"           # welfare, utility
RAWLS = "#F29E8E"          # the worst-off
HARS = "#7EC8F5"           # the average
MONEY = "#F2C14E"          # money, willingness to pay
LIFE = "#E8A0B4"           # lives, risks


def card(scene, n: int, title: str, question: str, say: str, lit=(), scale=("person", "market"), horizon=("a day",),
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


def ballot(ranking, count=None, w=1.25, font_size=22) -> VGroup:
    """A ballot: the plans in order, best on top, with how many islanders cast it."""
    rows = VGroup(*[label(c, font_size=font_size, color=VOTE[c]) for c in ranking]).arrange(DOWN, buff=0.12)
    box = RoundedRectangle(width=w, height=rows.height + 0.4, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2)
    rows.move_to(box)
    g = VGroup(box, rows)
    if count is not None:
        g.add(label(rf"{count}", font_size=font_size + 2, color=WHITE).next_to(box, UP, buff=0.12))
    return g


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
