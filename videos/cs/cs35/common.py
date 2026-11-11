"""Helpers shared by the scenes of Part 35 ("Databases")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401
from videos.cs.cs31.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES, edge_arrow,  # noqa: F401
                                   kv_rows)
from videos.cs.cs34.common import blk, num  # noqa: F401

from .compute import load  # noqa: F401

PART = 35
T1C, T2C, T3C = DATA, HEAD, LAM          # transaction colours
OPC = {"Scan": DATA, "IndexScan": YES, "Join": HEAD, "Aggregate": LAM, "Sort": KERN, "Project": GREY_B,
       "Filter": COST}


def rel_table(cols, rows, font=18, w=None, color=DATA, max_rows=None):
    """A relation drawn as a small table: a header row and the tuples."""
    rows = rows[:max_rows] if max_rows else rows
    widths = w or [max(1.3, 0.22 * max(len(str(c)), *(len(str(r[i])) for r in rows))) for i, c in enumerate(cols)]
    t = grid_table([rf"\textbf{{{c}}}" for c in cols], [[str(v) for v in r] for r in rows], widths=widths,
                   row_h=0.38, font_size=font, mono_cols=())
    for c in t.cells[0]:
        c.set_color(color)
    return t


TCOL = {1: T1C, 2: T2C, 3: T3C, 4: KERN}


def schedule_view(schedule, step=0.85, row=0.75, font=19):
    """A schedule drawn as a timeline: one row per transaction, one chip per operation, in order left to right.
    ``schedule`` holds (txn, action, item) with action r, w, c (commit) or a (abort).  Returns a VGroup with
    ``.chips`` (in schedule order) and ``.names``."""
    txns = sorted({t for t, _, _ in schedule})
    g = VGroup()
    g.names = VGroup(*[label(rf"$T_{t}$", font_size=font + 3, color=TCOL[t]).move_to([-0.8, -k * row, 0])
                       for k, t in enumerate(txns)])
    g.chips = VGroup()
    for i, (t, a, x) in enumerate(schedule):
        txt = {"r": rf"r({x})", "w": rf"w({x})", "c": "commit", "a": "abort"}[a]
        col = TCOL[t] if a in "rw" else (YES if a == "c" else NO)
        m = Text(txt, font="DejaVu Sans Mono", font_size=font - 4, color=col)
        if m.width > step - 0.08:
            m.width = step - 0.08
        m.move_to([i * step, -txns.index(t) * row, 0])
        g.chips.add(m)
    g.axis = Arrow([-0.4, -len(txns) * row + 0.25, 0], [len(schedule) * step, -len(txns) * row + 0.25, 0], buff=0,
                   color=GREY_D, stroke_width=1.5, max_tip_length_to_length_ratio=0.03)
    g.add(g.names, g.chips, g.axis)
    return g


def precedence_view(edges, txns, r=1.0, font=22):
    """Transactions as nodes on a circle, an arrow T_i -> T_j for each conflict edge."""
    import math
    g = VGroup()
    pos = {}
    for k, t in enumerate(txns):
        ang = math.pi / 2 + 2 * math.pi * k / len(txns) if len(txns) > 2 else math.pi * (1 - k)
        pos[t] = np.array([r * math.cos(ang), r * math.sin(ang), 0])
    nodes = VGroup()
    for t in txns:
        c = Circle(radius=0.32, stroke_color=TCOL[t], stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to(pos[t])
        nodes.add(VGroup(c, label(rf"$T_{t}$", font_size=font, color=TCOL[t]).move_to(c)))
    arrows = VGroup()
    es = {tuple(e) for e in edges}
    for a, b in es:
        start, end = pos[a], pos[b]
        if (b, a) in es:                                  # both ways: two arcs, one on each side
            d = (end - start) / np.linalg.norm(end - start)
            ar = CurvedArrow(start + d * 0.36, end - d * 0.36, angle=-0.6, color=NO, stroke_width=2.2)
        else:
            ar = Arrow(start, end, buff=0.36, color=GREY_A, stroke_width=2.2)
        arrows.add(ar)
    g.add(arrows, nodes)
    g.nodes, g.arrows = nodes, arrows
    return g
