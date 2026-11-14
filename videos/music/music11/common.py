"""Helpers shared by the scenes of Part 11 ("Rhythm and Meter")."""

from __future__ import annotations

import numpy as np

from explainer.music.kit import *  # noqa: F403
from explainer.music.rhythmviz import DIM, GOLD, dot_grid, flash, necklace, pattern_row, sticks, ticks  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 11
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
LOW = "#7DD3FC"       # the lower drum, the slower layer
HIGH = "#F5C542"      # the higher one


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def bracket(a, b, y: float, color=WEAK, drop: float = 0.14) -> VGroup:
    """A bracket under a group of marks, from x = a to x = b."""
    return VGroup(Line([a, y, 0], [b, y, 0], color=color, stroke_width=2.5), Line([a, y, 0], [a, y + drop, 0], color=color, stroke_width=2.5),
                  Line([b, y, 0], [b, y + drop, 0], color=color, stroke_width=2.5))


def group_brackets(xs, groups, y: float, pitch: float, color=WEAK) -> VGroup:
    """Brackets under consecutive groups of pulses: ``groups`` are sizes, ``xs`` the pulses' x, ``pitch`` their spacing."""
    out, i = VGroup(), 0
    for g in groups:
        out.add(bracket(xs[i] - 0.38 * pitch, xs[i + g - 1] + 0.38 * pitch, y, color))
        i += g
    return out
