"""Agora's many agents (Part 52): aggregation, Aiyagari's economy, Krusell and Smith, sequence-space Jacobians and a
one-asset HANK, Hopenhayn's industry."""

import numpy as np
import pytest

from explainer.economics.agora import hetero as H


def test_gorman():
    same = H.gorman_demand([10, 50, 90], [1, 2, 3], [0.6, 0.6, 0.6], 5.0, 2, 0)
    assert same["change"] == pytest.approx(0.0)
    diff = H.gorman_demand([10, 50, 90], [1, 2, 3], [0.9, 0.6, 0.3], 5.0, 2, 0)
    assert diff["change"] == pytest.approx((0.9 - 0.3) * 5.0)


def test_income_chain_mean_one():
    e, P, pi = H.income_chain(0.9, 0.2, 7)
    assert pi @ e == pytest.approx(1.0)
    assert np.allclose(P.sum(axis=1), 1.0)
    assert np.allclose(pi @ P, pi)


def test_young_step_preserves_mass():
    a = H.asset_grid(50, 0.0, 20.0)
    e, P, pi = H.income_chain(0.9, 0.2, 3)
    ap = np.clip(0.9 * a[:, None] + e[None, :], 0, 25.0)
    D = np.outer(np.full(50, 1 / 50), pi)
    Dn = H.young_step(D, ap, a, P)
    assert Dn.sum() == pytest.approx(1.0)
    assert (Dn >= 0).all()


@pytest.fixture(scope="module")
def aiy():
    return H.aiyagari(n_a=120, a_max=150.0, tol=1e-5)


def test_aiyagari_clears_and_saves_more(aiy):
    assert 0 < aiy["r"] < aiy["rho_time"]
    assert aiy["A"] == pytest.approx(aiy["K"], rel=2e-3)
    assert 0.2 < aiy["gini"] < 0.8
    assert aiy["top1"] < aiy["top10"] < 1
    rep = H.capital_demand(aiy["rho_time"])
    assert aiy["K"] > rep


def test_simulation_matches_histogram(aiy):
    sim = H.simulate(aiy, n=20000, T=300)
    assert sim["wealth"].mean() == pytest.approx(aiy["A"], rel=0.05)


def test_pareto_from_shares_exact():
    alpha = 1.5
    s = lambda p: p ** (1 - 1 / alpha)  # noqa: E731
    assert H.pareto_from_shares(s(0.01), s(0.10)) == pytest.approx(alpha)


def test_ks_chain_holds_unemployment():
    u = (0.10, 0.04)
    Pz, Pe = H.ks_chain(u)
    assert np.allclose(Pz.sum(axis=1), 1)
    for z in range(2):
        for zp in range(2):
            assert np.allclose(Pe[z, zp].sum(axis=1), 1)
            assert u[z] * Pe[z, zp, 0, 0] + (1 - u[z]) * Pe[z, zp, 1, 0] == pytest.approx(u[zp])


def test_krusell_smith_small():
    ks = H.krusell_smith(n_a=60, T=400, burn=50, max_rounds=40, tol=1e-5, inner_tol=1e-6)
    assert min(ks["r2"]) > 0.9999
    assert ks["dh_max"] < 2.0
    assert 0.9 < ks["b"][1][1] < 1.0


@pytest.fixture(scope="module")
def hank():
    ss = H.hank_steady_state(2.0, n_a=150)
    return ss, H.jacobians(ss, T=80)


def test_fake_news_matches_brute_force(hank):
    ss, jac = hank
    for inp, s in (("r", 0), ("r", 7), ("Z", 0), ("Z", 12)):
        b = H.jacobian_column_brute(ss, inp, s, T=80)
        for o in ("C", "A"):
            col = jac["J"][(o, inp)][:, s]
            assert np.max(np.abs(b[o] - col)) < 1e-3 * max(1.0, np.max(np.abs(col)))


def test_balanced_budget_multiplier_is_one(hank):
    ss, jac = hank
    m = H.hank_multiplier(ss, jac, financing="balanced")
    assert m["multiplier"] == pytest.approx(1.0, abs=1e-8)
    d = H.hank_multiplier(ss, jac, financing="deficit")
    assert d["multiplier"] > 1.0
    assert d["goods_residual"] < 1e-8


def test_rate_cut_adds_up(hank):
    ss, jac = hank
    rc = H.hank_rate_cut(ss, jac)
    assert rc["goods_residual"] < 1e-6
    assert np.allclose(rc["direct"] + rc["indirect"], rc["dC"])
    assert rc["dC"][0] > 0
    ra = H.ra_rate_cut(ss["r"], ss["B"], rc["dr"])
    assert ra["dC"][0] == pytest.approx(-rc["dr"].sum() / (1 + ss["r"]))
    assert ra["direct_share_impact"] > rc["direct_share_impact"]


def test_forward_guidance_matches_rate_cut(hank):
    ss, jac = hank
    fg = H.forward_guidance(ss, jac, [3, 10], -0.0025)
    for h, v in zip((3, 10), fg["ha"]):
        rc = H.hank_rate_cut(ss, jac, -0.0025, 0.0)
        dr = np.zeros(jac["T"])
        dr[h] = -0.0025
        dZ = -np.linalg.solve(jac["J"][("A", "Z")], jac["J"][("A", "r")] @ dr)
        dC0 = (jac["J"][("C", "r")] @ dr + jac["J"][("C", "Z")] @ dZ)[0]
        assert v == pytest.approx(dC0)
        assert rc["dr"][1] == pytest.approx(-0.0025)


def test_hopenhayn_entry_barrier():
    lo, hi = H.hopenhayn(c_e=40.0), H.hopenhayn(c_e=80.0)
    assert lo["entry_rate"] == pytest.approx(lo["exit_rate"])
    assert hi["p"] > lo["p"]
    assert hi["exit_rate"] < lo["exit_rate"]
    assert hi["productivity"] < lo["productivity"]
    assert np.all(np.diff(lo["survival"]) <= 1e-12)


def test_lumpy_plants_smooth_aggregate():
    L = H.lumpy_plants(n=5000, T=60, shock_at=40)
    assert np.mean(L["plants"][10:] == 0) > 0.5
    assert L["aggregate"][10:40].std() < 0.01
    assert L["aggregate"][40] > L["aggregate"][39]
