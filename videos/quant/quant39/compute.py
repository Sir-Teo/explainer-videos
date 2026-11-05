"""Every number in Part 39 (Crypto and DeFi), computed and cached in .cache/quant39/.

    python -m videos.quant.quant39.compute [items] [--force]

Data: Binance's public archive (hourly spot and USD-M perpetual candles and eight-hourly funding for BTC and ETH,
September 2019 to December 2025; one-minute ETHUSDT candles for 2023; USDCUSDT in March 2023; USTUSDT, LUNAUSDT and
FTTUSDT around their collapses) and Yahoo Finance bars for GBTC and IBIT. Models: constant-product and concentrated
pools against arbitrageurs, sandwich attacks, perpetual funding, and a learned liquidity provider in simulation.

* ``amm``       a constant-product pool: price, a trade's slippage, impermanent loss by price ratio;
* ``lvr``       loss-versus-rebalancing on ETH's 2023 minutes: exact against sigma^2/8, by month and by sampling
                frequency, and the fee yield that breaks even;
* ``fees``      fees and blocks: the share of blocks with an arbitrage and arbitrage profit against LVR, for Poisson
                and fixed blocks and on ETH's real minutes;
* ``v3``        concentrated liquidity: capital efficiency by range, LVR per unit of capital, and how often ETH left
                ranges of each width in 2023;
* ``rl``        a learned liquidity provider choosing its range by volatility, against fixed ranges, in simulation;
* ``mev``       a sandwich on a constant-product pool: the attacker's profit by slippage tolerance and trade size;
* ``funding``   BTC and ETH funding, 2019-2025: the share at exactly 0.01%, yearly carry, negative spells, and
                funding against the premium of the perpetual over spot;
* ``carry``     the cash-and-carry book (long spot, short perpetual): nine variants on the research window, the
                chosen one registered and opened on 2021-2025;
* ``stable``    USDC in March 2023, UST and LUNA in May 2022, FTT in November 2022, minute by minute or hour by hour;
* ``etf``       GBTC against Bitcoin from 2022 to its conversion, and IBIT's first year;
* ``research``  the LVR theorem's checks: continuous and discrete identities, concentrated liquidity, and the trade
                probability with fees, by simulation and on ETH.
"""

from __future__ import annotations

import inspect
import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import defi as D
from explainer.quant.house import pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant39")
load = pit.counted(CACHE.load, 39)
MIN_YEAR = 365 * 24 * 60


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _ymd(t):
    import datetime as _dt
    return np.array([int(_dt.datetime.fromtimestamp(float(x), _dt.UTC).strftime("%Y%m%d")) for x in t])


def _eth_minutes():
    k = data.binance_klines("ETHUSDT", "1m", "2023-01", "2023-12")
    return k["time"], k["close"]


# ---------------------------------------------------------------------------
# AMMs
# ---------------------------------------------------------------------------
def compute_amm() -> dict:
    # an ETH/USDC pool: 5,000 ETH and 10m USDC, price 2,000
    x, y = 5000.0, 10_000_000.0
    rows = []
    for dx in (10.0, 100.0, 500.0, 1000.0):
        got, _, _ = D.cpmm_swap(x, y, -dx, fee=0.003)          # buy dx ETH
        avg = -got / dx
        rows.append({"dx": dx, "paid": -got, "avg": avg, "slip": avg / 2000.0 - 1})
    r = np.exp(np.linspace(math.log(0.1), math.log(10), 121))
    return _json({"x": x, "y": y, "trades": rows, "r": r, "il": D.impermanent_loss(r),
                  "il2": float(D.impermanent_loss(2.0)), "il_half": float(D.impermanent_loss(0.5)),
                  "il4": float(D.impermanent_loss(4.0))})


