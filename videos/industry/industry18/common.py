"""Helpers shared by the scenes of Part 18 of *Industry, Built* ("Aerospace and Defence")."""

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

PART = 18
ASK = "Why are there only two makers of large airliners, and why does the engine maker sell at a loss?"
R = results()

AIRBUS, BOEING, ENGINE, DEFENCE, SUPPLIER, PRICE, GOOD, BAD = ("#7EC8F5", "#F2A65A", "#B58CFF", "#7BD88F", "#E6A0C4",
                                                               "#F6C453", "#7BD88F", "#E8554E")
YOU, RIVAL = AIRBUS, BOEING
GROUP_COL = {"airframer": AIRBUS, "engines": ENGINE, "defence": DEFENCE, "supplier": SUPPLIER, "lessor": PRICE}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def bn(v: float, digits: int = 1) -> str:
    return ("-" if v < 0 else "") + f"${abs(v):,.{digits}f}bn"
