"""Helpers shared by the scenes of Part 9 (No Arbitrage)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 9

CALL, PUT = QC.GAIN, QC.LOSS   # calls, puts
FWD = QC.SPOT                  # forwards, the underlying
Q_C = QC.Q                     # state prices, Q, the density: risk-neutral objects
P_C = QC.P                     # real-world probabilities
ARB = QC.CRISIS                # arbitrage, violations
ALT = QC.OPTION
HEDGE = QC.DELTA               # hedges, deltas


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def tbar(ax, x, t, color, width=0.5, lo=0.0):
    top, bot = ax.c2p(x, max(t, lo)), ax.c2p(x, min(t, lo))
    w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
    return Rectangle(width=w, height=max(abs(top[1] - bot[1]), 0.01), stroke_width=0, fill_color=color,
                     fill_opacity=0.85).move_to((top + bot) / 2)


def pause_at(question, width=9.6):
    """A pause-and-predict card, centred a little high (the answer goes under it)."""
    return pause_card(question, color=QC.HOUSE, width=width).move_to(UP * 0.9)


def answer_under(card, text, width=9.0):
    return wrapped_label(text, width, 24, GREY_A).next_to(card, DOWN, buff=0.45)


def side_why(text: str, width: float = 6.2, font_size=19):
    """A derivation note for a ladder that shares the frame with a picture: wrapped to the right column's width."""
    return wrapped_label(text, width, font_size, GREY_B)
