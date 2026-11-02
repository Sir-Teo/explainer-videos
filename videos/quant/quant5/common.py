"""Helpers shared by the scenes of Part 5 (Stochastic Calculus)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 5

BM = QC.SPOT          # Brownian paths, data
ITO = QC.IDEA         # Itô objects
STRAT = QC.OPTION     # Stratonovich, alternatives
DRIFT = QC.GAIN       # drift, predictable parts
JUMP = QC.LOSS        # jumps, errors
LOSS, GAIN = QC.LOSS, QC.GAIN


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
