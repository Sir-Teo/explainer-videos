"""Helpers shared by the scenes of Part 12 ("Languages and Automata")."""

from __future__ import annotations

import numpy as np

from explainer import zh_text

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401

from .compute import load  # noqa: F401

PART = 12

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"

KIND_COLORS = {"keyword": FUNC, "ident": CODE, "num": HEAD, "charlit": HEAD, "string": HEAD, "operator": CTRL,
               "comment": GREY_C, "space": GREY_D}


def kind_of(kind: str) -> str:
    from explainer.cs.lang.pebble_lang import KEYWORDS
    if kind in KEYWORDS:
        return "keyword"
    if kind in ("num", "charlit", "string", "ident"):
        return kind
    return "operator"


def literal_text(text, **kwargs):
    """A literal token, grammar symbol or program output; translate its explanation separately."""
    with zh_text.verbatim():
        return Text(text, **kwargs)


def chips(tokens, font_size=16, buff=0.08, max_width=13.0):
    """A row (wrapped into lines) of token chips: (kind, text) pairs, coloured by kind."""
    rows, row, w = VGroup(), VGroup(), 0.0
    for kind, text in tokens:
        c = KIND_COLORS[kind_of(kind)]
        t = literal_text(text, font="DejaVu Sans Mono", font_size=font_size, color=c)
        r = RoundedRectangle(width=t.width + 0.18, height=0.42, corner_radius=0.06, stroke_color=c, stroke_width=1.2,
                             fill_color=c, fill_opacity=0.12)
        chip = VGroup(r, t.move_to(r))
        if w + chip.width > max_width and len(row):
            rows.add(row.arrange(RIGHT, buff=buff))
            row, w = VGroup(), 0.0
        row.add(chip)
        w += chip.width + buff
    if len(row):
        rows.add(row.arrange(RIGHT, buff=buff))
    return rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT)


def tree(t, dx=0.75, dy=0.75, font_size=20, leaf_color=CODE, node_color=GREY_A, terms=None):
    """Lay out a parse tree given as (label, [children]) with string leaves.  Returns a VGroup whose ``.nodes``
    lists (mobject, depth) in pre-order and ``.edges`` the lines."""
    g = VGroup()
    nodes, edges = [], VGroup()
    leaves = [0]

    def width(x):
        return 1 if isinstance(x, str) else max(1, sum(width(k) for k in x[1]))

    def place(x, depth, left):
        if isinstance(x, str):
            m = literal_text(x, font="DejaVu Sans Mono", font_size=font_size, color=leaf_color)
            pos = np.array([(left + 0.5) * dx, -depth * dy, 0])
            m.move_to(pos)
            nodes.append((m, depth))
            return m
        lab, kids = x
        m = literal_text(lab, font="DejaVu Sans Mono", font_size=font_size, color=node_color)
        nodes.append((m, depth))
        kms = []
        cur = left
        for k in kids:
            kms.append(place(k, depth + 1, cur))
            cur += width(k)
        if kms:
            m.move_to([np.mean([k.get_x() for k in kms]), -depth * dy, 0])
        else:
            m.move_to([(left + 0.5) * dx, -depth * dy, 0])
            e = literal_text("ε", font_size=font_size - 2, color=GREY_C).move_to([(left + 0.5) * dx, -(depth + 1) * dy, 0])
            nodes.append((e, depth + 1))
            kms.append(e)
        for k in kms:
            edges.add(Line(m.get_bottom() + DOWN * 0.05, k.get_top() + UP * 0.05, color=GREY_D, stroke_width=1.5))
        return m

    place(t, 0, 0)
    g.add(edges, *[m for m, _ in nodes])
    g.nodes, g.edges = nodes, edges
    return g


def ast_tree(node, font_size=17):
    """A Pebble-language AST (or expression) as a (label, children) tree for :func:`tree`."""
    from explainer.cs.lang import pebble_lang as P

    def conv(x):
        if isinstance(x, P.Num):
            return str(x.value)
        if isinstance(x, P.Name):
            return x.id
        if isinstance(x, P.Null):
            return "null"
        if isinstance(x, P.CharLit):
            return repr(chr(x.value))
        if isinstance(x, P.Binary):
            return (x.op, [conv(x.l), conv(x.r)])
        if isinstance(x, P.Unary):
            return (x.op, [conv(x.e)])
        if isinstance(x, P.Field):
            return (".", [conv(x.e), x.name])
        if isinstance(x, P.Index):
            return ("[ ]", [conv(x.a), conv(x.i)])
        if isinstance(x, P.Call):
            return ("call", [conv(x.f)] + [conv(a) for a in x.args])
        if isinstance(x, P.Return):
            return ("return", [conv(x.e)] if x.e else [])
        if isinstance(x, P.If):
            kids = [conv(x.cond), conv(x.then)] + ([conv(x.els)] if x.els else [])
            return ("if", kids)
        if isinstance(x, P.While):
            return ("while", [conv(x.cond), conv(x.body)])
        if isinstance(x, P.Block):
            return ("{ }", [conv(s) for s in x.stmts])
        if isinstance(x, P.Assign):
            return ("=", [conv(x.target), conv(x.value)])
        if isinstance(x, P.Var):
            return ("var " + x.name, [conv(x.init)] if x.init else [])
        if isinstance(x, P.ExprStmt):
            return conv(x.e)
        if isinstance(x, P.SizeOf):
            return f"sizeof({x.type})"
        return type(x).__name__
    return conv(node)
