"""Helpers shared by the scenes of Part 16 ("Counting Steps")."""

from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono as _mono
from explainer import zh_text
from videos.cs.cs8.common import bar_chart  # noqa: F401
from videos.cs.cs11.common import region  # noqa: F401

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


def literal_text(text, **kwargs):
    """Source tokens, IR operands and machine output are data, not UI prose."""
    with zh_text.verbatim():
        return Text(text, **kwargs)


def mono(s, size=19, color=CODE):
    with zh_text.verbatim():
        return _mono(s, size, color)


def code(lines, size=18, color=CODE, buff=0.07):
    return VGroup(*[mono(l if l else " ", size, color) for l in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=buff)


def grid_table(header, rows, widths, row_h=0.42, font_size=18, header_color=GREY_B, colors=None, mono_cols=(0,)):
    """``header``: column titles (Tex); ``rows``: lists of strings (Tex, or monospaced in ``mono_cols``).
    Returns a VGroup with ``.cells[r][c]`` (r = 0 is the header) and ``.rule``."""
    g = VGroup()
    g.cells = []
    xs = np.cumsum([0] + list(widths[:-1])) + np.array(widths) / 2
    for r, row in enumerate([header] + rows):
        line = []
        for c, txt in enumerate(row):
            if r > 0 and c in mono_cols:
                m = (literal_text(txt, font="DejaVu Sans Mono", font_size=font_size - 3, color=CODE) if txt.strip()
                     else VectorizedPoint())
            else:
                col = header_color if r == 0 else (colors[r - 1][c] if colors else WHITE)
                m = label(txt, font_size=font_size, color=col) if txt else VectorizedPoint()
            if m.width > widths[c] - 0.1:
                m.width = widths[c] - 0.1
            m.move_to([xs[c], -r * row_h, 0])
            if r > 0 and c in mono_cols:
                m.align_to([xs[c] - widths[c] / 2 + 0.05, 0, 0], LEFT)
            line.append(m)
            g.add(m)
        g.cells.append(line)
    g.rule = Line([0, -row_h / 2, 0], [sum(widths), -row_h / 2, 0], color=GREY_D, stroke_width=1.5)
    g.add(g.rule)
    return g
