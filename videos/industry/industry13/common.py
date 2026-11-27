"""Helpers shared by the scenes of Part 13 of *Industry, Built* ("Electricity")."""

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

PART = 13
ASK = "How is a product that cannot be stored sold every second, and who pays for the wires?"
R = results()

# colour = meaning, the same in every chapter of this part
GAS, COAL, NUKE, WIND, SUN, HYDRO, STORE, OTHER = "#F2A65A", "#8C929B", "#B58CFF", "#7EC8F5", "#F6C453", "#5DA9E9", \
    "#7BD88F", "#5D6B82"
DEMAND, PRICE, COST, GOOD, BAD = "#E8EAED", "#F6C453", "#B58CFF", "#7BD88F", "#E8554E"
TEXAS, CALI, UK = "#F28B82", "#F6C453", "#7EC8F5"
FUEL_COL = {"gas": GAS, "coal": COAL, "nuclear": NUKE, "wind": WIND, "solar": SUN, "hydro": HYDRO, "battery": STORE,
            "other": OTHER, "oil": "#C9732F"}
FUEL_NAME = {"gas": "natural gas", "coal": "coal", "nuclear": "nuclear", "wind": "wind", "solar": "solar",
             "hydro": "hydro", "battery": "batteries", "other": "other", "oil": "oil"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mw(x: float) -> str:
    return f"{x / 1000:,.1f} GW" if abs(x) >= 1000 else f"{x:,.0f} MW"


def poly(pa, pts, color, width=3.0) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pa.ax.c2p(x, y) for x, y in pts])


def stack(pa, xs, layers, colors, opacity=0.85) -> VGroup:
    """Stacked areas: ``layers`` is a list of lists (bottom first), one value per x."""
    below = [0.0] * len(xs)
    g = VGroup()
    for vals, col in zip(layers, colors):
        top = [b + max(v or 0.0, 0.0) for b, v in zip(below, vals)]
        g.add(Polygon(*[pa.ax.c2p(x, t) for x, t in zip(xs, top)], *[pa.ax.c2p(x, b) for x, b in zip(reversed(xs), reversed(below))],
                      stroke_width=0, fill_color=col, fill_opacity=opacity))
        below = top
    return g
