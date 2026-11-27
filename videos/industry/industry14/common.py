"""Helpers shared by the scenes of Part 14 of *Industry, Built* ("Water and Waste")."""

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

PART = 14
ASK = "Why are the businesses nobody thinks about among the steadiest there are?"
R = results()

# colour = meaning, the same in every chapter of this part
WATER, SEWAGE, WASTE, LANDFILL, RECYCLE, BURN, HAZ = "#5DA9E9", "#A38B5E", "#9AA3B2", "#8A6A45", "#7BD88F", \
    "#F2A65A", "#E8554E"
PRICE, COST, GOOD, BAD, DEBT, EQUITY = "#F6C453", "#B58CFF", "#7BD88F", "#E8554E", "#E8554E", "#7BD88F"
UK, US, BR = "#7EC8F5", "#F28B82", "#7BD88F"
PLAN_COL = {"fill": "#7EC8F5", "ceiling": "#F6C453", "expand": "#B58CFF"}
PLAN_NAME = {"fill": "Fill it fast", "ceiling": "Charge the ceiling", "expand": "Ceiling, and expand"}
SERIES_COL = {"SEHG01": WATER, "SEHG02": RECYCLE, "SEHF01": "#F6C453", "SEHF02": "#F2A65A", "SEHA": "#B58CFF",
              "SA0": "#E8EAED"}
NAMES = {"WM": "Waste Management", "RSG": "Republic", "WCN": "Waste Connections", "CWST": "Casella",
         "CLH": "Clean Harbors", "AWK": "American Water", "WTRG": "Essential Utilities", "AWR": "American States",
         "CWT": "California Water", "HTO": "H2O America", "XOM": "Exxon Mobil", "NUE": "Nucor", "DOW": "Dow",
         "MU": "Micron", "FCX": "Freeport", "DAL": "Delta"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


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


def bn(x: float, cur: str = "$", digits: int = 1) -> str:
    return f"{cur}{x:,.{digits}f}bn"
