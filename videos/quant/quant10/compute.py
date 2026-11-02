"""Every number in Part 10 (Black–Scholes–Merton), computed and cached in .cache/quant10/.

    python -m videos.quant.quant10.compute [items] [--force]

Items (each seeded; minutes on a laptop):

* ``tree``      CRR prices of a 1-year at-the-money call for N = 1..400 steps against the formula; a 4-step tree to
                draw; the American put on an 2000-step tree, its early-exercise boundary and premium.
* ``ledger``    three seeded paths hedged at 20% that realize 12%, 20% and 28%, step by step (the hedging ledger),
                and 20,000 paths at each realized volatility for the P&L distributions.
* ``wrong_vol`` hedging at the wrong volatility: two paths with the same realized volatility and different P&L,
                and 4,000 Heston paths, their P&L against realized vol and against the gamma-weighted prediction.
* ``discrete``  hedging error against rebalancing frequency (4 to 1,024 hedges) on 20,000 paths, against the
                derived sqrt(dt) law; Leland's volatility with transaction costs.
* ``implied``   the implied-volatility solver at work on a real quote; the Surface's first look and its first row
                (Black–Scholes, one volatility per expiry), in and out of sample.
* ``btc``       real hedging: a 30-day at-the-money BTC call sold every day at DVOL from April 2021 and delta-hedged
                every hour on Binance's prices until expiry, with the gamma/theta decomposition of each.
* ``crash87``   19 October 1987 in Kenneth French's daily market returns: the move in standard deviations, what a
                Gaussian and a cubic tail say about how often it should happen.

The expansion's items (seconds to a few minutes each, one core): ``heat`` (the PDE solved by the heat kernel),
``tree3d`` (whole lattices against the surface), ``mc_seeds`` (Monte Carlo under Q, 8 seeds, and the Girsanov
baseline), ``hedge_choice`` and ``dgamma3d`` (hedge at implied or actual; dollar gamma), ``discrete_seeds`` and
``jump_floor`` (the sqrt(dt) law with seeds; the floor jumps leave), ``leland_grid`` and ``kabanov`` (costs against
risk; Leland's strategy as hedging speeds up), ``solver_race`` (every Surface quote inverted), ``carry`` (the
forward per expiry; the skew a forgotten forward draws), ``american_more`` (the premium surface, Kim's integral, BAW,
the dividend call), ``btc_replay`` (the BTC study month by month with bootstrap bands), ``insurance87`` (portfolio
insurance on the 1987 data), ``ltcm98`` (VIX through 1998), ``industry`` (the floor's 0.4 rule on the Surface),
``neural_iv`` (a learned first guess for implied volatility, 5 seeds).
"""

from __future__ import annotations

import numpy as np
from scipy import integrate, stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, hedge, paths, sim, surface, trees

CACHE = Cache("quant10")
load = CACHE.load


def _json(x):
    """Nested containers made JSON-safe (the cache keeps top-level arrays in .npz, everything else in .json)."""
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x
YEAR_H = 365 * 24  # crypto trades every hour of the year
COST_BTC = 0.0002  # 2 bp per unit traded: a market maker's all-in cost on BTC spot (a retail taker pays ~10 bp)


# ---------------------------------------------------------------------------
def compute_tree() -> dict:
    S, K, T, sig, r = 100.0, 100.0, 1.0, 0.2, 0.05
    exact = float(bs.price(S, K, T, sig, r))
    Ns = np.arange(1, 401)
    px = np.array([trees.crr(S, K, T, sig, r, N=int(n))["price"] for n in Ns])
    small = trees.crr(S, K, T, sig, r, N=4, keep=5)
    layers = {str(n): {k: (v.tolist() if v is not None else None) for k, v in L.items()}
              for n, L in small["layers"].items()}
    # the American put: price, boundary, and the early-exercise premium across spot
    am = trees.crr(S, K, T, sig, r, N=2000, cp=-1, american=True, boundary=True)
    eu_put = float(bs.price(S, K, T, sig, r, 0.0, -1))
    spots = np.linspace(60, 140, 41)
    am_curve = np.array([trees.crr(s, K, T, sig, r, N=600, cp=-1, american=True)["price"] for s in spots])
    eu_curve = bs.price(spots, K, T, sig, r, 0.0, -1)
    return {"S": S, "K": K, "T": T, "sigma": sig, "r": r, "exact": exact, "N": Ns, "price": px,
            "err": px - exact, "small": _json({"price": small["price"], "p": small["p"], "u": small["u"], "layers": layers}),
            "american_put": am["price"], "european_put": eu_put, "boundary_t": am["times"],
            "boundary": am["boundary"], "spots": spots, "am_curve": am_curve, "eu_curve": eu_curve,
            "big_N_price": float(px[-1]), "big_N_err": float(px[-1] - exact)}


# ---------------------------------------------------------------------------
LEDGER = {"K": 100.0, "T": 0.25, "sigma_i": 0.20, "n_steps": 252, "real": (0.12, 0.20, 0.28)}


def compute_ledger() -> dict:
    c = LEDGER
    out = {"K": c["K"], "T": c["T"], "sigma_i": c["sigma_i"], "real": list(c["real"])}
    rows = []
    for j, sr in enumerate(c["real"]):
        # the drawn path: the first of a seeded batch whose realized vol is within 0.5 point of the target
        t, S = paths.gbm(100.0, 0.0, sr, c["T"], c["n_steps"], 400, seed=100 + j)
        rv = paths.realized_vol(S, c["T"] / c["n_steps"])
        i = int(np.argmin(np.abs(rv - sr)))
        rec = hedge.delta_hedge(t, S[i:i + 1], c["K"], c["T"], c["sigma_i"], position=-1, record=[0])
        # the distribution over many paths
        t2, S2 = paths.gbm(100.0, 0.0, sr, c["T"], c["n_steps"], 20000, seed=200 + j)
        many = hedge.delta_hedge(t2, S2, c["K"], c["T"], c["sigma_i"], position=-1)
        rows.append({"sigma_r": sr, "realized": float(rv[i]), "pnl": float(rec["pnl"][0])})
        for k in ("value", "delta", "book", "gamma", "theta"):
            out[f"{k}_{j}"] = rec[k][0]
        out[f"S_{j}"] = S[i]
        out[f"pnl_many_{j}"] = many["pnl"]
        rows[-1].update({"mean": float(many["pnl"].mean()), "sd": float(many["pnl"].std()),
                         "p_loss": float((many["pnl"] < 0).mean())})
    out["t"] = t
    out["rows"] = _json(rows)
    out["premium"] = float(bs.price(100.0, c["K"], c["T"], c["sigma_i"]))
    return out


