"""Helpers shared by the scenes of Part 23 of *Industry, Built* ("Fashion and Luxury")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.beats import (beat, bullets, callout, dumbbell, ghost, hbars, head, hline,  # noqa: F401
                                      line_chart, marker, poly, quote, stat_cards, table, vbars)
from explainer.industry.draw import tx  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.industry.register import get, span  # noqa: F401
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 23
ASK = "How do two industries that sell clothes run on opposite rules?"
R = results()

FAST, LUX, SPORT, OFF, DEPT, BRANDC, PRICE, GOOD, BAD, CLEAR = ("#7EC8F5", "#F2A65A", "#7BD88F", "#B58CFF", "#9AA3B2",
                                                                "#F2A7B5", "#F6C453", "#7BD88F", "#E8554E", "#C9D3E0")
FAR, NEAR, CHASE = ("#9AA3B2", "#7EC8F5", "#F6C453")
GROUP_COL = {"sport": SPORT, "brand": BRANDC, "luxury": LUX, "store": FAST, "off": OFF, "dept": DEPT}
LEATHER = "#C8752E"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def eur(v: float) -> str:
    return f"€{v:.1f}bn"
