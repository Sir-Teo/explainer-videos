"""Helpers shared by the scenes of Part 8 ("Networks")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
CLS_A, CLS_B = "#E86F8A", "#58A6FF"  # the two spirals
HINGE = C.MODEL_Q
NEURON = "#7FD3FF"


def region_image(prob, regions, xs, width, height, boundary=True) -> ImageMobject:
    """Decision regions as a picture: tinted by the probability of class B, with the network's linear pieces drawn
    as thin dark lines where the activation pattern changes."""
    p = np.asarray(prob)
    ca, cb = np.array(ManimColor(CLS_A).to_rgb()), np.array(ManimColor(CLS_B).to_rgb())
    bg = np.array(ManimColor("#0B0F17").to_rgb())
    rgb = (1 - p)[..., None] * ca + p[..., None] * cb
    rgb = 0.55 * bg + 0.45 * rgb
    if boundary:
        r = np.asarray(regions)
        edge = np.zeros(r.shape, bool)
        edge[1:, :] |= r[1:, :] != r[:-1, :]
        edge[:, 1:] |= r[:, 1:] != r[:, :-1]
        rgb[edge] = 0.6 * rgb[edge] + 0.4 * np.array([0.92, 0.92, 0.95])
    img = ImageMobject((np.concatenate([rgb, np.ones(p.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def patch_image(regions, width, height, seed=0) -> ImageMobject:
    """Linear pieces, each its own colour."""
    r = np.asarray(regions)
    _, inv = np.unique(r, return_inverse=True)
    inv = inv.reshape(r.shape)
    hue = (inv * 0.61803 + seed * 0.1) % 1.0
    rgb = np.stack([0.32 + 0.3 * np.sin(2 * math.pi * hue), 0.38 + 0.28 * np.sin(2 * math.pi * (hue + 0.33)),
                    0.52 + 0.28 * np.sin(2 * math.pi * (hue + 0.66))], -1)
    img = ImageMobject((np.concatenate([rgb, np.ones(r.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def curve(ax, xs, ys, color, stroke_width=3) -> VMobject:
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
