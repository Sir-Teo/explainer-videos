"""Helpers shared by the scenes of Part 4 of *Psychology, Built* ("The Evidence")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 4

# one meaning per colour, for this part
TRUTH = "#5BD18B"  # the true effect, where the lab lets us know it
NULLC = "#8FA3BF"  # what "nothing is there" predicts
SIG = P.ACCENT  # a result that reached p < .05, and what got published
DRAWER = "#566074"  # a result that stayed in the file drawer
BAD = P.ERR  # a wrong conclusion, an inflated estimate
ORIG, REP = "#F2A65A", "#7EC8F5"  # an original study and its replication
KANT = P.KANT
SIZE = {"0.2": "#7EC8F5", "0.5": "#F2C14E", "0.8": "#F28FB8"}


def r2(x: float) -> str:
    """A number to two places without the leading zero: ``.22``; ``1.00`` stays."""
    s = f"{x:.2f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def pct(x: float, digits: int = 0) -> str:
    return rf"{100 * x:.{digits}f}\%"


def p_text(p: float) -> str:
    """A p-value as it is printed: ``.018``, or ``< .001``."""
    return r"< .001" if p < 0.001 else f"{p:.3f}".replace("0.", ".", 1)


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


def tiles(n: int, lit: int, color, off="#2A3242", size: float = 0.27, buff: float = 0.06, cols: int = 20) -> VGroup:
    """``n`` small squares, the first ``lit`` of them in ``color``: a count out of ``n`` that can be seen."""
    g = VGroup(*[Square(size, stroke_width=0, fill_color=(color if i < lit else off), fill_opacity=1) for i in range(n)])
    return g.arrange_in_grid(rows=int(np.ceil(n / cols)), cols=cols, buff=buff)


def big_number(value: str, caption: str, color, font_size: int = 72, width: float = 4.2, cap_size: int = 26) -> VGroup:
    """A number to remember, with one line under it saying what it is."""
    return VGroup(label(value, font_size=font_size, color=color), wrapped_label(caption, width, cap_size, GREY_A)).arrange(
        DOWN, buff=0.18)


def scatter(ax, xs, ys, color, radius: float = 0.03, opacity: float = 0.7) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color, fill_opacity=opacity) for x, y in zip(xs, ys)])


def bars_on(ax, edges, heights, color, opacity: float = 0.7) -> VGroup:
    """Histogram bars on ``ax`` from bin ``edges`` and ``heights`` (in the axis's own units)."""
    return hist(ax, edges, heights, color, opacity)


def code_block(lines, font_size=24, width: float | None = None) -> VGroup:
    """A few lines of code on a dark panel (monospace through TeX)."""
    rows = VGroup(*[label(rf"\texttt{{{ln}}}", font_size=font_size, color=WHITE) for ln in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    box = panel((width or rows.width + 0.8), rows.height + 0.6, color=P.PSYCHE)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    g = VGroup(box, rows)
    g.rows = rows
    return g
