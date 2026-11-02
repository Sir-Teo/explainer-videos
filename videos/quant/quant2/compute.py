"""Every number in Part 2 (The Machinery of Markets), computed and cached in .cache/quant2/.

    python -m videos.quant.quant2.compute [items] [--force]

Items (each seeded; seconds on a laptop):

* ``margin``    leveraged long BTC perpetuals (2x, 3x, 10x) opened on 1 March 2020 on Binance, marked to market hour
                by hour with funding, through the crash of 12 March: equity, maintenance margin, liquidations;
* ``netting``   a day of trades among 25 clearing members: gross, bilateral-net and centrally netted obligations;
* ``auction``   a closing auction: 300 limit orders, demand and supply, the price that executes the most;
* ``funding``   the perpetual's funding rate through 2020 and what holding one coin long cost;
* ``repo``      the repo market in September 2019 (FRED): SOFR, fed funds, interest on reserves, bank reserves;
* ``fees``      a fund charging 2 and 20 with a high-water mark, run on the US market's 94 calendar years.
"""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import funding, pit

CACHE = Cache("quant2")
load = CACHE.load


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _utc(ts):
    return datetime.fromtimestamp(float(ts), tz=timezone.utc)


# ---------------------------------------------------------------------------
MAINT = 0.005  # maintenance margin, 0.5% of notional: a typical exchange rule for the smallest BTC tier


def compute_margin() -> dict:
    k = data.binance_klines("BTCUSDT", "1h", "2020-02", "2020-04", market="futures/um")
    f = data.binance_funding("BTCUSDT", "2020-02", "2020-04")
    t0 = datetime(2020, 3, 1, tzinfo=timezone.utc).timestamp()
    t1 = datetime(2020, 3, 20, tzinfo=timezone.utc).timestamp()
    m = (k["time"] >= t0) & (k["time"] <= t1)
    t, p = k["time"][m], k["close"][m]
    # funding settles at 00:00, 08:00 and 16:00 UTC: charge each settlement at the bar that closes after it
    fr = np.zeros(len(t))
    for ft, rate in zip(f["time"], f["rate"]):
        i = np.searchsorted(t, ft)
        if 0 < i < len(t):
            fr[i] += rate
    out = {"t": t, "price": p, "low": k["low"][m], "entry": float(p[0]), "maint": MAINT, "funding": fr}
    runs = {}
    for L in (2, 3, 10):
        acc = funding.margin_account(p, 1.0, float(L), MAINT, funding=fr)
        li = acc["liquidated_at"]
        runs[str(L)] = {"equity": acc["equity"], "req": acc["maintenance_req"], "margin": acc["initial_margin"],
                        "liq_index": -1 if li is None else int(li),
                        "liq_time": None if li is None else float(t[li]),
                        "liq_price_formula": funding.liquidation_price(float(p[0]), float(L), MAINT),
                        "left": acc["left"], "funding_paid": acc["funding_paid"]}
    out["runs"] = _json(runs)
    i_min = int(np.argmin(p))
    out["min_price"], out["min_time"] = float(p[i_min]), float(t[i_min])
    out["fall"] = float(p[i_min] / p[0] - 1)
    d12 = [i for i, x in enumerate(t) if _utc(x).strftime("%Y%m%d") == "20200312"]
    out["day12_open"], out["day12_close"] = float(p[d12[0] - 1]), float(p[d12[-1]])
    return out


# ---------------------------------------------------------------------------
def compute_netting() -> dict:
    rng = np.random.default_rng(21)
    n, trades = 25, 6000
    size = np.exp(rng.normal(0, 1.2, trades)) * 1e6  # dollar values, heavy-tailed
    # a few large members trade more: draw members by a skewed weight
    w = np.exp(rng.normal(0, 0.9, n))
    w /= w.sum()
    a = rng.choice(n, trades, p=w)
    b = rng.choice(n, trades, p=w)
    keep = a != b
    a, b, size = a[keep], b[keep], size[keep]
    res = funding.netting(a, b, size, n)
    return {"n": n, "trades": int(keep.sum()), "gross": res["gross"], "bilateral": res["bilateral"],
            "multilateral": res["multilateral"], "net_position": res["net_position"],
            "saved": 1 - res["multilateral"] / res["gross"]}


