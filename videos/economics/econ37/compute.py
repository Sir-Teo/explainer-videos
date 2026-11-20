"""Precompute every number in Part 37 of *Economics, Built* ("Cities and Regions").

    python -m videos.economics.econ37.compute            # everything missing (about a minute)
    python -m videos.economics.econ37.compute --force zipf

Results are cached in ``.cache/econ37/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Census Bureau's Vintage 2024 population of every metropolitan area; HYDE's urban
shares since 1500, via Our World in Data; the twenty Case-Shiller metropolitan indices and the work-from-home rate,
via FRED; the tables of Saiz, Combes et al., Ahlfeldt et al., Ciccone and Hall, Diamond et al., Chetty et al., Hsieh
and Moretti with Greaney's comment, Donaldson, Baum-Snow, Kline and Moretti, Shenzhen's census and Schelling's
history).  Models: Agora's city (``agora.city``) with the Island's Part 37 truths.

Items:
    schelling    the checkerboard: a board played to the end, and the final mixing against tolerance
    thunen       von Thuenen's rings around the market town, before and after a railway
    mono         the monocentric town: rent, height and density gradients; the car and the lift
    agglo        agglomeration and sorting on the Island: across towns and from movers
    zipf         Zipf's law for America's metropolitan areas, and Gibrat's growth with a floor
    cp           Krugman's core and periphery: the wiggle diagram and the tomahawk
    towns        the Island's six towns in spatial equilibrium; amenities read from prices; shocks
    housing      house prices since 2000 in the twenty Case-Shiller metros against Saiz's elasticities
    berlin       a line city divided by a wall, and reunited
    transport    highways in the monocentric town; the railway in the rings
    place        a place-based subsidy where housing is tight and where it is not
    wfh          working from home, 2019-2026
    film         the intermission's data film: the world's urban share, 1500-2025
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import city
from explainer.economics.data import tables

CACHE = Cache("econ37")
load = CACHE.load
TRUTH = island.truths(37)
FILM_SECONDS = 50.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _thin(xs, k=150):
    xs = np.asarray(xs, float)
    step = max(1, len(xs) // k)
    return xs[::step].tolist()


def compute_schelling() -> dict:
    S = TRUTH["schelling"]
    run = city.schelling(S["n"], S["empty"], S["threshold"], S["seed"])
    half = city.schelling(S["n"], S["empty"], 0.5, S["seed"], keep_frames=False)
    ths = np.round(np.arange(0.05, 0.80, 0.05), 2)
    sweep = city.schelling_sweep(ths, seeds=(0, 1, 2), n=30)
    return {"frames": run["frames"], "like": run["like"], "unhappy": run["unhappy"], "moves": run["moves"],
            "rounds": run["rounds"], "final": run["final_like"], "start": run["like"][0], "settled": run["settled"],
            "half_final": half["final_like"], "sweep": sweep, "n": S["n"], "threshold": S["threshold"],
            "history": tables.SCHELLING_1971.data}


def compute_thunen() -> dict:
    crops = [dict(c) for c in TRUTH["thunen"]]
    x = np.linspace(0, 110, 1101)
    base = city.thunen(crops, x)
    rail = [dict(c) for c in crops]
    for c in rail:
        if c["name"] in ("grain", "cattle"):
            c["freight"] *= 0.5
    x2 = np.linspace(0, 220, 2201)
    after = city.thunen(rail, x2)
    return {"names": [c["name"] for c in crops], "x": _thin(x, 220), "bids": [_thin(b, 220) for b in base["bids"]],
            "rings": base["rings"], "rings_rail": after["rings"], "rent0": base["rent"][0], "crops": crops}


def compute_mono() -> dict:
    M = TRUTH["mono"]
    kw = {k: M[k] for k in ("N", "y", "t", "alpha", "theta", "i")}
    base = city.monocentric(**kw)
    car = city.monocentric(**{**kw, "t": M["t"] * M["car"]})
    lift = city.monocentric(**{**kw, "i": M["i"] * M["lift"]})

    def pack(m):
        x = np.array(m["x"])
        keep = x <= 40
        return {"x": _thin(x[keep], 160), "p": _thin(np.array(m["p"])[keep], 160),
                "far": _thin(np.array(m["far"])[keep], 160), "D": _thin(np.array(m["D"])[keep], 160),
                "r": _thin(np.array(m["r"])[keep], 160), "h": _thin(np.array(m["h"])[keep], 160),
                "edge": m["edge"], "u": m["u"], "centre_density": m["centre_density"], "within8": m["within8"],
                "far0": float(np.array(m["far"])[0]), "h0": float(np.array(m["h"])[0]),
                "p0": float(np.array(m["p"])[0])}

    b, c, li = pack(base), pack(car), pack(lift)
    # the rent gradient: the fall in floor rent per kilometre near the centre, in percent
    def grad(m):
        x, p = np.array(m["x"]), np.array(m["p"])
        k = np.searchsorted(x, 5.0)
        return float(100 * (1 - (p[k] / p[0]) ** (1 / x[k])))
    return {"base": b, "car": c, "lift": li, "grad": grad(b), "grad_car": grad(c), "params": dict(M)}


def compute_agglo() -> dict:
    A = TRUTH["agglo"]
    r = city.agglomeration_panel(gamma=A["gamma"], sort=A["sort"], seed=A["seed"])
    return {**r, "cdgr": tables.CDGR_2010.data, "ch": tables.CICCONE_HALL_1996.data}


def compute_zipf() -> dict:
    m = data.cbsa()
    pops = np.array(m["pop2024"], float)
    order = np.argsort(-pops)
    names = [m["name"][k].split(",")[0].split("-")[0] for k in order]
    fit_all = city.zipf_fit(pops)
    fit_100 = city.zipf_fit(pops, top=100)
    G = TRUTH["gibrat"]
    g = city.gibrat(G["n"], G["T"], G["sigma"], G["floor"], G["seed"])
    gs = np.sort(np.array(g["sizes"]))[::-1][:2000]
    return {"names": names[:12], "pops": pops[order].tolist(), "zeta_all": fit_all["zeta"], "se_all": fit_all["se"],
            "zeta_100": fit_100["zeta"], "se_100": fit_100["se"], "c_100": fit_100["intercept"], "n": len(pops),
            "ny": float(pops[order][0]), "second": float(pops[order][1]), "tenth": float(pops[order][9]),
            "gibrat_sizes": gs.tolist(), "gibrat_zeta": g["zeta"], "gibrat_theory": g["theory"],
            "gibrat_paths": g["paths"], "gibrat_sd": g["growth_sd_by_quintile"], "floor": G["floor"]}


def compute_cp() -> dict:
    P = TRUTH["cp"]
    lams = np.linspace(0, 1, 41)
    wig = {f"{T:.1f}": city.cp_gap(T, lams, P["mu"], P["sigma"]) for T in (1.5, 1.7, 2.1)}
    Ts = np.round(np.arange(1.30, 2.21, 0.02), 2)
    tom = city.cp_tomahawk(Ts, P["mu"], P["sigma"], n_lam=81)
    return {"lams": lams.tolist(), "wiggle": wig, "tomahawk": tom["points"], "break": tom["break"],
            "sustain": tom["sustain"], **P}


def compute_towns() -> dict:
    t = TRUTH["towns"]
    kw = {"b": t["b"], "alpha": t["alpha"]}
    base = city.roback(t["a"], t["q"], t["eta"], **kw)
    prod = city.roback_shock(t["a"], t["q"], t["eta"], 0, da=0.10, **kw)
    amen = city.roback_shock(t["a"], t["q"], t["eta"], 5, dq=0.10, **kw)
    relax = city.roback_shock(t["a"], t["q"], t["eta"], 0, deta=3.0, **kw)
    strip = lambda d: {k: v for k, v in d.items() if k not in ("base", "new")}  # noqa: E731
    return {"names": list(t["names"]), "a": list(t["a"]), "q": list(t["q"]), "eta": list(t["eta"]), "base": base,
            "prod": strip(prod), "prod_new": prod["new"], "amen": strip(amen), "amen_new": amen["new"],
            "relax": strip(relax), "relax_new": relax["new"], **kw}


def compute_housing() -> dict:
    S = tables.SAIZ_2010.data["metros"]
    rows = []
    for k, name in data.CASE_SHILLER_METROS.items():
        d = data.fred(f"{k}XRSA")
        v = {x: y for x, y in zip(d["date"], d["value"]) if np.isfinite(y)}
        a = np.mean([v[x] for x in v if x.startswith("2000")])
        b = np.mean([v[x] for x in v if x.startswith("2025")])
        rows.append({"metro": name, "elasticity": S[name], "growth": float(b / a), "last": max(v)})
    e = np.log([r["elasticity"] for r in rows])
    g = np.log([r["growth"] for r in rows])
    slope, icpt = np.polyfit(e, g, 1)
    corr = float(np.corrcoef(e, g)[0, 1])
    cpi = data.fred("CPIAUCSL")
    cv = {x: y for x, y in zip(cpi["date"], cpi["value"]) if np.isfinite(y)}
    infl = float(np.mean([cv[x] for x in cv if x.startswith("2025")]) / np.mean([cv[x] for x in cv
                                                                              if x.startswith("2000")]))
    # supply and demand: demand for a town's houses rises 20 percent; demand elasticity 1
    shift = 0.20
    ill = {f"{es:.1f}": {"dp": shift / (es + 1.0), "dq": es * shift / (es + 1.0)} for es in (0.6, 3.0)}
    return {"rows": rows, "slope": float(slope), "icpt": float(icpt), "corr": corr, "cpi": infl, "illus": ill,
            "saiz": {k: tables.SAIZ_2010.data[k] for k in ("weighted", "unweighted", "common")},
            "hm": tables.HSIEH_MORETTI_2019.data, "dmq": tables.DMQ_2019.data, "chk": tables.CHK_2016.data}


def compute_berlin() -> dict:
    B = TRUTH["berlin"]
    W = city.wall_experiment(**B)
    I, D = W["integrated"], W["divided"]
    return {"x_all": I["x"], "HM": I["HM"], "HR": I["HR"], "x": W["x"], "dist": W["dist"],
            "division": W["division"], "reunification": W["reunification"], "HM_div": D["HM"], "HR_div": D["HR"],
            "jobs_east": W["jobs_east"], "slope": W["slope"], "arsw": tables.ARSW_2015.data, **B}


def compute_transport() -> dict:
    M = TRUTH["mono"]
    kw = {k: M[k] for k in ("N", "y", "t", "alpha", "theta", "i")}
    base = city.monocentric(**kw)
    hw = city.monocentric(**{**kw, "t": M["t"] * 0.7})
    th = compute_thunen()
    return {"within8": base["within8"], "within8_hw": hw["within8"], "edge": base["edge"], "edge_hw": hw["edge"],
            "drop": hw["within8"] / base["within8"] - 1, "rings": th["rings"], "rings_rail": th["rings_rail"],
            "bs": tables.BAUM_SNOW_2007.data, "donaldson": tables.DONALDSON_2018.data}


def compute_place() -> dict:
    t = TRUTH["towns"]
    kw = {"b": t["b"], "alpha": t["alpha"]}
    out = {}
    for j in (0, 3):                        # Harbour (tight housing) and Grove (loose)
        sh = city.roback_shock(t["a"], t["q"], t["eta"], j, da=0.10, **kw)
        out[t["names"][j]] = {k: sh[k] for k in ("dlogw", "dlogr", "dlogN", "dv", "doutput")} | {"eta": t["eta"][j]}
    return {"towns": out, "shenzhen": tables.SHENZHEN.data, "tva": tables.KLINE_MORETTI_2014.data}


def compute_wfh() -> dict:
    d = data.fred("WFHCOVIDMATQUESTION")
    pts = [(x, y) for x, y in zip(d["date"], d["value"]) if np.isfinite(y)]
    t = [int(x[:4]) + (int(x[5:7]) - 1) / 12 for x, _ in pts]
    v = [y for _, y in pts]
    k = int(np.argmax(v))
    last12 = float(np.mean(v[-12:]))
    return {"t": t, "v": v, "pre": v[0], "peak": v[k], "peak_t": pts[k][0], "last": v[-1], "last_t": pts[-1][0],
            "last12": last12}


def film_time(t: float, first: float = 1500.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    W = data.urban_share("World")
    U = data.urban_share("United States")
    Cn = data.urban_share("China")
    ys = [y for y in W["year"] if y >= 1500]
    v = [W["value"][W["year"].index(y)] for y in ys]
    half = next(y for y, x in zip(ys, v) if x >= 50)
    return {"t": ys, "v": v, "times": [film_time(y) for y in ys], "us_t": U["year"], "us_v": U["value"],
            "cn_t": Cn["year"], "cn_v": Cn["value"], "half": half, "first": v[0], "last": v[-1],
            "v1800": W["value"][W["year"].index(1800)], "v1900": W["value"][W["year"].index(1900)],
            "v1950": W["value"][W["year"].index(1950)]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=7, log=False, low=40, high=86)
    events = {"film_end": film_time(2025) + 6.0, "first": times[0], "half": film_time(f["half"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"{x:.0f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the world's urban share, 1500-2025 (HYDE 3.5, via Our World in Data), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ37").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "schelling": compute_schelling,
    "thunen": compute_thunen,
    "mono": compute_mono,
    "agglo": compute_agglo,
    "zipf": compute_zipf,
    "cp": compute_cp,
    "towns": compute_towns,
    "housing": compute_housing,
    "berlin": compute_berlin,
    "transport": compute_transport,
    "place": compute_place,
    "wfh": compute_wfh,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
