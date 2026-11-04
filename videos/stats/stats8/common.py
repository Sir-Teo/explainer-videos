"""Helpers shared by the scenes of Part 8 of *Statistics, Built* ("From Sample to Population")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import load  # noqa: F401

PART = 8

DATA = S.MUSEUM
EXACT = S.TRUTH  # exact sampling distributions: gold
SIM = S.EST  # simulated sampling distributions: blue
RESID = S.RESID
NORMAL = GREY_B  # the normal curve, when it is the wrong answer


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    m.set_points_as_corners([ax.c2p(a, b) for a, b in zip(xs, ys)])
    return m


def fit_rows(rows: VGroup, width: float, buff: float, pos) -> VGroup:
    """Shrink any row wider than ``width``, left-align, and place the block's centre at ``pos``."""
    for r in rows:
        if r.width > width:
            r.width = width
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(pos)
    return rows


def pdf_curve(ax, xs, ys, color, stroke_width=3, ymax=None):
    ys = np.asarray(ys, float)
    if ymax is not None:
        keep = ys <= ymax
        xs, ys = np.asarray(xs)[keep], ys[keep]
    return curve(ax, xs, ys, color, stroke_width)


def normal_pdf_(x, mu=0.0, sd=1.0):
    return np.exp(-0.5 * ((np.asarray(x) - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
