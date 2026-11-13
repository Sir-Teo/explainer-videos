"""Helpers shared by the scenes of Part 2 ("Waves in Air")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403

from .compute import BOTTLE, C, CACHE, CLIPS, load  # noqa: F401

PART = 2
clip = clip_loader(CACHE, CLIPS)
DEGREES = {1: "C", 2: "D", 3: "E", 4: "F", 5: "G", 6: "A"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("air",), extra=extra, spoken=spoken)


def bottle_row(fills: dict, height: float = 2.3, gap: float = 0.5, names: bool = True) -> VGroup:
    """Six bottles, one per degree of the Tune, filled as computed.  ``row.by[degree]`` is a bottle's group;
    ``row.mouth(degree)`` the point above its neck."""
    row = VGroup()
    by = {}
    for degree in sorted(fills):
        b = bottle_shape(height=height, body_w=0.52 * height, neck_w=0.17 * height, neck_h=0.33 * height, fill=fills[degree])
        g = VGroup(b)
        if names:
            g.add(label(DEGREES[degree], font_size=28, color=GREY_B).next_to(b, DOWN, buff=0.18))
        by[degree] = g
        row.add(g)
    row.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    row.by = by
    return row


def puff(row: VGroup, degree: int, color=TUNE) -> Lens:
    """The air at a bottle's mouth, drawn as a small blur that a clip drives."""
    top = row.by[degree][0].get_top()
    return Lens(top + LEFT * 0.34 + UP * 0.22, top + RIGHT * 0.34 + UP * 0.22, amp=0.2, color=color, opacity=0.45)
