"""Helpers shared by the scenes of Part 34 ("Storage")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401
from videos.cs.cs31.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES, edge_arrow,  # noqa: F401
                                   kv_rows)

from .compute import load  # noqa: F401

PART = 34
META = HEAD          # metadata: inodes, bitmaps, directories
BITS = COST          # bitmaps
JRN = LAM            # the journal
FILEC = DATA         # file data
ROLEC = {"superblock": GREY_B, "inode bitmap": BITS, "data bitmap": BITS, "inode table": META, "journal": JRN,
         "data": FILEC, "file data": FILEC, "directory": YES, "indirect": KERN}


def num(v) -> str:
    """An integer with TeX thousands separators."""
    return f"{int(round(v)):,}".replace(",", "{,}")


def ms(v: float) -> str:
    if v >= 1000:
        return rf"{v / 1000:.1f}\ s"
    if v >= 10:
        return rf"{v:.0f}\ ms"
    if v >= 1:
        return rf"{v:.1f}\ ms"
    return rf"{v * 1000:.0f}\ $\mu$s"


def blk(text: str = "", color=FILEC, w: float = 0.62, h: float = 0.62, font: int = 16, fill: float = 0.18):
    """A disk block: a square with an optional label."""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=fill)
    g = VGroup(r)
    if text:
        t = label(text, font_size=font, color=WHITE)
        if t.width > w - 0.06:
            t.width = w - 0.06
        g.add(t.move_to(r))
    return g


def layout_bar(parts, width: float = 12.0, h: float = 0.7, font: int = 17):
    """A disk drawn as a bar: ``parts`` = [(name, blocks, color)], widths by a square root so small regions show."""
    import math
    ws = [math.sqrt(b) for _, b, _ in parts]
    s = width / sum(ws)
    g = VGroup()
    x = -width / 2
    for (name, b, c), w in zip(parts, ws):
        r = Rectangle(width=w * s, height=h, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.25)
        r.move_to([x + w * s / 2, 0, 0])
        t = label(name, font_size=font, color=WHITE)
        if t.width > w * s - 0.08:
            t.width = max(0.2, w * s - 0.08)
        t.move_to(r)
        g.add(VGroup(r, t))
        x += w * s
    return g


def platter(r: float = 2.0, tracks: int = 6, color=GREY_B):
    """A platter seen from above: concentric tracks, a spindle, and one sector marked."""
    g = VGroup(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1))
    for k in range(1, tracks):
        g.add(Circle(radius=r * (0.3 + 0.7 * k / tracks), stroke_color=GREY_D, stroke_width=1))
    g.add(Dot(radius=0.08, color=GREY_B))
    return g
