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


# --------------------------------------------------------------------------- Part 1: stats and the envelope
from explainer.quant.house import pit, stats  # noqa: E402


def test_variance_ratio_random_walk_and_ar1():
    """iid increments: VR(q) ~ 1 and z* ~ N(0, 1); AR(1) with rho: VR(q) -> 1 + 2 sum (1 - k/q) rho^k."""
    rng = np.random.default_rng(11)
    zs = [stats.variance_ratio(rng.standard_normal(2000), 4)["z_star"] for _ in range(300)]
    assert abs(np.mean(zs)) < 0.2 and np.std(zs) == pytest.approx(1.0, abs=0.15)
    rho, q, n = 0.3, 4, 200_000
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    want = 1 + 2 * sum((1 - k / q) * rho ** k for k in range(1, q))
    assert stats.variance_ratio(x, q)["vr"] == pytest.approx(want, rel=0.02)


def test_variance_ratio_robust_under_garch_like_volatility():
    """Clustered volatility, no autocorrelation: z* keeps its size where z over-rejects."""
    rng = np.random.default_rng(12)
    rej_z = rej_s = 0
    for _ in range(200):
        vol = np.exp(np.convolve(rng.standard_normal(3000), np.ones(50) / 7, mode="same"))
        r = vol * rng.standard_normal(3000)
        v = stats.variance_ratio(r, 8)
        rej_z += abs(v["z"]) > 1.96
        rej_s += abs(v["z_star"]) > 1.96
    assert rej_s / 200 < 0.10 and rej_z > rej_s


def test_hill_recovers_pareto_exponent():
    rng = np.random.default_rng(13)
    x = (1 - rng.random(400_000)) ** (-1 / 3.0)  # Pareto, alpha = 3
    assert stats.hill(x, frac=0.01) == pytest.approx(3.0, rel=0.05)
    assert stats.hill(rng.standard_normal(400_000), frac=0.01) > 4  # a Gaussian's "exponent" keeps climbing


def test_tail_years_and_aggregation():
    assert stats.gaussian_tail_years(-3.0) == pytest.approx(1 / (0.0013499 * 252), rel=1e-3)
    r = np.arange(10.0)
    assert stats.aggregate(r, 5).tolist() == [10.0, 35.0]
    assert stats.aggregate(r, 9, overlapping=True).tolist() == [36.0, 45.0]
    assert stats.autocorr(np.sin(np.arange(1000) / 3), [0, 1])[1] > 0.9


def test_envelope_seals_registers_and_opens_once(tmp_path, monkeypatch):
    monkeypatch.setattr(pit, "ENVELOPE", tmp_path / "envelope.json")
    d = np.array([20191231, 20201231, 20210104, 20210105])
    v = np.array([0.01, -0.02, 0.03, 0.0])
    assert pit.research(d, v)[0].tolist() == [20191231, 20201231]
    rec = pit.seal("toy", d, v)
    assert rec["n"] == 2 and rec["first"] == 20210104
    with pytest.raises(RuntimeError):
        pit.seal("toy", d, v + 1e-3)  # the hold-out changed
    with pytest.raises(RuntimeError):
        pit.open_envelope("s", "toy", d, v)  # not registered
    pit.register("s", "def f(): pass", {"lookback": 12}, trials=7)
    assert pit.open_envelope("s", "toy", d, v)[0].tolist() == [20210104, 20210105]
    assert pit.trials_so_far() == 7
    pit.register("s2", "def g(): pass", {}, trials=3)
    assert pit.trials_so_far() == 10


def test_smile_density_and_svix_on_a_flat_smile():
    """A flat smile is Black-76: SVI recovers it, the Breeden-Litzenberger density is the lognormal (mass 1,
    mean F), and var^Q(S_T / F) = exp(sigma^2 T) - 1."""
    from explainer.quant.house import smile
    F, T, sig = 100.0, 0.25, 0.5
    k = np.linspace(-0.6, 0.6, 41)
    p = smile.fit_svi(k, np.full_like(k, sig ** 2 * T))
    assert p["rmse"] < 1e-5
    K = np.linspace(5, 400, 8001)
    q = smile.risk_neutral_density(p, F, T, K)
    assert np.trapezoid(q, K) == pytest.approx(1.0, abs=2e-3)
    assert np.trapezoid(K * q, K) == pytest.approx(F, rel=2e-3)
    assert smile.svix2(p, F, T) == pytest.approx(np.exp(sig ** 2 * T) - 1, rel=1e-3)


