"""Precompute every number in Part 46 of *Economics, Built* ("Development").

    python -m videos.economics.econ46.compute            # everything missing (about a minute)
    python -m videos.economics.econ46.compute --force trap

Results are cached in ``.cache/econ46/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Data: the Data Room
(``explainer.economics.data``: the World Bank's poverty headcounts at $3.00 a day and its agriculture shares; three
experiments as distributed in the R package causaldata: Thornton's HIV-results incentives in Malawi, Cai, de Janvry
and Sadoulet's weather insurance in China, Manacorda, Miguel and Vigorito's PANES households in Uruguay; the tables
of Part 46). Models: Agora's village (``agora.village``) with the Island's Part 46 truths.

Items:
    poverty     the share below $3.00 a day: the world, its regions, China and India (World Bank)
    aid         the aid budget: six programmes, three ways to spend ten million, and the best mix
    trap        the village's S-shaped capital map, its three steady states, households with and without transfers
    lewis       the dual economy: modern employment and the wage, before and after the turning point
    agrigap     the raw agricultural productivity gap by country, against GDP per head (World Bank)
    lender      the moneylender's rate, decomposed
    credit      a randomized microlender: take-up, the average effect on profits, quantile effects
    cash        a transfer's rounds of local spending and the multiplier
    panes       Uruguay's PANES at its eligibility cutoff: participation and support for the government
    grad        the graduation programme on the trap: assets after the transfer against assets a decade on
    inpres      a school-building programme: the difference-in-differences and the Wald estimate
    nets        the Island's clinic: the demand for bed nets by price, and who uses them
    thornton    Thornton's Malawi experiment: collecting HIV results by incentive and by distance
    worms       deworming randomized by school: the within-school comparison against the between-school one
    townsend    Townsend's test on villages that pool risk fully, partly, or not at all
    index       index insurance: the best cover as basis risk rises, with and without trust
    insure      Cai, de Janvry and Sadoulet's farmers: take-up by session, default, and friends' take-up
    fert        present-biased farmers: fertilizer adoption with no offer, an offer at harvest, the same offer
                later, and half-price fertilizer at planting
    mita        a historical boundary: consumption on either side, by regression discontinuity
    sites       twelve sites: estimates, shrinkage, and the interval for the next site
    target      an emergency transfer: the poorest missed by village, phone and registry targeting
    film        the intermission's data film: the share of the world below $3.00 a day, 1981-2024
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import village

CACHE = Cache("econ46")
load = CACHE.load
TRUTH = island.truths(46)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0

TECH = ("a_low", "a_high", "alpha", "fixed")


def _tech() -> dict:
    T = TRUTH["trap"]
    return {k: T[k] for k in TECH}


def compute_poverty() -> dict:
    p = data.wdi_poverty()
    out = {}
    for k, d in p.items():
        ys = [int(y) for y, v in zip(d["year"], d["value"]) if v is not None and np.isfinite(v)]
        vs = [float(v) for v in d["value"] if v is not None and np.isfinite(v)]
        out[k] = {"name": d["name"], "year": ys, "value": vs, "first": vs[0], "first_year": ys[0], "last": vs[-1],
                  "last_year": ys[-1]}
    return out


def compute_aid() -> dict:
    P = {k: tuple(v) for k, v in TRUTH["aid"].items()}
    budget = 10.0
    best = village.aid_allocate(P, budget=budget, step=0.05)
    first = max(P, key=lambda k: P[k][0])
    all_first = float(village.aid_benefit(budget, *P[first]))
    even = {k: budget / len(P) for k in P}
    tot_even = float(sum(village.aid_benefit(even[k], *P[k]) for k in P))
    marg = {k: float(P[k][0] * np.exp(-best["alloc"][k] / P[k][1])) for k in P}
    xs = np.linspace(0, 6, 61)
    curves = {k: village.aid_benefit(xs, *P[k]).tolist() for k in P}
    return {"programmes": list(P), "params": {k: list(v) for k, v in P.items()}, "budget": budget, "first": first,
            "all_first": all_first, "even": tot_even, "best": best["total"], "alloc": best["alloc"],
            "marginal_at_best": marg, "xs": xs.tolist(), "curves": curves}


def compute_trap() -> dict:
    T = TRUTH["trap"]
    tech = _tech()
    ss = village.trap_steady_states(s=T["s"], delta=T["delta"], **tech)
    k = np.linspace(0.5, 80, 400)
    kn = village.trap_next(k, s=T["s"], delta=T["delta"], **tech)
    f_low = tech["a_low"] * k ** tech["alpha"]
    f_high = tech["a_high"] * k ** tech["alpha"] - tech["fixed"]
    switch = float((tech["fixed"] / (tech["a_high"] - tech["a_low"])) ** (1 / tech["alpha"]))
    runs = {}
    cons = {}
    for tr in (0.0, 10.0, 20.0):
        h = village.trap_households(n=T["n"], T=T["T"], transfer=tr, k_mu=T["k_mu"], k_sd=T["k_sd"],
                                    shock_sd=T["shock_sd"], s=T["s"], delta=T["delta"], seed=T["seed"], **tech)
        P = h["paths"]
        pick = np.linspace(0, P.shape[1] - 1, 40).astype(int)
        order = np.argsort(P[0, pick])
        cons[tr] = (1 - T["s"]) * village.trap_output(P, **tech)
        runs[f"{tr:.0f}"] = {"paths": P[:, pick[order]].T.tolist(), "share_above_end": h["share_above_end"],
                             "start_above": h["start_above"], "crossed": float(np.mean(h["crossed"])),
                             "median_end": float(np.median(P[-1])), "mean_end": float(np.mean(P[-1]))}
    # consumption (1 - s) f(k) of the same households with and without a transfer of 10: the same draws, so the
    # difference is the transfer's effect, a year on and at the end
    eff = {f"{tr:.0f}": [float(cons[tr][t].mean() / cons[0.0][t].mean() - 1) for t in range(T["T"] + 1)]
           for tr in (10.0, 20.0)}
    return {"cons_effect": eff, "k": k.tolist(), "next": kn.tolist(), "f_low": f_low.tolist(),
            "f_high": f_high.tolist(),
            "low": ss["low"], "threshold": ss["threshold"], "high": ss["high"], "switch": switch, "runs": runs,
            "s": T["s"], "delta": T["delta"], "years": T["T"]}


def compute_lewis() -> dict:
    L = TRUTH["lewis"]
    r = village.lewis(**L)
    return r


def compute_agrigap() -> dict:
    rows = data.wdi_agriculture()
    g = village.agri_gap(rows)
    names = {r["code"]: r["country"] for r in rows}
    pick = {}
    for c in ("ETH", "IND", "CHN", "BRA", "USA", "MWI", "BGD", "NGA", "MEX", "IDN", "KEN"):
        if c in g["code"]:
            i = g["code"].index(c)
            pick[c] = {"name": names[c], "gap": g["gap"][i], "gdppc": g["gdppc"][i], "emp": g["emp"][i],
                       "va": g["va"][i]}
    gaps = np.array(g["gap"])
    return {**g, "n": len(g["code"]), "pick": pick, "mean_log": float(np.exp(np.mean(np.log(gaps))))}


def compute_lender() -> dict:
    r = village.moneylender(**TRUTH["lender"])
    return r


def compute_credit() -> dict:
    return village.microcredit_trial(**TRUTH["credit"], boot_reps=200)


def compute_cash() -> dict:
    C = TRUTH["cash"]
    return village.local_multiplier(**C)


def compute_panes() -> dict:
    d = data.panes()
    x = np.asarray(d["score"], float)
    out = {"n": int(len(x))}
    edges = np.linspace(-0.02, 0.02, 21)
    for key in ("support", "participation"):
        y = np.asarray(d[key], float)
        r = village.panes_rd(x, y)
        mids, means = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            s = (x >= lo) & (x < hi) & np.isfinite(y)
            if s.sum() > 5:
                mids.append(float((lo + hi) / 2))
                means.append(float(y[s].mean()))
        ok = np.isfinite(y)
        fit_in = np.polyfit(x[ok & (x < 0)], y[ok & (x < 0)], 1).tolist()
        fit_out = np.polyfit(x[ok & (x >= 0)], y[ok & (x >= 0)], 1).tolist()
        out[key] = {"jump": r["jump"], "se": r["se"], "mids": mids, "means": means, "fit_in": fit_in,
                    "fit_out": fit_out,
                    "below": float(np.nanmean(y[x < 0])), "above": float(np.nanmean(y[x >= 0]))}
    # the participation-scaled effect (a fuzzy design's Wald ratio)
    out["wald"] = out["support"]["jump"] / out["participation"]["jump"]
    return out


def compute_grad() -> dict:
    T = TRUTH["trap"]
    tech = _tech()
    h = village.trap_households(n=T["n"], T=T["T"], transfer=10.0, k_mu=T["k_mu"], k_sd=T["k_sd"],
                                shock_sd=T["shock_sd"], s=T["s"], delta=T["delta"], seed=T["seed"] + 1, **tech)
    P = h["paths"]
    after = P[0]
    end = P[-1]
    th = h["threshold"]
    bins = np.arange(10.0, 40.0, 2.5)
    mids, gain = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        s = (after >= lo) & (after < hi)
        if s.sum() > 30:
            mids.append(float((lo + hi) / 2))
            gain.append(float(np.median(end[s] - after[s])))
    rng = np.random.default_rng(3)
    pick = rng.choice(len(after), 600, replace=False)
    return {"after": after[pick].tolist(), "end": end[pick].tolist(), "threshold": th, "mids": mids, "gain": gain,
            "share_crossed": float(np.mean(after > th)), "share_above_end": h["share_above_end"]}


def compute_inpres() -> dict:
    return village.inpres(**TRUTH["inpres"])


def compute_nets() -> dict:
    N = TRUTH["nets"]
    d = village.net_demand(wtp_median=N["wtp_median"], wtp_sigma=N["wtp_sigma"], use=N["use"], seed=N["seed"])
    s = village.net_demand(wtp_median=N["wtp_median"], wtp_sigma=N["wtp_sigma"], use=N["use"], use_slope=0.3,
                           seed=N["seed"])
    d["drop"] = 1 - d["take"][-1] / d["take"][0]
    d["screening"] = s
    return d


def compute_thornton() -> dict:
    d = data.thornton_hiv()
    got = np.asarray(d["got"], float)
    inc = np.asarray(d["incentive"], float)
    dist = np.asarray(d["distance"], float)
    ok = np.isfinite(got) & np.isfinite(inc)
    got, inc, dist = got[ok], inc[ok], dist[ok]
    edges = [(0.0, 0.0), (0.01, 0.25), (0.25, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.01)]
    labels, rates, ns, mids = [], [], [], []
    for lo, hi in edges:
        s = (inc == 0) if hi == 0 else ((inc >= lo) & (inc < hi))
        labels.append("none" if hi == 0 else f"{lo:.2f}-{min(hi, 3.0):.2f}")
        rates.append(float(got[s].mean()))
        ns.append(int(s.sum()))
        mids.append(0.0 if hi == 0 else float(np.mean(inc[s])))
    dedges = [(0, 1), (1, 2), (2, 3), (3, 5)]
    drates, dns = [], []
    for lo, hi in dedges:
        s = (dist >= lo) & (dist < hi)
        drates.append(float(got[s].mean()))
        dns.append(int(s.sum()))
    any_ = inc > 0
    # a linear probability slope per dollar among those offered something
    b = np.polyfit(inc[any_], got[any_], 1)
    return {"n": int(len(got)), "none": float(got[~any_].mean()), "any": float(got[any_].mean()), "labels": labels,
            "rates": rates, "ns": ns, "mids": mids, "dist_edges": dedges, "dist_rates": drates, "dist_ns": dns,
            "slope": float(b[0]), "villages": int(len(set(np.asarray(d["village"])[ok].tolist())))}


def compute_worms() -> dict:
    W = TRUTH["worms"]
    out = village.deworming(**W)
    out["no_spill"] = village.deworming(**{**W, "spill": 0.0})
    return out


def compute_townsend() -> dict:
    R = TRUTH["risk"]
    rows = []
    for pooled in (0.0, 0.25, 0.5, 0.85, 1.0):
        t = village.townsend(pooled=pooled, villages=R["villages"], households=R["households"], T=R["T"],
                             seed=R["seed"])
        rows.append({"pooled": pooled, "within": t["within"], "raw": t["raw"]})
    main = village.townsend(pooled=R["pooled"], villages=R["villages"], households=R["households"], T=R["T"],
                            seed=R["seed"])
    return {"rows": rows, "main": main}


def compute_index() -> dict:
    I = TRUTH["index"]
    bases = np.linspace(0, 0.5, 26)
    out = {"basis": bases.tolist()}
    for nm, trust, load_ in (("trust", I["trust"], I["load"]), ("full", 1.0, I["load"]), ("fair", 1.0, 0.0)):
        out[nm] = [village.index_insurance(basis=b, trust=trust, load=load_, gamma=I["gamma"],
                                           p_drought=I["p_drought"], loss=I["loss"])["cover"] for b in bases]
    return out


def compute_insure() -> dict:
    d = data.insure_china()
    take = np.asarray(d["takeup"], float)
    inten = np.asarray(d["intensive"], float)
    dflt = np.asarray(d["default"], float)
    pre = np.asarray(d["pre_takeup"], float)
    ok = np.isfinite(take)
    out = {"n": int(ok.sum()), "takeup": float(np.mean(take[ok])), "villages": int(len(set(d["village"])))}
    for nm, v in (("intensive", inten), ("default", dflt)):
        s = ok & np.isfinite(v)
        p1, p0 = float(take[s & (v == 1)].mean()), float(take[s & (v == 0)].mean())
        n1, n0 = int((s & (v == 1)).sum()), int((s & (v == 0)).sum())
        out[nm] = {"one": p1, "zero": p0, "n1": n1, "n0": n0, "diff": p1 - p0,
                   "se": float(np.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0))}
    s = ok & np.isfinite(pre)
    qs = np.quantile(pre[s], [0, 1 / 3, 2 / 3, 1])
    bins = []
    for j, (lo, hi) in enumerate(zip(qs[:-1], qs[1:])):
        m = s & (pre >= lo) & ((pre < hi) if j < 2 else (pre <= hi))
        bins.append({"lo": float(lo), "hi": float(hi), "rate": float(take[m].mean()), "n": int(m.sum())})
    out["friends"] = bins
    b = np.polyfit(pre[s], take[s], 1)
    out["friends_slope"] = float(b[0])
    return out


def compute_fert() -> dict:
    F = TRUTH["fert"]
    r = village.fertilizer(**F)
    r["patient"] = village.fertilizer(**{**F, "beta_lo": 1.0})
    return r


def compute_mita() -> dict:
    return village.geo_rd(**TRUTH["mita"])


def compute_sites() -> dict:
    return village.sites(**TRUTH["sites"])


def compute_target() -> dict:
    return village.targeting(**TRUTH["target"])


def film_time(t: float, first: float = 1981.0, last: float = 2024.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    p = compute_poverty()
    w = p["WLD"]
    out = {"t": w["year"], "v": w["value"], "times": [film_time(t) for t in w["year"]]}
    for k in ("SSF", "SAS", "EAS"):
        out[k] = {"t": p[k]["year"], "v": p[k]["value"]}
    out.update(first=w["value"][0], last=w["value"][-1], first_year=w["year"][0], last_year=w["year"][-1])
    i90 = w["year"].index(1990) if 1990 in w["year"] else 0
    out["v1990"] = w["value"][i90]
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "y1990": film_time(1990),
              "y2010": film_time(2010)}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.4, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the share of the world's people below $3.00 a day (2021 PPP), 1981-2024 (World "
                               "Bank, World Development Indicators), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ46").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "poverty": compute_poverty,
    "aid": compute_aid,
    "trap": compute_trap,
    "lewis": compute_lewis,
    "agrigap": compute_agrigap,
    "lender": compute_lender,
    "credit": compute_credit,
    "cash": compute_cash,
    "panes": compute_panes,
    "grad": compute_grad,
    "inpres": compute_inpres,
    "nets": compute_nets,
    "thornton": compute_thornton,
    "worms": compute_worms,
    "townsend": compute_townsend,
    "index": compute_index,
    "insure": compute_insure,
    "fert": compute_fert,
    "mita": compute_mita,
    "sites": compute_sites,
    "target": compute_target,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
