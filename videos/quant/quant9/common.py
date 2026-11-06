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
    return wrapped_label("Pause and predict: " + question, width, 26, QC.HOUSE).move_to(UP * 0.9)


def answer_under(card, text, width=9.0):
    return wrapped_label(text, width, 24, GREY_A).next_to(card, DOWN, buff=0.45)


def side_why(text: str, width: float = 6.2, font_size=19):
    """A derivation note for a ladder that shares the frame with a picture: wrapped to the right column's width."""
    return wrapped_label(text, width, font_size, GREY_B)


class FullRangeReplay(TrainingReplay):
    """Part 9 replay with full data extrema instead of percentile clipping."""
    def __init__(self, steps, loss, frame, checkpoints, ylabel=r"loss", xlabel=r"training step", log_y=False,
                 color=None, left=LEFT * 3.3, right=RIGHT * 3.4, x_length=5.2, y_length=3.4, font_size=15,
                 log_x=False):
        import numpy as np
        super().__init__(steps, loss, frame, checkpoints, ylabel=ylabel, xlabel=xlabel, log_y=log_y,
                         color=color, left=left, right=right, x_length=x_length, y_length=y_length,
                         font_size=font_size, log_x=log_x)
        old_g, old_band = self.g, self.band
        lo, hi = float(np.nanmin(self.L)), float(np.nanmax(self.L))
        pad = 0.08 * (hi - lo + 1e-12)
        xt = [self.steps[0], self.steps[-1]]
        xfmt = (lambda v: f"{10 ** v:,.0f}".replace(",", r"{,}")) if log_x else (lambda v: f"{v:,.0f}".replace(",", r"{,}"))
        self.g = axes([self.steps[0], self.steps[-1]], [lo - pad, hi + pad], x_length=x_length,
                      y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xt, xfmt=xfmt,
                      yticks=[round(lo, 2), round(hi, 2)],
                      yfmt=(lambda v: f"10^{{{v:.1f}}}") if log_y else None,
                      font_size=font_size, center=right)
        self.ax = self.g.ax
        self.lo, self.hi = lo - pad, hi + pad
        self.band = band(self.ax, self.steps, self.L.min(0), self.L.max(0), self.color, 0.15) if len(self.L) > 1 else VGroup()
        self.remove(old_g, old_band)
        self.add(self.g, self.band)
        self._panel_off = np.asarray(left, float) - self.g.get_center()

    def _y(self, s):
        import numpy as np
        return float(np.interp(s, self.steps, self.L[0]))
