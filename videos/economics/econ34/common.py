"""Helpers shared by the scenes of Part 34 of *Economics, Built* ("The Open Economy"): the chapter card, axes,
curves, T-accounts and colours."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import openecon  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 34
ASK = r"What sets the price of one money in terms of another, and what can a country not have at once?"

HOLD = E.MISS              # caveats
YOU = "#7BD88F"            # you, the viewer
OUTPUT = "#7BD88F"         # output
GBP = "#E8A0B4"            # the pound
DEM = "#F2C14E"            # the mark, the euro
USD = "#7EC8F5"            # the dollar
CNY = "#F25F5C"            # the renminbi
RES = "#C9A0FF"            # reserves
RATE = "#E8A0B4"           # interest rates
CRISIS = "#F25F5C"
CALM = "#7FD1B9"
PRICE = "#F2C14E"
TRUTH_C = WHITE
RECESS = "#3A3F4B"

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


def tacct(title: str, color, assets: list, liabilities: list, width: float = 4.2, height: float = 2.0,
          font_size=18) -> VGroup:
    """A T-account: a title, a horizontal rule, a vertical rule, assets on the left and liabilities on the right.
    ``assets`` and ``liabilities`` are lists of (text, colour)."""
    head = label(title, font_size=font_size + 4, color=color)
    top = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=3)
    VGroup(head, top).arrange(DOWN, buff=0.12)
    mid = Line(top.get_center(), top.get_center() + DOWN * height, color=color, stroke_width=3)
    sides = VGroup(label(r"assets", font_size=font_size - 3, color=GREY_B),
                   label(r"liabilities", font_size=font_size - 3, color=GREY_B))
    sides[0].next_to(top, UP, buff=0.06).align_to(top, LEFT)
    sides[1].next_to(top, UP, buff=0.06).align_to(top, RIGHT)
    left = VGroup(*[label(a, font_size=font_size, color=c) for a, c in assets]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.15)
    right = VGroup(*[label(a, font_size=font_size, color=c) for a, c in liabilities]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.15)
    if len(left):
        left.next_to(top, DOWN, buff=0.2).align_to(top, LEFT).shift(RIGHT * 0.15)
    if len(right):
        right.next_to(top, DOWN, buff=0.2).align_to(mid, LEFT).shift(RIGHT * 0.15)
    g = VGroup(head, top, mid, sides, *[x for x in (left, right) if len(x)])
    g.head, g.left, g.right = head, left, right
    return g
