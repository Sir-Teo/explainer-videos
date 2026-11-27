"""Helpers shared by the scenes of Part 25 of *Industry, Built* ("Homes")."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.beats import (beat, bullets, callout, dumbbell, ghost, hbars, head, hline,  # noqa: F401
                                      line_chart, marker, poly, quote, stat_cards, table, vbars)
from explainer.industry.draw import tx  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.industry.register import get, span  # noqa: F401
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 25
ASK = "Where does the price of a house come from: the house, the land or the loan?"
R = results()

HOUSE, LAND, LOAN, PRICE, GOOD, BAD, OWN, OPTION, RENT, ALL = ("#F2A65A", "#7BD88F", "#7EC8F5", "#F6C453", "#7BD88F",
                                                               "#E8554E", "#F2A65A", "#7EC8F5", "#B58CFF", "#C9D3E0")
GROUP_COL = {"builder": "#F2A65A", "factory": "#F2A7B5", "supply": "#7BD88F", "mortgage": "#7EC8F5", "broker": "#E8554E",
             "landlord": "#B58CFF"}
GROUP_NAME = {"builder": "homebuilders", "factory": "factory-built homes", "supply": "supplies and stores",
              "mortgage": "mortgage lenders", "broker": "brokers and portals", "landlord": "landlords"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def money(v: float) -> str:
    return f"${v:,.0f}"
