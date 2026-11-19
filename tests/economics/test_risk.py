"""Agora's time and risk (explainer.economics.agora.risk)."""

import numpy as np
import pytest

from explainer.economics.agora import risk as rk


def test_certainty_equivalents_and_premia():
    x, p = [50.0, 150.0], [0.5, 0.5]
    assert rk.certainty_equivalent(x, p) == pytest.approx(100.0)
    assert rk.certainty_equivalent(x, p, gamma=1.0) == pytest.approx(np.sqrt(50 * 150))
    assert 0 < rk.risk_premium(x, p, gamma=2.0) and rk.risk_premium(x, p, gamma=2.0) > rk.risk_premium(x, p, gamma=1.0)
    assert rk.certainty_equivalent(x, p, a=0.01) < 100.0


def test_arrow_pratt():
    ap = rk.arrow_pratt(lambda w: rk.crra(w, 3.0), 50.0)
    assert ap["relative"] == pytest.approx(3.0, rel=1e-4) and ap["absolute"] == pytest.approx(3.0 / 50, rel=1e-4)
    ap = rk.arrow_pratt(lambda w: rk.cara(w, 0.2), 10.0)
    assert ap["absolute"] == pytest.approx(0.2, rel=1e-4)


def test_stochastic_dominance():
    assert rk.fosd([1, 2], [0.5, 0.5], [0, 2], [0.5, 0.5])
    assert not rk.fosd([0, 2], [0.5, 0.5], [1, 2], [0.5, 0.5])
    assert rk.sosd([1], [1.0], [0, 2], [0.5, 0.5])          # the mean for sure beats a spread around it
    assert not rk.fosd([1], [1.0], [0, 2], [0.5, 0.5])


def test_allais_and_triangle():
    assert rk.allais_eu_consistent(True, True) and not rk.allais_eu_consistent(True, False)
    ev = {k: np.dot(*v) for k, v in rk.ALLAIS.items()}
    assert ev["1B"] - ev["1A"] == pytest.approx(ev["2B"] - ev["2A"])       # the same common-consequence shift
    assert rk.eu_slope(0.0, 1.0, 2.0) == pytest.approx(1.0)
    assert rk.eu_slope(0.0, 1.5, 2.0) > rk.eu_slope(0.0, 1.0, 2.0)          # more concave, steeper


def test_st_petersburg():
    assert rk.stpetersburg_value(30) == pytest.approx(30.0)
    # Bernoulli's log utility: the classic prices for wealth $1,000 and $1,000,000
    assert rk.stpetersburg_price(1000.0, "log") == pytest.approx(10.95, abs=0.01)
    assert rk.stpetersburg_price(1e6, "log") == pytest.approx(20.87, abs=0.01)
    # Cramer's square root: prizes 1, 2, 4, ... are worth about 2.9, half of prizes 2, 4, 8, ...
    assert rk.stpetersburg_ce_alone("sqrt") / 2 == pytest.approx(2.914, abs=0.001)
    play = rk.stpetersburg_play(100_000, np.random.default_rng(1))
    assert np.all(play >= 2) and np.median(play) <= 4


def test_fisher_euler():
    f = rk.fisher(100.0, 100.0, 0.05, 0.96, 2.0)
    assert abs(f["euler_gap"]) < 1e-12
    assert f["c1"] + f["c2"] / 1.05 == pytest.approx(f["wealth"])
    g = rk.fisher(100.0, 100.0, 0.0, 1.0, 2.0)
    assert g["c1"] == pytest.approx(100.0) and g["saving"] == pytest.approx(0.0)


def test_discounting_and_reversals():
    t = np.array([0.0, 1.0, 10.0])
    assert np.allclose(rk.discount(t, "exponential", rate=0.1), np.exp(-0.1 * t))
    assert rk.discount(0.0, "beta-delta") == 1.0
    assert rk.reversal(100, 110, 1 / 365, 30 / 365, kind="beta-delta", beta=0.7, delta=0.96)
    assert not rk.reversal(100, 110, 1 / 365, 30 / 365, kind="exponential", rate=0.05)


def test_insurance():
    assert rk.optimal_cover(100, 50, 0.1, 0.0, 2.0)["cover"] == pytest.approx(1.0)
    assert rk.optimal_cover(100, 50, 0.1, 0.3, 2.0)["cover"] < 1.0


def test_rabin_crra():
    g = rk.crra_gamma_to_reject(100, 110, 100_000)
    assert 85 < g < 95
    assert rk.crra_rejects(100, 110, 100_000, g + 1) and not rk.crra_rejects(100, 110, 100_000, g - 1)
    assert rk.crra_largest_gain(1000, 100_000, g) == float("inf")      # Rabin: lose $1,000, gain any sum
    assert 0 < rk.crra_largest_gain(500, 100_000, g) < 2000


def test_holt_laury():
    menu = rk.holt_laury_menu()
    assert len(menu) == 10 and menu[-1]["p"] == 1.0
    assert rk.safe_choices(0.0) == 4                                   # risk neutral
    lo, hi = rk.holt_laury_interval(6)
    assert lo == pytest.approx(0.41, abs=0.01) and hi == pytest.approx(0.68, abs=0.01)
    lo, hi = rk.holt_laury_interval(4)
    assert lo == pytest.approx(-0.15, abs=0.01) and hi == pytest.approx(0.15, abs=0.01)


def test_epstein_zin_reduces_to_eu():
    c = (1.0, [0.8, 1.2])
    p = [0.5, 0.5]
    v = rk.epstein_zin_value(c, p, 0.9, 2.0, 0.5)                     # gamma = 1/psi: expected utility
    eu = (1 - 0.9) * rk.crra(1.0, 2.0) + 0.9 * np.dot(p, rk.crra(np.array([0.8, 1.2]), 2.0))
    assert rk.crra(v, 2.0) == pytest.approx(eu, rel=1e-9)


