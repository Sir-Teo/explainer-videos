"""Helpers shared by the scenes of Part 6 of *Statistics, Built* ("The Laws of Averages")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403
from explainer.stats import museum  # noqa: F401

from .compute import clipped_segments, load  # noqa: F401

PART = 6

DATA = S.MUSEUM  # historical data
WORLD = S.WORLD
EXACT = S.TRUTH  # exact laws and limits: gold
SIM = S.EST  # simulations: blue
BOUND = S.RESID  # inequalities and bounds: red
NORMAL = S.TRUTH


def scatter(ax, x, y, color=WHITE, radius=0.025, opacity=0.7, xr=None, yr=None) -> VGroup:
    b = bounds(ax)
    xr = xr or b[:2]
    yr = yr or b[2:]
    return VGroup(*[Dot(ax.c2p(a, c), radius=radius, color=color, fill_opacity=opacity) for a, c in zip(x, y)
                    if xr[0] <= a <= xr[1] and yr[0] <= c <= yr[1]])


def normal_pdf(x, mu=0.0, sd=1.0):
    return np.exp(-0.5 * ((np.asarray(x) - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def polyline(ax, xs, ys, color, stroke_width=2.5, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
    previous = None
    for start, end in clipped_segments(xs, ys, bounds(ax)):
        if previous is None or not np.allclose(previous, start, atol=1e-12, rtol=0):
            m.start_new_path(ax.c2p(*start))
        m.add_line_to(ax.c2p(*end))
        previous = end
    return m


def curve(ax, xs, ys, color=WHITE, stroke_width=2.5, opacity=1.0) -> VMobject:
    """Sampled curves use the same honest viewport clipping as running paths."""
    return polyline(ax, xs, ys, color, stroke_width, opacity)


def pmf_bars(ax, ks, ps, color, width=0.8, opacity=0.8) -> VGroup:
    g = VGroup()
    for k, p in zip(ks, ps):
        lo, hi = ax.c2p(k - width / 2, 0), ax.c2p(k + width / 2, p)
        g.add(Rectangle(width=hi[0] - lo[0], height=max(1e-3, hi[1] - lo[1]), stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
    return g
