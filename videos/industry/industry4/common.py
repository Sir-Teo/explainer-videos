"""Helpers shared by the scenes of Part 4 of *Industry, Built* ("The Cost Curve")."""

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

PART = 4
ASK = "What does one more cost, and why does that decide almost everything?"
R = results()

# One colour per kind of plant, the same in every chapter of this part
TECH = {"wind": "#9FD3F5", "solar": "#F6C453", "hydro": "#3B7DD8", "nuclear": "#7BD88F", "coal": "#8C929B",
        "gas_cc": "#F2A65A", "gas_steam": "#D9825B", "gas_ct": "#E8554E", "oil": "#9B6BD6"}
FIXED, VAR, PROFIT, LOSS, PRICE = "#7EC8F5", "#F2A65A", "#7BD88F", "#E8554E", "#F6C453"


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def icon(key: str, h: float = 0.55) -> VGroup:
    """The little picture of each kind of plant."""
    if key == "wind":
        g = draw.wind_turbine(1.0)
    elif key == "solar":
        g = draw.solar_panel(1.0)
    elif key == "hydro":
        g = draw.dam(0.7)
    elif key == "nuclear":
        g = draw.cooling_tower(1.0)
    elif key == "coal":
        g = draw.coal_plant(0.8)
    elif key == "oil":
        g = draw.gas_plant(0.8, color=TECH["oil"])
    else:
        g = draw.gas_plant(0.8, color=TECH[key])
    g.scale_to_fit_height(h)
    return g
