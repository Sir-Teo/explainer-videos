"""Helpers shared by the scenes of Part 5 of *Economics, Built* ("What People Want")."""

from __future__ import annotations

import numpy as np

from explainer.economics import *  # noqa: F403
from explainer.economics.agora import consumer as cs  # noqa: F401
from explainer.economics.data import tables  # noqa: F401
from explainer.economics.kit import chapter, dollars, money_words, pct, say_num, say_pct, year_axis  # noqa: F401

from .compute import FILM_SECONDS, INCOME, film_time, load  # noqa: F401

PART = 5
ASK = r"Can you tell what someone wants from what they buy?"

FISHC = E.FISH          # fish, on the horizontal axis
COCO = E.COCONUT        # coconuts, on the vertical axis
BUDGET = "#F6C453"      # a budget line
IC = "#7EC8F5"          # an indifference curve
CHOICE = WHITE          # a chosen bundle
VIOL = E.MISS           # a revealed-preference violation
PASS = E.TRUTH          # consistent with utility maximization
RANDOM = GREY_B         # a random chooser
WHO = {k: island.CAST[k].color for k in ("bo", "ana", "chidi", "dara")}


def card(scene, n: int, title: str, question: str, say: str, lit=("households",), scale=("person",),
         horizon=("a day",), hold: float = 0.0):
    """The chapter card of this part, narrated, then cleared."""
    chapter(scene, PART, ASK, n, title, question, say, lit=lit, scale=scale, horizon=horizon, hold=hold)


def goods_axes(center=ORIGIN, top=13.0, x_length=5.2, y_length=5.2, font_size=19, xlabel=r"fish",
               ylabel=r"coconuts", ticks=(0, 4, 8, 12)):
    """Fish across, coconuts up: the plane every chapter of this part draws in."""
    from explainer.ai.viz import axes

    return axes([0, top], [0, top], x_length=x_length, y_length=y_length, xticks=list(ticks), yticks=list(ticks),
                xlabel=xlabel, ylabel=ylabel, font_size=font_size, center=center)


def budget_line(ax, A: float, B: float, color=BUDGET, width=3.0, opacity=1.0):
    """The budget line from (A, 0) to (0, B): A fish or B coconuts, or anything between."""
    a = ax.ax
    return Line(a.c2p(A, 0), a.c2p(0, B), color=color, stroke_width=width, stroke_opacity=opacity)


def curve(ax, xs, ys, color=IC, width=3.0, top=13.0, dashed=False):
    """A curve y(x) on goods axes, clipped to the frame."""
    a = ax.ax
    pts = [a.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y) and 0 <= y <= top and 0 <= x <= top]
    ln = VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts) if len(pts) > 3 else VMobject()
    return DashedVMobject(ln, num_dashes=40) if dashed and len(pts) > 3 else ln


def poly(ax, pts, color=IC, width=3.0, top=13.0):
    """A polyline through (x, y) points on goods axes, keeping only those inside the frame."""
    a = ax.ax
    keep = [a.c2p(x, y) for x, y in pts if np.isfinite(x) and np.isfinite(y) and 0 <= x <= top and 0 <= y <= top]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(keep) if len(keep) > 1 else VMobject()
