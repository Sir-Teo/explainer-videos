"""Helpers shared by the scenes of Part 7 ("The Limits of Proof": Gödel, Turing, Tarski, Löb)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import arith as A

from .compute import load  # noqa: F401

PART = 7
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
NUM = "#FFD166"        # Gödel numbers, codes
TAPE = "#5EE6D0"       # Turing tapes
PROV = "#C3A6FF"       # provability, Prov(x)
SELF = "#F28EC2"       # self-reference
STATE_COLORS = {"A": "#FF6B6B", "B": "#6FB7FF", "C": "#7BD389", "D": "#FFD166", "E": "#C3A6FF", "H": "#FFFFFF"}


def tape_row(cells, head: int | None = None, state: str | None = None, cell: float = 0.46, font_size=24) -> VGroup:
    """A strip of tape: squares with 0/1, the head as a triangle under its square, labelled by the state.
    ``self.sq[i]``, ``self.head``."""
    g = VGroup()
    g.sq = VGroup()
    for i, b in enumerate(cells):
        sq = Square(side_length=cell, stroke_width=1.5, stroke_color=GREY_C,
                    fill_color=TAPE if b else "#151A24", fill_opacity=0.55 if b else 1.0).move_to([i * cell, 0, 0])
        t = MathTex(str(b), font_size=font_size, color=WHITE if b else GREY_B).move_to(sq)
        g.sq.add(VGroup(sq, t))
    g.add(g.sq)
    g.head = VGroup()
    if head is not None:
        col = STATE_COLORS.get(state, WHITE)
        tri = Triangle(color=col, fill_color=col, fill_opacity=0.9, stroke_width=0).scale(0.13).next_to(
            g.sq[head], DOWN, buff=0.08)
        g.head = VGroup(tri, MathTex(state or "", font_size=font_size - 2, color=col).next_to(tri, DOWN, buff=0.06))
        g.add(g.head)
    return g


def head_mark(row: VGroup, i: int, state: str, font_size=22) -> VGroup:
    col = STATE_COLORS.get(state, WHITE)
    tri = Triangle(color=col, fill_color=col, fill_opacity=0.9, stroke_width=0).scale(0.13).next_to(
        row.sq[i], DOWN, buff=0.08)
    return VGroup(tri, MathTex(state, font_size=font_size, color=col).next_to(tri, DOWN, buff=0.06))


def spacetime_image(rows, height: float = 6.0, across: bool = False) -> ImageMobject:
    """The space–time diagram of a run: one row of pixels per step, 1s light, the head's cell in its state's
    colour (``across``: one column per step, time running to the right). Drawn with nearest-neighbour scaling so
    each cell stays a crisp square."""
    h, w = len(rows), len(rows[0][0])
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:, :] = (21, 26, 36)
    for y, (cells, head, state) in enumerate(rows):
        for x, b in enumerate(cells):
            if b:
                img[y, x] = (94, 230, 208)
        col = ManimColor(STATE_COLORS.get(state, "#FFFFFF")).to_rgb()
        img[y, head] = tuple(int(255 * c) for c in col)
    if across:
        img = np.ascontiguousarray(np.transpose(img, (1, 0, 2))[::-1])
    im = ImageMobject(img)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    im.height = height
    return im


def code_tex(s: str, font_size=28, color=WHITE) -> Tex:
    """A short line of code or a string, set in typewriter type."""
    esc = (s.replace("\\", r"\textbackslash{}").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")
           .replace("{", r"\{").replace("}", r"\}").replace("'", r"\textquotesingle{}"))
    return Tex(r"\texttt{" + esc + "}", font_size=font_size, color=color)


def gnum_tex(n: str, group: int = 3) -> str:
    """A long integer with thin spaces every three digits, for MathTex."""
    s = str(n)
    parts = []
    while s:
        parts.insert(0, s[-group:])
        s = s[:-group]
    return r"\,".join(parts)
