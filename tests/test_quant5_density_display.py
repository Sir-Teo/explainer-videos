"""A plot window must not renormalize the probability carried by its bins."""

import numpy as np

from videos.quant.quant5.compute import _full_sample_histogram_density


def test_density_retains_mass_of_samples_outside_the_view():
    values = [-1.0, 0.1, 0.4, 1.2]
    edges = np.array([0.0, 0.25, 0.75])
    density = _full_sample_histogram_density(values, edges)
    np.testing.assert_allclose(density * np.diff(edges), [0.25, 0.25])
    assert np.dot(density, np.diff(edges)) == 0.5


def test_weighted_density_uses_all_draws_without_self_normalizing():
    density = _full_sample_histogram_density([-1.0, 0.1, 0.4, 1.2], [0.0, 0.25, 0.75],
                                            weights=[4.0, 0.5, 1.0, 2.0])
    np.testing.assert_allclose(density * np.array([0.25, 0.5]), [0.125, 0.25])
