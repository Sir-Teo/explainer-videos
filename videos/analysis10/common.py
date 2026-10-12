"""Helpers shared by the scenes of Part 10 ("Banach Algebras and the Spectral Theorem").

Operators are drawn in C.OPERATOR, spectra in C.SPECTRUM (green), spectral measures in C.MEASURE (amber), and the
complex plane of the spectral parameter with the phase coloring of Part 7.
"""

from __future__ import annotations

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import heatmap, square_axes  # noqa: F401
from videos.analysis7.common import cplot, phase_wheel, zcurve  # noqa: F401

from .compute import load, trap  # noqa: F401
