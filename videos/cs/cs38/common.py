"""Helpers shared by the scenes of Part 38 ("Distributed Systems I: Agreement")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs31.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, box, seq_diagram, trace  # noqa: F401

from .compute import load  # noqa: F401

PART = 38
ROLEC = {"leader": YES, "candidate": HEAD, "follower": DATA, "down": GREY_D}
PROCC = [DATA, LAM, KERN, YES, HEAD]


def space_time(n, events, x0=-5.6, x1=5.6, y0=1.8, dy=1.3, names=None, font=18, stamps=None, stamp_color=WHITE):
    """Processes as horizontal lines (P0 on top), events as dots at increasing x, messages as arrows.
    events: [(proc, kind, peer, mid)] in order; x positions are evenly spaced by event index.
    stamps: optional list of strings to label each event.  Returns a VGroup with .dots, .arrows, .labels,
    .lines and .pos (event index -> point)."""
    g = VGroup()
    g.lines = VGroup()
    names = names or [f"$P_{i}$" for i in range(n)]
    for i in range(n):
        y = y0 - i * dy
        ln = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)
        nm = label(names[i], font_size=font + 2, color=PROCC[i % len(PROCC)]).next_to(ln, LEFT, buff=0.15)
        g.lines.add(VGroup(ln, nm))
    g.add(g.lines)
    m = len(events)
    step = (x1 - x0 - 0.6) / max(1, m - 1)
    g.pos = {}
    g.dots = VGroup()
    send_pos = {}
    g.arrows = VGroup()
    for k, (p, kind, peer, mid) in enumerate(events):
        pt = np.array([x0 + 0.3 + k * step, y0 - p * dy, 0])
        g.pos[k] = pt
        c = PROCC[p % len(PROCC)]
        d = Dot(pt, radius=0.08, color=c)
        g.dots.add(d)
        if kind == "send":
            send_pos[mid] = pt
        elif kind == "recv" and mid in send_pos:
            a = Arrow(send_pos[mid], pt, buff=0.08, color=GREY_B, stroke_width=2,
                      max_tip_length_to_length_ratio=0.08, tip_length=0.15)
            g.arrows.add(a)
    g.add(g.arrows, g.dots)
    g.labels = VGroup()
    if stamps:
        for k, s in enumerate(stamps):
            p = events[k][0]
            t = label(s, font_size=font - 2, color=stamp_color)
            t.next_to(g.pos[k], UP if p == 0 or k % 2 == 0 else DOWN, buff=0.1)
            g.labels.add(t)
        g.add(g.labels)
    return g


def role_strip(timeline, node, t_max, width=11.0, h=0.32, x0=-5.0, y=0.0):
    """One node's role over time from a sampled timeline [(t, [[role, term, log, commit], ...])] as coloured
    segments."""
    g = VGroup()
    prev = None
    start = 0.0
    for t, nodes in timeline + [[t_max + 1e-9, [[None, 0, 0, 0]] * len(timeline[0][1])]]:
        role = nodes[node][0]
        if role != prev:
            if prev is not None:
                a = x0 + start / t_max * width
                b = x0 + min(t, t_max) / t_max * width
                r = Rectangle(width=max(0.01, b - a), height=h, stroke_width=0, fill_color=ROLEC[prev],
                              fill_opacity=0.85 if prev != "follower" else 0.45)
                r.move_to([(a + b) / 2, y, 0])
                g.add(r)
            prev, start = role, t
    return g
