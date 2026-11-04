"""Every number in Part 26 (Backtesting Without Fooling Yourself), computed and cached in .cache/quant26/.

    python -m videos.quant.quant26.compute [items] [--force]

Research uses data to December 2020.  The technical rules are chosen on 1926-07 to 1986-12 (Sullivan, Timmermann and
White's in-sample era ends in 1986), checked on 1987-2020, and the best one is registered and opened once on the
sealed 2021-2025 daily market, in ``envelope``.

* ``lookahead``  a planted one-day look-ahead in a moving-average rule; GDP as first published against GDP as revised
                 (the Philadelphia Fed's real-time data), and a timing rule on each;
* ``survivor``   which of EDGAR's filers are still in the SEC's ticker file today, bankrupt or not; Brown, Goetzmann,
                 Ibbotson and Ross's survivorship, simulated;
* ``select``     the best Sharpe ratio of N noise strategies; the extreme-value formula; the minimum backtest length;
* ``engine``     the event-driven backtester against the vectorised one (EEM's one-day reversal); costs, borrow;
                 corporate actions (AAPL's 2020 split, SPY's dividends) handled and ignored;
* ``sharpe``     the Sharpe ratio's standard error: iid, non-normal (Cboe PutWrite), autocorrelated (Lo's eta);
* ``counter``    the trial counter before this part, by part, and the hurdle it implies;
* ``rules``      10,000 technical rules on the daily US market: in sample to 1986, out of sample 1987-2020;
* ``dsr``        the deflated Sharpe ratio of the best rule, with the trials' own variance and an effective N;
* ``pbo``        the probability of backtest overfitting by CSCV, for the rules in each era;
* ``cv``         a nearest-neighbour forecaster cross-validated four ways: shuffled, blocked, purged, walk-forward;
* ``rc``         White's reality check, Hansen's SPA and Romano-Wolf on the rules, in each era;
* ``monitor``    e-value monitors on 212 published predictors after publication, and e-BH across them;
* ``planted``    planted alpha in a simulated market: what each method finds, and what it invents;
* ``funding``    a capital ramp gated by an e-value monitor, for a real strategy and an overfitted one;
* ``envelope``   the best rule registered (10,000 trials) and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import inspect
import json
import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import backtest as B, martingale as MG, pit
from videos.quant.quant3.compute import _osap, _osap_matrix

CACHE = Cache("quant26")
load = pit.counted(CACHE.load, 26, items=("counter",))
IS_END = 19861231
RESEARCH_END = 20201231
N_RULES = 10_000
STRATEGY = "stw_best_rule_part26"
LAMS = (0.1, 0.2, 0.4, 0.6, 0.8, 0.95)   # the monitor's mixture of constant bets
WINSOR = 4.0                              # returns scaled (and winsorised) at four standard deviations


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _monthly(d, x):
    """Month-end values of a daily series (dates YYYYMMDD)."""
    ym = np.asarray(d) // 100
    last = np.r_[ym[1:] != ym[:-1], True]
    return ym[last], np.asarray(x)[last]


# ---------------------------------------------------------------------------
def compute_lookahead() -> dict:
    kf = data.ken_french_daily(through="2020-12-31")
    d, ex = kf["date"], kf["mkt"] - kf["rf"]
    P = np.cumprod(1 + kf["mkt"])
    m = d >= 19900101
    eng = B.RuleEngine(P)
    out = {}
    for key, rule in (("ma200", {"family": "ma", "fast": 1, "slow": 200, "band": 0.0, "delay": 0, "hold": 0}),
                      ("ma5", {"family": "ma", "fast": 1, "slow": 5, "band": 0.0, "delay": 0, "hold": 0})):
        pos = eng.positions(rule).astype(float)
        r1 = B.rule_returns(pos, ex)
        r0 = pos * ex
        ym, c1 = _monthly(d[m], np.cumprod(1 + r1[m]))
        _, c0 = _monthly(d[m], np.cumprod(1 + r0[m]))
        _, cb = _monthly(d[m], np.cumprod(1 + ex[m]))
        out[key] = {"label": B.rule_label(rule), "sr_honest": B.sharpe(r1[m], 252), "sr_bug": B.sharpe(r0[m], 252),
                    "ym": ym, "honest": c1, "bug": c0, "bh": cb, "in_market": float((pos[m] > 0).mean())}
    out["sr_bh"] = B.sharpe(ex[m], 252)

    # GDP: first release against the 2020 vintage
    g = data.philly_rtdsm()
    Q, V, A = g["quarters"], g["vintages"], g["values"]
    qi = {q: i for i, q in enumerate(Q)}
    last = V.index("2020M12")

    def gr(col, i):
        return 100 * ((A[i, col] / A[i - 1, col]) ** 4 - 1)
    i08 = qi["2008:Q4"]
    cols = [j for j in range(len(V)) if np.isfinite(A[i08, j])]
    path = {"vintage": [V[j] for j in cols], "growth": [gr(j, i08) for j in cols]}
    first, final, qs = [], [], []
    for q, i in qi.items():
        y = int(q[:4])
        if y < 1966 or y > 2019:
            continue
        cs = np.flatnonzero(np.isfinite(A[i, :]))
        if not len(cs) or not np.isfinite(A[i - 1, cs[0]]):
            continue
        first.append(gr(cs[0], i))
        final.append(gr(last, i))
        qs.append(q)
    first, final = np.array(first), np.array(final)

    # a timing rule: in the market next month if the latest GDP growth is positive
    kfm = data.ken_french_factors_monthly("2020-12")
    dm, exm = kfm["date"], kfm["mkt_rf"]
    rt, nv, tt = [], [], []
    for t, ym in enumerate(dm[:-1]):
        y, mo = divmod(int(ym), 100)
        if y < 1966:
            continue
        col = V.index(f"{y}M{mo}")
        i = np.flatnonzero(np.isfinite(A[:, col]))[-1]
        rt.append(gr(col, i))                                       # what was published by that month
        nv.append(gr(last, qi[f"{y}:Q{(mo - 1) // 3 + 1}"]))        # revised, merged on the quarter's first day
        tt.append(t)
    rt, nv, tt = np.array(rt), np.array(nv), np.array(tt)
    nxt = exm[tt + 1]
    timing = {"sr_realtime": B.sharpe((rt > 0) * nxt, 12), "sr_naive": B.sharpe((nv > 0) * nxt, 12),
              "sr_bh": B.sharpe(nxt, 12), "disagree": float(np.mean((rt > 0) != (nv > 0))),
              "first": int(dm[tt[0] + 1]), "last": int(dm[tt[-1] + 1])}
    out["gdp"] = {"q08": path, "first": first, "final": final, "quarters": qs,
                  "sign_changes": float(np.mean(np.sign(first) != np.sign(final))),
                  "mean_abs_rev": float(np.mean(np.abs(first - final))), "n": len(first),
                  "corr": float(np.corrcoef(first, final)[0, 1]), "timing": timing}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_survivor() -> dict:
    tick = data.sec_tickers()
    live = set(tick)
    bank = {}
    for y in range(2009, 2021):
        for r in data.sec_bankruptcy_8k(y):
            bank.setdefault(int(r[0]), y)
    by_year = {}
    for c, y in bank.items():
        n, k = by_year.get(y, (0, 0))
        by_year[y] = (n + 1, k + (c in live))
    floats = {}
    for y in range(2011, 2021):
        f = data.sec_frame("EntityPublicFloat", f"CY{y}Q2I", taxonomy="dei")
        pos = [c for c, v in f.items() if v[0] > 0]
        floats[y] = (len(pos), sum(c in live for c in pos))
    s = B.survivorship()
    r, a, sig = s["r"], s["alive"], s["sigma"]
    mean_all, mean_alive = r.mean(1), r[a].mean(1)
    bins = np.linspace(0.05, 0.35, 7)
    vb = [{"lo": float(lo), "hi": float(hi), "alive": float(a[(sig >= lo) & (sig < hi)].mean()),
           "mean_alive": float(r[a & (sig >= lo) & (sig < hi)].mean())} for lo, hi in zip(bins[:-1], bins[1:])]
    nb = sum(n for n, _ in by_year.values())
    kb = sum(k for _, k in by_year.values())
    return _json({"bank_by_year": {str(y): v for y, v in sorted(by_year.items())}, "bank_n": nb, "bank_live": kb,
                  "bank_share": kb / nb, "floats": {str(y): v for y, v in floats.items()},
                  "float12_share": floats[2012][1] / floats[2012][0], "n_tickers": len(tick),
                  "sim": {"n": len(a), "alive": float(a.mean()), "mean_all": float(r.mean()),
                          "mean_alive": float(r[a].mean()), "hist_all": np.histogram(mean_all, 40, (-0.3, 0.3))[0],
                          "hist_alive": np.histogram(mean_alive, 40, (-0.3, 0.3))[0], "by_vol": vb,
                          "years": r.shape[1], "cut": -0.3}})


# ---------------------------------------------------------------------------
def compute_select() -> dict:
    T = 1260
    ns = [1, 10, 100, 1000, 10000]
    dist = {}
    for n in ns:
        x = B.noise_max_sr(n, T, sims=2000, seed=n) * math.sqrt(252)
        h, e = np.histogram(x, 60, (-1.5, 3.0), density=True)
        dist[str(n)] = {"mean": float(x.mean()), "q05": float(np.quantile(x, 0.05)),
                        "q95": float(np.quantile(x, 0.95)), "hist": h, "edges": e}
    grid = np.unique(np.round(np.logspace(0, 6, 61)))
    evt = [B.expected_max_sr(n, 1 / T) * math.sqrt(252) for n in grid]
    btl = {str(s): [B.min_btl(n, s) for n in grid] for s in (0.5, 1.0, 2.0)}
    n45 = next(n for n in range(2, 1000) if B.min_btl(n, 1.0) > 5.0) - 1
    return _json({"T": T, "dist": dist, "grid": grid, "evt": evt, "btl": btl, "n_5y_sr1": n45,
                  "btl_45": B.min_btl(45, 1.0)})


# ---------------------------------------------------------------------------
def _raw_aapl():
    """AAPL as traded in 2020: Yahoo's split-adjusted bars un-adjusted before the 4:1 split of 31 August."""
    b = data.yahoo_bars("AAPL", "2019-12-01", "2020-12-31")
    k = int(np.flatnonzero(b["split"] != 1)[0])
    f = np.where(np.arange(len(b["date"])) < k, b["split"][k], 1.0)
    raw = {"date": b["date"], "open": b["open"] * f, "high": b["high"] * f, "low": b["low"] * f,
           "close": b["close"] * f, "volume": b["volume"] / f, "dividend": b["dividend"] * f, "split": b["split"]}
    return raw, k


