"""Helpers shared by the scenes of Part 7 (Time Series and Volatility)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 7

RET = QC.SPOT          # returns, data
VOL = QC.IDEA          # volatility
FC = QC.OPTION         # forecasts, models
GOOD, BAD = QC.GAIN, QC.LOSS
ALT = QC.IMPLIED


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def tbar(ax, x, t, color, width=0.5, lo=0.0):
    """A bar from ``lo`` to ``t`` at position ``x`` on axes ``ax``."""
    top, bot = ax.c2p(x, max(t, lo)), ax.c2p(x, min(t, lo))
    w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
    return Rectangle(width=w, height=max(abs(top[1] - bot[1]), 0.01), stroke_width=0, fill_color=color,
                     fill_opacity=0.85).move_to((top + bot) / 2)
