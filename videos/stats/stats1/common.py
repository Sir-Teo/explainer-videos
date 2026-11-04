"""Helpers shared by the scenes of Part 1 of *Statistics, Built* ("The Shape of Data")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 1

# one meaning per colour, for this part (the series' S.TRUTH / S.EST / S.DATA / S.RESID keep theirs)
MEAN = S.EST  # the mean: the sample's balance point
MEDIAN = "#F28FB8"  # the median
MODE = "#C3A6FF"  # the mode
MIDRANGE = GREY_B
DEV = S.RESID  # deviations from a centre, and their squares
BIRTHS = "#7EC8F5"  # christenings in the Bills
DEATHS = "#F26D6D"  # burials
PLAGUE = "#B85C5C"
MEN, WOMEN = "#6FA8DC", "#E59AB8"
REGION_COLORS = ["#5DADEC", "#7BD88F", "#F2C14E", "#FF9F5A", "#B48EF0", "#4FD1C5", "#F28FB8", "#E3B98A",
                 "#9FB4C7", "#C9E27B"]

COLORS = {r"\theta": S.TRUTH, r"\hat\theta": S.EST, r"\bar x": MEAN, r"\mu": S.TRUTH}


def kfmt(v: float) -> str:
    """An income in thousands for MathTex: 38.9 -> '38.9\\text{k}'."""
    return rf"{v:.1f}\text{{k}}"


def money(v: float) -> str:
    """An income for narration: 38910 -> '38,910'."""
    return f"{v:,.0f}"


def pct(v: float, d=1) -> str:
    return f"{100 * v:.{d}f}"


def frame_box(w, h, center=ORIGIN, color=GREY_D) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=color, stroke_width=1.5,
                            fill_color="#121722", fill_opacity=1).move_to(center)


def readout(tex: str, color=WHITE, font_size=30) -> MathTex:
    return MathTex(tex, font_size=font_size, color=color)


def vline(ax, x, color, y0=None, y1=None, stroke_width=3, dashed=False):
    y0 = bounds(ax)[2] if y0 is None else y0
    y1 = bounds(ax)[3] if y1 is None else y1
    cls = DashedLine if dashed else Line
    return cls(ax.c2p(x, y0), ax.c2p(x, y1), color=color, stroke_width=stroke_width)
