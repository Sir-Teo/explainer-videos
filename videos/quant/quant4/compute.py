"""Every number in Part 4 (Martingales and Measure), computed and cached in .cache/quant4/.

    python -m videos.quant.quant4.compute [items] [--force]

Research window: to December 2020 (the sealed envelope).  Items (seeded; seconds to a minute):

* ``doob``     Doob's decomposition: a biased coin (drift 0.1 a toss); the US market's log wealth 1926-2020 as the
               running sum of each day's drift forecast (the mean so far) plus a martingale; and that martingale's
               square, whose predictable part is the sum of each day's variance forecast (an EWMA known the day
               before);
* ``measure``  a change of measure on a coin: the likelihood-ratio martingale dQ/dP for p = 0.5, q = 0.6, its paths
               under P (mean one, median to zero) and under Q;
* ``ruin``     gambler's ruin on a fair coin, European and American roulette; bold play against timid play (Dubins and
               Savage): the chance of doubling a bankroll;
* ``stable``   stable laws: McCulloch's alpha for the US market by decade and for Bitcoin; alpha against horizon; the
               Mantegna-Stanley probability of return to the origin across time scales;
* ``nikkei``   the Nikkei 225 from July 1994 to March 1995 (FRED), the Kobe earthquake and the fall of Barings;
* ``peeking``  monitoring a fair game: a t-test checked every day rejects far more often than 5%; an e-process
               checked every day does not (Ville's inequality);
* ``eprocess`` testing by betting on real data: does the sign of yesterday's return predict today's?  US market from
               1926, from 1975 and from 2000; Bitcoin from 2018;
* ``envelope`` seals the Nikkei's hold-out and registers the two e-process tests.
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import martingale, pit

CACHE = Cache("quant4")
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


def _market():
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    return d, np.log1p(r)


def _btc_daily():
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    dates = np.array([int(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y%m%d")) for t in b["time"]])
    m = dates <= pit.RESEARCH_END
    return dates[m][1:], np.diff(np.log(b["close"][m]))


def _frac(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100 - 1) / 365


def _ewma_var(r, lam=0.94, warm=60):
    """Each day's variance forecast, made the day before (RiskMetrics): predictable."""
    v = np.empty_like(r)
    v[0] = np.var(r[:warm])
    for t in range(1, len(r)):
        v[t] = lam * v[t - 1] + (1 - lam) * r[t - 1] ** 2
    return v


# ---------------------------------------------------------------------------
def compute_doob() -> dict:
    rng = np.random.default_rng(19)  # a typical path: it ends near its expectation, 40
    n = 400
    steps = np.where(rng.random(n) < 0.55, 1.0, -1.0)
    x = np.concatenate([[0.0], np.cumsum(steps)])
    coin = martingale.doob_decomposition(x, np.full(n, 0.1))
    d, r = _market()
    # the drift each day as known the day before (the running mean), and the variance forecast (EWMA)
    m = np.concatenate([[r[:250].mean()], np.cumsum(r)[:-1] / np.arange(1, len(r))])
    m[:250] = r[:250].mean()
    X = np.concatenate([[0.0], np.cumsum(r)])
    dec1 = martingale.doob_decomposition(X, m)
    e = r - m
    v = _ewma_var(e)
    M = dec1["M"]
    dec2 = martingale.doob_decomposition(M ** 2, v)
    qv = np.concatenate([[0.0], np.cumsum(e ** 2)])
    step = 21
    t = np.concatenate([[_frac(d)[0]], _frac(d)])
    return _json({"coin_x": x, "coin_A": coin["A"], "coin_M": coin["M"],
                  "t": t[::step], "X": X[::step], "A": dec1["A"][::step], "M": M[::step],
                  "M2": (M ** 2)[::step], "A2": dec2["A"][::step], "N2": dec2["M"][::step], "qv": qv[::step],
                  "X_end": float(X[-1]), "A_end": float(dec1["A"][-1]), "M_end": float(M[-1]),
                  "A2_end": float(dec2["A"][-1]), "qv_end": float(qv[-1]), "M2_end": float(M[-1] ** 2),
                  "ratio_A2_qv": float(dec2["A"][-1] / qv[-1])})


