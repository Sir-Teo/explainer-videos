"""Helpers shared by the scenes of Part 13 ("Attention as Geometry")."""

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


LN_VEC = np.array([4.2, 1.0, 5.0, 0.6, 3.4, 1.8])  # one illustrative vector


def layernorm_picture(unit=0.3) -> VGroup:
    """A jargon-card picture of layer normalization: VGroup(the zero line, the band of spread one, a vector's numbers
    as bars).  ``layernorm_stage(pic, 1)`` is the same vector shifted to average zero, ``layernorm_stage(pic, 2)``
    also squashed to spread one, both rebuilt on the picture wherever it now is."""
    w = 0.5 * len(LN_VEC)
    zl = DashedLine([-0.35, 0, 0], [w - 0.15, 0, 0], color=GREY_B, stroke_width=1.5)
    band = VGroup(*[DashedLine([-0.35, s * unit, 0], [w - 0.15, s * unit, 0], color=C.TRUE_P, stroke_width=1.2,
                               dash_length=0.06) for s in (1, -1)])
    bars = VGroup(*[Rectangle(width=0.32, height=max(abs(u) * unit, 0.01), stroke_width=0, fill_color=C.EMBED,
                              fill_opacity=0.85).move_to([0.5 * i, u * unit / 2, 0]) for i, u in enumerate(LN_VEC)])
    return VGroup(zl, band, bars)


def layernorm_stage(pic: VGroup, stage: int) -> VGroup:
    zl, band, bars = pic
    y0 = zl.get_y()
    unit = band[0].get_y() - y0
    v = LN_VEC - LN_VEC.mean()
    if stage >= 2:
        v = v / LN_VEC.std()
    return VGroup(*[Rectangle(width=b.width, height=max(abs(u) * unit, 0.01), stroke_width=0, fill_color=C.TRUE_P,
                              fill_opacity=0.85).move_to([b.get_x(), y0 + u * unit / 2, 0]) for b, u in zip(bars, v)])


SM_SCORES = np.array([1.2, -0.5, 0.4, -1.0, 0.8])  # illustrative scores
SM_STAGES = (r"scores", r"$e^{\,\mathrm{score}}$: \ all positive", r"divided by the total: \ they add up to $1$")


def softmax_picture(unit=0.5) -> VGroup:
    """A jargon-card picture of the softmax: VGroup(zero line, bars, caption).  ``softmax_stage(pic, k)`` gives
    (bars, caption) for stage k: 0 the raw scores, 1 their exponentials, 2 those divided by their total."""
    zl = Line([-0.3, 0, 0], [0.45 * len(SM_SCORES) - 0.15, 0, 0], color=GREY_C, stroke_width=1.5)
    bars = _sm_bars(SM_SCORES, [0.45 * i for i in range(len(SM_SCORES))], 0.0, unit, 0.3, A)
    cap = label(SM_STAGES[0], font_size=18, color=GREY_A).next_to(zl, DOWN, buff=0.6)
    box = Rectangle(width=zl.get_length(), height=1.75 * unit, stroke_width=0, fill_opacity=0).next_to(zl, UP, buff=0)
    return VGroup(zl, bars, cap, box)  # (an invisible box keeps room for the tallest bars)


def _sm_bars(vals, xs, y0, unit, w, color):
    return VGroup(*[Rectangle(width=w, height=max(abs(float(v)) * unit, 0.01), stroke_width=0, fill_color=color,
                              fill_opacity=0.9 if v >= 0 else 0.45).move_to([x, y0 + float(v) * unit / 2, 0])
                    for x, v in zip(xs, vals)])


def softmax_stage(pic: VGroup, k: int) -> tuple[VGroup, Mobject]:
    zl, bars, cap, box = pic
    unit = box.height / 1.75
    e = np.exp(SM_SCORES)
    vals = SM_SCORES if k == 0 else 0.5 * e if k == 1 else 3.0 * e / e.sum()
    nb = _sm_bars(vals, [b.get_x() for b in bars], zl.get_y(), unit, bars[0].width, A)
    nc = label(SM_STAGES[k], font_size=18, color=GREY_A).scale(zl.get_length() / 2.4)  # as the picture was scaled
    return nb, nc.move_to(cap)
