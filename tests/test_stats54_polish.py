"""Independent checks for Part 54's corrected scientific computations."""
import itertools
import math
import ast
from pathlib import Path

import numpy as np
import pytest
from scipy.special import expit
from videos.stats.stats54 import checked as C
from explainer.stats.kit import slt as SL


def test_stump_never_splits_tied_features():
    rng = np.random.default_rng(540)
    for _ in range(30):
        X = rng.integers(0, 3, (18, 3)).astype(float)
        y = rng.choice([-1., 1.], len(X))
        weights = rng.random(len(y)); weights /= weights.sum()
        error, j, t, sign = C.best_stump(X, y, weights)
        brute = min(float(weights @ (SL.stump_predict(X, k, cut, s) != y))
                    for k in range(X.shape[1]) for cut in np.r_[-np.inf, np.unique(X[:, k])]
                    for s in (-1, 1))
        assert error == pytest.approx(brute, abs=1e-12)
        assert error == pytest.approx(weights @ (SL.stump_predict(X, j, t, sign) != y))


def test_adaboost_duplicate_weight_updates_match_exponential_loss():
    X = np.array([[0.], [0.], [1.], [1.], [2.], [2.]])
    y = np.array([-1., 1., -1., 1., 1., 1.])
    out = C.adaboost(X, y, 20, X, y)
    errors = np.array(out['weighted_errors'])
    assert np.all(errors <= .5 + 1e-12)
    assert np.allclose(out['alphas'], .5 * np.log((1 - errors) / errors))
    assert out['train'] == out['test']


@pytest.mark.parametrize('eta', [0., .1, .4])
def test_exact_threshold_supremum_includes_grouped_jump_limits(eta):
    x = np.array([0., .1234567, .1234567, .58, 1.])
    y = np.array([1, 0, 1, 1, 0])
    candidates = np.unique(np.r_[0., x, .5, 1.])
    values = []
    for t in candidates:
        values.append(abs(np.mean((x > t) != y) - SL.threshold_risk(t, eta=eta)))
        if t > 0:
            values.append(abs(np.mean((x >= t) != y) - SL.threshold_risk(t, eta=eta)))
    assert C.uniform_deviation_threshold(x, y, eta=eta) == pytest.approx(max(values))
    t = C.erm_threshold(x, y)
    assert np.mean((x > t) != y) == min(np.mean((x > t2) != y) for t2 in candidates)


def test_separator_all_triangle_patterns_and_square_xor():
    triangle = np.array([[0., 0.], [1., 0.], [.35, .0001]])
    for labels in itertools.product([0, 1], repeat=3):
        w, b = C.separator(triangle, labels)
        assert w is not None
        assert np.array_equal(triangle @ w > b, np.array(labels, bool))
        assert np.linalg.norm(w) == pytest.approx(1.)
    square = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    assert C.separator(square, [0, 1, 1, 0])[0] is None
    assert sum(C.separator(square, lab)[0] is not None for lab in itertools.product([0, 1], repeat=4)) == 14


@pytest.mark.parametrize('q', [0., .1, .8, 1.])
def test_bernoulli_kl_inverse_has_exact_support_endpoints(q):
    c = .08
    p = C.kl_inverse(q, c)
    if q < 1:
        assert C.kl_bernoulli(q, p) == pytest.approx(c, abs=1e-12)
    else:
        assert p == 1
    assert C.kl_bernoulli(q, q) == pytest.approx(0.)
    assert C.kl_bernoulli(0, 1) == np.inf
    assert C.kl_bernoulli(1, 0) == np.inf
    if q == 0: assert p == pytest.approx(1 - math.exp(-c))


def test_sgd_expected_bound_is_not_a_pathwise_bound():
    # A changed record selected immediately gives eta divergence, not eta/n.
    n, eta = 100, .5
    w = eta * expit(0)
    wp = -eta * expit(0)
    assert abs(w - wp) > 2 * eta / n
    X = np.array([[1., 0.], [0., 1.], [.5, .5]])
    y = np.array([1., -1., 1.])
    out = C.sgd_divergence(X, y, 50, .5, np.random.default_rng(54), reps=30)
    assert np.all(out['paths'] <= 2 * .5 * out['changed_visits'] + 1e-12)
    assert np.allclose(out['mcse'], np.std(out['paths'], axis=0, ddof=1) / math.sqrt(30))


@pytest.mark.parametrize('p', [5, 30])
def test_inverse_wishart_risk_agrees_with_independent_lstsq(p):
    rng = np.random.default_rng(545)
    n, P = 12, 40
    beta = np.ones(P) / math.sqrt(P)
    losses = []
    for _ in range(2000):
        X = rng.normal(size=(n, P))
        y = X @ beta + .5 * rng.normal(size=n)
        fit = np.linalg.lstsq(X[:, :p], y, rcond=None)[0]
        losses.append(np.sum((fit - beta[:p])**2) + np.sum(beta[p:]**2))
    assert abs(np.mean(losses) - C.expected_min_norm_risk(n, p, P)) < 5 * C.mcse(losses)
    assert all(np.isinf(C.expected_min_norm_risk(n, k, P)) for k in (n-1, n, n+1))


def test_benign_design_actually_interpolates_and_preserves_total_tail_variance():
    out = C.benign_risk(20, np.random.default_rng(3), p_tail=100, tail_var=.1, reps=3)
    assert max(out['train_mse']) < 1e-20
    assert out['tail_total_variance'] == 10
    assert out['tail_effective_rank'] == 100
    assert out['mcse'] == pytest.approx(C.mcse(out['samples']))


def test_logistic_psi_is_in_bits_and_matches_conditional_risk_gap():
    theta = np.array([0., .2, .8, 1.])
    eta = (1 + theta) / 2
    optimum = np.array([0. if e == 1 else -e * np.log2(e) - (1-e)*np.log2(1-e) for e in eta])
    assert np.allclose(SL.psi_transform(theta, 'logistic'), 1 - optimum)
    assert SL.psi_transform([1], 'logistic')[0] == 1


def test_hedge_bound_holds_for_adversarial_mixture_losses():
    T, K = 1000, 7
    L = np.random.default_rng(54).integers(0, 2, (T, K))
    eta = math.sqrt(8 * math.log(K) / T)
    regret = SL.hedge(L, eta)['regret']
    bound = math.log(K) / eta + eta * np.arange(1, T+1) / 8
    assert np.all(regret <= bound + 1e-10)


def test_scenes_board_call_and_static_tex_braces():
    for path in Path('videos/stats/stats54').glob('s*.py'):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'show_board':
                assert len(node.args) == 4