# ---------------------------------------------------------------------------
def compute_wrong_vol() -> dict:
    K, T, n = 100.0, 0.25, 252
    sig_i = 0.25  # sold and hedged at 25%; the world realizes 20%
    t, S = paths.gbm(100.0, 0.0, 0.20, T, n, 20000, seed=31)
    dt = T / n
    rv = paths.realized_vol(S, dt)
    res = hedge.delta_hedge(t, S, K, T, sig_i, position=-1)
    # dollar gamma at the hedge vol, integrated along each path: 1/2 int Gamma S^2 dt
    tau = T - t[:-1]
    G = bs.greeks(S[:, :-1], K, tau, sig_i)["gamma"]
    dollar_gamma = 0.5 * np.sum(G * S[:, :-1] ** 2, axis=1) * dt
    band = np.where(np.abs(rv - 0.20) < 0.0015)[0]
    near = band[np.argmax(dollar_gamma[band])]  # same realized vol, spent its time near the strike
    far = band[np.argmin(dollar_gamma[band])]  # same realized vol, wandered away from it
    # Heston: volatility that moves; P&L against realized vol, and against the gamma-weighted prediction
    th, Sh, vh = paths.heston(100.0, 0.04, 3.0, 0.04, 0.8, -0.7, T, n, 4000, seed=32)
    hr = hedge.delta_hedge(th, Sh, K, T, sig_i, position=-1)
    Gh = bs.greeks(Sh[:, :-1], K, T - th[:-1], sig_i)["gamma"]
    pred = np.sum(0.5 * Gh * Sh[:, :-1] ** 2 * (sig_i ** 2 - vh[:, :-1]), axis=1) * dt
    rvh = paths.realized_vol(Sh, dt)
    corr_rv = float(np.corrcoef(rvh, hr["pnl"])[0, 1])
    corr_pred = float(np.corrcoef(pred, hr["pnl"])[0, 1])
    return {"K": K, "T": T, "sigma_i": sig_i, "t": t, "S_near": S[near], "S_far": S[far],
            "rv_near": float(rv[near]), "rv_far": float(rv[far]), "pnl_near": float(res["pnl"][near]),
            "pnl_far": float(res["pnl"][far]), "dg_near": float(dollar_gamma[near]), "dg_far": float(dollar_gamma[far]),
            "heston_rv": rvh, "heston_pnl": hr["pnl"], "heston_pred": pred, "corr_rv": corr_rv,
            "corr_pred": corr_pred, "heston": {"v0": 0.04, "kappa": 3.0, "theta": 0.04, "xi": 0.8, "rho": -0.7},
            "n_band": int(len(band))}


# ---------------------------------------------------------------------------
def _expected_gamma2_s4(S0, K, T, sig, n=400):
    """I = int_0^T E[Gamma_t^2 S_t^4] dt for GBM with zero drift, by quadrature over the lognormal."""
    z, wz = np.polynomial.hermite_e.hermegauss(160)
    wz = wz / wz.sum()
    ts = np.linspace(0, T, n + 1)[:-1] + T / n / 2
    vals = []
    for t in ts:
        St = S0 * np.exp(-0.5 * sig ** 2 * t + sig * np.sqrt(t) * z)
        g = bs.greeks(St, K, T - t, sig)["gamma"]
        vals.append(np.sum(wz * g ** 2 * St ** 4))
    return float(np.sum(vals) * T / n)


def compute_discrete() -> dict:
    K, T, sig = 100.0, 0.25, 0.2
    Ns = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024])
    sd, mean = [], []
    for N in Ns:
        t, S = paths.gbm(100.0, 0.0, sig, T, int(N), 20000, seed=41)
        p = hedge.delta_hedge(t, S, K, T, sig, position=-1)["pnl"]
        sd.append(p.std())
        mean.append(p.mean())
    I = _expected_gamma2_s4(100.0, K, T, sig)
    theory = sig ** 2 * np.sqrt(T / Ns / 2 * I)
    vega = float(bs.greeks(100.0, K, T, sig)["vega"])
    kamal = np.sqrt(np.pi / 4) * vega * sig / np.sqrt(Ns)
    slope = float(np.polyfit(np.log(Ns), np.log(sd), 1)[0])
    # transaction costs: a proportional cost k per share traded (one way), hedged weekly
    k, Nh = 0.0025, 13
    dt = T / Nh
    sig_L = sig * np.sqrt(1 + np.sqrt(2 / np.pi) * (2 * k) / (sig * np.sqrt(dt)))
    t, S = paths.gbm(100.0, 0.0, sig, T, Nh, 40000, seed=42)
    naive = hedge.delta_hedge(t, S, K, T, sig, position=-1, cost=k)
    leland = hedge.delta_hedge(t, S, K, T, sig_L, position=-1, sigma_price=sig_L, cost=k)
    free = hedge.delta_hedge(t, S, K, T, sig, position=-1, cost=0.0)
    # Leland's formula prices the rebalancing; the first hedge and the unwind at expiry are extra
    leland_mid = hedge.delta_hedge(t, S, K, T, sig_L, position=-1, sigma_price=sig_L, cost=k, cost_ends=False)
    return {"K": K, "T": T, "sigma": sig, "N": Ns, "sd": np.array(sd), "mean": np.array(mean), "theory": theory,
            "kamal": kamal, "slope": slope, "I": I, "vega": vega,
            "cost": k, "cost_N": Nh, "sigma_leland": float(sig_L),
            "naive_mean": float(naive["pnl"].mean()), "naive_sd": float(naive["pnl"].std()),
            "leland_mean": float(leland["pnl"].mean()), "leland_sd": float(leland["pnl"].std()),
            "free_mean": float(free["pnl"].mean()), "free_sd": float(free["pnl"].std()),
            "naive_costs": float(naive["cost_total"].mean()), "leland_mid_mean": float(leland_mid["pnl"].mean()),
            "leland_mid_sd": float(leland_mid["pnl"].std()),
            "end_costs": float(naive["cost_total"].mean() - hedge.delta_hedge(t, S, K, T, sig, position=-1, cost=k,
                                                                              cost_ends=False)["cost_total"].mean()), "premium_bs": float(bs.price(100, K, T, sig)),
            "premium_leland": float(bs.price(100, K, T, sig_L)), "pnl_naive": naive["pnl"], "pnl_leland": leland["pnl"]}


# ---------------------------------------------------------------------------
def compute_implied() -> dict:
    q0 = surface.build(surface.DAYS[0])
    q1 = surface.build(surface.DAYS[1])
    # the solver at work on one real quote: the most-traded call near the money, about a month out
    T, K, F, iv, cp, n = q0["T"], q0["K"], q0["F"], q0["iv"], q0["cp"], q0["n"]
    cand = np.where((cp == 1) & (T > 20 / 365) & (T < 90 / 365) & (np.abs(q0["k"]) < 0.06))[0]
    j = int(cand[np.argmax(n[cand])])
    price_usd = float(bs.price(F[j], K[j], T[j], iv[j]))
    sol, its = bs.implied_vol(price_usd, F[j], K[j], T[j], return_iterations=True)
    its = np.array([float(x) for x in its])
    its_price = bs.price(F[j], K[j], T[j], its)
    # the Surface's first row: Black–Scholes with one volatility per expiry (the vega-weighted mean)
    def flat_fit(q):
        fit = {}
        for e in sorted(set(q["expiry"])):
            m = np.array(q["expiry"]) == e
            fit[e] = float(np.sum(q["vega"][m] * q["iv"][m]) / np.sum(q["vega"][m]))
        return fit

    fit0 = flat_fit(q0)
    model0 = np.array([fit0[e] for e in q0["expiry"]])
    rmse_in = surface.vega_rmse(model0, q0)
    common = np.array([e in fit0 for e in q1["expiry"]])
    model1 = np.array([fit0.get(e, np.nan) for e in q1["expiry"]])
    rmse_out = surface.vega_rmse(model1[common], q1, mask=common)
    # calendar arbitrage in the fitted flat smiles: total variance must not fall as maturity rises
    exps = sorted(fit0, key=lambda e: q0["T"][q0["expiry"].index(e)])
    w = [fit0[e] ** 2 * q0["T"][q0["expiry"].index(e)] for e in exps]
    cal_viol = int(sum(1 for a, b in zip(w, w[1:]) if b < a - 1e-12))
    # DVOL at the snapshot against the 30-day at-the-money vol interpolated from the Surface
    dv = data.deribit_dvol("2025-12", "2025-12")
    ref = surface._ref_ts(surface.DAYS[0])
    dvol_ref = float(dv["close"][np.argmin(np.abs(dv["time"] - ref))]) / 100
    atm = []
    for e in exps:
        m = np.array(q0["expiry"]) == e
        kk, vv = q0["k"][m], q0["iv"][m]
        o = np.argsort(kk)
        atm.append((q0["T"][q0["expiry"].index(e)], float(np.interp(0.0, kk[o], vv[o]))))
    at, av = np.array(atm).T
    atm30 = float(np.sqrt(np.interp(30 / 365, at, av ** 2 * at) / (30 / 365)))
    return {"q0": _json({k: v for k, v in q0.items() if k != "expiries"}), "expiries0": _json(q0["expiries"]),
            "q1_n": int(len(q1["K"])), "S0": q0["S"], "S1": q1["S"], "j": j, "solver_K": float(K[j]),
            "solver_T": float(T[j]), "solver_F": float(F[j]), "solver_price": price_usd, "solver_iv": float(sol),
            "solver_iters": its, "solver_iter_prices": its_price, "flat_fit": fit0, "rmse_in": rmse_in,
            "rmse_out": rmse_out, "n_out": int(common.sum()), "calendar_violations": cal_viol,
            "dvol_ref": dvol_ref, "atm30": atm30, "atm_T": at, "atm_iv": av,
            "surface_row": {"model": "Black--Scholes, one vol per expiry", "part": 10, "rmse_in": rmse_in,
                            "rmse_out": rmse_out, "arbitrage": cal_viol, "params": len(fit0)}}