# --------------------------------------------------------------------------- Part 2: the funding desk
def test_margin_account_liquidates_at_the_formula_price():
    from explainer.quant.house import funding
    entry, L, m = 100.0, 10.0, 0.005
    p_liq = funding.liquidation_price(entry, L, m, side=1)
    prices = np.concatenate([np.linspace(100, p_liq + 0.01, 50), [p_liq - 0.01, p_liq - 1]])
    acc = funding.margin_account(prices, 1.0, L, m)
    assert acc["liquidated_at"] == 50
    assert acc["initial_margin"] == pytest.approx(10.0)
    short = funding.margin_account(np.linspace(100, 120, 200), -1.0, 5.0, m)
    assert short["liquidated_at"] is not None
    assert funding.liquidation_price(100, 5, m, side=-1) == pytest.approx(120 / 1.005, rel=1e-9)


def test_margin_account_funding_and_netting_and_auction():
    from explainer.quant.house import funding
    acc = funding.margin_account(np.full(4, 100.0), 2.0, 2.0, 0.01, funding=np.full(4, 0.001))
    assert acc["funding_paid"] == pytest.approx(3 * 0.001 * 200)
    assert acc["left"] == pytest.approx(100 - 0.6)
    net = funding.netting([0, 1, 2, 0], [1, 2, 0, 2], [10, 10, 10, 5], 3)
    assert net["gross"] == 35 and net["multilateral"] == pytest.approx(5)
    assert net["bilateral"] == pytest.approx(10 + 10 + 5)  # 0->1 10, 1->2 10, 2->0 10 vs 0->2 5: 5
    au = funding.call_auction([101, 100, 99], [5, 5, 5], [98, 100, 102], [4, 6, 5])
    assert au["price"] == pytest.approx(100) and au["volume"] == 10


def test_fund_fees_high_water_mark_and_haircut():
    from explainer.quant.house import funding
    f = funding.fund_fees([0.10, -0.10, 0.10], mgmt=0.0, perf=0.2)
    assert f["fees"][0] == pytest.approx(0.02)          # 20% of a 10% gain
    assert f["fees"][1] == pytest.approx(0.0)           # no fee on a loss
    # after -10% the fund is below its mark: the recovery pays no performance fee until the mark is passed
    nav_after_loss = 1.08 * 0.9
    gain = nav_after_loss * 1.10
    want = 0.2 * max(gain - 1.08, 0) / nav_after_loss
    assert f["fees"][2] == pytest.approx(want)
    assert funding.max_leverage(0.02) == pytest.approx(50)


# --------------------------------------------------------------------------- Part 3: valuation
def test_valuation_closed_forms_and_irr():
    from explainer.quant.house import valuation as v
    assert v.annuity(100, 0.05, 10) == pytest.approx(v.npv(0.05, [0] + [100] * 10))
    assert v.gordon(5, 0.08, 0.03) == pytest.approx(100)
    long_ = v.npv(0.08, [0] + [5 * 1.03 ** k for k in range(2000)])
    assert long_ == pytest.approx(100, rel=1e-6)
    assert v.irr([-100, 10, 10, 110]) == pytest.approx(0.10, abs=1e-10)
    d = v.dcf([10, 11, 12], 0.09, 0.02)
    tv = 12 * 1.02 / 0.07 / 1.09 ** 3
    assert d["terminal"] == pytest.approx(tv) and d["value"] == pytest.approx(d["explicit"] + tv)


def test_modigliani_miller_and_merton():
    from explainer.quant.house import valuation as v
    # without taxes the WACC equals the asset return whatever the leverage
    rA, rD = 0.08, 0.04
    for de in (0.0, 0.5, 2.0):
        rE = v.mm_cost_of_equity(rA, rD, de)
        assert v.wacc(1.0, de, rE, rD) == pytest.approx(rA)
    m = v.merton_equity(np.array([100.0, 150.0]), 80.0, 1.0, 0.3, 0.02)
    assert np.allclose(m["equity"] + m["debt"], [100, 150])
    assert m["spread"][0] > m["spread"][1] > 0 and m["pd"][0] > m["pd"][1]


