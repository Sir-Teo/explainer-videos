"""A normalized illustrative feature density, never a fitted speech result."""
from __future__ import annotations

import numpy as np


def schematic_feature_density(x):
    """One feature coordinate: .6 N(-.3,.25²) + .4 N(.35,.30²).

    Coefficients are probability masses; density height is not probability.
    The renderer crops the tails for display and does not renormalize them.
    """
    x = np.asarray(x, dtype=float)
    return sum(weight * np.exp(-0.5 * ((x - mean) / sd) ** 2)
               / (sd * np.sqrt(2 * np.pi))
               for weight, mean, sd in [(0.6, -0.3, 0.25), (0.4, 0.35, 0.30)])
