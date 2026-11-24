"""Helpers shared by the scenes of Part 5 of *Industry, Built* ("The Moat")."""

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

PART = 5
ASK = "Why do some industries earn high returns for decades while others never do?"
R = results()

# colour = meaning, the same in every chapter of this part
RET, COST_, MOAT, ENTRANT, GOLD = "#7BD88F", "#E8554E", "#3B7DD8", "#F2A65A", "#F6C453"
STONE = "#C9D3E0"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
