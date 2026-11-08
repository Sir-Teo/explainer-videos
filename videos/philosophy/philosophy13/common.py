"""Helpers shared by the scenes of Part 13 ("Degrees of Belief")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import credence as Cr  # noqa: F401

from .compute import load  # noqa: F401

PART = 13
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
CRED = "#9DB4FF"      # credences
COH = "#5EE6D0"       # the coherent region
INC = "#F28EC2"       # incoherent credences
BET = "#FFD166"       # bets and money
WORLD_C = ["#6FB7FF", "#F2A65A", "#C3A6FF"]


def mark(ok: bool, font_size=30) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=OK if ok else BAD)


class Plane2(VGroup):
    """Credences in A and not-A as a point in the unit square; the coherent ones lie on the diagonal x + y = 1."""

    def __init__(self, center=ORIGIN, size=4.0, labels=True):
        super().__init__()
        self.ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=size, y_length=size, tips=False,
                       axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to(center)
        self.line = Line(self.ax.c2p(0, 1), self.ax.c2p(1, 0), color=COH, stroke_width=5)
        self.add(self.ax, self.line)
        if labels:
            self.xl = MathTex(r"c(A)", font_size=26).next_to(self.ax.x_axis, DOWN, buff=0.35)
            self.yl = MathTex(r"c(\lnot A)", font_size=26).next_to(self.ax.y_axis, LEFT, buff=0.35)
            self.vA = label(r"world $A$: \ (1, 0)", font_size=18, color=WORLD_C[0]).next_to(self.ax.c2p(1, 0), RIGHT,
                                                                                          buff=0.25)
            self.vN = label(r"world $\lnot A$: \ (0, 1)", font_size=18, color=WORLD_C[1]).next_to(
                self.ax.c2p(0, 1), UP, buff=0.2)
            self.add(self.xl, self.yl, self.vA, self.vN)

    def p(self, x, y):
        return self.ax.c2p(x, y)


class Simplex3(VGroup):
    """Credences over three worlds as a point in the cube; the coherent ones fill the triangle with corners (1,0,0),
    (0,1,0), (0,0,1)."""

    def __init__(self, origin=ORIGIN, scale=2.6):
        super().__init__()
        self.o, self.s = np.asarray(origin, float), scale
        O = self.p((0, 0, 0))
        axes = VGroup(*[Arrow(O, self.p(e), buff=0, color=GREY_C, stroke_width=2, max_tip_length_to_length_ratio=0.06)
                        for e in ((1.2, 0, 0), (0, 1.2, 0), (0, 0, 1.2))])
        names = VGroup(MathTex(r"c(w_1)", font_size=22).next_to(self.p((1.2, 0, 0)), RIGHT, buff=0.1),
                       MathTex(r"c(w_2)", font_size=22).next_to(self.p((0, 1.2, 0)), LEFT, buff=0.1),
                       MathTex(r"c(w_3)", font_size=22).next_to(self.p((0, 0, 1.2)), UP, buff=0.1))
        tri = Polygon(self.p((1, 0, 0)), self.p((0, 1, 0)), self.p((0, 0, 1)), stroke_color=COH, stroke_width=3,
                      fill_color=COH, fill_opacity=0.18)
        verts = VGroup(*[Dot(self.p(v), radius=0.08, color=WORLD_C[i]) for i, v in
                         enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1)))])
        self.axes, self.names, self.tri, self.verts = axes, names, tri, verts
        self.add(axes, names, tri, verts)

    def p(self, v):
        x, y, z = v
        return self.o + self.s * np.array([x - 0.5 * y, -0.42 * y + 0.0 * x + z * 0.95 - 0.12 * x, 0])


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
