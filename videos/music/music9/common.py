"""Helpers shared by the scenes of Part 9 ("Drums, Bars and Bells")."""

from __future__ import annotations

import numpy as np
from scipy.special import jn_zeros

from explainer.music.kit import *  # noqa: F403

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 9
clip = clip_loader(CACHE, CLIPS)
SKIN = "#E9D8B4"
WOODC = "#C8935A"
BRONZE = "#D9A441"
STEEL = "#9FB7C9"
PLAYERS = {"marimba": WOODC, "bells": BRONZE, "steelpan": STEEL, "kettledrums": SKIN}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, links=("string", "instrument"), extra=extra, spoken=spoken)


def curve_from(g, xs, ys, color, stroke_width=3):
    return curve(g.ax, np.asarray(xs, dtype=float), np.asarray(ys, dtype=float), color, stroke_width=stroke_width)


def lane(names, colors, width: float = 2.6, height: float = 0.9, buff: float = 0.25, font_size: int = 26) -> VGroup:
    return VGroup(*[VGroup(RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=c, stroke_width=2.5),
                           label(n, font_size=font_size, color=c)) for n, c in zip(names, colors)]).arrange(RIGHT, buff=buff)


def mode_diagram(m: int, n: int, radius: float = 0.8, up=AIR, down=BAD) -> VGroup:
    """A round skin's mode (m, n) as a map: regions that rise while their neighbours fall, with the nodal diameters
    and circles between them."""
    zeros = jn_zeros(m, n)
    rings = [0.0] + [float(z / zeros[-1]) * radius for z in zeros]
    g = VGroup()
    sectors = max(2 * m, 1)
    for k in range(n):
        for s in range(sectors):
            sign = (k + s) % 2 == 0
            g.add(AnnularSector(inner_radius=rings[k], outer_radius=rings[k + 1], start_angle=s * TAU / sectors + (TAU / (4 * m) if m else 0.0), angle=TAU / sectors,
                                fill_color=up if sign else down, fill_opacity=0.55, stroke_width=0))
    g.add(Circle(radius=radius, color=SKIN, stroke_width=3))
    return g


def rgba_image(rgba: np.ndarray, height: float) -> ImageMobject:
    img = ImageMobject(np.asarray(rgba, dtype=np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    img.height = height
    return img


def mode_image(u: np.ndarray, height: float, up=(125, 211, 252), down=(239, 83, 80)) -> ImageMobject:
    """A mode shape as a picture: one colour where the skin rises, another where it falls, clear where it is still or
    where there is no skin (zero).  Row 0 of ``u`` is the bottom."""
    z = np.asarray(u, dtype=float)[::-1]
    z = z / max(np.abs(z).max(), 1e-12)
    a = np.abs(z) ** 0.6
    rgba = np.zeros(z.shape + (4,), dtype=np.uint8)
    for c in range(3):
        rgba[..., c] = np.where(z >= 0, up[c], down[c])
    rgba[..., 3] = (255 * a).astype(np.uint8)
    return rgba_image(rgba, height)


def sand_image(u: np.ndarray, height: float, plate=(58, 46, 36), sand=(245, 230, 190)) -> ImageMobject:
    """A plate with sand on it: the sand lies where the plate does not move."""
    z = np.asarray(u, dtype=float)[::-1]
    z = z / max(np.abs(z).max(), 1e-12)
    w = np.exp(-(z / 0.09) ** 2)
    rgba = np.zeros(z.shape + (4,), dtype=np.uint8)
    for c in range(3):
        rgba[..., c] = (plate[c] * (1 - w) + sand[c] * w).astype(np.uint8)
    rgba[..., 3] = 255
    return rgba_image(rgba, height)


def tick_row(g, values, y: float, color, half: float = 0.2, font_size: int = 18, fmt="{:.2f}", labels: bool = True, crowd: float = 0.5) -> VGroup:
    """Marks on an axis for a list of frequencies or ratios, with their values above (a label too close to the one
    before it is raised clear of it)."""
    out = VGroup()
    last_x, raised = -1e9, False
    for v in values:
        top = g.ax.c2p(v, y + half)
        mk = VGroup(Line(g.ax.c2p(v, y - half), top, color=color, stroke_width=5))
        if labels:
            raised = (top[0] - last_x < crowd) and not raised
            mk.add(label(fmt.format(v), font_size=font_size, color=color).next_to(top, UP, buff=0.05 + (0.24 if raised else 0.0)))
            last_x = top[0]
        out.add(mk)
    return out


def polygon_shape(points, scale: float = 0.8, color=SKIN, fill=0.12) -> Polygon:
    return Polygon(*[np.array([x * scale, y * scale, 0.0]) for x, y in points], color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
