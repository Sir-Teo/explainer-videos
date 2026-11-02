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


# ===========================================================================
# The expansion (November 2026): every chapter's experiment.  New items only; the items above keep their cached numbers.
# ===========================================================================
def _vix():
    v = data.fred("VIXCLS", start="1990-01-02")
    return pit.research(v["date"], v["value"])


def _hist(x, lo, hi, bins):
    h, e = np.histogram(np.clip(x, lo, hi), bins=bins, range=(lo, hi))
    return h, e


def compute_acf_arma() -> dict:
    d, r = _market()
    x = r - r.mean()
    L = 250
    acfs = {"r": vol.acf(x, L), "abs": vol.acf(np.abs(x), L), "sq": vol.acf(x ** 2, L)}
    lb = {"r": vol.ljung_box(x, 20), "sq": vol.ljung_box(x ** 2, 20), "abs": vol.ljung_box(np.abs(x), 20)}
    dv, vv = _vix()
    lv = np.log(vv)
    pacf = [float(vol.ar_fit(lv, k)["beta"][-1]) for k in range(1, 11)]
    table = []
    for p_ in (0, 1, 2):
        for q_ in (0, 1, 2):
            if p_ == 0 and q_ == 0:
                continue
            f = vol.arma_fit(lv, p_, q_)
            table.append({"p": p_, "q": q_, "aic": f["aic"], "phi": f["phi"], "theta": f["theta"],
                          "lb": vol.ljung_box(f["resid"], 20)})
            print(f"    ARMA({p_},{q_}) AIC {f['aic']:.1f}", flush=True)
    best = min(table, key=lambda r_: r_["aic"])
    ar1 = vol.ar_fit(lv, 1)
    phi = float(ar1["beta"][1])
    # the MA(infinity) weights of the chosen model (Wold): psi_0 = 1, psi_k = phi psi_{k-1} (+ theta at k = 1, ...)
    ph, th = list(best["phi"]), list(best["theta"])
    psi = [1.0]
    for k in range(1, 41):
        v = sum(ph[i] * psi[k - 1 - i] for i in range(len(ph)) if k - 1 - i >= 0) + (th[k - 1] if k - 1 < len(th) else 0)
        psi.append(v)
    return _json({"acf": acfs, "lb": lb, "n": int(len(x)), "vix_t": _frac(dv)[::5], "vix_log": lv[::5],
                  "vix_acf": vol.acf(lv, 60), "vix_pacf": pacf, "table": table, "best": {"p": best["p"], "q": best["q"]},
                  "best_lb": best["lb"], "ar1_phi": phi, "ar1_half_life": float(np.log(0.5) / np.log(phi)),
                  "n_vix": int(len(lv)), "psi": psi})


def compute_unitroot() -> dict:
    t = vol.df_simulate(500, 20000, seed=0)
    lo, hi, bins = -5.0, 3.0, 64
    snaps = [100, 300, 1000, 3000, 10000, 20000]
    hists = [_hist(t[:k], lo, hi, bins)[0] for k in snaps]
    edges = _hist(t, lo, hi, bins)[1]
    db, cb = _btc_daily()
    dv, vv = _vix()
    y = data.fred("DGS10", start="1962-01-02")
    dy, yv = pit.research(y["date"], y["value"])
    dm, rm = _market()
    adfs = {"btc": vol.adf(np.log(cb), 5), "vix": vol.adf(np.log(vv), 5), "y10": vol.adf(yv, 5),
            "us": vol.adf(np.cumsum(rm), 5)}
    # Phillips (1986): the t-statistic of a regression of one independent walk on another grows like sqrt(T)
    rng = np.random.default_rng(11)
    Ts = [50, 100, 200, 500, 1000, 2000]
    med_t = []
    for T in Ts:
        a = np.cumsum(rng.standard_normal((1000, T)), 1)
        b = np.cumsum(rng.standard_normal((1000, T)), 1)
        ac, bc = a - a.mean(1, keepdims=True), b - b.mean(1, keepdims=True)
        beta = np.sum(ac * bc, 1) / np.sum(bc * bc, 1)
        u = ac - beta[:, None] * bc
        se = np.sqrt(np.sum(u * u, 1) / (T - 2) / np.sum(bc * bc, 1))
        med_t.append(float(np.median(np.abs(beta / se))))
    # one pair, the fitted slope as the sample grows
    a = np.cumsum(rng.standard_normal(2000))
    b = np.cumsum(rng.standard_normal(2000))
    slopes = []
    for T in range(50, 2001, 25):
        bc = b[:T] - b[:T].mean()
        slopes.append(float(np.sum((a[:T] - a[:T].mean()) * bc) / np.sum(bc * bc)))
    # the Dickey-Fuller limit, simulated from its Brownian form: (W(1)^2 - 1) / 2 / sqrt(int W^2) (no constant)
    W = np.cumsum(rng.standard_normal((20000, 1000)), 1) / np.sqrt(1000)
    lim = 0.5 * (W[:, -1] ** 2 - 1) / np.sqrt(np.mean(W ** 2, 1))
    return _json({"t": t[:2000], "q05": float(np.quantile(t, 0.05)), "q01": float(np.quantile(t, 0.01)),
                  "q10": float(np.quantile(t, 0.10)), "mean": float(t.mean()), "share_below_1645": float(np.mean(t < -1.645)),
                  "snaps": snaps, "hists": hists, "edges": edges, "adf": adfs, "Ts": Ts, "phillips_t": med_t,
                  "pair_a": a[::5], "pair_b": b[::5], "slopes": slopes, "lim_q05": float(np.quantile(lim, 0.05)),
                  "p_w1_lt_1": float(np.mean(np.abs(W[:, -1]) < 1)), "y10_t": _frac(dy)[::10], "y10": yv[::10]})


