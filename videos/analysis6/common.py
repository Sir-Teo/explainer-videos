"""Helpers shared by the scenes of Part 6 ("L^p, Hilbert Space and the Geometry of Functions").

Part 6 draws unit balls of the p-norms, functions with the areas between them shaded, right triangles of vectors
(projections, Bessel, Parseval), and measures as areas, atoms and staircases.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import heatmap, square_axes  # noqa: F401
from videos.analysis5.common import area_under, interval_band, step_graph  # noqa: F401

from .compute import load, trap  # noqa: F401


def p_ball_points(ax: Axes, p: float, r: float = 1.0, n: int = 720, center=(0.0, 0.0)) -> list:
    """The boundary of {|x|^p + |y|^p <= r^p} (p = np.inf for the square) as scene points on ax."""
    th = np.linspace(0, 2 * np.pi, n)
    c, s = np.cos(th), np.sin(th)
    if np.isinf(p):
        rad = 1 / np.maximum(np.abs(c), np.abs(s))
    else:
        rad = (np.abs(c) ** p + np.abs(s) ** p) ** (-1 / p)
    return [ax.c2p(center[0] + r * q * a, center[1] + r * q * b) for q, a, b in zip(rad, c, s)]


def p_ball(ax: Axes, p: float, color, r: float = 1.0, fill=0.15, stroke_width=3.5, center=(0.0, 0.0)) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=stroke_width, fill_color=color,
                    fill_opacity=fill).set_points_as_corners(p_ball_points(ax, p, r, center=center))


def pnorm(v, p: float) -> float:
    v = np.abs(np.asarray(v, float))
    return float(v.max()) if np.isinf(p) else float((v**p).sum() ** (1 / p))


def between(ax: Axes, x, y1, y2, color, opacity=0.35) -> Polygon:
    """The region between two graphs over the same x."""
    pts = [ax.c2p(a, b) for a, b in zip(x, y1)] + [ax.c2p(a, b) for a, b in zip(x[::-1], y2[::-1])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def vec(ax: Axes, a, b, color, stroke_width=4, tip=0.2) -> Arrow:
    """An arrow from point a to point b in ax's coordinates."""
    return Arrow(ax.c2p(*a), ax.c2p(*b), buff=0, color=color, stroke_width=stroke_width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=20)


def right_angle(ax: Axes, corner, d1, d2, size=0.18, color=GREY_B) -> VMobject:
    """The little square marking a right angle at ``corner`` between unit directions d1 and d2 (data coords)."""
    c = np.asarray(ax.c2p(*corner))
    u = np.asarray(ax.c2p(*(np.asarray(corner) + d1))) - c
    v = np.asarray(ax.c2p(*(np.asarray(corner) + d2))) - c
    u, v = u / np.linalg.norm(u) * size, v / np.linalg.norm(v) * size
    return VMobject(stroke_color=color, stroke_width=2).set_points_as_corners([c + u, c + u + v, c + v])