# ---------------------------------------------------------------------------
def compute_btc() -> dict:
    dv = data.deribit_dvol(*surface.DVOL_RANGE)
    kl = data.binance_klines("BTCUSDT", "1h", *surface.SPOT_RANGE)
    # the candle's close is the price at the end of its hour; align it to DVOL's hourly stamps
    spot_t = kl["time"] + 3600
    hours = np.arange(max(dv["time"][0], spot_t[0]), min(dv["time"][-1], spot_t[-1]) + 1, 3600.0)
    S = np.interp(hours, spot_t, kl["close"])  # a handful of missing hours are interpolated
    iv = np.interp(hours, dv["time"], dv["close"]) / 100
    gaps = int(len(hours) - np.isin(hours, spot_t).sum())
    H = 30 * 24
    starts = np.where((hours % 86400) == 8 * 3600)[0]
    starts = starts[starts + H < len(hours)]
    pnl, prem, rv, ivs, gam, the, res, t0s, pnl_c = [], [], [], [], [], [], [], [], []
    for s in starts:
        path = S[s:s + H + 1]
        path = path / path[0] * 100.0  # per 100 of BTC: the strike is at the money
        tt = np.arange(H + 1) / YEAR_H
        T = H / YEAR_H
        sig = iv[s]
        o = hedge.delta_hedge(tt, path[None, :], 100.0, T, sig, position=-1)
        pnl_c.append(hedge.delta_hedge(tt, path[None, :], 100.0, T, sig, position=-1, cost=COST_BTC)["pnl"][0])
        pnl.append(o["pnl"][0])
        prem.append(o["premium"][0])
        rv.append(paths.realized_vol(path, 1 / YEAR_H))
        ivs.append(sig)
        gam.append(o["gamma_total"][0])
        the.append(o["theta_total"][0])
        res.append(o["residual_total"][0])
        t0s.append(hours[s])
    pnl, prem, rv, ivs, pnl_c = map(np.array, (pnl, prem, rv, ivs, pnl_c))
    vega = bs.greeks(100.0, 100.0, H / YEAR_H, ivs)["vega"]  # per 1.00 of vol, per 100 of BTC
    # one month to replay in the hook and chapter 6: the start whose P&L is closest to the median
    pick = int(np.argmin(np.abs(pnl - np.median(pnl))))
    s = starts[pick]
    path = S[s:s + H + 1] / S[s] * 100
    tt = np.arange(H + 1) / YEAR_H
    rec = hedge.delta_hedge(tt, path[None, :], 100.0, H / YEAR_H, ivs[pick], position=-1, record=[0])
    # the worst month, for the crisis of the strategy
    worst = int(np.argmin(pnl))
    # non-overlapping months (every 30th start) for honest statistics
    sub = np.arange(0, len(pnl), 30)
    se = pnl[sub].std(ddof=1) / np.sqrt(len(sub))
    return {"start": np.array(t0s), "pnl": pnl, "pnl_cost": pnl_c, "cost": COST_BTC, "vega": vega,
            "mean_cost": float(pnl_c.mean()), "mean_vega": float(vega.mean()), "premium": prem, "rv": rv, "iv": ivs, "gamma": np.array(gam),
            "theta": np.array(the), "residual": np.array(res), "n": int(len(pnl)), "gaps": gaps,
            "mean": float(pnl.mean()), "median": float(np.median(pnl)), "p_win": float((pnl > 0).mean()),
            "mean_rv": float(rv.mean()), "mean_iv": float(ivs.mean()), "vrp": float((ivs - rv).mean()),
            "worst": float(pnl[worst]), "worst_start": float(t0s[worst]), "worst_rv": float(rv[worst]),
            "worst_iv": float(ivs[worst]), "best": float(pnl.max()),
            "nonoverlap_n": int(len(sub)), "nonoverlap_mean": float(pnl[sub].mean()), "nonoverlap_se": float(se),
            "pick": pick, "pick_start": float(t0s[pick]), "pick_S": path, "pick_S0": float(S[s]),
            "pick_premium": float(prem[pick]), "pick_t": tt, "pick_iv": float(ivs[pick]),
            "pick_rv": float(rv[pick]), "pick_pnl": float(pnl[pick]),
            **{f"pick_{k}": rec[k][0] for k in ("value", "delta", "book", "gamma", "theta")},
            "dvol_t": hours[::24], "dvol": iv[::24], "rv30_t": hours[H::24],
            "rv30": np.array([paths.realized_vol(S[i - H:i + 1], 1 / YEAR_H) for i in range(H, len(S), 24)])}


# ---------------------------------------------------------------------------
def compute_crash87() -> dict:
    kf = data.ken_french_daily()
    d, r = kf["date"], kf["mkt"]
    i = int(np.where(d == 19871019)[0][0])
    lr = np.log1p(r)
    trail = float(np.std(lr[i - 252:i], ddof=1))  # the year before
    z = float(lr[i] / trail)
    p_gauss = float(stats.norm.cdf(z))
    years_gauss = float(1 / (p_gauss * 252))
    # a power-law tail fitted to the daily losses of 1926-1986 (Hill estimator on the worst 2%)
    pre = -lr[:i]
    pre = pre[pre > 0]
    losses = np.sort(-lr[:i])[::-1]
    kk = int(0.02 * i)
    u = losses[kk]
    alpha = float(kk / np.sum(np.log(losses[:kk] / u)))
    p_tail = float((kk / i) * (-lr[i] / u) ** (-alpha))  # P(loss > this) per day
    years_tail = float(1 / (p_tail * 252))
    # the same loss in units of the whole-sample standard deviation (1926-1986)
    sd_all = float(np.std(lr[:i], ddof=1))
    worst_before = float(np.min(lr[:i]))
    worst_before_date = int(d[np.argmin(lr[:i])])
    return {"date": 19871019, "ret": float(r[i]), "logret": float(lr[i]), "trailing_sd": trail, "z": z,
            "p_gauss": p_gauss, "years_gauss": years_gauss, "alpha": alpha, "u": float(u), "k": kk,
            "p_tail": p_tail, "years_tail": years_tail, "sd_all": sd_all, "z_all": float(lr[i] / sd_all),
            "worst_before": worst_before, "worst_before_date": worst_before_date,
            "window_dates": d[i - 30:i + 10], "window_ret": r[i - 30:i + 10], "n_days": int(i)}


