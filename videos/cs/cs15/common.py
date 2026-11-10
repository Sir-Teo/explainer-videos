"""Helpers shared by the scenes of Part 15 ("Runtimes")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono as _mono
from explainer import zh_text
from videos.cs.cs8.common import bar_chart  # noqa: F401
from videos.cs.cs11.common import region  # noqa: F401

from .compute import load  # noqa: F401

PART = 15

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
WHITE_OBJ = "#d8dee9"     # tri-color: white
GRAY_OBJ = "#8a8f99"      # gray
BLACK_OBJ = "#2b2f38"     # black
KIND_COLOR = {"cons": DATA, "pair": FUNC, "closure": LAM}


def cell_obj(kind: str, fields, w=0.62, h=0.46, font_size=16, header=True):
    """A heap object as a row of cells: a header naming its kind, then one cell per field (an int, or a dot for a
    pointer).  ``.cells`` are the field cells, ``.dots`` the pointer dots (None for ints)."""
    color = KIND_COLOR.get(kind, GREY_B)
    g = VGroup()
    cells, dots = [], []
    if header:
        hd = VGroup(Rectangle(width=w * 1.25, height=h, stroke_color=color, stroke_width=1.6, fill_color=color,
                              fill_opacity=0.22), label(kind, font_size=font_size - 2, color=color))
        hd[1].move_to(hd[0])
        if hd[1].width > w * 1.15:
            hd[1].scale_to_fit_width(w * 1.15)
        g.add(hd)
    for f in fields:
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=BG, fill_opacity=1)
        if f is None:
            t = MathTex(r"\cdot", font_size=font_size + 4, color=GREY_D)
            d = None
        elif isinstance(f, str):
            t = Dot(radius=0.06, color=WHITE)
            d = t
        else:
            t = mono(str(f), font_size, WHITE)
            d = None
        t.move_to(r)
        cells.append(VGroup(r, t))
        dots.append(d)
    g.add(*cells)
    g.arrange(RIGHT, buff=0)
    g.cells, g.dots = cells, dots
    return g


def ptr(a, b, color=GREY_B, angle=0.0, sw=2.2):
    """An arrow from a pointer dot (or point) to the left edge of an object."""
    start = a.get_center() if hasattr(a, "get_center") else a
    end = b.get_left() if hasattr(b, "get_left") else b
    if angle:
        return CurvedArrow(start, end, angle=angle, color=color, stroke_width=sw, tip_length=0.14)
    return Arrow(start, end, buff=0.05, color=color, stroke_width=sw, tip_length=0.14, max_tip_length_to_length_ratio=0.2)


def sawtooth(log, S, total, x_len=10.5, y_len=3.0, color=COST):
    """Heap occupancy against words allocated: rising with allocation, falling to the live data at each
    collection.  Returns (axes, curve, drop_marks)."""
    ax = Axes(x_range=[0, total, total / 4], y_range=[0, S, S / 2], x_length=x_len, y_length=y_len,
              axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    pts = [ax.c2p(0, 0)]
    prev_clock, prev_live = 0, 0
    drops = VGroup()
    for r in log:
        pts.append(ax.c2p(r["clock"], min(prev_live + (r["clock"] - prev_clock), S)))
        pts.append(ax.c2p(r["clock"], r["live"]))
        drops.add(Dot(ax.c2p(r["clock"], r["live"]), radius=0.045, color=YES))
        prev_clock, prev_live = r["clock"], r["live"]
    pts.append(ax.c2p(total, min(prev_live + (total - prev_clock), S)))
    curve = VMobject(color=color, stroke_width=2.5).set_points_as_corners(pts)
    return ax, curve, drops


def words(n) -> str:
    return f"{n:,}"


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
