"""Helpers shared by the scenes of Part 33 ("Concurrency")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401
from videos.cs.cs31.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES, edge_arrow,  # noqa: F401
                                   gantt, kv_rows, state_node, time_axis)

from .compute import load  # noqa: F401

PART = 33
T0C, T1C, T2C = DATA, HEAD, LAM      # thread colours
TC = (T0C, T1C, T2C, YES, NO)


def num(v) -> str:
    """An integer with TeX thousands separators."""
    return f"{v:,}".replace(",", "{,}")


def thread_lane(name, ops, color, w=0.95, h=0.5, font=16):
    """A thread's instructions as a row of boxes; ``.cells[i]`` the boxes."""
    cells = VGroup()
    for t in ops:
        r = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=1.6,
                             fill_color=color, fill_opacity=0.15)
        cells.add(VGroup(r, mono(t, font, WHITE).move_to(r)))
    cells.arrange(RIGHT, buff=0.08)
    g = VGroup(label(name, font_size=20, color=color), cells).arrange(RIGHT, buff=0.25)
    g.cells = cells
    return g
