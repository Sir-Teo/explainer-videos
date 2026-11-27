"""Helpers shared by the scenes of Part 17 of *Industry, Built* ("Automobiles")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.ai.viz import CornerAxes, glow_dot  # noqa: F401
from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.draw import tx  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.industry.register import get, span  # noqa: F401
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 17
ASK = "Why is it so hard to make money making the most desired product of the century?"
R = results()

# colour = meaning, the same in every chapter of this part
MAKER, SUPPLIER, DEALER, FINANCE, PRICE, GOOD, BAD, EV = ("#7EC8F5", "#F2A65A", "#7BD88F", "#B58CFF", "#F6C453",
                                                         "#7BD88F", "#E8554E", "#5CE1E6")
YOU, RIVAL = "#7EC8F5", "#F2A65A"
COUNTRY_COL = {"China": "#E8554E", "Germany": "#C9D3E0", "Japan": "#E6A0C4", "South Korea": "#7EC8F5",
               "Mexico": "#7BD88F", "United States": "#F6C453", "Europe": "#B58CFF", "World": "#E8EAED",
               "Norway": "#5CE1E6", "India": "#F2A65A"}
GROUP_COL = {"volume": MAKER, "premium": PRICE, "electric": EV, "china": "#E8554E", "supplier": SUPPLIER,
             "dealer": DEALER}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def poly(pa, pts, color, width=3.0) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pa.ax.c2p(x, y) for x, y in pts])


def ghost(*mobs, opacity=0.15) -> VGroup:
    """Dim copies of what a beat will show, put up while its first sentence is spoken."""
    g = VGroup(*[m.copy() for m in mobs])
    for sm in g.get_family():
        if isinstance(sm, VMobject):
            filled = sm.get_fill_opacity() > 0
            stroked = sm.get_stroke_width() > 0 and sm.get_stroke_opacity() > 0
            sm.set_fill(opacity=opacity if filled else 0)
            sm.set_stroke(opacity=opacity if stroked else 0)
        elif hasattr(sm, "set_opacity"):
            sm.set_opacity(opacity)
    return g


def usd(x: float, digits: int = 0) -> str:
    """A dollar amount with a sign before the symbol: -$4,806."""
    return ("-" if x < 0 else "") + f"${abs(x):,.{digits}f}"


def say_usd(x: float) -> str:
    """A dollar amount for narration, rounded the way a person says it."""
    a = abs(x)
    if a >= 1e9:
        s = f"{a / 1e9:.1f} billion dollars"
    elif a >= 1e6:
        s = f"{a / 1e6:.0f} million dollars"
    elif a >= 10_000:
        s = f"{round(a, -3):,.0f} dollars"
    else:
        s = f"{round(a, -2):,.0f} dollars"
    return ("minus " if x < 0 else "") + s


def bar(x0, y, length, h, color, opacity=0.9) -> Rectangle:
    """A horizontal bar starting at x0 (negative lengths go left)."""
    r = Rectangle(width=max(abs(length), 0.01), height=h, stroke_width=0, fill_color=color, fill_opacity=opacity)
    return r.move_to([x0 + length / 2, y, 0])


def xlab(pa, text: str, size: float = 13) -> Mobject:
    """An x-axis title under the tick labels (for axes whose x axis crosses the middle, at y = 0)."""
    ax = pa.ax
    x0, x1 = ax.x_range[0], ax.x_range[1]
    return tx(text, size, GREY_B).next_to(ax.c2p((x0 + x1) / 2, ax.y_range[0]), DOWN, buff=0.55)
