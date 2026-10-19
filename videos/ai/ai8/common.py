"""Helpers shared by the scenes of Part 8 ("Fitting and Generalizing")."""

from __future__ import annotations


from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

TRAIN, TEST = GREY_B, C.BITS  # error on the examples it learned from; error on new ones
BIAS, VAR = C.TRUE_P, C.MODEL_Q
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"


def curve(ax, xs, ys, color, stroke_width=4, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)
