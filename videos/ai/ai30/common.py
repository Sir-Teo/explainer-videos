"""Helpers shared by the scenes of Part 30 ("Inside the Model")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import heat_image, signed_image  # noqa: F401

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
RESID = C.QUERY  # the residual stream's raw numbers
FEAT = C.BITS  # a sparse autoencoder's features
NEURON = C.NEURAL
FEATURE_COLORS = [C.TRUE_P, C.BITS, C.INTERVAL, C.SURPRISE, C.NEURAL, C.MODEL_Q]


def show(ch: str) -> str:
    return {" ": "·", "\n": "⏎"}.get(ch, ch)


def context_line(ctx: str, width: float, font_size=20, color=FEAT, at: int = -2) -> VGroup:
    """A window of text, one glyph per character, with the character at ``at`` lit (where the unit fired)."""
    n = len(ctx)
    step = width / n
    i_hot = at % n
    g = VGroup()
    for i, ch in enumerate(ctx):
        hot = i == i_hot
        t = Text(show(ch), font=MONO, font_size=font_size, color=WHITE if hot else (GREY_B if i < i_hot else GREY_D))
        t.move_to([-width / 2 + step * (i + 0.5), 0, 0])
        if hot:
            g.add(Rectangle(width=step * 1.05, height=font_size / 48 * 0.75, stroke_width=0, fill_color=color,
                            fill_opacity=0.55).move_to(t))
        g.add(t)
    return g


def arrow2d(origin, vec, color, scale=1.0, stroke_width=5) -> Arrow:
    end = origin + scale * np.array([vec[0], vec[1], 0.0])
    return Arrow(origin, end, buff=0, stroke_width=stroke_width, color=color, max_tip_length_to_length_ratio=0.15,
                 max_stroke_width_to_length_ratio=12)


def vec_bars(v, width, height, color, signed=True, floor=0.004) -> VGroup:
    """A vector as a row of thin bars (up for positive, down for negative), ``width`` wide and ``height`` tall at most."""
    v = np.asarray(v, float)
    top = max(np.abs(v).max(), 1e-9)
    w = width / len(v)
    g = VGroup()
    for i, x in enumerate(v):
        h = max(abs(x) / top * height / (2 if signed else 1), floor)
        r = Rectangle(width=w * 0.8, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9 if abs(x) > 1e-9 else 0.2)
        r.move_to([-width / 2 + w * (i + 0.5), (h / 2) * (1 if x >= 0 else -1), 0])
        g.add(r)
    return g
