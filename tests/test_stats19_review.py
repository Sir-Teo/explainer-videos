"""Independent mathematical checks for the Part 19 review."""
import itertools

import numpy as np
import pytest
from scipy.integrate import quad

from explainer.stats.kit import learn as L
from videos.stats.stats19 import compute as C


def test_exact_neighbour_risk_matches_independent_quadrature():
    x = np.array([.08, .22, .51, .68, .93])
    y = np.array([1., -.2, .5, -.3, .1])
    points = sorted({(a+b)/2 for a, b in itertools.combinations(x, 2)})
    for k in (1, 2, 3, len(x)):
        # Quad queries an independently implemented nearest-neighbour predictor.
        def loss(t):
            nearest = np.argsort(np.abs(x-t), kind='stable')[:k]
            return (y[nearest].mean()-C.truth_curve(t))**2
        expected = .09+quad(loss, 0, 1, points=points, epsabs=1e-11)[0]
        assert C.knn_population_risk(x, y, k) == pytest.approx(expected, abs=2e-12)


def test_neighbour_risk_includes_noise_and_rejects_invalid_windows():
    # Zero fitted function: integral of (sin(2*pi*x)+x/2)^2 plus noise.
    expected = .09+.5-1/(2*np.pi)+1/12
    assert C.knn_population_risk([.2, .8], [0, 0], 2) == pytest.approx(expected)
    with pytest.raises(ValueError):
        C.knn_population_risk([.2, .8], [0, 0], 3)
    with pytest.raises(ValueError):
        C.knn_population_risk([.2, .2], [0, 0], 1)


def test_threshold_precision_recall_matches_complete_ties():
    scores = np.array([.9, .8, .8, .5, .5, .2])
    labels = np.array([0, 1, 0, 1, 1, 0])
    actual = C.threshold_pr_curve(scores, labels)
    # The attainable positive sets contain 0, 1, 3, 5 and 6 observations.
    np.testing.assert_allclose(actual[0], [1, 0, 1/3, 3/5, 1/2])
    np.testing.assert_allclose(actual[1], [0, 0, 1/3, 1, 1])
    permutation = [0, 2, 1, 4, 3, 5]
    reordered = C.threshold_pr_curve(scores[permutation], labels[permutation])
    np.testing.assert_allclose(actual, reordered)
    assert actual[1][-1] == 1
    assert actual[0][-1] == labels.mean()


def test_normalized_ridge_and_lasso_share_the_stated_orthogonal_scale():
    g = np.random.default_rng(119)
    n = 30
    centered = g.normal(size=(n, 3))
    centered -= centered.mean(0)
    Q, _ = np.linalg.qr(centered)
    X = np.sqrt(n)*Q
    least_squares = np.array([2., -.4, .1])
    y = X@least_squares
    lam = .3
    np.testing.assert_allclose(L.ridge(X, y, n*lam), least_squares/(1+lam), atol=1e-12)
    np.testing.assert_allclose(L.lasso(X, y, lam), [1.7, -.1, 0.], atol=1e-12)
    d = C.load('lasso')
    assert d['n'] == 100
    assert d['ridge_lams'][0] == pytest.approx(10)


def test_fixed_design_risk_uses_bias_and_projection_variance():
    d = C.load('cp')
    x = np.asarray(C.load('poly')['x'])
    f = C.truth_curve(x)
    expected = []
    # A different polynomial basis gives the same projection risk, even under misspecification.
    for degree in d['deg']:
        V = np.polynomial.chebyshev.chebvander(2*x-1, degree)
        fitted = V@np.linalg.lstsq(V, f, rcond=None)[0]
        expected.append(np.mean((f-fitted)**2)+.09*(1+(degree+1)/len(x)))
    np.testing.assert_allclose(d['fixed_design_expected_risk'], expected, atol=1e-10)
    assert d['fixed_design_expected_risk'][-1] < 1
    assert d['test'][-1] > 100  # random-input instability is a different risk target


def test_polynomial_values_are_not_numerically_flattened():
    d = C.load('poly')
    values = np.array(d['fits']['12'])
    assert np.max(np.abs(values)) > 3
    assert not np.any(values == 3)
    segments = C.clipped_segments([0, 1, 2], [2, .5, 2], (0, 2, 0, 1))
    np.testing.assert_allclose(segments, [[[2/3, 1], [1, .5]], [[1, .5], [4/3, 1]]])


def test_tree_leaf_budget_can_skip_sizes():
    d = C.load('tree')
    def count(node):
        return count(node['left'])+count(node['right']) if 'left' in node else 1
    assert d['best'] == 4
    assert count(d['pruned']) == d['pruned_leaves'] == 3
    assert count(d['small']) == 3
