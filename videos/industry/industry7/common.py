"""Helpers shared by the scenes of Part 7 of *Industry, Built* ("Sizing a Market")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.ai.viz import CornerAxes, glow_dot  # noqa: F401
from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.draw import tx  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 7
ASK = "How big is a market, and how would anyone know?"
R = results()

# colour = meaning, the same in every chapter of this part
TAM, FACTORY, RETAIL, UNITS, GUESS = "#F6C453", "#7EC8F5", "#7BD88F", "#B58CFF", "#F2A65A"
STONE = "#C9D3E0"
WATER = "#5DA9E9"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def money(v: float, unit: str = "bn") -> str:
    return ("-" if v < 0 else "") + f"${abs(v):,.1f}{unit}"
