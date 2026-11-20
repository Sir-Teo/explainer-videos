"""Precompute every number in Part 41 of *Economics, Built* ("Taxes").

    python -m videos.economics.econ41.compute            # everything missing (about ten seconds)
    python -m videos.economics.econ41.compute --force top

Results are cached in ``.cache/econ41/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Piketty and Saez's top shares; from FRED, the IRS's top statutory rate since 1913 and
OMB's federal receipts and deficit as percentages of GDP; the tables of Laffer and Wanniski, Harberger, Fuest, Peichl
and Siegloch, Ramsey, Diamond and Mirrlees, Atkinson and Stiglitz, Mirrlees, Diamond, Saez, Diamond and Saez, Piketty,
Saez and Stantcheva, Feldstein, Gruber and Saez, Saez, Slemrod and Giertz, Kleven and Waseem, Chetty, Looney and
Kroft, Chamley, Judd, Straub and Werning, Zucman, Torslov, Wier and Zucman, the OECD, Allingham and Sandmo, Kleven et
al., Kleven, Landais and Saez, Mnuchin and the CBO).  Models: Agora's tax (``agora.tax``) with the Island's Part 41
truths.

Items:
    napkin       the Laffer curve for two elasticities of the base
    harberger    a tax on capital: workers' share of the burden against capital's mobility
    triangle     the Harberger triangle: revenue and deadweight loss against the rate
    top          the top rate: the Pareto parameter from the tax data, the formula, the top bracket's revenue
    ramsey       Ramsey's rates against a uniform rate raising the same revenue
    mirrlees     Diamond's schedule: the U-shaped marginal rates and their three factors
    eti          a century of top rates and top shares; the 1986 reform
    bunching     the Island's taxpayers at a kink, and the estimator
    evasion      Allingham and Sandmo: the declared share against the audit probability
    receipts     federal receipts as a share of GDP, 2010-2025
    film         the intermission's data film: the top income tax rate, 1913-2025
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import distribution
from explainer.economics.agora import tax as T
from explainer.economics.data import tables

CACHE = Cache("econ41")
load = CACHE.load
TRUTH = island.truths(41)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0
LAST_STATUTORY = (2025, 37.0)  # the top rate set in 2018 is still 37% in 2025 (FRED's IRS series ends in 2018)


def _annual(key: str) -> dict:
    d = data.fred(key)
    return {int(x[:4]): float(v) for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def top_rates() -> dict:
    r = _annual("IITTRHB")
    for y in range(max(r) + 1, LAST_STATUTORY[0] + 1):
        r[y] = LAST_STATUTORY[1]
    return r


def compute_napkin() -> dict:
    t = np.linspace(0, 1, 201)
    es = TRUTH["laffer"]["e"]
    return {"t": t.tolist(), "e": list(es), "rev": [T.laffer(t, e).tolist() for e in es],
            "peak": [T.laffer_peak(e) for e in es], "peak_rev": [float(T.laffer(T.laffer_peak(e), e)) for e in es]}


def compute_harberger() -> dict:
    H = TRUTH["harberger"]
    etas = np.concatenate([[0.0], np.exp(np.linspace(np.log(0.05), np.log(200), 80))])
    rows = [T.harberger(H["tau"], float(e), alpha=H["alpha"]) for e in etas]
    closed = T.harberger(H["tau"], 0.0, alpha=H["alpha"])
    opened = T.harberger(H["tau"], np.inf, alpha=H["alpha"])
    marks = {str(e): T.harberger(H["tau"], e, alpha=H["alpha"]) for e in H["eta"]}
    return {"eta": etas.tolist(), "share": [r["worker_share"] for r in rows],
            "per_revenue": [r["worker_per_revenue"] for r in rows], "closed": closed, "open": opened,
            "marks": marks, "tau": H["tau"], "alpha": H["alpha"], "fps": tables.HARBERGER_1962.data}


def compute_triangle() -> dict:
    P = TRUTH["triangle"]
    ts = np.linspace(0, 0.6, 61)
    rows = [T.triangle(float(t), P["eps_d"], P["eps_s"]) for t in ts]
    at = {str(t): T.triangle(t, P["eps_d"], P["eps_s"]) for t in (0.1, 0.2, 0.4)}
    return {"t": ts.tolist(), "rev": [r["revenue"] for r in rows], "dwl": [r["dwl"] for r in rows],
            "approx": [r["approx"] for r in rows], "at": at, **P}


def compute_mcpf() -> dict:
    out = {}
    for e in (0.25, 1.0):
        top = T.laffer_peak(e)
        t = np.linspace(0, top - 0.02, 120)
        out[str(e)] = {"t": t.tolist(), "m": T.mcpf(t, e).tolist(), "top": top,
                       "at": {str(x): float(T.mcpf(x, e)) for x in (0.2, 0.4, 0.6) if x < top - 0.01}}
    return out


def compute_top() -> dict:
    S = data.saez()
    k = S["year"].index(2022)
    a = distribution.pareto_alpha(S["top1"][k], S["top01"][k], 0.01, 0.001)
    Tp = TRUTH["top"]
    taus = np.linspace(0, 0.99, 100)
    curves = {str(e): T.top_revenue(taus, a, e).tolist() for e in Tp["e"]}
    rates = {str(e): T.top_rate(a, e) for e in Tp["e"]}
    rates_g = {str(g): T.top_rate(a, 0.25, g) for g in Tp["g"]}
    ds = tables.DIAMOND_SAEZ_2011.data
    return {"a": a, "taus": taus.tolist(), "curves": curves, "rates": rates, "rates_g": rates_g,
            "ds": ds, "ds_rate": T.top_rate(ds["a"], ds["e"]), "current": LAST_STATUTORY[1]}


def compute_ramsey() -> dict:
    R = TRUTH["ramsey"]
    r = T.ramsey(R["eps"], R["revenue"])
    return {**r, "goods": list(R["goods"]), "revenue": R["revenue"]}


def compute_mirrlees() -> dict:
    M = TRUTH["mirrlees"]
    D = T.diamond_schedule(M["e"], M["nu"], M["mu"], M["sigma"], M["alpha"], M["tail"])
    F, z = D["F"], D["z"]
    keep = np.unique(np.searchsorted(F, np.linspace(0.005, 0.9995, 240)))
    out = {"F": F[keep].tolist(), "z": z[keep].tolist(), "Tp": D["Tprime"][keep].tolist(), "B": D["B"][keep].tolist(),
           "C": D["C"][keep].tolist(), "A": D["A"], "top": D["top"], "e": M["e"], "alpha": M["alpha"],
           "a_income": D["a_income"]}
    zmed = float(np.interp(0.5, F, z))
    out["z_rel"] = (np.array(out["z"]) / zmed).tolist()
    tp = np.array(out["Tp"])
    i = int(np.argmin(tp))
    out["min"] = {"Tp": float(tp[i]), "F": float(out["F"][i]), "z_rel": float(out["z_rel"][i])}
    out["bottom"] = float(tp[0])
    out["at"] = {str(q): float(np.interp(q, F, D["Tprime"])) for q in (0.1, 0.5, 0.9, 0.99, 0.999)}
    return out


def compute_eti() -> dict:
    S = data.saez()
    r = top_rates()
    ys = [y for y in S["year"] if y in r]
    top1 = dict(zip(S["year"], S["top1"]))
    k = {y: S["year"].index(y) for y in (1985, 1986, 1987, 1988)}
    imp = np.log(top1[1988] / top1[1986]) / np.log((1 - r[1988] / 100) / (1 - r[1986] / 100))
    m = [y for y in ys if 1960 <= y <= 2022]
    b = np.polyfit(np.log([1 - r[y] / 100 for y in m]), np.log([top1[y] for y in m]), 1)
    return {"years": ys, "rate": [r[y] for y in ys], "top1": [top1[y] for y in ys], "r1986": r[1986],
            "r1988": r[1988], "s1986": top1[1986], "s1988": top1[1988],
            "s1986_kg": S["top1_kg"][k[1986]], "s1987_kg": S["top1_kg"][k[1987]], "tra86": float(imp),
            "naive": float(b[0]), "studies": tables.ETI_STUDIES.data, "rate_by_year": {str(y): r[y] for y in
                                                                                         (1913, 1918, 1944, 1963,
                                                                                          1964, 1982, 1988, 1993,
                                                                                          2003, 2013, 2018)}}


def compute_bunching() -> dict:
    B = TRUTH["bunching"]
    r = T.bunching(n=B["n"], e=B["e"], z_star=B["z_star"], t0=B["t0"], t1=B["t1"], friction=B["friction"],
                   seed=B["seed"])
    noisy = T.bunching(n=B["n"], e=B["e"], z_star=B["z_star"], t0=B["t0"], t1=B["t1"], friction=0.05,
                       seed=B["seed"], window=5.0)
    return {**r, "noisy_e_hat": noisy["e_hat"], "noisy_h": noisy["h"], "noisy_cf": noisy["cf"]}


def compute_evasion() -> dict:
    E = TRUTH["evasion"]
    ps = np.linspace(0.0, 0.6, 61)
    d = [T.allingham_sandmo(float(p), E["t"], E["theta"], E["rho"]) for p in ps]
    first = float(ps[next(i for i, v in enumerate(d) if v > 0)])
    full = float(ps[next(i for i, v in enumerate(d) if v >= 0.999)])
    at = {str(p): T.allingham_sandmo(p, E["t"], E["theta"], E["rho"]) for p in (0.01, 0.05, 0.2, 0.3)}
    return {"p": ps.tolist(), "declared": d, "first": first, "full": full, "at": at, **E,
            "dk": tables.EVASION.data}


def compute_receipts() -> dict:
    r = _annual("FYFRGDA188S")
    d = _annual("FYFSGDA188S")
    ys = [y for y in range(2010, 2026) if y in r]
    return {"years": ys, "receipts": [r[y] for y in ys], "deficit": [d[y] for y in ys], "r2017": r[2017],
            "r2018": r[2018], "r2019": r[2019], "cbo": tables.TCJA_2017.data}


def compute_score() -> dict:
    """Scoring a change in the top rate from 37%: the static estimate (incomes unchanged) against one with the
    elasticity's response, per top taxpayer, in units of the threshold (incomes above it Pareto with the 2022 a)."""
    a = compute_top()["a"]
    t0 = LAST_STATUTORY[1] / 100
    out = {}
    for t1 in (0.40, 0.30):
        static = (t1 - t0) * (a / (a - 1) - 1)
        dyn = {}
        for e in (0.25, 1.0):
            r0 = float(T.top_revenue([t0], a, e, tau0=t0)[0])
            r1 = float(T.top_revenue([t1], a, e, tau0=t0)[0])
            dyn[str(e)] = r1 - r0
        out[f"{t1:.2f}"] = {"static": static, "dynamic": dyn}
    return {"a": a, "t0": t0, "cases": out}


def film_time(t: float, first: float = 1913.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    r = top_rates()
    ys = sorted(r)
    v = [r[y] for y in ys]
    k = int(np.argmax(v))
    return {"t": ys, "v": v, "times": [film_time(y) for y in ys], "peak": v[k], "peak_y": ys[k], "first": v[0],
            "last": v[-1], "y1963": r[1963], "y1982": r[1982], "y1988": r[1988]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=8, log=False, low=40, high=84)
    events = {"film_end": film_time(2025) + 6.0, "first": times[0], "peak": film_time(f["peak_y"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the top statutory rate of the US individual income tax, 1913-2025 (IRS, via FRED; "
                               "37% since 2018), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ41").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "napkin": compute_napkin,
    "harberger": compute_harberger,
    "triangle": compute_triangle,
    "mcpf": compute_mcpf,
    "top": compute_top,
    "ramsey": compute_ramsey,
    "mirrlees": compute_mirrlees,
    "eti": compute_eti,
    "bunching": compute_bunching,
    "evasion": compute_evasion,
    "receipts": compute_receipts,
    "score": compute_score,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
