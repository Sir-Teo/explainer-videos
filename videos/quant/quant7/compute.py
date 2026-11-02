"""Every number in Part 7 (Time Series and Volatility), computed and cached in .cache/quant7/.

    python -m videos.quant.quant7.compute [items] [--force]

Research window: to December 2020.  Items (seeded; seconds to a few minutes on a CPU):

* ``spurious``  Granger and Newbold (1974): independent random walks regressed on each other, in levels and in
                differences; Bitcoin's price against the US stock index, 2017-2020;
* ``coint``     Bitcoin spot against its perpetual future (Binance, daily, 2020): Engle-Granger, the basis's half-life;
* ``regimes``   Hamilton's two-regime model on US monthly market returns, 1926-2020;
* ``garch``     GARCH(1,1), GJR and EGARCH by maximum likelihood on daily US returns 1926-2020 and on Bitcoin;
* ``dcc``       the stock-bond correlation by DCC: the US market against a bond return built from FRED's 10-year yield,
                1962-2020;
* ``realized``  Bitcoin's daily realized measures from one-minute prices (Aug 2017 - Dec 2020): RV at 5 minutes,
                bipower, realized quarticity, two-scale RV, realized kernel; the Kalman-filtered log volatility;
* ``har``       HAR and HARQ on Bitcoin's realized variance, 2017-2019, with Newey-West t-statistics; the cascade of the
                daily, weekly and monthly averages in 2019;
* ``race``      next-day realized variance forecasts for Bitcoin, 2020 (trained on 2017-2019): EWMA, GARCH, GJR,
                HAR-RV, HARQ, log-HAR (added after the first results), an LSTM and a small transformer (5 seeds each), scored by QLIKE and MSE with
                Diebold-Mariano tests; and every model's forecast for 12 March 2020;
* ``scaling``   square-root-of-time: GARCH's term structure of volatility against sqrt(T), on 13 March 2020;
* ``envelope``  registers the forecasting race (trial counter).
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, vol

CACHE = Cache("quant7")
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


def _ymd(ts):
    return np.array([int(datetime.fromtimestamp(x, tz=timezone.utc).strftime("%Y%m%d")) for x in ts])


def _frac(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100 - 1) / 365


def _market():
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    return d, np.log1p(r)


def _btc_daily():
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    d = _ymd(b["time"])
    m = d <= pit.RESEARCH_END
    return d[m], np.asarray(b["close"], float)[m]


# ---------------------------------------------------------------------------
def compute_spurious() -> dict:
    rng = np.random.default_rng(1)
    T, n = 500, 2000
    from explainer.quant.house import econ
    lev_rej, dif_rej, r2 = 0, 0, []
    for _ in range(n):
        a = np.cumsum(rng.standard_normal(T))
        b = np.cumsum(rng.standard_normal(T))
        rl = econ.ols(a, b)
        rd = econ.ols(np.diff(a), np.diff(b))
        lev_rej += abs(rl["t"][1]) > 1.96
        dif_rej += abs(rd["t"][1]) > 1.96
        r2.append(rl["r2"])
    # a real pair: Bitcoin against the US stock index, daily 2017-08 to 2020 (common dates)
    db, cb = _btc_daily()
    dm, rm = _market()
    idx = np.cumsum(rm)
    common = np.intersect1d(db, dm)
    lb = np.log(cb[np.searchsorted(db, common)])
    lm = idx[np.searchsorted(dm, common)]
    lv = econ.ols(lb, lm)
    df = econ.ols(np.diff(lb), np.diff(lm))
    return _json({"rej_levels": lev_rej / n, "rej_diffs": dif_rej / n, "r2": np.array(r2), "median_r2": float(np.median(r2)),
                  "btc_levels": {"t": float(lv["t"][1]), "r2": lv["r2"], "beta": float(lv["beta"][1])},
                  "btc_diffs": {"t": float(df["t"][1]), "r2": df["r2"], "beta": float(df["beta"][1])},
                  "t": _frac(common), "lb": lb, "lm": lm})


# ---------------------------------------------------------------------------
def compute_coint() -> dict:
    s = data.binance_klines("BTCUSDT", "1d", "2020-01", "2020-12")
    f = data.binance_klines("BTCUSDT", "1d", "2020-01", "2020-12", market="futures/um")
    ds, df_ = _ymd(s["time"]), _ymd(f["time"])
    common = np.intersect1d(ds, df_)
    ls = np.log(np.asarray(s["close"], float)[np.searchsorted(ds, common)])
    lf = np.log(np.asarray(f["close"], float)[np.searchsorted(df_, common)])
    eg = vol.engle_granger(lf, ls)
    basis = lf - ls
    ar = vol.ar_fit(basis, 1)
    rho = float(ar["beta"][1])
    a_s, a_f = vol.adf(ls), vol.adf(lf)
    # a pair that is not cointegrated: Bitcoin against an independent random walk with the same volatility
    rng = np.random.default_rng(3)
    fake = ls[0] + np.cumsum(rng.standard_normal(len(ls)) * np.std(np.diff(ls)))
    eg_fake = vol.engle_granger(fake, ls)
    return _json({"t": _frac(common), "ls": ls, "lf": lf, "basis_bp": 1e4 * basis, "eg_t": eg["t"],
                  "coint": eg["cointegrated_5pct"], "adf_spot_t": a_s["t"], "adf_fut_t": a_f["t"], "rho": rho,
                  "half_life_days": float(np.log(0.5) / np.log(rho)), "basis_mean_bp": float(1e4 * basis.mean()),
                  "basis_sd_bp": float(1e4 * basis.std()), "fake_t": eg_fake["t"]})


# ---------------------------------------------------------------------------
def compute_regimes() -> dict:
    ff = data.ken_french_factors_monthly()
    x = ff["mkt_rf"]
    ms = vol.markov_switching(x, n_iter=300)
    d = ff["date"]
    t = d // 100 + (d % 100 - 0.5) / 12
    return _json({"t": t, "x": x, "prob_high": ms["prob_high"], "mu": ms["mu"] * 12, "sd": ms["sd"] * np.sqrt(12),
                  "P": ms["P"], "duration_months": ms["duration"], "share_high": float(np.mean(ms["prob_high"] > 0.5))})


# ---------------------------------------------------------------------------
def compute_garch() -> dict:
    d, r = _market()
    x = r - r.mean()
    out = {}
    for kind in ("garch", "gjr", "egarch"):
        f = vol.garch_fit(x, kind)
        out[kind] = {"params": f["params"], "loglik": f["loglik"], "persistence": f["persistence"],
                     "half_life": f["half_life"]}
    g = vol.garch_fit(x, "garch")
    step = 5
    db, cb = _btc_daily()
    rb = np.diff(np.log(cb))
    xb = rb - rb.mean()
    gb = vol.garch_fit(xb)
    jb = vol.garch_fit(xb, "gjr")
    return _json({"us": out, "t": _frac(d)[::step], "vol_ann": np.sqrt(g["h"] * 252)[::step],
                  "absr_ann": (np.abs(x) * np.sqrt(252))[::step], "n": int(len(x)),
                  "btc": {"garch": gb["params"], "persistence": gb["persistence"], "half_life": gb["half_life"],
                          "gjr_gamma": float(jb["params"][2]), "loglik_garch": gb["loglik"], "loglik_gjr": jb["loglik"]}})


# ---------------------------------------------------------------------------
def compute_dcc() -> dict:
    y = data.fred("DGS10", start="1962-01-02")
    dy, yv = pit.research(y["date"], y["value"])
    dm, rm = _market()
    common = np.intersect1d(dy, dm)
    yy = yv[np.searchsorted(dy, common)] / 100
    # a constant-maturity 10-year bond's daily return, approximately: carry minus duration times the yield change
    dur = 8.0
    rb = yy[:-1] / 252 - dur * np.diff(yy)
    rs = rm[np.searchsorted(dm, common)][1:]
    d = common[1:]
    res = vol.dcc_fit(rs - rs.mean(), rb - rb.mean())
    t = _frac(d)
    yrs = d // 10000
    by_decade = {str(y0): float(np.corrcoef(rs[(yrs >= y0) & (yrs < y0 + 10)], rb[(yrs >= y0) & (yrs < y0 + 10)])[0, 1])
                 for y0 in (1962, 1970, 1980, 1990, 2000, 2010)}
    step = 5
    return _json({"t": t[::step], "rho": res["rho"][::step], "a": res["a"], "b": res["b"], "by_decade": by_decade})


# ---------------------------------------------------------------------------
def _btc_realized():
    t, c = (np.asarray(v, float) for v in (lambda b: (b["time"], b["close"]))(data.binance_klines("BTCUSDT", "1m",
                                                                                                    "2017-08", "2020-12")))
    day = (t // 86400).astype(int)
    lc = np.log(c)
    days = np.unique(day)
    rows = []
    for dd in days:
        x = lc[day == dd]
        if len(x) < 1200:
            continue
        r5 = np.diff(x[::5])
        rows.append((dd, vol.realized_variance(r5), vol.bipower_variation(r5), np.sum(r5 ** 4) * len(r5) / 3,
                     vol.two_scale_rv(x, 5), vol.realized_kernel(np.diff(x), 10), vol.realized_variance(np.diff(x))))
    a = np.array(rows)
    return a


def compute_realized() -> dict:
    a = _btc_realized()
    dd = a[:, 0].astype(int)
    ymd = np.array([int(datetime.fromtimestamp(x * 86400, tz=timezone.utc).strftime("%Y%m%d")) for x in dd])
    rv, bv, rq, ts, rk, rv1 = (a[:, k] for k in range(1, 7))
    lv = 0.5 * np.log(rv)
    k = vol.kalman_local_level(lv)
    jump_share = float(np.sum(np.maximum(rv - bv, 0)) / np.sum(rv))
    ann = lambda v: float(np.sqrt(np.mean(v) * 365))  # noqa: E731
    return _json({"ymd": ymd, "t": _frac(ymd), "rv": rv, "bv": bv, "rq": rq, "tsrv": ts, "rk": rk, "rv1": rv1,
                  "kalman": k["level"], "kalman_snr": k["signal_to_noise"], "jump_share": jump_share,
                  "vol_rv5": ann(rv), "vol_rv1": ann(rv1), "vol_tsrv": ann(ts), "vol_rk": ann(rk), "vol_bv": ann(bv),
                  "n_days": int(len(rv))})


def compute_har() -> dict:
    from explainer.quant.house import econ
    rz = load("realized")
    ymd, rv, rq = (np.asarray(rz[k]) for k in ("ymd", "rv", "rq"))
    end = int(np.searchsorted(ymd, 20200101))
    out = {}
    for name, q in (("HAR", None), ("HARQ", rq[:end])):
        X, y = vol._har_design(rv[:end], q)
        ok = np.all(np.isfinite(X), axis=1) & np.isfinite(y)
        X, y = X[ok], y[ok]
        f = econ.ols(y, X, se="nw", lags=5)
        out[name] = {"beta": f["beta"], "t": f["t"], "r2": f["r2"], "n": f["n"]}
    w = (ymd >= 20190101) & (ymd <= 20191231)
    ann = lambda v: np.sqrt(np.asarray(v) * 365)  # noqa: E731
    week = np.convolve(rv, np.ones(5) / 5)[:len(rv)]
    month = np.convolve(rv, np.ones(22) / 22)[:len(rv)]
    return _json({**out, "cascade_t": np.asarray(rz["t"])[w], "cascade_d": ann(rv[w]), "cascade_w": ann(week[w]),
                  "cascade_m": ann(month[w])})


# ---------------------------------------------------------------------------
def _nn_forecasts(lrv, train_end, val_end, kind, seed, lookback=22, epochs=300):
    """Train a small LSTM or transformer to predict tomorrow's log RV from the past ``lookback`` days."""
    import torch

    torch.set_num_threads(1)  # tiny models: more threads only contend with the renders (40x slower measured)
    torch.manual_seed(seed)
    np.random.seed(seed)
    mu, sd = lrv[:train_end].mean(), lrv[:train_end].std()
    z = (lrv - mu) / sd
    X = np.stack([z[i - lookback:i] for i in range(lookback, len(z))])[:, :, None]
    y = z[lookback:]
    tr = slice(0, train_end - lookback)
    va = slice(train_end - lookback, val_end - lookback)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32)

    class LSTM(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.rnn = torch.nn.LSTM(1, 16, batch_first=True)
            self.out = torch.nn.Linear(16, 1)

        def forward(self, x):
            h, _ = self.rnn(x)
            return self.out(h[:, -1]).squeeze(-1)

    class Tiny(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.inp = torch.nn.Linear(1, 16)
            self.pos = torch.nn.Parameter(torch.zeros(1, lookback, 16))
            layer = torch.nn.TransformerEncoderLayer(16, 2, 32, dropout=0.1, batch_first=True)
            self.enc = torch.nn.TransformerEncoder(layer, 1)
            self.out = torch.nn.Linear(16, 1)

        def forward(self, x):
            h = self.enc(self.inp(x) + self.pos)
            return self.out(h[:, -1]).squeeze(-1)

    model = LSTM() if kind == "lstm" else Tiny()
    opt = torch.optim.Adam(model.parameters(), lr=3e-3, weight_decay=1e-4)
    best, best_state, bad = 1e9, None, 0
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(tr.stop)
        for i in range(0, tr.stop, 64):
            idx = perm[i:i + 64]
            opt.zero_grad()
            loss = torch.mean((model(Xt[idx]) - yt[idx]) ** 2)
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            vl = float(torch.mean((model(Xt[va]) - yt[va]) ** 2))
        if vl < best - 1e-5:
            best, bad = vl, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad > 30:
                break
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred = model(Xt).numpy()
        resid_var = float(np.var(pred[va] - y[va]))
    lpred = pred * sd + mu
    # log-normal mean: E[RV] = exp(m + s^2 / 2), with the validation residual variance
    full = np.full(len(lrv), np.nan)
    full[lookback:] = np.exp(lpred + 0.5 * resid_var * sd ** 2)
    return full  # full[t] forecasts lrv index t from data up to t-1


def compute_race() -> dict:
    rz = load("realized")
    ymd = np.asarray(rz["ymd"])
    rv = np.asarray(rz["rv"])
    rq = np.asarray(rz["rq"])
    # daily close-to-close returns aligned to the RV days, from the same one-minute closes
    db, cb = _btc_daily()
    pos = np.searchsorted(db, ymd)
    ret = np.full(len(ymd), np.nan)
    ok = (pos > 0) & (pos < len(db)) & (db[np.minimum(pos, len(db) - 1)] == ymd)
    ret[ok] = np.log(cb[pos[ok]] / cb[pos[ok] - 1])
    ret = np.where(np.isfinite(ret), ret, 0.0)
    n = len(rv)
    test0 = int(np.searchsorted(ymd, 20200101))
    val0 = int(np.searchsorted(ymd, 20190701))
    fc = {}
    # EWMA on squared daily returns
    fc["EWMA"] = vol.ewma(ret, 0.94)
    # GARCH and GJR fitted on the training period, then filtered forward with fixed parameters
    for kind in ("garch", "gjr"):
        f = vol.garch_fit(ret[:test0] - ret[:test0].mean(), kind)
        fc[kind.upper() if kind == "gjr" else "GARCH"] = vol.garch_filter(f["params"], ret - ret[:test0].mean(), kind)
    # HAR and HARQ fitted on the training period; har_predict(beta, rv)[k] forecasts day k + 22 from data to k + 21
    for name, q in (("HAR", None), ("HARQ", rq)):
        fit_ = vol.har_fit(rv[:test0], None if q is None else q[:test0])
        p = vol.har_predict(fit_["beta"], rv, q)
        full = np.full(n, np.nan)
        full[22:] = p[:n - 22]
        fc[name] = np.maximum(full, 1e-8)
    lrv = np.log(rv)
    # log-HAR: HAR on log RV, mapped back with the log-normal mean (training residual variance).  Added after the first
    # results showed the networks, which model log RV, beating HAR in levels: it separates the log from the network.
    fit_ = vol.har_fit(lrv[:test0])
    _, ytr = vol._har_design(lrv[:test0])
    s2 = float(np.var(ytr - fit_["fitted"]))
    p = vol.har_predict(fit_["beta"], lrv)
    full = np.full(n, np.nan)
    full[22:] = np.exp(p[:n - 22] + 0.5 * s2)
    fc["log-HAR"] = full
    seeds = [0, 1, 2, 3, 4]
    nn = {}
    for kind, label in (("lstm", "LSTM"), ("tf", "Transformer")):
        runs = []
        for s in seeds:
            runs.append(_nn_forecasts(lrv, val0, test0, kind, s))
            print(f"    {label} seed {s} trained", flush=True)
        nn[label] = runs
        fc[label] = np.nanmean(np.array(runs), axis=0)
    names = ["EWMA", "GARCH", "GJR", "HAR", "HARQ", "log-HAR", "LSTM", "Transformer"]
    test = np.arange(test0, n)
    test = test[np.all([np.isfinite(fc[k][test]) for k in names], axis=0)]
    scores = {}
    for k in names:
        ql = vol.qlike(fc[k][test], rv[test])
        se = vol.mse(fc[k][test], rv[test])
        scores[k] = {"qlike": float(ql.mean()), "mse": float(se.mean())}
    dm = {k: vol.diebold_mariano(vol.qlike(fc[k][test], rv[test]), vol.qlike(fc["HAR"][test], rv[test]))
          for k in names if k != "HAR"}
    dm_log = {k: vol.diebold_mariano(vol.qlike(fc[k][test], rv[test]), vol.qlike(fc["log-HAR"][test], rv[test]))
              for k in ("LSTM", "Transformer")}
    seed_q = {lab: [float(vol.qlike(np.asarray(r)[test], rv[test]).mean()) for r in runs] for lab, runs in nn.items()}
    i12 = int(np.searchsorted(ymd, 20200312))
    march = {k: float(np.sqrt(fc[k][i12] * 365)) for k in names}
    march["realized"] = float(np.sqrt(rv[i12] * 365))
    w = (ymd >= 20200201) & (ymd <= 20200430)
    return _json({"names": names, "scores": scores, "dm_vs_har": dm, "dm_vs_loghar": dm_log, "seed_qlike": seed_q, "march12": march,
                  "test_days": int(len(test)), "train_days": int(val0), "val_days": int(test0 - val0),
                  "window_t": rz["t"][w.nonzero()[0][0]:w.nonzero()[0][-1] + 1],
                  "window_rv": np.sqrt(rv[w] * 365), "window_fc": {k: np.sqrt(fc[k][w] * 365) for k in names},
                  "test_t": np.asarray(rz["t"])[test], "test_rv": np.sqrt(rv[test] * 365),
                  "test_har": np.sqrt(fc["HAR"][test] * 365), "test_garch": np.sqrt(fc["GARCH"][test] * 365),
                  "test_loghar": np.sqrt(fc["log-HAR"][test] * 365), "test_lstm": np.sqrt(fc["LSTM"][test] * 365)})


# ---------------------------------------------------------------------------
def compute_scaling() -> dict:
    d, r = _market()
    x = r - r.mean()
    i = int(np.searchsorted(d, 20200313))
    f = vol.garch_fit(x[:i + 1])
    p = f["params"]
    h = f["h"]
    fc = vol.garch_forecast(p, x[i], h[i], 252)
    T = np.arange(1, 253)
    garch_vol = np.sqrt(np.cumsum(fc) / T * 252)
    sqrt_rule = np.full(len(T), np.sqrt(fc[0] * 252))
    uncond = float(np.sqrt(p[0] / (1 - f["persistence"]) * 252))
    return _json({"T": T, "garch_vol": garch_vol, "sqrt_rule": sqrt_rule, "uncond": uncond,
                  "spot_vol": float(np.sqrt(fc[0] * 252)), "date": 20200313,
                  "desk": {"daily": 0.01, "annual": 0.01 * np.sqrt(252), "weekly": 0.01 * np.sqrt(5)}})


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    reg = {"btc_vol_race_2020": pit.register("btc_vol_race_2020", inspect.getsource(compute_race),
                                             {"models": ["EWMA", "GARCH", "GJR", "HAR", "HARQ", "log-HAR", "LSTM",
                                                         "Transformer"], "seeds": 5, "test": "2020",
                                              "note": "log-HAR added after the first results; counted"}, trials=8)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


def compute_daily() -> dict:
    db, cb = _btc_daily()
    r = np.diff(np.log(cb))
    return _json({"ymd": db[1:], "t": _frac(db[1:]), "r": r})


ITEMS = {"daily": compute_daily, "spurious": compute_spurious, "coint": compute_coint, "regimes": compute_regimes, "garch": compute_garch,
         "dcc": compute_dcc, "realized": compute_realized, "har": compute_har, "race": compute_race, "scaling": compute_scaling,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
