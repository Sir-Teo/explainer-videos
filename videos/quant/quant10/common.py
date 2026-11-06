"""Helpers shared by the scenes of Part 10 (Black–Scholes–Merton)."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs  # noqa: F401

from .compute import load  # noqa: F401

PART = 10

# one meaning per colour, for the whole part (explainer.style.QC)
SPOT, OPT, DEL, GAM, THE, VEG = QC.SPOT, QC.OPTION, QC.DELTA, QC.GAMMA, QC.THETA, QC.VEGA
IMP, REA, CASH, QQ, PP = QC.IMPLIED, QC.REALIZED, QC.CASH, QC.Q, QC.P
GAIN, LOSS = QC.GAIN, QC.LOSS

COL = {
    r"S": SPOT, r"S_t": SPOT, r"dS": SPOT, r"S_T": SPOT, r"\Delta S": SPOT,
    r"V": OPT, r"V(t, S)": OPT, r"C": OPT, r"dV": OPT,
    r"\Delta": DEL, r"\partial_S V": DEL,
    r"\Gamma": GAM, r"\partial_{SS} V": GAM,
    r"\Theta": THE, r"\partial_t V": THE,
    r"\sigma": IMP, r"\sigma_i": IMP, r"\sigma_i^2": IMP, r"\sigma_r": REA, r"\sigma_r^2": REA,
    r"r": CASH, r"B": CASH, r"\mathbb Q": QQ, r"\mathbb P": PP, r"\mu": PP,
    r"K": QC.STRIKE, r"W": SPOT, r"dW": SPOT, r"dW_t": SPOT,
}


def ts_date(ts: float, fmt="%d %b %Y") -> str:
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime(fmt).lstrip("0")


def money(x: float, digits=2) -> str:
    return f"{x:+.{digits}f}"


def tag(text: str, color=GREY_B, font_size=20, corner=UR) -> Tex:
    return note(text, font_size=font_size, color=color).to_corner(corner, buff=0.3)


def computed(text=r"computed", corner=DR):
    return tag(text, corner=corner)


def real_data(text: str, corner=DR):
    """A source line for real data on screen."""
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


class FullRangeReplay(TrainingReplay):
    """Part 10 replay with full data extrema instead of percentile clipping."""
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


def common_side_density(ax, values, y_range, peak, bins=55, width=1.6, color=None, opacity=0.6):
    """Unclipped observed frequencies on a common count scale for the P/Q display."""
    h, edges = np.histogram(values, bins=bins, range=y_range)
    x0 = ax.get_right()[0] + 0.12
    g = VGroup()
    for k, count in enumerate(h):
        if not count:
            continue
        y0, y1 = ax.c2p(0, edges[k])[1], ax.c2p(0, edges[k + 1])[1]
        w = width * count / peak
        g.add(Rectangle(width=w, height=max(y1-y0-0.01, 0.005), stroke_width=0,
                        fill_color=color, fill_opacity=opacity).move_to([x0+w/2, (y0+y1)/2, 0]))
    return g
