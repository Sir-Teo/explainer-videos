"""Precompute every number in Part 31 of *Economics, Built* ("The Central Bank").

    python -m videos.economics.econ31.compute            # everything missing (about a minute)
    python -m videos.economics.econ31.compute --force mc

Results are cached in ``.cache/econ31/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's policy rates, the Federal Reserve's balance sheet and reserves, Treasury yields,
industrial production, prices and commodity prices, the OECD's European bond yields; the Philadelphia Fed's real-time
GDP vintages, Greenbook projections and SPF medians; the New York Fed's Holston-Laubach-Williams estimates).  Models:
Agora's central bank (``agora.cb``) with the Island's Part 31 truths.

Items:
    spreads    10-year yields of Italy, Spain, Germany and Britain, monthly, 2007-2016, and the spreads over Germany
    reserves   the Fed's assets and reserves, the funds rate and the rate on reserves; a corridor and a floor
    playit     the chair in early 1979: the data of the day against today's estimates
    transmission  the 2022 tightening: the funds rate against the 2- and 10-year yields
    realtime   Orphanides's point: output gaps from the data of the day against today's, and Taylor's rule on each
    island     one Island history: the rate, output and the true shock; the naive regression
    mc         four ways to identify a policy shock, on 300 Island histories with the truth known
    usvar      a recursive VAR on US monthly data, 1965-2007, with and without commodity prices
    zlb        policy rates at zero: the United States, Japan and the euro area
    qe         the Fed's balance sheet since 2007; the 10-year yield on QE1's announcement days
    tantrum    words as policy: the 10-year yield around 22 May 2013
    rstar      the natural rate: Holston-Laubach-Williams, the FOMC's longer-run dots, and the Island's filter
    debt       self-fulfilling yields with and without a backstop
    called     the Greenbook against the professional forecasters, 1969-2020
    frontier   runoff, the 2022-23 tightening and the Fed's deferred asset
    film       the intermission's data film: the federal funds rate, month by month, since 1954
    melody     its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import cb, rbc

CACHE = Cache("econ31")
load = CACHE.load
TRUTH = island.truths(31)
FILM_SECONDS = 50.0


def _series(key: str, first: str = "0000", last: str = "9999") -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v) and first <= x <= last}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365


def _monthly_mean(key: str, first: str = "0000", last: str = "9999") -> dict:
    out: dict = {}
    for x, v in _series(key, first, last).items():
        out.setdefault(x[:7] + "-01", []).append(v)
    return {k: float(np.mean(v)) for k, v in sorted(out.items())}


def compute_spreads() -> dict:
    Y = {c: _series(f"IRLTLT01{c}M156N", "2007-01-01", "2016-12-01") for c in ("IT", "ES", "DE", "GB")}
    ds = sorted(set(Y["IT"]) & set(Y["ES"]) & set(Y["DE"]) & set(Y["GB"]))
    out = {"t": [_t(d) for d in ds], **{c: [Y[c][d] for d in ds] for c in Y}}
    sp = {c: np.array([Y[c][d] - Y["DE"][d] for d in ds]) for c in ("IT", "ES", "GB")}
    out.update({f"{c}_DE": sp[c].tolist() for c in sp})
    k = int(np.argmax(sp["ES"]))
    at = {d: i for i, d in enumerate(ds)}
    out.update({"es_peak": float(sp["ES"][k]), "es_peak_date": ds[k], "it_peak": float(sp["IT"].max()),
                "it_peak_date": ds[int(np.argmax(sp["IT"]))],
                "jul12": {c: float(Y[c]["2012-07-01"]) for c in Y},
                "jul14": {c: float(Y[c]["2014-07-01"]) for c in Y},
                "es_spread_jul12": float(sp["ES"][at["2012-07-01"]]),
                "es_spread_jul14": float(sp["ES"][at["2014-07-01"]]),
                "it_spread_jul12": float(sp["IT"][at["2012-07-01"]]),
                "it_spread_jul14": float(sp["IT"][at["2014-07-01"]])})
    return out


def compute_reserves() -> dict:
    A = _monthly_mean("WALCL", "2003-01-01")
    R = _monthly_mean("WRESBAL", "2003-01-01")
    ff = _series("FEDFUNDS", "2003-01-01")
    ior = {**_monthly_mean("IOER"), **_monthly_mean("IORB")}
    ds = sorted(set(A) & set(R) & set(ff))
    pre = "2008-08-01"
    T = TRUTH["reserves"]
    cf = cb.corridor_and_floor(T["floor"], T["ceiling"], T["need"], T["spread"])
    ka = int(np.argmax([A[d] for d in ds]))
    kr = int(np.argmax([R[d] for d in ds]))
    gap = [ff[d] - ior[d] for d in ds if d in ior]
    return {"t": [_t(d) for d in ds], "assets": [A[d] / 1e6 for d in ds], "reserves": [R[d] / 1e6 for d in ds],
            "ff": [ff[d] for d in ds], "ior_t": [_t(d) for d in ds if d in ior],
            "ior": [ior[d] for d in ds if d in ior],
            "assets_pre": A[pre] / 1e6, "reserves_pre": R[pre] / 1e3, "assets_peak": A[ds[ka]] / 1e6,
            "assets_peak_date": ds[ka], "reserves_peak": R[ds[kr]] / 1e6, "reserves_peak_date": ds[kr],
            "assets_last": A[ds[-1]] / 1e6, "reserves_last": R[ds[-1]] / 1e6, "last": ds[-1],
            "ff_minus_ior_mean": float(np.mean(gap)), "curve": cf}


def _vintage_gaps() -> list:
    """Each first-quarter vintage: the output gap in the last quarter it reported, measured against a log-linear
    trend fitted to all the data that vintage held (the data of the day), and against the CBO's potential today."""
    R = data.rtdsm_q1()
    qs = R["quarters"]
    Y, P = _series("GDPC1"), _series("GDPPOT")
    out = []
    for v in R["vintages"]:
        lv = np.array(R["level"][v])
        ok = np.isfinite(lv)
        y = np.log(lv[ok])
        t = np.arange(len(y))
        b = np.polyfit(t, y, 1)
        last = [q for q, o in zip(qs, ok) if o][-1]
        yy, k = last.split(":Q")
        key = f"{yy}-{3 * (int(k) - 1) + 1:02d}-01"
        today = 100 * (np.log(Y[key]) - np.log(P[key])) if key in Y and key in P else float("nan")
        out.append({"vintage": v, "quarter": last, "date": key, "realtime": float(100 * (y[-1] - np.polyval(b, t[-1]))),
                    "today": float(today), "trend_growth": float(400 * b[0])})
    return out


