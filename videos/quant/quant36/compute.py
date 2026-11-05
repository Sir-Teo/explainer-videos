"""Every number in Part 36 (The Limit Order Book), computed and cached in .cache/quant36/.

    python -m videos.quant.quant36.compute [items] [--force]

The data are Binance's public best-bid/best-offer stream and aggregated trades for the BTCUSDT perpetual, reduced to a
100-millisecond grid: 16 and 17 May 2023 to fit (the stream's first days in the archive, partly covered), 20 and 21 May
(a weekend) to test.

* ``book``       what the best quotes look like: spread, depth, update rates through the day;
* ``micro``      Stoikov's microprice fitted on the training days, and its forecasts on the test days against the mid
                 and the size-weighted mid;
* ``ofi``        Cont-Kukanov-Stoikov order-flow imbalance against mid changes, and the impact coefficient against depth;
* ``memory``     trade-sign autocorrelation (Lillo-Farmer), a Hawkes fit to trade arrivals, and the signature plot;
* ``deep``       a small network on recent book states against linear rules, in and out of sample;
* ``qr``         the queue-reactive simulator fitted to the book, and its stylized-fact scorecard against the data.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import lob as L, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant36")
load = pit.counted(CACHE.load, 36)
TRAIN = ("2023-05-16", "2023-05-17")
TEST = ("2023-05-20", "2023-05-21")
TICK = 0.1


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _book(day):
    return data.binance_book_day("BTCUSDT", day)


def _cat(days):
    bs = [_book(d) for d in days]
    return {k: np.concatenate([b[k] for b in bs]) for k in bs[0]}


def compute_book() -> dict:
    out = {}
    for d in TRAIN + TEST:
        b = _book(d)
        S = np.rint((b["ask"] - b["bid"]) / TICK)
        hrs = ((b["time"] // 3600000) % 24).astype(int)
        out[d] = {"n": int(len(b["time"])), "hours": float(len(b["time"]) / 36000), "one_tick": float(np.mean(S == 1)),
                  "bq_med": float(np.median(b["bq"])), "aq_med": float(np.median(b["aq"])),
                  "updates_per_s": float(np.mean(b["updates"]) * 10),
                  "by_hour": [float(np.mean(b["updates"][hrs == h]) * 10) if np.any(hrs == h) else float("nan")
                              for h in range(24)],
                  "price": float(np.median(L.mid(b)))}
    b = _book(TRAIN[1])
    i0 = 36000 * 6
    seg = slice(i0, i0 + 600)                          # one minute at 100 ms
    return _json({"days": out, "seg": {"bid": b["bid"][seg], "ask": b["ask"][seg], "bq": b["bq"][seg],
                                        "aq": b["aq"][seg]},
                  "imb_hist": np.histogram(L.imbalance(b), bins=20, range=(0, 1), density=True)[0]})


def compute_micro() -> dict:
    tr = _cat(TRAIN)
    fit = L.microprice_fit(tr, n_imb=10, max_spread=2, tick=TICK)
    rows = []
    for d in TEST:
        b = _book(d)
        mp = L.microprice_apply(b, fit)
        for h, name in ((10, "1 s"), (100, "10 s"), (600, "1 min")):
            rows.append({"day": d, "h": name, "mid": L.forecast_mse(b, L.mid(b), h),
                         "wmid": L.forecast_mse(b, L.weighted_mid(b), h), "micro": L.forecast_mse(b, mp, h)})
    # the probability that the next mid move is up, by imbalance bucket (test days)
    te = _cat(TEST)
    m = L.mid(te)
    I = L.imbalance(te)
    nxt = np.full(len(m), np.nan)
    j = len(m) - 1
    last = np.nan
    for i in range(len(m) - 1, -1, -1):          # sign of the next change of the mid
        if i < len(m) - 1 and m[i + 1] != m[i]:
            last = np.sign(m[i + 1] - m[i])
        nxt[i] = last
    ok = np.isfinite(nxt)
    bins = np.minimum((I * 10).astype(int), 9)
    p_up = [float(np.mean(nxt[ok & (bins == k)] > 0)) for k in range(10)]
    return _json({"g": fit["g"], "g1": fit["g1"], "centers": fit["centers"], "count": fit["count"],
                  "converged": fit["converged"], "rows": rows, "p_up": p_up, "tick": TICK})


def compute_ofi() -> dict:
    out = {}
    for n, name in ((10, "1 s"), (100, "10 s"), (600, "1 min")):
        rows = []
        for d in TRAIN + TEST:
            b = _book(d)
            e = L.aggregate(L.ofi(b), n)
            m = L.aggregate(L.mid(b), n, "last")
            dm = np.r_[np.nan, np.diff(m)]
            ok = np.isfinite(dm)
            X = np.column_stack([np.ones(ok.sum()), e[ok]])
            beta, *_ = np.linalg.lstsq(X, dm[ok], rcond=None)
            res = dm[ok] - X @ beta
            rows.append({"day": d, "beta": float(beta[1]), "r2": float(1 - res.var() / dm[ok].var())})
        out[name] = rows
    # impact against depth: 10-second regressions in each half hour, against the half hour's mean depth
    b = _cat(TRAIN + TEST)
    e = L.aggregate(L.ofi(b), 100)
    m = L.aggregate(L.mid(b), 100, "last")
    dep = L.aggregate((b["bq"] + b["aq"]) / 2, 100, "last")
    dm = np.r_[np.nan, np.diff(m)]
    pts = []
    for s in range(1, len(e) - 180, 180):
        sl = slice(s, s + 180)
        x, y = e[sl], dm[sl]
        if np.std(x) == 0:
            continue
        bb = float(np.cov(x, y)[0, 1] / np.var(x))
        pts.append({"depth": float(np.mean(dep[sl])), "beta": bb})
    dd = np.log([p["depth"] for p in pts])
    bb = np.log(np.maximum([p["beta"] for p in pts], 1e-9))
    slope = float(np.polyfit(dd, bb, 1)[0])
    # an example minute of OFI and mid changes, at 1 s
    bx = _book(TRAIN[1])
    i0 = 36000 * 6
    ex = {"ofi": L.aggregate(L.ofi(bx), 10)[i0 // 10: i0 // 10 + 120],
          "dmid": np.diff(L.aggregate(L.mid(bx), 10, "last")[i0 // 10 - 1: i0 // 10 + 120])}
    return _json({"fits": out, "depth_pts": pts, "depth_slope": slope, "example": ex})


def compute_memory() -> dict:
    from explainer.quant.house import sim
    a = data.binance_aggtrades_day("BTCUSDT", TRAIN[1])
    lags = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
    acf = L.sign_acf(a["sign"], lags)
    ok = (acf > 0) & (np.asarray(lags) >= 10)
    gam = float(-np.polyfit(np.log(np.asarray(lags)[ok]), np.log(acf[ok]), 1)[0])
    # Hawkes on one hour of trade arrivals (seconds)
    t = a["time"] / 1000.0
    h0 = t[0] + 6 * 3600
    ev = t[(t >= h0) & (t < h0 + 3600)] - h0
    ev = np.unique(np.round(ev, 3))
    fit = sim.hawkes_fit(ev, 3600.0, x0=[len(ev) / 3600 * 0.2, 5.0, 6.0])
    comp = sim.hawkes_compensator(ev, fit["mu"], fit["alpha"], fit["beta"])
    gaps = np.diff(comp)
    from scipy import stats
    ks = float(stats.kstest(gaps, "expon").statistic)
    ks_p = float(stats.kstest(np.diff(ev) * len(ev) / 3600, "expon").statistic)
    b = _book(TRAIN[1])
    steps = [1, 2, 5, 10, 20, 50, 100, 200, 600]
    sig = L.signature(L.mid(b), steps)
    return _json({"lags": lags, "acf": acf, "gamma": gam, "hawkes": fit, "ks": ks, "ks_poisson": ks_p,
                  "n_events": int(len(ev)), "steps": steps, "signature": sig})


def _features(b, n_lag=10, step=10, horizon=10):
    """Features every second: the last ``n_lag`` one-second OFIs, mid changes and imbalances, and the spread; target:
    the mid change over the next ``horizon`` steps of a second."""
    e = L.aggregate(L.ofi(b), step)
    m = L.aggregate(L.mid(b), step, "last")
    I = L.aggregate(L.imbalance(b), step, "last")
    depth = L.aggregate((b["bq"] + b["aq"]) / 2, step, "last")
    dm = np.r_[0.0, np.diff(m)]
    X, y = [], []
    for t in range(n_lag, len(m) - horizon):
        X.append(np.r_[e[t - n_lag + 1:t + 1] / np.maximum(depth[t], 1e-9), dm[t - n_lag + 1:t + 1] / TICK,
                       I[t - n_lag + 1:t + 1] - 0.5])
        y.append((m[t + horizon] - m[t]) / TICK)
    return np.asarray(X, np.float32), np.asarray(y, np.float32)


def compute_deep() -> dict:
    from explainer.quant.house import ml
    out = {}
    for horizon, name in ((1, "1 s"), (10, "10 s")):
        Xtr, ytr = zip(*[_features(_book(d), horizon=horizon) for d in TRAIN])
        Xtr, ytr = np.concatenate(Xtr), np.concatenate(ytr)
        Xte, yte = zip(*[_features(_book(d), horizon=horizon) for d in TEST])
        Xte, yte = np.concatenate(Xte), np.concatenate(yte)
        n = len(Xtr)
        va = slice(int(0.8 * n), n)
        tr = slice(0, int(0.8 * n))

        def r2(p, y):
            return float(1 - np.mean((y - p) ** 2) / np.var(y))

        def acc(p, y):
            k = y != 0
            return float(np.mean(np.sign(p[k]) == np.sign(y[k])))
        # linear: imbalance now; and OFI + imbalance lags
        cols_i = [29]
        A = np.column_stack([np.ones(n), Xtr[:, cols_i]])
        bi, *_ = np.linalg.lstsq(A, ytr, rcond=None)
        p_tr_i = A @ bi
        p_te_i = np.column_stack([np.ones(len(Xte)), Xte[:, cols_i]]) @ bi
        A2 = np.column_stack([np.ones(n), Xtr])
        bl, *_ = np.linalg.lstsq(A2, ytr, rcond=None)
        p_tr_l = A2 @ bl
        p_te_l = np.column_stack([np.ones(len(Xte)), Xte]) @ bl
        net = ml.MLPEnsemble(hidden=(64, 32), seeds=(0, 1, 2), epochs=20, lr=1e-3, l1=1e-6, batch=1024)
        net.fit(Xtr[tr], ytr[tr], Xtr[va], ytr[va])
        p_tr_n = net.predict(Xtr)
        p_te_n = net.predict(Xte)
        out[name] = {k: {"train_r2": r2(a, ytr), "test_r2": r2(b_, yte), "train_acc": acc(a, ytr), "test_acc": acc(b_, yte)}
                     for k, a, b_ in (("imbalance", p_tr_i, p_te_i), ("linear", p_tr_l, p_te_l), ("network", p_tr_n, p_te_n))}
        out[name]["n_train"], out[name]["n_test"] = int(n), int(len(Xte))
    return _json(out)


def compute_qr() -> dict:
    tr = _book(TRAIN[1])
    unit = float(np.median(np.r_[tr["bq"], tr["aq"]]) / 4)
    fit = L.qr_fit(tr, unit=unit, n_q=30)
    sim = L.qr_simulate(fit, len(tr["time"]), seed=36)
    te = _book(TEST[0])

    def facts(bq, aq, m, unit_):
        I = bq / np.maximum(bq + aq, 1e-12)
        dm = np.diff(m)
        moves = np.flatnonzero(dm != 0)
        gaps = np.diff(moves) * 0.1
        mv = np.sign(dm[moves])
        ac1 = float(np.corrcoef(mv[1:], mv[:-1])[0, 1]) if len(mv) > 10 else float("nan")
        r10 = np.diff(m[::100])
        k = float(np.mean((r10 - r10.mean()) ** 4) / np.var(r10) ** 2) if np.var(r10) > 0 else float("nan")
        return {"imb_hist": np.histogram(I, bins=10, range=(0, 1), density=True)[0], "moves_per_min": float(len(moves) /
                (len(m) / 600)), "gap_cv": float(np.std(gaps) / np.mean(gaps)), "move_ac1": ac1, "kurt_10s": k,
                "queue_med": float(np.median(np.r_[bq, aq]) / unit_)}
    data_tr = facts(tr["bq"], tr["aq"], L.mid(tr) / (TICK / 2), unit)
    data_te = facts(te["bq"], te["aq"], L.mid(te) / (TICK / 2), unit)
    model = facts(sim["bq"] * unit, sim["aq"] * unit, sim["mid"], unit)
    return _json({"unit": unit, "p_up": fit["p_up"], "p_dn": fit["p_dn"], "refill": fit["refill"],
                  "occupancy": fit["occupancy"], "data_train": data_tr, "data_test": data_te, "model": model,
                  "sim_mid": sim["mid"][:36000:10], "sim_bq": sim["bq"][:6000:10]})


ITEMS = {"book": compute_book, "micro": compute_micro, "ofi": compute_ofi, "memory": compute_memory,
         "deep": compute_deep, "qr": compute_qr}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
