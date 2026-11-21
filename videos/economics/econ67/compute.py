"""Precompute every number in Part 67 of *Economics, Built* ("The Next Economics").

    python -m videos.economics.econ67.compute            # everything missing (about a minute)
    python -m videos.economics.econ67.compute --force camel

Results are cached in ``.cache/econ67/<name>.json``; scenes call ``load(name)``.  Model: Agora's ``field`` module (a
simulated research field with true effects, specification search by design and a publication filter; replication;
Andrews and Kasy's selection model; a simulated meta-study; many analysts and the specification curve; Brock and
Hommes's heterogeneous-expectations market; the audit of the series' Dials).  Data: Reinhart and Rogoff's panel as
processed by Herndon, Ash and Pollin; the Jordà-Schularick-Taylor Macrohistory Database (Britain's public debt and
growth, 1870-2020); Hamermesh's tables of the top three journals, 1963-2011, and the replication studies' published
numbers (``data/tables.py``).

Items:
    camel       the simulated field's published z-statistics against the first tries of every study
    playit      six published results picked by rule, and whether each replicates
    replication the field replicated at 90% power: the rate, the shrinkage, both by the original z
    multiverse  Reinhart and Rogoff's question asked 48 ways: thresholds, weights, start years, exclusions
    designs     the field by research design: histograms, the caliper ratio, the selection model's estimate
    meta        a simulated minimum-wage-style meta-study: the funnel, the naive mean, Andrews and Kasy's correction
    forking     the chance of a false positive against the number of specifications tried; ten outcomes and three
                multiple-testing rules
    turn        Hamermesh's methods in the top journals, 1963-2011
    audit       the series' Dials: statuses, estimates, the widest spreads
    analysts    seven analysts on one dataset, and every one of 288 specifications
    abm         Brock and Hommes's market: the bifurcation diagram and three paths
    profession  Hamermesh's authors: women, the young, co-authorship
    machine     automated search: false positives up to a thousand specifications
    markets     Called it?: the prediction markets of Camerer et al. (2016) against the outcome
    film        the intermission's data film: Britain's public debt and growth, 1870-2020 (JST)
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import field as FD
from explainer.economics.data import tables

CACHE = Cache("econ67")
load = CACHE.load
TRUTH = {"camel": "the field is simulated: its true effects, search and filter are assumed (agora.field)",
         "meta": "the meta-study is simulated: the true elasticity is -0.01 (agora.field.meta_literature)",
         "analysts": "the dataset is simulated: the programme's effect by age is assumed (agora.field)"}
FIELD = {"n": 160000, "null_share": 0.3, "tau": 2.0, "publish_ns": 0.35}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1870.0, 2020.0)
BINS = np.round(np.arange(0, 6.01, 0.1), 2)


def film_time(year: float) -> float:
    a, b = FILM_YEARS
    return 2.0 + (year - a) / (b - a) * (FILM_SECONDS - 4.0)


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, np.str_):
        return str(x)
    return x


def _field():
    return FD.mixed_field(**FIELD)


def compute_camel() -> dict:
    M = _field()
    first = np.concatenate([FD.literature(n=FIELD["n"] // 4, search=h, seed=670 + k, null_share=FIELD["null_share"],
                                          tau=FIELD["tau"], publish_ns=FIELD["publish_ns"])["first"]
                            for k, h in enumerate(FD.DESIGNS.values())])
    z = M["z"]
    hp, _ = np.histogram(z, bins=BINS)
    hf, _ = np.histogram(first, bins=BINS)
    c = FD.caliper(z, width=0.2)
    c0 = FD.caliper(first, width=0.2)
    assert c["ratio"] > 2.5 and c0["ratio"] < 1.0, (c, c0)
    return _jsonable({"bins": BINS, "published": hp, "first": hf, "n_pub": len(z), "n_all": len(first),
                      "share_sig": float(np.mean(z >= 1.96)), "share_sig_first": float(np.mean(first >= 1.96)),
                      "caliper": c, "caliper_first": c0,
                      "scale": float(len(z) / len(first))})


def compute_playit() -> dict:
    M = _field()
    z, zt, des = M["z"], M["z_true"], M["design"]
    sig = np.nonzero(z >= 1.96)[0]
    order = sig[np.argsort(z[sig])]
    picks = [int(order[int(q * (len(order) - 1))]) for q in (1 / 12, 3 / 12, 5 / 12, 7 / 12, 9 / 12, 11 / 12)]
    rng = np.random.default_rng(6701)
    rows = []
    from scipy import stats

    zpow = stats.norm.ppf(0.9) + 1.96
    for i in picks:
        k = zpow / z[i]
        zr = zt[i] * k + rng.normal()
        rows.append({"design": str(des[i]), "z": float(z[i]), "p": float(2 * stats.norm.sf(z[i])),
                     "z_true": float(zt[i]), "rep_z": float(zr), "replicated": bool(zr >= 1.96),
                     "rep_effect": float(zr / k / z[i])})
    R = FD.replicate_by_z(M)
    return _jsonable({"rows": rows, "by_z": R["rows"], "rule": "the published significant results at the 1st, 3rd, "
                      "5th, 7th, 9th and 11th twelfths of their z-statistics"})


def compute_replication() -> dict:
    M = _field()
    R = FD.replicate(M)
    B = FD.replicate_by_z(M)
    C = tables.CAMERER_2016.data
    assert 0.5 < R["rate"] < 0.7 and 0.6 < R["ratio"] < 0.8, R
    return _jsonable({"rate": R["rate"], "ratio": R["ratio"], "n": R["n"], "by_z": B["rows"],
                      "camerer": C, "others": tables.REPLICATION_67.data})


def compute_multiverse() -> dict:
    R = data.rr_hap()
    c, y = np.array(R["country"]), np.array(R["year"], int)
    d, g = np.array(R["debtgdp"], float), np.array(R["growth"], float)
    ok = np.isfinite(d) & np.isfinite(g) & ~((c == "Italy") & (y < 1951))
    rows = []
    for thr in (60, 70, 80, 90, 100, 120):
        for weight in ("country", "pooled"):
            for start in (1946, 1950):
                for drop in (False, True):
                    m = ok & (y >= start)
                    if drop:                       # Reinhart and Rogoff's exclusions of early postwar years (Part 32)
                        m &= ~(((c == "New Zealand") & (y < 1950)) | ((c == "Australia") & (y < 1951))
                               | ((c == "Canada") & (y < 1951)))
                    hi, lo = m & (d > thr), m & (d <= thr)
                    if weight == "pooled":
                        gh, gl = g[hi].mean(), g[lo].mean()
                    else:
                        gh = np.mean([g[hi & (c == cc)].mean() for cc in np.unique(c[hi])])
                        gl = np.mean([g[lo & (c == cc)].mean() for cc in np.unique(c[lo])])
                    rows.append({"threshold": thr, "weight": weight, "start": start, "drop": drop,
                                 "above": float(gh), "below": float(gl), "gap": float(gh - gl),
                                 "n_above": int(hi.sum())})
    rows.sort(key=lambda r: r["gap"])
    gaps = np.array([r["gap"] for r in rows])
    return _jsonable({"rows": rows, "n": len(rows), "lo": gaps.min(), "hi": gaps.max(), "median": np.median(gaps),
                      "share_neg": float(np.mean(gaps < 0)), "published": {"above90_mean": -0.1, "hap": 2.2}})


def compute_designs() -> dict:
    M = _field()
    out = {}
    for d_, h in FD.DESIGNS.items():
        z = M["z"][M["design"] == d_]
        hist, _ = np.histogram(z, bins=BINS)
        cal = FD.caliper(z, width=0.2)
        sel = FD.selection_mle(z)
        out[d_] = {"search": h, "hist": hist, "caliper": cal, "beta": sel["beta"], "n": len(z)}
    b = [out[k]["beta"] for k in FD.DESIGNS]
    assert b[0] > b[2] > b[3] and b[1] > b[2], b
    return _jsonable({"designs": out, "order": list(FD.DESIGNS), "bins": BINS})


def compute_meta() -> dict:
    L = FD.meta_literature(theta=-0.01, tau=0.005, beta_ns=0.3, beta_pos=0.3)
    P = FD.pet(L["est"], L["se"])
    A = FD.ak_meta(L["est"], L["se"])
    rng = np.random.default_rng(6702)
    pub = set(zip(np.round(L["est"], 10), np.round(L["se"], 10)))
    miss = [(float(e), float(s)) for e, s in zip(L["all_est"], L["all_se"])
            if (round(float(e), 10), round(float(s), 10)) not in pub]
    sample = [miss[i] for i in rng.choice(len(miss), 500, replace=False)]
    assert abs(A["theta"] + 0.01) < 0.003 and P["mean"] < -0.014, (A, P)
    return _jsonable({"est": L["est"], "se": L["se"], "missing": sample, "theta": L["theta"], "tau": L["tau"],
                      "beta_ns": L["beta_ns"], "beta_pos": L["beta_pos"], "naive": P["mean"], "wmean": P["naive"],
                      "ak": A, "n": len(L["est"])})


def compute_forking() -> dict:
    tries = [1, 2, 3, 5, 10, 20, 50, 100]
    curves = {str(r): FD.false_positive(tries, r) for r in (0.3, 0.6, 0.9)}
    # ten outcomes, three with real effects (80% power each), under three rules
    rng = np.random.default_rng(6703)
    sims, m, real = 20000, 10, 3
    mu = np.zeros(m)
    mu[:real] = 2.8
    from scipy import stats

    z = mu + rng.normal(size=(sims, m))
    p = 2 * stats.norm.sf(np.abs(z))
    rules = {}
    rules["none"] = p < 0.05
    rules["Bonferroni"] = p < 0.05 / m
    ps = np.sort(p, axis=1)
    k = np.arange(1, m + 1)
    below = ps <= 0.05 * k / m
    kmax = np.where(below.any(axis=1), m - np.argmax(below[:, ::-1], axis=1), 0)
    thr = np.where(kmax > 0, 0.05 * kmax / m, -1)
    rules["Benjamini-Hochberg"] = p <= thr[:, None]
    tab = {}
    for name, rej in rules.items():
        fp = rej[:, real:].sum(axis=1)
        tp = rej[:, :real].sum(axis=1)
        tab[name] = {"any_false": float(np.mean(fp > 0)), "false": float(fp.mean()), "true": float(tp.mean())}
    assert abs(tab["none"]["any_false"] - (1 - 0.95 ** 7)) < 0.02, tab
    return _jsonable({"tries": tries, "curves": curves, "rules": tab, "m": m, "real": real})


def compute_turn() -> dict:
    H = tables.HAMERMESH_2013.data
    return _jsonable(H)


def compute_audit() -> dict:
    A = FD.dial_audit()
    from explainer.economics import dials

    parts = sorted({p for d in dials.DIALS.values() for p in d.parts})
    per_part = {p: sum(1 for d in dials.DIALS.values() if p in d.parts) for p in parts}
    most = sorted(A["rows"], key=lambda r: (-len(r["parts"]), r["key"]))[:6]
    return _jsonable({**A, "per_part": per_part, "most_visited": most})


def compute_analysts() -> dict:
    A = FD.many_analysts()
    C = FD.specification_curve()
    assert A["n_sizes"] == 7 and A["ratio"] > 1.5, A
    return _jsonable({**A, "curve": [{"est": r["est"], "se": r["se"], "treated": r["treated"],
                                      "ages": r["ages"]} for r in C["rows"]],
                      "n_specs": C["n_specs"], "share_sig": C["share_sig"], "curve_lo": C["lo"],
                      "curve_hi": C["hi"], "curve_median": C["median"]})


def compute_abm() -> dict:
    B = FD.brock_hommes(betas=np.linspace(0.05, 10.0, 240), T=1500, keep=60)
    paths = {str(b): FD.brock_hommes_path(beta=b, T=70) for b in (1.0, 4.0, 9.0)}
    x = np.array(B["x"])
    bb = np.array(B["beta"])
    distinct = {str(b): int(len(np.unique(np.round(x[np.isclose(bb, b0)], 3))))
                for b, b0 in ((1.0, B["betas"][np.argmin(abs(B["betas"] - 1.0))]),
                              (4.0, B["betas"][np.argmin(abs(B["betas"] - 4.0))]),
                              (9.0, B["betas"][np.argmin(abs(B["betas"] - 9.0))]))}
    n_star = (1.35 - 1) / (2 * 1.35)
    beta_flip = float(np.log(1 / n_star - 1))
    return _jsonable({"beta": B["beta"], "x": B["x"], "paths": paths, "distinct": distinct, "beta_flip": beta_flip,
                      "b_over_B": B["b_over_B"], "C": B["C"]})


def compute_profession() -> dict:
    return _jsonable(tables.HAMERMESH_2013.data)


def compute_machine() -> dict:
    tries = [1, 10, 100, 1000]
    return {"tries": tries, "fp": FD.false_positive(tries, 0.6, sims=4000)}


def compute_markets() -> dict:
    C = tables.CAMERER_2016.data
    assert abs(C["replicated"] / C["studies"] - C["rate"]) < 0.001
    return dict(C)


def compute_film() -> dict:
    J = data.jst()
    c = np.array(J["country"])
    y = np.array(J["year"], int)
    d = np.array(J["debtgdp"], float)
    gdp = np.array(J["rgdpmad"], float)
    m = c == "UK"
    yrs, debt, rg = y[m], 100 * d[m], gdp[m]
    growth = np.full(len(rg), np.nan)
    growth[1:] = 100 * (rg[1:] / rg[:-1] - 1)
    keep = (yrs >= FILM_YEARS[0]) & (yrs <= FILM_YEARS[1]) & np.isfinite(debt)
    yrs, debt, growth = yrs[keep], debt[keep], growth[keep]
    hi = (debt > 90) & np.isfinite(growth)
    lo = (debt <= 90) & np.isfinite(growth)
    k = int(np.argmax(debt))
    peace = hi & ~np.isin(yrs, list(range(1914, 1920)) + list(range(1939, 1947)))
    return _jsonable({"years": yrs, "debt": debt, "growth": growth, "t": [film_time(v) for v in yrs],
                      "peak": debt[k], "peak_year": yrs[k], "g_hi": growth[hi].mean(), "g_lo": growth[lo].mean(),
                      "n_hi": int(hi.sum()), "g_hi_peace": growth[peace].mean(), "n_hi_peace": int(peace.sum()),
                      "last": debt[-1], "last_year": yrs[-1]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    qt = [film_time(float(v)) for v in f["years"]]
    qv = np.array(f["debt"], float)
    mel = SC.data_melody(qv, MELODY_SECONDS, times=qt, act=12, log=False, low=40, high=82)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": qt[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.15, "hz": SC.hz(nn), "name": f"{x:.0f}%"}
                       for tt, nn, x in zip(qt, mel["notes"], qv)],
                meta={"label": "Britain's public debt as a share of GDP, 1870-2020 (Jordà-Schularick-Taylor "
                               "Macrohistory Database), as a tune that rises with the debt (computed)",
                      "kind": "synthesized"})
    ClipStore("econ67").save("intermission.melody", clip)
    return {"times": qt, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "camel": compute_camel,
    "playit": compute_playit,
    "replication": compute_replication,
    "multiverse": compute_multiverse,
    "designs": compute_designs,
    "meta": compute_meta,
    "forking": compute_forking,
    "turn": compute_turn,
    "audit": compute_audit,
    "analysts": compute_analysts,
    "abm": compute_abm,
    "profession": compute_profession,
    "machine": compute_machine,
    "markets": compute_markets,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