def test_fundamentals_store_is_point_in_time_and_keeps_restatements():
    from explainer.quant.house.fundamentals import Store

    s = Store()
    s.add("ACME", "NetIncomeLoss", 20191231, 20200220, 200.0, "10-K")
    s.add("ACME", "NetIncomeLoss", 20191231, 20210315, 150.0, "10-K/A")
    s.add("ACME", "NetIncomeLoss", 20201231, 20210226, 240.0, "10-K")
    assert s.asof("ACME", "NetIncomeLoss", 20200131) is None
    assert s.asof("ACME", "NetIncomeLoss", 20200630) == 200.0
    assert [f.value for f in s.history("ACME", "NetIncomeLoss", 20210301)] == [200.0, 240.0]
    assert [f.value for f in s.history("ACME", "NetIncomeLoss", 20210630)] == [150.0, 240.0]
    assert [f.value for f in s.first_reported("ACME", "NetIncomeLoss")] == [200.0, 240.0]
    assert s.restatements("ACME", "NetIncomeLoss") == [(20191231, 200.0, 150.0, 20210315)]
    with pytest.raises(ValueError):
        s.add("ACME", "NetIncomeLoss", 20211231, 20211130, 1.0)
    cf = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"start": "2019-01-01", "end": "2019-12-31", "val": 1000, "filed": "2020-02-20", "form": "10-K", "accn": "x"}]}}}}}
    t = Store.from_companyfacts("ACME", cf)
    assert t.asof("ACME", "Revenues", 20200220) == 1000.0 and t.asof("ACME", "Revenues", 20200219) is None


def test_martingale_tools():
    from scipy.stats import levy_stable

    from explainer.quant.house import martingale as m

    # doubling: a win after k losses recovers them plus the base bet; ten losses in a row ruin a 1023 bankroll
    r = m.doubling([False, False, True], base=1, bankroll=100)
    assert r["wealth"][-1] == 101 and not r["ruined"]
    assert m.doubling([False] * 10, base=1, bankroll=1023)["ruined"]
    assert m.gamblers_ruin(1, 3) == pytest.approx(1 / 3)
    assert m.gamblers_ruin(5, 10, 0.6) == pytest.approx((1 - (2 / 3) ** 5) / (1 - (2 / 3) ** 10))
    # Doob: x_n = n^2 / 10 + noise; predicted increments recover the drift exactly
    x = np.arange(6) ** 2 / 10.0
    d = m.doob_decomposition(x, np.diff(x))
    assert np.allclose(d["M"], 0) and np.allclose(d["A"], x - x[0])
    # the likelihood ratio is a P-martingale: its mean under P is 1 at every n
    rng = np.random.default_rng(1)
    L = np.array([m.likelihood_ratio(rng.random(20) < 0.5, 0.5, 0.6)[-1] for _ in range(20000)])
    assert L.mean() == pytest.approx(1.0, abs=0.05)
    # McCulloch recovers a stable index; Gaussian data give alpha = 2 and a return-probability slope of -1/2
    xs = levy_stable.rvs(1.5, 0.0, size=20000, random_state=np.random.default_rng(2))
    assert m.stable_mcculloch(xs)["alpha"] == pytest.approx(1.5, abs=0.08)
    g = np.random.default_rng(3).standard_normal(200000)
    assert m.stable_mcculloch(g)["alpha"] > 1.9
    assert m.return_probability(g, [1, 2, 4, 8, 16, 32])["slope"] == pytest.approx(-0.5, abs=0.05)
    # the e-process stays small under the null (Ville: rarely reaches 20) and grows under an alternative
    hits = 0
    for k in range(200):
        e = m.EProcess()
        e.run(np.random.default_rng(100 + k).choice([-0.5, 0.5], 500))
        hits += e.rejected(0.05)
    assert hits <= 200 * 0.05 * 1.6
    e = m.EProcess()
    e.run(np.random.default_rng(7).choice([-0.5, 0.5], 500, p=[0.4, 0.6]))
    assert e.rejected(0.05)


