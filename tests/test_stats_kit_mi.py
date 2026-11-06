"""statkit.mi: missing data and measurement error (Part 41)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from explainer.stats.kit import mi as MI


def _bivariate(n=2000, seed=1, rho=0.6):
    g = np.random.default_rng(seed)
    x = g.standard_normal(n)
    y = 1.0 + rho * x + math.sqrt(1 - rho ** 2) * g.standard_normal(n)
    miss = MI.mask("mar", n, 0.4, g, driver=x, strength=2.0)["miss"]
    return x, y, miss


def test_mask_rates():
    g = np.random.default_rng(0)
    for kind in ("mcar", "mar", "mnar"):
        m = MI.mask(kind, 50_000, 0.3, g, driver=g.standard_normal(50_000))
        assert m["p"].mean() == pytest.approx(0.3, abs=1e-6)
        assert m["miss"].mean() == pytest.approx(0.3, abs=0.01)


def test_em_complete_is_mle_and_monotone():
    g = np.random.default_rng(2)
    X = g.multivariate_normal([0, 1, 2], [[1, 0.5, 0.2], [0.5, 2, 0.3], [0.2, 0.3, 1.5]], 500)
    e = MI.em_mvn(X)
    assert np.allclose(e["mu"], X.mean(0))
    assert np.allclose(e["S"], np.cov(X.T, bias=True))
    x, y, miss = _bivariate()
    Y = np.column_stack([x, np.where(miss, np.nan, y)])
    e = MI.em_mvn(Y)
    assert np.all(np.diff(e["ll"]) > -1e-8)
    assert e["mu"][1] == pytest.approx(1.0, abs=0.05)  # MAR: EM recovers the mean
    assert abs(np.nanmean(Y[:, 1]) - 1.0) > 0.1  # complete cases do not


def test_rubin_rules():
    r = MI.rubin([1.0] * 5, [0.04] * 5)
    assert r["T"] == pytest.approx(0.04) and r["B"] == 0.0
    r = MI.rubin([1.0, 1.2, 0.8, 1.1, 0.9], [0.04] * 5, df_complete=100)
    assert r["T"] == pytest.approx(0.04 + 1.2 * 0.025)
    assert r["df"] < 100


def test_multiple_imputation_covers_under_mar():
    g = np.random.default_rng(3)
    cover, cover_single = [], []
    for _ in range(150):
        n = 300
        x = g.standard_normal(n)
        y = 1.0 + 0.6 * x + 0.8 * g.standard_normal(n)
        miss = MI.mask("mar", n, 0.4, g, driver=x, strength=2.0)["miss"]
        yo = np.where(miss, np.nan, y)
        ests, vars_ = [], []
        for _ in range(10):
            yy = MI.impute_norm(yo, x, g, "proper")
            ests.append(yy.mean())
            vars_.append(yy.var(ddof=1) / n)
        r = MI.rubin(ests, vars_, df_complete=n - 1)
        cover.append(r["ci"][0] <= 1.0 <= r["ci"][1])
        ys = MI.impute_norm(yo, x, g, "mean")
        se = ys.std(ddof=1) / math.sqrt(n)
        cover_single.append(abs(ys.mean() - 1.0) <= 1.96 * se)
    assert np.mean(cover) >= 0.89
    assert np.mean(cover_single) < np.mean(cover)


def test_mice_runs_and_fills():
    g = np.random.default_rng(4)
    n = 300
    x = g.standard_normal(n)
    z = (g.random(n) < 1 / (1 + np.exp(-x))).astype(float)
    y = x + z + g.standard_normal(n)
    D = np.column_stack([x, z, y])
    D[g.random(n) < 0.2, 1] = np.nan
    D[g.random(n) < 0.2, 2] = np.nan
    imps = MI.mice(D, m=3, iters=5, rng=g, methods={1: "logreg", 2: "pmm"})
    assert len(imps) == 3
    for Y in imps:
        assert not np.isnan(Y).any()
        assert set(np.unique(Y[:, 1])) <= {0.0, 1.0}


def test_ipw_and_aipw():
    x, y, miss = _bivariate(5000, 5)
    r = (~miss).astype(float)
    rm = MI.response_model(r, x)
    ipw = MI.ipw_mean(y, r, rm["p"])
    D = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(D[r == 1], y[r == 1], rcond=None)[0]
    aipw = MI.aipw_mean(y, r, rm["p"], D @ b)
    assert ipw["est"] == pytest.approx(1.0, abs=0.05)
    assert aipw["est"] == pytest.approx(1.0, abs=0.04)
    # double robustness: a wrong outcome model with the right propensity is still fine
    wrong = MI.aipw_mean(y, r, rm["p"], np.zeros(len(x)))
    assert wrong["est"] == pytest.approx(1.0, abs=0.06)


def test_heckman_recovers_beta():
    g = np.random.default_rng(6)
    n = 4000
    x = g.standard_normal(n)
    z = g.standard_normal(n)
    e, u = g.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], n).T
    s = (0.3 + 0.8 * z + 0.5 * x + u > 0).astype(int)
    y = 1.0 + 2.0 * x + e
    ols = np.linalg.lstsq(np.column_stack([np.ones(s.sum()), x[s == 1]]), y[s == 1], rcond=None)[0]
    two = MI.heckman_twostep(y, x, s, np.column_stack([x, z]))
    mle = MI.heckman_mle(y, x, s, np.column_stack([x, z]))
    assert abs(ols[0] - 1.0) > 0.15  # selection biases OLS
    assert two["beta"][0] == pytest.approx(1.0, abs=0.12)
    assert mle["beta"][1] == pytest.approx(2.0, abs=0.06)
    assert mle["rho"] == pytest.approx(0.6, abs=0.12)


def test_simex_and_misclassification():
    g = np.random.default_rng(7)
    n = 3000
    x = g.standard_normal(n)
    w = x + 0.7 * g.standard_normal(n)
    y = 2.0 * x + 0.5 * g.standard_normal(n)
    s = MI.simex(w, y, 0.49, B=50, rng=g)
    assert s["naive"] < 1.6
    assert abs(s["simex"] - 2.0) < abs(s["naive"] - 2.0) / 2
    # expected counts under misclassification are corrected exactly
    se, sp = 0.8, 0.9
    te_case, tu_case, te_ctl, tu_ctl = 300.0, 700.0, 200.0, 800.0
    a = se * te_case + (1 - sp) * tu_case
    c = se * te_ctl + (1 - sp) * tu_ctl
    out = MI.misclass_correct(a, 1000 - a, c, 1000 - c, se, sp)
    assert out["or_corrected"] == pytest.approx(300 * 800 / (700 * 200))
    assert out["or_observed"] < out["or_corrected"]
    assert MI.disattenuate(0.3, 0.5) == pytest.approx(0.3 / math.sqrt(0.5))


def test_mrp_poststratifies():
    g = np.random.default_rng(8)
    A, R = 4, 6
    ea, er = g.normal(0, 0.6, A), g.normal(0, 0.4, R)
    pop = [(a, r_) for a in range(A) for r_ in range(R)]
    N = g.integers(500, 3000, len(pop))
    truth = sum(Nk / (1 + np.exp(-(-0.3 + ea[a] + er[r_]))) for Nk, (a, r_) in zip(N, pop)) / N.sum()
    # a sample that over-represents age group 3
    rows = []
    for (a, r_), Nk in zip(pop, N):
        k = int(Nk * (0.08 if a == 3 else 0.02))
        p = 1 / (1 + np.exp(-(-0.3 + ea[a] + er[r_])))
        rows += [(a, r_, float(g.random() < p)) for _ in range(k)]
    a_, r_, y = map(np.array, zip(*rows))
    fit = MI.mrp_fit(y, [a_, r_])
    pa = np.array([p[0] for p in pop])
    pr = np.array([p[1] for p in pop])
    est = float(np.sum(MI.mrp_predict(fit, [pa, pr]) * N) / N.sum())
    assert abs(est - truth) < abs(y.mean() - truth)
    assert est == pytest.approx(truth, abs=0.02)
