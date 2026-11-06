"""Scientific regressions for the matrix examples in Statistics, Built Part 4."""

import numpy as np
import pytest

from videos.stats.stats4 import compute


def test_gram_schmidt_basis_and_returned_triangular_factor_reconstruct_the_design():
    result = compute.compute_projection()
    q = np.column_stack([result['q1'], result['q2']])
    np.testing.assert_allclose(q.T @ q, np.eye(2), atol=1e-14)
    np.testing.assert_allclose(q @ result['R'], result['A'], atol=1e-14)
    np.testing.assert_allclose(np.tril(result['R'], -1), 0, atol=1e-14)


def test_projection_lab_handles_independent_columns_whose_gram_matrix_loses_rank(monkeypatch):
    from manim import VectorizedPoint
    from videos.stats.stats4 import common

    class GeometryStub:
        def __init__(self, **kwargs):
            pass

        def __getattr__(self, name):
            return lambda *args, **kwargs: VectorizedPoint()

    monkeypatch.setattr(common, 'NSpace', GeometryStub)
    a = np.column_stack([np.ones(3), [1., 1. + 1e-9, 1. - 1e-9]])
    y = np.array([2., -1., 3.])
    assert np.linalg.matrix_rank(a) == 2
    assert np.linalg.matrix_rank(a.T @ a) == 1
    lab = common.ProjectionLab(a, y)
    np.testing.assert_allclose(lab.P @ a, a, atol=1e-14)
    np.testing.assert_allclose(lab.P @ lab.P, lab.P, atol=1e-14)
    np.testing.assert_allclose(a.T @ lab.r, 0, atol=1e-14)
    assert y @ y == pytest.approx(lab.Py @ lab.Py + lab.r @ lab.r)


def test_block_inverse_check_covers_the_whole_matrix():
    result = compute.compute_blocks()
    assert result['err_block'] < 1e-14
    assert result['err_sm'] < 1e-14


def test_nearest_correlation_matrix_meets_the_symmetric_examples_known_optimum():
    result = compute.compute_extras3()['nearcorr']
    expected = np.array([[1., .5, -.5], [.5, 1., .5], [-.5, .5, 1.]])
    np.testing.assert_allclose(result['fixed'], expected, atol=1e-12)
    assert np.min(result['fixed_eig']) >= -1e-12