# ---------------------------------------------------------------------------
def compute_measure() -> dict:
    rng = np.random.default_rng(11)
    n, k, p, q = 300, 2000, 0.5, 0.6
    under_p = rng.random((k, n)) < p
    under_q = rng.random((k, n)) < q
    Lp = np.array([martingale.likelihood_ratio(h, p, q) for h in under_p])
    Lq = np.array([martingale.likelihood_ratio(h, p, q) for h in under_q])
    show = 40
    return _json({"n": n, "p": p, "q": q, "paths_p": np.log10(Lp[:show]), "paths_q": np.log10(Lq[:show]),
                  "mean_p": Lp.mean(axis=0), "median_p": np.median(Lp, axis=0), "frac_below_001": float(np.mean(Lp[:, -1] < 0.01)),
                  "mean_end_p": float(Lp[:, -1].mean()), "median_end_p": float(np.median(Lp[:, -1])),
                  "frac_q_above_100": float(np.mean(Lq[:, -1] > 100)), "max_end_p": float(Lp[:, -1].max())})


# ---------------------------------------------------------------------------
def compute_ruin() -> dict:
    games = {"fair coin": 0.5, "European roulette": 18 / 37, "American roulette": 18 / 38}
    a = np.arange(0, 101)
    curves = {k: [martingale.gamblers_ruin(int(i), 100, p) if i > 0 else 0.0 for i in a] for k, p in games.items()}
    # the chance of doubling a bankroll of n units with one-unit bets (timid), against one all-in bet (bold)
    units = [1, 2, 5, 10, 20, 50, 100, 500]
    timid = {k: [martingale.gamblers_ruin(u, 2 * u, p) for u in units] for k, p in games.items()}
    bold = {k: p for k, p in games.items()}
    # a check by simulation: 1,000-unit bankroll, timid play on European roulette, until doubled or ruined (n small)
    rng = np.random.default_rng(3)
    sims = []
    for _ in range(4000):
        w = 10
        while 0 < w < 20:
            w += 1 if rng.random() < 18 / 37 else -1
        sims.append(w == 20)
    return _json({"a": a, "curves": curves, "units": units, "timid": timid, "bold": bold,
                  "sim_timid_10": float(np.mean(sims)), "exact_timid_10": martingale.gamblers_ruin(10, 20, 18 / 37)})


# ---------------------------------------------------------------------------
def compute_stable() -> dict:
    d, r = _market()
    years = d // 10000
    dec = {}
    for y0 in range(1930, 2020, 10):
        m = (years >= y0) & (years < y0 + 10)
        dec[str(y0)] = martingale.stable_mcculloch(r[m])["alpha"]
    full = martingale.stable_mcculloch(r)
    db, rb = _btc_daily()
    btc = martingale.stable_mcculloch(rb)
    horizons = [1, 2, 5, 10, 20, 60]
    alpha_h = []
    for h in horizons:
        n = len(r) // h
        s = r[: n * h].reshape(n, h).sum(axis=1)
        alpha_h.append(martingale.stable_mcculloch(s)["alpha"])
    alpha_hb = []
    for h in horizons[:5]:
        n = len(rb) // h
        s = rb[: n * h].reshape(n, h).sum(axis=1)
        alpha_hb.append(martingale.stable_mcculloch(s)["alpha"])
    hz = [1, 2, 4, 8, 16, 32, 64]
    ms = martingale.return_probability(r, hz)
    msb = martingale.return_probability(rb, hz[:5])
    # within one decade with no crash, the same scaling
    m70 = (years >= 1962) & (years < 1987)
    ms70 = martingale.return_probability(r[m70], hz)
    gauss = martingale.return_probability(np.random.default_rng(0).standard_normal(len(r)) * r.std(), hz)
    return _json({"decades": dec, "full": full, "btc": btc, "horizons": horizons, "alpha_h": alpha_h,
                  "horizons_btc": horizons[:5], "alpha_hb": alpha_hb, "ms": ms, "ms_btc": msb, "ms_6286": ms70,
                  "ms_gauss": gauss, "n_us": int(len(r)), "n_btc": int(len(rb))})


# ---------------------------------------------------------------------------
def compute_nikkei() -> dict:
    f = data.fred("NIKKEI225", start="1994-07-01", through="1995-03-31")
    m = np.isfinite(f["value"])
    d, v = f["date"][m], f["value"][m]
    pick = {str(k): float(v[d == k][0]) for k in (19950113, 19950117, 19950120, 19950123, 19950224, 19950227)
            if np.any(d == k)}
    return _json({"date": d, "t": _frac(d), "value": v, "pick": pick, "low_date": int(d[np.argmin(v)]),
                  "low": float(v.min()), "start": float(v[0])})


