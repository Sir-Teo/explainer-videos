"""Precompute every number in Part 33 of *Economics, Built* ("Crises").

    python -m videos.economics.econ33.compute            # everything missing (about a minute)
    python -m videos.economics.econ33.compute --force panel

Results are cached in ``.cache/econ33/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Jorda-Schularick-Taylor Macrohistory Database, release 6; FRED's house prices,
mortgage delinquencies, the TED and Baa spreads, the Federal Reserve's balance sheet and swap lines, money market
funds, the baht, won and peso, and the NBER's bank suspensions).  Models: Agora's credit (``agora.credit``) with the
Island's Part 33 truths.

Items:
    booms        Play it: the eight largest postwar credit booms, unlabelled; each one's path and outcome, and the
                 predictor's chance fitted only on earlier years
    minsky       hedge, speculative and Ponzi borrowers through the Island's boom
    fisher       the United States, 1929-1933: prices, nominal GDP, loans and loans to GDP; bank suspensions
    bgg          the debt contract: the premium and default rate against leverage; the accelerator
    km           Kiyotaki and Moore: the land, land price and output paths, with and without the price feedback
    leverage     Geanakoplos's leverage cycle: prices and margins with and without leverage, and after bad news
    gfc          2007-2009 in order: house prices, delinquencies, the TED and Baa spreads, the Fed's balance sheet
    counties     the Island's counties: spending, housing wealth and leverage
    panel        the crisis predictor on 18 countries since 1870, in and out of sample; odds by credit boom
    recessions   output after normal and financial recessions, since 1870 and since 1948
    ccyb         Basel III's credit-gap guide to the countercyclical buffer, for Spain and the United States
    fight        the swap lines of 2008 and 2020, and the Fed's balance sheet
    em           the baht, the won and the peso in their crises
    frontier     money market funds' assets
    film         the intermission's data film: bank loans to GDP across the 18 countries since 1870, and crises
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import credit

CACHE = Cache("econ33")
load = CACHE.load
TRUTH = island.truths(33)
FILM_SECONDS = 50.0
NAMES = {"AUS": "Australia", "BEL": "Belgium", "CAN": "Canada", "CHE": "Switzerland", "DEU": "Germany",
         "DNK": "Denmark", "ESP": "Spain", "FIN": "Finland", "FRA": "France", "GBR": "the United Kingdom",
         "IRL": "Ireland", "ITA": "Italy", "JPN": "Japan", "NLD": "the Netherlands", "NOR": "Norway",
         "PRT": "Portugal", "SWE": "Sweden", "USA": "the United States"}


def _series(key: str, first: str = "0000", last: str = "9999") -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v) and first <= x <= last}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365


def _monthly(key: str, first: str, last: str) -> dict:
    """A daily or weekly series averaged by month: {"t": [...], "v": [...]}."""
    out: dict = {}
    for d, v in _series(key, first, last).items():
        out.setdefault(d[:7], []).append(v)
    ks = sorted(out)
    return {"t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks], "v": [float(np.mean(out[k])) for k in ks]}


def _panel():
    return credit.jst_panel(data.jst())


def compute_booms() -> dict:
    P = _panel()
    D = data.jst()
    iso, yr = np.array(D["iso"]), np.array(D["year"], int)
    cg = 100 * np.array(D["tloans"], float) / np.array(D["gdp"], float)
    rh = np.array(D["hpnom"], float) / np.array(D["cpi"], float)
    out = []
    for k, b in enumerate(credit.big_booms(P)):
        t0 = b["year"]
        m = (iso == b["iso"]) & (yr >= t0 - 10) & (yr <= t0 + 3)
        ys = yr[m]
        base = rh[m][list(ys).index(t0 - 5)] if (t0 - 5) in ys else np.nan
        out.append({**b, "letter": "ABCDEFGH"[k], "name": NAMES[b["iso"]], "years": ys.tolist(),
                    "cg": cg[m].tolist(), "house": (100 * rh[m] / base).tolist(),
                    "house5": float(100 * (rh[m][list(ys).index(t0)] / base - 1)),
                    "p": credit.predict_before(P, b["iso"], t0)})
    crises = sum(b["crisis"] for b in out)
    ps = np.array([b["p"] for b in out])
    ys_ = np.array([b["crisis"] for b in out], float)
    return {"booms": out, "crises": int(crises), "auc8": credit.auc(ps, ys_),
            "right_at_half": int(np.sum((ps >= 0.5) == (ys_ == 1)))}


def compute_minsky() -> dict:
    return credit.minsky_boom(**TRUTH["minsky"])


def compute_fisher() -> dict:
    D = data.jst()
    iso, yr = np.array(D["iso"]), np.array(D["year"], int)
    m = (iso == "USA") & (yr >= 1926) & (yr <= 1936)
    cpi, gdp, loans = (np.array(D[k], float)[m] for k in ("cpi", "gdp", "tloans"))
    ys = yr[m].tolist()
    i29, i32, i33 = ys.index(1929), ys.index(1932), ys.index(1933)
    ratio = 100 * loans / gdp
    s = _series("M09036USM155NNBR")
    a = {int(k[:4]): v for k, v in _series("X14AICBS", "1920-01-01", "1934-12-31").items()}
    illus = credit.debt_deflation(1.0, [0.1, 0.1, 0.1, 0.05], -0.05, repay=0.05)
    return {"years": ys, "cpi": cpi.tolist(), "gdp": gdp.tolist(), "loans": loans.tolist(), "ratio": ratio.tolist(),
            "cpi_fall": float(100 * (1 - cpi[i33] / cpi[i29])), "gdp_fall": float(100 * (1 - gdp[i33] / gdp[i29])),
            "loans_fall": float(100 * (1 - loans[i33] / loans[i29])), "ratio29": float(ratio[i29]),
            "ratio32": float(ratio[i32]), "ratio33": float(ratio[i33]),
            "susp_t": [_t(k) for k in sorted(s)], "susp": [s[k] for k in sorted(s)],
            "susp_annual": {str(k): v for k, v in a.items()}, "susp_30_33": float(sum(a[y] for y in range(1930, 1934))),
            "illus": illus}


def compute_bgg() -> dict:
    B = TRUTH["bgg"]
    C = credit.csv_contract(B["sigma"], B["mu"])
    base = credit.accelerator(1.0, C, K_star=B["K_star"], theta=B["theta"])
    low = credit.accelerator(1.0 - B["N_fall"], C, K_star=B["K_star"], theta=B["theta"])
    s_star = credit.premium_at(B["K_star"], C)
    Ks = np.linspace(1.4, 2.6, 61)
    demand = s_star * (Ks / B["K_star"]) ** -B["theta"]
    supply = [credit.premium_at(K / 1.0, C) for K in Ks]
    supply_low = [credit.premium_at(K / (1 - B["N_fall"]), C) for K in Ks]
    return {"leverage": C["leverage"], "premium": C["premium"], "default": C["default"],
            "at2": {"premium": s_star, "default": float(np.interp(2.0, C["leverage"], C["default"]))},
            "K": Ks.tolist(), "demand": demand.tolist(), "supply": supply, "supply_low": supply_low,
            "base": base, "low": low, "K_fall": float(100 * (low["K"] / base["K"] - 1)), **B}


def compute_km() -> dict:
    K = TRUTH["km"]
    kw = {k: K[k] for k in ("R", "eta", "a", "c")}
    A = credit.km_amplification(K["shock"], **kw)
    big = None
    for s in (0.015, 0.02, 0.03):
        try:
            credit.km_path(s, **kw)
        except ValueError:
            big = s
            break
    st = A["static_path"]
    dy = A["dynamic_path"]
    p = dy["params"]
    return {"t": dy["t"][: K["T"] + 1], "k": dy["k"][: K["T"] + 1], "q": dy["q"][: K["T"] + 1],
            "Y": dy["Y"][: K["T"] + 1], "k_static": st["k"][: K["T"] + 1], "Y_static": st["Y"][: K["T"] + 1],
            "static": A["static"], "dynamic": A["dynamic"], "q0": A["q0"], "k0": dy["k0"], "Y0": dy["Y"][0],
            "direct": float(100 * K["shock"] * p["a"] / (2 * (p["a"] + p["c"]))), "q_star": p["q"],
            "leverage": float(p["q"] / p["u"]), "no_equilibrium_at": big, **K}


def compute_leverage() -> dict:
    d = TRUTH["leverage"]["d"]
    return {"with": credit.leverage_static(d, True), "without": credit.leverage_static(d, False),
            "cycle": credit.leverage_cycle(d), "d": d}


def compute_gfc() -> dict:
    cs = _series("CSUSHPINSA", "1998-01-01", "2014-12-31")
    dq = _series("DRSFRMACBS", "2000-01-01", "2014-12-31")
    ted = _monthly("TEDRATE", "2006-01-01", "2010-12-31")
    baa = _monthly("BAA10Y", "2006-01-01", "2010-12-31")
    wal = _series("WALCL", "2007-01-01", "2010-12-31")
    k_cs = max(cs, key=cs.get)
    k_lo = min((k for k in cs if k > k_cs), key=cs.get)
    tedd = _series("TEDRATE", "2007-01-01", "2009-12-31")
    k_ted = max(tedd, key=tedd.get)
    baad = _series("BAA10Y", "2007-01-01", "2009-12-31")
    k_baa = max(baad, key=baad.get)
    k_dq = max(dq, key=dq.get)
    wk = sorted(wal)
    w_before = wal[max(k for k in wk if k <= "2008-09-10")]
    w_after = wal[min(k for k in wk if k >= "2008-12-17")]
    return {"cs_t": [_t(k) for k in sorted(cs)], "cs": [cs[k] for k in sorted(cs)], "cs_peak": cs[k_cs],
            "cs_peak_date": k_cs, "cs_trough": cs[k_lo], "cs_trough_date": k_lo,
            "cs_fall": float(100 * (1 - cs[k_lo] / cs[k_cs])),
            "dq_t": [_t(k) for k in sorted(dq)], "dq": [dq[k] for k in sorted(dq)], "dq_peak": dq[k_dq],
            "dq_peak_date": k_dq, "dq_2005": dq["2005-01-01"],
            "ted_t": ted["t"], "ted": ted["v"], "ted_peak": tedd[k_ted], "ted_peak_date": k_ted,
            "ted_2006": float(np.mean([v for k, v in _series("TEDRATE", "2006-01-01", "2006-12-31").items()])),
            "baa_t": baa["t"], "baa": baa["v"], "baa_peak": baad[k_baa], "baa_peak_date": k_baa,
            "wal_t": [_t(k) for k in wk], "wal": [wal[k] / 1e6 for k in wk], "wal_before": w_before / 1e6,
            "wal_after": w_after / 1e6}


def compute_counties() -> dict:
    return credit.counties(**TRUTH["counties"])


def compute_panel() -> dict:
    P = _panel()
    rl = credit.crisis_predictor(P, "real_loans")
    cg = credit.crisis_predictor(P, "credit_gdp")
    odds = credit.boom_odds(P)
    yr = P["year"]
    m = ~P["war"]
    return {"real_loans": {k: v for k, v in rl.items() if k != "b"}, "credit_gdp": {k: v for k, v in cg.items()
                                                                                       if k != "b"},
            "odds": odds, "crises_all": int(P["crisis"].sum()), "countries": len(set(P["iso"])),
            "first": int(yr.min()), "last": int(yr.max()), "years_peace": int(m.sum()),
            "base_rate": float(P["crisis"][m].sum() / m.sum())}


def compute_recessions() -> dict:
    P = _panel()
    a = credit.recession_paths(P)
    b = credit.recession_paths(P, first=1948)
    return {"all": a, "post": b, "gap5_all": a["normal"][5] - a["financial"][5],
            "gap5_post": b["normal"][5] - b["financial"][5]}


def compute_ccyb() -> dict:
    D = data.jst()
    iso, yr = np.array(D["iso"]), np.array(D["year"], int)
    out = {}
    for c in ("ESP", "USA"):
        m = (iso == c) & (yr >= 1960) & (yr <= 2015)
        with np.errstate(divide="ignore", invalid="ignore"):
            cg = 100 * np.array(D["tloans"], float)[m] / np.array(D["gdp"], float)[m]
        g = credit.one_sided_gap(cg)
        b = credit.ccyb_guide(g)
        y = yr[m]
        full = [int(a) for a, v in zip(y, b) if v >= 2.5 and a >= 1990]
        out[c] = {"years": y.tolist(), "ratio": cg.tolist(), "gap": g.tolist(), "buffer": b.tolist(),
                  "first_full": full[0] if full else None, "gap2007": float(g[list(y).index(2007)]),
                  "buffer2007": float(b[list(y).index(2007)])}
    return out


def compute_fight() -> dict:
    sw = _series("SWPT", "2007-06-01", "2021-12-31")
    k8 = max((k for k in sw if k < "2010-01-01"), key=sw.get)
    k20 = max((k for k in sw if k >= "2020-01-01"), key=sw.get)
    ks = sorted(sw)
    wal = _series("WALCL", "2020-01-01", "2020-12-31")
    w0 = wal[max(k for k in wal if k <= "2020-03-04")]
    w1 = wal[min(k for k in wal if k >= "2020-06-10")]
    return {"t": [_t(k) for k in ks], "swaps": [sw[k] / 1e3 for k in ks], "peak08": sw[k8] / 1e3, "peak08_date": k8,
            "wal20_before": w0 / 1e6, "wal20_after": w1 / 1e6,
            "peak20": sw[k20] / 1e3, "peak20_date": k20, "scap_banks": 19, "scap_short": 10, "scap_gap": 74.6}


def compute_em() -> dict:
    out = {}
    for key, name, a, b, pre in (("EXTHUS", "baht", "1996-01-01", "1999-12-01", "1997-06-01"),
                                  ("EXKOUS", "won", "1996-01-01", "1999-12-01", "1997-06-01"),
                                  ("EXMXUS", "peso", "1994-01-01", "1995-12-01", "1994-11-01")):
        s = _series(key, a, b)
        ks = sorted(s)
        kp = max(ks, key=s.get)
        out[name] = {"t": [_t(k) for k in ks], "v": [s[k] for k in ks], "before": s[pre], "before_date": pre,
                     "peak": s[kp], "peak_date": kp, "fall": float(100 * (1 - s[pre] / s[kp]))}
    return out


def compute_frontier() -> dict:
    m = _series("MMMFFAQ027S")
    ks = sorted(m)
    k08 = max((k for k in ks if "2007" <= k < "2010"), key=m.get)
    return {"t": [_t(k) for k in ks], "mmf": [m[k] / 1e6 for k in ks], "peak08": m[k08] / 1e6, "peak08_date": k08,
            "last": m[ks[-1]] / 1e6, "last_date": ks[-1]}


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1870.0, last: float = 2020.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    D = data.jst()
    yr = np.array(D["year"], int)
    with np.errstate(divide="ignore", invalid="ignore"):
        cg = np.array(D["tloans"], float) / np.array(D["gdp"], float) * 100
    cr = np.nan_to_num(np.array(D["crisisJST"], float))
    years = list(range(1870, 2021))
    med, n_cr = [], []
    for y in years:
        v = cg[(yr == y) & np.isfinite(cg)]
        med.append(float(np.median(v)) if len(v) >= 5 else float("nan"))
        n_cr.append(int(cr[yr == y].sum()))
    med = np.array(med)
    ok = np.isfinite(med)
    med = np.interp(np.array(years, float), np.array(years, float)[ok], med[ok])
    return {"years": years, "median": med.tolist(), "crises": n_cr, "times": [film_time(y) for y in years],
            "peak_crises": int(max(n_cr)), "peak_year": years[int(np.argmax(n_cr))]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["median"])
    times = f["times"]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40, high=86)
    events = {"film_end": film_time(2020) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.0f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the median of bank loans to GDP across 18 economies, year by year, 1870-2020 "
                               "(Jorda, Schularick and Taylor's Macrohistory Database), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ33").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "booms": compute_booms,
    "minsky": compute_minsky,
    "fisher": compute_fisher,
    "bgg": compute_bgg,
    "km": compute_km,
    "leverage": compute_leverage,
    "gfc": compute_gfc,
    "counties": compute_counties,
    "panel": compute_panel,
    "recessions": compute_recessions,
    "ccyb": compute_ccyb,
    "fight": compute_fight,
    "em": compute_em,
    "frontier": compute_frontier,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
