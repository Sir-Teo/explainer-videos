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


class OrderBookLadder(VGroup):
    """The order book as queues: one row per price level (asks above, bids below), each resting share a block, so
    arrivals stack at the back of a queue, cancels take blocks out, and a market order bites blocks from the front.
    ``frames[t]`` holds the depth of the 2n levels (n bids, lowest first, then n asks) after event t; the drawing
    follows the float index ``tracker``.  ``kinds[t]`` (0/1 limit buy/sell, 2/3 market buy/sell, 4/5 cancels)
    colours the event marker."""

    def __init__(self, frames, tracker, kinds=None, block=0.13, row_h=0.32, max_blocks=24, price0=100.00,
                 tick=0.01):
        super().__init__()
        self.F = np.asarray(frames)
        self.kinds = None if kinds is None else np.asarray(kinds)
        self.t, self.block, self.row_h, self.maxb = tracker, block, row_h, max_blocks
        n2 = self.F.shape[1]
        self.n = n2 // 2
        self.anchor = VectorizedPoint(ORIGIN)
        self.prices = VGroup()
        for i in range(n2):
            px = price0 + (i - self.n) * tick
            col = QC.LOSS if i >= self.n else QC.GAIN
            self.prices.add(MathTex(f"{px:.2f}", font_size=20, color=col).move_to([-0.55, self._y(i), 0]))
        self.add(self.anchor, self.prices, always_redraw(self._draw))

    def _y(self, i):
        return (i - self.n + 0.5) * self.row_h

    def frame(self):
        return self.F[int(np.clip(round(self.t.get_value()), 0, len(self.F) - 1))]

    def best(self):
        f = self.frame()
        bids = np.flatnonzero(f[:self.n])
        asks = np.flatnonzero(f[self.n:])
        return (int(bids[-1]) if len(bids) else 0), (self.n + int(asks[0]) if len(asks) else 2 * self.n - 1)

    def _draw(self):
        f = self.frame()
        o = self.anchor.get_center()
        g = VGroup()
        for i, q in enumerate(f):
            col = QC.LOSS if i >= self.n else QC.GAIN
            for k in range(min(int(q), self.maxb)):
                g.add(Square(self.block * 0.86, stroke_width=0, fill_color=col, fill_opacity=0.85 - 0.02 * k)
                      .move_to(o + np.array([k * self.block + self.block / 2, self._y(i), 0])))
        bb, ba = self.best()
        x = -1.05
        br = VGroup(Line(o + [x, self._y(bb), 0], o + [x, self._y(ba), 0], color=QC.IDEA, stroke_width=3),
                    Line(o + [x, self._y(bb), 0], o + [x + 0.12, self._y(bb), 0], color=QC.IDEA, stroke_width=3),
                    Line(o + [x, self._y(ba), 0], o + [x + 0.12, self._y(ba), 0], color=QC.IDEA, stroke_width=3))
        g.add(br)
        return g


def ro(tex_left: str, fn, digits=2, font_size=30, color=WHITE, unit: str = "") -> VGroup:
    """A live readout: ``tex_left``, then a number that follows ``fn()``, then ``unit``, which stays beside the
    number however wide it grows."""
    left = MathTex(tex_left, font_size=font_size, color=color)
    num_ = DecimalNumber(fn(), num_decimal_places=digits, font_size=font_size, color=color)
    g = VGroup(left, num_).arrange(RIGHT, buff=0.15)
    u = MathTex(unit, font_size=font_size, color=color) if unit else None
    if u is not None:
        g.add(u)
        u.next_to(num_, RIGHT, buff=0.08)

    def upd(m):
        m.set_value(fn())
        m.next_to(left, RIGHT, buff=0.15)
        if u is not None:
            u.next_to(m, RIGHT, buff=0.08)
    num_.add_updater(upd)
    g.num = num_
    return g
