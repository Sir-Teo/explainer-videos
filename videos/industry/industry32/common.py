"""Helpers shared by the scenes of Part 32 of *Industry, Built* ("E-commerce")."""

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

PART = 32
ASK = "Is selling online a shop, a toll road or an advertising business?"
R = results()

SHOP, MARKET, ADS, CLOUD, SUBS, TOOLS, BRAND, DELIV, GOOD, BAD, ALL, PHYS = (
    "#7EC8F5", "#F6C453", "#FF8FB1", "#B58CFF", "#9FE0D0", "#F2A65A", "#C89F6A", "#7BD88F", "#7BD88F", "#E8554E", "#C9D3E0",
    "#5A8FD0")
GROUP_COL = {"shop": SHOP, "market": MARKET, "mixed": CLOUD, "tools": TOOLS, "delivery": SUBS, "brand": BRAND}
GROUP_NAME = {"shop": "own the stock", "market": "marketplaces", "mixed": "both, and more", "tools": "tools for sellers",
              "delivery": "delivery platforms", "brand": "direct brands"}
MIX = [("online", "online stores", SHOP), ("physical", "physical stores", PHYS), ("3p", "third-party seller services", MARKET),
       ("ads", "advertising", ADS), ("subs", "subscriptions", SUBS), ("aws", "AWS", CLOUD), ("other", "other", ALL)]


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def bn(v: float) -> str:
    return f"{'-' if v < 0 else ''}${abs(v) / 1e9:,.1f}bn"


def near(d: dict, x: float):
    """The key of ``d`` nearest ``x``."""
    return min(d, key=lambda k: abs(k - x))
