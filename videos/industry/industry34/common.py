"""Helpers shared by the scenes of Part 34 of *Industry, Built* ("Restaurants and Franchising")."""

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

PART = 34
ASK = "Who actually owns a fast-food restaurant, and who is making the money?"
R = results()

FR, OP, FULL, MASTER, APPS, FOODC, LABC, ADC, OTHER, GOOD, BAD, ALL = ("#F6C453", "#7EC8F5", "#B58CFF", "#F2A65A", "#FF8FB1",
                                                                      "#C89F6A", "#9FE0D0", "#B58CFF", "#9AA3B2", "#7BD88F",
                                                                      "#E8554E", "#C9D3E0")
GROUP_COL = {"franchisor": FR, "operator": OP, "full": FULL, "master": MASTER, "delivery": APPS}
GROUP_NAME = {"franchisor": "franchisors", "operator": "own their restaurants", "full": "full service", "master": "master franchisees",
              "delivery": "delivery"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def k(v: float) -> str:
    return f"{'-' if v < 0 else ''}${abs(v) / 1e3:,.0f}k"


def near(d: dict, x: float):
    return min(d, key=lambda key: abs(key - x))
