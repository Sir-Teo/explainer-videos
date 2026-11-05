"""Helpers shared by the scenes of Part 16 ("Counting Steps")."""

from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401

from .compute import load  # noqa: F401

PART = 16

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"
LAM = "#9b8cd6"


def value_bars(values, width=0.42, gap=0.08, scale=0.32, color=DATA, labels=True, font_size=16):
    """An array as a row of bars (height proportional to value), bottoms aligned; ``.bars`` and ``.labels``."""
    g = VGroup()
    bars, labs = VGroup(), VGroup()
    for k, v in enumerate(values):
        b = Rectangle(width=width, height=max(v * scale, 0.04), stroke_width=0, fill_color=color, fill_opacity=0.85)
        b.move_to([k * (width + gap), b.height / 2, 0])
        bars.add(b)
        if labels:
            labs.add(mono(str(v), font_size, GREY_A).next_to(b, DOWN, buff=0.08))
    g.add(bars, labs)
    g.bars, g.labels = bars, labs
    return g


def loglog_axes(xr, yr, x_len=6.0, y_len=4.0):
    return Axes(x_range=xr, y_range=yr, x_length=x_len, y_length=y_len,
                axis_config={"color": GREY_D, "include_numbers": False})


def words(n) -> str:
    return f"{n:,}"


def big(n: float) -> str:
    """A large count in words: 98.9 million, 15.0 billion."""
    for v, name in ((1e12, "trillion"), (1e9, "billion"), (1e6, "million")):
        if n >= v:
            return f"{n / v:.1f} {name}"
    return f"{n:,.0f}"
