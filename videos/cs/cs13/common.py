"""Helpers shared by the scenes of Part 13 ("The Compiler")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401

from .compute import load  # noqa: F401

PART = 13

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"
PALETTE = [DATA, CTRL, YES, FUNC, HEAD, NO, "#9b8cd6", "#5fb7a8", "#d68c9b", "#8cb3d6", "#c9b26b", "#7fb069",
           "#b07fb0"]


def ir_block(label: str, lines: list, color=DATA, size=15, width=None):
    """A basic block: its label above, its instructions in a box."""
    body = VGroup(*[mono(l, size, CODE) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    w = max(body.width + 0.3, width or 0)
    r = RoundedRectangle(width=w, height=body.height + 0.25, corner_radius=0.08, stroke_color=color,
                         stroke_width=1.6, fill_color=color, fill_opacity=0.08)
    body.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.15)
    t = mono(label + ":", size - 1, color).next_to(r, UP, buff=0.05).align_to(r, LEFT)
    g = VGroup(r, body, t)
    g.box = r
    g.lines = body
    return g


def cfg_arrow(a, b, color=GREY_B, bend=0.0):
    """An edge between two block boxes (bottom of a to top of b, or around when going back up)."""
    ra, rb = a.box, b.box
    if rb.get_top()[1] < ra.get_bottom()[1]:
        start, end = ra.get_bottom(), rb.get_top()
    else:                               # a back edge: from the side of a up to the side of b
        start, end = ra.get_right(), rb.get_right()
        bend = bend or -1.2
    if bend:
        return CurvedArrow(start, end, angle=bend, color=color, stroke_width=2, tip_length=0.14)
    return Arrow(start, end, buff=0.05, color=color, stroke_width=2, max_tip_length_to_length_ratio=0.12)


def graph(nodes: list, edges: list, colors: dict | None = None, radius=2.6, node_r=0.28, font_size=14,
          positions: dict | None = None):
    """Nodes on a circle (or at given positions), edges as lines, optional colour index per node."""
    pos = positions or {n: radius * np.array([np.cos(2 * PI * k / len(nodes) + PI / 2),
                                              np.sin(2 * PI * k / len(nodes) + PI / 2), 0])
                        for k, n in enumerate(nodes)}
    es = VGroup(*[Line(pos[a], pos[b], color=GREY_D, stroke_width=1.5) for a, b in edges])
    ns = {}
    for n in nodes:
        c = PALETTE[colors[n] % len(PALETTE)] if colors and n in colors else GREY_C
        circ = Circle(radius=node_r, stroke_color=c, stroke_width=2, fill_color=c,
                      fill_opacity=0.35 if colors else 0.1).move_to(pos[n])
        t = Text(n.replace("%", ""), font="DejaVu Sans Mono", font_size=font_size, color=WHITE)
        if t.width > node_r * 1.8:
            t.scale_to_fit_width(node_r * 1.8)
        ns[n] = VGroup(circ, t.move_to(circ))
    g = VGroup(es, *ns.values())
    g.nodes, g.edges, g.pos = ns, es, pos
    return g


# The small function `total` (compute.DEMO): where each of its seven blocks sits on screen.
DEMO_POS = {"entry": (0, 3.05), "while1": (0, 1.75), "body2": (0, 0.35), "then5": (-1.8, -1.45),
            "else7": (1.8, -1.45), "endif6": (0, -2.95), "endwhile3": (3.3, 1.75)}
DEMO_POS_SMALL = {"entry": (0, 2.4), "while1": (0, 1.2), "body2": (0, 0.0), "then5": (-1.2, -1.2),
                  "else7": (1.2, -1.2), "endif6": (0, -2.4), "endwhile3": (1.9, 1.2)}


def cfg_edge(a, b, color=GREY_B, width=2.0, xmin=None):
    """An edge between two blocks: down (bottom to the top of the label), across (side to side), or back up (out to
    the left of everything at ``xmin``, up, and in)."""
    ra, rb = a.box, b.box
    tip = dict(tip_length=0.13)
    if rb.get_top()[1] < ra.get_bottom()[1] - 0.05:
        return Arrow(ra.get_bottom(), b.get_top(), buff=0.03, color=color, stroke_width=width, **tip)
    if rb.get_bottom()[1] <= ra.get_top()[1] + 0.05 and rb.get_top()[1] >= ra.get_bottom()[1] - 0.05:
        side = (RIGHT, LEFT) if rb.get_x() > ra.get_x() else (LEFT, RIGHT)
        return Arrow(ra.get_edge_center(side[0]), rb.get_edge_center(side[1]), buff=0.04, color=color,
                     stroke_width=width, **tip)
    x = (xmin if xmin is not None else min(ra.get_left()[0], rb.get_left()[0])) - 0.3
    p0 = ra.get_left()
    p3 = rb.get_left()
    path = VMobject(color=color, stroke_width=width).set_points_as_corners([p0, [x, p0[1], 0], [x, p3[1], 0]])
    head = Arrow([x, p3[1], 0], p3, buff=0.02, color=color, stroke_width=width, **tip)
    return VGroup(path, head)


def cfg_view(fv: dict, pos: dict, size=12, lines=True, colors: dict | None = None, at=ORIGIN, width=None,
             back_pad=0.0):
    """A function view (compute._func_view) drawn as a control-flow graph.  ``lines=False`` draws labelled boxes
    only.  Returns a VGroup with ``.blocks`` (label -> block) and ``.edges`` ((src, dst) -> arrow)."""
    blocks = {}
    for b in fv["blocks"]:
        c = (colors or {}).get(b["label"], DATA)
        if lines:
            g = ir_block(b["label"], b["ins"], c, size, width)
        else:
            t = mono(b["label"], size, WHITE)
            r = RoundedRectangle(width=max(t.width + 0.35, width or 0), height=t.height + 0.3, corner_radius=0.08,
                                 stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.15)
            t.move_to(r)
            g = VGroup(r, t)
            g.box, g.lines = r, VGroup(t)
        x, y = pos[b["label"]]
        g.move_to([x, y, 0]) if not lines else g.shift(np.array([x, y, 0]) - g.box.get_center())
        blocks[b["label"]] = g
    edges = {}
    xmin = min(g.get_left()[0] for g in blocks.values()) - back_pad
    for b in fv["blocks"]:
        for s in b["succs"]:
            edges[(b["label"], s)] = cfg_edge(blocks[b["label"]], blocks[s], xmin=xmin)
    v = VGroup(*blocks.values(), *edges.values())
    v.shift(at)
    v.blocks, v.edges = blocks, edges
    return v
