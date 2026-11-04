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


# ---------------------------------------------------------------------------
# Part 11: quoting
# ---------------------------------------------------------------------------
def test_quoting_book_and_surfaces():
    from explainer.quant.house import bs as B, quoting as Q
    st = Q.strategies(100.0, 0.25)
    g = Q.book_greeks(st["straddle"], 100.0, 0.2)
    assert abs(g["delta"]) < 0.06 and g["gamma"] > 0 and g["vega"] > 0 and g["theta"] < 0
    rr = Q.book_greeks(st["risk reversal"], 100.0, 0.2)
    assert rr["delta"] > 0 and abs(rr["vega"]) < 0.25 * g["vega"]
    surf = Q.pnl_surface(st["straddle"], 100.0, 0.2, [-0.1, 0.0, 0.1], [-0.05, 0.0, 0.05], 1 / 365)
    assert surf[1, 1] < 0 < surf[1, 0] and surf[2, 1] > 0  # theta bleeds at rest; moves and vol pay
    # implied correlation: two equal stocks of 30% vol at weight 1/2, index at 30% means correlation 1
    assert abs(Q.implied_correlation(0.3, [0.5, 0.5], [0.3, 0.3]) - 1.0) < 1e-12
    assert abs(Q.implied_correlation(0.3 / np.sqrt(2), [0.5, 0.5], [0.3, 0.3])) < 1e-12
    q = Q.quote(0.5, inventory_vega=10, half_spread=0.01, skew_per_vega=0.001)
    assert q["mid"] < 0.5 and q["ask"] - q["bid"] > 0.019


def test_quoting_band_hedging_costs():
    from explainer.quant.house import quoting as Q
    g = np.random.default_rng(5)
    n, paths = 250, 2000
    t = np.linspace(0, 1.0, n + 1)
    z = g.standard_normal((paths, n))
    S = 100 * np.exp(np.column_stack([np.zeros(paths), np.cumsum(-0.02 * (1 / n) + 0.2 * np.sqrt(1 / n) * z, axis=1)]))
    every = Q.hedge_with_band(t, S, 100, 1.0, 0.2, cost=0.002, band_half=0.0)
    band = Q.hedge_with_band(t, S, 100, 1.0, 0.2, cost=0.002, band_half=None, gamma_risk=1.0)
    assert band["cost"].mean() < every["cost"].mean() and band["trades"].mean() < every["trades"].mean()


# ---------------------------------------------------------------------------
# Part 12: the surface builder
# ---------------------------------------------------------------------------
def test_volsurface_flat_and_ssvi():
    from explainer.quant.house import bs as B, volsurface as V
    # flat 20% vol: the variance swap and the VIX formula both recover 0.2; local vol is flat
    F, T = 100.0, 0.25
    K = np.linspace(20, 300, 2801)
    otm = np.where(K < F, B.price(F, K, T, 0.2, cp=-1), B.price(F, K, T, 0.2, cp=1))
    assert abs(np.sqrt(V.var_swap_strike(K, otm, F, T)) - 0.2) < 2e-3
    Kv = np.arange(50, 200.5, 2.5)
    assert abs(V.vix(Kv, B.price(F, Kv, T, 0.2, cp=1), B.price(F, Kv, T, 0.2, cp=-1), F, T) - 0.2) < 5e-3
    f = lambda k, t: 0.04 * t + 0 * k  # noqa: E731
    w, dw, d2w, dT = V.numeric_derivs(f, np.array([0.0, 0.2]), 0.5)
    assert np.allclose(V.dupire_local_var(np.array([0.0, 0.2]), w, dw, d2w, dT), 0.04)
    # SSVI with eta (1 + |rho|) <= 2 has g >= 0 (no butterfly arbitrage)
    k = np.linspace(-1.5, 1.5, 301)
    g_ = V.g_function(k, *V.numeric_derivs(lambda kk, t: V.ssvi_w(kk, 0.04, -0.4, 1.2, 0.5), k, 0.5)[:3])
    assert g_.min() > 0
    # fit SSVI back from its own quotes
    Ts = np.repeat([0.1, 0.5, 1.0], 25)
    kk = np.tile(np.linspace(-0.5, 0.5, 25), 3)
    th = np.repeat([0.01, 0.045, 0.09], 25)
    wq = V.ssvi_w(kk, th, -0.35, 1.1, 0.45)
    fit = V.fit_ssvi(kk, Ts, wq)
    assert fit["rmse"] < 1e-4 and abs(fit["rho"] + 0.35) < 0.02


# ---------------------------------------------------------------- stochvol (Part 13)


def test_cos_heston_benchmark():
    from explainer.quant.house import stochvol as sv

    # Fang and Oosterlee (2008), Table 4: reference 5.785155435
    cf = lambda u, T: sv.heston_cf(u, T, 0.0175, 1.5768, 0.0398, 0.5751, -0.5711)  # noqa: E731
    assert abs(sv.cos_price(cf, 100.0, 100.0, 1.0, 1)[0] - 5.785155435) < 1e-6


def test_cos_matches_black_and_martingales():
    from explainer.quant.house import bs, stochvol as sv

    K = np.array([60.0, 80, 100, 120, 150])
    for T in (2 / 365, 0.5):
        for cp in (1, -1):
            p = sv.cos_price(lambda u, TT: sv.bs_cf(u, TT, 0.6), 100.0, K, T, cp)
            assert np.allclose(p, bs.black(100.0, K, T, 0.6, cp=cp), atol=1e-9)
    one = np.array([-1j])
    for cf in (lambda u: sv.vg_cf(u, 0.5, 0.5, 0.2, -0.1), lambda u: sv.nig_cf(u, 0.5, 5, -1, 1),
               lambda u: sv.bates_cf(u, 0.5, 0.2, 2, 0.2, 1, -0.2, 1, -0.05, 0.1),
               lambda u: sv.kou_jump_cf(u, 0.5, 1, 0.4, 10, 5)):
        assert abs(cf(one)[0] - 1) < 1e-12


def test_qe_and_levy_simulation_match_cos():
    from explainer.quant.house import stochvol as sv

    p = (0.0175, 1.5768, 0.0398, 0.5751, -0.5711)
    S = sv.heston_qe(100, *p, 1.0, 50, 100_000, seed=1)
    ref = sv.cos_price(lambda u, T: sv.heston_cf(u, T, *p), 100.0, 100.0, 1.0, 1)[0]
    pay = np.maximum(S[-1] - 100, 0)
    assert abs(pay.mean() - ref) < 4 * pay.std() / np.sqrt(len(pay))
    V = sv.vg_paths(100, 0.5, 0.2, -0.1, 0.5, 20, 100_000, seed=2)
    ref = sv.cos_price(lambda u, T: sv.vg_cf(u, T, 0.5, 0.2, -0.1), 100.0, 110.0, 0.5, 1)[0]
    pay = np.maximum(V[-1] - 110, 0)
    assert abs(pay.mean() - ref) < 4 * pay.std() / np.sqrt(len(pay))


def test_sabr_atm_and_calibration_roundtrip():
    from explainer.quant.house import stochvol as sv

    # at the money with beta = 1 and no vol of vol, Hagan's vol is alpha
    assert abs(sv.sabr_iv(1.0, 1.0, 0.5, 0.4, 1.0, 0.0, 1e-8)[0] - 0.4) < 1e-6
    # Heston round trip: synthetic quotes from known parameters are recovered to a small error
    x = (0.25, 3.0, 0.3, 1.2, -0.4)
    T = np.repeat([30 / 365, 90 / 365, 180 / 365], 9)
    K = np.tile(np.exp(np.linspace(-0.3, 0.3, 9)), 3)
    iv = np.concatenate([sv.surface_iv("Heston", x, 1.0, K[T == t], t) for t in np.unique(T)])
    Q = {"F": np.ones_like(K), "K": K, "T": T, "iv": iv, "cp": np.where(K >= 1, 1, -1),
         "vega": np.ones_like(K)}
    r = sv.calibrate("Heston", Q)
    assert r["rmse"] < 0.05


def test_theta_at_and_local_vol_paths_reprice():
    from explainer.quant.house import bs as B, volsurface as V

    fit = {"T": np.array([0.1, 0.3]), "theta": np.array([0.016, 0.048]), "rho": -0.3, "eta": 0.6, "gamma": 0.5}
    # linear from zero, and the last forward variance carried past the last expiry
    assert np.allclose(V.theta_at(fit, [0.05, 0.2, 0.5]), [0.008, 0.032, 0.08])
    X = V.local_vol_paths(fit, 73, 40_000, seed=3)
    T = 73 / 365
    for k in (-0.15, 0.0, 0.15):
        cp = 1 if k >= 0 else -1
        p = np.mean(np.maximum(cp * (np.exp(X[-1]) - np.exp(k)), 0))
        iv = B.implied_vol(p, 1.0, np.exp(k), T, 0.0, 0.0, cp)
        assert abs(iv - np.sqrt(V.ssvi_surface_w(fit, k, T) / T)) < 0.01


# ---------------------------------------------------------------- rough (Part 14)


def test_rough_heston_reduces_to_heston_and_lift_is_close():
    from explainer.quant.house import rough as R, stochvol as sv

    u = np.array([0.5, 1.0, 3.0, -1j])
    a = R.rough_heston_cf(u, 1.0, 0.04, 1.5, 0.05, 0.4, -0.6, H=0.5, n=200)
    assert np.abs(a - sv.heston_cf(u, 1.0, 0.04, 1.5, 0.05, 0.4, -0.6)).max() < 1e-5
    r = R.rough_heston_cf(u, 1.0, 0.04, 1.5, 0.05, 0.4, -0.6, H=0.1, n=400)
    assert abs(r[-1] - 1) < 1e-10  # the martingale condition, phi(-i) = 1
    lift = R.lifted_heston_cf(u, 1.0, 0.04, 1.5, 0.05, 0.4, -0.6, H=0.1, N=50)
    assert np.abs(lift - r).max() < 3e-3


def test_rbergomi_martingale_and_skew_decay():
    from explainer.quant.house import rough as R

    S = R.rbergomi_paths(0.1, 1.9, -0.9, 0.235 ** 2, 0.5, 182, 20_000, seed=2)
    assert abs(S[-1].mean() - 1) < 4 * S[-1].std() / np.sqrt(S.shape[1])


def test_roughness_estimator_and_pdv_recovery():
    from explainer.quant.house import rough as R, sim

    x = sim.fbm(0.15, 20_000, 1.0, 1, seed=4)
    x = np.asarray(x).ravel()
    assert abs(R.log_rv_scaling(x)["H"] - 0.15) < 0.03
    g = np.random.default_rng(5)
    r = 0.03 * g.standard_normal(3000)
    R1, R2 = R.pdv_features(r, 1 / 365, 1.5, 0.05, 1.8, 0.03, lookback=600)
    vol = 0.1 - 0.05 * R1 + 0.9 * np.sqrt(R2) + 0.002 * g.standard_normal(3000)
    f = R.fit_pdv(r, vol, lookback=600, burn=600)
    assert f["r2"] > 0.95 and abs(f["beta"][2] - 0.9) < 0.1


# ---------------------------------------------------------------- exotics (Part 15)


def test_barriers_parity_and_bgk():
    from explainer.quant.house import bs as B, exotics as X

    S, K, H, T, s, r = 100.0, 100.0, 85.0, 0.5, 0.3, 0.02
    # in + out = vanilla (puts), and a down-and-out call is a vanilla minus its reflection
    P = X.gbm_paths(S, s, T, 2000, 60_000, r, seed=1)
    kin = P.min(axis=0) <= H
    mc = np.exp(-r * T) * np.maximum(K - P[-1], 0)
    assert abs(X.down_in_put(S, K, H, T, s, r) - mc[kin].sum() / len(mc)) < 0.15
    assert abs(X.down_out_call(S, K, H, T, s, r) - X.down_out_call(S, K, H, T, s, r)) == 0
    assert X.down_out_call(S, K, H, T, s, r) < B.price(S, K, T, s, r)
    # discrete monitoring (50 dates) matches the continuous formula with the shifted barrier
    alive = P[::40].min(axis=0) > H
    mcd = np.exp(-r * T) * np.mean(np.maximum(P[-1] - K, 0) * alive)
    assert abs(X.down_out_call(S, K, X.bgk_barrier(H, S, s, T / 50), T, s, r) - mcd) < 0.15


def test_asian_lookback_digital_uvm():
    from explainer.quant.house import bs as B, exotics as X

    S, K, T, s, r = 100.0, 100.0, 0.5, 0.3, 0.02
    P = X.gbm_paths(S, s, T, 500, 60_000, r, seed=2)
    geo = np.exp(np.log(P[10::10]).mean(axis=0))
    assert abs(X.geometric_asian_call(S, K, T, s, 50, r) - np.exp(-r * T) * np.mean(np.maximum(geo - K, 0))) < 0.1
    assert abs(X.lookback_floating_call(S, T, s, 0.0) - X.lookback_floating_call(S, T, s, 1e-5)) < 1e-3
    assert X.call_spread_digital(S, K, T, s, 1.0, r) > X.digital_call(S, K, T, s, r)
    grid = np.linspace(1, 300, 300)
    v = X.uvm_price(lambda x: np.maximum(x - K, 0), grid, T, s, s, r)
    assert abs(np.interp(S, grid, v) - B.price(S, K, T, s, r)) < 0.02
    # a convex payoff's upper UVM price is Black-Scholes at the top volatility
    v2 = X.uvm_price(lambda x: np.maximum(x - K, 0), grid, T, 0.2, 0.4, r)
    assert abs(np.interp(S, grid, v2) - B.price(S, K, T, 0.4, r)) < 0.03


def test_snowball_coupon_in_range():
    from explainer.quant.house import exotics as X

    c = X.fair_coupon(0.22, n_paths=20_000)
    assert 0.08 < c < 0.25
    assert X.snowball_price(0.22, coupon=c + 0.05, n_paths=20_000) > 1.0


# ---------------------------------------------------------------- engine (Part 16)


def test_engine_mc_variance_reduction_and_qmc():
    from explainer.quant.house import bs as B, engine as E

    ex = B.price(100.0, 100.0, 1.0, 0.2, 0.05)
    p, se = E.mc_call(100, 100, 1, 0.2, 0.05, 100_000, "plain")
    pc, sec = E.mc_call(100, 100, 1, 0.2, 0.05, 100_000, "control")
    assert abs(p - ex) < 4 * se and abs(pc - ex) < 4 * sec and sec < se / 2
    pi, sei = E.mc_call(100, 160, 1, 0.2, 0.05, 100_000, "is")
    assert abs(pi - B.price(100.0, 160.0, 1.0, 0.2, 0.05)) < 4 * sei and sei < 0.002
    vals = [E.asian_call_paths(100, 100, 1, 0.2, 0.05, 4096, 64, "sobol", True, seed=i) for i in range(6)]
    assert np.std(vals) < 0.02


def test_engine_american_bounds_and_fd():
    from explainer.quant.house import engine as E

    lo, coefs = E.lsm_put(100, 100, 1, 0.2, 0.05, 25, 60_000, return_policy=True)
    hi, se = E.andersen_broadie_put(100, 100, 1, 0.2, 0.05, coefs, n_steps=25, n_outer=200, n_inner=800, seed=3)
    fd = E.fd_american_put(100, 100, 1, 0.2, 0.05, nS=150, nt=150)
    assert lo - 0.05 < fd < hi + 3 * se + 0.05


def test_engine_greeks_aad_adi_fourier():
    from explainer.quant.house import engine as E, stochvol as sv

    g = E.greeks_three_ways(100, 100, 1, 0.2, 0.05, 100_000)
    assert abs(g["pathwise"]["delta"] - g["likelihood ratio"]["delta"]) < 0.02
    a = E.aad_greeks(100, 100, 1, 0.2, 0.05, 5000, 20)
    for k in a["aad"]:
        assert abs(a["aad"][k] - a["bump"][k]) < 0.01 * max(1, abs(a["bump"][k]))
    cf = lambda u, T: sv.heston_cf(u, T, 0.04, 1.5, 0.04, 0.5, -0.7)  # noqa: E731
    ref = sv.cos_price(cf, 100.0, 100.0, 1.0, 1)[0]
    assert abs(E.heston_adi(100, 100, 1.0, 0.04, 1.5, 0.04, 0.5, -0.7, nS=80, nv=40, nt=40) - ref) < 0.03
    k, C = E.carr_madan(cf, 100.0, 1.0)
    assert abs(np.interp(100.0, k, C) - ref) < 0.01


def test_simulation_library_part5_second_pass():
    from scipy.stats import norm

    from explainer.quant.house import sim

    # Levy's construction: each level refines the last, and the increments of the finest level have variance 2^-k
    lv = sim.levy_construction(10, seed=1)
    assert np.allclose(lv[10][::2], lv[9]) and len(lv[10]) == 2 ** 10 + 1
    inc = np.concatenate([np.diff(sim.levy_construction(8, seed=s)[8]) for s in range(200)])
    assert inc.var() == pytest.approx(2 ** -8, rel=0.05)
    # signature: Chen's loop agrees with signature2; the batch version agrees with the loop; the unit square's area
    p = np.random.default_rng(3).standard_normal((30, 2)).cumsum(axis=0)
    S = sim.signature(p, 3)
    assert np.allclose(S[2], sim.signature2(p)["S2"])
    assert np.allclose(sim.signature_batch(p[None], 3)[0], np.concatenate([s.ravel() for s in S[1:]]))
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], float)
    S = sim.signature(sq, 2)
    assert (S[2][0, 1] - S[2][1, 0]) / 2 == pytest.approx(1.0)
    # local time of Brownian motion at 0 by t = 1 has mean sqrt(2/pi)
    _, W = sim.brownian(1.0, 2000, 4000, seed=4)
    L = sim.local_time(W, 0.0, 0.03)[:, -1]
    assert L.mean() == pytest.approx(np.sqrt(2 / np.pi), rel=0.05)
    # Hawkes time-rescaling: the compensator's gaps are Exp(1)
    ev = sim.hawkes_thinning(0.5, 0.8, 1.6, 3000.0, seed=5)
    g = np.diff(sim.hawkes_compensator(ev, 0.5, 0.8, 1.6))
    assert g.mean() == pytest.approx(1.0, abs=0.05) and g.var() == pytest.approx(1.0, abs=0.12)
    tr = sim.hawkes_thinning_trace(0.5, 0.8, 1.6, 500.0, seed=6)
    assert np.all(tr["lam"] <= tr["bound"] + 1e-12) and 0 < tr["accepted"].mean() < 1
    cl = sim.hawkes_clusters(0.5, 0.5, 1.6, 4000.0, seed=7)
    assert len(cl["t"]) / 4000 == pytest.approx(1.0, rel=0.1) and np.all(np.diff(cl["t"]) >= 0)
    assert np.all(cl["parent"] < np.arange(len(cl["t"])))
    # CIR: exact MLE recovers the parameters of a simulated sample
    x = sim.cir_exact(0.04, 0.5, 0.05, 0.08, 400.0, 4800, 1, seed=8)[0]
    f = sim.cir_mle(x, 400.0 / 4800, [0.3, 0.03, 0.1])
    assert f["kappa"] == pytest.approx(0.5, rel=0.3) and f["theta"] == pytest.approx(0.05, rel=0.1)
    assert f["sigma"] == pytest.approx(0.08, rel=0.05) and len(f["iterates"]) > 10
    # importance-sampled digital: unbiased, and far tighter than plain Monte Carlo
    m, se, _ = sim.is_digital(100.0, 160.0, 0.2, 1.0, 40000, seed=9)
    d2 = (np.log(100 / 160) - 0.02) / 0.2
    assert m == pytest.approx(norm.cdf(d2), abs=4 * se) and se < 0.0002
    # Heston full truncation: E v_T and the martingale S
    S, v = sim.heston_euler(100.0, 0.09, 2.0, 0.04, 0.5, -0.7, 1.0, 200, 20000, seed=10)
    assert v[:, -1].mean() == pytest.approx(0.04 + 0.05 * np.exp(-2.0), rel=0.05)
    assert S[:, -1].mean() == pytest.approx(100.0, rel=0.01)


