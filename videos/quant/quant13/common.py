"""Helpers shared by the scenes of Part 13 (Stochastic Volatility and Jumps)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 13

IV = QC.IMPLIED       # market implied volatility
VAR = QC.Q            # the variance process
RV = QC.REALIZED      # realized
BAD = QC.LOSS
SPOT = QC.SPOT
OPT = QC.OPTION

# one colour per model, used in every chapter
MODEL_COL = {"BS": GREY_B, "LV": QC.THETA, "Heston": QC.Q, "Bates": QC.OPTION, "VG": QC.GAIN, "NIG": QC.DELTA,
             "SLV": "#E2E8F0", "SABR": QC.VEGA}


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
