"""Helpers shared by the scenes of Part 24 of *Industry, Built* ("Construction")."""

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

PART = 24
ASK = "Why has almost everything become cheaper to make, except a building?"
R = results()

BUILD, MAKE, ALL, PRICE, GOOD, BAD, YOU, RIVAL, CASH, PROFIT = ("#F6C453", "#7EC8F5", "#C9D3E0", "#F6C453", "#7BD88F",
                                                                "#E8554E", "#F6C453", "#9AA3B2", "#7BD88F", "#F2A65A")
GROUP_COL = {"trade": "#F6C453", "general": "#F2A65A", "engineer": "#7EC8F5", "materials": "#B58CFF", "rental": "#7BD88F",
             "concession": "#F2A7B5"}
GROUP_NAME = {"trade": "specialty contractors", "general": "general contractors", "engineer": "engineers",
              "materials": "materials", "rental": "equipment rental", "concession": "concessions"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