def _cpi_q4() -> dict:
    """CPI inflation over the four quarters to each fourth quarter (the CPI is never revised)."""
    c = _series("CPIAUCSL")
    q4 = {int(d[:4]): np.mean([c[f"{d[:4]}-{m}-01"] for m in ("10", "11", "12")]) for d in c
          if d[5:7] == "12" and all(f"{d[:4]}-{m}-01" in c for m in ("10", "11", "12"))}
    return {y: float(100 * (q4[y] / q4[y - 1] - 1)) for y in q4 if y - 1 in q4}


def compute_realtime() -> dict:
    T = TRUTH["taylor"]
    G = [g for g in _vintage_gaps() if g["vintage"] <= "2008Q1"]
    pi = _cpi_q4()
    ff = _monthly_mean("FEDFUNDS")
    rows = []
    for g in G:
        y = int(g["vintage"][:4])
        if y - 1 not in pi:
            continue
        p = pi[y - 1]
        base = T["rstar"] + p + T["a_pi"] * (p - T["target"])
        f = np.mean([ff[f"{y}-0{m}-01"] for m in (1, 2, 3)])
        rows.append({"year": y, "pi": p, "gap_rt": g["realtime"], "gap_today": g["today"],
                     "rule_rt": base + T["a_y"] * g["realtime"], "rule_today": base + T["a_y"] * g["today"],
                     "ff": float(f), "trend_growth": g["trend_growth"]})
    yr = np.array([r["year"] for r in rows])
    err = np.array([r["gap_rt"] - r["gap_today"] for r in rows])
    seventies = (yr >= 1971) & (yr <= 1982)          # gaps at the ends of 1970-81, rates set in 1971-82
    return {"rows": rows, "mean_error_70s": float(err[seventies].mean()),
            "mean_error_after": float(err[yr >= 1985].mean()),
            "rule_gap_70s": float(np.mean([r["rule_today"] - r["rule_rt"] for r in rows if 1971 <= r["year"] <= 1982])),
            "ff_minus_rule_rt_70s": float(np.mean([r["ff"] - r["rule_rt"] for r in rows if 1971 <= r["year"] <= 1982])),
            "ff_minus_rule_today_70s": float(np.mean([r["ff"] - r["rule_today"] for r in rows
                                                      if 1971 <= r["year"] <= 1982]))}