def compute_riskneutral() -> dict:
    """The same paths under P (drift mu) and Q (drift r), and Monte Carlo prices under each."""
    S0, K, T, sig, r, mu = 100.0, 100.0, 1.0, 0.25, 0.05, 0.15
    n_draw, n_mc = 80, 400_000
    tP, SP = paths.gbm(S0, mu, sig, T, 120, n_draw, seed=51)
    rng = np.random.default_rng(52)
    Z = rng.standard_normal(n_mc)
    STP = S0 * np.exp((mu - 0.5 * sig ** 2) * T + sig * np.sqrt(T) * Z)
    STQ = S0 * np.exp((r - 0.5 * sig ** 2) * T + sig * np.sqrt(T) * Z)
    disc = np.exp(-r * T)
    payQ = disc * np.maximum(STQ - K, 0)
    payP = disc * np.maximum(STP - K, 0)
    # Girsanov: P's samples reweighted by dQ/dP give Q's expectation
    theta = (mu - r) / sig
    w = np.exp(-theta * np.sqrt(T) * Z - 0.5 * theta ** 2 * T)
    payW = payP * w
    d1, d2 = bs.d1_d2(S0, K, T, sig, r)
    return {"S0": S0, "K": K, "T": T, "sigma": sig, "r": r, "mu": mu, "t": tP, "paths_P": SP,
            "ST_P": STP[:60000], "ST_Q": STQ[:60000], "theta": theta,
            "mc_Q": float(payQ.mean()), "se_Q": float(payQ.std() / np.sqrt(n_mc)),
            "mc_P": float(payP.mean()), "se_P": float(payP.std() / np.sqrt(n_mc)),
            "mc_W": float(payW.mean()), "se_W": float(payW.std() / np.sqrt(n_mc)),
            "exact": float(bs.price(S0, K, T, sig, r)), "N_d1": float(stats.norm.cdf(d1)),
            "N_d2": float(stats.norm.cdf(d2)), "q_itm": float((STQ > K).mean()), "p_itm": float((STP > K).mean()),
            "n_mc": n_mc}


# ===========================================================================
# The expansion (November 2026): the PDE solved, the lattice in 3D, seeds, jumps, Leland, the solver race, the
# carry, the American premium, BTC replayed, 1987 replayed, 1998, the floor's arithmetic, a learned first guess.
# ===========================================================================
def compute_heat() -> dict:
    """Chapter 3: the call's value over (log-spot, time left) as the heat equation's solution; the kernel at three
    times; the convolution (bs.heat_price) against the formula at nine points."""
    K, sig, r = 100.0, 0.25, 0.05
    x = np.linspace(np.log(50.0), np.log(200.0), 60)
    tau = np.linspace(0.0, 1.0, 40)
    V = np.array([[float(bs.price(np.exp(a), K, max(t, 1e-9), sig, r)) for a in x] for t in tau])
    kern = {}
    for t in (0.1, 0.4, 1.0):
        sd = sig * np.sqrt(t)
        y0 = np.log(110.0) + (r - 0.5 * sig ** 2) * t
        z = np.linspace(y0 - 4 * sd, y0 + 4 * sd, 81)
        kern[str(t)] = {"z": z.tolist(), "phi": (np.exp(-0.5 * ((z - y0) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))).tolist(),
                        "y0": float(y0)}
    pts = [(S, t) for S in (80.0, 100.0, 125.0) for t in (0.1, 0.5, 1.0)]
    call = lambda s: np.maximum(s - K, 0.0)  # noqa: E731
    conv = np.array([bs.heat_price(call, S, t, sig, r, kinks=(K,)) for S, t in pts])
    form = np.array([float(bs.price(S, K, t, sig, r)) for S, t in pts])
    lab = {"heat": bs.heat_price(lambda s: np.maximum(s - 100.0, 0.0), 100.0, 1.0, 0.2, 0.05, kinks=(100.0,)),
           "formula": float(bs.price(100.0, 100.0, 1.0, 0.2, 0.05))}
    return {"K": K, "sigma": sig, "r": r, "x": x, "tau": tau, "V": V, "kernel": kern, "pts": _json(pts),
            "conv": conv, "formula": form, "max_err": float(np.max(np.abs(conv - form))), "lab": lab}


def compute_tree3d() -> dict:
    """Chapter 5: whole CRR lattices (N = 4, 16, 64, 256) for the 1-year at-the-money call, every node's (t, S, V),
    and how far the nodes sit from the Black–Scholes surface; the lab's three runs."""
    S, K, T, sig, r = 100.0, 100.0, 1.0, 0.2, 0.05
    out = {"S": S, "K": K, "T": T, "sigma": sig, "r": r}
    gaps = []
    for N in (4, 16, 64, 256):
        o = trees.crr(S, K, T, sig, r, N=N, keep=N + 1)
        tt, ss, vv = [], [], []
        layers = dict(o["layers"])
        last = S * o["u"] ** (2 * np.arange(N + 1) - N)
        layers[N] = {"spots": last, "values": np.maximum(last - K, 0.0)}
        for n, L in layers.items():
            m = (L["spots"] > 40) & (L["spots"] < 220)
            tt += [n * T / N] * int(m.sum())
            ss += L["spots"][m].tolist()
            vv += L["values"][m].tolist()
        tt, ss, vv = map(np.array, (tt, ss, vv))
        exact = bs.price(ss, K, np.maximum(T - tt, 1e-12), sig, r)
        live = (tt < T - 1e-9) & (np.abs(np.log(ss / K)) < 0.4)
        gaps.append(float(np.max(np.abs(vv - exact)[live])))
        out[f"t_{N}"], out[f"s_{N}"], out[f"v_{N}"] = tt, ss, vv
        out[f"price_{N}"] = o["price"]
    out["N"] = [4, 16, 64, 256]
    out["max_gap"] = gaps
    out["lab"] = {str(n): trees.crr(S, K, T, sig, r, N=n)["price"] for n in (4, 64, 400)}
    out["exact"] = float(bs.price(S, K, T, sig, r))
    return out


def compute_mc_seeds() -> dict:
    """Chapter 4: the Monte Carlo price under Q as the sample grows, 8 seeds; the Girsanov-weighted estimator from
    P-paths as the baseline (same budget)."""
    S0, K, T, sig, r, mu = 100.0, 100.0, 1.0, 0.25, 0.05, 0.15
    n_max = 400_000
    ns = np.unique(np.round(np.logspace(2, np.log10(n_max), 40)).astype(int))
    th = (mu - r) / sig
    q_runs, w_runs = [], []
    for seed in range(8):
        Z = np.random.default_rng(1000 + seed).standard_normal(n_max)
        payQ = np.exp(-r * T) * np.maximum(S0 * np.exp((r - 0.5 * sig ** 2) * T + sig * np.sqrt(T) * Z) - K, 0)
        payP = np.exp(-r * T) * np.maximum(S0 * np.exp((mu - 0.5 * sig ** 2) * T + sig * np.sqrt(T) * Z) - K, 0)
        wts = np.exp(-th * np.sqrt(T) * Z - 0.5 * th ** 2 * T)
        q_runs.append(np.cumsum(payQ)[ns - 1] / ns)
        w_runs.append(np.cumsum(payP * wts)[ns - 1] / ns)
        if seed == 0:
            sdQ, sdW = float(payQ.std()), float((payP * wts).std())
    q_runs, w_runs = np.array(q_runs), np.array(w_runs)
    exact = float(bs.price(S0, K, T, sig, r))
    within = np.all(np.abs(q_runs - exact) < 0.1, axis=0)
    stays = np.flip(np.cumprod(np.flip(within))).astype(bool)  # within from here to the end
    first = int(ns[int(np.argmax(stays))]) if stays.any() else None
    return {"n": ns, "q": q_runs, "w": w_runs, "exact": exact, "sd_q": sdQ, "sd_w": sdW, "ratio": sdW / sdQ,
            "theta": th, "theory_ratio": float(np.sqrt(np.exp(th ** 2 * T))), "n_within_10c": first,
            "spread_q_end": float(q_runs[:, -1].max() - q_runs[:, -1].min()),
            "spread_w_end": float(w_runs[:, -1].max() - w_runs[:, -1].min())}


