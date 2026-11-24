"""Helpers shared by the scenes of Part 6 of *Industry, Built* ("The Cycle")."""

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

PART = 6
ASK = "Why do industries keep building too much at the top?"
R = results()

# colour = meaning, the same in every chapter of this part
BOOM, BUST, CAP, ORDER, PRICE = "#7BD88F", "#E8554E", "#7EC8F5", "#F6C453", "#F2A65A"
STONE = "#C9D3E0"
HOG = "#F2A7B5"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def say_bn(x: float, digits: int = 1) -> str:
    """Narration for a dollar amount in billions: 'fifteen point five billion dollars' style, as digits."""
    return f"{x:.{digits}f} billion dollars"
