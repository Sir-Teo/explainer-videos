"""Helpers shared by the scenes of Part 31 ("The Kernel")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code, region  # noqa: F401
from videos.cs.cs16.common import big, value_bars, words  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401

from .compute import load  # noqa: F401

PART = 31

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
KERN = "#d98c5f"        # the kernel, wherever it appears

JOBC = {"A": DATA, "B": HEAD, "C": YES, "D": LAM, "kernel": KERN, "switch": GREY_D, "tok": DATA, "job": HEAD,
        "H1": NO, "H2": LAM, "I": YES, "a": DATA, "b": HEAD, "c": YES, "hog": NO, "gamer": HEAD,
        "meteo": DATA, "bus": YES, "comms": NO, "good": YES, "halter": NO, "scribbler": COST}


def gantt(segments, t0, t1, width=11.0, h=0.5, colors=None, lanes=None, font=18, gap=0.12, names=True,
          min_w=0.0, label_inside=True):
    """A Gantt chart.  ``segments`` are (start, end, name).  With ``lanes`` (a list of names) each name gets its own
    row, labelled on the left; otherwise one row, names written inside the wider bars.  ``.bars`` holds the bars in
    time order, ``.lane_labels`` the row labels, ``.x(t)`` maps a time to an x coordinate."""
    colors = {**JOBC, **(colors or {})}
    span = t1 - t0
    sx = width / span
    g = VGroup()
    bars = VGroup()
    rows = {n: i for i, n in enumerate(lanes)} if lanes else None
    x0 = -width / 2
    anchor = Dot([x0, 0, 0], radius=0.001).set_opacity(0)

    def x0_(t):
        return x0 + (t - t0) * sx
    x = x0_
    for a, b, n in segments:
        if b <= t0 or a >= t1:
            continue
        a, b = max(a, t0), min(b, t1)
        w = max((b - a) * sx, min_w)
        y = 0 if rows is None else -rows.get(n, 0) * (h + gap)
        c = colors.get(n, GREY_B)
        r = Rectangle(width=w, height=h, stroke_width=0.6, stroke_color=BG, fill_color=c, fill_opacity=0.85)
        r.move_to([x(a) + w / 2, y, 0])
        bar = VGroup(r)
        if names and label_inside and rows is None and w > 0.32 and n != "switch":
            bar.add(label(n, font_size=font, color=BG).move_to(r))
        bars.add(bar)
    g.add(bars)
    g.bars = bars
    g.lane_labels = VGroup()
    if lanes:
        for n, i in rows.items():
            t = label(n, font_size=font, color=colors.get(n, WHITE)).move_to([x0 - 0.2, -i * (h + gap), 0],
                                                                             aligned_edge=RIGHT)
            g.lane_labels.add(t)
        g.add(g.lane_labels)
    g.add(anchor)

    def xnow(t):
        return anchor.get_center()[0] + (t - t0) * sx * (g.bars.width / max(g._w0, 1e-9) if g._w0 else 1.0)
    g._w0 = bars.width
    g.x = xnow
    g.t0, g.t1 = t0, t1
    return g


def time_axis(g, ticks, y=None, font=15, unit=""):
    """Tick labels under a Gantt chart ``g`` at the given times."""
    yb = (g.bars.get_bottom()[1] if y is None else y) - 0.12
    out = VGroup()
    for t in ticks:
        out.add(Line([g.x(t), yb + 0.06, 0], [g.x(t), yb - 0.02, 0], color=GREY_C, stroke_width=1))
        out.add(label(f"{t}{unit}", font_size=font, color=GREY_B).move_to([g.x(t), yb - 0.2, 0]))
    return out


def state_node(text, color, pos, w=1.7, h=0.62, font=22):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1).move_to(pos)
    return VGroup(r, label(text, font_size=font, color=color).move_to(r))


def edge_arrow(a, b, text=None, color=GREY_B, font=17, bend=0.0, side=UP, buff=0.08):
    """An arrow from mobject a to mobject b (edge to edge), optionally curved, with a small label."""
    pa, pb = a.get_center(), b.get_center()
    d = pb - pa
    d = d / (np.linalg.norm(d) + 1e-9)
    s = a.get_boundary_point(d) if hasattr(a, "get_boundary_point") else pa
    e = b.get_boundary_point(-d) if hasattr(b, "get_boundary_point") else pb
    if bend:
        arr = CurvedArrow(s, e, angle=bend, color=color, stroke_width=2.2, tip_length=0.16)
    else:
        arr = Arrow(s, e, buff=buff, color=color, stroke_width=2.2, max_tip_length_to_length_ratio=0.12)
    g = VGroup(arr)
    if text:
        mid = arr.point_from_proportion(0.5)
        g.add(label(text, font_size=font, color=color).next_to(mid, side, buff=0.08))
    return g


def kv_rows(pairs, font=21, key_color=GREY_B, val_color=WHITE, buff=0.16, key_w=None):
    """Two aligned columns: key, value."""
    rows = VGroup()
    for k, v in pairs:
        rows.add(VGroup(label(k, font_size=font, color=key_color), label(v, font_size=font, color=val_color)))
    kw = key_w or max(r[0].width for r in rows) + 0.4
    for r in rows:
        r[1].next_to(r[0], RIGHT, buff=0.3)
        r[1].shift(RIGHT * (kw - r[0].width - 0.3))
    rows.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return rows
