"""Helpers shared by the scenes of Part 12 (The Volatility Surface)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 12

IV = QC.IMPLIED       # implied volatility
LV = QC.IDEA          # local volatility, models
RV = QC.GAIN          # realized
BAD = QC.LOSS
SPOT = QC.SPOT
OPT = QC.OPTION


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
