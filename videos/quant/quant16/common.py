"""Helpers shared by the scenes of Part 16 (Computing Prices)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 16

SPOT = QC.SPOT
OPT = QC.OPTION
BAD = QC.LOSS
GOOD = QC.GAIN
IV = QC.IMPLIED
DELTA = QC.DELTA
VEGA = QC.VEGA

METHOD_COL = {"plain": GREY_B, "antithetic": QC.THETA, "control": QC.GAIN, "sobol": QC.Q, "pseudo-random": GREY_B,
              "Sobol": QC.Q, "Sobol + bridge": QC.OPTION, "Monte Carlo (QE, 50 steps)": GREY_B,
              "ADI (Craig-Sneyd)": QC.DELTA, "COS": QC.GAIN, "Carr-Madan FFT": QC.Q}


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def loglog(x_lo, x_hi, y_lo, y_hi, xlabel, ylabel, x_length=6.4, y_length=4.2, xt=None, yt=None, font_size=15):
    """Axes in log10 units with tick labels as powers of ten."""
    import numpy as np
    xt = xt or list(range(int(np.ceil(x_lo)), int(np.floor(x_hi)) + 1))
    yt = yt or list(range(int(np.ceil(y_lo)), int(np.floor(y_hi)) + 1))
    return axes([x_lo, x_hi], [y_lo, y_hi], x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xt, yticks=yt, xfmt=lambda u: f"10^{{{int(round(u))}}}", yfmt=lambda u: f"10^{{{int(round(u))}}}",
                log_x=True, font_size=font_size)