def test_martingale_part4_expansion():
    import itertools

    from explainer.quant.house import martingale as m

    # conditional expectation on a partition agrees with brute force, and is the L2 projection
    x, p = np.array([3.0, 0.0, 1.0]), np.array([0.5, 0.3, 0.2])
    y = m.cond_exp(x, np.array([0, 0, 1]), p)
    assert np.allclose(y, [1.875, 1.875, 1.0])
    assert abs(((x - y) * p * np.array([1.0, 1.0, 0.0])).sum()) < 1e-12  # the error is orthogonal to G
    # pattern waits (Li 1980) and Penney's game against simulation
    assert m.pattern_wait("HH") == 6 and m.pattern_wait("HT") == 4 and m.pattern_wait("HTH") == 10
    assert m.pattern_wait("ABRACADABRA", 26) == 26 ** 11 + 26 ** 4 + 26
    assert m.penney_odds("HHT", "THH") == pytest.approx(0.75)
    # first passage: P(tau_1 > n) = P(S_n in {0, 1}), checked by enumeration for n = 6
    n = 6
    count = sum(1 for s in itertools.product((-1, 1), repeat=n) if max(np.cumsum(s)) < 1)
    assert m.first_passage_survival(n) == pytest.approx(count / 2 ** n)
    # every system pays the same tax per unit staked on roulette (stakes are predictable)
    rng = np.random.default_rng(0)
    W = rng.random((4000, 100)) < 18 / 37
    for s in ("flat", "dalembert", "labouchere", "oscar"):
        H = m.system_stakes(s, W, limit=50)
        g = (np.where(W, 1, -1) * H).sum(1)
        assert abs(g.mean() / H.sum(1).mean() + 1 / 37) < 0.01
    # Polya's urn: the red fraction is a martingale (mean stays 1/2)
    P = m.polya_urn(200, n_urns=4000, seed=1)
    assert abs(P[:, -1].mean() - 0.5) < 0.02
    # upcrossings: Doob's inequality holds path by path
    walk = np.concatenate([[0.0], np.cumsum(rng.choice([-1.0, 1.0], 2000))])
    u = m.upcrossings(walk, -2, 2)
    assert 4 * u["U"] <= u["wealth"][-1] + max(-2 - walk[-1], 0) + 1e-9
    # the Esscher tilt hits its target; Hellinger affinity of equal coins is 1
    xs = rng.standard_normal(5000) * 0.01 + 0.0004
    th, w = m.esscher_tilt(xs, 0.0001)
    assert abs(np.log(w @ np.exp(xs)) - 0.0001) < 1e-10
    assert m.hellinger_affinity(0.5, 0.5) == pytest.approx(1.0) and m.hellinger_affinity(0.5, 0.6) < 1
    # the ECF regression finds alpha = 2 for Gaussian data
    assert abs(m.ecf_alpha(rng.standard_normal(20000))["alpha"] - 2) < 0.1
    # the ONS bettor is anytime-valid under the null: false alarms at 1/alpha stay below alpha
    b = m.ONSBettor(2000)
    mx = np.zeros(2000)
    for _ in range(500):
        mx = np.maximum(mx, b.update(rng.choice([-0.5, 0.5], 2000)))
    assert (mx >= 20).mean() <= 0.05
    g = m.AGrapaBettor(500)
    for _ in range(2000):
        wg = g.update(np.clip(0.1 + 0.3 * rng.standard_normal(500), -0.99, 0.99))
    assert np.median(wg) > 20  # a real edge is found
    # e-BH reduces to BH on calibrated e = 1/p
    pv = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216])
    bh = np.flatnonzero(np.sort(pv) <= 0.1 * np.arange(1, 11) / 10)
    assert len(m.e_bh(1 / pv, 0.1)) == bh.max() + 1
    # a betting confidence sequence covers the mean of a fair coin
    cs = m.betting_cs(rng.random(400) < 0.5, np.linspace(0.01, 0.99, 99))
    assert cs["lower"][-1] <= 0.5 <= cs["upper"][-1]


# ---------------------------------------------------------------------------
# Part 7 (extended): time-series tools of the volatility forecaster
def test_ljung_box_and_arma_recover_truth():
    from explainer.quant.house import vol
    rng = np.random.default_rng(0)
    e = rng.standard_normal(4000)
    assert vol.ljung_box(e, 10)["p"] > 0.01
    x = np.zeros(4000)
    for t in range(1, 4000):
        x[t] = 0.6 * x[t - 1] + e[t] + 0.3 * e[t - 1]
    assert vol.ljung_box(x, 10)["p"] < 1e-6
    f = vol.arma_fit(x, 1, 1)
    assert abs(f["phi"][0] - 0.6) < 0.05 and abs(f["theta"][0] - 0.3) < 0.06
    assert vol.ljung_box(f["resid"], 10)["p"] > 0.01
    assert f["aic"] < vol.arma_fit(x, 1, 0)["aic"]


def test_dickey_fuller_distribution():
    from explainer.quant.house import vol
    t = vol.df_simulate(250, 8000, seed=1)
    assert abs(np.quantile(t, 0.05) - (-2.87)) < 0.08  # MacKinnon: -2.87 at T = 250, constant
    assert np.mean(t) < -1.3


def test_johansen_finds_one_cointegrating_vector():
    from explainer.quant.house import vol
    rng = np.random.default_rng(2)
    n = 3000
    trend = np.cumsum(rng.standard_normal(n))
    u = np.zeros(n)
    for t in range(1, n):
        u[t] = 0.7 * u[t - 1] + rng.standard_normal()
    X = np.column_stack([trend + 0.5 * rng.standard_normal(n), 2 * trend + u, np.cumsum(rng.standard_normal(n))])
    j = vol.johansen(X, k=2)
    assert j["rank"] == 1
    b = j["beta"][:, 0] / j["beta"][0, 0]
    assert abs(b[1] + 0.5) < 0.05 and abs(b[2]) < 0.05
    ecm = vol.ecm_fit(X[:, 1], X[:, 0])
    assert ecm["alpha_y"] < 0


def test_hamilton_filter_matches_markov_switching_and_kalman_gain():
    from explainer.quant.house import vol
    rng = np.random.default_rng(3)
    s = np.zeros(2000, int)
    for t in range(1, 2000):
        s[t] = s[t - 1] if rng.random() < (0.98 if s[t - 1] == 0 else 0.9) else 1 - s[t - 1]
    x = np.where(s == 0, 0.01 + 0.03 * rng.standard_normal(2000), -0.02 + 0.09 * rng.standard_normal(2000))
    ms = vol.markov_switching(x, n_iter=60)
    hf = vol.hamilton_filter(x, ms["mu"], ms["sd"], ms["P"])
    assert np.mean((hf["filt"][:, 1] > 0.5) == (s == 1)) > 0.9
    k = vol.kalman_states(np.cumsum(rng.standard_normal(500)) + rng.standard_normal(500), q=0.5, r=1.0)
    assert abs(k["K"][-1] - vol.steady_gain(0.5)) < 1e-6


def test_sv_qml_and_t_garch_recover_parameters():
    from explainer.quant.house import vol
    rng = np.random.default_rng(4)
    n = 6000
    h = np.zeros(n)
    for t in range(1, n):
        h[t] = -9 + 0.97 * (h[t - 1] + 9) + 0.2 * rng.standard_normal()
    h[0] = -9
    r = np.exp(h / 2) * rng.standard_normal(n)
    sv = vol.sv_qml(r)
    assert abs(sv["phi"] - 0.97) < 0.03 and abs(sv["sigma_eta"] - 0.2) < 0.08 and abs(sv["mu"] + 9) < 0.3
    z = rng.standard_t(6, n) / np.sqrt(6 / 4)
    hh = np.empty(n)
    rr = np.empty(n)
    hh[0] = 1e-4
    for t in range(n):
        if t:
            hh[t] = 1e-6 + 0.08 * rr[t - 1] ** 2 + 0.9 * hh[t - 1]
        rr[t] = np.sqrt(hh[t]) * z[t]
    g = vol.garch_t_fit(rr)
    assert 4 < g["nu"] < 9 and abs(g["params"][1] - 0.08) < 0.03


def test_nelson_boundary_and_news_impact():
    from explainer.quant.house import vol
    assert vol.nelson_elog(0.3, 0.75) < 0 < vol.nelson_elog(0.25, 0.80) + 0.02
    assert vol.nelson_elog(0.1, 0.9) < 0  # IGARCH: strictly stationary
    rng = np.random.default_rng(5)
    z = rng.standard_normal(2_000_000)
    assert abs(vol.nelson_elog(0.3, 0.75) - np.mean(np.log(0.3 * z ** 2 + 0.75))) < 3e-3
    ni = vol.news_impact((1e-6, 0.02, 0.1, 0.9), "gjr", np.array([-0.02, 0.02]), 1e-4)
    assert ni[0] > ni[1]


def test_signature_and_bns_jump_test():
    from explainer.quant.house import vol
    rng = np.random.default_rng(6)
    n = 1440
    x = np.cumsum(rng.standard_normal(n) * 0.001)
    sig = vol.signature_plot(x + 0.0005 * rng.standard_normal(n), (1, 5, 30))
    assert sig[0] > sig[1] > 0 and sig[0] > 1.3 * sig[2]
    zs = [vol.bns_jump_z(rng.standard_normal(288)) for _ in range(400)]
    assert abs(np.mean(np.array(zs) > 2.33) - 0.01) < 0.03
    r = rng.standard_normal(288) * 0.001
    r[100] += 0.02
    assert vol.bns_jump_z(r) > 3


def test_mincer_zarnowitz_and_mcs():
    from explainer.quant.house import vol
    rng = np.random.default_rng(7)
    f = np.exp(rng.standard_normal(1000))
    y = f * np.exp(0.3 * rng.standard_normal(1000) - 0.045)
    mz = vol.mincer_zarnowitz(f, y)
    assert abs(mz["b"] - 1) < 0.1
    L = np.column_stack([rng.standard_normal(500) + 1.0, rng.standard_normal(500) + 1.02, rng.standard_normal(500) + 2.0])
    m = vol.model_confidence_set(L, ["a", "b", "c"], B=500)
    assert "c" in m["eliminated"] and "a" in m["survivors"]


def test_vol_target_vra_and_forecast():
    from explainer.quant.house import vol
    rng = np.random.default_rng(8)
    s = np.where(np.arange(4000) % 1000 < 500, 0.005, 0.02)
    r = s * rng.standard_normal(4000)
    vt = vol.vol_target(r, 0.10, com=20)
    sc = vt["scaled"][200:]
    assert abs(np.std(sc) * np.sqrt(252) - 0.10) < 0.02
    lam = vol.vra(np.column_stack([r, r]), np.full((4000, 2), 0.01))
    assert lam[450] < 1 < lam[950]  # calm block (vol 0.5%), then a stormy one (2%), against forecasts of 1%
    rv = np.exp(np.convolve(rng.standard_normal(1200), np.ones(20) / 4, "same") - 8)
    fc = vol.forecast(rv, 22)
    assert len(fc["daily"]) == 22 and np.all(fc["daily"] > 0)


# --------------------------------------------------------------------------- Part 2, expanded
def test_min_var_hedge_and_carry():
    from explainer.quant.house import funding
    rng = np.random.default_rng(2)
    dF = rng.standard_normal(200000)
    dS = 0.96 * dF + 0.28 * rng.standard_normal(200000)  # rho = 0.96 / sqrt(0.96^2 + 0.28^2) = 0.96
    h, eff = funding.min_var_hedge(dS, dF)
    assert h == pytest.approx(0.96, abs=0.01) and eff == pytest.approx(0.96 ** 2, abs=0.01)
    assert funding.hedge_effectiveness(dS, dF, 0.0) == pytest.approx(0.0)
    assert funding.implied_carry(100 * np.exp(0.03 * 0.5), 100, 0.5) == pytest.approx(0.03)


def test_ewma_margin_constant_returns_and_lambda_fit():
    from explainer.quant.house import funding
    r = np.full(500, 0.01)
    m = funding.ewma_margin(r, lam=0.97, z=2.326, h=2, v0=0.0001)
    assert m[-1] == pytest.approx(2.326 * np.sqrt(2) * 0.01, rel=1e-9)  # v stays r^2 when it starts there
    rng = np.random.default_rng(3)
    v, x = 1e-4, []
    for _ in range(6000):  # data generated by EWMA itself, lambda 0.94
        e = np.sqrt(v) * rng.standard_normal()
        x.append(e)
        v = 0.94 * v + 0.06 * e * e
    assert funding.fit_ewma_lambda(np.array(x))["lam"] == pytest.approx(0.94, abs=0.02)
    k = funding.kupiec(10, 1000, 0.01)
    assert k["LR"] == pytest.approx(0.0, abs=1e-9) and k["p_value"] == pytest.approx(1.0)


def test_netting_bounds_on_random_graphs_and_waterfall():
    from explainer.quant.house import funding
    rng = np.random.default_rng(4)
    for _ in range(50):
        n = int(rng.integers(3, 12))
        a, b = rng.integers(0, n, 80), rng.integers(0, n, 80)
        k = a != b
        r = funding.netting(a[k], b[k], rng.exponential(1, k.sum()), n)
        assert r["multilateral"] <= r["bilateral"] + 1e-9 <= r["gross"] + 2e-9
        assert abs(r["net_position"].sum()) < 1e-9
    w = funding.ccp_waterfall(rng.exponential(30, 1000), [10, 5, 3, 20, 10])
    assert np.allclose(w.sum(1), w.sum(1)) and (w[:, :5] <= np.array([10, 5, 3, 20, 10]) + 1e-12).all()
    loss = np.array([4.0, 12.0, 60.0])
    assert np.allclose(funding.ccp_waterfall(loss, [10, 5, 3, 20, 10]).sum(1), loss)


def test_fire_sale_deleverage_short_and_liquidation_probability():
    from explainer.quant.house import funding
    L = funding.fire_sale(5, 2.0, 0.5)
    assert np.allclose(L, 0.5 * 4 * (np.arange(1, 6) - 0.5)) and L[-1] / L[0] == pytest.approx(9)
    d = funding.deleverage(2.0, 100.0, 0.04, 1e-5)
    assert d["sold"][0] == pytest.approx(50.0) and d["amplification"] > 1
    assert funding.deleverage(2.0, 100.0, 0.04, 0.0)["amplification"] == pytest.approx(1.0)
    assert funding.short_pnl(100, 90, 0.05, 0.01, 1.0) == pytest.approx(10 + 1.02 * 100 * 0.04)
    assert funding.short_pnl(100, 100, 0.02, 0.10, 1.0) < 0  # a special: the rebate is negative
    p = funding.liquidation_probability(np.array([2.0, 5.0, 10.0]), 30, 0.04)
    assert np.all(np.diff(p) > 0) and np.all((p > 0) & (p < 1))


def test_glm_smoothing_variance_and_fit():
    from explainer.quant.house import funding
    rng = np.random.default_rng(5)
    th = np.array([0.5, 0.3, 0.2])
    R = rng.normal(0.0, 1.0, 200000)
    Ro = funding.glm_smooth(R, th)
    assert Ro.var() == pytest.approx(np.sum(th ** 2), rel=0.02)
    rho1 = (th[0] * th[1] + th[1] * th[2]) / np.sum(th ** 2)
    assert np.corrcoef(Ro[:-1], Ro[1:])[0, 1] == pytest.approx(rho1, abs=0.01)
    assert np.allclose(funding.glm_fit(Ro[:20000])["theta"], th, atol=0.03)


# --------------------------------------------------------------------------- Part 3, expanded
def test_part3_rates_duration_and_implied_return():
    from explainer.quant.house import valuation as v
    # a project with two sign changes has two IRRs; bisection finds the one in its bracket
    assert v.irr_bisect([-100, 230, -132], 0.0, 0.15)["root"] == pytest.approx(0.10, abs=1e-9)
    assert v.irr_bisect([-100, 230, -132], 0.15, 0.5)["root"] == pytest.approx(0.20, abs=1e-9)
    b = v.irr_bisect([-100] + [5] * 9 + [105], 0.0, 0.2)["brackets"]
    assert all(h1 - l1 <= (h0 - l0) / 2 + 1e-15 for (l0, h0), (l1, h1) in zip(b, b[1:]))
    d = v.gordon_duration(0.08, 0.05)
    w = v.pv_weights(0.08, 0.05, 20000)
    assert w.sum() == pytest.approx(1.0) and (np.arange(1, 20001) @ w) == pytest.approx(d["macaulay"], rel=1e-6)
    # the implied rate inverts the two-stage valuation
    t = np.arange(1, 6)
    cf = 4.0 * 1.06 ** t
    price = float(np.sum(cf / 1.085 ** t) + cf[-1] * 1.02 / (0.085 - 0.02) / 1.085 ** 5)
    assert v.implied_rate(price, 4.0, 0.06, 0.02) == pytest.approx(0.085, abs=1e-10)
    # growth at RONIC = WACC adds nothing
    assert v.value_driver_tv(100, 0.03, 0.08, 0.08) == pytest.approx(v.value_driver_tv(100, 0.0, 0.08, 0.08))


def test_part3_residual_income_equals_ddm_on_the_toy_firm():
    from explainer.quant.house import fundamentals as f, valuation as v
    firm = f.Firm()
    book0 = firm.equity
    rows = f.simulate(firm, 12, seed=3, write_off=0.04, tax=0.21, rate_debt=0.01)
    E = [r["net_income"] for r in rows]
    D = [r["dividends"] for r in rows]
    out = v.residual_income(book0, E, D, 0.02)
    assert out["value"] == pytest.approx(out["ddm"], abs=1e-9)
    assert out["book"][-1] == pytest.approx(firm.equity)
    assert v.pb_steady(0.08, 0.08, 0.03) == pytest.approx(1.0) and v.pb_steady(0.12, 0.08, 0.04) == pytest.approx(2.0)


def test_part3_three_statements_balance_and_indirect_cash_flow():
    from explainer.quant.house import fundamentals as f
    firm = f.Firm()
    cash0 = firm.cash
    rows = f.simulate(firm, 20, seed=0, write_off=0.05, payout=0.3)
    dcash = sum(r["cfo"] - r["capex"] - r["dividends"] for r in rows)
    assert firm.cash - cash0 == pytest.approx(dcash)
    assert all(abs(r["net_income"] - r["cfo"] - r["accruals"]) < 1e-12 for r in rows)
    # accruals with a reversing error persist less than cash flows (Sloan's mechanism)
    p = f.earnings_panel(3000, 8, seed=1)
    y = p["E"][:, 1:].ravel()
    X = np.column_stack([p["CFO"][:, :-1].ravel(), p["ACC"][:, :-1].ravel()])
    beta = np.linalg.lstsq(np.column_stack([np.ones(len(y)), X]), y, rcond=None)[0]
    assert beta[2] < beta[1]


def test_part3_events_and_filing_lags():
    from explainer.quant.house import fundamentals as f
    x = np.array([1.0, 1.0, 1.0, 1.0] + [1.0 + 0.1 * k for k in range(1, 13)])
    s = f.sue(x)
    assert np.isnan(s[:12]).all() and np.isfinite(s[12:]).all()
    r = np.zeros(100)
    r[50] = 0.05
    c = f.car(r, np.zeros(100), 50, (-5, 10))
    assert c[4] == 0 and c[5] == pytest.approx(0.05) and c[-1] == pytest.approx(0.05)
    st = f.Store()
    st.add("A", "NetIncomeLoss", 20191231, 20200220, 1.0, "10-K")
    st.add("A", "NetIncomeLoss", 20191231, 20210220, 2.0, "10-K")
    assert f.filing_lags(st, "A", "NetIncomeLoss") == [(20191231, 51)]


