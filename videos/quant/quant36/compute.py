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
* ``edge``       what the linear rule's direction calls are worth: accuracy by move size, and the mid change captured;
* ``qr``         the queue-reactive simulator fitted to the book, and its stylized-fact scorecard against the data;
* ``queue``      a small passive order replayed against the book and the trade tape: fill rates, time to fill and
                 markouts at the back and the front of the queue (adverse selection);
* ``research``   the microprice theorem tested: the spectrum of the fitted B, the geometric decay of B^k G1, the series
                 against the closed form, and the drift of mid, weighted mid and microprice by imbalance on the test days.
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
    hfits = {h: L.horizon_fit(tr, h, n_imb=10, max_spread=2, tick=TICK) for h in (10, 100, 600)}
    sim = _sim_book(36)
    fs = L.microprice_fit(sim, n_imb=10, max_spread=1, tick=TICK)
    rows = []
    for d in TEST:
        b = _book(d)
        mp = L.microprice_apply(b, fit)
        for h, name in ((10, "1 s"), (100, "10 s"), (600, "1 min")):
            hp = L.microprice_apply(b, hfits[h])
            ok = np.isfinite(mp) & np.isfinite(hp)
            mse = {k: L.forecast_mse(b, np.where(ok, e, np.nan), h) for k, e in
                   (("mid", L.mid(b)), ("wmid", L.weighted_mid(b)), ("micro", mp), ("emp", hp))}
            rows.append({"day": d, "h": name, **mse})
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
                  "converged": fit["converged"], "rows": rows, "p_up": p_up, "tick": TICK,
                  "emp": {f"{h / 10:g} s": f_["g"] for h, f_ in hfits.items()}, "g_sim": fs["g"],
                  "move_med": float(np.median(np.abs(np.diff(L.mid(tr)))[np.diff(L.mid(tr)) != 0]) / TICK)})


def _sim_book(seed, n=400000):
    """A long run of the queue-reactive simulator (fitted as in ``qr``) as a book: a large-tick market in which the
    spread is always one tick and the mid moves half a tick when a queue empties."""
    tr = _book(TRAIN[1])
    unit = float(np.median(np.r_[tr["bq"], tr["aq"]]) / 4)
    sim = L.qr_simulate(L.qr_fit(tr, unit=unit, n_q=30), n, seed=seed)
    m = sim["mid"] * TICK / 2
    return {"bid": m - TICK / 2, "ask": m + TICK / 2, "bq": sim["bq"], "aq": sim["aq"]}


def _beta(b, fit, horizons):
    """For each horizon, the slope of the mean mid change by state on the fitted adjustment g (count-weighted, through
    the origin): one when the drift over that horizon has reached the microprice."""
    out = []
    for h in horizons:
        hf = L.horizon_fit(b, h, n_imb=fit["n_imb"], max_spread=fit["max_spread"], tick=fit["tick"])
        c, d, g = hf["count"], hf["g"], np.asarray(fit["g"])
        out.append(float(np.sum(c * d * g) / np.sum(c * g * g)))
    return out


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


def compute_edge() -> dict:
    """What the linear rule's direction calls are worth: accuracy by the size of the next second's move, and the mean
    mid change, in ticks, captured by trading the sign of the forecast whenever it exceeds a threshold (test days)."""
    Xtr, ytr = zip(*[_features(_book(d), horizon=1) for d in TRAIN])
    Xtr, ytr = np.concatenate(Xtr), np.concatenate(ytr)
    Xte, yte = zip(*[_features(_book(d), horizon=1) for d in TEST])
    Xte, yte = np.concatenate(Xte), np.concatenate(yte)
    bl, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(Xtr)), Xtr]), ytr, rcond=None)
    p = np.column_stack([np.ones(len(Xte)), Xte]) @ bl
    by = []
    for lo, hi in ((0.01, 1.6), (1.6, 5.0), (5.0, np.inf)):
        k = (np.abs(yte) >= lo) & (np.abs(yte) < hi)
        by.append({"lo": lo, "hi": float(min(hi, 1e9)), "share": float(k.mean()),
                   "acc": float(np.mean(np.sign(p[k]) == np.sign(yte[k])))})
    trade = []
    for th in (0.5, 1.0, 2.0):
        k = np.abs(p) > th
        trade.append({"th": th, "share": float(k.mean()), "gain": float(np.mean(np.sign(p[k]) * yte[k]))})
    return _json({"zero": float(np.mean(yte == 0)), "by_size": by, "trade": trade, "tick_bp": float(
        TICK / np.median(L.mid(_book(TEST[0]))) * 1e4)})


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


