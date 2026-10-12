"""Level curves by marching squares (no plotting library needed), drawn on manim Axes.

    segs = contour_segments(F, xs, ys, level)      # F(X, Y) vectorized; returns an (N, 2, 2) array of segments
    mob = contour_mobject(ax, segs, color, 2.0)    # one VMobject holding every segment as its own subpath
"""

from __future__ import annotations

import numpy as np
from manim import Axes, VMobject


def contour_segments(F, xs, ys, level=0.0) -> np.ndarray:
    X, Y = np.meshgrid(xs, ys)
    Z = F(X, Y) - level
    segs = []
    ny, nx = Z.shape
    z00, z10, z11, z01 = Z[:-1, :-1], Z[:-1, 1:], Z[1:, 1:], Z[1:, :-1]
    x0, x1 = X[:-1, :-1], X[:-1, 1:]
    y0, y1 = Y[:-1, :-1], Y[1:, :-1]

    def interp(za, zb, pa, pb):
        t = za / (za - zb)
        return pa + t * (pb - pa)

    # crossing points on each edge (NaN where the edge is not crossed)
    with np.errstate(invalid="ignore", divide="ignore"):
        cb = (z00 > 0) != (z10 > 0)  # bottom edge
        cr = (z10 > 0) != (z11 > 0)  # right edge
        ct = (z01 > 0) != (z11 > 0)  # top edge
        cl = (z00 > 0) != (z01 > 0)  # left edge
        pb = np.stack([interp(z00, z10, x0, x1), y0], -1)
        pr = np.stack([x1, interp(z10, z11, y0, y1)], -1)
        pt = np.stack([interp(z01, z11, x0, x1), y1], -1)
        pl = np.stack([x0, interp(z00, z01, y0, y1)], -1)
    edges = [(cb, pb), (cr, pr), (ct, pt), (cl, pl)]
    count = cb.astype(int) + cr + ct + cl
    for i, j in zip(*np.nonzero(count >= 2)):
        pts = [p[i, j] for c, p in edges if c[i, j]]
        if len(pts) == 2:
            segs.append(pts)
        elif len(pts) == 4:  # saddle: pair by the center value
            zc = (z00[i, j] + z10[i, j] + z11[i, j] + z01[i, j]) / 4
            b, r, t, l_ = pts
            if (zc > 0) == (z00[i, j] > 0):
                segs += [[b, r], [t, l_]]
            else:
                segs += [[b, l_], [r, t]]
    return np.array(segs).reshape(-1, 2, 2)


def contour_mobject(ax: Axes, segs: np.ndarray, color, stroke_width=2.0, opacity=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity, fill_opacity=0)
    for a, b in segs:
        pa, pb = ax.c2p(*a), ax.c2p(*b)
        m.start_new_path(pa)
        m.add_line_to(pb)
    return m


def contours(ax: Axes, F, xs, ys, levels, color, stroke_width=2.0, opacity=1.0):
    """A list of VMobjects, one per level."""
    return [contour_mobject(ax, contour_segments(F, xs, ys, lv), color, stroke_width, opacity) for lv in levels]
