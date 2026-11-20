"""Precompute every number in Part 34 of *Economics, Built* ("The Open Economy").

    python -m videos.economics.econ34.compute            # everything missing (about half a minute)
    python -m videos.economics.econ34.compute --force uip

Results are cached in ``.cache/econ34/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's exchange rates, interest rates, import prices, the dollar index, the US current
account and net international investment position, the UK's reserves, the VIX; the World Bank's current accounts;
The Economist's Big Mac index; the Jorda-Schularick-Taylor database for real exchange rates since 1870).  Models:
Agora's open economy (``agora.openecon``) with the Island's Part 34 truths.

Items:
    story        Black Wednesday: sterling against the mark in the ERM band, the UK's reserves, and interest rates
    bop          the US current account and net international investment position, as shares of GDP
    playit       the governor's choice: Obstfeld's regions, and where Britain's slack put it
    ppp          real exchange rates since 1870 and their half-lives; the Big Mac index and Balassa-Samuelson
    uip          Fama's regression by currency; the carry trade
    meese        Meese and Rogoff's horse race at one, three and twelve months
    mf           Mundell-Fleming: policy under fixed and floating rates
    dornbusch    overshooting after a 10% rise in money
    crises       a first-generation attack; second-generation regions
    euro         ten-year yields in the euro crisis
    imbalances   current accounts of the United States, China, Germany and Japan since 1980
    dollar       pass-through into US import prices; the renminbi; the VIX
    film         the intermission's data film: the pound in dollars, month by month, since 1971
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import openecon

CACHE = Cache("econ34")
load = CACHE.load
TRUTH = island.truths(34)
FILM_SECONDS = 50.0
ERM = {"central": 2.95, "band": 0.06}


def _series(key: str, first: str = "0000", last: str = "9999") -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v) and first <= x <= last}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365


def _monthly(key: str, first: str = "0000", last: str = "9999", how: str = "mean") -> dict:
    out: dict = {}
    for d, v in sorted(_series(key, first, last).items()):
        out.setdefault(d[:7], []).append(v)
    return {k: (float(np.mean(v)) if how == "mean" else float(v[-1])) for k, v in out.items()}


def _m(key: str) -> dict:
    """A monthly FRED series keyed "YYYY-MM"."""
    return {k[:7]: v for k, v in _series(key).items()}


def _gdp_q() -> dict:
    return {k: v for k, v in _series("GDP").items()}


def log_usd_per(c: str, end_of_month: bool = False) -> dict:
    """Log dollars per unit of currency ``c``, monthly (averages, or end of month from daily data)."""
    if end_of_month:
        key, inv = {"GB": ("DEXUSUK", False), "JP": ("DEXJPUS", True), "CA": ("DEXCAUS", True),
                    "CH": ("DEXSZUS", True)}[c]
        s = _monthly(key, how="last")
    elif c == "DE":
        de, eu = _m("EXGEUS"), _m("EXUSEU")
        return {**{k: -np.log(v) for k, v in de.items() if k < "1999-01"},
                **{k: np.log(v / 1.95583) for k, v in eu.items()}}
    else:
        key, inv = {"GB": ("EXUSUK", False), "JP": ("EXJPUS", True), "CA": ("EXCAUS", True),
                    "CH": ("EXSZUS", True), "AU": ("EXUSAL", False), "NZ": ("EXUSNZ", False)}[c]
        s = _m(key)
    return {k: (-np.log(v) if inv else np.log(v)) for k, v in s.items()}


CURRENCIES = ("GB", "DE", "JP", "CH", "CA", "AU", "NZ")
NAMES = {"GB": "pound", "DE": "mark, then euro", "JP": "yen", "CH": "Swiss franc", "CA": "Canadian dollar",
         "AU": "Australian dollar", "NZ": "New Zealand dollar"}


def compute_story() -> dict:
    uk, de = _m("EXUSUK"), _m("EXGEUS")
    ks = sorted(k for k in uk if k in de and "1990-01" <= k <= "1993-12")
    gd = [uk[k] * de[k] for k in ks]
    res = _m("TRESEGGBM052N")
    rk = sorted(k for k in res if "1990-01" <= k <= "1993-12")
    ig, idm = _m("IR3TIB01GBM156N"), _m("IR3TIB01DEM156N")
    ik = sorted(k for k in ig if k in idm and "1990-01" <= k <= "1994-12")
    t = [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks]
    c, b = ERM["central"], ERM["band"]
    return {"t": t, "gbpdem": gd, "central": c, "floor": c * (1 - b), "ceiling": c * (1 + b),
            "aug92": uk["1992-08"] * de["1992-08"], "oct92": uk["1992-10"] * de["1992-10"],
            "fall": float(100 * (1 - (uk["1992-10"] * de["1992-10"]) / (uk["1992-08"] * de["1992-08"]))),
            "res_t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in rk], "reserves": [res[k] / 1000 for k in rk],
            "res_aug": res["1992-08"] / 1000, "res_sep": res["1992-09"] / 1000,
            "i_t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ik], "i_uk": [ig[k] for k in ik],
            "i_de": [idm[k] for k in ik], "i_uk_aug92": ig["1992-08"], "i_uk_feb93": ig["1993-02"],
            "i_de_aug92": idm["1992-08"]}


def compute_bop() -> dict:
    gdp = _gdp_q()
    ca, ni = _series("IEABC"), _series("IIPUSNETIQ")
    ck = sorted(k for k in ca if k in gdp)
    nk = sorted(k for k in ni if k in gdp)
    cas = [100 * 4 * ca[k] / (1000 * gdp[k]) for k in ck]
    nis = [100 * ni[k] / (1000 * gdp[k]) for k in nk]
    return {"ca_t": [_t(k) for k in ck], "ca": cas, "ca_last": cas[-1], "ca_min": float(min(cas)),
            "ca_min_t": _t(ck[int(np.argmin(cas))]), "ni_t": [_t(k) for k in nk], "niip": nis,
            "niip_first": nis[0], "niip_last": nis[-1], "last": ck[-1]}


def compute_playit() -> dict:
    P = TRUTH["playit"]
    R = openecon.obstfeld_regions(P["cost"], P["gamma"], P["delta"])
    us = np.linspace(0, 1.4, 141)
    out = {"no": [openecon.obstfeld_outcome(u, False, P["cost"], P["gamma"], P["delta"]) for u in us],
           "yes": [openecon.obstfeld_outcome(u, True, P["cost"], P["gamma"], P["delta"]) for u in us]}
    return {**R, **P, "u": us.tolist(), **out,
            "island_no": openecon.obstfeld_outcome(P["u_island"], False, P["cost"], P["gamma"], P["delta"]),
            "island_yes": openecon.obstfeld_outcome(P["u_island"], True, P["cost"], P["gamma"], P["delta"]),
            "options": ["raise rates and spend reserves", "ask the anchor to cut its rate", "let the currency float"]}


def compute_ppp() -> dict:
    Rr = openecon.real_rates(data.jst())
    full = openecon.ppp_halflife(Rr, 1870, 2020)
    flt = openecon.ppp_halflife(Rr, 1973, 2020)
    y, q = Rr["GBR"]
    k = (y >= 1870) & (y <= 2020)
    B = data.bigmac()
    last = max(B["date"])
    idx = [i for i, d in enumerate(B["date"]) if d == last]
    pick = {}
    for nm in ("Switzerland", "Norway", "United States", "Euro area", "Britain", "Japan", "China", "India",
               "South Africa", "Brazil"):
        j = [i for i in idx if B["name"][i] == nm]
        if j:
            pick[nm] = {"price": B["dollar_price"][j[0]], "raw": B["USD_raw"][j[0]]}
    ok = [i for i in idx if np.isfinite(B["GDP_bigmac"][i]) and np.isfinite(B["USD_raw"][i])
          and B["iso_a3"][i] != "USA"]
    lg = np.log([B["GDP_bigmac"][i] for i in ok])
    val = [B["USD_raw"][i] for i in ok]
    bs = openecon.balassa_samuelson(lg, val)
    us_price = pick.get("United States", {}).get("price", float("nan"))
    return {"full": {kk: full[kk] for kk in ("rho", "halflife", "n")}, "floating": {kk: flt[kk] for kk in
                                                                                  ("rho", "halflife", "n")},
            "by_country": flt["by_country"], "gb_t": y[k].tolist(), "gb_q": (q[k] - np.nanmean(q[k])).tolist(),
            "bigmac_date": last, "pick": pick, "us_price": us_price, "bs": bs,
            "scatter": [(float(a), float(b)) for a, b in zip(lg, val)],
            "n_bigmac": len(ok)}


def compute_uip() -> dict:
    i_us = _m("IR3TIB01USM156N")
    out = {}
    pooled_x, pooled_y = [], []
    for c in CURRENCIES:
        ls = log_usd_per(c)
        rf = _m(f"IR3TIB01{c}M156N")
        f = openecon.fama(ls, i_us, rf, h=3)
        out[c] = f
    rates = {c: _m(f"IR3TIB01{c}M156N") for c in CURRENCIES}
    ls_all = {c: log_usd_per(c) for c in CURRENCIES}
    C = openecon.carry(ls_all, rates, i_us)
    ks = C["months"]
    del pooled_x, pooled_y
    return {"fama": out, "names": NAMES, "carry": {kk: C[kk] for kk in ("mean", "sd", "sharpe", "skew", "worst")},
            "carry_t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks], "carry_cum": C["cumulative"],
            "negative": sum(1 for v in out.values() if v["beta"] < 0)}


def compute_meese() -> dict:
    i_us = _m("IR3TIB01USM156N")
    series = {c: {k: v for k, v in log_usd_per(c, end_of_month=True).items() if k >= "1980-01"}
              for c in ("GB", "JP", "CA", "CH")}
    rates = {c: _m(f"IR3TIB01{c}M156N") for c in series}
    return {f"h{h}": openecon.horse_race(series, rates, i_us, h) for h in (1, 3, 12)}


def compute_mf() -> dict:
    out = {}
    for reg in ("floating", "fixed"):
        out[reg] = {"fiscal": openecon.mundell_fleming(reg, dg=1.0), "money": openecon.mundell_fleming(reg, dm=1.0)}
    return {**out, "params": openecon.MF}


def compute_dornbusch() -> dict:
    return openecon.dornbusch(**TRUTH["dornbusch"])


def compute_crises() -> dict:
    K = openecon.krugman_attack(**TRUTH["krugman"])
    return {"krugman": K}


def compute_euro() -> dict:
    out = {}
    for c in ("DE", "IT", "ES", "GR"):
        s = _m(f"IRLTLT01{c}M156N")
        ks = sorted(k for k in s if "1995-01" <= k <= "2019-12")
        out[c] = {"t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks], "v": [s[k] for k in ks]}
    return out


def compute_imbalances() -> dict:
    W = data.wdi_ca()
    out = {c: {"year": W[c]["year"], "value": W[c]["value"]} for c in ("USA", "CHN", "DEU", "JPN")}
    chn = dict(zip(W["CHN"]["year"], W["CHN"]["value"]))
    deu = dict(zip(W["DEU"]["year"], W["DEU"]["value"]))
    usa = dict(zip(W["USA"]["year"], W["USA"]["value"]))
    return {**out, "chn2007": chn[2007], "usa2006": usa[2006], "deu2015": deu[2015], "usa_last": usa[2025],
            "chn_last": chn[2025], "deu_last": deu[2025]}


def compute_dollar() -> dict:
    ip, tw = _m("IREXFUELS"), _m("TWEXBMTH")
    ks = sorted(k for k in ip if k in tw and k <= "2019-12")
    lp, le = np.log([ip[k] for k in ks]), np.log([tw[k] for k in ks])
    pt = openecon.passthrough(np.diff(lp), np.diff(le), lags=12)
    cn = _monthly("DEXCHUS", "1994-01-01", "2026-12-31")
    ck = sorted(cn)
    vx = _monthly("VIXCLS", "1990-01-01")
    vk = sorted(vx)
    return {"pt": pt, "pt_first": ks[0], "pt_last": ks[-1],
            "cny_t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ck], "cny": [cn[k] for k in ck],
            "cny_2005": cn["2005-06"], "cny_2008": cn["2008-12"], "cny_last": cn[ck[-1]],
            "vix_t": [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in vk], "vix": [vx[k] for k in vk],
            "vix_peak": float(max(vx.values())), "vix_peak_m": max(vx, key=vx.get)}


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1971.0, last: float = 2026.8) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    s = _m("EXUSUK")
    ks = sorted(s)
    t = [int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks]
    return {"t": t, "v": [s[k] for k in ks], "times": [film_time(x) for x in t], "max": float(max(s.values())),
            "min": float(min(s.values())), "min_m": min(s, key=s.get), "first": s[ks[0]], "last": s[ks[-1]]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=7, log=True, low=40, high=86)
    events = {"film_end": film_time(2026.8) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the pound in dollars, month by month, 1971-2026 (Board of Governors, H.10, via "
                               "FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ34").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "story": compute_story,
    "bop": compute_bop,
    "playit": compute_playit,
    "ppp": compute_ppp,
    "uip": compute_uip,
    "meese": compute_meese,
    "mf": compute_mf,
    "dornbusch": compute_dornbusch,
    "crises": compute_crises,
    "euro": compute_euro,
    "imbalances": compute_imbalances,
    "dollar": compute_dollar,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