# ---------------------------------------------------------------------------
def compute_auction() -> dict:
    rng = np.random.default_rng(22)
    nb = na = 150
    bp = np.round(100 + rng.normal(-0.15, 0.6, nb), 2)
    ap = np.round(100 + rng.normal(0.15, 0.6, na), 2)
    bq = np.round(np.exp(rng.normal(5, 0.8, nb)))
    aq = np.round(np.exp(rng.normal(5, 0.8, na)))
    au = funding.call_auction(bp, bq, ap, aq)
    return {"bid_px": bp, "bid_qty": bq, "ask_px": ap, "ask_qty": aq, "price": au["price"], "volume": au["volume"],
            "candidates": au["candidates"], "demand": au["demand"], "supply": au["supply"],
            "total_bid": float(bq.sum()), "total_ask": float(aq.sum())}


# ---------------------------------------------------------------------------
def compute_funding() -> dict:
    f = data.binance_funding("BTCUSDT", "2020-01", "2020-12")
    k = data.binance_klines("BTCUSDT", "1d", "2020-01", "2020-12", market="futures/um")
    # the cost of holding one coin long: each settlement pays rate x the price at that time
    px = np.interp(f["time"], k["time"], k["close"])
    paid = f["rate"] * px
    return {"time": f["time"], "rate": f["rate"], "annualized": float(f["rate"].mean() * 3 * 365),
            "cum_paid": np.cumsum(paid), "paid_total": float(paid.sum()), "px_start": float(k["close"][0]),
            "px_end": float(k["close"][-1]), "max_rate": float(f["rate"].max()), "min_rate": float(f["rate"].min()),
            "share_positive": float(np.mean(f["rate"] > 0))}


# ---------------------------------------------------------------------------
def compute_repo() -> dict:
    out = {}
    for s in ("SOFR", "DFF", "IOER"):
        x = data.fred(s, "2018-01-01", "2025-12-31")
        m = (x["date"] >= 20190801) & (x["date"] <= 20191031)
        out[s] = {"date": x["date"][m], "value": x["value"][m]}
    r = data.fred("WRESBAL", "2018-01-01", "2025-12-31")
    m = (r["date"] >= 20180101) & (r["date"] <= 20201231)
    out["reserves"] = {"date": r["date"][m], "value": r["value"][m] / 1e6}  # trillions of dollars
    sofr = dict(zip(out["SOFR"]["date"].tolist(), out["SOFR"]["value"].tolist()))
    ioer = dict(zip(out["IOER"]["date"].tolist(), out["IOER"]["value"].tolist()))
    dff = dict(zip(out["DFF"]["date"].tolist(), out["DFF"]["value"].tolist()))
    out["key"] = {str(d): {"sofr": sofr.get(d), "ioer": ioer.get(d), "dff": dff.get(d)}
                  for d in (20190912, 20190913, 20190916, 20190917, 20190918, 20190919)}
    rr = out["reserves"]
    i19 = int(np.argmin(np.where((rr["date"] >= 20190101) & (rr["date"] <= 20191031), rr["value"], 1e9)))
    out["reserves_low"], out["reserves_low_date"] = float(rr["value"][i19]), int(rr["date"][i19])
    j = int(np.argmax(np.where(rr["date"] <= 20190101, rr["value"], -1)))
    out["reserves_2018"] = float(rr["value"][0])
    return {k: (_json(v) if isinstance(v, dict) else v) for k, v in out.items()}


# ---------------------------------------------------------------------------
def compute_fees() -> dict:
    kf = data.ken_french_daily()
    d, simple = pit.research(kf["date"], kf["mkt"])
    years = d // 10000
    ys = np.arange(1927, 2021)
    gross = np.array([np.prod(1 + simple[years == y]) - 1 for y in ys])
    f = funding.fund_fees(gross, mgmt=0.02, perf=0.20)
    wg = np.cumprod(1 + gross)
    wn = np.cumprod(1 + f["net"])
    f1 = funding.fund_fees(gross, mgmt=0.01, perf=0.0)
    return {"years": ys, "gross": gross, "net": f["net"], "fees": f["fees"], "wealth_gross": wg, "wealth_net": wn,
            "final_gross": float(wg[-1]), "final_net": float(wn[-1]), "final_1pct": float(np.prod(1 + f1["net"])),
            "geo_gross": float(wg[-1] ** (1 / len(ys)) - 1), "geo_net": float(wn[-1] ** (1 / len(ys)) - 1),
            "share_kept": float((wn[-1] - 1) / (wg[-1] - 1))}


ITEMS = {"margin": compute_margin, "netting": compute_netting, "auction": compute_auction, "funding": compute_funding,
         "repo": compute_repo, "fees": compute_fees}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