def compute_hedge_choice() -> dict:
    """Chapter 8: a call bought at 20% when the world realizes 30% (and 25%), hedged at implied or at actual
    volatility (Ahmad and Wilmott 2005): the final P&L of 20,000 paths, and three paths marked to market."""
    K, T, n, s_i, mu = 100.0, 0.25, 252, 0.20, 0.10
    out = {"K": K, "T": T, "sigma_i": s_i, "mu": mu}
    for tag_, s_r in (("30", 0.30), ("25", 0.25)):
        t, S = paths.gbm(100.0, mu, s_r, T, n, 20000, seed=61 if tag_ == "30" else 62)
        imp = hedge.delta_hedge(t, S, K, T, s_i, position=1, sigma_price=s_i)["pnl"]
        act = hedge.delta_hedge(t, S, K, T, s_r, position=1, sigma_price=s_i)["pnl"]
        out[f"imp_{tag_}"], out[f"act_{tag_}"] = imp, act
        out[f"stats_{tag_}"] = {"imp_mean": float(imp.mean()), "imp_sd": float(imp.std()),
                                "act_mean": float(act.mean()), "act_sd": float(act.std()),
                                "imp_loss": float((imp < 0).mean()), "act_loss": float((act < 0).mean()),
                                "locked": float(bs.price(100.0, K, T, s_r) - bs.price(100.0, K, T, s_i))}
        if tag_ == "30":
            # three paths marked to market at the implied (market) volatility, hedged both ways
            dt = T / n
            tau = T - t
            Sp = S[:3]
            Vi = bs.price(Sp, K, np.maximum(tau, 1e-12), s_i)
            prem = float(bs.price(100.0, K, T, s_i))
            for name, sh in (("imp", s_i), ("act", s_r)):
                d = bs.greeks(Sp[:, :-1], K, np.maximum(tau[:-1], 1e-12), sh)["delta"]
                gains = np.concatenate([np.zeros((3, 1)), np.cumsum(-d * np.diff(Sp, axis=1), axis=1)], axis=1)
                out[f"mtm_{name}"] = Vi - prem + gains
            out["t"] = t
            out["paths"] = Sp
    return out


def compute_dgamma3d() -> dict:
    """Chapter 8: dollar gamma 1/2 Gamma S^2 over (t, S) at the hedge volatility of wrong_vol, and the column each
    of the two paths fills, int 1/2 Gamma S^2 dt."""
    w = load("wrong_vol")
    K, T, sig = w["K"], w["T"], w["sigma_i"]
    t = np.linspace(0, T * 0.985, 50)
    S = np.linspace(88, 132, 40)
    G = np.array([[0.5 * float(bs.greeks(s, K, T - x, sig)["gamma"]) * s * s for s in S] for x in t])
    tt = np.asarray(w["t"], float)
    cols = {}
    for name in ("near", "far"):
        P = np.asarray(w[f"S_{name}"], float)
        g = 0.5 * bs.greeks(P[:-1], K, T - tt[:-1], sig)["gamma"] * P[:-1] ** 2
        cols[name] = np.concatenate([[0.0], np.cumsum(g * np.diff(tt))])
    return {"t": t, "S": S, "G": G, "col_near": cols["near"], "col_far": cols["far"], "K": K, "T": T, "sigma": sig}


def compute_discrete_seeds() -> dict:
    """Chapter 9: the hedging error's sd against the number of hedges, 5 seeds of 20,000 paths (resumable); the
    distribution's skew at 13 and 252 hedges."""
    K, T, sig = 100.0, 0.25, 0.2
    Ns = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    part = CACHE.partial("discrete_seeds", {"K": K, "T": T, "sigma": sig, "Ns": Ns, "paths": 20000})
    for seed in range(5):
        for N in Ns:
            key = f"{seed}_{N}"
            if key not in part:
                t, S = paths.gbm(100.0, 0.0, sig, T, N, 20000, seed=700 + 10 * seed + N % 7)
                p = hedge.delta_hedge(t, S, K, T, sig, position=-1)["pnl"]
                part[key] = {"sd": float(p.std()), "mean": float(p.mean()), "skew": float(stats.skew(p))}
    sd = np.array([[part[f"{s}_{N}"]["sd"] for N in Ns] for s in range(5)])
    sk = np.array([[part[f"{s}_{N}"]["skew"] for N in Ns] for s in range(5)])
    hists = {}
    for N in (13, 252):
        t, S = paths.gbm(100.0, 0.0, sig, T, N, 20000, seed=790 + N)
        p = hedge.delta_hedge(t, S, K, T, sig, position=-1)["pnl"]
        hists[str(N)] = {"pnl": p, "skew": float(stats.skew(p)), "sd": float(p.std())}
    slopes = [float(np.polyfit(np.log(Ns), np.log(row), 1)[0]) for row in sd]
    return {"N": np.array(Ns), "sd": sd, "skew": sk, "slopes": slopes, "pnl_13": hists["13"]["pnl"],
            "pnl_252": hists["252"]["pnl"], "skew_13": hists["13"]["skew"], "skew_252": hists["252"]["skew"],
            "sd_13": hists["13"]["sd"], "sd_252": hists["252"]["sd"], "spread_max": float(np.max(sd.max(0) / sd.min(0) - 1))}


JUMPS = {"lam": 2.0, "mj": -0.05, "sj": 0.08}


def compute_jump_floor() -> dict:
    """Chapter 9 (Derman and Taleb 2005): hedging in steps on Merton jump paths, against GBM with the same total
    variance: the jump error does not shrink as hedging gets more frequent."""
    K, T, sig = 100.0, 0.25, 0.2
    lam, mj, sj = JUMPS["lam"], JUMPS["mj"], JUMPS["sj"]
    tot = float(np.sqrt(sig ** 2 + lam * (mj ** 2 + sj ** 2)))
    Ns = [16, 32, 64, 128, 256, 512, 1024]
    part = CACHE.partial("jump_floor", {"K": K, "T": T, "sigma": sig, **JUMPS, "Ns": Ns, "paths": 10000})
    for seed in range(3):
        for N in Ns:
            key = f"{seed}_{N}"
            if key not in part:
                Sj = sim.merton_jumps(100.0, 0.0, sig, lam, mj, sj, T, N, 10000, seed=900 + 10 * seed + N % 7)
                t = np.linspace(0, T, N + 1)
                pj = hedge.delta_hedge(t, Sj, K, T, tot, position=-1)["pnl"]
                t2, Sg = paths.gbm(100.0, 0.0, tot, T, N, 10000, seed=950 + 10 * seed + N % 7)
                pg = hedge.delta_hedge(t2, Sg, K, T, tot, position=-1)["pnl"]
                part[key] = {"jump": float(pj.std()), "gbm": float(pg.std())}
    J = np.array([[part[f"{s}_{N}"]["jump"] for N in Ns] for s in range(3)])
    G = np.array([[part[f"{s}_{N}"]["gbm"] for N in Ns] for s in range(3)])
    # the floor: the variance the jumps leave whatever the frequency, int lam E[(V(Se^J) - V - Delta S(e^J - 1))^2] dt
    z, wz = np.polynomial.hermite_e.hermegauss(40)
    wz = wz / wz.sum()
    ts = np.linspace(0, T, 81)[:-1] + T / 160
    acc = 0.0
    for t_ in ts:
        St = 100.0 * np.exp(-0.5 * tot ** 2 * t_ + tot * np.sqrt(t_) * z)
        tau = T - t_
        g = bs.greeks(St, K, tau, tot)
        for jz, jw in zip(z, wz):
            Sj_ = St * np.exp(mj + sj * jz)
            err = bs.price(Sj_, K, tau, tot) - g["price"] - g["delta"] * (Sj_ - St)
            acc += jw * float(np.sum(wz * err ** 2)) * lam * (T / 80)
    return {"N": np.array(Ns), "jump": J, "gbm": G, "total_vol": tot, **JUMPS, "floor": float(np.sqrt(acc)),
            "ratio_jump": float(J.mean(0)[0] / J.mean(0)[-1]), "ratio_gbm": float(G.mean(0)[0] / G.mean(0)[-1])}


