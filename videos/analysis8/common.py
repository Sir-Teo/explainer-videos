"""Helpers shared by the scenes of Part 8 ("Banach Spaces")."""

from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import square_axes  # noqa: F401
from videos.analysis6.common import between, p_ball, pnorm  # noqa: F401

from .compute import load, trap  # noqa: F401


def p_ball_exact_points(ax, p: float, r: float = 1.0, m: int = 240, center=(0.0, 0.0)) -> list:
    """The boundary of {|x|^p + |y|^p <= r^p} for finite p as scene points on ax, parametrized by
    |x| = r |cos t|^{2/p}, |y| = r |sin t|^{2/p} (so |x|^p + |y|^p = r^p exactly), with t running over 4m + 1
    points that include every multiple of pi/2: the four tips of a star (p < 1) are on the curve, not cut off as
    equal-angle sampling does."""
    t = np.linspace(0, 2 * np.pi, 4 * m + 1)
    c, s = np.cos(t), np.sin(t)
    c[::m] = np.round(c[::m])  # the quarter points exactly
    s[::m] = np.round(s[::m])
    x = r * np.sign(c) * np.abs(c) ** (2 / p)
    y = r * np.sign(s) * np.abs(s) ** (2 / p)
    assert np.allclose(np.abs(x) ** p + np.abs(y) ** p, r**p)
    return [ax.c2p(center[0] + a, center[1] + b) for a, b in zip(x, y)]


def p_ball_exact(ax, p: float, color, r: float = 1.0, fill=0.15, stroke_width=3.5, center=(0.0, 0.0)) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=stroke_width, fill_color=color,
                    fill_opacity=fill).set_points_as_corners(p_ball_exact_points(ax, p, r, center=center))


def y_axis_at(ax, x_at: float, values=(), font_size=18, decimals=0, color=GREY_C, stroke_width=2.0) -> VGroup:
    """Move the y-axis of ``ax`` to x = x_at (left of the first bar or dot, which would otherwise sit on it): the
    axes' own y-axis is hidden, and a line with ticks (and numbers at ``values``) is drawn at x_at instead.
    Manim always puts the y-axis at x = 0 when 0 is in the x-range."""
    ax.y_axis.set_opacity(0)
    y0, y1 = ax.y_range[0], ax.y_range[1]
    g = VGroup(Line(ax.c2p(x_at, y0), ax.c2p(x_at, y1), color=color, stroke_width=stroke_width))
    for v in values:
        p = ax.c2p(x_at, v)
        g.add(Line(p + LEFT * 0.1, p + RIGHT * 0.1, color=color, stroke_width=stroke_width))
        g.add(MathTex(f"{v:.{decimals}f}", font_size=font_size).next_to(p, LEFT, buff=0.18))
    return g


def logn_axes(width: float, height: float, y_max: float = 7.5, y_step: float = 2, k_max: int = 6, labelled=(0, 2, 4, 6),
              font_size: int = 18, y_numbers=(2, 4, 6)) -> tuple:
    """The axes of the Part 8 plots of ||D_n||_1 against n: log10 n on [0, k_max] with 10^k under the ticks in
    ``labelled``; the y-axis sits 0.4 to the left of 10^0, so the dot at n = 1 is not drawn on it.
    Returns (ax, decor): plot at ax.c2p(log10 n, value)."""
    ax = plain_axes([-0.4, k_max + 0.05, 1], [0, y_max, y_step], width, height)
    decor = y_axis_at(ax, -0.4, y_numbers, font_size=font_size)
    decor.add(*[MathTex(rf"10^{{{k}}}", font_size=font_size).next_to(ax.c2p(k, 0), DOWN, buff=0.12) for k in labelled])
    return ax, decor


def fixed_runs(ax, x, y, color, stroke_width=3.0, pieces=10) -> VGroup:
    """The graph of y over x cut where it leaves the axes' y-range (never flattened against the edge), as a group of
    exactly ``pieces`` polylines, so a curve redrawn every frame keeps one family shape (become() scrambles a group
    whose size changes). Each piece ends exactly on the window's edge; unused pieces are invisible points."""
    lo, hi = ax.y_range[0], ax.y_range[1]
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = (y >= lo) & (y <= hi)
    runs_ = []
    i, n = 0, len(x)
    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and ok[j + 1]:
            j += 1
        xs, ys = list(x[i:j + 1]), list(y[i:j + 1])
        for a, b, front in ((i - 1, i, True), (j + 1, j, False)):  # extend to the crossing with the edge
            if 0 <= a < n:
                edge = hi if y[a] > hi else lo
                xc = x[b] + (edge - y[b]) * (x[a] - x[b]) / (y[a] - y[b])
                if front:
                    xs.insert(0, xc)
                    ys.insert(0, edge)
                else:
                    xs.append(xc)
                    ys.append(edge)
        runs_.append((np.array(xs), np.array(ys)))
        i = j + 1
    assert len(runs_) <= pieces, (len(runs_), pieces)
    g = VGroup()
    for xs, ys in runs_:
        g.add(polyline(ax, xs, ys, color=color, stroke_width=stroke_width))
    while len(g) < pieces:
        p = ax.c2p(float(x[0]), max(lo, min(hi, 0.0)))
        g.add(VMobject(stroke_width=0, stroke_opacity=0).set_points_as_corners([p, p + RIGHT * 1e-4]))
    return g


def clip_to_box(p0, p1, box) -> tuple | None:
    """The part of the segment p0 -> p1 (data coordinates) inside box = (xmin, xmax, ymin, ymax) (Liang-Barsky),
    or None if it misses the box."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - box[0]), (dx, box[1] - x0), (-dy, y0 - box[2]), (dy, box[3] - y0)):
        if abs(p) < 1e-15:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 > t1:
        return None
    return (np.array([x0 + t0 * dx, y0 + t0 * dy]), np.array([x0 + t1 * dx, y0 + t1 * dy]))


def boxes_overlap(a: Mobject, b: Mobject, pad: float = 0.0) -> bool:
    return not (a.get_right()[0] + pad < b.get_left()[0] or b.get_right()[0] + pad < a.get_left()[0]
                or a.get_top()[1] + pad < b.get_bottom()[1] or b.get_top()[1] + pad < a.get_bottom()[1])


def curve_hits_box(points, m: Mobject, pad: float = 0.04) -> bool:
    """Whether any of the scene points (n x 3) lies inside m's bounding box (grown by pad)."""
    P = np.asarray(points)
    x0, x1 = m.get_left()[0] - pad, m.get_right()[0] + pad
    y0, y1 = m.get_bottom()[1] - pad, m.get_top()[1] + pad
    return bool(np.any((P[:, 0] >= x0) & (P[:, 0] <= x1) & (P[:, 1] >= y0) & (P[:, 1] <= y1)))


def dense_points(m: VMobject, per_curve: int = 12) -> np.ndarray:
    """Sample points along every curve in m's family (for collision checks against labels)."""
    out = []
    for sm in m.family_members_with_points():
        P = sm.points
        for k in range(0, len(P) - 3, 4):
            a, b, c, d = P[k:k + 4]
            for t in np.linspace(0, 1, per_curve):
                out.append((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d)
    return np.array(out) if out else np.zeros((0, 3))