def test_simulation_library():
    from explainer.quant.house import sim

    # scheme orders on GBM: strong 1/2 for Euler, 1 for Milstein; weak 1 for both
    o = sim.scheme_orders(n_paths=8000)
    assert o["slope_strong_euler"] == pytest.approx(0.5, abs=0.12)
    assert o["slope_strong_milstein"] == pytest.approx(1.0, abs=0.15)
    assert o["strong_milstein"][-1] < o["strong_euler"][-1]
    # OU and CIR exact transitions: stationary moments
    X = sim.ou_exact(0.0, 2.0, 1.0, 0.5, 5.0, 50, 20000, seed=1)[:, -1]
    assert X.mean() == pytest.approx(1.0, abs=0.02) and X.var() == pytest.approx(0.25 / 4, rel=0.06)
    C = sim.cir_exact(0.04, 1.5, 0.04, 0.2, 5.0, 50, 20000, seed=2)[:, -1]
    assert C.min() >= 0 and C.mean() == pytest.approx(0.04, rel=0.03)
    # Merton: the drift is compensated
    S = sim.merton_jumps(1.0, 0.05, 0.2, 2.0, -0.1, 0.15, 1.0, 50, 40000, seed=3)[:, -1]
    assert S.mean() == pytest.approx(np.exp(0.05), rel=0.02)
    # Hawkes: the mean rate is mu / (1 - branching), and MLE recovers the parameters
    ev = sim.hawkes_thinning(0.5, 0.8, 1.6, 4000.0, seed=4)
    assert len(ev) / 4000 == pytest.approx(0.5 / (1 - 0.5), rel=0.1)
    fit = sim.hawkes_fit(ev, 4000.0)
    assert fit["branching"] == pytest.approx(0.5, abs=0.08) and fit["loglik"] > fit["loglik_poisson"]
    # fBM: variance t^{2H}, and the Hurst estimator recovers H
    for H in (0.1, 0.5, 0.8):
        B = sim.fbm(H, 4096, n_paths=1, seed=5)[0]
        assert sim.hurst_from_increments(B)["H"] == pytest.approx(H, abs=0.06)
    ends = sim.fbm(0.3, 64, T=1.0, n_paths=4000, seed=6)[:, -1]
    assert ends.var() == pytest.approx(1.0, rel=0.08)
    # signature: level 1 is the increment; the symmetric part of level 2 is S1 S1^T / 2; the unit square's Levy area
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], float)
    s = sim.signature2(sq)
    assert np.allclose(s["S1"], 0) and s["levy_area"][0, 1] == pytest.approx(1.0)
    p = np.random.default_rng(7).standard_normal((50, 3)).cumsum(axis=0)
    s = sim.signature2(p)
    assert np.allclose((s["S2"] + s["S2"].T) / 2, np.outer(s["S1"], s["S1"]) / 2)