def test_part3_taxes_campbell_shiller_and_beneish():
    from explainer.quant.house import valuation as v
    assert v.tax_shield(0.21, 100, 0.05) == pytest.approx(21)
    assert v.tax_shield(0.21, 100, 0.05, 2000) == pytest.approx(21, rel=1e-6)
    assert v.miller_gain(0.35, 0.0, 0.0) == pytest.approx(0.35)
    assert v.miller_gain(0.21, 0.2, 0.37) == pytest.approx(1 - 0.79 * 0.8 / 0.63)
    # an exactly linear Campbell-Shiller world: the identity holds to rounding
    rng = np.random.default_rng(0)
    T = 400
    dp = np.empty(T)
    dp[0] = -3.2
    for t in range(1, T):
        dp[t] = -3.2 + 0.9 * (dp[t - 1] + 3.2) + 0.1 * rng.standard_normal()
    dg = 0.02 + 0.05 * rng.standard_normal(T - 1)
    rho = 1 / (1 + np.exp(dp.mean()))
    r = 0.05 - rho * dp[1:] + dg + dp[:-1]
    cs = v.campbell_shiller(r, dg, dp)
    assert abs(cs["identity_gap"]) < 1e-12 and cs["lr_r"] - cs["lr_d"] == pytest.approx(1.0)
    neutral = {k: 1.0 for k in ("DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "LVGI")} | {"TATA": 0.0}
    assert v.beneish_m(neutral) == pytest.approx(-2.48, abs=1e-9)
    item = dict(sales=100, cogs=60, receivables=10, current_assets=40, ppe=50, assets=100, depreciation=5, sga=10,
                current_liabilities=20, long_term_debt=30, net_income=8, cfo=10)
    rt = v.beneish_ratios(item, item)
    assert rt["missing"] == [] and all(rt[k] == pytest.approx(1.0) for k in neutral if k != "TATA")
    assert rt["TATA"] == pytest.approx(-0.02)


def test_econometrics_part6_expansion():
    from explainer.quant.house import econ
    from scipy import stats as sst

    rng = np.random.default_rng(6)
    # long-run variance of an AR(1) with phi = 0.5 and unit innovations: 1 / (1 - phi)^2 = 4
    e = rng.standard_normal(20000)
    z = np.empty_like(e)
    z[0] = e[0]
    for t in range(1, len(e)):
        z[t] = 0.5 * z[t - 1] + e[t]
    assert econ.lrv(z, "bartlett", bw=60) == pytest.approx(4.0, rel=0.15)
    assert econ.lrv(z, "qs", bw=30) == pytest.approx(4.0, rel=0.15)
    assert econ.lrv(z, "ewc", nu=200) == pytest.approx(4.0, rel=0.25)
    # fixed-b: b -> 0 gives the normal 1.96; larger b gives fatter critical values
    assert econ.fixed_b_cv(0.002, reps=8000, T=500) == pytest.approx(1.96, abs=0.08)
    assert econ.fixed_b_cv(0.3, reps=8000, T=500) > 2.4
    # Hodrick 1B: under the null, |t| rarely exceeds 1.96 for overlapping horizons with a persistent predictor
    rej = 0
    for s in range(60):
        r = np.random.default_rng(100 + s)
        x = np.cumsum(r.standard_normal(400)) * 0.05
        x = x - np.linspace(0, 1, 400) * x[-1]
        rej += abs(econ.hodrick_se(r.standard_normal(400), x, 12)["t"][1]) > 1.96
    assert rej <= 12
    # within + between: month fixed effects equal the dispersion-weighted FM average
    T, N = 60, 30
    X = rng.standard_normal((T, N)) * rng.uniform(0.5, 2, (T, 1)) + rng.standard_normal((T, 1))
    Y = 0.3 * X + rng.standard_normal((T, N))
    wb = econ.within_between(Y.ravel(), X.ravel(), np.repeat(np.arange(T), N))
    sl = econ.fama_macbeth(Y, X)["slopes"][:, 1]
    disp = ((X - X.mean(1, keepdims=True)) ** 2).sum(1)
    assert wb["within"] == pytest.approx(np.sum(disp * sl) / disp.sum(), rel=1e-9)
    assert wb["pooled"] == pytest.approx(wb["w_within"] * wb["within"] + (1 - wb["w_within"]) * wb["between"], rel=1e-9)
    # two-pass recovers a planted premium; GRS does not reject a true model
    T, N = 600, 20
    f = 0.5 + rng.standard_normal(T)
    b = rng.uniform(0.5, 1.5, N)
    R = np.outer(f, b) + 0.5 * rng.standard_normal((T, N))
    tp = econ.two_pass(R, f)
    assert tp["lambda"][1] == pytest.approx(0.5, abs=0.15) and tp["se_shanken"][1] >= tp["se_fm"][1]
    assert econ.grs(R, f)["p"] > 0.001
    # MLE of a Student t: estimates near the truth, sandwich close to naive when the model is right
    x = sst.t.rvs(5, loc=0.1, scale=1.5, size=4000, random_state=1)
    nll = lambda th: -sst.t.logpdf(x, 2 + np.exp(th[2]), th[0], np.exp(th[1]))  # noqa: E731
    m = econ.mle(nll, [0.0, 0.0, 1.0])
    assert m["theta"][0] == pytest.approx(0.1, abs=0.08) and np.exp(m["theta"][1]) == pytest.approx(1.5, rel=0.1)
    assert m["se_sandwich"][0] == pytest.approx(m["se_naive"][0], rel=0.2)
    assert m["nll"][-1] <= m["nll"][0]
    # out of sample: a useless predictor has a negative R2_OS; a real one positive
    x = rng.standard_normal(600)
    o0 = econ.oos_r2(rng.standard_normal(600), x, 120)
    o1 = econ.oos_r2(0.5 * x + rng.standard_normal(600), x, 120)
    assert o0["r2_os"] < 0.02 and o1["r2_os"] > 0.1
    # Amihud-Hurvich and IVX: under the null with a persistent predictor, sizes near nominal
    rej_ivx = rej_aug = 0
    for s in range(150):
        r_ = np.random.default_rng(200 + s)
        L_ = np.linalg.cholesky([[1, -0.9], [-0.9, 1]])
        E = r_.standard_normal((241, 2)) @ L_.T
        xx = np.zeros(241)
        for t in range(1, 241):
            xx[t] = 0.98 * xx[t - 1] + E[t, 1]
        rr = E[1:, 0]
        rr = np.append(rr, 0.0)
        rej_ivx += econ.ivx(rr, xx)["p"] < 0.05
        rej_aug += abs(econ.augmented_predictive(rr, xx)["t"]) > 1.96
    assert rej_ivx / 150 < 0.13 and rej_aug / 150 < 0.13
    # event days: a planted 0.3 shift on 100 of 5000 days is found; placebo means centre on the overall mean
    rr = rng.standard_normal(5000)
    ev = np.zeros(5000, bool)
    ev[rng.choice(5000, 100, replace=False)] = True
    rr[ev] += 0.3
    assert econ.event_mean_test(rr, ev)["t"] > 1.5
    pm = econ.placebo_means(rr, 100, reps=500, exclude=ev)
    assert abs(pm.mean() - rr[~ev].mean()) < 0.02
    # stationary bootstrap indices: right shape, mean block length near the target
    idx = econ.stationary_indices(1000, 12, B=20, seed=3)
    assert idx.shape == (20, 1000) and idx.min() >= 0 and idx.max() < 1000
    breaks = np.mean(np.diff(idx, axis=1) % 1000 != 1)
    assert 1 / breaks == pytest.approx(12, rel=0.25)
    # Gibbs: with no true dispersion, tau's posterior sits near zero and the alphas shrink toward the mean
    est = rng.normal(0.02, 0.05, 40)
    g = econ.gibbs_hierarchical(est, np.full(40, 0.05), draws=1500, chains=2)
    assert np.median(g["tau"]) < 0.04 and np.var(g["alpha_post"]) < 0.3 * np.var(est)
    # 2SLS undoes confounding; DiD; staggered TWFE puts negative weight on some cells; CS recovers the truth
    n = 5000
    u = rng.standard_normal(n)
    zz = rng.standard_normal(n)
    xx = zz + u + rng.standard_normal(n)
    yy = 0.5 * xx + 2 * u + rng.standard_normal(n)
    iv = econ.iv_2sls(yy, xx, zz)
    assert iv["beta"] == pytest.approx(0.5, abs=0.1) and iv["F"] > 100
    assert econ.did_2x2([3.0], [1.0], [2.0], [1.0]) == pytest.approx(1.0)
    units, T = 60, 10
    coh = np.repeat([3, 6, 9], 20).astype(float)
    tt = np.arange(T)
    D = (tt[None, :] >= coh[:, None]).astype(float)
    eff = np.where(D > 0, 0.2 * (tt[None, :] - coh[:, None] + 1), 0.0)
    Y = rng.standard_normal((units, 1)) + 0.1 * tt[None, :] + eff + 0.05 * rng.standard_normal((units, T))
    tw = econ.twfe(Y, D)
    cs = econ.did_cs(Y, coh)
    true_att = eff[D > 0].mean()
    assert (tw["weights"] < 0).any() and abs(cs["att"] - eff[(D > 0) & (tt[None, :] < 9)].mean()) < 0.1
    assert tw["beta"] < true_att - 0.1  # growing effects: early cohorts as controls drag TWFE down
    # RD: a planted jump of 0.5 at zero
    xr = rng.uniform(-1, 1, 4000)
    yr = 0.3 * xr + 0.5 * (xr >= 0) + 0.2 * rng.standard_normal(4000)
    rd = econ.rd_local_linear(xr, yr, 0.0, 0.4)
    assert rd["jump"] == pytest.approx(0.5, abs=0.1)


# ---------------------------------------------------------------------------
# Part 9 expansion: the arbitrage checker's new tools
# ---------------------------------------------------------------------------
def test_part9_simplex_agrees_with_highs_and_finds_the_arbitrage():
    from scipy.optimize import linprog
    from explainer.quant.house import arbitrage as A

    rng = np.random.default_rng(9)
    for _ in range(40):
        Am = rng.normal(size=(3, 6))
        b = Am @ rng.random(6)
        c = rng.normal(size=6)
        mine, ref = A.simplex(c, Am, b), linprog(c, A_eq=Am, b_eq=b, method="highs")
        assert (mine["status"] == "optimal") == (ref.status == 0)
        if ref.status == 0:
            assert abs(mine["fun"] - ref.fun) < 1e-7
    # the fundamental theorem's LP: max t s.t. D psi = p, psi_j - t - s_j = 0
    D = np.vstack([np.ones(3), [80.0, 100.0, 125.0]])
    Aeq = np.zeros((5, 7))
    Aeq[:2, :3], Aeq[2:, :3], Aeq[2:, 3], Aeq[2:, 4:] = D, np.eye(3), -1, -np.eye(3)
    c = np.zeros(7)
    c[3] = -1
    ok = A.simplex(c, Aeq, [1, 100, 0, 0, 0])
    assert ok["status"] == "optimal" and np.allclose(ok["x"][:3], [5 / 13, 4 / 13, 4 / 13])
    bad = A.simplex(c, Aeq, [1, 130, 0, 0, 0])
    theta = bad["farkas"][:2]
    assert bad["status"] == "infeasible" and theta @ [1, 130] < 0 and np.all(D.T @ theta >= -1e-9)


def test_part9_superhedge_tree_is_crr_for_a_convex_payoff():
    from explainer.quant.house import arbitrage as A

    for N in (1, 4, 16):
        sh = A.superhedge_tree(100, 100, 1.0, 0.25, N)
        assert abs(sh["upper"] - trees.crr(100, 100, 1.0, 0.25, N=N)["price"]) < 1e-9
        assert abs(sh["lower"]) < 1e-12  # all mass on the middle branch: intrinsic value at the money


def test_part9_power_iteration_and_ross_recovery():
    from explainer.quant.house import arbitrage as A

    rng = np.random.default_rng(1)
    P = rng.random((6, 6)) * 0.2
    pi = A.power_iteration(P, 200)
    rr = A.ross_recovery(P)
    assert abs(pi["delta"][-1] - rr["delta"]) < 1e-10
    assert np.allclose(pi["z"][-1], rr["z"] / rr["z"].sum(), atol=1e-10)
    assert np.allclose(rr["F"].sum(1), 1.0)


def test_part9_mot_dual_and_entropic_match_the_lp():
    from explainer.quant.house import arbitrage as A

    x, mu = np.array([0.9, 1.1]), np.array([0.5, 0.5])
    y, nu = np.array([0.7, 1.0, 1.3]), np.array([0.3, 0.4, 0.3])
    c = lambda a, b: abs(b - a)  # noqa: E731
    lp = A.mot_bounds(x, mu, y, nu, c)
    up, lo = A.mot_dual(x, mu, y, nu, c, sign=-1), A.mot_dual(x, mu, y, nu, c, sign=1)
    assert abs(up["value"] - lp["upper"]) < 1e-9 and abs(up["dual_value"] - lp["upper"]) < 1e-9
    assert abs(lo["dual_value"] - lp["lower"]) < 1e-9
    assert up["slack"].min() > -1e-9 and lo["slack"].max() < 1e-9  # the hedge dominates (is dominated by) the claim
    ent = A.entropic_mot(x, mu, y, nu, c, eps=0.002, iters=3000, sign=-1)
    assert abs(ent["value"] - lp["upper"]) < 0.01
    assert np.allclose(ent["pi"].sum(1), mu, atol=1e-6) and np.allclose((ent["pi"] * (y[None] - x[:, None])).sum(1), 0,
                                                                         atol=1e-4)


def test_part9_implied_forward_reads_parity():
    from explainer.quant.house import arbitrage as A

    F, idx, K = 92000.0, 91000.0, 90000.0
    C, P = 0.06, 0.06 - (1 - K / F)
    mk = lambda kind, px, ts: {"instrument_name": f"BTC-27MAR26-90000-{kind}", "timestamp": ts, "price": px,  # noqa: E731
                               "mark_price": px, "index_price": idx}
    rows = A.implied_forward([mk("C", C, 1765353600000), mk("P", P, 1765353660000)])
    assert len(rows) == 1 and abs(rows[0][2] * idx - F) < 1e-6


def test_part9_neural_mot_dual_is_near_the_lp():
    pytest.importorskip("torch")
    from explainer.quant.house import arbitrage as A
    from explainer.quant.house import deep

    x, mu = np.array([0.9, 1.1]), np.array([0.5, 0.5])
    y, nu = np.array([0.7, 1.0, 1.3]), np.array([0.3, 0.4, 0.3])
    c = lambda a, b: abs(b - a)  # noqa: E731
    lp = A.mot_bounds(x, mu, y, nu, c)["upper"]
    r = deep.mot_neural(x, mu, y, nu, c, steps=3000, gamma=3000.0, width=32, lr=1e-2, seed=0)
    assert abs(r["bound"] - lp) < 0.03


# ---------------------------------------------------------------- rough, Part 14 expanded


def test_part14_volterra_riemann_misses_the_singular_cell():
    from explainer.quant.house import rough as R
    t, Y, _ = R.volterra_riemann(0.3, 1.0, 100, 20000, seed=1)
    assert abs(Y[:, -1].var() - 1.0) < 0.1                    # t^{2H} = 1 at t = 1
    _, Y5, _ = R.volterra_riemann(0.05, 1.0, 100, 20000, seed=1)
    S, v = R.rbergomi_paths(0.05, 1.0, 0.0, 1.0, 1.0, 100, 20000, seed=1, return_v=True)
    hyb = (np.log(v[-1]) + 0.5).var()
    assert Y5[:, -1].var() < 0.7 < hyb


def test_part14_skew_term_fit_recovers_a_power_law():
    from explainer.quant.house import rough as R
    T = np.array([2, 5, 9, 16, 30, 60, 90, 180, 365]) / 365
    f = R.skew_term_fit(T, 0.2 * T ** -0.4)
    assert abs(f["power"]["a"] - 0.4) < 1e-4 and abs(f["H"] - 0.1) < 1e-4


def test_part14_fou_paths():
    from explainer.quant.house import rough as R, sim
    x = R.fou_paths(0.3, None, 2000, 1.0, seed=4)
    B = np.asarray(sim.fbm(0.3, 2000, 2000.0, 1, seed=4)).ravel()
    assert np.allclose(x, B[1:] - B[0])
    y = R.fou_paths(0.3, 10.0, 20000, 1.0, seed=5)
    assert np.isfinite(y.var()) and y.var() < np.var(R.fou_paths(0.3, None, 20000, 1.0, seed=5))


def test_part14_rfsv_beats_last_value_on_fbm():
    from explainer.quant.house import rough as R, sim
    x = np.asarray(sim.fbm(0.1, 3000, 3000.0, 1, seed=8)).ravel()
    p = R.rfsv_predict(x, 0.1, 5, window=250)
    i = np.arange(260, len(x) - 5)
    assert np.mean((x[i + 5] - p[i]) ** 2) < np.mean((x[i + 5] - x[i]) ** 2)


def test_part14_pdv4_ema_is_the_two_exponential_convolution():
    from explainer.quant.house import rough as R
    r = np.random.default_rng(0).standard_normal(400) * 0.02
    dt, l0, l1, th = 1 / 365, 50.0, 5.0, 0.3
    got = R.pdv4_features(r, dt, l0, l1, th)
    j = np.arange(400)
    K = lambda lam: (1 - np.exp(-lam * dt)) * np.exp(-lam * dt * j)  # noqa: E731  exact EMA weights
    want = (1 - th) * np.convolve(r / dt, K(l0))[:400] + th * np.convolve(r / dt, K(l1))[:400]
    assert np.allclose(got, want)


def test_part14_qrh_floor_and_deterministic_without_noise():
    from explainer.quant.house import rough as R
    S, V, Z = R.qrh_paths(0.4, 0.1, 0.003, 1.0, 1.0, 0.1, 0.1, 1.0, 100, 500, seed=1)
    assert (V >= 0.003 - 1e-12).all()
    S0, V0, Z0 = R.qrh_paths(0.4, 0.1, 0.003, 1.0, 0.0, 0.1, 0.05, 1.0, 100, 50, seed=1)
    assert np.allclose(Z0, Z0[:1])                              # eta = 0: Z is the same on every path


def test_part14_sigvol_constant_ell_is_black_scholes():
    from explainer.quant.house import bs, rough as R
    feats, words = R.sigvol_features([50], 50, 0.5 / 50, 40000, depth=3, seed=2)
    f = feats[50]
    ell = np.zeros(len(words))
    ell[0] = 0.4
    ST = np.exp(R.sigvol_logS(ell, -0.5, f["AW"], f["AP"], f["B"]))
    p = np.mean(np.maximum(ST - 1.0, 0))
    assert abs(p - bs.price(1.0, 1.0, 0.5, 0.4, 0.0, 0.0, 1)) < 3 * np.std(np.maximum(ST - 1, 0)) / np.sqrt(40000)


def test_part14_hawkes_branching_mean_count():
    from explainer.quant.house import sim
    mu, n, T = 0.5, 0.8, 20000.0
    counts = [len(sim.hawkes_branching_powerlaw(mu, n, 1.5, 1.0, T, seed=s)) for s in range(4)]
    assert abs(np.mean(counts) / (mu * T / (1 - n)) - 1) < 0.05


def test_part14_lift_weights_fit_the_kernel():
    from scipy.special import gamma
    from explainer.quant.house import rough as R
    t = np.exp(np.linspace(np.log(1e-2), 0, 30))
    K = t ** (0.6 - 1) / gamma(0.6)
    err = []
    for N in (5, 20, 50):
        c, x = R.lift_weights(0.1, N)
        err.append(np.max(np.abs((c[None, :] * np.exp(-x[None, :] * t[:, None])).sum(1) / K - 1)))
    assert err[1] < 0.2 and err[2] < err[1] < err[0]


# ---------------------------------------------------------------- engine, expanded (Part 16)


def test_engine_geometric_asian_and_controls():
    from explainer.quant.house import engine as E
    S0, K, T, s, r = 100.0, 100.0, 1.0, 0.2, 0.05
    ex = E.geometric_asian_call(S0, K, T, s, r, 16)
    g = np.random.default_rng(0)
    dt = T / 16
    t = dt * np.arange(1, 17)
    W = np.cumsum(np.sqrt(dt) * g.standard_normal((200000, 16)), axis=1)
    G = np.exp(np.mean(np.log(S0) + (r - 0.5 * s * s) * t + s * W, axis=1))
    y = np.exp(-r * T) * np.maximum(G - K, 0)
    assert abs(y.mean() - ex) < 3 * y.std() / np.sqrt(len(y))
    cv = E.asian_control(S0, K, T, s, r, 20000, 64, seed=1)
    plain = E.asian_control(S0, K, T, s, r, 200000, 64, seed=2, control="none")
    assert cv["ratio"] > 100 and abs(cv["price"] - plain["price"]) < 3 * np.hypot(cv["se"], plain["se"])


def test_engine_stratified_and_cross_entropy():
    from explainer.quant.house import bs as B, engine as E
    S0, K, T, s, r = 100.0, 100.0, 1.0, 0.2, 0.05
    ex = float(B.price(S0, K, T, s, r))
    p, se = E.stratified_call(S0, K, T, s, r, 16384, 64, seed=3)
    _, se0 = E.mc_call(S0, K, T, s, r, 16384, seed=3)
    assert abs(p - ex) < 4 * se and se < se0
    drift = (r - 0.5 * s * s) * T
    f = lambda z: np.maximum(S0 * np.exp(drift + s * z) - 160.0, 0)  # noqa: E731
    th = E.is_cross_entropy(f, 0.0, 20000, 4, seed=4)[-1]
    z = np.random.default_rng(5).standard_normal(200000)
    grid = np.linspace(1.5, 4.0, 51)
    var = [np.var(f(z + t) * np.exp(-t * (z + t) + 0.5 * t * t)) for t in grid]
    assert abs(th - grid[int(np.argmin(var))]) < 0.3


def test_engine_path_matrices_and_discrepancy():
    from scipy.stats import qmc
    from explainer.quant.house import engine as E
    n = 32
    i = np.arange(1, n + 1)
    C = np.minimum.outer(i, i) / n
    share = {}
    for k in ("step", "bridge", "pca"):
        L = E.path_matrix(n, 1.0, k)
        assert np.abs(L @ L.T - C).max() < 1e-12
        share[k] = E.variance_captured(np.ones(n) / n, L)[0]
    assert share["pca"] >= share["bridge"] >= share["step"]
    assert E.l2_star_discrepancy(np.array([[0.5]])) == pytest.approx(np.sqrt(1 / 12), rel=1e-12)
    sob = qmc.Sobol(2, scramble=True, seed=0).random(1024)
    rnd = np.random.default_rng(0).random((1024, 2))
    assert E.l2_star_discrepancy(sob) < E.l2_star_discrepancy(rnd)


def test_engine_mlmc_run_matches_and_milstein_decays():
    from explainer.quant.house import bs as B, engine as E
    a = E.mlmc_run(0.05, seed=3, trace=True)
    assert a["estimate"] == E.mlmc(0.05, seed=3)["estimate"] and len(a["trace"]) >= 1
    m = E.mlmc_run(0.02, scheme="milstein", payoff="call", seed=1, L0=8, max_level=8)
    V = np.log2(m["V"])
    slope = -np.polyfit(np.arange(3, 9), V[3:9], 1)[0]
    assert slope >= 1.7
    ex = float(B.price(100, 100, 1, 0.2, 0.05))
    se = np.sqrt(sum(v / n for v, n in zip(m["V"], m["N"])))
    assert abs(m["estimate"] - ex) < 3 * se + 0.01


def test_engine_lsm_trace_bermudan_and_max_call():
    from explainer.quant.house import deep, engine as E, trees
    S0, K, T, s, r = 100.0, 100.0, 1.0, 0.2, 0.05
    tr = E.lsm_put_trace(S0, K, T, s, r, 25, 40000, seed=1, n_show=0)
    b = np.asarray(tr["boundary"], float)
    ok = np.isfinite(b)
    assert np.all(b[ok] <= K + 1e-9) and b[ok][-1] > b[ok][len(b[ok]) // 2]
    lo, se = E.lsm_put_eval(tr["coefs"], S0, K, T, s, r, 25, 40000, seed=9)
    berm = E.bermudan_tree(S0, K, T, s, r, 25, 1000)
    amer = trees.crr(S0, K, T, s, r, N=2000, cp=-1, american=True)["price"]
    euro = trees.crr(S0, K, T, s, r, N=2000, cp=-1)["price"]
    assert euro < berm < amer and lo < amer + 3 * se
    p = dict(deep.MAX_CALL, d=2)
    mc = E.lsm_max_call(p, 20000, 100000, seed=1)
    assert abs(mc["lower"] - 13.902) < 0.1


def test_engine_aad_basket_penalty_lewis():
    from explainer.quant.house import engine as E, stochvol as sv, trees
    a = E.aad_basket(3, 2000, 6, reps=1)
    assert a["max_delta_diff"] < 1e-3 and a["inputs"] == 6
    pe = E.fd_american_penalty(100, 100, 1, 0.2, 0.05, 200, 200)
    tree = trees.crr(100, 100, 1, 0.2, 0.05, N=2000, cp=-1, american=True)["price"]
    assert abs(pe["price"] - tree) < 0.02 and np.isfinite(pe["boundary"][-1])
    cf = lambda u, T: sv.heston_cf(u, T, 0.04, 1.5, 0.04, 0.5, -0.7)  # noqa: E731
    assert abs(E.lewis_call(cf, 100, 100, 1.0) - float(sv.cos_price(cf, 100, 100, 1.0, 1, N=4096, L=40)[0])) < 1e-8


def test_engine_mlae_and_chebyshev():
    from explainer.quant.house import engine as E
    a = 0.3
    errs = [E.mlae(a, (0, 1, 2, 4, 8, 16, 32, 64, 128), 50, seed=s)["estimates"][-1] - a for s in range(20)]
    calls = E.mlae(a, (0, 1, 2, 4, 8, 16, 32, 64, 128), 50)["calls"][-1]
    assert np.sqrt(np.mean(np.square(errs))) < np.sqrt(a * (1 - a) / calls)
    f = lambda x, y: 1 + x - 2 * x ** 3 * y ** 2 + y ** 4  # noqa: E731
    m = E.chebyshev2d(f, ((-1.0, 2.0), (0.5, 1.5)), 6)
    x, y = np.random.default_rng(0).uniform(-1, 2, 50), np.random.default_rng(1).uniform(0.5, 1.5, 50)
    assert np.allclose(E.chebyshev2d_eval(m, x, y), f(x, y), atol=1e-10)
    S, v, G = E.heston_adi_grid(100, 100, 1.0, 0.04, 1.5, 0.04, 0.5, -0.7, r=0.0, nS=20, nv=10, nt=10)
    assert G.shape == (len(v), len(S))


# ---------------------------------------------------------------------------
# Part 12's expansion: the surface builder's new tools
# ---------------------------------------------------------------------------
def test_svi_jw_round_trip_and_lee():
    from explainer.quant.house import volsurface as V

    p = {"a": 0.02, "b": 0.12, "rho": -0.25, "m": 0.07, "s": 0.3}
    q = V.svi_from_jw(V.svi_jw(p, 0.4), 0.4)
    for x in p:
        assert q[x] == pytest.approx(p[x], abs=1e-10)
    assert float(V.lee_moment(2.0)) == pytest.approx(0.0)
    assert float(V.lee_moment(1e-9)) > 1e7
    for pm in (0.1, 1.0, 3.7):
        assert float(V.lee_moment(V.lee_slope(pm))) == pytest.approx(pm, rel=1e-12)


def test_ssvi_butterfly_bound_matches_a_scan():
    from explainer.quant.house import volsurface as V

    assert V.ssvi_butterfly_bound({"rho": -0.3, "eta": 1.2, "gamma": 0.4}) == 0.0
    fit = {"rho": -0.23, "eta": 1.4, "gamma": 0.6}
    b = V.ssvi_butterfly_bound(fit)
    th = np.logspace(-14, 1, 200001)
    p = V.phi_power(th, fit["eta"], fit["gamma"])
    bad = th * p * p * (1 + abs(fit["rho"])) > 4
    assert b == pytest.approx(th[bad].max(), rel=1e-3)


def test_fit_ssvi_path_ends_where_fit_ssvi_does():
    from explainer.quant.house import volsurface as V

    k = np.tile(np.linspace(-0.3, 0.3, 9), 3)
    T = np.repeat([0.1, 0.3, 0.6], 9)
    w = V.ssvi_w(k, np.repeat([0.02, 0.05, 0.09], 9), -0.3, 0.9, 0.45)
    a, b = V.fit_ssvi(k, T, w), V.fit_ssvi_path(k, T, w)
    assert b["rho"] == pytest.approx(a["rho"], abs=1e-9) and b["rmse"] < 1e-6
    assert len(b["path"]) == len(b["rmse_path"]) >= 5 and b["rmse_path"][0] > b["rmse_path"][-1]


def test_skew_stickiness_and_pca():
    from explainer.quant.house import volsurface as V

    g = np.random.default_rng(0)
    dl = 0.03 * g.standard_normal(500)
    sk = -0.4
    assert V.skew_stickiness(dl, sk * dl + 1e-4 * g.standard_normal(500), np.full(500, sk))["R"] == pytest.approx(1, abs=0.02)
    assert abs(V.skew_stickiness(dl, 1e-4 * g.standard_normal(500), np.full(500, sk))["R"]) < 0.02
    f = np.linspace(1, 2, 20)
    X = np.outer(g.standard_normal(300), f) + 0.01 * g.standard_normal((300, 20))
    out = V.surface_pca(X)
    assert out["explained"].sum() == pytest.approx(1.0)
    assert abs(out["components"][0] @ (f / np.linalg.norm(f))) > 0.999


def test_conditional_variance_and_strip_replication():
    from explainer.quant.house import bs as B, volsurface as V

    g = np.random.default_rng(1)
    x = 0.3 * g.standard_normal(200000)
    assert np.allclose(V.conditional_variance(x, np.full_like(x, 0.09), [-0.2, 0, 0.2]), 0.09)
    F, T, s = 100.0, 30 / 365, 0.5
    K = np.linspace(5, 600, 20000)
    otm = np.where(K < F, B.price(F, K, T, s, 0, 0, -1), B.price(F, K, T, s, 0, 0, 1))
    flat = V.strip_replication(K, otm, F, T, np.full(50, F))
    assert flat["kvar"] == pytest.approx(s * s, rel=2e-3) and abs(flat["replicated"]) < 1e-9 and flat["rv"] == 0
    path = F * np.exp(np.cumsum(np.concatenate([[0], s * np.sqrt(T / 720) * g.standard_normal(720)])))
    r = V.strip_replication(K, otm, F, T, path)
    lr = np.diff(np.log(path))
    cubic = 2 / T * np.sum(lr ** 3 / 6 + lr ** 4 / 24)  # 2(e^x - 1 - x) - x^2 = x^3/3 + x^4/12 + ...
    assert r["error"] == pytest.approx(cubic, abs=2e-3 * r["rv"])


def test_vol_swap_vix_and_moments():
    from explainer.quant.house import bs as B, volsurface as V

    rv = np.array([0.04, 0.09, 0.16, 0.25])
    c = V.vol_swap_convexity(rv)
    assert c["gap"] == pytest.approx(np.sqrt(rv.mean()) - np.sqrt(rv).mean())
    small = 0.09 * (1 + 0.05 * np.random.default_rng(2).standard_normal(1000))
    cs = V.vol_swap_convexity(small)
    assert cs["approx_gap"] == pytest.approx(cs["gap"], rel=0.1)
    assert V.vix_30d(20 / 365, 0.5, 40 / 365, 0.5) == pytest.approx(0.5)
    F, T, s = 100.0, 0.25, 0.4
    K = F * np.exp(np.linspace(-4, 4, 40001))
    otm = np.where(K < F, B.price(F, K, T, s, 0, 0, -1), B.price(F, K, T, s, 0, 0, 1))
    m = V.rn_moments(K, otm, F, T)
    assert m["var"] == pytest.approx(s * s, rel=1e-3) and abs(m["skew"]) < 1e-3 and m["kurt"] == pytest.approx(3, abs=1e-2)
    assert m["mean"] == pytest.approx(-s * s * T / 2, rel=1e-3)


def test_vx_index_and_inverse_note():
    from explainer.quant.house import volsurface as V

    days = list(range(1, 61))
    exps = [20, 41, 62, 83]
    flat = {e: {d: 15.0 for d in days} for e in exps}
    out = V.vx_index(days, flat, exps)
    assert np.allclose(out["ret"], 0) and out["w1"].max() <= 1 and out["w1"].min() >= 0
    up = {e: {d: 15.0 * (1.1 if d >= 30 else 1.0) for d in days} for e in exps}
    assert V.vx_index(days, up, exps)["ret"][28] == pytest.approx(0.1)
    r = np.array([0.01, -0.02, 0.1, 1.2])
    n = V.inverse_note(r)
    assert np.allclose(n[:4], np.cumprod(np.concatenate([[1], 1 - r[:3]]))) and n[-1] == 0.0
    assert V.rebalance_flow(-1, 0.1, 1.0) == pytest.approx(0.2) and V.rebalance_flow(2, 0.1, 1.0) == pytest.approx(0.2)


def test_gamma_day_feedback():
    from explainer.quant.house import volsurface as V

    eps = 0.001 * np.random.default_rng(3).standard_normal((4000, 390))
    same = V.gamma_day(eps, 0.0)
    assert np.allclose(same["r"], eps)
    lo, hi = V.gamma_day(eps, 0.5), V.gamma_day(eps, -0.5)
    assert lo["rest"].std() / same["rest"].std() == pytest.approx(1 / 1.25, rel=1e-6)
    assert np.polyfit(hi["rest"], hi["last"], 1)[0] == pytest.approx(0.25, abs=0.03)
    assert np.polyfit(lo["rest"], lo["last"], 1)[0] == pytest.approx(-0.25, abs=0.03)


def test_derman_kani_tree():
    from explainer.quant.house import bs as B, trees, volsurface as V

    flat = trees.derman_kani(100.0, 1.0, 40, lambda K, t: 0.2)
    K = np.array([85.0, 100.0, 115.0])
    assert np.allclose(trees.tree_price(flat, K), B.price(100.0, K, 1.0, 0.2, 0, 0, 1), atol=0.12)
    fit = {"rho": -0.25, "eta": 0.8, "gamma": 0.45, "theta": [0.02, 0.06], "T": [0.1, 0.3]}
    iv = lambda K, t: float(np.sqrt(V.ssvi_surface_w(fit, np.log(K / 100.0), t) / t))  # noqa: E731
    tr = trees.derman_kani(100.0, 0.25, 30, iv)
    P = np.concatenate(tr["p"])
    assert P.min() > 0 and P.max() < 1
    # the last level reprices calls struck at the previous level's central nodes (its construction)
    s = tr["nodes"][-2]
    mid = s[np.abs(np.log(s / 100)) < 0.3]
    got = trees.tree_price(tr, mid)
    want = np.array([B.price(100.0, k, 0.25, iv(k, 0.25), 0, 0, 1) for k in mid])
    assert np.allclose(got, want, rtol=2e-3, atol=1e-3)


def test_surface_net_learns_without_arbitrage():
    import torch

    from explainer.quant.house import deep, volsurface as V

    torch.set_num_threads(1)
    fit = {"rho": -0.3, "eta": 0.8, "gamma": 0.4, "theta": [0.01, 0.03, 0.06], "T": [0.05, 0.15, 0.3]}
    k, T = np.tile(np.linspace(-0.4, 0.4, 15), 3), np.repeat([0.05, 0.15, 0.3], 15)
    iv = np.sqrt(V.ssvi_surface_w(fit, k, T) / T)
    r = deep.train_surface_net(k, T, iv, steps=800, every=400, T_range=(0.03, 0.4), k_range=(-0.6, 0.6), colloc=(21, 10))
    assert r["train_rmse"] < 0.5 and r["g_viol"] == 0.0 and r["cal_viol"] == 0.0


# ---------------------------------------------------------------------------
# Part 11's expansion: the options desk
# ---------------------------------------------------------------------------
def test_pnl_explain_residual_is_third_order():
    from explainer.quant.house import quoting as Q
    legs = [Q.Leg(1, 100.0, 30 / 365, 1), Q.Leg(-1, 90.0, 30 / 365, -2)]
    res = []
    for h in (0.02, 0.01):
        e = Q.pnl_explain(legs, 100.0, 100.0 * (1 + h), 0.5, 0.5 + h, 1e-6)
        res.append(abs(e["unexplained"]))
    assert res[1] < res[0] / 5          # O(h^3): halving the move cuts it about eightfold


def test_delta_strike_flat_smile_closed_form():
    from scipy.stats import norm
    from explainer.quant.house import quoting as Q
    F, T, s = 100.0, 0.25, 0.4
    K = Q.delta_strike(F, T, lambda k: s, 0.25)
    assert K == pytest.approx(F * np.exp(-s * np.sqrt(T) * norm.ppf(0.25) + 0.5 * s * s * T), rel=1e-7)
    Kp = Q.delta_strike(F, T, lambda k: s, -0.25, cp=-1)
    assert Kp == pytest.approx(F * np.exp(s * np.sqrt(T) * norm.ppf(0.25) + 0.5 * s * s * T), rel=1e-7)


def test_vanna_volga_returns_the_pillars():
    from explainer.quant.house import quoting as Q
    F, T = 100.0, 30 / 365
    k3, v3 = [88.0, 100.0, 113.0], [0.62, 0.50, 0.55]
    out = Q.vanna_volga(k3, F, T, k3, v3, 0.50)
    assert np.allclose(out, v3, atol=1e-8)


def test_markouts_recover_a_permanent_impact():
    from explainer.quant.house import quoting as Q
    ts = np.array([0.0, 10.0, 400.0, 900.0])
    sign = np.array([1, 1, 1, 1])
    mark = np.array([0.05, 0.05, 0.051, 0.051])
    price = mark + 0.0004                      # takers pay 4 bp of the index over mark
    idx = np.full(4, 100.0)
    out = Q.markouts(ts, sign, price, mark, idx, np.zeros(4), np.full(4, 1.0), horizons=(300,))
    assert np.allclose(out["edge"], 0.04)
    # the first trade's markout: the mark moved up 0.1 (in index units x 100) against the maker
    assert out[300][0] == pytest.approx(-(0.051 * 100 - 0.0504 * 100))
    assert np.isnan(out[300][-1])


def test_market_maker_dp_q_learning_and_glft():
    from explainer.quant.house import quoting as Q
    dp = Q.mm_value_iteration(Q=4)
    assert np.allclose(dp["skew"], -dp["skew"][::-1])          # antisymmetric in inventory
    assert dp["skew"][-2] > 0 > dp["skew"][1]                  # long: both quotes move down
    ql = Q.mm_q_learning(steps=120_000, seed=0, Q=4)
    v_ql = Q.mm_policy_value(ql["policy"], Q=4)[4]
    assert v_ql > 0.8 * dp["V"][4]
    g = Q.glft_quotes(np.array([-2, 0, 2]), 0.45, 1.5, 0.02)
    assert g["skew"][0] < 0 == g["skew"][1] < g["skew"][2]


def test_greek_hedge_zeroes_the_greeks():
    from explainer.quant.house import quoting as Q
    gk = lambda K, T: {k: float(v) for k, v in bs.greeks(100.0, K, T, 0.5).items()}  # noqa: E731
    book = {k: -2 * v for k, v in gk(100.0, 30 / 365).items()}
    a, b = gk(100.0, 7 / 365), gk(100.0, 60 / 365)
    h = Q.greek_hedge(book, (a, b))
    for key in ("gamma", "vega"):
        assert book[key] + h["n1"] * a[key] + h["n2"] * b[key] == pytest.approx(0, abs=1e-9)
    assert book["delta"] + h["n1"] * a["delta"] + h["n2"] * b["delta"] + h["shares"] == pytest.approx(0, abs=1e-9)


def test_delta_hedge_on_moves_band_zero_is_every_step():
    t, S = paths.gbm(100.0, 0.0, 0.5, 30 / 365, 60, 50, seed=3)
    t = np.linspace(0, 30 / 365, 61) if np.ndim(t) == 0 else t
    a = hedge.delta_hedge_on_moves(t, S, 100.0, 30 / 365, 0.5, 0.0)["pnl"]
    b = hedge.delta_hedge(t, S, 100.0, 30 / 365, 0.5)["pnl"]
    assert np.allclose(a, b, atol=1e-9)


def test_pin_simulation_without_hedgers_is_gbm():
    from explainer.quant.house import sim
    t, S = sim.pin_simulation(100.0, 100.0, 0.05, 0.4, 0.0, 5.0, 50, 40000, seed=1)
    lr = np.log(S[:, -1] / 100.0)
    assert lr.var() == pytest.approx(0.4 ** 2 * 0.05, rel=0.03)
    _, P = sim.pin_simulation(100.0, 100.0, 0.05, 0.4, 2.0, 5.0, 50, 4000, seed=1)
    assert np.mean(np.abs(P[:, -1] - 100) < 0.5) > np.mean(np.abs(S[:4000, -1] - 100) < 0.5)


def test_american_call_with_dividend():
    from explainer.quant.house import trees as TR
    o = TR.american_call_dividend(100.0, 100.0, 0.5, 0.04, 0.3, 0.0, 0.25, N=400)
    assert o["price"] == pytest.approx(float(bs.price(100.0, 100.0, 0.5, 0.3, 0.04)), abs=0.02)
    assert not o["region"]                                    # no dividend: never exercise
    o2 = TR.american_call_dividend(100.0, 90.0, 2 / 12, 0.04, 0.3, 5.0, 5 / 52, N=200)
    assert o2["price"] > o2["european"]
    steps = {n for n, _, _ in o2["region"]}
    assert max(steps) * o2["dt"] < 5 / 52                     # only before the dividend


# ---------------------------------------------------------------- exotics, expanded (Part 15)
def test_one_touch_reflection_and_mc():
    from explainer.quant.house import exotics as X
    from scipy.stats import norm
    S, H, T, s = 100.0, 90.0, 0.5, 0.25
    ot = X.one_touch(S, H, T, s)
    d1 = (np.log(S / H) + 0.5 * s * s * T) / (s * np.sqrt(T))
    assert ot == pytest.approx(norm.cdf(-(d1 - s * np.sqrt(T))) + S / H * norm.cdf(-d1), abs=1e-12)
    # zero drift in the log: exactly twice the digital
    mu0 = X.one_touch(S, H, T, s, r=0.5 * s * s)
    assert mu0 * np.exp(0.5 * s * s * T) == pytest.approx(2 * norm.cdf(np.log(H / S) / (s * np.sqrt(T))), abs=1e-12)
    P = X.gbm_paths(S, s, T, 2000, 40000, seed=2)
    Hb = X.bgk_barrier(H, S, s, T / 2000)
    assert np.mean(P.min(axis=0) <= H) == pytest.approx(X.one_touch(S, Hb, T, s), abs=0.01)


def test_static_dic_hedge_is_exact_under_bs():
    from explainer.quant.house import bs as B, exotics as X
    for K, H in ((100.0, 90.0), (105.0, 80.0)):
        w, k = X.static_dic_hedge(K, H, 100.0)
        dic = B.price(100.0, K, 0.5, 0.25) - X.down_out_call(100.0, K, H, 0.5, 0.25)
        assert w * B.price(100.0, k, 0.5, 0.25, 0, 0, -1) == pytest.approx(float(dic), abs=1e-10)


def test_snowball_AB_is_the_price_and_the_fair_coupon():
    from explainer.quant.house import exotics as X
    A, B = X.snowball_AB(0.2, n_paths=4000, seed=3)
    for c in (0.0, 0.1, 0.2):
        assert A + c * B == pytest.approx(X.snowball_price(0.2, coupon=c, n_paths=4000, seed=3), abs=1e-12)
    A, B = X.snowball_AB(0.2, n_paths=4000, seed=1)
    assert (1 - A) / B == pytest.approx(X.fair_coupon(0.2, n_paths=4000, seed=1), abs=2e-3)


def test_autocall_on_paths_reduces_to_snowball_payoff():
    from explainer.quant.house import exotics as X
    P = X.gbm_paths(1.0, 0.2, 2.0, 504, 2000, 0.02, seed=4)
    pv, _, _ = X.snowball_payoff(P, coupon=0.12)
    obs = [m * 21 for m in range(3, 25)]
    disc = np.exp(-0.02 * np.array(obs) / 252)
    pv2 = X.autocall_on_paths(P, obs, 1.03, 0.75, [0.12 * m / 12 for m in range(3, 25)], disc)
    assert np.allclose(pv, pv2, atol=1e-12)


def test_worst_of_autocall_with_perfect_correlation_is_single_asset():
    from explainer.quant.house import exotics as X
    a1, b1 = X.worst_of_autocall_AB(0.2, 0.2, 1.0, n_paths=2000, seed=5)
    a0, b0 = X.snowball_AB(0.2, n_paths=2000, seed=5)
    assert a1 == pytest.approx(a0, abs=1e-12) and b1 == pytest.approx(b0, abs=1e-12)
    a2, b2 = X.worst_of_autocall_AB(0.2, 0.2, 0.5, n_paths=2000, seed=5)
    assert (1 - a2) / b2 > (1 - a1) / b1                       # less correlation, dearer put, higher coupon


def test_margrabe_against_mc():
    from explainer.quant.house import exotics as X
    P1, P2 = X.two_asset_paths(0.3, 0.2, 0.4, 1.0, 1, 200000, seed=6)
    pay = np.maximum(P1[-1] - P2[-1], 0)
    assert X.margrabe(1.0, 1.0, 1.0, 0.3, 0.2, 0.4) == pytest.approx(pay.mean(), abs=3 * pay.std() / np.sqrt(len(pay)))


def test_cliquet_unbounded_is_a_martingale_sum():
    from explainer.quant.house import exotics as X
    m, se = X.cliquet_bs(0.25, 12, cap=np.inf, floor=-np.inf, gfloor=-np.inf, n_paths=100000, seed=1)
    assert abs(m) < 3 * se
    lo, _ = X.cliquet_bs(0.25, 12, cap=0.02, floor=-1.0, gfloor=0.0, n_paths=20000, seed=1)
    hi, _ = X.cliquet_bs(0.10, 12, cap=0.02, floor=-1.0, gfloor=0.0, n_paths=20000, seed=1)
    assert lo < hi                                             # a capped, unfloored cliquet is short volatility


def test_uvm_solve_matches_uvm_price_and_lagrangian_helps():
    from explainer.quant.house import bs as B, exotics as X
    grid = np.linspace(40, 200, 81)
    cs = lambda x: (np.maximum(x - 95, 0) - np.maximum(x - 105, 0)) / 10  # noqa: E731
    a = X.uvm_price(cs, grid, 0.5, 0.15, 0.35, n_t=50)
    b = X.uvm_solve(cs(grid), grid, 0.5, 0.15, 0.35, n_t=50)
    assert np.allclose(a, b, atol=1e-10)
    calls = [lambda x: np.maximum(x - 90, 0), lambda x: np.maximum(x - 110, 0)]
    mkt = [float(B.price(100.0, k, 0.5, 0.25)) for k in (90.0, 110.0)]
    out = X.uvm_lagrangian(cs, calls, mkt, grid, 100.0, 0.5, 0.15, 0.35, n_t=50, maxfev=30)
    assert out["unhedged"] == pytest.approx(float(np.interp(100.0, grid, b)), abs=1e-10)
    assert out["price"] <= out["unhedged"] + 1e-12


def test_kl_worst_case_mean_at_zero_and_monotone():
    from explainer.quant.house import exotics as X
    v = np.random.default_rng(0).normal(1.0, 0.2, 20000)
    assert X.kl_worst_case(v, 0.0)[0] == pytest.approx(v.mean(), abs=1e-12)
    w = [X.kl_worst_case(v, e)[0] for e in (0.01, 0.05, 0.1, 0.2)]
    assert all(a > b for a, b in zip(w, w[1:]))
    assert w[2] == pytest.approx(1.0 - 0.2 * np.sqrt(0.2), abs=0.01)  # Gaussian: a shift of sigma sqrt(2 eta)


def test_digital_delta_estimators():
    from explainer.quant.house import exotics as X
    from scipy.stats import norm
    S, K, T, s = 100.0, 100.0, 21 / 252, 0.25
    exact = norm.pdf((np.log(S / K) - 0.5 * s * s * T) / (s * np.sqrt(T))) / (S * s * np.sqrt(T))
    pw, lr, bd = X.digital_delta_estimators(S, K, T, s, 100000, seed=1)
    assert np.all(pw == 0)
    for e in (lr, bd):
        assert e.mean() == pytest.approx(exact, abs=3 * e.std() / np.sqrt(len(e)))
    assert bd.std() < lr.std() / 3


# ---------------------------------------------------------------------------
# Part 8 expansion: control (HJB by finite differences, viscosity, costs, stopping, crowds, robust, PPO with costs)
# ---------------------------------------------------------------------------
def test_control_hjb_fd_matches_merton():
    from explainer.quant.house import control as C
    o = C.hjb_fd_merton(0.08, 0.02, 0.18, 3.0, T=5.0, n_t=100, n_y=101)
    m = np.abs(o["y"]) <= 1.5
    assert np.max(np.abs(o["pi"][m] - C.merton_fraction(0.08, 0.02, 0.18, 3.0))) < 1e-3
    assert np.max(np.abs(o["V"][m] / o["exact"][m] - 1)) < 5e-3


def test_control_eikonal_monotone_vs_central():
    from explainer.quant.house import control as C
    up = C.eikonal_march(41, "upwind", t_end=3.0)
    assert np.max(np.abs(up["u"] - (1 - np.abs(up["x"])))) < 1e-10
    ce = C.eikonal_march(41, "central", t_end=3.0)
    assert not np.all(np.isfinite(ce["u"])) or np.max(np.abs(ce["u"] - (1 - np.abs(ce["x"])))) > 1.0


def test_control_consumption_rate():
    from explainer.quant.house import control as C
    assert abs(C.merton_consumption_rate(0.03, 0.08, 0.02, 0.18, 1.0) - 0.03) < 1e-12  # log utility spends rho
    nu = C.merton_consumption_rate(0.03, 0.08, 0.02, 0.18, 3.0)
    assert abs(float(C.merton_consumption_rate(0.03, 0.08, 0.02, 0.18, 3.0, tau=1e6)) - nu) < 1e-9
    assert float(C.merton_consumption_rate(0.03, 0.08, 0.02, 0.18, 3.0, tau=0.01)) > 50


def test_control_no_trade_band():
    from explainer.quant.house import control as C
    pm = C.merton_fraction(0.08, 0.02, 0.18, 3.0)
    b = C.no_trade_band(0.08, 0.02, 0.18, 3.0, 0.01, 1 / 12, 120)
    assert b["lo"] < pm < b["hi"]
    half = 0.5 * (b["hi"] - b["lo"])
    assert 0.5 * C.band_halfwidth_asymptotic(0.08, 0.02, 0.18, 3.0, 0.01) < half < 1.3 * C.band_halfwidth_asymptotic(
        0.08, 0.02, 0.18, 3.0, 0.01)
    z = C.no_trade_band(0.08, 0.02, 0.18, 3.0, 0.0, 1 / 12, 60)  # no cost: no band beyond the grid step
    assert z["hi"] - z["lo"] < 0.01


def test_control_snell_and_perpetual_put():
    from explainer.quant.house import control as C
    g = np.array([0, 2, 5, 3, 1, 4, 8, 6, 3, 2, 3, 5, 9, 7, 6, 4, 2, 3, 6, 4, 0], float)
    U = C.snell_envelope(g, tol=1e-14)["U"]
    assert np.max(np.abs(U - C.concave_majorant(g))) < 1e-10
    p = C.perpetual_put(100, 0.05, 0.3)
    bs = np.linspace(30, 95, 651)
    v = C.perpetual_put_value(100.0, 100, 0.05, 0.3, bs)
    assert abs(bs[np.argmax(v)] - p["b"]) < 0.2  # smooth fit is the value-maximizing level
    h = 1e-4  # and the curve leaves the payoff with slope -1
    d = (C.perpetual_put_value(p["b"] + h, 100, 0.05, 0.3, p["b"]) - (100 - p["b"])) / h
    assert abs(d + 1) < 1e-3


def test_control_mfg_liquidation_matches_closed_form():
    from explainer.quant.house import control as C
    for N in (1, 2, np.inf):
        o = C.mfg_liquidation(N, 4.0, 1.0, T=1.0, n=400, iters=500)
        assert np.max(np.abs(o["Q"][:, 0] - C.liquidation_closed(N, 4.0, 1.0, 1.0, o["t"]))) < 1e-5


def test_control_cpt_robust_drawdown():
    from explainer.quant.house import control as C
    # CPT of a sure gain is its value; a symmetric 50/50 gamble is negative (loss aversion)
    assert abs(C.cpt_value([0.1, 0.1]) - 0.1 ** 0.88) < 1e-12
    assert C.cpt_value([-0.1, 0.1]) < 0
    assert abs(C.robust_fraction(0.08, 0.02, 0.18, 3.0, 0.0) - C.merton_fraction(0.08, 0.02, 0.18, 3.0)) < 1e-12
    th = C.theta_for_detection(0.2, 0.08, 0.02, 0.18, 3.0, 50)
    pi = C.robust_fraction(0.08, 0.02, 0.18, 3.0, th)
    assert abs(C.detection_error(th * pi * 0.18 ** 2, 0.18, 50) - 0.2) < 1e-9
    assert C.grossman_zhou_fraction(0.8, 1.0, 0.8, 1.5) == 0.0
    assert abs(C.grossman_zhou_fraction(1.0, 1.0, 0.8, 1.5) - 0.3) < 1e-12


def test_control_simulate_rebalance_and_ppo_rebalance_runs():
    from explainer.quant.house import control as C
    pm = C.merton_fraction(0.08, 0.02, 0.18, 1.0)
    free = C.simulate_rebalance(lambda n, p: np.full_like(p, pm), 0.08, 0.02, 0.18, 0.0, 10.0, 40, paths=20000, seed=1)
    assert abs(free["growth"] - C.growth_continuous(pm, 0.06, 0.18, 0.02)) < 0.005
    o = C.ppo_rebalance(0.08, 0.02, 0.18, 0.01, iters=2, batch=64, seed=0, snapshots=(0, 1))
    assert len(o["mean_target"]) == 2 and o["final"].shape == o["grid_p"].shape


def test_neural_sde_generator_learns():
    torch = pytest.importorskip("torch")
    from explainer.quant.house import deep

    torch.set_num_threads(1)
    real = np.random.default_rng(0).standard_normal((400, 16)) * 1.5
    m, curve, fans = deep.train_nsde(real, L=16, iters=40, batch=64, lr=1e-2, depth=3, every=20, n_show=4)
    assert m.sample(5).shape == (5, 16) and set(fans) == {0, 20, 40} and fans[0].shape == (4, 16)
    assert np.mean(curve[-10:]) < 0.5 * np.mean(curve[:5])


# ---------------------------------------------------------------- stochvol, expanded (Part 13)


def test_cgmy_martingale_and_vg_limit():
    from explainer.quant.house import stochvol as sv

    for Y in (-0.5, 0.5, 1.5):
        assert abs(sv.cgmy_cf(np.array([-1j]), 0.7, 0.4, 3.0, 5.0, Y)[0] - 1) < 1e-12
    s, nu, th = 0.5, 0.2, -0.1  # VG's Levy density is CGMY's with Y = 0, C = 1/nu
    a = np.sqrt(th ** 2 * nu ** 2 / 4 + s ** 2 * nu / 2)
    M, G = 1 / (a + th * nu / 2), 1 / (a - th * nu / 2)
    u = np.linspace(0, 20, 41)
    assert np.max(np.abs(sv.cgmy_cf(u, 0.5, 1 / nu, G, M, 0.0) - sv.vg_cf(u, 0.5, s, nu, th))) < 1e-12
    assert np.max(np.abs(sv.cgmy_cf(u, 0.5, 1 / nu, G, M, 1e-4) - sv.vg_cf(u, 0.5, s, nu, th))) < 1e-3


def test_merton_series_equals_cos():
    from explainer.quant.house import stochvol as sv

    K = np.array([70.0, 90, 100, 110, 140])
    for cp in (1, -1):
        a = sv.merton_series(100.0, K, 0.5, 0.3, 1.5, -0.1, 0.2, cp=cp)
        b = sv.cos_price(lambda u, T: sv.bs_cf(u, T, 0.3) * sv.merton_jump_cf(u, T, 1.5, -0.1, 0.2), 100.0, K, 0.5, cp,
                         N=4096)
        assert np.max(np.abs(a - b)) < 1e-8


def _synthetic_quotes(name, x):
    from explainer.quant.house import stochvol as sv

    T = np.repeat([20 / 365, 60 / 365, 180 / 365], 9)
    K = np.tile(np.exp(np.linspace(-0.3, 0.3, 9)), 3)
    iv = np.concatenate([sv.surface_iv(name, x, 1.0, K[T == t], t) for t in np.unique(T)])
    return {"F": np.ones_like(K), "K": K, "T": T, "iv": iv, "cp": np.where(K >= 1, 1, -1), "vega": np.ones_like(K)}


def test_merton_kou_cgmy_calibrate_round_trip_and_trace():
    from explainer.quant.house import stochvol as sv

    for name, x in (("Merton", (0.35, 1.0, -0.15, 0.2)), ("Kou", (0.35, 2.0, 0.4, 12.0, 6.0)),
                    ("CGMY", (0.5, 4.0, 7.0, 0.6))):
        r = sv.calibrate(name, _synthetic_quotes(name, x), max_nfev=200, trace=True)
        assert r["rmse"] < 0.05
        best = min(r["trace"], key=lambda e: e[1])
        assert abs(best[1] - r["rmse"]) < 1e-9 and np.allclose(best[2], r["x"])


def test_calibrate_fixed_parameter_and_regularised():
    from explainer.quant.house import stochvol as sv

    x = (0.25, 3.0, 0.3, 1.2, -0.4)
    Q = _synthetic_quotes("Heston", x)
    lo, hi = list(sv.MODELS["Heston"]["lo"]), list(sv.MODELS["Heston"]["hi"])
    lo[1] = hi[1] = 6.0
    r = sv.calibrate("Heston", Q, lo=lo, hi=hi, max_nfev=200)
    assert r["x"][1] == 6.0
    r0 = sv.calibrate("Heston", Q, x0=(0.2, 2.0, 0.25, 1.0, -0.2), max_nfev=200)
    g0 = sv.calibrate_reg("Heston", Q, (0.2, 2.0, 0.25, 1.0, -0.2), 0.0, max_nfev=200)
    assert abs(r0["rmse"] - g0["rmse"]) < 1e-6 and np.allclose(r0["x"], g0["x"], rtol=1e-4, atol=1e-6)
    prev = (0.2, 2.0, 0.25, 1.0, -0.2)
    big = sv.calibrate_reg("Heston", Q, prev, 1e6, max_nfev=200)
    assert np.allclose(big["x"], prev, rtol=1e-3, atol=1e-4)


def test_slv_paths_reprice_local_vol():
    from explainer.quant.house import bs as B, volsurface as V, stochvol as sv

    fit = {"T": np.array([0.1, 0.3]), "theta": np.array([0.016, 0.048]), "rho": -0.3, "eta": 0.6, "gamma": 0.5}
    X = sv.slv_paths(V.local_vol_fn(fit), (0.16, 3.0, 0.16, 1.5, -0.4), 60, 20_000, mix=0.5, n_sub=4000, seed=3)
    T = 60 / 365
    for k in (-0.1, 0.0, 0.1):
        cp = 1 if k >= 0 else -1
        p = np.mean(np.maximum(cp * (np.exp(X[-1]) - np.exp(k)), 0))
        assert abs(B.implied_vol(p, 1.0, np.exp(k), T, 0.0, 0.0, cp) - np.sqrt(V.ssvi_surface_w(fit, k, T) / T)) < 0.01


def test_heston_vix_jensen_and_forward_start():
    from explainer.quant.house import stochvol as sv

    v0, ka, th, xi = 0.2, 4.0, 0.25, 2.0
    T = 30 / 365
    r = sv.heston_vix_options(v0, ka, th, xi, T, [0.3, 0.45, 0.6])
    ev = th + (v0 - th) * np.exp(-ka * T)
    assert r["future"] <= np.sqrt(sv.heston_vix2(ev, ka, th)) + 1e-9  # Jensen: E[VIX] <= sqrt(E[VIX^2])
    assert np.allclose(r["call"] - r["put"], r["future"] - np.array([0.3, 0.45, 0.6]), atol=1e-12)
    x = (0.04, 1.5, 0.04, 1.0, -0.7)
    p = sv.heston_forward_start(x, 0.5, 0.25, [0.0], n=400)[0]
    S = sv.heston_qe(1.0, *x, 0.75, 75, 100_000, seed=3)
    pay = np.maximum(S[-1] / S[50] - 1, 0)
    assert abs(pay.mean() - p) < 4 * pay.std() / np.sqrt(len(pay))


def test_sabr_pde_density_is_a_density():
    from explainer.quant.house import bs, stochvol as sv

    r = sv.sabr_pde_density(0.03, 0.035, 0.5, -0.3, 0.4, 1.0, n=300, f_max=0.25, n_t=400, K=[0.03])
    assert abs(r["mass"] - 1) < 1e-10 and r["Q"].min() >= 0 and abs(r["mean"] - 0.03) < 1e-6
    iv = bs.implied_vol(float(r["call"][0]), 0.03, 0.03, 1.0, 0.0, 0.0, 1)
    assert abs(iv - sv.sabr_iv(0.03, 0.03, 1.0, 0.035, 0.5, -0.3, 0.4)[0]) < 0.003


def test_mv_delta_minimises_hedge_variance():
    from explainer.quant.house import stochvol as sv

    g = np.random.default_rng(0)
    S, delta, vega, beta = 100.0, 0.5, 20.0, -0.6
    ret = 0.03 * g.standard_normal(200_000)
    dsig = beta * ret + 0.01 * g.standard_normal(len(ret))
    dC = delta * S * ret + vega * dsig  # an option's change, to first order
    mv = sv.mv_delta(delta, vega, beta, S)
    e_bs, e_mv = dC - delta * S * ret, dC - mv * S * ret
    assert abs(e_mv.var() - (vega * 0.01) ** 2) < 0.02 * (vega * 0.01) ** 2 and e_mv.var() < 0.3 * e_bs.var()


# ---------------------------------------------------------------------------
# Part 17's expansion (deep.py): traces reproduce the plain trainers; the new objectives and classical twins
# ---------------------------------------------------------------------------
def test_deep_traces_reproduce_plain_trainers():
    from explainer.quant.house import deep
    import torch

    rng = np.random.default_rng(0)
    X = rng.standard_normal((300, 2))
    y = (X[:, :1] ** 2 + X[:, 1:]).astype(float)
    a = deep.train_mlp_regressor(X, y, width=8, depth=2, epochs=3, seed=4)
    b, curve, snaps = deep.train_mlp_trace(X, y, width=8, depth=2, epochs=3, seed=4, every=1, snap_every=1,
                                           snap_fn=lambda n: 0)
    xt = torch.tensor(X[:5], dtype=torch.float32)
    with torch.no_grad():
        assert torch.allclose(a(xt), b(xt))
    assert len(curve) == 3 and sorted(snaps) == [0, 1, 2, 3]
    mkt = deep.bachelier_basket(3, seed=1)
    Xb, Yb, dYb = deep.bachelier_samples(mkt, 128, seed=2)
    f1 = deep.train_differential(Xb, Yb, dYb, epochs=4, seed=3)
    f2, c2, s2 = deep.train_differential_trace(Xb, Yb, dYb, epochs=4, seed=3, snap_at=(0, 4), snap_fn=lambda f: 1)
    assert np.allclose(f1(Xb[:5])[0], f2(Xb[:5])[0], atol=1e-6) and sorted(s2) == [0, 4]


def test_gp_with_gradients_interpolates_values_and_gradients():
    from explainer.quant.house import deep

    g = np.linspace(-1, 1, 5)
    X = np.array([(a, b) for a in g for b in g])
    f = X[:, 0] ** 2 + 0.5 * X[:, 1] ** 2
    dY = np.c_[2 * X[:, 0], X[:, 1]]
    m, sd, gr = deep.gp_with_gradients(X, f, dY, X, ls=1.0, sf=2.0, noise_y=1e-10, noise_d=1e-10, grad=True)
    assert np.max(np.abs(m - f)) < 1e-4 and np.max(np.abs(gr - dY)) < 1e-4 and np.max(sd) < 1e-3


def test_gbm_mu_zero_reproduces_gbm_and_merton_leland_closed_forms():
    from explainer.quant.house import deep
    import math
    import torch

    a = deep.gbm_torch(50, 10, 0.1, 0.2, 100.0, torch.Generator().manual_seed(1))
    b = deep.gbm_torch_mu(50, 10, 0.1, 0.2, 0.0, 100.0, torch.Generator().manual_seed(1))
    assert torch.equal(a, b)
    assert deep.merton_hedge(100.0, 0.2, 0.3, 1.0) == pytest.approx(0.075)
    assert deep.leland_sigma(0.2, 0.0, 1 / 365) == 0.2
    le = math.sqrt(2 / math.pi) * 0.01 / (0.2 * math.sqrt(1 / 365))
    assert deep.leland_sigma(0.2, 0.005, 1 / 365) == pytest.approx(0.2 * math.sqrt(1 + le))


def test_cvar_ru_minimum_is_the_empirical_cvar():
    from explainer.quant.house import deep
    import torch

    X = torch.randn(20000, generator=torch.Generator().manual_seed(0)) * 2 + 0.3
    ws = torch.linspace(-2, 4, 6001)
    vals = torch.stack([deep.cvar_ru(X, w, 0.5) for w in ws])
    assert float(vals.min()) == pytest.approx(float(deep.cvar(X, 0.5)), abs=1e-3)


def test_train_hedger_p_with_no_drift_is_train_hedger():
    from explainer.quant.house import deep

    _, c1, _ = deep.train_hedger("mlp", 0.0, iters=3, batch=256, seed=5)
    _, c2, _ = deep.train_hedger_p("mlp", 0.0, 0.0, iters=3, batch=256, seed=5)
    assert np.allclose(c1, c2)


def test_ww_band_hedger_starts_at_whalley_wilmott():
    from explainer.quant.house import deep, quoting
    import torch

    pol = deep.WWBandHedger(0.005, seed=0)
    T = 30 / 365
    with torch.no_grad():
        lo, hi = pol.band(torch.zeros(1), torch.full((1,), 0.5))
    ww = quoting.ww_band(100.0, 100.0, 0.5 * T, 0.2, 0.005, gamma_risk=1.0)
    assert float(lo) == pytest.approx(ww["lo"], abs=1e-3) and float(hi) == pytest.approx(ww["hi"], abs=1e-3)


def test_garch_paths_unconditional_variance():
    from explainer.quant.house import deep
    import torch

    params = (0.05, 0.05, 0.08, 0.85)
    res = np.random.default_rng(0).standard_normal(5000)
    _, e = deep.garch_paths_torch(params, res, 4000, 200, gen=torch.Generator().manual_seed(0))
    hbar = 0.05 / (1 - 0.05 - 0.04 - 0.85)
    assert float(e.pow(2).mean()) == pytest.approx(hbar, rel=0.1)


def test_calibrate_neural_trace_matches_calibrate_neural():
    from explainer.quant.house import deep
    import torch

    torch.manual_seed(0)
    net = deep.calib_net(width=8, depth=1)
    T = np.array([0.05, 0.1, 0.3])
    k = np.array([-0.1, 0.0, 0.1])
    iv = np.array([0.6, 0.55, 0.5])
    a = deep.calibrate_neural(net, T, k, iv, starts=2, iters=10)
    b = deep.calibrate_neural_trace(net, T, k, iv, starts=2, iters=10, every=5)
    assert np.allclose(a["x"], b["x"]) and len(b["traces"]) == 2 and len(b["traces"][0]["step"]) == 3


def test_ddpm_snapshots_end_at_the_sample():
    from explainer.quant.house import deep

    real = np.random.default_rng(0).standard_normal((64, 8))
    s1, _ = deep.train_ddpm(real, steps=20, iters=5, batch=16, width=16)
    s2, curve, abar = deep.train_ddpm_snap(real, steps=20, iters=5, batch=16, width=16)
    x, snaps = s2(6, seed=3, snap_at=(20, 10, 0))
    assert np.allclose(snaps[0], x) and np.allclose(x, s1(6, seed=3), atol=1e-6) and sorted(snaps) == [0, 10, 20]


def test_deep_bsde_snap_linear_check():
    from explainer.quant.house import deep

    p = dict(deep.DEFAULT_RISK, d=10, delta=1.0)
    # 300 steps leave u0 a few units short; 800 reach the Monte Carlo price to within a few cents
    r = deep.deep_bsde_snap(p, iters=800, batch=256, lr=0.05, seed=0, snap_at=(0, 800), n_snap=64)
    mc, _ = deep.no_default_price(p, n=100000)
    assert abs(r["u0"] - mc) < 1.5 and r["snaps"][800]["Ypath"].shape == (32, 41)


def test_stopping_regions_last_date():
    from explainer.quant.house import deep

    p = dict(deep.MAX_CALL, d=2)
    r = deep.deep_stopping(p, steps=80, batch=2048, n_eval=100000, seed=0)
    grid, reg = deep.stopping_regions(r["nets"], p, grid=np.array([60.0, 100.0, 150.0]), dates=[p["N"] - 1])
    R = reg[p["N"] - 1]  # rows S2, columns S1
    assert R[0, 2] == 1 and R[1, 1] == 0


# ---------------------------------------------------------------------------
# Part 10: the solver's frozen entries, the heat kernel, Leland, BAW, Kim's premium, portfolio insurance
# ---------------------------------------------------------------------------
def test_implied_vol_freezes_converged_quotes():
    from explainer.quant.house import bs as bs_

    # a short-dated deep out-of-the-money call (slow) next to an at-the-money one (fast): once converged, an entry
    # must stay converged while the other iterates
    F, K, T = np.array([100.0, 100.0]), np.array([100.0, 175.0]), np.array([0.5, 16 / 365])
    iv = np.array([0.45, 0.80])
    p = bs_.price(F, K, T, iv)
    sig, its = bs_.implied_vol(p, F, K, T, return_iterations=True)
    assert np.allclose(sig, iv, atol=1e-10)
    err = np.array([np.abs(x - iv) for x in its])
    for j in range(2):
        first = int(np.argmax(err[:, j] < 1e-10))
        assert err[first:, j].max() < 1e-10  # never knocked out again
    rng = np.random.default_rng(3)
    n = 400
    F, K = np.full(n, 100.0), 100 * np.exp(rng.uniform(-1.0, 1.0, n))
    T, iv, cp = rng.uniform(2 / 365, 1.0, n), rng.uniform(0.2, 1.2, n), rng.choice([-1, 1], n)
    p = bs_.price(F, K, T, iv, 0, 0, cp)
    sig = bs_.implied_vol(p, F, K, T, 0, 0, cp)
    tv = p - np.maximum(cp * (F - K), 0.0)  # time value: below ~1e-4 the price no longer pins the volatility down
    ok = np.isfinite(sig) & (tv > 1e-4)
    assert ok.mean() > 0.9 and np.allclose(sig[ok], iv[ok], atol=1e-8)


def test_heat_price_matches_the_formula():
    for cp in (1, -1):
        hp = bs.heat_price(lambda s, cp=cp: np.maximum(cp * (s - 100.0), 0.0), 100.0, 1.0, 0.2, 0.05, kinks=(100.0,))
        assert abs(hp - float(bs.price(100.0, 100.0, 1.0, 0.2, 0.05, 0.0, cp))) < 1e-9
    dig = bs.heat_price(lambda s: (s > 110.0).astype(float), 100.0, 0.5, 0.3, 0.02, kinks=(110.0,))
    d2 = bs.d1_d2(100.0, 110.0, 0.5, 0.3, 0.02)[1]
    assert abs(dig - np.exp(-0.02 * 0.5) * bs.ndtr(d2)) < 1e-9


def test_leland_vol_problem_four():
    assert round(float(bs.leland_vol(0.2, 0.002, 1 / 252)), 3) == 0.212
    assert round(float(bs.leland_vol(0.2, 0.002, 1 / 52)), 3) == 0.206
    assert float(bs.leland_vol(0.2, 0.0, 1 / 252)) == pytest.approx(0.2)


def test_baw_against_the_tree():
    o = bs.baw(100.0, 100.0, 1.0, 0.2, 0.05, cp=-1)
    tree = trees.crr(100.0, 100.0, 1.0, 0.2, 0.05, N=2000, cp=-1, american=True)["price"]
    assert abs(float(o["price"]) - tree) < 0.02 and 75 < o["critical"] < 90
    c = bs.baw(100.0, 100.0, 1.0, 0.2, 0.05, cp=1)  # no dividends: never exercised early
    assert float(c["price"]) == pytest.approx(float(bs.price(100.0, 100.0, 1.0, 0.2, 0.05)))
    deep = bs.baw(60.0, 100.0, 1.0, 0.2, 0.05, cp=-1)
    assert float(deep["price"]) == pytest.approx(40.0)


def test_early_exercise_premium_integral():
    pb = trees.put_boundary(100.0, 100.0, 1.0, 0.2, 0.05, N=2000)
    eu = float(bs.price(100.0, 100.0, 1.0, 0.2, 0.05, 0.0, -1))
    prem = trees.early_exercise_premium(100.0, 100.0, 0.05, 0.2, pb["times"], pb["boundary"])
    assert abs(eu + prem - pb["price"]) < 0.015
    assert np.nanmax(pb["boundary"] - pb["raw"]) > 0  # interpolation lifts the staircase
    zero = trees.early_exercise_premium(100.0, 100.0, 0.0, 0.2, pb["times"], pb["boundary"])
    assert zero == pytest.approx(0.0)


def test_replicate_put_keeps_the_floor_without_gaps():
    t, S = paths.gbm(100.0, 0.0, 0.15, 1.0, 252, 2000, seed=11)
    ret = S[:, 1:] / S[:, :-1] - 1
    o = hedge.replicate_put(ret, 0.0, 95.0, 1.0, 0.15)
    ends, fv = o["V"][:, -1], o["floor_value"]
    assert np.mean(ends >= 0.98 * fv) >= 0.99
    gap = np.zeros(252)
    gap[100] = -0.25
    o = hedge.replicate_put(gap, 0.0, 95.0, 1.0, 0.15, start=100.0)
    assert o["V"][-1] < fv and o["w"][101] < o["w"][99]


def test_trial_counter_is_cumulative_by_part():
    """Every registration has a part, and the counter a part shows never goes down from one part to the next."""
    from explainer.quant.house import pit
    vals = [pit.trials_upto(n) for n in range(1, 44)]
    assert all(a <= b for a, b in zip(vals, vals[1:]))
    assert vals[-1] == pit.trials_so_far()


# ---------------------------------------------------------------------------
# Part 18: the rates desk
# ---------------------------------------------------------------------------
def test_bond_at_its_coupon_is_par_and_yield_inverts():
    from explainer.quant.house import rates as R
    assert abs(R.bond_price(0.045, 0.045, 10) - 100) < 1e-10
    p = R.bond_price(0.03, 0.05, 7)
    assert abs(R.bond_yield(p, 0.03, 7) - 0.05) < 1e-12


def test_bond_risk_against_finite_differences():
    from explainer.quant.house import rates as R
    c, y, T, h = 0.04, 0.047, 12, 1e-5
    r = R.bond_risk(c, y, T)
    up, dn = R.bond_price(c, y + h, T), R.bond_price(c, y - h, T)
    assert abs(-(up - dn) / (2 * h) / r["price"] - r["modified"]) < 1e-6
    assert abs((up - 2 * r["price"] + dn) / h ** 2 / r["price"] - r["convexity"]) < 1e-3
    assert abs(R.bond_risk(0.0, 0.04, 10, freq=1)["macaulay"] - 10) < 1e-12  # a zero's duration is its maturity


def test_bootstrap_reprices_its_par_bonds():
    from explainer.quant.house import rates as R
    T = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    y = [0.052, 0.051, 0.049, 0.045, 0.043, 0.041, 0.041, 0.042, 0.046, 0.044]
    c = R.bootstrap_par(T, y)
    for Ti, yi in zip(T, y):
        if Ti > 1:
            assert abs(c.par(Ti) - yi) < 1e-10
    assert abs(c.fwd(2, 3) * 1 - (c.zero(3) * 3 - c.zero(2) * 2)) < 1e-12


def test_fit_nss_recovers_a_svensson_curve():
    from explainer.quant.house import rates as R
    t = np.array([0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30])
    y = R.nss(t, [4.5, -1.2, 2.0, -1.5], (1.7, 9.0))
    f = R.fit_nss(t, y)
    assert f["rmse"] < 1e-6


def test_conversion_factor_is_the_price_at_six_percent():
    from explainer.quant.house import rates as R
    assert R.conversion_factor(0.06, 9, 0) == 1.0
    assert R.conversion_factor(0.06, 9, 3) == 0.9999  # linear accrual between coupon dates
    # on a coupon date (z = 0) the factor is the bond's price per 1 at a 6% yield
    assert abs(R.conversion_factor(0.04, 8, 0) - round(R.bond_price(0.04, 0.06, 8) / 100, 4)) < 1e-12
    assert R.conversion_factor(0.04, 8, 4) == R.conversion_factor(0.04, 8, 3)  # quarters for the 10-year


def test_key_rate_dv01s_sum_to_the_parallel_dv01():
    from explainer.quant.house import rates as R
    c = R.Curve([0.5, 2, 5, 10, 30], [0.04, 0.042, 0.043, 0.045, 0.047])
    t, cf = np.arange(1, 21) / 2, np.r_[np.full(19, 2.0), 102.0]
    kr = R.key_rate_dv01(t, cf, c, [0.5, 2, 5, 10, 30])
    par = float(np.sum(cf * c.df(t) * (np.exp(1e-4 * t) - 1)))
    assert abs(kr.sum() - par) < 1e-4 * par  # equal to first order


def test_fly_is_neutral_to_level_and_slope():
    from explainer.quant.house import rates as R
    rng = np.random.default_rng(0)
    L = np.linalg.qr(rng.normal(size=(6, 6)))[0].T
    w = R.fly_weights(L, (1, 3, 5))
    assert np.allclose(L[[0, 1]][:, [1, 3, 5]] @ w, 0)


def test_swap_sofr_taylor():
    from explainer.quant.house import rates as R
    c = R.Curve([1, 5, 10], [0.03, 0.035, 0.04])
    s = R.par_swap_rate(c, 10, freq=2)
    assert abs(s - c.par(10)) < 1e-12 and abs(R.swap_value(c, 10, s, freq=2)) < 1e-12
    assert abs(R.compound_in_arrears([0.05], [1]) - 0.05) < 1e-12
    assert R.compound_in_arrears([0.05] * 90, [1] * 90) > 0.05
    assert float(R.taylor_rule(2.0, 0.0)) == 4.0


def test_ldi_spiral_amplifies_and_loses_nav():
    from explainer.quant.house import rates as R
    a = R.ldi_spiral(50, impact_bp_per_pct=0.0)
    b = R.ldi_spiral(50, impact_bp_per_pct=1.5)
    assert a["dy_bp"][-1] == 50 and b["dy_bp"][-1] > 50 and b["nav"][-1] < a["nav"][-1]


def test_acm_finds_no_term_premium_where_there_is_none():
    """Yields generated by an affine model with zero prices of risk: the regression should find a premium near 0
    and reprice the curve."""
    from explainer.quant.house import rates as R
    rng = np.random.default_rng(3)
    K, T, N = 3, 20000, 60  # long: with a 0.99 root the prices of risk are estimated slowly
    Phi = np.diag([0.99, 0.95, 0.9])
    mu = np.array([0.0, 0.0, 0.0])
    Sigma = np.diag([2e-7, 1e-7, 5e-8])
    d0, d1 = 0.003, np.array([1.0, 0.5, -0.3])
    A, B = R._affine(mu, Phi, Sigma, 0.0, d0, d1, np.zeros(K), np.zeros((K, K)), N)
    x = np.zeros((T, K))
    eps = rng.multivariate_normal(np.zeros(K), Sigma, size=T)
    for t in range(1, T):
        x[t] = x[t - 1] @ Phi.T + eps[t]
    logp = A[1:][None, :] + x @ B[1:].T + rng.normal(0, 1e-6, (T, N)) * np.arange(1, N + 1)
    out = R.acm_decompose(logp, K=3, rx_mats=np.arange(6, N, 6))
    assert np.mean(np.abs(out["tp"][:, -1])) < 1.5e-3  # under 15 bp at five years, on average
    assert out["fit_rmse"] < 2e-4


# ---------------------------------------------------------------------------
# Part 19: term-structure models
# ---------------------------------------------------------------------------
def test_affine_riccati_matches_vasicek_and_cir():
    from explainer.quant.house import termstructure as TS
    T = np.array([0.5, 2.0, 10.0])
    assert np.allclose(TS.affine_zcb(0.03, 0.3, 0.05, 0.01 ** 2, 0.0, T), TS.vasicek_zcb(0.03, 0.3, 0.05, 0.01, T),
                       rtol=1e-8)
    assert np.allclose(TS.affine_zcb(0.03, 0.3, 0.05, 0.0, 0.08 ** 2, T), TS.cir_zcb(0.03, 0.3, 0.05, 0.08, T),
                       rtol=1e-8)


def _hw():
    from explainer.quant.house import rates as R, termstructure as TS
    c = R.Curve([0.5, 1, 2, 5, 10, 30], [0.04, 0.039, 0.037, 0.038, 0.041, 0.045])
    return c, TS.HullWhite(c, a=0.05, sigma=0.01)


def test_hull_white_fits_the_curve_and_simulates_it():
    c, hw = _hw()
    T = np.array([1.0, 3.0, 7.0, 15.0])
    assert np.allclose(hw.zcb(0.0, T, 0.0), c.df(T), rtol=1e-12)
    x, D = hw.simulate_x(T, 200000, seed=1)
    assert np.allclose(D.mean(0), c.df(T), rtol=3e-3)
    # a bond's price at t from the formula equals the discounted expectation of 1 at T
    t, S = 3.0, 10.0
    x3, D3 = hw.simulate_x(np.array([t, S]), 200000, seed=2)
    assert abs(np.mean(D3[:, 0] * hw.zcb(t, S, x3[:, 0])) - c.df(S)) < 3e-3 * c.df(S)


def test_hull_white_options_parity_and_jamshidian():
    from explainer.quant.house import termstructure as TS
    c, hw = _hw()
    K, T, S = 0.8, 2.0, 7.0
    call, put = hw.zcb_option(K, T, S, 1), hw.zcb_option(K, T, S, -1)
    assert abs(call - put - (c.df(S) - K * c.df(T))) < 1e-12
    # payer minus receiver swaption is a forward-starting payer swap
    k, T0, ten = 0.04, 2.0, 5.0
    pay, rec = hw.swaption(k, T0, ten, payer=True), hw.swaption(k, T0, ten, payer=False)
    times = T0 + np.arange(1, 6)
    fwd_swap = c.df(T0) - c.df(times[-1]) - k * c.df(times).sum()
    assert abs(pay - rec - fwd_swap) < 1e-10


def test_bachelier_and_normal_sabr():
    from explainer.quant.house import termstructure as TS
    p = TS.bachelier(0.03, 0.031, 2.0, 0.009)
    assert abs(TS.normal_iv(p, 0.03, 0.031, 2.0) - 0.009) < 1e-10
    # with no vol of vol, normal SABR is Bachelier with vol alpha
    assert np.allclose(TS.sabr_normal_iv(0.03, np.array([0.02, 0.03, 0.04]), 1.0, 0.008, 0.0, 0.0, 1e-10), 0.008)


def test_hjm_discounted_bonds_are_martingales():
    from explainer.quant.house import termstructure as TS
    tau = np.linspace(0, 10, 81)
    f0 = 0.03 + 0.01 * (1 - np.exp(-tau / 3))
    vols = np.array([0.008 * np.ones_like(tau), 0.006 * np.exp(-tau / 2)])
    out = TS.hjm_gaussian(f0, tau, vols, T=2.0, n_steps=200, n_paths=20000, seed=0)
    fT = out["curves"][-1]
    P_T = np.exp(-np.trapezoid(fT[:, :41], tau[:41], axis=1))  # P(2, 7)
    P0 = np.exp(-np.trapezoid(f0[:57], tau[:57]))  # P(0, 7)
    assert abs(np.mean(P_T / out["bank"]) / P0 - 1) < 2e-3


def test_lmm_caplets_match_black_and_bachelier():
    from explainer.quant.house import termstructure as TS
    L0 = np.array([0.03, 0.032, 0.034, 0.035])
    o = TS.lmm_caplets(L0, 0.5, 0.2, n_paths=40000, seed=0)
    assert np.allclose(o["mc"], o["exact"], rtol=0.03)
    o = TS.lmm_caplets(L0, 0.5, 0.008, n_paths=40000, seed=0, normal=True)
    assert np.allclose(o["mc"], o["exact"], rtol=0.03)


def test_bermudan_is_worth_at_least_its_best_european():
    from explainer.quant.house import termstructure as TS
    c, hw = _hw()
    out = TS.bermudan_swaption_lsm(hw, 0.04, 1.0, 10.0, n_paths=20000, seed=0)
    assert out["price"] + 3 * out["se"] >= max(out["europeans"])


def test_lattice_bermudan_matches_jamshidian_and_bounds_lsm():
    from explainer.quant.house import termstructure as TS
    c, hw = _hw()
    for t in (1.0, 5.0):  # one exercise date: a European, against the closed form
        assert TS.bermudan_swaption_lattice(hw, 0.04, 1.0, 10.0, dates=[t]) == pytest.approx(
            hw.swaption(0.04, t, 10.0 - t, 1, payer=False), rel=1e-3)
    lat = TS.bermudan_swaption_lattice(hw, 0.04, 1.0, 10.0)
    lsm = TS.bermudan_swaption_lsm(hw, 0.04, 1.0, 10.0, n_paths=20000, seed=0)
    assert lsm["price"] - 3 * lsm["se"] <= lat <= lsm["price"] + 4 * lsm["se"] + 2e-4  # LSM is a lower bound


def test_mbs_oas_below_zero_vol_spread():
    from scipy.optimize import brentq
    from explainer.quant.house import termstructure as TS
    oas = brentq(lambda z: TS.mbs_price(0.065, 0.0, n_paths=200, seed=0, oas=z) - 101.0, -0.02, 0.05)
    zvs = brentq(lambda z: TS.mbs_price(0.065, 0.0, n_paths=2, seed=0, sigma=1e-9, oas=z) - 101.0, -0.02, 0.05)
    assert 0 < oas < zvs  # the option costs the holder yield


def test_mbs_has_negative_convexity():
    from explainer.quant.house import termstructure as TS
    p = [TS.mbs_price(0.065, s, n_paths=300, seed=0) for s in (-0.01, 0.0, 0.01)]
    assert p[0] + p[2] - 2 * p[1] < 0  # concave in rates near par: prepayment caps the upside


# ---------------------------------------------------------------------------
# Part 20: credit
# ---------------------------------------------------------------------------
def test_merton_solve_round_trip_and_kmv_recovers_asset_vol():
    from explainer.quant.house import credit as CR
    V, s, D, r, T = 120.0, 0.25, 100.0, 0.03, 1.0
    E, delta = CR.merton_equity(V, s, D, r, T)
    sE = delta * s * V / E
    v2, s2 = CR.merton_solve(float(E), float(sE), D, r, T)
    assert v2 == pytest.approx(V, rel=1e-6) and s2 == pytest.approx(s, rel=1e-6)
    rng = np.random.default_rng(0)
    n, dt = 750, 1 / 252
    lv = np.log(150.0) + np.cumsum((0.05 - 0.5 * 0.2 ** 2) * dt + 0.2 * np.sqrt(dt) * rng.standard_normal(n))
    Es = CR.merton_equity(np.exp(lv), 0.2, D, r, T)[0]
    out = CR.kmv_iterate(Es, D, r, T)
    assert out["sigma_V"] == pytest.approx(0.2, rel=0.08)
    assert np.all(out["V"] > Es)


def test_black_cox_first_passage_exceeds_terminal_default():
    from explainer.quant.house import credit as CR
    term = CR.merton_pd(100.0, 0.3, 70.0, 0.05, 2.0)
    fp = CR.black_cox_pd(100.0, 0.3, 0.05, 70.0, 2.0)
    assert fp > term > 0
    # Monte Carlo check of the first-passage formula
    rng = np.random.default_rng(1)
    n, steps = 20000, 2000
    dt = 2.0 / steps
    x = np.zeros(n)
    hit = np.zeros(n, bool)
    for _ in range(steps):
        x += (0.05 - 0.045) * dt + 0.3 * np.sqrt(dt) * rng.standard_normal(n)
        hit |= x <= np.log(0.7)
    assert hit.mean() == pytest.approx(fp, abs=0.015)


def test_cds_credit_triangle_bootstrap_and_upfront():
    from explainer.quant.house import credit as CR

    def df(t):
        return np.exp(-0.03 * np.asarray(t, float))
    s = CR.cds_par_spread(5.0, [5.0], [0.02], df, R=0.4)
    assert s == pytest.approx(0.02 * 0.6, rel=0.01)  # spread ~ hazard x (1 - R)
    k, h = CR.bootstrap_hazard([1, 3, 5, 7, 10], [0.006, 0.009, 0.012, 0.014, 0.015], df, R=0.4)
    for T, q in zip([1, 3, 5, 7, 10], [0.006, 0.009, 0.012, 0.014, 0.015]):
        assert CR.cds_par_spread(T, k, h, df, 0.4) == pytest.approx(q, abs=1e-10)
    assert CR.cds_upfront(CR.cds_par_spread(5.0, k, h, df), 5.0, k, h, df) == pytest.approx(0.0, abs=1e-12)
    assert CR.cds_upfront(0.01, 5.0, k, h, df) > 0  # par spread above the 100 bp coupon: the buyer pays upfront


def test_logit_and_gbm_and_auc():
    from explainer.quant.house import credit as CR
    rng = np.random.default_rng(0)
    n = 20000
    X = rng.standard_normal((n, 3))
    eta = -3 + 1.0 * X[:, 0] - 0.5 * X[:, 1]
    y = rng.random(n) < 1 / (1 + np.exp(-eta))
    b = CR.logit_fit(X, y)
    assert np.allclose(b, [-3, 1.0, -0.5, 0.0], atol=0.12)
    # a nonlinear target the logit cannot see but the trees can
    y2 = rng.random(n) < 1 / (1 + np.exp(-(-3 + 2.0 * (np.abs(X[:, 2]) > 1.2))))
    tr, te = slice(0, 15000), slice(15000, None)
    g = CR.GBM(n_trees=150, depth=2, lr=0.1, seed=0).fit(X[tr], y2[tr])
    a_g = CR.auc(y2[te], g.predict_proba(X[te]))
    a_l = CR.auc(y2[te], CR.logit_predict(CR.logit_fit(X[tr], y2[tr]), X[te]))
    assert a_g > 0.65 > a_l
    assert np.argmax(g.importance(3)) == 2
    # AUC against the pairwise definition
    s = rng.random(300)
    yy = rng.random(300) < 0.3
    pair = np.mean([(a > c) + 0.5 * (a == c) for a in s[yy] for c in s[~yy]])
    assert CR.auc(yy, s) == pytest.approx(pair, abs=1e-12)


def test_vasicek_pool_basel_and_tranches():
    from explainer.quant.house import credit as CR
    pd_, rho = 0.02, 0.15
    q = CR.vasicek_quantile(0.99, pd_, rho)
    assert CR.vasicek_loss_cdf(q, pd_, rho) == pytest.approx(0.99, abs=1e-9)
    x = np.linspace(1e-6, 1 - 1e-6, 200001)
    assert np.trapezoid(x * CR.vasicek_loss_pdf(x, pd_, rho), x) == pytest.approx(pd_, rel=1e-3)
    # the Basel risk weight for PD 1%, LGD 45%, M 2.5 is 92.32% (BCBS example tables)
    assert 12.5 * CR.basel_irb_k(0.01) == pytest.approx(0.9232, abs=0.002)
    # tranches partition the pool's expected loss
    R = 0.4
    cuts = [0, 0.03, 0.07, 0.1, 0.15, 0.3, 1.0]
    tot = sum((d - a) * CR.lhp_tranche_el(pd_, rho, R, a, d) for a, d in zip(cuts[:-1], cuts[1:]))
    assert tot == pytest.approx((1 - R) * pd_, rel=1e-4)
    # a finite pool by simulation approaches the large-pool equity tranche loss
    k, _ = CR.copula_defaults(500, pd_, rho, 20000, seed=0)
    mc = CR.tranche_loss((1 - R) * k / 500, 0, 0.03).mean()
    assert mc == pytest.approx(CR.lhp_tranche_el(pd_, rho, R, 0, 0.03), rel=0.03)
    el = CR.lhp_tranche_el(pd_, 0.3, R, 0, 0.03)
    assert CR.base_correlation(el, pd_, R, 0.03) == pytest.approx(0.3, abs=1e-6)
    # the t copula fattens the senior tail at the same pd and rho
    kg, _ = CR.copula_defaults(200, pd_, rho, 20000, seed=1)
    kt, _ = CR.copula_defaults(200, pd_, rho, 20000, seed=1, nu=4)
    assert np.mean(kt / 200 > 0.15) > np.mean(kg / 200 > 0.15)


# ---------------------------------------------------------------------------
# Part 21: XVA
# ---------------------------------------------------------------------------
def _xva_setup():
    from explainer.quant.house import rates as R, termstructure as TS
    t = np.array([0.5, 1, 2, 3, 5, 7, 10, 20, 30.0])
    c = R.Curve(t, 0.035 + 0.003 * np.log1p(t))
    return c, TS.HullWhite(c, 0.03, 0.01)


def test_par_swap_is_worth_zero_and_exposure_profile_shape():
    from explainer.quant.house import xva as XV
    c, hw = _xva_setup()
    pay = np.arange(1, 11)
    K = float((1 - c.df(10.0)) / c.df(pay).sum())
    v0 = XV.swap_values_hw(hw, np.zeros(1), 0.0, K, 10.0)
    assert abs(v0[0]) < 1e-10
    times = np.linspace(0.25, 10, 40)
    x, _ = hw.simulate_x(times, 4000, seed=0)
    V = np.stack([XV.swap_values_hw(hw, x[:, j], t, K, 10.0) for j, t in enumerate(times)], 1)
    ex = XV.exposure_profile(V)
    assert np.all(ex["EE"] >= 0) and np.all(ex["ENE"] <= 0) and np.all(ex["PFE"] >= ex["EE"] - 1e-12)
    k = int(np.argmax(ex["EE"]))
    assert 0 < k < len(times) - 2 and ex["EE"][-1] < 0.3 * ex["EE"][k]  # the diffusion-amortisation hump


def test_cva_formula_collateral_and_waterfall():
    from explainer.quant.house import xva as XV

    def df(t):
        return np.exp(-0.03 * np.asarray(t, float))
    times = np.linspace(0.5, 5, 10)
    EE = np.full(10, 0.02)
    c = XV.cva(EE, times, df, [5.0], [0.02], R=0.4)
    ref = 0.6 * 0.02 * np.sum(df(times) * np.diff(np.exp(-0.02 * np.r_[0, times])) * -1)
    assert c == pytest.approx(ref, rel=1e-12)
    # bilateral CVA is smaller than unilateral (the bank may default first)
    assert XV.cva(EE, times, df, [5.0], [0.02], own=([5.0], [0.01])) < c
    rng = np.random.default_rng(0)
    V = np.cumsum(rng.standard_normal((2000, 60)) * 0.01, 1)
    tt = np.linspace(1 / 60, 1, 60)
    assert XV.exposure_profile(XV.collateralised(V, tt, mpor=2 / 60))["EPE"] < 0.4 * XV.exposure_profile(V)["EPE"]
    L = rng.exponential(1.0, 1000)
    w = XV.ccp_waterfall(L, 0.5, 0.2, 0.1, 1.0, 0.5)
    assert np.allclose(sum(w.values()), L)


def test_cva_torch_matches_numpy_and_bumps():
    from explainer.quant.house import xva as XV, rates as R, termstructure as TS
    zt = np.array([0.5, 1, 2, 5, 10, 30.0])
    zz = np.array([0.035, 0.036, 0.037, 0.039, 0.041, 0.043])
    swaps = [(0.04, 5.0, 1.0, True)]
    times = np.linspace(0.25, 5, 20)
    c0, gz, gh = XV.cva_torch(zt, zz, [5.0], [0.02], 0.03, 0.01, swaps, times, n_paths=20000, seed=3)
    # numpy reference on the same curve
    hw = TS.HullWhite(R.Curve(zt, zz), 0.03, 0.01)
    x, _ = hw.simulate_x(times, 20000, seed=3)
    V = np.stack([XV.swap_values_hw(hw, x[:, j], t, 0.04, 5.0) for j, t in enumerate(times)], 1)

    def df(t):
        return hw.c.df(t)
    c1 = XV.cva(XV.exposure_profile(V)["EE"], times, df, [5.0], [0.02])
    assert c0 == pytest.approx(c1, rel=0.05)
    # the hazard gradient against a bump of the same torch computation (same random numbers)
    up, _, _ = XV.cva_torch(zt, zz, [5.0], [0.0201], 0.03, 0.01, swaps, times, n_paths=20000, seed=3)
    assert gh[0] == pytest.approx((up - c0) / 1e-4, rel=0.02)
    assert gz[3] > 0  # a payer swap's exposure, and so its CVA, rises with the 5-year rate


def test_sa_ccr_and_simm_like():
    from explainer.quant.house import xva as XV
    t1 = {"notional": 10000, "S": 0, "E": 10, "delta": -1, "mtm": 30}
    t2 = {"notional": 10000, "S": 0, "E": 4, "delta": 1, "mtm": -20}
    both = XV.sa_ccr_ir_ead([t1, t2])["EAD"]
    assert both < XV.sa_ccr_ir_ead([t1])["EAD"] + XV.sa_ccr_ir_ead([t2])["EAD"]  # netting helps
    assert XV.sa_ccr_ir_ead([t1], collateral=30)["RC"] == 0
    s = np.zeros(9)
    s[5] = 1.0
    assert XV.simm_like_ir_delta(s) == pytest.approx(XV.SIMM_RW[5])
    s2 = s.copy()
    s2[4] = -1.0
    assert XV.simm_like_ir_delta(s2) < XV.simm_like_ir_delta(np.abs(s2))  # offsetting tenors net


def test_wrong_way_cva_rises_with_correlation():
    from explainer.quant.house import xva as XV
    c, hw = _xva_setup()
    times = np.linspace(0.25, 10, 40)
    x, _ = hw.simulate_x(times, 6000, seed=0)
    K = float((1 - c.df(10.0)) / c.df(np.arange(1, 11)).sum())
    V = np.stack([XV.swap_values_hw(hw, x[:, j], t, K, 10.0) for j, t in enumerate(times)], 1)
    cv = [XV.wrong_way_cva(V, x, times, c.df, 0.02, rho=r_, seed=1) for r_ in (-0.5, 0.0, 0.5)]
    assert cv[0] < cv[1] < cv[2]


# ---------------------------------------------------------------------------- Part 22: the macro desk
def test_cip_basis_zero_at_parity_and_signs():
    from explainer.quant.house import macro as M
    Q, ru, rf, tau = 1.27, 0.05, 0.01, 0.25
    F = M.cip_forward(Q, ru, rf, tau)
    assert F > Q  # the low-rate currency trades at a forward premium
    assert abs(M.cip_basis(Q, F, ru, rf, tau)) < 1e-12
    # a forward above parity: swapping pounds into dollars costs more than borrowing dollars directly -> negative x
    assert M.cip_basis(Q, F * 1.0005, ru, rf, tau) < 0


def test_fama_regression_recovers_uip_and_carry_sort():
    from explainer.quant.house import macro as M
    rng = np.random.default_rng(0)
    T = 600
    ru = np.full(T, 0.03)
    rf = 0.03 + 0.04 * np.sin(np.arange(T) / 40)
    h = 1 / 12
    s = np.zeros(T)  # s = ln(foreign per dollar); UIP: E[ds] = (rf - ru) h
    for t in range(1, T):
        s[t] = s[t - 1] + (rf[t - 1] - ru[t - 1]) * h + 0.002 * rng.standard_normal()
    out = M.fama_regression(np.exp(-s), ru, rf, h)
    assert out["beta"] == pytest.approx(1.0, abs=0.15)
    ex = np.array([[0.01, 0.0, -0.01, 0.02, -0.02, 0.0]])
    diff = np.array([[5, 4, 3, 2, 1, 0]], float)
    cs = M.carry_sort(ex, diff, k=2)
    assert cs["long"][0] == pytest.approx(0.005) and cs["short"][0] == pytest.approx(-0.01)
    assert cs["ls"][0] == pytest.approx(0.015)


def test_fx_deltas_and_strikes():
    from explainer.quant.house import macro as M
    S, T, sig, rd, rf = 1.10, 0.5, 0.09, 0.045, 0.025
    for kind in ("spot", "forward", "spot_pa", "forward_pa"):
        for cp, d in ((1, 0.25), (-1, -0.25)):
            K = M.strike_from_delta(S, T, sig, rd, rf, d, cp, kind)
            assert float(M.fx_delta(S, K, T, sig, rd, rf, cp, kind)) == pytest.approx(d, abs=1e-8)
    F = S * np.exp((rd - rf) * T)
    for pa, kind in ((False, "forward"), (True, "forward_pa")):
        K = M.atm_dns_strike(F, T, sig, pa)
        assert float(M.fx_delta(S, K, T, sig, rd, rf, 1, kind) + M.fx_delta(S, K, T, sig, rd, rf, -1, kind)) == \
            pytest.approx(0.0, abs=1e-12)
    q = M.smile_quotes(0.08, -0.01, 0.003)
    assert q["25c"] - q["25p"] == pytest.approx(-0.01) and (q["25c"] + q["25p"]) / 2 - q["atm"] == pytest.approx(0.003)
    # Garman-Kohlhagen put-call parity
    c = M.garman_kohlhagen(S, 1.1, T, sig, rd, rf, 1)
    p = M.garman_kohlhagen(S, 1.1, T, sig, rd, rf, -1)
    assert float(c - p) == pytest.approx(S * np.exp(-rf * T) - 1.1 * np.exp(-rd * T), abs=1e-12)


def test_commodity_carry_roll_and_basis():
    from explainer.quant.house import macro as M
    F1 = M.carry_forward(70.0, 1 / 12, 0.05, storage=0.02, convenience=0.10)
    F2 = M.carry_forward(70.0, 2 / 12, 0.05, storage=0.02, convenience=0.10)
    assert M.implied_convenience(F1, F2, 1 / 12, 0.05, storage=0.02) == pytest.approx(0.10)
    # a flat, unchanging curve earns nothing, whichever contract is held
    days = np.array([20200100 + d for d in range(1, 29)] + [20200200 + d for d in range(1, 28)] +
                    [20200300 + d for d in range(1, 30)])
    c = np.full(len(days), 50.0)
    out = M.rolled_front(days, c, c)
    assert np.nanmax(np.abs(out["r"])) == 0
    # WTI's May 2020 contract stopped trading on 21 April 2020
    td = np.array([20200400 + d for d in (1, 2, 3, 6, 7, 8, 9, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27)])
    assert M.wti_last_trade(2020, 5, td) == 20200421
    rp = M.implied_repo(cash_dirty=101.0, futures=110.0, cf=0.92, accrued_delivery=0.5, days=90)
    assert rp == pytest.approx(((110 * 0.92 + 0.5) / 101 - 1) * 4)


def test_attack_model_and_breakeven():
    from explainer.quant.house import macro as M
    a = M.attack_model(peg=1.0, d0=0.5, mu=0.05, alpha=2.0)
    assert a["t_star"] == pytest.approx(8.0)  # (1 - 0.1 - 0.5)/0.05
    assert a["t_star"] < a["reserves_if_no_attack_run_out"]  # the attack comes before reserves would run out
    i = np.searchsorted(a["t"], a["t_star"])
    assert a["s"][i + 1] == pytest.approx(a["shadow"][i + 1]) and a["R"][i + 1] == 0
    assert M.breakeven(0.045, 0.02) == pytest.approx(0.025)
    d = np.array([20000101 + 100 * m for m in range(12)] + [20010101 + 100 * m for m in range(12)])
    cpi = np.r_[np.full(12, 100.0), np.full(12, 103.0)]
    assert M.realised_inflation(d, cpi, 20000115, 1) == pytest.approx(0.03)


# ---------------------------------------------------------------------------- Part 23: the expected-return framework
def test_frontier_gmv_tangency():
    from explainer.quant.house import premia as P
    mu = np.array([0.06, 0.08, 0.10])
    S = np.array([[0.04, 0.006, 0.004], [0.006, 0.09, 0.012], [0.004, 0.012, 0.16]])
    g = P.gmv(S)
    k = P.frontier_constants(mu, S)
    assert g["var"] == pytest.approx(1 / k["C"])
    m = 0.085
    w = P.frontier_weights(m, mu, S)
    assert w.sum() == pytest.approx(1.0) and w @ mu == pytest.approx(m)
    assert np.sqrt(w @ S @ w) == pytest.approx(float(P.frontier_sigma(m, mu, S)))
    t = P.tangency(mu, S, rf=0.03)
    assert (t["mean"] - 0.03) / t["sd"] == pytest.approx(t["sharpe"])
    two = P.two_asset_gmv(0.2, 0.2, 0.5)
    assert two["w1"] == pytest.approx(0.5) and two["sd"] == pytest.approx(0.2 * np.sqrt(0.75))


def test_capm_hj_and_sdf():
    from explainer.quant.house import premia as P
    rng = np.random.default_rng(0)
    T = 4000
    m = 0.005 + 0.04 * rng.standard_normal(T)
    betas = np.array([0.5, 1.0, 1.5])
    R = m[:, None] * betas + 0.02 * rng.standard_normal((T, 3))
    c = P.capm_betas(R, m)
    assert np.allclose(c["beta"], betas, atol=0.03)
    s = P.sml(c["beta"], R.mean(0))
    assert s["slope"] == pytest.approx(m.mean(), abs=0.002)
    mu = np.array([0.005, 0.003])
    Sg = np.array([[0.0016, 0.0002], [0.0002, 0.0009]])
    assert P.hj_excess(mu, Sg) >= max(abs(mu / np.sqrt(np.diag(Sg))))
    g = np.exp(0.02 + 0.02 * rng.standard_normal(5000))
    assert P.sdf_ratio(g, 10) > P.sdf_ratio(g, 2)
    f = P.euler_moments(g, np.c_[np.full(5000, 1.02)])
    assert f((1 / 1.02, 0.0)).mean() == pytest.approx(0.0, abs=1e-12)


def test_shiller_cs_limits_bubbles():
    from explainer.quant.house import premia as P
    d = np.ones(50)
    p = P.ex_post_rational(d, 0.05, terminal=20.0)
    assert p[0] == pytest.approx(20.0, rel=1e-9)  # a constant dividend priced at 1/r stays there
    rng = np.random.default_rng(1)
    dp = rng.standard_normal(200) * 0.3 - 3
    r = np.r_[0, -0.5 * np.diff(dp)] + 0.01 * rng.standard_normal(200)
    out = P.cs_decomposition(dp, r, np.zeros(200), horizon=10)
    assert 0 < out["rho"] < 1 and out["b_d"] == pytest.approx(0.0)
    sv0 = P.shleifer_vishny(a=0.0)
    sv2 = P.shleifer_vishny(a=1.5)
    assert sv2["p2"] < sv0["p2"]  # performance-based withdrawals deepen the mispricing
    assert P.gk_multiplier(0.2) == pytest.approx(5.0)
    T = 120
    R = np.full((T, 2), 0.0)
    R[:24, 0] = 0.05  # +222% in two years
    R[24:30, 0] = -0.15  # then a crash
    out = P.run_ups(R, np.zeros(T), months=24, threshold=1.0, crash=0.4, horizon=24)
    assert out["n"] == 1 and out["events"][0]["crash"]


# ---------------------------------------------------------------------------- Part 24: factors, the Track Record
def test_factor_stats_and_drawdown():
    from explainer.quant.house import factors as FA
    r = np.array([0.10, -0.50, 0.20, 0.10])
    dd = FA.drawdown(r)
    assert abs(dd["max"] - (0.55 / 1.10 - 1)) < 1e-12 and dd["peak"] == 0 and dd["trough"] == 1
    s = FA.stats(np.r_[np.full(60, 0.01), np.full(60, -0.005)])
    assert abs(s["mean"] - 0.0025 * 12) < 1e-12 and s["n"] == 120


def test_two_by_three_signs():
    from explainer.quant.house import factors as FA
    size = np.array([1, 1, 1, 10, 10, 10.0])
    bm = np.array([0.2, 1.0, 3.0, 0.2, 1.0, 3.0])
    ret = np.array([0.02, 0.03, 0.05, 0.01, 0.015, 0.03])
    t = FA.two_by_three(size, bm, np.ones(6, bool), ret, size)
    assert t["smb"] > 0 and t["hml"] > 0
    assert abs(t["hml"] - ((0.05 + 0.03) / 2 - (0.02 + 0.01) / 2)) < 1e-12


def test_vol_scaled_and_factor_momentum_are_point_in_time():
    from explainer.quant.house import factors as FA
    rng = np.random.default_rng(0)
    r = rng.normal(0.005, 0.05, 120)
    a = FA.vol_scaled(r, 0.12, 6)
    r2 = r.copy()
    r2[80:] *= 5
    b = FA.vol_scaled(r2, 0.12, 6)
    assert np.allclose(a[:80], b[:80], equal_nan=True)
    F = rng.normal(0, 0.03, (100, 3))
    m1 = FA.factor_momentum(F, 12)["r"]
    F2 = F.copy()
    F2[60:] = -F2[60:]
    m2 = FA.factor_momentum(F2, 12)["r"]
    assert np.allclose(m1[:60], m2[:60], equal_nan=True)


def test_ddm_bm_directions():
    from explainer.quant.house import factors as FA
    base = FA.ddm_bm(0.12, 0.05, 0.09)
    assert FA.ddm_bm(0.08, 0.05, 0.09) > base      # less profitable: higher B/M
    assert FA.ddm_bm(0.12, 0.07, 0.09) < base      # more investment: lower B/M
    assert FA.ddm_bm(0.12, 0.05, 0.11) > base      # higher discount rate: higher B/M


def test_track_record_rows(tmp_path, monkeypatch):
    from explainer.quant.house import track
    monkeypatch.setattr(track, "LEDGER", tmp_path / "t.json")
    rng = np.random.default_rng(1)
    row = track.record("toy", 24, rng.normal(0.01, 0.04, 240), rng.normal(0.0, 0.04, 60), 0.012)
    assert row["holdout"]["n"] == 60 and row["research"]["sharpe_net"] < row["research"]["sharpe"]
    with pytest.raises(RuntimeError):
        track.record("toy", 25, np.ones(3) * 0.01, np.ones(3) * 0.01)


# ---------------------------------------------------------------------------- Part 25: the factor zoo
def test_zoo_hurdles_and_shrinkage():
    from explainer.quant.house import zoo as Z
    assert Z.bonferroni_t(1) == pytest.approx(1.95996, abs=1e-4)
    assert Z.bonferroni_t(100) > Z.bonferroni_t(10) > 2.0
    m = Z.noise_max_t(200, 120, 500, seed=1)
    assert 2.4 < m["mean"] < 3.1
    rng = np.random.default_rng(0)
    theta = rng.normal(2.0, 1.0, 4000)
    t = theta + rng.standard_normal(4000)
    eb = Z.eb_shrink(t)
    assert eb["shrink"] == pytest.approx(0.5, abs=0.05)


def test_kns_and_rp_pca_and_lasso():
    from explainer.quant.house import zoo as Z
    rng = np.random.default_rng(2)
    F = rng.normal(0.005, 0.03, (300, 8))
    mu, S = F.mean(0), np.cov(F.T)
    b0 = Z.kns_b(mu, S, 0.0)
    assert np.allclose(S @ b0, mu)
    assert np.linalg.norm(Z.kns_b(mu, S, 1.0)) < np.linalg.norm(b0)
    cv = Z.kns_cv(F, [1e-6, 1e-4, 1e-2], folds=3)
    assert len(cv["r2"]) == 3
    p = Z.pca(F)
    assert p["share"].sum() == pytest.approx(1.0) and np.all(np.diff(p["eig"]) <= 1e-15)
    rp = Z.rp_pca(F, 10.0)
    assert rp["V"].shape == (8, 8)
    X = rng.normal(size=(300, 6))
    y = 3 * X[:, 0] + 0.1 * rng.standard_normal(300)
    b = Z.lasso(X, y, 0.1)
    assert abs(b[0] - 3) < 0.3 and np.all(np.abs(b[1:]) < 0.05)
    assert Z.max_sh2(F[:, :1]) <= Z.max_sh2(F) + 1e-12


def test_backtest_statistics():
    import math

    from explainer.quant.house import backtest as B
    # the extreme-value approximation against simulation
    for n in (10, 1000):
        sim = B.noise_max_sr(n, 1260, sims=300, seed=n)
        assert B.expected_max_sr(n, 1 / 1260) == pytest.approx(sim.mean(), rel=0.06)
    # Bailey, Borwein, Lopez de Prado and Zhu: five years allow about 45 trials at a Sharpe ratio of one
    assert B.min_btl(45, 1.0) == pytest.approx(5.0, abs=0.05)
    # Lo's eta: sqrt(q) without autocorrelation, smaller with positive autocorrelation
    assert B.lo_eta(np.zeros(11), 12) == pytest.approx(math.sqrt(12))
    assert B.lo_eta(np.full(11, 0.2), 12) < math.sqrt(12)
    # the iid standard error against the sampling spread of the estimate
    rng = np.random.default_rng(3)
    est = [B.sharpe(rng.normal(0.1, 1, 500)) for _ in range(3000)]
    assert np.std(est) == pytest.approx(math.sqrt((1 + 0.5 * 0.1 ** 2) / 500), rel=0.06)
    assert B.psr(0.1, 0.1, 500) == pytest.approx(0.5)
    d = B.deflated_sharpe(0.1, 500, 100, 0.002)
    assert d["sr0"] == pytest.approx(B.expected_max_sr(100, 0.002)) and d["dsr"] < B.psr(0.1, 0.0, 500)


def test_cscv_and_cross_validation():
    from explainer.quant.house import backtest as B
    pbos = [B.cscv(np.random.default_rng(s).standard_normal((1600, 50)), S=8)["pbo"] for s in range(12)]
    assert 0.35 < np.mean(pbos) < 0.65                      # noise: the in-sample winner is a coin flip out of sample
    rng = np.random.default_rng(4)
    noise = rng.standard_normal((1600, 50))
    assert B.cscv(noise, S=8)["n_combos"] == 70
    skill = noise.copy()
    skill[:, 0] += 0.4
    assert B.cscv(skill, S=8)["pbo"] < 0.05
    t0 = np.arange(100)
    t1 = t0 + 5
    for tr, te in B.purged_kfold(t0, t1, 5, embargo=3):
        a, b = t0[te].min(), t1[te].max()
        assert not np.any((t0[tr] <= b) & (t1[tr] >= a))
        assert not np.any((t0[tr] > b) & (t0[tr] <= b + 3))
    for tr, te in B.walk_forward(100, 40, 20):
        assert tr.max() < te.min()


def test_reality_checks():
    from explainer.quant.house import backtest as B
    rng = np.random.default_rng(5)
    T, K = 1000, 200
    d = rng.standard_normal((T, K)).astype(np.float32) * 0.01
    counts = B.stationary_bootstrap_counts(T, 300, 5.0, seed=1)
    assert np.allclose(counts.sum(1), T)
    mean, sd = d.mean(0).astype(float), d.std(0, ddof=1).astype(float)
    bm = B.boot_means(d, counts)
    assert B.reality_check(mean, bm, T)["p"] > 0.05
    d[:, 7] += 0.003
    mean = d.mean(0).astype(float)
    bm = B.boot_means(d, counts)
    assert B.reality_check(mean, bm, T)["p"] < 0.05
    assert B.spa(mean, bm, sd, T)["p"] < 0.05
    assert 7 in B.romano_wolf(mean, bm, sd, T)["rejected"]


def test_rules_and_engine():
    from explainer.quant.house import backtest as B
    rng = np.random.default_rng(6)
    P = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, 600)))
    # point in time: a rule's position at t does not change when later prices change
    for r in B.random_rules(40, seed=1):
        a = B.rule_positions(P, r)
        Q = P.copy()
        Q[400:] *= 1.5
        assert np.array_equal(a[:400], B.rule_positions(Q, r)[:400])
    # a fixed holding period closes the position
    pos = B.rule_positions(P, {"family": "ma", "fast": 1, "slow": 20, "band": 0.0, "delay": 0, "hold": 5})
    runs = np.diff(np.flatnonzero(np.diff(np.r_[0, (pos != 0).astype(int), 0])))[::2]
    assert np.all(runs <= 5)
    # the engine, at the close it computed from and without costs, reproduces the vectorised backtest
    n = len(P)
    bars = {"date": np.arange(n), "open": P, "high": P, "low": P, "close": P, "volume": np.full(n, 1e7)}
    sig = lambda v: 1.0 if v["close"][-1] > v["close"][-2] else -1.0  # noqa: E731
    res = B.Backtester(bars, sig, latency=0, fill="close").run()
    w = np.r_[0.0, np.where(np.diff(P) > 0, 1.0, -1.0)]
    w[0] = 0.0
    vec = B.vectorized(w, P, 0.0, 1)
    assert np.allclose(res.returns[2:], vec[2:], atol=1e-9)
    # a split ignored halves the equity of a holder of a 2:1 split stock priced as traded
    raw = dict(bars, close=np.r_[np.full(300, 100.0), np.full(300, 50.0)], open=np.r_[np.full(300, 100.0),
                                                                                    np.full(300, 50.0)])
    raw["split"] = np.ones(n)
    raw["split"][300] = 2.0
    hold = lambda v: 1.0  # noqa: E731
    ok = B.Backtester(raw, hold).run().equity
    bad = B.Backtester(raw, hold, adjust_splits=False).run().equity
    assert ok[-1] == pytest.approx(ok[10], rel=1e-9) and bad[-1] == pytest.approx(0.5 * bad[10], rel=1e-9)


