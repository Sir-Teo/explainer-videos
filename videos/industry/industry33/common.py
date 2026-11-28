"""Helpers shared by the scenes of Part 33 of *Industry, Built* ("The Middlemen")."""

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

PART = 33
ASK = "If the internet removes the middleman, why are the middlemen among the largest companies in every country?"
R = results()

DRUG, FOOD, TECH, IND, CROP, TRADE, GOOD, BAD, ALL, GOODS = ("#7EC8F5", "#7BD88F", "#B58CFF", "#F2A65A", "#C89F6A", "#F6C453",
                                                            "#7BD88F", "#E8554E", "#C9D3E0", "#C89F6A")
GROUP_COL = {"drugs": DRUG, "food": FOOD, "tech": TECH, "industrial": IND, "crops": CROP, "trading": TRADE}
GROUP_NAME = {"drugs": "drugs and medical", "food": "food service", "tech": "electronics and IT", "industrial": "industrial and trade supply",
              "crops": "crop traders", "trading": "Japanese trading house"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def m(v: float) -> str:
    return f"{'-' if v < 0 else ''}${abs(v) / 1e6:,.0f}m"


def near(d: dict, x: float):
    return min(d, key=lambda k: abs(k - x))
