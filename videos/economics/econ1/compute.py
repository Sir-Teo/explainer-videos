"""Precompute every number in Part 1 of *Economics, Built* ("Who Feeds Paris?").

    python -m videos.economics.econ1.compute            # everything missing (about a minute)
    python -m videos.economics.econ1.compute --force pit

Results are cached in ``.cache/econ1/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data come from the
Data Room (``explainer.economics.data``, frozen on 18 November 2026, each series with its source) and transcribed
tables (``explainer.economics.data.tables``); models from Agora (``explainer.economics.agora``); the Island's
parameters from ``explainer.economics.island``.  Every random choice is seeded, and where the film shows one
simulated run it is chosen by rule (the median of many by a stated statistic), never by how it looks.

Items:
    pit          the opening pit market: the cards, the competitive prediction, 41 runs of six periods by traders who
                 adjust their margins and by zero-intelligence traders, Smith's coefficient of convergence and the
                 efficiency of each, and the run shown (the median by final-period convergence)
    crusoe       one person's frontier with diminishing returns, the hour-by-hour opportunity cost, and his best day
    ricardo      Crusoe and Friday: hours per fish and per coconut, opportunity costs, the day alone, the competitive
                 equilibrium of trade, the gains, the joint frontier; Ricardo's own four numbers
    pins         Smith's pin factory, from the text
    tin          Hayek's tin: sixty users who see only the price, a mine that closes, the price that clears, who cuts
                 back, the marginal value of tin under equal rationing, and the value each allocation gives up
    fine         the Haifa day-care fine (Gneezy and Rustichini 2000, Table 1): weekly means of the six fined centres
                 and the four others, the period means checked against the paper's Table 2, the difference in
                 differences
    longrun      GDP per head from the Maddison Project: the world since 1820, England since 1252 and others; average
                 growth before and after 1800, doubling times
    film         the intermission's data film: every country's GDP per head and population, year by year, 1820-2022
                 (log-linear between benchmark years), and the world's
    melody       the intermission's data melody: the world's GDP per head as a tune (saved as a clip)
    collapses    1929 and 2008 side by side: industrial production, unemployment, consumer prices and real GDP from
                 each peak
    spf          Called it?: the professional forecasters' median forecast for 2009, made in August 2008, against
                 the outcome
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import crusoe as cr
from explainer.economics.agora import market as mk
from explainer.economics.agora import signals
from explainer.economics.data import tables

CACHE = Cache("econ1")
load = CACHE.load
TRUTH = island.truths(1)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _market() -> mk.Market:
    pit = TRUTH["pit"]
    return mk.Market(values=pit["values"], costs=pit["costs"])


# ---------------------------------------------------------------------------
def compute_pit() -> dict:
    m = _market()
    eq = m.equilibrium()
    viewer = TRUTH["pit"]["viewer"]
    assert eq["q"] == 6 and abs(eq["p_lo"] - 2.20) < 1e-9 and abs(eq["p_hi"] - 2.30) < 1e-9
    seeds = range(41)
    zip_runs = [mk.double_auction(m, "zip", periods=6, seed=s, viewer=viewer) for s in seeds]
    zi_runs = [mk.double_auction(m, "zi", periods=6, seed=s, viewer=viewer) for s in seeds]

    def table(runs):
        alpha = np.array([[p["alpha"] for p in r["periods"]] for r in runs])
        eff = np.array([[p["efficiency"] for p in r["periods"]] for r in runs])
        mean = np.array([[p["mean"] for p in r["periods"]] for r in runs])
        return alpha, eff, mean

    za, ze, zm = table(zip_runs)
    ia, ie, im = table(zi_runs)
    # the run the film shows: the one whose last-period convergence is the median of the 41
    order = np.argsort(za[:, -1])
    shown = int(order[len(order) // 2])
    run = zip_runs[shown]
    periods = []
    for p in run["periods"]:
        periods.append({"prices": [t["price"] for t in p["trades"]], "alpha": p["alpha"],
                        "efficiency": p["efficiency"], "n": p["n"],
                        "viewer_price": next((t["price"] for t in p["trades"] if t["viewer"]), None),
                        "shouts": [[s["price"], 1 if s["side"] == "buy" else 0] for s in p["shouts"]][:40],
                        "trades": [[t["price"], t["value"], t["cost"]] for t in p["trades"]]})
    # learning traders converge: the median alpha falls from the first period to the last
    assert np.median(za[:, -1]) < np.median(za[:, 0]) / 2
    # zero-intelligence traders capture most of the surplus without converging
    assert ie.mean() > 0.85 and np.median(ia[:, -1]) > 2 * np.median(za[:, -1])
    viewer_value = TRUTH["pit"]["values"][viewer]
    return {
        "values": list(m.values), "costs": list(m.costs), "viewer": viewer, "viewer_value": viewer_value,
        "q": eq["q"], "p_lo": eq["p_lo"], "p_hi": eq["p_hi"], "p": eq["p"], "surplus": eq["surplus"],
        "cs": eq["cs_at_mid"], "ps": eq["ps_at_mid"], "steps": m.steps(),
        "shown_seed": shown, "periods": periods,
        "zip_alpha_median": np.median(za, axis=0), "zip_eff_mean": ze.mean(axis=0),
        "zi_alpha_median": np.median(ia, axis=0), "zi_eff_mean": ie.mean(axis=0),
        "zip_mean_median": np.median(zm, axis=0), "zi_mean_median": np.median(im, axis=0),
        "zi_eff_all": float(ie.mean()), "zip_eff_last": float(ze[:, -1].mean()),
        "n_runs": len(seeds),
        "viewer_surplus_at_p": viewer_value - eq["p"],
    }


def compute_crusoe() -> dict:
    c = cr.Crusoe(**TRUTH["crusoe_alone"])
    f = c.frontier(201)
    best = c.best()
    hours = c.hour_by_hour()
    assert abs(best["mrs"] - best["mrt"]) < 1e-5
    assert all(a["cost_per_fish"] < b["cost_per_fish"] for a, b in zip(hours, hours[1:]))
    marks = {str(h): c.marginal(h) for h in (2.0, 6.0, 9.0)}
    return {"params": TRUTH["crusoe_alone"], "h": f["h"], "fish": f["fish"], "coconuts": f["coconuts"],
            "best": best, "hours": hours, "marks": marks,
            "max_fish": float(c.fish(c.hours)), "max_coconuts": float(c.coconuts(0.0))}


def compute_ricardo() -> dict:
    r = cr.ricardo(**TRUTH["two"])
    assert r["regime"] == "both specialize"
    assert r["absolute_advantage_in_both"][0] and all(p["gain_u"] > 0 for p in r["people"])
    assert r["band"][0] < r["price"] < r["band"][1]
    for k in ("fish", "coconuts"):
        assert r["total_trade"][k] >= r["total_alone"][k] - 1e-9
    rc = tables.RICARDO_1817.data
    eng, por = rc["england"], rc["portugal"]
    return {**r, "joint": cr.joint_frontier(r),
            "ricardo": {"england": eng, "portugal": por,
                        "england_oc_wine": eng["wine"] / eng["cloth"], "portugal_oc_wine": por["wine"] / por["cloth"]}}


def compute_pins() -> dict:
    s = tables.SMITH_1776.data
    assert s["men"] * s["per_person"] == s["pins_per_day"] == s["pounds_per_day"] * s["pins_per_pound"]
    assert s["per_person"] / s["alone_at_most"] == s["ratio_low"]
    return dict(s)


def compute_tin() -> dict:
    u = signals.users(60, seed=1945)
    cut = 0.20
    c = signals.compare(u, cut)
    t = signals.tatonnement(u, cut)
    rationed = u["a"] * (1 - cut)
    mv_ration = (rationed / u["a"]) ** (-1 / u["e"])  # what the last unit is worth to each, under equal rationing
    assert abs(c["q1"].sum() - u["supply"] * (1 - cut)) < 1e-6
    assert c["loss_price"] < c["loss_rationing"]
    assert abs(t["path"][-1] - c["price"]) < 1e-6
    # those with good substitutes cut most
    assert np.corrcoef(u["e"], c["cut_share"])[0, 1] > 0.95
    return {"a": u["a"], "e": u["e"], "n": u["n"], "cut": cut, "price": c["price"], "q1": c["q1"],
            "cut_share": c["cut_share"], "mv_ration": mv_ration, "loss_price": c["loss_price"],
            "loss_rationing": c["loss_rationing"], "extra_share": c["loss_rationing"] / c["loss_price"] - 1,
            "path": t["path"], "excess": t["excess"], "numbers_planner": c["numbers_planner"],
            "mv_lo": float(mv_ration.min()), "mv_hi": float(mv_ration.max()),
            "cut_lo": float(c["cut_share"].min()), "cut_hi": float(c["cut_share"].max())}


def compute_fine() -> dict:
    g = tables.GNEEZY_RUSTICHINI_2000.data
    weeks = np.arange(1, g["weeks"] + 1)
    test = np.array([g["centres"][c][1] for c in g["test"]], float)
    ctrl = np.array([g["centres"][c][1] for c in g["control"]], float)
    # the transcription against the paper's Table 2 (period means per centre)
    for c, means in g["table2"].items():
        x = np.array(g["centres"][c][1], float)
        mine = (x[0:4].mean(), x[4:8].mean(), x[4:16].mean(), x[16:20].mean())
        for a, b in zip(mine, means):  # Table 2 truncates (does not round) its means to one decimal
            assert abs(math.floor(a * 10 + 1e-9) / 10 - b) < 1e-9 or abs(a - b) < 1e-9, (c, mine, means)

    def period(x, a, b):
        return float(x[:, a - 1:b].mean())

    before = (period(test, 1, 4), period(ctrl, 1, 4))
    during = (period(test, 5, 16), period(ctrl, 5, 16))
    after = (period(test, 17, 20), period(ctrl, 17, 20))
    did = (during[0] - before[0]) - (during[1] - before[1])
    assert did > 5
    return {"weeks": weeks, "test": test.mean(axis=0), "control": ctrl.mean(axis=0), "test_all": test,
            "control_all": ctrl, "before": before, "during": during, "after": after, "did": did,
            "ratio_test": during[0] / before[0], "ratio_after": after[0] / before[0],
            "children": {c: g["centres"][c][0] for c in g["centres"]}, "fine_nis": g["fine_nis"],
            "fee_nis": g["fee_nis_month"], "nis_per_usd": g["nis_per_usd"],
            "fine_usd": g["fine_nis"] / g["nis_per_usd"]}


def _growth(years, values, a, b) -> float:
    """Average annual growth between years a and b, by the endpoints (log difference over the years)."""
    y, v = np.asarray(years), np.asarray(values, float)
    va, vb = v[y == a][0], v[y == b][0]
    return float(math.log(vb / va) / (b - a))


def compute_longrun() -> dict:
    w = data.maddison_world()
    wy = np.array(w["year"])
    wv = np.array(w["World"])
    ok = np.isfinite(wv)
    uk = data.maddison_country("GBR")
    out = {"world_year": wy[ok], "world": wv[ok]}
    out["uk_year"], out["uk"] = np.array(uk["year"]), np.array(uk["gdppc"])
    for code in ("NLD", "CHN", "IND", "JPN", "ITA", "USA", "KOR", "NGA", "ETH"):
        c = data.maddison_country(code)
        out[f"{code}_year"], out[f"{code}_gdppc"] = np.array(c["year"]), np.array(c["gdppc"])
    g_uk_pre = _growth(uk["year"], uk["gdppc"], 1270, 1700)
    g_uk_post = _growth(uk["year"], uk["gdppc"], 1820, 2022)
    g_world = _growth(wy[ok], wv[ok], 1820, 2022)
    ratio = float(wv[wy == 2022][0] / wv[wy == 1820][0])
    uk_v = dict(zip(uk["year"], uk["gdppc"]))
    out.update({
        "g_uk_pre": g_uk_pre, "g_uk_post": g_uk_post, "g_world": g_world, "world_ratio": ratio,
        "world_1820": float(wv[wy == 1820][0]), "world_2022": float(wv[wy == 2022][0]),
        "uk_1270": float(uk_v[1270]), "uk_1700": float(uk_v[1700]), "uk_1800": float(uk_v[1800]),
        "uk_2022": float(uk_v[2022]), "uk_ratio_pre": float(uk_v[1700] / uk_v[1270]),
        "double_pre": math.log(2) / g_uk_pre, "double_world": math.log(2) / g_world,
        "rule70_world": 70 / (100 * g_world),
    })
    # the gap between the richest and the poorest country in the extract, at three dates
    for yr in (1820, 1913):
        g = sorted(r["gdppc"] for r in data.maddison_year(yr) if np.isfinite(r["gdppc"]))
        out[f"gap_{yr}"] = float(g[-1] / g[0])
        out[f"n_{yr}"] = len(g)
    kor = dict(zip(*[data.maddison_country("KOR")[k] for k in ("year", "gdppc")]))
    g1950 = sorted(r["gdppc"] for r in data.maddison_year(1950) if np.isfinite(r["gdppc"]))
    out["kor_1950"], out["kor_2022"] = float(kor[1950]), float(kor[2022])
    out["kor_1950_share_poorer"] = float(np.mean(np.array(g1950) < kor[1950]))
    out["fra_2022"] = float(dict(zip(*[data.maddison_country("FRA")[k] for k in ("year", "gdppc")]))[2022])
    assert out["kor_2022"] > max(out["uk_2022"], out["fra_2022"]) and out["kor_1950_share_poorer"] < 0.25
    assert out["gap_1913"] > 3 * out["gap_1820"]
    assert g_uk_pre < 0.003 and g_world > 0.012
    return out


def compute_film() -> dict:
    years = np.arange(1820, 2023)
    rows = data._maddison_rows()
    by = {}
    for r in rows:
        y = int(r["year"])
        if y < 1820 or r["gdppc"] == "":
            continue
        by.setdefault(r["code"], {"name": r["country"], "region": r["region"], "y": [], "g": [], "p": []})
        d = by[r["code"]]
        d["y"].append(y)
        d["g"].append(float(r["gdppc"]))
        d["p"].append(float(r["pop"]) if r["pop"] else float("nan"))
    codes, regions, names, G, P = [], [], [], [], []
    for code, d in sorted(by.items()):
        y = np.array(d["y"])
        g = np.log(np.array(d["g"]))
        p = np.array(d["p"])
        o = np.argsort(y)
        y, g, p = y[o], g[o], p[o]
        lg = np.interp(years, y, g, left=np.nan, right=np.nan)
        okp = np.isfinite(p)
        lp = np.interp(years, y[okp], np.log(p[okp]), left=np.nan, right=np.nan) if okp.sum() >= 2 else \
            np.full(len(years), np.log(p[okp][0]) if okp.any() else np.nan)
        codes.append(code)
        regions.append(d["region"])
        names.append(d["name"])
        G.append(lg)
        P.append(lp)
    G, P = np.array(G), np.array(P)
    w = data.maddison_world()
    wy, wv = np.array(w["year"]), np.array(w["World"])
    ok = np.isfinite(wv)
    world = np.exp(np.interp(years, wy[ok], np.log(wv[ok])))
    regions_list = sorted(set(regions))
    shown = int(np.isfinite(G[:, -1]).sum())
    assert shown > 150
    return {"years": years, "codes": codes, "regions": regions, "names": names, "region_list": regions_list,
            "log_gdppc": G, "log_pop": P, "world": world, "world_years": wy[ok], "world_values": wv[ok],
            "n_2022": shown, "n_1820": int(np.isfinite(G[:, 0]).sum())}


FILM_SECONDS = 32.0  # the data film's run from 1820 to 2022
MELODY_SECONDS = 44.0  # with the "story so far" card after it


def film_time(year: float) -> float:
    """When the data film reaches ``year``."""
    return 1.5 + FILM_SECONDS * (year - 1820) / (2022 - 1820)


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    w = data.maddison_world()
    wy, wv = np.array(w["year"]), np.array(w["World"])
    ok = np.isfinite(wv)
    wy, wv = wy[ok], wv[ok]
    times = [film_time(y) for y in wy]
    mel = score.data_melody(wv, MELODY_SECONDS, times=times, act=1)
    store = ClipStore("econ1")
    events = {f"y{int(y)}": float(t) for y, t in zip(wy, times)}
    events["film_end"] = film_time(2022) + 1.0
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 1.0, "hz": score.hz(m), "name": str(int(y))}
                       for t, m, y in zip(times, mel["notes"], wy)],
                meta={"label": "the world's GDP per head, 1820-2022, as a tune (computed)", "kind": "synthesized"})
    store.save("intermission.melody", clip)
    return {"years": wy, "values": wv, "times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS,
            "film_seconds": FILM_SECONDS}


def _monthly(series: str, start: str, months: int) -> np.ndarray:
    s = data.fred(series)
    i = s["date"].index(start)
    return np.array(s["value"][i:i + months + 1], float)


def compute_collapses() -> dict:
    n = 60
    ip29, ip07 = _monthly("INDPRO", "1929-08-01", n), _monthly("INDPRO", "2007-12-01", n)
    cpi29, cpi07 = _monthly("CPIAUCNS", "1929-08-01", n), _monthly("CPIAUCNS", "2007-12-01", n)
    u29 = _monthly("M0892AUSM156SNBR", "1929-08-01", n)
    u07 = _monthly("UNRATE", "2007-12-01", n)
    g = data.fred("GDPCA")
    gy = [int(d[:4]) for d in g["date"]]
    gv = np.array(g["value"])
    gdp29 = gv[gy.index(1929):gy.index(1929) + 8] / gv[gy.index(1929)] * 100
    gdp07 = gv[gy.index(2007):gy.index(2007) + 8] / gv[gy.index(2007)] * 100
    out = {"months": np.arange(n + 1), "ip29": ip29 / ip29[0] * 100, "ip07": ip07 / ip07[0] * 100,
           "cpi29": cpi29 / cpi29[0] * 100, "cpi07": cpi07 / cpi07[0] * 100, "u29": u29, "u07": u07,
           "gdp_years": np.arange(8), "gdp29": gdp29, "gdp07": gdp07}
    out.update({
        "ip29_min": float(out["ip29"].min()), "ip07_min": float(out["ip07"].min()),
        "ip29_min_month": int(np.argmin(out["ip29"])), "ip07_min_month": int(np.argmin(out["ip07"])),
        "u29_max": float(np.nanmax(u29)), "u07_max": float(np.nanmax(u07)),
        "cpi29_min": float(out["cpi29"].min()), "cpi07_min": float(out["cpi07"].min()),
        "gdp29_min": float(gdp29.min()), "gdp07_min": float(gdp07.min()),
    })
    assert out["ip29_min"] < 60 and out["u29_max"] > 24 and out["u07_max"] < 11
    return out


def compute_spf() -> dict:
    rows = {(r["year"], r["quarter"]): r for r in data.spf()}
    g = data.fred("GDPCA")
    gy = [int(d[:4]) for d in g["date"]]
    gv = np.array(g["value"])
    actual_2009 = gv[gy.index(2009)] / gv[gy.index(2008)] - 1
    # the largest fall since 1946
    falls = [(gv[i] / gv[i - 1] - 1, gy[i]) for i in range(1, len(gy)) if gy[i] > 1946]
    assert min(falls)[1] == 2009
    q = data.fred("GDPC1")
    qi = q["date"].index("2008-10-01")
    actual_q4 = (q["value"][qi] / q["value"][qi - 1]) ** 4 - 1
    surveys = []
    for key in ((2008, 1), (2008, 2), (2008, 3), (2008, 4), (2009, 1)):
        r = rows[key]
        nxt = r["rgdp_b"] / r["rgdp_a"] - 1 if key[0] == 2008 else float("nan")
        surveys.append({"year": key[0], "quarter": key[1], "forecast_2009": nxt, "recess": r["recess"],
                        "growth_q": r["growth_q"]})
    aug = surveys[2]
    out = {"surveys": surveys, "actual_2009": float(actual_2009), "aug_2009": float(aug["forecast_2009"]),
           "nov_2009": float(surveys[3]["forecast_2009"]), "aug_q4": float(aug["growth_q"][1] / 100),
           "aug_recess_q4": float(aug["recess"][1]), "actual_q4": float(actual_q4)}
    assert out["aug_2009"] > 0.01 and out["actual_2009"] < -0.02
    return out


ITEMS = {
    "pit": compute_pit,
    "crusoe": compute_crusoe,
    "ricardo": compute_ricardo,
    "pins": compute_pins,
    "tin": compute_tin,
    "fine": compute_fine,
    "longrun": compute_longrun,
    "film": compute_film,
    "melody": compute_melody,
    "collapses": compute_collapses,
    "spf": compute_spf,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
