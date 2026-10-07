"""Field -> RGB conversion tuned for a dark 3b1b-style background."""

from __future__ import annotations

import numpy as np

from ..style import BACKGROUND, PRESSURE_HIGH, PRESSURE_LOW, VORT_NEG, VORT_POS


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


BG = hex_rgb(BACKGROUND)


def diverging(field, vmax, neg=VORT_NEG, pos=VORT_POS, gamma=0.8, bg=None):
    """Signed field: 0 -> background, -vmax -> ``neg``, +vmax -> ``pos``."""
    bg = BG if bg is None else hex_rgb(bg)
    t = np.clip(np.asarray(field, dtype=np.float32) / vmax, -1, 1)
    a = np.abs(t)[..., None] ** gamma
    col = np.where(t[..., None] >= 0, hex_rgb(pos), hex_rgb(neg))
    return bg + a * (col - bg)


def sequential(field, vmin, vmax, low=PRESSURE_LOW, high=PRESSURE_HIGH, mid=None):
    """Two- or three-stop linear colormap."""
    t = np.clip((np.asarray(field, dtype=np.float32) - vmin) / (vmax - vmin), 0, 1)[..., None]
    lo, hi = hex_rgb(low), hex_rgb(high)
    if mid is None:
        return lo + t * (hi - lo)
    md = hex_rgb(mid)
    return np.where(t < 0.5, lo + 2 * t * (md - lo), md + (2 * t - 1) * (hi - md))


def dye_overlay(dye, vort, vmax, base_gain=0.18, gamma=0.9):
    """Smoke-like dye whose tint follows the local spin direction."""
    dye = np.clip(np.asarray(dye, dtype=np.float32), 0, 1)[..., None] ** gamma
    t = np.clip(np.asarray(vort, dtype=np.float32) / vmax, -1, 1)[..., None]
    white = np.array([0.93, 0.95, 1.0], dtype=np.float32)
    tint = np.where(t >= 0, hex_rgb(VORT_POS), hex_rgb(VORT_NEG))
    col = white + np.abs(t) * (tint - white)
    glow = diverging(vort, vmax) * base_gain + BG * (1 - base_gain)
    return glow + dye * (col - glow)


def to_uint8(rgb) -> np.ndarray:
    return (np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8)


def solid_mask(rgb, solid, color="#C9CED6"):
    rgb = np.array(rgb, copy=True)
    rgb[solid] = hex_rgb(color)
    return rgb
