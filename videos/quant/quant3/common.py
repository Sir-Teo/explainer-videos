"""Helpers shared by the scenes of Part 3 (Value, Accounting and the Firm)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 3

PRICE = QC.SPOT        # market prices
VALUE = QC.IDEA        # present values, fundamentals
CASH = QC.GAIN         # cash flows
DEBT = QC.CASH         # debt, rates
EQUITY = QC.OPTION     # equity
LOSS, GAIN = QC.LOSS, QC.GAIN


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def live(prefix: str, value: float, digits: int = 2, suffix: str = "", font_size=28, color=WHITE, group_sep=False):
    """A readout rebuilt every frame cheaply: a fixed TeX prefix (compiled once) and a DecimalNumber (its digits
    are cached glyphs), so an always_redraw does not compile a new formula on every frame."""
    parts = [MathTex(prefix, font_size=font_size, color=color)] if prefix else []
    num_ = DecimalNumber(value, num_decimal_places=digits, font_size=font_size, color=color,
                         group_with_commas=group_sep)
    parts.append(num_)
    if suffix:
        parts.append(MathTex(suffix, font_size=font_size, color=color))
    return VGroup(*parts).arrange(RIGHT, buff=0.12)