# ---------------------------------------------------------------------------
# LVR on ETH
# ---------------------------------------------------------------------------
def compute_lvr() -> dict:
    t, p = _eth_minutes()
    k = 1.0
    V = D.cpmm_value(k, p)
    step = D.lvr_step_cpmm(V[:-1], p[:-1], p[1:])
    frac = step / V[:-1]                                   # LVR per unit of pool value, per minute
    lr = np.diff(np.log(p))
    ym = _ymd(t[1:]) // 100
    months = []
    for m in np.unique(ym):
        s = ym == m
        months.append({"month": int(m), "lvr_pct": 100 * float(np.sum(frac[s])),
                       "rv8_pct": 100 * float(np.sum(lr[s] ** 2) / 8), "vol": float(np.sqrt(np.sum(lr[s] ** 2) * 12))})
    total = float(np.sum(frac))
    rv = float(np.sum(lr ** 2))
    by_freq = []
    for name, h in (("1 minute", 1), ("5 minutes", 5), ("1 hour", 60), ("1 day", 1440)):
        q = p[::h]
        Vq = D.cpmm_value(k, q)
        by_freq.append({"freq": name, "lvr_pct": 100 * float(np.sum(D.lvr_step_cpmm(Vq[:-1], q[:-1], q[1:]) / Vq[:-1])),
                        "vol": float(np.sqrt(np.sum(np.diff(np.log(q)) ** 2)))})
    # the simulated pool on the real minutes, no fee: the path of value against rebalancing and holding
    sim = D.arb_pool(p[::10], 0.0, k=1.0)
    hold = 0.5 * sim["V0"] * (p[::10] / p[0]) + 0.5 * sim["V0"]
    idx = np.linspace(0, len(sim["lp"]) - 1, 400).astype(int)
    return _json({"months": months, "lvr_pct": 100 * total, "rv8_pct": 100 * rv / 8, "vol": math.sqrt(rv),
                  "by_freq": by_freq, "p0": float(p[0]), "p1": float(p[-1]),
                  "path": {"day": (t[::10][idx] - t[0]) / 86400, "lp": sim["lp"][idx] / sim["V0"],
                           "rebal": sim["rebal"][idx] / sim["V0"], "hold": hold[idx] / sim["V0"],
                           "price": p[::10][idx]},
                  "il_year": float(D.impermanent_loss(p[-1] / p[0]))})


def compute_fees() -> dict:
    rng = np.random.default_rng(39)
    sig = 0.8 / math.sqrt(365 * 24 * 300)                  # 80% a year, per 12-second block
    n = 300 * 24 * 60
    out = {"sigma_block": sig, "poisson": [], "fixed": [], "eth": []}
    dts = rng.exponential(1.0, n)
    lp = np.cumsum(sig * np.sqrt(dts) * rng.standard_normal(n) - 0.5 * sig ** 2 * dts)
    pp = np.r_[2000.0, 2000.0 * np.exp(lp)]
    lp2 = np.cumsum(sig * rng.standard_normal(n) - 0.5 * sig ** 2)
    pf = np.r_[2000.0, 2000.0 * np.exp(lp2)]
    fees = (0.0001, 0.0005, 0.001, 0.003, 0.01)
    for name, path in (("poisson", pp), ("fixed", pf)):
        V = D.cpmm_value(1.0, path)
        l0 = float(np.sum(D.lvr_step_cpmm(V[:-1], path[:-1], path[1:])))
        for fee in fees:
            r = D.arb_pool(path, fee, k=1.0)
            out[name].append({"fee": fee, "p_trade": r["p_trade"], "theory": D.p_trade_theory(fee, sig, 1.0),
                              "arb_lvr": r["arb"] / l0, "fees_lvr": float(r["fees"][-1]) / l0})
    t, p = _eth_minutes()
    lr = np.diff(np.log(p))
    s_min = float(np.std(lr))
    V = D.cpmm_value(1.0, p)
    l0 = float(np.sum(D.lvr_step_cpmm(V[:-1], p[:-1], p[1:])))
    for fee in fees:
        r = D.arb_pool(p, fee, k=1.0)
        out["eth"].append({"fee": fee, "p_trade": r["p_trade"], "theory": D.p_trade_theory(fee, s_min, 1.0),
                           "arb_lvr": r["arb"] / l0, "fees_lvr": float(r["fees"][-1]) / l0})
    out["eth_sigma_min"] = s_min
    return _json(out)


