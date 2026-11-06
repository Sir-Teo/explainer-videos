"""Helpers shared by the scenes of Part 18 ("Theories and Reality")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import science as Sc  # noqa: F401

from .compute import load  # noqa: F401

PART = 18
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
REAL = "#F2A65A"      # realism
ANTI = "#6FB7FF"      # anti-realism and empiricism
THEORY = "#5EE6D0"    # theories and laws
DATA = "#F28EC2"      # data and observation
UP_C, DOWN_C = "#F2A65A", "#3B6FB6"   # Ising spins


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-3.2, top=1.7, gap=0.42, label_size=22, text_size=21, width=9.6):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])


def spin_image(lattice, size: float) -> ImageMobject:
    """An Ising lattice (list of lists of +-1) as a crisp image of the given side length."""
    a = np.array(lattice)
    up = np.array([int(UP_C[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.uint8)
    dn = np.array([int(DOWN_C[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.uint8)
    rgb = np.where(a[..., None] > 0, up, dn).astype(np.uint8)
    rep = max(1, int(round(600 / a.shape[0])))
    rgb = np.kron(rgb, np.ones((rep, rep, 1), dtype=np.uint8))
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.height = size
    return img


def bar_hist(ax, counts, edges, color, opacity=0.5) -> VGroup:
    g = VGroup()
    for c, lo, hi in zip(counts, edges[:-1], edges[1:]):
        w = ax.c2p(hi, 0)[0] - ax.c2p(lo, 0)[0]
        h = ax.c2p(0, c)[1] - ax.c2p(0, 0)[1]
        g.add(Rectangle(width=w * 0.92, height=max(h, 1e-3), stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([ax.c2p((lo + hi) / 2, 0)[0], ax.c2p(0, 0)[1] + h / 2, 0]))
    return g