# ---------------------------------------------------------------------------
def compute_peeking() -> dict:
    """Under the null (fair +-1 increments, i.e. mean zero), check every day for 2,500 days."""
    rng = np.random.default_rng(21)
    n_paths, n = 2000, 2500
    t_reject, e_reject, t_first, e_max = 0, 0, [], []
    show_t, show_e = [], []
    for k in range(n_paths):
        x = rng.choice([-0.5, 0.5], n)
        cs = np.cumsum(x)
        idx = np.arange(1, n + 1)
        z = cs / (0.5 * np.sqrt(idx))
        hit = np.abs(z[19:]) > 1.96
        if hit.any():
            t_reject += 1
        ep = martingale.EProcess()
        hist = ep.run(x)
        e_max.append(hist.max())
        if hist.max() >= 20:
            e_reject += 1
        if k < 30:
            show_t.append(z[::10])
            show_e.append(np.log10(hist[1:][::10]))
    return _json({"n": n, "paths": n_paths, "t_reject": t_reject / n_paths, "e_reject": e_reject / n_paths,
                  "show_z": show_t, "show_loge": show_e, "e_max_median": float(np.median(e_max))})


# ---------------------------------------------------------------------------
def _sign_test(r, cap=0.9, k=4.0):
    """Bet on continuation: x_t = sign(r_{t-1}) * clip((r_t - m_{t-1}) / (k sd_{t-1}), -cap, cap), with the running
    mean m and an EWMA scale sd known the day before.  Under the null that yesterday's sign does not predict today's
    demeaned return, x has conditional mean zero (approximately: the running mean is a forecast, not the truth)."""
    r = np.asarray(r, float)
    m = np.concatenate([[0.0], np.cumsum(r)[:-1] / np.arange(1, len(r))])
    sd = np.sqrt(_ewma_var(r - m))
    x = np.sign(np.concatenate([[0.0], r[:-1]])) * np.clip((r - m) / (k * sd), -cap, cap)
    x[0] = 0.0
    e = martingale.EProcess()
    return e.run(x)


def compute_eprocess() -> dict:
    d, r = _market()
    out = {}
    for start in (19260701, 19750101, 20000101):
        m = d >= start
        h = _sign_test(r[m])
        dd = d[m]
        cross = np.flatnonzero(h[1:] >= 20)
        out[str(start)] = {"t": _frac(dd)[::5], "loge": np.log10(h[1:])[::5], "max": float(h.max()),
                           "end": float(h[-1]), "cross": int(dd[cross[0]]) if len(cross) else None,
                           "rho1": float(np.corrcoef(r[m][1:], r[m][:-1])[0, 1])}
    db, rb = _btc_daily()
    m = db >= 20180101
    hb = _sign_test(rb[m])
    cross = np.flatnonzero(hb[1:] >= 20)
    out["btc"] = {"t": _frac(db[m]), "loge": np.log10(hb[1:]), "max": float(hb.max()), "end": float(hb[-1]),
                  "cross": int(db[m][cross[0]]) if len(cross) else None, "rho1": float(np.corrcoef(rb[m][1:], rb[m][:-1])[0, 1])}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    f = data.fred("NIKKEI225", start="1949-05-01", through="2025-12-31")
    m = np.isfinite(f["value"])
    recs = {"Nikkei 225 (FRED)": pit.seal("fred/NIKKEI225", f["date"][m], f["value"][m])}
    reg = {"sign_continuation_eprocess_us": pit.register("sign_continuation_eprocess_us", inspect.getsource(_sign_test),
                                                         {"data": "Ken French daily market", "starts": [1926, 1975, 2000]},
                                                         trials=3),
           "sign_continuation_eprocess_btc": pit.register("sign_continuation_eprocess_btc", inspect.getsource(_sign_test),
                                                          {"data": "Binance BTCUSDT 1d", "start": 2018}, trials=1)}
    return _json({"sealed": recs, "registered": reg, "trials": pit.trials_so_far()})


ITEMS = {"doob": compute_doob, "measure": compute_measure, "ruin": compute_ruin, "stable": compute_stable,
         "nikkei": compute_nikkei, "peeking": compute_peeking, "eprocess": compute_eprocess, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
