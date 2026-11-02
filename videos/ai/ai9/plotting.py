"""Pure plot-coordinate helpers for Part 9; no scene, producer or cache imports."""

from __future__ import annotations

import math

import numpy as np


def checkpoint_prefix(xs, ys, step):
    """Reveal past checkpoints and the interpolated current endpoint, never a future vertex.

    Duplicate the sole initial point to give Manim a stationary path. The input
    checkpoints stay unchanged; interpolation matches the scene's moving marker.
    """
    xs, ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    if (xs.ndim != 1 or ys.shape != xs.shape or not len(xs)
            or not np.isfinite(xs).all() or not np.isfinite(ys).all()
            or not np.all(np.diff(xs) > 0) or not np.isfinite(step)):
        raise ValueError("checkpoint curve needs finite values and strictly increasing steps")
    current = float(np.clip(step, xs[0], xs[-1]))
    stop = int(np.searchsorted(xs, current, side="right"))
    points = np.column_stack((xs[:stop], ys[:stop]))
    if points[-1, 0] < current:
        points = np.vstack((points, [current, np.interp(current, xs, ys)]))
    if len(points) == 1:
        points = np.repeat(points, 2, axis=0)
    return points


def finite_plot_values(values, lo, hi):
    """Keep the existing finite-value viewport clamp, leaving gaps for NaN/inf.

    A non-finite loss is missing/diverged data, never a measured chart-edge loss.
    The shared ``curve`` helper splits its path at these NaNs.
    """
    values = np.asarray(values, dtype=float)
    return np.where(np.isfinite(values), np.clip(values, lo, hi), np.nan)


def safe_log_values(values):
    """Exact base-ten logs of positive observations, with nonfinite gaps.

    Zero has no finite logarithm and needs an explicit scene annotation. Reject
    it (and invalid negative values) instead of inventing a positive error floor.
    """
    values = np.asarray(values, dtype=float)
    finite = np.isfinite(values)
    if np.any(finite & (values <= 0)):
        raise ValueError("log plots require positive observations; zero needs explicit log-axis annotation")
    logs = np.full(values.shape, np.nan)
    np.log10(values, out=logs, where=finite)
    return logs


def _finite_history_values(histories):
    arrays = [np.asarray(h, dtype=float).reshape(-1) for h in histories]
    values = np.concatenate(arrays) if arrays else np.array([], dtype=float)
    finite = values[np.isfinite(values)]
    if not finite.size:
        raise ValueError("plot range needs at least one finite observation")
    return finite


def _check_padding(padding):
    if not math.isfinite(padding) or padding <= 0:
        raise ValueError("plot padding must be finite and positive")


def log_plot_range(histories, padding=0.15):
    """Integer-decade bounds around every positive finite recorded value.

    Padding is in decades. Only the viewport changes, never the observations.
    A constant history gets a nonzero axis span; absent/nonpositive data fail
    explicitly rather than producing a fabricated default endpoint or floor.
    """
    _check_padding(padding)
    values = _finite_history_values(histories)
    logs = safe_log_values(values)
    return math.floor(float(logs.min()) - padding), math.ceil(float(logs.max()) + padding)


def linear_plot_range(histories, padding=0.05):
    """Bounds around all finite recorded values; padding is a span fraction.

    Constant histories expand the axis by padding * max(abs(value), 1) on each
    side. Empty/all-nonfinite histories and unrepresentable bounds fail clearly.
    """
    _check_padding(padding)
    values = _finite_history_values(histories)
    lo, hi = float(values.min()), float(values.max())
    span = hi - lo
    margin = padding * (span if span else max(abs(lo), 1.0))
    bounds = lo - margin, hi + margin
    if not all(math.isfinite(v) for v in bounds) or bounds[0] >= bounds[1]:
        raise ValueError("plot bounds cannot represent the requested finite range and padding")
    return bounds


def clip_y_segments(xs, ys, lo, hi):
    """Clip piecewise-linear geometry to a viewport, without flattening data onto its edges.

    Separate visible runs stay separate across an off-screen excursion. Crossing
    points interpolate the original segment; input observations are unchanged.
    """
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    if xs.ndim != 1 or ys.shape != xs.shape or not np.isfinite([lo, hi]).all() or lo >= hi:
        raise ValueError('clipping needs paired coordinates and a finite increasing viewport')
    runs, current = [], []

    def finish():
        nonlocal current
        if len(current) >= 2:
            runs.append(np.asarray(current))
        current = []

    points = np.column_stack((xs, ys))
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            finish()
            continue
        delta = end - start
        if delta[1] == 0:
            if not lo <= start[1] <= hi:
                finish()
                continue
            enter, leave = 0., 1.
        else:
            ta, tb = sorted(((lo - start[1]) / delta[1], (hi - start[1]) / delta[1]))
            enter, leave = max(0., ta), min(1., tb)
            if enter >= leave:
                finish()
                continue
        a, b = start + enter * delta, start + leave * delta
        if current and not np.allclose(current[-1], a, rtol=0, atol=1e-12):
            finish()
        if not current:
            current.append(a)
        current.append(b)
        if leave < 1. or not lo <= end[1] <= hi:
            finish()
    finish()
    return runs
