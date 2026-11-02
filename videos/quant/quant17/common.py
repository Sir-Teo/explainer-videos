"""Helpers shared by the scenes of Part 17 (Deep Pricing and Hedging)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 17

SPOT = QC.SPOT
OPT = QC.OPTION
BAD = QC.LOSS
GOOD = QC.GAIN
IV = QC.IMPLIED
DELTA = QC.DELTA
VEGA = QC.VEGA
NET = QC.Q          # anything a network produced
REF = WHITE         # the reference it is checked against

GEN_COL = {"real (held out)": WHITE, "real (train)": GREY_B, "i.i.d. normal": GREY_C, "i.i.d. bootstrap": GREY_B,
           "GJR-GARCH": QC.DELTA, "signature LSTM": QC.Q, "diffusion": QC.GAIN}


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def sci(x: float, digits: int = 0) -> str:
    """A number in scientific notation for MathTex: 2\\times 10^{-2}, not 2e-02."""
    import math
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f}\times 10^{{{e}}}"