def compute_v3() -> dict:
    t, p = _eth_minutes()
    widths = (1.01, 1.02, 1.05, 1.1, 1.25, 1.5, 2.0)
    rows = []
    day = (t - t[0]) // 86400
    starts = np.r_[0, np.flatnonzero(np.diff(day)) + 1]
    for w in widths:
        out_share = []
        for a, b in zip(starts, np.r_[starts[1:], len(p)]):
            p0 = p[a]
            seg = p[a:b]
            out_share.append(float(np.mean((seg < p0 / w) | (seg > p0 * w))))
        rows.append({"w": w, "pct": 100 * (w - 1), "eff": D.v3_efficiency(w), "out_share": float(np.mean(out_share)),
                     "days_left": float(np.mean(np.array(out_share) > 0))})
    # a concentrated position's value against price, for the picture
    L, pa, pb = 1.0, 1600.0, 2500.0
    grid = np.linspace(1200, 3000, 181)
    return _json({"rows": rows, "curve": {"p": grid, "v3": D.v3_value(L, grid, pa, pb),
                                          "x": D.v3_reserves(L, grid, pa, pb)[0], "y": D.v3_reserves(L, grid, pa, pb)[1]},
                  "pa": pa, "pb": pb})


# ---------------------------------------------------------------------------
# A learned liquidity provider
# ---------------------------------------------------------------------------
RL_ACTIONS = (None, 2.0, 1.2, 1.05)        # withdraw, wide, medium, narrow (range [P / w, P w], re-centred daily)
RL_NAMES = ("withdraw", "wide (x2)", "medium (+-20%)", "narrow (+-5%)")


def _lp_day(rng, sigma_y, w, steps=288, fee_yield=None, recentre=0.001):
    """One day of a concentrated (or withdrawn) position re-centred at the day's open: fee income while in range
    (``fee_yield`` per unit of full-range capital per day, scaled by the range's efficiency), minus the exact loss
    against rebalancing on a GBM path, minus the cost of re-centring. Per unit of capital."""
    if w is None:
        return 0.0
    s = sigma_y / math.sqrt(365 * steps)
    lp = np.r_[0.0, np.cumsum(s * rng.standard_normal(steps) - 0.5 * s * s)]
    p = 100.0 * np.exp(lp)
    pa, pb = 100.0 / w, 100.0 * w
    V0 = float(D.v3_value(1.0, 100.0, pa, pb))
    r = D.arb_pool(p, 0.0, L=1.0, pa=pa, pb=pb)
    loss = float(r["lvr"][-1]) / V0
    inr = float(np.mean((p > pa) & (p < pb)))
    return fee_yield * D.v3_efficiency(w) * inr - loss - recentre


