"""statkit.optim, checked against SciPy and closed forms."""

import numpy as np
import pytest
from scipy.optimize import linprog, minimize

from explainer.stats.kit import optim as O


def data(n=200, p=5, seed=0):
    g = np.random.default_rng(seed)
    X = g.normal(size=(n, p))
    beta = np.array([2.0, -1.5, 0, 0, 1.0][:p])
    return X, X @ beta + g.normal(size=n), g


def test_newton_quadratic_converges_in_one_step():
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    bvec = np.array([1.0, -1.0])
    r = O.newton(lambda x: 0.5 * x @ A @ x - bvec @ x, lambda x: A @ x - bvec, lambda x: A, [5.0, 5.0])
    assert np.allclose(r["path"][1], np.linalg.solve(A, bvec))


def test_newton_line_search_rescues_cauchy():
    g = np.random.default_rng(1)
    x = g.standard_cauchy(25) + 3.0
    f, gr, h = O.cauchy_location(x)
    best = minimize(lambda t: -f(t), [np.median(x)]).x[0]
    good = O.newton(f, gr, h, [np.median(x)], maximize=True)
    assert good["x"][0] == pytest.approx(best, abs=1e-6)
    ls = O.newton(f, gr, h, [np.median(x) + 6], maximize=True)
    assert np.all(np.diff(ls["values"]) >= -1e-9)  # with the line search the likelihood never falls


def test_logistic_scoring_matches_scipy():
    X, _, g = data()
    X = np.column_stack([np.ones(len(X)), X[:, :2]])
    y = (g.random(len(X)) < 1 / (1 + np.exp(-(X @ [0.3, 1.0, -0.5])))).astype(float)
    r = O.logistic_scoring(X, y)
    nll = lambda b: -np.sum(y * (X @ b) - np.logaddexp(0, X @ b))  # noqa: E731
    ref = minimize(nll, np.zeros(3), method="BFGS").x
    assert np.allclose(r["b"], ref, atol=1e-4)
    assert np.all(np.diff(r["loglik"]) >= -1e-9)


@pytest.mark.parametrize("tau", [0.5, 0.25, 0.9])
def test_quantile_mm_matches_the_lp(tau):
    X, y, _ = data(150, 3)
    X = np.column_stack([np.ones(150), X])
    lp = O.quantile_lp(X, y, tau)
    mm = O.quantile_mm(X, y, tau, iters=400, eps=1e-8)
    assert np.sum(O.check_loss(y - X @ mm["b"], tau)) == pytest.approx(lp["objective"], rel=1e-5)
    assert np.all(np.diff(mm["objective"]) <= 1e-6)
    assert len(lp["basic"]) >= X.shape[1]  # an LP solution interpolates p points


def test_simplex_matches_linprog():
    c = np.array([3.0, 2.0, 4.0])
    A = np.array([[1.0, 1.0, 2.0], [2.0, 0.0, 3.0], [2.0, 1.0, 3.0]])
    b = np.array([4.0, 5.0, 7.0])
    r = O.simplex(c, A, b)
    ref = linprog(-c, A_ub=A, b_ub=b, method="highs")
    assert r["value"] == pytest.approx(-ref.fun)
    assert np.all(A @ r["x"] <= b + 1e-9) and np.all(np.diff([c @ v for v in r["path"]]) >= -1e-12)


def test_neyman_pearson_lp_is_a_likelihood_ratio_test():
    from scipy.stats import binom

    k = np.arange(21)
    p0, p1 = binom.pmf(k, 20, 0.5), binom.pmf(k, 20, 0.7)
    r = O.neyman_pearson_lp(p0, p1, 0.05)
    assert r["size"] == pytest.approx(0.05, abs=1e-9)
    lr = p1 / p0
    rej = r["phi"] > 1 - 1e-9
    acc = r["phi"] < 1e-9
    assert lr[rej].min() >= lr[acc].max()  # reject exactly where the ratio is largest
    assert r["k"] == pytest.approx(lr[(~rej) & (~acc)][0], rel=1e-6)


