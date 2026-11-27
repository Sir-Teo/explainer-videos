"""Helpers shared by the scenes of Part 12 of *Industry, Built* ("Chemicals")."""

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

PART = 12
ASK = "How does a molecule of gas become a thousand products, and where in the chain is the money?"
R = results()

# colour = meaning, the same in every chapter of this part
GAS, OIL, SALT, ETHYL, NITRO = "#7EC8F5", "#C9732F", "#E8EAED", "#7BD88F", "#5DA9E9"
TEXAS, EUROPE, ASIA = "#F6C453", "#B58CFF", "#F28B82"
PRICE, COST, GOOD, BAD = "#F6C453", "#B58CFF", "#7BD88F", "#E8554E"
PLASTIC, SPEC, GASES, FERT = "#C9D3E0", "#F28B82", "#7EC8F5", "#7BD88F"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def mlabel(m: str) -> str:
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[int(m[5:7]) - 1]} {m[:4]}"


def mx(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


def mm(x: float) -> str:
    return ("−" if x < 0 else "+") + f"${abs(x):,.0f}m"
