"""Precompute every number in Part 20 of *Economics, Built* ("Growth I: Capital").

    python -m videos.economics.econ20.compute            # everything missing (seconds)
    python -m videos.economics.econ20.compute --force convergence

Results are cached in ``.cache/econ20/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Penn World Table 11.0; the Maddison Project).  Models: Agora's growth module
(``agora.growth``), with the Island's Part 20 truths.

Items:
    hook         the two Koreas' GDP per head, 1911-2022 (Maddison), and South Korea's investment share (PWT)
    kaldor       Kaldor's six facts on the Penn World Table: the United States since 1950, and growth across countries
    harrod       Harrod-Domar growth and its knife edge on the island; Easterly's test, as published
    solow        the island's Solow diagram: saving, break-even investment, the steady state
    playit       five saving rates for a century; the golden rule; a jump in saving from 15% to 30%
    transition   the speed of convergence, linearized and simulated, with a narrow and a broad capital share
    convergence  growth against initial income across countries, absolute and conditional (PWT), and MRW's numbers
    accounting   growth accounting for the United States, 1950-2019, and for eight countries
    eastasia     Young's four tigers, as published, against the same accounting on the PWT
    development  development accounting, 2019: capital intensity, schooling and TFP across 140-odd countries
    lucas        Lucas's question: the marginal product of capital in India and the United States
    ramsey       the Ramsey-Cass-Koopmans phase diagram and the saddle path found by shooting
    china        China since 1978: investment share, capital-output ratio, return to capital, accounting
    dial         the speed of convergence and capital's share: the rows the Dials chapter draws
    slowdown     US TFP growth by period (the slowdown since 2005) and convergence since 2000
    film         the intermission's data film: investment share and GDP per head, 1960-2023 (PWT)
    melody       its data melody: South Korea's investment share, 1953-2023
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import growth as gr

CACHE = Cache("econ20")
load = CACHE.load
TRUTH = island.truths(20)
SOLOW = TRUTH["solow"]


def _pwt_by_country():
    out = {}
    for r in data.pwt():
        out.setdefault(r["countrycode"], {})[r["year"]] = r
    return out


def _fin(*vs):
    return all(v is not None and np.isfinite(v) for v in vs)


def _trend(years, values):
    """Average annual growth from a log-linear trend."""
    b = np.polyfit(np.asarray(years, float), np.log(np.asarray(values, float)), 1)[0]
    return float(np.exp(b) - 1)


# ---------------------------------------------------------------------------------------------------------------
# the hook: one peninsula, two economies

def compute_hook() -> dict:
    out = {}
    for c in ("KOR", "PRK"):
        g = data.maddison_country(c)
        pts = [(int(y), float(v)) for y, v in zip(g["year"], g["gdppc"]) if v and np.isfinite(v) and y >= 1911]
        out[c] = {"years": [y for y, _ in pts], "gdppc": [v for _, v in pts]}
    kor = dict(zip(out["KOR"]["years"], out["KOR"]["gdppc"]))
    prk = dict(zip(out["PRK"]["years"], out["PRK"]["gdppc"]))
    rows = data.pwt("KOR")
    inv = [(r["year"], r["csh_i"]) for r in rows if _fin(r["csh_i"])]
    gap = [y for y in range(1944, 1990) if y not in prk]
    return {**out, "kor": {str(y): kor[y] for y in (1911, 1940, 1953, 1960, 1990, 2022)},
            "prk": {str(y): prk[y] for y in (1911, 1940, 1990, 2000, 2022)},
            "ratio_1940": prk[1940] / kor[1940], "ratio_1990": kor[1990] / prk[1990], "ratio_2022": kor[2022] / prk[2022],
            "gap": [gap[0], gap[-1]], "inv_years": [y for y, _ in inv], "inv": [v for _, v in inv],
            "inv_1960": dict(inv)[1960], "inv_1990": dict(inv)[1990], "growth_1953_2022": (kor[2022] / kor[1953]) ** (1 / 69) - 1}


# ---------------------------------------------------------------------------------------------------------------
# chapter 1: Kaldor's facts

def compute_kaldor() -> dict:
    us = {r["year"]: r for r in data.pwt("USA")}
    years = [y for y in sorted(us) if _fin(us[y]["rgdpna"], us[y]["emp"], us[y]["rnna"], us[y]["labsh"])]
    ypw = [us[y]["rgdpna"] / us[y]["emp"] for y in years]
    kpw = [us[y]["rnna"] / us[y]["emp"] for y in years]
    ky = [us[y]["rnna"] / us[y]["rgdpna"] for y in years]
    ls = [us[y]["labsh"] for y in years]
    irr_years = [y for y in years if _fin(us[y]["irr"])]
    irr = [us[y]["irr"] for y in irr_years]
    # fact 6: growth of GDP per head, 1960-2019, across countries with a million people or more
    pw = _pwt_by_country()
    g = []
    for c, d in pw.items():
        a, b = d.get(1960), d.get(2019)
        if a and b and _fin(a["rgdpna"], a["pop"], b["rgdpna"], b["pop"]) and a["pop"] >= 1.0:
            g.append((c, float(np.log((b["rgdpna"] / b["pop"]) / (a["rgdpna"] / a["pop"])) / 59)))
    g.sort(key=lambda t: t[1])
    vals = np.array([v for _, v in g])
    half = years.index(1985)
    return {"years": years, "ypw": ypw, "kpw": kpw, "ky": ky, "labsh": ls, "irr_years": irr_years, "irr": irr,
            "g_ypw": _trend(years, ypw), "g_kpw": _trend(years, kpw),
            "g_ypw_halves": [_trend(years[:half + 1], ypw[:half + 1]), _trend(years[half:], ypw[half:])],
            "ky_mean": float(np.mean(ky)), "ky_range": [float(min(ky)), float(max(ky))],
            "irr_mean": float(np.mean(irr)), "irr_range": [float(min(irr)), float(max(irr))],
            "ls_1950_79": float(np.mean([v for y, v in zip(years, ls) if y <= 1979])),
            "ls_2010_": float(np.mean([v for y, v in zip(years, ls) if y >= 2010])), "first": years[0],
            "last": years[-1], "cross": {"codes": [c for c, _ in g], "growth": vals.tolist(), "n": len(g),
                                         "lo": g[0], "hi": g[-1], "p10": float(np.percentile(vals, 10)),
                                         "p90": float(np.percentile(vals, 90)), "median": float(np.median(vals))}}


# ---------------------------------------------------------------------------------------------------------------
# chapter 2: Harrod and Domar

def compute_harrod() -> dict:
    """The island with a fixed capital-output ratio v = 3.5: capital grows at s / v - delta, the labour force at 1%; a
    saving rate below v (n + delta) leaves workers without machines, one above it leaves machines without workers."""
    v, delta, n = 3.5, 0.03, 0.01
    paths = {}
    for s in (0.10, 0.14, 0.20):
        gk = s / v - delta
        T = 50
        K = np.exp(gk * np.arange(T + 1))
        L = np.exp(n * np.arange(T + 1))
        # with no substitution, output is min(K / v, L / l) with l set so that K and L match in year 0
        idle_k = np.maximum(0, 1 - L / K)
        unemployed = np.maximum(0, 1 - K / L)
        paths[f"{s:.2f}"] = {"growth": gk, "idle": idle_k.tolist(), "unemployed": unemployed.tolist()}
    hd = gr.harrod_domar(0.2, 3.5, delta=0.03, labour=0.01)
    return {"v": v, "delta": delta, "n": n, "warranted": v * (n + delta), "paths": paths, "years": list(range(51)),
            "growth_20": hd["growth"], "needed_7": hd["needed_for_target"](0.07),
            # Easterly (1999), as published: an ICOR of 3.5 and a one-year lag; Zambia's counterfactual
            "easterly": {"icor": 3.5, "lag": 1, "years": "1961-1992"}}


# ---------------------------------------------------------------------------------------------------------------
# chapters 3-5: the Solow model on the island

def _solow_kw():
    return {k: SOLOW[k] for k in ("n", "g", "delta", "alpha")}


def compute_solow() -> dict:
    kw = _solow_kw()
    s = SOLOW["s0"]
    st = gr.solow_steady(s, **kw)
    k = np.linspace(0.0, 3.0 * st["k"], 301)
    f = k ** kw["alpha"]
    brk = (kw["n"] + kw["g"] + kw["delta"]) * k
    st2 = gr.solow_steady(0.30, **kw)
    return {"k": k.tolist(), "f": f.tolist(), "sf": (s * f).tolist(), "sf2": (0.30 * f).tolist(),
            "break": brk.tolist(), "steady": st, "steady_30": st2, "s": s, "kw": kw,
            "rate": kw["n"] + kw["g"] + kw["delta"],
            "ratio_y": st2["y"] / st["y"], "ratio_k": st2["k"] / st["k"],
            "elasticity": kw["alpha"] / (1 - kw["alpha"])}


def compute_playit() -> dict:
    kw = _solow_kw()
    p = TRUTH["playit"]
    s0 = SOLOW["s0"]
    k0 = gr.solow_steady(s0, **kw)["k"]
    runs = {}
    trend = (1 + kw["g"]) ** np.arange(p["years"] + 1)
    base_c = np.array(gr.solow_path(s0, p["years"], k0=k0, **kw)["c"]) * trend    # staying at 15%
    for s in p["options"]:
        path = gr.solow_path(s, p["years"], k0=k0, **kw)
        c = np.array(path["c"]) * trend                                             # consumption per worker
        above = c >= base_c - 1e-12
        # the year the new rate's consumption passes (or, for a lower rate, falls below) staying at 15%
        if s > s0:
            cross = next((t for t in range(1, len(c)) if above[t]), None)
        else:
            cross = next((t for t in range(1, len(c)) if not above[t]), None)
        runs[f"{s:.2f}"] = {"c": c.tolist(), "c_end": float(c[-1]), "c_first": float(c[1]),
                            "steady_c": gr.solow_steady(s, **kw)["c"], "cross": cross,
                            "vs_base_end": float(c[-1] / base_c[-1] - 1)}
    best = max(runs, key=lambda k_: runs[k_]["c_end"])
    gold = gr.golden_rule(**kw)
    t0, lo, hi = p["jump"]
    jump = gr.solow_path(lambda t: hi if t >= t0 else lo, 80, k0=k0, **kw)
    y = np.array(jump["y_per_worker"])
    base = np.array(gr.solow_path(lo, 80, k0=k0, **kw)["y_per_worker"])
    growth = np.diff(np.log(y))
    return {"options": list(p["options"]), "years": p["years"], "runs": runs, "best": best, "base": base_c.tolist(),
            "s0": s0,
            "golden": {"s": gold["s"].tolist(), "c": gold["c"].tolist(), "s_gold": gold["s_gold"],
                       "c_gold": gold["c_gold"]},
            "jump": {"t0": t0, "lo": lo, "hi": hi, "y": y.tolist(), "base": base.tolist(), "growth": growth.tolist(),
                     "peak_growth": float(growth.max()), "long_growth": float(growth[-1]),
                     "level_gain": float(y[-1] / base[-1] - 1),
                     "half": int(next(t for t in range(t0, 81)
                                      if np.log(y[t] / base[t]) >= 0.5 * np.log(y[-1] / base[-1]))) - t0}}


def compute_transition() -> dict:
    kw = _solow_kw()
    narrow = gr.convergence_speed(**kw)
    broad = gr.convergence_speed(**{**kw, "alpha": 0.75})
    s = 0.2
    paths = {}
    for a in (kw["alpha"], 0.75):
        kk = {**kw, "alpha": a}
        ks = gr.solow_steady(s, **kk)["k"]
        p = gr.solow_path(s, 120, k0=0.25 * ks, **kk)
        gap = np.log(ks ** a) - np.log(np.array(p["y"]))
        paths[f"{a:.2f}"] = {"gap": (gap / gap[0]).tolist()}
    return {"narrow": narrow, "broad": broad, "paths": paths, "years": list(range(121)),
            "rate": kw["n"] + kw["g"] + kw["delta"]}


# ---------------------------------------------------------------------------------------------------------------
# chapter 6: convergence

def _sample(pw, a, b, min_pop):
    rows = []
    for c, d in pw.items():
        r0, r1 = d.get(a), d.get(b)
        if not (r0 and r1 and _fin(r0["rgdpna"], r0["pop"], r1["rgdpna"], r1["pop"], r0["hc"])):
            continue
        if r0["pop"] < min_pop:
            continue
        inv = [d[y]["csh_i"] for y in range(a, b + 1) if y in d and _fin(d[y]["csh_i"]) and d[y]["csh_i"] > 0]
        if len(inv) < 0.8 * (b - a + 1):
            continue
        n = np.log(r1["pop"] / r0["pop"]) / (b - a)
        rows.append({"code": c, "y0": r0["rgdpna"] / r0["pop"], "y1": r1["rgdpna"] / r1["pop"],
                     "s": float(np.mean(inv)), "n": float(n), "h0": r0["hc"]})
    return rows


def compute_convergence() -> dict:
    t = TRUTH["convergence"]
    pw = _pwt_by_country()
    out = {}
    for a, b in t["spans"]:
        rows = _sample(pw, a, b, t["min_pop"])
        y0 = [r["y0"] for r in rows]
        y1 = [r["y1"] for r in rows]
        ab = gr.convergence(y0, y1, b - a)
        ctl = [np.log([r["s"] for r in rows]), np.log([r["n"] + t["gd"] for r in rows]),
               np.log([r["h0"] for r in rows])]
        co = gr.convergence(y0, y1, b - a, controls=ctl)
        growth = (np.log(y1) - np.log(y0)) / (b - a)
        # Frisch-Waugh: growth and initial income, each net of the controls (plus their means, for the picture)
        Z = np.column_stack([np.ones(len(rows)), *ctl])

        def resid(v):
            v = np.asarray(v, float)
            return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0] + v.mean()
        out[f"{a}-{b}"] = {"codes": [r["code"] for r in rows], "ly0": np.log(y0).tolist(),
                           "growth": growth.tolist(), "absolute": ab, "conditional": co, "n": len(rows),
                           "partial_ly0": resid(np.log(y0)).tolist(), "partial_growth": resid(growth).tolist()}
    # MRW (1992) and Islam (1995), as published
    lit = {"mrw_unconditional_nonoil": -0.00360, "mrw_lambda_nonoil": 0.0137, "mrw_lambda_nonoil_se": 0.0019,
           "mrw_lambda_oecd": 0.0203, "islam_lambda_nonoil": 0.0507, "islam_lambda_nonoil_se": 0.0091,
           "mrw_alpha_textbook": 0.59, "mrw_alpha": 0.31, "mrw_beta": 0.28, "mrw_r2_aug": 0.78, "mrw_r2_textbook": 0.59}
    return {"spans": [f"{a}-{b}" for a, b in t["spans"]], **out, "lit": lit}


# ---------------------------------------------------------------------------------------------------------------
# chapters 7-8: growth accounting

ACCOUNT = (("USA", 1950, 2019), ("GBR", 1950, 2019), ("JPN", 1950, 2019), ("KOR", 1966, 2019), ("CHN", 1980, 2019),
           ("IND", 1980, 2019), ("BRA", 1960, 2019), ("NGA", 1960, 2019))


def compute_accounting() -> dict:
    out = {}
    for c, a, b in ACCOUNT:
        rows = data.pwt(c)
        out[c] = gr.growth_accounting(rows, a, b)
    us = data.pwt("USA")
    periods = {}
    for a, b in ((1950, 1973), (1973, 1995), (1995, 2005), (2005, 2019)):
        periods[f"{a}-{b}"] = gr.growth_accounting(us, a, b)
    # Solow (1957), as published: output per man-hour, US private non-farm, 1909-1949
    solow57 = {"years": "1909-1949", "technical": 0.875, "capital": 0.125}
    return {"countries": out, "order": [c for c, _, _ in ACCOUNT], "us_periods": periods, "solow57": solow57}


def compute_eastasia() -> dict:
    # Young (1995), QJE 110(3), as published: TFP growth a year; Korea and Taiwan excluding agriculture
    young = {"HKG": ("Hong Kong", "1966-1991", 0.023), "SGP": ("Singapore", "1966-1990", 0.002),
             "KOR": ("South Korea", "1966-1990", 0.017), "TWN": ("Taiwan", "1966-1990", 0.026)}
    ours = {}
    for c, b in (("HKG", 1991), ("SGP", 1990), ("KOR", 1990), ("TWN", 1990)):
        ours[c] = gr.growth_accounting(data.pwt(c), 1966, b)
    # South Korea's growth of GDP per head by decade (PWT), and the Soviet Union's (Maddison)
    kor = {r["year"]: r["rgdpna"] / r["pop"] for r in data.pwt("KOR") if _fin(r["rgdpna"], r["pop"])}
    kor_dec = {f"{a}s": float(np.log(kor[a + 10] / kor[a]) / 10) for a in (1960, 1970, 1980, 1990, 2000, 2010)}
    su = data.maddison_country("SUN")
    us = data.maddison_country("USA")
    S = {int(y): float(v) for y, v in zip(su["year"], su["gdppc"]) if v and np.isfinite(v)}
    U = {int(y): float(v) for y, v in zip(us["year"], us["gdppc"]) if v and np.isfinite(v)}
    su_years = [y for y in sorted(S) if 1928 <= y <= 1991 and y in U]
    su_dec = {f"{a}s": float((S[a + 10] / S[a]) ** 0.1 - 1) for a in (1950, 1960, 1970, 1980)}
    ratio = {y: S[y] / U[y] for y in su_years}
    peak = max(ratio, key=ratio.get)
    return {"young": young, "ours": ours, "order": ["HKG", "SGP", "KOR", "TWN"], "kor_decades": kor_dec,
            "soviet": {"years": su_years, "ratio": [ratio[y] for y in su_years], "decades": su_dec,
                       "peak_year": peak, "peak": ratio[peak]},
            "hsieh": {"SGP": "more than 2 points a year above the primal estimate", "TWN": "about 1 point above",
                      "KOR": "close to the primal", "HKG": "close to the primal"}}


# ---------------------------------------------------------------------------------------------------------------
# chapters 9-10: levels

def compute_development() -> dict:
    t = TRUTH["development"]
    rows = [r for r in data.pwt(year=t["year"]) if _fin(r["pop"]) and r["pop"] >= 1.0]
    d = gr.development_accounting(rows, alpha=t["alpha"])
    lab = {}
    for c in ("USA", "CHN", "IND", "NGA", "KOR", "BRA", "DEU", "ETH"):
        if c in d["codes"]:
            i = d["codes"].index(c)
            lab[c] = {"y": d["y_rel"][i], "ky": d["ky_rel"][i], "h": d["h_rel"][i], "A": d["A_rel"][i]}
    # five richest and five poorest by output per worker (geometric means), as Hall and Jones did for 1988
    y = np.array(d["y_rel"])
    order = np.argsort(y)
    lo, hi = order[:5], order[-5:]

    def gm(v, ix):
        return float(np.exp(np.mean(np.log(np.array(v)[ix]))))
    five = {k: gm(d[k], hi) / gm(d[k], lo) for k in ("y_rel", "ky_rel", "h_rel", "A_rel")}
    lit = {"hj_1988": {"y": 31.7, "ky": 1.8, "h": 2.2, "A": 8.3},
           "caselli_1996": {"success1": 0.40, "success2": 0.35, "hj_form": 0.26, "n": 93}}
    return {**d, "labels": lab, "five": five, "richest": [d["codes"][i] for i in hi],
            "poorest": [d["codes"][i] for i in lo], "lit": lit, "year": t["year"]}


def compute_lucas() -> dict:
    t = TRUTH["lucas"]
    rows = {r["countrycode"]: r for r in data.pwt(year=t["year"])}
    p, r = rows[t["poor"]], rows[t["rich"]]
    yp, yr = p["rgdpo"] / p["emp"], r["rgdpo"] / r["emp"]
    m = gr.mpk_ratio(yp, yr, alpha=t["alpha"], h_poor=p["hc"], h_rich=r["hc"])
    # Lucas (1990), as published: y ratio 15 (1988), alpha 0.4: 58; with Krueger's E = 5: about 5; with spillovers 1.04
    lit = {"ratio_y": 15, "raw": 15 ** 1.5, "E": 5, "with_h": 3 ** 1.5, "spill": 3 ** 1.5 / 5}
    return {"ratio_y": yr / yp, "ratio_h": r["hc"] / p["hc"], **m, "irr_poor": p["irr"], "irr_rich": r["irr"],
            "lit": lit, "year": t["year"], "alpha": t["alpha"]}


# ---------------------------------------------------------------------------------------------------------------
# chapter 11: Ramsey

def compute_ramsey() -> dict:
    kw = _solow_kw()
    t = TRUTH["ramsey"]
    r = gr.ramsey(alpha=kw["alpha"], delta=kw["delta"], rho=t["rho"], theta=t["theta"], n=kw["n"], g=kw["g"],
                  k0_share=t["k0_share"])
    gold = (kw["alpha"] / (kw["n"] + kw["g"] + kw["delta"])) ** (1 / (1 - kw["alpha"]))
    s_ramsey = 1 - r["c_ss"] / r["k_ss"] ** kw["alpha"]
    path_s = [1 - c / k ** kw["alpha"] for k, c in zip(r["path_k"], r["path_c"])]
    return {**r, "k_gold": gold, "s_ramsey": s_ramsey, "path_s": path_s[::20],
            "r_ss": kw["alpha"] * r["k_ss"] ** (kw["alpha"] - 1) - kw["delta"],
            "rate_req": t["rho"] + t["theta"] * kw["g"], "rho": t["rho"], "theta": t["theta"]}


# ---------------------------------------------------------------------------------------------------------------
# chapter 12: China

def compute_china() -> dict:
    d = {r["year"]: r for r in data.pwt("CHN")}
    years = [y for y in sorted(d) if y >= 1960 and _fin(d[y]["csh_i"], d[y]["rnna"], d[y]["rgdpna"])]
    irr_y = [y for y in years if _fin(d[y]["irr"])]
    acc = gr.growth_accounting(data.pwt("CHN"), 1980, 2019)
    acc2 = {f"{a}-{b}": gr.growth_accounting(data.pwt("CHN"), a, b) for a, b in ((1980, 1995), (1995, 2008),
                                                                               (2008, 2019))}
    return {"years": years, "inv": [d[y]["csh_i"] for y in years],
            "ky": [d[y]["rnna"] / d[y]["rgdpna"] for y in years], "irr_years": irr_y,
            "irr": [d[y]["irr"] for y in irr_y], "accounting": acc, "periods": acc2,
            "inv_1978": d[1978]["csh_i"], "inv_peak": max(d[y]["csh_i"] for y in years),
            "inv_peak_year": max(years, key=lambda y: d[y]["csh_i"]),
            "ky_1978": d[1978]["rnna"] / d[1978]["rgdpna"], "ky_last": d[years[-1]]["rnna"] / d[years[-1]]["rgdpna"],
            "last": years[-1]}


# ---------------------------------------------------------------------------------------------------------------
# chapter 13: the Dials

def compute_dial() -> dict:
    conv = compute_convergence()
    mine = conv["1960-2019"]["conditional"]["lambda"]
    d = dials.DIALS["convergence_speed"]
    row = [e for e in d.estimates if e.who.startswith("this film")]
    assert row and abs(row[0].value - round(100 * mine, 1)) < 0.051, (row, mine)
    us = {r["year"]: r for r in data.pwt("USA")}
    share = 1 - float(np.mean([us[y]["labsh"] for y in range(1950, 2020)]))
    return {"lambda_mine": mine, "capital_share_us": share,
            "half_lives": [{"who": e.who, "year": e.year, "sample": e.sample,
                            "half_life": float(np.log(2) / (e.value / 100))} for e in d.estimates]}


# ---------------------------------------------------------------------------------------------------------------
# chapter 15: the frontier

def compute_slowdown() -> dict:
    acc = compute_accounting()["us_periods"]
    conv = compute_convergence()
    pw = _pwt_by_country()
    # rolling absolute convergence: the slope of growth over 10 years on initial log GDP per head
    roll = []
    for a in range(1960, 2010):
        b = a + 10
        rows = _sample(pw, a, b, 1.0)
        c = gr.convergence([r["y0"] for r in rows], [r["y1"] for r in rows], 10)
        roll.append({"start": a, "slope": c["slope"], "se": c["se"], "n": c["n"]})
    return {"periods": {k: {"tfp": v["tfp"], "per_hour": v["per_hour"]} for k, v in acc.items()},
            "absolute_2000_2019": conv["2000-2019"]["absolute"], "rolling": roll,
            # Kremer, Willis and You (2022), as published: divergence about 0.5% a year 1985-95, convergence about
            # 0.7% a year 2005-15 (unconditional)
            "kwy": {"diverge_1985_1995": 0.005, "converge_2005_2015": 0.007}}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: the world saves

FILM_SECONDS = 42.0
MELODY_SECONDS = 52.0
FILM_FIRST, FILM_LAST = 1960, 2023
FILM_HIGHLIGHT = ("KOR", "CHN", "JPN", "SGP", "USA", "IND", "BWA")


def film_time(year: float) -> float:
    return 1.5 + FILM_SECONDS * (year - FILM_FIRST) / (FILM_LAST - FILM_FIRST)


def compute_film() -> dict:
    """For each country with a million people in 2000: its investment share (the average of the last five years, so
    the dots move smoothly) and its GDP per head at current PPPs relative to the United States, 1960-2023."""
    pw = _pwt_by_country()
    years = list(range(FILM_FIRST, FILM_LAST + 1))
    out = {"years": years, "times": [film_time(y) for y in years], "countries": {}}
    for c, d in pw.items():
        if 2000 not in d or not _fin(d[2000]["pop"]) or d[2000]["pop"] < 1.0:
            continue
        s, y, p = [], [], []
        for t in years:
            win = [d[u]["csh_i"] for u in range(t - 4, t + 1) if u in d and _fin(d[u]["csh_i"]) and d[u]["csh_i"] > 0]
            r = d.get(t)
            us = pw["USA"].get(t)
            if r and us and win and _fin(r["rgdpe"], r["pop"], us["rgdpe"], us["pop"]):
                s.append(float(np.mean(win)))
                y.append(float((r["rgdpe"] / r["pop"]) / (us["rgdpe"] / us["pop"])))
                p.append(float(r["pop"]))
            else:
                s.append(None)
                y.append(None)
                p.append(None)
        if sum(v is not None for v in y) >= 10:
            out["countries"][c] = {"s": s, "y": y, "pop": p, "name": d[2000]["country"]}
    out["highlight"] = [c for c in FILM_HIGHLIGHT if c in out["countries"]]
    yrs = {c: [t for t, v in zip(years, out["countries"][c]["y"]) if v is not None][0] for c in out["countries"]}
    out["first_year"] = yrs
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    rows = [r for r in data.pwt("KOR") if _fin(r["csh_i"]) and FILM_FIRST <= r["year"] <= FILM_LAST]
    years = [r["year"] for r in rows]
    vals = np.array([r["csh_i"] for r in rows])
    times = [film_time(y) for y in years]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=5, log=False, low=50, high=81)
    events = {"film_end": film_time(FILM_LAST) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.25, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "South Korea's investment share of GDP, 1960-2023 (Penn World Table 11.0), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ20").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": years, "seconds": MELODY_SECONDS,
            "peak_year": years[int(np.argmax(vals))], "peak": float(vals.max())}


ITEMS = {
    "hook": compute_hook,
    "kaldor": compute_kaldor,
    "harrod": compute_harrod,
    "solow": compute_solow,
    "playit": compute_playit,
    "transition": compute_transition,
    "convergence": compute_convergence,
    "accounting": compute_accounting,
    "eastasia": compute_eastasia,
    "development": compute_development,
    "lucas": compute_lucas,
    "ramsey": compute_ramsey,
    "china": compute_china,
    "dial": compute_dial,
    "slowdown": compute_slowdown,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
