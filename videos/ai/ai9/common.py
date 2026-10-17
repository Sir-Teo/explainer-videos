"""Helpers shared by the scenes of Part 9 ("Going Downhill")."""

from __future__ import annotations

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

OPT_COLORS = {"sgd": GREY_B, "momentum": "#7FD3FF", "adam": C.MODEL_Q, "adamw": C.BITS, "muon": C.INTERVAL}
OPT_NAMES = {"sgd": r"SGD", "momentum": r"SGD $+$ momentum", "adam": r"Adam", "adamw": r"AdamW", "muon": r"Muon"}
SCHED_COLORS = {"constant": GREY_B, "cosine": "#7FD3FF", "wsd": C.BITS}


def curve(ax, xs, ys, color, stroke_width=3) -> VMobject:
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