def compute_playit() -> dict:
    R = {r["year"]: r for r in compute_realtime()["rows"]}
    r = R[1979]
    return {**r, "options": ["about 4% below its potential", "about at its potential", "about 2% above"],
            "answer": 2}


def compute_transmission() -> dict:
    """The 2022 tightening: the funds rate's upper limit against the 2- and 10-year Treasury yields, monthly."""
    ff = _monthly_mean("DFEDTARU", "2021-01-01", "2024-06-30")
    y2 = _series("GS2", "2021-01-01", "2024-06-30")
    y10 = _monthly_mean("DGS10", "2021-01-01", "2024-06-30")
    ds = sorted(set(ff) & set(y2) & set(y10))
    return {"t": [_t(d) for d in ds], "ff": [ff[d] for d in ds], "y2": [y2[d] for d in ds],
            "y10": [y10[d] for d in ds], "ff_mar22": ff["2022-03-01"], "y2_mar22": y2["2022-03-01"],
            "y2_dec21": y2["2021-12-01"], "y2_sep21": y2["2021-09-01"], "ff_dec22": ff["2022-12-01"],
            "y10_dec21": y10["2021-12-01"], "y10_oct23": y10["2023-10-01"]}


def compute_island() -> dict:
    H = cb.history(240, seed=TRUTH["mc"]["seed"], **TRUTH["history"])
    y, i, v = (np.array(H[k]) for k in ("y", "i", "v"))
    di = np.diff(i)
    nv = cb.naive_irf(H, 8)
    return {"q": list(range(len(y))), "y": H["y"], "pi": H["pi"], "i": H["i"], "v": H["v"],
            "di": di[:-1].tolist(), "y_next": y[2:].tolist(), "naive_y1": nv["y"][1],
            "corr_y_i": float(np.corrcoef(y, i)[0, 1]), "corr_v_di": float(np.corrcoef(v[1:], di)[0, 1]),
            "sd_v": float(np.std(v)), "sd_di": float(np.std(di)), "truth": cb.true_irf(16, **TRUTH["history"])}


def compute_mc() -> dict:
    M = TRUTH["mc"]
    R = cb.identification_mc(reps=M["reps"], T=M["T"], h=M["h"], seed=M["seed"], info=M["info"],
                             proxy_noise=M["proxy_noise"])
    tr = R["truth"]
    R["peaks"] = {m: {"y": cb.peak(v["y"]["mean"]), "pi_end": v["pi"]["mean"][-1], "y_1": v["y"]["mean"][1]}
                  for m, v in R["methods"].items()}
    R["peaks"]["truth"] = {"y": cb.peak(tr["y"]), "pi_end": tr["pi"][-1], "y_1": tr["y"][1]}
    return R


def _var_irf(X, p, h, k_shock, reps=200, seed=0):
    fit = rbc.var_ols(X, p)
    L = np.linalg.cholesky(fit["Sigma"])
    base = np.array([P @ L[:, k_shock] for P in rbc._ma(fit["A"], h)]) / L[k_shock, k_shock]
    rng = np.random.default_rng(seed)
    T, n = X.shape
    A = fit["A"]
    c = fit.get("c", np.zeros(n))
    U = fit["U"] if "U" in fit else None
    draws = []
    if U is not None:
        for _ in range(reps):
            e = U[rng.integers(0, len(U), len(U))]
            Xb = np.array(X[:p], float)
            for t in range(len(U)):
                x = c + sum(A[j] @ Xb[-1 - j] for j in range(p)) + e[t]
                Xb = np.vstack([Xb, x])
            fb = rbc.var_ols(Xb, p)
            Lb = np.linalg.cholesky(fb["Sigma"])
            draws.append(np.array([P @ Lb[:, k_shock] for P in rbc._ma(fb["A"], h)]) / Lb[k_shock, k_shock])
    D = np.array(draws) if draws else None
    return base, D


