"""Agora's money (Part 25): Kiyotaki and Wright's economy, Cagan's inflation tax, Baumol and Tobin, cash in advance."""

import numpy as np

from explainer.economics.agora import money as mo


def test_kiyotaki_wright_fundamental_holdings():
    f = mo.kw_simulate(n=200, periods=300, speculative=False, seed=1)
    d = np.array(f["dist"])
    # type 1 always holds its own product (good 2); type 3 holds good 1; type 2 holds goods 1 and 3 half and half
    assert d[0, 1] > 0.99 and d[2, 0] > 0.99
    assert abs(d[1, 0] - 0.5) < 0.05 and abs(d[1, 2] - 0.5) < 0.05
    # only good 1 is passed on
    assert f["medium"][0] > 0.99


def test_kiyotaki_wright_equilibrium_checks():
    f = mo.kw_simulate(n=200, periods=300, speculative=False, seed=2)
    s = mo.kw_simulate(n=200, periods=300, speculative=True, seed=2)
    # costly fish: fundamental play is an equilibrium; cheap fish: speculation is
    assert not mo.kw_best_response(f["dist"], c=(0.1, 0.2, 0.6), beta=0.9)["accept_3"]
    assert mo.kw_best_response(s["dist"], c=(0.1, 0.2, 0.25), beta=0.9, speculative=True)["accept_3"]
    assert s["medium"][2] > 0.2 and s["medium"][0] > 0.2


def test_barter_and_money():
    b = mo.barter_matches(10)
    assert abs(b["barter"] - 1 / 81) < 1e-12 and abs(b["money"] - 1 / 9) < 1e-12


def test_cagan_laffer_peak():
    for alpha in (2.0, 5.0, 8.0):
        L = mo.cagan_laffer(alpha, mus=np.linspace(0, 3 / alpha, 30001))
        assert abs(L["best"] - 1 / alpha) < 1e-3
        assert abs(L["max"] - np.exp(-1) / alpha) < 1e-6


def test_cagan_deficit_stability():
    alpha, d = 5.0, 0.04
    slow = mo.cagan_deficit(alpha, d, 0.1, periods=200)
    fast = mo.cagan_deficit(alpha, d, 0.5, periods=200)
    lo, hi = slow["steady"]
    assert lo < 1 / alpha < hi
    assert abs(slow["path"][-1] - lo) < 0.01 and not slow["exploded"]
    assert fast["exploded"]
    # a deficit beyond the Laffer maximum has no steady state
    assert mo.cagan_deficit(alpha, 0.2, 0.1)["steady"] == []


def test_baumol_tobin_square_root():
    b = mo.baumol_tobin(1000.0, [0.01, 0.04], 2.0)
    assert abs(b["money"][0] / b["money"][1] - 2.0) < 1e-12
    # the trips minimize the total cost
    i, Y, cost = 0.01, 1000.0, 2.0
    n = np.linspace(0.5, 10, 2000)
    tot = i * Y / (2 * n) + cost * n
    assert abs(n[np.argmin(tot)] - b["trips"][0]) < 0.01


def test_cash_in_advance_friedman_rule():
    c = mo.cia(np.linspace(-0.04, 0.5, 400), beta=0.96, a=1.0)
    loss = np.array(c["loss"])
    assert np.all(np.diff(loss) > 0)                 # the cost rises with inflation
    assert abs(loss[0]) < 1e-9                        # and is zero at the Friedman rule
    assert abs(c["friedman_mu"] + 0.04) < 1e-12


def test_loans_create_deposits():
    t = mo.taccounts(loan=100.0)
    assert t["broad_money"] == 100.0 and t["base_money"] == 0.0
    t2 = mo.taccounts(loan=100.0, cash_share=0.2)
    hh = t2["household"]["assets"]
    assert abs(hh["deposit"] + hh["currency"] - 100.0) < 1e-12
