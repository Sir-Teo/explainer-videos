"""Helpers shared by the scenes of Part 28 of *Industry, Built* ("Airlines")."""

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

PART = 28
ASK = "Why has an industry that changed the world lost money over most of its history?"
R = results()

SKY, LEISURE, BIZ, FUEL, CASH, GOOD, BAD, SEAT, CARD, ALL = ("#7EC8F5", "#7BD88F", "#F6C453", "#B58CFF", "#F2A65A", "#7BD88F",
                                                            "#E8554E", "#2E3645", "#F2A7B5", "#C9D3E0")
GROUP_COL = {"network": "#7EC8F5", "lowcost": "#F2A65A", "ulcc": "#E8554E", "regional": "#9FE0D0", "foreign": "#B58CFF",
             "lessor": "#7BD88F", "systems": "#C9D3E0"}
GROUP_NAME = {"network": "network airlines", "lowcost": "low-cost", "ulcc": "ultra-low-cost", "regional": "regional",
              "foreign": "outside America", "lessor": "aircraft lessors", "systems": "booking systems"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def fill(cab, leisure: int, business: int, empty_col: str = SEAT):
    """Colour a cabin's seats: business travellers at the front, then leisure, the rest empty."""
    for i, s in enumerate(cab.seats):
        s.set_fill(BIZ if i < business else (LEISURE if i < business + leisure else empty_col))


def usd(v: float) -> str:
    """A signed dollar amount, sign first: +$5,457 or -$5,028."""
    return f"{'+' if v >= 0 else '-'}${abs(v):,.0f}"