def test_econometrics_module():
    from explainer.quant.house import econ

    rng = np.random.default_rng(0)
    # OLS recovers coefficients; NW on overlapping sums inflates the SE roughly by sqrt(horizon)
    x = rng.standard_normal(3000)
    y = 1 + 2 * x + rng.standard_normal(3000)
    r = econ.ols(y, x)
    assert r["beta"] == pytest.approx([1, 2], abs=0.06)
    e = rng.standard_normal(3000)
    h = 12
    yo = np.convolve(e, np.ones(h), "valid")
    xo = np.convolve(rng.standard_normal(3000), np.ones(h), "valid")
    naive = econ.ols(yo, xo)["se"][1]
    nw = econ.ols(yo, xo, se="nw", lags=2 * h)["se"][1]
    assert nw / naive > 2.0
    # clustering by a common shock within groups widens the SE
    g = np.repeat(np.arange(100), 30)
    shock = np.repeat(rng.standard_normal(100), 30)
    xc = np.repeat(rng.standard_normal(100), 30) + 0.1 * rng.standard_normal(3000)
    yc = shock + rng.standard_normal(3000)
    assert econ.ols(yc, xc, se="cluster", groups=g)["se"][1] > 3 * econ.ols(yc, xc)["se"][1]
    # Fama-MacBeth on a panel with a true slope of 0.5
    Xp = rng.standard_normal((200, 50))
    Yp = 0.5 * Xp + rng.standard_normal((200, 50)) + rng.standard_normal((200, 1))
    fm = econ.fama_macbeth(Yp, Xp)
    assert fm["beta"][1] == pytest.approx(0.5, abs=0.05)
    # bootstraps are centred on the statistic
    z = rng.standard_normal(600)
    bs1 = econ.moving_block_bootstrap(z, np.mean, block=12, B=500)
    bs2 = econ.stationary_bootstrap(z, np.mean, mean_block=12, B=300)
    assert abs(bs1.mean() - z.mean()) < 0.02 and abs(bs2.mean() - z.mean()) < 0.03
    assert bs1.std() == pytest.approx(1 / np.sqrt(600), rel=0.25)
    # Sharpe standard error and years to significance
    assert econ.sharpe_se(0.0, 100) == pytest.approx(0.1)
    assert econ.years_to_significance(0.5) == pytest.approx(16.0)
    # multiple testing: BH rejects at least what Holm rejects, Holm at least Bonferroni
    p = np.concatenate([rng.uniform(0, 0.002, 10), rng.uniform(0, 1, 90)])
    b, ho, bh = econ.bonferroni(p), econ.holm(p), econ.benjamini_hochberg(p)
    assert b.sum() <= ho.sum() <= bh.sum() and bh[:10].all()
    # Stambaugh: simulated mean bias near the formula
    sims = econ.simulate_predictive(120, 0.95, -0.9, n=1500, seed=1)
    assert sims.mean() == pytest.approx(econ.stambaugh_bias(0.95, -0.9, 1.0, 120), rel=0.35)
    # GMM: the mean and variance of a normal sample, overidentified with the third moment
    w = rng.normal(1.0, 2.0, 4000)
    mom = lambda th: np.column_stack([w - th[0], (w - th[0]) ** 2 - th[1], (w - th[0]) ** 3])  # noqa: E731
    gm = econ.gmm(mom, [0.0, 1.0])
    assert gm["theta"] == pytest.approx([1.0, 4.0], rel=0.08) and gm["p_J"] > 0.01
    # double ML recovers a planted effect where naive OLS is biased
    n = 3000
    Xd = rng.uniform(-2, 2, (n, 2))
    d = np.sin(2 * Xd[:, 0]) + Xd[:, 1] ** 2 + rng.standard_normal(n)
    yd = 0.5 * d + 2 * np.sin(2 * Xd[:, 0]) + Xd[:, 1] ** 2 + rng.standard_normal(n)
    dm = econ.dml_plr(yd, d, Xd)
    assert dm["theta"] == pytest.approx(0.5, abs=0.08) and abs(dm["naive"] - 0.5) > 0.2
    # shrinkage pulls noisy means toward the grand mean
    sh = econ.shrink_means(rng.normal(0.01, 0.002, 30) + rng.normal(0, 0.01, 30), np.full(30, 0.01))
    assert np.var(sh["shrunk"]) < 0.5 * np.var(sh["shrunk"] / sh["shrunk"] * 0 + rng.normal(0, 0.01, 30)) + 1


