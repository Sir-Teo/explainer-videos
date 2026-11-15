"""Helpers shared by the scenes of Part 20 of *Psychology, Built* ("Memory I: Storing and Finding")."""

from __future__ import annotations

import numpy as np

from explainer.psychology import *  # noqa: F403
from explainer.psychology import archive, ledger  # noqa: F401

from .compute import load  # noqa: F401

PART = 20

# one meaning per colour, for this part
WORD = "#F2C14E"  # a studied item; a memory trace; recall
CTX = "#7EC8F5"  # context: the drifting state the items are bound to
CUE = "#B39DDB"  # cues, search, the probe
LOST = "#EF6F6C"  # forgetting, failures, intrusions, interference
SAM = "#F28FB8"  # the search of associative memory (SAM)
MODEL = "#5BD18B"  # what Psyche computes: the context model, the networks
YOU = "#F2C14E"  # the viewer
DATA = P.ARCHIVE
BAD = P.ERR
KANT = P.KANT
GOOD = "#5BD18B"

# the list the viewer studies in the hook (sixteen words, as in the open data)
WORDS = ("CANDLE", "HORSE", "PENCIL", "RIVER", "JACKET", "ONION", "LADDER", "TRUMPET",
         "GARDEN", "MONKEY", "BOTTLE", "CASTLE", "PEPPER", "WINDOW", "TIGER", "BASKET")


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


def position_axes(center, x_length=6.0, y_length=3.0, ymax=1.0, font_size=18, ylabel=r"recalled"):
    """Axes for a serial-position curve over the sixteen positions."""
    return axes([1, 16], [0, ymax], x_length=x_length, y_length=y_length, xticks=[1, 4, 8, 12, 16],
                 yticks=[0, 0.5, 1] if ymax >= 1 else [0, ymax / 2, ymax], xlabel=r"position in the list",
                 ylabel=ylabel, center=center, font_size=font_size, yfmt=lambda v: f"{100 * v:.0f}\\%")


def lag_axes(center, x_length=6.0, y_length=3.0, ymax=0.5, font_size=18, max_lag=5):
    """Axes for a lag-CRP: lags -max_lag..max_lag."""
    return axes([-max_lag, max_lag], [0, ymax], x_length=x_length, y_length=y_length,
                xticks=list(range(-max_lag, max_lag + 1)), yticks=[0, ymax / 2, ymax], xlabel=r"lag",
                ylabel=r"probability of the next recall", center=center, font_size=font_size,
                xfmt=lambda v: f"{int(v):+d}" if v else "0", yfmt=lambda v: f"{v:.2f}")


def crp_curves(ax, lags, crp, color, stroke_width=4, dots=True) -> VGroup:
    """A lag-CRP drawn as two branches (negative and positive lags), with lag 0 left out."""
    lags, crp = np.asarray(lags, float), np.asarray(crp, float)
    out = VGroup()
    for side in (lags < 0, lags > 0):
        x, y = lags[side & np.isfinite(crp)], crp[side & np.isfinite(crp)]
        if len(x) > 1:
            out.add(curve(ax, x, y, color, stroke_width=stroke_width))
        if dots:
            out.add(scatter(ax, x, y, color, radius=0.06, opacity=1.0))
    return out


def word_chip(word: str, color=WORD, font_size=26, width=None) -> VGroup:
    """A word in a rounded box, the unit of the free-recall scenes."""
    t = label(word, font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=width or t.width + 0.3, height=t.height + 0.25,
                           stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
    return VGroup(box, t.move_to(box))


def grid_pattern(values, size=0.22, on=WORD, off="#2A2F3A", n=10) -> VGroup:
    """A +-1 pattern of n x n units drawn as squares (a Hopfield network's state)."""
    v = np.asarray(values, float).reshape(n, n)
    out = VGroup()
    for r in range(n):
        for c in range(n):
            out.add(Square(side_length=size * 0.92, stroke_width=0, fill_color=on if v[r, c] > 0 else off,
                           fill_opacity=1).move_to([c * size, -r * size, 0]))
    return out.center()


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
