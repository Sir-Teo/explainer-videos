"""Color maps for complex amplitudes (pure NumPy; used by compute.py and the scenes).

The convention, the same everywhere in the video (and the same hue order as the Riemann video's domain coloring):
the *phase* arg(psi) is the hue (0 red, pi/2 yellow-green, pi cyan, 3pi/2 violet), and the *size* |psi| is the
brightness, fading into the background where psi = 0.  Hues are taken at constant lightness and chroma in OKLCH
(a perceptually uniform space), so no phase looks brighter than another: the bright yellow and cyan bands of a
plain HSV wheel would read as features that aren't there.
"""

from __future__ import annotations

import numpy as np

BACKGROUND = "#0E1117"
L_PHASE, C_PHASE = 0.745, 0.125  # OKLCH lightness and chroma of a full-size amplitude (the largest chroma in sRGB at every hue)
HUE0 = np.deg2rad(29.0)  # OKLab hue angle of sRGB red: phase 0 is red


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i: i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


BG = hex_rgb(BACKGROUND)


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


def hue_rgb(phase, lightness=L_PHASE, chroma=C_PHASE) -> np.ndarray:
    """Phase (radians) -> sRGB in [0, 1], shape phase.shape + (3,)."""
    h = np.asarray(phase, dtype=np.float64) + HUE0
    return _oklab_to_srgb(np.full_like(h, lightness), chroma * np.cos(h), chroma * np.sin(h)).astype(np.float32)


def phase_rgb(psi, vmax=None, gamma=0.75, floor=0.0) -> np.ndarray:
    """Complex array -> RGB: hue = arg(psi), brightness = (|psi| / vmax)^gamma over the background."""
    psi = np.asarray(psi)
    mag = np.abs(psi)
    vmax = float(mag.max()) if vmax is None else float(vmax)
    t = np.clip(mag / max(vmax, 1e-30), 0, 1)[..., None] ** gamma
    t = np.maximum(t, floor)
    col = hue_rgb(np.angle(psi))
    # Very bright spots turn slightly whiter (like light piling up), keeping the hue readable.
    hot = np.clip((np.abs(psi) / max(vmax, 1e-30) - 0.85) / 0.6, 0, 1)[..., None] * 0.35
    col = col + (1 - col) * hot
    return BG + t * (col - BG)


def real_rgb(f, vmax, pos="#F2A541", neg="#4FA3D9", gamma=0.85) -> np.ndarray:
    """Signed real field (e.g. a Wigner function): 0 -> background, +vmax -> ``pos``, -vmax -> ``neg``."""
    t = np.clip(np.asarray(f, dtype=np.float32) / vmax, -1, 1)
    a = np.abs(t)[..., None] ** gamma
    col = np.where(t[..., None] >= 0, hex_rgb(pos), hex_rgb(neg))
    return BG + a * (col - BG)


def to_uint8(rgb) -> np.ndarray:
    return (np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8)


def rgba(rgb, alpha=1.0) -> np.ndarray:
    """RGB float -> RGBA uint8 with a constant (or per-pixel) alpha."""
    rgb = to_uint8(rgb)
    a = np.broadcast_to(np.asarray(alpha, dtype=np.float32), rgb.shape[:2])
    return np.concatenate([rgb, to_uint8(a)[..., None]], axis=2)
