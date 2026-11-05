"""Helpers shared by the scenes of Part 17 ("Data Structures")."""

from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401
from videos.cs.cs16.common import big, value_bars, words  # noqa: F401

from .compute import load  # noqa: F401

PART = 17

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"
LAM = "#9b8cd6"


def slots(occupied, w=0.26, h=0.42, color=DATA, empty=GREY_D):
    """A hash table as a row of slots, filled ones coloured; ``.cells``."""
    g = VGroup(*[Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.0,
                           fill_color=color if o else BG, fill_opacity=0.9 if o else 1.0) for o in occupied])
    g.arrange(RIGHT, buff=0.02)
    g.cells = g
    return g


def tree_layout(root_key, children, x0=0.0, dx=6.4, dy=0.9):
    """Positions for a binary tree given as {key: (left, right)}: in-order x, depth y."""
    pos, order = {}, []

    def walk(k, d):
        if k is None:
            return
        l, r = children.get(k, (None, None))
        walk(l, d + 1)
        order.append((k, d))
        walk(r, d + 1)
    walk(root_key, 0)
    n = len(order)
    for i, (k, d) in enumerate(order):
        pos[k] = np.array([x0 - dx / 2 + dx * (i + 0.5) / n, -d * dy, 0.0])
    return pos


def draw_tree(root_key, children, color=DATA, r=0.24, font=18, dx=6.4, dy=0.9, highlight=()):
    """A binary tree of labelled circles; returns (group, {key: node}, edges)."""
    pos = tree_layout(root_key, children, dx=dx, dy=dy)
    nodes, edges = {}, VGroup()
    for k, p in pos.items():
        c = Circle(radius=r, stroke_color=HEAD if k in highlight else color, stroke_width=2,
                   fill_color=BG, fill_opacity=1).move_to(p)
        t = mono(str(k), font, WHITE).move_to(p)
        nodes[k] = VGroup(c, t)
    for k, (l, rr) in children.items():
        for ch in (l, rr):
            if ch is not None and ch in pos and k in pos:
                edges.add(Line(pos[k], pos[ch], buff=r, color=GREY_B, stroke_width=1.6))
    g = VGroup(edges, *nodes.values())
    return g, nodes, edges


def bst_children(keys):
    """Insert keys into a plain BST; return (root, {key: (left, right)})."""
    root, ch = None, {}
    for k in keys:
        if root is None:
            root = k
            ch[k] = (None, None)
            continue
        n = root
        while True:
            l, r = ch[n]
            if k < n:
                if l is None:
                    ch[n] = (k, r)
                    break
                n = l
            else:
                if r is None:
                    ch[n] = (l, k)
                    break
                n = r
        ch[k] = (None, None)
    return root, ch
