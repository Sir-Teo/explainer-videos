"""Precompute every number in Part 36 of *Economics, Built* ("Trade II: Scale, Firms and Gravity").

    python -m videos.economics.econ36.compute            # everything missing (about a minute)
    python -m videos.economics.econ36.compute --force gravity

Results are cached in ``.cache/econ36/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: CEPII's Gravity database for 2019; FRED's US imports from and exports to China,
manufacturing employment, end-use trade, customs duties; the tables of Autor, Dorn and Hanson, Bernard and Jensen,
Fajgelbaum et al., Boehm et al., Xing and Detert, McCallum and Krugman).  Models: Agora's trade (``agora.trade``)
with the Island's Part 36 truths.

Items:
    web          the trade web of 2019 among twenty large economies
    intra        two-way trade: America's end-use categories in 1967 and 2025
    krugman      love of variety, scale and the home-market effect
    playit       Spain's exports to Portugal, Japan and Brazil, and what gravity predicts
    gravity      gravity on 2019 data: OLS and PPML with fixed effects; Germany's exports against distance
    firms        exporters are few and large: Bernard and Jensen, and the Island's firms
    melitz       Melitz's cutoffs, selection and the gain from opening
    ek           Eaton and Kortum: the shares by formula and by simulation
    ek_prices    Eaton and Kortum: the prices a buyer pays, by source (the same distribution)
    realloc      Melitz: each firm's sales with trade against alone, by productivity
    chain_va     a value chain's gross and value-added exports (Leontief inverse)
    gains_int    the gains formula with traded intermediate inputs
    hat          the gains from trade by the ACR formula and a counterfactual by hat algebra on 2019 trade
    china        the China shock: imports, manufacturing jobs, Autor, Dorn and Hanson, and the Island's zones
    tariffs      the 2018-19 tariffs and the 2025 ones
    chains       the iPhone's accounting
    film         the intermission's data film: America's imports of goods from China, 1985-2025
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import trade
from explainer.economics.data import tables

CACHE = Cache("econ36")
load = CACHE.load
TRUTH = island.truths(36)
FILM_SECONDS = 50.0

WEB = {"USA": (39, -98), "CHN": (35, 104), "JPN": (36, 138), "DEU": (51, 10), "IND": (21, 78), "GBR": (54, -2),
       "FRA": (46, 2), "ITA": (42, 12), "BRA": (-10, -52), "CAN": (56, -106), "KOR": (36, 128), "RUS": (60, 90),
       "AUS": (-25, 134), "ESP": (40, -4), "MEX": (23, -102), "IDN": (-2, 118), "NLD": (52, 5), "SAU": (24, 45),
       "TUR": (39, 35), "CHE": (47, 8)}


def _annual(key: str, how: str = "mean") -> dict:
    d = data.fred(key)
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(x[:4]), []).append(v)
    return {y: (float(np.sum(v)) if how == "sum" else float(np.mean(v))) for y, v in out.items()
            if how != "sum" or len(v) == 12}


def _grav():
    G = data.gravity()
    return {k: (np.array(v, float) if k not in ("iso3_o", "iso3_d") else np.array(v)) for k, v in G.items()}


def compute_web() -> dict:
    G = _grav()
    keep = np.isin(G["iso3_o"], list(WEB)) & np.isin(G["iso3_d"], list(WEB))
    pairs: dict = {}
    for o, d, x in zip(G["iso3_o"][keep], G["iso3_d"][keep], G["tradeflow_baci"][keep]):
        k = tuple(sorted((o, d)))
        pairs[k] = pairs.get(k, 0.0) + x
    top = sorted(pairs.items(), key=lambda kv: -kv[1])[:40]
    total = float(np.nansum(G["tradeflow_baci"])) / 1e6
    return {"nodes": {k: list(v) for k, v in WEB.items()}, "links": [[a, b, v / 1e6] for (a, b), v in top],
            "world_bn": total, "largest": [top[0][0][0], top[0][0][1], top[0][1] / 1e6]}


def compute_intra() -> dict:
    pairs = {"capital goods": ("A640RC1A027NBEA", "A650RC1A027NBEA"),
             "cars and parts": ("B641RC1A027NBEA", "B651RC1A027NBEA"),
             "consumer goods": ("A642RC1A027NBEA", "A652RC1A027NBEA")}
    out = {}
    for name, (xk, mk) in pairs.items():
        X, M = _annual(xk), _annual(mk)
        yrs = sorted(k for k in X if k in M)
        out[name] = {"years": yrs, "gl": [float(trade.grubel_lloyd(X[y], M[y])) for y in yrs],
                     "x2025": X[yrs[-1]], "m2025": M[yrs[-1]], "gl1967": float(trade.grubel_lloyd(X[1967], M[1967])),
                     "gl2025": float(trade.grubel_lloyd(X[yrs[-1]], M[yrs[-1]]))}
    return out


def compute_krugman() -> dict:
    K = TRUTH["krugman"]
    one = trade.krugman_variety(K["L"], K["f"], K["sigma"], 1)
    two = trade.krugman_variety(K["L"], K["f"], K["sigma"], 2)
    ten = trade.krugman_variety(K["L"], K["f"], K["sigma"], 10)
    s = np.linspace(0.3, 0.7, 41)
    hm = trade.home_market(s, K["phi"])
    return {"n": one["n_home"], "q": one["q"], "markup": one["price_markup"], "gain2": two["welfare_gain"],
            "gain10": ten["welfare_gain"], "s": s.tolist(), "hm": hm.tolist(), **K,
            "hm_55": float(trade.home_market([0.55], K["phi"])[0])}


def compute_playit() -> dict:
    G = _grav()
    pos = (G["tradeflow_baci"] > 0) & np.isfinite(G["gdp_o"]) & np.isfinite(G["gdp_d"]) & \
        np.isfinite(G["distw_harmonic"])
    X = np.column_stack([np.log(G["gdp_o"]), np.log(G["gdp_d"]), np.log(G["distw_harmonic"]), G["contig"],
                         G["comlang_off"]])
    ok = pos & np.all(np.isfinite(X), axis=1)
    R = trade.gravity_ols(G["tradeflow_baci"][ok], X[ok])
    out = {}
    for d in ("PRT", "JPN", "BRA"):
        i = np.where((G["iso3_o"] == "ESP") & (G["iso3_d"] == d))[0][0]
        pred = np.exp(R["const"] + X[i] @ R["beta"])
        out[d] = {"actual": float(G["tradeflow_baci"][i]) / 1e6, "pred": float(pred) / 1e6,
                  "gdp": float(G["gdp_d"][i]) / 1e9, "dist": float(G["distw_harmonic"][i])}
    return {"pairs": out, "options": ["Portugal", "Japan", "Brazil"]}


def compute_gravity() -> dict:
    G = _grav()
    ok = (np.isfinite(G["tradeflow_baci"]) & np.isfinite(G["gdp_o"]) & np.isfinite(G["gdp_d"]) &
          np.isfinite(G["distw_harmonic"]) & (G["distw_harmonic"] > 0) & np.isfinite(G["contig"]) &
          np.isfinite(G["comlang_off"]) & np.isfinite(G["fta_wto"]) & np.isfinite(G["col_dep_ever"]))
    names = ["log GDP of exporter", "log GDP of importer", "log distance", "shared border", "common language",
             "colonial tie", "trade agreement"]
    X = np.column_stack([np.log(G["gdp_o"]), np.log(G["gdp_d"]), np.log(G["distw_harmonic"]), G["contig"],
                         G["comlang_off"], G["col_dep_ever"], G["fta_wto"]])[ok]
    y = G["tradeflow_baci"][ok]
    R = trade.gravity_ols(y, X)
    o_codes = {c: i for i, c in enumerate(sorted(set(G["iso3_o"][ok])))}
    d_codes = {c: i for i, c in enumerate(sorted(set(G["iso3_d"][ok])))}
    o = np.array([o_codes[c] for c in G["iso3_o"][ok]])
    d = np.array([d_codes[c] for c in G["iso3_d"][ok]])
    P = trade.ppml_fe(y, X[:, 2:], o, d)
    # Germany's exports, divided by the partner's GDP, against distance
    de = ok & (G["iso3_o"] == "DEU") & (G["tradeflow_baci"] > 0)
    dist = G["distw_harmonic"][de]
    rel = G["tradeflow_baci"][de] / G["gdp_d"][de]
    slope = float(np.polyfit(np.log(dist), np.log(rel), 1)[0])
    M = tables.MCCALLUM_1995.data
    return {"names": names, "ols": R["beta"].tolist(), "ols_r2": R["r2"], "n": R["n"], "n_all": int(ok.sum()),
            "ppml": P["beta"].tolist(), "ppml_names": names[2:], "de_dist": dist.tolist(),
            "de_rel": (rel * 1000).tolist(), "de_slope": slope, "de_names": G["iso3_d"][de].tolist(),
            "mccallum": M["factor"], "zeros": float(np.mean(y == 0))}


def compute_firms() -> dict:
    Mt = TRUTH["melitz"]
    kw = {k: Mt[k] for k in ("sigma", "k", "f", "fx", "fe", "tau", "delta")}
    F = trade.melitz_firms(n=Mt["n"], seed=Mt["seed"], **kw)
    alive = F["alive_trade"]
    exp_ = F["exporter"] & alive
    BJ = tables.BERNARD_JENSEN_1995.data
    sales = F["sales"][alive]
    phi = F["phi"][alive]
    return {"n_alive": int(alive.sum()), "share_exporters": float(exp_.sum() / alive.sum()),
            "sales_share_exporters": float(F["sales"][exp_].sum() / F["sales"][alive].sum()),
            "size_ratio": float(F["sales"][exp_].mean() / F["sales"][alive & ~F["exporter"]].mean()),
            "prod_ratio": float(F["phi"][exp_].mean() / F["phi"][alive & ~F["exporter"]].mean()),
            "phi": phi.tolist(), "sales": sales.tolist(), "exporter": F["exporter"][alive].tolist(),
            "bj76": BJ["share_1976"], "bj87": BJ["share_1987"]}


def compute_melitz() -> dict:
    Mt = TRUTH["melitz"]
    kw = {k: Mt[k] for k in ("sigma", "k", "f", "fx", "fe", "tau", "delta")}
    M = trade.melitz(**kw)
    F = trade.melitz_firms(n=Mt["n"], seed=Mt["seed"], **kw)
    tau = np.linspace(1.0, 2.5, 31)
    gains = [trade.melitz(**{**kw, "tau": t})["welfare_gain"] for t in tau]
    exs = [trade.melitz(**{**kw, "tau": t})["export_share"] for t in tau]
    return {**{k: float(v) for k, v in M.items()}, "tau_grid": tau.tolist(), "gains": gains, "export_shares": exs,
            "phi_sample": np.sort(F["phi"])[::-1][:400].tolist(), **kw}


def compute_ek() -> dict:
    E = TRUTH["ek"]
    T, d = np.array(E["T"]), np.array(E["d"])
    w = np.ones(3)
    a = trade.eaton_kortum_shares(T, w, d, E["theta"])
    s = trade.eaton_kortum_simulate(T, w, d, E["theta"], E["goods"], E["seed"])
    return {"analytic": a.tolist(), "simulated": s.tolist(), "theta": E["theta"], "T": list(T),
            "max_gap": float(np.abs(a - s).max())}


def compute_ek_prices() -> dict:
    E = TRUTH["ek"]
    return trade.eaton_kortum_prices(E["T"], np.ones(3), E["d"], E["theta"], E["goods"], E["seed"], buyer=0)


def compute_realloc() -> dict:
    Mt = TRUTH["melitz"]
    kw = {k: Mt[k] for k in ("sigma", "k", "f", "fx", "fe", "tau", "delta")}
    M = trade.melitz(**kw)
    sig, tau = kw["sigma"], kw["tau"]
    phi = np.exp(np.linspace(0, np.log(4.0), 400))
    aut = np.where(phi >= M["phi_autarky"], (phi / M["phi_autarky"]) ** (sig - 1), 0.0)
    dom = np.where(phi >= M["phi_trade"], (phi / M["phi_trade"]) ** (sig - 1), 0.0)
    exp_ = np.where(phi >= M["phi_export"], dom * tau ** (1 - sig), 0.0)
    tot = dom + exp_
    with np.errstate(divide="ignore", invalid="ignore"):
        chg = np.where(aut > 0, tot / aut - 1, np.nan)
    k_mid = int(np.searchsorted(phi, (M["phi_trade"] + M["phi_export"]) / 2))
    k_top = int(np.searchsorted(phi, M["phi_export"] * 1.2))
    return {"phi": phi.tolist(), "change": chg.tolist(), "phi_a": M["phi_autarky"], "phi_t": M["phi_trade"],
            "phi_x": M["phi_export"], "shrink": float(chg[k_mid]), "grow": float(chg[k_top])}


def compute_chain_va() -> dict:
    C = TRUTH["chain"]
    return trade.value_added_trade(C["A"], C["exports"], names=("the Island", "the Archipelago", "the Far Isle"))


def compute_gains_int() -> dict:
    H = compute_hat()
    beta = TRUTH["intermediates"]
    lam = np.array(H["lambda"])
    # as in item hat: the real income lost by moving to autarky, 1 - lambda^(1/theta); with a share beta of costs in
    # traded intermediate inputs the exponent becomes 1/(theta (1 - beta))
    one = 1 - lam ** (1 / H["theta"])
    inter = 1 - lam ** (1 / (H["theta"] * (1 - beta)))
    return {"regions": H["regions"], "lambda": lam.tolist(), "one": one.tolist(), "inter": inter.tolist(),
            "beta": beta, "theta": H["theta"], "crc_lo": 2, "crc_hi": 8}


def compute_hat() -> dict:
    H = TRUTH["hat"]
    G = _grav()
    gdp = {}
    for c, v in zip(G["iso3_o"], G["gdp_o"]):
        if np.isfinite(v):
            gdp[c] = v
    top = sorted(gdp, key=gdp.get, reverse=True)[:H["n_top"]]
    regions = top + ["RoW"]
    idx = {c: i for i, c in enumerate(top)}
    N = len(regions)
    X = np.zeros((N, N))          # X[n, i]: spending by n on goods from i
    exports = np.zeros(N)
    for o, dd, x in zip(G["iso3_o"], G["iso3_d"], G["tradeflow_baci"]):
        if not np.isfinite(x) or o not in gdp or dd not in gdp:
            continue
        i, n = idx.get(o, N - 1), idx.get(dd, N - 1)
        if i == n:                 # within the rest of the world: counts as domestic
            continue
        X[n, i] += x
        exports[i] += x
    gdp_r = np.array([gdp[c] for c in top] + [sum(v for c, v in gdp.items() if c not in idx)])
    for n in range(N):
        X[n, n] = gdp_r[n] - exports[n]
    lam = np.diag(X) / X.sum(axis=1)
    acr = [trade.acr_gains(l_, H["theta"]) for l_ in lam]
    dh = np.ones((N, N))
    u, c = idx["USA"], idx["CHN"]
    dh[u, c] = dh[c, u] = H["rise"]
    R = trade.hat_algebra(X, dh, H["theta"])
    return {"regions": regions, "lambda": lam.tolist(), "acr": acr, "welfare": R["welfare"].tolist(),
            "w": R["w"].tolist(), "us_china_share_before": float(R["pi"][u, c]),
            "us_china_share_after": float(R["pi_new"][u, c]), **H}


def compute_china() -> dict:
    imp = _annual("IMPCH", "sum")
    exp_ = _annual("EXPCH", "sum")
    man = _annual("MANEMP")
    A = tables.ADH_2013.data
    S = trade.shift_share(**TRUTH["shock"])
    yrs = sorted(imp)
    return {"years": yrs, "imp_bn": [imp[y] / 1000 for y in yrs], "exp_bn": [exp_.get(y, np.nan) / 1000 for y in yrs],
            "man_y": sorted(man), "man": [man[y] / 1000 for y in sorted(man)], "imp1991": imp[1991] / 1000,
            "imp2007": imp[2007] / 1000, "imp_peak": max(imp.values()) / 1000, "imp_peak_y": max(imp, key=imp.get),
            "man2000": man[2000] / 1000, "man2010": man[2010] / 1000, **{f"adh_{k}": v for k, v in A.items()},
            "sim_ols": S["ols"], "sim_iv": S["iv"], "sim_beta": S["beta"], "sim_x": S["exposure"].tolist(),
            "sim_y": S["outcome"].tolist(), "sim_corr": S["corr_iv"]}


def compute_tariffs() -> dict:
    F = tables.FAJGELBAUM_2020.data
    duty, impg = _annual("B235RC1A027NBEA"), _annual("A255RC1A027NBEA")
    imp = _annual("IMPCH", "sum")
    rate = {y: 100 * duty[y] / impg[y] for y in duty if y in impg}
    return {**{k: v for k, v in F.items()}, "rate2017": rate[2017], "rate2019": rate[2019], "rate2024": rate[2024],
            "rate2025": rate[2025], "imp2018": imp[2018] / 1000, "imp2019": imp[2019] / 1000,
            "imp2024": imp[2024] / 1000, "imp2025": imp.get(2025, np.nan) / 1000 if 2025 in imp else None,
            "years": sorted(rate), "rate": [rate[y] for y in sorted(rate)], "peak_y": max(rate, key=rate.get),
            "peak": max(rate.values()), "since": max(y for y in rate if y < 2025 and rate[y] >= rate[2025])}


def compute_chains() -> dict:
    return dict(tables.XING_DETERT_2010.data)


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1985.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    imp = _annual("IMPCH", "sum")
    ys = sorted(y for y in imp if y >= 1985)
    v = [imp[y] / 1000 for y in ys]
    return {"t": ys, "v": v, "times": [film_time(y) for y in ys], "max": float(max(v)),
            "max_y": int(ys[int(np.argmax(v))]), "first": v[0], "last": v[-1], "last_y": ys[-1]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=7, log=True, low=40, high=86)
    events = {"film_end": film_time(f["last_y"]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"${x:.0f}bn"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "America's imports of goods from China, 1985-2025 (Census, via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ36").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "ek_prices": compute_ek_prices,
    "realloc": compute_realloc,
    "chain_va": compute_chain_va,
    "gains_int": compute_gains_int,
    "web": compute_web,
    "intra": compute_intra,
    "krugman": compute_krugman,
    "playit": compute_playit,
    "gravity": compute_gravity,
    "firms": compute_firms,
    "melitz": compute_melitz,
    "ek": compute_ek,
    "hat": compute_hat,
    "china": compute_china,
    "tariffs": compute_tariffs,
    "chains": compute_chains,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
