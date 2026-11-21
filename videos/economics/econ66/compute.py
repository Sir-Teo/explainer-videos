"""Precompute every number in Part 66 of *Economics, Built* ("Geoeconomics and Industrial Policy").

    python -m videos.economics.econ66.compute            # everything missing (under a minute)
    python -m videos.economics.econ66.compute --force bloc

Results are cached in ``.cache/econ66/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``tradewar`` module
(the reciprocal formula, tariffs with revenue in the quantitative trade model on CEPII's 2019 flows, the two-bloc
tariff war, the repeated game, dependence as power, resilience, learning by doing, subsidy races).  Data: FRED
(customs duties and imports of goods by quarter, the monthly trade balance, core goods prices, import prices, core
PCE prices), CEPII's Gravity database (2019).

Items:
    formula     the 2 April 2025 rate for Vietnam, with the pass-through the formula assumed and with 0.945
    effective   the effective US tariff rate by quarter, 2015-2026 (customs duties over imports of goods)
    prices      core goods prices and import prices excluding food and fuel, monthly, 2023-2026
    world       a world of twelve economies and the rest, from 2019 flows, with deficits purged
    scenarios   a uniform 15% US tariff, without and with retaliation, for three trade elasticities
    bloc        the United States against the rest as one bloc: best responses, the optimal tariff, the Nash war
    repeated    a ten-round tariff game against three kinds of partner
    triangle    bilateral imbalances among three countries whose trade is balanced overall
    power       the welfare cost of losing a supplier, by its share of spending (ACR)
    resilience  how much to buy from a supplier that can be cut off, privately and socially
    infant      learning by doing behind a temporary tariff: three learning rates, Mill's and Bastable's tests
    subsidies   Brander and Spencer's subsidy race in a third market
    fomc        Called it?: the FOMC's June 2025 projection of 2025 core PCE inflation against the outcome
    film        the intermission's data film: the US trade balance in goods and services, monthly, 1992-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import tradewar as TW

CACHE = Cache("econ66")
load = CACHE.load
TRUTH = {"world": "the model's trade elasticity and the tariffs are assumed (agora.tradewar.tariff_hat)",
         "infant": "the learning rates are assumed (agora.tradewar.infant_industry)"}
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1992.0, 2026.75)
VIETNAM = {"imports": 136.6, "exports": 13.1, "published": 0.46, "later": 0.20}     # 2024, billions; USTR
PUBLISHED = {"China": 0.34, "European Union": 0.20, "Vietnam": 0.46, "Japan": 0.24, "United Kingdom": 0.10}
TOP = 12


def film_time(year: float) -> float:
    a, b = FILM_YEARS
    return 2.0 + (year - a) / (b - a) * (FILM_SECONDS - 4.0)


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, np.str_):
        return str(x)
    return x


def compute_formula() -> dict:
    v = VIETNAM
    raw = (v["imports"] - v["exports"]) / v["imports"]
    return _jsonable({**v, "raw": raw, "rate": TW.reciprocal_rate(v["imports"], v["exports"]),
                      "rate_945": TW.reciprocal_rate(v["imports"], v["exports"], phi=0.945),
                      "published_rates": PUBLISHED})


def compute_effective() -> dict:
    c = data.fred("B235RC1Q027SBEA")
    m = data.fred("A255RC1Q027SBEA")
    dm = dict(zip(m["date"], m["value"]))
    rows = [(d, v / dm[d]) for d, v in zip(c["date"], c["value"]) if d in dm and d >= "2015-01-01"]
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 + 1 / 8 for d, _ in rows]
    rate = [r for _, r in rows]
    k = int(np.argmax(rate))
    q = dict(rows)
    return _jsonable({"t": t, "rate": rate, "dates": [d for d, _ in rows], "peak": rate[k], "peak_date": rows[k][0],
                      "q2017": q["2017-01-01"], "q2019": q["2019-10-01"], "q2025_1": q["2025-01-01"],
                      "last": rate[-1], "last_date": rows[-1][0],
                      "retrieved": data.FRED_RETRIEVED.get("B235RC1Q027SBEA")})


def compute_prices() -> dict:
    g = data.fred("CUSR0000SACL1E")
    i = data.fred("IREXFDFLS")
    dg, di = dict(zip(g["date"], g["value"])), dict(zip(i["date"], i["value"]))
    dates = [d for d in g["date"] if d >= "2023-01-01" and d in di]
    base = "2025-01-01"
    goods = [100 * dg[d] / dg[base] for d in dates]
    imp = [100 * di[d] / di[base] for d in dates]
    t = [int(d[:4]) + (int(d[5:7]) - 0.5) / 12 for d in dates]
    out = {"t": t, "dates": dates, "goods": goods, "imports": imp,
           "goods_2024": dg["2024-12-01"] / dg["2023-12-01"] - 1,
           "goods_2025": dg["2025-12-01"] / dg["2024-12-01"] - 1,
           "imports_2025": di["2025-12-01"] / di["2024-12-01"] - 1,
           "goods_to_sep": dg["2025-09-01"] / dg["2025-01-01"] - 1,
           "imports_to_sep": di["2025-09-01"] / di["2025-01-01"] - 1}
    return _jsonable(out)


def _world():
    G = data.gravity()
    G = {k: (np.array(v, float) if k not in ("iso3_o", "iso3_d") else np.array(v)) for k, v in G.items()}
    gdp = {}
    for c, v in zip(G["iso3_o"], G["gdp_o"]):
        if np.isfinite(v):
            gdp[str(c)] = v
    top = sorted(gdp, key=gdp.get, reverse=True)[:TOP]
    idx = {c: i for i, c in enumerate(top)}
    N = len(top) + 1
    X = np.zeros((N, N))
    exports = np.zeros(N)
    for o, d, x in zip(G["iso3_o"], G["iso3_d"], G["tradeflow_baci"]):
        o, d = str(o), str(d)
        if not np.isfinite(x) or o not in gdp or d not in gdp:
            continue
        i, n = idx.get(o, N - 1), idx.get(d, N - 1)
        if i == n:
            continue
        X[n, i] += x
        exports[i] += x
    gdp_r = np.array([gdp[c] for c in top] + [sum(v for c, v in gdp.items() if c not in idx)])
    for n in range(N):
        X[n, n] = gdp_r[n] - exports[n]
    Xb = TW.purge_deficits(X, 4.0)
    return top + ["RoW"], X, Xb, idx["USA"]


def compute_world() -> dict:
    regions, X, Xb, us = _world()
    E = X.sum(axis=1)
    return _jsonable({"regions": regions, "us": us, "us_import_share": 1 - X[us, us] / E[us],
                      "us_gdp_share": E[us] / E.sum(), "deficit_share": (E[us] - X[:, us].sum()) / E[us],
                      "Xb": Xb})


def compute_scenarios() -> dict:
    W = load("world")
    return _jsonable(TW.tariff_scenarios(np.array(W["Xb"]), W["us"], 0.15))


def compute_bloc() -> dict:
    W = load("world")
    B = TW.two_bloc(np.array(W["Xb"]), W["us"], 4.0, grid=np.round(np.linspace(0, 0.6, 25), 4))
    return _jsonable(B)


def compute_repeated() -> dict:
    B = load("bloc")
    st = TW.stage_payoffs(B, 0.25)
    R = TW.repeated(st)
    return _jsonable({"stage": st, **R})


def compute_triangle() -> dict:
    # each country sells 100 to the next: A -> B -> C -> A; and a little back
    flows = {("A", "B"): 100.0, ("B", "C"): 100.0, ("C", "A"): 100.0, ("B", "A"): 40.0, ("C", "B"): 40.0,
             ("A", "C"): 40.0}
    names = ("A", "B", "C")
    total = {c: sum(v for (o, d), v in flows.items() if o == c) - sum(v for (o, d), v in flows.items() if d == c)
             for c in names}
    bilateral = {f"{a}{b}": flows.get((a, b), 0) - flows.get((b, a), 0) for a in names for b in names if a < b}
    return {"flows": {f"{o}{d}": v for (o, d), v in flows.items()}, "total": total, "bilateral": bilateral}


def compute_power() -> dict:
    s = np.linspace(0, 0.5, 51)
    out = {"share": s, "loss4": TW.cutoff_loss(s, 4.0), "loss2": TW.cutoff_loss(s, 2.0),
           "loss8": TW.cutoff_loss(s, 8.0)}
    out["examples"] = {f"{x:.2f}": float(TW.cutoff_loss(x, 4.0)) for x in (0.02, 0.05, 0.10, 0.20, 0.40)}
    return _jsonable(out)


def compute_resilience() -> dict:
    return _jsonable(TW.resilience())


def compute_infant() -> dict:
    rows = {f"{b:.2f}": TW.infant_industry(b, r=0.10) for b in (0.15, 0.20, 0.30)}
    return _jsonable({"cases": rows, "r": 0.10})


def compute_subsidies() -> dict:
    return _jsonable(TW.brander_spencer())


def compute_fomc() -> dict:
    f = data.fred("PCEPILFE")
    d = dict(zip(f["date"], f["value"]))

    def q4(y):
        return float(np.mean([d[f"{y}-{m:02d}-01"] for m in (10, 11, 12)]))
    out = q4(2025) / q4(2024) - 1
    assert 0.026 < out < 0.030, out                         # calls.fomc_2025: below the 3.1% projected
    return {"projected_june": 0.031, "projected_march": 0.028, "outcome": out,
            "retrieved": data.FRED_RETRIEVED.get("PCEPILFE")}


def compute_film() -> dict:
    b = data.fred("BOPGSTB")
    yrs = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in b["date"]]
    v = [x / 1000 for x in b["value"]]
    d = dict(zip(b["date"], v))
    k = int(np.argmin(v))
    return _jsonable({"years": yrs, "balance": v, "t": [film_time(y) for y in yrs], "worst": v[k],
                      "worst_date": b["date"][k], "mar2025": d["2025-03-01"], "apr2025": d["2025-04-01"],
                      "first": b["date"][0], "last": b["date"][-1], "last_value": v[-1],
                      "y2006": float(np.mean([d[f"2006-{m:02d}-01"] for m in range(1, 13)]))})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    yrs = np.array(f["years"])
    vals = np.array(f["balance"])
    # one note a quarter: the quarter's average balance
    qt, qv = [], []
    for k in range(0, len(vals) - 2, 3):
        qt.append(film_time(float(yrs[k])))
        qv.append(float(vals[k:k + 3].mean()))
    mel = SC.data_melody(np.array(qv), MELODY_SECONDS, times=qt, act=12, log=False, low=40, high=80)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": qt[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.15, "hz": SC.hz(nn), "name": f"{x:.0f}bn"}
                       for tt, nn, x in zip(qt, mel["notes"], qv)],
                meta={"label": "the US trade balance in goods and services, quarterly averages of monthly figures, "
                               "1992-2026 (Census and BEA via FRED), as a tune that falls with the deficit (computed)",
                      "kind": "synthesized"})
    ClipStore("econ66").save("intermission.melody", clip)
    return {"times": qt, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "formula": compute_formula,
    "effective": compute_effective,
    "prices": compute_prices,
    "world": compute_world,
    "scenarios": compute_scenarios,
    "bloc": compute_bloc,
    "repeated": compute_repeated,
    "triangle": compute_triangle,
    "power": compute_power,
    "resilience": compute_resilience,
    "infant": compute_infant,
    "subsidies": compute_subsidies,
    "fomc": compute_fomc,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
