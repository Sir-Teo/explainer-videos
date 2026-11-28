"""Helpers shared by the scenes of Part 30 of *Industry, Built* ("Telecoms")."""

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

PART = 30
ASK = "Why do the companies that carry everything capture so little of what it is worth?"
R = results()

WIRELESS, CABLE, WIRE, TOWER, OVER, GOOD, BAD, ALL, FOREIGN, EQUIP, SAT = (
    "#7EC8F5", "#B58CFF", "#C9D3E0", "#F6C453", "#7BD88F", "#7BD88F", "#E8554E", "#C9D3E0", "#F2A65A", "#9FE0D0", "#F2A7B5")
YOU, RIVALS = "#F6C453", ("#7EC8F5", "#B58CFF", "#F2A65A")
GROUP_COL = {"wireless": WIRELESS, "cable": CABLE, "wireline": WIRE, "towers": TOWER, "foreign": FOREIGN, "equipment": EQUIP,
             "satellite": SAT}
GROUP_NAME = {"wireless": "wireless carriers", "cable": "cable", "wireline": "wireline", "towers": "tower companies",
              "foreign": "outside the US", "equipment": "equipment", "satellite": "satellite"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def bn(v: float, d: int = 2) -> str:
    return f"${v:,.{d}f}bn"
