"""Helpers shared by the scenes of Part 2 of *Industry, Built* ("The Economy on One Page")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.ai.viz import CornerAxes, glow_dot  # noqa: F401
from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 2
ASK = "How big is each industry, and compared with what?"
R = results()

# One colour per broad group of sectors, the same in every chapter of this part
GROUP = {"goods": "#F2A65A", "trade": "#7EC8F5", "info": "#B58CFF", "finance": "#F2C14E", "services": "#4FD1C5",
         "people": "#7BD88F", "government": "#8B95A7"}
SECTOR_GROUP = {
    "Farms, forestry, fishing": "goods", "Mining": "goods", "Utilities": "goods", "Construction": "goods",
    "Manufacturing": "goods", "Wholesale trade": "trade", "Retail trade": "trade",
    "Transportation and warehousing": "trade", "Information": "info", "Finance and insurance": "finance",
    "Real estate": "finance", "Professional and technical services": "services", "Management of companies": "services",
    "Administrative and waste services": "services", "Educational services": "people",
    "Health care and social assistance": "people", "Arts and recreation": "people", "Hotels and restaurants": "people",
    "Other services": "people", "Government": "government",
}
SHORT = {"Farms, forestry, fishing": "Farms", "Transportation and warehousing": "Transport",
         "Professional and technical services": "Professional services", "Management of companies": "Head offices",
         "Administrative and waste services": "Admin and waste", "Educational services": "Education",
         "Health care and social assistance": "Health care", "Arts and recreation": "Arts",
         "Hotels and restaurants": "Hotels, restaurants"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def gcol(sector: str) -> str:
    return GROUP[SECTOR_GROUP.get(sector, "government")]


def short(sector: str) -> str:
    return SHORT.get(sector, sector)


def bil(x: float) -> str:
    """$2,930bn / $30.9tn for the screen, from billions."""
    return f"${x / 1e3:.1f}tn" if x >= 1e3 else f"${x:,.0f}bn"
