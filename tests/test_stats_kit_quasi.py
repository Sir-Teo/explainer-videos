"""statkit.quasi (Part 37): instruments, regression discontinuity, DiD, synthetic control, panels and bounds."""

from __future__ import annotations

import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import quasi as Q


def _rng(s):
    return np.random.default_rng(s)


def test_tsls_binary_instrument_is_the_wald_ratio_and_liml_agrees():
    g = _rng(1)
    n = 5000
    z = (g.random(n) < 0.5).astype(float)
    u = g.standard_normal(n)
    d = 1.0 + 0.8 * z + 0.7 * u + g.standard_normal(n)
    y = 2.0 + 0.5 * d + u
    t = Q.tsls(y, d, z)
    wald = (y[z == 1].mean() - y[z == 0].mean()) / (d[z == 1].mean() - d[z == 0].mean())
    assert t["beta"] == pytest.approx(wald, rel=1e-10)
    li = Q.liml(y, d, z)
    assert li["kappa"] == pytest.approx(1.0, abs=1e-8)  # just identified: LIML = 2SLS
    assert li["beta"] == pytest.approx(t["beta"], rel=1e-8)
    assert t["ols"] > 0.6  # OLS is biased up by the shared u


def test_ar_set_endpoints_sit_on_the_critical_value():
    g = _rng(2)
    n = 2000
    z = g.standard_normal(n)
    u = g.standard_normal(n)
    d = 0.3 * z + 0.6 * u + g.standard_normal(n)
    y = 1.0 * d + u
    s = Q.ar_set(y, d, z, alpha=0.1)
    assert s["kind"] == "interval"
    for b in (s["lo"], s["hi"]):
        assert Q.anderson_rubin(y, d, z, None, b)["p"] == pytest.approx(0.1, abs=1e-6)
    assert Q.ar_covers(s, 1.0)


def test_ar_set_is_unbounded_when_the_instrument_is_irrelevant():
    g = _rng(3)
    n = 500
    z = g.standard_normal(n)
    d = g.standard_normal(n)
    y = d + g.standard_normal(n)
    kinds = {Q.ar_set(y, d, g.standard_normal(n))["kind"] for _ in range(20)}
    assert kinds & {"line", "outside"}


def test_local_linear_matches_weighted_least_squares():
    g = _rng(4)
    x = g.uniform(-1, 1, 3000)
    y = 1 + 2 * x + 0.5 * (x >= 0) + 0.3 * g.standard_normal(3000)
    h = 0.4
    o = Q.local_linear(x, y, 0.0, h, 1, "right")
    k = (x >= 0) & (x <= h)
    w = 1 - x[k] / h
    X = np.column_stack([np.ones(k.sum()), x[k] / h])
    b = np.linalg.solve((X.T * w) @ X, (X.T * w) @ y[k])
    assert o["a"] == pytest.approx(b[0], rel=1e-10)
    r = Q.rd(x, y, 0.0, h)
    assert abs(r["tau"] - 0.5) < 4 * r["se"]


def test_rd_robust_corrects_curvature_bias():
    g = _rng(5)
    reps, cov_c, cov_r = 200, 0, 0
    for _ in range(reps):
        x = g.uniform(-1, 1, 2000)
        y = 3 * x ** 2 + 1.0 * (x >= 0) + 0.5 * g.standard_normal(2000)
        o = Q.rd_robust(x, y, 0.0, 0.6)
        cov_c += o["conv"]["ci"][0] <= 1 <= o["conv"]["ci"][1]
        cov_r += o["robust"]["ci"][0] <= 1 <= o["robust"]["ci"][1]
    assert cov_r / reps > 0.83 and cov_c / reps < cov_r / reps


def test_mccrary_detects_bunching_and_not_a_smooth_density():
    g = _rng(6)
    x = g.normal(0, 1, 20000)
    assert abs(Q.mccrary(x, 0.3, 0.05, 0.6)["z"]) < 3
    bumped = np.where((x > 0.1) & (x < 0.3) & (g.random(20000) < 0.6), 0.3 + 0.05 * g.random(20000), x)
    assert Q.mccrary(bumped, 0.3, 0.05, 0.6)["z"] > 5


