"""Helpers shared by the scenes of Part 19 of *Industry, Built* ("Machinery")."""

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

PART = 19
ASK = "How do the companies that make the machines earn more from them after the sale than at it?"
R = results()

MACHINE, SERVICE, PRICE, GOOD, BAD, ROBOT, CHINA, BLUE = ("#F6C453", "#7BD88F", "#F2A65A", "#7BD88F", "#E8554E", "#B58CFF",
                                                           "#E8554E", "#7EC8F5")
YOU, RIVAL = BLUE, PRICE
GROUP_COL = {"construction": MACHINE, "farm": "#A3D977", "components": "#C9D3E0", "buildings": BLUE, "automation": ROBOT,
             "conglomerate": "#E6A0C4", "rental": PRICE}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def bn(v: float, digits: int = 1) -> str:
    return ("-" if v < 0 else "") + f"${abs(v):,.{digits}f}bn"
