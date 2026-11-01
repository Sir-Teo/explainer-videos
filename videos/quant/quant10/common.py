"""Helpers shared by the scenes of Part 10 (Black–Scholes–Merton)."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs  # noqa: F401

from .compute import load  # noqa: F401

PART = 10

# one meaning per colour, for the whole part (explainer.style.QC)
SPOT, OPT, DEL, GAM, THE, VEG = QC.SPOT, QC.OPTION, QC.DELTA, QC.GAMMA, QC.THETA, QC.VEGA
IMP, REA, CASH, QQ, PP = QC.IMPLIED, QC.REALIZED, QC.CASH, QC.Q, QC.P
GAIN, LOSS = QC.GAIN, QC.LOSS

COL = {
    r"S": SPOT, r"S_t": SPOT, r"dS": SPOT, r"S_T": SPOT, r"\Delta S": SPOT,
    r"V": OPT, r"V(t, S)": OPT, r"C": OPT, r"dV": OPT,
    r"\Delta": DEL, r"\partial_S V": DEL,
    r"\Gamma": GAM, r"\partial_{SS} V": GAM,
    r"\Theta": THE, r"\partial_t V": THE,
    r"\sigma": IMP, r"\sigma_i": IMP, r"\sigma_i^2": IMP, r"\sigma_r": REA, r"\sigma_r^2": REA,
    r"r": CASH, r"B": CASH, r"\mathbb Q": QQ, r"\mathbb P": PP, r"\mu": PP,
    r"K": QC.STRIKE, r"W": SPOT, r"dW": SPOT, r"dW_t": SPOT,
}


def ts_date(ts: float, fmt="%d %b %Y") -> str:
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime(fmt).lstrip("0")


def money(x: float, digits=2) -> str:
    return f"{x:+.{digits}f}"


def tag(text: str, color=GREY_B, font_size=20, corner=UR) -> Tex:
    return note(text, font_size=font_size, color=color).to_corner(corner, buff=0.3)


def computed(text=r"computed", corner=DR):
    return tag(text, corner=corner)


def real_data(text: str, corner=DR):
    """A source line for real data on screen."""
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)
