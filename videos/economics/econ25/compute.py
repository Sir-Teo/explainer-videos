"""Precompute every number in Part 25 of *Economics, Built* ("Money").

    python -m videos.economics.econ25.compute            # everything missing (a minute)
    python -m videos.economics.econ25.compute --force kw

Results are cached in ``.cache/econ25/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the World Bank's money growth and inflation by country since 1960; FRED's M1, M2, the
monetary base, currency, reserves, M2's velocity, nominal GDP, the CPI and the three-month bill rate; Hanke and Krus's
hyperinflation table).  Models: Agora's money (``agora.money``) with the Island's Part 25 truths.

Items:
    barter       the chance of a double coincidence against a medium of exchange, for 2 to 12 goods
    kw           Kiyotaki and Wright's economy on the Island: holdings and media of exchange, fish fresh and smoked
    kw_region    where each equilibrium exists: type 1's gain from accepting fish, over storage costs and patience
    world        money growth against inflation by country (WDI, 1990-2024 averages), and year by year
    us_money     M2 growth and CPI inflation by decade; M2's velocity since 1959
    laffer       the inflation tax's Laffer curve with Cagan's semi-elasticity; the hyperinflation table
    deficit      a deficit financed by printing, with slow and fast expectations
    baumol       Baumol and Tobin's square-root rule; US M1 demand against the bill rate, 1959-2019
    base         the monetary base, M2 and currency since 1959: the multiplier before and after 2008
    fisher       the bill rate against inflation, by decade: the real rate
    cia          the cash-in-advance economy: the cost of inflation and the Friedman rule
    film         the intermission's data film: the base, M2 and prices since 1959, on a log scale
    melody       its data melody: M2, month by month
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import money as mo
from explainer.economics.data import tables

CACHE = Cache("econ25")
load = CACHE.load
TRUTH = island.truths(25)


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def _series(*keys):
    """Several FRED series on the dates they share."""
    out = {k: dict(zip(data.fred(k)["date"], data.fred(k)["value"])) for k in keys}
    d = sorted(set.intersection(*[set(o) for o in out.values()]))
    return d, {k: np.array([out[k][x] for x in d], float) for k in keys}


def compute_barter() -> dict:
    ns = list(range(2, 13))
    rows = [mo.barter_matches(n) for n in ns]
    return {"n": ns, "barter": [r["barter"] for r in rows], "money": [r["money"] for r in rows]}


def compute_kw() -> dict:
    T = TRUTH["kw"]
    fund = mo.kw_simulate(n=T["n"], periods=T["periods"], speculative=False, seed=T["seed"])
    spec = mo.kw_simulate(n=T["n"], periods=T["periods"], speculative=True, seed=T["seed"])
    c_fresh = T["c"]
    c_smoked = (T["c"][0], T["c"][1], T["c3_smoked"])
    out = {"fund": fund, "spec": spec, **T}
    for name, c in (("fresh", c_fresh), ("smoked", c_smoked)):
        out[f"{name}_fund"] = mo.kw_best_response(fund["dist"], c=c, u=T["u"], beta=T["beta"], speculative=False)
        out[f"{name}_spec"] = mo.kw_best_response(spec["dist"], c=c, u=T["u"], beta=T["beta"], speculative=True)
    return out


def compute_kw_region() -> dict:
    T = TRUTH["kw"]
    k = compute_kw()
    c3s = np.linspace(0.21, 0.8, 24)
    betas = np.linspace(0.5, 0.97, 20)
    fund_ok = np.zeros((len(betas), len(c3s)), bool)
    spec_ok = np.zeros_like(fund_ok)
    for i, b in enumerate(betas):
        for j, c3 in enumerate(c3s):
            c = (T["c"][0], T["c"][1], float(c3))
            fund_ok[i, j] = not mo.kw_best_response(k["fund"]["dist"], c=c, u=T["u"], beta=float(b))["accept_3"]
            spec_ok[i, j] = mo.kw_best_response(k["spec"]["dist"], c=c, u=T["u"], beta=float(b),
                                                speculative=True)["accept_3"]
    return {"c3": c3s.tolist(), "beta": betas.tolist(), "fund": fund_ok.astype(int).tolist(),
            "spec": spec_ok.astype(int).tolist()}


def compute_world() -> dict:
    rows = data.wdi_money()
    by = {}
    for r in rows:
        if 1990 <= r["year"] <= 2024 and np.isfinite(r["money"]) and np.isfinite(r["cpi"]):
            by.setdefault(r["code"], []).append(r)
    pts = []
    for code, rs in by.items():
        if len(rs) < 20:
            continue
        mg = np.array([np.log1p(x["money"] / 100) for x in rs if x["money"] > -99])
        pi = np.array([np.log1p(x["cpi"] / 100) for x in rs if x["cpi"] > -99])
        g = np.array([np.log1p(x["growth"] / 100) for x in rs if np.isfinite(x["growth"])])
        pts.append({"code": code, "country": rs[0]["country"], "region": rs[0]["region"], "years": len(rs),
                    "money": float(np.mean(mg)), "inflation": float(np.mean(pi)),
                    "growth": float(np.mean(g)) if len(g) else float("nan")})
    m = np.array([p["money"] for p in pts])
    pi = np.array([p["inflation"] for p in pts])
    g = np.array([p["growth"] for p in pts])
    slope, icept = np.polyfit(m, pi, 1)
    ok = np.isfinite(g)
    slope_g = np.polyfit(m[ok] - g[ok], pi[ok], 1)[0]
    # year by year, in countries with low inflation: money growth and inflation in the same year
    yy = [(np.log1p(r["money"] / 100), np.log1p(r["cpi"] / 100)) for r in rows
          if 1990 <= r["year"] <= 2024 and np.isfinite(r["money"]) and np.isfinite(r["cpi"]) and 0 <= r["cpi"] < 10
          and -50 < r["money"] < 100]
    yy = np.array(yy)
    lab = {}
    for name in ("United States", "Japan", "Switzerland", "Germany", "Brazil", "Argentina", "Turkiye", "Zimbabwe",
                 "Venezuela, RB", "Angola", "Belarus", "Ukraine", "Russian Federation", "China", "India", "Nigeria"):
        p = next((p for p in pts if p["country"] == name), None)
        if p:
            lab[name] = p
    return {"points": pts, "slope": float(slope), "intercept": float(icept), "corr": float(np.corrcoef(m, pi)[0, 1]),
            "slope_net": float(slope_g), "n": len(pts), "annual_corr": float(np.corrcoef(yy[:, 0], yy[:, 1])[0, 1]),
            "annual_n": int(len(yy)), "labels": lab}


def compute_us_money() -> dict:
    d, v = _series("M2SL", "CPIAUCSL")
    t = np.array([_t(x) for x in d])
    out = []
    for a in range(1960, 2030, 10):
        i0 = np.searchsorted(t, a)
        i1 = min(np.searchsorted(t, a + 10), len(t) - 1)
        if i1 - i0 < 24:
            continue
        yrs = t[i1] - t[i0]
        out.append({"decade": f"{a}s", "money": float(np.log(v["M2SL"][i1] / v["M2SL"][i0]) / yrs),
                    "inflation": float(np.log(v["CPIAUCSL"][i1] / v["CPIAUCSL"][i0]) / yrs)})
    V = data.fred("M2V")
    return {"decades": out, "v_t": [_t(x) for x in V["date"]], "v": list(V["value"]),
            "v_first": V["value"][0], "v_last": V["value"][-1], "v_max": float(np.nanmax(V["value"])),
            "v_max_when": V["date"][int(np.nanargmax(V["value"]))]}


def compute_laffer() -> dict:
    T = TRUTH["cagan"]
    L = mo.cagan_laffer(T["alpha"], mus=np.linspace(0, 1.2, 241))
    hk = tables.HANKE_KRUS_2012.data
    rows = []
    for k in ("germany", "yugoslavia", "zimbabwe", "hungary"):
        r = hk[k]
        doubling_days = np.log(2) / np.log1p(r["monthly_pct"] / 100) * 30
        rows.append({**r, "key": k, "doubling_days": float(doubling_days), "log10": float(np.log10(r["monthly_pct"]))})
    return {**L, "alpha": T["alpha"], "table": rows, "cagan": hk["cagan_germany"]}


def compute_deficit() -> dict:
    T = TRUTH["cagan"]
    slow = mo.cagan_deficit(T["alpha"], T["deficit"], T["lam_slow"], periods=T["months"])
    fast = mo.cagan_deficit(T["alpha"], T["deficit"], T["lam_fast"], periods=T["months"])
    big = mo.cagan_deficit(T["alpha"], 0.09, T["lam_slow"], periods=T["months"])
    return {"slow": slow, "fast": fast, "big": big, **T}


def compute_baumol() -> dict:
    T = TRUTH["baumol"]
    i = np.linspace(0.002, 0.02, 60)
    bt = mo.baumol_tobin(T["Y"], i, T["b"])
    # US M1 demand: ln(M1/GDP) against the bill rate, quarterly, 1959-2019 (M1 was redefined in 2020)
    d, v = _series("M1SL", "TB3MS")
    G = data.fred("GDP")
    gmap = dict(zip(G["date"], G["value"]))
    pts = []
    for x, m1, r in zip(d, v["M1SL"], v["TB3MS"]):
        if x in gmap and "1959" <= x[:4] <= "2019" and np.isfinite(m1) and np.isfinite(r):
            pts.append((_t(x), r, np.log(m1 / gmap[x])))
    t, r, lm = (np.array(z) for z in zip(*pts))
    slope_all, b0 = np.polyfit(r, lm, 1)
    pre = t < 1981
    slope_pre = np.polyfit(r[pre], lm[pre], 1)[0]
    post = t >= 1994
    slope_post = np.polyfit(r[post], lm[post], 1)[0]
    return {"i": i.tolist(), **bt, **T, "t": t.tolist(), "rate": r.tolist(), "lm": lm.tolist(),
            "semi_all": float(slope_all), "semi_pre": float(slope_pre), "semi_post": float(slope_post),
            "intercept": float(b0)}


def compute_base() -> dict:
    d, v = _series("BOGMBASE", "M2SL", "CURRCIR", "TOTRESNS")
    t = [_t(x) for x in d]
    mult = v["M2SL"] / v["BOGMBASE"]
    k07 = d.index("2007-12-01")
    k14 = d.index("2014-08-01")
    return {"t": t, "base": v["BOGMBASE"].tolist(), "m2": v["M2SL"].tolist(), "currency": v["CURRCIR"].tolist(),
            "reserves": v["TOTRESNS"].tolist(), "mult": mult.tolist(), "mult_2007": float(mult[k07]),
            "mult_2014": float(mult[k14]), "base_2007": float(v["BOGMBASE"][k07]),
            "base_2014": float(v["BOGMBASE"][k14]), "m2_2007": float(v["M2SL"][k07]),
            "m2_2014": float(v["M2SL"][k14]), "reserves_2007": float(v["TOTRESNS"][k07]),
            "reserves_2014": float(v["TOTRESNS"][k14]), "last": d[-1],
            "currency_share_last": float(v["CURRCIR"][-1] / v["M2SL"][-1])}


def compute_fisher() -> dict:
    d, v = _series("TB3MS", "CPIAUCSL")
    t = np.array([_t(x) for x in d])
    cpi = v["CPIAUCSL"]
    infl = np.full(len(cpi), np.nan)
    infl[12:] = 100 * (cpi[12:] / cpi[:-12] - 1)
    rows = []
    for a in range(1960, 2030, 10):
        m = (t >= a) & (t < a + 10) & np.isfinite(infl)
        if m.sum() < 24:
            continue
        rows.append({"decade": f"{a}s", "rate": float(np.mean(v["TB3MS"][m])), "inflation": float(np.mean(infl[m])),
                     "real": float(np.mean(v["TB3MS"][m] - infl[m]))})
    ok = np.isfinite(infl)
    return {"t": t[ok].tolist(), "rate": v["TB3MS"][ok].tolist(), "inflation": infl[ok].tolist(), "decades": rows}


def compute_cia() -> dict:
    T = TRUTH["cia"]
    mus = np.linspace(T["beta"] - 1, 0.5, 200)
    c = mo.cia(mus, beta=T["beta"], a=T["a"])
    at = {f"{int(round(100 * x))}": float(mo.cia([x], beta=T["beta"], a=T["a"])["loss"][0])
          for x in (0.0, 0.02, 0.10, 0.5)}
    return {**c, **T, "at": at}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1959.0, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    d, v = _series("BOGMBASE", "M2SL", "CPIAUCSL")
    t = np.array([_t(x) for x in d])
    idx = {k: (v[k] / v[k][0]).tolist() for k in v}
    return {"t": t.tolist(), "base": idx["BOGMBASE"], "m2": idx["M2SL"], "cpi": idx["CPIAUCSL"],
            "times": [film_time(x) for x in t], "first": float(t[0]), "last": float(t[-1]),
            "base_end": idx["BOGMBASE"][-1], "m2_end": idx["M2SL"][-1], "cpi_end": idx["CPIAUCSL"][-1]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    qs = np.arange(t[0], t[-1] + 1e-9, 0.5)
    vals = np.interp(qs, t, f["m2"])
    times = [film_time(x) for x in qs]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=6, log=True, low=45, high=84)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], qs)],
                meta={"label": "US M2, half-year by half-year, 1959-2026 (Federal Reserve via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ25").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": qs.tolist(), "seconds": MELODY_SECONDS}


ITEMS = {
    "barter": compute_barter,
    "kw": compute_kw,
    "kw_region": compute_kw_region,
    "world": compute_world,
    "us_money": compute_us_money,
    "laffer": compute_laffer,
    "deficit": compute_deficit,
    "baumol": compute_baumol,
    "base": compute_base,
    "fisher": compute_fisher,
    "cia": compute_cia,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
