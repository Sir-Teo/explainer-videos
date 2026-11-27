"""Helpers shared by the scenes of Part 10 of *Industry, Built* ("Farming and Food")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.ai.viz import CornerAxes, glow_dot  # noqa: F401
from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.draw import tx  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.industry.register import get, span  # noqa: F401
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 10
ASK = "Why do farmers grow ever more, and keep so little of what we pay?"
R = results()

# colour = meaning, the same in every chapter of this part
WHEATC, CORN, SOY, FARM, MEAT = "#E2B85C", "#F2C14E", "#7BD88F", "#6FAF5A", "#E8554E"
STATE, PRICE, LAND, COCOA, COST = "#E8554E", "#F6C453", "#A47A4C", "#C9732F", "#B58CFF"
TRADE, BRAND, SHOP = "#7EC8F5", "#F28B82", "#C9D3E0"
SOIL = "#6B4F33"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mlabel(m: str) -> str:
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(m[5:7]) - 1]} {m[:4]}"


def mx(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12
