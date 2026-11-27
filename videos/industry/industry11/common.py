"""Helpers shared by the scenes of Part 11 of *Industry, Built* ("Heavy Materials")."""

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

PART = 11
ASK = "Why do the things everything is made of earn so little?"
R = results()

# colour = meaning, the same in every chapter of this part
ORE, SCRAP, STEELC, MOLTEN, HOT = "#C96A3D", "#7EC8F5", "#AEB6C4", "#FF8A3D", "#FFD166"
CEMENT, ALU, PACK, STONE, CARBON = "#D7DCE3", "#9AD1F5", "#C49A6C", "#9AA0A6", "#E8554E"
PRICE, COST, CHINA, USA, REST = "#F6C453", "#B58CFF", "#F28B82", "#7EC8F5", "#5D6B82"
GOOD, BAD = "#7BD88F", "#E8554E"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mlabel(m: str) -> str:
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(m[5:7]) - 1]} {m[:4]}"


def mx(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


def cents(x: float) -> str:
    """A price a kilogram, in cents below a dollar and dollars above."""
    return f"{100 * x:.1f}c" if x < 0.1 else (f"{100 * x:.0f}c" if x < 1 else f"${x:.2f}")


def mm(x: float) -> str:
    """$ million with a proper minus sign: -308 -> "-$308m"."""
    return ("−" if x < 0 else "+") + f"${abs(x):,.0f}m"
