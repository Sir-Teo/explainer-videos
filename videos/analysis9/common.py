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


def spike_halves(ax, x, y, color, stroke_width, top=None):
    """The graph of a spike peaked at 0, cut where it leaves the window (never flattened), as two pieces, left and
    right of the peak: the group keeps one shape whether or not the spike fits."""
    top = ax.y_range[1] if top is None else top
    out = VGroup()
    for side in (x <= 0, x >= 0):
        xs, ys = x[side], y[side]
        if side[0]:  # left half: rising
            k = np.flatnonzero(ys > top)
            if len(k):
                i = k[0]
                xc = xs[i - 1] + (top - ys[i - 1]) * (xs[i] - xs[i - 1]) / (ys[i] - ys[i - 1])
                xs, ys = np.append(xs[:i], xc), np.append(ys[:i], top)
        else:  # right half: falling
            k = np.flatnonzero(ys > top)
            if len(k):
                i = k[-1]
                xc = xs[i] + (ys[i] - top) * (xs[i + 1] - xs[i]) / (ys[i] - ys[i + 1])
                xs, ys = np.insert(xs[i + 1:], 0, xc), np.insert(ys[i + 1:], 0, top)
        out.add(polyline(ax, xs, ys, color=color, stroke_width=stroke_width))
    return out
