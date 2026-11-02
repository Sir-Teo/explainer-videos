"""Helpers shared by the scenes of Part 5 (Stochastic Calculus)."""

from __future__ import annotations

import numpy as np

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


def pause(question: str, answer: str, width=6.2, font_size=24):
    """A pause-and-predict card and its answer (a label), unplaced; the scene positions them."""
    pc = pause_card(question, width=width, font_size=font_size)
    ans = wrapped_label(answer, width, font_size - 2, QC.GAIN)
    return pc, ans


def pct(x, d=0):
    return f"{100 * x:.{d}f}"


def sci(x: float, d: int = 1) -> str:
    """x in LaTeX scientific notation: 1.2 \\times 10^{-3} (plain decimals between 0.01 and 1,000)."""
    if x == 0 or 0.01 <= abs(x) < 1000:
        return f"{x:.{max(d, 2)}f}"
    e = int(np.floor(np.log10(abs(x))))
    return rf"{x / 10 ** e:.{d}f} \times 10^{{{e}}}"