def test_lasso_solvers_agree_and_the_gap_closes():
    X, y, _ = data(300, 5)
    lam = 0.2
    cd = O.cd_lasso(X, y, lam, sweeps=200)
    fi = O.ista(X, y, lam, iters=2000, accelerate=True)
    ad = O.admm_lasso(X, y, lam, iters=2000)
    assert np.allclose(cd["b"], fi["b"], atol=1e-5) and np.allclose(cd["b"], ad["b"], atol=1e-4)
    assert O.lasso_dual_gap(X, y, cd["b"], lam)["gap"] == pytest.approx(0, abs=1e-8)
    assert O.lasso_dual_gap(X, y, np.zeros(5), lam)["gap"] > 0.1
    # an ill-conditioned design, where acceleration matters
    g = np.random.default_rng(9)
    Z = g.normal(size=(300, 1)) + 0.05 * g.normal(size=(300, 6))
    yz = Z @ np.ones(6) + g.normal(size=300)
    best = O.cd_lasso(Z, yz, 0.05, sweeps=3000)["objective"][-1]
    ist = O.ista(Z, yz, 0.05, iters=200)
    fis = O.ista(Z, yz, 0.05, iters=200, accelerate=True)
    assert np.all(np.diff(ist["objective"]) <= 1e-12)
    assert fis["objective"][200] - best < ist["objective"][200] - best


def test_fused_lasso_limits():
    g = np.random.default_rng(3)
    y = np.r_[np.zeros(30), 3 * np.ones(30)] + g.normal(0, 0.5, 60)
    assert np.allclose(O.fused_lasso_admm(y, 0.0, iters=300)["b"], y, atol=1e-6)
    flat = O.fused_lasso_admm(y, 1e4, rho=50.0, iters=3000)["b"]
    assert np.allclose(flat, y.mean(), atol=1e-2)
    mid = O.fused_lasso_admm(y, 3.0, iters=2000)
    assert mid["primal_res"][-1] < 1e-5
    assert abs(mid["b"][:25].mean() - 0) < 0.6 and abs(mid["b"][35:].mean() - 3) < 0.6


def test_averaged_sgd_approaches_the_mle():
    g = np.random.default_rng(4)
    n = 40_000
    X = np.column_stack([np.ones(n), g.normal(size=n)])
    y = (g.random(n) < 1 / (1 + np.exp(-(X @ [-0.5, 1.0])))).astype(float)
    mle = O.logistic_scoring(X, y)["b"]
    s = O.sgd_logistic(X, y, step0=1.0, power=0.6)
    assert np.linalg.norm(s["avg"] - mle) < 0.03
    assert np.linalg.norm(s["avg"] - mle) < np.linalg.norm(s["b"] - mle)


def test_robbins_monro_median():
    x = np.random.default_rng(5).normal(2.0, 1.0, 20_000)
    assert O.robbins_monro_quantile(x, 0.5, step0=2.0)["theta"] == pytest.approx(2.0, abs=0.05)


def test_pava_against_brute_force_and_sklearn():
    g = np.random.default_rng(6)
    y = np.cumsum(g.normal(0.2, 1.0, 40))  + g.normal(0, 2, 40)
    r = O.pava(y)
    assert np.all(np.diff(r["fit"]) >= -1e-12)
    try:
        from sklearn.isotonic import IsotonicRegression
        assert np.allclose(r["fit"], IsotonicRegression().fit_transform(np.arange(40), y))
    except ImportError:
        pass
    # KKT: each pooled block's fit is the block mean
    for s, e in r["blocks"]:
        assert r["fit"][s] == pytest.approx(y[s:e + 1].mean())


def test_bradley_terry_mm_matches_direct_mle():
    wins = np.array([[0, 7, 8, 9], [3, 0, 6, 7], [2, 4, 0, 6], [1, 3, 4, 0]], float)
    r = O.bradley_terry_mm(wins, iters=500)
    assert np.all(np.diff(r["loglik"]) >= -1e-10)

    def nll(t):
        g = np.exp(np.r_[0.0, t])
        P = g[:, None] / (g[:, None] + g[None, :])
        return -np.sum(wins * np.log(P + (wins == 0)))

    t = minimize(nll, np.zeros(3), method="BFGS").x
    ref = np.exp(np.r_[0.0, t])
    assert np.allclose(r["g"] / r["g"][0], ref / ref[0], rtol=1e-4)
