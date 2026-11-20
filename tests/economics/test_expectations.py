"""Agora's expectations (Part 28): Phillips's curve, acceleration, adaptive forecasts, Lucas's islands, the critique,
Barro-Gordon and Rogoff, the sacrifice ratio."""

import numpy as np

from explainer.economics.agora import expectations as ex


def test_phillips_1958():
    # wages stable near 5.5% unemployment; about 1.8% a year at 2.5%
    assert abs(ex.phillips1958(5.5)) < 0.01
    assert abs(ex.phillips1958(2.5) - 1.79) < 0.01
    assert ex.phillips1958(10.0) > -0.9           # the curve never falls below -0.9


def test_acceleration():
    a = ex.accelerate(years=10, ustar=5, u_target=4, beta=0.5, lam=1.0, pi0=2.0)
    assert np.allclose(np.diff(a["pi"]), 0.5)
    slow = ex.accelerate(years=40, ustar=5, u_target=4, beta=0.5, lam=0.3, pi0=2.0)
    d = np.diff(slow["pi"])
    assert np.allclose(d[5:], 0.3 * 0.5)             # it still climbs, every year, by lam * beta * (u* - u)


def test_adaptive_forecasts():
    x = [1.0, 2.0, 3.0, 4.0]
    f = ex.adaptive_forecasts(x, 1.0)
    assert f["forecast"] == [1.0, 2.0, 3.0] and np.allclose(f["error"], 1.0)
    g = ex.adaptive_forecasts([2.0] * 10, 0.3)
    assert g["rmse"] == 0.0


def test_lucas_islands_signal_extraction():
    assert abs(ex.signal_extraction(1.0, 1.0) - 0.5) < 1e-12
    calm = ex.lucas_islands(1.0, 0.5, years=400, seed=1)
    wild = ex.lucas_islands(1.0, 3.0, years=400, seed=1)
    assert abs(calm["slope"] - 0.8) < 0.05 and abs(wild["slope"] - 0.1) < 0.02


def test_critique():
    c = ex.critique(seed=2, years=400)
    assert abs(c["slope"] - 2.0) < 0.2                 # the old rule's data show a trade-off
    assert c["predicted"] > 100 + 6                     # which predicts a gain from the new rule
    assert abs(c["actual"] - 100) < 0.5                 # that never comes


def test_barro_gordon_and_rogoff():
    g = ex.barro_gordon(1.0, 2.0, 1.0)
    assert g["pi_discretion"] == 2.0 and g["loss_discretion"] > g["loss_rule"] > g["loss_cheat"]
    r = ex.conservative_banker(1.0, 2.0, 2.0, 1.0)
    assert 0 < r["best"] < 1.0 and r["best_loss"] < min(r["loss_at_lam"], r["loss_at_zero"])
    # Monte Carlo check of society's loss at the best weight
    rng = np.random.default_rng(0)
    e = rng.normal(0, 2.0, 400_000)
    w = r["best"]
    pi = w * 2.0 - (w / (1 + w)) * e
    y = (pi - w * 2.0) + e
    loss = np.mean(0.5 * pi ** 2 + 0.5 * (y - 2.0) ** 2)
    assert abs(loss - r["best_loss"]) < 0.03


def test_sacrifice_ratio():
    s = ex.sacrifice_ratio([-2, -4, -3, -1], 9.0, 4.0)
    assert s["lost"] == 10 and s["fall"] == 5 and s["ratio"] == 2.0


def test_persistence():
    rng = np.random.default_rng(3)
    x = np.zeros(5000)
    for t in range(1, len(x)):
        x[t] = 0.8 * x[t - 1] + rng.normal()
    assert abs(ex.persistence(x) - 0.8) < 0.03
