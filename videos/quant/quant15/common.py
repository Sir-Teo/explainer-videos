"""Helpers shared by the scenes of Part 15 (Exotics and Structured Products)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 15

SPOT = QC.SPOT
OPT = QC.OPTION
BAD = QC.LOSS
GOOD = QC.GAIN
IV = QC.IMPLIED
DELTA = QC.DELTA
VEGA = QC.VEGA
BARRIER = QC.STRIKE
CASH = QC.CASH


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def ymd_to_year(d):
    import numpy as np
    from datetime import date
    d = np.asarray(d, int)
    out = []
    for x in d:
        t = date(x // 10000, (x // 100) % 100, x % 100)
        out.append(t.year + (t.timetuple().tm_yday - 1) / 365)
    return np.array(out)
