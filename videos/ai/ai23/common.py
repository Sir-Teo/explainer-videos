"""Helpers shared by the scenes of Part 23 ("Every Sense Is a Token")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
TEXT_C, IMG_C, SND_C = C.TRUE_P, C.BITS, C.INTERVAL
TOKEN_COLORS = ["#58A6FF", "#F7D154", "#FF6B8B", "#5BD17A", "#D4A5FF", "#FF9F45", "#7FD3FF", "#E86F8A"]


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def heat(M, width, height, color=SND_C, signed=False, lo=None, hi=None) -> ImageMobject:
    """A matrix as a picture; ``lo``/``hi`` fix the brightness scale (default: this matrix's own range)."""
    M = np.asarray(M, float)
    bg = np.array(ManimColor("#121722").to_rgb())
    if signed:
        s = np.clip(M / max(np.abs(M).max(), 1e-9), -1, 1)
        a = np.abs(s)[..., None]
        rgb = bg * (1 - a) + np.where(s[..., None] > 0, np.array(ManimColor(C.TRUE_P).to_rgb()),
                                      np.array(ManimColor(C.SURPRISE).to_rgb())) * a
    else:
        lo_, hi_ = (M.min() if lo is None else lo), (M.max() if hi is None else hi)
        v = np.clip((M - lo_) / max(hi_ - lo_, 1e-9), 0, 1)[..., None]
        rgb = bg * (1 - v) + np.array(ManimColor(color).to_rgb()) * v
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def token_chips(pieces, font_size=26, height=0.5, buff=0.06) -> VGroup:
    """Text pieces as coloured chips, side by side (a leading space shown as a dim dot)."""
    g = VGroup()
    for i, p in enumerate(pieces):
        t = Text(p.replace(" ", "·"), font=MONO, font_size=font_size, color=WHITE)
        box = RoundedRectangle(width=t.width + 0.16, height=height, corner_radius=0.08, stroke_width=0,
                               fill_color=TOKEN_COLORS[i % len(TOKEN_COLORS)], fill_opacity=0.35)
        g.add(VGroup(box, t.move_to(box)))
    return g.arrange(RIGHT, buff=buff)
