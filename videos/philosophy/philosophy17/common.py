"""Helpers shared by the scenes of Part 17 ("Cause")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import causal as Ca  # noqa: F401

from .compute import load  # noqa: F401

PART = 17
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
CAUSE = "#F2A65A"     # causes
EFFECT = "#5EE6D0"    # effects
HIDDEN = "#9AA5B8"    # unobserved variables
DOC = "#F28EC2"       # interventions
SUZY, BILLY = "#F2A65A", "#6FB7FF"


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


class CausalGraph(VGroup):
    """Nodes at given positions with labels; edges as arrows; dashed bidirected arcs for hidden confounders.
    ``node[name]``, ``edge[(a, b)]``."""

    def __init__(self, pos: dict, edges, hidden=(), colors=None, radius=0.38, font_size=20, dashed=()):
        super().__init__()
        colors = colors or {}
        self.node, self.edge = {}, {}
        for n, p in pos.items():
            c = colors.get(n, HIDDEN if n in hidden else WHITE)
            circ = Circle(radius=radius, color=c, stroke_width=3).move_to(p)
            if n in hidden:
                circ = DashedVMobject(circ, num_dashes=18)
            t = label(n, font_size=font_size, color=c).move_to(p)
            g = VGroup(circ, t)
            self.node[n] = g
            self.add(g)
        for a, b in edges:
            pa, pb = np.array(pos[a], float), np.array(pos[b], float)
            u = (pb - pa) / np.linalg.norm(pb - pa)
            ar = Arrow(pa + u * radius, pb - u * radius, buff=0.02, color=GREY_B, stroke_width=3,
                       max_tip_length_to_length_ratio=0.18)
            if (a, b) in dashed:
                ar = DashedVMobject(ar, num_dashes=12)
            self.edge[(a, b)] = ar
            self.add(ar)

    def highlight(self, names, color):
        return [self.node[n][0].animate.set_color(color) for n in names]


def series_plot(ax, ys, color, xs=None, width=3) -> VMobject:
    xs = xs if xs is not None else list(range(len(ys)))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [ax.c2p(x, y) for x, y in zip(xs, ys)])
