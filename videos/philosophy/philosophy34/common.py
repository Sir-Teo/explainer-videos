"""Helpers shared by the scenes of Part 34 ("Games and the Social Contract")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np  # noqa: F401

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import games as G  # noqa: F401

from .compute import load  # noqa: F401

PART = 34
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
ROW = "#6FB7FF"       # the row player
COL = "#F2A65A"       # the column player
COOP = "#5EE6D0"      # cooperation
DEFECT = "#F28EC2"    # defection
MONEY = "#F2C14E"     # payoffs, prices
INST = "#C3A6FF"      # institutions, mechanisms

STRAT_COL = {"tit for tat": "#6FB7FF", "generous tit for tat": "#5EE6D0", "win-stay lose-shift": "#C3A6FF",
             "grim": "#F2A65A", "tit for two tats": "#8FD18F", "Joss": "#F28EC2", "random": "#9AA0A6",
             "always cooperate": "#F2C14E", "always defect": "#E05A5A", "extortioner": "#B07CFF"}


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            if m.width > 1.15 * width:
                m = wrapped_label(t, width, font_size, c)
            else:
                m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)


def rows_table(rows, x_label=-6.4, x_text=-2.6, top=1.7, gap=0.45, label_size=22, text_size=21, width=8.8):
    g = VGroup()
    for a, b, c in rows:
        x = label(a, font_size=label_size, color=c)
        y = wrapped_label(b, width, text_size, WHITE)
        x.move_to([x_label + x.width / 2, top - x.height / 2, 0])
        y.move_to([x_text + y.width / 2, top - y.height / 2, 0])
        g.add(VGroup(x, y))
        top -= max(x.height, y.height) + gap
    return g


def bimatrix(A, B, acts, row_name=r"row", col_name=r"column", font_size=22, cell=1.3, center=ORIGIN):
    """A 2x2 payoff table: each cell shows (row payoff, column payoff), row player's in blue, column's in orange."""
    g = VGroup()
    cells = VGroup()
    for i in range(len(A)):
        for j in range(len(A[0])):
            box = Square(cell, color=GREY_B, stroke_width=1.5).move_to([j * cell, -i * cell, 0])
            a_, b_ = MathTex(f"{A[i][j]:g}", font_size=font_size + 4, color=ROW), \
                MathTex(f"{B[i][j]:g}", font_size=font_size + 4, color=COL)
            comma = MathTex(",", font_size=font_size + 4, color=GREY_A)
            t = VGroup(a_, comma, b_).arrange(RIGHT, buff=0.1)
            comma.align_to(a_, DOWN).shift(DOWN * 0.06)
            t.move_to(box)
            cells.add(VGroup(box, t))
    g.add(cells)
    rl = VGroup(*[label(a, font_size=font_size - 2, color=ROW).next_to(cells[i * len(A[0])], LEFT, buff=0.2)
                  for i, a in enumerate(acts)])
    cl = VGroup(*[label(a, font_size=font_size - 2, color=COL).next_to(cells[j], UP, buff=0.15)
                  for j, a in enumerate(acts)])
    g.add(rl, cl)
    g.cells, g.row_labels, g.col_labels = cells, rl, cl
    return g.move_to(center)


def mark(v, size=24):
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)
