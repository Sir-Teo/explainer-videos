"""Helpers shared by the scenes of Part 17 of *Economics, Built* ("Markets by Design"): the chapter card, axes, curves, the
matching board and the islanders' cards."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import matching as mt  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 17
ASK = r"Can a market be engineered, when prices cannot do the work?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
EQ = E.ACCENT              # an equilibrium
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
PROPOSE = "#7EC8F5"        # proposals, the proposing side
HELD = "#F2C14E"           # held offers, tentative
REJECT = "#F2788F"         # rejections, blocking pairs
STABLE = "#7FD1B9"         # stable, final
MECH = "#C9A0FF"           # mechanisms, the designer
MONEY = "#F29E8E"          # payments, taxes
KIDNEY = "#E8A0B4"         # patients and donors
SCHOOL = "#9FB8F2"         # schools
PLACES = {"boatyard": "#E8C07D", "kiln": "#F29E8E", "loft": "#7FD1B9", "grove": "#C8E07A"}
PLACE_NAMES = {"boatyard": "the boatyard", "kiln": "the kiln", "loft": "the net loft", "grove": "the grove"}


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


def place_chip(key, w=2.2, h=0.62, font_size=22) -> VGroup:
    """A workshop's name on a coloured card."""
    c = PLACES[key]
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=c, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(PLACE_NAMES[key], font_size=font_size, color=c).move_to(box)
    return VGroup(box, t)


def who_chip(key, height=0.55, font_size=20) -> VGroup:
    """An islander with a name under them."""
    name = "you" if key == "you" else island.CAST[key].name
    fig = person(height, color=YOU) if key == "you" else islander(key, height)
    col = YOU if key == "you" else island.CAST[key].color
    return VGroup(fig, label(name, font_size=font_size, color=col)).arrange(DOWN, buff=0.06)


def color_of(key):
    return YOU if key == "you" else island.CAST[key].color


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def fmt(v, nd=1) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.{nd}f}"
