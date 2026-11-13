"""Helpers shared by the scenes of Part 3 of *Psychology, Built* ("The Measure")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 3

# one meaning per colour, for this part
TRUE = "#5BD18B"  # the true score, and any truth the Pool lets us know
ERRC = P.ERR  # error
OBS = P.POOL  # an observed score
KANT = P.KANT
GROUP_A, GROUP_B = "#7EC8F5", "#F2A65A"  # two groups answering one item
SCALE = {"nominal": "#B9C2D0", "ordinal": "#7EC8F5", "interval": "#F2C14E", "ratio": "#7BD88F"}
TRAIT = {"conscientious": "#F2C14E", "neurotic": "#F28FB8", "extravert": "#7EC8F5"}
TRAIT_NAME = {"conscientious": r"conscientiousness", "neurotic": r"neuroticism", "extravert": r"extraversion"}
METHOD_NAME = {"self": r"questionnaire", "peer": r"friend's rating", "record": r"records"}
GRIT = "#F2A65A"


def signed(x: float, digits: int = 1) -> str:
    """A number with its sign, and a plain zero for anything that rounds to zero (never ``-0.0``)."""
    v = round(float(x), digits)
    return f"{0:.{digits}f}" if v == 0 else f"{v:+.{digits}f}"


def r2(x: float) -> str:
    """A correlation or reliability to two places without the leading zero: ``.83``; ``1.00`` stays."""
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def keep_in_frame(mob, margin: float = 0.25):
    """Shift ``mob`` sideways so that it does not cross the left or right edge of the frame."""
    half = config.frame_width / 2 - margin
    if mob.get_left()[0] < -half:
        mob.shift(RIGHT * (-half - mob.get_left()[0]))
    if mob.get_right()[0] > half:
        mob.shift(LEFT * (mob.get_right()[0] - half))
    return mob


def people_row(n: int, colors, height: float = 0.5, buff: float = 0.12, per_row: int | None = None) -> VGroup:
    """``n`` little people coloured by ``colors`` (a colour, or one per person)."""
    cols = colors if isinstance(colors, (list, tuple, np.ndarray)) else [colors] * n
    g = VGroup(*[little_person(height, color=c) for c in cols])
    if per_row:
        g.arrange_in_grid(rows=int(np.ceil(n / per_row)), cols=per_row, buff=buff)
    else:
        g.arrange(RIGHT, buff=buff)
    return g


def code_block(lines, font_size=24, width: float | None = None) -> VGroup:
    """A few lines of code on a dark panel (monospace through TeX)."""
    rows = VGroup(*[label(rf"\texttt{{{ln}}}", font_size=font_size, color=WHITE) for ln in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    box = panel((width or rows.width + 0.8), rows.height + 0.6, color=P.PSYCHE)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    g = VGroup(box, rows)
    g.rows = rows
    return g


def rating_bars(shares, color, width: float = 3.2, height: float = 1.7, font_size=20, show_values=True) -> VGroup:
    """The shares of answers in each category of a rating scale (lowest first) as bars on a base line, with the
    category numbers under them.  ``.bars``, ``.base``, ``.ticks``."""
    k = len(shares)
    w = width / k
    top = max(max(shares), 1e-9)
    bars, ticks = VGroup(), VGroup()
    for i, s in enumerate(shares):
        h = max(height * s / top, 0.02)
        bars.add(Rectangle(width=w * 0.82, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
                 .move_to([(i + 0.5) * w, h / 2, 0]))
        ticks.add(label(rf"{i + 1}", font_size=font_size, color=GREY_B).move_to([(i + 0.5) * w, -0.22, 0]))
    base = Line([0, 0, 0], [width, 0, 0], color=GREY_B, stroke_width=2)
    g = VGroup(base, bars, ticks)
    g.base, g.bars, g.ticks = base, bars, ticks
    return g


def heat_color(r: float):
    """A correlation as a colour: dark at 0, the accent at +1, the error colour at -1."""
    return interpolate_color(ManimColor("#161C28"), ManimColor(P.ACCENT if r >= 0 else P.ERR), min(abs(float(r)), 1.0) ** 0.8)


def heatmap(matrix, cell: float = 0.5, font_size=16, show_values=True, diagonal=True) -> VGroup:
    """A correlation matrix as a grid of coloured cells; ``.cells[i][j]`` is the square in row ``i``, column ``j``,
    and ``.values[i][j]`` its number (two places, no leading zero)."""
    m = np.asarray(matrix, dtype=float)
    n = m.shape[0]
    g, cells, values = VGroup(), [], []
    for i in range(n):
        crow, vrow = [], []
        for j in range(n):
            sq = Square(cell, stroke_color=BACKGROUND, stroke_width=1.5, fill_color=heat_color(m[i, j]), fill_opacity=1)
            sq.move_to([(j + 0.5) * cell, -(i + 0.5) * cell, 0])
            if i == j and not diagonal:
                sq.set_fill("#0B0F16")
            txt = VGroup()
            if show_values and not (i == j and not diagonal):
                txt = label(r2(m[i, j]), font_size=font_size, color=WHITE if abs(m[i, j]) < 0.55 else BLACK)
                txt.move_to(sq)
            crow.append(sq), vrow.append(txt)
            g.add(sq, txt)
        cells.append(crow), values.append(vrow)
    g.cells, g.values, g.cell = cells, values, cell
    return g


def scatter(ax, xs, ys, color, radius: float = 0.03, opacity: float = 0.7) -> VGroup:
    """Points on ``ax``."""
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color, fill_opacity=opacity) for x, y in zip(xs, ys)])


def density(values, lo: float, hi: float, bins: int):
    """Histogram ``(edges, densities)`` of ``values`` for :func:`hist`."""
    dens, edges = np.histogram(np.asarray(values, dtype=float), bins=bins, range=(lo, hi), density=True)
    return edges, dens
