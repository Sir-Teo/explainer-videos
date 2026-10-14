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
    """The boundary of {|x|^p + |y|^p <= r^p} (p = np.inf for the square) as scene points on ax.

    For p < 1 (a star with cusps) equal angles would cut the four tips off, so the curve is parametrized by
    |x| = r |cos t|^{2/p}, |y| = r |sin t|^{2/p} with t through every multiple of pi/2: the tips are on the curve."""
    if p < 1:
        m = n // 4
        t = np.linspace(0, 2 * np.pi, 4 * m + 1)
        c, s = np.cos(t), np.sin(t)
        c[::m], s[::m] = np.round(c[::m]), np.round(s[::m])  # the four tips exactly
        x, y = r * np.sign(c) * np.abs(c) ** (2 / p), r * np.sign(s) * np.abs(s) ** (2 / p)
        assert np.allclose(np.abs(x) ** p + np.abs(y) ** p, r**p) and np.isclose(np.abs(x).max(), r)
        return [ax.c2p(center[0] + a, center[1] + b) for a, b in zip(x, y)]
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


def dict_table(left_title: str, right_title: str, pairs, xs=(-1.6, 0.25, 3.55), widths=(2.8, 5.6), top=2.55,
               font_size=24, gap=0.3, colors=None) -> VGroup:
    """The series' two-column dictionary (as ``dictionary_card``: centred cells, a grey double arrow between them),
    laid out on given column centres ``xs = (left, arrow, right)`` so a picture can sit beside it.  A cell wider than
    its column wraps onto further lines instead of shrinking.  ``colors`` maps a row index to its right cell's colour.
    Returns a VGroup with .titles, .rows (each VGroup(left, right)) and .arrows."""
    lx, mx, rx = xs
    lt = label(left_title, font_size=font_size + 4, color=GREY_A).move_to([lx, top, 0])
    rt = label(right_title, font_size=font_size + 4, color=GREY_A).move_to([rx, top, 0])
    rows, arrows = VGroup(), VGroup()
    y = top - max(lt.height, rt.height) / 2 - 0.5
    for i, (l_, r_) in enumerate(pairs):
        lm = wrapped_label(l_, widths[0], font_size)
        rm = wrapped_label(r_, widths[1], font_size, (colors or {}).get(i, WHITE))
        h = max(lm.height, rm.height)
        lm.move_to([lx, y - h / 2, 0])
        rm.move_to([rx, y - h / 2, 0])
        rows.add(VGroup(lm, rm))
        arrows.add(MathTex(r"\longleftrightarrow", color=GREY_C, font_size=34).move_to([mx, y - h / 2, 0]))
        y -= h + gap
    g = VGroup(VGroup(lt, rt), rows, arrows)
    g.titles, g.rows, g.arrows = g[0], rows, arrows
    return g


def left_y_axis(ax: Axes, values, decimals=0, font_size=18, color=GREY_C, stroke_width=2.0) -> VGroup:
    """A numbered y-axis at the left edge of ``ax`` (x = x_min), so no curve, chord or hull inside the plot ever
    runs through a tick number.  The axes' own y-axis at x = 0 stays, unnumbered.  Manim always puts the y-axis at
    x = 0 when 0 is in the x-range."""
    x0, (y0, y1) = ax.x_range[0], ax.y_range[:2]
    g = VGroup(Line(ax.c2p(x0, y0), ax.c2p(x0, y1), color=color, stroke_width=stroke_width))
    for v in values:
        p = ax.c2p(x0, v)
        g.add(Line(p + LEFT * 0.08, p + RIGHT * 0.08, color=color, stroke_width=stroke_width))
        g.add(MathTex(f"{v:.{decimals}f}", font_size=font_size).next_to(p, LEFT, buff=0.15))
    return g
