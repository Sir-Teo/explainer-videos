"""Helpers shared by the scenes of Part 32 of *Psychology, Built* ("Intelligence")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 32

# one meaning per colour, for this part
G = "#F2C14E"  # g, the general factor
VERB = "#7EC8F5"  # verbal tests and factors
VIS = "#B39DDB"  # visual-spatial tests and factors
SPEED = "#FF9F43"  # speeded tests
MODEL = "#B39DDB"  # what Psyche computes
GOOD = "#5BD18B"
LOST = "#EF6F6C"
HARM = "#EF6F6C"  # the history of harm
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
KANT = P.KANT
AGE = "#7EC8F5"
COHORT = "#B39DDB"


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


def word_chip(word: str, color=AGE, font_size=26, width=None) -> VGroup:
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


SHADES = ["#F4F4F4", "#8A8F98", "#2B2F36"]


def glyph(attrs, scale: float = 1.0) -> VGroup:
    """One matrix cell from its attributes (shape, number, shade, size), each 0, 1 or 2: circles, triangles or squares;
    one to three of them; white, grey or dark; small, medium or large."""
    shape, number, shade, size = (int(a) for a in attrs)
    r = [0.09, 0.125, 0.16][size] * scale
    items = VGroup()
    for _ in range(number + 1):
        if shape == 0:
            m = Circle(radius=r)
        elif shape == 1:
            m = Triangle().scale(r * 1.25)
        else:
            m = Square(side_length=1.7 * r)
        m.set_stroke(WHITE, 2).set_fill(SHADES[shade], opacity=1)
        items.add(m)
    # sizes are fixed whatever the number, so a size rule reads the same in every cell; three sit two over one
    if len(items) == 3:
        top = VGroup(items[0], items[1]).arrange(RIGHT, buff=0.05 * scale)
        items[2].next_to(top, DOWN, buff=0.04 * scale)
    else:
        items.arrange(RIGHT, buff=0.06 * scale)
    return items


def matrix_panel(grid, cell: float = 0.95, missing: bool = True) -> VGroup:
    """A 3x3 matrix item; the bottom-right cell is a box with a question mark when ``missing``."""
    out = VGroup()
    for r in range(3):
        for c in range(3):
            box = Square(side_length=cell, stroke_color=GREY_B, stroke_width=2).move_to([c * cell, -r * cell, 0])
            if r == 2 and c == 2 and missing:
                out.add(VGroup(box, label("?", font_size=36, color=YOU).move_to(box)))
            else:
                out.add(VGroup(box, glyph(grid[r][c], scale=cell / 0.95).move_to(box)))
    return out
