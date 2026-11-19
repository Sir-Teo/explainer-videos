"""Precompute every number in Part 8 of *Economics, Built* ("The Firm").

    python -m videos.economics.econ8.compute            # everything missing (seconds)
    python -m videos.economics.econ8.compute --force douglas

Results are cached in ``.cache/econ8/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Penn World Table's labour share for the United States, 1950-2023, via FRED; Cobb
and Douglas's 1899-1922 indices as reproduced by Felipe and Adams).  Models: Agora's firm (``agora.firm``), with the
Island's Part 8 truths.  Every random draw is seeded.

Items:
    douglas      Cobb and Douglas's data: the three indices, where output lies between labour and capital each year,
                 and the regressions (constant returns imposed, unrestricted, with a trend, in growth rates, to 1920)
    share        the labour share in the United States, 1950-2023 (Penn World Table)
    techs        isoquants for elasticities of substitution 0, 0.5, 1, 2 and infinity; the boatyard's isoquants,
                 marginal products and technical rate of substitution
    scale        returns to scale for the yard; a pipeline's steel against its capacity; the six-tenths rule
    costmin      the yard's least-cost slipways and shipwrights, its cost function, Shephard's lemma checked
    curves       short-run costs with four slipways, and the long-run envelope
    playit       the boatyard game: the marginal product of each shipwright and its value
    supply       the yard's supply, short and long run; Hotelling's lemma; Le Chatelier
    industry     free entry: identical yards and yards with different fixed costs
    selection    Alchian's survival: rule-of-thumb markups under selection
    boundary     hold-up, Grossman-Hart-Moore, make or buy
    dial         the dials' rows: capital's output elasticity and the elasticity of substitution
    film         the intermission's data film: Cobb and Douglas's indices drawn year by year
    melody       its data melody: the index of output, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import firm as fm
from explainer.economics.data import tables

CACHE = Cache("econ8")
load = CACHE.load
TRUTH = island.truths(8)


def _yard() -> fm.CobbDouglas:
    y = TRUTH["yard"]
    return fm.CobbDouglas(y["A"], y["a"], y["b"])


# ---------------------------------------------------------------------------------------------------------------
# Douglas's data

def compute_douglas() -> dict:
    d = tables.COBB_DOUGLAS_1928.data
    Y, L, K = (np.array(d[k], float) for k in ("output", "labour", "capital"))
    years = np.array(d["years"])
    where = (np.log(Y) - np.log(L)) / np.maximum(np.log(K) - np.log(L), 1e-9)
    where[0] = np.nan                                        # 1899: all three are 100
    fits = {h: fm.fit_cobb_douglas(Y, K, L, h, years=years) for h in ("crs", "unrestricted", "trend", "growth")}
    early = fm.fit_cobb_douglas(Y[:-2], K[:-2], L[:-2], "unrestricted")
    fa = d["felipe_adams"]
    assert abs(fits["unrestricted"]["labour"] - fa["unrestricted"]["labour"]) < 0.003
    assert abs(fits["unrestricted"]["capital"] - fa["unrestricted"]["capital"]) < 0.003
    assert fits["trend"]["capital"] < 0
    out = {"years": years, "Y": Y, "L": L, "K": K, "where": where, "where_mean": float(np.nanmean(where[1:])),
           "early": {k: v for k, v in early.items() if not isinstance(v, np.ndarray)},
           "fitted_crs": np.exp(fits["crs"]["fitted"]) * L}
    for h, f in fits.items():
        out[h] = {k: v for k, v in f.items() if not isinstance(v, np.ndarray)}
    out["A"] = float(np.exp(fits["crs"]["const"]))
    return out


def compute_share() -> dict:
    s = data.fred("LABSHPUSA156NRUG")
    years = np.array([int(x[:4]) for x in s["date"]])
    v = np.array(s["value"], float)
    ok = np.isfinite(v)
    years, v = years[ok], v[ok]
    early = v[(years >= 1950) & (years <= 1999)]
    late = v[years >= 2000]
    return {"years": years, "share": v, "mean_1950_1999": float(early.mean()), "min_1950_1999": float(early.min()),
            "max_1950_1999": float(early.max()), "last": float(v[-1]), "last_year": int(years[-1]),
            "mean_2000_on": float(late.mean())}


# ---------------------------------------------------------------------------------------------------------------
# technologies and scale

def compute_techs() -> dict:
    t = TRUTH["techs"]
    s = t["share"]
    Ls = np.linspace(0.05, 4.0, 300)
    curves = {}
    for sg in t["sigmas"]:
        if sg == 0:
            tech = fm.Leontief(1.0, 1.0)
        elif abs(sg - 1) < 1e-9:
            tech = fm.CobbDouglas(1.0, s, 1 - s)
        else:
            tech = fm.CES(1.0, s, sg, 1.0)
        # normalized to pass through (1, 1): q = 1 at K = L = 1
        curves[f"{sg:g}"] = list(fm.isoquant(tech, float(tech.q(1.0, 1.0)), Ls))
    # perfect substitutes: K = (1 - (1 - s) L) / s
    curves["inf"] = list((1 - (1 - s) * Ls) / s)
    y = _yard()
    Lg = np.linspace(0.5, 12, 200)
    q44 = float(y.q(4.0, 4.0))                                 # the isoquant through four of each: 5.66 boats
    iso = {"4": list(fm.isoquant(y, 4.0, Lg)), "5.66": list(fm.isoquant(y, q44, Lg)), "8": list(fm.isoquant(y, 8.0, Lg))}
    K0 = TRUTH["yard"]["slipways"]
    workers = np.arange(1, 13)
    mpl = y.mp(K0, workers.astype(float))[1]
    inc = np.diff(y.q(K0, np.arange(0, 13, dtype=float)))      # what each shipwright adds, one at a time
    return {"Ls": Ls, "curves": curves, "share": s, "Lg": Lg, "iso": iso, "workers": workers, "mpl": mpl, "inc": inc,
            "trs_at": {"K": 4.0, "L": 4.0, "trs": float(y.trs(4.0, 4.0))}, "yard": TRUTH["yard"]}


def compute_scale() -> dict:
    y = _yard()
    ts = np.array([1.0, 2.0, 3.0, 4.0])
    out_q = [float(y.q(4.0 * t, 4.0 * t)) for t in ts]
    crs = fm.CobbDouglas(2.0, 0.3, 0.7)
    irs = fm.CobbDouglas(2.0, 0.4, 0.8)
    rows = {"decreasing (0.75)": out_q, "constant (1.0)": [float(crs.q(4 * t, 4 * t)) for t in ts],
            "increasing (1.2)": [float(irs.q(4 * t, 4 * t)) for t in ts]}
    # a pipe: steel ~ circumference x length (d), capacity ~ cross-section (d^2): cost per unit of capacity ~ 1/d
    d = np.linspace(0.25, 2.0, 50)
    steel, capacity = d, d ** 2
    cap = np.linspace(1, 100, 100)
    six = cap ** 0.6
    return {"ts": ts, "rows": rows, "d": d, "steel": steel, "capacity": capacity, "cap": cap, "six": six,
            "pipe_exponent": 0.5, "tank_exponent": 2 / 3}


# ---------------------------------------------------------------------------------------------------------------
# costs

def compute_costmin() -> dict:
    t = TRUTH["yard"]
    y = _yard()
    w, r = t["wage"], t["rent"]
    q = 8.0
    K, L = y.demand(w, r, q)
    c = y.cost(w, r, q)
    Lg = np.linspace(0.5, 30, 300)
    iso = list(fm.isoquant(y, q, Lg))
    # isocost lines through the optimum and two dearer ones
    lines = {f"{k:g}": [(0.0, k / r), (k / w, 0.0)] for k in (c, 1.3 * c, 0.75 * c)}
    # factor demands as the relative price changes
    ratios = np.linspace(0.5, 5.0, 46)
    dem = [y.demand(w, w / x, q) for x in ratios]
    errs = {}
    for name, tech in (("yard", y), ("CES 0.5", fm.CES(2.0, 0.3, 0.5, 0.75)), ("CES 2", fm.CES(2.0, 0.3, 2.0, 0.75))):
        errs[name] = max(fm.shephard_errors(tech, w, r, q).values())
    qs = np.linspace(0.5, 20, 60)
    return {"w": w, "r": r, "q": q, "K": K, "L": L, "cost": c, "Lg": Lg, "iso": iso, "lines": lines,
            "ratios": ratios, "K_of_ratio": [k for k, _ in dem], "L_of_ratio": [l_ for _, l_ in dem],
            "shephard": errs, "qs": qs, "cost_curve": [y.cost(w, r, x) for x in qs]}


def compute_curves() -> dict:
    t = TRUTH["yard"]
    y = _yard()
    w, r = t["wage"], t["rent"]
    sr = fm.ShortRun(y, t["slipways"], w, r)
    qs = np.linspace(0.6, 16, 300)
    lr_ac = np.array([y.cost(w, r, q) / q for q in qs])
    srs = {}
    for K in (1.0, 2.0, 4.0, 8.0, 16.0):
        s_ = fm.ShortRun(y, K, w, r)
        srs[f"{K:g}"] = list(s_.atc(qs))
    i_min = int(np.argmin(sr.atc(qs)))
    j_min = int(np.argmin(sr.avc(qs)))
    return {"qs": qs, "fc": float(r * t["slipways"]), "vc": sr.vc(qs), "tc": sr.tc(qs), "atc": sr.atc(qs),
            "avc": sr.avc(qs), "mc": sr.mc(qs), "lr_ac": lr_ac, "srs": srs, "atc_min_q": float(qs[i_min]),
            "atc_min": float(sr.atc(qs)[i_min]), "avc_min": float(sr.avc(qs)[j_min])}


def compute_playit() -> dict:
    t = TRUTH["yard"]
    y = _yard()
    h = fm.hire(t["price"], t["wage"], y, t["slipways"], max_workers=12)
    return {"workers": h["workers"], "output": h["output"], "mp": h["mp"], "value": t["price"] * h["mp"],
            "wage": t["wage"], "price": t["price"], "hired": h["hired"], "profit": h["profit"] - t["rent"] *
            t["slipways"], "best": h["best"], "slipways": t["slipways"], "rent": t["rent"]}


def compute_supply() -> dict:
    t = TRUTH["yard"]
    y = _yard()
    w, r = t["wage"], t["rent"]
    ps = np.linspace(400, 3000, 120)
    lr = [fm.cd_supply(y, p, w, r) for p in ps]
    sr_ = fm.ShortRun(y, t["slipways"], w, r)
    # short run: price = MC with K fixed, above the minimum of AVC (which is 0 here: AVC rises from 0)
    b = y.b
    k = w / (y.A * t["slipways"] ** y.a) ** (1 / b)          # VC = k q^(1/b)
    sr = [float((p * b / k) ** (b / (1 - b))) for p in ps]
    lc = fm.le_chatelier(y)
    errs = fm.hotelling_errors(y, t["price"], w, r)
    q_now = fm.cd_supply(y, t["price"], w, r)
    return {"ps": ps, "lr": lr, "sr": sr, "le_chatelier": lc, "hotelling": errs, "q_now": q_now,
            "profit_now": fm.cd_profit(y, t["price"], w, r), "K_now": y.demand(w, r, q_now)[0],
            "mc_check": float(sr_.mc(5.0))}


def compute_industry() -> dict:
    t = TRUTH["industry"]
    a, b = t["demand"]
    same = fm.industry(a, b, t["F"], t["c"], t["d"])
    fixed = np.linspace(*t["fixed_range"], t["entrants"])
    het = fm.industry(a, b, None, t["c"], t["d"], fixed_costs=fixed)
    u = fm.UCost(t["F"], t["c"], t["d"])
    qs = np.linspace(1, 20, 200)
    # the long-run supply with heterogeneous yards: for each number of yards, the price at which the marginal one
    # just breaks even
    lrs = []
    for n in range(1, len(fixed) + 1, 5):
        uu = fm.UCost(fixed[n - 1], t["c"], t["d"])
        lrs.append((n * uu.efficient_scale, uu.breakeven))
    return {"same": {k: v for k, v in same.items()}, "het": {k: v for k, v in het.items() if k != "profits"},
            "het_profits": het["profits"], "qs": qs, "atc": u.atc(qs), "mc": u.mc(qs), "breakeven": u.breakeven,
            "scale": u.efficient_scale, "lrs": lrs, "demand": (a, b)}


def compute_selection() -> dict:
    s = TRUTH["selection"]
    out = fm.selection(s["yards"], s["months"], s["elasticity"], s["noise"], s["mutation"], s["seed"])
    M = out["markups"]
    pct = np.percentile(M, [10, 25, 50, 75, 90], axis=1)
    return {"months": np.arange(M.shape[0]), "pct": pct, "first": M[0], "last": M[-1], "best": out["best"],
            "closures": out["closures"], "total_closed": int(out["closures"].sum())}


def compute_boundary() -> dict:
    h = TRUTH["holdup"]
    hu = fm.hold_up(h["V"], h["theta"])
    i = np.linspace(0, 140, 200)
    value = 2 * h["V"] * np.sqrt(i)
    g = TRUTH["ghm"]
    gh = fm.ghm(g["va"], g["vb"], g["outside"], g["outside"])
    gh2 = fm.ghm(g["vb"], g["va"], g["outside"], g["outside"])
    k = np.linspace(0, 1.2, 61)
    mb = fm.make_or_buy(k)
    return {"holdup": hu, "i": i, "value": value, "V": h["V"], "theta": h["theta"], "ghm": gh, "ghm_swapped": gh2,
            "k": k, "market": mb["market"], "hierarchy": mb["hierarchy"], "switch": mb["switch"]}


def compute_dial() -> dict:
    out = {}
    for key in ("capital_share", "kl_substitution"):
        dl = dials.DIALS[key]
        out[key] = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dl.estimates]
    return out


# ---------------------------------------------------------------------------------------------------------------
# the intermission: Douglas's chart, year by year

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    d = compute_douglas()
    n = len(d["years"])
    return {"years": d["years"], "Y": d["Y"], "L": d["L"], "K": d["K"], "fitted": d["fitted_crs"],
            "times": [film_time(k, n) for k in range(n)], "A": d["A"], "labour": d["crs"]["labour"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    Y = np.array(f["Y"])
    times = f["times"]
    mel = score.data_melody(Y, MELODY_SECONDS, times=times, act=2, log=True, low=45, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "American manufacturing output, 1899-1922 (Cobb and Douglas's index), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ8").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "Y": Y, "seconds": MELODY_SECONDS}


ITEMS = {
    "douglas": compute_douglas,
    "share": compute_share,
    "techs": compute_techs,
    "scale": compute_scale,
    "costmin": compute_costmin,
    "curves": compute_curves,
    "playit": compute_playit,
    "supply": compute_supply,
    "industry": compute_industry,
    "selection": compute_selection,
    "boundary": compute_boundary,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
