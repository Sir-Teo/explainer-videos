"""Helpers shared by the scenes of Part 3 ("All and Some": first-order logic)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import fol

from .compute import load  # noqa: F401

PART = 3
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
VAR = "#6FB7FF"       # variables
QUANT = "#C3A6FF"     # quantifiers
OBJ = "#5EE6D0"       # objects of a structure
REL = "#FF9F68"       # relations


def fm(s: str, font_size=38, color=WHITE) -> MathTex:
    """A first-order formula (Reasoner syntax) as TeX."""
    return MathTex(fol.show(fol.parse(s), tex=True), font_size=font_size, color=color)


def relation_graph(names, pairs, radius=2.0, center=ORIGIN, color=REL, node_color=OBJ, font_size=26) -> VGroup:
    """Objects on a circle, a binary relation as arrows (self-loops as small circles)."""
    n = len(names)
    c = np.asarray(center, float)
    pos = [c + radius * np.array([np.cos(PI / 2 - TAU * i / n), np.sin(PI / 2 - TAU * i / n), 0]) for i in range(n)]
    nodes = VGroup()
    for nm, p in zip(names, pos):
        d = Circle(radius=0.36, stroke_color=node_color, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=1)
        nodes.add(VGroup(d, label(nm, font_size=font_size, color=node_color).move_to(d)).move_to(p))
    arrows = VGroup()
    amap = {}
    for a, b in pairs:
        if a == b:
            loop = Circle(radius=0.22, stroke_color=color, stroke_width=2.5).move_to(
                pos[a] + (pos[a] - c) / np.linalg.norm(pos[a] - c) * 0.55)
            arrows.add(loop)
            amap[(a, b)] = loop
        else:
            ar = Arrow(pos[a], pos[b], buff=0.42, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.12)
            arrows.add(ar)
            amap[(a, b)] = ar
    g = VGroup(arrows, nodes)
    g.nodes, g.arrows, g.amap, g.pos = nodes, arrows, amap, pos
    return g


def tableau_tree(node, top=3.3, col_w=3.3, line_h=0.46, font_size=26, x_center=0.0, split_gap=0.32):
    """Draw a tableau. ``node`` = {"lines": [(formula_text, tag, closes)], "kids": [node, ...]}: a segment of formulas
    stacked down a branch, then the branches it splits into. Returns a VGroup with ``.steps``: the drawn pieces in
    depth-first order (each formula with its tag and × mark, and each split's two edges), for animating one by one."""
    def leaves(n):
        return max(1, sum(leaves(k) for k in n.get("kids", [])))

    g = VGroup()
    g.steps = []

    def draw(n, x, y, width):
        for f, tag, closes in n["lines"]:
            t = MathTex(fol.show(fol.parse(f), tex=True), font_size=font_size).move_to([x, y, 0])
            piece = VGroup(t)
            if tag:
                piece.add(label(tag, font_size=font_size - 8, color=GREY_B).next_to(t, RIGHT, buff=0.15))
            if closes:
                t.set_color(BAD)
                piece.add(MathTex(r"\times", font_size=font_size + 6, color=BAD).next_to(t, DOWN, buff=0.08))
            g.add(piece)
            g.steps.append(piece)
            y -= line_h
        kids = n.get("kids", [])
        if kids:
            total = sum(leaves(k) for k in kids)
            x0 = x - width / 2
            edges = VGroup()
            pos = []
            for k in kids:
                w = width * leaves(k) / total
                cx = x0 + w / 2
                pos.append((k, cx, w))
                edges.add(Line([x, y + line_h * 0.55, 0], [cx, y - split_gap + line_h * 0.35, 0], color=GREY_C,
                               stroke_width=2))
                x0 += w
            g.add(edges)
            g.steps.append(edges)
            for k, cx, w in pos:
                draw(k, cx, y - split_gap, w)

    draw(node, x_center, top, col_w * leaves(node))
    return g
