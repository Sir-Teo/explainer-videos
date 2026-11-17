"""Helpers shared by the scenes of Part 34 of *Psychology, Built* ("Social Influence")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 34

# one meaning per colour, for this part
PERSON = "#F2C14E"  # the individual: you, a participant, one node
CROWD = "#7EC8F5"  # the others, the group, the majority
AUTH = "#EF6F6C"  # authority, pressure, the wrong answer
MODEL = "#B39DDB"  # what Psyche computes
GOOD = "#5BD18B"  # help, dissent, the right answer
LOST = "#EF6F6C"
YOU = "#F2C14E"  # the viewer
OFF = "#3A3F48"  # not (yet) in, not adopted
G = "#F2C14E"
DATA = P.ARCHIVE
KANT = P.KANT


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def spct(x: float) -> str:
    """A share as narration reads it: "45 percent"."""
    return f"{100 * x:.0f} percent"


def num(n) -> str:
    """An integer with thousands separators that TeX sets without a gap."""
    return f"{int(n):,}".replace(",", "{,}")


def keep_in_frame(mob, margin: float = 0.25):
    half = config.frame_width / 2 - margin
    if mob.get_left()[0] < -half:
        mob.shift(RIGHT * (-half - mob.get_left()[0]))
    if mob.get_right()[0] > half:
        mob.shift(LEFT * (mob.get_right()[0] - half))
    return mob


def rows_of(items, width: float, font_size: int = 30, buff: float = 0.34) -> VGroup:
    """Lines of text, each (text, colour), wrapped to ``width`` and stacked."""
    return VGroup(*[wrapped_label(t, width, font_size, c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def bounds(ax):
    """The data range of an axis pair (corner axes store their ranges shifted to start at zero)."""
    ox, oy = getattr(ax, "_off", (0.0, 0.0))
    return (float(ax.x_range[0] + ox), float(ax.x_range[1] + ox)), (float(ax.y_range[0] + oy), float(ax.y_range[1] + oy))


def scatter(ax, x, y, color, radius: float = 0.04, opacity: float = 0.85) -> VGroup:
    (x0, x1), (y0, y1) = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1) & np.isfinite(x) & np.isfinite(y)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(x[keep], y[keep])])


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def bars(ax, xs, ys, color, width: float = 0.6, opacity: float = 0.85) -> VGroup:
    """Vertical bars from zero (or the axis floor) to ``ys`` at ``xs``, in data units."""
    (_, _), (y0, _) = bounds(ax)
    out = VGroup()
    colors = color if isinstance(color, (list, tuple)) else [color] * len(xs)
    for x, y, c in zip(xs, ys, colors):
        lo, hi = ax.c2p(float(x), max(y0, 0.0)), ax.c2p(float(x), float(y))
        w = abs(ax.c2p(float(x) + width / 2, 0)[0] - ax.c2p(float(x) - width / 2, 0)[0])
        out.add(Rectangle(width=w, height=max(abs(hi[1] - lo[1]), 1e-3), stroke_width=0, fill_color=c,
                          fill_opacity=opacity).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
    return out


def word_chip(word: str, color=CROWD, font_size=26, width=None) -> VGroup:
    """A word in a rounded box."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))




def heatmap(R, names=None, cell: float = 0.55, font_size: int = 16, values: bool = True, lo: float = 0.0,
            hi: float = 1.0, name_color=GREY_A) -> VGroup:
    """A correlation matrix as coloured squares (dark for 0, gold for 1, red below 0), with optional values and
    names on the left and top.  Returns VGroup(cells, labels) with ``.cells`` indexed [i][j]."""
    R = np.asarray(R, float)
    p = len(R)
    cells = VGroup()
    grid = []
    for i in range(p):
        row = []
        for j in range(p):
            r = float(R[i, j])
            if r >= 0:
                t = min(1.0, (r - lo) / (hi - lo))
                col = interpolate_color(ManimColor("#14181F"), ManimColor(G), t)
            else:
                col = interpolate_color(ManimColor("#14181F"), ManimColor(LOST), min(1.0, -r / 0.3))
            sq = Square(side_length=cell, stroke_width=1, stroke_color=BLACK, fill_color=col, fill_opacity=1)
            sq.move_to([j * cell, -i * cell, 0])
            g_ = VGroup(sq)
            if values and i != j:
                g_.add(label(f"{r:.2f}".replace("0.", ".", 1) if r >= 0 else f"{r:.2f}".replace("-0.", "-.", 1),
                             font_size=font_size, color=BLACK if r > 0.55 else WHITE).move_to(sq))
            cells.add(g_)
            row.append(g_)
        grid.append(row)
    labels = VGroup()
    if names:
        for i, nm in enumerate(names):
            labels.add(label(nm, font_size=font_size + 2, color=name_color).next_to(grid[i][0], LEFT, buff=0.12))
    out = VGroup(cells, labels)
    out.cells = grid
    return out
