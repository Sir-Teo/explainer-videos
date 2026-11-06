"""Helpers shared by the scenes of Part 32 ("Virtual Memory")."""

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

PART = 32
L1C, L2C, OFFC = LAM, HEAD, YES        # the three fields of a virtual address


def addr_bits(va: int, fields=((10, L1C, "L1 index"), (10, L2C, "L2 index"), (12, OFFC, "offset")), cell=0.3,
              font=16, labels=True):
    """A 32-bit address as 32 boxes, grouped into coloured fields; ``.fields[i]`` the boxes of field i,
    ``.tags`` the field names with their values."""
    bits = format(va & 0xFFFFFFFF, "032b")
    g = VGroup()
    fields_g = VGroup()
    tags = VGroup()
    k = 0
    for n, color, name in fields:
        fg = VGroup()
        for _ in range(n):
            r = Square(cell, stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=0.15)
            t = mono(bits[k], font, WHITE).move_to(r)
            fg.add(VGroup(r, t))
            k += 1
        fg.arrange(RIGHT, buff=0)
        fields_g.add(fg)
    fields_g.arrange(RIGHT, buff=0.08)
    g.add(fields_g)
    if labels:
        k = 0
        for (n, color, name), fg in zip(fields, fields_g):
            val = int(bits[k:k + n], 2)
            k += n
            tags.add(label(rf"{name}: \ {val}", font_size=font + 2, color=color).next_to(fg, DOWN, buff=0.12))
        g.add(tags)
    g.fields, g.tags = fields_g, tags
    return g


def hx(v: int) -> str:
    return f"0x{v:x}"
