"""statkit.amp (Part 59): the Sur-Candes system, ridge and ridgeless risk, AMP and its state evolution."""

import math

import numpy as np

from explainer.stats.kit import amp as M
from explainer.stats.kit import sparse as SP


def test_sur_candes_matches_the_paper():
    # Sur & Candes (2019): kappa = 0.1, gamma^2 = 5 gives (alpha, sigma, lambda) = (1.1678, 3.3466, 0.9605), factor 1.1660;
    # kappa = 0.2, gamma^2 = 5 gives alpha = 1.499, sigma = 4.744
    r = M.sur_candes(0.1, math.sqrt(5))
    assert abs(r["alpha"] - 1.1678) < 2e-4 and abs(r["sigma"] - 3.3466) < 2e-4 and abs(r["lam"] - 0.9605) < 2e-4
    assert abs(r["factor"] - 1.1660) < 2e-4
    r = M.sur_candes(0.2, math.sqrt(5))
    assert abs(r["alpha"] - 1.499) < 1e-3 and abs(r["sigma"] - 4.744) < 1e-3
    # the global null: alpha = 1 and the LRT factor exceeds one
    r0 = M.sur_candes(0.2, 0.0)
    assert r0["factor"] > 1


def test_lrt_inflation_by_simulation():
    rng = np.random.default_rng(3)
    n, p = 600, 120
    stats_ = []
    for _ in range(200):
        X = rng.standard_normal((n, p)) / math.sqrt(n)
        y = (rng.random(n) < 0.5).astype(float)
        stats_.append(M.lrt_one(X, y, 0)["llr2"])
    factor = M.sur_candes(p / n, 0.0)["factor"]
    assert abs(np.mean(stats_) - factor) < 0.3  # E[factor * chi2_1] = factor
    assert np.mean(stats_) > 1.05


def test_ridge_and_ridgeless():
    rng = np.random.default_rng(4)
    th = M.ridge_risk([0.2, 1.0], 0.5, 4.0)["risk"]
    sim = M.ridge_sim(400, 0.5, 4.0, [0.2, 1.0], 20, rng)
    assert np.all(np.abs(sim - th) / th < 0.08)
    for g in (0.5, 2.0):
        assert abs(M.ridge_sim(300, g, 4.0, [0.0], 20, rng)[0] - float(M.ridgeless_risk(g, 4.0))) / float(M.ridgeless_risk(g, 4.0)) < 0.12
    # the optimal penalty gamma/snr beats its neighbours
    lam = np.array([0.5, 1.0, 2.0]) * 0.5 / 4.0
    r = M.ridge_risk(lam, 0.5, 4.0)["risk"]
    assert r[1] <= r[0] and r[1] <= r[2]


def test_amp_state_evolution_and_phase_curve():
    rng = np.random.default_rng(5)
    n, p = 500, 1000
    x0 = np.zeros(p)
    idx = rng.choice(p, 100, replace=False)
    x0[idx] = rng.choice([-1.0, 1.0], 100)
    A = rng.standard_normal((n, p)) / math.sqrt(n)
    y = A @ x0 + 0.1 * rng.standard_normal(n)
    r = M.amp_lasso(A, y, 1.5, 30)
    se = M.state_evolution(0.5, 0.1, 0.01, 1.5, 30)
    assert abs(r["tau"][-1] ** 2 - se[-1]) / se[-1] < 0.15
    d = [0.2, 0.5, 0.8]
    assert np.allclose(M.minimax_threshold_curve(d), SP.phase_curve(d), atol=1e-5)