def compute_usvar() -> dict:
    ip, cpi, ppi, ff = (_series(k, "1965-01-01", "2007-12-01") for k in ("INDPRO", "CPIAUCSL", "PPIACO",
                                                                        "FEDFUNDS"))
    ds = sorted(set(ip) & set(cpi) & set(ppi) & set(ff))
    lip = 100 * np.log([ip[d] for d in ds])
    lcp = 100 * np.log([cpi[d] for d in ds])
    lpp = 100 * np.log([ppi[d] for d in ds])
    f = np.array([ff[d] for d in ds])
    h = 48
    out = {"h": list(range(h + 1)), "first": ds[0], "last": ds[-1]}
    for name, X, kf in (("plain", np.column_stack([lip, lcp, f]), 2),
                        ("commod", np.column_stack([lip, lcp, lpp, f]), 3)):
        base, D = _var_irf(X, 12, h, kf, reps=200, seed=7)
        r = {"ip": base[:, 0].tolist(), "cpi": base[:, 1].tolist(), "ff": base[:, kf].tolist()}
        if D is not None:
            for j, key in ((0, "ip"), (1, "cpi")):
                r[f"{key}_lo"] = np.percentile(D[:, :, j], 5, 0).tolist()
                r[f"{key}_hi"] = np.percentile(D[:, :, j], 95, 0).tolist()
        r["ip_trough"] = cb.peak(r["ip"])
        r["cpi_24"] = r["cpi"][24]
        r["cpi_48"] = r["cpi"][48]
        r["cpi_max"] = float(max(r["cpi"][:25]))
        out[name] = r
    return out


def compute_zlb() -> dict:
    us = {**_monthly_mean("DFEDTAR", "1990-01-01"), **_monthly_mean("DFEDTARU", "2008-12-01")}
    ff = _series("FEDFUNDS", "1990-01-01", "2008-11-01")
    us = {**{d: v for d, v in ff.items()}, **{d: v for d, v in us.items() if d >= "2008-12-01"}}
    jp = _series("IRSTCI01JPM156N", "1990-01-01")
    ecb = _monthly_mean("ECBDFR", "1999-01-01")
    zero_us = [d for d, v in us.items() if v <= 0.25 + 1e-9]
    neg_ecb = [d for d, v in ecb.items() if v < 0]
    jp_low = [d for d, v in jp.items() if v <= 0.1]
    return {"us_t": [_t(d) for d in sorted(us)], "us": [us[d] for d in sorted(us)],
            "jp_t": [_t(d) for d in sorted(jp)], "jp": [jp[d] for d in sorted(jp)],
            "ecb_t": [_t(d) for d in sorted(ecb)], "ecb": [ecb[d] for d in sorted(ecb)],
            "us_zero_months": len(zero_us), "ecb_negative_months": len(neg_ecb), "ecb_min": float(min(ecb.values())),
            "ecb_first_negative": min(neg_ecb), "ecb_last_negative": max(neg_ecb), "jp_low_months": len(jp_low),
            "jp_first_low": min(jp_low)}


QE1_BASELINE = ("2008-11-25", "2008-12-01", "2008-12-16", "2009-01-28", "2009-03-18", "2009-08-12", "2009-09-23",
                "2009-11-04")


