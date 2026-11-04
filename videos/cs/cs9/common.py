"""Helpers shared by the scenes of Part 9 ("The Memory Hierarchy")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401

from .compute import load  # noqa: F401

PART = 9

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
CLOCK = C.CS_CLOCK
HIST = C.HUMAN
BG = "#121722"

LEVEL_COLOR = {"L1": YES, "L2": DATA, "L3": CTRL, "DRAM": NO}
FIELD_COLOR = {"tag": CTRL, "index": DATA, "offset": YES}


def size_label(b: int) -> str:
    """Bytes as a short Tex label: 4 KB, 32 KB, 1 MB, 512 MB."""
    if b >= 1 << 30:
        return rf"{b >> 30} GB"
    if b >= 1 << 20:
        return rf"{b >> 20} MB"
    if b >= 1 << 10:
        return rf"{b >> 10} KB"
    return rf"{b} B"


def address_bits(addr: int, tag_bits: int, index_bits: int, offset_bits: int, cell=0.28, font_size=16):
    """An address as a row of bits, coloured by field: ``.fields`` maps tag/index/offset to their cells, ``.braces``
    the labelled braces under them."""
    total = tag_bits + index_bits + offset_bits
    bits = format(addr, f"0{total}b")[-total:]
    g = VGroup()
    cells = VGroup()
    for k, b in enumerate(bits):
        field = "tag" if k < tag_bits else ("index" if k < tag_bits + index_bits else "offset")
        r = Square(side_length=cell, stroke_color=FIELD_COLOR[field], stroke_width=1.5, fill_color=FIELD_COLOR[field],
                   fill_opacity=0.18)
        t = Text(b, font="DejaVu Sans Mono", font_size=font_size, color=WHITE).move_to(r)
        cells.add(VGroup(r, t))
    cells.arrange(RIGHT, buff=0.02)
    g.add(cells)
    g.cells = cells
    g.fields = {"tag": VGroup(*cells[:tag_bits]), "index": VGroup(*cells[tag_bits:tag_bits + index_bits]),
                "offset": VGroup(*cells[tag_bits + index_bits:])}
    g.braces = VGroup()
    for name, grp in g.fields.items():
        if len(grp) == 0:
            continue
        br = Brace(grp, DOWN, buff=0.05, color=FIELD_COLOR[name])
        lab = label(rf"{name} \ ({len(grp)})", font_size=18, color=FIELD_COLOR[name]).next_to(br, DOWN, buff=0.05)
        g.braces.add(VGroup(br, lab))
    g.add(g.braces)
    return g


class Shelves(VGroup):
    """A set-associative cache as shelves: one row per set, ``ways`` slots per row.  ``slot(s, w)`` is a slot;
    ``put(s, w, text, color)`` returns the mobject to show in it."""

    def __init__(self, sets=8, ways=1, w=1.3, h=0.42, set_labels=True, font_size=14):
        super().__init__()
        self.sets_n, self.ways_n, self.w, self.h = sets, ways, w, h
        self.slots = {}
        for s in range(sets):
            for k in range(ways):
                r = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.2).move_to(
                    [k * (w + 0.06), -s * (h + 0.05), 0])
                self.slots[(s, k)] = r
                self.add(r)
            if set_labels:
                self.add(label(rf"set {s}", font_size=font_size, color=GREY_B).next_to(self.slots[(s, 0)], LEFT,
                                                                                   buff=0.15))

    def put(self, s, k, text, color=DATA, font_size=14):
        r = self.slots[(s, k)]
        f = r.copy().set_fill(color, opacity=0.35).set_stroke(color, width=1.5)
        t = Text(text, font="DejaVu Sans Mono", font_size=font_size, color=WHITE)
        if t.width > r.width * 0.9:
            t.width = r.width * 0.9
        return VGroup(f, t.move_to(r))


def staircase_axes(points, x_length=10.5, y_length=4.4, ymax=None):
    """Log-size axes for the latency staircase: x = log2(bytes), y = nanoseconds."""
    xs = [np.log2(p["bytes"]) for p in points]
    ymax = ymax or max(p["ns"] for p in points) * 1.1
    ax = Axes(x_range=[min(xs), max(xs) + 0.5, 2], y_range=[0, ymax, 50 if ymax > 150 else 10], x_length=x_length,
              y_length=y_length, tips=False, axis_config={"color": GREY_C, "font_size": 16})
    ticks = VGroup()
    for p in points[::2]:
        x = np.log2(p["bytes"])
        ticks.add(label(size_label(p["bytes"]), font_size=15, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.12))
    return ax, ticks
