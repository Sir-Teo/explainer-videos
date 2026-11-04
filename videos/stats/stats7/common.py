"""Helpers shared by the scenes of Part 7 of *Statistics, Built* ("Randomness on Demand")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 7

BAD = S.RESID  # RANDU and other failures
GOOD = S.EST  # PCG32 and honest draws
EXACT = S.TRUTH
ACC, REJ = S.LIK, S.RESID  # accepted, rejected
CHAIN = S.PRIOR


def scatter(ax, x, y, color=WHITE, radius=0.025, opacity=0.7, xr=None, yr=None) -> VGroup:
    b = bounds(ax)
    xr = xr or b[:2]
    yr = yr or b[2:]
    return VGroup(*[Dot(ax.c2p(a, c), radius=radius, color=color, fill_opacity=opacity) for a, c in zip(x, y)
                    if xr[0] <= a <= xr[1] and yr[0] <= c <= yr[1]])


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    m.set_points_as_corners([ax.c2p(a, b) for a, b in zip(xs, ys)])
    return m


def bars(ax, ks, ps, color, width=0.7, opacity=0.8) -> VGroup:
    g = VGroup()
    for k, p in zip(ks, ps):
        lo, hi = ax.c2p(k - width / 2, 0), ax.c2p(k + width / 2, p)
        g.add(Rectangle(width=hi[0] - lo[0], height=max(1e-3, hi[1] - lo[1]), stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
    return g


def fit_rows(rows: VGroup, width: float, buff: float, pos) -> VGroup:
    """Shrink any row wider than ``width``, left-align, and place the block's centre at ``pos``."""
    for r in rows:
        if r.width > width:
            r.width = width
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(pos)
    return rows
