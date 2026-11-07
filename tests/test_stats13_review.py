"""Independent references for the experimental-design illustrations."""

import itertools

import numpy as np
import pytest
import statsmodels.api as sm
from scipy import stats

from videos.stats.stats13 import compute as c


def test_pooled_contrast_pvalues_match_full_anova_linear_model():
    d = c.compute_contrasts()
    g = c.rng(1953)
    groups = [g.normal(50 + effect, 2, 6) for effect in d['eff']]
    X = np.repeat(np.eye(5), 6, axis=0)
    reference = sm.OLS(np.concatenate(groups), X).fit()
    for pair in d['pairs']:
        contrast = np.eye(5)[pair['j']] - np.eye(5)[pair['i']]
        assert pair['p_raw'] == pytest.approx(float(reference.t_test(contrast).pvalue))
    # SciPy's randomized multivariate-t integration must repeat exactly.
    assert c.compute_contrasts()['dunnett_p'] == d['dunnett_p']


def test_blocking_example_is_the_first_replicate_before_any_pvalue_selection():
    d = c.compute_blocking()
    g = c.rng(1857)
    allocation = np.column_stack([g.permutation(4) for _ in range(6)])
    field = c.D.Field(rows=4, cols=6, gradient=8, hump=0, noise=1.5, seed=1937)
    y = field.harvest(np.array([0., 2., 3., 1.5])[allocation], rng=g)
    assert np.array_equal(d['alloc'], allocation)
    assert np.allclose(d['y'], y)
    rows, columns = np.indices(y.shape)
    design = np.column_stack([np.ones(y.size)] +
        [(allocation.ravel() == j).astype(float) for j in range(1, 4)] +
        [(columns.ravel() == j).astype(float) for j in range(1, 6)])
    reference = sm.OLS(y.ravel(), design).fit()
    contrast = np.zeros((3, 9)); contrast[:, 1:4] = np.eye(3)
    assert d['rcbd']['p'] == pytest.approx(float(reference.f_test(contrast).pvalue))
    assert d['rcbd']['p'] > .05


def test_fractional_contrasts_are_finite_and_equal_alias_sums():
    X = c.D.full_factorial(4)
    keep = np.prod(X, axis=1) == 1
    # Known main effect A=4 and three-way BCD=2 become the same column.
    y = 60 + 2*X[:, 0] + np.prod(X[:, 1:], axis=1) + .75*X[:, 0]*X[:, 1]
    half = c.factorial_contrasts(X[keep], y[keep], 'ABCD')
    assert 'ABCD' not in half  # Constant defining word is not an estimable contrast.
    assert np.isfinite(list(half.values())).all()
    assert half['A'] == pytest.approx(6)
    assert half['BCD'] == pytest.approx(6)
    assert half['AB'] == pytest.approx(half['CD'])
    assert c.compute_fraction()['pb_orth']


def test_central_composite_design_has_five_levels_and_rotatable_variance():
    d = c.compute_rsm()
    points = (np.asarray(d['pts2']) - d['c1']) / d['step2']
    assert [len(np.unique(np.round(points[:, i], 10))) for i in range(2)] == [5, 5]
    u, v = points.T
    X = np.column_stack([np.ones(len(u)), u, v, u*u, v*v, u*v])
    inverse = np.linalg.inv(X.T @ X)
    for radius in (.5, 1, 1.5):
        variance = []
        for angle in np.linspace(0, 2*np.pi, 33):
            a, b = radius*np.array([np.cos(angle), np.sin(angle)])
            f = np.array([1, a, b, a*a, b*b, a*b])
            variance.append(f @ inverse @ f)
        assert np.ptp(variance) < 1e-12


def test_splitplot_wholeplot_test_matches_paired_block_comparison():
    y = c.splitplot_once(np.random.default_rng(400), blocks=9, a_eff=.8)
    block_differences = y.mean(axis=2)[:, 1] - y.mean(axis=2)[:, 0]
    reference = stats.ttest_1samp(block_differences, 0)
    actual = c.splitplot_tests(y)
    assert actual['F_right'] == pytest.approx(reference.statistic**2)
    assert actual['p_right'] == pytest.approx(reference.pvalue)
    assert actual['df_wp'] == 8


def test_quadratic_optimal_design_satisfies_equivalence_bound():
    d = c.compute_doptimal()
    xs = np.linspace(-1, 1, 2001)
    F = np.column_stack([np.ones(len(xs)), xs, xs*xs])
    supports = np.array([[1, -1, 1], [1, 0, 0], [1, 1, 1]])
    M = supports.T @ supports / 3
    assert np.linalg.det(M) == pytest.approx(4/27)
    variance = np.einsum('ij,jk,ik->i', F, np.linalg.inv(M), F)
    assert variance.max() == pytest.approx(3)
    assert variance[[0, 1000, 2000]] == pytest.approx(np.full(3, 3))
    assert d['dets']['thirds'] == pytest.approx(np.linalg.det(M))


def test_randomization_problem_exhaustive_sharp_null_and_complements():
    values = np.array([14, 16, 18, 10, 11, 15])
    deltas = [values[list(group)].mean() - np.delete(values, group).mean()
              for group in itertools.combinations(range(6), 3)]
    assert np.mean(np.abs(deltas) >= 4 - 1e-12) == pytest.approx(.2)
    assert sorted(deltas) == pytest.approx(sorted(-np.array(deltas)))