def compute_leland_grid() -> dict:
    """Chapter 10: the short at-the-money call over hedges per quarter N and one-way cost k: expected cost, the sd of
    the hedged P&L, and their sum; the best N for each k."""
    K, T, sig = 100.0, 0.25, 0.2
    Ns = [4, 8, 13, 26, 52, 126, 252]
    ks = [0.0, 0.0002, 0.0005, 0.001, 0.0025, 0.005]
    part = CACHE.partial("leland_grid", {"Ns": Ns, "ks": ks, "paths": 10000})
    for N in Ns:
        if str(N) in part:
            continue
        t, S = paths.gbm(100.0, 0.0, sig, T, N, 10000, seed=1100 + N)
        row = []
        for k in ks:
            o = hedge.delta_hedge(t, S, K, T, sig, position=-1, cost=k)
            row.append({"cost": float(o["cost_total"].mean()), "sd": float(o["pnl"].std()),
                        "mean": float(o["pnl"].mean())})
        part[str(N)] = row
    cost = np.array([[part[str(N)][j]["cost"] for N in Ns] for j in range(len(ks))])
    sd = np.array([[part[str(N)][j]["sd"] for N in Ns] for j in range(len(ks))])
    tot = cost + sd
    best = [int(Ns[int(np.argmin(r))]) for r in tot]
    lab = {"daily": float(bs.leland_vol(0.2, 0.002, 1 / 252)), "weekly": float(bs.leland_vol(0.2, 0.002, 1 / 52))}
    return {"N": np.array(Ns), "k": np.array(ks), "cost": cost, "sd": sd, "total": tot, "best": best, "lab": lab}


def compute_kabanov() -> dict:
    """Chapter 10 (Kabanov and Safarian 1997): Leland's strategy with a fixed cost and ever more frequent hedging:
    the volatility and the premium grow without bound; what the book's error does."""
    K, T, sig, k = 100.0, 0.25, 0.2, 0.0025
    Ns = [13, 52, 252, 1008, 4032]
    n_paths = {13: 10000, 52: 10000, 252: 10000, 1008: 4000, 4032: 2000}  # memory: paths x steps stays small
    part = CACHE.partial("kabanov", {"Ns": Ns, "k": k, "paths": n_paths})
    for N in Ns:
        if str(N) in part:
            continue
        sL = float(bs.leland_vol(sig, 2 * k, T / N))
        t, S = paths.gbm(100.0, 0.0, sig, T, N, n_paths[N], seed=1200 + N)
        o = hedge.delta_hedge(t, S, K, T, sL, position=-1, sigma_price=sL, cost=k, cost_ends=False)
        part[str(N)] = {"sigma_L": sL, "premium": float(bs.price(100.0, K, T, sL)), "mean": float(o["pnl"].mean()),
                        "sd": float(o["pnl"].std()), "cost": float(o["cost_total"].mean())}
    rows = [dict(N=N, paths=n_paths[N], **part[str(N)]) for N in Ns]
    return {"rows": rows, "k": k, "premium_bs": float(bs.price(100.0, K, T, sig)), "share": 100.0}


def _surface_quotes():
    d = load("implied")
    q = d["q0"]
    T, K, F, iv, cp = (np.asarray(q[k], float) for k in ("T", "K", "F", "iv", "cp"))
    return d, q, T, K, F, iv, cp


def compute_solver_race() -> dict:
    """Chapter 11: every Surface quote inverted at once: the House's solver (Corrado–Miller start, bracketed Newton)
    against plain Newton from a flat 50% start; the normalized price surface b(x, s); one tick's worth of vol."""
    from scipy.special import ndtr

    d, q, T, K, F, iv, cp = _surface_quotes()
    p = bs.price(F, K, T, iv, 0, 0, cp)
    sol, its = bs.implied_vol(p, F, K, T, 0, 0, cp, return_iterations=True)
    E = np.array([np.abs(x - iv) for x in its])
    need = np.array([int(np.argmax(E[:, j] < 1e-10)) if (E[:, j] < 1e-10).any() else len(its) for j in range(len(iv))])
    x = np.log(F / K)
    target = p / np.sqrt(F * K)

    def nprice(s):
        with np.errstate(all="ignore"):
            d1 = x / s + s / 2
            return cp * (np.exp(x / 2) * ndtr(cp * d1) - np.exp(-x / 2) * ndtr(cp * (d1 - s)))

    def nvega(s):
        with np.errstate(all="ignore"):
            d1 = x / s + s / 2
            return np.exp(x / 2) * bs.npdf(d1)

    s = 0.5 * np.sqrt(T)
    naive = [s / np.sqrt(T)]
    broke = np.zeros(len(T), bool)
    for _ in range(14):
        with np.errstate(all="ignore"):
            s = s - (nprice(s) - target) / nvega(s)
        broke |= ~np.isfinite(s) | (s <= 0)
        naive.append(s / np.sqrt(T))
    En = np.array([np.where(np.isfinite(v), np.abs(v - iv), np.inf) for v in naive])
    n_iter = 13
    house_err = np.array([E[min(i, len(E) - 1)] for i in range(n_iter)])
    naive_err = En[:n_iter]
    worst = int(np.argmax(need))
    # one tick: the worst (flattest) quote priced 0.01% of the forward higher
    j = worst
    bumped = float(bs.implied_vol(p[j] + 1e-4 * F[j], F[j], K[j], T[j], 0, 0, cp[j]))
    xs = np.linspace(-1.0, 1.0, 41)
    ss = np.linspace(0.02, 1.2, 40)
    B = np.array([[float(np.exp(a / 2) * ndtr(a / sv + sv / 2) - np.exp(-a / 2) * ndtr(a / sv - sv / 2))
                   for a in xs] for sv in ss])
    atm = int(np.argmin(np.abs(x) + 10 * (T < 20 / 365)))
    return {"iters_house": len(its) - 1, "need": need, "median": float(np.median(need)),
            "p90": float(np.percentile(need, 90)), "max": int(need.max()), "worst": worst,
            "worst_T_days": float(T[worst] * 365), "worst_k": float(np.log(K[worst] / F[worst])),
            "worst_iv": float(iv[worst]), "worst_vega": float(nvega(iv[worst] * np.sqrt(T[worst]))[worst]),
            "house_max": np.nanmax(house_err, axis=1), "house_med": np.nanmedian(house_err, axis=1),
            "naive_max": np.max(np.where(np.isfinite(naive_err), naive_err, 9.99), axis=1),
            "naive_med": np.median(np.where(np.isfinite(naive_err), naive_err, 9.99), axis=1),
            "naive_broke": int(broke.sum()), "naive_unfinished": int(np.sum(~(En[-1] < 1e-8))),
            "house_paths": np.array([np.where(np.isfinite(v), v, np.nan) for v in its[:n_iter]]),
            "naive_paths": np.array([np.where(np.isfinite(v) & (v > 0) & (v < 3), v, np.nan) for v in naive[:n_iter]]),
            "k": np.log(K / F), "T": T, "iv": iv, "n": int(len(iv)),
            "tick_iv": bumped, "tick_shift": float(bumped - iv[j]),
            "bx": xs, "bs_": ss, "B": B,
            "atm_j": atm, "atm_bs": float(0.4 * F[atm] * iv[atm] * np.sqrt(T[atm])),
            "atm_price": float(bs.price(F[atm], K[atm], T[atm], iv[atm], 0, 0, cp[atm])) if cp[atm] > 0 else
            float(bs.price(F[atm], K[atm], T[atm], iv[atm], 0, 0, 1))}


