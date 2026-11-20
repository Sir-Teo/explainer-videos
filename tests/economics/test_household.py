"""Agora's households and overlapping generations (Part 22): permanent income, the life cycle, the buffer stock by
the endogenous grid method, Friedman's cross-section, Campbell and Mankiw's instrument, the wealthy hand-to-mouth,
and Diamond's economy."""

import numpy as np

from explainer.economics.agora import household as hh
from explainer.economics.agora import olg


def test_permanent_income_annuity():
    w = hh.pih(1.0, r=0.03)
    assert abs(w["share"] - 0.03 / 1.03) < 1e-12
    # a finite horizon spends more of the windfall each year, and in total spends it all in present value
    f = hh.pih(1.0, r=0.03, horizon=10)
    pv = sum(f["per_year"] / 1.03 ** t for t in range(1, 11)) * 1.03
    assert f["share"] > w["share"] and abs(pv - 1.0) < 1e-9


def test_life_cycle_exhausts_wealth_and_peaks_at_retirement():
    lc = hh.life_cycle(work=40, retire=20, R=1.02, beta=1 / 1.02, gamma=2.0)
    assert abs(lc["end_assets"]) < 1e-9
    assert lc["peak_age"] == 65
    c = np.array(lc["consumption"])
    assert np.allclose(c, c[0])            # beta R = 1: flat


def test_buffer_stock_solution():
    bs = hh.buffer_stock()
    m, c, mpc = np.array(bs["m"]), np.array(bs["c"]), np.array(bs["mpc"])
    # consumption rises with cash, never exceeds it, and is concave: the MPC falls
    assert np.all(np.diff(c) >= -1e-9) and np.all(c <= m + 1e-9)
    assert mpc[50] > mpc[150] > mpc[500]
    assert 1.2 < bs["target"] < 1.7
    # the Euler equation holds off the constraint (checked at the grid points the method produced)
    p = bs["params"]
    psi, wp, th, wt = hh._shocks(p["perm_sd"], p["tran_sd"], p["p_zero"])
    mg, cg = np.array(bs["m_grid"]), np.array(bs["c_grid"])
    for k in (40, 90, 150):
        a = mg[k] - cg[k]
        rhs = sum(w1 * w2 * (p["G"] * s * np.interp(p["R"] * a / (p["G"] * s) + t, mg, cg)) ** -p["gamma"]
                  for s, w1 in zip(psi, wp) for t, w2 in zip(th, wt))
        assert abs(cg[k] ** -p["gamma"] / (p["beta"] * p["R"] * rhs) - 1) < 2e-3
    # without risk an impatient household spends everything until a year's income
    sure = hh.buffer_stock(perm_sd=0.0, tran_sd=0.0, p_zero=0.0)
    cs = np.array(sure["c"])
    assert np.allclose(cs[:90], m[:90], atol=1e-6)
    assert np.all(c[200:] < cs[200:])      # risk: more saving at every level of cash past the kink


def test_population_mpc_and_hand_to_mouth():
    bs = hh.buffer_stock()
    s = hh.simulate_mpc(bs, n=4000, seed=1)
    assert 0.15 < s["mean_mpc"] < 0.35
    assert s["mpc_by_decile"][0] > s["mpc_by_decile"][-1]
    owner = hh.buffer_stock(beta=0.96 * 1.03 / 1.07)
    h = hh.hand_to_mouth(bs, owner, n=4000, seed=1)
    assert h["mpc_owners"] > h["mpc_renters"] and h["net_owners"] > 3 * h["net_renters"]
    assert h["corr_liquid"] < -0.9 and h["corr_net"] > 0


def test_friedman_cross_section():
    f = hh.friedman_cross_section(n=20000, seed=3)
    assert abs(f["elasticity"] - f["elasticity_theory"]) < 0.02
    assert f["intercept"] > 0 and f["slope"] < 0.9
    assert f["apc_by_decile"][0] > 1 > f["apc_by_decile"][-1]
    assert max(f["apc_time"]) - min(f["apc_time"]) < 0.03


def test_rule_of_thumb_iv():
    reps = [hh.rule_of_thumb(lam=0.4, T=240, seed=k) for k in range(60)]
    assert np.mean([r["ols"] for r in reps]) > 0.55
    assert abs(np.median([r["iv"] for r in reps]) - 0.4) < 0.08


def test_diamond_economy():
    for beta in (0.3, 0.9):
        st = olg.diamond_steady(beta=beta)
        k_closed = (beta * 0.7 * 10 / ((1 + beta) * 1.4)) ** (1 / 0.7)
        assert abs(st["k"] - k_closed) < 1e-6
    pat = olg.pension_welfare([0.0, 0.2, 0.4], beta=0.9)
    imp = olg.pension_welfare([0.0, 0.2, 0.4], beta=0.3)
    assert pat["R"][0] < 1.4 < imp["R"][0]
    assert pat["utility"][1] > pat["utility"][0] and imp["utility"][1] < imp["utility"][0]
    s = olg.samuelson_money(n=0.4, beta=0.9)
    assert s["utility_money"] > s["utility_autarky"] and abs(s["return"] - 1.4) < 1e-12
