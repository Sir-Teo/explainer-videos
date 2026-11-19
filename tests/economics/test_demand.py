"""Agora's demand systems (explainer.economics.agora.demand): duality, Slutsky, Giffen, welfare, indices, AIDS."""

import numpy as np
import pytest

from explainer.economics.agora import demand as dm
from explainer.economics.island import truths

P3 = np.array([2.0, 3.0, 1.5])
SYSTEMS = [dm.CobbDouglas((0.5, 0.3, 0.2)), dm.CES((0.5, 0.3, 0.2), 0.5), dm.CES((0.5, 0.3, 0.2), 2.5),
           dm.StoneGeary((0.3, 0.5, 0.2), (5.0, 2.0, 1.0)), dm.AIDS(alpha0=np.log(100.0))]


@pytest.mark.parametrize("sys", SYSTEMS, ids=lambda s: type(s).__name__)
def test_duality_identities(sys):
    errs = dm.duality_errors(sys, P3, 100.0)
    assert max(errs.values()) < 1e-7, errs


@pytest.mark.parametrize("sys", SYSTEMS, ids=lambda s: type(s).__name__)
def test_slutsky_matrix_symmetric_nsd(sys):
    rep = dm.slutsky_report(dm.slutsky_matrix(sys, P3, 100.0), P3)
    assert rep["asymmetry"] < 1e-6 and rep["nsd"] and rep["Sp"] < 1e-6


@pytest.mark.parametrize("sys", SYSTEMS, ids=lambda s: type(s).__name__)
def test_budget_adds_up_and_homogeneity(sys):
    x = sys.x(P3, 100.0)
    assert abs(P3 @ x - 100.0) < 1e-9
    assert np.allclose(sys.x(2 * P3, 200.0), x)


def test_slutsky_elasticity_form():
    el = dm.elasticities(dm.StoneGeary((0.3, 0.7), (4.0, 1.0)), np.array([2.0, 5.0]), 60.0)
    E, H, eta, w = el["marshall"], el["hicks"], el["income"], el["shares"]
    assert np.allclose(E, H - np.outer(eta, w))
    assert abs(w @ eta - 1) < 1e-6                                  # Engel aggregation
    assert np.allclose(E.sum(1) + eta, 0, atol=1e-6)                # homogeneity
    assert np.allclose(w @ E, -w, atol=1e-6)                        # Cournot aggregation


def test_decompositions_for_bo():
    bo = dm.CobbDouglas((0.6, 0.4))
    hk = dm.decompose(bo, 0, [10.0, 6.0], [6.0, 6.0], 60.0, "hicks")
    sl = dm.decompose(bo, 0, [10.0, 6.0], [6.0, 6.0], 60.0, "slutsky")
    assert np.allclose(hk["A"], [3.6, 4.0]) and np.allclose(hk["C"], [6.0, 4.0])
    assert abs(hk["m_comp"] - 44.1613) < 1e-3 and abs(sl["m_comp"] - 45.6) < 1e-12
    assert abs(hk["substitution"] - 0.8161) < 1e-3 and abs(sl["substitution"] - 0.96) < 1e-12
    assert hk["substitution"] + hk["income"] == pytest.approx(2.4)
    # Hicks's compensated bundle lies on the old indifference curve
    assert bo.v([6.0, 6.0], hk["m_comp"]) == pytest.approx(bo.v([10.0, 6.0], 60.0))


def test_diet_zones_and_giffen():
    d = dm.Diet()
    lo, hi = d.zone_bounds(1.2, 2.0)
    assert d.choose(1.2, 2.0, lo - 0.5)["zone"] == "deprived"
    assert d.choose(1.2, 2.0, (lo + hi) / 2)["zone"] == "subsistence"
    assert d.choose(1.2, 2.0, hi + 0.5)["zone"] == "standard"
    # the Play-it bundles: on both constraints
    for p, (f, s) in ((1.2, (6.4286, 6.7857)), (1.5, (4.8, 7.6))):
        b = d.choose(p, 2.0, 21.0)
        assert b["zone"] == "subsistence" and abs(b["f"] - f) < 1e-3 and abs(b["s"] - s) < 1e-3
        assert abs(p * b["s"] + 2 * b["f"] - 21) < 1e-9 and abs(d.calories(b["s"], b["f"]) - 14000) < 1e-6
    assert d.elasticity(1.2, 2.0, 21.0) == pytest.approx(d.giffen_elasticity(1.2, 2.0), rel=1e-5)
    assert d.giffen_elasticity(1.2, 2.0) == pytest.approx(0.3 / 0.7)
    assert d.elasticity(1.2, 2.0, lo - 1) == pytest.approx(-1.0, abs=1e-6)
    assert d.elasticity(1.2, 2.0, hi + 5) < 0


