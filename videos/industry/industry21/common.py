"""Helpers shared by the scenes of Part 21 of *Industry, Built* ("Medical Technology")."""

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

PART = 21
ASK = "Who is the customer when the one who uses it, the one who chooses it and the one who pays are three different people?"
R = results()

DEVICE, IMAGING, TOOLS, LABS, PRICE, GOOD, BAD, PAYER, SURGEON = ("#7EC8F5", "#B58CFF", "#7BD88F", "#F2A65A", "#F6C453",
                                                                  "#7BD88F", "#E8554E", "#F2A65A", "#7EC8F5")
GROUP_COL = {"devices": DEVICE, "imaging": IMAGING, "tools": TOOLS, "labs": LABS}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
