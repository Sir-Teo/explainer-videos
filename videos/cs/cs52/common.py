"""Helpers shared by the scenes of Part 52 ("Computing with Real Numbers")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, trace  # noqa: F401
from videos.cs.cs40.common import code_block, module_box  # noqa: F401

from .compute import load  # noqa: F401

PART = 52


def tag_box(text: str, color=DATA, size=18, w=None, h=0.5):
    """A DOM node or a token drawn as a rounded box with monospace text."""
    t = mono(text, size=size, color=color)
    box = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.6, fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


def timeline_bar(x0: float, x1: float, y: float, color, h=0.32, scale=1.0, label_text=None, size=14):
    """A span of time on a horizontal timeline (x in scene units), optionally labelled inside."""
    r = Rectangle(width=max(0.02, (x1 - x0) * scale), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x0 * scale + (x1 - x0) * scale / 2, y, 0])
    if label_text:
        t = label(label_text, font_size=size, color=BLACK)
        if t.width < r.width - 0.05:
            t.move_to(r)
            return VGroup(r, t)
    return VGroup(r)