def compute_johansen() -> dict:
    ser = {}
    for k in ("DTB3", "DGS5", "DGS10"):
        f = data.fred(k, start="1990-01-02")
        ser[k] = pit.research(f["date"], f["value"])
    common = ser["DTB3"][0]
    for k in ("DGS5", "DGS10"):
        common = np.intersect1d(common, ser[k][0])
    X = np.column_stack([ser[k][1][np.searchsorted(ser[k][0], common)] for k in ("DTB3", "DGS5", "DGS10")])
    j = vol.johansen(X, k=2)
    adfs = {k: vol.adf(X[:, i], 5)["t"] for i, k in enumerate(("DTB3", "DGS5", "DGS10"))}
    Xc = X - X.mean(0)
    w, V = np.linalg.eigh(np.cov(Xc.T))
    o = np.argsort(w)[::-1]
    # Bitcoin spot and perpetual: who corrects?
    c = load("coint")
    ecm = vol.ecm_fit(np.asarray(c["lf"]), np.asarray(c["ls"]))
    # the drunk and her dog (Murray 1994): two walks, the dog pulled toward the drunk
    rng = np.random.default_rng(5)
    n = 600
    D, G = np.zeros((n, 2)), np.zeros((n, 2))
    G[0] = [0.5, -0.3]
    for t in range(1, n):
        D[t] = D[t - 1] + rng.standard_normal(2) * 0.35 + 0.08 * (G[t - 1] - D[t - 1])
        G[t] = G[t - 1] + rng.standard_normal(2) * 0.35 + 0.3 * (D[t - 1] - G[t - 1])
    gap = np.linalg.norm(D - G, axis=1)
    return _json({"t": _frac(common)[::10], "X": X[::10], "eig": j["eig"], "trace": j["trace"], "crit5": j["crit5"],
                  "rank": j["rank"], "beta": j["beta"], "adf": adfs, "pca_var": w[o] / w.sum(), "pca_vec": V[:, o],
                  "mean": X.mean(0), "n": int(len(X)), "ecm": {k: v for k, v in ecm.items() if k != "u"},
                  "drunk": D, "dog": G, "gap": gap, "adf_drunk": vol.adf(D[:, 0])["t"], "adf_gap": vol.adf(D[:, 0] - G[:, 0])["t"]})


def compute_regimes_em() -> dict:
    ff = data.ken_french_factors_monthly()
    x = ff["mkt_rf"]
    its = [1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 300]
    path = []
    for k in its:
        m = vol.markov_switching(x, n_iter=k)
        path.append({"it": k, "loglik": m["loglik"], "mu": m["mu"], "sd": m["sd"]})
    ms = vol.markov_switching(x, n_iter=300)
    hf = vol.hamilton_filter(x, ms["mu"], ms["sd"], ms["P"])
    P = ms["P"]
    pi_storm = float((1 - P[0, 0]) / (2 - P[0, 0] - P[1, 1]))
    # one month of -8% after a calm prediction: the posterior
    prior = np.array([P[0, 0], P[0, 1]])
    dens = np.exp(-0.5 * ((-0.08 - ms["mu"]) / ms["sd"]) ** 2) / ms["sd"]
    post = prior * dens / np.sum(prior * dens)
    d = ff["date"]
    t = d // 100 + (d % 100 - 0.5) / 12
    return _json({"path": path, "t": t, "x": x, "pred": hf["pred"][:, 1], "filt": hf["filt"][:, 1], "P": P,
                  "mu": ms["mu"], "sd": ms["sd"], "pi_storm": pi_storm, "prior_storm": float(prior[1]),
                  "post_storm_m8": float(post[1])})


def compute_kalman() -> dict:
    z = load("realized")
    lv = 0.5 * np.log(np.asarray(z["rv"]))
    k = vol.kalman_local_level(lv)
    st = vol.kalman_states(lv, k["q"], k["r"])
    qr = np.logspace(-3, 2, 120)
    d, r = _market()
    x = r - r.mean()
    sv = vol.sv_qml(x)
    g = vol.garch_fit(x)
    sv_vol = np.sqrt(np.exp(sv["smoothed"]) * 252)
    g_vol = np.sqrt(g["h"] * 252)
    return _json({"t": z["t"], "y": lv, "m": st["m"], "m_prior": st["m_prior"], "P_prior": st["P_prior"], "P": st["P"],
                  "K": st["K"], "q": k["q"], "r": k["r"], "snr": k["signal_to_noise"], "qr": qr, "gain": vol.steady_gain(qr),
                  "K_ss": float(vol.steady_gain(k["signal_to_noise"])),
                  "sv": {"phi": sv["phi"], "sigma_eta": sv["sigma_eta"], "mu": sv["mu"],
                         "half_life": float(np.log(0.5) / np.log(sv["phi"]))},
                  "us_t": _frac(d)[::5], "sv_vol": sv_vol[::5], "garch_vol": g_vol[::5],
                  "corr_sv_garch": float(np.corrcoef(sv_vol, g_vol)[0, 1])})


def compute_garch_lik() -> dict:
    from scipy.signal import lfilter
    from scipy.optimize import brentq
    from scipy.stats import norm, t as student
    d, r = _market()
    x = r - r.mean()
    v = float(np.var(x))
    z = x / np.sqrt(v)
    z2 = z ** 2
    n = len(z)

    def ll(a, b):  # variance targeting: omega = 1 - a - b in unit-variance returns
        if a + b >= 0.9995 or a < 0 or b < 0:
            return np.nan
        w = 1 - a - b
        h = np.empty(n)
        h[0] = 1.0
        h[1:] = lfilter([1.0], [1.0, -b], w + a * z2[:-1], zi=[b * 1.0])[0]
        return float(-0.5 * np.sum(np.log(2 * np.pi * h) + z2 / h) - 0.5 * n * np.log(v))

    A = np.linspace(0.02, 0.22, 41)
    B = np.linspace(0.74, 0.98, 41)
    grid = np.array([[ll(a, b) for a in A] for b in B])
    path = [(0.04, 0.80)]
    from scipy import optimize as opt
    res = opt.minimize(lambda p: -ll(*p) if np.isfinite(ll(*p)) else 1e12, path[0], method="Nelder-Mead",
                       callback=lambda p: path.append(tuple(p)), options={"xatol": 1e-5, "fatol": 1e-3})
    path = np.array(path)
    lls = np.array([ll(a, b) for a, b in path])
    ck = sorted(set([0, 3, 8, 15, 30, len(path) - 1]))
    snaps = []
    for i in ck:
        a, b = path[i]
        h = np.empty(n)
        h[0] = 1.0
        h[1:] = lfilter([1.0], [1.0, -b], (1 - a - b) + a * z2[:-1], zi=[b])[0]
        snaps.append(np.sqrt(h * v * 252)[::20])
    tg = vol.garch_t_fit(x)
    g = vol.garch_fit(x)
    zs = x / np.sqrt(g["h"])
    ps = np.linspace(0.002, 0.998, 120)
    nu = tg["nu"]
    qq = {"emp": np.quantile(zs / zs.std(), ps), "normal": norm.ppf(ps),
          "t": student.ppf(ps, nu) * np.sqrt((nu - 2) / nu)}
    al = np.linspace(0.01, 0.6, 60)
    nb = [brentq(lambda b_: vol.nelson_elog(a_, b_), 1e-6, 2.0) for a_ in al]
    gb = load("garch")
    us = gb["us"]["garch"]["params"]
    btc = gb["btc"]["garch"]
    # the leaky bucket: a GARCH simulated with the US parameters (in daily percent)
    rng = np.random.default_rng(7)
    w_, a_, b_ = us[0] * 1e4, us[1], us[2]
    hs, rs = np.empty(400), np.empty(400)
    hs[0] = w_ / (1 - a_ - b_)
    for i in range(400):
        if i:
            hs[i] = w_ + a_ * rs[i - 1] ** 2 + b_ * hs[i - 1]
        rs[i] = np.sqrt(hs[i]) * rng.standard_normal()
    lags = np.arange(1, 61)
    return _json({"A": A, "B": B, "grid": grid, "path": path, "path_ll": lls, "ck": ck, "snaps": snaps,
                  "t_snap": _frac(d)[::20], "n_iter": int(len(path)), "t_garch": {"params": tg["params"], "nu": nu,
                                                                                    "loglik": tg["loglik"]},
                  "g_loglik": g["loglik"], "qq": qq, "kurt_z": float(np.mean(zs ** 4) / np.mean(zs ** 2) ** 2),
                  "nelson_a": al, "nelson_b": nb, "us": us, "btc": btc,
                  "e_03_075": float(vol.nelson_elog(0.3, 0.75)), "e_025_080": float(vol.nelson_elog(0.25, 0.80)),
                  "e_us": float(vol.nelson_elog(us[1], us[2])), "bucket_h": hs, "bucket_r": rs,
                  "unroll": us[1] * us[2] ** (lags - 1), "floor": float(us[0] / (1 - us[2]))})


