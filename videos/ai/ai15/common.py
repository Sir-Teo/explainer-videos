"""Helpers shared by the scenes of Part 15 ("Images and Video")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
PATCH = C.BITS
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def heat_image(M, size, color=C.ATTN, gamma=0.7) -> ImageMobject:
    M = np.asarray(M, float)
    v = np.clip((M - M.min()) / max(M.max() - M.min(), 1e-12), 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def patch_grid(img_mob, n, color=PATCH, stroke_width=1.5) -> VGroup:
    """Lines cutting a square picture into n x n patches."""
    w = img_mob.width
    ul = img_mob.get_corner(UL)
    g = VGroup()
    for k in range(1, n):
        g.add(Line(ul + RIGHT * w * k / n, ul + RIGHT * w * k / n + DOWN * w, color=color, stroke_width=stroke_width))
        g.add(Line(ul + DOWN * w * k / n, ul + DOWN * w * k / n + RIGHT * w, color=color, stroke_width=stroke_width))
    return g
