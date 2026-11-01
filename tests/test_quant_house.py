"""The House's library: every desk's tools checked against independent results (python -m pytest tests/test_quant_house.py)."""

import numpy as np
import pytest

from explainer.quant.house import bs, hedge, paths, trees


def test_put_call_parity():
    S, K, T, s, r, q = 100.0, np.array([80, 100, 125.0]), 0.7, 0.3, 0.04, 0.01
    c = bs.price(S, K, T, s, r, q, 1)
    p = bs.price(S, K, T, s, r, q, -1)
    assert np.allclose(c - p, S * np.exp(-q * T) - K * np.exp(-r * T), atol=1e-12)


def test_greeks_match_finite_differences():
    S, K, T, s, r, q = 103.0, 100.0, 0.5, 0.25, 0.03, 0.02
    for cp in (1, -1):
        g = bs.greeks(S, K, T, s, r, q, cp)
        h = 1e-4
        f = lambda **kw: bs.price(**{"S": S, "K": K, "T": T, "sigma": s, "r": r, "q": q, "cp": cp, **kw})
        assert g["delta"] == pytest.approx((f(S=S + h) - f(S=S - h)) / (2 * h), rel=1e-6)
        assert g["gamma"] == pytest.approx((f(S=S + h) - 2 * f() + f(S=S - h)) / h ** 2, rel=1e-4)
        assert g["vega"] == pytest.approx((f(sigma=s + h) - f(sigma=s - h)) / (2 * h), rel=1e-6)
        assert g["theta"] == pytest.approx(-(f(T=T + h) - f(T=T - h)) / (2 * h), rel=1e-5)
        assert g["rho"] == pytest.approx((f(r=r + h) - f(r=r - h)) / (2 * h), rel=1e-5)


def test_black_scholes_pde():
    """Theta + (r - q) S Delta + 1/2 sigma^2 S^2 Gamma - r V = 0."""
    S = np.linspace(50, 150, 11)
    g = bs.greeks(S, 100.0, 0.8, 0.35, 0.05, 0.02, 1)
    lhs = g["theta"] + (0.05 - 0.02) * S * g["delta"] + 0.5 * 0.35 ** 2 * S ** 2 * g["gamma"] - 0.05 * g["price"]
    assert np.allclose(lhs, 0, atol=1e-10)


def test_implied_vol_round_trip():
    rng = np.random.default_rng(1)
    n = 4000
    S = 100.0
    K = S * np.exp(rng.uniform(-1.2, 1.2, n))
    T = rng.uniform(0.01, 3.0, n)
    sig = rng.uniform(0.03, 2.0, n)
    cp = rng.choice([-1, 1], n)
    p = bs.price(S, K, T, sig, 0.02, 0.0, cp)
    intrinsic = np.maximum(cp * (S - K * np.exp(-0.02 * T)), 0)
    keep = p - intrinsic > 1e-9 * S  # a time value below this carries no information about sigma in doubles
    iv = bs.implied_vol(p[keep], S, K[keep], T[keep], 0.02, 0.0, cp[keep])
    assert np.nanmax(np.abs(iv - sig[keep])) < 1e-7
    assert np.isnan(bs.implied_vol(150.0, 100.0, 100.0, 1.0))  # above the no-arbitrage bound


def test_crr_converges_and_american_put():
    exact = float(bs.price(100, 100, 1.0, 0.2, 0.05, 0.0, 1))
    errs = [abs(trees.crr(100, 100, 1.0, 0.2, 0.05, N=N)["price"] - exact) for N in (50, 200, 800)]
    assert errs[2] < errs[0] and errs[2] < 5e-3
    am = trees.crr(100, 100, 1.0, 0.2, 0.05, N=800, cp=-1, american=True, boundary=True)
    eu = float(bs.price(100, 100, 1.0, 0.2, 0.05, 0.0, -1))
    assert am["price"] > eu + 0.2  # the early-exercise premium of a 1-year put at 5%
    assert am["price"] == pytest.approx(6.09, abs=0.01)  # the standard benchmark, 6.0904
    b = am["boundary"][~np.isnan(am["boundary"])]
    assert np.all(b < 100) and b[-1] > b[0]  # the boundary rises towards the strike near expiry
    # an American call on a non-dividend stock is never exercised early
    amc = trees.crr(100, 100, 1.0, 0.2, 0.05, N=400, cp=1, american=True)["price"]
    assert amc == pytest.approx(trees.crr(100, 100, 1.0, 0.2, 0.05, N=400, cp=1)["price"], abs=1e-12)


def test_gbm_and_heston_moments():
    t, S = paths.gbm(100, 0.0, 0.2, 1.0, 50, 200_000, seed=3)
    assert S[:, -1].mean() == pytest.approx(100, rel=3e-3)
    assert np.log(S[:, -1]).std() == pytest.approx(0.2, rel=1e-2)
    t, S, v = paths.heston(100, 0.04, 2.0, 0.04, 0.5, -0.7, 1.0, 100, 100_000, seed=4)
    assert S[:, -1].mean() == pytest.approx(100, rel=5e-3)  # a martingale (mu = 0)
    assert v.mean(axis=0)[-1] == pytest.approx(0.04, rel=3e-2)
    assert v.min() >= 0


def test_hedge_accounting_identity_and_convergence():
    t, S = paths.gbm(100, 0.05, 0.2, 0.5, 200, 4000, seed=5)
    out = hedge.delta_hedge(t, S, 100, 0.5, 0.2, position=-1, record=[0, 1])
    # at r = q = 0 the final P&L is the edge plus the marked-to-market steps, exactly
    assert np.allclose(out["pnl"], out["edge"] + out["mtm"] - out["cost_total"], atol=1e-9)
    # hedging at the true volatility: P&L ~ 0 with a spread that halves when the steps are cut by four
    sd = []
    for n in (50, 200):
        t, S = paths.gbm(100, 0.05, 0.2, 0.5, n, 20000, seed=6)
        p = hedge.delta_hedge(t, S, 100, 0.5, 0.2, position=-1)["pnl"]
        assert abs(p.mean()) < 0.03
        sd.append(p.std())
    assert sd[1] / sd[0] == pytest.approx(0.5, rel=0.12)
    # the gamma-theta terms explain the marked P&L up to a small residual
    assert np.std(out["residual_total"]) < 0.2 * np.std(out["mtm"])


def test_hedge_variance_pnl_sign():
    """Long gamma hedged at 20% on paths realizing 30% makes money; on paths realizing 10% loses it."""
    for real, sign in ((0.3, 1), (0.1, -1)):
        t, S = paths.gbm(100, 0.0, real, 0.5, 250, 4000, seed=7)
        p = hedge.delta_hedge(t, S, 100, 0.5, 0.2, position=1)["pnl"]
        assert np.sign(p.mean()) == sign


def test_hedge_with_rates_and_carry():
    t, S = paths.gbm(100, 0.03 - 0.01, 0.25, 1.0, 400, 20000, seed=8)  # risk-neutral drift r - q
    p = hedge.delta_hedge(t, S, 100, 1.0, 0.25, position=-1, r=0.03, q=0.01)["pnl"]
    assert abs(p.mean()) < 0.03 and p.std() < 0.6