def _stock_bond():
    y = data.fred("DGS10", start="1962-01-02")
    dy, yv = pit.research(y["date"], y["value"])
    dm, rm = _market()
    common = np.intersect1d(dy, dm)
    yy = yv[np.searchsorted(dy, common)] / 100
    rb = yy[:-1] / 252 - 8.0 * np.diff(yy)
    rs = rm[np.searchsorted(dm, common)][1:]
    return common[1:], rs, rb


def compute_dcc_ell() -> dict:
    d, rs, rb = _stock_bond()
    yrs = d // 10000
    years = list(range(1962, 2021))
    cov = [np.cov(np.vstack([rs[yrs == y], rb[yrs == y]])) * 252 for y in years]
    rho = [float(c[0, 1] / np.sqrt(c[0, 0] * c[1, 1])) for c in cov]
    lam = 0.94
    s11, s22, s12 = np.var(rs[:60]), np.var(rb[:60]), 0.0
    ew = np.empty(len(rs))
    for t in range(len(rs)):
        ew[t] = s12 / np.sqrt(s11 * s22)
        s11 = lam * s11 + (1 - lam) * rs[t] ** 2
        s22 = lam * s22 + (1 - lam) * rb[t] ** 2
        s12 = lam * s12 + (1 - lam) * rs[t] * rb[t]
    # 60/40 in 2010: the risk the model said (correlation +0.3) against the risk realized
    m = yrs == 2010
    v1, v2 = np.var(rs[m]) * 252, np.var(rb[m]) * 252
    model = np.sqrt(0.36 * v1 + 0.16 * v2 + 2 * 0.24 * 0.3 * np.sqrt(v1 * v2))
    real = np.std(0.6 * rs[m] + 0.4 * rb[m]) * np.sqrt(252)
    return _json({"years": years, "cov": cov, "rho": rho, "t": _frac(d)[::5], "ewma": ew[::5],
                  "rho_2010": rho[years.index(2010)], "model_6040": float(model), "real_6040": float(real)})


