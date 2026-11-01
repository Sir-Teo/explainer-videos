"""The Surface: the series' pricing scoreboard (videos/quant/SYLLABUS.md, "The Surface").

One full Deribit BTC options surface on one fixed day, rebuilt from that day's trades, plus the same surface a day
later for out-of-sample checks.  Every pricing model in the series is calibrated to it and scored on it.

**The day.**  Wednesday 10 December 2025, the day of a Federal Reserve rate decision (the same day as the Nasdaq
ITCH data of the ``trading`` video), and Thursday 11 December for the next-day check.  The snapshot is 08:00 UTC,
Deribit's daily expiry time, built from the trades of 00:00-12:00 UTC (before the Fed's 19:00 UTC announcement).

**From trades to quotes.**
1. Each trade carries the instrument (expiry, strike, call or put), its price and *mark price* in BTC, Deribit's
   implied volatility, and the BTC index price at that moment.
2. Deribit's options are inverse: the price in BTC is the dollar price divided by the underlying forward F, so put-call
   parity reads C - P = 1 - K / F (in BTC).  For each expiry, pairs of call and put trades at one strike within ten
   minutes give F / index; the median over pairs is the expiry's basis (an interest-rate-like premium of the
   futures over the index).  Expiries with no pairs take the basis of a rate fitted across the others.
3. Every trade's mark price, times its forward, is a dollar Black-76 price; inverting it (``bs.implied_vol``) gives
   that moment's implied volatility.  An instrument's quote is the median over its trades in the window.
4. Quotes are out of the money (puts below the forward, calls above), from 1 day to 1.2 years.

``build(day)`` returns the quotes as arrays (``expiry``, ``T``, ``K``, ``F``, ``k`` = ln K/F, ``cp``, ``iv``,
``iv_deribit``, ``vega``, ``n``), the per-expiry ``expiries`` table, and the snapshot's index price.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

import numpy as np

from explainer.quant.house import bs

DAYS = ("2025-12-10", "2025-12-11")
HOURS = range(0, 12)
REF_HOUR = 8
DVOL_RANGE = ("2021-04", "2025-12")
SPOT_RANGE = ("2021-04", "2025-12")
YEAR = 365.0 * 86400
MIN_T, MAX_T = 1.0 / 365, 1.2


def parse_instrument(name: str):
    """'BTC-26JUN26-85000-P' -> (expiry datetime at 08:00 UTC, strike, cp)."""
    _, exp, strike, kind = name.split("-")
    d = datetime.strptime(exp, "%d%b%y").replace(hour=8, tzinfo=timezone.utc)
    return d, float(strike), (1 if kind == "C" else -1)


def _ref_ts(day: str) -> float:
    return datetime.strptime(day, "%Y-%m-%d").replace(hour=REF_HOUR, tzinfo=timezone.utc).timestamp()


def build(day: str) -> dict:
    from explainer.quant.data import deribit_trades

    trades = deribit_trades(day, hours=HOURS)
    ref = _ref_ts(day)
    ts = np.array([t["timestamp"] / 1e3 for t in trades])
    idx = np.array([t["index_price"] for t in trades])
    near = np.abs(ts - ref) < 1800
    S_ref = float(np.median(idx[near]))

    by_inst = defaultdict(list)
    for t, s in zip(trades, ts):
        exp, K, cp = parse_instrument(t["instrument_name"])
        T = (exp.timestamp() - s) / YEAR
        if T <= 0:
            continue
        by_inst[(exp, K, cp)].append((s, t["mark_price"], t["index_price"], t["iv"], T))

    # 2. the forward of each expiry from put-call parity on mark prices
    ratio = {}
    expiries = sorted({e for e, _, _ in by_inst})
    for e in expiries:
        rs = []
        for (e2, K, cp), calls in by_inst.items():
            if e2 != e or cp != 1 or (e, K, -1) not in by_inst:
                continue
            puts = by_inst[(e, K, -1)]
            pt = np.array([p[0] for p in puts])
            for s, cm, ci, _, _ in calls:
                j = int(np.argmin(np.abs(pt - s)))
                if abs(pt[j] - s) > 600 or abs(np.log(K / ci)) > 0.2:
                    continue
                diff = cm - puts[j][1]
                if diff < 1 - 1e-9:
                    rs.append(K / (1 - diff) / (0.5 * (ci + puts[j][2])))
        if len(rs) >= 3:
            ratio[e] = float(np.median(rs))
    T_ref = {e: (e.timestamp() - ref) / YEAR for e in expiries}
    have = [e for e in ratio if T_ref[e] > 2 / 365]
    if have:  # a basis rate b with F / S = exp(b T), the median over expiries that have pairs
        b = float(np.median([np.log(ratio[e]) / T_ref[e] for e in have]))
    else:
        b = 0.0
    for e in expiries:
        ratio.setdefault(e, float(np.exp(b * max(T_ref[e], 0.0))))

    # 3. each trade's implied volatility from its mark price, then the instrument's median
    rows = []
    for (e, K, cp), tr in by_inst.items():
        T0 = T_ref[e]
        if not (MIN_T <= T0 <= MAX_T):
            continue
        F_ref = ratio[e] * S_ref
        if (cp == 1) != (K >= F_ref):  # out of the money only
            continue
        s, mark, ind, ivd, T = (np.array(c, float) for c in zip(*tr))
        F = ratio[e] * ind
        iv = bs.implied_vol(mark * F, F, K, T, 0.0, 0.0, cp)
        ok = np.isfinite(iv) & (iv > 0.05) & (iv < 3.0)
        if not ok.any():
            continue
        sig = float(np.median(iv[ok]))
        vega = float(bs.greeks(F_ref, K, T0, sig, 0.0, 0.0, cp)["vega"]) / F_ref
        rows.append((e.strftime("%Y-%m-%d"), T0, K, F_ref, np.log(K / F_ref), cp, sig, float(np.median(ivd)) / 100,
                     vega, int(ok.sum())))
    rows.sort(key=lambda r: (r[1], r[2]))
    cols = list(zip(*rows))
    out = {
        "day": day, "ref_time": f"{day}T{REF_HOUR:02d}:00Z", "S": S_ref, "basis_rate": b,
        "expiry": list(cols[0]), "T": np.array(cols[1]), "K": np.array(cols[2]), "F": np.array(cols[3]),
        "k": np.array(cols[4]), "cp": np.array(cols[5], int), "iv": np.array(cols[6]),
        "iv_deribit": np.array(cols[7]), "vega": np.array(cols[8]), "n": np.array(cols[9], int),
        "n_trades": len(trades),
    }
    exps = sorted(set(out["expiry"]), key=lambda x: x)
    out["expiries"] = [{"expiry": x, "T": float(out["T"][out["expiry"].index(x)]),
                        "F": float(out["F"][out["expiry"].index(x)]),
                        "n": int(sum(1 for y in out["expiry"] if y == x)),
                        "parity": any(e.strftime("%Y-%m-%d") == x for e in ratio if e in have)} for x in exps]
    return out


def vega_rmse(iv_model, quotes: dict, mask=None) -> float:
    """Vega-weighted RMSE in vol points (1 vol point = 0.01) between a model's implied vols and the quotes."""
    w = quotes["vega"] if mask is None else quotes["vega"][mask]
    e = (np.asarray(iv_model) - (quotes["iv"] if mask is None else quotes["iv"][mask])) * 100
    return float(np.sqrt(np.sum(w * e * e) / np.sum(w)))
