"""Helpers shared by the scenes of Part 39 ("Distributed Systems II: Scale")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, box, seq_diagram, trace  # noqa: F401

from .compute import load  # noqa: F401

PART = 39
KINDC = {"map": DATA, "reduce": LAM}


def gantt(run, x0=-5.6, width=11.4, y0=2.0, lane=0.26, t_max=None, font=13):
    """Every task attempt of a MapReduce run as a bar in its worker's lane; lost attempts red, duplicates grey."""
    tl = run["timeline"]
    t_max = t_max or max(a["end"] for a in tl)
    g = VGroup()
    g.bars = VGroup()
    g.names = VGroup()
    for w in range(run["workers"]):
        y = y0 - w * lane
        g.names.add(label(f"{w + 1}", font_size=font, color=GREY_B).move_to([x0 - 0.25, y, 0]))
    for a in tl:
        s = a["start"] if a["start"] is not None else a["end"]
        x1 = x0 + s / t_max * width
        x2 = x0 + a["end"] / t_max * width
        c = KINDC[a["kind"]]
        if a["outcome"] == "lost":
            c = NO
        elif a["outcome"] == "duplicate":
            c = GREY_C
        r = Rectangle(width=max(0.02, x2 - x1 - 0.01), height=lane * 0.78, stroke_width=0, fill_color=c,
                      fill_opacity=0.85)
        r.move_to([(x1 + x2) / 2, y0 - a["worker"] * lane, 0])
        g.bars.add(r)
    g.add(g.names, g.bars)
    g.t_max = t_max
    g.x0, g.width, g.y0, g.lane = x0, width, y0, lane
    return g
