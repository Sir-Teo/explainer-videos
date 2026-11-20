"""Agora's labour (Part 38): each model checked against something it does not compute itself."""

import numpy as np
import pytest
from scipy.stats import norm

from explainer.economics import data
from explainer.economics.agora import labour
from explainer.economics.island import truths

T = truths(38)


def test_hours_solve_the_first_order_condition_and_bend_back():
    kw = {k: T["supply"][k] for k in ("y", "gamma", "phi", "psi")}
    for w in (3.0, 12.0, 40.0):
        h = labour.hours(w, **kw)
        c = w * h + kw["y"]
        assert abs(w * c ** -kw["gamma"] - kw["psi"] * h ** (1 / kw["phi"])) < 1e-9
    hs = [labour.hours(w, **kw) for w in np.linspace(2, 50, 49)]
    k = int(np.argmax(hs))
    assert 0 < k < 48                         # rises, then bends back


def test_slutsky_and_the_log_case():
    kw = {k: T["supply"][k] for k in ("y", "gamma", "phi", "psi")}
    e = labour.supply_elasticities(6.0, **kw)
    assert abs(e["hicksian"] - (e["marshallian"] - e["income_effect"])) < 1e-12
    assert e["hicksian"] > 0 and e["income_effect"] < 0
    # with log utility (gamma = 1) and no other income, hours do not depend on the wage at all
    h = [labour.hours(w, y=0.0, gamma=1.0, phi=0.5) for w in (2.0, 10.0, 50.0)]
    assert max(h) - min(h) < 1e-9


def test_competitive_floor():
    M = T["market"]
    eq = labour.competitive(**M)
    assert abs(M["A"] * eq["w"] ** -M["eps_d"] - eq["L"]) < 1e-9
    L = labour.floor_competitive(eq["w"] * 1.188, **M)
    assert abs(L / eq["L"] - 1.188 ** -M["eps_d"]) < 1e-12
    # a floor below the market wage does not bind
    assert labour.floor_competitive(eq["w"] * 0.9, **M) == pytest.approx(eq["L"], rel=1e-12)


def test_monopsony_markdown_and_minimum():
    P = T["monopsony"]
    R = labour.monopsony(**P)
    mrpl = P["a"] * R["L_m"] ** -P["b"]
    assert abs((mrpl - R["w_m"]) / mrpl - 1 / (1 + P["eta"])) < 1e-6
    ms = np.linspace(R["w_m"], R["w_c"] * 1.2, 400)
    emp = labour.floor_monopsony(ms, **P)
    assert abs(ms[int(np.argmax(emp))] - R["w_c"]) < 0.03
    assert emp[0] == pytest.approx(R["L_m"], rel=1e-6)


def test_border_experiment_signs():
    B = T["border"]
    kw = {k: B[k] for k in ("n_treat", "n_ctrl", "m0", "m1", "eps_d", "eta", "trend", "noise")}
    c = np.mean([labour.border_experiment("competitive", seed=s, **kw)["did_emp"] for s in range(30)])
    m = np.mean([labour.border_experiment("monopsony", seed=s, **kw)["did_emp"] for s in range(30)])
    assert c < 0 < m
    # without noise and with no trend, the design recovers the competitive model exactly in each store
    r = labour.border_experiment("competitive", noise=0.0, trend=0.0, **{k: kw[k] for k in kw if k not in
                                                                          ("noise", "trend")})
    L0, L1, w0, w1 = (np.array(r[k]) for k in ("L0", "L1", "w0", "w1"))
    assert np.allclose(np.log(L1 / L0), -B["eps_d"] * np.log(w1 / w0))


def test_ols_and_tsls_against_closed_forms():
    rng = np.random.default_rng(0)
    n = 5000
    z = rng.normal(size=n)
    u = rng.normal(size=n)
    x = 0.8 * z + 0.6 * u + rng.normal(size=n)
    y = 1.0 + 0.5 * x + u
    one = np.ones(n)
    iv = labour.tsls(y, np.column_stack([one, x]), np.column_stack([one, z]))
    wald = np.cov(z, y)[0, 1] / np.cov(z, x)[0, 1]       # the just-identified IV is the ratio of covariances
    assert abs(iv["b"][1] - wald) < 1e-10
    o = labour.ols(y, np.column_stack([one, x]))
    assert o["b"][1] > 0.6                                  # least squares is biased up by the shared u
    assert iv["first_stage_F"] > 1000


def test_card_1995_published_estimates():
    C = data.wooldridge("card")

    def col(k):
        return np.array(C[k], float)
    y, s = col("lwage"), col("educ")
    ctrl = [col(k) for k in ("exper", "expersq", "black", "smsa", "south", "smsa66", "reg662", "reg663", "reg664",
                             "reg665", "reg666", "reg667", "reg668", "reg669")]
    one = np.ones_like(s)
    iv = labour.tsls(y, np.column_stack([one, s, *ctrl]), np.column_stack([one, col("nearc4"), *ctrl]))
    assert abs(iv["b"][1] - 0.1315) < 0.001                 # Wooldridge, Example 15.4: 0.132 (0.055)
    assert abs(iv["se"][1] - 0.055) < 0.003


def test_heckman_recovers_the_mean_and_mills_ratio():
    R = T["roy"]
    r = labour.roy(**R)
    w1, z, sec = np.array(r["w1"]), np.array(r["z"]), np.array(r["second"])
    one = np.ones_like(w1)
    H = labour.heckman_two_step(w1, one[:, None], ~sec, np.column_stack([one, z]))
    assert abs(H["corrected"][0] - w1.mean()) < 0.02
    assert H["naive"][0] - w1.mean() > 0.05
    # the truncated-normal mean that the correction rests on
    rng = np.random.default_rng(1)
    e, v = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], 400000).T
    c = 0.3
    assert abs(e[v > -c].mean() - 0.6 * norm.pdf(c) / norm.cdf(c)) < 0.01
