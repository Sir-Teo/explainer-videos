"""Helpers shared by the scenes of Part 9 of *Industry, Built* ("Mining and Metals")."""

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

PART = 9
ASK = "Why is a mine worth a fortune in one decade and nothing in the next?"
R = results()

# colour = meaning, the same in every chapter of this part
COPPER, IRON, GOLDC, LITH, STATE = "#D9824B", "#B5574B", "#F6C453", "#7BD88F", "#E8554E"
COST, PRICE, CHINA, ROCK = "#B58CFF", "#F6C453", "#E8554E", "#8A6E52"
STONE = "#C9D3E0"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mlabel(m: str) -> str:
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(m[5:7]) - 1]} {m[:4]}"


def mx(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12
