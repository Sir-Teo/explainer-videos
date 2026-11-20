"""Precompute every number in Part 43 of *Economics, Built* ("Measuring Market Power").

    python -m videos.economics.econ43.compute            # everything missing (about two minutes)
    python -m videos.economics.econ43.compute --force cars

Results are cached in ``.cache/econ43/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Berry, Levinsohn and Pakes's 2,217 cars from BLPestimatoR; from FRED, corporate profits
after tax and GDP; the tables of the FTC's cereal case, Nevo, Bain and Demsetz, Bresnahan and Lau, Lancaster,
McFadden and Berry, Berry, Levinsohn and Pakes, Petrin, Olley and Pakes, Levinsohn and Petrin, Ackerberg, Caves and
Frazer, Syverson, De Loecker and Warzynski, De Loecker, Eeckhout and Unger and their critics, Bresnahan and Reiss,
the Merger Guidelines, MillerCoors and Axtell).  Models: Agora's industrial organization (``agora.io``) with the
Island's Part 43 truths.

Items:
    scp          300 industries that all play Cournot: concentration against margins
    playit       the merger game: five brands in three nests, two proposed mergers
    conduct      Bresnahan's identification: parallel shifts against a rotation of demand
    logit        the red bus and the blue bus; diversion under logit and nested logit
    contraction  Berry's contraction in one market, step by step
    cars         the Island's car market: OLS, IV logit and BLP against the truth, over 40 Islands
    blpdata      Berry, Levinsohn and Pakes's cars: plain logit by OLS and by IV; elasticities and markups
    cereal       the Island's cereal aisle: margins under single-product, actual and joint ownership
    merger       a merger in the aisle: prices after, and the cost savings that would offset it
    newgood      the value of a new good: a clone under logit and nested logit
    plants       production functions: OLS, within and Ackerberg-Caves-Frazer against the truth
    dlw          markups from production data, with the right and the wrong output elasticity
    entry        Bresnahan and Reiss: thresholds from 400 towns
    film         the intermission's data film: corporate profits after tax over GDP, 1947-2026
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import io
from explainer.economics.data import tables

CACHE = Cache("econ43")
load = CACHE.load
TRUTH = island.truths(43)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def compute_scp() -> dict:
    S = io.scp(**TRUTH["scp"])
    hhi, pcm = np.array(S["hhi"]), np.array(S["pcm"])
    share, margin = np.array(S["share"]), np.array(S["margin"])
    rng = np.random.default_rng(43)
    pick = rng.choice(len(share), 400, replace=False)
    hi = hhi > np.median(hhi)
    return {"hhi": hhi.tolist(), "pcm": pcm.tolist(), "corr": S["corr"], "slope": S["slope"],
            "within_corr": S["within_corr"], "share": share[pick].tolist(), "margin": margin[pick].tolist(),
            "pcm_hi": float(pcm[hi].mean()), "pcm_lo": float(pcm[~hi].mean()), "hhi_med": float(np.median(hhi)),
            "bain": tables.BAIN_1951.data}


def _playit_market():
    P = TRUTH["playit"]
    q, mc, nests = np.array(P["quality"]), np.array(P["mc"]), np.array(P["nests"])

    def shares(p):
        return io.nested_shares(q - P["alpha"] * np.asarray(p, float), nests, P["sigma"])
    return P, q, mc, nests, shares


def compute_playit() -> dict:
    P, q, mc, nests, shares = _playit_market()
    owner = np.arange(5)
    p0 = io.bertrand(shares, mc, owner)
    s0 = shares(p0)
    cs0 = io.nested_surplus(q - p0, nests, P["sigma"], P["alpha"])
    out = {"names": P["names"], "nests": P["nests"], "p0": p0.tolist(), "s0": s0.tolist(), "mc": mc.tolist(),
           "inside": float(s0.sum()), "shares_inside": (s0 / s0.sum()).tolist()}
    for key in ("x", "y"):
        mg = list(P[key])
        r = io.merger(shares, p0, owner, mg)
        p1 = np.array(r["p1"])
        dp = np.array(r["dp"])
        cs1 = io.nested_surplus(q - p1, nests, P["sigma"], P["alpha"])
        out[key] = {"pair": mg, "dp": dp.tolist(), "merged": float(np.mean(dp[mg])), "avg": r["avg"],
                    "dhhi": r["dhhi"], "hhi0": r["hhi0"], "hhi1": r["hhi0"] + r["dhhi"],
                    "dcs": float(cs1 - cs0), "dcs_pct": float((cs1 - cs0) / cs0),
                    "share_pair": float(np.sum(s0[mg]) / s0.sum())}
    # diversion: when one brand's price rises, where do its lost buyers go?
    J = io.jacobian(shares, p0)
    out["diversion"] = [(-J[j] / J[j, j]).tolist() for j in range(5)]
    return out


def compute_conduct() -> dict:
    C = io.conduct(shifts=(0.0, 1.5, 3.0), rotations=(0.0, 0.5))
    return C


def compute_logit() -> dict:
    # the red bus and the blue bus: a car and a blue bus equally liked; a red bus identical to the blue one appears
    logit2 = io.logit_shares([0.0, 0.0]) / io.logit_shares([0.0, 0.0]).sum()
    logit3 = io.logit_shares([0.0, 0.0, 0.0]) / io.logit_shares([0.0, 0.0, 0.0]).sum()
    # nested logit: buses in one nest, sigma near one: the new bus splits the bus riders
    nest3 = io.nested_shares([0.0, 0.0, 0.0], [0, 1, 1], 0.95)
    nest3 = nest3 / nest3.sum()
    # diversion from Bran Buds under plain logit and the game's nested logit, at the same shares
    P, q, mc, nests, shares = _playit_market()
    G = compute_playit()
    p0 = np.array(G["p0"])
    s0 = shares(p0)
    j = 3
    plain = s0 / (1 - s0[j])
    plain[j] = 0.0
    outside_plain = (1 - s0.sum()) / (1 - s0[j])
    nested = np.array(G["diversion"][j])
    nested[j] = 0.0
    outside_nested = 1 - nested.sum()
    return {"logit2": logit2.tolist(), "logit3": logit3.tolist(), "nest3": nest3.tolist(),
            "plain": plain.tolist(), "outside_plain": float(outside_plain), "nested": nested.tolist(),
            "outside_nested": float(outside_nested), "from": j, "names": P["names"]}


def _cars(seed: int):
    T = TRUTH["cars"]
    return io.island_cars(T=T["T"], firms=T["firms"], per_firm=T["per_firm"], alpha=T["alpha"], sigma=T["sigma"],
                          seed=seed)


def compute_contraction() -> dict:
    C = _cars(TRUTH["cars"]["seed"])
    idx = C["t"] == 0
    tr = io.contraction_trace(C["share"][idx], C["price"][idx], C["nu"], C["sigma"])
    # the true mean utilities (the xi and characteristics planted), for comparison
    b = C["beta"]
    truth = b[0] + b[1] * C["size"][idx] + b[2] * C["power"][idx] + C["xi"][idx] - C["alpha"] * C["price"][idx]
    return {**tr, "truth": truth.tolist(), "share": C["share"][idx].tolist(), "price": C["price"][idx].tolist(),
            "err_start": float(np.max(np.abs(np.array(tr["start"]) - truth))),
            "err_end": float(np.max(np.abs(np.array(tr["delta"]) - truth)))}


def _estimate(C) -> dict:
    n = len(C["t"])
    share = C["share"]
    outshr = np.zeros(n)
    for m in np.unique(C["t"]):
        idx = C["t"] == m
        outshr[idx] = 1 - share[idx].sum()
    X = np.column_stack([C["size"], C["power"]])
    Zd = io.diff_instruments(C["t"], X)
    Z = np.column_stack([C["w"], Zd, Zd ** 2 / 100, C["w"] ** 2])
    ols = io.logit_ols(share, outshr, C["price"], X)
    iv = io.logit_iv(share, outshr, C["price"], X, Z)
    b = io.blp(share, C["t"], C["price"], X, Z, C["nu"], bounds=(0.0, 0.6))
    # own elasticities under each
    el = {"ols": io.own_elasticities_logit(ols["alpha"], C["price"], share),
          "iv": io.own_elasticities_logit(iv["alpha"], C["price"], share)}
    blp_own = np.zeros(n)
    for m in np.unique(C["t"]):
        idx = np.where(C["t"] == m)[0]
        p = C["price"][idx]
        mk = io.RCMarket(b["delta"][idx] + b["alpha"] * p, b["alpha"], b["sigma"], C["nu"])
        E = mk.jac(p) * p[:, None] / mk.shares(p)[None, :]
        blp_own[idx] = np.diag(E)
    el["blp"] = blp_own
    return {"ols": ols["alpha"], "iv": iv["alpha"], "F": iv["F"], "blp_alpha": b["alpha"], "blp_sigma": b["sigma"],
            "el": {k: float(np.median(v)) for k, v in el.items()}, "el_all": el}


def compute_cars() -> dict:
    T = TRUTH["cars"]
    C = _cars(T["seed"])
    first = _estimate(C)
    runs = []
    for s in range(T["runs"]):
        Cs = C if s == 0 else _cars(T["seed"] + s)
        r = first if s == 0 else _estimate(Cs)
        runs.append({"ols": r["ols"], "iv": r["iv"], "blp_alpha": r["blp_alpha"], "blp_sigma": r["blp_sigma"],
                     "el_ols": r["el"]["ols"], "el_iv": r["el"]["iv"], "el_blp": r["el"]["blp"],
                     "el_true": float(np.median(Cs["true_own"]))})
    R = {k: np.array([r[k] for r in runs]) for k in runs[0]}
    # one Island's scatter: true own elasticity against price, and the plain-logit IV line
    rng = np.random.default_rng(43)
    pick = rng.choice(len(C["price"]), 240, replace=False)
    return {"alpha": T["alpha"], "sigma": T["sigma"], "first": {k: v for k, v in first.items() if k != "el_all"},
            "runs": {k: v.tolist() for k, v in R.items()},
            "mean": {k: float(v.mean()) for k, v in R.items()}, "sd": {k: float(v.std()) for k, v in R.items()},
            "price": C["price"][pick].tolist(), "true_own": C["true_own"][pick].tolist(),
            "iv_own": first["el_all"]["iv"][pick].tolist(), "blp_own": first["el_all"]["blp"][pick].tolist(),
            "corr_w": float(np.corrcoef(C["w"], C["price"])[0, 1]),
            "corr_xi": float(np.corrcoef(C["xi"], C["price"])[0, 1])}


def compute_blpdata() -> dict:
    d = {k: np.asarray(v) for k, v in data.blp_cars().items()}
    X = np.column_stack([d["hpwt"], d["air"], d["mpg"], d["space"]])
    Z = io.blp_instruments(d["year"], d["firm"], X)
    ols = io.logit_ols(d["share"], d["outshr"], d["price"], X)
    iv = io.logit_iv(d["share"], d["outshr"], d["price"], X, Z)
    out = {"n": int(len(d["price"])), "years": [int(d["year"].min()), int(d["year"].max())],
           "price_med": float(np.median(d["price"])), "price_lo": float(np.quantile(d["price"], 0.05)),
           "price_hi": float(np.quantile(d["price"], 0.95))}
    for nm, r in (("ols", ols), ("iv", iv)):
        e = io.own_elasticities_logit(r["alpha"], d["price"], d["share"])
        L = io.logit_markups(r["alpha"], d["price"], d["share"], d["year"], d["firm"])
        out[nm] = {"alpha": r["alpha"], "inelastic": int(np.sum(np.abs(e) < 1)), "el_med": float(np.median(e)),
                   "lerner_med": float(np.median(L)), "markup_dollars_med": float(np.median(L * d["price"])),
                   "single_dollars": float(1 / r["alpha"])}
    out["iv"]["F"] = iv["F"]
    rng = np.random.default_rng(43)
    pick = rng.choice(len(d["price"]), 300, replace=False)
    Liv = io.logit_markups(iv["alpha"], d["price"], d["share"], d["year"], d["firm"])
    last = d["year"] == d["year"].max()
    out["y1990"] = {c: d[c][last].tolist() for c in ("hpwt", "space", "mpg", "price", "share", "air")}
    out["n1990"] = int(last.sum())
    out["scatter"] = {"price": d["price"][pick].tolist(),
                      "el_ols": io.own_elasticities_logit(ols["alpha"], d["price"], d["share"])[pick].tolist(),
                      "el_iv": io.own_elasticities_logit(iv["alpha"], d["price"], d["share"])[pick].tolist(),
                      "dollars_iv": (Liv * d["price"])[pick].tolist()}
    return out


def _cereal():
    T = TRUTH["cereal"]
    rng = np.random.default_rng(T["seed"])
    J = len(T["owner"])
    base = rng.normal(T["base_mean"], T["base_sd"], J)
    mc = np.exp(rng.normal(np.log(T["mc_median"]), T["mc_sd"], J))
    nu = np.random.default_rng(T["seed"] + 1).standard_normal(T["ns"])
    mk = io.RCMarket(base, T["alpha"], T["sigma"], nu)
    owner = np.array(T["owner"])
    return T, mk, mc, owner


def compute_cereal() -> dict:
    T, mk, mc, owner = _cereal()
    p = mk.bertrand(mc, owner)
    s = mk.shares(p)
    J = len(owner)
    true = (p - mc) / p
    im = io.implied_margins(mk.shares, p, {"single": np.arange(J), "actual": owner, "joint": np.zeros(J, int)})
    w = s / s.sum()

    def wavg(v):
        return float(np.sum(w * np.asarray(v)))
    firm_share = [float(s[owner == f].sum() / s.sum()) for f in np.unique(owner)]
    E = mk.jac(p) * p[:, None] / s[None, :]
    return {"p": p.tolist(), "s": s.tolist(), "mc": mc.tolist(), "owner": owner.tolist(), "true": true.tolist(),
            "implied": im, "avg": {k: wavg(v) for k, v in im.items()}, "true_avg": wavg(true),
            "firm_share": firm_share, "inside": float(s.sum()), "own_el": np.diag(E).tolist(),
            "own_el_med": float(np.median(np.diag(E))), "markup_med": float(np.median(p / mc))}


def compute_merger() -> dict:
    T, mk, mc, owner = _cereal()
    p = mk.bertrand(mc, owner)
    mg = list(T["merge"])
    r = io.merger(mk.shares, p, owner, mg)
    c = io.cmcr(mk.shares, p, owner, mg)
    firms = sorted({int(owner[j]) for j in mg})
    merged = np.isin(owner, firms)
    dp = np.array(r["dp"])
    return {"dp": dp.tolist(), "avg": r["avg"], "dhhi": r["dhhi"], "hhi0": r["hhi0"], "hhi1": r["hhi0"] + r["dhhi"],
            "merged": merged.tolist(), "dp_merged": float(np.mean(dp[merged])),
            "dp_rivals": float(np.mean(dp[~merged])), "cmcr": c.tolist(),
            "cmcr_merged": float(np.mean(c[merged])), "firms": firms,
            "share_merged": float(np.sum(np.array(r["s0"])[merged]) / np.sum(r["s0"]))}


def compute_newgood() -> dict:
    P, q, mc, nests, shares = _playit_market()
    G = compute_playit()
    p0 = np.array(G["p0"])
    d = q - P["alpha"] * p0
    j = 2  # Nut Clusters, cloned
    base = io.logit_surplus(d, P["alpha"])
    gain_logit = io.logit_surplus(np.r_[d, d[j]], P["alpha"]) - base
    sig = np.round(np.linspace(0.0, 0.98, 50), 3)
    gains = []
    for sg in sig:
        b = io.nested_surplus(d, nests, sg, P["alpha"])
        c = io.nested_surplus(np.r_[d, d[j]], np.r_[nests, nests[j]], sg, P["alpha"])
        gains.append(c - b)
    return {"logit": float(gain_logit), "sigma": sig.tolist(), "gains": gains, "price": float(p0[j]),
            "pct_logit": float(gain_logit / p0[j]), "at_game": float(gains[int(np.argmin(np.abs(sig - P["sigma"])))]),
            "game_sigma": P["sigma"], "minivan": tables.PETRIN_2002.data["year"]}


def compute_plants() -> dict:
    P = io.island_plants(**TRUTH["plants"])
    r = io.acf(P)
    y, l, k, i, om = (np.asarray(P[c]) for c in ("y", "l", "k", "i", "omega"))

    def dm(v):
        m = np.bincount(i, v) / np.bincount(i)
        return v - m[i]
    bw = np.linalg.lstsq(np.column_stack([dm(l), dm(k)]), dm(y), rcond=None)[0]
    last = P["t"] == P["t"].max()
    q90, q10 = np.quantile(om[last], 0.9), np.quantile(om[last], 0.1)
    rng = np.random.default_rng(43)
    pick = rng.choice(int(last.sum()), 300, replace=False)
    yl = (y - P["bk"] * k)[last][pick]
    return {**r, "within": {"bl": float(bw[0]), "bk": float(bw[1])}, "ratio": float(np.exp(q90 - q10)),
            "corr_l_omega": float(np.corrcoef(l, om)[0, 1]), "l": l[last][pick].tolist(), "yk": yl.tolist(),
            "omega": om[last][pick].tolist(), "syverson": tables.PRODUCTION_1996.data["ratio"]}


def compute_dlw() -> dict:
    D = TRUTH["dlw"]
    rng = np.random.default_rng(D["seed"])
    mu = D["median"] * np.exp(D["sd"] * rng.standard_normal(D["n"]))
    pl = load("plants")
    bl = TRUTH["plants"]["bl"]
    share = bl / mu                     # labour's share of revenue at each plant's markup
    est = {"truth": bl, "acf": pl["acf"]["bl"], "ols": pl["ols"]["bl"], "within": pl["within"]["bl"]}
    med = {k: float(np.median(v / share)) for k, v in est.items()}
    edges = np.linspace(0.6, 3.0, 49)
    hists = {k: np.histogram(v / share, edges)[0].tolist() for k, v in est.items()}
    return {"theta": est, "median": med, "share_med": float(np.median(share)), "edges": edges.tolist(),
            "hist": hists, "deu": tables.DLW_2012.data}


def compute_entry() -> dict:
    T = TRUTH["towns"]
    W = io.island_towns(n=T["n"], F=T["F"], sd=T["sd"], seed=T["seed"], margins=T["margins"])
    K = len(T["margins"])
    r = io.ordered_thresholds(W["pop"], W["n"], n_max=K)
    true_S = np.array(W["thresholds"])
    per = true_S / np.arange(1, K + 1)
    cour = io.entry_thresholds(K, 1.0, 1.0, "cournot")
    coll = io.entry_thresholds(K, 1.0, 1.0, "collusion")
    return {"pop": W["pop"], "n": W["n"], "true_S": true_S.tolist(), "true_per": per.tolist(),
            "true_ratio": (per[1:] / per[:-1]).tolist(), "est": r, "margins": T["margins"],
            "cournot_ratio": cour["ratio"], "collusion_ratio": coll["ratio"],
            "counts": np.bincount(np.array(W["n"]), minlength=K + 1).tolist()}


def _quarterly(series: str) -> dict:
    f = data.fred(series)
    return {d: v for d, v in zip(f["date"], f["value"]) if v is not None}


def film_time(t: float, first: float = 1947.0, last: float = 2026.5) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    cp, gdp = _quarterly("CPATAX"), _quarterly("GDP")
    ds = sorted(d for d in cp if d in gdp)
    ts = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in ds]
    v = [100 * cp[d] / gdp[d] for d in ds]

    def avg(a, b):
        return float(np.mean([x for t, x in zip(ts, v) if a <= t < b]))
    k = int(np.argmax(v))
    return {"t": ts, "v": v, "times": [film_time(t) for t in ts], "peak": v[k], "peak_t": ts[k],
            "low": float(np.min(v)), "first": v[0], "last": v[-1], "last_t": ts[-1],
            "m1980_2000": avg(1980, 2000), "m2010_2026": avg(2010, 2027), "m1950s": avg(1950, 1960)}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "peak": film_time(f["peak_t"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "corporate profits after tax (with inventory valuation and capital consumption "
                               "adjustments) as a percentage of GDP, quarterly, 1947-2026 (BEA, via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ43").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "scp": compute_scp,
    "playit": compute_playit,
    "conduct": compute_conduct,
    "logit": compute_logit,
    "contraction": compute_contraction,
    "cars": compute_cars,
    "blpdata": compute_blpdata,
    "cereal": compute_cereal,
    "merger": compute_merger,
    "newgood": compute_newgood,
    "plants": compute_plants,
    "dlw": compute_dlw,
    "entry": compute_entry,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
