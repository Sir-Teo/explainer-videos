"""Agora's dynamic programming and real business cycle (Part 29): the cake and its contraction, Markov chains, the
trend filters, Brock and Mirman's closed form, the RBC model's linear solution, and the long-run VAR."""

import numpy as np
import pytest

from explainer.economics.agora import dp, rbc


def test_cake_contracts_at_beta_and_eats_one_minus_beta():
    r = dp.cake(beta=0.9, n=501, iters=400)
    g = np.array(r["gaps"])
    assert np.allclose(g[5:60] / g[4:59], 0.9, atol=1e-9)
    assert g[-1] < 1e-10
    w, c = np.array(r["w"]), np.array(r["c"])
    share = np.median((c / w)[len(w) // 5:])
    assert share == pytest.approx(0.1, abs=0.01)
    # finite-horizon iterates fall as the horizon lengthens
    assert np.all(np.array(r["kept"]["5"]) <= np.array(r["kept"]["2"]) + 1e-12)


def test_rouwenhorst_is_exact_and_tauchen_is_not_for_persistent_shocks():
    for rho in (0.5, 0.95, 0.995):
        ch = dp.rouwenhorst(7, rho, 0.01)
        m = dp.chain_moments(ch["z"], ch["P"])
        assert m["sd"] == pytest.approx(0.01 / np.sqrt(1 - rho ** 2), rel=1e-8)
        assert m["rho"] == pytest.approx(rho, abs=1e-8)
        assert np.allclose(np.array(ch["P"]).sum(axis=1), 1)
    t = dp.tauchen(7, 0.95, 0.007)
    assert dp.chain_moments(t["z"], t["P"])["sd"] > 1.1 * 0.007 / np.sqrt(1 - 0.95 ** 2)
    stuck = dp.tauchen(7, 0.995, 0.007)
    assert np.min(np.diag(np.array(stuck["P"]))) > 0.9999


def test_hp_leaves_a_line_alone_and_hamilton_drops_the_start():
    t = np.arange(120.0)
    line = 3 + 0.02 * t
    assert np.allclose(dp.hp_filter(line)["cycle"], 0, atol=1e-8)
    rng = np.random.default_rng(0)
    y = np.cumsum(rng.standard_normal(200))
    h = dp.hamilton_filter(y, h=8, p=4)
    assert len(h["cycle"]) == 200 - 8 - 3 and h["start"] == 11
    assert abs(np.mean(h["cycle"])) < 1e-8


def test_brock_mirman_on_a_grid_matches_the_formula():
    bm = rbc.brock_mirman(T=50)
    assert bm["saving_rate"] == pytest.approx(0.36 * 0.96)
    k, y = np.array(bm["k"]), np.array(bm["y"])
    assert np.allclose(k[1:], 0.36 * 0.96 * y[:-1])
    g = rbc.growth_vfi(delta=1.0, nk=101, nz=5)
    kk, zz = np.array(g["k"]), np.array(g["z"])
    exact = 0.36 * 0.96 * zz[:, None] * kk[None, :] ** 0.36
    step = kk[1] - kk[0]
    assert np.max(np.abs(np.array(g["kprime"]) - exact)) <= step


def test_rbc_steady_state_roots_and_linear_solution():
    m = rbc.RBC()
    sol = m.solve()
    assert sol["bk_ok"] and sol["n_stable"] == 2
    assert sol["moduli"][1] == pytest.approx(0.95, abs=1e-6)          # technology's own root
    assert sol["moduli"][2] > 1
    # the Euler equation holds in the steady state
    r = m.alpha * m.y_ss / m.k_ss + 1 - m.delta
    assert m.beta * r == pytest.approx(1.0)
    # the policy solves the linear system: A [s'; F s'] = B [s; F s] with E z' = rho z
    A, B = m.linear_system()
    rng = np.random.default_rng(1)
    for _ in range(5):
        s = rng.standard_normal(2) * 0.01
        x = np.array([s[0], s[1], (m.F @ s)[0]])
        sn = m.P @ s
        xn = np.array([sn[0], sn[1], (m.F @ sn)[0]])
        assert np.allclose(A @ xn, B @ x, atol=1e-10)


def test_rbc_responses_and_moments():
    m = rbc.RBC()
    m.solve()
    irf = m.irf(20, 0.01)
    assert irf["i"][0] > irf["y"][0] > irf["n"][0] > irf["c"][0] > 0
    assert np.allclose(irf["w"], irf["c"])                            # with log c - A n, the wage is A c
    mo = rbc.moments(m.simulate(4000, 3))
    assert mo["y"]["rel"] == pytest.approx(1.0)
    assert mo["i"]["rel"] > 2 and mo["c"]["rel"] < 0.5
    # a smaller Frisch elasticity means smaller swings in hours
    rel = []
    for f in (0.5, 2.0, None):
        mm = rbc.RBC(frisch=f)
        mm.solve()
        rel.append(rbc.moments(mm.simulate(4000, 3))["n"]["rel"])
    assert rel[0] < rel[1] < rel[2]


def test_long_run_restriction():
    rng = np.random.default_rng(2)
    A = [np.array([[0.3, 0.1], [0.05, 0.5]])]
    S = np.array([[1.0, 0.3], [0.3, 0.8]])
    B0 = rbc.long_run_impact(A, S)
    assert np.allclose(B0 @ B0.T, S)
    C1 = np.linalg.inv(np.eye(2) - A[0])
    assert abs((C1 @ B0)[0, 1]) < 1e-10                               # only shock 1 moves variable 1 in the long run
    # a VAR fitted to its own simulated data recovers the coefficients
    T = 4000
    X = np.zeros((T, 2))
    L = np.linalg.cholesky(S)
    for t in range(1, T):
        X[t] = A[0] @ X[t - 1] + L @ rng.standard_normal(2)
    fit = rbc.var_ols(X, p=1)
    assert np.allclose(fit["A"][0], A[0], atol=0.05)
