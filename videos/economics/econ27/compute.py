"""Precompute every number in Part 27 of *Economics, Built* ("The Keynesian Revolution").

    python -m videos.economics.econ27.compute            # everything missing (half a minute)
    python -m videos.economics.econ27.compute --force coop_path

Results are cached in ``.cache/econ27/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's real GNP and GDP deflator from 1929, the NBER's unemployment rate 1929-1942,
industrial production, America's monetary gold stock 1914-1946, real GDP against the CBO's potential, the
unemployment rate and its natural rate, the NBER's recession months since 1854, the federal funds rate and Japan's
call rate).  Models: Agora's Keynesian economy (``agora.keynes``) with the Island's Part 27 truths.

Items:
    coop_path    the Island's co-op, week by week: a recession, then the board prints coupons
    coop_curve   evenings out per couple against coupons per couple
    depression   the United States, 1929-1941: real GNP, prices, unemployment, industrial production
    cross        the Keynesian cross and Kahn's multiplier, round by round
    thrift       the paradox of thrift, with investment fixed and with investment rising with income
    islm         IS and LM curves; fiscal and monetary policy; a slump into the liquidity trap
    trap         the policy rate at zero: Japan's call rate since 1985 and the federal funds rate since 2000
    moniac       Phillips's machine: income and its flows when government purchases rise
    wages        notional and actual pay changes when cuts are resisted
    asad         aggregate demand and supply: a demand shock and a supply shock
    gold         America's gold stock and industrial production, 1929-1941
    okun         Okun's law: the unemployment gap on the output gap, quarterly since 1949
    spells       the length of American expansions and recessions since 1854
    film         the intermission's data film: industrial production month by month, 1919-1945
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import keynes as ks

CACHE = Cache("econ27")
load = CACHE.load
TRUTH = island.truths(27)


def _t(d: str) -> float:
    y, m = int(d[:4]), int(d[5:7])
    return y + (m - 1) / 12


def _annual(key: str) -> dict:
    d = data.fred(key)
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items()}


def _between(key: str, first: str, last: str) -> tuple[list, list]:
    d = data.fred(key)
    pts = [(x, v) for x, v in zip(d["date"], d["value"]) if first <= x <= last and np.isfinite(v)]
    return [_t(x) for x, _ in pts], [v for _, v in pts]


def compute_coop_path() -> dict:
    C = TRUTH["coop"]
    r = ks.coop(n=C["n"], coupons=C["start"], target=C["target"], weeks=C["weeks"], p=C["p"], seed=C["seed"],
                print_at=C["print_at"], print_to=C["print_to"])
    ev = np.array(r["evenings"])
    smooth = np.convolve(ev, np.ones(4) / 4, mode="same")
    k = C["print_at"]
    return {**C, "weeks_": list(range(C["weeks"])), "evenings": ev.tolist(), "smooth": smooth.tolist(),
            "money": r["money"], "before": float(ev[20:k].mean()), "after": float(ev[k + 20:].mean()),
            "potential": r["potential"], "goers_before": float(np.mean(r["goers"][20:k])),
            "sitters_before": float(np.mean(r["sitters"][20:k]))}


def compute_coop_curve() -> dict:
    C = TRUTH["coop"]
    levels = np.arange(1, 25)
    c = ks.coop_curve(levels, n=C["n"], target=C["target"], p=C["p"], seed=C["seed"])
    k = int(np.argmax(c["evenings"]))
    return {**c, "best": c["coupons"][k], "best_evenings": c["evenings"][k], "target": C["target"],
            "potential": C["p"] * (1 - C["p"])}


def compute_depression() -> dict:
    gnp = _annual("GNPCA")
    defl = _annual("A191RD3A086NBEA")
    un = _annual("M0892AUSM156SNBR")
    yrs = list(range(1929, 1942))
    t_ip, ip = _between("INDPRO", "1929-01-01", "1941-12-01")
    i29, i33 = gnp[1929], gnp[1933]
    return {"years": yrs, "gnp": [gnp[y] for y in yrs], "deflator": [defl[y] for y in yrs],
            "unemployment": [un.get(y, float("nan")) for y in yrs], "ip_t": t_ip, "ip": ip,
            "gnp_fall": 100 * (1 - i33 / i29), "price_fall": 100 * (1 - defl[1933] / defl[1929]),
            "u29": un[1929], "u33": un[1933], "u_peak": max(un[y] for y in yrs if y in un),
            "gnp_back": next(y for y in yrs if y > 1933 and gnp[y] >= i29),
            "ip_fall": 100 * (1 - min(ip) / max(ip[:12]))}


def compute_cross() -> dict:
    C = TRUTH["cross"]
    base = ks.cross(C["a"], C["b"], C["I"], C["G"], C["T"])
    up = ks.cross(C["a"], C["b"], C["I"], C["G"] + C["dG"], C["T"])
    rounds = ks.multiplier_rounds(C["dG"], C["b"], 14)
    return {**C, "base": base, "up": up, "rounds": rounds}


def compute_thrift() -> dict:
    T = TRUTH["thrift"]
    fixed = ks.paradox_of_thrift(T["a"], T["b"], T["I"], 0.0, T["da"], h=0.0)
    induced = ks.paradox_of_thrift(T["a"], T["b"], T["I"], 0.0, T["da"], h=T["h"])
    return {**T, "fixed": fixed, "induced": induced}


def compute_islm() -> dict:
    P = TRUTH["islm"]
    kw = {k: P[k] for k in ("a", "b", "T", "I0", "d", "k", "h")}
    base = ks.islm(P["G"], P["M"], **kw)
    fiscal = ks.islm(P["G"] + P["dG"], P["M"], **kw)
    money = ks.islm(P["G"], P["M"] + P["dM"], **kw)
    slump_kw = {**kw, "I0": P["I0"] - P["slump"]}
    slump = ks.islm(P["G"], P["M"], **slump_kw)
    slump_money = ks.islm(P["G"], P["M"] + 2 * P["dM"], **slump_kw)
    slump_fiscal = ks.islm(P["G"] + P["dG"], P["M"] + 2 * P["dM"], **slump_kw)
    # expected inflation in percent a year, like the interest rate: deflation of 2% raises the real rate at i = 0
    deflation = ks.islm(P["G"], P["M"] + 2 * P["dM"], **{**slump_kw, "pe": -2.0})
    promise = ks.islm(P["G"], P["M"] + 2 * P["dM"], **{**slump_kw, "pe": 2.0})
    Y = np.linspace(1000, 1800, 161)
    i = np.linspace(0, 8, 161)
    return {**P, "slump_size": P["slump"], "base": base, "fiscal": fiscal, "money": money, "slump": slump,
            "slump_money": slump_money,
            "slump_fiscal": slump_fiscal, "deflation": deflation, "promise": promise, "i": i.tolist(), "Y": Y.tolist(),
            "is0": ks.is_curve(P["G"], i, **{k: kw[k] for k in ("a", "b", "T", "I0", "d")}).tolist(),
            "is1": ks.is_curve(P["G"] + P["dG"], i, **{k: kw[k] for k in ("a", "b", "T", "I0", "d")}).tolist(),
            "is_slump": ks.is_curve(P["G"], i, **{**{k: kw[k] for k in ("a", "b", "T", "d")},
                                                  "I0": P["I0"] - P["slump"]}).tolist(),
            "is_slump_fiscal": ks.is_curve(P["G"] + P["dG"], i, **{**{k: kw[k] for k in ("a", "b", "T", "d")},
                                                                   "I0": P["I0"] - P["slump"]}).tolist(),
            "lm0": ks.lm_curve(P["M"], Y, k=P["k"], h=P["h"]).tolist(),
            "lm1": ks.lm_curve(P["M"] + P["dM"], Y, k=P["k"], h=P["h"]).tolist(),
            "lm2": ks.lm_curve(P["M"] + 2 * P["dM"], Y, k=P["k"], h=P["h"]).tolist(),
            "fiscal_mult": (fiscal["Y"] - base["Y"]) / P["dG"], "cross_mult": 1 / (1 - P["b"]),
            "trap_fiscal_mult": (slump_fiscal["Y"] - slump_money["Y"]) / P["dG"]}


def compute_trap() -> dict:
    tj, vj = _between("IRSTCI01JPM156N", "1985-01-01", "2026-12-01")
    tu, vu = _between("FEDFUNDS", "2000-01-01", "2026-12-01")
    j = dict(zip(tj, vj))
    first_low = next(t for t, v in zip(tj, vj) if v < 0.5)
    return {"jp_t": tj, "jp": vj, "us_t": tu, "us": vu, "jp_1990": max(v for t, v in j.items() if 1990 <= t < 1991),
            "jp_below_half": first_low, "us_zero_months": int(sum(1 for v in vu if v < 0.25))}


def compute_moniac() -> dict:
    M = TRUTH["moniac"]
    return {**M, **ks.moniac(b=M["b"], tax=M["tax"], I=M["I"], G=M["G"], Y0=(M["I"] + M["G"]) /
                              (1 - M["b"] * (1 - M["tax"])), speed=M["speed"], steps=M["steps"],
                              shock_at=M["shock_at"], dG=M["dG"])}


def compute_wages() -> dict:
    W = TRUTH["wages"]
    w = ks.wage_changes(n=W["n"], mean=W["mean"], sd=W["sd"], rigid=W["rigid"], seed=W["seed"])
    edges = np.linspace(-0.12, 0.14, 53)
    hw, _ = np.histogram(w["want"], edges)
    hg, _ = np.histogram(w["got"], edges)
    return {**W, **{k: v for k, v in w.items() if k not in ("want", "got")}, "edges": edges.tolist(),
            "hist_want": (hw / W["n"]).tolist(), "hist_got": (hg / W["n"]).tolist()}


def compute_asad() -> dict:
    A = TRUTH["asad"]
    I = TRUTH["islm"]
    kw = {k: I[k] for k in ("a", "b", "T", "I0", "d", "k", "h")}
    P = np.linspace(0.6, 1.6, 101)
    ad0 = ks.ad_curve(P, I["G"], I["M"], **kw)
    ad1 = ks.ad_curve(P, I["G"], I["M"] + A["dM"], **kw)
    as0 = ks.as_curve(P, A["Ystar"], A["Pe"], A["kappa"])
    as1 = ks.as_curve(P - A["cost"], A["Ystar"], A["Pe"], A["kappa"])
    e0 = ks.asad(I["G"], I["M"], A["Ystar"], A["Pe"], A["kappa"], **kw)
    e1 = ks.asad(I["G"], I["M"] + A["dM"], A["Ystar"], A["Pe"], A["kappa"], **kw)
    e2 = ks.asad(I["G"], I["M"], A["Ystar"], A["Pe"], A["kappa"], cost=A["cost"], **kw)
    return {**A, "P": P.tolist(), "ad0": ad0.tolist(), "ad1": ad1.tolist(), "as0": as0.tolist(), "as1": as1.tolist(),
            "e0": e0, "demand": e1, "supply": e2}


def compute_gold() -> dict:
    tg, vg = _between("M1476BUSM027NNBR", "1929-01-01", "1941-12-01")
    ti, vi = _between("INDPRO", "1929-01-01", "1941-12-01")
    g = dict(zip(tg, vg))
    i = dict(zip(ti, vi))
    return {"t": tg, "gold": vg, "ip_t": ti, "ip": vi, "gold_1933": g[_t("1933-03-01")],
            "gold_1934": g[_t("1934-02-01")], "gold_1941": g[_t("1941-12-01")],
            "ip_1933": i[_t("1933-03-01")], "ip_1937": max(v for t, v in i.items() if 1937 <= t < 1938),
            "ip_1938": min(v for t, v in i.items() if 1938 <= t < 1939), "ip_1929": max(v for t, v in i.items()
                                                                                          if t < 1930),
            "ip_1941": i[_t("1941-12-01")]}


def compute_okun() -> dict:
    gdp = dict(zip(data.fred("GDPC1")["date"], data.fred("GDPC1")["value"]))
    pot = dict(zip(data.fred("GDPPOT")["date"], data.fred("GDPPOT")["value"]))
    un = data.fred("UNRATE")
    nr = dict(zip(data.fred("NROU")["date"], data.fred("NROU")["value"]))
    uq: dict = {}
    for x, v in zip(un["date"], un["value"]):
        q = f"{x[:4]}-{(int(x[5:7]) - 1) // 3 * 3 + 1:02d}-01"
        uq.setdefault(q, []).append(v)
    # a quarter counts only with all three months (the BLS took no survey in October 2025)
    dates = sorted(d for d in gdp if d in pot and d in nr and d in uq and len(uq[d]) == 3 and
                   all(np.isfinite(uq[d])) and np.isfinite(gdp[d]) and d <= "2025-12-31")
    gap = np.array([100 * (gdp[d] / pot[d] - 1) for d in dates])
    ugap = np.array([np.mean(uq[d]) - nr[d] for d in dates])
    X = np.column_stack([np.ones_like(gap), gap])
    beta, *_ = np.linalg.lstsq(X, ugap, rcond=None)
    res = ugap - X @ beta
    r2 = 1 - res.var() / ugap.var()
    # Okun's own form: output points per point of unemployment
    Xu = np.column_stack([np.ones_like(ugap), ugap])
    g2, *_ = np.linalg.lstsq(Xu, gap, rcond=None)
    pre = [k for k, d in enumerate(dates) if d < "2020-01-01"]
    bp, *_ = np.linalg.lstsq(X[pre], ugap[pre], rcond=None)
    return {"dates": dates, "t": [_t(d) for d in dates], "gap": gap.tolist(), "ugap": ugap.tolist(),
            "beta": float(beta[1]), "alpha": float(beta[0]), "r2": float(r2), "okun_points": float(g2[1]),
            "beta_pre2020": float(bp[1]), "first": dates[0], "last": dates[-1], "n": len(dates)}


def compute_spells() -> dict:
    d = data.fred("USREC")
    s = ks.spells(d["value"], d["date"])
    rec, exp = np.array(s["recessions"]), np.array(s["expansions"])
    rs, es = np.array(s["rec_start"]), np.array(s["exp_start"])
    post = rs >= 1945
    post_e = es >= 1945
    return {**s, "rec_mean": float(rec.mean()), "exp_mean": float(exp.mean()), "rec_mean_post": float(rec[post].mean()),
            "exp_mean_post": float(exp[post_e].mean()), "n_rec": int(len(rec)), "n_rec_post": int(post.sum()),
            "longest_exp": int(exp.max()), "longest_exp_start": int(es[np.argmax(exp)])}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1919.0, last: float = 1946.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    t, v = _between("INDPRO", "1919-01-01", "1945-12-01")
    vv = np.array(v)
    k29 = int(np.argmax([x if tt < 1930 else 0 for tt, x in zip(t, v)]))
    return {"t": t, "ip": v, "times": [film_time(x) for x in t], "first": t[0], "last": t[-1],
            "peak29": float(vv[k29]), "trough": float(vv[[k for k, tt in enumerate(t) if tt < 1934]].min()),
            "peak_war": float(vv.max()), "end": float(vv[-1])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["ip"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=6, log=True, low=40, high=86)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "American industrial production, month by month, 1919-1945 (Federal Reserve via FRED), "
                               "as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ27").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "coop_path": compute_coop_path,
    "coop_curve": compute_coop_curve,
    "depression": compute_depression,
    "cross": compute_cross,
    "thrift": compute_thrift,
    "islm": compute_islm,
    "trap": compute_trap,
    "moniac": compute_moniac,
    "wages": compute_wages,
    "asad": compute_asad,
    "gold": compute_gold,
    "okun": compute_okun,
    "spells": compute_spells,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
