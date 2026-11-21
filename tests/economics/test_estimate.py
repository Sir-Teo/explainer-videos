"""Agora's estimation harness (Part 54): maximum likelihood, GMM, simulated moments, indirect inference, sensitivity,
unobserved heterogeneity, validation and simulation-based inference, each checked against a known truth."""

import numpy as np
import pytest

from explainer.economics.agora import estimate as E


def test_logit_recovers_truth():
    d = E.simulate_commuters(4000, seed=1)
    r = E.logit_ml(d["X"], d["y"])
    truth = np.concatenate([d["beta"], d["asc"][1:]])
    assert np.all(np.abs(r["b"] - truth) < 3 * r["se"])
    shares = E.logit_shares(d["X"], r["b"], 2)
    assert shares.sum() == pytest.approx(1.0)
    assert shares[1] == pytest.approx(d["y"].mean(), abs=1e-6)


def test_gmm_euler_and_j():
    data = E.euler_data(T=3000, seed=2)
    r = E.gmm(E.euler_moments(data), [0.95, 2.0])
    assert abs(r["theta"][0] - 0.97) < 4 * r["se"][0] + 1e-3
    assert abs(r["theta"][1] - 3.0) < 4 * r["se"][1]
    assert r["df"] == 6
    assert r["p_J"] > 0.01


def test_gmm_linear_iv_matches_2sls():
    rng = np.random.default_rng(3)
    n = 2000
    z = rng.standard_normal((n, 2))
    u = rng.standard_normal(n)
    x = z @ np.array([1.0, 0.5]) + 0.5 * u + rng.standard_normal(n)
    y = 2.0 * x + u
    Z = np.column_stack([np.ones(n), z])
    X = np.column_stack([np.ones(n), x])

    def m(th):
        return Z * (y - X @ th)[:, None]

    r = E.gmm(m, [0.0, 0.0], two_step=False)
    P = Z @ np.linalg.solve(Z.T @ Z, Z.T)
    b2 = np.linalg.solve(X.T @ P @ X, X.T @ P @ y)
    # one-step GMM with W = I is not 2SLS, but both are consistent
    assert r["theta"][1] == pytest.approx(b2[1], abs=0.1)


def test_lifecycle_saves_for_retirement():
    sol = E.lifecycle(0.95, 2.0)
    m = E.lifecycle_moments(sol, n=1000, seed=1)
    wealth = m[10:]
    assert wealth.argmax() < len(wealth) - 1
    assert wealth.max() > 1.0


def test_sensitivity_inverts_jacobian():
    rng = np.random.default_rng(4)
    G = rng.standard_normal((5, 2))
    W = np.eye(5)
    L = E.sensitivity(G, W)
    assert np.allclose(L @ G, -np.eye(2))


def test_indirect_inference_ma1():
    y = E.ma1_data(0.5, 2000, 5)
    r = E.indirect_ma1(y)
    assert r["theta"] == pytest.approx(0.5, abs=0.08)


def test_mixture_logit_em():
    rng = np.random.default_rng(6)
    people, T = 600, 8
    types = rng.random(people) < 0.4
    alpha = np.where(types, -1.5, 1.0)
    g = np.repeat(np.arange(people), T)
    x = rng.standard_normal(people * T)
    p = 1 / (1 + np.exp(-(alpha[g] + 0.8 * x)))
    y = (rng.random(people * T) < p).astype(float)
    r = E.mixture_logit_em(x, y, T, g)
    assert r["alpha"][0] == pytest.approx(-1.5, abs=0.4)
    assert r["alpha"][1] == pytest.approx(1.0, abs=0.4)
    assert r["b"] == pytest.approx(0.8, abs=0.15)


def test_validation_passes_and_fails():
    ok = E.validate_subsidy(E.school_villages(seed=1))
    assert abs(ok["predicted_effect"] - ok["experimental_effect"]) < 3 * ok["experimental_se"]
    bad = E.validate_subsidy(E.school_villages(seed=1, label_effect=0.6))
    assert bad["experimental_effect"] - bad["predicted_effect"] > 3 * bad["experimental_se"]


def test_amortized_estimator():
    r = E.amortized_ma1(n=400, train=1500, test=200, seed=2)
    assert r["rmse"] < 0.1


def test_nested_logit_reduces_to_logit_and_sums_to_one():
    rng = np.random.default_rng(7)
    V = rng.standard_normal((50, 3))
    P1 = E.nested_shares(V, [[0], [1, 2]], [1.0, 1.0])
    L = np.exp(V) / np.exp(V).sum(axis=1, keepdims=True)
    assert np.allclose(P1, L)
    P2 = E.nested_shares(V, [[0], [1, 2]], [1.0, 0.4])
    assert np.allclose(P2.sum(axis=1), 1.0)
    # a correlated nest: the third alternative takes relatively more from the second than the plain logit says
    two = np.exp(V[:, :2]) / np.exp(V[:, :2]).sum(axis=1, keepdims=True)
    drop_logit = (two[:, 1] - L[:, 1]).mean() / (two[:, 0] - L[:, 0]).mean()
    drop_nested = (two[:, 1] - P2[:, 1]).mean() / (two[:, 0] - P2[:, 0]).mean()
    assert drop_nested > drop_logit


def test_logit_trace_and_loglik():
    d = E.simulate_commuters(1500, seed=3)
    r = E.logit_ml(d["X"], d["y"])
    assert np.allclose(r["trace"][-1], r["b"])
    assert E.logit_loglik(d["X"], d["y"], r["b"]) == pytest.approx(r["loglik"])
    assert E.logit_loglik(d["X"], d["y"], r["b"] * 0.9) < r["loglik"]


def test_mixture_with_two_covariates_removes_spurious_state_dependence():
    rng = np.random.default_rng(8)
    people, T = 800, 9
    low = rng.random(people) < 0.4
    alpha = np.where(low, -1.5, 1.0)
    g = np.repeat(np.arange(people), T)
    x = rng.standard_normal(people * T)
    y = (rng.random(people * T) < 1 / (1 + np.exp(-(alpha[g] + 0.8 * x)))).astype(float)
    lag = np.roll(y, 1)
    keep = np.tile(np.arange(T) > 0, people)
    pooled = E.pooled_logit(np.column_stack([x[keep], lag[keep]]), y[keep])
    assert pooled["b"][2] > 0.5
    mix = E.mixture_logit_em(np.column_stack([x[keep], lag[keep]]), y[keep], T - 1, g[keep])
    assert abs(mix["b"][1]) < 0.3


def test_sensitivity_sign_for_data_moments():
    # conditions written as model minus data: a rise dm in the data moves the estimate by -Lambda dm
    rng = np.random.default_rng(9)
    A = rng.standard_normal((6, 2))
    W = np.diag(rng.uniform(0.5, 2.0, 6))
    m = rng.standard_normal(6)

    def est(data):
        return np.linalg.solve(A.T @ W @ A, A.T @ W @ data)

    dm = 1e-3 * rng.standard_normal(6)
    L = E.sensitivity(A, W)
    assert np.allclose(est(m + dm) - est(m), -L @ dm)
