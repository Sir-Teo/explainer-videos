"""Precompute every number in Part 40 of *Economics, Built* ("Inequality and Mobility").

    python -m videos.economics.econ40.compute            # everything missing (about two minutes)
    python -m videos.economics.econ40.compute --force speed

Results are cached in ``.cache/econ40/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Piketty and Saez's top shares, 1913-2022; the World Inequality Database's top 1%
shares via Our World in Data; Opportunity Insights' mobility tables (by parent percentile, by birth cohort, by
commuting zone); the Federal Reserve's Distributional Financial Accounts and the Census Bureau's Gini via FRED; the
Penn World Table; the tables of Pen, Atkinson, Auten and Splinter, Pareto, Gabaix, Lasry, Lions and Moll, Piketty,
Kuznets, Solon, Mazumder, Corak, Chetty and coauthors, Lakner and Milanovic, Klass et al. and the frontier).  Models:
Agora's distribution (``agora.distribution``) with the Island's Part 40 truths.

Items:
    parade       Pen's parade: American families by income percentile, heights against the mean; the top 0.01%
    guess        the four numbers of the game
    measures     the Island's incomes: Lorenz curve, Gini, Atkinson, Theil, top shares with standard errors;
                 two societies with the same Gini whose Lorenz curves cross; America's Gini since 1967
    top          a century of top shares (Piketty and Saez); top 1% shares in eight countries (WID)
    pareto       the Pareto exponent implied by top shares, 1913-2022; the tail in 1970 and 2022
    growth       random growth: careers, the simulated tail against the Kolmogorov forward equation's
    speed        the transition after a shock: pure random growth against type dependence; America's top 1%
    wealth       wealth shares (DFA) and the exponent they imply; the exponent against r - g
    kuznets      Kuznets's dual economy; America's top 10% share
    ige          generations: the elasticity from one year and from averages; ranks
    gatsby       the mechanism (a family of economies); 709 commuting zones
    chetty       the rank-rank line, the quintile matrix, absolute mobility by cohort
    places       commuting zones: the spread of upward mobility, the largest places, what correlates
    world        inequality between countries (PWT), with and without China and India; the world's top 1%
    practice     a distributional table: a flat tax with an equal transfer on the Island
    film         the intermission's data film: the top 1% share, 1913-2022
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import distribution as D
from explainer.economics.data import tables

CACHE = Cache("econ40")
load = CACHE.load
TRUTH = island.truths(40)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0
HEIGHT = 1.7  # metres: the height of a person with the average income
WID_SHOWN = ("United States", "United Kingdom", "France", "Sweden", "Germany", "China", "India", "Russia")


def _a(d, k):
    return np.array(d[k], float)


def _annual(key: str, min_obs: int = 1) -> dict:
    d = data.fred(key)
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items() if len(v) >= min_obs}


def _latest(key: str) -> tuple[str, float]:
    d = data.fred(key)
    for x, v in zip(d["date"][::-1], d["value"][::-1]):
        if np.isfinite(v):
            return x, float(v)
    raise ValueError(key)


def compute_parade() -> dict:
    N = data.opportunity("national")
    inc = _a(N, "par_inc")
    mean = float(inc.mean())
    S = data.saez()
    k = S["year"].index(2022)
    avg = S["avg"][k]
    top001 = S["top001"][k] / 100 / 0.0001  # the top 0.01%'s average income over the average
    top01 = S["top01"][k] / 100 / 0.001
    top1 = S["top1"][k] / 100 / 0.01
    h = inc / mean * HEIGHT
    cross = int(np.argmax(inc >= mean)) + 1
    return {"pctile": list(range(1, 101)), "income": inc.tolist(), "height": h.tolist(), "mean": mean,
            "median": float((inc[49] + inc[50]) / 2), "minute_mean": 0.6 * cross, "pct_mean": cross,
            "h_median": float((h[49] + h[50]) / 2), "h_p10": float(h[9]), "h_p90": float(h[89]),
            "h_p99": float(h[98]), "h_p100": float(h[99]), "inc_p100": float(inc[99]), "inc_p1": float(inc[0]),
            "inc_p10": float(inc[9]), "inc_p90": float(inc[89]), "inc_p99": float(inc[98]),
            "saez_avg": avg, "ratio_top1": top1, "ratio_top01": top01, "ratio_top001": top001,
            "h_top1": top1 * HEIGHT, "h_top01": top01 * HEIGHT, "h_top001": top001 * HEIGHT,
            "inc_top001": top001 * avg}


def compute_guess() -> dict:
    S = data.saez()
    k = S["year"].index(2022)
    d, w = _latest("WFRBST01134")
    N = data.opportunity("national")
    q5q1 = float(np.mean(_a(N, "q5")[:20]))
    A = data.opportunity("absmob")
    am = dict(zip([int(c) for c in A["cohort"]], A["mean"]))
    return {"top1_income": S["top1"][k], "top1_income_kg": S["top1_kg"][k], "income_year": 2022,
            "top1_wealth": w, "wealth_date": d, "q5q1": q5q1, "absmob1940": am[1940], "absmob1984": am[1984]}


def _crossing() -> dict:
    """Two ten-person societies with the same Gini whose Lorenz curves cross: in A four people are poor and six
    alike, in B one person is rich and nine alike."""
    from scipy.optimize import brentq

    a = np.array([0.2] * 4 + [1.0] * 6)

    def soc_b(t):
        return np.array([0.8] * 9 + [0.8 + t])
    ga = D.gini(a)
    t = brentq(lambda t: D.gini(soc_b(t)) - ga, 0.0, 30.0)
    b = soc_b(t)
    pa, La = D.lorenz(a)
    pb, Lb = D.lorenz(b)
    return {"a": a.tolist(), "b": b.tolist(), "gini": ga, "pa": pa.tolist(), "La": La.tolist(), "pb": pb.tolist(),
            "Lb": Lb.tolist(), "atk": {str(e): [D.atkinson(a, e), D.atkinson(b, e)] for e in (0.5, 1.0, 2.0)},
            "top10": [D.top_share(a, 0.1), D.top_share(b, 0.1)], "bottom10": [a[0] / a.sum(), b[0] / b.sum()],
            "var_log": [float(np.var(np.log(a))), float(np.var(np.log(b)))]}


def _island_sample():
    T = TRUTH["sample"]
    x = D.simulate_growth(T["n"], T["years"], T["nu"], T["sigma"], T["delta"], seed=T["seed"])
    return x / x.mean() * 60000.0  # in Island dollars, a mean of 60,000


def compute_measures() -> dict:
    x = _island_sample()
    M = D.measures(x, B=400, seed=40)
    p, L = D.lorenz(x)
    k = np.linspace(0, len(p) - 1, 201).astype(int)
    ede = {str(e): D.ede(x, e) for e in (0.0, 0.5, 1.0, 2.0, 4.0)}
    g = _annual("GINIALLRH")
    ys = sorted(g)
    N = data.opportunity("national")
    us_gini = D.gini(_a(N, "par_inc"))
    return {"n": len(x), "mean": float(x.mean()), "median": float(np.median(x)), "p": p[k].tolist(),
            "L": L[k].tolist(), "m": M, "ede": ede, "crossing": _crossing(), "census_years": ys,
            "census_gini": [g[y] for y in ys], "oi_gini": us_gini}


def compute_top() -> dict:
    S = data.saez()
    ys = S["year"]
    out = {"years": ys, "top10": S["top10"], "top1": S["top1"], "top01": S["top01"], "top1_kg": S["top1_kg"],
           "top10_kg": S["top10_kg"]}
    v10 = {y: v for y, v in zip(ys, S["top10"]) if np.isfinite(v)}
    v1 = dict(zip(ys, S["top1"]))
    out["min10"] = min(v10, key=v10.get)
    out["at"] = {str(y): {"top10": v10.get(y), "top1": v1[y]} for y in (1917, 1928, 1940, 1944, 1950, 1970, 1980,
                                                                        2000, 2007, 2012, 2019, 2022)}
    out["wid"] = {e: data.wid_top1(e) for e in WID_SHOWN}
    out["as"] = tables.AUTEN_SPLINTER_2024.data
    return out


def compute_pareto() -> dict:
    S = data.saez()
    ys, a1, a2 = [], [], []
    for y, s1, s01, s001 in zip(S["year"], S["top1"], S["top01"], S["top001"]):
        if np.isfinite(s1) and np.isfinite(s01):
            ys.append(y)
            a1.append(D.pareto_alpha(s1, s01, 0.01, 0.001))
            a2.append(D.pareto_alpha(s01, s001, 0.001, 0.0001))
    tails = {}
    for y in (1970, 2022):
        k = S["year"].index(y)
        ps = [0.10, 0.05, 0.01, 0.005, 0.001, 0.0001]
        sh = [S[c][k] for c in ("top10", "top5", "top1", "top05", "top01", "top001")]
        b = np.polyfit(np.log10(ps[2:]), np.log10(sh[2:]), 1)[0]
        tails[str(y)] = {"p": ps, "share": sh, "slope": float(b), "alpha": float(1 / (1 - b))}
    d1 = dict(zip(ys, a1))
    return {"years": ys, "alpha": a1, "alpha_top": a2, "tails": tails, "a1970": d1[1970], "a2022": d1[2022],
            "a1928": d1[1928], "amax_year": ys[int(np.argmax(a1))], "amax": float(max(a1))}


def compute_growth() -> dict:
    G = TRUTH["growth"]
    rng = np.random.default_rng(G["seed"])
    # five careers, sixty years, the high-volatility economy
    paths = []
    for _ in range(5):
        y, ys = 0.0, [0.0]
        for _t in range(60):
            y += G["nu"] + G["sigma1"] * rng.standard_normal()
            y = max(y, G["floor"])
            ys.append(y)
        paths.append(np.exp(ys).tolist())
    x = D.simulate_growth(G["n"], 300, G["nu"], G["sigma1"], G["delta"], seed=G["seed"])
    grid, surv = D.ccdf(x, 120)
    K = D.KFE(G["nu"], G["sigma1"], G["delta"], y_lo=G["floor"])
    p = K.stationary()
    xs = np.exp(K.y)
    sk = 1.0 - np.cumsum(p)
    zeta = D.zeta(G["nu"], G["sigma1"], G["delta"])
    k = len(x) // 100
    return {"paths": paths, "grid": grid.tolist(), "surv": surv.tolist(), "kfe_x": xs[::4].tolist(),
            "kfe_surv": sk[::4].tolist(), "zeta": zeta, "zeta0": D.zeta(G["nu"], G["sigma0"], G["delta"]),
            "hill": D.hill(x, k), "n": len(x), "top1_sim": D.top_share(x, 0.01), "top1_kfe": K.top_share(p, 0.01),
            "sigma0": G["sigma0"], "sigma1": G["sigma1"], "delta": G["delta"]}


def compute_speed() -> dict:
    G, T = TRUTH["growth"], TRUTH["types"]
    K0 = D.KFE(G["nu"], G["sigma0"], G["delta"], y_lo=G["floor"])
    p0 = K0.stationary()
    K1 = D.KFE(G["nu"], G["sigma1"], G["delta"], y_lo=G["floor"])
    pure = K1.path(p0, 80, dt=0.5, qs=(0.01,))
    Ka = D.KFE(T["nu_l"], T["sigma"], G["delta"], nu_h=T["nu_h0"], psi=T["psi"], q_h=T["q_h"], y_lo=G["floor"])
    pa = Ka.stationary()
    Kb = D.KFE(T["nu_l"], T["sigma"], G["delta"], nu_h=T["nu_h1"], psi=T["psi"], q_h=T["q_h"], y_lo=G["floor"])
    types = Kb.path(pa, 80, dt=0.5, qs=(0.01,))
    S = data.saez()
    us = [(y, v) for y, v in zip(S["year"], S["top1"]) if 1975 <= y <= 2022]
    return {"t": pure["t"], "pure": pure[0.01], "types": types[0.01],
            "pure_end": K1.top_share(K1.stationary(), 0.01), "types_end": Kb.top_share(Kb.stationary(), 0.01),
            "hl_pure": D.half_life(pure["t"], np.log(pure[0.01]), np.log(K1.top_share(K1.stationary(), 0.01))),
            "hl_types": D.half_life(types["t"], np.log(types[0.01]), np.log(Kb.top_share(Kb.stationary(), 0.01))),
            "us_years": [y for y, _ in us], "us_top1": [v for _, v in us],
            "zeta_h": [D.zeta(T["nu_h0"], T["sigma"], G["delta"] + T["psi"]),
                       D.zeta(T["nu_h1"], T["sigma"], G["delta"] + T["psi"])]}


def compute_wealth() -> dict:
    keys = {"top1": "WFRBST01134", "next9": "WFRBSN09161", "next40": "WFRBSN40188", "bottom50": "WFRBSB50215"}
    series = {k: data.fred(v) for k, v in keys.items()}
    dates = series["top1"]["date"]
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in dates]
    out = {"t": t, **{k: s["value"] for k, s in series.items()}}
    alpha = [D.pareto_alpha(a + b, a, 0.10, 0.01) for a, b in zip(out["top1"], out["next9"])]
    out["alpha"] = alpha
    out["first"] = {k: out[k][0] for k in keys} | {"date": dates[0], "alpha": alpha[0]}
    out["last"] = {k: out[k][-1] for k in keys} | {"date": dates[-1], "alpha": alpha[-1]}
    W = TRUTH["wealth"]
    rg = np.linspace(-0.01, 0.045, 56)
    z = [D.wealth_zeta(r, W["c"], W["sigma"], W["delta"]) for r in rg]
    out["rg"], out["zeta"] = rg.tolist(), z
    out["marks"] = {str(r): D.wealth_zeta(r, W["c"], W["sigma"], W["delta"]) for r in W["r_minus_g"]}
    out["forbes"] = tables.FORBES_400.data["alpha"]
    return out


def compute_kuznets() -> dict:
    K = TRUTH["kuznets"]
    s = np.linspace(0, 1, 41)
    r = D.kuznets(s, K["gap"], K["sd_a"], K["sd_m"], K["n"], K["seed"])
    k = int(np.argmax(r["gini"]))
    S = data.saez()
    ys = [y for y, v in zip(S["year"], S["top10"]) if np.isfinite(v)]
    v = [v for v in S["top10"] if np.isfinite(v)]
    return {**r, "peak_share": r["share"][k], "peak_gini": r["gini"][k], "years": ys, "top10": v,
            "top10_1928": v[ys.index(1928)], "top10_1970": v[ys.index(1970)], "top10_2022": v[ys.index(2022)]}


def compute_ige() -> dict:
    T = TRUTH["generations"]
    g = D.generations(T["n"], T["beta"], T["sd_perm"], T["sd_trans"], T["years"], T["seed"])
    rows = []
    for yrs in (1, 3, 5, 10, 15):
        b, se = D.ige(g["child"], g["parent_years"][:, :yrs].mean(axis=1))
        rows.append({"years": yrs, "ige": b, "se": se,
                     "theory": T["beta"] * D.attenuation(yrs, T["sd_perm"], T["sd_trans"])})
    perm = D.ige(g["child"], g["parent"])
    rank1 = D.rank_slope(g["child"], g["parent_years"][:, 0])
    rankp = D.rank_slope(g["child"], g["parent"])
    k = np.random.default_rng(1).choice(T["n"], 600, replace=False)
    N = data.opportunity("national")
    lp, lk = np.log(_a(N, "par_inc")), np.log(_a(N, "kid_inc"))
    m = slice(9, 90)
    binned = float(np.polyfit(lp[m], lk[m], 1)[0])
    xs = np.linspace(1, 16, 60)
    curve = [T["beta"] * D.attenuation(x, T["sd_perm"], T["sd_trans"]) for x in xs]
    return {"beta": T["beta"], "rows": rows, "curve_x": xs.tolist(), "curve_y": curve, "perm": perm[0],
            "perm_se": perm[1], "rank_one": rank1,
            "rank_perm": rankp, "scatter_p": g["parent_years"][k, 0].tolist(), "scatter_c": g["child"][k].tolist(),
            "binned_ige": binned, "studies": tables.IGE_STUDIES.data, "chetty": tables.CHETTY_2014.data}


def _wcorr(x, y, w):
    x, y, w = np.asarray(x, float), np.asarray(y, float), np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(w)
    x, y, w = x[m], y[m], w[m]
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    c = np.average((x - mx) * (y - my), weights=w)
    return float(c / np.sqrt(np.average((x - mx) ** 2, weights=w) * np.average((y - my) ** 2, weights=w)))


def compute_gatsby() -> dict:
    G = TRUTH["gatsby"]
    r = D.gatsby(G["returns"], G["lam"], G["sd_h"], G["sd_u"], G["n"], G["seed"])
    C = data.opportunity("cz")
    gini, rm, am, pop = _a(C, "gini99"), _a(C, "rm"), _a(C, "am"), _a(C, "pop2000")
    m = np.isfinite(gini) & np.isfinite(am) & np.isfinite(pop)
    b = np.polyfit(gini[m], am[m], 1, w=np.sqrt(pop[m]))
    return {**r, "lam": G["lam"], "cz_gini": gini[m].tolist(), "cz_am": am[m].tolist(), "cz_pop": pop[m].tolist(),
            "cz_n": int(m.sum()), "corr_rm": _wcorr(gini, rm, pop), "corr_am": _wcorr(gini, am, pop),
            "fit": b.tolist(), "corak": tables.IGE_STUDIES.data}


def compute_chetty() -> dict:
    N = data.opportunity("national")
    r = _a(N, "kid_rank")
    p = (np.arange(1, 101) - 0.5) / 100
    b = np.polyfit(p, r, 1)
    Q = np.array([[float(np.mean(_a(N, f"q{j}")[20 * i: 20 * i + 20])) for j in range(1, 6)] for i in range(5)])
    A = data.opportunity("absmob")
    coh = [int(c) for c in A["cohort"]]
    by = {c: [A[f"p{k}"][i] for k in range(1, 101)] for i, c in enumerate(coh)}
    return {"rank": r.tolist(), "slope": float(b[0]), "intercept": float(b[1]), "quint": Q.tolist(),
            "q5q1": float(Q[0, 4]), "q1q1": float(Q[0, 0]), "q5q5": float(Q[4, 4]), "q1q5": float(Q[4, 0]),
            "cohorts": coh, "absmob": A["mean"], "by1940": by[1940], "by1984": by[1984],
            "college_p1": N["college"][0], "college_p100": N["college"][99], "t": tables.CHETTY_2014.data}


def compute_places() -> dict:
    C = data.opportunity("cz")
    am, pop = _a(C, "am"), _a(C, "pop2000")
    m = np.isfinite(am)
    big = [i for i in np.argsort(-pop) if np.isfinite(am[i])][:50]
    big_sorted = sorted(big, key=lambda i: am[i])
    pick = big_sorted[:4] + big_sorted[-4:]
    names = [f"{C['name'][i]}, {C['state'][i]}" for i in pick]
    corrs = {}
    for k in ("single_mothers", "racial_seg", "income_seg", "gini99", "middle", "social_capital", "test_scores",
              "religious", "school_spend", "commute15", "frac_black", "foreign"):
        corrs[k] = _wcorr(_a(C, k), am, pop)
    q = _a(C, "q5q1")
    w = np.where(m, pop, 0)
    return {"am": am[m].tolist(), "pop": pop[m].tolist(), "n": int(m.sum()), "pick": names,
            "pick_am": [float(am[i]) for i in pick], "pick_q": [float(q[i]) for i in pick],
            "pick_pop": [float(pop[i]) for i in pick], "corrs": corrs,
            "am_p10": float(np.percentile(am[m], 10)), "am_p90": float(np.percentile(am[m], 90)),
            "am_mean": float(np.average(am[m], weights=w[m])), "places": tables.PLACES.data}


def compute_world() -> dict:
    first, last = 1980, 2023
    rows = {}
    for r in data.pwt():
        if first <= r["year"] <= last and np.isfinite(r["rgdpe"]) and np.isfinite(r["pop"]) and r["pop"] > 0:
            rows.setdefault(r["countrycode"], {})[r["year"]] = (r["rgdpe"] / r["pop"], r["pop"])
    keep = [c for c, v in rows.items() if all(y in v for y in range(first, last + 1))]
    out = {"years": list(range(first, last + 1)), "n": len(keep)}
    for name, drop in (("all", ()), ("no_china", ("CHN",)), ("no_china_india", ("CHN", "IND"))):
        cs = [c for c in keep if c not in drop]
        out[name] = [D.between_gini([rows[c][y][0] for c in cs], [rows[c][y][1] for c in cs])
                     for y in range(first, last + 1)]
    out["pop_share"] = float(sum(rows[c][last][1] for c in keep) / sum(v[last][1] for v in rows.values()
                                                                        if last in v))
    out["world_top1"] = data.wid_top1("World")
    for c in ("CHN", "IND", "USA"):
        out[c] = {"y1980": rows[c][first][0], "y2023": rows[c][last][0]}
    out["global"] = tables.GLOBAL.data
    return out


def compute_practice() -> dict:
    x = _island_sample()
    r = D.incidence(x, TRUTH["policy"]["tax"])
    M = D.measures(x, B=400, seed=41)
    small = x[np.random.default_rng(3).choice(len(x), 200, replace=False)]
    Ms = D.measures(small, B=400, seed=42)
    return {**r, "tax": TRUTH["policy"]["tax"], "gini": M["gini"], "gini_small": Ms["gini"], "n": len(x),
            "top1": M["top1"], "top1_small": Ms["top1"]}


def film_time(t: float, first: float = 1913.0, last: float = 2022.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    S = data.saez()
    ys, v = S["year"], S["top1"]
    k = int(np.argmin(v))
    return {"t": ys, "v": v, "times": [film_time(y) for y in ys], "low": v[k], "low_y": ys[k],
            "y1928": v[ys.index(1928)], "last": v[-1], "first": v[0]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=8, log=False, low=40, high=84)
    events = {"film_end": film_time(2022) + 6.0, "first": times[0], "low": film_time(f["low_y"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the share of income received by the top 1% of American tax units, 1913-2022 "
                               "(Piketty and Saez, updated), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ40").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "parade": compute_parade,
    "guess": compute_guess,
    "measures": compute_measures,
    "top": compute_top,
    "pareto": compute_pareto,
    "growth": compute_growth,
    "speed": compute_speed,
    "wealth": compute_wealth,
    "kuznets": compute_kuznets,
    "ige": compute_ige,
    "gatsby": compute_gatsby,
    "chetty": compute_chetty,
    "places": compute_places,
    "world": compute_world,
    "practice": compute_practice,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
