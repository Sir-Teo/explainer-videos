"""Helpers shared by the scenes of Part 10 ("Banach Algebras and the Spectral Theorem").

Operators are drawn in C.OPERATOR, spectra in C.SPECTRUM (green), spectral measures in C.MEASURE (amber), and the
complex plane of the spectral parameter with the phase coloring of Part 7.
"""

from __future__ import annotations

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import polyline  # noqa: F401
from videos.analysis.analysis2.common import plain_axes  # noqa: F401
from videos.analysis.analysis4.common import heatmap, square_axes  # noqa: F401
from videos.analysis.analysis7.common import cplot, phase_wheel, zcurve  # noqa: F401

from .compute import load, trap  # noqa: F401


def phase_key(radius=0.3, font_size=20) -> VGroup:
    """Part 7's phase wheel (the legend of a domain coloring) with its labels at a legible size."""
    w = phase_wheel(radius)
    ring, labs, t = w
    for m_, side in zip(labs, (RIGHT, LEFT, UP)):
        m_.scale(font_size / 18).next_to(ring, side, buff=0.06 if side is not UP else 0.04)
    t.scale(font_size / 20).next_to(ring, DOWN, buff=0.06)
    return w
