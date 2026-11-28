"""Helpers shared by the scenes of Part 35 of *Industry, Built* ("Travel and Hotels")."""

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

PART = 35
ASK = "Why do the biggest hotel companies own almost no hotels?"
R = results()

BRAND, OWNER, AGENT, CRUISE, CASINO, PARK, GOOD, BAD, ALL, STAFF, FIXC, FEE = (
    "#F6C453", "#7EC8F5", "#FF8FB1", "#7BD8D0", "#F2A65A", "#B58CFF", "#7BD88F", "#E8554E", "#C9D3E0", "#9FE0D0", "#9AA3B2",
    "#F2C14E")
GROUP_COL = {"brand": BRAND, "owner": OWNER, "agent": AGENT, "cruise": CRUISE, "casino": CASINO, "park": PARK}
GROUP_NAME = {"brand": "hotel brands", "owner": "hotel owners", "agent": "online travel", "cruise": "cruise lines",
              "casino": "casinos and betting", "park": "parks and timeshare"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def m(v: float, d: int = 2) -> str:
    """Dollars in millions: 2.877e6 -> '$2.88m'."""
    return f"{'-' if v < 0 else ''}${abs(v) / 1e6:,.{d}f}m"


def bn(v: float, d: int = 1) -> str:
    return f"{'-' if v < 0 else ''}${abs(v):,.{d}f}bn"
