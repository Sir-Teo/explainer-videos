"""Agora's insurance (Part 42): pooling, Baily-Chetty, the liquidity split, the weekly model, health insurance,
lotteries, examiners, defaults, the EITC, pensions and the MVPF."""

import numpy as np
import pytest

from explainer.economics.agora import insurance as I


def test_pooling_independent_falls_correlated_floors():
    r = I.pooling([10, 1000, 100000, 10 ** 7], p_low=0.03, p_high=0.09, q=0.15)
    ind, cor = np.array(r["independent"]), np.array(r["correlated"])
    assert ind[-1] < 0.002 and ind[0] / ind[1] == pytest.approx(10.0)
    assert cor[-1] == pytest.approx(r["floor"], rel=1e-3) and np.all(cor >= r["floor"])


def test_baily_chetty_holds_at_the_welfare_optimum():
    m = I.Baily(theta=0.3856, kappa=11.81)
    b = m.optimum()
    s = m.sides(b)
    assert s["gain"] == pytest.approx(s["cost"], rel=2e-3)
    # the budget balances
    assert (1 - s["e"]) * b == pytest.approx(s["e"] * s["tau"], rel=1e-8)
    # welfare is lower on either side
    assert m.solve(b)["welfare"] > m.solve(b - 0.05)["welfare"]
    assert m.solve(b)["welfare"] > m.solve(b + 0.05)["welfare"]
    # the MVPF of a little more is one at the optimum, above below it, below above it
    assert I.ui_mvpf(m, b) == pytest.approx(1.0, abs=2e-3)
    assert I.ui_mvpf(m, 0.2) > 1 > I.ui_mvpf(m, 0.5)


def test_liquidity_split_adds_up_and_matches_formula():
    m = I.Baily(theta=0.3856, kappa=11.81)
    sp = m.split(0.3)
    # de/db = de/dA - de/dw, and moral_hazard is -de/dw
    assert sp["de_db"] == pytest.approx(sp["liquidity"] + sp["moral_hazard"], rel=1e-4)
    assert sp["share"] == pytest.approx(sp["share_formula"], rel=1e-4)
    # higher risk aversion: a higher best benefit
    assert I.Baily(gamma=4.0, theta=0.3856, kappa=11.81).optimum() > m.optimum()


def test_weekly_model_hazard_rises_to_exhaustion():
    r = I.weekly(b=0.5, K=26, theta=240.0, kappa=0.5)
    h = np.array(r["hazard"])
    assert np.all(np.diff(h[:27]) >= -1e-12) and h[26] > 1.5 * h[0]
    assert np.all(h[26:] == h[26])
    el = I.weekly_elasticities(b=0.5, K=26, theta=240.0, kappa=0.5)
    assert 0.2 < el["level"] < 0.8 and el["length"] > 0
    # more generous benefits, longer spells
    assert I.weekly(b=0.6, theta=240.0, kappa=0.5)["duration"] > r["duration"]


def test_health_tradeoff_has_an_interior_optimum():
    h = I.Health(gamma=3.0, p_sick=0.7, median=0.05, sigma=1.3, cap=0.7, k=0.316)
    c = h.optimum()
    assert 0.05 < c < 0.9
    free, none = h.plan(0.0), h.plan(1.0)
    assert free["risk_premium"] == pytest.approx(0.0, abs=1e-12) and none["overuse"] == pytest.approx(0.0, abs=1e-12)
    assert h.plan(c)["ce"] > max(free["ce"], none["ce"])
    # RAND's ratio: the 95% plan spends 30% less than free care
    assert 1 - h.plan(0.95)["spending"] / free["spending"] == pytest.approx(0.30, abs=0.005)
    assert I.arc_elasticity(1000, 700, 0.25, 0.95) == pytest.approx(-0.3025, abs=1e-3)


def test_lottery_wald_is_unbiased_on_average():
    est = [I.lottery(n=30000, seed=s)["outcomes"]["ed_visits"]["wald"] for s in range(30)]
    assert np.mean(est) == pytest.approx(0.41, abs=0.06)
    r = I.lottery(n=30000, seed=1)
    assert 0.2 < r["first_stage"] < 0.32


def test_examiner_instrument_beats_the_naive_gap():
    X = I.examiners(seed=3)
    assert abs(X["iv"] - X["true_marginal"]) < 0.06
    assert X["naive"] < X["iv"] < 0


def test_defaults_and_eitc_and_payg_and_mvpf():
    D = I.defaults(seed=1)
    assert D["auto"][15] > D["opt_in"][15] + 0.3
    assert D["opt_in"][-1] > D["opt_in"][15] and D["auto"][-1] < D["auto"][15]
    cr = I.eitc([0, 10000, 17880, 23350, 61555, 80000], 0.45, 17880, 23350, 0.2106)
    assert cr[0] == 0 and cr[1] == pytest.approx(4500) and cr[2] == pytest.approx(8046)
    assert cr[3] == pytest.approx(8046) and cr[4] == pytest.approx(0, abs=1) and cr[5] == 0
    assert I.payg(workers_per_retiree=2.3)["replacement"] == pytest.approx(0.2852)
    p = I.payg()
    assert p["loss_share"] == pytest.approx(p["interest_on_debt"])
    assert I.mvpf(1.0, 1.0, -1.2) == float("inf") and I.mvpf(1.0, 1.0, 0.25) == pytest.approx(0.8)
    t = I.tagging(0.2, 0.7, 0.1)
    assert t["tagged"] == pytest.approx(0.14 / 0.22)


def test_basic_income_budget_and_laffer():
    rng = np.random.default_rng(0)
    x = np.exp(rng.normal(np.log(50000), 0.7, 5000))
    r = I.basic_income(x, 0.3)
    assert r["B"] == pytest.approx(0.3 * x.mean())
    assert r["gini_after"] < r["gini_before"]
    bs = [I.basic_income(x, t, e=0.25)["B"] for t in np.linspace(0.05, 0.95, 19)]
    assert int(np.argmax(bs)) == 15   # the peak at 1/(1 + e) = 80%