def test_twfe_equals_dummy_regression_and_bacon_adds_up():
    g = _rng(7)
    N, T = 60, 12
    times = np.arange(T)
    G = g.choice([3.0, 6.0, 9.0, np.inf], N)
    D = (times[None, :] >= G[:, None]).astype(float)
    Y = g.standard_normal(N)[:, None] + 0.2 * times[None, :] + D * (1 + 0.3 * (times[None, :] - np.where(np.isfinite(G), G, 0)[:, None])) \
        + 0.5 * g.standard_normal((N, T))
    tw = Q.twfe(Y, D)
    unit, tt = np.repeat(np.arange(N), T), np.tile(np.arange(T), N)
    X = np.column_stack([D.ravel(), np.eye(N)[unit], np.eye(T)[tt][:, 1:]])
    b = np.linalg.lstsq(X, Y.ravel(), rcond=None)[0][0]
    assert tw["beta"] == pytest.approx(b, rel=1e-8)
    parts = Q.bacon(Y, G, times)
    assert sum(p["w"] for p in parts) == pytest.approx(1.0)
    assert sum(p["w"] * p["est"] for p in parts) == pytest.approx(tw["beta"], rel=1e-8)


def test_callaway_santanna_and_imputation_recover_dynamic_effects():
    g = _rng(8)
    N, T = 400, 15
    times = np.arange(T)
    G = g.choice([4.0, 8.0, 11.0, np.inf], N, p=[0.3, 0.3, 0.2, 0.2])
    rel = times[None, :] - G[:, None]
    tau = np.where(rel >= 0, 0.5 * (rel + 1), 0.0)
    Y = g.standard_normal(N)[:, None] + np.sin(times)[None, :] + tau + 0.3 * g.standard_normal((N, T))
    D = rel >= 0
    truth = tau[D].mean()
    cs = Q.callaway_santanna(Y, G, times)
    im = Q.imputation(Y, G, times)
    assert abs(cs["att"] - truth) < 4 * cs["se"]
    assert im["att"] == pytest.approx(truth, abs=0.1)
    assert Q.twfe(Y, D.astype(float))["beta"] < truth - 0.5  # TWFE is dragged down by the forbidden comparisons


def test_simplex_ls_recovers_convex_weights():
    g = _rng(9)
    B = g.standard_normal((30, 8))
    w = np.array([0.5, 0.3, 0.2, 0, 0, 0, 0, 0])
    est = Q.simplex_ls(B @ w, B)
    assert est.sum() == pytest.approx(1.0)
    assert np.all(est >= 0)
    assert est == pytest.approx(w, abs=1e-4)


def test_sdid_reproduces_prop99():
    """Arkhangelsky et al. (2021), Table 1: SDID -15.6, SC -19.6, DiD -27.3 packs per capita."""
    d = museum.prop99()
    Y = d["cigsale"]
    j = d["states"].index("California")
    T0 = int(np.flatnonzero(d["years"] == 1989)[0])
    s = Q.sdid(Y, j, T0)
    assert s["tau"] == pytest.approx(-15.6, abs=0.1)
    assert s["sc"] == pytest.approx(-19.6, abs=0.15)
    assert s["did"] == pytest.approx(-27.3, abs=0.1)


def test_within_and_nickell():
    g = _rng(10)
    N, T = 200, 6
    a = g.standard_normal(N)
    x = a[:, None] + g.standard_normal((N, T))
    y = 2 * x + 3 * a[:, None] + g.standard_normal((N, T))
    unit = np.repeat(np.arange(N), T)
    assert Q.within(y.ravel(), x.ravel()[:, None], unit)["b"][0] == pytest.approx(2.0, abs=0.1)
    rho, Tn = 0.5, 5
    est = []
    for _ in range(40):
        aa = g.standard_normal(2000)
        Yp = np.zeros((2000, Tn + 1))
        Yp[:, 0] = aa / (1 - rho) + g.standard_normal(2000) / np.sqrt(1 - rho ** 2)
        for t in range(1, Tn + 1):
            Yp[:, t] = rho * Yp[:, t - 1] + aa + g.standard_normal(2000)
        uu = np.repeat(np.arange(2000), Tn)
        est.append(Q.within(Yp[:, 1:].ravel(), Yp[:, :-1].ravel()[:, None], uu)["b"][0])
    assert np.mean(est) == pytest.approx(rho + Q.nickell_bias(rho, Tn), abs=0.01)


def test_bounds_contain_the_truth():
    g = _rng(11)
    n = 20000
    t = g.random(n) < 0.5
    u = g.random(n)
    always, marginal = u < 0.6, (u >= 0.6) & (u < 0.75)
    w0 = np.where(always, 15 + 3 * g.standard_normal(n), 10 + 2 * g.standard_normal(n))
    w = np.where(t & always, w0 + 1, w0)
    s = always | (marginal & t)
    lb = Q.lee_bounds(w, t, s)
    assert lb["lo"] <= 1.0 <= lb["hi"]
    e = s.astype(float)
    r = g.random(n) < 0.8
    m = Q.manski(e, t, r, 0, 1)
    assert m["lo"] <= e[t].mean() - e[~t].mean() <= m["hi"]
    assert m["hi"] - m["lo"] == pytest.approx((1 - r[t].mean()) + (1 - r[~t].mean()), abs=1e-12)
