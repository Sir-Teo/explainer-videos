"""Helpers shared by the scenes of Part 5 ("Beyond True and False": non-classical logics and vagueness)."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import prop

from .compute import load  # noqa: F401

PART = 5
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
HALF = "#F6C177"      # the middle value, 1/2
BOTH = "#C3A6FF"      # FDE's B: told true and told false
NEITHER = "#8A93A6"   # FDE's N: told nothing
EMPTY = "#4A5263"     # Priest's fifth value
DES = "#FFD166"       # designated values are ringed in this colour

VAL_COLOR = {"0": BAD, "1/2": HALF, "1": OK, "t": OK, "f": BAD, "b": BOTH, "n": NEITHER, "e": EMPTY}
VAL_TEX = {"0": "0", "1/2": r"\tfrac12", "1": "1", "t": r"\mathbf{T}", "f": r"\mathbf{F}", "b": r"\mathbf{B}",
           "n": r"\mathbf{N}", "e": r"\mathbf{E}"}
OP_TEX = {"not": r"\lnot", "and": r"\land", "or": r"\lor", "imp": r"\to"}


def vtex(v: str) -> str:
    """A value (as the cache stores it: '0', '1/2', '1', 't', 'b', ...) as TeX."""
    if v in VAL_TEX:
        return VAL_TEX[v]
    if "/" in v:
        a, b = v.split("/")
        return rf"\tfrac{{{a}}}{{{b}}}"
    return v


def vmob(v: str, font_size=30) -> MathTex:
    return MathTex(vtex(v), font_size=font_size, color=VAL_COLOR.get(v, WHITE))


def mxf(s: str, font_size=36, color=WHITE) -> MathTex:
    """A propositional formula (the Reasoner's syntax) as TeX."""
    return MathTex(prop.show(prop.parse(s), tex=True), font_size=font_size, color=color)


def mx_tex(s: str) -> str:
    return prop.show(prop.parse(s), tex=True)


def arg_tex(premises, conclusion) -> str:
    """``p, ¬p ⊨ q`` as TeX."""
    ps = r",\ ".join(mx_tex(p) for p in premises)
    return (ps + r" \ \models\ " if ps else r"\models\ ") + mx_tex(conclusion)


def cm_tex(cm: dict) -> str:
    """A countermodel {'p': '1/2', 'q': '0'} as TeX: p = 1/2, q = 0."""
    return r",\ ".join(rf"{k} = {vtex(v)}" for k, v in sorted(cm.items()))


class ConnTable(VGroup):
    """A connective's table as a grid of coloured cells: ``values`` label the rows (first argument) and columns
    (second); ``grid[r][c]`` is the value. For ¬, pass ``grid`` as a single row. ``self.cell[r][c]`` is a square with
    its value; ``self.designated`` rings the designated values in the header."""

    def __init__(self, op: str, values, grid, designated=(), size=0.62, font_size=26, title: str | None = None):
        super().__init__()
        n = len(values)
        unary = op == "not"
        self.cell = []
        body = VGroup()
        rows = [grid] if unary else grid
        for r, row in enumerate(rows):
            cells = []
            for c, v in enumerate(row):
                sq = Square(side_length=size, stroke_width=1.2, stroke_color=GREY_D, fill_color=VAL_COLOR.get(v, GREY_C),
                            fill_opacity=0.28)
                sq.move_to([c * size, -r * size, 0])
                t = MathTex(vtex(v), font_size=font_size, color=VAL_COLOR.get(v, WHITE)).move_to(sq)
                g = VGroup(sq, t)
                cells.append(g)
                body.add(g)
            self.cell.append(cells)
        self.body = body
        heads = VGroup()
        self.designated = VGroup()
        for c, v in enumerate(values):
            h = MathTex(vtex(v), font_size=font_size - 2, color=VAL_COLOR.get(v, WHITE))
            h.move_to([c * size, size * 0.85, 0])
            heads.add(h)
            if v in designated:
                self.designated.add(Circle(radius=size * 0.32, color=DES, stroke_width=2).move_to(h))
        side = VGroup()
        if not unary:
            for r, v in enumerate(values):
                h = MathTex(vtex(v), font_size=font_size - 2, color=VAL_COLOR.get(v, WHITE))
                h.move_to([-size * 0.9, -r * size, 0])
                side.add(h)
                if v in designated:
                    self.designated.add(Circle(radius=size * 0.32, color=DES, stroke_width=2).move_to(h))
        corner = MathTex(OP_TEX[op], font_size=font_size + 4, color=CONN).move_to([-size * 0.9, size * 0.85, 0])
        self.heads, self.side, self.corner = heads, side, corner
        self.add(body, heads, side, corner, self.designated)
        if title:
            self.title = label(title, font_size=font_size - 2, color=GREY_A).next_to(self, UP, buff=0.25)
            self.add(self.title)
        self.move_to(ORIGIN)


def head_icon(hair: float, status: str | None = None, r=0.2) -> VGroup:
    """A small head with hair in proportion to ``hair`` in [0, 1]; ``status`` ('T' bald, 'F' not, 'I' borderline)
    tints the face."""
    col = {"T": OK, "F": BAD, "I": HALF, None: GREY_B}[status]
    face = Circle(radius=r, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.18)
    strands = VGroup()
    k = int(round(9 * hair))
    for j in range(k):
        a = PI * (0.18 + 0.64 * (j + 0.5) / 9)
        p = face.get_center() + r * np.array([np.cos(a), np.sin(a), 0])
        strands.add(Line(p, p + 0.11 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_A, stroke_width=1.6))
    g = VGroup(face, strands)
    g.face, g.strands = face, strands
    return g


def men_row(statuses, width=12.6, r=0.17, y=0.0) -> VGroup:
    """A row of heads, hair growing left to right, faces tinted by status ('T', 'F', 'I' or None)."""
    n = len(statuses)
    g = VGroup()
    for i, s in enumerate(statuses):
        h = head_icon(i / max(n - 1, 1), s, r=r)
        h.move_to([-width / 2 + width * i / max(n - 1, 1), y, 0])
        g.add(h)
    return g


def status_strip(statuses, width=12.0, height=0.36, y=0.0) -> VGroup:
    """A strip of cells coloured by status: T green, F red, I amber."""
    n = len(statuses)
    w = width / n
    g = VGroup()
    for i, s in enumerate(statuses):
        col = {"T": OK, "F": BAD, "I": HALF}[s]
        g.add(Rectangle(width=w * 0.92, height=height, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
            [-width / 2 + w * (i + 0.5), y, 0]))
    return g
