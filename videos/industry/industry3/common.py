"""Helpers shared by the scenes of Part 3 of *Industry, Built* ("The Accounts")."""

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

PART = 3
ASK = "What do a company's accounts say about the business underneath?"
R = results()

# One colour per company, the same in every chapter of this part
CO = {"cost": "#E8554E", "msft": "#4FA3F7", "jpm": "#B58CFF", "nee": "#7BD88F", "dal": "#F2A65A", "lly": "#F2C14E"}
OWN, OWE, OWNER = "#7EC8F5", "#F2A65A", "#7BD88F"  # what a business has; what it owes; what its owners put in


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def usd(x: float, digits: int = 0) -> str:
    """$13,509 for the screen."""
    return f"${x:,.{digits}f}"


def bn(x: float, digits: int = 1) -> str:
    """$115.9bn for the screen, from billions."""
    return f"${x:,.{digits}f}bn"


def say_usd(x: float) -> str:
    """For the narrator: 13509 -> '13,509 dollars'."""
    return f"{x:,.0f} dollars"


def name(k: str) -> str:
    return R["six"][k]["name"]