def compute_qe() -> dict:
    A = _series("WALCL", "2007-01-01")
    ds = sorted(A)
    y10 = _series("DGS10", "2008-01-01", "2010-12-31")
    ev = cb.event_changes(QE1_BASELINE, y10, window=1)
    days = sorted(y10)
    non = 100 * (y10[days[days.index("2010-03-31")]] - y10[days[days.index("2008-11-24")]]) - 100 * sum(
        e["change"] for e in ev)
    k = int(np.argmax([A[d] for d in ds]))
    return {"t": [_t(d) for d in ds], "assets": [A[d] / 1e6 for d in ds], "events": ev,
            "event_bp": [100 * e["change"] for e in ev], "total_bp": float(100 * sum(e["change"] for e in ev)),
            "first5_bp": float(100 * sum(e["change"] for e in ev[:5])), "nonevent_bp": float(non),
            "y10_t": [_t(d) for d in days], "y10": [y10[d] for d in days],
            "peak": A[ds[k]] / 1e6, "peak_date": ds[k], "last": A[ds[-1]] / 1e6, "last_date": ds[-1],
            "pre": A["2008-08-27"] / 1e6 if "2008-08-27" in A else None}


def compute_tantrum() -> dict:
    """Words as policy: the 10-year Treasury yield around Bernanke's testimony of 22 May 2013."""
    y = _series("DGS10", "2012-07-01", "2014-06-30")
    ds = sorted(y)
    before = y["2013-05-21"]
    k = int(np.argmax([y[d] for d in ds if d <= "2013-12-31"]))
    peak_d = [d for d in ds if d <= "2013-12-31"][k]
    return {"t": [_t(d) for d in ds], "y": [y[d] for d in ds], "before": before, "peak": y[peak_d],
            "peak_date": peak_d, "rise_bp": float(100 * (y[peak_d] - before)), "min_2012": float(min(
                y[d] for d in ds if d <= "2012-12-31"))}


def compute_rstar() -> dict:
    H = data.hlw()
    sep = _series("FEDTARMDLR")
    T = TRUTH["rstar"]
    isl = cb.rstar_island(**T)
    t = [_t(d) for d in H["date"]]
    last = {k: H[k][-1] for k in ("rstar_us", "rstar_ca", "rstar_ea")}
    at = {d[:4]: i for i, d in enumerate(H["date"]) if d.endswith("01-01")}
    return {"t": t, "us": H["rstar_us"], "ca": H["rstar_ca"], "ea": H["rstar_ea"], "g": H["g_us"],
            "last": last, "last_date": H["date"][-1],
            "us_2000": H["rstar_us"][at["2000"]], "us_2007": H["rstar_us"][at["2007"]],
            "us_2015": H["rstar_us"][at["2015"]],
            "sep_t": [_t(d) for d in sorted(sep)], "sep_real": [sep[d] - 2.0 for d in sorted(sep)],
            "sep_first": sep[min(sep)] - 2.0, "sep_min": min(sep.values()) - 2.0, "sep_last": sep[max(sep)] - 2.0,
            "sep_last_date": max(sep), "island": isl}


def compute_debt() -> dict:
    D = TRUTH["debt"]
    pr = cb.debt_params(D["debt"], D["rf"], D["r_good"], D["r_bad"])
    kw = {"debt": D["debt"], "rf": D["rf"], **pr}
    free = cb.debt_game(**kw)
    capped = cb.debt_game(cap=D["cap"], **kw)
    return {"free": free, "capped": capped, "params": pr, "cap": D["cap"],
            "path_up": cb.debt_path(D["r_bad"] + 0.004, periods=8, **kw),
            "path_down": cb.debt_path(D["r_bad"] - 0.004, periods=14, **kw),
            "path_capped": cb.debt_path(D["r_bad"] + 0.004, periods=14, cap=D["cap"], **kw)}


