import numpy as np

from explainer.stats.kit import learn as L


def test_one_se_rule_picks_simplest_within_one_se():
    best, simple = L.one_se_rule([5.0, 3.1, 3.0, 3.05], [0.2, 0.2, 0.2, 0.2])
    assert best == 2 and simple == 1


def test_knn_regression_and_classification():
    X = np.array([[0.0], [1.0], [2.0], [10.0]])
    y = np.array([0.0, 1.0, 2.0, 10.0])
    assert np.allclose(L.knn_predict(X, y, [[0.9]], 1), [1.0])
    assert np.allclose(L.knn_predict(X, y, [[0.9]], 3), [1.0])
    assert L.knn_predict(X, np.array([0, 0, 1, 1]), [[9.0]], 1, classify=True)[0] == 1


def test_cv_score_shape_and_mean():
    g = np.random.default_rng(0)
    X = g.normal(size=(100, 1))
    y = X[:, 0] + g.normal(0, 0.1, 100)
    res = L.cv_score(lambda a, b, c: L.knn_predict(a, b, c, 5), X, y, 10, g)
    assert res["folds"].shape == (10,) and 0 < res["mean"] < 0.1


def test_poisson_nb_log_odds_formula():
    counts = np.array([[10, 0], [8, 1], [1, 6], [0, 9]])
    lengths = np.array([1000, 1000, 1000, 1000])
    labels = np.array([0, 0, 1, 1])
    nb = L.PoissonNB().fit(counts, lengths, labels)
    lo = nb.log_odds([[0, 5]], [1000])[0]
    assert lo > 0 and nb.log_odds([[9, 0]], [1000])[0] < 0
    assert np.isclose(nb.contributions([0, 5], 1000).sum(), lo)


def test_logistic_ridge_matches_unpenalized_mle_and_shrinks():
    import statsmodels.api as sm

    g = np.random.default_rng(1)
    X = g.normal(size=(300, 2))
    y = (g.random(300) < 1 / (1 + np.exp(-(0.5 + X @ [1.0, -2.0])))).astype(float)
    b0 = L.logistic_ridge(X, y, 0.0)
    ref = sm.Logit(y, sm.add_constant(X)).fit(disp=0).params
    assert np.allclose(b0, ref, atol=1e-6)
    b1 = L.logistic_ridge(X, y, 50.0)
    assert np.linalg.norm(b1[1:]) < np.linalg.norm(b0[1:])


def test_tree_finds_the_step_and_prunes():
    x = np.linspace(0, 1, 200)
    y = np.where(x > 0.6, 3.0, 1.0)
    t = L.grow_tree(x[:, None], y, max_depth=3, min_leaf=5)
    assert abs(t.threshold - 0.6) < 0.01 and len(L.leaves(t)) == 2
    g = np.random.default_rng(2)
    t2 = L.grow_tree(x[:, None], y + g.normal(0, 0.3, 200), max_depth=5, min_leaf=5)
    small = L.prune_to(t2, 2)
    assert len(L.leaves(small)) == 2 and abs(small.threshold - 0.6) < 0.05
    path = L.prune_path(t2)
    alphas = [a for a, _ in path]
    assert path[-1][1] == 1 and all(a2 >= a1 - 1e-9 for a1, a2 in zip(alphas, alphas[1:]))


def test_ridge_closed_form_and_lasso_kkt():
    g = np.random.default_rng(3)
    X = g.normal(size=(80, 5))
    y = X @ [2.0, 0.0, -1.0, 0.0, 0.5] + g.normal(0, 0.5, 80)
    X = X - X.mean(0)
    y = y - y.mean()
    assert np.allclose(L.ridge(X, y, 0.0), np.linalg.lstsq(X, y, rcond=None)[0])
    lam = 0.2
    b = L.lasso(X, y, lam)
    grad = X.T @ (y - X @ b) / len(y)
    act = b != 0
    assert np.allclose(grad[act], lam * np.sign(b[act]), atol=1e-7)
    assert np.all(np.abs(grad[~act]) <= lam + 1e-7)
    path = L.lasso_path(X, y, [2.0, 0.5, 0.1])
    assert np.all(path[0] == 0) and np.count_nonzero(path[-1]) >= np.count_nonzero(path[1])


def test_metrics():
    c = L.confusion([1, 1, 0, 0], [1, 0, 1, 0])
    assert c["accuracy"] == 0.5 and c["precision"] == 0.5 and c["recall"] == 0.5
    assert L.auc([0.9, 0.8, 0.3, 0.1], [1, 1, 0, 0]) == 1.0
    p, r = L.pr_curve([0.9, 0.2, 0.8], [1, 0, 1])
    assert np.allclose(r[-1], 1.0) and np.isclose(p[1], 1.0)
