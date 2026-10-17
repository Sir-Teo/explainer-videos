"""Helpers shared by the scenes of Part 14 ("Diffusion and Flow")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
NOISE, DATA = C.TRUE_P, C.BITS  # noise points, data points
SCORE = C.MODEL_Q  # the score / velocity arrows
DDPM_C, DDIM_C, FM_C, RF_C = C.SURPRISE, C.TRUE_P, C.INTERVAL, C.BITS


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def cloud(P, color, radius=0.03, scale=1.0, shift=ORIGIN, opacity=0.9) -> VGroup:
    return VGroup(*[Dot([p[0] * scale + shift[0], p[1] * scale + shift[1], 0], radius=radius, color=color,
                        fill_opacity=opacity) for p in np.asarray(P)])


def move_cloud(dots: VGroup, P, scale=1.0, shift=ORIGIN) -> list:
    return [d.animate.move_to([p[0] * scale + shift[0], p[1] * scale + shift[1], 0]) for d, p in zip(dots, np.asarray(P))]


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def arrows_field(grid, field, scale=0.12, max_len=0.45, color=SCORE, stroke_width=2.2, shift=ORIGIN, unit=1.0) -> VGroup:
    """Little arrows showing a 2D vector field (lengths compressed so that the strongest ones don't swamp the rest)."""
    g = VGroup()
    F = np.asarray(field)
    mag = np.linalg.norm(F, axis=1)
    top = max(np.percentile(mag, 95), 1e-9)
    for p, v, m in zip(np.asarray(grid), F, mag):
        L = max_len * min(m / top, 1.0) ** 0.6
        if L < 0.04:
            continue
        d = v / max(m, 1e-9)
        s = np.array([p[0] * unit + shift[0], p[1] * unit + shift[1], 0])
        g.add(Arrow(s, s + L * np.array([d[0], d[1], 0]), buff=0, color=color, stroke_width=stroke_width,
                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
    return g


def distill_picture() -> VGroup:
    """A jargon-card picture of distillation: VGroup(teacher's curved path, its many small steps, the student's one
    jump, the two names, the start and the end).  Show the path and ends first, then the steps, then the jump."""
    a, b = np.array([-1.6, -0.45, 0]), np.array([1.6, 0.25, 0])
    path = ArcBetweenPoints(a, b, angle=-1.1, color=FM_C, stroke_width=2.5)
    steps = VGroup(*[Dot(path.point_from_proportion(u), radius=0.045, color=FM_C) for u in np.linspace(0.08, 0.92, 11)])
    jump = Arrow(a, b, buff=0.08, color=RF_C, stroke_width=4, max_tip_length_to_length_ratio=0.12)
    ends = VGroup(Dot(a, radius=0.08, color=NOISE), Dot(b, radius=0.08, color=DATA))
    names = VGroup(label(r"teacher: \ many small steps", font_size=18, color=FM_C).next_to(path, UP, buff=0.08),
                   label(r"student: \ one jump, \ the same place", font_size=18, color=RF_C).next_to(jump, DOWN, buff=0.12))
    return VGroup(path, steps, jump, names, ends)
