"""Faithful local polyline plots; no experiment or model imports."""
from __future__ import annotations

import math

import numpy as np
from manim import VMobject


def _clip_segment(a, b, x_bounds, y_bounds):
    """Liang–Barsky clipping in data coordinates, including boundary contacts."""
    if not all(math.isfinite(v) for v in (*a, *b)):
        return None
    x0, y0 = a
    dx, dy = b[0] - x0, b[1] - y0
    xmin, xmax = x_bounds
    ymin, ymax = y_bounds
    if not all(math.isfinite(v) for v in (dx, dy, x0 - xmin, xmax - x0, y0 - ymin, ymax - y0)):
        raise ValueError("segment arithmetic overflows data coordinates")
    lo, hi = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0),
                 (-dy, y0 - ymin), (dy, ymax - y0)):
        if p == 0:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            lo = max(lo, t)
        else:
            hi = min(hi, t)
        if lo > hi:
            return None

    def at(t):
        # Reconstructing an unchanged endpoint can lose low bits after a large
        # subtraction. Keep original data vertices exactly at t=0 or t=1.
        if t == 0:
            return a
        if t == 1:
            return b
        x, y = x0 + t * dx, y0 + t * dy
        # Only intersection round-off is bounded here; outside data is never
        # projected onto an edge to fabricate a flat segment.
        return (min(max(x, xmin), xmax), min(max(y, ymin), ymax))

    return at(lo), at(hi), lo, hi


def clipped_curve(ax, xs, ys, *, x_bounds, y_bounds, color, stroke_width=3, **kw):
    """A piecewise-linear VMobject clipped to a rectangle in data coordinates.

    Visible original vertices are retained. Excursions outside the rectangle and
    nonfinite gaps split subpaths, even when exit and re-entry touch the same
    boundary point. No smoothing, flat caps or bridges are introduced.
    """
    xs, ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    if xs.ndim != 1 or ys.ndim != 1 or len(xs) != len(ys):
        raise ValueError("xs and ys must be one-dimensional arrays of equal length")
    x_bounds, y_bounds = tuple(x_bounds), tuple(y_bounds)
    if (len(x_bounds) != 2 or len(y_bounds) != 2
            or not all(math.isfinite(v) for v in (*x_bounds, *y_bounds))
            or x_bounds[0] >= x_bounds[1] or y_bounds[0] >= y_bounds[1]):
        raise ValueError("bounds must be finite, increasing pairs")
    result = VMobject(color=color, stroke_width=stroke_width, **kw)
    runs, run = [], []
    for p in zip(xs, ys):
        if all(math.isfinite(v) for v in p):
            run.append(p)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    for vertices in runs:
        if len(vertices) == 1:
            p = vertices[0]
            if (x_bounds[0] <= p[0] <= x_bounds[1]
                    and y_bounds[0] <= p[1] <= y_bounds[1]):
                result.start_new_path(ax.c2p(*p))
                result.add_line_to(ax.c2p(*p))
            continue
        previous_reached_vertex = False
        for a, b in zip(vertices, vertices[1:]):
            segment = _clip_segment(a, b, x_bounds, y_bounds)
            if segment is None:
                previous_reached_vertex = False
                continue
            start, end, lo, hi = segment
            if not (previous_reached_vertex and lo == 0):
                result.start_new_path(ax.c2p(*start))
            result.add_line_to(ax.c2p(*end))
            previous_reached_vertex = hi == 1
    return result