def compute_signature() -> dict:
    from scipy.special import gamma as G
    b = data.binance_klines("BTCUSDT", "1m", "2017-08", "2020-12")
    t, c = np.asarray(b["time"], float), np.asarray(b["close"], float)
    day = (t // 86400).astype(int)
    lc = np.log(c)
    steps = (1, 2, 3, 5, 10, 15, 20, 30, 60)
    days, sig, eta2, z, nobs, rq5 = [], [], [], [], [], []
    examples = {}
    bounds = np.searchsorted(day, np.unique(day))
    bounds = list(bounds) + [len(day)]
    for i in range(len(bounds) - 1):
        x = lc[bounds[i]:bounds[i + 1]]
        if len(x) < 1200:
            continue
        dd = int(day[bounds[i]])
        ymd = int(datetime.fromtimestamp(dd * 86400, tz=timezone.utc).strftime("%Y%m%d"))
        days.append(ymd)
        sig.append(vol.signature_plot(x, steps))
        r1 = np.diff(x)
        eta2.append(np.sum(r1 ** 2) / (2 * len(r1)))
        r5 = np.diff(x[::5])
        z.append(vol.bns_jump_z(r5))
        rq5.append(np.sum(r5 ** 4) * len(r5) / 3)
        nobs.append(len(x))
        if ymd in (20190626, 20200312, 20191025):
            examples[str(ymd)] = x
    days, sig, eta2, z, rq5 = (np.asarray(v) for v in (days, sig, eta2, z, rq5))
    y19 = (days >= 20190101) & (days <= 20191231)
    ann = lambda v: np.sqrt(np.mean(v, 0) * 365)  # noqa: E731
    # Bandi and Russell (2008): n* = (IQ / (4 eta^4))^(1/3) per day, IQ estimated by 5-minute realized quarticity
    nstar = (rq5 / (4 * eta2 ** 2)) ** (1 / 3)
    minutes = 1440 / nstar
    crit = 2.326
    rz = load("realized")
    rv = np.asarray(rz["rv"])
    se = np.sqrt(2 * np.asarray(rz["rq"]) / 288)
    ymd_r = np.asarray(rz["ymd"])
    w = (ymd_r >= 20190101) & (ymd_r <= 20191231)
    return _json({"steps": steps, "days": days, "sig_all": ann(sig), "sig_2019": ann(sig[y19]),
                  "eta2_median": float(np.median(eta2)), "z": z, "jump_share_1pct": float(np.mean(z > crit)),
                  "jump_share_01pct": float(np.mean(z > 3.09)), "z_0312": float(z[days == 20200312][0]),
                  "nstar_min_median": float(np.median(minutes)), "nstar_min_q": np.quantile(minutes, [0.25, 0.75]),
                  "examples": {k: v - v[0] for k, v in examples.items()},
                  "clt_t": np.asarray(rz["t"])[w], "clt_rv": rv[w], "clt_se": se[w],
                  "mu43": float(2 ** (2 / 3) * G(7 / 6) / G(1 / 2))})


def compute_har_roll() -> dict:
    rz = load("realized")
    ymd, rv, bv = (np.asarray(rz[k]) for k in ("ymd", "rv", "bv"))
    t = np.asarray(rz["t"])
    sg = load("signature")
    zd = dict(zip(np.asarray(sg["days"]).tolist(), np.asarray(sg["z"]).tolist()))
    z = np.array([zd.get(int(d), 0.0) for d in ymd])
    J = np.where(z > 2.326, np.maximum(rv - bv, 0), 0.0)
    end = int(np.searchsorted(ymd, 20200101))
    roll_t, roll_b = [], []
    for e in range(252 + 22, len(rv) + 1, 5):
        f = vol.har_fit(rv[e - 252 - 22:e])
        roll_t.append(t[e - 1])
        roll_b.append(f["beta"])
    cj = vol.har_cj(rv[:end], bv[:end], J[:end])
    lrv = np.log(rv)
    lh = vol.har_fit(lrv[:end])
    h = load("har")["HAR"]["beta"]
    bd, bw, bm = h[1], h[2], h[3]
    wts = np.array([bd + bw / 5 + bm / 22] + [bw / 5 + bm / 22] * 4 + [bm / 22] * 17)
    gb = load("garch")["btc"]["garch"]
    gw = gb[1] * gb[2] ** np.arange(22)
    # the autocorrelation of log RV, against what the fitted log-HAR and an AR(1) imply (by simulation)
    lags = np.arange(1, 101)
    emp = vol.acf(lrv, 100)[1:]
    rng = np.random.default_rng(9)
    _, ytr = vol._har_design(lrv[:end])
    res = ytr - lh["fitted"]
    sim = list(lrv[:22])
    for _ in range(100000):
        x_ = np.array(sim[-22:])
        sim.append(lh["beta"][0] + lh["beta"][1] * x_[-1] + lh["beta"][2] * x_[-5:].mean() + lh["beta"][3] * x_.mean()
                   + res[rng.integers(len(res))])
    har_acf = vol.acf(np.array(sim[1000:]), 100)[1:]
    phi = vol.acf(lrv, 1)[1]
    return _json({"roll_t": roll_t, "roll_b": roll_b, "cj": cj["beta"], "jump_days": float(np.mean(J > 0)),
                  "loghar": lh["beta"], "har_w": wts, "garch_w": gw, "lags": lags, "acf_emp": emp, "acf_har": har_acf,
                  "acf_ar1": phi ** lags})


def _fgn_path(H, n, rng):
    k = np.arange(n)
    g = 0.5 * (np.abs(k + 1) ** (2 * H) - 2 * np.abs(k) ** (2 * H) + np.abs(k - 1) ** (2 * H))
    C = g[np.abs(k[:, None] - k[None, :])]
    return np.cumsum(np.linalg.cholesky(C + 1e-12 * np.eye(n)) @ rng.standard_normal(n))


def compute_rough() -> dict:
    from explainer.quant.house import rough
    rz = load("realized")
    lv = 0.5 * np.log(np.asarray(rz["rv"]))
    btc = rough.log_rv_scaling(lv)
    rng = np.random.default_rng(14)
    sims = {}
    for H in (0.1, 0.5):
        Hs = [rough.log_rv_scaling(_fgn_path(H, len(lv), rng))["H"] for _ in range(5)]
        sims[str(H)] = Hs
    path01 = _fgn_path(0.1, 2048, np.random.default_rng(3))
    path05 = _fgn_path(0.5, 2048, np.random.default_rng(3))
    return _json({"btc": btc, "sims": sims, "path01": path01, "path05": path05, "lv": lv, "t": rz["t"]})


def compute_scoring() -> dict:
    from scipy.special import gammaln
    rng = np.random.default_rng(21)
    R, T = 200, 2500
    w, a, b = 0.02, 0.10, 0.88
    h = np.full(R, w / (1 - a - b))
    H, P1, P78 = np.empty((T, R)), np.empty((T, R)), np.empty((T, R))
    for t in range(T):
        H[t] = h
        z = rng.standard_normal(R)
        P1[t] = h * z ** 2
        P78[t] = h * rng.chisquare(78, R) / 78
        h = w + a * P1[t] + b * h
    ma = np.full_like(H, np.nan)
    c = np.cumsum(np.vstack([np.zeros(R), P1]), 0)
    ma[60:] = (c[60:-1] - c[:-61]) / 60
    fc = {"truth": H, "truth x 0.8": 0.8 * H, "truth x 1.2": 1.2 * H, "60-day average": ma}
    proxies = {"squared return": P1, "RV, 78 returns": P78, "the truth": H}
    losses = {"QLIKE": lambda f, p: p / f - np.log(np.maximum(p, 1e-300) / f) - 1,
              "MSE on variance": lambda f, p: (p - f) ** 2, "MSE on volatility": lambda f, p: (np.sqrt(p) - np.sqrt(f)) ** 2,
              "MAE on volatility": lambda f, p: np.abs(np.sqrt(p) - np.sqrt(f))}
    table = {}
    for ln, L in losses.items():
        table[ln] = {}
        for pn, P in proxies.items():
            m = {fn: float(np.nanmean(L(F[60:], P[60:]))) for fn, F in fc.items()}
            table[ln][pn] = {"mean": m, "winner": min(m, key=m.get)}
    # expected loss curves against a proxy h * chi2_k / k, with h = 1: QLIKE and MSE on volatility
    hh = np.linspace(0.25, 2.0, 141)
    curves = {}
    for k in (1, 5, 78, 0):
        if k:
            Es = float(np.exp(0.5 * np.log(2 / k) + gammaln((k + 1) / 2) - gammaln(k / 2)))  # E sqrt(chi2_k / k)
            Elog = float(np.log(2 / k) + __import__("scipy.special", fromlist=["digamma"]).digamma(k / 2))
        else:
            Es, Elog = 1.0, 0.0
        curves[str(k)] = {"qlike": 1 / hh - Elog + np.log(hh) - 1, "msevol": 1 - 2 * np.sqrt(hh) * Es + hh,
                          "argmin_msevol": Es ** 2}
    return _json({"table": table, "R": R, "T": T, "params": [w, a, b], "hh": hh, "curves": curves})


# ---------------------------------------------------------------------------
# Networks with their training recorded (the race's LSTM and transformer, retrained with the same seeds, plus HARNet)
def _nn_train(lrv, train_end, val_end, kind, seed, lookback=22, epochs=300, checkpoints=(0, 5, 10, 20, 40)):
    """The race's ``_nn_forecasts`` loop, unchanged in every operation that touches the random state, with the training
    and validation loss recorded per epoch and the validation forecasts kept at a few epochs.  ``kind`` 'harnet' is a
    HARNet-style model (Reisenhofer, Bayer and Hautsch 2022): learnable 1-, 5- and 22-day averaging filters initialised
    as averages, a linear head initialised to log-HAR's least-squares coefficients, and a small ReLU branch whose last
    layer starts at zero, so that at epoch 0 it *is* log-HAR."""
    import torch

    torch.set_num_threads(1)
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

    class HARNet(torch.nn.Module):
        def __init__(self, beta):
            super().__init__()
            w = torch.zeros(3, lookback)
            w[0, -1] = 1.0
            w[1, -5:] = 1 / 5
            w[2, :] = 1 / lookback
            self.filt = torch.nn.Parameter(w)
            self.head = torch.nn.Linear(3, 1)
            with torch.no_grad():
                self.head.weight[:] = torch.tensor(beta[1:], dtype=torch.float32)[None, :]
                self.head.bias[:] = float(beta[0])
            self.mlp = torch.nn.Sequential(torch.nn.Linear(3, 8), torch.nn.ReLU(), torch.nn.Linear(8, 1))
            with torch.no_grad():
                self.mlp[2].weight.zero_()
                self.mlp[2].bias.zero_()

        def forward(self, x):
            a = x[:, :, 0] @ self.filt.T
            return (self.head(a) + self.mlp(a)).squeeze(-1)

    if kind == "lstm":
        model = LSTM()
    elif kind == "tf":
        model = Tiny()
    else:
        Xh = X[tr, :, 0]
        A = np.column_stack([np.ones(len(Xh)), Xh[:, -1], Xh[:, -5:].mean(1), Xh.mean(1)])
        beta, *_ = np.linalg.lstsq(A, y[tr], rcond=None)
        model = HARNet(beta)
    n_par = int(sum(p.numel() for p in model.parameters()))
    opt = torch.optim.Adam(model.parameters(), lr=3e-3, weight_decay=1e-4)
    best, best_state, bad, best_ep = 1e9, None, 0, 0
    tr_hist, va_hist, snaps = [], [], {}

    def val_pred():
        model.eval()
        with torch.no_grad():
            return (model(Xt[va]).numpy() * sd + mu).tolist()

    snaps["0"] = val_pred()
    with torch.no_grad():
        va_hist0 = float(torch.mean((model(Xt[va]) - yt[va]) ** 2))
        tr_hist0 = float(torch.mean((model(Xt[tr]) - yt[tr]) ** 2))
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(tr.stop)
        tot, cnt = 0.0, 0
        for i in range(0, tr.stop, 64):
            idx = perm[i:i + 64]
            opt.zero_grad()
            loss = torch.mean((model(Xt[idx]) - yt[idx]) ** 2)
            loss.backward()
            opt.step()
            tot += float(loss) * len(idx)
            cnt += len(idx)
        model.eval()
        with torch.no_grad():
            vl = float(torch.mean((model(Xt[va]) - yt[va]) ** 2))
        tr_hist.append(tot / cnt)
        va_hist.append(vl)
        if ep + 1 in checkpoints:
            snaps[str(ep + 1)] = val_pred()
        if vl < best - 1e-5:
            best, bad, best_ep = vl, 0, ep + 1
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad > 30:
                break
    model.load_state_dict(best_state)
    model.eval()
    snaps["best"] = val_pred()
    with torch.no_grad():
        pred = model(Xt).numpy()
        resid_var = float(np.var(pred[va] - y[va]))
    lpred = pred * sd + mu
    full = np.full(len(lrv), np.nan)
    full[lookback:] = np.exp(lpred + 0.5 * resid_var * sd ** 2)
    out = {"full": full, "train": [tr_hist0] + tr_hist, "val": [va_hist0] + va_hist, "best_epoch": best_ep,
           "snaps": snaps, "n_params": n_par}
    if kind == "harnet":
        out["filters"] = model.filt.detach().numpy()
        out["head"] = model.head.weight.detach().numpy()[0]
    return out


def compute_training() -> dict:
    import json as _js
    rz = load("realized")
    ymd, rv = np.asarray(rz["ymd"]), np.asarray(rz["rv"])
    lrv = np.log(rv)
    test0 = int(np.searchsorted(ymd, 20200101))
    val0 = int(np.searchsorted(ymd, 20190701))
    runs_dir = CACHE.dir / "training_runs"  # one file per run: the item resumes where it stopped
    runs_dir.mkdir(parents=True, exist_ok=True)
    out = {}
    for kind, label in (("lstm", "LSTM"), ("tf", "Transformer"), ("harnet", "HARNet")):
        runs = []
        for s in range(5):
            f = runs_dir / f"{kind}_{s}.json"
            if f.exists():
                runs.append(_js.loads(f.read_text()))
                continue
            res = _json(_nn_train(lrv, val0, test0, kind, s))
            f.write_text(_js.dumps(res))
            runs.append(res)
            print(f"    {label} seed {s}: best epoch {res['best_epoch']}", flush=True)
        out[label] = runs
    test = np.arange(test0, len(rv))
    res = {}
    for label, runs in out.items():
        full = np.array([np.asarray(r["full"], float) for r in runs])
        seed_q = [float(vol.qlike(f[test], rv[test]).mean()) for f in full]
        res[label] = {"train": [r["train"] for r in runs], "val": [r["val"] for r in runs],
                      "best_epoch": [r["best_epoch"] for r in runs], "snaps": runs[0]["snaps"],
                      "n_params": runs[0]["n_params"], "seed_qlike": seed_q, "forecast": np.nanmean(full, 0)}
        if label == "HARNet":
            res[label]["filters"] = runs[0]["filters"]
            res[label]["head"] = runs[0]["head"]
    va = slice(val0, test0)
    return _json({**res, "val_t": np.asarray(rz["t"])[va], "val_lrv": lrv[va], "val0": val0, "test0": test0})


def _classical(rz):
    """The race's classical forecasts, recomputed exactly as ``compute_race`` makes them."""
    ymd, rv, rq = (np.asarray(rz[k]) for k in ("ymd", "rv", "rq"))
    db, cb = _btc_daily()
    pos = np.searchsorted(db, ymd)
    ret = np.full(len(ymd), np.nan)
    ok = (pos > 0) & (pos < len(db)) & (db[np.minimum(pos, len(db) - 1)] == ymd)
    ret[ok] = np.log(cb[pos[ok]] / cb[pos[ok] - 1])
    ret = np.where(np.isfinite(ret), ret, 0.0)
    n = len(rv)
    test0 = int(np.searchsorted(ymd, 20200101))
    fc = {"EWMA": vol.ewma(ret, 0.94)}
    for kind in ("garch", "gjr"):
        f = vol.garch_fit(ret[:test0] - ret[:test0].mean(), kind)
        fc["GJR" if kind == "gjr" else "GARCH"] = vol.garch_filter(f["params"], ret - ret[:test0].mean(), kind)
    for name, q in (("HAR", None), ("HARQ", rq)):
        fit_ = vol.har_fit(rv[:test0], None if q is None else q[:test0])
        p = vol.har_predict(fit_["beta"], rv, q)
        full = np.full(n, np.nan)
        full[22:] = p[:n - 22]
        fc[name] = np.maximum(full, 1e-8)
    lrv = np.log(rv)
    fit_ = vol.har_fit(lrv[:test0])
    _, ytr = vol._har_design(lrv[:test0])
    s2 = float(np.var(ytr - fit_["fitted"]))
    p = vol.har_predict(fit_["beta"], lrv)
    full = np.full(n, np.nan)
    full[22:] = np.exp(p[:n - 22] + 0.5 * s2)
    fc["log-HAR"] = full
    return fc, test0


def compute_race2() -> dict:
    rz = load("realized")
    rv = np.asarray(rz["rv"])
    fc, test0 = _classical(rz)
    tr = load("training")
    for k in ("LSTM", "Transformer", "HARNet"):
        fc[k] = np.asarray(tr[k]["forecast"], float)
    names = ["EWMA", "GARCH", "GJR", "HAR", "HARQ", "log-HAR", "LSTM", "Transformer", "HARNet"]
    test = np.arange(test0, len(rv))
    test = test[np.all([np.isfinite(fc[k][test]) for k in names], axis=0)]
    old = load("race")["scores"]
    check = max(abs(float(vol.qlike(fc[k][test], rv[test]).mean()) - old[k]["qlike"]) for k in names if k in old)
    Lq = np.column_stack([vol.qlike(fc[k][test], rv[test]) for k in names])
    scores = {k: {"qlike": float(Lq[:, i].mean()), "mse": float(vol.mse(fc[k][test], rv[test]).mean())}
              for i, k in enumerate(names)}
    dm_log = {k: vol.diebold_mariano(Lq[:, i], Lq[:, names.index("log-HAR")]) for i, k in enumerate(names) if k != "log-HAR"}
    mz = {k: vol.mincer_zarnowitz(fc[k][test], rv[test]) for k in names}
    mcs = vol.model_confidence_set(Lq, names, alpha=0.10, B=2000, block=10)
    full = vol.model_confidence_set(Lq, names, alpha=1.01, B=2000, block=10)  # every model's MCS p-value
    mcs["pvalues"] = dict(zip(full["eliminated"] + full["survivors"], full["p"] + [1.0]))
    cum = np.cumsum(Lq, 0) / np.arange(1, len(test) + 1)[:, None]
    return _json({"names": names, "scores": scores, "dm_vs_loghar": dm_log, "mz": mz, "mcs": mcs, "check": check,
                  "cum": cum[::2], "cum_t": np.asarray(rz["t"])[test][::2], "test_days": int(len(test)),
                  "i12": int(np.searchsorted(np.asarray(rz["ymd"])[test], 20200312)) // 2})


def compute_industry() -> dict:
    from explainer.quant.house import econ
    d, r = _market()
    x = r - r.mean()
    m = d >= 19900101
    xr = x[m]
    # RiskMetrics' decay factor: one lambda for everything, chosen by the RMSE of daily variance forecasts (TD 4e,
    # section 5.3.2); here also by QLIKE against the next week's summed squared returns
    lams = np.round(np.arange(0.85, 0.996, 0.005), 3)
    rmse, ql = [], []
    wk = np.add.reduceat(xr ** 2, np.arange(0, len(xr) - 5, 5))[:-1]
    for lam in lams:
        h = vol.ewma(xr, lam)
        rmse.append(float(np.sqrt(np.mean((xr[100:] ** 2 - h[100:]) ** 2))))
        hw = 5 * h[np.arange(0, len(xr) - 5, 5)][:-1]
        ql.append(float(np.mean(vol.qlike(hw[20:], wk[20:]))))
    # a volatility-regime adjustment, Barra-style, on the ten size deciles (our replica: half-lives our choice)
    sz = data.ken_french_size_daily()
    ds, R = pit.research(sz["date"], sz["deciles"])
    lam_v = 0.5 ** (1 / 90)
    S2 = np.empty_like(R)
    S2[0] = np.var(R[:60], 0)
    for t in range(1, len(R)):
        S2[t] = lam_v * S2[t - 1] + (1 - lam_v) * R[t - 1] ** 2
    sig = np.sqrt(S2)
    lam_t = vol.vra(R, sig, halflife=42)
    adj = sig * lam_t[:, None]
    q_raw = float(np.mean(vol.qlike(S2[250:], R[250:] ** 2 + 1e-12)))
    q_adj = float(np.mean(vol.qlike(adj[250:] ** 2, R[250:] ** 2 + 1e-12)))
    z_raw = np.std(R[250:] / sig[250:])
    z_adj = np.std(R[250:] / adj[250:])
    ys = ds // 10000
    peaks = {str(y0): float(lam_t[(ys >= y0) & (ys <= y1)].max()) for y0, y1 in ((1929, 1933), (1987, 1987), (2008, 2009), (2020, 2020))}
    # volatility targeting, 10% (Harvey et al. 2018): the US market 1927-2020, scaled by sigma_{t-2}
    kf = data.ken_french_daily()
    dk, ex = pit.research(kf["date"], kf["mkt_rf"])
    vt = vol.vol_target(ex, 0.10, com=60, lag=2)
    ok = np.isfinite(vt["weight"]) & (dk >= 19270101)
    sc, un = vt["scaled"][ok], ex[ok]
    un = un * np.std(sc) / np.std(un)  # the unscaled market at the same full-sample volatility
    def stats(v):
        sr = float(v.mean() / v.std() * np.sqrt(252))
        es = float(np.mean(np.sort(v)[:max(1, int(0.01 * len(v)))]))
        cum = np.cumsum(v)
        dd = float(np.max(np.maximum.accumulate(cum) - cum))
        return {"sharpe": sr, "es1": es, "maxdd_log": dd, "skew": float(np.mean((v - v.mean()) ** 3) / v.std() ** 3)}
    # the options desk: the VIX against the next month's realized volatility
    dv, vv = _vix()
    dm2, rm2 = d, x
    pos = np.searchsorted(dm2, dv)
    ok2 = (pos + 21 < len(dm2)) & (dm2[np.minimum(pos, len(dm2) - 1)] == dv)
    fwd = np.array([np.sqrt(np.sum(rm2[p_ + 1:p_ + 22] ** 2) * 252 / 21) for p_ in pos[ok2]]) * 100
    vix = vv[ok2]
    g = vol.garch_fit(x[:np.searchsorted(d, 19900101)])
    hg = vol.garch_filter(g["params"], x, "garch")
    pers = g["persistence"]
    vbar = g["params"][0] / (1 - pers)
    gf = np.array([np.sqrt(np.mean(vbar + pers ** np.arange(21) * (hg[p_ + 1] - vbar)) * 252) for p_ in pos[ok2]]) * 100
    mz_vix = econ.ols(fwd, vix, se="nw", lags=21)
    mz_g = econ.ols(fwd, gf, se="nw", lags=21)
    both = econ.ols(fwd, np.column_stack([vix, gf]), se="nw", lags=21)
    return _json({"lams": lams, "rmse": rmse, "qlike": ql, "lam_rmse": float(lams[int(np.argmin(rmse))]),
                  "lam_qlike": float(lams[int(np.argmin(ql))]),
                  "vra_t": _frac(ds)[::5], "vra": lam_t[::5], "vra_peaks": peaks, "q_raw": q_raw, "q_adj": q_adj,
                  "z_raw": float(z_raw), "z_adj": float(z_adj),
                  "vt_t": _frac(dk[ok])[::10], "vt_w": vt["weight"][ok][::10], "vt_scaled": stats(sc), "vt_plain": stats(un),
                  "vt_cum_scaled": np.cumsum(sc)[::10], "vt_cum_plain": np.cumsum(un)[::10],
                  "vix_t": _frac(dv[ok2])[::5], "vix": vix[::5], "fwd_rv": fwd[::5], "share_vix_above": float(np.mean(vix > fwd)),
                  "vrp_mean": float(np.mean(vix - fwd)), "vrp_var_mean": float(np.mean(vix ** 2 - fwd ** 2)),
                  "mz_vix": {"a": mz_vix["beta"][0], "b": mz_vix["beta"][1], "r2": mz_vix["r2"]},
                  "mz_garch": {"a": mz_g["beta"][0], "b": mz_g["beta"][1], "r2": mz_g["r2"]},
                  "encompass": {"b_vix": both["beta"][1], "t_vix": both["t"][1], "b_garch": both["beta"][2],
                                "t_garch": both["t"][2], "r2": both["r2"]}})


def _synthetic_vol(n, L, rng):
    """The toy foundation model's pretraining corpus: daily volatility-like series from four families with random
    parameters and levels (log AR(1), log HAR, two regimes, and a GARCH's sigma), never a market series."""
    out = np.empty((n, L))
    for i in range(n):
        fam = i % 4
        e = rng.standard_normal(L + 300)
        h = np.zeros(L + 300)
        if fam == 0:
            phi, s = rng.uniform(0.85, 0.995), rng.uniform(0.05, 0.35)
            for t in range(1, L + 300):
                h[t] = phi * h[t - 1] + s * e[t]
        elif fam == 1:
            bd, bw, bm = rng.dirichlet([3, 2, 3]) * rng.uniform(0.85, 0.98)
            s = rng.uniform(0.1, 0.4)
            for t in range(22, L + 300):
                h[t] = bd * h[t - 1] + bw * h[t - 5:t].mean() + bm * h[t - 22:t].mean() + s * e[t]
        elif fam == 2:
            lo, hi, p, q = 0.0, rng.uniform(0.5, 1.5), rng.uniform(0.95, 0.995), rng.uniform(0.85, 0.98)
            st = 0
            for t in range(1, L + 300):
                st = st if rng.random() < (p if st == 0 else q) else 1 - st
                h[t] = (hi if st else lo) + 0.15 * e[t]
        else:
            w, a = rng.uniform(0.02, 0.1), rng.uniform(0.03, 0.15)
            b = rng.uniform(0.80, 0.995 - a)
            v, r_ = 1.0, 0.0
            for t in range(1, L + 300):
                v = w + a * r_ ** 2 + b * v
                r_ = np.sqrt(v) * e[t]
                h[t] = 0.5 * np.log(v)
        noise = rng.uniform(0.0, 0.45)
        out[i] = np.exp(h[300:] + noise * rng.standard_normal(L) + rng.uniform(-4, 1))
    return out


def compute_foundation() -> dict:
    """A toy time-series foundation model in the manner of Chronos (Ansari et al. 2024): mean-scale the context,
    quantise each value into one of 128 bins, train a small transformer by cross-entropy to predict the next bin, on
    synthetic series only; then forecast Bitcoin's 2020 volatility zero-shot (weights frozen, nothing fitted to it)."""
    import torch
    torch.set_num_threads(1)
    C, NB, LO, HI = 64, 128, 0.0, 4.0
    edges = np.linspace(LO, HI, NB + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    rng = np.random.default_rng(0)
    corpus = _synthetic_vol(3000, 400, rng)
    rz = load("realized")
    ymd, rv = np.asarray(rz["ymd"]), np.asarray(rz["rv"])
    v = np.sqrt(rv)
    test0 = int(np.searchsorted(ymd, 20200101))
    i13 = int(np.searchsorted(ymd, 20200313))

    def tok(ctx):
        s = np.mean(np.abs(ctx), -1, keepdims=True)
        return np.clip(np.digitize(ctx / s, edges[1:-1]), 0, NB - 1), s

    class TSFM(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = torch.nn.Embedding(NB, 48)
            self.pos = torch.nn.Parameter(torch.zeros(1, C, 48))
            layer = torch.nn.TransformerEncoderLayer(48, 4, 96, dropout=0.0, batch_first=True)
            self.enc = torch.nn.TransformerEncoder(layer, 2)
            self.out = torch.nn.Linear(48, NB)

        def forward(self, x):
            return self.out(self.enc(self.emb(x) + self.pos)[:, -1])

    def predict(model, ctx):
        tk, s = tok(ctx)
        with torch.no_grad():
            p = torch.softmax(model(torch.tensor(tk)), -1).numpy()
        return p, s[:, 0]

    steps, ckpts = 3000, [0, 100, 300, 1000, 3000]
    runs = []
    test_ctx = np.stack([v[t - C:t] for t in range(test0, len(v))])
    for seed in range(3):
        torch.manual_seed(seed)
        g = np.random.default_rng(100 + seed)
        model = TSFM()
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        hist, snaps = [], {}
        for st in range(steps + 1):
            if st in ckpts:
                p, s = predict(model, v[i13 - C:i13][None, :])
                snaps[str(st)] = {"p": p[0], "s": float(s[0])}
            if st == steps:
                break
            ii = g.integers(len(corpus), size=128)
            jj = g.integers(0, 400 - C - 1, size=128)
            win = np.stack([corpus[a, b:b + C + 1] for a, b in zip(ii, jj)])
            tk, sc = tok(win[:, :C])
            tgt = np.clip(np.digitize(win[:, C] / sc[:, 0], edges[1:-1]), 0, NB - 1)
            model.train()
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(model(torch.tensor(tk)), torch.tensor(tgt))
            loss.backward()
            opt.step()
            hist.append(float(loss.detach()))
        model.eval()
        p, s = predict(model, test_ctx)
        ev2 = (s ** 2) * (p @ centers ** 2)
        cdf = np.cumsum(p, 1)
        qs = {str(q): s * centers[np.argmax(cdf >= q, 1)] for q in (0.1, 0.5, 0.9)}
        runs.append({"loss": hist, "snaps": snaps, "var": ev2, "q": qs})
        print(f"    toy foundation model seed {seed}: final loss {np.mean(hist[-100:]):.3f}", flush=True)
    fc, _ = _classical(rz)
    test = np.arange(test0, len(v))
    var = np.mean([r_["var"] for r_ in runs], 0)
    lq = vol.qlike(var, rv[test])
    lh = vol.qlike(fc["log-HAR"][test], rv[test])
    loss = np.array([r_["loss"] for r_ in runs])
    k = 50
    sm = np.array([np.convolve(l_, np.ones(k) / k, "valid")[::25] for l_ in loss])
    tks, _ = tok(v[i13 - C:i13][None, :])
    return _json({"qlike": float(lq.mean()), "qlike_loghar": float(lh.mean()), "dm_vs_loghar": vol.diebold_mariano(lq, lh),
                  "seed_qlike": [float(vol.qlike(r_["var"], rv[test]).mean()) for r_ in runs],
                  "loss_steps": np.arange(k - 1, steps, 25)[:sm.shape[1]], "loss": sm, "ckpts": ckpts,
                  "snaps": runs[0]["snaps"], "centers": centers, "ctx": v[i13 - C:i13], "ctx_tokens": tks[0],
                  "next_true": float(v[i13]), "test_t": np.asarray(rz["t"])[test],
                  "q10": np.mean([r_["q"]["0.1"] for r_ in runs], 0), "q50": np.mean([r_["q"]["0.5"] for r_ in runs], 0),
                  "q90": np.mean([r_["q"]["0.9"] for r_ in runs], 0), "test_v": v[test],
                  "cover80": float(np.mean((v[test] >= np.mean([r_["q"]["0.1"] for r_ in runs], 0)) &
                                           (v[test] <= np.mean([r_["q"]["0.9"] for r_ in runs], 0)))),
                  "n_series": 3000, "context": C, "bins": NB, "steps": steps,
                  "n_params": int(sum(p_.numel() for p_ in TSFM().parameters()))})


def compute_envelope2() -> dict:
    """The models added in the expansion, registered before their test-year scores were computed."""
    reg = {"btc_vol_harnet_2020": pit.register("btc_vol_harnet_2020", inspect.getsource(_nn_train),
                                               {"model": "HARNet-style", "seeds": 5, "test": "2020"}, trials=1),
           "btc_vol_toy_tsfm_2020": pit.register("btc_vol_toy_tsfm_2020", inspect.getsource(compute_foundation),
                                                 {"model": "toy Chronos-style TSFM", "seeds": 3, "test": "2020"}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far(), "part7_trials": 8 + 1 + 1})


def compute_house_fc() -> dict:
    """The House's forecaster called as a desk would call it, on the last day of the research window."""
    rz = load("realized")
    btc = vol.forecast(np.asarray(rz["rv"]), 22)
    d, r = _market()
    x = r - r.mean()
    g = vol.garch_fit(x)
    p = g["params"]
    fc = vol.garch_forecast(p, x[-1], g["h"][-1], 252)
    T = np.array([1, 5, 21, 63, 252])
    term = np.sqrt(np.cumsum(fc)[T - 1] / T * 252)
    return _json({"btc_next": btc["next_vol"], "btc_month": btc["avg_vol"], "btc_beta": btc["beta"],
                  "btc_date": int(np.asarray(rz["ymd"])[-1]), "us_T": T, "us_term": term,
                  "us_long": float(np.sqrt(p[0] / (1 - g["persistence"]) * 252)), "us_date": int(d[-1])})


ITEMS = {"daily": compute_daily, "spurious": compute_spurious, "coint": compute_coint, "regimes": compute_regimes, "garch": compute_garch,
         "dcc": compute_dcc, "realized": compute_realized, "har": compute_har, "race": compute_race, "scaling": compute_scaling,
         "envelope": compute_envelope, "acf_arma": compute_acf_arma, "unitroot": compute_unitroot,
         "johansen": compute_johansen, "regimes_em": compute_regimes_em, "kalman": compute_kalman,
         "garch_lik": compute_garch_lik, "dcc_ell": compute_dcc_ell, "signature": compute_signature,
         "har_roll": compute_har_roll, "rough": compute_rough, "scoring": compute_scoring, "training": compute_training,
         "race2": compute_race2, "industry": compute_industry, "foundation": compute_foundation,
         "envelope2": compute_envelope2, "house_fc": compute_house_fc}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
