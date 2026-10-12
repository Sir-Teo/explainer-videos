"""Helpers shared by the scenes of Part 9 ("Distributions and the Fourier Transform").

The space side is drawn in blue, the frequency side in orange (C.FREQ), test functions in C.TEST_FN and
distributions in C.DISTRIBUTION.
"""

from __future__ import annotations

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import polyline  # noqa: F401
from videos.analysis2.common import plain_axes  # noqa: F401
from videos.analysis4.common import square_axes  # noqa: F401
from videos.analysis5.common import area_under  # noqa: F401
from videos.analysis7.common import cplot  # noqa: F401

from .compute import SQ2PI, bump, load, rho, trap  # noqa: F401
