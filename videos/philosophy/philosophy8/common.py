"""Helpers shared by the scenes of Part 8 ("The Liar": truth and paradox)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import truth as Tr

from .compute import load  # noqa: F401

PART = 8
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
SELF = "#F28EC2"
GLUT = "#C3A6FF"
VCOL = {"t": P.TRUE, "f": P.FALSE, "n": "#5A6372", "b": GLUT}
VTEX = {"t": r"\mathsf{t}", "f": r"\mathsf{f}", "n": r"\mathsf{n}", "b": r"\mathsf{b}"}

# where each sentence of the toy world sits on screen
POS = {"s1": (-5.7, 1.9), "s2": (-5.7, -0.9), "s3": (-3.0, 2.5), "s4": (-3.0, 0.4), "s5": (-0.4, 1.5),
       "s9": (-0.4, -0.5), "s10": (-0.4, -2.4), "L": (2.6, 1.9), "s8": (5.4, 1.9), "H": (2.6, -0.2),
       "s13": (5.4, -0.2), "A": (2.6, -2.4), "B": (5.4, -2.4)}


def sentence_node(name: str, gloss: str, width: float = 2.3, font_size=20) -> VGroup:
    """A sentence of the toy world: its name, and what it says, in a box whose fill shows its value."""
    nm = label(rf"\textbf{{{name}}}", font_size=font_size + 4, color=WHITE)
    gl = label(gloss.replace("‘", "`").replace("’", "'"), font_size=font_size, color=GREY_A)
    if gl.width > width - 0.2:
        gl.width = width - 0.2
    inner = VGroup(nm, gl).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(width=width, height=inner.height + 0.3, corner_radius=0.1, stroke_color=GREY_C,
                           stroke_width=2, fill_color="#151A24", fill_opacity=1)
    inner.move_to(box)
    g = VGroup(box, inner)
    g.box = box
    return g


def world_graph(d: dict, width: float = 2.3) -> VGroup:
    """The toy world: one node per sentence, and an arrow from each sentence to every sentence it mentions.
    ``self.node[name]``, ``self.edges``."""
    g = VGroup()
    g.node = {}
    for n in d["names"]:
        nd = sentence_node(n, d["gloss"][n], width=width).move_to([*POS[n], 0])
        g.node[n] = nd
    g.edges = VGroup()
    for n, rs in d["refs"].items():
        for r in rs:
            a, b = g.node[n], g.node[r]
            if r == n:
                loop = CurvedArrow(a.get_corner(UR) + LEFT * 0.4, a.get_corner(UR) + DOWN * 0.15, angle=-2.6,
                                   color=SELF, stroke_width=2, tip_length=0.12)
                g.edges.add(loop)
            else:
                g.edges.add(Arrow(a.get_center(), b.get_center(), buff=0.62, color=GREY_B, stroke_width=2,
                                  stroke_opacity=0.6, max_tip_length_to_length_ratio=0.08))
    g.add(g.edges, *g.node.values())
    return g


def paint(node: VGroup, v: str):
    """The animation that fills a sentence's box with the colour of value v."""
    return node.box.animate.set_fill(VCOL[v], opacity=0.55 if v != "n" else 1.0).set_stroke(VCOL[v] if v != "n"
                                                                                           else GREY_C)


def value_chip(v: str, font_size=26) -> VGroup:
    sq = RoundedRectangle(width=0.5, height=0.42, corner_radius=0.06, stroke_width=0, fill_color=VCOL[v],
                          fill_opacity=0.85)
    return VGroup(sq, MathTex(VTEX[v], font_size=font_size, color=WHITE).move_to(sq))
