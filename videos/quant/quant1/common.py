"""Helpers shared by the scenes of Part 1 (The Fair Game)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 1

# one meaning per colour, for the whole part (explainer.style.QC)
REAL = QC.SPOT          # real market data
GAUSS = GREY_B          # the Gaussian / random-walk benchmark
BTC = "#F7931A"         # Bitcoin, in its own orange
TAIL = QC.CRISIS        # tails and crashes
VOL = QC.REALIZED       # volatility, the size of moves
QQ, PP = QC.Q, QC.P     # risk-neutral and real-world
GAIN, LOSS = QC.GAIN, QC.LOSS
SMALL, LARGE = QC.GAMMA, "#2DD4BF"  # small stocks (pink) and large (teal)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def day_text(d: int) -> str:
    """19871019 -> '19 October 1987'."""
    d = int(d)
    return f"{d % 100} {MONTHS[(d // 100) % 100 - 1]} {d // 10000}"


def real_data(text: str, corner=DR):
    """A source line for real data on screen."""
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def bars(ax, xs, ys, width, color_pos, color_neg=None, opacity=0.9, min_h=0.004) -> VGroup:
    """Vertical bars from zero on ``ax`` (one per value)."""
    color_neg = color_neg or color_pos
    g = VGroup()
    for x, y in zip(xs, ys):
        y0, y1 = ax.c2p(x, 0)[1], ax.c2p(x, y)[1]
        g.add(Rectangle(width=width, height=max(abs(y1 - y0), min_h), stroke_width=0,
                        fill_color=color_pos if y >= 0 else color_neg, fill_opacity=opacity)
              .move_to([ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
    return g


def hist_bars(ax, edges, dens, color, opacity=0.75, stroke=False) -> VGroup:
    """A histogram drawn as bars on ``ax`` (``dens`` per bin between ``edges``)."""
    g = VGroup()
    for a, b, h in zip(edges[:-1], edges[1:], dens):
        if h <= 0:
            continue
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, h)
        g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.002), stroke_width=0.6 if stroke else 0,
                        stroke_color=BLACK, fill_color=color, fill_opacity=opacity)
              .move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
    return g


def sci(x: float, digits=1) -> str:
    """5.47e8 -> '5.5\\times 10^{8}' (TeX)."""
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    return rf"{m:.{digits}f}\times 10^{{{e}}}"


def words_years(x: float) -> str:
    """A spoken 'once every ...' for a huge number of years: '500 million', '3 thousand trillion'."""
    for v, w in ((1e15, "thousand trillion"), (1e12, "trillion"), (1e9, "billion"), (1e6, "million"),
                 (1e3, "thousand")):
        if x >= v:
            return f"{x / v:.0f} {w}"
    return f"{x:.0f}"
