"""Helpers shared by the scenes of Part 4 (Martingales and Measure)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 4

P_C = QC.SPOT        # the real-world measure P, and data
Q_C = QC.OPTION      # the other measure Q
MART = QC.IDEA       # martingales, fair games
DRIFT = QC.GAIN      # predictable parts
LOSS, GAIN = QC.LOSS, QC.GAIN
INFO = QC.IMPLIED    # information, filtrations


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