def compute_engine() -> dict:
    b = data.yahoo_bars("EEM")
    c = b["adjclose"]
    r = np.concatenate([[0.0], c[1:] / c[:-1] - 1])
    w = -np.sign(r)
    vec = B.vectorized(w, c, 0.0, 1)
    o = b["open"] * b["adjclose"] / b["close"]
    on = np.zeros(len(c))
    on[1:] = w[:-1] * (o[1:] / c[:-1] - 1)
    intra = np.zeros(len(c))
    intra[1:] = w[:-1] * (c[1:] / o[1:] - 1)

    def strat(view):
        cl = view["close"]
        return -float(np.sign(cl[-1] / cl[-2] - 1)) if len(cl) > 1 else None
    runs = {}
    specs = [("close_now", 0, "close", B.Costs()), ("open_next", 1, "open", B.Costs()),
             ("spread", 1, "open", B.Costs(half_spread_bps=1.0)),
             ("all", 1, "open", B.Costs(half_spread_bps=1.0, impact=0.1, commission_per_share=0.005,
                                        borrow_bps_year=30))]
    for key, lat, fill, cost in specs:
        res = B.Backtester(b, strat, latency=lat, fill=fill, costs=cost).run()
        ym, eq = _monthly(b["date"], res.equity / res.equity[0])
        yrs = (len(b["date"]) - 1) / 252
        runs[key] = {"sr": B.sharpe(res.returns, 252), "cagr": (res.equity[-1] / res.equity[0]) ** (1 / yrs) - 1,
                     "ym": ym, "eq": eq, "costs": res.costs, "trades": len(res.trades)}
    ym, ve = _monthly(b["date"], np.cumprod(1 + vec))
    vector = {"sr": B.sharpe(vec, 252), "ym": ym, "eq": ve, "sr_overnight": B.sharpe(on, 252),
              "sr_intraday": B.sharpe(intra, 252)}

    # corporate actions
    raw, k = _raw_aapl()
    hold = lambda view: 1.0  # noqa: E731
    ok = B.Backtester(raw, hold, latency=1, fill="open").run()
    bad = B.Backtester(raw, hold, latency=1, fill="open", adjust_splits=False).run()
    mom = np.zeros(len(raw["close"]))
    mom[20:] = np.sign(raw["close"][20:] / raw["close"][:-20] - 1)
    adj = data.yahoo_bars("AAPL", "2019-12-01", "2020-12-31")["close"]
    mom_ok = np.zeros(len(adj))
    mom_ok[20:] = np.sign(adj[20:] / adj[:-20] - 1)
    split = {"date": raw["date"], "raw": raw["close"], "adj": adj, "k": k, "ok": ok.equity / ok.equity[0],
             "bad": bad.equity / bad.equity[0], "split_day": int(raw["date"][k]),
             "fake_return": float(raw["close"][k] / raw["close"][k - 1] - 1),
             "mom_raw_flat_days": int(np.sum((mom != mom_ok)[20:])),
             "mom_raw_first_wrong": int(raw["date"][20 + int(np.flatnonzero((mom != mom_ok)[20:])[0])])
             if np.any((mom != mom_ok)[20:]) else None}
    spy = data.yahoo_bars("SPY")
    yrs = (len(spy["date"]) - 1) / 252
    div = {"price_cagr": (spy["close"][-1] / spy["close"][0]) ** (1 / yrs) - 1,
           "total_cagr": (spy["adjclose"][-1] / spy["adjclose"][0]) ** (1 / yrs) - 1,
           "dividends": float(spy["dividend"].sum()), "n_div": int((spy["dividend"] > 0).sum())}
    return _json({"symbol": "EEM", "first": int(b["date"][0]), "last": int(b["date"][-1]), "vector": vector,
                  "runs": runs, "split": split, "div": div, "turnover": float(np.abs(np.diff(w)).sum() / yrs)})


