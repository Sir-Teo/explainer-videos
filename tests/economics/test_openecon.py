"""Agora's open economy (Part 34): real exchange rates and half-lives, Balassa-Samuelson, Fama's regression, the
carry trade, the horse race, Mundell-Fleming, Dornbusch, Krugman's attack, Obstfeld's regions and pass-through."""

import numpy as np
import pytest

from explainer.economics.agora import openecon


def _months(n, start=1980):
    return [f"{start + j // 12}-{j % 12 + 1:02d}" for j in range(n)]


def test_halflife_recovers_a_planted_ar1():
    rng = np.random.default_rng(0)
    rho, out = 0.8, {}
    for c in range(12):
        q = np.zeros(400)
        for t in range(1, 400):
            q[t] = rho * q[t - 1] + rng.normal(0, 0.1)
        out[f"C{c}"] = (np.arange(1700, 2100), q + c)          # country effects removed by demeaning
    H = openecon.ppp_halflife(out, 1700, 2099)
    assert H["rho"] == pytest.approx(rho, abs=0.02)
    assert H["halflife"] == pytest.approx(np.log(0.5) / np.log(rho), rel=0.08)


def test_real_rates_definition():
    D = {"iso": ["USA", "USA", "GBR", "GBR"], "year": [2000, 2001, 2000, 2001], "cpi": [100, 110, 100, 100],
         "xrusd": [1, 1, 0.5, 0.5]}
    y, q = openecon.real_rates(D)["GBR"]
    assert list(y) == [2000, 2001]
    assert q[1] - q[0] == pytest.approx(np.log(1.1))          # US prices up 10%: the pound 10% cheaper in real terms


def test_balassa_samuelson_slope():
    x = np.log([1000, 5000, 20000, 60000])
    R = openecon.balassa_samuelson(x, 0.1 * x - 1)
    assert R["slope"] == pytest.approx(0.1) and R["corr"] == pytest.approx(1.0)


def test_fama_slope_is_one_under_parity():
    rng = np.random.default_rng(1)
    ks = _months(480)
    gap = {k: 4 * np.sin(j / 30) for j, k in enumerate(ks)}       # home minus foreign, % a year
    i_home = {k: 5 + g for k, g in gap.items()}
    i_for = {k: 5.0 for k in ks}
    s, ls = 0.0, {}
    for j, k in enumerate(ks):                                    # the currency drifts by the monthly gap
        ls[k] = s
        s += gap[k] / 1200 + rng.normal(0, 0.0005)
    F = openecon.fama(ls, i_home, i_for, h=3)
    assert F["beta"] == pytest.approx(1.0, abs=0.1) and F["se"] > 0


def test_carry_earns_the_gap_when_rates_do_not_move():
    ks = _months(60, 1990)
    ls = {"A": {k: 0.0 for k in ks}, "B": {k: 0.0 for k in ks}, "C": {k: 0.0 for k in ks}}
    rates = {"A": {k: 8.0 for k in ks}, "B": {k: 1.0 for k in ks}, "C": {k: 2.0 for k in ks}}
    C = openecon.carry(ls, rates, {k: 3.0 for k in ks}, first="1990-01", k=1)
    assert C["mean"] == pytest.approx(0.07)                     # long A at 8%, short B at 1%


def test_horse_race_random_walk_is_one():
    rng = np.random.default_rng(2)
    ks = _months(300)
    x = np.cumsum(rng.normal(0, 0.03, 300))
    H = openecon.horse_race({"A": dict(zip(ks, x))}, {"A": {k: 3.0 for k in ks}}, {k: 3.0 for k in ks}, 3)
    assert H["ratio"]["random walk"] == 1.0
    assert H["ratio"]["interest parity"] == pytest.approx(1.0)  # equal rates: parity predicts no change
    assert 0.9 < H["ratio"]["AR(1)"] < 1.2


def test_mundell_fleming():
    a, c, k = openecon.MF["a"], openecon.MF["c"], openecon.MF["k"]
    f = openecon.mundell_fleming("floating", dg=1.0)
    assert f["y"] == 0 and f["e"] == pytest.approx(-1 / c)
    m = openecon.mundell_fleming("floating", dm=1.0)
    assert m["y"] == pytest.approx(1 / k) and m["e"] == pytest.approx((1 - a) / (k * c))
    assert openecon.mundell_fleming("fixed", dg=1.0)["y"] == pytest.approx(1 / (1 - a))
    assert openecon.mundell_fleming("fixed", dm=1.0)["y"] == 0


def test_dornbusch_overshoots_and_converges():
    D = openecon.dornbusch(0.10, lam=4.0, theta=0.5, T=40.0, n=801)
    assert D["jump"] == pytest.approx(0.15) and D["factor"] == pytest.approx(1.5)
    assert D["s"][-1] == pytest.approx(0.10, abs=1e-6) and D["p"][-1] == pytest.approx(0.10, abs=1e-6)
    s, p, i = map(np.array, (D["s"], D["p"], D["i"]))
    assert np.all(np.diff(s) < 0) and np.all(np.diff(p) > 0) and i[0] == pytest.approx(-0.10 / 4)
    # interest parity along the path: the expected appreciation equals the interest gap
    ds = np.gradient(s, D["t"])
    assert np.allclose(ds[5:-5], i[5:-5], atol=1e-3)


def test_krugman_attack_timing():
    K = openecon.krugman_attack(100, 60, 2, 5, 25)
    assert K["T_attack"] == 15 and K["T_exhaust"] == 20 and K["jump_reserves"] == 10
    t, s, r = map(np.array, (K["t"], K["s"], K["reserves"]))
    assert np.all(s[t < 15] == 100) and np.all(r[t >= 15] == 0)
    j = np.searchsorted(t, 15)
    assert s[j] == pytest.approx(100)                           # no jump in the rate: the attack is not a surprise


def test_obstfeld_regions():
    R = openecon.obstfeld_regions(1.0, 1.0, 0.5)
    assert (R["safe_below"], R["doomed_above"]) == (0.5, 1.0)
    for u, out in ((0.3, ("defend", "defend")), (0.75, ("defend", "abandon")), (1.2, ("abandon", "abandon"))):
        assert tuple(openecon.obstfeld_outcome(u, e) for e in (False, True)) == out


def test_passthrough_recovers_planted_lags():
    rng = np.random.default_rng(3)
    e = rng.normal(0, 0.02, 600)
    w = np.r_[0.1, 0.1, 0.1, np.zeros(10)]
    p = np.convolve(e, w)[:600] + rng.normal(0, 0.001, 600)
    P = openecon.passthrough(p, e, lags=12)
    assert P["impact"] == pytest.approx(0.1, abs=0.02) and P["long_run"] == pytest.approx(0.3, abs=0.03)
