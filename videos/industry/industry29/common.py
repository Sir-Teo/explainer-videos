"""Helpers shared by the scenes of Part 29 of *Industry, Built* ("Rail, Trucks and Parcels")."""

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

PART = 29
ASK = "Why is one freight industry a set of regional monopolies, and the next a market of half a million firms?"
R = results()

RAIL, TRUCK, LTL, PARCEL, GOOD, BAD, ALL, SKY, FUEL, CASH = ("#F6C453", "#E8554E", "#F2A65A", "#C89F6A", "#7BD88F",
                                                            "#E8554E", "#C9D3E0", "#7EC8F5", "#B58CFF", "#9FE0D0")
GROUP_COL = {"rail": RAIL, "parcel": PARCEL, "intermodal": SKY, "truckload": TRUCK, "ltl": LTL, "broker": FUEL,
             "logistics": CASH}
GROUP_NAME = {"rail": "railways", "parcel": "parcels", "intermodal": "intermodal", "truckload": "truckload",
              "ltl": "less than truckload", "broker": "brokers", "logistics": "contract logistics"}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def usd(v: float, d: int = 0) -> str:
    """A signed dollar amount, sign first: +$166 or -$1,716."""
    return f"{'+' if v >= 0 else '-'}${abs(v):,.{d}f}"
