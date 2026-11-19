"""Helpers shared by the scenes of Part 6 of *Economics, Built* ("Demand")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import demand as dm  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, film_time, load  # noqa: F401

PART = 6
ASK = r"When a price changes, what happens to what people buy, and to how well off they are?"

FISHC = E.FISH          # fish, on the horizontal axis
COCO = E.COCONUT        # coconuts, on the vertical axis
BUDGET = "#F6C453"      # a budget line
NEWB = "#F2A65A"        # the budget line after the change
IC = "#7EC8F5"          # an indifference curve
CAL = "#7BD88F"         # the calorie line
SUB = "#C9A0FF"         # the substitution effect
INC = "#F28C6F"         # the income effect
MARSH = WHITE           # Marshall's (ordinary) demand
HICKS = "#5BD1C4"       # Hicks's (compensated) demand
CHOICE = WHITE          # a chosen bundle
GIFF = E.MISS           # Giffen behaviour
PASS = E.TRUTH          # a gain, a check that passes
ZONE = {"standard": IC, "subsistence": GIFF, "deprived": GREY_B}
WHO = {k: island.CAST[k].color for k in ("bo", "ana", "chidi", "dara")}


def card(scene, n: int, title: str, question: str, say: str, lit=("households",), scale=("person",),
         horizon=("a year",), hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def goods_axes(center=ORIGIN, top=13.0, x_length=5.2, y_length=5.2, font_size=19, xlabel=r"fish",
               ylabel=r"coconuts", ticks=(0, 4, 8, 12), xtop=None):
    """Fish across, coconuts up: the plane of Part 5, again."""
    from explainer.ai.viz import axes

    xt = top if xtop is None else xtop
    return axes([0, xt], [0, top], x_length=x_length, y_length=y_length, xticks=list(ticks), yticks=list(ticks),
                xlabel=xlabel, ylabel=ylabel, font_size=font_size, center=center)


def budget_line(ax, A: float, B: float, color=BUDGET, width=3.0, opacity=1.0):
    """The budget line from (A, 0) to (0, B): A fish or B coconuts, or anything between."""
    a = ax.ax
    return Line(a.c2p(A, 0), a.c2p(0, B), color=color, stroke_width=width, stroke_opacity=opacity)


def curve(ax, xs, ys, color=IC, width=3.0, top=13.0, xtop=None, dashed=False):
    """A curve y(x) on goods axes, clipped to the frame."""
    a = ax.ax
    xt = top if xtop is None else xtop
    pts = [a.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y) and 0 <= y <= top and 0 <= x <= xt]
    ln = VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts) if len(pts) > 3 else VMobject()
    return DashedVMobject(ln, num_dashes=40) if dashed and len(pts) > 3 else ln


def poly(ax, pts, color=IC, width=3.0, top=13.0, xtop=None):
    """A polyline through (x, y) points, keeping only those inside the frame."""
    a = ax.ax
    xt = top if xtop is None else xtop
    keep = [a.c2p(x, y) for x, y in pts if np.isfinite(x) and np.isfinite(y) and 0 <= x <= xt and 0 <= y <= top]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(keep) if len(keep) > 1 else VMobject()


def arrow_between(ax, p, q, color, width=5, buff=0.08, tip=0.18):
    """An arrow from bundle p to bundle q on goods axes."""
    a = ax.ax
    return Arrow(a.c2p(*p), a.c2p(*q), color=color, stroke_width=width, buff=buff, max_tip_length_to_length_ratio=0.35,
                 tip_length=tip)


def zone_band(ax, x0, x1, y0, y1, color, label_text, font_size=17, opacity=0.10):
    """A shaded band on an axis between x0 and x1 (from y0 to y1 in data units), labelled at its top."""
    a = ax.ax
    r = Polygon(a.c2p(x0, y0), a.c2p(x1, y0), a.c2p(x1, y1), a.c2p(x0, y1), stroke_width=0, fill_color=color,
                fill_opacity=opacity)
    t = label(label_text, font_size=font_size, color=color).move_to(a.c2p((x0 + x1) / 2, y1)).shift(DOWN * 0.22)
    return VGroup(r, t)


def tex_safe(s: str) -> str:
    """Plain text (a citation, a dial's sample) made safe for a Tex label."""
    for ch, rep in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(ch, rep)
    return s


def signed(x: float, digits: int = 2) -> str:
    """+0.34, -0.61, and 0.00 (never -0.00), for the screen."""
    v = round(x, digits)
    return f"{0.0:.{digits}f}" if v == 0 else f"{v:+.{digits}f}"
