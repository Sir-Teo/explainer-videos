"""Drawing the windy lane of chapters 9 and 10: the road seen from above, drives as lines rising through time, and a
learner's table of actions as a strip of arrows."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, EXPERT, FAIL

ROAD = "#3A4250"
GRASS = "#1E3A2A"


class LaneView(VGroup):
    """Offsets -D..D across, time upward.  ``cell`` units per offset, ``height`` for ``T`` steps."""

    def __init__(self, D, T, cell=0.3, height=5.0, center=ORIGIN):
        super().__init__()
        self.D, self.T, self.cell, self.h = D, T, cell, height
        W = (2 * D + 1) * cell
        self.W = W
        grass = Rectangle(width=W, height=height, stroke_width=0, fill_color=GRASS, fill_opacity=1)
        road = Rectangle(width=3 * cell, height=height, stroke_width=0, fill_color=ROAD, fill_opacity=1)
        edges = VGroup(*[DashedLine(road.get_corner(c1), road.get_corner(c2), color=GREY_B, stroke_width=1.5,
                                    dash_length=0.12) for c1, c2 in ((UL, DL), (UR, DR))])
        verge = VGroup(*[Line(grass.get_corner(c1), grass.get_corner(c2), color=GREY_C, stroke_width=3)
                         for c1, c2 in ((UL, DL), (UR, DR))])
        self.add(grass, road, edges, verge)
        self.move_to(center)
        self.base = grass

    def p(self, d, t):
        x0 = self.base.get_left()[0] + self.cell / 2
        y0 = self.base.get_bottom()[1]
        return np.array([x0 + (d + self.D) * self.cell, y0 + self.h * t / self.T, 0.0])

    def drive(self, ds, color, width=2.5, opacity=0.85):
        pts = [self.p(d, t) for t, d in enumerate(ds)]
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(pts)
        return m

    def wind(self, n=4):
        g = VGroup()
        for k in range(n):
            y = self.base.get_bottom()[1] + self.h * (k + 0.5) / n
            g.add(Arrow([self.base.get_left()[0] - 0.9, y, 0], [self.base.get_left()[0] - 0.15, y, 0], buff=0,
                        color=GREY_B, stroke_width=2.5, max_tip_length_to_length_ratio=0.3))
        return g


def table_strip(view: LaneView, tab, seen=None, y=None, color=AGENT, size=0.24) -> VGroup:
    """The learner's action for each camera reading, under the lane: an arrow left / a dot / an arrow right; readings
    it was never shown are drawn grey (their action is arbitrary)."""
    g = VGroup()
    y = view.base.get_bottom()[1] - 0.35 if y is None else y
    for k, a in enumerate(tab):
        d = k - view.D
        x = view.p(d, 0)[0]
        known = seen is None or bool(seen[k])
        col = color if known else GREY_D
        if a == 0:
            m = Dot([x, y, 0], radius=0.05, color=col)
        else:
            m = Arrow([x - a * size / 2, y, 0], [x + a * size / 2, y, 0], buff=0, stroke_width=3, color=col,
                      max_tip_length_to_length_ratio=0.5)
        g.add(m)
    return g
