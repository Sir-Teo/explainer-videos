"""Precompute every number in Part 35 of *Economics, Built* ("Trade I: Comparative Advantage").

    python -m videos.economics.econ35.compute            # everything missing (a few seconds)
    python -m videos.economics.econ35.compute --force ho

Results are cached in ``.cache/econ35/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Jorda-Schularick-Taylor database's imports and exports since 1870; FRED's customs
duties, imports of goods, and exports and imports by end use; imports and GDP; Trefler's 1983 factor-content data;
the transcribed tables of Ricardo, Bernhofen and Brown, Leontief, Irwin, Goldberg and Maggi and others).  Models:
Agora's trade (``agora.trade``) with the Island's Part 35 truths.

Items:
    openness     trade (exports plus imports) over GDP since 1870: the median of the JST economies, Britain, the US
    playit       the Island and the Archipelago: four numbers, autarky, trade, gains
    ricardo      Ricardo's four numbers: autarky prices, the world price, gains, the wage band
    many         the chain of comparative advantage, and the DFS continuum with growth and shipping costs
    japan        Bernhofen and Brown's tables, and the gains from opening
    ho           the Heckscher-Ohlin world: autarky and trade, the Lerner diagram, Rybczynski
    stolper      Stolper-Samuelson: factor prices against the price of cloth
    leontief     Leontief's ratio, and Trefler's factor-content statistics recomputed
    specific     specific factors: the labour diagram and who gains from a rise in the price of food
    tariff       a small country's tariff and its triangles; a quota; a large country's optimal tariff
    politics     protection for sale on ten industries; Smoot-Hawley; trade's interwar collapse
    war          a tariff war: best responses, the Nash tariff, the payoff matrix
    compensation who gains and who loses when the Island opens, and whether the winners could pay
    dials        the gains from trade for the United States by the ACR formula
    facts        two-way trade: the Grubel-Lloyd index for America's capital goods, cars and consumer goods
    film         the intermission's data film: America's average tariff on imported goods since 1929
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import trade
from explainer.economics.data import tables

CACHE = Cache("econ35")
load = CACHE.load
TRUTH = island.truths(35)
FILM_SECONDS = 50.0


def _annual(key: str) -> dict:
    d = data.fred(key)
    return {int(x[:4]): v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def compute_openness() -> dict:
    D = data.jst()
    iso, yr = np.array(D["iso"]), np.array(D["year"], int)
    with np.errstate(divide="ignore", invalid="ignore"):
        op = 100 * (np.array(D["imports"], float) + np.array(D["exports"], float)) / np.array(D["gdp"], float)
    years = list(range(1870, 2021))
    med = []
    for y in years:
        v = op[(yr == y) & np.isfinite(op)]
        med.append(float(np.median(v)) if len(v) >= 10 else float("nan"))
    def one(c):  # noqa: E306
        m = (iso == c)
        return {int(y): float(v) for y, v in zip(yr[m], op[m]) if np.isfinite(v)}
    gb, us = one("GBR"), one("USA")
    md = dict(zip(years, med))
    return {"years": years, "median": med, "gbr_y": sorted(gb), "gbr": [gb[y] for y in sorted(gb)],
            "usa_y": sorted(us), "usa": [us[y] for y in sorted(us)],
            "m1913": md[1913], "m1932": min(md[y] for y in range(1929, 1939)), "m1932_y": int(min(range(1929, 1939),
                                                                                                   key=md.get)),
            "m1870": md[1870], "m2019": md[2019], "us1929": us[1929], "us1932": us[1932], "us2019": us[2019]}


def compute_playit() -> dict:
    P = TRUTH["playit"]
    R = trade.ricardo_trade(P["island"], P["arch"], P["L_island"], P["L_arch"], P["beta"])
    I, A = R["H"], R["F"]
    return {**P, "hours_island": P["island"], "hours_arch": P["arch"], "p": R["p"], "pI": R["pH"], "pA": R["pF"],
            "island": {k: I[k] for k in ("q1", "q2", "c1", "c2", "gain", "w1", "w2")},
            "arch": {k: A[k] for k in ("q1", "q2", "c1", "c2", "gain", "w1", "w2")},
            "aut_island": {k: I["autarky"][k] for k in ("q1", "q2", "c1", "c2")},
            "aut_arch": {k: A["autarky"][k] for k in ("q1", "q2", "c1", "c2")},
            "wage_ratio": R["wage_ratio"],
            "options": ["the Archipelago makes both", "the Island makes cloth", "the Island makes fish"]}


def compute_ricardo() -> dict:
    T = tables.RICARDO_1817.data
    R0 = TRUTH["ricardo"]
    aE = (T["England"]["cloth"], T["England"]["wine"])
    aP = (T["Portugal"]["cloth"], T["Portugal"]["wine"])
    R = trade.ricardo_trade(aE, aP, R0["L_england"], R0["L_portugal"], R0["beta"])
    S = trade.ricardo_world_supply(aE, aP, R0["L_england"], R0["L_portugal"])
    # world relative demand for wine (good 2) over cloth: Q2/Q1 = (1 - b)/b / p
    ps = np.linspace(0.6, 1.6, 101)
    rd = (1 - R0["beta"]) / R0["beta"] / ps
    return {"aE": aE, "aP": aP, "pE": aE[1] / aE[0], "pP": aP[1] / aP[0], "p": R["p"],
            "gain_E": R["F"]["gain"], "gain_P": R["H"]["gain"], "wage_ratio": 1 / R["wage_ratio"],
            "wage_lo": aE[0] / aP[0], "wage_hi": aE[1] / aP[1], "supply": S, "ps": ps.tolist(), "rd": rd.tolist(),
            "saving_E": aE[1] - aE[0] * R["p"], "saving_P": aP[0] - aP[1] / R["p"]}


def compute_many() -> dict:
    D = TRUTH["dfs"]
    n = D["n"]
    z = (np.arange(n) + 0.5) / n
    A = D["level"] * np.exp(D["k"] * (1 - 2 * z))
    free = trade.dfs(A, L=D["L"], Lf=D["Lf"])
    ship = trade.dfs(A, L=D["L"], Lf=D["Lf"], g=D["g"])
    grow = trade.dfs(A, L=D["L"], Lf=D["Lf"] * D["growth"])
    # the chain: ten goods drawn from the continuum
    idx = np.linspace(0, n - 1, 10).astype(int)
    return {"z": z.tolist(), "A": A.tolist(), "B": trade.dfs_demand(z, D["L"], D["Lf"]).tolist(),
            "B_grow": trade.dfs_demand(z, D["L"], D["Lf"] * D["growth"]).tolist(),
            "free": {"omega": free["omega"], "zbar": free["share_home"]},
            "ship": {"omega": ship["omega"], "zH": ship["zH"], "zF": ship["zF"],
                     "nontraded": float(ship["nontraded"].mean())},
            "grow": {"omega": grow["omega"], "zbar": grow["share_home"]},
            "chain_A": A[idx].tolist(), "chain_home": (free["omega"] < A[idx]).tolist(), **D}


def compute_japan() -> dict:
    B = tables.BERNHOFEN_BROWN_2004.data
    G = tables.BERNHOFEN_BROWN_2005.data
    Irw = tables.IRWIN_2005.data
    rows = ("imports_observed", "woolens", "imports_approx", "exports_observed", "exports_approx")
    tot = [sum(B[r][k] for r in rows) for k in range(len(B["years"]))]
    return {"years": list(B["years"]), "total": list(B["total"]), "recomputed": tot,
            "imports": sorted(B["imports"].items(), key=lambda kv: -kv[1]),
            "exports": sorted(B["exports"].items(), key=lambda kv: -kv[1]),
            "imp_obs": list(B["imports_observed"]), "exp_obs": list(B["exports_observed"]),
            "gain_lo": G["upper_bound_lo"], "gain_hi": G["upper_bound_hi"], "embargo": Irw["cost"],
            "embargo_trade": Irw["trade_share"], "negative": int(sum(t < 0 for t in B["total"]))}


def compute_ho() -> dict:
    H = TRUTH["ho"]
    al = H["alphas"]
    W = trade.ho_world(al, {"island": H["island"], "arch": H["arch"]}, H["beta"])
    out = {"alphas": al, "beta": H["beta"], "p": W["p"], "w": W["island"]["w"], "r": W["island"]["r"]}
    for k in ("island", "arch"):
        a = trade.ho_autarky(al, *H[k], H["beta"])
        out[k] = {"L": H[k][0], "K": H[k][1], "Q": W[k]["Q"].tolist(), "X": W[k]["X"].tolist(),
                  "aut_p": a["p"], "aut_w": a["w"], "aut_r": a["r"], "aut_Q": a["Q"].tolist(),
                  "diversified": W[k]["diversified"]}
    w, r = W["island"]["w"], W["island"]["r"]
    iso = {}
    for i, (a, pr) in enumerate(zip(al, (1.0, W["p"]))):
        Ls, Ks, star = trade.unit_value_isoquant(a, pr, w, r)
        iso[f"good{i + 1}"] = {"L": Ls.tolist(), "K": Ks.tolist(), "star": list(star)}
    out["iso"] = iso
    out["isocost"] = {"L0": 1 / w, "K0": 1 / r}
    out["kL"] = W["island"]["kL"].tolist()
    ry = trade.rybczynski(al, (1.0, W["p"]), *H["arch"], 0.10)
    out["rybczynski"] = {"dQ": ry["dQ"].tolist()}
    return out


def compute_stolper() -> dict:
    H = TRUTH["ho"]
    al = H["alphas"]
    p2 = load("ho")["p"]
    ss = trade.stolper_samuelson(al, (1.0, p2), 0.10, 0)
    grid = np.linspace(0.7, 1.4, 71)                     # the price of cloth, machines' price fixed
    fp = [trade.ho_factor_prices(al, (g, p2)) for g in grid]
    return {"dw": ss["dw"], "dr": ss["dr"], "dp": ss["dp"], "grid": grid.tolist(), "w": [f["w"] for f in fp],
            "r": [f["r"] for f in fp], "p2": p2,
            "real_w": [ss["dw"] - 0.10, ss["dw"]], "real_r": [ss["dr"] - 0.10, ss["dr"]]}


def compute_leontief() -> dict:
    Lt = tables.LEONTIEF_1953.data
    R = trade.leontief_ratio(Lt["exports"], Lt["imports"])
    F = trade.factor_content(data.trefler())
    Tr = tables.TREFLER_1995.data
    keep = np.abs(F["predicted"]) < 8
    return {"k_exports": R["exports"], "k_imports": R["imports"], "ratio": R["ratio"], **Lt,
            "sign_test": F["sign_test"], "variance_ratio": F["variance_ratio"], "rank": F["rank"],
            "measured": F["measured"][keep].tolist(), "predicted": F["predicted"][keep].tolist(),
            "factor": [f for f, k in zip(F["factor"], keep) if k], "n_shown": int(keep.sum()),
            "n_points": len(F["measured"]), "by_factor": F["by_factor"], "paper_sign": Tr["sign_test"],
            "paper_variance": Tr["variance_ratio"], "n_countries": F["n_countries"], "n_factors": F["n_factors"]}


def compute_specific() -> dict:
    S = TRUTH["specific"]
    kw = {k: S[k] for k in ("L", "K", "T", "theta")}
    c = trade.specific_change(S["pM"], S["pA"], S["dpA"], **kw)
    v0 = trade.vmpl_curves(S["pM"], S["pA"], **kw)
    v1 = trade.vmpl_curves(S["pM"], S["pA"] * (1 + S["dpA"]), **kw)
    return {"dw": c["dw"], "drK": c["drK"], "drT": c["drT"], "dpA": S["dpA"], "dLM": c["dLM"],
            "LM0": c["before"]["LM"], "LM1": c["after"]["LM"], "w0": c["before"]["w"], "w1": c["after"]["w"],
            "curve_L": v0["LM"].tolist(), "vM": v0["vM"].tolist(), "vA0": v0["vA"].tolist(), "vA1": v1["vA"].tolist(),
            "L": S["L"]}


def compute_tariff() -> dict:
    t = TRUTH["tariff"]
    sm = trade.tariff_small(t["a"], t["b"], t["c"], t["d"], t["pw"], t["t"])
    q = trade.quota_equivalent(t["a"], t["b"], t["c"], t["d"], t["pw"], sm["M1"])
    op = trade.optimal_tariff(t["a"], t["b"], t["c"], t["d"], t["e"], t["f"])
    grid = np.linspace(0, 2.5, 51)
    wel = [trade.tariff_large(t["a"], t["b"], t["c"], t["d"], t["e"], t["f"], x)["welfare"] for x in grid]
    one = trade.tariff_large(t["a"], t["b"], t["c"], t["d"], t["e"], t["f"], t["t"])
    return {**t, "small": sm, "quota": q, "opt_t": op["t"], "opt_av": op["ad_valorem"],
            "opt_inv": op["inverse_elasticity"],
            "opt_welfare": op["welfare"], "opt_pw": op["p_world"], "grid": grid.tolist(), "welfare": wel,
            "large_t1": {k: one[k] for k in ("p_world", "p_home", "welfare", "tot_gain", "M", "revenue")},
            "prohibitive": float(grid[int(np.argmax(np.array(wel) < -1e-9))]) if min(wel) < 0 else None}


def compute_politics() -> dict:
    G = TRUTH["gh"]
    rng = np.random.default_rng(G["seed"])
    n = G["n"]
    z = rng.uniform(0.5, 6.0, n)          # output over imports
    e = rng.uniform(1.0, 3.0, n)          # import demand elasticity
    org = np.array(G["organized"], int)
    t = trade.protection_for_sale(z, e, org, G["a"], G["alpha_L"])
    t5 = trade.protection_for_sale(z, e, org, 5.0, G["alpha_L"])
    S = tables.IRWIN_SMOOT_HAWLEY.data["dutiable"]
    GM = tables.GOLDBERG_MAGGI_1999.data
    return {"z": z.tolist(), "e": e.tolist(), "organized": org.tolist(), "t": t.tolist(), "t_a5": t5.tolist(),
            "a": G["a"], "alpha_L": G["alpha_L"], "smoot": {str(k): v for k, v in S.items()},
            "gm_lo": GM["weight_lo"], "gm_hi": GM["weight_hi"],
            "max_org": float(t[org == 1].max()), "min_unorg": float(t[org == 0].min()),
            "max_org5": float(t5[org == 1].max())}


def compute_war() -> dict:
    W = trade.tariff_war(**TRUTH["war"])
    return {"nash": W["nash"], "grid": W["grid"], "br": W["best_response"],
            "pay": {f"{i}|{j}": list(v) for (i, j), v in W["payoffs"].items()},
            "prohibitive": trade.prohibitive(TRUTH["war"]["A"], TRUTH["war"]["b_lo"], TRUTH["war"]["b_hi"])}


def compute_compensation() -> dict:
    """The Island opens and the price of food falls 20% (it imports food): real incomes by group, measured with a
    Cobb-Douglas price index (half on each good)."""
    S = TRUTH["specific"]
    kw = {k: S[k] for k in ("L", "K", "T", "theta")}
    a = trade.specific_factors(S["pM"], S["pA"], **kw)
    b = trade.specific_factors(S["pM"], S["pA"] * 0.8, **kw)
    P0, P1 = 1.0, (S["pM"] * S["pA"] * 0.8) ** 0.5 / (S["pM"] * S["pA"]) ** 0.5
    groups = {"workers": (a["w"] * S["L"], b["w"] * S["L"]), "capital": (a["rK"] * S["K"], b["rK"] * S["K"]),
              "land": (a["rT"] * S["T"], b["rT"] * S["T"])}
    real = {g: (x1 / P1) / (x0 / P0) - 1 for g, (x0, x1) in groups.items()}
    money = {g: x1 / P1 - x0 / P0 for g, (x0, x1) in groups.items()}
    # the national gain: income at the new prices can buy more, since consumption can now differ from production
    total = sum(x1 for _, x1 in groups.values()) / P1 - sum(x0 for x0, _ in groups.values()) / P0
    T = tables.TAA.data
    return {"real": real, "money": money, "total": total, "winners": sum(v for v in money.values() if v > 0),
            "losers": -sum(v for v in money.values() if v < 0), "food_fall": 0.20, **{f"taa_{k}": v for k, v in
                                                                                      T.items()}}


def compute_dials() -> dict:
    M, Y = _annual("IMPGSA"), _annual("GDPA")
    yrs = sorted(k for k in M if k in Y)
    last = yrs[-1]
    share = M[last] / Y[last]
    lam = 1 - share
    A = tables.ACR_2012.data
    return {"year": last, "import_share": share, "lambda": lam, "gain5": trade.acr_gains(lam, 5.0),
            "gain10": trade.acr_gains(lam, 10.0), "acr_lambda": A["lambda"],
            "acr5": trade.acr_gains(A["lambda"], 5.0), "acr10": trade.acr_gains(A["lambda"], 10.0),
            "share_series_y": yrs, "share_series": [100 * M[y] / Y[y] for y in yrs]}


def compute_facts() -> dict:
    pairs = {"capital goods": ("A640RC1A027NBEA", "A650RC1A027NBEA"),
             "cars and parts": ("B641RC1A027NBEA", "B651RC1A027NBEA"),
             "consumer goods": ("A642RC1A027NBEA", "A652RC1A027NBEA")}
    out = {}
    for name, (xk, mk) in pairs.items():
        X, M = _annual(xk), _annual(mk)
        last = max(k for k in X if k in M)
        out[name] = {"x": X[last], "m": M[last], "gl": float(trade.grubel_lloyd(X[last], M[last])),
                     "x1967": X[1967], "m1967": M[1967], "gl1967": float(trade.grubel_lloyd(X[1967], M[1967])),
                     "year": last}
    return out


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1929.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    duty, imp = _annual("B235RC1A027NBEA"), _annual("A255RC1A027NBEA")
    ys = sorted(k for k in duty if k in imp)
    v = [100 * duty[y] / imp[y] for y in ys]
    d = dict(zip(ys, v))
    return {"t": ys, "v": v, "times": [film_time(y) for y in ys], "max": float(max(v)),
            "max_y": int(ys[int(np.argmax(v))]),
            "min": float(min(v)), "min_y": int(ys[int(np.argmin(v))]), "v1929": d[1929], "v2024": d[2024],
            "v2025": d[2025], "last": ys[-1]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=7, log=True, low=40, high=86)
    events = {"film_end": film_time(2025) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.4, "hz": score.hz(nn), "name": f"{x:.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "America's customs duties as a share of goods imports, 1929-2025 (BEA, via FRED), as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ35").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "openness": compute_openness,
    "playit": compute_playit,
    "ricardo": compute_ricardo,
    "many": compute_many,
    "japan": compute_japan,
    "ho": compute_ho,
    "stolper": compute_stolper,
    "leontief": compute_leontief,
    "specific": compute_specific,
    "tariff": compute_tariff,
    "politics": compute_politics,
    "war": compute_war,
    "compensation": compute_compensation,
    "dials": compute_dials,
    "facts": compute_facts,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
