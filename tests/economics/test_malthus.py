"""Agora's long run (Part 19): the Malthusian economy, England's labour demand curve, and the unified growth toy."""

import numpy as np

from explainer.economics import data
from explainer.economics.agora import malthus as ml


def test_technology_buys_people_not_income():
    s = ml.simulate(1500, L0=0.7, invention=(500, 0.5), beta=0.6, lam=0.02)
    assert abs(s["y"][499] - 1.0) < 1e-3                      # at subsistence before the invention
    assert s["y"][500] > 1.25                                  # richer the day it arrives ...
    assert abs(s["y"][-1] - 1.0) < 1e-3                        # ... and back at subsistence in the end
    assert abs(s["L"][-1] / s["L_star"] - 1) < 0.01               # with the new steady state's people,
    assert abs(s["L_star"] / ml.steady_state(1.0, beta=0.6) - 1.5 ** (1 / 0.6)) < 1e-9   # (1.5)^(1/beta) times more


def test_plague_raises_income_by_the_survivors_share():
    s = ml.simulate(300, L0=1.0, plague=(100, 0.45), beta=0.6)
    assert abs(s["y"][100] / s["y"][99] - 0.55 ** -0.6) < 1e-9
    assert s["y"][100] > s["y"][150] > s["y"][250] > 1.0       # and drifts back as the population recovers


def test_vital_rates_cross_at_subsistence():
    b, d = ml.vital_rates([0.8, 1.0, 1.2])
    assert b[1] == d[1] and b[0] < d[0] and b[2] > d[2]


def test_wage_elasticity_recovers_a_planted_slope():
    rng = np.random.default_rng(1)
    years = np.arange(1300, 1700)
    pop = np.exp(rng.normal(8, 0.3, len(years)))
    wage = np.exp(5 - 0.8 * np.log(pop) + rng.normal(0, 0.05, len(years)))
    r = ml.wage_elasticity(years, pop, wage, 1300, 1699)
    assert abs(r["slope"] + 0.8) < 3 * r["se_hc1"] + 0.01


def test_england_is_malthusian_before_1640_and_not_after_1600():
    m = data.millennium()
    before = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], 1270, 1640)
    after = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], 1600, 1800)
    assert before["slope"] < -0.5 and before["slope"] + 3 * before["se_nw"] < 0
    assert after["slope"] > 0
    i = {y: k for k, y in enumerate(m["year"])}
    assert m["population"][i[1351]] < 0.6 * m["population"][i[1348]]     # the Black Death
    assert m["real_wage"][i[1450]] > 2.5 * m["real_wage"][i[1348]]


def test_education_starts_above_a_threshold_and_fertility_falls():
    assert ml.education_choice(0.02) == 0.0
    assert ml.education_choice(0.3) > 0.0
    qq = ml.quantity_quality()
    ns = [r["n"] for r in qq]
    es = [r["e"] for r in qq]
    assert all(a >= b for a, b in zip(ns, ns[1:])) and all(a <= b for a, b in zip(es, es[1:]))


def test_unified_economy_passes_through_three_regimes_in_order():
    u = ml.unified(phi=0.065)
    regimes = [r["regime"] for r in u["rows"]]
    order = [regimes[0]] + [b for a, b in zip(regimes, regimes[1:]) if a != b]
    assert order == ["Malthusian", "post-Malthusian", "modern"]
    ys = [r["y"] for r in u["rows"]]
    assert max(ys[:10]) < 1.1 < ys[-1]
    ns = [r["n"] for r in u["rows"]]
    assert ns[-1] < max(ns) - 0.05


def test_spatial_noise_fools_ordinary_standard_errors():
    r = ml.spatial_noise(n_sites=200, reps=200)
    assert r["independent"]["reject"] < 0.1 < 0.3 < r["smooth"]["reject"]