def compute_carry() -> dict:
    """Chapter 13: the carry (basis) per expiry, ln(F/S)/T, and the implied volatilities one would get by forgetting
    the forward (inverting with spot and no carry)."""
    d, q, T, K, F, iv, cp = _surface_quotes()
    S = float(q["S"])
    exps = d["expiries0"]
    eT = np.array([e["T"] for e in exps])
    eF = np.array([e["F"] for e in exps])
    par = [bool(e["parity"]) for e in exps]
    carry = np.log(eF / S) / eT
    p = bs.price(F, K, T, iv, 0, 0, cp)
    iv_s = bs.implied_vol(p, np.full_like(F, S), K, T, 0, 0, cp)
    err = 100 * (iv_s - iv)
    rows = []
    for e in exps:
        m = np.isclose(T, e["T"])
        rows.append({"days": float(e["T"] * 365), "calls": float(np.nanmean(err[m & (cp > 0)])) if (m & (cp > 0)).any()
                     else None, "puts": float(np.nanmean(err[m & (cp < 0)])) if (m & (cp < 0)).any() else None})
    # problem 7: an at-the-money-forward call, b = 4%, T = 0.5, sigma = 45%, inverted with S instead of F
    b, Tp, sp = 0.04, 0.5, 0.45
    Fp = 100 * np.exp(b * Tp)
    c = float(bs.price(Fp, Fp, Tp, sp))
    pp = float(bs.price(Fp, Fp, Tp, sp, 0, 0, -1))
    prob = {"call_iv": float(bs.implied_vol(c, 100.0, Fp, Tp)), "put_iv": float(bs.implied_vol(pp, 100.0, Fp, Tp, 0, 0, -1)),
            "approx": float(100 * b * Tp / (0.4 * np.sqrt(Tp)) / 100)}
    return {"S": S, "T": eT, "carry": carry, "parity": par, "basis_rate": float(q["basis_rate"]), "rows": rows,
            "k": np.log(K / F), "Tq": T, "cp": cp, "iv": iv, "iv_spot": iv_s, "problem7": prob}


def compute_american_more() -> dict:
    """Chapter 14: the early-exercise premium P_A - P_E over (S, time left) from 600-step trees; the boundary,
    raw and interpolated; Kim's integral against the tree; Barone-Adesi–Whaley; the call before a dividend."""
    K, sig, r = 100.0, 0.2, 0.05
    spots = np.linspace(60, 140, 33)
    taus = np.linspace(1 / 24, 1.0, 24)
    part = CACHE.partial("american_more", {"spots": spots.tolist(), "taus": taus.tolist(), "N": 600})
    for i, tau in enumerate(taus):
        if str(i) not in part:
            part[str(i)] = [trees.crr(s, K, tau, sig, r, N=600, cp=-1, american=True)["price"]
                            - float(bs.price(s, K, tau, sig, r, 0, -1)) for s in spots]
    prem = np.array([part[str(i)] for i in range(len(taus))])
    pb = trees.put_boundary(100.0, K, 1.0, sig, r, N=2000)
    eu = float(bs.price(100.0, K, 1.0, sig, r, 0, -1))
    kim_raw = eu + trees.early_exercise_premium(100.0, K, r, sig, pb["times"], pb["raw"])
    kim = eu + trees.early_exercise_premium(100.0, K, r, sig, pb["times"], pb["boundary"])
    o = bs.baw(100.0, K, 1.0, sig, r, cp=-1)
    baw_curve = np.array([float(bs.baw(s, K, 1.0, sig, r, cp=-1)["price"]) for s in spots])
    # the call with one cash dividend just before expiry
    dv = trees.american_call_dividend(100.0, 90.0, 0.5, 0.05, 0.25, 4.0, 0.4, N=400)
    steps = sorted({n for n, _, _ in dv["region"]})
    return {"spots": spots, "taus": taus, "premium": prem, "b_times": pb["times"], "b_smooth": pb["boundary"],
            "b_raw": pb["raw"], "tree": pb["price"], "european": eu, "kim": kim, "kim_raw": kim_raw,
            "baw": float(o["price"]), "baw_critical": o["critical"],
            "tree_critical": float(pb["raw"][np.isfinite(pb["raw"])][0]),
            "smooth_critical": float(pb["boundary"][np.isfinite(pb["boundary"])][0]), "baw_curve": baw_curve,
            "div": {"S": 100.0, "K": 90.0, "T": 0.5, "D": 4.0, "tD": 0.4, "american": dv["price"],
                    "european": dv["european"], "steps": steps, "first_t": float(min(steps) * dv["dt"]),
                    "last_t": float(max(steps) * dv["dt"]), "n_nodes": len(dv["region"])}}


def compute_btc_replay() -> dict:
    """Chapter 15: the BTC study swept month by month: the running mean of the non-overlapping months and its 90%
    block-bootstrap interval (5 seeds x 200 resamples), the cumulative P&L, each month's gamma and theta."""
    b = load("btc")
    pnl = np.asarray(b["pnl"], float)
    sub = np.arange(0, len(pnl), 30)
    x = pnl[sub]
    n = len(x)
    lo_s, hi_s = [], []
    for seed in range(5):
        rng = np.random.default_rng(1500 + seed)
        lo, hi = np.full(n, np.nan), np.full(n, np.nan)
        for m in range(6, n + 1):
            blocks = int(np.ceil(m / 3))
            st = rng.integers(0, m - 2, size=(200, blocks))
            idx = (st[:, :, None] + np.arange(3)).reshape(200, -1)[:, :m]
            means = x[:m][idx].mean(1)
            lo[m - 1], hi[m - 1] = np.percentile(means, [5, 95])
        lo_s.append(lo)
        hi_s.append(hi)
    run = np.cumsum(x) / np.arange(1, n + 1)
    return {"start": np.asarray(b["start"], float)[sub], "pnl": x, "running": run, "cum": np.cumsum(x),
            "lo": np.array(lo_s), "hi": np.array(hi_s), "gamma": np.asarray(b["gamma"], float)[sub],
            "theta": np.asarray(b["theta"], float)[sub], "gap": (np.asarray(b["iv"], float) - np.asarray(b["rv"], float))[sub],
            "n": n, "final_lo": float(np.min(np.array(lo_s)[:, -1])), "final_hi": float(np.max(np.array(hi_s)[:, -1])),
            "first_positive": float(np.asarray(b["start"], float)[sub][int(np.argmax(np.all(np.array(lo_s) > 0, axis=0)))])
            if np.any(np.all(np.array(lo_s) > 0, axis=0)) else None}


