"""Helpers shared by the scenes of Part 36 of *Industry, Built* ("Software")."""

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

PART = 36
ASK = "What is a business worth when the second copy costs nothing?"
R = results()

SUB, LIC, SALES, ENG, HOST, GA, PROFIT, LOSS, STOCK, ALL, AI = ("#7EC8F5", "#F2A65A", "#FF8FB1", "#B58CFF", "#9AA3B2", "#C9D3E0",
                                                                "#7BD88F", "#E8554E", "#F6C453", "#C9D3E0", "#9FE0D0")
GROUP_COL = {"platform": "#F6C453", "apps": "#7EC8F5", "design": "#F2A65A", "dev": "#B58CFF", "data": "#9FE0D0", "security": "#FF8FB1"}
GROUP_NAME = {"platform": "platforms", "apps": "applications", "design": "design tools", "dev": "developer tools",
              "data": "data", "security": "security"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mn(v: float, d: int = 0) -> str:
    return f"{'-' if v < 0 else ''}${abs(v) / 1e6:,.{d}f}m"


def bn(v: float, d: int = 1) -> str:
    return f"{'-' if v < 0 else ''}${abs(v):,.{d}f}bn"
