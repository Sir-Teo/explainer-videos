"""Agora's revenue manager (Part 60): pricing rules checked against their definitions and closed forms."""

import numpy as np
import pytest
from scipy import stats

from explainer.economics.agora import revenue as R


def test_markup_rule_and_flat_top():
    C = R.cost_plus_robustness()
    assert C["p_opt"] == pytest.approx(2.6 / 1.6)
    assert C["fixed"] == pytest.approx((0.5 * 1.5 ** -2.6) / (0.625 * 1.625 ** -2.6))
    assert C["fixed"] > C["rule_mean"] > C["rule_p10"]


def test_conjoint_recovers_planted_values():
    J = R.conjoint()
    for k in ("wifi", "legroom", "bag"):
        assert abs(J["wtp"][k] - J["truth"][k]) < 3 * J["wtp_se"][k]


def test_interference_inflates_ab_test():
    X = R.interference(reps=20)
    assert X["naive"] > 1.5 * X["global"]
    assert abs(X["cluster"] - X["global"]) < 3 * X["cluster_sd"]


def test_littlewood_rule_matches_exact_optimum():
    L = R.littlewood()
    assert L["y_star"] == L["y_best"]
    sf = stats.poisson.sf(np.arange(0, 101), 30)
    assert sf[L["y_star"]] <= L["ratio"] < sf[L["y_star"] - 1]


def test_emsr_b_nested():
    p = R.emsr_b()["protect"]
    assert p[0] < p[1] < p[2]


def test_overbooking_marginal_rule():
    O = R.overbooking()
    b = O["best"]
    assert stats.binom.sf(99, b - 1, 0.9) <= 200 / 600 < stats.binom.sf(99, b, 0.9)


def test_dynamic_programme_beats_fixed_price_and_one_seat_rule():
    F = R.flight()
    D = R.dp_prices(F, grid=np.arange(40.0, 501.0, 10.0))
    assert D["V0"] > D["fixed"]["best"]
    # with one seat left on the last day the fare maximizes p P(at least one buyer) = p (1 - exp(-lambda e^(-p/mu)))
    g = np.arange(40.0, 501.0, 10.0)
    best = g[np.argmax(g * (1 - np.exp(-F["lam"][-1] * np.exp(-g / F["mu"][-1]))))]
    assert D["policy"][-1, 1] == best


def test_menu_distorts_below_the_top():
    M = R.menu()
    assert M["q"][-1] == pytest.approx(M["thetas"][-1])
    assert M["q"][0] < M["thetas"][0]
    assert M["profit_one"] < M["profit"] < M["profit_full_info"]


def test_mfn_forces_one_price():
    m = R.mfn()
    assert m["p_sep"] == [60.0, 40.0]
    assert m["p_one"] == pytest.approx(50.0)
    assert m["profit_one"] < m["profit_sep"]


def test_big_bundles_approach_mean_value():
    B = R.big_bundle(ns=(1, 100), consumers=8000)
    r1, r100 = (r["revenue_per_good"] for r in B["rows"])
    assert r1 == pytest.approx(0.25, abs=0.01)
    assert 0.4 < r100 < 0.5


def test_hilo_needs_a_taste_for_deals():
    assert R.hilo(eta=0.0)["revenue_hilo"] < R.hilo(eta=0.0)["revenue_edlp"]
    assert R.hilo(eta=0.8)["revenue_hilo"] > R.hilo(eta=0.8)["revenue_edlp"]


def test_chain_uniform_price_between_store_prices():
    Ch = R.chain()
    assert min(Ch["p_store"]) < Ch["uniform"] < max(Ch["p_store"])
    assert 0 < Ch["loss"] < 0.05


def test_passthrough_lags_recovers_planted_coefficients():
    rng = np.random.default_rng(0)
    q = np.exp(np.cumsum(rng.normal(0, 0.01, 400)))
    dq = np.diff(np.log(q))
    b = 0.05 * np.ones(13)
    dr = np.r_[np.zeros(12), [sum(b[k] * dq[t - k] for k in range(13)) for t in range(12, len(dq))]]
    dr = dr + rng.normal(0, 0.0005, len(dr))
    r = np.exp(np.r_[0.0, np.cumsum(dr)])
    P = R.passthrough_lags(r, q)
    assert P["cum"][-1] == pytest.approx(0.65, abs=0.05)


def test_thompson_sampling_beats_test_then_commit_eventually():
    B = R.bandit_pricing(horizon=20000, test=1200, reps=8)
    assert B["ts_regret"][-1] < B["tc_regret"][-1]