def test_voucher_experiment_finds_the_giffen_group():
    T = truths(6)
    dd, v = T["diet"], T["vouchers"]
    diet = dm.Diet(dd["coconut_kcal"], dd["fish_kcal"], dd["need"], dd["beta"], dd["s0"], dd["other_share"],
                   dd["other_kcal"])
    ex = dm.voucher_experiment(diet, v["households"], v["villages"], v["cuts"], v["coconut"], v["fish"], v["median"],
                               v["sigma"], v["need_sd"], v["report_sd"], v["income_sd"], v["seed"])
    sh = ex["share0"]
    full = dm.fe_regression(ex["dS"], ex["dP"], ex["cell"], ex["hh"])
    k = (sh >= 0.6) & (sh <= 0.8)
    mid = dm.fe_regression(ex["dS"][k], ex["dP"][k], ex["cell"][k], ex["hh"][k])
    assert abs(full["b"]) < 2 * full["se"]
    assert mid["b"] - 2 * mid["se"] > 0
    assert set(np.unique(ex["zone"])) == {"standard", "subsistence", "deprived"}


def test_arc_percent_and_fe_regression():
    assert dm.arc_pct(1.0, 3.0) == pytest.approx(100.0)
    rng = np.random.default_rng(1)
    cell = np.repeat(np.arange(20), 50)
    x = rng.normal(size=1000)
    y = 0.7 * x + cell * 3.0 + rng.normal(0, 0.1, 1000)
    r = dm.fe_regression(y, x, cell, np.arange(1000))
    assert abs(r["b"] - 0.7) < 0.02


def test_loop_income_and_greens_theorem():
    path = dm.circle_path((0.1, -0.1), 0.3)
    sym = dm.AIDS(alpha=(0.4, 0.35, 0.25), beta=(0, 0, 0),
                  gamma=((-0.1, 0.05, 0.05), (0.05, -0.1, 0.05), (0.05, 0.05, -0.1)))
    circ = dm.AIDS(alpha=(0.4, 0.35, 0.25), beta=(0, 0, 0),
                   gamma=((-0.1, 0.08, 0.02), (0.02, -0.1, 0.08), (0.08, 0.02, -0.1)))
    assert abs(dm.loop_income(sym.shares, path)[-1]) < 1e-10
    assert dm.loop_income(circ.shares, path)[-1] == pytest.approx((0.02 - 0.08) * np.pi * 0.09, rel=1e-4)
    assert dm.slutsky_report(dm.slutsky_matrix(circ, np.ones(3), 100.0), np.ones(3))["asymmetry"] > 0.1


def test_welfare_orderings_and_hausman():
    bo = dm.CobbDouglas((0.6, 0.4))
    cv = dm.cv(bo, [10, 6], [6, 6], 60)
    ev = dm.ev(bo, [10, 6], [6, 6], 60)
    cs = dm.cs(bo, 0, [10, 6], [6, 6], 60)
    assert ev < cs < cv < 0             # a gain: |CV| < |CS| < |EV|
    assert cs == pytest.approx(-36 * np.log(10 / 6), rel=1e-6)
    L = dm.LinearDemand(-4.0, 0.1, 6.0)
    k = L.k(1.2, 60.0)
    assert L.e(1.2, k) == pytest.approx(60.0)
    # Roy's identity along the expenditure function: de/dp = h
    dp = 1e-6
    assert (L.e(1.5 + dp, k) - L.e(1.5 - dp, k)) / (2 * dp) == pytest.approx(L.h(1.5, k), rel=1e-6)
    r = L.tax(1.2, 0.6, 60.0)
    assert r["ev"] < r["cs"] < r["cv"]
    assert r["cs"] == pytest.approx(3.6) and r["dwl_marshall"] == pytest.approx(0.72)
    assert r["dwl_exact"] == pytest.approx(0.6146, abs=1e-3)
    assert dm.willig_gap(L.delta * 60 / 7.2, r["cs"], 60.0) == pytest.approx(0.025)


