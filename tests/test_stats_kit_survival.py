"""statkit.survival against statsmodels and closed forms (Part 40)."""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from explainer.stats import museum as M
from explainer.stats.kit import survival as SV

warnings.filterwarnings("ignore")
sm = pytest.importorskip("statsmodels.api")
from statsmodels.duration.survfunc import SurvfuncRight, survdiff  # noqa: E402


def _sim(n=300, seed=1, beta=(0.7, -0.4)):
    g = np.random.default_rng(seed)
    X = g.standard_normal((n, len(beta)))
    T = g.exponential(1 / np.exp(X @ np.array(beta)))
    C = g.exponential(1.5, n)
    return np.minimum(T, C).round(2) + 0.01, (T <= C).astype(int), X


def test_km_greenwood_against_statsmodels():
    g = M.gehan()
    for grp in (0, 1):
        k = g["group"] == grp
        km = SV.kaplan_meier(g["time"][k], g["event"][k])
        sf = SurvfuncRight(g["time"][k], g["event"][k])
        assert np.allclose(km["surv"], sf.surv_prob)
        f = np.isfinite(km["se"]) & (km["n"] > km["d"])
        assert np.allclose(km["se"][f], sf.surv_prob_se[f])
    km = SV.kaplan_meier(g["time"][g["group"] == 1], g["event"][g["group"] == 1])
    assert SV.km_median(km) == 23.0


def test_redistribute_to_the_right_is_km():
    t, e, _ = _sim(60, 3)
    rd = SV.redistribute_right(t, e)
    assert np.allclose(rd["surv"], SV.kaplan_meier(t, e)["surv"])


def test_logrank_gehan():
    g = M.gehan()
    lr = SV.logrank(g["time"], g["event"], g["group"])
    chi2, p = survdiff(g["time"], g["event"], g["group"])
    assert lr["chi2"] == pytest.approx(chi2, rel=1e-10)
    gw = SV.logrank(g["time"], g["event"], g["group"], weight="gehan")
    chi2g, _ = survdiff(g["time"], g["event"], g["group"], weight_type="gb")
    assert gw["chi2"] == pytest.approx(chi2g, rel=1e-8)


@pytest.mark.parametrize("ties", ["breslow", "efron"])
def test_cox_against_phreg(ties):
    t, e, X = _sim()
    f = SV.cox_fit(t, e, X, ties=ties)
    m = sm.PHReg(t, X, status=e, ties=ties).fit()
    assert np.allclose(f["beta"], m.params, atol=1e-7)
    assert np.allclose(f["se"], m.bse, rtol=1e-6)
    assert f["loglik"] == pytest.approx(m.llf, rel=1e-9)


def test_cox_start_stop_entry():
    t, e, X = _sim(200, 5)
    entry = np.random.default_rng(9).uniform(0, 0.005, len(t))
    f = SV.cox_fit(t, e, X, entry=entry, ties="breslow")
    m = sm.PHReg(t, X, status=e, entry=entry, ties="breslow").fit()
    assert np.allclose(f["beta"], m.params, atol=1e-7)
    # splitting each row at a cut point leaves the fit unchanged
    cut = 0.3
    a = t > cut
    tt = np.concatenate([np.minimum(t, cut), t[a]])
    ee = np.concatenate([np.where(a, 0, e), e[a]])
    en = np.concatenate([np.zeros(len(t)), np.full(a.sum(), cut)])
    XX = np.vstack([X, X[a]])
    f2 = SV.cox_fit(tt, ee, XX, entry=en, ties="breslow")
    f1 = SV.cox_fit(t, e, X, ties="breslow")
    assert np.allclose(f1["beta"], f2["beta"], atol=1e-8)


def test_schoenfeld_against_phreg():
    t, e, X = _sim(150, 7)
    t = t + np.arange(len(t)) * 1e-6  # no ties
    f = SV.cox_fit(t, e, X, ties="breslow")
    s = SV.schoenfeld(t, e, X, f)
    m = sm.PHReg(t, X, status=e, ties="breslow").fit()
    r = m.schoenfeld_residuals
    r = r[~np.isnan(r[:, 0])]
    order = np.argsort(t[e == 1])
    assert np.allclose(np.sort(s["resid"][:, 0]), np.sort(r[:, 0]), atol=1e-8)
    assert s["chi2"].shape == (2,) and np.all(s["p"] > 0.001)
    assert len(order) == len(s["t"])


