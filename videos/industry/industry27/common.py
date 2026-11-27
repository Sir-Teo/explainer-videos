"""Helpers shared by the scenes of Part 27 of *Industry, Built* ("Shipping and Ports")."""

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

PART = 27
ASK = "How did moving a tonne across an ocean become nearly free, and why do the companies that do it swing between fortune and ruin?"
R = results()

SEA, BOX, RATE, FUEL, GOOD, BAD, SHIP, TANK, PORT, ALL = ("#4FB0E6", "#F2A65A", "#F6C453", "#B58CFF", "#7BD88F", "#E8554E",
                                                          "#7EC8F5", "#9AA3B2", "#9FE0D0", "#C9D3E0")
GROUP_COL = {"liner": "#F2A65A", "lessor": "#7BD88F", "tanker": "#9AA3B2", "bulk": "#D9B382", "gas": "#B58CFF",
             "forwarder": "#7EC8F5", "barge": "#9FE0D0"}
GROUP_NAME = {"liner": "container lines", "lessor": "ship lessors", "tanker": "tankers", "bulk": "dry bulk", "gas": "gas carriers",
              "forwarder": "forwarders", "barge": "barges"}
CHOKE_COL = {"Suez Canal": "#F2A65A", "Bab el-Mandeb Strait": "#E8554E", "Cape of Good Hope": "#7BD88F", "Panama Canal": "#4FB0E6",
             "Strait of Hormuz": "#B58CFF", "Malacca Strait": "#9FE0D0"}
CHOKE_LONLAT = {"Suez Canal": (32.5, 30.5), "Bab el-Mandeb Strait": (43.4, 12.6), "Cape of Good Hope": (18.5, -34.4),
                "Panama Canal": (-79.7, 9.1), "Strait of Hormuz": (56.4, 26.5), "Malacca Strait": (100.5, 3.0)}


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)
