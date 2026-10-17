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


SIG_SCORES = np.array([0.6, 0.1, -0.4, 0.3])  # illustrative router scores for four experts


def gate_picture() -> VGroup:
    """A jargon-card picture of softmax against sigmoid gates: VGroup(softmax panel, sigmoid panel), each
    VGroup(bars, base, name).  ``gate_bars(pic, boost)`` rebuilds both panels' bars with expert 1's score raised by
    ``boost``: under the softmax the others shrink (they compete), under the sigmoid they stay put (each its own)."""
    parts = VGroup()
    for name in (r"softmax: \ they compete", r"sigmoid: \ each its own"):
        base = Line(LEFT * 0.95, RIGHT * 0.95, color=GREY_C, stroke_width=1.5)
        parts.add(VGroup(Rectangle(width=1.9, height=1.0, stroke_width=0, fill_opacity=0).next_to(base, UP, buff=0), base,
                         label(name, font_size=18, color=GREY_A).next_to(base, DOWN, buff=0.1)))
    parts.arrange(RIGHT, buff=0.7)  # (an invisible box above each base keeps room for the tallest bars)
    bars = gate_bars(VGroup(*[VGroup(VGroup(), p_[1]) for p_ in parts]), 0.0)
    return VGroup(*[VGroup(b_, p_[1], p_[2], p_[0]) for b_, p_ in zip(bars, parts)])


def gate_bars(pic: VGroup, boost: float) -> tuple[VGroup, VGroup]:
    s = SIG_SCORES.copy()
    s[0] += boost
    soft = np.exp(s) / np.exp(s).sum()
    sig = 1 / (1 + np.exp(-s))
    out = []
    for panel, vals in zip(pic, (soft, sig)):
        base = panel[1]
        unit = base.get_length() / 2.2  # the bars' height scale follows the picture's size
        x0 = base.get_left()[0] + 0.25 * unit
        out.append(VGroup(*[Rectangle(width=0.3 * unit, height=max(1.2 * unit * float(v), 0.01), stroke_width=0,
                                      fill_color=EXPERT_COLORS[i], fill_opacity=0.9)
                            .move_to([x0 + (0.15 + 0.5 * i) * unit, base.get_y() + 0.6 * unit * float(v), 0])
                            for i, v in enumerate(vals)]))
    return tuple(out)
