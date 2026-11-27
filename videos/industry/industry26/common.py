"""Helpers shared by the scenes of Part 26 of *Industry, Built* ("Property")."""

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

PART = 26
ASK = "What is a building worth, and why does that number move so much when the building does not?"
R = results()

OFFICE, SHED, SHOP, INCOME, RATE, VALUE, LOAN, GOOD, BAD, ALL = ("#7EC8F5", "#F2A65A", "#F2A7B5", "#7BD88F", "#B58CFF",
                                                                 "#F6C453", "#F28C8C", "#7BD88F", "#E8554E", "#C9D3E0")
GROUP_COL = {"industrial": "#F2A65A", "towers": "#9FE0D0", "data": "#4FB0E6", "retail": "#F2A7B5", "office": "#7EC8F5",
             "homes": "#B58CFF", "storage": "#D9B382", "health": "#E8D26E", "manager": "#F6C453", "services": "#C9D3E0",
             "lender": "#F28C8C"}
GROUP_NAME = {"industrial": "warehouses", "towers": "towers", "data": "data centres", "retail": "shops and malls",
              "office": "offices", "homes": "flats", "storage": "self-storage", "health": "senior housing",
              "manager": "managers", "services": "services", "lender": "lenders"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def m(v: float, d: int = 1) -> str:
    """$ million, e.g. m(39.73) -> '$39.7m'."""
    return f"${v:,.{d}f}m"
