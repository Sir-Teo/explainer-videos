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
             "SLV": "#E2E8F0", "SABR": QC.VEGA, "Merton": "#F28B82", "Kou": "#FBBC04", "CGMY": "#81C995",
             "CGMY_inf": "#81C995"}
NAMES = {"BS": r"Black--Scholes", "LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma",
         "NIG": r"NIG", "SLV": r"SLV", "SABR": r"SABR, per expiry", "Merton": r"Merton", "Kou": r"Kou",
         "CGMY": r"CGMY", "CGMY_inf": r"CGMY"}


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def simulated(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def pause(question: str, width: float = 6.0, font_size=22, corner=DR):
    """A pause-and-predict card, in a corner."""
    return pause_card(question, width=width, font_size=font_size).to_corner(corner, buff=0.3)


def yr(ts):
    import numpy as _np

    return 1970 + _np.asarray(ts, float) / (365.2425 * 86400)
