"""Helpers shared by the scenes of Part 27 ("Sense and Reference")."""

from __future__ import annotations

import math  # noqa: F401

import numpy as np  # noqa: F401

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import semantics as M  # noqa: F401

from .compute import load  # noqa: F401

PART = 27
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
NAME = "#6FB7FF"      # names, referring expressions
SENSE = "#C3A6FF"     # senses, intensions, lambda terms
REF = "#F2A65A"       # referents, extensions, individuals
WORLD = "#5EE6D0"     # worlds, models, contexts
SPEAK = "#F28EC2"     # speakers, believers, uses
TRUTH = "#F2C14E"     # truth values, sentences


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


def tv(v, size=24):
    """A truth value as a coloured symbol: T, F, or a gap."""
    if v is None:
        return MathTex(r"\text{---}", font_size=size, color=GREY_B)
    return MathTex(r"\text{T}" if v else r"\text{F}", font_size=size, color=OK if v else BAD)


def tree_layout(tree, x0=-6.0, x1=6.0, y_top=2.4, dy=1.0):
    """Positions for the nodes of a binary tree (leaves spread evenly, parents centred over children). Returns a
    dict path -> (x, y) and the list of leaf paths. Paths use 'L', 'R' for pairs and '1' for a lambda node's child."""
    leaves = []

    def collect(t, path):
        if isinstance(t, str):
            leaves.append(path)
        elif t[0] == "lambda":
            collect(t[2], path + "1")
        else:
            collect(t[0], path + "L")
            collect(t[1], path + "R")

    collect(tree, "")
    n = len(leaves)
    xs = {p: x0 + (x1 - x0) * (i + 0.5) / n for i, p in enumerate(leaves)}
    pos = {}

    def depth(t):
        if isinstance(t, str):
            return 0
        if t[0] == "lambda":
            return 1 + depth(t[2])
        return 1 + max(depth(t[0]), depth(t[1]))

    def place(t, path, level):
        if isinstance(t, str):
            x = xs[path]
        elif t[0] == "lambda":
            place(t[2], path + "1", level + 1)
            x = pos[path + "1"][0]
        else:
            place(t[0], path + "L", level + 1)
            place(t[1], path + "R", level + 1)
            x = (pos[path + "L"][0] + pos[path + "R"][0]) / 2
        pos[path] = (x, y_top - level * dy)

    place(tree, "", 0)
    return pos, leaves
