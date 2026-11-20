"""Agora's asset prices and investment (Part 23): the Gordon formula, the user cost, Hayashi's firm, the option to
wait, Mehra and Prescott's economy, the Hansen-Jagannathan bound, rare disasters, habits and the laboratory market."""

import numpy as np

from explainer.economics.agora import assets as ast


def test_gordon_and_present_value():
    g = ast.gordon(4.0, 0.07, 0.03)
    assert abs(g["price"] - 100) < 1e-9 and abs(g["price_up"] - 80) < 1e-9
    # the closed form agrees with a long sum
    pv = ast.present_value(4.0 * 1.03 ** np.arange(3000), 0.07)
    assert abs(pv - 100) < 1e-6
    assert abs(ast.user_cost(0.05, 0.08) - 0.13) < 1e-12


def test_q_investment_converges():
    q = ast.q_investment()
    assert q["q0"] > q["q_new"] > 1
    assert abs(q["K"][-1] - q["K_new"]) < 0.01 * q["K_new"]
    assert np.all(np.diff(q["K"]) >= -1e-9)


def test_option_to_wait():
    o = ast.option_to_wait(r=0.04, mu=0.0, sigma=0.2)
    assert abs(o["beta"] - 2.0) < 1e-12 and abs(o["multiple"] - 2.0) < 1e-12
    # more volatility, a higher threshold; no volatility, the NPV rule
    assert ast.option_to_wait(sigma=0.4)["multiple"] > o["multiple"]
    assert ast.option_to_wait(sigma=0.01)["multiple"] < 1.05


def test_mehra_prescott():
    # risk neutrality: no premium
    m = ast.mehra_prescott(0.98, 0.0)
    assert abs(m["premium"]) < 1e-12
    # their bound: with gamma <= 10 and a safe rate below 4%, the premium stays under about 0.4%
    reg = ast.mp_region(np.linspace(0.05, 10, 40), np.linspace(0.8, 0.999, 40))
    pts = np.array(reg["points"])
    assert pts[pts[:, 2] <= 0.04][:, 3].max() < 0.004
    # the premium rises with risk aversion
    assert ast.mehra_prescott(0.99, 10)["premium"] > ast.mehra_prescott(0.99, 2)["premium"] > 0


def test_hj_and_lognormal():
    h = ast.hj_bound(0.3, 0.036, [1, 10])
    assert 8 < h["needed_gamma"] < 8.5
    t = ast.lognormal_tree(0.99, 2.0)
    assert t["premium"] == 2.0 * 0.036 ** 2


def test_disasters_and_habit():
    beta = np.exp(-0.03)
    w = ast.disasters(beta, 3.5)
    wo = ast.disasters(beta, 3.5, p=0.0)
    assert w["premium"] > 0.04 and wo["premium"] < 0.003 and w["rf"] < wo["rf"]
    h = ast.habit(years=200, seed=1)
    assert abs(h["steady_price"] - np.sqrt(2.0 * (1 - 0.87))) < 1e-9
    assert min(h["S"]) > 0 and max(h["S"]) <= h["smax"] + 1e-12


def test_ssw_market():
    s = ast.ssw_market()
    fv, p = np.array(s["fv"]), np.array(s["price"])
    assert p[0] < fv[0] and np.any(p > fv + 0.5) and p[-1] < 0.5 * p.max()
