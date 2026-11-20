"""Agora's industrial organization (Part 43): demand, pricing, estimation, production and entry."""

import numpy as np
import pytest

from explainer.economics.agora import io


def test_cournot_margin_is_hhi_over_elasticity():
    a, b = 10.0, 1.0
    c = np.array([3.0, 4.0, 5.0])
    q = io.cournot_hetero(a, b, c)
    Q = q.sum()
    p = a - b * Q
    s = q / Q
    eps = p / (b * Q)
    assert np.allclose((p - c) / p, s / eps)
    assert np.sum(s * (p - c) / p) == pytest.approx(np.sum(s ** 2) / eps)


def test_nested_logit_reduces_to_logit():
    d = np.array([0.3, -0.2, 0.5, 0.1])
    assert np.allclose(io.nested_shares(d, [0, 0, 1, 1], 0.0), io.logit_shares(d))
    s = io.nested_shares(d, [0, 0, 1, 1], 0.7)
    assert 0 < s.sum() < 1


def test_rc_market_jacobian_matches_differences():
    rng = np.random.default_rng(1)
    mk = io.RCMarket(rng.normal(1, 0.5, 5), 1.2, 0.3, rng.standard_normal(200))
    p = np.full(5, 2.0)
    assert np.allclose(mk.jac(p), io.jacobian(mk.shares, p), atol=1e-7)


def test_bertrand_prices_satisfy_first_order_conditions():
    rng = np.random.default_rng(2)
    mk = io.RCMarket(rng.normal(1, 0.5, 6), 1.5, 0.3, rng.standard_normal(300))
    mc = np.full(6, 1.1)
    owner = np.array([0, 0, 1, 1, 2, 2])
    p = mk.bertrand(mc, owner)
    O = (owner[:, None] == owner[None, :]).astype(float)
    assert np.max(np.abs(mk.shares(p) + (O * mk.jac(p)) @ (p - mc))) < 1e-9
    assert np.allclose(io.costs_from_prices(mk.shares, p, owner), mc, atol=1e-6)


def test_merger_of_close_substitutes_raises_prices_more():
    q = np.array([0.8, 0.0, 1.0, -0.5, -0.5])
    mc = np.array([1.5, 1.2, 1.6, 1.0, 1.0])
    nests = np.array([0, 0, 1, 2, 2])

    def shares(p):
        return io.nested_shares(q - p, nests, 0.6)
    owner = np.arange(5)
    p0 = io.bertrand(shares, mc, owner)
    x = io.merger(shares, p0, owner, [3, 4])
    y = io.merger(shares, p0, owner, [0, 2])
    assert np.mean(np.array(x["dp"])[[3, 4]]) > 5 * np.mean(np.array(y["dp"])[[0, 2]])
    assert x["dhhi"] < y["dhhi"]


def test_cmcr_keeps_prices_unchanged():
    rng = np.random.default_rng(3)
    mk = io.RCMarket(rng.normal(1, 0.5, 4), 1.5, 0.3, rng.standard_normal(300))
    owner = np.arange(4)
    p = mk.bertrand(np.full(4, 1.2), owner)
    c = io.cmcr(mk.shares, p, owner, [0, 1])
    mc1 = io.costs_from_prices(mk.shares, p, owner) * (1 - c)
    new = np.array([0, 0, 2, 3])
    assert np.allclose(mk.bertrand(mc1, new, p0=p), p, atol=1e-6)


def test_contraction_recovers_mean_utilities():
    rng = np.random.default_rng(4)
    nu = rng.standard_normal(300)
    x = rng.uniform(1, 3, 6)
    delta = rng.normal(-1, 0.5, 6)
    s = io.rc_shares(delta, x, nu, 0.4)
    tr = io.contraction_trace(s, x, nu, 0.4, iters=200)
    assert np.allclose(tr["delta"], delta, atol=1e-9)
    assert tr["steps"][5] < tr["steps"][0]


def test_implied_margins_pick_out_the_true_conduct():
    rng = np.random.default_rng(5)
    mk = io.RCMarket(rng.normal(1, 0.5, 6), 1.6, 0.4, rng.standard_normal(300))
    mc = np.exp(rng.normal(np.log(1.2), 0.15, 6))
    owner = np.array([0, 0, 0, 1, 1, 2])
    p = mk.bertrand(mc, owner)
    im = io.implied_margins(mk.shares, p, {"single": np.arange(6), "actual": owner, "joint": np.zeros(6, int)})
    true = (p - mc) / p
    assert np.allclose(im["actual"], true, atol=1e-6)
    assert np.all(np.array(im["single"]) < np.array(im["actual"]) + 1e-12)
    assert np.all(np.array(im["joint"]) > np.array(im["actual"]))


def test_logit_markups_are_one_over_alpha_for_small_single_products():
    p = np.array([5.0, 10.0, 20.0])
    s = np.array([1e-4, 1e-4, 1e-4])
    L = io.logit_markups(0.2, p, s, [0, 0, 0], [0, 1, 2])
    assert np.allclose(L * p, 1 / (0.2 * (1 - s)))


def test_acf_recovers_production_elasticities():
    P = io.island_plants(n=800, T=8, sd_lerr=0.3, sd_eta=0.15, seed=7)
    r = io.acf(P)
    assert r["acf"]["bl"] == pytest.approx(0.6, abs=0.05)
    assert r["acf"]["bk"] == pytest.approx(0.3, abs=0.05)
    assert r["ols"]["bl"] > 0.75


def test_entry_thresholds_recovered_by_ordered_probit():
    m = (1.0, 0.6, 0.48, 0.46, 0.45)
    T = io.island_towns(n=800, sd=0.2, seed=11, margins=m)
    est = io.ordered_thresholds(T["pop"], T["n"], n_max=5)
    assert np.allclose(est["S"], T["thresholds"], rtol=0.15)
    assert est["ratio"][0] > 1.4 and abs(est["ratio"][-1] - 1) < 0.1
    assert io.entry_thresholds(4, mode="collusion")["ratio"] == pytest.approx([1.0, 1.0, 1.0])


def test_conduct_parallel_shifts_cannot_tell_rotation_can():
    C = io.conduct()
    for a, b in zip(C["A"], C["B"]):
        if a["z"] == 0.0:
            assert a["P"] == pytest.approx(b["P"]) and a["Q"] == pytest.approx(b["Q"])
        else:
            assert abs(a["P"] - b["P"]) > 0.1


def test_surplus_of_a_clone_vanishes_as_nests_tighten():
    d = np.array([0.5, 0.2, 0.1])
    nests = np.array([0, 1, 1])
    gain = [io.nested_surplus(np.r_[d, d[1]], np.r_[nests, 1], s, 1.0) - io.nested_surplus(d, nests, s, 1.0)
            for s in (0.0, 0.5, 0.99)]
    assert gain[0] == pytest.approx(io.logit_surplus(np.r_[d, d[1]], 1.0) - io.logit_surplus(d, 1.0))
    assert gain[0] > gain[1] > gain[2] > 0 and gain[2] < 0.01 * gain[0]
