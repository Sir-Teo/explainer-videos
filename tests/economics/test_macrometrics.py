"""Agora's macro-econometrics (Part 55): the Island's structural VAR and every scheme against its truth, local
projections, the New Keynesian model's solution, Kalman likelihood and estimation, impulse-response matching."""

import numpy as np
import pytest

from explainer.economics.agora import macrometrics as MM


def test_truth_long_run_and_signs():
    M = MM.island_svar()
    lr = M["C1"][0] @ M["B"]
    assert lr[0] > 0 and abs(lr[1]) < 1e-12 and abs(lr[2]) < 1e-12
    b = M["B"][:, 2]
    assert b[2] > 0 and b[0] < 0 and b[1] < 0
    comp = np.block([[M["A"][0], M["A"][1]], [np.eye(3), np.zeros((3, 3))]])
    assert np.abs(np.linalg.eigvals(comp)).max() < 1


def test_schemes_on_average():
    mc = MM.schemes_mc(reps=80, seed=11)
    tr = MM.svar_true_irf(16)
    for m in ("proxy", "hetero"):
        assert mc["methods"][m]["pi"]["mean"][0] == pytest.approx(tr["monetary"]["pi"][0], abs=0.05)
    assert mc["methods"]["recursive"]["pi"]["mean"][0] == pytest.approx(0.0, abs=1e-9)
    assert mc["methods"]["long_run"]["y"]["mean"][-1] == pytest.approx(tr["supply"]["y"][-1], abs=0.1)


def test_rotations_fit_equally():
    H = MM.svar_simulate(200, 3)
    fit = MM.var_fit(H["X"], 4)
    L = np.linalg.cholesky(fit["Sigma"])
    Q, _ = np.linalg.qr(np.random.default_rng(0).standard_normal((3, 3)))
    B = L @ Q
    assert np.allclose(B @ B.T, fit["Sigma"])


def test_sign_set_keeps_some():
    H = MM.svar_simulate(240, 5)
    fit = MM.var_fit(H["X"], 4)
    s = MM.sign_set(fit, 8, draws=500)
    assert 0 < s["accepted"] < s["tried"]
    assert all(v <= 1e-12 for v in s["pi"]["hi"][:3])


def test_lp_matches_var_in_large_samples():
    H = MM.svar_simulate(4000, 9)
    lp = np.cumsum(MM.lp_iv(H["X"], H["z"], 0, 8, lags=4))
    tr = np.array(MM.svar_true_irf(8)["monetary"]["y"])
    assert np.max(np.abs(lp - tr)) < 0.08


def test_nk_solution_satisfies_equations():
    p = MM.NK_DEFAULT
    G = MM.nk_solve(p)
    for j, rho in enumerate((p["rho_d"], p["rho_u"], p["rho_v"])):
        x, pi, i = G[:, j]
        unit = np.eye(3)[j]
        assert x == pytest.approx(rho * x - (i - rho * pi) / p["sigma"] + unit[0])
        assert pi == pytest.approx(p["beta"] * rho * pi + p["kappa"] * x + unit[1])
        assert i == pytest.approx(p["phi_pi"] * pi + p["phi_x"] * x + unit[2])


def test_kalman_likelihood_peaks_near_truth():
    D = MM.nk_simulate(T=200, seed=4)
    ll = [MM.nk_loglik({**MM.NK_DEFAULT, "kappa": k}, D["Y"]) for k in (0.05, 0.1, 0.2)]
    assert ll[1] > ll[0] and ll[1] > ll[2]


def test_irf_match_recovers_sigma():
    p = {**MM.NK_DEFAULT, "sd_v": 1.0}
    tr = MM.nk_irf(p, 12)
    tr = tr / tr[0, 2]
    m = MM.irf_match(tr, np.full_like(tr, 0.1), h=12, free=("kappa", "sigma"), start=(0.3, 0.8))
    assert m["estimate"]["sigma"] == pytest.approx(1.5, rel=1e-3)
    assert m["estimate"]["kappa"] == pytest.approx(0.1, rel=1e-3)
