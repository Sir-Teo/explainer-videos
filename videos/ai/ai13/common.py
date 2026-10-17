"""Helpers shared by the scenes of Part 13 ("Sparsity")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
ROUTER = C.ATTN
EXPERT_COLORS = ["#58A6FF", "#F7D154", "#FF6B8B", "#5BD17A", "#D4A5FF", "#FF9F45", "#7FD3FF", "#E86F8A"]
MODES = [("none", r"no balancing", C.SURPRISE), ("aux", r"auxiliary loss", C.TRUE_P), ("bias", r"loss-free bias", C.INTERVAL)]


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def billions(v: float) -> str:
    return (f"{v / 1e12:.2f}".rstrip("0").rstrip(".") + r"\,\mathrm{T}") if v >= 1e12 else (f"{v / 1e9:,.1f}".rstrip("0").rstrip(".") + r"\,\mathrm{B}")


def load_image(L, width, height) -> ImageMobject:
    """Expert loads over training as a picture: rows = experts, columns = time; bright = busy (1 = a fair share)."""
    L = np.asarray(L, float).T  # expert, time
    E = L.shape[0]
    v = np.clip(L * E / 3.0, 0, 1) ** 0.7  # 3x a fair share or more: full brightness
    hot = np.array(ManimColor(C.BITS).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + hot[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(v.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)
