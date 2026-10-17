"""Helpers shared by the scenes of Part 11 ("Attention as Geometry")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
Q, K, V, A = C.QUERY, C.KEY, C.VALUE, C.ATTN
POS = C.POSITION
OURS = C.NEURAL  # our transformer on the scoreboard


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def heat_image(M, width, height, color=A, gamma=0.5, mask_upper=False) -> ImageMobject:
    """A matrix as a picture: dark for 0, ``color`` for the largest entry; ``gamma`` < 1 lifts the small ones.
    With ``mask_upper``, entries above the diagonal (the future, for causal attention) are drawn darker still."""
    M = np.asarray(M, float)
    v = np.clip(M / max(M.max(), 1e-12), 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    if mask_upper:
        up = np.triu(np.ones(M.shape, bool), 1)
        rgb[up] = np.array(ManimColor("#080B11").to_rgb())
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def signed_image(M, width, height, pos=C.TRUE_P, neg=C.SURPRISE) -> ImageMobject:
    """A signed matrix as a picture: blue for positive, red for negative, dark for zero."""
    M = np.asarray(M, float)
    s = np.clip(M / max(np.abs(M).max(), 1e-12), -1, 1)
    bg = np.array(ManimColor("#121722").to_rgb())
    cp, cn = np.array(ManimColor(pos).to_rgb()), np.array(ManimColor(neg).to_rgb())
    a = np.abs(s)[..., None]
    rgb = bg * (1 - a) + np.where(s[..., None] > 0, cp, cn) * a
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def char_row(text: str, width: float, font_size=26, color=GREY_A) -> VGroup:
    """One glyph per character, evenly spaced across ``width`` (spaces shown as a dim dot)."""
    step = width / len(text)
    g = VGroup()
    for i, ch in enumerate(text):
        if ch == " ":
            m = Dot(radius=0.025, color=GREY_D)
        else:
            m = Text(ch, font=MONO, font_size=font_size, color=color)
        g.add(m.move_to([-width / 2 + step * (i + 0.5), 0, 0]))
    return g


def attention_arcs(row: VGroup, i: int, weights, color=A, max_width=12, floor=0.02, up=True) -> VGroup:
    """Arcs from character ``i`` back to each earlier character, as thick as the attention weight."""
    w = np.asarray(weights, float)
    arcs = VGroup()
    top = max(w[: i + 1].max(), 1e-9)
    for j in range(i):
        if w[j] < floor * top:
            continue
        a, b = row[i].get_top() if up else row[i].get_bottom(), row[j].get_top() if up else row[j].get_bottom()
        a, b = a + (UP if up else DOWN) * 0.08, b + (UP if up else DOWN) * 0.08
        ang = -PI / 2.2 if up else PI / 2.2
        arcs.add(ArcBetweenPoints(a, b, angle=ang, stroke_width=1 + max_width * w[j] / top, color=color)
                 .set_stroke(opacity=float(0.25 + 0.75 * w[j] / top)))
    return arcs
