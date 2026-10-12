"""Domain colorings for the analysis series (Part 7 onward): a complex function drawn as an image.

The convention is the repo's phase-as-hue map (the same hue order as the Riemann and quantum videos): arg f is the
hue (0 red, pi/2 yellow-green, pi cyan, 3pi/2 violet) at constant OKLCH lightness and chroma, so no phase looks
brighter than another; |f| sets the brightness, with faint rings where |f| crosses a power of 2, so zeros are dark
points circled by shrinking rings and poles are bright points circled by growing ones.
"""

from __future__ import annotations

import numpy as np
from manim import RESAMPLING_ALGORITHMS, ImageMobject

from explainer.style import BACKGROUND

HUE0 = np.deg2rad(29.0)  # OKLab hue angle of sRGB red: phase 0 is red
L_PHASE, C_PHASE = 0.72, 0.16  # vivid; a few hues clip slightly in sRGB


def _oklab_to_srgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    lin = np.clip(np.stack([r, g, bb], axis=-1), 0, 1)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def hue_rgb(phase) -> np.ndarray:
    """Phase (radians) -> sRGB in [0, 1]."""
    h = np.asarray(phase, dtype=np.float64) + HUE0
    return _oklab_to_srgb(np.full_like(h, L_PHASE), C_PHASE * np.cos(h), C_PHASE * np.sin(h))


def _hex(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i: i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255.0


def domain_rgb(Z, rings=True) -> np.ndarray:
    """Complex array -> RGB in [0, 1]."""
    Z = np.asarray(Z, dtype=np.complex128)
    Z = np.where(np.isfinite(Z), Z, 1e8)
    mag = np.abs(Z)
    col = hue_rgb(np.angle(Z))
    m = mag**0.6
    v = 0.12 + 0.88 * m / (1 + m)  # dark near a zero, 0.56 at |f| = 1, -> 1 near a pole
    if rings:
        lm = np.log2(np.maximum(mag, 1e-12))
        v = v * (0.74 + 0.26 * (lm - np.floor(lm)))
    v = v * np.clip(mag / 0.06, 0, 1) ** 0.35  # sink to black right at the zeros
    bg = _hex(BACKGROUND)
    big = np.clip((mag - 8) / 40, 0, 1)[..., None] * 0.35  # whiten toward the poles
    col = col + (1 - col) * big
    return bg + v[..., None] * (col - bg)


def domain_image(F, xr, yr, width, height, px=720, rings=True, mask=None) -> ImageMobject:
    """F(Z) on the rectangle xr x yr of the complex plane, as an image of the given scene size (place it with
    .move_to(ax.c2p(center))).  ``mask(Z)`` (optional) makes the pixels where it is False transparent."""
    py = max(2, int(px * height / width))
    X, Y = np.meshgrid(np.linspace(xr[0], xr[1], px), np.linspace(yr[1], yr[0], py))
    with np.errstate(all="ignore"):
        Z = F(X + 1j * Y)
    rgb = domain_rgb(Z, rings=rings)
    if mask is not None:  # mask(Z) -> bool: transparent where False
        a = mask(X + 1j * Y).astype(float)[..., None]
        rgb = np.concatenate([rgb, a], axis=-1)
    img = ImageMobject((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height)
    return img


__all__ = ["domain_image", "domain_rgb", "hue_rgb"]
