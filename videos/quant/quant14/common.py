"""Helpers shared by the scenes of Part 14 (Rough and Path-Dependent Volatility)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 14

IV = QC.IMPLIED       # market implied volatility
VAR = QC.Q            # variance processes, models
RV = QC.REALIZED      # realized
ROUGH = QC.GAMMA      # rough models
BAD = QC.LOSS
SPOT = QC.SPOT
OPT = QC.OPTION

MODEL_COL = {"Heston": QC.Q, "rBergomi": QC.GAMMA, "rough Heston": QC.OPTION, "PDV": QC.VEGA, "power": WHITE,
             "shifted": QC.DELTA}


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
