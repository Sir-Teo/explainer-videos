"""Helpers shared by the scenes of Part 16 of *Industry, Built* ("Electronics")."""

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

PART = 16
ASK = "Why does the company that builds the device keep the least of it?"
R = results()

# colour = meaning, the same in every chapter of this part
BRAND, ASSEMBLER, PARTS, PRICE, GOOD, BAD, BOARD = "#7BD88F", "#F2A65A", "#7EC8F5", "#F6C453", "#7BD88F", "#E8554E", "#2F6B4F"
GROUP_COL = {"brand": BRAND, "assembler": ASSEMBLER, "components": PARTS}
COUNTRY_COL = {"China": "#E8554E", "India": "#F2A65A", "Vietnam": "#7BD88F", "Mexico": "#B58CFF", "Taiwan": "#7EC8F5",
               "Thailand": "#F6C453", "Malaysia": "#9AA3B2", "South Korea": "#C9D3E0", "Japan": "#E6A0C4", "other": "#5C6472"}
NAMES = {"AAPL": "Apple", "DELL": "Dell", "HPQ": "HP", "LOGI": "Logitech", "SONY": "Sony", "HONHAI": "Hon Hai (Foxconn)",
         "JBL": "Jabil", "FLEX": "Flex", "SANM": "Sanmina", "CLS": "Celestica", "PLXS": "Plexus", "BHE": "Benchmark",
         "SMCI": "Supermicro", "APH": "Amphenol", "TEL": "TE Connectivity", "GLW": "Corning", "LPL": "LG Display",
         "ASX": "ASE"}


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


def smile(width=9.0, height=3.2, depth=0.82) -> VMobject:
    """Shih's curve: value added high at both ends, low in the middle (a schematic, not data)."""
    xs = np.linspace(-1, 1, 60)
    pts = [[x * width / 2, height * (x ** 2) * depth - height * 0.42, 0] for x in xs]
    return VMobject(fill_opacity=0).set_points_smoothly(pts)
