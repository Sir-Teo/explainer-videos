"""Helpers shared by the scenes of Part 28 of *Psychology, Built* ("Motivation")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 28

# one meaning per colour, for this part
BODY = "#7EC8F5"  # the body, homeostasis, set points
WANT = "#F2C14E"  # wanting, incentive salience, dopamine
LIKE = "#F28FB8"  # liking, pleasure, hedonic reactions
INTR = "#5BD18B"  # intrinsic motivation, goals that hold
EXTR = "#FF9F43"  # extrinsic rewards, incentives
CTRL = "#9AA4B2"  # self-control, effort, waiting
MODEL = "#B39DDB"  # what Psyche computes
LOST = "#EF6F6C"  # what failed, what starves
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
BAD = P.ERR
KANT = P.KANT
GOOD = "#5BD18B"
WORD = BODY


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
    keep = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
    return VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=radius, color=color, fill_opacity=opacity)
                    for a, b in zip(x[keep], y[keep])])


def curve_in(ax, x, y, color, stroke_width=3, smooth=False):
    """A curve with the points outside the axes' x range left out."""
    (x0, x1), _ = bounds(ax)
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= x0) & (x <= x1)
    return curve(ax, x[keep], y[keep], color, stroke_width=stroke_width, smooth=smooth)


def frame_box(mob, color=GREY_C, buff: float = 0.0) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2)


def word_chip(word: str, color=WORD, font_size=26, width=None) -> VGroup:
    """A word in a rounded box."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))


def bars(ax, xs, ys, color, width: float = 0.6, opacity: float = 0.85) -> VGroup:
    """Vertical bars from zero (or the axis floor) to ``ys`` at ``xs``, in data units."""
    (_, _), (y0, _) = bounds(ax)
    out = VGroup()
    for x, y in zip(xs, ys):
        lo, hi = ax.c2p(float(x), max(y0, 0.0)), ax.c2p(float(x), float(y))
        w = abs(ax.c2p(float(x) + width / 2, 0)[0] - ax.c2p(float(x) - width / 2, 0)[0])
        out.add(Rectangle(width=w, height=max(hi[1] - lo[1], 1e-3), stroke_width=0, fill_color=color,
                          fill_opacity=opacity).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
    return out
