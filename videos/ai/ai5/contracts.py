"""Small numerical definitions used by Part 5; importing never computes an item."""
from __future__ import annotations

from fractions import Fraction
import math

import numpy as np


def coin_sample_sizes(epsilon, delta):
    """Separate a qualifying fixed sample size from an eventual lattice threshold.

    Enumerate through a Hoeffding-certified cutoff; that bound controls every
    larger integer, so two consecutive successes are never used as a proof.
    """
    from scipy.stats import binom

    if not (0 < epsilon < 0.5 and 0 < delta < 1):
        raise ValueError("require 0 < epsilon < 1/2 and 0 < delta < 1")
    threshold = Fraction(1, 2) + Fraction(str(epsilon))
    cutoff = math.ceil(math.log(1 / delta) / (2 * epsilon ** 2))
    while math.exp(-2 * cutoff * epsilon ** 2) > delta:
        cutoff += 1
    tails = []
    for n in range(1, cutoff + 1):
        first = (n * threshold.numerator + threshold.denominator - 1) // threshold.denominator
        tails.append(float(binom.sf(first - 1, n, 0.5)))
    passing = [n for n, tail in enumerate(tails, 1) if tail <= delta]
    failed = [n for n, tail in enumerate(tails, 1) if tail > delta]
    return dict(minimum=passing[0], eventual=1 + max(failed, default=0),
                certified_cutoff=cutoff, probabilities=np.asarray(tails),
                scope="Inclusive one-sided fair-coin tail; exact binomial enumeration and Hoeffding beyond cutoff")


def es_gradient(values, probes, sigma, kind="plain"):
    """Estimate the Gaussian-smoothed objective gradient with an explicit baseline.

    The same-batch mean needs N/(N-1) for iid probes. In an antithetic batch
    the shared scalar baseline cancels; applying that correction would bias it.
    """
    values, probes = np.asarray(values, float), np.asarray(probes, float)
    if (values.ndim != 1 or probes.ndim != 2 or len(values) != len(probes)
            or not len(values) or not math.isfinite(sigma) or sigma <= 0
            or not np.isfinite(values).all() or not np.isfinite(probes).all()):
        raise ValueError("finite values and matching probes with positive sigma required")
    if kind not in ("plain", "base", "mirror"):
        raise ValueError("unknown estimator")
    factor = 1.0
    if kind != "plain":
        if kind == "base":
            if len(values) < 2:
                raise ValueError("iid baseline needs at least two independent probes")
            factor = len(values) / (len(values) - 1)
        elif len(values) % 2 or not np.array_equal(probes[:len(values) // 2], -probes[len(values) // 2:]):
            raise ValueError("mirrored probes must contain exact antithetic pairs")
        values = values - values.mean()
    return factor * (values[:, None] * probes).mean(axis=0) / sigma


def rosen_smoothed_gradient(theta, sigma):
    """Analytic gradient of E[(1-X)^2+5(Y-X^2)^2], Gaussian variance sigma²."""
    x, y = np.asarray(theta, float)
    if not np.isfinite([x, y, sigma]).all() or sigma < 0:
        raise ValueError("finite parameters and nonnegative sigma required")
    return np.array([-2 * (1 - x) - 20 * x * (y - x * x) + 60 * x * sigma ** 2,
                     10 * (y - x * x) - 10 * sigma ** 2])


def rosen_smoothed_minimum(sigma):
    if not math.isfinite(sigma) or sigma < 0:
        raise ValueError("finite nonnegative sigma required")
    x = 1 / (1 + 20 * sigma ** 2)
    return np.array([x, x * x + sigma ** 2])


def rosen_smoothed_value(theta, sigma):
    """Analytic Gaussian expectation, including its additive constants."""
    p = np.asarray(theta, float)
    if p.shape[-1:] != (2,) or not np.isfinite(p).all() or not math.isfinite(sigma) or sigma < 0:
        raise ValueError("finite two-coordinate points and nonnegative sigma required")
    x, y = p[..., 0], p[..., 1]
    v = sigma ** 2
    return (1 - x) ** 2 + v + 5 * ((y - x * x) ** 2 + v * (1 - 2 * y + 6 * x * x) + 3 * v * v)


def left_halfspace_reference():
    """Exact X<0 mass and conditional x variance of density2's normalized mixture."""
    masses = np.array([2 / 3, 1 / 3])
    means = np.array([-1.6, 1.5])
    variances = np.array([0.35, 0.25])
    sds = np.sqrt(variances)
    a = -means / sds
    cdf = np.array([0.5 * math.erfc(-float(z) / math.sqrt(2)) for z in a])
    pdf = np.exp(-0.5 * a * a) / math.sqrt(2 * math.pi)
    mass = float(masses @ cdf)
    first = float(masses @ (means * cdf - sds * pdf))
    second = float(masses @ ((means * means + variances) * cdf - sds * means * pdf))
    return dict(mass=mass, mean=first / mass, variance=second / mass - (first / mass) ** 2,
                scope="Normalized two-dimensional mixture, marginal event x<0; not component membership")


def mixture_bin_density(edges, means, variances, weights):
    """Exact Gaussian-mixture bin averages, conditioned on the displayed window.

    This matches histogram(..., density=True), including its window normalization;
    a density sampled at a nearby grid point is a different statistic.
    """
    from scipy.special import ndtr

    edges = np.asarray(edges, float)
    means, variances, weights = (np.asarray(a, float) for a in (means, variances, weights))
    if (edges.ndim != 1 or len(edges) < 2 or np.any(np.diff(edges) <= 0)
            or means.ndim != 1 or means.shape != variances.shape or means.shape != weights.shape
            or not len(means) or not all(np.isfinite(a).all() for a in (edges, means, variances, weights))
            or np.any(variances <= 0) or np.any(weights < 0) or weights.sum() <= 0):
        raise ValueError("ordered finite edges and valid finite mixture parameters required")
    cdf = ndtr((edges[:, None] - means) / np.sqrt(variances)) @ (weights / weights.sum())
    masses = np.diff(cdf)
    if cdf[-1] <= cdf[0]:
        raise ValueError("window has no numerically resolved probability mass")
    return masses / ((cdf[-1] - cdf[0]) * np.diff(edges))
