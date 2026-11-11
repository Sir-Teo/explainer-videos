"""Every number in Part 35 (Who Trades With Whom), computed and cached in .cache/quant35/.

    python -m videos.quant.quant35.compute [items] [--force]

Theory is simulated; measurement uses Binance's public one-minute bars for BTCUSDT on the spot and USD-margined perpetual
markets (2021-2024), whose taker-buy volume gives the signed order flow directly, and Yahoo Finance's daily bars for ten
US ETFs (2015-2020).

* ``dealer``     an inventory dealer with and without quote skew (Garman; Ho and Stoll);
* ``gm``         Glosten and Milgrom's spread and beliefs, averaged over runs, for three shares of informed traders;
* ``kyle``       Kyle's one-shot equilibrium by Monte Carlo; the N-auction recursion; the continuous-time bridge;
* ``flow``       Kyle's lambda on Binance one-minute returns against signed flow: by month, by hour, by size;
* ``measures``   Roll, Corwin-Schultz and Amihud on ten ETFs against their dollar volume, and Roll on BTC minutes;
* ``vpin``       bulk-volume VPIN on BTC around two crashes, and its correlation with volatility;
* ``discovery``  Hasbrouck's information shares of the spot and perpetual markets, month by month.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import micro as M, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant35")
load = pit.counted(CACHE.load, 35)
START, END = "2021-01", "2024-12"
ETFS = ["SPY", "QQQ", "IWM", "EEM", "TLT", "HYG", "GLD", "XBI", "PFF", "IWC"]


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _btc(market="spot"):
    k = data.binance_klines("BTCUSDT", "1m", START, END, market=market)
    return k


# ---------------------------------------------------------------------------
# Theory
# ---------------------------------------------------------------------------
def compute_dealer() -> dict:
    out = {}
    for skew in (0.0, 0.05):
        runs = [M.inventory_dealer(20000, 0.5, skew, arrival=1.0, sigma=0.2, seed=s) for s in range(20)]
        inv = np.array([r["inventory"] for r in runs])
        pnl = np.array([r["pnl"][-1] for r in runs])
        out[str(skew)] = {"inv_sd": float(inv[:, 2000:].std()), "inv_max": float(np.abs(inv).max(1).mean()),
                          "pnl_mean": float(pnl.mean()), "pnl_sd": float(pnl.std()), "path": runs[0]["inventory"][::20]}
    return _json(out)


def compute_gm() -> dict:
    out = {}
    for mu in (0.1, 0.3, 0.5):
        sp, pb = [], []
        for s in range(400):
            g = M.gm_simulate(mu, 80, v_true=1.0, seed=s)
            sp.append(g["ask"] - g["bid"])
            pb.append(g["p"])
        sp, pb = np.array(sp), np.array(pb)
        first = [int(np.argmax(r > 0.99)) if np.any(r > 0.99) else 80 for r in pb]
        out[str(mu)] = {"spread": sp.mean(0), "belief": pb.mean(0), "spread0": float(sp[0, 0]),
                        "to99": float(np.median(first)), "example": M.gm_simulate(mu, 80, seed=7)["p"]}
    return _json(out)


def compute_kyle() -> dict:
    rng = np.random.default_rng(35)
    sv, su = 1.0, 1.0
    k = M.kyle_one(sv, su)
    v = rng.normal(0, sv, 200000)
    u = rng.normal(0, su, 200000)
    x = k["beta"] * v
    p = k["lambda"] * (x + u)
    mc = {"profit": float(np.mean((v - p) * x)), "post_var": float(np.var(v - p)),
          "noise_loss": float(np.mean((p - v) * u))}
    # deviations: if the insider traded more or less aggressively against the same lambda
    dev = [{"scale": c, "profit": float(np.mean((v - k["lambda"] * (c * x + u)) * c * x))} for c in (0.5, 0.75, 1.0, 1.25, 1.5)]
    multi = {}
    for N in (1, 2, 4, 16, 64, 256):
        m = M.kyle_multi(N, sv, su)
        multi[str(N)] = {"lambda0": float(m["lambda"][0]), "Sigma_half": float(np.interp(0.5, m["t"], m["Sigma"])),
                         "Sigma_end": float(m["Sigma"][-1]), "lam": m["lambda"], "Sigma": m["Sigma"]}
    # the continuous-time bridge: many paths, Var(v - p_t) against 1 - t, and the insider's profit
    T = 400
    paths, vs, profits = [], [], []
    for s in range(600):
        vv = float(rng.normal(0, sv))
        c = M.kyle_continuous(vv, 0.0, sv, su, n=T, seed=1000 + s)
        paths.append(c["p"])
        vs.append(vv)
    P = np.array(paths)
    V = np.array(vs)
    var = ((V[:, None] - P) ** 2).mean(0)
    # profit: sum over steps of (v - p_{t+1}) dx; recompute dx from the strategy
    dt = 1.0 / T
    lam = sv / su
    tt = np.arange(T) * dt
    dx = (V[:, None] - P[:, :-1]) / (lam * np.maximum(1 - tt, dt)) * dt
    prof = float(np.mean(np.sum((V[:, None] - P[:, 1:]) * dx, 1)))
    return _json({"one": k, "mc": mc, "dev": dev, "multi": multi, "bridge_t": np.arange(T + 1) * dt,
                  "bridge_var": var, "bridge_example": [P[i] for i in range(4)], "bridge_v": V[:4],
                  "bridge_profit": prof, "bridge_profit_theory": sv * su})


# ---------------------------------------------------------------------------
# Measurement on Binance
# ---------------------------------------------------------------------------
def compute_flow() -> dict:
    k = _btc()
    t = k["time"]
    c = k["close"]
    r = np.r_[np.nan, np.diff(np.log(c))] * 1e4                   # bp
    flow = (2 * k["taker_buy"] - k["volume"]) * c / 1e6            # signed flow, $m
    mon_full = t.astype("int64").astype("datetime64[s]").astype("datetime64[M]")
    months = np.unique(mon_full)
    by_month = []
    for m in months:
        s = mon_full == m
        fit = M.kyle_lambda(r[s], flow[s])
        by_month.append({"month": str(m), **fit, "vol": float(np.nanstd(r[s])),
                         "flow_sd": float(np.nanstd(flow[s]))})
    hour = ((t // 3600) % 24).astype(int)
    by_hour = [{"hour": h, **M.kyle_lambda(r[hour == h], flow[hour == h]), "volume": float(np.mean(k["volume"][hour == h] *
                                                                                                    c[hour == h] / 1e6))}
               for h in range(24)]
    # concavity: mean return in buckets of signed flow
    q = np.nanquantile(flow, np.linspace(0.01, 0.99, 25))
    b = np.digitize(flow, q)
    buckets = [{"flow": float(np.nanmean(flow[b == i])), "ret": float(np.nanmean(r[b == i]))} for i in range(1, 25)]
    # aggregation: the same regression on 1, 5, 15 and 60-minute bars
    agg = {}
    for n in (1, 5, 15, 60):
        m_ = len(c) // n * n
        cc = c[:m_].reshape(-1, n)[:, -1]
        ff = flow[:m_].reshape(-1, n).sum(1)
        rr = np.r_[np.nan, np.diff(np.log(cc))] * 1e4
        agg[str(n)] = M.kyle_lambda(rr, ff)
    full = M.kyle_lambda(r, flow)
    return _json({"months": by_month, "hours": by_hour, "buckets": buckets, "agg": agg, "full": full,
                  "flow_sd": float(np.nanstd(flow)), "n": int(len(r))})


def compute_measures() -> dict:
    rows = []
    for sym in ETFS:
        b = data.yahoo_bars(sym, "2015-01-01", "2020-12-31")
        c, h, l_, v = (np.asarray(b[k], float) for k in ("close", "high", "low", "volume"))
        ret = np.r_[np.nan, np.diff(np.log(c))]
        dv = c * v
        roll_bp = M.roll_spread(np.log(c)) * 1e4
        # Corwin-Schultz (2012) two-day high-low estimator
        bta = (np.log(h[1:] / l_[1:])) ** 2 + (np.log(h[:-1] / l_[:-1])) ** 2
        gma = np.log(np.maximum(h[1:], h[:-1]) / np.minimum(l_[1:], l_[:-1])) ** 2
        k_ = 3 - 2 * math.sqrt(2)
        a_ = (np.sqrt(2 * bta) - np.sqrt(bta)) / k_ - np.sqrt(gma / k_)
        S = 2 * (np.exp(a_) - 1) / (1 + np.exp(a_))
        cs_bp = float(np.nanmean(np.maximum(S, 0))) * 1e4
        rows.append({"sym": sym, "roll_bp": roll_bp, "cs_bp": cs_bp, "amihud": M.amihud(ret, dv) * 1e9,
                     "dollar_vol": float(np.nanmedian(dv)), "vol": float(np.nanstd(ret) * math.sqrt(252))})
    k = _btc()
    sub = slice(0, 1440 * 365)
    roll_btc = M.roll_spread(np.log(k["close"][sub])) * 1e4
    return _json({"etfs": rows, "roll_btc_bp": roll_btc, "btc_tick_bp": float(0.01 / np.median(k["close"]) * 1e4)})


def compute_vpin() -> dict:
    k = _btc()
    t, c, vol = k["time"], k["close"], k["volume"]
    dp = np.r_[0.0, np.diff(np.log(c))]
    daily_vol = float(np.sum(vol) / (len(vol) / 1440))
    bucket = daily_vol / 50
    vp = M.bvc_vpin(dp, vol, bucket, n_buckets=50)
    # bucket end times
    cum = np.cumsum(vol)
    ends = np.searchsorted(cum, bucket * np.arange(1, len(vp) + 1))
    ends = np.minimum(ends, len(t) - 1)
    bt = t[ends]
    # realised volatility over each bucket window of 50 buckets
    rv = np.full(len(vp), np.nan)
    starts = np.r_[0, ends[:-1]]
    for i in range(49, len(vp), 10):
        a, b = starts[i - 49], ends[i]
        rv[i] = np.std(dp[a:b]) * math.sqrt(1440 * 365)
    ok = np.isfinite(vp) & np.isfinite(rv)
    corr = float(np.corrcoef(vp[ok], rv[ok])[0, 1])
    # actual taker imbalance per bucket window, to compare BVC with the true signed flow
    tb = k["taker_buy"]
    ctb = np.r_[0.0, np.cumsum(tb)]
    cv = np.r_[0.0, np.cumsum(vol)]
    true_imb = np.full(len(vp), np.nan)
    for i in range(49, len(vp), 10):
        a, b = starts[i - 49], ends[i] + 1
        buys = ctb[b] - ctb[a]
        tot = cv[b] - cv[a]
        true_imb[i] = abs(2 * buys - tot) / tot
    ok2 = np.isfinite(vp) & np.isfinite(true_imb)
    events = {}
    for name, day in (("2021-05-19", 1621382400), ("2022-11-08", 1667865600)):
        s = (bt >= day - 7 * 86400) & (bt <= day + 7 * 86400)
        i_p = (t >= day - 7 * 86400) & (t <= day + 7 * 86400)
        events[name] = {"t": (bt[s] - day) / 86400, "vpin": vp[s], "pt": (t[i_p][::30] - day) / 86400,
                        "price": c[i_p][::30]}
    step = max(1, len(vp) // 1500)
    return _json({"vpin": vp[::step], "t": bt[::step], "corr_rv": corr,
                  "corr_true": float(np.corrcoef(vp[ok2], true_imb[ok2])[0, 1]), "events": events,
                  "bucket_btc": bucket, "mean": float(np.nanmean(vp))})


def compute_discovery() -> dict:
    s = _btc("spot")
    f = _btc("futures/um")
    common = np.intersect1d(s["time"], f["time"])
    si = np.searchsorted(s["time"], common)
    fi = np.searchsorted(f["time"], common)
    ps, pf = np.log(s["close"][si]), np.log(f["close"][fi])
    month = common.astype("int64").astype("datetime64[s]").astype("datetime64[M]")
    out = []
    for m in np.unique(month):
        k = month == m
        if k.sum() < 20000:
            continue
        r = M.hasbrouck_is(pf[k], ps[k], lags=5)          # market 1: the perpetual, market 2: spot
        basis = float(np.mean(pf[k] - ps[k]) * 1e4)
        out.append({"month": str(m), "perp_low": r["is_low"][0], "perp_high": r["is_high"][0],
                    "perp_mid": r["is_mid"][0], "perp_gg": r["gg"][0], "basis_bp": basis})
    vol = {"spot": float(np.mean(s["volume"][si] * s["close"][si])), "perp": float(np.mean(f["volume"][fi] * f["close"][fi]))}
    rs, rf = np.diff(ps), np.diff(pf)
    ok = np.diff(common) == 60
    rs, rf = rs[ok], rf[ok]
    corr0 = float(np.corrcoef(rs, rf)[0, 1])
    lead_pf = float(np.corrcoef(rf[:-1], rs[1:])[0, 1])     # perp leads spot by a minute
    lead_sp = float(np.corrcoef(rs[:-1], rf[1:])[0, 1])
    width = float(np.mean([m["perp_high"] - m["perp_low"] for m in out]))
    return _json({"months": out, "dollar_vol_min": vol, "corr0": corr0, "lead_perp": lead_pf, "lead_spot": lead_sp,
                  "width": width})


def compute_cross() -> dict:
    """Kyle's lambda across five coins in 2024, against Kyle's prediction lambda ~ sigma_r / sigma_flow."""
    out = []
    for sym in ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"):
        k = data.binance_klines(sym, "1m", "2024-01", "2024-12")
        c = k["close"]
        r = np.r_[np.nan, np.diff(np.log(c))] * 1e4
        flow = (2 * k["taker_buy"] - k["volume"]) * c / 1e6
        fit = M.kyle_lambda(r, flow)
        out.append({"sym": sym[:-4], **fit, "sigma_r": float(np.nanstd(r)), "sigma_flow": float(np.nanstd(flow)),
                    "dollar_vol": float(np.mean(k["volume"] * c))})
    x = np.log([o["sigma_r"] / o["sigma_flow"] for o in out])
    y = np.log([o["lambda"] for o in out])
    b, a = np.polyfit(x, y, 1)
    ratio = [o["lambda"] * o["sigma_flow"] / o["sigma_r"] for o in out]
    return _json({"coins": out, "slope": float(b), "intercept": float(a), "ratio": ratio})


def compute_daily() -> dict:
    """Kyle's lambda for BTC day by day, 2021-2024: liquidity that comes and goes."""
    k = _btc()
    t, c = k["time"], k["close"]
    r = np.r_[np.nan, np.diff(np.log(c))] * 1e4
    flow = (2 * k["taker_buy"] - k["volume"]) * c / 1e6
    day = (t // 86400).astype(int)
    days = np.unique(day)
    lam, vol, dv = [], [], []
    for d_ in days:
        m = day == d_
        if m.sum() < 1000:
            lam.append(np.nan), vol.append(np.nan), dv.append(np.nan)
            continue
        lam.append(M.kyle_lambda(r[m], flow[m])["lambda"])
        vol.append(float(np.nanstd(r[m]) * math.sqrt(1440)))
        dv.append(float(np.sum(k["volume"][m] * c[m]) / 1e9))
    lam, vol, dv = np.array(lam), np.array(vol), np.array(dv)
    ok = np.isfinite(lam)
    top = np.argsort(np.where(ok, lam, -np.inf))[::-1][:5]
    dates = [str(np.datetime64(int(d_) * 86400, "s").astype("datetime64[D]")) for d_ in days]
    return _json({"dates": dates, "lambda": lam, "vol": vol, "dollar_bn": dv,
                  "top": [{"date": dates[i], "lambda": float(lam[i]), "vol": float(vol[i])} for i in top],
                  "median": float(np.nanmedian(lam)), "corr_vol": float(np.corrcoef(lam[ok], vol[ok])[0, 1]),
                  "corr_dv": float(np.corrcoef(lam[ok], dv[ok])[0, 1])})


def compute_acf() -> dict:
    """The autocorrelation of signed order flow and of returns, minute by minute: flow is persistent, returns are not."""
    k = _btc()
    c = k["close"]
    r = np.diff(np.log(c))
    flow = ((2 * k["taker_buy"] - k["volume"]) * c)[1:]
    lags = [1, 2, 5, 10, 30, 60, 120, 240]

    def ac(x, L):
        x = x - x.mean()
        return float(np.dot(x[L:], x[:-L]) / np.dot(x, x))
    sign = np.sign(flow)
    return _json({"lags": lags, "flow": [ac(flow, L) for L in lags], "sign": [ac(sign, L) for L in lags],
                  "ret": [ac(r, L) for L in lags]})


ITEMS = {"dealer": compute_dealer, "gm": compute_gm, "kyle": compute_kyle, "flow": compute_flow,
         "measures": compute_measures, "vpin": compute_vpin, "discovery": compute_discovery, "cross": compute_cross,
         "daily": compute_daily, "acf": compute_acf}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