# ---------------------------------------------------------------------------
def compute_sharpe() -> dict:
    kfm = data.ken_french_factors_monthly("2020-12")
    x = kfm["mkt_rf"]
    mkt = {"sr": B.sharpe(x, 12), "se": B.sharpe_se(x) * math.sqrt(12),
           "se_nn": B.sharpe_se(x, "nonnormal") * math.sqrt(12), "years": len(x) / 12,
           "skew": float(stats.skew(x)), "kurt": float(stats.kurtosis(x, fisher=False))}
    p = data.cboe_index("PUT", through="2020-12-31")
    k = p["date"] >= 20061229
    _, mc = _monthly(p["date"][k], p["close"][k])
    pr = mc[1:] / mc[:-1] - 1
    rf = kfm["rf"][kfm["date"] >= 200701]
    pe = pr - rf[: len(pr)]
    put = {"sr": B.sharpe(pe, 12), "se": B.sharpe_se(pe) * math.sqrt(12),
           "se_nn": B.sharpe_se(pe, "nonnormal") * math.sqrt(12), "skew": float(stats.skew(pe)),
           "kurt": float(stats.kurtosis(pe, fisher=False)), "months": len(pe)}
    # Lo: smoothed (illiquid) returns overstate the annualised Sharpe ratio
    rng = np.random.default_rng(26)
    true_m, sr_true = 1.0 / math.sqrt(12), 1.0
    e = rng.standard_normal(600_000) + true_m * 0 + sr_true / math.sqrt(12)
    wts = np.array([0.5, 0.3, 0.2])
    sm = np.convolve(e, wts, mode="valid")
    rho = [float(np.corrcoef(sm[:-q], sm[q:])[0, 1]) for q in range(1, 12)]
    sr_m = B.sharpe(sm)
    smooth = {"weights": wts, "rho": rho, "naive": sr_m * math.sqrt(12), "lo": sr_m * B.lo_eta(rho, 12),
              "true": sr_true}
    smooth["overstated"] = smooth["naive"] / smooth["lo"] - 1
    # years needed for 2 standard errors, by Sharpe ratio
    srs = np.linspace(0.2, 2.0, 37)
    yrs = [4 * (1 + (s / math.sqrt(12)) ** 2 / 2) / (s / math.sqrt(12)) ** 2 / 12 for s in srs]
    # simulated sampling distribution of the Sharpe estimate: 5 years monthly, true 0.5
    sims = np.array([B.sharpe(rng.normal(0.5 / math.sqrt(12), 1, 60), 12) for _ in range(20000)])
    return _json({"mkt": mkt, "put": put, "smooth": smooth, "srs": srs, "years_2se": yrs,
                  "sim": {"hist": np.histogram(sims, 60, (-1.5, 2.5), density=True)[0], "edges": np.linspace(-1.5, 2.5, 61),
                          "sd": float(sims.std()), "formula": math.sqrt((1 + (0.5 / math.sqrt(12)) ** 2 / 2) / 60) * math.sqrt(12),
                          "neg": float(np.mean(sims < 0))}})


# ---------------------------------------------------------------------------
def compute_counter() -> dict:
    reg = pit._read()["registered"]
    parts = {}
    for k, r in reg.items():
        p = pit.PARTS[k][0]
        if p < 26:
            parts[p] = parts.get(p, 0) + r["trials"]
    before = sum(parts.values())
    T = 2520
    grid = np.unique(np.round(np.logspace(0, 5, 51)))
    hurdle = [B.expected_max_sr(n, 1 / T) * math.sqrt(252) for n in grid]
    return _json({"parts": {str(p): v for p, v in sorted(parts.items())}, "before": before, "T_years": T / 252,
                  "grid": grid, "hurdle": hurdle, "at_before": B.expected_max_sr(before, 1 / T) * math.sqrt(252),
                  "at_after": B.expected_max_sr(before + N_RULES, 1 / T) * math.sqrt(252), "trials": before})


# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=1)
def _rule_matrix():
    """The 10,000 rules' daily excess returns (float32), 1926-07 to 2020-12, and the market's."""
    kf = data.ken_french_daily(through="2020-12-31")
    d, ex = kf["date"], kf["mkt"] - kf["rf"]
    P = np.cumprod(1 + kf["mkt"])
    rules = B.random_rules(N_RULES, seed=26)
    eng = B.RuleEngine(P)
    R = np.empty((len(d), len(rules)), np.float32)
    for j, r in enumerate(rules):
        R[:, j] = B.rule_returns(eng.positions(r), ex)
    return d, ex, rules, R