def compute_insurance87() -> dict:
    """Chapter 16: an illustrative insured portfolio (a one-year floor at 95, sigma 15%, bills at the T-bill rate)
    replicated daily on Kenneth French's market returns from 1 July 1987; Brady's rule checked on the model."""
    kf = data.ken_french_daily()
    d, r, rf = kf["date"], kf["mkt"], kf["rf"]
    i0, i1 = int(np.searchsorted(d, 19870701)), int(np.searchsorted(d, 19871231, side="right"))
    floor, T, sig = 95.0, 1.0, 0.15
    o = hedge.replicate_put(r[i0:i1], rf[i0:i1], floor, T, sig)
    dates = d[i0:i1]
    rr = float(rf[i0] * 252)

    def weight(S):
        g = bs.greeks(S, floor, T, sig, rr, 0, -1)
        return float(S * (1 + g["delta"]) / (S + g["price"]))

    w100, w90 = weight(100.0), weight(90.0)
    # stock held per insured dollar at 100 and at 90 (as a fraction of what was held): the model's sale on a 10% fall
    units_100 = w100 * (100 + float(bs.price(100, floor, T, sig, rr, 0, -1))) / 100
    units_90 = w90 * (90 + float(bs.price(90, floor, T, sig, rr, 0, -1))) / 90
    sold = 1 - units_90 / units_100

    def on(day):
        j = int(np.searchsorted(dates, day))
        return {"date": int(dates[j]), "w": float(o["w"][j]), "S": float(o["S"][j]), "V": float(o["V"][j])}

    end_oct = int(np.searchsorted(dates, 19871031)) - 1
    return {"dates": dates, "S": o["S"], "V": o["V"], "w": o["w"], "floor_value": o["floor_value"], "sigma": sig,
            "floor": floor, "rate": rr, "sold_on_10pct": sold, "w100": w100, "w90": w90,
            "oct5": on(19871005), "oct16": on(19871016), "oct19": on(19871019), "oct20": on(19871020),
            "end_oct": {"date": int(dates[end_oct]), "V": float(o["V"][end_oct + 1]), "S": float(o["S"][end_oct + 1])},
            "end": {"V": float(o["V"][-1]), "S": float(o["S"][-1])},
            "breach": bool(o["V"][end_oct + 1] < o["floor_value"])}


def compute_ltcm98() -> dict:
    """Chapter 17: the VIX through 1998 (FRED VIXCLS) and an illustrative unit short-vega book."""
    v = data.fred("VIXCLS", start="1998-01-01", through="1998-12-31")
    d, x = v["date"], v["value"]
    j0 = int(np.searchsorted(d, 19980701))
    jm = int(np.argmax(x))
    return {"date": d, "vix": x, "jul1": float(x[j0]), "jul1_date": int(d[j0]), "peak": float(x[jm]),
            "peak_date": int(d[jm]), "book": -(x - x[j0]), "low": float(x.min())}


def compute_industry() -> dict:
    """Chapter 18: the floor trader's rule C = 0.4 F sigma sqrt(T) at the money, against the exact price, for each
    expiry of the Surface."""
    d = load("implied")
    at, av = np.asarray(d["atm_T"], float), np.asarray(d["atm_iv"], float)
    exact = np.array([float(bs.price(1.0, 1.0, t, v)) for t, v in zip(at, av)])
    rule = 0.4 * av * np.sqrt(at)
    rel = rule / exact - 1
    return {"T": at, "iv": av, "exact": exact, "rule": rule, "rel": rel, "max_abs_rel": float(np.max(np.abs(rel))),
            "s_max": float(np.max(av * np.sqrt(at)))}


def _norm_otm(x, s):
    """The normalized out-of-the-money Black price: a call when K > F (x < 0), a put otherwise."""
    from scipy.special import ndtr

    cp = np.where(x < 0, 1.0, -1.0)
    d1 = x / s + s / 2
    return cp * (np.exp(x / 2) * ndtr(cp * d1) - np.exp(-x / 2) * ndtr(cp * (d1 - s)))


def compute_neural_iv() -> dict:
    """Chapter 19: a small network learns a first guess for implied volatility from (x, log normalized price), the
    gated-initial-guess idea of the 2026 papers, trained on synthetic quotes (5 seeds), then two Newton steps; scored
    on the Surface's quotes against the Corrado–Miller start."""
    import torch

    from explainer.quant.house import deep

    torch.set_num_threads(1)
    rng = np.random.default_rng(1900)
    n = 24000
    x = rng.uniform(-1.2, 1.2, n)
    s = np.exp(rng.uniform(np.log(0.03), np.log(1.4), n))
    b = _norm_otm(x, s)
    keep = b > 1e-9
    X = np.stack([x[keep], np.log(b[keep])], 1).astype(np.float32)
    y = np.log(s[keep]).astype(np.float32)
    d, q, T, K, F, iv, cp = _surface_quotes()
    xs = np.log(F / K)
    s_true = iv * np.sqrt(T)
    bq = _norm_otm(xs, s_true)
    Xq = np.stack([xs, np.log(bq)], 1).astype(np.float32)

    def guess(net):
        with torch.no_grad():
            return np.exp(net(torch.tensor(Xq)).numpy()[:, 0])

    def newton(s0, k):
        s_ = s0.copy()
        for _ in range(k):
            dd = xs / s_ + s_ / 2
            v = np.exp(xs / 2) * bs.npdf(dd)
            s_ = np.clip(s_ - (_norm_otm(xs, s_) - bq) / v, 1e-4, 4.0)
        return s_

    curves, snaps, final = [], [], []
    for seed in range(5):
        net, curve, sn = deep.train_mlp_trace(X, y, width=32, depth=2, epochs=60, lr=3e-3, batch=512, seed=seed,
                                             every=3, snap_every=12 if seed == 0 else 0,
                                             snap_fn=(lambda m: guess(m).tolist()) if seed == 0 else None)
        curves.append([c[1] for c in curve])
        g = guess(net)
        err0 = np.abs(g - s_true) / np.sqrt(T)
        err1 = np.abs(newton(g, 1) - s_true) / np.sqrt(T)
        err2 = np.abs(newton(g, 2) - s_true) / np.sqrt(T)
        final.append({"guess_med": float(np.median(err0)), "guess_max": float(np.max(err0)),
                      "one_med": float(np.median(err1)), "one_max": float(np.max(err1)),
                      "two_med": float(np.median(err2)), "two_max": float(np.max(err2))})
        if seed == 0:
            epochs = [c[0] for c in curve]
            snaps = {str(k): (np.asarray(v) / np.sqrt(T)).tolist() for k, v in sn.items()}
    # the classical start for comparison
    _, its = bs.implied_vol(bs.price(F, K, T, iv, 0, 0, cp), F, K, T, 0, 0, cp, return_iterations=True)
    cm = np.abs(its[0] - iv)
    return {"epochs": np.array(epochs), "loss": np.array(curves), "snaps": snaps, "final": final,
            "iv": iv, "k": np.log(K / F), "T": T, "cm_med": float(np.median(cm)), "cm_max": float(np.max(cm)),
            "n_train": int(keep.sum())}


ITEMS = {"tree": compute_tree, "riskneutral": compute_riskneutral, "ledger": compute_ledger, "wrong_vol": compute_wrong_vol,
         "discrete": compute_discrete, "implied": compute_implied, "btc": compute_btc, "crash87": compute_crash87,
         "heat": compute_heat, "tree3d": compute_tree3d, "mc_seeds": compute_mc_seeds, "hedge_choice": compute_hedge_choice,
         "dgamma3d": compute_dgamma3d, "discrete_seeds": compute_discrete_seeds, "jump_floor": compute_jump_floor,
         "leland_grid": compute_leland_grid, "kabanov": compute_kabanov, "solver_race": compute_solver_race,
         "carry": compute_carry, "american_more": compute_american_more, "btc_replay": compute_btc_replay,
         "insurance87": compute_insurance87, "ltcm98": compute_ltcm98, "industry": compute_industry,
         "neural_iv": compute_neural_iv}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
