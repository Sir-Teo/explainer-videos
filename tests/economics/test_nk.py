"""Agora's sticky prices (Part 30): menu costs, Calvo's slope, determinacy, the three-equation model's solution,
optimal policy, the zero bound, the hybrid model and the selection effect."""

import numpy as np
import pytest

from explainer.economics.agora import nk


def test_menu_cost_is_second_order_for_the_firm():
    m = nk.menu_cost(6.0, (0.01, 0.02))
    a, b = m["rows"]
    assert m["markup"] == pytest.approx(1.2)
    assert a["profit_loss"] == pytest.approx(6 * 5 * 0.01 ** 2 / 2, rel=0.05)
    assert b["profit_loss"] / a["profit_loss"] == pytest.approx(4, rel=0.05)      # quadratic
    assert b["output_loss"] / a["output_loss"] == pytest.approx(2, rel=0.05)      # linear


def test_kappa_matches_gali_and_falls_with_stickiness():
    assert nk.kappa(2 / 3, 0.99, 1, 1, 1 / 3, 6) == pytest.approx(0.1275)
    ks = [nk.kappa(t) for t in (0.5, 0.67, 0.8)]
    assert ks[0] > ks[1] > ks[2] > 0
    d = nk.calvo_durations(2 / 3)
    assert d["mean_months"] == pytest.approx(9.0)
    assert nk.theta_from_monthly(d["monthly_frequency"]) == pytest.approx(2 / 3)


def test_taylor_principle():
    k = nk.kappa(2 / 3, 0.99, 1, 1, 1 / 3, 6)
    for fp, fx in ((1.5, 0.125), (1.01, 0.0), (0.99, 0.0), (0.9, 0.5), (0.5, 0.125)):
        d = nk.determinacy(fp, fx, 0.99, 1.0, k)
        assert d["unique"] == d["condition"]
    assert nk.determinacy(1.5, 0.125, kap=k)["unique"]
    assert not nk.determinacy(0.8, 0.125, kap=k)["unique"]


def test_irfs_solve_the_model():
    kw = {"theta": 2 / 3, "alpha": 1 / 3}
    p = nk._params(**kw)
    for shock in ("monetary", "demand", "cost"):
        r = nk.irf_ar1(shock, rho_s=0.5, size=1.0, **kw)
        x, pi = np.array(r["x"]), np.array(r["pi"]) / 4
        i = np.array(r["i"]) / 4
        u = 0.25 * 0.5 ** np.arange(len(x)) if shock == "cost" else 0 * x
        rn = 0.25 * 0.5 ** np.arange(len(x)) if shock == "demand" else 0 * x
        # the Phillips curve and the IS curve hold with expectations 0.5 times today's values
        assert np.allclose(pi, p["beta"] * 0.5 * pi + p["kappa"] * x + u, atol=1e-12)
        assert np.allclose(x, 0.5 * x - (i - 0.5 * pi - rn) / p["sigma"], atol=1e-12)
    m = nk.irf_ar1("monetary", rho_s=0.5, size=1.0, **kw)
    assert m["x"][0] < 0 and m["pi"][0] < 0 and m["i"][0] > 0


def test_klein_matches_undetermined_coefficients():
    kw = {"theta": 2 / 3, "alpha": 1 / 3}
    h = nk.hybrid_irf(rho_v=0.5, size=1.0, periods=8, **kw)
    a = nk.irf_ar1("monetary", rho_s=0.5, size=1.0, periods=8, **kw)
    assert h["bk_ok"]
    assert np.allclose(h["x"], a["x"], atol=1e-9) and np.allclose(h["pi"], a["pi"], atol=1e-9)
    rich = nk.hybrid_irf(habit=0.9, index=0.9, smooth=0.8, rho_v=0.5, size=1.0, periods=12, **kw)
    assert rich["peak_x"] >= 1                                                    # a hump


def test_commitment_beats_discretion_and_returns_the_price_level():
    o = nk.optimal_policy(rho_u=0.5, size=1.0, periods=40, theta=2 / 3, alpha=1 / 3)
    assert o["loss_c"] < o["loss_d"]
    assert abs(o["price_c"][-1]) < 1e-3 < o["price_d"][-1]
    assert 0 < o["delta"] < 1


def test_zero_bound_and_forward_guidance():
    kw = {"theta": 2 / 3, "alpha": 1 / 3}
    z0 = nk.zlb(T=6, rn_low=-2.0, extra=0, **kw)
    z2 = nk.zlb(T=6, rn_low=-2.0, extra=2, **kw)
    assert z0["x"][0] < 0 and z0["pi"][0] < 0
    assert z2["x"][0] > z0["x"][0]
    assert all(v == 0 for v in z0["i"][:6])
    fg = nk.forward_guidance_puzzle(horizons=(1, 4, 8), cut=1.0, **kw)["rows"]
    assert fg[0]["x0"] < fg[1]["x0"] < fg[2]["x0"]
    flat = nk.forward_guidance_puzzle(horizons=(1, 8), cut=1.0, kappa=0.0)["rows"]
    assert flat[0]["x0"] == pytest.approx(flat[1]["x0"])                          # kappa = 0: no growth


def test_selection_effect():
    c = nk.price_setters("calvo", n=6000, months=12, freq=0.1, shock=0.05, sigma_a=0.04, seed=1)
    m = nk.price_setters("menu", n=6000, months=12, freq=0.1, shock=0.05, sigma_a=0.04, seed=1)
    assert np.mean(c["resets"][3:]) == pytest.approx(0.1, abs=0.02)
    assert c["pass_through"][0] == pytest.approx(0.1, abs=0.03)
    assert m["pass_through"][0] > 3 * c["pass_through"][0]
    assert m["pass_through"][-1] > 0.95
