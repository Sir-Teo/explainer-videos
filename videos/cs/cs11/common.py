"""Helpers shared by the scenes of Part 11 ("The Running Program")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401

from .compute import load  # noqa: F401

PART = 11

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
LIMIT = C.CS_LIMIT
INF = C.CS_INF
BG = "#121722"

SECTION_COLOR = {".text": DATA, ".data": CTRL, ".bss": FUNC, "heap": YES, "stack": NO, "libs": GREY_B}
FILE_COLORS = [DATA, CTRL, YES, FUNC]


def code(lines, size=18, color=CODE, buff=0.07):
    """A listing: one mono line per entry, left-aligned, indentation kept."""
    return VGroup(*[mono(l, size, color) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def region(w, h, text, color, font_size=18, fill=0.18):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=fill)
    t = label(text, font_size=font_size, color=color)
    if t.width > w - 0.1:
        t.width = w - 0.1
    if t.height > h - 0.04:
        t.height = max(0.05, h - 0.04)
    t.move_to(r)
    g = VGroup(r, t)
    g.rect, g.text = r, t
    return g


def memory_strip(parts, w=2.6, total_h=5.6, gap=0.04):
    """A tall strip of memory, low addresses at the bottom: ``parts`` = [(name, height_fraction, color)], bottom up.
    Returns a VGroup with ``.parts[name]``."""
    g = VGroup()
    g.parts = {}
    y = -total_h / 2
    for name, frac, color in parts:
        h = total_h * frac
        reg = region(w, max(h - gap, 0.08), name, color)
        reg.move_to([0, y + h / 2, 0])
        g.parts[name] = reg
        g.add(reg)
        y += h
    return g


def frame_box(name, color, w=2.6, h=0.55, font_size=18):
    return region(w, h, name, color, font_size=font_size, fill=0.25)