def test_ml_linear_and_kernel():
    from explainer.quant.house import ml
    rng = np.random.default_rng(7)
    X = rng.standard_normal((40, 3))
    # random features approximate the Gaussian kernel exp(-gamma^2 |x - y|^2 / 2)
    Z = ml.rff(X, 20000, gamma=0.7, seed=1)
    K = np.exp(-0.5 * 0.49 * ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    assert np.abs(Z @ Z.T - K).max() < 0.05
    # the dual ridge equals the primal one
    Z = ml.rff(X, 30, seed=2)
    y = rng.standard_normal(40)
    b = ml.ridge_dual(Z, y, 0.1)
    assert np.allclose(b, np.linalg.solve(Z.T @ Z + 0.1 * 40 * np.eye(30), Z.T @ y), atol=1e-8)
    # PCR and PLS with every component are OLS
    X2 = rng.standard_normal((200, 4))
    y2 = X2 @ np.array([1.0, -0.5, 0.2, 0.0]) + 0.1 * rng.standard_normal(200)
    f_ols, f_pcr, f_pls = ml.ols(X2, y2), ml.pcr(X2, y2, 4), ml.pls(X2, y2, 4)
    assert np.allclose(f_ols(X2), f_pcr(X2), atol=1e-8) and np.allclose(f_ols(X2), f_pls(X2), atol=1e-6)
    assert ml.r2_oos(y2, f_ols(X2)) > 0.9


def test_ml_trees_conformal_toolkit():
    from explainer.quant.house import ml
    rng = np.random.default_rng(8)
    X = rng.uniform(-1, 1, (2000, 2))
    y = np.where(X[:, 0] > 0, 1.0, -1.0) + 0.1 * rng.standard_normal(2000)
    g = ml.GBMRegressor(n_trees=60, depth=2, lr=0.2, seed=0).fit(X, y)
    assert np.mean((g.predict(X) - np.sign(X[:, 0])) ** 2) < 0.02
    q = ml.split_conformal(rng.standard_normal(999), alpha=0.1)
    test = rng.standard_normal(20000)
    assert abs(np.mean(np.abs(test) <= q) - 0.9) < 0.02
    x = np.cumsum(rng.standard_normal(300))
    assert np.allclose(ml.fracdiff(x, 1.0)[1:], np.diff(x))
    c = np.r_[np.full(5, 100.0), 103.0, np.full(5, 103.0)]
    tb = ml.triple_barrier(c, np.full(len(c), 0.01), horizon=10, up=2, down=2)
    assert tb["label"][0] == 1 and tb["end"][0] == 5
    bars = ml.dollar_bars(np.arange(10), np.ones(10), np.full(10, 5.0), 10.0)
    assert len(bars["t"]) == 5
    w = ml.uniqueness_weights([0, 0], [1, 1], 3)
    assert np.allclose(w, 0.5)


def test_ridge_theory_matches_simulation():
    import numpy as np
    from explainer.quant.house import ml as ML
    x = np.linspace(0, 12, 120001)
    assert abs(np.trapezoid(ML.mp_density(x, 0.5), x) - 1) < 1e-3
    assert abs(np.trapezoid(ML.mp_density(x, 2.0), x) - 0.5) < 1e-3
    for g, lam in ((0.5, 0.0), (1.5, 0.0), (3.0, 3.0), (0.9, 0.9)):
        th = ML.ridge_risk_theory(g, lam)["risk"]
        sm = np.median(ML.ridge_risk_sim(200, int(g * 200), lam, seeds=10))
        assert abs(sm / th - 1) < 0.12
    assert ML.ridge_risk_theory(2.0, 0.0)["risk"] == 1.0 * 0.5 + 1.0
    e = ML.rff_kernel_error(P_list=(100, 10000))
    assert e[1] < e[0] / 5
