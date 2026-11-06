"""Helpers shared by the scenes of Part 40 ("Software Engineering")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, box, trace  # noqa: F401

from .compute import load  # noqa: F401

PART = 40


def module_box(name, color, w=2.3, h=0.6, font=18):
    """A module drawn as a rounded box with its name."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=color, fill_opacity=0.12)
    t = label(name, font_size=font, color=WHITE).move_to(r)
    if t.width > w - 0.15:
        t.scale_to_fit_width(w - 0.15)
    return VGroup(r, t)


def code_block(lines, size=17, color=None, buff=0.08):
    """Lines of code, left-aligned, in the series' monospace face."""
    g = VGroup(*[mono(s, size=size, color=color) if color else mono(s, size=size) for s in lines])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return g
