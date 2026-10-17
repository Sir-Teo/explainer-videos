"""Helpers shared by the scenes of Part 12 ("Memory")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
Q, K, V, A = C.QUERY, C.KEY, C.VALUE, C.ATTN
STATE = C.EMBED  # the fixed-size memory
ADD, DECAY, DELTA = C.SURPRISE, C.TRUE_P, C.INTERVAL  # the three ways to write to it


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def gib(n_bytes: float) -> str:
    """A byte count in the unit that reads best (KiB, MiB, GiB, TiB), as TeX."""
    for unit, p in (("TiB", 40), ("GiB", 30), ("MiB", 20), ("KiB", 10)):
        if n_bytes >= 2 ** p:
            v = n_bytes / 2 ** p
            return (f"{v:,.0f}" if v >= 100 else f"{v:.1f}" if v >= 10 else f"{v:.2f}").replace(",", "{,}") + rf"\,\mathrm{{{unit}}}"
    return f"{n_bytes:.0f}" + r"\,\mathrm{B}"


def grid_matrix(M, size, color=STATE, gamma=0.6) -> VGroup:
    """A small matrix as a grid of squares, brightness by |entry|."""
    M = np.asarray(M, float)
    n, m = M.shape
    top = max(np.abs(M).max(), 1e-9)
    cell = size / max(n, m)
    g = VGroup()
    for i in range(n):
        for j in range(m):
            g.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=color,
                         fill_opacity=float(0.08 + 0.85 * (abs(M[i, j]) / top) ** gamma))
                  .move_to([j * cell, -i * cell, 0]))
    return g.center()


def vec_column(vals, cell=0.22, color=K) -> VGroup:
    v = np.asarray(vals, float)
    top = max(np.abs(v).max(), 1e-9)
    return VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=color,
                           fill_opacity=float(0.15 + 0.75 * abs(x) / top)) for x in v]).arrange(DOWN, buff=0)
