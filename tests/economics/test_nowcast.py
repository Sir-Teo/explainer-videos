"""Agora's nowcast module (Part 57): revisions, seasonal adjustment, nowcasting, signals and forecast scoring."""

import numpy as np
import pytest

from explainer.economics.agora import nowcast as N


def test_revisions_2008q4():
    R = N.revisions()
    p = R["path_2008q4"]
    assert p[0]["vintage"] == "2009Q1" and p[0]["growth"] == pytest.approx(-3.8, abs=0.1)
    assert p[-1]["growth"] < -7
    assert 0.5 < R["mae"] < 3 and R["corr"] > 0.8


def test_x11_recovers_a_planted_season():
    rng = np.random.default_rng(0)
    n = 240
    season = np.tile(np.array([-2, -1.5, -1, 0, 0.5, 1, 0, 0.2, 0.5, 0.8, 1, 1.5]) / 100, n // 12)
    season -= season.mean()
    level = np.exp(np.log(100) + 0.002 * np.arange(n) + season + 0.002 * rng.standard_normal(n))
    out = N.x11(level, 0)
    mid = slice(36, n - 36)
    assert np.max(np.abs(out["seasonal"][mid] - season[mid])) < 0.004


def test_x11_outlier_step_protects_the_factors():
    rng = np.random.default_rng(1)
    n = 240
    season = np.tile(np.linspace(-0.01, 0.01, 12), n // 12)
    y = np.log(100) + season + 0.001 * rng.standard_normal(n)
    y[123] -= 0.15                                     # a one-off collapse in one April
    lv = np.exp(y)
    raw, rob = N.x11(lv, 0, robust=False), N.x11(lv, 0, robust=True)
    k = 135                                            # the next April
    assert abs(rob["seasonal"][k] - season[k]) < abs(raw["seasonal"][k] - season[k])


def test_island_nowcast_improves_and_is_calibrated():
    r = N.island_nowcast(quarters=160, seed=3)
    assert np.all(np.diff(r["rmse"]) < 0.05) and r["rmse"][-1] < 0.5 * r["rmse"][0]
    assert 0.55 < np.mean(r["coverage"]) < 0.8


def test_probit_and_sahm():
    P = N.yield_curve_probit()
    assert P["b"][1] < 0 and P["auc"] > 0.7
    S = N.sahm_rule()
    assert any(t["month"] == "2024-07" and t["recession"] is None for t in S["rt_triggers"])


def test_score_spf_beats_mean_near_and_not_far():
    S = N.score_spf()
    r0, r4 = S["rows"][0], S["rows"][-1]
    assert r0["rmse"] < r0["rmse_mean"] and r0["dm_p"] < 0.05
    assert r4["dm_p"] > 0.05 and r4["share_neg_fc"] < 0.02


def test_greenbook_and_bates_granger():
    G = N.greenbook_vs_spf()
    assert all(r["rmse_gb"] < r["rmse_spf"] for r in G["rows"])
    assert G["rows"][0]["rmse_bg"] <= min(G["rows"][0]["rmse_gb"], G["rows"][0]["rmse_spf"]) + 1e-9


def test_regimes_best_forecast_never_negative_a_year_ahead():
    Rg = N.regime_forecasts()
    assert Rg["rows"][-1]["share_neg"] == 0 and Rg["share_neg_growth"] > 0.1
    assert Rg["pi_rec"] == pytest.approx(0.05 / 0.3)
