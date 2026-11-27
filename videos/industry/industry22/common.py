"""Helpers shared by the scenes of Part 22 of *Industry, Built* ("Consumer Goods")."""

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

PART = 22
ASK = "Why can a company charge double for soap, for a hundred years?"
R = results()

BRAND, STORE, ADS, PRICE, GOOD, BAD, VOL, DRINK, FOOD, SMOKE = ("#F2A65A", "#C9D3E0", "#B58CFF", "#F6C453", "#7BD88F",
                                                                "#E8554E", "#7EC8F5", "#7EC8F5", "#F6C453", "#9AA3B2")
GROUP_COL = {"home": BRAND, "drink": DRINK, "food": GOOD, "tobacco": SMOKE}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
