"""Helpers shared by the scenes of Part 15 of *Industry, Built* ("Semiconductors")."""

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

PART = 15
ASK = "Why do the most advanced chips come from so few factories?"
R = results()

# colour = meaning, the same in every chapter of this part
SILICON, LIGHT, DIE, DEFECT, GOOD, BAD, PRICE = "#9AA3B2", "#B58CFF", "#7EC8F5", "#E8554E", "#7BD88F", "#E8554E", "#F6C453"
GROUP_COL = {"foundry": "#7EC8F5", "integrated": "#9AA3B2", "fabless": "#7BD88F", "memory": "#F2A65A",
             "equipment": "#B58CFF", "design software": "#F6C453", "packaging": "#C9732F"}
NAMES = {"TSM": "TSMC", "GFS": "GlobalFoundries", "UMC": "UMC", "INTC": "Intel", "TXN": "Texas Instruments",
         "ADI": "Analog Devices", "MCHP": "Microchip", "ON": "onsemi", "NXPI": "NXP", "STM": "STMicro", "NVDA": "Nvidia",
         "AVGO": "Broadcom", "QCOM": "Qualcomm", "AMD": "AMD", "MRVL": "Marvell", "MU": "Micron", "AMAT": "Applied Materials",
         "LRCX": "Lam Research", "KLAC": "KLA", "SNPS": "Synopsys", "CDNS": "Cadence", "AMKR": "Amkor", "ASML": "ASML"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def poly(pa, pts, color, width=3.0) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pa.ax.c2p(x, y) for x, y in pts])


def ghost(*mobs, opacity=0.15) -> VGroup:
    """Dim copies of what a beat will show, put up while its first sentence is spoken."""
    g = VGroup(*[m.copy() for m in mobs])
    g.set_opacity(opacity)
    return g
