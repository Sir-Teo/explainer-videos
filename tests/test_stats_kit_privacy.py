"""statkit.privacy (Part 63): mechanisms, accountants, trade-off curves, private inference, post-processing, DP-SGD,
membership attacks, fairness rates and multicalibration."""

import math

import numpy as np
from explainer.stats.kit import privacy as P


def test_gaussian_calibration_and_randomized_response():
    # the analytic sigma meets delta exactly, and needs less noise than the classic bound
    s = P.gaussian_sigma_analytic(1, 1.0, 1e-5)
    assert abs(P.gaussian_delta(s, 1, 1.0) - 1e-5) < 1e-9
    assert s < P.gaussian_sigma_classic(1, 1.0, 1e-5)
    # the exact delta falls with sigma
    assert P.gaussian_delta(2.0, 1, 1.0) > P.gaussian_delta(4.0, 1, 1.0)
    # randomized response is unbiased after debiasing
    rng = np.random.default_rng(1)
    x = (rng.random(200000) < 0.3).astype(int)
    assert abs(P.rr_debias(P.randomized_response(x, math.log(3), rng), math.log(3)) - 0.3) < 0.01


def test_accountants():
    # zCDP and RDP agree for Gaussians; both beat basic composition over many releases
    rho = 1000 * P.zcdp_gaussian(1, 5.0)
    assert abs(rho - 20) < 1e-12
    e_z, e_r = P.zcdp_to_dp(rho, 1e-5), P.rdp_gaussian_eps(1, 5.0, 1000, 1e-5)
    assert abs(e_z - e_r) / e_z < 0.01
    assert P.basic_composition(1.0, 1000)[0] == 1000
    # advanced composition beats basic for small per-step epsilon
    assert P.advanced_composition(0.01, 1000, 1e-5)[0] < 10
    assert abs(P.zcdp_to_dp(2.63, 1e-10) - (2.63 + 2 * math.sqrt(2.63 * math.log(1e10)))) < 1e-12


def test_tradeoff_curves():
    a = np.linspace(0.001, 0.999, 500)
    g = P.tradeoff_gaussian(a, 1.0)
    # mu = 0 is guessing; curves are decreasing and below the diagonal
    assert np.allclose(P.tradeoff_gaussian(a, 0.0), 1 - a, atol=1e-9)
    assert np.all(np.diff(g) <= 1e-12) and np.all(g <= 1 - a + 1e-12)
    # the Laplace mechanism is eps-DP: its curve lies on or above the eps-DP curve
    assert np.all(P.tradeoff_laplace(a, 1.0) >= P.tradeoff_eps_delta(a, 1.0) - 1e-9)
    # the Gaussian is not pure eps-DP: near alpha = 0 it dips below
    assert P.tradeoff_gaussian(np.array([1e-4]), 1.0)[0] < P.tradeoff_eps_delta(np.array([1e-4]), 1.0)[0]
    # a simulated membership attack on a Gaussian mean lands on G_mu
    rng = np.random.default_rng(2)
    m = P.membership_attack_roc(100, 0.01, 40000, rng)
    assert abs(m["mu"] - 1.0) < 1e-12
    k = (m["fpr"] > 0.02) & (m["fpr"] < 0.98)
    assert np.max(np.abs((1 - m["tpr"][k]) - P.tradeoff_gaussian(m["fpr"][k], 1.0))) < 0.02


def test_private_inference_and_cost():
    rng = np.random.default_rng(3)
    cov = {"naive": 0, "aware": 0}
    for _ in range(1500):
        x = (rng.random(300) < 0.3).astype(int)
        o = P.private_proportion(x, 0.1, rng)
        for k in cov:
            cov[k] += o[k][0] <= 0.3 <= o[k][1]
    assert cov["naive"] / 1500 < 0.85 and abs(cov["aware"] / 1500 - 0.95) < 0.025
    m = P.mean_mse_central_local(1000, 1.0, 3000, rng)
    assert abs(m["central"] - (0.21 / 1000 + 2 / 1000 ** 2)) < 2.5e-5
    assert m["local"] > 4 * m["central"]


def test_projection_and_dpsgd():
    noisy = np.array([-3.0, 1.0, 10.0, 20.0])
    c = P.nonneg_total_projection(noisy, 30.0)
    assert np.all(c >= 0) and abs(c.sum() - 30) < 1e-6
    # the KKT form of the least-squares projection: the positive counts are all shifted by one constant
    lam = (noisy - c)[c > 0]
    assert np.allclose(lam, lam[0])
    rng = np.random.default_rng(4)
    n = 600
    X = np.column_stack([np.ones(n), rng.standard_normal((n, 2))])
    y = (rng.random(n) < 1 / (1 + np.exp(-(X @ [0.2, 1.5, -1.0])))).astype(float)
    w_np = P.dp_logistic_gd(X, y, float("inf"), 100, 1.0, 2.0, rng)
    w_p = P.dp_logistic_gd(X, y, 0.001, 100, 1.0, 2.0, rng)
    assert w_np["sigma"] == 0 and w_p["sigma"] == math.sqrt(100 / 0.002)
    acc = lambda w: np.mean(((X @ w) > 0) == y)  # noqa: E731
    assert acc(w_np["w"]) > 0.7 and acc(w_np["w"]) >= acc(w_p["w"]) - 0.02


def test_fairness_identity_and_multicalibration():
    rng = np.random.default_rng(5)
    n = 20000
    grp = np.where(rng.random(n) < 0.5, "a", "b")
    risk = np.clip(rng.beta(2, 3, n) + np.where(grp == "a", 0.15, 0.0), 0, 1)
    y = (rng.random(n) < risk).astype(int)
    score = np.ceil(risk * 10).clip(1, 10)
    r = P.group_rates(score, y, grp, 5)
    for v in r.values():
        assert abs(P.chouldechova_fpr(v["base"], v["ppv"], v["fnr"]) - v["fpr"]) < 1e-12
    # a calibrated score with different base rates has unequal FPRs
    assert r["a"]["base"] > r["b"]["base"] and r["a"]["fpr"] > r["b"]["fpr"]
    # multicalibration repairs a model that ignores a subgroup
    g = [grp == "a", grp == "b"]
    pred = np.full(n, y.mean())
    mc = P.multicalibrate(pred, y, g, alpha=0.01, n_bins=5, min_n=100)
    assert mc["history"][-1] <= 0.01 < mc["history"][0]
    assert np.allclose(P.apply_patches(pred, g, mc["patches"], 5), mc["pred"])
    assert P.weighted_calibration_gap(mc["pred"], y, g) < P.weighted_calibration_gap(pred, y, g)
    assert P.max_calibration_gap(mc["pred"], y, g, n_bins=5, min_n=100) <= 0.01 + 1e-12
