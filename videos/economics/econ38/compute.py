"""Precompute every number in Part 38 of *Economics, Built* ("Work and Wages").

    python -m videos.economics.econ38.compute            # everything missing (about a minute)
    python -m videos.economics.econ38.compute --force ck

Results are cached in ``.cache/econ38/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Card and Krueger's 410 restaurants; Wooldridge's labour datasets (Card's 1995 young
men, the 1976 Current Population Survey, the 1980 National Longitudinal Survey); FRED's federal minimum wage and
consumer prices; the tables of Neumark and Wascher, Cengiz et al., Jardim et al., the cab-driver studies, Chetty et
al., Sokolova and Sorensen, Angrist and Krueger, Oreopoulos, the Mariel studies and the 1979 survey).  Models:
Agora's labour (``agora.labour``) with the Island's Part 38 truths.

Items:
    ck           Card and Krueger's data: employment and starting wages by state and wave, the difference in
                 differences, the own-wage elasticity with a bootstrap interval, entrée prices
    supply       labour supply with income effects: hours against the wage, the three elasticities, participation
    market       a competitive market and a wage floor
    monopsony    one employer: supply, marginal cost of labour, marginal product; employment against the minimum
    border       the border experiment on the Island, under competition and under monopsony, 200 times each
    mincer       Mincer's equation on the 1976 CPS; log wages by schooling for Card's young men
    returns      the return to schooling: least squares, college proximity as an instrument, ability bias with IQ
    roy          Roy's two occupations and Heckman's correction
    film         the intermission's data film: the federal minimum wage in 2025 dollars, 1938-2025
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import labour
from explainer.economics.data import tables

CACHE = Cache("econ38")
load = CACHE.load
TRUTH = island.truths(38)
FILM_SECONDS = 50.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _arr(d, k):
    return np.array(d[k], float)


def _ck_frame():
    D = data.njmin()
    st = _arr(D, "state")
    fte1 = _arr(D, "empft") + _arr(D, "nmgrs") + 0.5 * _arr(D, "emppt")
    fte2 = _arr(D, "empft2") + _arr(D, "nmgrs2") + 0.5 * _arr(D, "emppt2")
    closed = _arr(D, "status2") == 3
    fte2 = np.where(closed, 0.0, fte2)
    return D, st, fte1, fte2, _arr(D, "wage_st"), _arr(D, "wage_st2")


def compute_ck() -> dict:
    D, st, f1, f2, w1, w2 = _ck_frame()
    out = {}
    for s, nm in ((1, "nj"), (0, "pa")):
        g = st == s
        a, b = f1[g & np.isfinite(f1)], f2[g & np.isfinite(f2)]
        out[nm] = {"before": float(a.mean()), "after": float(b.mean()), "n_before": int(a.size), "n_after": int(b.size),
                   "se_before": float(a.std(ddof=1) / np.sqrt(a.size)),
                   "se_after": float(b.std(ddof=1) / np.sqrt(b.size)),
                   "wage_before": float(np.nanmean(w1[g])), "wage_after": float(np.nanmean(w2[g])),
                   "at_old": float(np.nanmean(np.isclose(w1[g], 4.25))),
                   "below_new_before": float(np.nanmean(w1[g][np.isfinite(w1[g])] < 5.05)),
                   "at_new_after": float(np.nanmean(np.isclose(w2[g][np.isfinite(w2[g])], 5.05)))}
    did = (out["nj"]["after"] - out["nj"]["before"]) - (out["pa"]["after"] - out["pa"]["before"])
    # the balanced panel: stores with employment in both waves (closed stores at zero)
    ok = np.isfinite(f1) & np.isfinite(f2)
    dnj, dpa = (f2 - f1)[ok & (st == 1)], (f2 - f1)[ok & (st == 0)]
    did_bal = float(dnj.mean() - dpa.mean())
    se_bal = float(np.sqrt(dnj.var(ddof=1) / dnj.size + dpa.var(ddof=1) / dpa.size))
    # the own-wage elasticity: proportional changes, relative to Pennsylvania, with a store bootstrap
    okw = ok & np.isfinite(w1) & np.isfinite(w2)

    def owe(idx):
        s1 = st[idx] == 1
        F1, F2, W1, W2 = f1[idx], f2[idx], w1[idx], w2[idx]
        de = (F2[s1].mean() / F1[s1].mean()) / (F2[~s1].mean() / F1[~s1].mean()) - 1
        dw = (W2[s1].mean() / W1[s1].mean()) / (W2[~s1].mean() / W1[~s1].mean()) - 1
        return de, dw, de / dw

    idx = np.flatnonzero(okw)
    de, dw, e = owe(idx)
    rng = np.random.default_rng(38)
    nj_i, pa_i = idx[st[idx] == 1], idx[st[idx] == 0]
    boots = []
    for _ in range(2000):
        b = np.r_[rng.choice(nj_i, nj_i.size), rng.choice(pa_i, pa_i.size)]
        boots.append(owe(b)[2])
    lo, hi = np.percentile(boots, [5, 95])
    # starting wages: distributions by state and wave
    bins = np.round(np.arange(4.20, 5.85, 0.10), 2)
    hist = {}
    for s, nm in ((1, "nj"), (0, "pa")):
        for wv, ww in (("before", w1), ("after", w2)):
            v = ww[(st == s) & np.isfinite(ww)]
            h, _ = np.histogram(v, bins=bins)
            hist[f"{nm}_{wv}"] = (h / max(v.size, 1)).tolist()
    p1, p2 = _arr(D, "pentree"), _arr(D, "pentree2")
    pr = {}
    for s, nm in ((1, "nj"), (0, "pa")):
        g = (st == s) & np.isfinite(p1) & np.isfinite(p2)
        pr[nm] = float(np.log(p2[g]).mean() - np.log(p1[g]).mean())
    return {**out, "did": float(did), "did_balanced": did_bal, "se_balanced": se_bal, "emp_rel": float(de),
            "wage_rel": float(dw), "owe": float(e), "owe_lo": float(lo), "owe_hi": float(hi), "bins": bins.tolist(),
            "hist": hist, "price_nj": pr["nj"], "price_pa": pr["pa"], "closed": int((_arr(D, "status2") == 3).sum()),
            "m0": tables.CK_1994.data["m0"], "m1": tables.CK_1994.data["m1"], "stores": tables.CK_1994.data["stores"],
            "n_nj": tables.CK_1994.data["nj"], "n_pa": tables.CK_1994.data["pa"]}


def compute_supply() -> dict:
    S = TRUTH["supply"]
    kw = {k: S[k] for k in ("y", "gamma", "phi", "psi")}
    ws = np.linspace(1.0, 50.0, 120)
    h = [labour.hours(w, **kw) for w in ws]
    peak = float(ws[int(np.argmax(h))])
    el = {f"{w:.0f}": labour.supply_elasticities(w, **kw) for w in (6.0, 30.0)}
    part = labour.participation(ws, np.log(S["res_median"]), S["res_sd"]).tolist()
    return {"w": ws.tolist(), "h": h, "peak": peak, "el": el, "participation": part, **S,
            "chetty": tables.CHETTY_2011.data, "cabs": tables.CABS.data}


def compute_market() -> dict:
    M = TRUTH["market"]
    eq = labour.competitive(**M)
    ms = np.linspace(eq["w"] * 0.6, eq["w"] * 1.6, 100)
    emp = labour.floor_competitive(ms, **M).tolist()
    m19 = eq["w"] * 1.188
    L19 = float(labour.floor_competitive(m19, **M))
    return {**eq, "m": ms.tolist(), "emp": emp, "m19": m19, "L19": L19, "drop19": L19 / eq["L"] - 1,
            "supply_at_m19": float(M["B"] * m19 ** M["eps_s"]), **M}


def compute_monopsony() -> dict:
    P = TRUTH["monopsony"]
    R = labour.monopsony(**P)
    Ls = np.linspace(20, 320, 150)
    w_sup = (Ls / P["B"]) ** (1 / P["eta"])
    mcl = w_sup * (1 + 1 / P["eta"])
    mrpl = P["a"] * Ls ** (-P["b"])
    ms = np.linspace(R["w_m"] * 0.92, R["w_c"] * 1.18, 120)
    emp = labour.floor_monopsony(ms, **P).tolist()
    return {**R, "L": Ls.tolist(), "w_sup": w_sup.tolist(), "mcl": mcl.tolist(), "mrpl": mrpl.tolist(),
            "m": ms.tolist(), "emp": emp, **P, "ss": tables.SS_2021.data}


def compute_border() -> dict:
    B = TRUTH["border"]
    kw = {k: B[k] for k in ("n_treat", "n_ctrl", "m0", "m1", "eps_d", "eta", "trend", "noise")}
    res = {}
    for reg in ("competitive", "monopsony"):
        runs = [labour.border_experiment(reg, seed=s, **kw) for s in range(B["seeds"])]
        d = np.array([r["did_emp"] for r in runs])
        o = np.array([r["owe"] for r in runs])
        res[reg] = {"did": d.tolist(), "owe": o.tolist(), "mean_did": float(d.mean()), "mean_owe": float(o.mean()),
                    "share_negative": float((d < 0).mean()), "did_wage": float(runs[0]["did_wage"]),
                    "se": float(runs[0]["se_emp"])}
    ck = compute_ck()
    return {**res, "ck_owe": ck["owe"], "ck_emp": float(np.log1p(ck["emp_rel"])), **B}


def compute_hicks() -> dict:
    """Hicks's formula for the elasticity of labour demand in a competitive industry with constant returns and other
    inputs in elastic supply: -[(1 - s) sigma + s eps], with s labour's share of costs, sigma the elasticity of
    substitution and eps the elasticity of demand for the product."""
    sh = np.linspace(0, 1, 41)
    cases = [(0.5, 0.5), (0.5, 2.0), (1.5, 0.5)]
    lines = [[(1 - x) * sg + x * ep for x in sh] for sg, ep in cases]
    M = TRUTH["market"]
    return {"s": sh.tolist(), "cases": cases, "lines": lines, "island": {"s": 0.3, "sigma": 0.5, "eps": 0.5,
                                                                        "eta": 0.7 * 0.5 + 0.3 * 0.5},
            "eps_d": M["eps_d"]}


def compute_power() -> dict:
    """The border design's precision as the number of stores grows, and with the same stores split evenly."""
    B = TRUTH["border"]
    kw = {k: B[k] for k in ("m0", "m1", "eps_d", "eta", "trend", "noise")}
    out = []
    for f in (0.5, 1, 2, 4, 8, 16):
        nt, nc = int(round(B["n_treat"] * f)), int(round(B["n_ctrl"] * f))
        d = [labour.border_experiment("competitive", n_treat=nt, n_ctrl=nc, seed=1000 + s, **kw)["did_emp"]
             for s in range(60)]
        out.append({"f": f, "n": nt + nc, "sd": float(np.std(d, ddof=1)), "mean": float(np.mean(d))})
    n = B["n_treat"] + B["n_ctrl"]
    even = [labour.border_experiment("competitive", n_treat=n // 2, n_ctrl=n - n // 2, seed=2000 + s, **kw)["did_emp"]
            for s in range(60)]
    eff = float(np.mean([r["mean"] for r in out]))
    # stores needed for 80% power at 5% (two-sided): the standard error must be |effect| / 2.8
    sd1 = out[1]["sd"]
    need = n * (sd1 / (abs(eff) / 2.8)) ** 2
    return {"rows": out, "even_sd": float(np.std(even, ddof=1)), "n": n, "effect": eff, "need": float(need),
            "n_treat": B["n_treat"], "n_ctrl": B["n_ctrl"]}


def compute_mincer() -> dict:
    W = data.wooldridge("wage1")
    y, s, x = _arr(W, "lwage"), _arr(W, "educ"), _arr(W, "exper")
    X = np.column_stack([np.ones_like(s), s, x, x ** 2])
    r = labour.ols(y, X)
    C = data.wooldridge("card")
    yc, sc = _arr(C, "lwage"), _arr(C, "educ")
    years = list(range(8, 19))
    means = [float(yc[sc == k].mean()) if (sc == k).sum() > 20 else None for k in years]
    counts = [int((sc == k).sum()) for k in years]
    rc = labour.ols(yc, np.column_stack([np.ones_like(sc), sc]))
    peak_exp = -r["b"][2] / (2 * r["b"][3])
    return {"b": r["b"], "se": r["se"], "n": r["n"], "r2": r["r2"], "peak_exper": float(peak_exp),
            "years": years, "means": means, "counts": counts, "card_slope": rc["b"][1], "card_icpt": rc["b"][0],
            "n_card": int(len(yc)), "mean_wage1976": float(np.mean(_arr(W, "wage")))}


def compute_returns() -> dict:
    C = data.wooldridge("card")
    y, s = _arr(C, "lwage"), _arr(C, "educ")
    ex, ex2 = _arr(C, "exper"), _arr(C, "expersq")
    ctrl = [_arr(C, k) for k in ("black", "smsa", "south", "smsa66", "reg662", "reg663", "reg664", "reg665", "reg666",
                                 "reg667", "reg668", "reg669")]
    one = np.ones_like(s)
    X = np.column_stack([one, s, ex, ex2, *ctrl])
    Z = np.column_stack([one, _arr(C, "nearc4"), ex, ex2, *ctrl])
    o = labour.ols(y, X)
    iv = labour.tsls(y, X, Z)
    near = _arr(C, "nearc4") > 0.5
    W2 = data.wooldridge("wage2")
    y2, s2, iq = _arr(W2, "lwage"), _arr(W2, "educ"), _arr(W2, "IQ")
    x2, t2 = _arr(W2, "exper"), _arr(W2, "tenure")
    one2 = np.ones_like(s2)
    a = labour.ols(y2, np.column_stack([one2, s2, x2, t2]))
    b = labour.ols(y2, np.column_stack([one2, s2, x2, t2, iq]))
    iq_by_s = labour.ols(iq, np.column_stack([one2, s2]))
    return {"ols": o["b"][1], "ols_se": o["se"][1], "iv": iv["b"][1], "iv_se": iv["se"][1], "F": iv["first_stage_F"],
            "n": o["n"], "educ_near": float(s[near].mean()), "educ_far": float(s[~near].mean()),
            "lwage_near": float(y[near].mean()), "lwage_far": float(y[~near].mean()), "share_near": float(near.mean()),
            "w2_ols": a["b"][1], "w2_ols_se": a["se"][1], "w2_iq": b["b"][1], "w2_iq_se": b["se"][1],
            "iq_coef": b["b"][4], "iq_per_year": iq_by_s["b"][1], "n2": a["n"], "ak": tables.AK_1991.data,
            "oreo": tables.OREOPOULOS_2006.data}


def compute_roy() -> dict:
    R = TRUTH["roy"]
    r = labour.roy(**R)
    w1, z, sec = np.array(r["w1"]), np.array(r["z"]), np.array(r["second"])
    one = np.ones_like(w1)
    H = labour.heckman_two_step(w1, one[:, None], ~sec, np.column_stack([one, z]))
    w2 = np.array(r["w2"])
    return {k: v for k, v in r.items() if not isinstance(v, list)} | {
        "naive": H["naive"][0], "corrected": H["corrected"][0], "lambda": H["lambda"], "truth": float(w1.mean()),
        "sample_w1": w1[:600].tolist(), "sample_w2": w2[:600].tolist(), "sample_second": sec[:600].tolist(), **R}


def film_time(t: float, first: float = 1938.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def _annual(key: str) -> dict:
    d = data.fred(key)
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items()}


def compute_film() -> dict:
    mw = _annual("FEDMINNFRWG")
    cpi = _annual("CPIAUCNS")
    ys = [y for y in sorted(mw) if 1938 <= y <= 2025 and y in cpi]
    real = [mw[y] * cpi[2025] / cpi[y] for y in ys]
    nominal = [mw[y] for y in ys]
    k = int(np.argmax(real))
    return {"t": ys, "v": real, "nominal": nominal, "times": [film_time(y) for y in ys], "peak": real[k],
            "peak_y": ys[k], "last": real[-1], "last_nominal": nominal[-1], "first": real[0],
            "y1992": real[ys.index(1992)],
            "since2009": nominal[ys.index(2009)]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=8, log=False, low=40, high=86)
    events = {"film_end": film_time(2025) + 6.0, "first": times[0], "peak": film_time(f["peak_y"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"${x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the federal minimum wage in 2025 dollars, 1938-2025 (Department of Labor and BLS, "
                               "via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ38").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "ck": compute_ck,
    "supply": compute_supply,
    "market": compute_market,
    "monopsony": compute_monopsony,
    "border": compute_border,
    "hicks": compute_hicks,
    "power": compute_power,
    "mincer": compute_mincer,
    "returns": compute_returns,
    "roy": compute_roy,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
