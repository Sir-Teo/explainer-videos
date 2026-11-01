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
"""

from __future__ import annotations

import numpy as np
from scipy import integrate, stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, hedge, paths, surface, trees

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
            "pick": pick, "pick_start": float(t0s[pick]), "pick_S": path, "pick_t": tt, "pick_iv": float(ivs[pick]),
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


ITEMS = {"tree": compute_tree, "ledger": compute_ledger, "wrong_vol": compute_wrong_vol,
         "discrete": compute_discrete, "implied": compute_implied, "btc": compute_btc, "crash87": compute_crash87}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
