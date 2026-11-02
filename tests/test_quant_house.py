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
