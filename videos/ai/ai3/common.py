"""Helpers shared by the scenes of Part 3 ("Change")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
VALUE, GRAD = "#58A6FF", "#FF9F45"  # values flow forward (blue), gradients flow back (orange)


def bowl(x, y):
    """The landscape of chapters 2 and 3: a tilted bowl with a ripple (illustrative)."""
    return 0.18 * x * x + 0.32 * y * y + 0.35 * np.sin(1.3 * x) * np.cos(0.9 * y) + 0.6


def bowl_grad(x, y):
    return np.array([0.36 * x + 0.455 * np.cos(1.3 * x) * np.cos(0.9 * y),
                     0.64 * y - 0.315 * np.sin(1.3 * x) * np.sin(0.9 * y)])
