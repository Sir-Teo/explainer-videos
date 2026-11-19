"""Helpers shared by the scenes of Part 16 of *Economics, Built* ("Auctions"): the chapter card, axes, curves and
the bidders' paddles."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import auctions as au  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 16
ASK = r"How should something be sold when nobody knows what it is worth to the buyers?"

ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color
CRUSOE = island.CAST["crusoe"].color
DARA = island.CAST["dara"].color
FRIDAY = island.CAST["friday"].color
EQ = E.ACCENT              # an equilibrium
HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer's bidder
FIRST = "#F2C14E"          # first-price, the Dutch clock
SECOND = "#7EC8F5"         # second-price, the English clock
ALLPAY = "#C9A0FF"         # all-pay
VALUE = "#F2788F"          # values
PRICE = "#7FD1B9"          # prices paid, revenue
RESERVE = "#F29E8E"        # the reserve price
CURSE = "#B9A7A0"          # the winner's curse
RIVALS = ("#9FB8F2", "#F2C14E", "#F2788F", "#7FD1B9")   # bidders 1-4


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


def paddle(text, color, w=1.5, h=0.62, font_size=22) -> VGroup:
    """A bidder's paddle: a rounded card with a number or name."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(text, font_size=font_size, color=color).move_to(box)
    return VGroup(box, t)


def gavel(height=0.9) -> VGroup:
    """The auction's mark: Crusoe, who sells, with a hammer drawn beside him."""
    who = islander("crusoe", height)
    head = RoundedRectangle(width=0.5, height=0.22, corner_radius=0.05, fill_color=GREY_B, fill_opacity=1,
                            stroke_width=0).rotate(-0.5)
    handle = Line(ORIGIN, DOWN * 0.55 + LEFT * 0.25, color=GREY_B, stroke_width=5)
    handle.next_to(head, DOWN, buff=-0.05)
    hammer = VGroup(handle, head).next_to(who, RIGHT, buff=0.15)
    return VGroup(who, hammer)


def tex_safe(s: str) -> str:
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def fmt(v, nd=1) -> str:
    v = float(v)
    return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.{nd}f}"