def _sr(X):
    """Per-period Sharpe ratios of the columns of X; a rule that never holds a position scores 0 (it is cash)."""
    mu = X.mean(0, dtype=np.float64)
    sd = X.std(0, ddof=1, dtype=np.float64)
    return np.where(sd > 0, mu / np.where(sd > 0, sd, 1.0), 0.0)


def _eras(d):
    return {"in": (d > d[0]) & (d <= IS_END), "out": (d > IS_END) & (d <= RESEARCH_END)}


def compute_rules() -> dict:
    d, ex, rules, R = _rule_matrix()
    out = {}
    sr = {}
    for era, m in _eras(d).items():
        sr[era] = _sr(R[m]) * math.sqrt(252)
        out[era] = {"first": int(d[m][0]), "last": int(d[m][-1]), "T": int(m.sum()), "sr_bh": B.sharpe(ex[m], 252),
                    "n_pos": int((sr[era] > 0).sum()), "n_beat_bh": int((sr[era] > B.sharpe(ex[m], 252)).sum()),
                    "hist": np.histogram(sr[era], 70, (-1.5, 2.0))[0]}
    best = int(np.argmax(sr["in"]))
    fam = {}
    for f in B.FAMILIES:
        idx = [j for j, r in enumerate(rules) if r["family"] == f]
        j = idx[int(np.argmax(sr["in"][idx]))]
        fam[f] = {"n": len(idx), "best": B.rule_label(rules[j]), "sr_in": float(sr["in"][j]),
                  "sr_out": float(sr["out"][j]), "mean_in": float(np.mean(sr["in"][idx])),
                  "mean_out": float(np.mean(sr["out"][idx]))}
    top = np.argsort(sr["in"])[::-1][:10]
    curves = {}
    for era, m in _eras(d).items():
        ym, cb = _monthly(d[m], np.cumprod(1 + R[m, best].astype(np.float64)))
        _, cm = _monthly(d[m], np.cumprod(1 + ex[m]))
        curves[era] = {"ym": ym, "best": cb, "mkt": cm}
    rng = np.random.default_rng(0)
    samp = rng.choice(len(rules), 1500, replace=False)
    return _json({"n": len(rules), "best": best, "best_label": B.rule_label(rules[best]), "best_rule": rules[best],
                  "best_in": float(sr["in"][best]), "best_out": float(sr["out"][best]),
                  "rank_out_of_best": int((sr["out"] > sr["out"][best]).sum()) + 1,
                  "top10": [{"label": B.rule_label(rules[j]), "in": float(sr["in"][j]), "out": float(sr["out"][j])}
                            for j in top],
                  "corr": float(np.corrcoef(sr["in"], sr["out"])[0, 1]),
                  "rank_corr": float(stats.spearmanr(sr["in"], sr["out"])[0]),
                  "eras": out, "families": fam, "curves": curves,
                  "scatter": {"in": sr["in"][samp], "out": sr["out"][samp]},
                  "share_out_below_half": float(np.mean(sr["out"][top] < 0.5 * sr["in"][top]))})


def compute_acf() -> dict:
    """The daily market's first-order autocorrelation by decade: the stale prices of thinly traded stocks make an
    index's daily returns positively autocorrelated (Fisher 1966; Lo and MacKinlay 1990)."""
    kf = data.ken_french_daily(through="2020-12-31")
    d, ex = kf["date"], kf["mkt"] - kf["rf"]
    out = []
    for y0 in range(1930, 2021, 10):
        m = (d >= y0 * 10000) & (d < (y0 + 10) * 10000)
        x = ex[m]
        if len(x) > 1000:   # whole decades only (2020 alone is one extraordinary year)
            out.append({"decade": y0, "rho1": float(np.corrcoef(x[:-1], x[1:])[0, 1])})
    m = d < 19300101
    x = ex[m]
    out.insert(0, {"decade": 1926, "rho1": float(np.corrcoef(x[:-1], x[1:])[0, 1])})
    return _json({"rows": out})


def compute_dsr() -> dict:
    d, ex, rules, R = _rule_matrix()
    res = {}
    for era, m in _eras(d).items():
        X = R[m].astype(np.float64)
        T = X.shape[0]
        sr = _sr(X)                                             # per day
        j = int(np.argmax(sr))
        x = X[:, j]
        g3, g4 = float(stats.skew(x)), float(stats.kurtosis(x, fisher=False))
        var = float(sr.var(ddof=1))
        rng = np.random.default_rng(1)
        live = np.flatnonzero(X.std(0) > 0)
        samp = rng.choice(live, 1500, replace=False)
        ev = np.linalg.eigvalsh(np.nan_to_num(np.corrcoef(X[:, samp].T)))
        n_eff_share = float(ev.sum() ** 2 / (ev ** 2).sum()) / len(samp)
        n_eff = n_eff_share * X.shape[1]
        out = {"T": T, "label": B.rule_label(rules[j]), "sr_best": float(sr[j] * math.sqrt(252)), "skew": g3,
               "kurt": g4, "var_trials": var, "sd_trials_ann": math.sqrt(var * 252), "psr0": B.psr(sr[j], 0.0, T, g3, g4),
               "n": X.shape[1], "n_eff": n_eff, "n_eff_share": n_eff_share,
               "sr_hist": np.histogram(sr * math.sqrt(252), 70, (-1.5, 2.0))[0]}
        for key, n in (("raw", X.shape[1]), ("eff", n_eff)):
            r = B.deflated_sharpe(sr[j], T, n, var, g3, g4)
            out[key] = {"n": n, "sr0": r["sr0"] * math.sqrt(252), "dsr": r["dsr"]}
        r = B.deflated_sharpe(sr[j], T, X.shape[1], 1 / T, g3, g4)
        out["noise"] = {"sr0": r["sr0"] * math.sqrt(252), "dsr": r["dsr"]}
        grid = np.unique(np.round(np.logspace(0, 4, 41)))
        out["grid"] = grid
        out["dsr_curve"] = [B.deflated_sharpe(sr[j], T, n, var, g3, g4)["dsr"] for n in grid]
        out["sr0_curve"] = [B.expected_max_sr(n, var) * math.sqrt(252) for n in grid]
        res[era] = out
        del X
    return _json(res)