def test_bernoulli_game_and_median():
    # Bernoulli's own game pays 1, 2, 4, ...: half the prizes of the 2, 4, 8, ... game, so the log certainty
    # equivalent ignoring wealth is 2 and Cramer's square root is 2.914 (his "about 2.9")
    assert rk.stpetersburg_ce_alone("log", first=1.0) == pytest.approx(2.0)
    assert rk.stpetersburg_ce_alone("sqrt", first=1.0) == pytest.approx(2.914, abs=0.001)
    assert rk.stpetersburg_value(10, first=1.0) == pytest.approx(5.0)
    # Hayden and Platt's truncations: 3, 5, 8, 10, 15 tosses are worth $2.50, $3.50, $5, $6, $8.50
    assert [rk.stpetersburg_truncated_value(n) for n in (3, 5, 8, 10, 15)] == pytest.approx([2.5, 3.5, 5, 6, 8.5])
    p1000, p1m = rk.stpetersburg_price(1000.0, first=1.0), rk.stpetersburg_price(1e6, first=1.0)
    assert 5 < p1000 < 7 and 10 < p1m < 12 and p1m - p1000 == pytest.approx(np.log2(1000) / 2, abs=0.1)
    assert rk.stpetersburg_median_prize(1, reps=501) in (1.0, 2.0)  # a single game's median is $1 or $2 (by
    # convention $1.50: half the games pay $1)
    assert rk.stpetersburg_median_prize(1000, reps=500) > rk.stpetersburg_median_prize(10, reps=500)


def test_deductibles_and_portfolios():
    g = rk.deductible_gamma(100_000, 0.05, 500, 1000, 100)
    assert 150 < g < 300                                            # $75 over the expected saving: absurd aversion
    assert rk.deductible_gamma(100_000, 0.05, 500, 1000, 26) < 10   # a dollar over it: modest
    assert rk.merton_share(0.08, 0.02, 0.2, 2.0) == pytest.approx(0.75)
    s = np.linspace(0, 1, 501)
    eu = rk.portfolio_eu(s, 100.0, 0.02, [1.3, 0.86], [0.5, 0.5], 4.0)
    assert 0 < s[np.argmax(eu)] < 1


def test_early_resolution():
    eu = rk.ez_resolution(1, 1, [0.8, 1.2], [0.5, 0.5], 0.95, 2.0, 0.5)
    assert not eu["prefers_early"] and eu["premium"] == 0.0
    ez = rk.ez_resolution(1, 1, [0.8, 1.2], [0.5, 0.5], 0.95, 10.0, 1.5)
    assert ez["prefers_early"] and 0 < ez["premium"] < 0.5
    late = rk.ez_resolution(1, 1, [0.8, 1.2], [0.5, 0.5], 0.95, 0.5, 0.5)    # gamma < 1/psi: prefers late
    assert late["early"] < late["late"]


def test_beta_delta():
    b = rk.beta_delta_path(300.0, 6, 0.7)
    assert b["plan"].sum() == pytest.approx(300) and b["naive"].sum() == pytest.approx(300)
    assert np.allclose(b["plan"][1:], b["plan"][1])                  # the plan: equal after today
    assert np.all(np.diff(b["naive"]) < 0)                            # what happens: each self eats more than planned
    e = rk.beta_delta_path(300.0, 6, 1.0)
    assert np.allclose(e["naive"], 50) and np.allclose(e["plan"], 50)  # exponential: plan and action agree


def test_euler_regression():
    rng = np.random.default_rng(3)
    z = rng.normal(size=400)
    r = z + rng.normal(scale=0.5, size=400)
    g = 0.5 * r + rng.normal(scale=0.3, size=400)
    out = rk.euler_regression(g, r, instruments=z)
    assert out["iv"] == pytest.approx(0.5, abs=0.08) and out["first_F"] > 100


def test_measurement_and_paradoxes():
    assert [rk.hrs_threshold(c) for c in (0.5, 1 / 3)] == pytest.approx([1.0, 2.0])
    assert rk.hrs_threshold(0.2) == pytest.approx(3.76, abs=0.01)
    ch = rk.holt_laury_respond([0.0] * 50, 1e-6, np.random.default_rng(0))
    assert (ch.sum(axis=1) == 4).all() and not rk.switches_back(ch).any()
    noisy = rk.holt_laury_respond([0.4] * 300, 0.5, np.random.default_rng(1))
    assert rk.switches_back(noisy).mean() > 0.1
    e = rk.ellsberg_maxmin()
    assert e["I"] > e["II"] and e["IV"] > e["III"]                    # Ellsberg's frequent pattern
    L = {"1A": (0, 0), "1B": (0.01, 0.10), "2A": (0.89, 0), "2B": (0.90, 0.10)}
    u, w = (0.0, 0.85, 1.0), (6.0, 1.0, 2.0)
    V = {k: rk.weighted_utility_value(*v, u, w) for k, v in L.items()}
    assert V["1A"] > V["1B"] and V["2B"] > V["2A"]                    # fanning out produces Allais's pattern
    (x0, y0), (x1, y1) = rk.weighted_utility_line(0.5, u, w)
    k0 = rk.weighted_utility_value(0.3, y0 + 0.3 * (y1 - y0), u, w)
    assert k0 == pytest.approx(0.5)
    assert rk.tk_value(-1.0) == pytest.approx(-2.25) and rk.tk_weight(0.01) > 0.01 and rk.tk_weight(0.99) < 0.99
