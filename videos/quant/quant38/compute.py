"""Every number in Part 38 (Market Making, ETFs and the Speed Race), computed and cached in .cache/quant38/.

    python -m videos.quant.quant38.compute [items] [--force]

Data: Binance's public best-quote stream and aggregated trades for the BTCUSDT perpetual (Part 36's grid: 16, 17 and
20 May 2023), and Yahoo Finance's daily bars for HYG and TLT (2020). Models: GLFT quotes, the sniping equilibrium.

* ``fills``    the fill intensity of a quote at a distance from the mid, fitted as A exp(-k delta);
* ``glft``     GLFT's quotes with Bitcoin's fitted A, k and volatility, by risk aversion;
* ``maker``    a two-sided maker replayed on the tape: slow, idealised fast, and fast with an imbalance filter, by day;
* ``deep``     quotes resting several ticks away, filled whenever the tape reaches them: P&L per fill by distance;
* ``bcs``      the sniping equilibrium: the closed form, simulations in continuous trading and in batch auctions, and
               a rough calibration on Bitcoin;
* ``etf``      HYG and TLT through March 2020: prices, volumes and drawdowns.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import lob as L, making as M, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant38")
load = pit.counted(CACHE.load, 38)
DAYS = ("2023-05-16", "2023-05-17", "2023-05-20")
TICK = 0.1


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _book(day):
    return data.binance_book_day("BTCUSDT", day)


def _trades(day):
    return data.binance_aggtrades_day("BTCUSDT", day)


def compute_fills() -> dict:
    deltas = [0.5, 1, 2, 3, 5, 8, 12, 20, 30, 45]
    out = {}
    for d in DAYS[:2]:
        out[d] = M.fill_intensity(_book(d), _trades(d), deltas, horizon=10, tick=TICK)
    P = np.mean([out[d]["P"] for d in out], 0)
    lam = -np.log(1 - P) / out[DAYS[0]]["dt"]
    k, logA = np.polyfit(np.asarray(deltas, float), np.log(lam), 1)
    return _json({"days": out, "deltas": deltas, "P": P, "lam": lam, "A": math.exp(logA), "k": -k})


def compute_glft() -> dict:
    f = load("fills")
    A, k = f["A"], f["k"]
    b = _book(DAYS[1])
    m = L.mid(b) / TICK
    sigma = float(np.std(np.diff(m[::10])))            # ticks per second
    rows = []
    for g in (1e-4, 1e-3, 1e-2, 1e-1):
        q = M.glft(A, k, sigma, g)
        rows.append({"gamma": g, **q})
    return _json({"A": A, "k": k, "sigma": sigma, "rows": rows})


def compute_maker() -> dict:
    variants = {"slow": {}, "fast": {"fast": True}, "fast, filtered": {"fast": True, "filt": 0.2}}
    out = {}
    for d in DAYS:
        b, a = _book(d), _trades(d)
        out[d] = {}
        for name, kw in variants.items():
            r = M.maker_replay(b, a, max_inv=5, tick=TICK, **kw)
            n = r["n_fills"]
            out[d][name] = {"n": n, "half": float(np.mean(r["half_spread"])), "step": float(np.mean(r["move_in_step"])),
                            "mk1": float(np.mean(r["mk10"])), "mk10": float(np.mean(r["mk100"])),
                            "mk60": float(np.mean(r["mk600"])), "pnl_per_fill": r["pnl_final"] / max(n, 1),
                            "inv_sd": float(np.std(r["inv_path"]))}
    tick_bp = TICK / float(np.median(L.mid(_book(DAYS[1])))) * 1e4
    return _json({"days": out, "tick_bp": tick_bp})


def compute_deep() -> dict:
    """Test the Poisson fill assumption: quote at mid +- delta ticks at the start of each second; a buy (sell) reaching
    the ask (bid) fills it. The P&L per fill against the mid 1, 10 and 60 s later, in ticks, by delta (16-17 May)."""
    deltas = [0.5, 2, 5, 10, 20, 30, 45]
    rows = {d: {"n": 0, "pnl1": 0.0, "pnl10": 0.0, "pnl60": 0.0} for d in deltas}
    secs = 0
    for day in DAYS[:2]:
        b, a = _book(day), _trades(day)
        m = L.mid(b) / TICK
        tg = b["time"]
        w = ((a["time"] - tg[0]) // 1000).astype(np.int64)
        nw = len(m) // 10
        ok = (w >= 0) & (w < nw - 61)
        w, tp, sg = w[ok], a["price"][ok] / TICK, a["sign"][ok]
        m0 = m[np.arange(nw) * 10]
        up = np.full(nw, -np.inf)
        dn = np.full(nw, -np.inf)
        np.maximum.at(up, w[sg > 0], tp[sg > 0] - m0[w[sg > 0]])
        np.maximum.at(dn, w[sg < 0], m0[w[sg < 0]] - tp[sg < 0])
        secs += nw
        for d in deltas:
            for side, reach in ((-1, up), (1, dn)):          # we sell at the ask (side -1), buy at the bid (side +1)
                k = np.flatnonzero(reach[: nw - 61] >= d)
                px = m0[k] - side * d
                for h, key in ((1, "pnl1"), (10, "pnl10"), (60, "pnl60")):
                    rows[d][key] += float(np.sum(side * (m0[k + h] - px)))
                rows[d]["n"] += len(k)
    out = [{"delta": d, "fills_per_hour": 3600 * r["n"] / secs, "pnl1": r["pnl1"] / max(r["n"], 1),
            "pnl10": r["pnl10"] / max(r["n"], 1), "pnl60": r["pnl60"] / max(r["n"], 1),
            "per_hour60": 3600 * r["pnl60"] / secs} for d, r in rows.items()]
    return _json({"rows": out})


def compute_bcs() -> dict:
    lam_i, lam_j, J = 1.0, 0.1, 4.0
    s_star = M.bcs_spread(lam_i, lam_j, J)
    grid = np.linspace(0.05, 1.0, 20) * J
    sims = []
    for h in grid:
        r = M.bcs_simulate(float(h), lam_i, lam_j, J, 5, 200000.0, seed=38)
        sims.append({"half": float(h), "lp": r["lp"], "sniper": r["sniper"]})
    byN = []
    for N in (2, 3, 5, 10, 30):
        rr = [M.bcs_simulate(s_star, lam_i, lam_j, J, N, 200000.0, seed=s) for s in range(3)]
        byN.append({"N": N, "lp": float(np.mean([x["lp"] for x in rr])), "sniper": float(np.mean([x["sniper"] for x in rr]))})
    fba = M.bcs_simulate(s_star, lam_i, lam_j, J, 5, 200000.0, seed=38, batch=0.1)
    # a rough calibration on Bitcoin: jumps of 5 ticks or more in 100 ms, taker trades a second
    cal = []
    for d in DAYS[:2]:
        b, a = _book(d), _trades(d)
        m = L.mid(b) / TICK
        dm = np.abs(np.diff(m))
        secs = len(m) / 10
        jumps = dm[dm >= 5]
        cal.append({"day": d, "lam_i": len(a["time"]) / secs, "lam_j": len(jumps) / secs, "J": float(np.mean(jumps))})
    # the general condition with Bitcoin's empirical jump sizes: lam_I h = lam_all E[(|dM| - h)^+], over every 100-ms
    # mid change, solved for h by bisection
    allj, secs_all = [], 0.0
    for d in DAYS[:2]:
        m = L.mid(_book(d)) / TICK
        dm = np.abs(np.diff(m))
        allj.append(dm[dm > 0])
        secs_all += len(m) / 10
    allj = np.concatenate(allj)
    lam_all = len(allj) / secs_all
    lam_i_all = float(np.mean([c["lam_i"] for c in cal]))

    def gap(h):
        return lam_i_all * h - lam_all * float(np.mean(np.maximum(allj - h, 0.0)))
    lo_, hi_ = 0.0, 50.0
    for _ in range(60):
        mid_ = 0.5 * (lo_ + hi_)
        lo_, hi_ = (mid_, hi_) if gap(mid_) < 0 else (lo_, mid_)
    general = 0.5 * (lo_ + hi_)
    # check the general condition by simulation, with jumps drawn from Bitcoin's own moves (rates per second)
    gsims = []
    for h in np.linspace(0.1, 0.6, 11):
        r = M.bcs_simulate_dist(float(h), lam_i_all, lam_all, allj, 5, 200000.0, seed=7)
        gsims.append({"half": float(h), "lp": r["lp"], "sniper": r["sniper"]})
    li = float(np.mean([c["lam_i"] for c in cal]))
    lj = float(np.mean([c["lam_j"] for c in cal]))
    Jb = float(np.mean([c["J"] for c in cal]))
    return _json({"lam_i": lam_i, "lam_j": lam_j, "J": J, "s_star": s_star, "sims": sims, "byN": byN,
                  "fba": fba, "btc": {"days": cal, "lam_i": li, "lam_j": lj, "J": Jb,
                                      "half": M.bcs_spread(li, lj, Jb), "general_half": general,
                                      "lam_all": lam_all, "mean_move": float(allj.mean()), "gsims": gsims}})


def compute_etf() -> dict:
    out = {}
    for sym in ("HYG", "TLT"):
        b = data.yahoo_bars(sym, "2015-01-01", "2020-12-31")
        t = np.asarray(b["date"]) if "date" in b else np.asarray(b["time"])
        c = np.asarray(b["close"], float)
        v = np.asarray(b["volume"], float)
        out[sym] = {"t": [f"{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}" for x in t], "close": c, "volume": v}
    res = {}
    for sym, d in out.items():
        t = d["t"]
        k = [i for i, x in enumerate(t) if "2020-01-02" <= x <= "2020-04-30"]
        c = np.asarray(d["close"])[k]
        v = np.asarray(d["volume"])[k]
        base_v = float(np.median(np.asarray(d["volume"])[[i for i, x in enumerate(t) if "2019-01-01" <= x <= "2019-12-31"]]))
        dd = c / np.maximum.accumulate(c) - 1          # the maximum drawdown in the window: trough after its peak
        trough = int(np.argmin(dd))
        peak = int(np.argmax(c[: trough + 1]))
        res[sym] = {"t": [t[i] for i in k], "close": c, "vol_x": v / base_v, "peak_date": t[k[peak]],
                    "trough_date": t[k[trough]], "drawdown": float(c[trough] / c[peak] - 1),
                    "max_vol_x": float(np.max(v / base_v))}
    return _json(res)


ITEMS = {"fills": compute_fills, "glft": compute_glft, "maker": compute_maker, "deep": compute_deep, "bcs": compute_bcs, "etf": compute_etf}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
