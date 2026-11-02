"""Helpers shared by the scenes of Part 2 (The Machinery of Markets)."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 2

BTC = "#F7931A"
CASH = QC.CASH
CCP = QC.Q            # the clearing house
TRADE = QC.SPOT       # orders and trades
LOSS, GAIN = QC.LOSS, QC.GAIN
RATE = QC.IMPLIED     # interest rates
HOUSE = QC.HOUSE


def ts_date(ts: float, fmt="%d %b %Y") -> str:
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime(fmt).lstrip("0")


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def node(text: str, color, width=2.3, height=0.9, font_size=22) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.12)
    t = label(text, font_size=font_size)
    if t.width > width - 0.2:
        t.width = width - 0.2
    return VGroup(box, t.move_to(box))


def arrow(a: Mobject, b: Mobject, color=GREY_B, buff=0.08, sw=3) -> Arrow:
    return Arrow(a.get_right(), b.get_left(), buff=buff, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.18)


def lab(scene, card, outputs, **kw):
    """Run a lab card: its printed output is data (numbers and code), shown as it is in both languages."""
    from explainer.zh_text import verbatim
    with verbatim():
        return lab_run(scene, card, outputs, **kw)


def fmt_bn(x: float, digits=1) -> str:
    return f"{x:.{digits}f}"


def pct(x: float, digits=1) -> str:
    return f"{100 * x:.{digits}f}"