def test_exponential_aft_closed_form():
    t, e, _ = _sim(400, 11, beta=(0.0, 0.0))
    f = SV.aft_fit(t, e, dist="exponential")
    rate = e.sum() / t.sum()
    assert np.exp(-f["coef"][0]) == pytest.approx(rate, rel=1e-5)
    w = SV.aft_fit(t, e, dist="weibull")
    assert w["sigma"] == pytest.approx(1.0, abs=0.15)


def test_weibull_aft_matches_cox_hr():
    g = np.random.default_rng(13)
    n = 1500
    x = g.standard_normal(n)
    T = (g.exponential(1, n) / np.exp(0.8 * x)) ** (1 / 1.5)  # Weibull, shape 1.5, log HR 0.8
    C = g.uniform(0, 3, n)
    t, e = np.minimum(T, C), (T <= C).astype(int)
    w = SV.aft_fit(t, e, x[:, None], dist="weibull")
    hr = -w["coef"][1] / w["sigma"]
    assert hr == pytest.approx(0.8, abs=0.08)
    assert 1 / w["sigma"] == pytest.approx(1.5, abs=0.1)


def test_aalen_johansen_and_fine_gray():
    g = np.random.default_rng(17)
    n = 800
    x = g.standard_normal(n)
    T1, T2, C = g.exponential(1 / np.exp(0.5 * x)), g.exponential(2, n), g.exponential(3, n)
    t = np.minimum.reduce([T1, T2, C])
    st = np.where(t == C, 0, np.where(t == T1, 1, 2))
    aj = SV.aalen_johansen(t, st)
    assert np.allclose(aj["cif1"] + aj["cif2"] + aj["surv"], 1.0)
    assert np.all(aj["naive1"] >= aj["cif1"] - 1e-12)
    # with no competing events, Fine--Gray is Cox (Breslow)
    st1 = np.where(st == 2, 0, st)
    fg = SV.fine_gray(t, st1, x)
    cx = SV.cox_fit(t, (st1 == 1).astype(int), x, ties="breslow")
    assert fg["beta"][0] == pytest.approx(cx["beta"][0], abs=1e-7)


def test_rmst_and_nelson_aalen():
    t, e, _ = _sim(200, 19)
    km = SV.kaplan_meier(t, e)
    r = SV.rmst(km, 1.0)
    grid = np.linspace(0, 1, 20001)
    assert r["rmst"] == pytest.approx(np.trapezoid(SV.km_at(km, grid), grid), abs=1e-3)
    na = SV.nelson_aalen(t, e)
    assert np.all(np.exp(-na["H"]) >= km["surv"] - 1e-12)  # exp(-H_NA) >= KM


def test_concordance_and_brier():
    t, e, X = _sim(300, 23)
    f = SV.cox_fit(t, e, X)
    risk = X @ f["beta"]
    c = SV.concordance(t, e, risk)
    assert 0.6 < c < 0.8
    assert SV.concordance(t, e, -risk) == pytest.approx(1 - c, abs=1e-12)
    S = SV.cox_survival(f, X, [0.5])[:, 0]
    assert SV.brier_ipcw(t, e, S, 0.5) < SV.brier_ipcw(t, e, np.full(len(t), S.mean()), 0.5)


def test_gamma_frailty_recovers_theta():
    g = np.random.default_rng(29)
    m = 400
    Z = g.gamma(1 / 0.8, 0.8, m)
    cl = np.repeat(np.arange(m), 3)
    T = (g.exponential(1, 3 * m) / Z[cl]) ** (1 / 1.3)
    C = g.uniform(0, 4, 3 * m)
    t, e = np.minimum(T, C), (T <= C).astype(int)
    f = SV.gamma_frailty_weibull(t, e, cl)
    assert f["theta"] == pytest.approx(0.8, abs=0.25)
    assert f["k"] == pytest.approx(1.3, abs=0.12)


def test_conformal_lpb_covers():
    g = np.random.default_rng(31)
    cover = []
    for _ in range(40):
        n = 600
        x = g.uniform(0, 1, 2 * n)
        T = g.exponential(1 + x)
        C = g.exponential(4, 2 * n)
        q = (1 + x) * -np.log(0.9)  # the true 10% quantile, as a fitted q
        lpb = SV.conformal_lpb(T[:n], C[:n], q[:n], q[n:], c0=3.0, alpha=0.1)
        cover.append(np.mean(T[n:] >= lpb))
    assert np.mean(cover) >= 0.88