def compute_pbo() -> dict:
    d, ex, rules, R = _rule_matrix()
    out = {}
    for era, m in _eras(d).items():
        c = B.cscv(R[m], S=16)
        rng = np.random.default_rng(2)
        k = rng.choice(c["n_combos"], 800, replace=False)
        slope = float(np.polyfit(c["is_sr"], c["oos_sr"], 1)[0])
        out[era] = {"pbo": c["pbo"], "n_combos": c["n_combos"],
                    "logit_hist": np.histogram(c["logits"], 40, (-8, 8))[0],
                    "is_sr": c["is_sr"][k] * math.sqrt(252), "oos_sr": c["oos_sr"][k] * math.sqrt(252),
                    "mean_is": float(c["is_sr"].mean() * math.sqrt(252)),
                    "mean_oos": float(c["oos_sr"].mean() * math.sqrt(252)), "slope": slope,
                    "oos_loss": float(np.mean(c["oos_sr"] < 0)), "median_logit": float(np.median(c["logits"]))}
    return _json(out)


def compute_rc() -> dict:
    d, ex, rules, R = _rule_matrix()
    out = {}
    for era, m in _eras(d).items():
        X = R[m]
        T = X.shape[0]
        mean = X.mean(0, dtype=np.float64)
        sd = X.std(0, ddof=1, dtype=np.float64)
        sd = np.where(sd > 0, sd, 1.0)          # a rule that never trades has mean 0 and t = 0
        counts = B.stationary_bootstrap_counts(T, 500, 10.0, seed=26)
        bm = B.boot_means(X, counts)
        rc = B.reality_check(mean, bm, T)
        sp = B.spa(mean, bm, sd, T)
        rw = B.romano_wolf(mean, bm, sd, T, 0.05)
        t = math.sqrt(T) * mean / sd
        j = int(np.argmax(t))
        Vb = math.sqrt(T) * (bm - mean).max(axis=1)
        out[era] = {"T": T, "rc_p": rc["p"], "spa_p": sp["p"], "rw_n": int(len(rw["rejected"])),
                    "rw_crit": rw["crit"], "best_t": float(t[j]), "best_label": B.rule_label(rules[j]),
                    "nominal_p": float(1 - stats.norm.cdf(t[j])), "n_t2": int((t > 1.96).sum()),
                    "V": rc["V"], "Vb_q95": float(np.quantile(Vb, 0.95)),
                    "Vb_hist": np.histogram(Vb, 50)[0], "Vb_edges": np.histogram(Vb, 50)[1],
                    "rw_families": {f: int(sum(rules[i]["family"] == f for i in rw["rejected"])) for f in B.FAMILIES}}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_cv() -> dict:
    kf = data.ken_french_daily(through="2020-12-31")
    d, ex = kf["date"], kf["mkt"] - kf["rf"]
    m = d >= 19630701
    x = ex[m]
    n, h = len(x), 20
    lx = np.log1p(x)
    c = np.concatenate([[0.0], np.cumsum(lx)])
    idx = np.arange(60, n - h)
    fwd = c[idx + 1 + h] - c[idx + 1]
    vol = np.array([lx[i - 19:i + 1].std() for i in idx])
    feat = np.column_stack([c[idx + 1] - c[idx + 1 - k] for k in (1, 5, 20, 60)] + [vol])
    feat = (feat - feat.mean(0)) / feat.std(0)

    def knn(tr, te, k=25):
        Xtr, out = feat[tr], []
        for a in range(0, len(te), 400):
            D = ((feat[te[a:a + 400]][:, None, :] - Xtr[None, :, :]) ** 2).sum(-1)
            nn = np.argpartition(D, k, axis=1)[:, :k]
            out.append(fwd[tr][nn].mean(1))
        return np.concatenate(out)
    t0, t1 = idx, idx + h
    res = {}
    for name, folds, splits in (("shuffled", 5, B.kfold(len(idx), 5, True)), ("blocked", 5, B.kfold(len(idx), 5, False)),
                                ("purged", 5, B.purged_kfold(t0, t1, 5, embargo=h)),
                                ("blocked20", 20, B.kfold(len(idx), 20, False)),
                                ("purged20", 20, B.purged_kfold(t0, t1, 20, embargo=h)),
                                ("walk", 0, B.walk_forward(len(idx), 2520, 1260))):
        sse = sst = hit = N = 0
        dropped = []
        for tr, te in splits:
            p = knn(tr, te)
            mu, med = fwd[tr].mean(), np.median(fwd[tr])
            sse += ((fwd[te] - p) ** 2).sum()
            sst += ((fwd[te] - mu) ** 2).sum()
            hit += ((p > med) == (fwd[te] > med)).sum()
            N += len(te)
            dropped.append(len(idx) - len(tr) - len(te))
        res[name] = {"r2": 1 - sse / sst, "hit": hit / N, "folds": folds, "dropped": float(np.mean(dropped))}
    # how close is a test day's nearest neighbour in time, under shuffling?
    rng = np.random.default_rng(0)
    te = np.sort(rng.choice(len(idx), 400, replace=False))
    tr = np.setdiff1d(np.arange(len(idx)), te)
    D = ((feat[te][:, None, :] - feat[tr][None, :, :]) ** 2).sum(-1)
    nn = tr[np.argmin(D, axis=1)]
    gap = np.abs(nn - te)
    return _json({"n": len(idx), "h": h, "first": int(d[m][60]), "last": int(d[m][n - h - 1]), "res": res,
                  "nn_gap_median": float(np.median(gap)), "nn_gap_within_h": float(np.mean(gap <= h))})


