"""Agora's banks (Part 26): Diamond and Dybvig, runs, Bagehot's lender, Merton's put, repo, global games, monitoring."""

import numpy as np
from scipy.stats import binom

from explainer.economics.agora import bank as bk


def test_dd_contract_first_order_condition_and_budget():
    d = bk.dd_contract(R=1.5, gamma=2.0, t=0.25)
    c1, c2 = d["c1"], d["c2"]
    assert abs(0.25 * c1 + 0.75 * c2 / 1.5 - 1) < 1e-12          # the budget binds
    assert abs(c1 ** -2.0 - 1.5 * c2 ** -2.0) < 1e-12              # u'(c1) = R u'(c2)
    assert abs(c1 - 1.1596) < 1e-3 and abs(c2 - 1.4202) < 1e-3
    assert d["eu"] > d["eu_autarky"]                                 # the bank beats going it alone
    # log utility gives the autarky allocation: nothing to insure against
    lg = bk.dd_contract(R=1.5, gamma=1.0, t=0.25)
    assert abs(lg["c1"] - 1) < 1e-12 and abs(lg["c2"] - 1.5) < 1e-12


def test_run_threshold_is_where_staying_stops_paying():
    d = bk.dd_contract(R=1.5, gamma=2.0, t=0.25)
    f = d["threshold"]
    stay = bk.dd_stayers([f - 1e-6, f, f + 1e-6], d["c1"], 1.5)
    assert stay[0] > d["c1"] and abs(stay[1] - d["c1"]) < 1e-9 and stay[2] < d["c1"]
    # if only the impatient withdraw, stayers get exactly c2
    assert abs(bk.dd_stayers([0.25], d["c1"], 1.5)[0] - d["c2"]) < 1e-12


def test_sequential_service_pays_one_over_c1():
    r = bk.sequential_service(n=1000, c1=1.25, seed=3)
    assert r["served"] == 800 and r["last_paid"] == 0.0
    s = bk.suspension(0.25, 1.16, 1.5)
    assert s["stay"] and s["c2_guaranteed"] > 1.16


def test_bagehot_fire_sale_against_lender():
    L = bk.lender_of_last_resort(10, 90, 90, 10, 30, fire_price=0.6, haircut=0.2, penalty=0.05)
    assert abs(L["sold"] - 100 / 3) < 1e-9 and abs(L["equity_fire"] + 10 / 3) < 1e-9 and not L["survives_fire"]
    assert abs(L["equity_llr"] - 9) < 1e-12 and L["survives_llr"]


def test_merton_put_call_parity_and_monotone_in_risk():
    lo, hi = bk.merton_put(100, 90, 0.05), bk.merton_put(100, 90, 0.25)
    for m in (lo, hi):
        assert abs(m["equity"] - m["put"] - 10) < 1e-9               # C - P = V - D at r = 0
    assert hi["put"] > lo["put"] > 0
    # Monte Carlo check of the put at 25% volatility
    rng = np.random.default_rng(0)
    vt = 100 * np.exp(-0.5 * 0.25 ** 2 + 0.25 * rng.standard_normal(400_000))
    assert abs(np.mean(np.maximum(90 - vt, 0)) - hi["put"]) < 0.05


def test_bond_loss_matches_duration():
    b = bk.bond_loss(0.015, 10, 0.015, 0.0151)
    assert abs(b["p0"] - 1) < 1e-12
    assert abs(b["change"] / 0.0001 + b["duration"]) < 0.01          # dP/P = -D dy for a small move
    big = bk.bond_loss(0.015, 10, 0.015, 0.045)
    assert -0.25 < big["change"] < -0.22


def test_capital_ratio_and_deposit_beta():
    c = bk.capital_ratio({"reserves": 10, "loans": 60, "bonds": 30}, 10, {"reserves": 0, "loans": 1, "bonds": 0},
                         loss=7.12)
    assert abs(c["leverage"] - 0.1) < 1e-12 and abs(c["risk_based"] - 1 / 6) < 1e-12
    assert abs(c["after_loss"] - 2.88 / 92.88) < 1e-12 and c["solvent"]
    assert abs(bk.deposit_beta(0.08, 5.33, 0.06, 0.46) - 0.4 / 5.25) < 1e-12


def test_repo_leverage():
    r = bk.repo_leverage(100, 4, 0.04, 0.20)
    assert abs(r["max_leverage_from"] - 25) < 1e-9 and abs(r["max_leverage_to"] - 5) < 1e-9
    assert abs(r["must_sell"] - 80) < 1e-9 and abs(r["repo_from"] - 96) < 1e-9 and abs(r["repo_after"] - 16) < 1e-9


def test_global_game_threshold():
    g = bk.global_game(c=1.0, R=2.0, sigma=0.05, n=4000, seed=1)
    assert abs(g["theta_star"] - 0.5) < 1e-12
    th, fail = np.array(g["theta"]), np.array(g["fail"])
    # fails below the threshold, survives above it (allowing a band of a few noise widths)
    assert fail[th < 0.4].all() and not fail[th > 0.6].any()
    # the marginal depositor is indifferent: P(theta > theta* | x*) = c / R
    from scipy.stats import norm
    assert abs(norm.cdf((g["x_star"] - g["theta_star"]) / 0.05) - 0.5) < 1e-9
    gen = bk.global_game(c=1.2, R=2.0, sigma=0.05)
    assert gen["theta_star"] > g["theta_star"]


def test_diversified_failure():
    assert abs(bk.diversified_failure(1, 0.9, 1.3) - 0.1) < 1e-12
    assert abs(bk.diversified_failure(10, 0.9, 1.3) - binom.cdf(7, 10, 0.9)) < 1e-12
    p = [bk.diversified_failure(n, 0.9, 1.3) for n in (10, 100, 1000)]
    assert p[0] > p[1] > p[2] and p[1] < 1e-4
    # Monte Carlo
    rng = np.random.default_rng(0)
    x = rng.binomial(10, 0.9, 400_000)
    assert abs(np.mean(x * 1.3 < 10) - p[0]) < 0.003
