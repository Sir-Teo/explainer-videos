"""Agora's credit (Part 33): Minsky's borrowers, debt deflation, the costly-state-verification contract and the
accelerator, Kiyotaki and Moore, the leverage cycle, county balance sheets, the crisis predictor and Basel's guide."""

import numpy as np
import pytest

from explainer.economics.agora import credit


def test_minsky_and_debt_deflation():
    s = credit.minsky_shares([1.0, 1.0, 1.0], [12.0, 20.0, 40.0], 0.03)     # due 0.96, 1.6, 2.4; interest 1.2
    assert s["hedge"] == pytest.approx(1 / 3) and s["speculative"] == pytest.approx(1 / 3)
    assert s["ponzi"] == pytest.approx(1 / 3)
    assert credit.minsky_shares([1.0], [12.0], 0.09)["ponzi"] == 1.0
    b = credit.debt_deflation(1.0, [0.1] * 4, -0.05, repay=0.05)
    assert b[-1] == pytest.approx(1 / 0.9 ** 4)
    assert credit.debt_deflation(1.0, [0.0] * 3, 0.0, repay=0.1)[-1] == pytest.approx(0.9 ** 3)


def test_lognormal_partial_expectation():
    sigma, ob = 0.35, 0.8
    F, f, G, Gamma = credit._lognormal(np.array([ob]), sigma)
    rng = np.random.default_rng(0)
    w = np.exp(rng.normal(-sigma ** 2 / 2, sigma, 400_000))
    assert G[0] == pytest.approx(np.mean(w * (w < ob)), abs=2e-3)
    assert F[0] == pytest.approx(np.mean(w < ob), abs=2e-3)


def test_premium_rises_with_leverage_and_accelerates():
    C = credit.csv_contract(0.35, 0.15)
    assert np.all(np.diff(C["leverage"]) > 0) and np.all(np.diff(C["premium"]) > 0)
    assert credit.premium_at(1.2, C) < credit.premium_at(3.0, C)
    a0 = credit.accelerator(1.0, C)
    a1 = credit.accelerator(0.9, C)
    assert a0["K"] == pytest.approx(2.0, abs=1e-6)
    assert a1["K"] < a0["K"] and a1["premium"] > a0["premium"]


def test_kiyotaki_moore():
    s = credit.km_steady(R=1.1, a=1.0)
    assert s["q"] == pytest.approx(11.0) and s["u"] == pytest.approx(1.0)
    st = credit.km_path(0.01, static=True, R=1.1, eta=2.0)
    assert st["k0"] == pytest.approx(100 * (0.99 ** (2 / 3) - 1))
    A = credit.km_amplification(0.01, R=1.1, eta=2.0)
    assert A["dynamic"] > 5 * A["static"]
    k = np.array(A["dynamic_path"]["k"])
    assert np.all(np.diff(k) > 0) and abs(k[-1]) < 1e-3             # recovers, monotonically
    with pytest.raises(ValueError):
        credit.km_path(0.03, R=1.1, eta=2.0)                       # too large a shock: no equilibrium


def test_leverage_cycle_matches_geanakoplos():
    w, wo = credit.leverage_static(0.2, True), credit.leverage_static(0.2, False)
    assert wo["p"] == pytest.approx(0.677, abs=1e-3) and w["p"] == pytest.approx(0.749, abs=1e-3)
    c = credit.leverage_cycle(0.2)
    assert c["ok"]
    assert c["p0"] == pytest.approx(0.95, abs=0.01) and c["pD"] == pytest.approx(0.69, abs=0.01)
    assert c["marginD"] > c["margin0"]


def test_counties_recover_the_planted_slope():
    c = credit.counties(n=4000, seed=1)
    mp = [q["mpc"] for q in c["by_quintile"]]
    tr = [q["truth"] for q in c["by_quintile"]]
    assert np.allclose(mp, tr, atol=0.006)
    assert mp[-1] > mp[0]


def test_auc_and_predictor_on_synthetic_panel():
    assert credit.auc([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]) == pytest.approx(0.75)
    rng = np.random.default_rng(2)
    n_c, T = 12, 140
    iso = np.repeat([f"C{k}" for k in range(n_c)], T)
    year = np.tile(np.arange(1870, 1870 + T), n_c)
    drl = rng.normal(0.03, 0.05, n_c * T)
    s5 = np.array([drl[max(0, i - 5):i].sum() if i % T >= 5 else 0 for i in range(n_c * T)])
    p = 1 / (1 + np.exp(-(-4.0 + 8 * s5)))
    crisis = (rng.random(n_c * T) < p).astype(float)
    P = {"iso": iso, "year": year, "crisis": crisis, "drl": drl, "cg": np.cumsum(drl), "rh": np.zeros(n_c * T),
         "y": np.zeros(n_c * T), "war": np.zeros(n_c * T, bool)}
    R = credit.crisis_predictor(P, "real_loans", oos_from=1950)
    assert R["auc_in"] > 0.6 and R["auc_oos"] > 0.55
    assert R["sum_coef"] == pytest.approx(5 * 8, rel=0.4)                  # 8 on each of five lags


def test_basel_guide():
    assert np.allclose(credit.ccyb_guide([0, 2, 6, 10, 20]), [0, 0, 1.25, 2.5, 2.5])
    x = np.concatenate([np.full(20, 50.0), 50 + 3.0 * np.arange(1, 11)])
    g = credit.one_sided_gap(x)
    assert np.all(np.isnan(g[:10])) and abs(g[19]) < 1e-6 and g[-1] > 5   # the trend absorbs part of a ramp
    t = np.arange(40.0)
    assert credit.hp_trend(3 + 2 * t, 1e5) == pytest.approx(3 + 2 * t, abs=1e-6)   # a line is its own trend
