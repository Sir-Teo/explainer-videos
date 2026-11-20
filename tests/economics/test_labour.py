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


# --- Part II (Part 39): the wage structure ----------------------------------------------------------------------------
T39 = truths(39)


def test_canonical_model_and_katz_murphy():
    rng = np.random.default_rng(0)
    years = np.arange(1963, 2001)
    t = years - years[0]
    # supply growth that slows after 1980, so that trend and supply are not collinear
    S = np.where(years < 1980, 0.04 * t, 0.04 * 17 + 0.015 * (t - 17))
    sigma, g = 1.6, 0.03
    prem = labour.skill_premium(S, g * t * sigma / (sigma - 1), sigma) + rng.normal(0, 0.005, t.size)
    km = labour.katz_murphy(prem, S, years)
    assert abs(km["sigma"] - sigma) < 0.15 and abs(km["trend"] - g) < 0.004
    D = labour.implied_demand(prem, S, sigma)
    assert np.allclose(np.diff(D), g, atol=0.02)


def test_task_model_thresholds_and_automation():
    T = T39["tasks"]
    kw = {k: T[k] for k in ("L", "M", "H", "beta")}
    b, a = labour.task_model(**kw), labour.task_model(**kw, auto=T["auto"])
    lw = b["lnw"]
    assert abs((lw[1] - lw[0]) - (T["beta"][1] - T["beta"][0]) * b["I_L"]) < 1e-8
    assert abs((lw[2] - lw[1]) - (T["beta"][2] - T["beta"][1]) * b["I_H"]) < 1e-8
    assert abs(b["share_L"] + b["share_M"] + b["share_H"] - 1) < 1e-12
    # machines take the middle band: the middle loses against both neighbours, and moves out to both edges
    assert a["wM_wL"] < b["wM_wL"] and a["wH_wM"] > b["wH_wM"]
    assert a["I_L"] < b["I_L"] and a["I_H"] > b["I_H"]


def test_akm_recovers_truth_and_shows_limited_mobility_bias():
    F = T39["firms"]
    small = {**F, "n_workers": 8000, "n_firms": 200, "years": 5}
    E = labour.worker_firm_economy(**small)
    A = labour.akm(E["y"], E["firm"])
    assert abs(A["var_psi"] - E["truth"]["var_psi"]) < 0.004
    assert abs(A["corr"] - E["truth"]["corr"]) < 0.05
    E2 = labour.worker_firm_economy(**{**small, "move": 0.005})
    A2 = labour.akm(E2["y"], E2["firm"])
    assert A2["var_psi"] > 1.3 * E2["truth"]["var_psi"] and A2["corr"] < E2["truth"]["corr"] - 0.1


def test_superstars_hedonic_and_discrimination_models():
    S = labour.superstars(n=20000, seed=1)
    assert abs(S["top1"][0] - S["talent_top1"]) < 1e-12 and S["top1"][0] < S["top1"][1] < S["top1"][2]
    H = labour.hedonic(n=40, seed=2)
    r, w, d = np.array(H["r"]), np.array(H["w"]), np.array(H["d"])
    k = slice(5, 35)
    slope = np.gradient(w, r)[k]
    ok = np.isfinite(slope) & (np.diff(r, prepend=r[0])[k] > 1e-6)
    assert np.allclose(slope[ok], d[k][ok], rtol=0.25)
    assert labour.becker(0.1, 0.2)["gap"] == 0.0 and labour.becker(0.3, 0.1)["gap"] > 0
    P = labour.phelps([0.0, 2.0], sd_q=1.0, sd_noise=(0.5, 1.0))
    assert abs(P[0]["lam"] - 0.8) < 1e-12 and abs(P[1]["pay"][1] - 1.0) < 1e-12 and P[0]["pay"][0] == 0.0


def test_oaxaca_and_within():
    rng = np.random.default_rng(3)
    n = 4000
    xa, xb = rng.normal(13, 2, n), rng.normal(12.5, 2, n)
    Xa, Xb = np.column_stack([np.ones(n), xa]), np.column_stack([np.ones(n), xb])
    ya, yb = 0.5 + 0.08 * xa + rng.normal(0, 0.3, n), 0.5 + 0.08 * xb + rng.normal(0, 0.3, n)
    O = labour.oaxaca(ya, Xa, yb, Xb)
    assert abs(O["explained"] + O["unexplained"] - O["gap"]) < 1e-12
    assert abs(O["unexplained"]) < 0.03 and abs(O["explained"] - 0.08 * (xa.mean() - xb.mean())) < 0.01
    ids = np.repeat(np.arange(300), 6)
    fe = rng.normal(0, 1, 300)[ids]
    x = rng.normal(0, 1, ids.size) + fe
    y = 0.4 * x + fe + rng.normal(0, 0.1, ids.size)
    W = labour.within(y, x[:, None], ids)
    D = np.column_stack([x, (ids[:, None] == np.arange(300)[None, :]).astype(float)])
    b = np.linalg.lstsq(D, y, rcond=None)[0]
    assert abs(W["b"][0] - b[0]) < 1e-10


def test_child_penalty_and_robots_recover_planted_effects():
    C = labour.child_penalty(n=2500, seed=4)
    assert abs(C["long_run"] - np.mean(C["planted"][-5:])) < 0.05
    assert max(abs(v) for v in C["penalty"][:4]) < 0.05
    R = labour.robot_zones(seed=5, noise=0.4)
    assert abs(R["ctrl"] - R["beta"]) < 3 * R["ctrl_se"] and R["naive"] < R["ctrl"]


def test_part39_data():
    R = data.resume()
    cb = np.array(R["received_callback"])
    race = np.array(R["race"])
    assert cb.size == 4870 and int(cb[race == "white"].sum()) == 235 and int(cb[race == "black"].sum()) == 157
    A = data.autor_dorn("pctile")
    assert abs(sum(A["emp1980"]) - 100) < 0.01 and abs(sum(A["emp2005"]) - 100) < 0.05
    O = data.autor_dorn("occ")
    assert abs(np.nansum(O["sh_empl1980"]) - 100) < 0.01
    assert all(data.occ_group(int(c)) for c in O["occ1990dd"])
    from explainer.economics.data.stata import read_dta  # noqa: PLC0415
    assert callable(read_dta)
