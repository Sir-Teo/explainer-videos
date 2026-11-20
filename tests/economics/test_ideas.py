"""Agora's ideas module (Part 21): Romer's balanced path, Aghion and Howitt's research, semi-endogenous growth,
directed technical change."""

import numpy as np

from explainer.economics.agora import ideas as I


def test_replication_increasing_returns():
    r = I.replication(alpha=0.3)
    assert abs(r["double_KL"] - 2) < 1e-12 and abs(r["double_KLA"] - 4) < 1e-12


def test_romer_balanced_path_and_scale():
    b = I.romer_bgp(L=1.0, delta=0.1, alpha=0.5, rho=0.02, theta=1.0)
    # the researcher's wage equals the value of the ideas found: L_Y = r / (alpha delta), and g = delta L_A
    assert abs(b["L_Y"] - b["r"] / (0.5 * 0.1)) < 1e-12
    assert abs(b["g"] - 0.1 * b["L_A"]) < 1e-12
    assert abs(b["r"] - (0.02 + b["g"])) < 1e-12
    g = I.romer_scale([1.0, 2.0], delta=0.1, alpha=0.5, rho=0.02, theta=1.0)["g"]
    assert g[1] > g[0]                                      # the scale effect


def test_aghion_howitt_wedges():
    kw = dict(lam=0.1, alpha=0.6, rho=0.05, L=1.0)
    small, big = I.ah_research(gamma=1.2, **kw), I.ah_research(gamma=2.5, **kw)
    assert small["too_much"] and not big["too_much"]       # business stealing wins for small steps
    r = I.ah_research(gamma=1.5, **kw)
    # the arbitrage condition holds at the decentralized n: alpha (rho + lam n) = lam gamma (1 - alpha) (L - n)
    n = r["n_dec"]
    assert abs(0.6 * (0.05 + 0.1 * n) - 0.1 * 1.5 * 0.4 * (1 - n)) < 1e-12
    s = I.ah_sectors(lam=0.1, n=0.25, gamma=1.5, years=200, sectors=400, seed=1)
    assert abs(s["mean"][-1] / s["expected"][-1] - 1) < 0.1


def test_semi_endogenous_long_run():
    s = I.semi_endogenous(lam=1.0, phi=-2.0, n=0.043, theta=0.05, years=600)
    assert abs(s["gA"][-1] - 0.043 / 3) < 5e-4
    assert s["research_productivity"][-1] < s["research_productivity"][100]


def test_directed_slopes():
    d = I.directed(3.0, np.exp(np.linspace(-1, 1, 21)))
    sl = np.polyfit(np.log(d["ratio"]), np.log(d["long"]), 1)[0]
    assert abs(sl - 1.0) < 1e-9 and abs(d["short_slope"] + 1 / 3) < 1e-12
