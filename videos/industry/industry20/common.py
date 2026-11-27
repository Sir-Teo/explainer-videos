"""Helpers shared by the scenes of Part 20 of *Industry, Built* ("Pharmaceuticals")."""

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

PART = 20
ASK = "Why does a pill that costs cents to make sell for dollars, and then one day for cents?"
R = results()

BRAND, GENERIC, LAB, PRICE, GOOD, BAD, BIO, GOV = ("#B58CFF", "#C9D3E0", "#7BD88F", "#F6C453", "#7BD88F", "#E8554E",
                                                   "#7EC8F5", "#F2A65A")
GROUP_COL = {"large": BRAND, "biotech": BIO, "generics": GENERIC}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