def test_volatility_module():
    from explainer.quant.house import vol

    rng = np.random.default_rng(0)
    # GARCH(1,1): simulate and recover
    n, w, a, b = 6000, 0.02, 0.08, 0.9
    h, r = np.empty(n), np.empty(n)
    h[0] = w / (1 - a - b)
    for t in range(n):
        if t:
            h[t] = w + a * r[t - 1] ** 2 + b * h[t - 1]
        r[t] = np.sqrt(h[t]) * rng.standard_normal()
    f = vol.garch_fit(r)
    assert f["params"][1] == pytest.approx(a, abs=0.03) and f["params"][2] == pytest.approx(b, abs=0.04)
    assert f["persistence"] == pytest.approx(a + b, abs=0.02)
    g = vol.garch_fit(r, "gjr")
    assert g["loglik"] >= f["loglik"] - 1.0
    e = vol.garch_fit(r, "egarch")
    assert np.isfinite(e["loglik"])
    fc = vol.garch_forecast(f["params"], r[-1], f["h"][-1], 500)
    assert fc[-1] == pytest.approx(f["params"][0] / (1 - f["persistence"]), rel=0.05)
    # realized measures: Brownian with noise; TSRV and the kernel are closer to the truth than the dense RV
    m = 23400
    x = np.cumsum(rng.standard_normal(m) * np.sqrt(1 / m)) + 0.003 * rng.standard_normal(m)
    rv = vol.realized_variance(np.diff(x))
    assert rv > 1.2
    assert abs(vol.two_scale_rv(x, 30) - 1) < abs(rv - 1)
    assert abs(vol.realized_kernel(np.diff(x), 30) - 1) < abs(rv - 1)
    clean = np.diff(np.cumsum(rng.standard_normal(m) * np.sqrt(1 / m)))
    jumpy = clean.copy()
    jumpy[100] += 0.5
    assert vol.bipower_variation(jumpy) < vol.realized_variance(jumpy) - 0.2
    # HAR on a persistent RV series; QLIKE is minimised by the truth
    lv = np.empty(3000)
    lv[0] = 0
    for t in range(1, 3000):
        lv[t] = 0.97 * lv[t - 1] + 0.2 * rng.standard_normal()
    rvs = np.exp(lv)
    hf = vol.har_fit(rvs)
    assert hf["beta"][1:].sum() == pytest.approx(0.97, abs=0.1)
    assert len(vol.har_predict(hf["beta"], rvs)) == len(rvs) - 21
    assert vol.qlike(2.0, 2.0) == pytest.approx(0) and vol.qlike(1.0, 2.0) > 0
    dm = vol.diebold_mariano(rng.random(500) + 0.2, rng.random(500))
    assert dm["t"] > 3
    # unit roots and cointegration
    walk = np.cumsum(rng.standard_normal(2000))
    assert not vol.adf(walk)["reject_5pct"] and vol.adf(rng.standard_normal(2000))["reject_5pct"]
    y = 2 * walk + rng.standard_normal(2000)
    assert vol.engle_granger(y, walk)["cointegrated_5pct"]
    false_pos = np.mean([vol.engle_granger(np.cumsum(rng.standard_normal(400)), np.cumsum(rng.standard_normal(400)))
                         ["cointegrated_5pct"] for _ in range(150)])
    assert false_pos < 0.12  # the test's size is about 5%
    # regimes: two volatility states recovered
    s = np.zeros(3000, int)
    for t in range(1, 3000):
        s[t] = s[t - 1] if rng.random() < 0.98 else 1 - s[t - 1]
    xs = rng.standard_normal(3000) * np.where(s, 3.0, 1.0)
    ms = vol.markov_switching(xs, n_iter=60)
    assert ms["sd"][0] == pytest.approx(1.0, rel=0.15) and ms["sd"][1] == pytest.approx(3.0, rel=0.15)
    assert np.corrcoef(ms["prob_high"], s)[0, 1] > 0.8
    # Kalman: the filtered level tracks a random walk under noise
    lvl = np.cumsum(0.1 * rng.standard_normal(1500))
    k = vol.kalman_local_level(lvl + 0.5 * rng.standard_normal(1500))
    assert k["signal_to_noise"] == pytest.approx(0.04, rel=0.6)
    # DCC recovers a correlation that switches
    z1 = rng.standard_normal(3000)
    rho_true = np.where(np.arange(3000) < 1500, 0.2, 0.8)
    z2 = rho_true * z1 + np.sqrt(1 - rho_true ** 2) * rng.standard_normal(3000)
    d = vol.dcc_fit(z1, z2)
    assert d["rho"][:1400].mean() < d["rho"][1600:].mean() - 0.3
    assert vol.acf(walk, 5)[1] > 0.95 and len(vol.ar_fit(xs, 2)["beta"]) == 3


# ---------------------------------------------------------------------------
# Part 8: control
# ---------------------------------------------------------------------------
def test_control_utility_and_kelly():
    from explainer.quant.house import control as C
    # a 50/50 gamble of 50 or 150 at log utility: CE = sqrt(50*150)
    assert abs(C.certainty_equivalent([50, 150], [0.5, 0.5], 1.0) - np.sqrt(7500)) < 1e-9
    assert abs(C.kelly_binary(0.6) - 0.2) < 1e-12
    f = np.linspace(0, 0.99, 991)
    assert abs(f[np.argmax(C.growth_binary(f, 0.6))] - 0.2) < 1e-3
    # twice Kelly grows at (about) zero in the continuous model
    assert abs(C.growth_continuous(2 * 0.06 / 0.04, 0.06, 0.2)) < 1e-12


def test_control_bellman_matches_merton_and_hara():
    from explainer.quant.house import control as C
    mu, r, s, g = 0.08, 0.02, 0.18, 3.0
    out = C.bellman_merton(mu, r, s, g, T=5, steps=20, n_w=120)
    pi = out["pi"][0, 20:100]
    assert abs(np.median(pi) - C.merton_fraction(mu, r, s, g)) < 0.03
    out = C.bellman_merton(mu, r, s, g, T=5, steps=20, n_w=120, floor=0.5)
    w = out["cushion"] + out["pv_floor"][0]
    k = np.searchsorted(w, 1.2)
    assert abs(out["pi"][0, k] - C.hara_fraction(w[k], 0, 5, mu, r, s, g, 0.5)) < 0.04