def compute_rl() -> dict:
    rng = np.random.default_rng(7)
    sig = (0.45, 1.2)                      # calm and stormy regimes, annual
    switch = 0.05                          # daily probability of switching regime
    fee_yield = 0.75 ** 2 / 8 / 365        # a full-range pool breaks even at 75% volatility
    edges = (0.6, 0.9)                     # yesterday's realised volatility buckets

    def world(days, seed):
        r_ = np.random.default_rng(seed)
        reg = np.zeros(days, int)
        for d in range(1, days):
            reg[d] = reg[d - 1] ^ int(r_.random() < switch)
        return reg

    def realised(sig_y, r_):
        s = sig_y / math.sqrt(365 * 288)
        return float(np.sqrt(np.sum((s * r_.standard_normal(288)) ** 2) * 365))

    def state(v):
        return int(np.searchsorted(edges, v))

    # learning: one-step Q-learning (a contextual bandit, since the action does not change the next state)
    nS, nA = 3, len(RL_ACTIONS)
    Q = np.zeros((nS, nA))
    N = np.zeros((nS, nA))
    reg = world(4000, 1)
    v_prev = realised(sig[0], rng)
    curve = []
    for d in range(len(reg)):
        s_ = state(v_prev)
        a = int(rng.integers(nA)) if rng.random() < max(0.05, 1 - d / 2000) else int(np.argmax(Q[s_]))
        rwd = _lp_day(rng, sig[reg[d]], RL_ACTIONS[a], fee_yield=fee_yield)
        N[s_, a] += 1
        Q[s_, a] += (rwd - Q[s_, a]) / N[s_, a]
        v_prev = realised(sig[reg[d]], rng)
        if d % 200 == 199:
            curve.append({"day": d + 1, "Q": Q.copy()})
    policy = [int(np.argmax(Q[s_])) for s_ in range(nS)]
    # evaluation on a fresh world: the learned policy against every fixed choice and the regime oracle
    reg = world(2000, 2)
    ev = {n: [] for n in RL_NAMES}
    ev["learned"] = []
    ev["oracle"] = []
    v_prev = realised(sig[0], rng)
    best_by_regime = {}
    for g in (0, 1):
        rr = np.random.default_rng(100 + g)
        best_by_regime[g] = int(np.argmax([np.mean([_lp_day(rr, sig[g], w, fee_yield=fee_yield) for _ in range(150)])
                                           for w in RL_ACTIONS]))
    for d in range(len(reg)):
        seed = 10_000 + d
        for i, (n_, w) in enumerate(zip(RL_NAMES, RL_ACTIONS)):
            ev[n_].append(_lp_day(np.random.default_rng(seed), sig[reg[d]], w, fee_yield=fee_yield))
        a = policy[state(v_prev)]
        ev["learned"].append(_lp_day(np.random.default_rng(seed), sig[reg[d]], RL_ACTIONS[a], fee_yield=fee_yield))
        ev["oracle"].append(_lp_day(np.random.default_rng(seed), sig[reg[d]], RL_ACTIONS[best_by_regime[reg[d]]],
                                    fee_yield=fee_yield))
        v_prev = realised(sig[reg[d]], rng)
    res = {k_: {"mean_bp": 1e4 * float(np.mean(v)), "sd_bp": 1e4 * float(np.std(v)),
                "annual_pct": 100 * 365 * float(np.mean(v))} for k_, v in ev.items()}
    return _json({"Q": Q, "N": N, "policy": [RL_NAMES[a] for a in policy], "edges": edges, "sig": sig,
                  "switch": switch, "fee_yield": fee_yield, "curve": curve, "eval": res, "names": list(RL_NAMES),
                  "oracle": {str(g): RL_NAMES[a] for g, a in best_by_regime.items()}})


# ---------------------------------------------------------------------------
# MEV
# ---------------------------------------------------------------------------
def compute_mev() -> dict:
    x, y = 5000.0, 10_000_000.0
    rows = []
    for size in (10_000.0, 100_000.0, 1_000_000.0):
        for slip in (0.001, 0.005, 0.01, 0.03):
            s = D.sandwich(x, y, size, slip, fee=0.003)
            rows.append({"size": size, "slip": slip, "profit": s["profit"], "front": s["front"],
                         "victim_loss": s["shortfall"] * 2000.0})
    return _json({"x": x, "y": y, "rows": rows})


# ---------------------------------------------------------------------------
# Perpetuals and funding
# ---------------------------------------------------------------------------
def _hourly(sym):
    sp = data.binance_klines(sym, "1h", "2019-09", "2025-12", market="spot")
    fu = data.binance_klines(sym, "1h", PERP_START, "2025-12", market="futures/um")
    f = data.binance_funding(sym, FUND_START, "2025-12")
    common = np.intersect1d(sp["time"], fu["time"])
    i = np.searchsorted(sp["time"], common)
    j = np.searchsorted(fu["time"], common)
    return {"t": common, "spot": sp["close"][i], "perp": fu["close"][j], "ft": f["time"], "rate": f["rate"]}


PERP_START = "2020-01"
FUND_START = "2020-01"


