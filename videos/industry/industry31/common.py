"""Helpers shared by the scenes of Part 31 of *Industry, Built* ("Grocery and Mass Retail")."""

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

PART = 31
ASK = "How does a business that keeps two or three cents of every dollar become one of the largest on earth?"
R = results()

MASS, CLUB, GROCER, DOLLAR, ONLINE, CONV, GOOD, BAD, ALL, GOODS = ("#7EC8F5", "#F6C453", "#7BD88F", "#F2A65A", "#B58CFF",
                                                                  "#9FE0D0", "#7BD88F", "#E8554E", "#C9D3E0", "#C89F6A")
GROUP_COL = {"mass": MASS, "club": CLUB, "grocer": GROCER, "dollar": DOLLAR, "online": ONLINE, "convenience": CONV}
GROUP_NAME = {"mass": "mass merchants", "club": "warehouse clubs", "grocer": "supermarkets", "dollar": "dollar and discount",
              "online": "online", "convenience": "convenience"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def m(v: float) -> str:
    return f"${v / 1e6:,.2f}m"
