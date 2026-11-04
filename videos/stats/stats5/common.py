"""Helpers shared by the scenes of Part 5 of *Statistics, Built* ("Many Variables at Once")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 5

DATA = S.MUSEUM  # Galton's historical counts
WORLD = S.WORLD
COND = S.POST  # conditional distributions and means
MARG = S.EST  # marginals
LINE_YX, LINE_XY, LINE_MAJ = S.EST, S.LIK, S.ACCENT  # the three lines
EXACT = S.TRUTH
SIM = S.EST
IN2CM = 2.54


def money(v: float) -> str:
    return f"{v:,.0f}"


def ellipse_curve(ax, mean, cov, c=1.0, color=S.ACCENT, stroke_width=2.5, opacity=1.0, n=160) -> VMobject:
    ev, V = np.linalg.eigh(np.asarray(cov, float))
    th = np.linspace(0, TAU, n)
    pts = [np.asarray(mean) + c * (np.sqrt(ev[0]) * np.cos(t) * V[:, 0] + np.sqrt(ev[1]) * np.sin(t) * V[:, 1]) for t in th]
    return VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity).set_points_smoothly(
        [ax.c2p(*p) for p in pts])


def scatter(ax, x, y, color=WHITE, radius=0.025, opacity=0.7, xr=None, yr=None) -> VGroup:
    b = bounds(ax)
    xr = xr or b[:2]
    yr = yr or b[2:]
    return VGroup(*[Dot(ax.c2p(a, b), radius=radius, color=color, fill_opacity=opacity) for a, b in zip(x, y)
                    if xr[0] <= a <= xr[1] and yr[0] <= b <= yr[1]])