def compute_queue() -> dict:
    after = (10, 100, 600)
    res = {}
    for pos in ("back", "front"):
        parts = []
        for d in TRAIN:
            b = _book(d)
            tr = data.binance_aggtrades_day("BTCUSDT", d)
            for side in ("bid", "ask"):
                parts.append(L.queue_fills(b, tr, side=side, every=300, wait=600, front=pos == "front", after=after,
                                           tick=TICK))
        f = np.concatenate([x["filled"] for x in parts]).astype(bool)
        st = np.concatenate([x["steps"] for x in parts])
        qq = np.concatenate([x["queue"] for x in parts])
        mk = {h: np.concatenate([x["markout"][h] for x in parts]) for h in after}
        ms = np.concatenate([x["missed"] for x in parts])
        edges = np.quantile(qq, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
        by = []
        for a, b_ in zip(edges[:-1], edges[1:]):
            k = (qq >= a) & (qq <= b_)
            by.append({"q": float(np.median(qq[k])), "fill": float(f[k].mean()),
                       "mk10": float(np.nanmean(mk[100][k & f])) if (k & f).any() else float("nan")})
        res[pos] = {"n": int(len(f)), "fill": float(f.mean()), "median_s": float(np.nanmedian(st) / 10),
                    "markout": {f"{h / 10:g} s": float(np.nanmean(mk[h][f])) for h in after},
                    "markout_se": {f"{h / 10:g} s": float(np.nanstd(mk[h][f]) / math.sqrt(max(f.sum(), 1)))
                                   for h in after},
                    "missed": float(np.nanmean(ms[~f])) if (~f).any() else float("nan"), "by_queue": by,
                    "queue_med": float(np.median(qq))}
    return _json(res)


def compute_research() -> dict:
    tr = _cat(TRAIN)
    fit = L.microprice_fit(tr, n_imb=10, max_spread=2, tick=TICK)
    B, g1 = np.asarray(fit["B"]), np.asarray(fit["g1"])
    ev = np.sort(np.abs(np.linalg.eigvals(B)))[::-1]
    # stationary law of B, and the closed form (1 - B + 1 pi')^{-1} g1
    w, V = np.linalg.eig(B.T)
    pi = np.real(V[:, np.argmin(np.abs(w - 1))])
    pi = pi / pi.sum()
    K = len(g1)
    closed = np.linalg.solve(np.eye(K) - B + np.outer(np.ones(K), pi), g1)
    norms, gk = [], g1.copy()
    for k in range(41):
        norms.append(float(np.max(np.abs(gk))))
        gk = B @ gk
    drift = {}
    te = _cat(TEST)
    S = np.rint((te["ask"] - te["bid"]) / TICK)
    I = L.imbalance(te)
    ests = {"mid": L.mid(te), "weighted": L.weighted_mid(te), "micro": L.microprice_apply(te, fit)}
    bins = np.minimum((I * 10).astype(int), 9)
    for h, name in ((1, "100 ms"), (10, "1 s")):
        ok = (S[:-h] == 1) & np.isfinite(ests["micro"][:-h]) & np.isfinite(ests["micro"][h:])
        drift[name] = {}
        for k_, e in ests.items():
            dd = (e[h:] - e[:-h]) / TICK
            drift[name][k_] = {"mean": [float(np.mean(dd[ok & (bins[:-h] == j)])) for j in range(10)],
                               "se": [float(np.std(dd[ok & (bins[:-h] == j)]) / math.sqrt(max(1, np.sum(ok & (bins[:-h]
                                      == j))))) for j in range(10)]}
            x = (I[:-h][ok] - 0.5)
            drift[name][k_]["slope"] = float(np.polyfit(x, dd[ok], 1)[0])
    # where the hypotheses hold: the simulator, fitted on one run and tested on another
    sa, sb = _sim_book(1), _sim_book(2)
    fs = L.microprice_fit(sa, n_imb=10, max_spread=1, tick=TICK)
    Is = L.imbalance(sb)
    bs = np.minimum((Is * 10).astype(int), 9)
    sim_drift = {}
    for k_, e in (("mid", L.mid(sb)), ("weighted", L.weighted_mid(sb)), ("micro", L.microprice_apply(sb, fs))):
        dd = (e[10:] - e[:-10]) / TICK
        sim_drift[k_] = [float(np.mean(dd[bs[:-10] == j])) for j in range(10)]
    def markov_gap(bk):
        """H1's testable consequence: given the state just after a mid change, the sign of the next change should not
        depend on the sign of the last. The count-weighted mean, over post-move states, of
        E[next sign | last up, state] - E[next sign | last down, state]."""
        mm = L.mid(bk)
        Sx = np.rint((bk["ask"] - bk["bid"]) / TICK).astype(int)
        ib = np.minimum((L.imbalance(bk) * 10).astype(int), 9)
        stx = (np.clip(Sx, 1, 2) - 1) * 10 + ib
        mv = np.flatnonzero(np.diff(mm) != 0)
        sg = np.sign(np.diff(mm)[mv])
        post = stx[mv + 1]
        last, nxt, st_ = sg[:-1], sg[1:], post[:-1]
        tot, wsum = 0.0, 0.0
        for x in np.unique(st_):
            k = st_ == x
            up, dn = k & (last > 0), k & (last < 0)
            if up.sum() > 20 and dn.sum() > 20:
                w = float(k.sum())
                tot += w * (nxt[up].mean() - nxt[dn].mean())
                wsum += w
        return float(tot / wsum), int(len(mv))
    mg_btc, n_btc = markov_gap(te)
    mg_sim, n_sim = markov_gap(sb)
    # H2 dropped: the unmirrored fit has a drift at every move, and the partial sums grow without bound
    fa = L.microprice_fit(tr, n_imb=10, max_spread=2, tick=TICK, symmetric=False)
    Ba, ga = np.asarray(fa["B"]), np.asarray(fa["g1"])
    wa, Va = np.linalg.eig(Ba.T)
    pa = np.real(Va[:, np.argmin(np.abs(wa - 1))])
    pa = pa / pa.sum()
    part, acc_, gk_ = [], np.zeros_like(ga), ga.copy()
    for k in range(400):
        acc_ = acc_ + gk_
        gk_ = Ba @ gk_
        if k + 1 in (10, 100, 400):
            part.append(float(np.mean(acc_) / TICK))
    hs_sim = [1, 3, 10, 30, 100, 300, 1000]
    hs_btc = [1, 3, 10, 30, 100, 300, 600, 1800]
    betas = [_beta(sb if k == 2 else _sim_book(k), fs, hs_sim) for k in (2, 3, 4, 5)]
    ev_s = np.sort(np.abs(np.linalg.eigvals(np.asarray(fs["B"]))))[::-1]
    return _json({"eig": ev[:5], "pi_g1": float(pi @ g1), "closed_vs_series": float(np.max(np.abs(closed - fit["g"]))),
                  "norms": norms, "drift": drift, "g_max": float(np.max(np.abs(fit["g"]))),
                  "sim": {"g": fs["g"][:10], "eig2": float(ev_s[1]), "drift": sim_drift, "h": hs_sim,
                          "beta_runs": betas, "beta": np.mean(betas, 0)},
                  "btc": {"h": hs_btc, "beta": _beta(te, fit, hs_btc)},
                  "markov": {"btc": mg_btc, "n_btc": n_btc, "sim": mg_sim, "n_sim": n_sim},
                  "asym": {"pi_g1_ticks": float(pa @ ga / TICK), "partial": part, "n": [10, 100, 400]}})


ITEMS = {"book": compute_book, "micro": compute_micro, "ofi": compute_ofi, "memory": compute_memory,
         "deep": compute_deep, "qr": compute_qr, "queue": compute_queue, "edge": compute_edge,
         "research": compute_research}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