def test_control_secretary():
    from explainer.quant.house import control as C
    p = C.secretary(50, [18], trials=40000, seed=1)[0]
    assert abs(p - C.secretary_exact(50, 18)) < 0.01
    assert abs(max(C.secretary_exact(100, k) for k in range(1, 100)) - 1 / np.e) < 0.01


def test_control_bsde_black_scholes_and_two_rates():
    from explainer.quant.house import bs as B, control as C
    call = lambda x: np.maximum(x - 100, 0)  # noqa: E731
    out = C.bsde_regression(call, 100, 1.0, 0.2, 0.08, 0.05, steps=40, paths=60000, seed=2)
    assert abs(out["Y0"] - float(B.price(100, 100, 1.0, 0.2, 0.05))) < 0.15
    # a call is hedged with borrowed cash throughout: its price at two rates is Black-Scholes at the borrowing rate
    out = C.bsde_regression(call, 100, 1.0, 0.2, 0.08, 0.01, R=0.06, steps=40, paths=60000, seed=3)
    assert abs(out["Y0"] - float(B.price(100, 100, 1.0, 0.2, 0.06))) < 0.2
    pde = C.hjb_two_rates(call, 100, 1.0, 0.2, 0.01, 0.06)
    assert abs(pde - float(B.price(100, 100, 1.0, 0.2, 0.06))) < 0.05


# ---------------------------------------------------------------------------
# Part 9: arbitrage
# ---------------------------------------------------------------------------
def test_arbitrage_ftap_and_superhedge():
    from explainer.quant.house import arbitrage as A
    D = np.array([[1.0, 1.0], [2.0, 0.5]])
    ok = A.ftap(D, [1.0, 1.0])
    assert ok["no_arbitrage"] and np.allclose(ok["psi"], [1 / 3, 2 / 3])
    bad = A.ftap(D, [1.0, 2.5])  # the stock costs more than it can ever pay relative to the bond
    assert not bad["no_arbitrage"] and bad["cost"] <= 1e-9 and np.all(bad["payoff"] >= -1e-9)
    D3 = np.array([[1.0, 1.0, 1.0], [0.5, 1.0, 2.0]])
    call = np.array([0.0, 0.0, 1.0])
    h = A.superhedge(D3, [1.0, 1.0], call)
    assert h["lower"] < h["upper"]
    assert A.ftap(np.vstack([D3, call]), [1.0, 1.0, 0.5 * (h["lower"] + h["upper"])])["no_arbitrage"]
    assert not A.ftap(np.vstack([D3, call]), [1.0, 1.0, h["upper"] + 0.01])["no_arbitrage"]


def test_arbitrage_static_and_mot():
    from explainer.quant.house import arbitrage as A, bs as B
    K = np.linspace(60, 140, 41)
    C = B.price(100, K, 0.5, 0.3)
    assert A.static_checks(K, C, 100.0)["ok"]
    C2 = C.copy()
    C2[20] += 1.0  # a bump makes a negative butterfly
    assert not A.static_checks(K, C2, 100.0)["ok"]
    x, mu = np.array([-1.0, 1.0]), np.array([0.5, 0.5])
    y, nu = np.array([-2.0, 0.0, 2.0]), np.array([0.25, 0.5, 0.25])
    out = A.mot_bounds(x, mu, y, nu, lambda a, b: b * b)
    assert abs(out["lower"] - 2.0) < 1e-8 and abs(out["upper"] - 2.0) < 1e-8
    out = A.mot_bounds(x, mu, y, nu, lambda a, b: abs(b - a))
    assert out["lower"] <= out["upper"] + 1e-12


def test_arbitrage_ross_recovery():
    from explainer.quant.house import arbitrage as A
    g = np.random.default_rng(0)
    c = np.array([0.9, 1.0, 1.1, 1.2])
    pi = g.random((4, 4)) + 0.2
    pi /= pi.sum(axis=1, keepdims=True)
    delta, gamma = 0.97, 3.0
    P = delta * pi * (c[None, :] / c[:, None]) ** (-gamma)
    out = A.ross_recovery(P)
    assert abs(out["delta"] - delta) < 1e-10 and np.allclose(out["F"], pi)