def compute_called() -> dict:
    G = data.greenbook()
    D = _series("GDPDEF")

    def qd(q):
        y, k = q.split("Q")
        return f"{y}-{3 * (int(k) - 1) + 1:02d}-01"

    def add(q, h):
        y, k = map(int, q.split("Q"))
        n = y * 4 + k - 1 + h
        return f"{n // 4}Q{n % 4 + 1}"

    def year(f):
        return float(100 * (np.prod((1 + np.asarray(f, float) / 100) ** 0.25) - 1))

    gbq = {}
    for r in G["gb"]:
        y, k = r["quarter"].split("Q")
        mid = np.datetime64(f"{y}-{3 * (int(k) - 1) + 2:02d}-15")
        dist = abs(int((np.datetime64(r["date"]) - mid).astype(int)))
        if r["quarter"] not in gbq or dist < gbq[r["quarter"]][0]:
            gbq[r["quarter"]] = (dist, r)
    spf = {r["quarter"]: r for r in G["spf"]}
    rows = []
    for q in sorted(gbq):
        g, s = gbq[q][1], spf.get(q)
        if s is None or not all(np.isfinite(g["f"][1:5])) or not all(np.isfinite(s["f"][1:5])):
            continue
        a0, a4 = qd(q), qd(add(q, 4))
        if a0 in D and a4 in D:
            rows.append({"q": q, "t": int(q[:4]) + (int(q[-1]) - 1) / 4, "gb": year(g["f"][1:5]),
                         "spf": year(s["f"][1:5]), "actual": float(100 * (D[a4] / D[a0] - 1))})

    def era(lo, hi):
        R = [r for r in rows if lo <= r["q"] <= hi]
        a = np.array([r["actual"] for r in R])
        gb, sp = np.array([r["gb"] for r in R]), np.array([r["spf"] for r in R])
        X = np.column_stack([np.ones(len(a)), gb, sp])
        b, *_ = np.linalg.lstsq(X, a, rcond=None)
        return {"n": len(R), "first": R[0]["q"], "last": R[-1]["q"], "rmse_gb": float(np.sqrt(np.mean((a - gb) ** 2))),
                "rmse_spf": float(np.sqrt(np.mean((a - sp) ** 2))), "w_gb": float(b[1]), "w_spf": float(b[2])}

    return {"rows": rows, "rr": era("1968Q4", "1991Q4"), "after": era("1992Q1", "2020Q4")}


def compute_frontier() -> dict:
    rem = _series("RESPPLLOPNWW", "2019-01-01")
    ds = sorted(rem)
    neg = [d for d in ds if rem[d] < 0]
    A = _series("WALCL", "2019-01-01")
    da = sorted(A)
    k = int(np.argmax([A[d] for d in da]))
    ff = _monthly_mean("DFEDTARU", "2019-01-01")
    cpi = _series("CPIAUCSL", "2018-01-01")
    infl = {d: 100 * (cpi[d] / cpi[f"{int(d[:4]) - 1}{d[4:]}"] - 1) for d in cpi if f"{int(d[:4]) - 1}{d[4:]}" in cpi}
    j = int(np.argmin([rem[d] for d in ds]))
    return {"rem_t": [_t(d) for d in ds], "rem": [rem[d] / 1e3 for d in ds], "first_negative": neg[0] if neg else None,
            "deferred_max": -rem[ds[j]] / 1e3, "deferred_max_date": ds[j], "deferred_last": -rem[ds[-1]] / 1e3,
            "rem_last_date": ds[-1], "a_t": [_t(d) for d in da], "assets": [A[d] / 1e6 for d in da],
            "peak": A[da[k]] / 1e6, "peak_date": da[k], "last": A[da[-1]] / 1e6, "last_date": da[-1],
            "ff_t": [_t(d) for d in sorted(ff)], "ff": [ff[d] for d in sorted(ff)],
            "cpi_t": [_t(d) for d in sorted(infl)], "cpi": [infl[d] for d in sorted(infl)],
            "cpi_peak": float(max(infl.values())), "cpi_peak_date": max(infl, key=infl.get),
            "ff_peak": float(max(ff.values()))}


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1954.5, last: float = 2026.9) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    ff = _series("FEDFUNDS")
    ds = sorted(ff)
    return {"t": [_t(d) for d in ds], "ff": [ff[d] for d in ds], "times": [film_time(_t(d)) for d in ds],
            "first": ds[0], "last": ds[-1], "peak": float(max(ff.values())), "peak_date": max(ff, key=ff.get)}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["ff"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40,
                            high=86)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the effective federal funds rate, month by month, 1954-2026 (via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ31").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "spreads": compute_spreads,
    "reserves": compute_reserves,
    "playit": compute_playit,
    "realtime": compute_realtime,
    "transmission": compute_transmission,
    "island": compute_island,
    "mc": compute_mc,
    "usvar": compute_usvar,
    "zlb": compute_zlb,
    "qe": compute_qe,
    "tantrum": compute_tantrum,
    "rstar": compute_rstar,
    "debt": compute_debt,
    "called": compute_called,
    "frontier": compute_frontier,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
