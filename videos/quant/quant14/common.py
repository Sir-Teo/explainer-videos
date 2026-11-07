"""Helpers shared by the scenes of Part 14 (Rough and Path-Dependent Volatility)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 14

IV = QC.IMPLIED       # market implied volatility
VAR = QC.Q            # variance processes, models
RV = QC.REALIZED      # realized
ROUGH = QC.GAMMA      # rough models
BAD = QC.LOSS
SPOT = QC.SPOT
OPT = QC.OPTION

MODEL_COL = {"Heston": QC.Q, "rBergomi": QC.GAMMA, "rough Heston": QC.OPTION, "PDV": QC.VEGA, "power": QC.SPOT,
             "shifted": QC.DELTA}


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def loglog_skew_axes(x_length=7.0, y_length=4.4, t_lo=1 / 365, y_range=(-1.6, 0.6), font_size=15,
                     ylabel=r"at-the-money skew $|\partial_k\sigma|$ (log scale)"):
    """Log-log axes for the skew term structure: years to expiry against |skew|, both log10."""
    ticks = [x for x in (1 / 365, 3 / 365, 7 / 365, 30 / 365, 0.25, 1.0) if x >= t_lo * 0.999]
    g = axes([np.log10(t_lo), 0], list(y_range), x_length=x_length, y_length=y_length,
             xlabel=r"time to expiry (log scale)", ylabel=ylabel, xticks=[np.log10(x) for x in ticks],
             xfmt=lambda u: {0: "1y"}.get(round(u, 3), f"{365 * 10 ** u:.0f}d"), log_x=True, font_size=font_size)
    for v in (0.03, 0.1, 0.3, 1, 3):
        if y_range[0] <= np.log10(v) <= y_range[1]:
            g.add(label(f"{v:g}", font_size=font_size, color=GREY_B).next_to(g.ax.c2p(np.log10(t_lo), np.log10(v)),
                                                                            LEFT, buff=0.12))
    return g


def loglog_curve(ax, T, sk, color, y_range=(-1.6, 0.6), stroke_width=3):
    T, sk = np.asarray(T, float), np.abs(np.asarray(sk, float))
    ok = sk > 1e-4
    return curve(ax, np.log10(T[ok]), np.clip(np.log10(sk[ok]), *y_range), color, stroke_width=stroke_width)


def pause(question: str, width=7.2, font_size=24):
    return wrapped_label(question, max_width=width, font_size=font_size,
                         color=QC.IDEA).to_corner(DL, buff=0.3)


def running_min(xs):
    out, m = [], np.inf
    for x in xs:
        m = min(m, x)
        out.append(m)
    return np.array(out)
