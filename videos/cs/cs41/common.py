"""Helpers shared by the scenes of Part 41 ("Version Control, Builds and Dependencies")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, trace  # noqa: F401
from videos.cs.cs40.common import code_block, module_box  # noqa: F401

from .compute import load  # noqa: F401

PART = 41


def oid_label(oid: str, n: int = 7, size=16, color=None):
    """An object id, abbreviated as git does."""
    return mono(oid[:n], size=size, color=color or GREY_A)


def commit_dot(color=DATA, r=0.16):
    return Circle(radius=r, color=color, fill_opacity=0.9, stroke_width=0).set_fill(color)