# ---------------------------------------------------------------------------
def compute_monitor() -> dict:
    ym, names, R = _osap_matrix()
    _, doc = _osap()
    y = ym // 100
    lams = LAMS
    recs = []
    for j, c in enumerate(names):
        dd = doc.get(c)
        try:
            s0, s1, py = int(float(dd["SampleStartYear"])), int(float(dd["SampleEndYear"])), int(float(dd["Year"]))
        except (TypeError, ValueError, KeyError):
            continue
        x = R[:, j]
        ins = x[(y >= s0) & (y <= s1) & np.isfinite(x)]
        pm = (y > py) & (ym <= 202012) & np.isfinite(x)
        post = x[pm]
        if len(ins) < 24 or len(post) < 12:
            continue
        m_in, sd = float(ins.mean()), float(ins.std(ddof=1))
        if m_in <= 0:
            continue
        cap = WINSOR * sd
        row = {"name": c, "year": py, "m_in": m_in, "t_in": m_in / sd * math.sqrt(len(ins)), "n_post": int(len(post)),
               "m_post": float(post.mean()), "ym": ym[pm]}
        for key, target in (("full", m_in), ("half", 0.5 * m_in)):
            z = (target - post) / cap
            row[f"clip_{key}"] = float(np.mean(np.abs(z) >= 0.99))
            ep = MG.EProcess(lams=lams).run(np.clip(z, -0.99, 0.99))
            row[f"e_{key}"] = float(ep[-1])
            row[f"max_{key}"] = float(ep.max())
            hit = np.flatnonzero(ep[1:] >= 20)
            row[f"flag_{key}"] = int(ym[pm][hit[0]]) if len(hit) else None
            row[f"path_{key}"] = ep
        recs.append(row)
    out = {"n": len(recs)}
    for key in ("full", "half"):
        e = np.array([r[f"e_{key}"] for r in recs])
        rej = MG.e_bh(e, 0.1)
        out[key] = {"flagged": int(sum(r[f"flag_{key}"] is not None for r in recs)), "ebh": int(len(rej)),
                    "clip": float(np.mean([r[f"clip_{key}"] for r in recs])),
                    "years_to_flag": [(r[f"flag_{key}"] // 100 - r["year"]) for r in recs if r[f"flag_{key}"]]}
    # two examples: a strong predictor flagged early, and one the monitor never doubted
    fl = sorted([r for r in recs if r["flag_full"]], key=lambda r: -r["t_in"])
    ok = sorted([r for r in recs if not r["max_full"] >= 5], key=lambda r: -r["n_post"])
    ex = {}
    for k, r in (("flagged", fl[0] if fl else None), ("kept", ok[0] if ok else None)):
        if r:
            ex[k] = {kk: r[kk] for kk in ("name", "year", "m_in", "t_in", "m_post", "n_post", "flag_full", "e_full",
                                           "max_full")}
            ex[k]["ym"] = r["ym"]
            ex[k]["path"] = np.log10(np.maximum(r["path_full"][1:], 1e-6))
            ex[k]["cum"] = np.cumsum(R[np.isin(ym, r["ym"]), names.index(r["name"])])
            ex[k]["long"] = doc[r["name"]].get("LongDescription", r["name"])
    out["examples"] = ex
    out["table"] = [{k: r[k] for k in ("name", "year", "t_in", "m_in", "m_post", "e_full", "e_half", "flag_full",
                                         "flag_half")} for r in recs]
    return _json(out)


# ---------------------------------------------------------------------------
def compute_planted() -> dict:
    sims, n, n_true, T = 40, 1000, 10, 1260
    rows = {}
    for sr_true in (1.0, 2.0):
        acc = {k: [] for k in ("naive", "bonferroni", "rw", "dsr_best", "best_true")}
        for s in range(sims):
            mk = B.planted_market(n, n_true, sr_true, T, rho=0.2, seed=1000 * int(sr_true) + s)
            Rm, pl = mk["R"], mk["planted"]
            mean, sd = Rm.mean(0), Rm.std(0, ddof=1)
            t = math.sqrt(T) * mean / sd
            naive = t > 1.96
            bon = t > stats.norm.ppf(1 - 0.05 / n)
            counts = B.stationary_bootstrap_counts(T, 300, 5.0, seed=s)
            bm = B.boot_means(Rm, counts)
            rwj = np.zeros(n, bool)
            rwj[B.romano_wolf(mean, bm, sd, T, 0.05)["rejected"]] = True
            j = int(np.argmax(t))
            srp = mean / sd
            dsr = B.deflated_sharpe(srp[j], T, n, float(srp.var(ddof=1)))["dsr"]
            for k, sel in (("naive", naive), ("bonferroni", bon), ("rw", rwj)):
                acc[k].append((int((sel & pl).sum()), int((sel & ~pl).sum())))
            acc["dsr_best"].append((dsr > 0.95, bool(pl[j])))
            acc["best_true"].append(bool(pl[j]))
        rows[str(sr_true)] = {k: {"true": float(np.mean([a for a, _ in v])), "false": float(np.mean([b for _, b in v]))}
                              for k, v in acc.items() if k in ("naive", "bonferroni", "rw")}
        dv = acc["dsr_best"]
        rows[str(sr_true)]["dsr"] = {"pass": float(np.mean([a for a, _ in dv])),
                                     "pass_and_true": float(np.mean([a and b for a, b in dv])),
                                     "pass_and_false": float(np.mean([a and not b for a, b in dv]))}
        rows[str(sr_true)]["best_is_true"] = float(np.mean(acc["best_true"]))
    # one market to draw
    mk = B.planted_market(n, n_true, 1.0, T, rho=0.2, seed=7)
    t = math.sqrt(T) * mk["R"].mean(0) / mk["R"].std(0, ddof=1)
    return _json({"sims": sims, "n": n, "n_true": n_true, "T": T, "rows": rows,
                  "example": {"t": t, "planted": mk["planted"]}})


# ---------------------------------------------------------------------------
def _ramp(true_sr, seed, months=60, bt_sr=1.5, vol=0.10, share=1.0):
    """A capital ramp: six months of paper trading, then 10% of the target capital, raised by 15 points a quarter
    to 100%, unless the monitor (H0: the true Sharpe ratio is at least ``share`` of the backtest's) reaches 20,
    which ends it."""
    rng = np.random.default_rng(seed)
    r = rng.normal(true_sr * vol / 12, vol / math.sqrt(12), months)
    target = share * bt_sr * vol / 12
    ep = MG.EProcess(lams=LAMS)
    cap, frac, stopped, pnl = [], 0.0, None, 0.0
    for t in range(months):
        if stopped is None:
            if t == 6:
                frac = 0.1
            elif t > 6 and (t - 6) % 3 == 0:
                frac = min(1.0, frac + 0.15)
        cap.append(frac)
        pnl += frac * r[t]
        e = ep.update(float(np.clip((target - r[t]) / (WINSOR * vol / math.sqrt(12)), -0.99, 0.99)))
        if stopped is None and e >= 20:
            stopped, frac = t, 0.0
    return np.array(cap), stopped, pnl, np.cumsum(r)


def compute_funding() -> dict:
    out = {}
    for share in (1.0, 0.5):
        for key, sr in (("real", 1.0), ("overfit", 0.0)):
            caps, stops, pnls, full = [], [], [], []
            for s in range(1000):
                c, st, p, cum = _ramp(sr, 10_000 * (key == "real") + s, share=share)
                caps.append(c)
                stops.append(st)
                pnls.append(p)
                full.append(cum[-1])
            caps = np.array(caps)
            st = [s for s in stops if s is not None]
            out[f"{key}_{share:g}"] = {"mean_cap": caps.mean(0), "stopped": len(st) / len(stops),
                                       "stop_hist": np.bincount(st, minlength=60) if st else np.zeros(60, int),
                                       "median_stop": float(np.median(st)) if st else None,
                                       "pnl_ramp": float(np.mean(pnls)), "pnl_full": float(np.mean(full)),
                                       "examples": caps[:6], "capital_months": float(caps.sum(1).mean())}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    r = load("rules")
    rule = r["best_rule"]
    code = inspect.getsource(B.RuleEngine) + inspect.getsource(B._apply) + inspect.getsource(B._filter_trig) + \
        inspect.getsource(B.rule_returns)
    pit.register(STRATEGY, code, {"rule": rule, "selected_on": "1926-07..1986-12, max Sharpe of 10,000 rules",
                                  "returns": "position at close t times the next day's market excess return"},
                 trials=N_RULES)
    kf = data.ken_french_daily(through="2025-12-31")
    d = kf["date"]
    hd, hm = pit.open_envelope(STRATEGY, "kenfrench/mkt_daily", d, kf["mkt"])
    _, hr = pit.open_envelope(STRATEGY, "kenfrench/rf_daily", d, kf["rf"])
    keep = d < pit.HOLDOUT_START
    dd = np.concatenate([d[keep], hd])
    mkt = np.concatenate([kf["mkt"][keep], hm])
    rf = np.concatenate([kf["rf"][keep], hr])
    pos = B.rule_positions(np.cumprod(1 + mkt), rule)
    ret = B.rule_returns(pos, mkt - rf)
    h = dd >= pit.HOLDOUT_START
    o = (dd > IS_END) & (dd <= RESEARCH_END)
    i = (dd <= IS_END) & (dd > dd[0])
    ym, ce = _monthly(dd[h], np.cumprod(1 + ret[h]))
    _, cm = _monthly(dd[h], np.cumprod(1 + (mkt - rf)[h]))
    rule_label = B.rule_label(rule)
    return _json({"label": rule_label, "sr_in": B.sharpe(ret[i], 252), "sr_out": B.sharpe(ret[o], 252),
                  "sr_hold": B.sharpe(ret[h], 252), "sr_bh_hold": B.sharpe((mkt - rf)[h], 252),
                  "se_hold": B.sharpe_se(ret[h]) * math.sqrt(252), "in_market": float(np.mean(pos[h] > 0)),
                  "short": float(np.mean(pos[h] < 0)), "ym": ym, "eq": ce, "mkt": cm, "first": int(dd[h][0]),
                  "last": int(dd[h][-1]), "trials": pit.trials_so_far(), "n_trials": N_RULES})


# ---------------------------------------------------------------------------
def _tn_cdf(x, mu, s, lo, hi):
    """P(X <= x) for X ~ N(mu, s^2) truncated to [lo, hi]."""
    return float(stats.truncnorm.cdf(x, (lo - mu) / s, (hi - mu) / s, loc=mu, scale=s))


def _invert(x, s, lo, hi, p, width=60.0):
    """The mu at which the truncated normal puts probability p below x (the cdf falls as mu rises)."""
    from scipy.optimize import brentq
    g = lambda m_: _tn_cdf(x, m_, s, lo, hi) - p  # noqa: E731
    a, b = x - width * s, x + width * s
    if g(a) < 0:
        return float(a)
    if g(b) > 0:
        return float(b)
    return float(brentq(g, a, b, xtol=1e-6 * s))


def _winner_inference(X, s, rho, j, c_beta, alpha=0.05, beta=0.005):
    """Andrews, Kitagawa and McCloskey's inference on the winner j = argmax X, for X ~ N(mu, s^2 C) with C[:, j] = rho.

    Conditional on the winner and on Z = X - rho X_j (independent of X_j), X_j is N(mu_j, s^2) truncated to
    [L, U], L = max over k with rho_k < 1 of Z_k/(1 - rho_k).  Inverting its cdf gives a median-unbiased estimate and an
    equal-tailed interval with exact conditional coverage.  The hybrid also conditions on mu_j lying in the level-beta
    projection interval X_j +- c_beta s, which keeps it no wider than projection."""
    keep = (np.arange(len(X)) != j) & (rho < 1 - 1e-9)
    Z = X[keep] - rho[keep] * X[j]
    L = float(np.max(Z / (1 - rho[keep]))) if keep.any() else -np.inf
    U = np.inf
    x = float(X[j])
    cond = (_invert(x, s, L, U, 1 - alpha / 2), _invert(x, s, L, U, alpha / 2))
    med = _invert(x, s, L, U, 0.5)
    lo_p, hi_p = x - c_beta * s, x + c_beta * s
    at = (alpha - beta) / (1 - beta)
    grid = np.linspace(lo_p, hi_p, 801)
    lo_t, hi_t = np.maximum(L, grid - c_beta * s), np.minimum(U, grid + c_beta * s)
    F = stats.truncnorm.cdf(x, (lo_t - grid) / s, (hi_t - grid) / s, loc=grid, scale=s)
    ok = (F >= at / 2) & (F <= 1 - at / 2)
    hyb = (float(grid[ok].min()), float(grid[ok].max())) if ok.any() else (x, x)
    k = int(np.argmin(np.abs(F - 0.5)))
    return {"x": x, "L": L, "gap": (x - L) / s, "naive": (x - 1.96 * s, x + 1.96 * s), "cond": cond, "med": med,
            "hybrid": hyb, "hyb_med": float(grid[k]), "proj": (lo_p, hi_p)}


def compute_winners() -> dict:
    """The research chapter: inference on winners (Andrews, Kitagawa and McCloskey 2024).  The best of many backtests
    is biased up; conditioning on its having won turns its estimate into a truncated normal whose cdf can be inverted.
    Checked by simulation (coverage, median bias, length), then applied to the best of the 10,000 rules, chosen on
    1926-86 and on 1987-2003, against what each earned afterwards."""
    rng = np.random.default_rng(2626)
    # ---- simulation: J equicorrelated estimates with known variance
    J, rho0, reps = 50, 0.5, 4000
    C = np.full((J, J), rho0) + (1 - rho0) * np.eye(J)
    Lc = np.linalg.cholesky(C)
    xi = rng.standard_normal((20000, J)) @ Lc.T
    c_beta = float(np.quantile(np.abs(xi).max(1), 1 - 0.005))
    c_95 = float(np.quantile(np.abs(xi).max(1), 0.95))
    configs = {"all zero": np.zeros(J), "one clear winner": np.r_[3.0, np.zeros(J - 1)],
               "spread 0 to 2": np.linspace(0, 2, J)}
    sims = {}
    for name, mu in configs.items():
        rec = {k: [] for k in ("naive", "cond", "hybrid", "proj")}
        bias_naive, bias_med, length = [], [], {k: [] for k in rec}
        for _ in range(reps):
            X = mu + rng.standard_normal(J) @ Lc.T
            j = int(np.argmax(X))
            r = _winner_inference(X, 1.0, np.full(J, rho0), j, c_beta)
            r["proj"] = (r["x"] - c_95, r["x"] + c_95)
            for k in rec:
                rec[k].append(r[k][0] <= mu[j] <= r[k][1])
                length[k].append(r[k][1] - r[k][0])
            bias_naive.append(r["x"] - mu[j])
            bias_med.append(r["med"] - mu[j])
        sims[name] = {"cover": {k: float(np.mean(v)) for k, v in rec.items()},
                      "length": {k: float(np.median(v)) for k, v in length.items()},
                      "bias_naive": float(np.mean(bias_naive)), "medbias_naive": float(np.median(bias_naive)),
                      "medbias_med": float(np.median(bias_med))}
    # ---- the truncated normal picture for one draw
    # ---- data: the 10,000 rules
    d, ex, rules, R = _rule_matrix()
    splits = {"1926-86": ((d > d[0]) & (d <= IS_END), (d > IS_END) & (d <= RESEARCH_END)),
              "1987-2003": ((d > IS_END) & (d <= 20031231), (d > 20031231) & (d <= RESEARCH_END))}
    data_out = {}
    for name, (mi, mo) in splits.items():
        Ri = R[mi].astype(np.float64)
        T = int(mi.sum())
        X = _sr(Ri) * math.sqrt(252)
        j = int(np.argmax(X))
        Zs = Ri - Ri.mean(0)
        sd = Zs.std(0, ddof=1)
        sd = np.where(sd > 0, sd, 1.0)
        zj = Zs[:, j] / sd[j]
        rho = (Zs.T @ zj) / ((T - 1) * sd)
        rho = np.clip(rho, -1, 1)
        s = math.sqrt(252 / T)
        # projection critical value by the multiplier bootstrap of the standardized means
        Zn = (Zs / sd).astype(np.float32)
        mx = []
        for _ in range(4):
            W = rng.standard_normal((100, T)).astype(np.float32)
            mx.append(np.abs(W @ Zn).max(1) / math.sqrt(T - 1))
        mx = np.concatenate(mx)
        cb = float(np.quantile(mx, 1 - 0.005))
        r = _winner_inference(X, s, rho, j, cb)
        Xo = _sr(R[mo].astype(np.float64)) * math.sqrt(252)
        To = int(mo.sum())
        top = np.argsort(X)[::-1]
        data_out[name] = {**r, "T": T, "T_out": To, "s": s, "s_out": math.sqrt(252 / To), "c_beta": cb,
                          "c_95": float(np.quantile(mx, 0.95)), "label": B.rule_label(rules[j]),
                          "out": float(Xo[j]), "second": float(X[top[1]]), "second_label": B.rule_label(rules[top[1]]),
                          "rho_second": float(rho[top[1]]), "n_close": int(np.sum(X > X[j] - 2 * s)),
                          "binding": B.rule_label(rules[int(np.flatnonzero((np.arange(len(X)) != j) & (rho < 1 - 1e-9))[
                              int(np.argmax((X - rho * X[j])[(np.arange(len(X)) != j) & (rho < 1 - 1e-9)] /
                                            (1 - rho[(np.arange(len(X)) != j) & (rho < 1 - 1e-9)])))])]),
                          "first": int(d[mi][0]), "last": int(d[mi][-1]), "first_out": int(d[mo][0]),
                          "last_out": int(d[mo][-1])}
    # the inversion for the 1987-2003 winner (it won by a hair): F(mu) = P_mu(X_j <= x_j | won), naive, conditional
    # and hybrid (the hybrid is defined only inside the projection interval)
    w = data_out["1987-2003"]
    mus = np.linspace(-3.0, 2.0, 401)
    x_, s_, L_, cb_ = w["x"], w["s"], w["L"], w["c_beta"]
    F_naive = stats.norm.cdf((x_ - mus) / s_)
    F_cond = stats.truncnorm.cdf(x_, (L_ - mus) / s_, np.inf, loc=mus, scale=s_)
    inside = np.abs(x_ - mus) <= cb_ * s_
    lo_t = np.maximum(L_, mus - cb_ * s_)
    F_hyb = np.where(inside, stats.truncnorm.cdf(x_, (lo_t - mus) / s_, cb_, loc=mus, scale=s_), np.nan)
    inv = {"mu": mus, "naive": F_naive, "cond": F_cond, "hybrid": F_hyb}
    return _json({"J": J, "rho": rho0, "reps": reps, "c_beta": c_beta, "c_95": c_95, "sims": sims, "data": data_out,
                  "inv": inv})


ITEMS = {"lookahead": compute_lookahead, "survivor": compute_survivor, "select": compute_select,
         "engine": compute_engine, "sharpe": compute_sharpe, "counter": compute_counter, "rules": compute_rules,
         "acf": compute_acf, "dsr": compute_dsr, "pbo": compute_pbo, "cv": compute_cv, "rc": compute_rc, "monitor": compute_monitor,
         "planted": compute_planted, "funding": compute_funding, "envelope": compute_envelope,
         "winners": compute_winners}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
