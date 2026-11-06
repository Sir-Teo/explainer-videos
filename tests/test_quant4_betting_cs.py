"""Regression checks for bounded, continuous-mean betting confidence sequences."""

import itertools

import numpy as np
import pytest

from explainer.quant.house.martingale import betting_cs


def test_constant_mean_between_grid_points_is_covered_at_every_time():
    # Grid points are numerical brackets, not an assumption about possible means.
    cs = betting_cs(np.full(400, 0.37), [0.2, 0.4, 0.6, 0.8])
    assert np.all(cs["lower"] <= 0.37)
    assert np.all(cs["upper"] >= 0.37)
    assert np.all(np.diff(cs["lower"]) >= 0)
    assert np.all(np.diff(cs["upper"]) <= 0)


@pytest.mark.parametrize("mean", [0.1, 0.37, 0.9])
def test_exact_bernoulli_probability_of_any_false_exclusion(mean):
    # Enumerate the complete null law, including skewed coins and off-grid means.
    alpha, n, false_probability = 0.2, 9, 0.0
    for path in itertools.product((0.0, 1.0), repeat=n):
        cs = betting_cs(path, [0.1, 0.3, 0.5, 0.7, 0.9], alpha=alpha)
        heads = sum(path)
        if np.any(~((cs["lower"] <= mean) & (mean <= cs["upper"]))):
            false_probability += mean ** heads * (1 - mean) ** (n - heads)
    assert false_probability <= alpha + 1e-12


def test_changing_return_units_preserves_the_interval():
    x = np.random.default_rng(4).beta(2, 5, 200)
    grid = np.linspace(0.1, 0.9, 81)
    unit = betting_cs(x, grid)
    returns = betting_cs(0.4 * x - 0.2, 0.4 * grid - 0.2, lo=-0.2, hi=0.2)
    np.testing.assert_allclose(returns["lower"], 0.4 * unit["lower"] - 0.2)
    np.testing.assert_allclose(returns["upper"], 0.4 * unit["upper"] - 0.2)


def test_out_of_range_observations_are_rejected_instead_of_clipped():
    with pytest.raises(ValueError, match="within"):
        betting_cs([0.1, 1.1], [0.2, 0.5, 0.8])
