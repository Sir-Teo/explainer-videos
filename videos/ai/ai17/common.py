"""Helpers shared by the scenes of Part 17 ("Reasoning")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
DIRECT, CHAIN = C.SURPRISE, C.INTERVAL  # answering at once; writing a chain of thought first
RIGHT_C, WRONG_C = C.INTERVAL, C.SURPRISE


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def chip(text: str, size=0.46, color=GREY_B, font_size=28, fill=0.12, width=None) -> VGroup:
    """A rounded box with a short monospace text in it."""
    box = RoundedRectangle(width=width or size, height=size, corner_radius=0.08, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=fill)
    t = Text(text, font=MONO, font_size=font_size, color=WHITE).move_to(box)
    return VGroup(box, t)


def bit_row(bits, size=0.46, buff=0.08, color=GREY_B, font_size=28) -> VGroup:
    return VGroup(*[chip(str(int(b)), size, color, font_size) for b in bits]).arrange(RIGHT, buff=buff)


def mark(ok: bool, font_size=30) -> MathTex:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=RIGHT_C if ok else WRONG_C)


def hit_image(R, width, height) -> ImageMobject:
    """A boolean matrix as a picture: green where right, dark red where wrong."""
    R = np.asarray(R, bool)
    g, r = np.array(ManimColor(RIGHT_C).to_rgb()), np.array(ManimColor(WRONG_C).to_rgb()) * 0.45
    rgb = np.where(R[..., None], g, r)
    img = ImageMobject((np.concatenate([rgb, np.ones(R.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)
