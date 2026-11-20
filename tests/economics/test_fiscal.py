"""Agora's treasury (Part 32): debt dynamics, the New Keynesian spending multiplier, local-projection multipliers,
the regional multiplier, tax smoothing, the fiscal theory, unpleasant arithmetic and Arellano's default model."""

import numpy as np
import pytest

from explainer.economics.agora import fiscal


def test_debt_arithmetic():
    b = fiscal.debt_path(1.0, 0.03, 0.02, 0.0, years=10)
    assert b[-1] == pytest.approx((1.03 / 1.02) ** 10)
    s = fiscal.stabilizing_surplus(1.0, 0.03, 0.02)
    assert s == pytest.approx(0.01 / 1.02)
    assert fiscal.debt_path(1.0, 0.03, 0.02, s, years=25)[-1] == pytest.approx(1.0)
    assert fiscal.stabilizing_surplus(1.0, 0.01, 0.03) < 0                       # r < g: a deficit can be run


def test_nk_multiplier():
    m0 = fiscal.nk_multiplier(0.5)
    z0 = fiscal.nk_multiplier(0.5, zlb=True)
    assert m0["multiplier"] < 1 < z0["multiplier"]
    assert z0["inflation"] > m0["inflation"] > 0
    z = [fiscal.nk_multiplier(r, zlb=True)["multiplier"] for r in (0.0, 0.3, 0.5, 0.7)]
    assert np.all(np.diff(z) > 0)                                                # longer traps, bigger multipliers
    assert not fiscal.nk_multiplier(0.8, zlb=True)["bounded"]
    # with no supply effect and no rule, a one-period shock moves output one for one
    assert fiscal.nk_multiplier(0.0, zlb=True, gamma=1.0)["multiplier"] == pytest.approx(1.0)


def test_local_projection_recovers_a_known_multiplier():
    rng = np.random.default_rng(3)
    n = 6000
    news = rng.standard_normal(n)
    g = np.zeros(n)
    for t in range(1, n):
        g[t] = 0.85 * g[t - 1] + news[t]
    y = 1.3 * g + 0.5 * rng.standard_normal(n)
    S = {"y": y, "g": g, "news": news, "slack": (rng.random(n) < 0.4).astype(float)}
    out = fiscal.lp_multiplier(S, "news", H=12)
    assert out["multiplier"][4] == pytest.approx(1.3, abs=0.05)
    assert out["multiplier"][12] == pytest.approx(1.3, abs=0.05)
    st = fiscal.lp_multiplier(S, "news", H=8, state="slack")
    assert st["high"][8] == pytest.approx(1.3, abs=0.1) and st["low"][8] == pytest.approx(1.3, abs=0.1)


def test_regions_missing_intercept():
    r = fiscal.regions(R=60, T=300, m_local=1.5, m_agg=0.6, seed=1)
    assert r["b_fe"] == pytest.approx(1.5, abs=0.06)
    assert r["b_nat"] == pytest.approx(0.6, abs=0.15)


def test_tax_smoothing():
    flat = fiscal.tax_smoothing([0.2] * 30)
    assert flat["tau_smooth"] == pytest.approx(0.2) and flat["ratio"] == pytest.approx(1.0)
    war = fiscal.tax_smoothing([0.2] * 10 + [0.5] * 5 + [0.2] * 35, r=0.03)
    assert war["debt"][-1] == pytest.approx(0.0, abs=1e-9)
    assert max(war["debt"]) == pytest.approx(war["debt"][15])                    # the debt peaks as the war ends
    assert war["ratio"] > 1


def test_fiscal_theory_and_unpleasant_arithmetic():
    assert fiscal.ftpl_price_level(100, 2.0, 0.02) == pytest.approx(1.0)
    assert fiscal.ftpl_price_level(100, 1.5, 0.02) == pytest.approx(4 / 3)
    u = fiscal.unpleasant(T_tight=12, years=30, deficit=0.01, b0=0.5, base=0.15, mu_tight=0.0)
    assert u["mu_after_tight"] > u["mu_loose"] > 0
    assert u["tight"]["debt"][12] > u["loose"]["debt"][12]
    assert np.ptp(u["loose"]["debt"]) < 1e-9                                     # loose money holds debt steady


def test_arellano_small_grid():
    M = fiscal.arellano(ny=11, nb=60)
    q, D = np.array(M["q"]), np.array(M["default"], bool)
    assert q.max() <= 1 / (1 + M["params"]["r"]) + 1e-12 and q.min() >= -1e-12
    for row in q:
        assert np.all(np.diff(row) >= -1e-9)                                     # more debt never sells dearer
    assert D[0].mean() >= D[-1].mean()                                           # default comes in bad times
    S = fiscal.arellano_simulate(M, T=4000, seed=2)
    assert 0 <= S["default_rate_annual"] < 0.2
