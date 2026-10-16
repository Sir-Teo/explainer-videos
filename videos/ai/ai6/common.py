"""Helpers shared by the scenes of Part 6 ("Statistical ML")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
AUSTEN, DICKENS = "#E86F8A", "#58A6FF"  # as in Part 5
HIDDEN = "#B39DDB"  # hidden variables, latent states
VOWEL, CONSONANT = C.BITS, "#58A6FF"


def mix(a, b, t) -> ManimColor:
    return interpolate_color(ManimColor(a), ManimColor(b), float(np.clip(t, 0, 1)))


def ellipse_2sd(ax, mean, cov, color, stroke_width=3, k=2.0) -> VMobject:
    """The k-standard-deviation ellipse of a 2D Gaussian, drawn on ``ax``."""
    vals, vecs = np.linalg.eigh(np.asarray(cov))
    ts = np.linspace(0, 2 * np.pi, 90)
    pts = [np.asarray(mean) + vecs @ (k * np.sqrt(np.maximum(vals, 1e-9)) * np.array([np.cos(t), np.sin(t)]))
           for t in ts]
    return VMobject(color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(*p) for p in pts])
