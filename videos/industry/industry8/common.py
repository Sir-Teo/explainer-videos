"""Helpers shared by the scenes of Part 8 of *Industry, Built* ("Oil and Gas")."""

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

PART = 8
ASK = "What does a barrel cost, and who decides what it sells for?"
R = results()

# colour = meaning, the same in every chapter of this part
CRUDE, BRENT, WTI, GAS, STATE = "#C8875A", "#7EC8F5", "#F2A65A", "#7BD88F", "#E8554E"
COST, PRICE, SHALE, OPEC = "#B58CFF", "#F6C453", "#F2A65A", "#E8554E"
STONE = "#C9D3E0"
ROCK = ["#3A3226", "#4B4030", "#5C4E3A", "#2F2A22", "#6B5B44"]


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mlabel(m: str) -> str:
    """'2026-03' -> 'Mar 2026'."""
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(m[5:7]) - 1]} {m[:4]}"


def mx(m: str) -> float:
    """A month as a decimal year (the middle of the month)."""
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12
