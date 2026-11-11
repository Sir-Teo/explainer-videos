"""Helpers shared by the scenes of Part 15 (Exotics and Structured Products)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 15

SPOT = QC.SPOT
OPT = QC.OPTION
BAD = QC.LOSS
GOOD = QC.GAIN
IV = QC.IMPLIED
DELTA = QC.DELTA
VEGA = QC.VEGA
BARRIER = QC.STRIKE
CASH = QC.CASH


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def ymd_to_year(d):
    import numpy as np
    from datetime import date
    d = np.asarray(d, int)
    out = []
    for x in d:
        t = date(x // 10000, (x // 100) % 100, x % 100)
        out.append(t.year + (t.timetuple().tm_yday - 1) / ((date(t.year + 1, 1, 1) - date(t.year, 1, 1)).days))
    return np.array(out)


def data_range(*arrays, pad=0.06, zero=False):
    """Full finite support for display; no winsorization of computed observations."""
    import numpy as np
    values = np.concatenate([np.asarray(a, float).ravel() for a in arrays])
    values = values[np.isfinite(values)]
    if zero:
        values = np.r_[values, 0.0]
    if not len(values):
        raise ValueError("No finite observations")
    lo, hi = float(values.min()), float(values.max())
    margin = max(hi - lo, abs(lo) * 0.05, 1e-8) * pad
    return lo - margin, hi + margin


_base_axes = axes


def axes(x_range, y_range, **kwargs):
    """Keep selected tick labels inside the displayed support."""
    for name, support in (("xticks", x_range), ("yticks", y_range)):
        if kwargs.get(name) is not None:
            kwargs[name] = [x for x in kwargs[name] if support[0] <= x <= support[1]]
    return _base_axes(x_range, y_range, **kwargs)


def pause_card(text, width=12.4, font_size=25):
    """Part-local prediction card retaining this lecture's width argument."""
    return wrapped_label(text, max_width=width, font_size=font_size, color=QC.IDEA).to_edge(DOWN, buff=0.3)
