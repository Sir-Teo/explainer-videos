"""Helpers shared by the scenes of Part 6 ("Paradise and Paradox": sets and the infinite)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import sets as S

from .compute import load  # noqa: F401

PART = 6
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
SETC = "#5EE6D0"      # sets drawn as boxes
ORD = "#C3A6FF"       # ordinals
CARD = "#FF9F68"      # cardinals
BIT1, BIT0 = "#7BD389", "#3A4150"
DEPTH_COLORS = ["#5EE6D0", "#6FB7FF", "#C3A6FF", "#F28EC2", "#FFD166"]


def set_box(s: frozenset, depth: int = 0, unit: float = 0.32) -> VGroup:
    """A hereditarily finite set as nested boxes: the empty set is a small empty box; a set is a box around its
    members, laid side by side (members in Ackermann order)."""
    col = DEPTH_COLORS[depth % len(DEPTH_COLORS)]
    if not s:
        return VGroup(RoundedRectangle(width=unit, height=unit, corner_radius=0.05, stroke_color=col,
                                       stroke_width=2.2))
    kids = VGroup(*[set_box(x, depth + 1, unit * 0.92) for x in sorted(s, key=S.ackermann_code)]).arrange(
        RIGHT, buff=0.08, aligned_edge=DOWN)
    box = RoundedRectangle(width=kids.width + 0.18, height=kids.height + 0.18, corner_radius=0.07,
                           stroke_color=col, stroke_width=2.2).move_to(kids)
    return VGroup(box, kids)


def bit_table(rows, cell=0.42, font_size=24) -> VGroup:
    """A table of 0/1 entries; ``self.cell[r][c]``."""
    g = VGroup()
    g.cell = []
    for r, row in enumerate(rows):
        cs = []
        for c, b in enumerate(row):
            sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D, fill_color=BIT1 if b else BIT0,
                        fill_opacity=0.35).move_to([c * cell, -r * cell, 0])
            t = MathTex(str(b), font_size=font_size, color=WHITE).move_to(sq)
            v = VGroup(sq, t)
            cs.append(v)
            g.add(v)
        g.cell.append(cs)
    return g


def ord_tex(s: str, font_size=34, color=ORD) -> MathTex:
    return MathTex(s, font_size=font_size, color=color)
