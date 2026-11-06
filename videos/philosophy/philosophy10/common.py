"""Helpers shared by the scenes of Part 10 ("The Mind's Own Laws": Descartes to Kant)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import modern as Mo  # noqa: F401
from explainer.zh_text import verbatim

from .compute import load  # noqa: F401

PART = 10
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
REASON = "#9DB4FF"     # the rationalists: reason, innate ideas
SENSE = "#E0B07A"      # the empiricists: experience, impressions
KANT = "#C3A6FF"       # the mind's own forms
DOUBT = "#F28EC2"
KIND_COL = {"D": "#6FB7FF", "A": "#E8C07D", "P": "#C3A6FF"}


def ethics_dag(d: dict, x0=-6.2, x1=6.2, top=2.9, gap=0.4, r=0.075, font_size=13, labels=True) -> VGroup:
    """Spinoza's Ethics I as a layered graph: one column per depth (definitions and axioms first), an edge from
    every item cited to the proposition that cites it. ``g.node[name]``, ``g.edge[(a, b)]``, ``g.cols``."""
    depth = d["depth"]
    cols = {}
    for n in d["nodes"]:
        cols.setdefault(depth[n], []).append(n)
    ncol = max(cols) + 1
    pos = {}
    for c, names in cols.items():
        x = x0 + (x1 - x0) * c / (ncol - 1)
        h = gap * (len(names) - 1)
        for i, n in enumerate(names):
            pos[n] = np.array([x, h / 2 - i * gap + (top - 2.9), 0])
    g = VGroup()
    g.node, g.edge, g.pos, g.label = {}, {}, pos, {}
    edges = VGroup()
    for a, b in d["edges"]:
        ln = Line(pos[a], pos[b], color=GREY_B, stroke_width=1, stroke_opacity=0.35)
        g.edge[(a, b)] = ln
        edges.add(ln)
    dots = VGroup()
    labs = VGroup()
    for n, p in pos.items():
        dt = Dot(p, radius=r, color=KIND_COL[n[0]])
        g.node[n] = dt
        dots.add(dt)
        if labels:
            with verbatim():
                t = Text(n, font=MONO, font_size=font_size, color=GREY_A).next_to(dt, UP, buff=0.04)
            g.label[n] = t
            labs.add(t)
    g.edges, g.dots, g.labs = edges, dots, labs
    g.add(edges, dots, labs)
    g.cols = cols
    return g


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def rows_at(pairs, x_left=-6.2, x_right=-2.4, y0=1.6, dy=0.75, font_size=24, left_color=WHITE, right_color=GREY_A):
    g = VGroup()
    for i, (a, b) in enumerate(pairs):
        y = y0 - i * dy
        la = label(a, font_size=font_size, color=left_color).move_to([x_left, y, 0], aligned_edge=LEFT)
        lb = label(b, font_size=font_size - 2, color=right_color).move_to([x_right, y, 0], aligned_edge=LEFT)
        g.add(VGroup(la, lb))
    return g