def test_price_indices_bound_the_coli():
    for sys in (dm.CobbDouglas((0.6, 0.4)), dm.CES((0.6, 0.4), 0.3), dm.CES((0.6, 0.4), 3.0)):
        p0, p1, m = np.array([10.0, 6.0]), np.array([6.0, 6.0]), 60.0
        u0, u1 = sys.v(p0, m), sys.v(p1, m)
        assert dm.paasche(p0, p1, sys.x(p1, m)) <= dm.coli(sys, p0, p1, u1) + 1e-12
        assert dm.coli(sys, p0, p1, u0) <= dm.laspeyres(p0, p1, sys.x(p0, m)) + 1e-12
    assert dm.feenstra(1.0, 0.95, 4.0) == pytest.approx(0.95 ** (1 / 3))
    assert dm.virtual_price(-2.0, 14.28) == pytest.approx(7.14)


def test_working_leser_and_hamilton():
    rng = np.random.default_rng(3)
    m = np.exp(rng.normal(np.log(300), 0.5, 5000))
    w = 0.9 - 0.1 * np.log(m) + rng.normal(0, 0.02, 5000)
    wl = dm.working_leser(w, m)
    assert abs(wl["b"] + 0.1) < 0.003 and wl["eta_at"](0.4) == pytest.approx(1 + wl["b"] / 0.4)
    years, Ws, Ms, Ys, Rs = (0, 5, 10), [], [], [], []
    for t in years:
        lrel = rng.normal(0, 0.08, 10)[np.arange(3000) % 10]
        ly = np.log(300) + 0.02 * t + 0.5 * rng.standard_normal(3000)
        Ws.append(0.6 - 0.1 * (ly - np.log(300)) + 0.05 * lrel + rng.normal(0, 0.03, 3000))
        Ms.append(np.exp(ly - 0.015 * t) / 300)
        Ys.append(np.full(3000, t))
        Rs.append(lrel)
    fit = dm.hamilton_drift(*map(np.concatenate, (Ws, Ms, Ys, Rs)))
    assert np.allclose(fit["cumulative_bias"], [0, 0.075, 0.15], atol=0.02)


def test_aids_fit_recovers_and_tests():
    s = truths(6)["survey"]
    truth = dm.AIDS(alpha=s["alpha"], beta=s["beta"], gamma=s["gamma"], alpha0=np.log(s["median"]))
    d = dm.Survey(truth, s["villages"], s["months"], s["per_cell"], s["price_sd"], s["median"], s["m_sigma"],
                  s["share_sd"], s["seed"]).draw()
    f = dm.aids_fit(d["W"], d["logP"], d["logm"], "symmetry", alpha0=np.log(s["median"]))
    assert np.allclose(f["gamma"], np.array(s["gamma"]), atol=0.01)
    assert np.allclose(f["beta"], s["beta"], atol=0.005)
    assert np.allclose(f["gamma"], f["gamma"].T)
    assert f["tests"]["homogeneity"]["p"] > 0.01 and f["tests"]["symmetry"]["p"] > 0.01
    # tastes with an asymmetric gamma are rejected
    bad = dm.AIDS(alpha=s["alpha"], beta=s["beta"],
                  gamma=((-0.06, 0.08, -0.02), (0.00, -0.04, 0.04), (0.06, -0.04, -0.02)), alpha0=np.log(s["median"]))
    d2 = dm.Survey(bad, 20, 12, 25, 0.15, s["median"], 0.5, 0.03, 7).draw()
    f2 = dm.aids_fit(d2["W"], d2["logP"], d2["logm"], "none", alpha0=np.log(s["median"]))
    assert f2["tests"]["symmetry"]["p"] < 1e-6
