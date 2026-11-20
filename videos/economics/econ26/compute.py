"""Precompute every number in Part 26 of *Economics, Built* ("Banks and Runs").

    python -m videos.economics.econ26.compute            # everything missing (seconds)
    python -m videos.economics.econ26.compute --force dd

Results are cached in ``.cache/econ26/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's bank suspensions of 1921-1941, the federal funds rate, the FDIC's national deposit
rates, Treasury yields, deposits at small and large banks, banks' equity ratio, money market funds' assets; the
transcribed facts of Silicon Valley Bank's failure and the 2022 stress scenario).  Models: Agora's banks
(``agora.bank``) with the Island's Part 26 truths.

Items:
    dd           Diamond and Dybvig's contract, the stayers' payment against the share withdrawing, the threshold
    run          a run with sequential service: who is paid
    sheet        the Island bank's balance sheet before and after rates rise 3 points
    llr          a sound but illiquid bank: a fire sale against Bagehot's lender
    merton       deposit insurance as a put: its value against the bank's risk
    gg           the global game: the share withdrawing and failure against the bank's strength
    suspensions  US bank suspensions, 1921-1941, and month by month 1921-1933
    svb          Silicon Valley Bank's numbers; weekly deposits at small and large banks, 2022-2024
    rates        the 2022 stress scenario against the federal funds rate and the 10-year yield
    betas        deposit betas: savings and 12-month CD rates against the federal funds rate, 2022-2023
    capital      banks' equity to assets, 1988-2020
    mmf          money market funds' assets
    repo         a dealer funded by repo when haircuts rise
    monitor      Diamond's delegated monitor: the bank's chance of failing against the number of its loans
    crisis       the American output loss of 2007-09: peak to trough, and against the 1990-2007 trend
    film         the intermission's data film: deposits at small and large banks, week by week, 2022-2024
    melody       its data melody: small banks' deposits
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import bank as bk
from explainer.economics.data import tables

CACHE = Cache("econ26")
load = CACHE.load
TRUTH = island.truths(26)


def _t(d: str) -> float:
    y, m, dd = int(d[:4]), int(d[5:7]), int(d[8:10])
    return y + (m - 1) / 12 + (dd - 1) / 365


def compute_dd() -> dict:
    T = TRUTH["dd"]
    d = bk.dd_contract(R=T["R"], gamma=T["gamma"], t=T["t"])
    f = np.linspace(0, 0.85, 171)
    stay = bk.dd_stayers(f, d["c1"], T["R"])
    p = TRUTH["playit"]
    at_half = float(bk.dd_stayers([p["share_saying"]], d["c1"], T["R"])[0])
    return {**d, "f": f.tolist(), "stay": stay.tolist(), "at_half": at_half, "share_saying": p["share_saying"]}


def compute_run() -> dict:
    T = TRUTH["dd"]
    d = bk.dd_contract(R=T["R"], gamma=T["gamma"], t=T["t"])
    r = bk.sequential_service(n=T["n"], c1=d["c1"], seed=T["seed"])
    s = bk.suspension(T["t"], d["c1"], T["R"])
    return {**r, **s, "c1": d["c1"]}


def compute_sheet() -> dict:
    S = TRUTH["sheet"]
    assets = {"reserves": S["reserves"], "loans": S["loans"], "bonds": S["bonds"]}
    b = bk.bond_loss(S["coupon"], S["years"], S["y0"], S["y1"])
    loss = -b["change"] * S["bonds"]
    cap = bk.capital_ratio(assets, S["equity"], S["weights"], loss=loss)
    return {**S, **b, "loss": float(loss), **cap}


def compute_llr() -> dict:
    return {**TRUTH["llr"], **bk.lender_of_last_resort(**TRUTH["llr"])}


def compute_merton() -> dict:
    M = TRUTH["merton"]
    sig = np.linspace(0.02, 0.3, 57)
    rows = [bk.merton_put(M["V"], M["D"], float(s)) for s in sig]
    pts = [bk.merton_put(M["V"], M["D"], float(s)) for s in M["sigmas"]]
    return {**M, "sigma": sig.tolist(), "put": [r["put"] for r in rows], "equity": [r["equity"] for r in rows],
            "points": pts}


def compute_gg() -> dict:
    G = TRUTH["gg"]
    base = bk.global_game(c=G["c"], R=G["R"], sigma=G["sigma"], n=G["n"], seed=G["seed"])
    gen = bk.global_game(c=G["c_generous"], R=G["R"], sigma=G["sigma"], n=G["n"], seed=G["seed"])
    return {"base": base, "generous": gen, **G}


def compute_suspensions() -> dict:
    a = data.fred("X14AICBS")
    m = data.fred("M09036USM155NNBR")
    yrs = [int(d[:4]) for d in a["date"]]
    vals = list(a["value"])
    s30_33 = int(sum(v for y, v in zip(yrs, vals) if 1930 <= y <= 1933))
    v33 = int(vals[yrs.index(1933)])
    v34 = int(vals[yrs.index(1934)])
    return {"years": yrs, "annual": vals, "sum_30_33": s30_33, "y1933": v33, "y1934": v34,
            "m_t": [_t(d) for d in m["date"]], "monthly": list(m["value"])}


def compute_svb() -> dict:
    S = tables.SVB_2023.data
    out = {}
    for key, name in (("DPSSCBW027SBOG", "small"), ("DPSLCBW027SBOG", "large")):
        d = data.fred(key)
        pts = [(x, v) for x, v in zip(d["date"], d["value"]) if "2022-01-01" <= x <= "2024-12-31"]
        out[name] = {"t": [_t(x) for x, _ in pts], "v": [v for _, v in pts], "dates": [x for x, _ in pts]}
    sm = out["small"]
    k8 = sm["dates"].index("2023-03-08")
    k15 = sm["dates"].index("2023-03-15")
    lg = out["large"]
    return {**S, **out, "small_drop": float(sm["v"][k8] - sm["v"][k15]), "large_change": float(lg["v"][k15] -
                                                                                              lg["v"][k8])}


def compute_rates() -> dict:
    st = tables.STRESS_2022.data
    out = {}
    for key, name in (("FEDFUNDS", "ff"), ("GS10", "ten")):
        d = data.fred(key)
        pts = [(x, v) for x, v in zip(d["date"], d["value"]) if "2021-01-01" <= x <= "2024-12-31"]
        out[name] = {"t": [_t(x) for x, _ in pts], "v": [v for _, v in pts], "dates": [x for x, _ in pts]}
    ff = dict(zip(out["ff"]["dates"], out["ff"]["v"]))
    ten = dict(zip(out["ten"]["dates"], out["ten"]["v"]))
    return {**out, "scenario_t": [p[0] for p in st["path"]], "scenario_v": [p[1] for p in st["path"]],
            "ff_2022_01": ff["2022-01-01"], "ff_2022_12": ff["2022-12-01"], "ff_2023_08": ff["2023-08-01"],
            "ten_2022_01": ten["2022-01-01"], "ten_2022_10": ten["2022-10-01"], "ten_2023_10": ten["2023-10-01"],
            "trough": st["ten_year_trough"], "unemployment_peak": st["unemployment_peak"]}


def compute_betas() -> dict:
    ff = dict(zip(data.fred("FEDFUNDS")["date"], data.fred("FEDFUNDS")["value"]))
    sv = dict(zip(data.fred("SNDR")["date"], data.fred("SNDR")["value"]))
    cd = dict(zip(data.fred("NDR12MCD")["date"], data.fred("NDR12MCD")["value"]))
    a, b = "2022-02-01", "2023-12-01"
    beta_s = bk.deposit_beta(ff[a], ff[b], sv[a], sv[b])
    beta_c = bk.deposit_beta(ff[a], ff[b], cd[a], cd[b])
    dates = sorted(set(sv) & set(ff) & set(cd))
    return {"from": a, "to": b, "ff_from": ff[a], "ff_to": ff[b], "sav_from": sv[a], "sav_to": sv[b],
            "cd_from": cd[a], "cd_to": cd[b], "beta_savings": float(beta_s), "beta_cd": float(beta_c),
            "t": [_t(x) for x in dates], "ff": [ff[x] for x in dates], "sav": [sv[x] for x in dates],
            "cd": [cd[x] for x in dates]}


def compute_capital() -> dict:
    d = data.fred("EQTA")
    v = list(d["value"])
    return {"t": [_t(x) for x in d["date"]], "v": v, "first": v[0], "last": v[-1], "first_date": d["date"][0],
            "last_date": d["date"][-1]}


def compute_mmf() -> dict:
    d = data.fred("MMMFFAQ027S")
    pts = [(x, v / 1e6) for x, v in zip(d["date"], d["value"]) if x >= "1980-01-01"]
    v = {x: y for x, y in pts}
    return {"t": [_t(x) for x, _ in pts], "v": [y for _, y in pts], "q2_2008": v.get("2008-04-01"),
            "q4_2008": v.get("2008-10-01"), "last": pts[-1][1], "last_date": pts[-1][0]}


def compute_repo() -> dict:
    R = TRUTH["repo"]
    hs = np.linspace(0.01, 0.5, 50)
    return {**R, **bk.repo_leverage(R["assets"], R["equity"], R["haircut_from"], R["haircut_to"]),
            "h": hs.tolist(), "lev": (1 / hs).tolist()}


def compute_monitor() -> dict:
    M = TRUTH["monitor"]
    ns = np.unique(np.round(np.logspace(0, 3, 61)).astype(int))
    fail = [bk.diversified_failure(int(n), M["p"], M["R"], M["D"]) for n in ns]
    pts = {str(n): bk.diversified_failure(n, M["p"], M["R"], M["D"]) for n in M["ns"]}
    return {**M, "n": ns.tolist(), "fail": fail, "points": pts,
            "direct_cost": M["depositors"] * M["cost"], "bank_cost": M["cost"]}


def compute_crisis() -> dict:
    d = data.fred("GDPC1")
    dt, v = d["date"], np.array(d["value"], float)
    i, j = dt.index("2007-10-01"), dt.index("2009-04-01")
    k = [n for n, x in enumerate(dt) if "1990-01-01" <= x <= "2007-10-01"]
    tt = np.arange(len(v))
    b = np.polyfit(tt[k], np.log(v[k]), 1)
    show = [n for n, x in enumerate(dt) if "1990-01-01" <= x <= "2019-10-01"]
    trend = np.exp(np.polyval(b, tt[show]))
    m = dt.index("2019-10-01")
    return {"t": [_t(dt[n]) for n in show], "gdp": v[show].tolist(), "trend": trend.tolist(),
            "peak": float(v[i]), "trough": float(v[j]), "fall": float(100 * (1 - v[j] / v[i])),
            "trend_growth": float(400 * b[0]),
            "gap_2019": float(100 * (1 - v[m] / np.exp(np.polyval(b, tt[m]))))}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 2022.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    s = compute_svb()
    sm, lg = s["small"], s["large"]
    n = min(len(sm["t"]), len(lg["t"]))
    t = np.array(sm["t"][:n])
    return {"t": t.tolist(), "small": sm["v"][:n], "large": lg["v"][:n], "times": [film_time(x) for x in t],
            "first": float(t[0]), "last": float(t[-1]), "small_drop": s["small_drop"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["small"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=6, log=True, low=45, high=84)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.0f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "deposits at small US banks, week by week, 2022-2024 (Federal Reserve via FRED), as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ26").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "dd": compute_dd,
    "run": compute_run,
    "sheet": compute_sheet,
    "llr": compute_llr,
    "merton": compute_merton,
    "gg": compute_gg,
    "suspensions": compute_suspensions,
    "svb": compute_svb,
    "rates": compute_rates,
    "betas": compute_betas,
    "capital": compute_capital,
    "mmf": compute_mmf,
    "repo": compute_repo,
    "monitor": compute_monitor,
    "crisis": compute_crisis,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
