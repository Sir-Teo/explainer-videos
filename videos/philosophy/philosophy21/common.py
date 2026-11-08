"""Helpers shared by the scenes of Part 21 ("Identity and Persistence")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import persist as Pe  # noqa: F401

from .compute import load  # noqa: F401

PART = 21
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
PARTC = "#5EE6D0"     # parts, planks, stages
WHOLE = "#F2A65A"     # wholes, ships, worms
UNIV = "#6FB7FF"      # relations, continuity
NOM = "#F28EC2"       # persons, selves
ABS = "#C3A6FF"       # modal and logical machinery


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            if m.width > 1.15 * width:  # break a long row into lines rather than shrink it out of legibility
                m = wrapped_label(t, width, font_size, c)
            else:
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


def hasse(n: int, edges, names=None, center=ORIGIN, width=4.0, height=3.0, color=PARTC, radius=0.12,
          font_size=18, top_color=WHOLE) -> VGroup:
    """Draw a Hasse diagram: nodes placed by rank (longest chain from below), edges from part to whole. Returns a
    VGroup with ``.dots``, ``.lines``, ``.names`` and ``.pos``."""
    below = {i: [a for a, b in edges if b == i] for i in range(n)}
    rank = {}

    def rk(i):
        if i not in rank:
            rank[i] = 0 if not below[i] else 1 + max(rk(j) for j in below[i])
        return rank[i]

    for i in range(n):
        rk(i)
    levels = {}
    for i in range(n):
        levels.setdefault(rank[i], []).append(i)
    top = max(levels) if levels else 0
    pos = {}
    c = np.array(center, float)
    for r, items in levels.items():
        y = c[1] - height / 2 + (height * r / top if top else height / 2)
        for k, i in enumerate(items):
            x = c[0] + (k - (len(items) - 1) / 2) * (width / max(1, len(items) - 1) if len(items) > 1 else 0)
            if len(items) > 1:
                x = c[0] - width / 2 + width * k / (len(items) - 1)
            pos[i] = np.array([x, y, 0])
    g = VGroup()
    g.lines = VGroup(*[Line(pos[a], pos[b], color=GREY_B, stroke_width=2.5) for a, b in edges])
    g.dots = VGroup(*[Dot(pos[i], radius=radius, color=top_color if rank[i] == top and top > 0 else color)
                      for i in range(n)])
    g.names = VGroup()
    if names:
        for i in range(n):
            g.names.add(label(names[i], font_size=font_size, color=GREY_A).next_to(
                g.dots[i], DOWN if rank[i] == 0 else UP, buff=0.12))
    g.pos = pos
    g.add(g.lines, g.dots, g.names)
    return g


def block_grid(rows: int, cols: int, chosen=(), size=0.6, center=ORIGIN, on=PARTC, off=GREY_D) -> VGroup:
    """A grid of square simples; ``chosen`` cells are highlighted."""
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            sq = Square(side_length=size * 0.9, stroke_width=1.5, stroke_color=GREY_B,
                        fill_color=on if i in chosen else off, fill_opacity=0.85 if i in chosen else 0.25)
            sq.move_to(np.array(center) + np.array([(c - (cols - 1) / 2) * size, ((rows - 1) / 2 - r) * size, 0]))
            g.add(sq)
    return g


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if y is not None]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)