def compute_funding() -> dict:
    out = {}
    for sym in ("BTCUSDT", "ETHUSDT"):
        h = _hourly(sym)
        ft, rate = h["ft"], h["rate"]
        years = (_ymd(ft) // 10000)
        by = []
        for y_ in range(2020, 2026):
            s = years == y_
            r = rate[s]
            by.append({"year": y_, "annual_pct": 100 * float(np.mean(r)) * 3 * 365, "at_base": float(np.mean(np.abs(r - 1e-4) < 1e-7)),
                       "neg": float(np.mean(r < 0)), "max_pct": 100 * float(np.max(r)), "min_pct": 100 * float(np.min(r))})
        prem = h["perp"] / h["spot"] - 1
        # the premium over the 8 hours before each settlement, against the rate set
        tt = h["t"]
        avgp, rr = [], []
        for t_, r_ in zip(ft, rate):
            s = (tt > t_ - 8 * 3600 - 1) & (tt <= t_ - 3600 + 1)
            if s.sum() >= 6:
                avgp.append(float(np.mean(prem[s])))
                rr.append(float(r_))
        avgp, rr = np.array(avgp), np.array(rr)
        rule = D.binance_funding_rule(avgp)
        b, a = np.polyfit(avgp, rr, 1)
        out[sym] = {"by_year": by, "at_base": float(np.mean(np.abs(rate - 1e-4) < 1e-7)), "neg": float(np.mean(rate < 0)),
                    "annual_pct": 100 * float(np.mean(rate)) * 3 * 365, "prem_med_bp": 1e4 * float(np.median(prem)),
                    "slope": float(b), "corr_rule": float(np.corrcoef(rule, rr)[0, 1]), "corr_prem": float(np.corrcoef(avgp, rr)[0, 1]),
                    "series": {"t": ft[::9], "rate": rate[::9]}, "n": int(len(rate)),
                    "scatter": {"prem": avgp[::7], "rate": rr[::7]}}
    return _json(out)


# ---------------------------------------------------------------------------
# The cash-and-carry book (registered)
# ---------------------------------------------------------------------------
STRATEGY = "carry_basis_part39"
COST = 0.0015            # entering or leaving: spot and perpetual legs, 7.5 bp each
LEV = 3.0                # the short perpetual is margined at 1/3 of its notional


def _carry_book(t, spot, perp, ft, rate, rule: str, cost: float = COST):
    """Hourly returns per unit of capital of a book long one unit of spot and short one unit of the perpetual,
    holding margin of 1/LEV of the notional for the short: price legs marked hourly, funding received at each
    settlement (paid when negative). ``rule``: "always", or "pos7" / "hurdle7" (hold only while the trailing seven-day
    mean funding is above zero / above 5% a year, decided at each settlement on rates already known), with a cost
    at each switch."""
    cap = 1.0 + 1.0 / LEV
    n = len(t)
    on = np.ones(n, bool)
    fi = np.searchsorted(ft, t, side="right") - 1          # the latest settlement at or before each hour
    if rule != "always":
        trail = np.array([np.mean(rate[max(0, i - 20):i + 1]) if i >= 0 else 0.0 for i in range(len(rate))])
        hurdle = 0.0 if rule == "pos7" else 0.05 / (3 * 365)
        dec = trail > hurdle
        on = np.where(fi >= 0, dec[np.clip(fi, 0, None)], False)
    ret = np.zeros(n)
    ret[1:] = (spot[1:] / spot[:-1] - 1) - (perp[1:] / perp[:-1] - 1) * (perp[:-1] / spot[:-1])
    ret[1:] *= on[:-1]
    # funding received at settlements falling in (t[i-1], t[i]] by a position open over that hour
    fsum = np.zeros(n)
    k = np.searchsorted(t + 3600, ft)                     # the hour whose close is at or after the settlement
    ok = (k > 0) & (k < n)
    np.add.at(fsum, k[ok], rate[ok])
    ret[1:] += fsum[1:] * on[:-1] * (perp[:-1] / spot[:-1])
    sw = np.r_[on[0], on[1:] != on[:-1]]
    ret -= sw * cost
    return ret / cap, on


def _monthly(t, r):
    ym = _ymd(t) // 100
    ks = np.unique(ym)
    return ks, np.array([np.prod(1 + r[ym == k]) - 1 for k in ks])


def _stats(r, per_year):
    r = np.asarray(r, float)
    m, s = float(np.mean(r)), float(np.std(r, ddof=1))
    eq = np.cumprod(1 + r)
    return {"ann_pct": 100 * ((1 + m) ** per_year - 1), "vol_pct": 100 * s * math.sqrt(per_year),
            "sharpe": m / s * math.sqrt(per_year) if s > 0 else float("nan"),
            "maxdd_pct": 100 * float(np.min(eq / np.maximum.accumulate(eq) - 1))}


def compute_carry() -> dict:
    from explainer.quant.house import track
    books = {}
    for sym in ("BTCUSDT", "ETHUSDT"):
        h = _hourly(sym)
        books[sym] = h
    t = np.intersect1d(books["BTCUSDT"]["t"], books["ETHUSDT"]["t"])
    d = _ymd(t)
    variants = []
    rets = {}
    for asset in ("BTC", "ETH", "BTC+ETH"):
        for rule in ("always", "pos7", "hurdle7"):
            rs = []
            for sym in (("BTCUSDT",) if asset == "BTC" else ("ETHUSDT",) if asset == "ETH" else ("BTCUSDT", "ETHUSDT")):
                h = books[sym]
                i = np.searchsorted(h["t"], t)
                r, _ = _carry_book(t, h["spot"][i], h["perp"][i], h["ft"], h["rate"], rule)
                rs.append(r)
            r = np.mean(rs, axis=0)
            rets[(asset, rule)] = r
            res = d <= pit.RESEARCH_END
            ks, mr = _monthly(t[res], r[res])
            variants.append({"asset": asset, "rule": rule, **_stats(mr, 12)})
    best = max(variants, key=lambda v: v["sharpe"])
    key = (best["asset"], best["rule"])
    code = inspect.getsource(_carry_book)
    pit.register(STRATEGY, code, {"asset": best["asset"], "rule": best["rule"], "cost": COST, "margin": 1 / LEV,
                                  "data": "Binance spot and USD-M perpetual hourly closes; eight-hourly funding"},
                 trials=len(variants))
    rate_mat = []
    fts = books["BTCUSDT"]["ft"]
    e_rate = np.interp(fts, books["ETHUSDT"]["ft"], books["ETHUSDT"]["rate"])
    rate_mat = np.c_[books["BTCUSDT"]["rate"], e_rate]
    pit.open_envelope(STRATEGY, "binance/btc_eth_funding_8h", _ymd(fts), np.round(rate_mat, 10))
    r = rets[key]
    res = d <= pit.RESEARCH_END
    hold = d >= pit.HOLDOUT_START
    rm_k, rm = _monthly(t[res], r[res])
    hm_k, hm = _monthly(t[hold], r[hold])
    row = track.record(STRATEGY, 39, rm, hm, 0.0,
                       note=f"cash-and-carry, {best['asset']}, rule {best['rule']}, net of 15 bp a switch, 1/3 margin")
    years = {}
    for y_ in range(2021, 2026):
        s = (d // 10000) == y_
        years[str(y_)] = {"ret_pct": 100 * float(np.prod(1 + r[s]) - 1), **_stats(_monthly(t[s], r[s])[1], 12)}
    eq = np.cumprod(1 + r[hold])
    idx = np.linspace(0, len(eq) - 1, 500).astype(int)
    # what a venue failure would have done: the margin (a quarter of capital) lost at a stroke
    on_share = float(np.mean(_carry_book(t, books["BTCUSDT"]["spot"][np.searchsorted(books["BTCUSDT"]["t"], t)],
                                         books["BTCUSDT"]["perp"][np.searchsorted(books["BTCUSDT"]["t"], t)],
                                         books["BTCUSDT"]["ft"], books["BTCUSDT"]["rate"], best["rule"])[1][hold]))
    return _json({"variants": variants, "best": best, "trials": pit.trials_so_far(), "n_trials": len(variants),
                  "row": row, "years": years, "hold": _stats(hm, 12), "res": _stats(rm, 12),
                  "eq": {"day": (t[hold][idx] - t[hold][0]) / 86400, "v": eq[idx]}, "on_share": on_share,
                  "margin_share": (1 / LEV) / (1 + 1 / LEV), "res_months": len(rm), "hold_months": len(hm)})


# ---------------------------------------------------------------------------
# Stablecoins and collapses
# ---------------------------------------------------------------------------
def compute_stable() -> dict:
    u = data.binance_klines("USDCUSDT", "1m", "2023-03", "2023-03")
    lo = int(np.argmin(u["low"]))
    below = u["close"] < 0.98
    rec = int(np.argmax((u["time"] > u["time"][lo]) & (u["close"] > 0.995)))
    idx = np.linspace(0, len(u["time"]) - 1, 600).astype(int)
    out = {"usdc": {"t": u["time"][idx], "p": u["close"][idx], "low": float(u["low"][lo]), "t_low": float(u["time"][lo]),
                    "t0": float(u["time"][0]), "min_below98": int(below.sum()), "hours_to_995": (u["time"][rec] - u["time"][lo]) / 3600}}
    for sym, mo in (("USTUSDT", "2022-05"), ("LUNAUSDT", "2022-05"), ("FTTUSDT", "2022-11")):
        k = data.binance_klines(sym, "1h", mo, mo)
        if sym == "LUNAUSDT":           # after 28 May the symbol is the new chain's token: keep the original's collapse
            keep = k["time"] < 1652486400                # 14 May 2022, 00:00 UTC
            k = {c: v[keep] for c, v in k.items()}
        out[sym] = {"t": k["time"], "p": k["close"], "low": float(np.min(k["low"])), "first": float(k["close"][0]),
                    "last": float(k["close"][-1]), "t_last": float(k["time"][-1])}
    # Diamond-Dybvig on chain: reserves liquid share l, the rest sold at a discount d in a run
    dd = []
    for l in (1.0, 0.8, 0.5, 0.2):
        for disc in (0.05, 0.2):
            value_in_run = l + (1 - l) * (1 - disc)              # what the reserves are worth if all redeem at once
            dd.append({"liquid": l, "disc": disc, "full_run": value_in_run, "last_get": max(0.0, value_in_run - 0.0)})
    out["dd"] = dd
    return _json(out)


def compute_etf() -> dict:
    g = data.yahoo_bars("GBTC", "2022-01-01", "2024-12-31")
    i = data.yahoo_bars("IBIT", "2024-01-01", "2024-12-31")
    b = data.binance_klines("BTCUSDT", "1d", "2022-01", "2024-12")
    bd = _ymd(b["time"])
    gd = np.array([int(x) for x in g["date"]])
    common = np.intersect1d(gd, bd)
    gi = np.searchsorted(gd, common)
    bi = np.searchsorted(bd, common)
    ratio = np.asarray(g["close"], float)[gi] / b["close"][bi]
    k0 = int(np.argmin(np.abs(common - 20221230)))
    k1 = int(np.argmin(np.abs(common - 20240110)))
    idd = np.array([int(x) for x in i["date"]])
    vol = np.asarray(i["volume"], float) * np.asarray(i["close"], float)
    return _json({"gbtc": {"d": common, "ratio": ratio / ratio[k0], "rise": float(ratio[k1] / ratio[k0] - 1)},
                  "ibit": {"d": idd, "dollar_vol": vol, "first_day_bn": float(vol[0] / 1e9),
                           "mean_bn": float(np.mean(vol) / 1e9), "close_last": float(np.asarray(i["close"])[-1])}})


# ---------------------------------------------------------------------------
# Research: the LVR theorem's checks
# ---------------------------------------------------------------------------
def compute_research() -> dict:
    rng = np.random.default_rng(3939)
    sig = 0.01                                              # per step
    n = 400_000
    p = np.r_[100.0, 100.0 * np.exp(np.cumsum(sig * rng.standard_normal(n) - 0.5 * sig ** 2))]
    V = D.cpmm_value(1.0, p)
    r = D.arb_pool(p, 0.0, k=1.0)
    cont = float(np.sum(D.lvr_rate_cpmm(sig, V[:-1])))
    exact = float(np.sum(D.lvr_step_cpmm(V[:-1], p[:-1], p[1:])))
    # refinement: the same Brownian path on finer grids, so discrete LVR converges to sigma^2/8
    ref = []
    for m in (1, 4, 16, 64):
        rr = np.random.default_rng(5)
        s_ = 1.0 / math.sqrt(m)                             # a step's volatility, refined at a fixed total variance
        R = np.exp(rr.standard_normal(4_000_000) * s_ - 0.5 * s_ ** 2)
        per_v = (np.sqrt(R) - 1) ** 2 / 2                   # the exact one-step loss per unit of pool value
        ref.append({"m": m, "step_sigma": s_, "ratio": float(np.mean(per_v) / (s_ ** 2 / 8)),
                    "closed": float((1 - math.exp(-s_ ** 2 / 8)) / (s_ ** 2 / 8))})
    # concentrated: a range around the start, simulated against sigma^2 L sqrt(P)/4 in range
    L, pa, pb = 1.0, 60.0, 160.0
    q = p[:100_000]
    r3 = D.arb_pool(q, 0.0, L=L, pa=pa, pb=pb)
    th3 = float(np.sum(D.lvr_rate_v3(sig, L, q[:-1], pa, pb)))
    # trade probability: the stationary mispricing density, measured in simulation
    sigb = 0.002
    dts = rng.exponential(1.0, n)
    path = np.r_[100.0, 100.0 * np.exp(np.cumsum(sigb * np.sqrt(dts) * rng.standard_normal(n) - 0.5 * sigb ** 2 * dts))]
    fee = 0.003
    rf = D.arb_pool(path, fee, k=1.0)
    Vp = D.cpmm_value(1.0, path)
    l0 = float(np.sum(D.lvr_step_cpmm(Vp[:-1], path[:-1], path[1:])))
    # the mispricing z = log(p / P) just before each block, from a re-run that records it
    P = path[0]
    g = 1 - fee
    zs = []
    for t in range(1, len(path)):
        zs.append(math.log(path[t] / P))
        if g * P > path[t]:
            P = path[t] / g
        elif P < g * path[t]:
            P = path[t] * g
    zs = np.array(zs)
    band = -math.log(g)
    hist, edges = np.histogram(zs, bins=80, range=(-4 * band, 4 * band), density=True)
    a_ = math.sqrt(2.0) / sigb
    c_ = 1.0 / (2 * band + 2 / a_)
    zc = 0.5 * (edges[1:] + edges[:-1])
    dens = np.where(np.abs(zc) <= band, c_, c_ * np.exp(-a_ * (np.abs(zc) - band)))
    return _json({"cont": cont, "exact": exact, "sim": float(r["lvr"][-1]), "ratio": exact / cont, "refine": ref,
                  "v3": {"sim": float(r3["lvr"][-1]), "theory": th3, "in_range": float(np.mean((q > pa) & (q < pb)))},
                  "trade": {"fee": fee, "sigma": sigb, "p_trade": rf["p_trade"], "theory": D.p_trade_theory(fee, sigb, 1.0),
                            "arb_lvr": rf["arb"] / l0, "outside": float(np.mean(np.abs(zs) > band)),
                            "hist": hist, "zc": zc, "dens": dens, "band": band}})


ITEMS = {"amm": compute_amm, "lvr": compute_lvr, "fees": compute_fees, "v3": compute_v3, "rl": compute_rl,
         "mev": compute_mev, "funding": compute_funding, "carry": compute_carry, "stable": compute_stable,
         "etf": compute_etf, "research": compute_research}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
