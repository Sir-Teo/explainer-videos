"""Helpers shared by the scenes of Part 3 (Value, Accounting and the Firm)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 3

PRICE = QC.SPOT        # market prices
VALUE = QC.IDEA        # present values, fundamentals
CASH = QC.GAIN         # cash flows
DEBT = QC.CASH         # debt, rates
EQUITY = QC.OPTION     # equity
LOSS, GAIN = QC.LOSS, QC.GAIN


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
